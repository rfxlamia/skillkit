import { cpSync, mkdirSync, existsSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { spinner, log } from '@clack/prompts'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PACKAGE_ROOT = join(__dirname, '..')

export async function installSelected({ skills, agents }, { skillsDir, agentsDir }) {
  // Validate inputs
  if (!Array.isArray(skills)) throw new TypeError('skills must be an array')
  if (!Array.isArray(agents)) throw new TypeError('agents must be an array')

  const s = spinner()
  s.start('Installing...')

  let installed = 0
  const skipped = []

  for (const skill of skills) {
    if (!skill.name || !skill.path) {
      skipped.push(`invalid-skill-${installed}`)
      continue
    }
    const src = join(PACKAGE_ROOT, skill.path)
    const dest = join(skillsDir, skill.name)
    if (!existsSync(src)) { skipped.push(skill.name); continue }
    mkdirSync(dest, { recursive: true })
    cpSync(src, dest, { recursive: true })
    installed++
  }

  for (const agent of agents) {
    if (!agent.name || !agent.path) {
      skipped.push(`invalid-agent-${installed}`)
      continue
    }
    const src = join(PACKAGE_ROOT, agent.path)
    const dest = join(agentsDir, agent.name + '.md')
    if (!existsSync(src)) { skipped.push(agent.name); continue }
    mkdirSync(agentsDir, { recursive: true })
    cpSync(src, dest)
    installed++
  }

  s.stop(`Installed ${installed} item(s)`)

  if (skipped.length > 0) {
    log.warn(`Skipped (not found in package): ${skipped.join(', ')}`)
  }

  return { installed, skipped }
}
