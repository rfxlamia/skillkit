# Common Implicit Intent Patterns

## Pattern Categories

### Category 1: Scope Expansion

User says something specific, but implicitly expects broader handling.

| Surface | Implicit Expansion |
|---------|-------------------|
| "Fix this bug" | Fix + prevent regression (add test) |
| "Add this feature" | Add + integrate with existing |
| "Update this API" | Update + update clients + update docs |

**Detection:** Keywords "this", "the" without explicit scope.

### Category 2: Scope Restriction

User says something broad, but implicitly expects targeted action.

| Surface | Implicit Restriction |
|---------|---------------------|
| "Delete unused code" | Delete unused BUT keep possibly-needed |
| "Refactor everything" | Refactor BUT preserve behavior |
| "Update all tests" | Update relevant tests, not literally all |

**Detection:** Keywords "all", "every", "everything" in destructive context.

### Category 3: Quality Assumptions

User assumes certain quality standards without stating.

| Unstated Assumption | What It Means |
|--------------------|---------------|
| Code should work | Include error handling |
| Code should be maintainable | Follow existing patterns |
| Changes should be safe | Don't break existing functionality |
| Performance shouldn't degrade | Consider performance implications |

**Detection:** Any code modification request.

### Category 4: Domain Context

User assumes domain knowledge is shared.

| Domain | Common Implicit Knowledge |
|--------|--------------------------|
| API | Don't change public contracts without versioning |
| Database | Don't drop tables without backup consideration |
| Auth | Security implications are paramount |
| Payment | Extra caution for financial operations |

**Detection:** Keywords related to sensitive domains.

---

## Detection Heuristics

### High-Confidence Implicit Intent

**Pattern: Singular Reference to Plural Scope**
```
"Update the config" → probably all related configs
"Fix the test" → probably all failing tests
"Change the variable name" → probably all usages
```

**Pattern: Action Without Object Specification**
```
"Make it work" → fix the immediate issue
"Clean this up" → improve readability, not restructure
"Simplify" → reduce complexity, keep functionality
```

### Low-Confidence (Ask for Clarification)

**Pattern: Contradictory Signals**
```
"Delete everything but keep it working"
"Refactor completely but don't change behavior"
"Update all files quickly"
```

**Pattern: Vague Quality Targets**
```
"Make it better" → better how?
"Optimize this" → for what metric?
"Improve performance" → latency? throughput? memory?
```

---

## Intent Translation Examples

### Example 1: Bug Fix Request

**User says:** "Fix the login bug"

**Think phase:**
- Which login bug? (may be multiple)
- Just the symptom or root cause?
- Should I add tests?
- Are there related auth issues?

**Good response:**
"I found 2 issues in the login flow:
1. Null check missing at line 45
2. Race condition in session handling

Should I fix both or focus on one?"

### Example 2: Feature Addition

**User says:** "Add dark mode"

**Think phase:**
- Where should toggle be?
- Persist preference?
- Affect all components or specific?
- What about existing color variables?

**Good response:**
"For dark mode, I will:
1. Add CSS variables for theming
2. Add toggle in settings
3. Persist to localStorage

Won't change existing color values without confirmation. OK?"

### Example 3: Code Deletion

**User says:** "Delete unused functions"

**Think phase:**
- Unused = no direct calls, or no reachable calls?
- Include dynamically called functions?
- What about exported but unused?
- What about test helpers?

**Good response:**
"I found 5 functions without direct callers:
- 3 internal helpers (safe to delete)
- 2 exported functions (might be used externally)

I will delete 3 internal helpers. 2 exported functions need confirmation."
