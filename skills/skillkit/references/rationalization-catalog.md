# Rationalization Catalog

Use this file to convert observed agent excuses into explicit counters inside `SKILL.md`.

## How to Use

1. Collect rationalizations from RED runs (verbatim).
2. Match each rationalization to the closest row below.
3. Copy the counter sentence into your skill's rule section.
4. Add unmatched rationalizations as new rows.
5. Re-run GREEN and REFACTOR pressure checks.

## Discipline Skills (TDD, verification gates, strict process)

| Rationalization | Why It Fails | Counter Sentence |
|-----------------|--------------|------------------|
| "Too simple to test" | simple code still breaks | "Simple code breaks. Test takes 30 seconds." |
| "I'll test after" | tests-after cannot prove intent | "Tests-after proves nothing." |
| "I'm following the spirit" | letter violation is spirit violation | "Violating letter means violating spirit." |
| "I'll keep it as reference" | reference use bypasses reset rule | "Delete means delete. Do not look at old code." |
| "Just this once" | one exception becomes pattern | "No exceptions. Not once." |
| "Already manually tested" | manual checks are non-repeatable | "Manual testing does not replace automated tests." |
| "This case is different" | generic loophole language | "Different wording, same violation: start over." |

## Technique Skills (how-to methods)

| Rationalization | Counter Sentence |
|-----------------|------------------|
| "Quick fix is faster" | "Quick fix now creates rework later." |
| "Technique is overkill here" | "Technique exists for exactly this situation." |
| "I'll skip one step" | "Skipping one step breaks the method's guarantees." |

## Pattern Skills (mental models)

| Rationalization | Counter Sentence |
|-----------------|------------------|
| "Pattern is overkill" | "Pattern prevents predictable failures from shortcuts." |
| "Hack works for now" | "Works-now is not stable-later." |
| "I know this already" | "Pattern must still be applied explicitly." |

## Reference Skills (lookup and application)

| Rationalization | Counter Sentence |
|-----------------|------------------|
| "I remember this" | "Memory is fallible. Check the reference." |
| "Probably correct" | "Probably means uncertainty: verify before acting." |
| "Close enough" | "Reference tasks require exactness, not approximation." |

## Ready-to-Paste SKILL.md Snippet

Use this block after baseline testing:

```markdown
## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll test after" | Tests-after proves nothing. |
| "Just this once" | No exceptions. |

## Red Flags - Stop and Restart

- "I'll do it quickly first"
- "I already tested manually"
- "This case is different"

All red flags mean: stop, reset, follow the required workflow.
```

## Maintenance Rule

Whenever a new rationalization appears in testing:
- add it to this catalog
- add the counter to the target skill
- re-run pressure tests
