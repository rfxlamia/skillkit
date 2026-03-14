# Impact Analysis Techniques

## Dependency Graph Construction

### Code-Level Dependencies

**Function Dependencies:**
```
Target Function
     │
     ├── Callers (who calls this?)
     │     ├── Direct callers
     │     └── Indirect callers (caller's callers)
     │
     ├── Callees (what does this call?)
     │     └── External dependencies
     │
     └── Shared State
           ├── Global variables
           ├── Module state
           └── External resources (DB, files)
```

**File Dependencies:**
```
Target File
     │
     ├── Importers (who imports this?)
     ├── Imports (what does this import?)
     ├── Re-exports (pass-through dependencies)
     └── Implicit (same directory, naming conventions)
```

### Type-Level Dependencies

TypeScript/typed languages have an extra layer:
- Interface implementations
- Type aliases
- Generic constraints
- Union/intersection types

---

## Analysis Workflows

### Workflow 1: Function Change

```
1. Find all callers
   grep -r "functionName(" --include="*.ts"

2. Check each caller's expectations
   - Parameter types
   - Return value usage
   - Error handling

3. Find tests
   grep -r "functionName" --include="*.test.*"

4. Check types/interfaces
   grep -r "type.*functionName\|: functionName"
```

### Workflow 2: File Rename/Delete

```
1. Find all imports
   grep -r "from.*oldFileName\|import.*oldFileName"

2. Check for path references
   grep -r "oldFileName" (in configs, tests, etc.)

3. Check for dynamic imports
   grep -r "import(" | grep "oldFileName"

4. Check package.json exports (if applicable)
```

### Workflow 3: Type Change

```
1. Find all usages of the type
   grep -r "TypeName" --include="*.ts"

2. Check implements/extends
   grep -r "implements.*TypeName\|extends.*TypeName"

3. Check type assertions
   grep -r "as TypeName\|<TypeName>"
```

---

## Risk Assessment Matrix

| Change Type | Scope | Risk Level | Action |
|-------------|-------|------------|--------|
| Local variable | Function | LOW | Proceed |
| Function signature | Multiple callers | MEDIUM | Confirm scope |
| Interface/Type | Unknown usages | HIGH | Full analysis |
| Export rename | Unknown importers | HIGH | Full analysis |
| Delete file | Unknown dependencies | CRITICAL | Deep analysis |

---

## Silent Failure Patterns

### Pattern 1: Optional Chaining Hide Errors

```typescript
// Before: crashes if user is undefined
const name = user.name;

// After: silently returns undefined
const name = user?.name;

// Risk: undefined propagates silently
```

### Pattern 2: Default Parameter Masks

```typescript
// Before
function fetch(url, options) { ... }

// After (breaking for callers expecting positional)
function fetch(url, options = {}) { ... }
```

### Pattern 3: Type Coercion

```typescript
// Loose equality hides type mismatch
if (value == "5")  // true for value = 5

// Strict would catch it
if (value === "5") // false for value = 5
```

---

## Tools for Impact Analysis

### Built-in Searches
- `grep -r`: Text search across files
- `find`: Locate files by pattern
- `git log -p`: History of changes

### IDE Features
- "Find All References"
- "Go to Definition"
- "Call Hierarchy"

### Static Analysis
- TypeScript compiler: `tsc --noEmit`
- ESLint with appropriate plugins
- Dependency cruiser: visualize dependencies
