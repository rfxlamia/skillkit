# Multi-Tool Support for SkillKit Installer

**Date:** 2026-03-15
**Status:** Approved

## Background

The SkillKit installer (`npx @rfxlamia/skillkit`) currently only installs skills to Claude Code paths (`~/.claude/skills/`). The repo was renamed from `claude-skillkit` to `skillkit` to signal multi-tool intent, but the installer never followed through. This spec adds support for OpenAI Codex, OpenCode, and GitHub Copilot.

## Supported Tools & Paths

| Tool | Skills (user) | Skills (project) | Agents (user) | Agents (project) |
|------|--------------|-----------------|---------------|-----------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `~/.claude/agents/` | `.claude/agents/` |
| OpenCode | `~/.config/opencode/skills/skillkit/` | `.opencode/skills/` | `~/.config/opencode/agents/` | `.opencode/agents/` |
| Copilot | `~/.copilot/skills/` | *(none)* | `~/.claude/agents/` *(shared with Claude Code)* | `.github/agents/` |
| Codex | `~/.agents/skills/skillkit/` | *(none)* | *(skip)* | *(skip)* |

**Codex agents note:** Codex does not natively load agent definition files via `spawn_agent`. Agents are skipped for Codex. If a user selects only Codex and picks "agents-only" or selects specific agents, `installSelected()` will skip silently and log a note: `"Agents are not supported for Codex — skipped."` This is a known limitation, not an error.

**Copilot agents note:** Copilot shares `~/.claude/agents/` with Claude Code for user scope. Project scope uses `.github/agents/`.

## New CLI Flow

```
Banner + update check              (unchanged)
intro('SkillKit Installer')        (unchanged)
   ↓
[NEW] selectTools()                multiselect: Claude Code, OpenCode, Codex, Copilot
      + isCancel check → cancel('Cancelled.') + process.exit(0)
   ↓
selectScope()                      returns 'user' | 'project' (plain string)
                                   → if Codex selected: warn "Codex is always user-scoped"
   ↓
pickInstallables()                 unchanged (skills/agents picker)
   ↓
installSelected(selected, targets[])   install to each target
   ↓
outro: "X item(s) installed to Claude Code (user), OpenCode (project)."
log.info: "Restart your coding agent tools to pick up new skills."
```

## Components

### `src/tools.js` (new file)

Two exported functions:

**`selectTools()`** — interactive multiselect returning `string[]` of tool IDs (`claude-code`, `opencode`, `codex`, `copilot`).

**`getToolTargets(selectedTools, scope)`** — pure function, maps tool IDs + scope to a `Target[]`.

Path deduplication applies to both `skillsDir` and `agentsDir`. Targets with identical resolved paths are merged before installation — only one copy operation runs per unique path. This prevents double-install when, e.g., Copilot user + Claude Code user both resolve to `~/.claude/agents/`.

```js
Target = {
  name: string,        // display name e.g. "Claude Code"
  scope: string,       // 'user' | 'project' (used for outro label)
  skillsDir: string,   // absolute path
  agentsDir: string | null  // null means skip agents
}
```

Mapping rules:
- `claude-code`: respects scope (user/project)
- `opencode`: respects scope (user → `~/.config/opencode/`, project → `.opencode/`)
- `codex`: always user scope regardless of selected scope; `agentsDir: null`
- `copilot`: skills always `~/.copilot/skills/` regardless of scope; agents: user → `~/.claude/agents/`, project → `.github/agents/`

### `src/cli.js` (modified)

- Add `selectTools()` call between `intro` and `selectScope()`
- Add `isCancel` check after `selectTools()`; call `cancel('Cancelled.')` and `process.exit(0)` on cancel
- Pass only the `scope` string (not the old `{ scope, skillsDir, agentsDir }` object) to `getToolTargets()`
- Pass `targets` array to `installSelected()`
- Build `outro` message from `results[]`: e.g. `"31 item(s) installed to Claude Code (user), OpenCode (project)."`
- Update `log.info` to `"Restart your coding agent tools to pick up new skills."`

### `src/scope.js` (modified)

