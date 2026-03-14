import { test } from 'node:test'
import assert from 'node:assert'
import { mkdtempSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'fs'
import { join } from 'path'
import { tmpdir } from 'os'
import { installSelected } from './install.js'

function createTempDir() {
  return mkdtempSync(join(tmpdir(), 'skillkit-test-'))
}

test('installSelected validates skills is an array', async () => {
  await assert.rejects(
    installSelected({ skills: 'not-array', agents: [] }, { skillsDir: '/tmp', agentsDir: '/tmp' }),
    /skills must be an array/
  )
})

test('installSelected validates agents is an array', async () => {
  await assert.rejects(
    installSelected({ skills: [], agents: 'not-array' }, { skillsDir: '/tmp', agentsDir: '/tmp' }),
    /agents must be an array/
  )
})

test('installSelected skips invalid skill objects', async () => {
  const skillsDir = createTempDir()
  const agentsDir = createTempDir()

  const result = await installSelected(
    { skills: [{ name: null }, { name: 'valid', path: 'skills/valid' }], agents: [] },
    { skillsDir, agentsDir }
  )

  assert.strictEqual(result.installed, 0)
  assert.strictEqual(result.skipped.length, 2)

  rmSync(skillsDir, { recursive: true })
  rmSync(agentsDir, { recursive: true })
})
