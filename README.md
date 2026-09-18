# krubot
Knowledge Reinforced Utility Bot

A simple handy assistant/harness that works by executing commands and processing the results in Termux/Android environments

# Interactive OpenAI-Compatible Tool Chat

`krubot.py` starts an interactive chat session against any endpoint that
implements the OpenAI Chat Completions request shape. It uses only Python's
standard library, so it can run on Linux, Android Termux, and Windows without
installing a package.

## Setup

Set the endpoint credentials in the environment. `LLM_BASE_URL` should be the
API root, such as `https://api.openai.com/v1`; a URL that already ends in
`/chat/completions` is also accepted.

# In Termux - defaults to executing commands without approval
```sh
sh krubot.sh
```

The client also accepts `OPENAI_API_KEY` as a fallback. A compatible local
server can use an empty or placeholder key if it requires an Authorization
header:

```sh
python krubot.py --base-url http://localhost:1234/v1 --model local-model --api-key local
```

## Interactive commands

Type prompts at `You:`. Type `/reset` to clear the conversation or `/exit` to
quit. The assistant may call the configured tools in one turn and receives
their results before producing its answer.

Shell commands require an approval prompt by default. To disable that prompt
for a trusted environment, use `--no-confirm`. Tool stdout and stderr are
captured and sent to the LLM; they are not printed as tool output. Only the
assistant's final response is printed.

```sh
python krubot.py --no-confirm
```

## Markdown tool definitions

Tool definitions live in `tools/*.md`. Each file must provide:

1. `# Tool: tool_name`
2. `## Handler` containing a handler key
3. `## Description` containing the model-facing description
4. `## Parameters` containing an object-shaped JSON Schema code block

The loader discovers every Markdown file at startup, converts the definitions
to OpenAI function tools, and exposes them to the model. To add a tool, create
another Markdown definition, implement a validated Python handler, and register
it in `HANDLERS` in `krubot.py`. The initial `tools/shell_command.md` contains
the full shell-tool contract, portability notes, safety guidance, examples, and
the extension instructions.

The model can request a maximum of 20 tool rounds for one user prompt. Shell
output is bounded before it is added to the conversation so a command cannot
consume the entire model context, configurable through the `MAX_TOOL_ROUNDS` variable in krubot.py.

## Endpoint compatibility

The endpoint receives a JSON POST like:

```json
{
  "model": "gpt-4o-mini",
  "messages": [],
  "tools": []
}
```

The response must provide `choices[0].message`, including standard
`tool_calls` entries when it wants to run a tool. This supports OpenAI-style
providers and local servers that implement the same Chat Completions format.

## About/Background
I created this primarily because popular harnesses and assistants I tried did not install in my mobile. My mobile has a 32-bit OS and armv8a processor and a lot of Python packages of late and utilities target 64-bit system. This tool was initially my attempt to bridge the gap I had in my mobile for a few quick tasks - quick productivity areas like parsing bank statements to prepare to paste in my budget-expense spreadsheet, quick research of information and summarize from web/SearXNG, backing up files in my mobile to my local NAS server and so on. I kept asking this assistant, "What did you learn from your work now" and started saving most of my sessions as a skill - though a lot of them made sense to be a tool. Nonetheless, I am sharing those in case this would be of help to someone - at least for me when I figure out a better tool or buy a better phone. :-)


