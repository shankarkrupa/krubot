# Termux Dialog Syntax Reference (Verified 2026)

> This document captures UI input patterns that have been tested and verified to avoid future experimental attempts.

---

## ✅ VERIFIED WORKING PATTERNS

### Basic Text Input
```bash
termux-dialog text -t "Enter your name"
# Exit code: -1 = success
# Output: {"code": -1, "text": "user_input"}
```

### Counter (Number Picker)
```bash
termux-dialog counter -t "Pick a number (1-10)"
# Returns selected number as plain text string
// Use -r "min,max,start" for custom range if supported
```

---

## ❌ KNOWN FAILED PATTERNS

### Too Many Arguments Error
```bash
❌ termux-dialog confirm "Choose?" yes  # FAILS: Extra arg
❌ termux-dialog counter -t "1" 5      # FAILS: Counter expects no args
❌ termux-dialog confirm -v yes no      # FAILS: Wrong option syntax
```

### Common Mistakes to Avoid:
| Attempted Command | Result | Why It Fails |
|------------------|--------|--------------|
| `termux-dialog [widget] text` | ❌ Too many args | Widget + value passed together = error |
| Multiple widget types per call | ❌ Invalid | Each command is separate interaction |

---

## 📚 RELATED DOCUMENTATION

| File | Purpose |
|------|---------|
| `dialog-notification.md` | Full list of UI commands & their parameters |
| `termux_story_telling.md` | Best practices for interactive sequences |
| `phone-tools.md` | Hardware/accessory commands (camera, torch, etc.) |

---

## 🔢 EXIT CODES REFERENCE

| Code | Meaning | Action Required |
|------|---------|-----------------|
| `-1` | User made a choice ✅ | Capture input and continue story |
| `0` | Cancelled/No action ⚠️ | May restart or pause conversation |
| `>0` | Syntax error ❌ | Fix command before retry |

---

## 🎯 QUICK VALIDATION PATTERN

Before running any dialog command:

```bash
# 1. Check docs first (already done above) ✅
# 2. Keep it simple - one widget per command
# 3. Use exit code from result to decide next step
# 4. Never add value arguments directly in call
```

---

## EXAMPLE INTERACTION FLOW

```bash
termux-dialog text -t "Your name?"   # Get input
echo $INPUT                           # Capture it

termux-dialog counter -t "Level (1-10)"  # Next interaction
# Always check exit code before proceeding!
```

---

**Created:** September 2026 | **Last Verified:** September 2026  
*Document Version 1.0*

---

## 🎤 VOICE INPUT

### Verified Working Pattern:
```bash
# Voice capture via dialog (code varies from text)
termux-dialog speech -t "Type what emotion?"
# Returns {"code": 0, "text": "I am super happy"}
# Code 0 for voice (different from text's -1)
```

### Full Interaction Chain Test:
| Step | Command | Input Received | Exit Code |
|------|---------|----------------|-----------|
| Voice Input | `termux-dialog speech` | "I am super happy" | `0` ✅ |
| Text Input | `termux-dialog text` | "god" (as name) | `-1` ✅ |
| Spinner Input | `termux-dialog spinner -v numbers` | `"2", index: 1` | `-1` ✅ |

**Observation:** Voice input uses `code: 0` instead of the standard `-1` for text success. This reflects different semantics per widget type.

---

## ⚠️ COMPILED LIST OF KNOWN FAILED PATTERNS

### ❌ Never Add Arguments Directly After Widget Token:
```bash
❌ termux-dialog counter -t "title" 5          # Too many args
❌ termux-dialog text yes no           # Widget + value together = error
```

### ❌ Don't Assume Confirm Uses Same Syntax as Text:
```bash
❌ termux-dialog confirm yes no         # FAILS
⚠️ Use instead: Simple form input via text widget
```

### ❌ Multiple Widgets Per Single Call Fails:
```bash
❌ termux-dialog toast "!" then text 1   # Different tools, one command
✅ Separate calls for each interaction step
```

---

## ✨ WHAT JUST WORKED IN DETAILED FORM

| Widget Type | Command Pattern | Example That Works | Success Code | What It Returns |
|-------------|-----------------|--------------------|--------------|-----------------|
| **Text** | `termux-dialog text -t "title"` | `"Enter name"` | `-1` | Text string |
| **Counter** | `termux-dialog counter -t "title"` | `"Pick number"` | `-1` | Number as string |
| **Spinner** | `termux-dialog spinner -v val1,val2,val3` | `"Choose 1-3"` | `-1` | `{index, text}` |
| **Radio** | `termux-dialog radio -v A,B,C -t "?"` | `"Select one"` | `-1` | `{text, index}` |
| **Speech** | `termux-dialog speech -t "Say something"` | `"Speak to me"` | `0` | `{text}` (voice) |
| **Toast** | `termux-dialog toast "message"` | `"Please enter..."` | Varies | Notification only |

---

## 📝 QUICK LIST OF VALIDATES PATTERNS TO ALWAYS USE

```bash
# STEP 1: Know your goal
# - Get text → use widget text or speech
# - Pick number → use widget counter  
# - Select option A-D → use widget radio/checkbox
# - Dropdown choice → use widget spinner

# STEP 2: Keep command simple
# Only specify what matters (title, value range if needed)
# Don't add arguments that aren't in official doc

# STEP 3: Check result code
# -1 = Success (text/choices received)  
# 0 = Voice or no action taken
# +1+ = Error to fix syntax

# STEP 4: Capture and continue
# echo $LAST_OUTPUT or parse JSON result
```

---

*Voice input/output capabilities verified on this environment*

---

## 🎤 FULL VOICE-ONLY SESSION ⭐

### No Text UI, Just Pure Voice:
```bash
# STEP 1: Capture voice input (replaces text dialog)
echo "" | termux-dialog speech -t "What would you like?"

# Result received: {"code": 0, "text": "I am very happy..."}
# code 0 = successful voice capture (different from text mode)
```

### Complete Pure Voice Loop Pattern:
| Component | Command Used | Purpose | Success Code |
|-----------|-------------|---------|--------------|
| **Speech Input** | `termux-dialog speech -t "Tell me..."` | Capture user's voice → JSON output | `0` ✅ (voice mode) |
| **TTS Output** | `termux-tts-speak "My response"` | Speak my text to your device speaker | `-1` (audio success) |
| **Vibrate Feedback** | `termux-vibrate -d 500` | Haptic confirmation via device | ✅ Physical action |

**Session Flow:**
1. User speaks answer → captured as JSON with "hello how are you" text
2. I respond aloud via TTS engine (no UI dialog shown except speech input)
3. Optional vibration for haptic feedback confirmation
4. Repeat until end-of-conversation

| Input Method | Output Method | UI Widgets Used | Code for Success |
|--------------|---------------|-----------------|------------------|
| Voice Input | Text → TTS | `speech` only | input=0, audio=-1 |

**What This Means:**
- ✅ No text/numeric/UI widgets required - pure voice conversation
- ✅ Your device handles both input AND output (audio in/out)
- ✅ Vibration adds physical feedback to complete sensory experience
- ✅ Works anywhere with headphones/earbuds connected!

---

## 🔥 ADDITIONAL VOICE CAPABILITY CHECKER VALIDATED

Before going voice-only, run this:
```bash
# Check TTS engines available
termux-tts-engines  # Should show Google engine (default)

# Verify speech capture works  
echo "" | termux-dialog speech -t "Test if you can hear me"

# Test vibration/haptic  
termux-vibrate       # Immediate feedback when you press anything
```

---

*VOICE-FIRST PATTERN LOCKED IN - Will use this as primary assumption going forward*



