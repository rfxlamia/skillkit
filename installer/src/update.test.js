import { test } from 'node:test'
import assert from 'node:assert'
import { isNpxExecution } from './update.js'

test('isNpxExecution returns true when npm_execpath includes npx', () => {
  const original = process.env.npm_execpath
  process.env.npm_execpath = '/usr/local/lib/node_modules/npm/bin/npx-cli.js'
  assert.strictEqual(isNpxExecution(), true)
  process.env.npm_execpath = original
})

test('isNpxExecution returns false when npm_execpath does not include npx', () => {
  const original = process.env.npm_execpath
  process.env.npm_execpath = '/usr/local/lib/node_modules/npm/bin/npm-cli.js'
  assert.strictEqual(isNpxExecution(), false)
  process.env.npm_execpath = original
})

test('isNpxExecution returns false when npm_execpath is undefined', () => {
  const original = process.env.npm_execpath
  delete process.env.npm_execpath
  assert.strictEqual(isNpxExecution(), false)
  process.env.npm_execpath = original
})
