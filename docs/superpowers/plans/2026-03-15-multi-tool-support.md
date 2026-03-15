# Multi-Tool Support Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the SkillKit installer to support OpenCode, Codex, and GitHub Copilot in addition to Claude Code, letting users install skills/agents to multiple tools in one run.

**Architecture:** Add a new `tools.js` module for tool selection and path resolution, modify `scope.js` to return a plain string, update `install.js` to accept multiple targets, then wire everything in `cli.js`. Each layer is independently testable.

**Tech Stack:** Node.js ESM, `@clack/prompts`, `node:test` (built-in test runner), `node:assert`

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `installer/src/tools.js` | Create | Tool selection UI + path resolution (`getToolTargets`) |
| `installer/src/tools.test.js` | Create | Unit tests for `getToolTargets` |
| `installer/src/scope.js` | Modify | Return plain `'user'\|'project'` string; remove old path helpers |
| `installer/src/scope.test.js` | Modify | Update tests for new return type |
| `installer/src/install.js` | Modify | Accept `targets[]`, return `{ results[], totalInstalled }` |
| `installer/src/install.test.js` | Modify | Update calls to new signature |
| `installer/src/picker.js` | Modify | `skillkit` first in list; dynamic count label |
| `installer/src/banner.js` | Modify | Update subtitle string |
| `installer/src/cli.js` | Modify | Add tool selection step; wire all parts together |
| `installer/tests/integration.test.js` | Modify | Assert `tools.js` module exports |

---

## Chunk 1: tools.js — Tool Selection and Path Resolution

### Task 1: Write failing tests for `getToolTargets`

**Files:**
- Create: `installer/src/tools.test.js`

- [ ] **Step 1: Create the test file**

```js
// installer/src/tools.test.js
import { test } from 'node:test'
import assert from 'node:assert'
import { homedir } from 'os'
import { join } from 'path'
import { getToolTargets } from './tools.js'

const home = homedir()
const cwd = process.cwd()

test('getToolTargets returns empty array for empty selection', () => {
  const result = getToolTargets([], 'user')
  assert.deepStrictEqual(result, [])
})

test('getToolTargets claude-code user scope', () => {
  const [t] = getToolTargets(['claude-code'], 'user')
  assert.strictEqual(t.name, 'Claude Code')
  assert.strictEqual(t.scope, 'user')
  assert.strictEqual(t.skillsDir, join(home, '.claude', 'skills'))
  assert.strictEqual(t.agentsDir, join(home, '.claude', 'agents'))
})

test('getToolTargets claude-code project scope', () => {
  const [t] = getToolTargets(['claude-code'], 'project')
  assert.strictEqual(t.scope, 'project')
  assert.strictEqual(t.skillsDir, join(cwd, '.claude', 'skills'))
  assert.strictEqual(t.agentsDir, join(cwd, '.claude', 'agents'))
})

test('getToolTargets opencode user scope', () => {
  const [t] = getToolTargets(['opencode'], 'user')
  assert.strictEqual(t.name, 'OpenCode')
  assert.strictEqual(t.skillsDir, join(home, '.config', 'opencode', 'skills', 'skillkit'))
  assert.strictEqual(t.agentsDir, join(home, '.config', 'opencode', 'agents'))
})

test('getToolTargets opencode project scope', () => {
  const [t] = getToolTargets(['opencode'], 'project')
  assert.strictEqual(t.skillsDir, join(cwd, '.opencode', 'skills'))
  assert.strictEqual(t.agentsDir, join(cwd, '.opencode', 'agents'))
})

test('getToolTargets codex user scope — agentsDir is null', () => {
  const [t] = getToolTargets(['codex'], 'user')
  assert.strictEqual(t.name, 'Codex')
  assert.strictEqual(t.skillsDir, join(home, '.agents', 'skills', 'skillkit'))
  assert.strictEqual(t.agentsDir, null)
})

test('getToolTargets codex project scope — still resolves to user path', () => {
  const [t] = getToolTargets(['codex'], 'project')
  assert.strictEqual(t.scope, 'user')
  assert.strictEqual(t.skillsDir, join(home, '.agents', 'skills', 'skillkit'))
  assert.strictEqual(t.agentsDir, null)
})

test('getToolTargets copilot user scope', () => {
  const [t] = getToolTargets(['copilot'], 'user')
  assert.strictEqual(t.name, 'GitHub Copilot')
  assert.strictEqual(t.skillsDir, join(home, '.copilot', 'skills'))
  assert.strictEqual(t.agentsDir, join(home, '.claude', 'agents'))
})

test('getToolTargets copilot project scope — skills still user path, agents project path', () => {
  const [t] = getToolTargets(['copilot'], 'project')
  assert.strictEqual(t.skillsDir, join(home, '.copilot', 'skills'))
  assert.strictEqual(t.agentsDir, join(cwd, '.github', 'agents'))
})

test('getToolTargets deduplicates agentsDir for claude-code + copilot (user)', () => {
  const targets = getToolTargets(['claude-code', 'copilot'], 'user')
  assert.strictEqual(targets.length, 2)
  const agentsDirs = targets.map(t => t.agentsDir).filter(Boolean)
  const uniqueAgentsDirs = [...new Set(agentsDirs)]
  assert.strictEqual(agentsDirs.length, uniqueAgentsDirs.length, 'no duplicate agentsDirs')
  // Claude Code gets agentsDir, Copilot gets null (deduped)
  assert.strictEqual(targets[0].agentsDir, join(home, '.claude', 'agents'))
  assert.strictEqual(targets[1].agentsDir, null)
})
```

