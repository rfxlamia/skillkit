// installer/src/tools.js
import { multiselect } from '@clack/prompts'
import { homedir } from 'os'
import { join } from 'path'

export async function selectTools() {
  return multiselect({
    message: 'Install to which tools?',
    options: [
      { value: 'claude-code', label: 'Claude Code', hint: '~/.claude/skills/' },
      { value: 'opencode', label: 'OpenCode', hint: '~/.config/opencode/skills/' },
      { value: 'codex', label: 'Codex', hint: '~/.agents/skills/' },
      { value: 'copilot', label: 'GitHub Copilot', hint: '~/.copilot/skills/' }
    ],
    required: true
  })
}

export function getToolTargets(selectedTools, scope) {
  if (!selectedTools.length) return []

  const home = homedir()
  const cwd = process.cwd()
  const isUser = scope === 'user'

  const resolve = {
    'claude-code': {
      name: 'Claude Code',
      scope,
      skillsDir: isUser ? join(home, '.claude', 'skills') : join(cwd, '.claude', 'skills'),
      agentsDir: isUser ? join(home, '.claude', 'agents') : join(cwd, '.claude', 'agents')
    },
    'opencode': {
      name: 'OpenCode',
      scope,
      skillsDir: isUser
        ? join(home, '.config', 'opencode', 'skills', 'skillkit')
        : join(cwd, '.opencode', 'skills'),
      agentsDir: isUser
        ? join(home, '.config', 'opencode', 'agents')
        : join(cwd, '.opencode', 'agents')
    },
    'codex': {
      name: 'Codex',
      scope: 'user',
      skillsDir: join(home, '.agents', 'skills', 'skillkit'),
      agentsDir: null
    },
    'copilot': {
      name: 'GitHub Copilot',
      scope: isUser ? 'user' : 'project',
      skillsDir: join(home, '.copilot', 'skills'),
      agentsDir: isUser
        ? join(home, '.claude', 'agents')
        : join(cwd, '.github', 'agents')
    }
  }

  const targets = selectedTools
    .filter(id => resolve[id])
    .map(id => ({ ...resolve[id] }))

  // Dedup: if skillsDir or agentsDir appears more than once, null it in later targets
  const seenSkills = new Set()
  const seenAgents = new Set()

  for (const t of targets) {
    if (seenSkills.has(t.skillsDir)) t.skillsDir = null
    else seenSkills.add(t.skillsDir)

    if (t.agentsDir && seenAgents.has(t.agentsDir)) t.agentsDir = null
    else if (t.agentsDir) seenAgents.add(t.agentsDir)
  }

  return targets.filter(t => t.skillsDir || t.agentsDir)
}
