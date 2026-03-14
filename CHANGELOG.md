# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
