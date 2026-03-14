import { test } from 'node:test'
import assert from 'node:assert'
import { homedir } from 'os'
import { join } from 'path'
import { getUserScope, getProjectScope } from './scope.js'

test('getUserScope returns correct paths', () => {
  const scope = getUserScope()
  assert.strictEqual(scope.scope, 'user')
  assert.strictEqual(scope.skillsDir, join(homedir(), '.claude', 'skills'))
  assert.strictEqual(scope.agentsDir, join(homedir(), '.claude', 'agents'))
})

test('getProjectScope returns correct paths', () => {
  const scope = getProjectScope()
  assert.strictEqual(scope.scope, 'project')
  assert.strictEqual(scope.skillsDir, join(process.cwd(), '.claude', 'skills'))
  assert.strictEqual(scope.agentsDir, join(process.cwd(), '.claude', 'agents'))
})
