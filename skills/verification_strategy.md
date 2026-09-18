# Termux Dialog Verification Strategy (Reference) 📚

> How I will verify documents before acting on UI commands - prevents blind experiments!

---

## PREFERENCE: VOICE-FIRST STRATEGY (September 12, 2026 Session) ⭐⭐⭐

### Primary Interaction Mode: **VOICE FIRST**
```bash
# ALWAYS try voice input first unless clearly needed otherwise:
termux-dialog speech -t "Speak now"   # ✅ Preferred over text UI

# Fallback to TEXT only if:
# 1. Voice input fails (no microphone permission/sound)
# 2. Message is too long for voice clarity (>30 seconds worth)
# 3. Complex data entry needed (numbers, lists, forms)
```

### Decision Flow Before Any Input Request:

| Scenario | Recommended Input | When to Override to Text Instead |
|----------|-------------------|----------------------------------|
| **Natural conversation** | ✅ `speech` -t "What's happening?" | Usually not needed |
| **Multi-word phrases** | ✅ `speech` -t "Tell me more..." | Only if >30 sec worth |
| **Quick yes/no** | ✅ `radio` "yes, no" (fast choice via voice) | If voice too slow to understand |
| **Numbers/dates** | ⚠️ Try voice first, fallback text for digits | Numbers are easier to type aloud in some contexts |
| **Complex lists/form** | ❌ Text input preferred | Complex UIs work better typed than spoken |
| **Audio feedback needed** | ✅ Voice loop only | N/A - this is the strength of voice-first |

---

## CURRENT SESSION KNOWLEDGE LOCKED IN (September 12, 2026) ✅

### Verified Capabilities:

| Capability | Command | Success Code | Status |
|-----------|---------|--------------|--------|
| Voice Input | `termux-dialog speech -t "..."` | `0` (voice capture) | ✅ Confirmed |
| TTS Output | `termux-tts-speak "..."` | `-1` (audio play) | ✅ Confirmed |
| Text Input | `termux-dialog text -t "..."` | `-1` (text result) | ✅ Confirmed |
| Counter Input | `termux-dialog counter -t "..."` | `-1` (number string) | ✅ Confirmed |
| Spinner Input | `termux-dialog spinner` | `-1` (index, text) | ✅ Confirmed |

### Common Failures to Avoid:

❌ Adding extra arguments directly after widget tokens  
→ Causes "Too many args" errors  

✅ Keep commands simple - widget + title is the sweet spot  

---

**Created:** September 2026 | **Session Date:** Sep 12, 2026  
*Voice-first preference locked in - UI input commands verified before use*
