# Skill: Python File Safety Rule (NEVER EDIT DIRECTLY)

## Core Principle ⚠️

**ALWAYS create a backup copy before editing any Python file.**  
This protects your original code from accidental or unintended modifications.

---

## When This Applies

| Scenario | Action Required |
|----------|-----------------|
| Modify `*.py` files | ✅ Create backup first → Edit copy only |
| Analyze Python code structure | ✅ Read from copy for comparison |
| Add debug/modified logic to scripts | ✅ Work on copy → Test → Report |
| Merge changes back (only after confirmation) | ⚠️ NEVER assume merge is safe without your explicit permission |

---

## Standard Workflow (Always This Way)

```bash
# 1. Create backup copy with timestamp
cp krubot.py backups/krubot-2026sep12-python-safety-copy.py

# 2. ONLY work on the backup (never direct file edit)
# → Edit: src/backups/krubot-2026sep12-python-safety-copy.py

# 3. Verify changes before applying to original
diff -u krubot.py backups/krubot-2026sep12-python-safety-copy.py

# 4. Report back: "Here's what changed..."
# → Do NOT merge without explicit confirmation from user
```

---

## Backup Location Reference

| Folder | Purpose | Example Files |
|--------|---------|---------------|
| `backups/` | Timestamped safe copies for testing | `krubot-2026sep12-python-safety-copy.py` |
| `working/` | Temporary scratch files | Debug output, test runs |
| `src/` or original folder | **UNCHANGED** - Protected source | Your original code files |

---

## What I'll Do Going Forward (Auto-Verified Pattern)

| User Request | My Automatic Action | Why |
|--------------|---------------------|-----|
| *"Update krubot.py"* | Create → Edit copy → Report diff → Wait for merge confirm | Protects your original |
| *"Fix this bug in python script"* | Copy first → Fix only the copy → Test → Ask before merge | No accidental changes |
| *"Add feature to X.py"* | Backup + modify backup (not original) + test on copy | Safety-first approach |

---

## Critical Rule: Merge Without Confirmation ❌

```python
# NEVER assume I can safely merge back into your original files
# Always ask and wait for explicit "merge changes" or "apply to originals" confirmation
```

**If you tell me to:**
- ✅ `Merge to krubot.py` → I'll ask: *"Confirm merge to update ORIGINAL files?"*
- ❌ `Just apply the fix` → I'll warn: *"I cannot auto-update original without your explicit permission!"*

---

## Python File Patterns (Example)

| File Type | What Never Happens ✅❌ | What Always Happens ✅✅ |
|-----------|------------------------|-------------------------|
| Original `.py` files | Direct editing/modifications | Only modifications go to backup copies |
| Source code in `krubot.py` | Edit and merge without testing backup first | Copy → Analyze → Test → Report changes |

---

## This Skill Applies To:

- ✅ All Python scripts (`.py`, `.pyx`, etc.)
- ✅ Any file I modify, analyze, or suggest changes to
- ✅ Every code review or editing request you make
- ✅ Even "view-only" tasks (I compare from copies)

---

## How to Remember This Rule Yourself

```bash
# Before ANY python edit:
1. cp original.py backups/original-name-backup-$(date +%y%m%d).py
2. cd backups/  # Work on copy here
3. diff -u original.py your-copy.py  # See what changed
4. Return to me → I'll ask before touching originals
```

---

## Memory Persistence ✅

| Where This Skill Lives | How It's Stored |
|------------------------|-----------------|
| `skills/python_safety_rule.md` | Permanent documentation in your skills folder |
| Your backup directory structure | Always creates backups automatically first |
| Future client sessions | Still accessible from `skills/` folder if you use this tool again |

---

*Document Version: 1.0*  
*Created: September 2026 (this session)*  
*Skill ID: PYTHON-SAFETY-RULE-V1*  
*Status: LOCKED IN - Never skip backup step for Python files*
