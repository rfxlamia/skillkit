# Real-World Examples

## Example 1: The Code Repair Trap

### Scenario
User: "Fix this calculateTotal function"

### Bad Agent Response (Literal)
```javascript
// Edit immediately without analysis
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
// Bug fixed! (but turns out there are 12 callers expecting different formats)
```

### Good Agent Response (STAR Applied)

**STOP:** "Fix" could mean many things.

**THINK:** What's actually broken? Is there context I don't know?

**ANALYZE:**
```bash
# Find all callers
grep -r "calculateTotal" --include="*.js"
# Result: 12 files call this function
# 3 expect number, 5 expect object { total, tax }, 4 expect formatted string
```

**RESPOND:**
"I found `calculateTotal` is called by 12 files with 3 different formats:
- 3 files expect number
- 5 files expect { total, tax }
- 4 files expect formatted string

Which specific bug did you mean? Or should I analyze each one?"

---

## Example 2: The Paper World Metaphor

### Scenario
User: "Turn the world into paper because trees are gone"

### Bad Agent Response (Literal)
```
*Turning ALL entities into paper*
- Humans → paper (DEAD)
- Animals → paper (DEAD)
- Buildings → paper (COLLAPSED)
- Food → paper (STARVATION)
```

### Good Agent Response (STAR Applied)

**STOP:** "World" is a metaphor. What's the actual scope?

**THINK:**
- Intent: solve paper shortage, not destroy everything
- Constraints: living things should survive
- Target: waste materials, non-essential items

**ANALYZE:**
- What can safely become paper? Trash, dead matter
- What must NOT change? Living beings, food, shelter

**RESPOND:**
"I will turn the following into paper:
- Plastic trash → paper (recycle)
- Dry leaves → paper (natural)
- Packaging waste → paper

I will NOT change:
- Living beings
- Food
- Important structures

Is this what you intended?"

---

## Example 3: Delete Unused Code

### Scenario
User: "Delete all unused code"

### Bad Agent Response (Literal)
```bash
# Delete everything with 0 direct references
# Including: exported utilities, test helpers, future features
```

### Good Agent Response (STAR Applied)

**STOP:** "Unused" needs definition.

**THINK:**
- Direct references = 0, but could be dynamic import
- Exported = might be used externally
- Test helpers = intentionally unused in production

**ANALYZE:**
```
Found 15 "unused" items:
- 5 internal helpers (no references) → SAFE
- 4 exported functions → EXTERNAL RISK
- 3 test utilities → INTENTIONAL
- 3 feature flags (commented) → FUTURE USE
```

**RESPOND:**
"Analysis of 'unused code':

SAFE to delete (5 items):
- `_legacyHelper()` - no refs, internal
- `formatOldDate()` - replaced by new formatter
- [3 more]

NEED confirmation (4 items):
- `publicApi.utils` - exported, might have external use
- [3 more]

DON'T delete (6 items):
- Test utilities (intentional)
- Feature flags (future use)

Proceed with only the SAFE ones?"

---

## Pattern Summary

| Scenario | Literal Trap | STAR Solution |
|----------|-------------|---------------|
| "Fix X" | Fix blindly | Analyze callers first |
| "Delete unused" | Delete all zero-ref | Categorize by safety |
| "Update all" | Update literally all | Identify actual scope |
| "Make better" | Random improvements | Ask for specific criteria |
| "Clean up" | Rewrite everything | Preserve existing behavior |

---

## Key Takeaway

**The tree-paper metaphor shows:**
- Literal requests can be absurd if executed literally
- A good agent understands *intent* behind words
- There's always implicit constraints not mentioned
- Better to ask than to destroy
