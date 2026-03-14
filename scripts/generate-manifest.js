#!/usr/bin/env node
import { readdirSync, readFileSync, writeFileSync } from 'fs'
import { join, resolve } from 'path'

const root = resolve('.')

// Skills: read name + description + category from SKILL.md frontmatter
const skills = readdirSync(join(root, 'skills'))
  .filter(d => !d.startsWith('.'))
  .map(name => {
    let description = ''
    let category = 'uncategorized'
    try {
      const content = readFileSync(join(root, 'skills', name, 'SKILL.md'), 'utf8')
      // Extract description from frontmatter
      const descMatch = content.match(/^description:\s*[>|]?\s*\n?(.*)/m)
      if (descMatch) description = descMatch[1].trim().replace(/^["']|["']$/g, '')
      // Extract category from frontmatter
      const catMatch = content.match(/^category:\s*(\w+)/m)
      if (catMatch) category = catMatch[1].trim()
    } catch {}
    return { name, description, category, type: 'skill', path: `skills/${name}` }
  })

// Agents: read name from filename + description from frontmatter
const agents = readdirSync(join(root, 'agents'))
  .filter(f => f.endsWith('.md') || f.endsWith('.mdx'))
  .map(file => {
    const name = file.replace(/\.mdx?$/, '')
    let description = ''
    try {
      const content = readFileSync(join(root, 'agents', file), 'utf8')
      const match = content.match(/description:\s*"?([^"\n]+)"?/)
      if (match) description = match[1].trim()
    } catch {}
    return { name, description, type: 'agent', path: `agents/${file}` }
  })

const manifest = { skills, agents, generatedAt: new Date().toISOString() }
writeFileSync(join(root, 'installer', 'skills-manifest.json'), JSON.stringify(manifest, null, 2))
console.log(`Generated manifest: ${skills.length} skills, ${agents.length} agents`)
