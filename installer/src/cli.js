// installer/src/cli.js
import { intro, outro, cancel, isCancel, log } from '@clack/prompts'
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { printBanner } from './banner.js'
import { selectScope } from './scope.js'
import { pickInstallables } from './picker.js'
import { installSelected } from './install.js'
import { checkForUpdates } from './update.js'
import { selectTools, getToolTargets } from './tools.js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const { version } = JSON.parse(readFileSync(join(__dirname, '..', 'package.json'), 'utf8'))

export async function run() {
  printBanner(version)
  await checkForUpdates()

  intro('SkillKit Installer')

  const selectedTools = await selectTools()
  if (isCancel(selectedTools)) { cancel('Cancelled.'); process.exit(0) }

  const scope = await selectScope(selectedTools)
  if (isCancel(scope)) { cancel('Cancelled.'); process.exit(0) }

  const selected = await pickInstallables()
  if (isCancel(selected)) { cancel('Cancelled.'); process.exit(0) }

  const targets = getToolTargets(selectedTools, scope)
  const { results, totalInstalled } = await installSelected(selected, targets)

  const targetLabels = results
    .filter(r => r.installed > 0)
    .map(r => `${r.target.name} (${r.target.scope})`)
    .join(', ')

  outro(`Done! ${totalInstalled} item(s) installed to ${targetLabels || 'no targets'}.`)
  log.info('Restart your coding agent tools to pick up new skills.')
}
