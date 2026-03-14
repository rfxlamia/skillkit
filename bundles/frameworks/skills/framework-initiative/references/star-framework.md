# STAR Framework - Detailed Implementation

## Stop Phase: Detection Triggers

### Automatic Triggers

Activate STOP when detecting the following patterns in requests:

**Quantifier Ambiguity:**
```
"all", "every", "each" → Is it really ALL?
"unused", "old" → Whose criteria for unused/old?
"duplicate" → Exact duplicate or similar?
```

**Verb Ambiguity:**
```
"fix" → patch? refactor? rewrite?
"improve" → performance? readability? both?
"update" → in-place? migration? version bump?
"clean" → delete? reorganize? format?
```

**Scope Ambiguity:**
```
"this file" → file only or related files?
"this function" → function only or callers?
"the code" → specific code or entire codebase?
```

### Stop Checklist

```
Before ANY code modification:
□ Did user specify exact files?
□ Did user specify exact functions/lines?
□ Are there implicit constraints not mentioned?
□ Could this break something not mentioned?
```

---

## Think Phase: Intent Translation

### Intent Mapping Matrix

| Surface Request | Hidden Intent | Verification Question |
|-----------------|---------------|----------------------|
| "Delete this" | Remove safely | "Are there references to this?" |
| "Rename X" | Rename consistently | "Where else is X used?" |
| "Add feature Y" | Add without breaking | "What depends on this area?" |
| "Make faster" | Optimize meaningfully | "Where is the actual bottleneck?" |
| "Fix the bug" | Fix root cause | "What's the actual root cause?" |

### Contextual Inference

**Technical Context:**
- Is this production code or experimental?
- Is there test coverage?
- Is there CI/CD that will validate?

**Business Context:**
- Is this a critical path?
- Is there a deadline not mentioned?
- Are there other stakeholders affected?

**Historical Context:**
- Has user requested similar before?
- Is there a pattern from previous conversation?

---

## Analyze Phase: Dependency Mapping

### Quick Scan Commands

```bash
# Find all usages of a function
grep -r "functionName" --include="*.ts" .

# Find imports of a module
grep -r "import.*from.*moduleName" .

# Find type references
grep -r "type.*TypeName\|interface.*TypeName" .

# Find test files
find . -name "*.test.*" -o -name "*.spec.*"
```

### Impact Assessment Template

```
┌─ IMPACT ASSESSMENT ────────────────────────┐
│                                            │
│ Target: [function/file/component]          │
│                                            │
│ Direct Impact:                             │
│   □ Files modified: [count]                │
│   □ Functions affected: [list]             │
│                                            │
│ Indirect Impact:                           │
│   □ Callers: [count]                       │
│   □ Tests: [count]                         │
│   □ API contracts: [yes/no]                │
│                                            │
│ Risk Level: [LOW/MEDIUM/HIGH]              │
│                                            │
│ Recommendation:                            │
│   □ Proceed                                │
│   □ Proceed with confirmation              │
│   □ Request more info                      │
│                                            │
└────────────────────────────────────────────┘
```

### Breaking Change Detection

**Type Changes:**
- Parameter added/removed → Callers break
- Return type changed → Consumers break
- Property renamed → Destructuring breaks

**Behavioral Changes:**
- Side effects added/removed
- Error handling changed
- Async/sync change

---

## Respond Phase: Execution Strategy

### Communication Template

```markdown
## Proposed Changes

**Scope:** [specific files/functions]

**Actions:**
1. [action 1]
2. [action 2]

**Impact:**
- Will affect: [list]
- Will NOT touch: [explicit exclusions]

**Risk:** [LOW/MEDIUM/HIGH]

Proceed?
```

### Execution Order

1. **Read-only first**: Analyze before modify
2. **Tests second**: Ensure test passes before change
3. **Leaf nodes first**: Change callees before callers
4. **Atomic commits**: One logical change per commit

### Rollback Plan

Always have a rollback strategy:
- Git: `git stash` before major changes
- Backup: Copy file before destructive edit
- Incremental: Commit after each valid step
