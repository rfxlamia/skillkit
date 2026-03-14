import { select, log } from '@clack/prompts'
import { homedir } from 'os'
import { join } from 'path'
import { existsSync } from 'fs'

export async function selectScope() {
  const userSkillsPath = join(homedir(), '.claude', 'skills')
  const projectSkillsPath = join(process.cwd(), '.claude', 'skills')
  const projectExists = existsSync(join(process.cwd(), '.claude', 'skills'))

  const scope = await select({
    message: 'Install to:',
    options: [
      {
        value: 'user',
        label: `User scope  ~/.claude/skills/`,
        hint: 'available in all projects'
      },
      {
        value: 'project',
        label: `Project scope  ./.claude/skills/`,
        hint: projectExists ? 'detected .claude/skills/ here' : `will create ${projectSkillsPath}`
      }
    ]
  })

  if (scope === 'user') {
    return {
      scope: 'user',
      skillsDir: userSkillsPath,
      agentsDir: join(homedir(), '.claude', 'agents')
    }
  }

  return {
    scope: 'project',
    skillsDir: projectSkillsPath,
    agentsDir: join(process.cwd(), '.claude', 'agents')
  }
}

// Export for testing
export function getUserScope() {
  return {
    scope: 'user',
    skillsDir: join(homedir(), '.claude', 'skills'),
    agentsDir: join(homedir(), '.claude', 'agents')
  }
}

export function getProjectScope() {
  return {
    scope: 'project',
    skillsDir: join(process.cwd(), '.claude', 'skills'),
    agentsDir: join(process.cwd(), '.claude', 'agents')
  }
}
