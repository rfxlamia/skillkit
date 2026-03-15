// installer/src/install.test.js
import { test } from 'node:test'
import assert from 'node:assert'
import { mkdtempSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'fs'
import { join, dirname } from 'path'
import { tmpdir } from 'os'
import { fileURLToPath } from 'url'
import { installSelected } from './install.js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PACKAGE_ROOT = join(__dirname, '..')

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

test('installSelected copies skill directory to destination (happy path)', async () => {
  // Create a source skill directory inside PACKAGE_ROOT (same as install.js uses)
  const fixtureDir = join(PACKAGE_ROOT, '.test-fixture', 'my-test-skill')
  mkdirSync(fixtureDir, { recursive: true })
  writeFileSync(join(fixtureDir, 'SKILL.md'), '# Test Skill')

  const destDir = createTempDir()

  const { totalInstalled, results } = await installSelected(
    { skills: [{ name: 'my-test-skill', path: '.test-fixture/my-test-skill' }], agents: [] },
    [makeTarget(destDir, null)]
  )

  assert.strictEqual(totalInstalled, 1)
  assert.strictEqual(results[0].installed, 1)
  assert.ok(existsSync(join(destDir, 'my-test-skill', 'SKILL.md')))

  rmSync(join(PACKAGE_ROOT, '.test-fixture'), { recursive: true })
  rmSync(destDir, { recursive: true })
})
