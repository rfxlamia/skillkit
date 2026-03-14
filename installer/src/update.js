import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { log, select } from '@clack/prompts'

const __dirname = dirname(fileURLToPath(import.meta.url))
const pkg = JSON.parse(readFileSync(join(__dirname, '..', 'package.json'), 'utf8'))

export async function checkForUpdates() {
  // npx always runs latest — no need to check
  if (process.env.npm_execpath?.includes('npx')) return

  try {
    const res = await fetch(`https://registry.npmjs.org/@rfxlamia/skillkit/latest`)
    if (!res.ok) {
      if (process.env.DEBUG) log.warn(`Update check failed: HTTP ${res.status}`)
      return
    }
    const { version: latest } = await res.json()

    if (latest !== pkg.version) {
      log.warn(`Update available: ${pkg.version} → ${latest}`)
      log.info(`Run: npx @rfxlamia/skillkit@latest install`)
    }
  } catch (err) {
    // Network unavailable or other errors — log in debug mode
    if (process.env.DEBUG) log.warn(`Update check failed: ${err.message}`)
  }
}

// Export for testing
export function isNpxExecution() {
  return process.env.npm_execpath?.includes('npx') ?? false
}
