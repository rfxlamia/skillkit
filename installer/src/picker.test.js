import { test } from 'node:test'
import assert from 'node:assert'
import { getCategoryDisplay } from './picker.js'

test('getCategoryDisplay returns icon and category label', () => {
  const skill = { name: 'test-skill', category: 'creative' }
  const result = getCategoryDisplay(skill)
  assert.strictEqual(result, '✍️ creative')
})

test('getCategoryDisplay handles uncategorized skills', () => {
  const skill = { name: 'test-skill', category: 'unknown-category' }
  const result = getCategoryDisplay(skill)
  assert.strictEqual(result, '   unknown category')
})

test('getCategoryDisplay handles missing category', () => {
  const skill = { name: 'test-skill' }
  const result = getCategoryDisplay(skill)
  assert.strictEqual(result, '   ')
})
