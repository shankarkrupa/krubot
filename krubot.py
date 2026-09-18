#!/usr/bin/env python3
"""Interactive OpenAI-compatible chat client with Markdown-defined tools.

The program intentionally writes only the final assistant response to the
conversation output. Tool stdout and stderr are captured and returned to the
model as tool messages.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "http://NASSERVER3:PORT/v1"
DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_MAX_TOOL_OUTPUT_CHARS = 12_000
MAX_TOOL_ROUNDS = 20
SYSTEM_PROMPT = (
    "You are a helpful assistant. You may use the provided tools when they are "
    "useful. After using a tool, answer the user using the tool result. Never "
    "claim that a tool succeeded unless its result confirms that it did."
    "Read the .md files inside the 'skills' folder to learn how to use the available tools. Remember to save your learnings here when needed."
    "Use the only the 'working' folder if any temporary files are to be created for processing information"
)


class ConfigurationError(Exception):
    """Raised when a Markdown tool definition is invalid."""


class LLMRequestError(Exception):
    """Raised when the OpenAI-compatible endpoint cannot be called."""


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: str

    def as_openai_tool(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


@dataclass
class ToolContext:
    confirm_commands: bool
    default_timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    max_output_chars: int = DEFAULT_MAX_TOOL_OUTPUT_CHARS


def _section(markdown: str, heading: str) -> str:
    """Return the body of a level-two Markdown heading."""
    pattern = rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, markdown)
    return match.group(1).strip() if match else ""


def _all_sections(markdown: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?ms)^##\s+(.+?)\s*$\n(.*?)(?=^##\s+|\Z)", markdown))
    return [(match.group(1).strip(), match.group(2).strip()) for match in matches]


def _json_code_block(section: str, path: Path) -> dict[str, Any]:
    match = re.search(r"(?s)```(?:json)?\s*(.*?)\s*```", section)
    if not match:
        raise ConfigurationError(f"{path}: Parameters must contain a JSON code block")
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"{path}: invalid parameter JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigurationError(f"{path}: parameters must be a JSON object")
    return value


def _single_value(section: str, path: Path, field_name: str) -> str:
    value = section.strip().strip("`").strip()
    if not value:
        raise ConfigurationError(f"{path}: missing {field_name}")
    return value


def load_tool_definitions(tools_dir: Path) -> list[ToolDefinition]:
    """Load every ``*.md`` tool definition from a directory."""
    if not tools_dir.is_dir():
        raise ConfigurationError(f"Tool directory does not exist: {tools_dir}")

    definitions: list[ToolDefinition] = []
    seen_names: set[str] = set()
    for path in sorted(tools_dir.glob("*.md")):
        markdown = path.read_text(encoding="utf-8")
        name_match = re.search(r"(?m)^#\s+Tool:\s*([A-Za-z0-9_-]+)\s*$", markdown)
        if not name_match:
            raise ConfigurationError(f"{path}: expected '# Tool: tool_name'")

        name = name_match.group(1)
        if name in seen_names:
            raise ConfigurationError(f"{path}: duplicate tool name: {name}")
        seen_names.add(name)

        description = _single_value(_section(markdown, "Description"), path, "Description")
        guidance_sections = [
            f"{heading}:\n{body}"
            for heading, body in _all_sections(markdown)
            if heading.lower() not in {"handler", "parameters", "adding more tools"} and body
        ]
        description = "\n\n".join(guidance_sections) or description
        handler = _single_value(_section(markdown, "Handler"), path, "Handler")
        parameters = _json_code_block(_section(markdown, "Parameters"), path)
        if parameters.get("type") != "object":
            raise ConfigurationError(f"{path}: Parameters JSON must have type 'object'")
        definitions.append(ToolDefinition(name, description, parameters, handler))

    if not definitions:
        raise ConfigurationError(f"No Markdown tool definitions found in {tools_dir}")
    return definitions


def _bounded_text(value: str, maximum: int) -> str:
    if len(value) <= maximum:
        return value
    omitted = len(value) - maximum
    return f"{value[:maximum]}\n\n[tool output truncated; {omitted} characters omitted]"


def _ask_for_command(command: str) -> bool:
    try:
        answer = input(f"Allow shell command `{command}`? [y/N] ")
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer.strip().lower() in {"y", "yes"}


def execute_shell_command(arguments: dict[str, Any], context: ToolContext) -> str:
    command = arguments.get("command")
    if not isinstance(command, str) or not command.strip():
        return json.dumps({"ok": False, "error": "command must be a non-empty string"})

    if context.confirm_commands and not _ask_for_command(command):
        return json.dumps({"ok": False, "cancelled": True, "error": "user denied command"})

    cwd = arguments.get("cwd")
    if cwd is not None and not isinstance(cwd, str):
        return json.dumps({"ok": False, "error": "cwd must be a string when provided"})

    timeout = arguments.get("timeout_seconds", context.default_timeout_seconds)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        return json.dumps({"ok": False, "error": "timeout_seconds must be a positive number"})
    timeout = min(float(timeout), 900.0)

    try:
        print(f"Executing {command}")
        completed = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        result = {
            "ok": completed.returncode == 0,
            "exit_code": completed.returncode,
            "stdout": _bounded_text(completed.stdout, context.max_output_chars),
            "stderr": _bounded_text(completed.stderr, context.max_output_chars),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        result = {
            "ok": False,
            "timed_out": True,
            "timeout_seconds": timeout,
            "stdout": _bounded_text(stdout, context.max_output_chars),
            "stderr": _bounded_text(stderr, context.max_output_chars),
        }
    except (OSError, ValueError) as exc:
        result = {"ok": False, "error": str(exc)}

    return json.dumps(result, ensure_ascii=False)


HANDLERS: dict[str, Callable[[dict[str, Any], ToolContext], str]] = {
    "shell_command": execute_shell_command,
}


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int) -> None:
        self.endpoint = self._make_endpoint(base_url)
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    @staticmethod
    def _make_endpoint(base_url: str) -> str:
        print(base_url)
        endpoint = base_url.rstrip("/")
        if not endpoint.endswith("/chat/completions"):
            endpoint += "/chat/completions"
        return endpoint

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "messages": messages}
        if tools:
            payload["tools"] = tools

        request = Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LLMRequestError(f"LLM endpoint returned HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise LLMRequestError(f"Could not reach LLM endpoint: {exc.reason}") from exc
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMRequestError("LLM endpoint returned invalid JSON") from exc
        if not isinstance(data, dict):
            raise LLMRequestError("LLM endpoint returned a JSON value instead of an object")
        return data


def _tool_call_arguments(tool_call: dict[str, Any]) -> dict[str, Any]:
    function = tool_call.get("function")
    if not isinstance(function, dict):
        raise ValueError("tool call has no function object")
    raw_arguments = function.get("arguments", "{}")
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if not isinstance(raw_arguments, str):
        raise ValueError("tool arguments must be a JSON object")
    parsed = json.loads(raw_arguments)
    if not isinstance(parsed, dict):
        raise ValueError("tool arguments must decode to a JSON object")
    return parsed


def run_turn(
    client: OpenAICompatibleClient,
    messages: list[dict[str, Any]],
    definitions: dict[str, ToolDefinition],
    context: ToolContext,
) -> str:
    openai_tools = [definition.as_openai_tool() for definition in definitions.values()]
    for _ in range(MAX_TOOL_ROUNDS):
        response = client.complete(messages, openai_tools)
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMRequestError("LLM response did not contain any choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise LLMRequestError("LLM response choice did not contain a message")

        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            messages.append(message)
            content = message.get("content")
            if content is None:
                return ""
            if not isinstance(content, str):
                return json.dumps(content, ensure_ascii=False)
            return content

        messages.append(message)
        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                continue
            call_id = str(tool_call.get("id", "unknown"))
            function = tool_call.get("function")
            tool_name = function.get("name") if isinstance(function, dict) else None
            definition = definitions.get(tool_name) if isinstance(tool_name, str) else None
            if definition is None:
                result = json.dumps({"ok": False, "error": f"unknown tool: {tool_name}"})
            else:
                handler = HANDLERS.get(definition.handler)
                if handler is None:
                    result = json.dumps(
                        {"ok": False, "error": f"unsupported tool handler: {definition.handler}"}
                    )
                else:
                    try:
                        result = handler(_tool_call_arguments(tool_call), context)
                    except (ValueError, json.JSONDecodeError) as exc:
                        result = json.dumps({"ok": False, "error": f"invalid tool arguments: {exc}"})
                    except Exception as exc:  # Keep the tool loop alive for model-visible failures.
                        result = json.dumps({"ok": False, "error": f"tool failed: {exc}"})
            messages.append({"role": "tool", "tool_call_id": call_id, "content": result})

    raise LLMRequestError(f"tool call limit exceeded ({MAX_TOOL_ROUNDS})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interactive OpenAI-compatible LLM chat")
    parser.add_argument("--base-url", default=os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument(
        "--api-key",
        default=os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"),
        help="API key; defaults to LLM_API_KEY or OPENAI_API_KEY",
    )
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", "qwen354b-128k"))
    parser.add_argument(
        "--tools-dir",
        type=Path,
        default=Path(__file__).with_name("tools"),
        help="directory containing Markdown tool definitions",
    )
    parser.add_argument("--no-confirm", action="store_true", help="run shell commands without prompting")
    parser.add_argument("--request-timeout", type=int, default=120)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print("Set LLM_API_KEY or OPENAI_API_KEY before starting.", file=sys.stderr)
        return 2
    if args.request_timeout <= 0:
        print("--request-timeout must be positive.", file=sys.stderr)
        return 2

    try:
        loaded_definitions = load_tool_definitions(args.tools_dir)
    except (OSError, ConfigurationError) as exc:
        print(f"Tool configuration error: {exc}", file=sys.stderr)
        return 2

    definitions = {definition.name: definition for definition in loaded_definitions}
    client = OpenAICompatibleClient(args.base_url, args.api_key, args.model, args.request_timeout)
    context = ToolContext(confirm_commands=not args.no_confirm)
    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"Interactive chat using {args.model}. Type /help for commands; /exit to quit.")
    while True:
        try:
            prompt = input("\033[95mYou:\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not prompt:
            continue
        if prompt in {"/exit", "/quit", "exit"}:
            break
        if prompt == "/help":
            print("Enter a prompt. /reset clears conversation history. /exit quits.")
            continue
        if prompt == "/reset":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation reset.")
            continue

        messages.append({"role": "user", "content": prompt})
        try:
            answer = run_turn(client, messages, definitions, context)
        except LLMRequestError as exc:
            messages.pop()
            print(f"Request failed: {exc}", file=sys.stderr)
            continue
        print(f"\033[92mAssistant:\033[0m {answer}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