- `selectScope()` now returns a plain `'user' | 'project'` string (previously returned `{ scope, skillsDir, agentsDir }`)
- The exported test helpers `getUserScope()` and `getProjectScope()` are removed — they are no longer valid since path resolution moves to `getToolTargets()`
- Accept `selectedTools` parameter (passed from `cli.js` after tool selection)
- If `codex` is in `selectedTools` and user picks project scope, log a warning: `"Codex does not support project scope — skills will be installed to ~/.agents/skills/skillkit/"`

### `src/install.js` (modified)

Signature change:

```js
// before
installSelected({ skills, agents }, { skillsDir, agentsDir })

// after
installSelected({ skills, agents }, targets[])
```

Returns:

```js
{
  results: Array<{ target: Target, installed: number, skipped: string[] }>,
  totalInstalled: number
}
```

Iterates over each `Target`, copies skills to `target.skillsDir` and agents to `target.agentsDir` (skipped if `null`). If `agentsDir` is `null` and the user selected agents, logs: `"Agents are not supported for Codex — skipped."` `totalInstalled` is the sum of unique file-write operations after path deduplication.

### `src/picker.js` (modified)

- Sort skills list: `skillkit` always first, then alphabetical by name (housekeeping, unrelated to multi-tool)
- Update "Everything" label to reflect current manifest count dynamically

### `src/banner.js` (modified)

- Update subtitle from `"Claude Code Skills Installer"` to `"Multi-Tool Skills Installer"`

### `src/tools.test.js` (new file)

Unit tests for `getToolTargets()`:
- Claude Code user scope → correct paths
- Claude Code project scope → correct paths
- Codex with user scope → `skillsDir` is `~/.agents/skills/skillkit/`, `agentsDir` is `null`
- Codex with project scope → `skillsDir` is still `~/.agents/skills/skillkit/` (scope override), `agentsDir` is `null`
- Copilot user → skills to `~/.copilot/skills/`, agents to `~/.claude/agents/`
- Copilot project → skills to `~/.copilot/skills/` (unchanged), agents to `.github/agents/`
- OpenCode user → `~/.config/opencode/` paths
- OpenCode project → `.opencode/` paths
- Multi-tool `['claude-code', 'copilot']` user scope → two targets, `agentsDir` deduplicated (no `~/.claude/agents/` duplicate)
- Empty selection `[]` → returns `[]`

## Data Flow

```
selectTools()          → string[]           e.g. ['claude-code', 'opencode']
     ↓
selectScope()          → 'user' | 'project'
     ↓
getToolTargets()       → Target[]           (deduped by path)
     ↓
installSelected()      → for each target:
                           copy skills → target.skillsDir/
                           copy agents → target.agentsDir/ (skip if null)
                         → { results[], totalInstalled }
```

## Edge Cases

| Case | Handling |
|------|----------|
| Codex + project scope selected | Override to user scope + warning log |
| Copilot + Claude Code both selected (user) | `agentsDir` deduped — agents installed once to `~/.claude/agents/` |
| Copilot project scope + skills | Copilot has no project scope for skills → always `~/.copilot/skills/` |
| No tools selected (cancel) | `isCancel` check after `selectTools()`, exit with message |
| Codex selected + agents-only picked | Skip agents silently, log note, `installed: 0` for Codex target |

## Files Changed

| File | Action | Notes |
|------|--------|-------|
| `src/tools.js` | Create | `selectTools()` + `getToolTargets()` |
| `src/tools.test.js` | Create | Unit tests for `getToolTargets()` |
| `src/cli.js` | Modify | Add tool selection step |
| `src/scope.js` | Modify | Returns plain string; remove `getUserScope`/`getProjectScope` helpers |
| `src/scope.test.js` | Modify | Update to test new string return type; remove tests for deleted helpers |
| `src/install.js` | Modify | New `targets[]` signature + new return shape |
| `src/install.test.js` | Modify | Update calls to new `installSelected(selected, targets[])` signature; assert `{ results[], totalInstalled }` return shape |
| `src/picker.js` | Modify | `skillkit` first, dynamic "Everything" label |
| `src/banner.js` | Modify | Update subtitle string |
