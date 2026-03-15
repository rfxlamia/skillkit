# SkillKit

**Build custom skills for your AI workflow agent — and share them with thousands.**

SkillKit is an open toolkit for creating reusable skills that extend how your AI agent works. Works across Claude Code, OpenAI Codex, and other AI coding tools. Install community-built skills in seconds, or create your own in ~10 minutes and contribute them back.

> **Previously known as `claude-skillkit`.** All old links redirect here automatically.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.6-green.svg)](.claude-plugin/plugin.json)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=githubsponsors)](https://github.com/sponsors/rfxlamia)

---

## What is SkillKit?

SkillKit is a plugin for AI agents that provides a collection of **25 skills** and **7 subagents** designed to extend Claude's capabilities across content creation, engineering frameworks, security testing, and more.

At its core, SkillKit includes a **meta-skill** (`skillkit`) that helps create and validate new skills/subagents using a dual-mode workflow:
- **Fast mode** for quick structural validation
- **Full mode** for structural + behavioral validation with TDD-style pressure testing

> Not sure what skills are or if you need one? Run `/skillkit-help` first.
> Ready to build? Run `/skillkit`.

---

## Installation

```bash
npx @rfxlamia/skillkit
```

Interactive installer — pick skills/agents, choose user or project scope. Done.

<details>
<summary>Other install methods</summary>
**Manual (Clone + Copy)**

```bash
git clone https://github.com/rfxlamia/skillkit.git
cp -r skillkit/skills/. ~/.claude/skills/
cp skillkit/agents/. ~/.claude/agents/
```

**Plugin Marketplace (Currently Broken)**

> **⚠️ Known issue:** Installation via the Claude Code plugin marketplace is currently broken. The `disable-model-invocation` error prevents skills from being invoked after install. Use `npx` instead.

</details>

---

## Create Your First Skill

1. Install SkillKit: `npx @rfxlamia/skillkit`
2. Run `/skillkit-help` and follow the guided path — you'll have a working skill in ~10 minutes
3. Submit a PR to share it with the community

[Starter template](skills/skillkit-help/template/SKILL.md) · [Contribution guide](.github/PULL_REQUEST_TEMPLATE/skill_submission.md)

---

## Skills Catalog

<details>
<summary>25 skills — click to expand</summary>

| # | Skill | Description |
|---|-------|-------------|
| 1 | **skillkit** | Meta-skill for creating new skills and subagents with dual-mode (12-step fast, 15-step full) workflow |
| 2 | **skillkit-help** | Pre-build orientation for skill creators — understand what skills are, decide skills vs subagents, validate an existing skill |
| 3 | **prompt-engineering** | Select optimal prompting methods (CoT, Few-Shot, ReAct, ToT) and output formats based on task complexity |
| 4 | **creative-copywriting** | Persuasive social media writing with 150+ psychological triggers, hook formulas, and storytelling frameworks |
| 5 | **social-media-seo** | Optimize social media content for discoverability with 100+ formula databases across Instagram, X/Twitter, and Threads |
| 6 | **thread-pro** | Transform content into viral threads with strong hooks and relatable voice for X/Twitter and Threads |
| 7 | **humanize-docs** | Transform AI-to-AI documentation into human-readable prose with personality |
| 8 | **imagine** | Prepare detailed prompts for Google Imagen 3/4 image generation with technical photography specs |
| 9 | **storyteller** | Transform abstract narratives into concrete visual story structures |
| 10 | **screenwriter** | Create production-ready screenplays optimized for AI video generation pipelines |
| 11 | **diverse-content-gen** | Generate diverse creative content using Verbalized Sampling (1.6-2.1x diversity increase) |
| 12 | **coolhunter** | Trend intelligence and cultural signal detection for emerging behaviors |
| 13 | **framework-critical-thinking** | Build AI agents with critical thinking, metacognition, and self-verification capabilities |
| 14 | **framework-initiative** | STAR framework for agents to understand implicit intent and think before acting |
| 15 | **baby-education** | Explain concepts with extreme clarity using analogies-first approach and ELI5 style |
| 16 | **readme-expert** | Create README files with anti-hallucination validation and codebase-grounded accuracy |
| 17 | **red-teaming** | Adversarial security testing methodology for cybersecurity and AI/LLM systems |
| 18 | **tinkering** | Safe experimentation framework with isolated sandboxes for prototyping and technical spikes |
| 19 | **quick-spec** | Create implementation-ready technical specifications through conversational discovery and code investigation |
| 20 | **pre-deploy-checklist** | Intelligent pre-deployment QA checklist generator with parallel domain subagent analysis |
| 21 | **been-there-done-that** | Document developer progress objectively after sprints with git session detection and factual logging |
| 22 | **adversarial-review** | Adversarial review protocol with mandatory bug quota, reality validation, and structured resolution paths |
| 23 | **releasing** | Automate release workflow: version bumping, changelog generation, git tagging, and GitHub releases |
| 24 | **validate-plan** | Validate implementation plans against DRY, YAGNI, TDD principles before execution |
| 25 | **verify-before-ship** | Enforce 7 production safety gates with evidence before deployment |

</details>

## Subagents Catalog

<details>
<summary>7 subagents — click to expand</summary>

| # | Subagent | Description |
|---|----------|-------------|
| 1 | **seo-manager** | Social media SEO content orchestration with platform-specific optimization |
| 2 | **creative-copywriter** | Psychology-backed creative copywriting for social media |
| 3 | **red-team** | Security testing, threat modeling, adversary emulation, and vulnerability assessment |
| 4 | **doc-simplifier** | Documentation condensing that removes verbosity while preserving clarity |
| 5 | **sam-altman** | Velocity-first, market-driven decision-making and aggressive execution strategies |
| 6 | **dario-amodei** | Safety-first decision-making with transparency, intellectual rigor, and democratic oversight |
| 7 | **kotlin-pro** | Kotlin code review, refactoring, and coroutines/Flow optimization |

</details>

---

## Core: SkillKit Creator

The `skillkit` skill is the engine that powers creation of new skills and subagents.

| Trigger | Workflow | Steps |
|---------|----------|-------|
| `create skill` | Full skill creation | 12 steps with research + validation |
| `create subagent` | Subagent creation | 8 steps with template-based workflow |
| `validate skill` | Validation only | Structure, references, quality checks |
| `Skills vs Subagents` | Decision helper | Recommends approach, then creates |
| `convert doc to skill` | Migration | Transform existing docs into skills |

Quality target: **9.0+/10** via 5-layer validation and multi-proposal generation.

---

## Automation Scripts

14 Python scripts in `skills/skillkit/scripts/` — all support `--format {text|json}`.

<details>
<summary>View all scripts</summary>

| Script | Purpose |
|--------|---------|
| `init_skill.py` | Initialize new skill directory structure |
| `init_subagent.py` | Initialize new subagent with YAML template |
| `validate_skill.py` | Structure and YAML validation |
| `token_estimator.py` | Token consumption and cost estimation |
| `split_skill.py` | Progressive disclosure auto-splitting |
| `pattern_detector.py` | Workflow pattern recommendation |
| `pattern_detector_new.py` | Enhanced pattern detection |
| `decision_helper.py` | Skills vs Subagents decision tree |
| `security_scanner.py` | Security vulnerability detection |
| `test_generator.py` | Automated test generation |
| `quality_scorer.py` | 5-category quality scoring (100 points) |
| `migration_helper.py` | Document to skill conversion |
| `package_skill.py` | Package skill for distribution |
| `quick_validate.py` | Quick validation checks |

</details>

---

## Screenshots

<!-- TODO: Replace with actual screenshots -->
**CLI installer**
![installer](docs/images/installer.png)

**Guided orientation**
![skillkit-help](docs/images/skillkit-help.png)

**A finished skill**
![skill](docs/images/skill.png)

---

## Knowledge Base

23 knowledge files in `skills/skillkit/knowledge/` — see [`INDEX.md`](skills/skillkit/knowledge/INDEX.md) for the full navigation guide.

---

## License

[Apache 2.0](LICENSE) - Copyright 2025 rfxlamia
