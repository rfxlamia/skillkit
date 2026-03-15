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
