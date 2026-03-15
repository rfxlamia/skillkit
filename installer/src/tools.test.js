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
