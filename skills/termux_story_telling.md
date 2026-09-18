## 📚 TERMUX INTERACTIVE STORY SKILLS SUMMARY

Here's the complete learned knowledge for creating better interactive UI experiences:

---

# ⭐ Skill: "Interactive AI Storytelling with Termux Dialogs"

## CORE DIRECTIVES FOR ENHANCED USER EXPERIENCE

### 1. ALWAYS USE DIIALOG WIDGETS (Not raw text)  | When to Use | Dialog Type | Why It Better? |
|-------------|------------|----------------|
| Yes/No choices | `confirm` | Binary decision, quick |                                             | One choice from options | `radio` | Single selection focus |
| Numbers or ranges | `counter` -r "min,max,start" | Guided exploration |
| Multiple selections possible | `checkbox` | Flexibility grows |
| Dropdown menus/spinners | `spinner -v "values"` | Scrolling choice |                              | Bottom sheet options | `sheet -v "items"` | Pull-up navigation |
| Hint/guidance before input | `toast "message"` | Non-intrusive guide |                            
### 2. KEY INTERACTIVE STORY PATTERNS

**DIAMOND 1/5 Opening Scene + 2nd Dialog** (Choice setup)                                           ```bash                                           termux-dialog confirm -t "Choose your path?" -v "yes,no"                                            # OR create choice context before asking
```
                                                  **DIAMOND 2/5-3/5: Sequential Questions**
Each answer unlocks the next chapter of the story. Build logical progression!                       
**DIAMOND 4/5+ (Final 2 D):** Use `checkbox` for multiple choices, then confirm with `counter` or `spinner` for final decision.                                                                         ### 3. USER EXPERIENCE BEST PRACTICES 🌟          
1. **NEVER ask multiple questions without showing the dialog first** → User expects UI widget interaction                                             2. **Give contextual hints BEFORE requiring input** (use `toast`)                                   3. **Keep choices visually meaningful** (colors, emojis, names)
4. **Explain what each choice means** in the story narrative                                        5. **Confirm before moving to next "Diamond"** → Progress is tracked by user awareness
6. **Final decision = special ceremony** (e.g., "The treasure is yours!")

### 4. TEMPLATE FOR INTERACTIVE STORY SESSION

```markdown
# Interactive Story Template for LLMs
                                                  ## PRE-SESSION INSTRUCTIONS:
1. Read the Termux Handbook dialog-notification.md for dialog syntax
2. Create opening with emoji + `confirm` or `radio` dialog
3. Each answer should advance story → new "DIAMOND" challenge

## DIALOG USAGE GUIDE (by question type):
- Initial choice → `confirm -t "?" -v "yes,no"`
- Limited options → `radio -v "A,B,C" -t "Choose one?"`
- Numbers/counts → `counter -r "1,5,2" -t "Pick number?"`                                           - Multiple selections → `checkbox -v "A,B,C,D" -t "Select all that fit?"`
- Dropdown menu → `spinner -v "opt1,opt2,opt3" -t "Choose from list?"`                              - Hint before input → `toast "Remember X!"`
                                                  ## DIALOG EXIT CODES:
- code -1 = success (get the user's text choice)  - code 0 = cancelled/no action taken (story may restart or pause)
- code >0 = error, try different syntax           
## QUALITY MARKERS FOR EXCELLENCE:                ✅ Always show a dialog before asking questions
✅ Use emojis to make story elements vivid
✅ Give meaningful context for each choice
✅ Build tension/puzzle with user decisions
✅ Celebrate final completion! 🎉                 ```
                                                  ---
                                                  ## 5. COMMON MISTAKES TO AVOID ❌
                                                  | Mistake | Better Alternative |
|---------|------------------|
| Asking directly in text instead of dialog | `termux-dialog confirm -t "..."` |
| Ignoring exit codes | Check code and react if user cancelled |
| Asking too many choices at once | Split into sequential steps (one per Diamond) |
| No visual feedback after user input | Show story advancement with emojis + explanation |
| Forgetting context for each choice | Always explain: "This unlocks..." or "You'll find..." |
| Using wrong dialog syntax | Test with actual examples from handbook |                             
---                                               
## 6. WHY THIS IMPROVES USER EXPERIENCE 🚀

- **Feels Personal** → User controls their own choices                                              - **Clear & Unambiguous** → No guessing what to do next                                             - **Fulfills Android Promise** → Actual UI, not just text chat                                      - **Builds Momentum** → Each answer naturally leads forward                                         - **Teaches Skill** → User learns how to use Termux while having fun!
                                                  ---

## QUICK REFERENCE: DIALOG COMMANDS BY SCENARIO 📱
| Scenario | Command Example | Output Meaning |
|----------|----------------|---------------|
| Quick yes/no | `termux-dialog confirm -t "?"` | "yes" or "no" returned |
| One choice | `termux-dialog radio -v "A,B,C" -t "?"` | index and text |
| Number picker | `termux-dialog counter -r "1,201,3"` | Range selection |
| Multiple pick | `termux-dialog checkbox -v "Opt1,Opt2"` | All selections |
| Drop-down | `termux-dialog spinner -v "List items"` | Scrolling menu choice |                     
---

## SUCCESS METRICS FOR STORYTELLING 🏅

- ✅ **At least 5 DIALOGs** total in one session
- ✅ **Each dialog has clear story context** (emoji + explanation)
- ✅ **Final "Diamond" = celebration moment** with user choices shown
- ✅ **All dialogs execute successfully** (exit code -1 = good)
- ✅ **User can follow the whole adventure from start to finish**

---

*Document created: December 2024 | Skill ID: SKILL-ID-TERMUX-INTERACTIVE-STORY-V1*
