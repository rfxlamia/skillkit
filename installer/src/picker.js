import { multiselect, select, log } from '@clack/prompts'
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const manifest = JSON.parse(readFileSync(join(__dirname, '..', 'skills-manifest.json'), 'utf8'))

const CATEGORY_ICONS = {
  core: '⚙️',
  engineering: '🧠',
  documentation: '📖',
  planning: '📐',
  deployment: '🚀',
  productivity: '📊',
  quality: '🛡️',
  security: '🔒',
  experimentation: '🧪',
  'agent-frameworks': '🤖',
  creative: '✍️',
  uncategorized: '  '
}

export function getCategoryDisplay(skill) {
  const icon = CATEGORY_ICONS[skill.category] || CATEGORY_ICONS.uncategorized
  const label = skill.category ? skill.category.replace(/-/g, ' ') : ''
  return `${icon} ${label}`
}

export async function pickInstallables() {
  const mode = await select({
    message: 'What to install?',
    options: [
      { value: 'all', label: `Everything (${manifest.skills.length} skills + ${manifest.agents.length} agents)` },
      { value: 'skills-only', label: 'All skills only' },
      { value: 'agents-only', label: 'All agents only' },
      { value: 'pick', label: 'Let me choose...' }
    ]
  })

  if (mode === 'all') return { skills: manifest.skills, agents: manifest.agents }
  if (mode === 'skills-only') return { skills: manifest.skills, agents: [] }
  if (mode === 'agents-only') return { skills: [], agents: manifest.agents }

  const sortedSkills = [...manifest.skills].sort((a, b) => {
    if (a.name === 'skillkit') return -1
    if (b.name === 'skillkit') return 1
    return a.name.localeCompare(b.name)
  })

  const skillChoices = sortedSkills.map(s => ({
    value: s.name,
    label: `${getCategoryDisplay(s)} ${s.name}`,
    hint: s.description.slice(0, 60) + (s.description.length > 60 ? '…' : '')
  }))

  const agentChoices = manifest.agents.map(a => ({
    value: a.name,
    label: `🤝 ${a.name}`,
    hint: a.description.slice(0, 60) + (a.description.length > 60 ? '…' : '')
  }))

  const selectedSkills = await multiselect({
    message: 'Select skills to install: (space to toggle, a to select all)',
    options: skillChoices,
    required: false
  })

  const selectedAgents = await multiselect({
    message: 'Select agents to install:',
    options: agentChoices,
    required: false
  })

  return {
    skills: sortedSkills.filter(s => selectedSkills.includes(s.name)),
    agents: manifest.agents.filter(a => selectedAgents.includes(a.name))
  }
}
