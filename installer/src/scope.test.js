// installer/src/scope.test.js
import { test } from 'node:test'
import assert from 'node:assert'
import { selectScope } from './scope.js'

test('selectScope is an async function', () => {
  const AsyncFunction = (async () => {}).constructor
  assert.ok(selectScope instanceof AsyncFunction)
})

test('getUserScope and getProjectScope are no longer exported', async () => {
  const mod = await import('./scope.js')
  assert.strictEqual(mod.getUserScope, undefined)
  assert.strictEqual(mod.getProjectScope, undefined)
})
