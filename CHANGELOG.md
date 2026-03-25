# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [3.0.0] - 2026-03-25

### Changed
- **BREAKING:** Community skills (24) and agents (7) moved to [SkillKit Marketplace](https://github.com/skillkit-marketplace/skills)
- Installer simplified to core skills only (`skillkit` + `skillkit-help`)
- For community skills & agents, use `npx @rfxlamia/sm`

### Removed
- Bundles system
- 24 community skills (now in marketplace)
- 7 agents (now in marketplace)

---

## [2.6.0] - 2026-03-24

### Added
- Unified `init.py` script with subcommand pattern (`skill` and `subagent` subcommands)
- Enhanced `validate_skill.py` with `--security-only`, `--tokens-only`, `--structure-only` flags
- Comprehensive test suite: `test_consolidation.py` with 17 tests

### Changed
- Consolidated 6 scripts into 2: `init_skill.py` + `init_subagent.py` → `init.py`, `security_scanner.py` + `token_estimator.py` → `validate_skill.py`
- Deprecated old scripts with clear migration warnings
- Updated all documentation references to use new commands
- ~800 lines of code saved through consolidation

---

## [2.5.2] - 2026-03-22

### Fixed
- `section-2-fast-creation-workflow.md` and `section-2-full-creation-workflow.md`: add `decision_answer.json` format documentation to STEP 0 so agents know the required JSON structure when using Mode 1 of `decision_helper.py`

## [2.5.1] - 2026-03-21

### Fixed
- `package_skill.py`: default output now saves `.skill` file inside the skill's own folder instead of CWD or parent directory
- `package_skill.py`: added `*.skill` exclusion filter to prevent self-inclusion on subsequent packaging runs
- `package_skill.py`: success message now shows absolute path and claude.ai usage hint
- `package_skill.py`: removed dead `is_project_directory()` function (was no longer reachable)

---

## [2.5.0] - 2026-03-16

### Added
- `section-2-fast-creation-workflow.md`: dedicated reference file for fast mode creation workflow (12 steps, 4 phases), making fast and full modes equally documented

### Changed
- `skillkit` SKILL.md: rewritten for symmetry — both Workflow A (fast) and Workflow B (full) now use identical summary+pointer format pointing to their respective reference files
- `skillkit` SKILL.md: frontmatter description updated with explicit WHAT/WHEN/triggers for better routing
- `skillkit` SKILL.md: reduced from 511 to 426 lines (bloat reduction, removed inline Python code block, condensed Section 8)
- `section-4-decision-workflow-skills-vs-subagents.md`: bash invocation block moved here from SKILL.md inline
- Quality score improved from 5.5/10 to 7.0/10

---

## [2.4.0] - 2026-03-15

### Added
- `skillkit-help` skill: pre-build orientation for new skill creators (understand skills, decide skills vs subagents, validate existing skills)
- Starter template at `skills/skillkit-help/template/SKILL.md` for first-time creators
- GitHub PR submission template at `.github/PULL_REQUEST_TEMPLATE/skill_submission.md`
- `sortSkills` exported pure function in installer picker (testable, `skillkit-help` pinned second)

### Changed
- README hero rewritten to be platform-agnostic (works across Claude Code, Codex, and other AI coding tools)
- Added "Create Your First Skill" onboarding section to README
- Skills catalog updated to 25 skills

---

## [2.3.0] - 2026-03-15

### Added
- Multi-tool installer support: OpenCode, Codex, and GitHub Copilot alongside Claude Code
- `tools.js` module with `selectTools` UI and `getToolTargets` path resolver
- Deduplication logic for shared agent directories (Claude Code + Copilot)
- Codex always installs to user scope (`~/.agents/skills/skillkit/`) regardless of selection
- 10 unit tests for tool path resolution, 1 happy-path install test

### Changed
- Installer subtitle updated to "Multi-Tool Skills Installer"
- `skillkit` skill now appears first in the manual picker list
- Everything label now shows dynamic skill/agent counts
- `selectScope` returns a plain string instead of a path object
- `installSelected` accepts a `targets[]` array, returns `{ results[], totalInstalled }`

### Removed
- `releasing-skillkit` skill (moved to local user skills)
- `getUserScope` / `getProjectScope` helpers from `scope.js`

## [2.2.0] - 2026-03-15

### Added
- Interactive CLI installer published as `@rfxlamia/skillkit` on npm
- ASCII banner with version display
- User vs Project scope selection for skill installation
- Interactive skills/agents picker with category icons
- File copy engine for installing skills to `~/.claude/skills/` or `./.claude/skills/`
- Update checker (skips for npx runs)
- 11 unit tests + 3 integration tests for installer
- GitHub Actions CI workflow for installer testing
- Category metadata added to all 24 skill frontmatters

### Changed
- Updated README installation section to recommend `npx @rfxlamia/skillkit`

## [2.1.5] - 2026-03-14

### Fixed
- Add plugin.json to skills/skillkit/.claude-plugin/ for proper plugin metadata
- Commands, skills, and plugin.json now properly colocated

## [2.1.4] - 2026-03-14

### Fixed
- Move commands/ folder to skills/skillkit/ for proper plugin discovery

## [2.1.3] - 2026-03-14

### Fixed
- Add commands/ folder for slash command registration (/skillkit, /verify, /validate-plan)
- Fix bundle structure to include actual skill files instead of broken relative paths
- Fix frameworks bundle missing all skills (now has 4 skills + references)
- Fix essentials bundle (now has 9 skills + references)
- Fix creative bundle (now has 6 skills + references)
- Fix subagents bundle (now has 7 agent files)

### Added
- Plugin installation test script (scripts/test-plugin-install.sh)

### Summary
Plugin structure completely rebuilt. All bundles now contain actual skill files instead of broken relative path references. Slash commands now work with commands/ folder.

## [2.1.2] - 2025-03-14

### Added
- feat: add releasing, validate-plan, and verify-before-ship skills (2680b2a)

### Summary
3 new skills added: releasing (automated release workflow with semver support), validate-plan (DRY/YAGNI/TDD plan validation), and verify-before-ship (7 production safety gates). Total: 24 skills and 7 subagents.

## [2.1.1] - 2025-03-14

### Changed
- chore: rename claude-skillkit to skillkit in plugin.json, marketplace.json, and README (f66599b)
- chore: update repo URLs in bundle READMEs to skillkit (dd5e5ca)
- chore: update repo references in skills/ to skillkit (75c73b8)

### Summary
Repository renamed from `claude-skillkit` to `skillkit` for model-agnostic positioning. All URLs and references updated. Old links redirect automatically.

## [2.1.0] - 2025-03-13

### Added
- feat: bump to v2.1.0 and update behavioral guide (900eb13)
- chore: bump version to 2.1.0 (ba42822)

### Summary
Full Mode Behavioral Testing Protocol with TDD-style RED-GREEN-REFACTOR cycle, deprecates legacy pressure_tester.py in favor of subagent-based pressure testing.