- [ ] **Step 2: Run tests to confirm they fail (module doesn't exist yet)**

```bash
cd installer && node --test src/tools.test.js
```

Expected: Error — `Cannot find module './tools.js'`

---

### Task 2: Implement `tools.js`

**Files:**
- Create: `installer/src/tools.js`

- [ ] **Step 3: Create the implementation**

```js
// installer/src/tools.js
import { multiselect } from '@clack/prompts'
import { homedir } from 'os'
import { join } from 'path'

export async function selectTools() {
  return multiselect({
    message: 'Install to which tools?',
    options: [
      { value: 'claude-code', label: 'Claude Code', hint: '~/.claude/skills/' },
      { value: 'opencode', label: 'OpenCode', hint: '~/.config/opencode/skills/' },
      { value: 'codex', label: 'Codex', hint: '~/.agents/skills/' },
      { value: 'copilot', label: 'GitHub Copilot', hint: '~/.copilot/skills/' }
    ],
    required: true
  })
}

export function getToolTargets(selectedTools, scope) {
  if (!selectedTools.length) return []

  const home = homedir()
  const cwd = process.cwd()
  const isUser = scope === 'user'

  const resolve = {
    'claude-code': {
      name: 'Claude Code',
      scope,
      skillsDir: isUser ? join(home, '.claude', 'skills') : join(cwd, '.claude', 'skills'),
      agentsDir: isUser ? join(home, '.claude', 'agents') : join(cwd, '.claude', 'agents')
    },
    'opencode': {
      name: 'OpenCode',
      scope,
      skillsDir: isUser
        ? join(home, '.config', 'opencode', 'skills', 'skillkit')
        : join(cwd, '.opencode', 'skills'),
      agentsDir: isUser
        ? join(home, '.config', 'opencode', 'agents')
        : join(cwd, '.opencode', 'agents')
    },
    'codex': {
      name: 'Codex',
      scope: 'user',
      skillsDir: join(home, '.agents', 'skills', 'skillkit'),
      agentsDir: null
    },
    'copilot': {
      name: 'GitHub Copilot',
      scope: isUser ? 'user' : 'project',
      skillsDir: join(home, '.copilot', 'skills'),
      agentsDir: isUser
        ? join(home, '.claude', 'agents')
        : join(cwd, '.github', 'agents')
    }
  }

  const targets = selectedTools
    .filter(id => resolve[id])
    .map(id => ({ ...resolve[id] }))

  // Dedup: if skillsDir or agentsDir appears more than once, null it in later targets
  const seenSkills = new Set()
  const seenAgents = new Set()

  for (const t of targets) {
    if (seenSkills.has(t.skillsDir)) t.skillsDir = null
    else seenSkills.add(t.skillsDir)

    if (t.agentsDir && seenAgents.has(t.agentsDir)) t.agentsDir = null
    else if (t.agentsDir) seenAgents.add(t.agentsDir)
  }

  return targets.filter(t => t.skillsDir || t.agentsDir)
}
```

- [ ] **Step 4: Run tests — all must pass**

```bash
cd installer && node --test src/tools.test.js
```

Expected: all 10 tests pass

- [ ] **Step 5: Commit**

```bash
git add installer/src/tools.js installer/src/tools.test.js
git commit -m "feat(installer): add tools.js with selectTools and getToolTargets"
```

---

## Chunk 2: scope.js — Return Plain String

### Task 3: Update scope tests for new return type

**Files:**
- Modify: `installer/src/scope.test.js`

- [ ] **Step 1: Replace scope.test.js content**

```js
// installer/src/scope.test.js
import { test } from 'node:test'
import assert from 'node:assert'
import { selectScope } from './scope.js'

test('selectScope is an async function', () => {
  assert.strictEqual(typeof selectScope, 'function')
})

test('getUserScope and getProjectScope are no longer exported', async () => {
  const mod = await import('./scope.js')
  assert.strictEqual(mod.getUserScope, undefined)
  assert.strictEqual(mod.getProjectScope, undefined)
})
```

- [ ] **Step 2: Run tests — they should fail (old exports still exist)**

```bash
cd installer && node --test src/scope.test.js
```

Expected: second test fails because `getUserScope` is still exported

---

### Task 4: Modify `scope.js`

**Files:**
- Modify: `installer/src/scope.js`

- [ ] **Step 3: Replace scope.js content**

```js
// installer/src/scope.js
import { select, log } from '@clack/prompts'

export async function selectScope(selectedTools = []) {
  const scope = await select({
    message: 'Install to:',
    options: [
      {
        value: 'user',
        label: 'User scope',
        hint: 'available in all projects'
      },
      {
        value: 'project',
        label: 'Project scope',
        hint: 'this project only'
      }
    ]
  })

  if (selectedTools.includes('codex') && scope === 'project') {
    log.warn('Codex does not support project scope — skills will be installed to ~/.agents/skills/skillkit/')
  }

  return scope
}
```

- [ ] **Step 4: Run scope tests — all must pass**

```bash
cd installer && node --test src/scope.test.js
```

Expected: both tests pass

- [ ] **Step 5: Commit**

```bash
git add installer/src/scope.js installer/src/scope.test.js
git commit -m "refactor(installer): selectScope returns plain string, remove path helpers"
```

---

## Chunk 3: install.js — Multiple Targets

### Task 5: Update install tests for new signature

**Files:**
- Modify: `installer/src/install.test.js`

- [ ] **Step 1: Replace install.test.js content**

```js
// installer/src/install.test.js
import { test } from 'node:test'
import assert from 'node:assert'
import { mkdtempSync, writeFileSync, mkdirSync, existsSync, rmSync, cpSync } from 'fs'
import { join } from 'path'
import { tmpdir } from 'os'
import { installSelected } from './install.js'

function createTempDir() {
  return mkdtempSync(join(tmpdir(), 'skillkit-test-'))
}

function makeTarget(skillsDir, agentsDir, name = 'Test Tool') {
  return { name, scope: 'user', skillsDir, agentsDir }
}

test('installSelected validates skills is an array', async () => {
  await assert.rejects(
    installSelected({ skills: 'not-array', agents: [] }, [makeTarget('/tmp', '/tmp')]),
    /skills must be an array/
  )
})

test('installSelected validates agents is an array', async () => {
  await assert.rejects(
    installSelected({ skills: [], agents: 'not-array' }, [makeTarget('/tmp', '/tmp')]),
    /agents must be an array/
  )
})

test('installSelected validates targets is an array', async () => {
  await assert.rejects(
    installSelected({ skills: [], agents: [] }, 'not-array'),
    /targets must be an array/
  )
})

test('installSelected skips invalid skill objects', async () => {
  const skillsDir = createTempDir()
  const agentsDir = createTempDir()

  const { totalInstalled, results } = await installSelected(
    { skills: [{ name: null }, { name: 'valid', path: 'skills/valid' }], agents: [] },
    [makeTarget(skillsDir, agentsDir)]
  )

  assert.strictEqual(totalInstalled, 0)
  assert.strictEqual(results[0].skipped.length, 2)

  rmSync(skillsDir, { recursive: true })
  rmSync(agentsDir, { recursive: true })
})

test('installSelected returns results per target', async () => {
  const dir1 = createTempDir()
  const dir2 = createTempDir()

  const { results, totalInstalled } = await installSelected(
    { skills: [], agents: [] },
    [makeTarget(dir1, null, 'Tool A'), makeTarget(dir2, null, 'Tool B')]
  )

  assert.strictEqual(results.length, 2)
  assert.strictEqual(results[0].target.name, 'Tool A')
  assert.strictEqual(results[1].target.name, 'Tool B')
  assert.strictEqual(totalInstalled, 0)

  rmSync(dir1, { recursive: true })
  rmSync(dir2, { recursive: true })
})

test('installSelected skips agents when agentsDir is null', async () => {
  const skillsDir = createTempDir()

  const { results } = await installSelected(
    { skills: [], agents: [{ name: 'test-agent', path: 'agents/test-agent.md' }] },
    [makeTarget(skillsDir, null)]
  )

  assert.strictEqual(results[0].target.agentsDir, null)

  rmSync(skillsDir, { recursive: true })
})
```

- [ ] **Step 2: Run tests — they should fail (old signature)**

```bash
cd installer && node --test src/install.test.js
```

Expected: failures due to signature mismatch and missing `totalInstalled`/`results` shape

---

### Task 6: Modify `install.js`

**Files:**
- Modify: `installer/src/install.js`

- [ ] **Step 3: Replace install.js content**

```js
// installer/src/install.js
import { cpSync, mkdirSync, existsSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { spinner, log } from '@clack/prompts'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PACKAGE_ROOT = join(__dirname, '..')

export async function installSelected({ skills, agents }, targets) {
  if (!Array.isArray(skills)) throw new TypeError('skills must be an array')
  if (!Array.isArray(agents)) throw new TypeError('agents must be an array')
  if (!Array.isArray(targets)) throw new TypeError('targets must be an array')

  const s = spinner()
  s.start('Installing...')

  const results = []
  let totalInstalled = 0

  for (const target of targets) {
    let installed = 0
    const skipped = []

    if (target.skillsDir) {
      for (const skill of skills) {
        if (!skill.name || !skill.path) {
          skipped.push(`invalid-skill-${installed}`)
          continue
        }
        const src = join(PACKAGE_ROOT, skill.path)
        const dest = join(target.skillsDir, skill.name)
        if (!existsSync(src)) { skipped.push(skill.name); continue }
        mkdirSync(dest, { recursive: true })
        cpSync(src, dest, { recursive: true })
        installed++
      }
    }

    if (target.agentsDir) {
      for (const agent of agents) {
        if (!agent.name || !agent.path) {
          skipped.push(`invalid-agent-${installed}`)
          continue
        }
        const src = join(PACKAGE_ROOT, agent.path)
        const dest = join(target.agentsDir, agent.name + '.md')
        if (!existsSync(src)) { skipped.push(agent.name); continue }
        mkdirSync(target.agentsDir, { recursive: true })
        cpSync(src, dest)
        installed++
      }
    } else if (agents.length > 0) {
      log.warn(`Agents are not supported for ${target.name} — skipped.`)
    }

    results.push({ target, installed, skipped })
    totalInstalled += installed
  }

  s.stop(`Installed ${totalInstalled} item(s)`)

  const allSkipped = results.flatMap(r => r.skipped)
  if (allSkipped.length > 0) {
    log.warn(`Skipped (not found in package): ${allSkipped.join(', ')}`)
  }

  return { results, totalInstalled }
}
```

- [ ] **Step 4: Run install tests — all must pass**

```bash
cd installer && node --test src/install.test.js
```

Expected: all 6 tests pass

- [ ] **Step 5: Commit**

```bash
git add installer/src/install.js installer/src/install.test.js
git commit -m "feat(installer): installSelected accepts targets[], returns results per target"
```

---

## Chunk 4: Wiring — picker.js, banner.js, cli.js, integration

### Task 7: Update `picker.js` (skillkit first, dynamic count)

**Files:**
- Modify: `installer/src/picker.js`

- [ ] **Step 1: Edit the `pickInstallables` function in picker.js**

Change the mode options and skill sort in `pickInstallables`:

```js
// Replace the mode options (the 'all' label):
{ value: 'all', label: `Everything (${manifest.skills.length} skills + ${manifest.agents.length} agents)` },
```

Add skill sort before building `skillChoices` (put this just before the `const skillChoices = ...` line):

```js
const sortedSkills = [...manifest.skills].sort((a, b) => {
  if (a.name === 'skillkit') return -1
  if (b.name === 'skillkit') return 1
  return a.name.localeCompare(b.name)
})
```

Then replace `manifest.skills.map(...)` with `sortedSkills.map(...)` for `skillChoices`, and replace `manifest.skills.filter(...)` with `sortedSkills.filter(...)` in the return.

The full updated `pickInstallables` function:

```js
export async function pickInstallables() {
  const mode = await select({
    message: 'What to install?',
    options: [
      { value: 'all', label: `Everything (${manifest.skills.length} skills + ${manifest.agents.length} agents)` },
      { value: 'skills-only', label: 'All skills only' },
      { value: 'agents-only', label: 'All agents only' },
      { value: 'pick', label: 'Let me choose...' }
    ]
  })

  if (mode === 'all') return { skills: manifest.skills, agents: manifest.agents }
  if (mode === 'skills-only') return { skills: manifest.skills, agents: [] }
  if (mode === 'agents-only') return { skills: [], agents: manifest.agents }

  const sortedSkills = [...manifest.skills].sort((a, b) => {
    if (a.name === 'skillkit') return -1
    if (b.name === 'skillkit') return 1
    return a.name.localeCompare(b.name)
  })

  const skillChoices = sortedSkills.map(s => ({
    value: s.name,
    label: `${getCategoryDisplay(s)} ${s.name}`,
    hint: s.description.slice(0, 60) + (s.description.length > 60 ? '…' : '')
  }))

  const agentChoices = manifest.agents.map(a => ({
    value: a.name,
    label: `🤝 ${a.name}`,
    hint: a.description.slice(0, 60) + (a.description.length > 60 ? '…' : '')
  }))

  const selectedSkills = await multiselect({
    message: 'Select skills to install: (space to toggle, a to select all)',
    options: skillChoices,
    required: false
  })

  const selectedAgents = await multiselect({
    message: 'Select agents to install:',
    options: agentChoices,
    required: false
  })

  return {
    skills: sortedSkills.filter(s => selectedSkills.includes(s.name)),
    agents: manifest.agents.filter(a => selectedAgents.includes(a.name))
  }
}
```

- [ ] **Step 2: Run picker tests — must still pass**

```bash
cd installer && node --test src/picker.test.js
```

Expected: all 3 existing tests pass (we only changed `pickInstallables`, not `getCategoryDisplay`)

- [ ] **Step 3: Commit**

```bash
git add installer/src/picker.js
git commit -m "feat(installer): skillkit first in skill list, dynamic everything label"
```

---

### Task 8: Update `banner.js`

**Files:**
- Modify: `installer/src/banner.js`

- [ ] **Step 1: Update the subtitle string**

Change line 8 of `banner.js`:

```js
// Before:
\x1b[90mv${version} · Claude Code Skills Installer\x1b[0m

// After:
\x1b[90mv${version} · Multi-Tool Skills Installer\x1b[0m
```

- [ ] **Step 2: Commit**

```bash
git add installer/src/banner.js
git commit -m "chore(installer): update banner subtitle to Multi-Tool Skills Installer"
```

---

### Task 9: Wire everything in `cli.js`

**Files:**
- Modify: `installer/src/cli.js`

- [ ] **Step 1: Replace cli.js content**

```js
// installer/src/cli.js
import { intro, outro, cancel, isCancel, log } from '@clack/prompts'
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { printBanner } from './banner.js'
import { selectScope } from './scope.js'
import { pickInstallables } from './picker.js'
import { installSelected } from './install.js'
import { checkForUpdates } from './update.js'
import { selectTools, getToolTargets } from './tools.js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const { version } = JSON.parse(readFileSync(join(__dirname, '..', 'package.json'), 'utf8'))

export async function run() {
  printBanner(version)
  await checkForUpdates()

  intro('SkillKit Installer')

  const selectedTools = await selectTools()
  if (isCancel(selectedTools)) { cancel('Cancelled.'); process.exit(0) }

  const scope = await selectScope(selectedTools)
  if (isCancel(scope)) { cancel('Cancelled.'); process.exit(0) }

  const selected = await pickInstallables()
  if (isCancel(selected)) { cancel('Cancelled.'); process.exit(0) }

  const targets = getToolTargets(selectedTools, scope)
  const { results, totalInstalled } = await installSelected(selected, targets)

  const targetLabels = results
    .filter(r => r.installed > 0)
    .map(r => `${r.target.name} (${r.target.scope})`)
    .join(', ')

  outro(`Done! ${totalInstalled} item(s) installed to ${targetLabels || 'no targets'}.`)
  log.info('Restart your coding agent tools to pick up new skills.')
}
```

- [ ] **Step 2: Commit**

```bash
git add installer/src/cli.js
git commit -m "feat(installer): wire multi-tool selection into CLI flow"
```

---

### Task 10: Update integration test

**Files:**
- Modify: `installer/tests/integration.test.js`

- [ ] **Step 1: Add `tools.js` to the module existence check**

Replace the `'All source modules exist...'` test body:

```js
test('All source modules exist and export expected functions', async () => {
  const banner = await import('../src/banner.js')
  const scope = await import('../src/scope.js')
  const picker = await import('../src/picker.js')
  const install = await import('../src/install.js')
  const update = await import('../src/update.js')
  const tools = await import('../src/tools.js')

  assert.ok(banner.printBanner, 'banner exports printBanner')
  assert.ok(scope.selectScope, 'scope exports selectScope')
  assert.ok(picker.pickInstallables, 'picker exports pickInstallables')
  assert.ok(install.installSelected, 'install exports installSelected')
  assert.ok(update.checkForUpdates, 'update exports checkForUpdates')
  assert.ok(tools.selectTools, 'tools exports selectTools')
  assert.ok(tools.getToolTargets, 'tools exports getToolTargets')
})
```

- [ ] **Step 2: Run full test suite**

```bash
cd installer && node --test src/**/*.test.js tests/**/*.test.js
```

Expected: all tests pass

- [ ] **Step 3: Final commit**

```bash
git add installer/tests/integration.test.js
git commit -m "test(installer): add tools.js to integration module check"
```

---

## Verification

After all tasks complete, run the full suite one final time:

```bash
cd installer && node --test src/**/*.test.js tests/**/*.test.js
```

All tests must pass with zero failures before declaring done.
