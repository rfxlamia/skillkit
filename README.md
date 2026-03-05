# Claude SkillKit

> Professional skill creation with research-driven workflow and automated validation. Features dual-mode workflow (fast/full), behavioral validation, and multi-layer quality gates for achieving 9.0/10+ quality scores.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](.claude-plugin/plugin.json)

---

## Table of Contents

- [What is Claude SkillKit?](#what-is-claude-skillkit)
- [Skills Catalog](#skills-catalog)
- [Subagents Catalog](#subagents-catalog)
- [Core: SkillKit Creator](#core-skillkit-creator)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Automation Scripts](#automation-scripts)
- [Knowledge Base](#knowledge-base)
- [Project Structure](#project-structure)
- [License](#license)

---

## What is Claude SkillKit?

Claude SkillKit v2 is a plugin for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that provides a collection of **21 skills** and **7 subagents** designed to extend Claude's capabilities across content creation, engineering frameworks, security testing, and more.

At its core, SkillKit v2 includes a **meta-skill** (`skillkit`) that helps create and validate new skills/subagents using a dual-mode workflow:
- **Fast mode** for quick structural validation
- **Full mode** for structural + behavioral validation with TDD-style pressure testing

In short, SkillKit v2 is a practical system for building reliable Claude capabilities with repeatable quality gates, not just a template pack.

---

## Skills Catalog

| # | Skill | Description |
|---|-------|-------------|
| 1 | **skillkit** | Meta-skill for creating new skills and subagents with dual-mode (12-step fast, 15-step full) workflow |
| 2 | **prompt-engineering** | Select optimal prompting methods (CoT, Few-Shot, ReAct, ToT) and output formats based on task complexity |
| 3 | **creative-copywriting** | Persuasive social media writing with 150+ psychological triggers, hook formulas, and storytelling frameworks |
| 4 | **social-media-seo** | Optimize social media content for discoverability with 100+ formula databases across Instagram, X/Twitter, and Threads |
| 5 | **thread-pro** | Transform content into viral threads with strong hooks and relatable voice for X/Twitter and Threads |
| 6 | **humanize-docs** | Transform AI-to-AI documentation into human-readable prose with personality |
| 7 | **imagine** | Prepare detailed prompts for Google Imagen 3/4 image generation with technical photography specs |
| 8 | **storyteller** | Transform abstract narratives into concrete visual story structures |
| 9 | **screenwriter** | Create production-ready screenplays optimized for AI video generation pipelines |
| 10 | **diverse-content-gen** | Generate diverse creative content using Verbalized Sampling (1.6-2.1x diversity increase) |
| 11 | **coolhunter** | Trend intelligence and cultural signal detection for emerging behaviors |
| 12 | **framework-critical-thinking** | Build AI agents with critical thinking, metacognition, and self-verification capabilities |
| 13 | **framework-initiative** | STAR framework for agents to understand implicit intent and think before acting |
| 14 | **baby-education** | Explain concepts with extreme clarity using analogies-first approach and ELI5 style |
| 15 | **readme-expert** | Create README files with anti-hallucination validation and codebase-grounded accuracy |
| 16 | **red-teaming** | Adversarial security testing methodology for cybersecurity and AI/LLM systems |
| 17 | **tinkering** | Safe experimentation framework with isolated sandboxes for prototyping and technical spikes |
| 18 | **quick-spec** | Create implementation-ready technical specifications through conversational discovery and code investigation |
| 19 | **pre-deploy-checklist** | Intelligent pre-deployment QA checklist generator with parallel domain subagent analysis |
| 20 | **been-there-done-that** | Document developer progress objectively after sprints with git session detection and factual logging |
| 21 | **adversarial-review** | Adversarial review protocol with mandatory bug quota, reality validation, and structured resolution paths |

---

## Subagents Catalog

| # | Subagent | Description |
|---|----------|-------------|
| 1 | **seo-manager** | Social media SEO content orchestration with platform-specific optimization |
| 2 | **creative-copywriter** | Psychology-backed creative copywriting for social media |
| 3 | **red-team** | Security testing, threat modeling, adversary emulation, and vulnerability assessment |
| 4 | **doc-simplifier** | Documentation condensing that removes verbosity while preserving clarity |
| 5 | **sam-altman** | Velocity-first, market-driven decision-making and aggressive execution strategies |
| 6 | **dario-amodei** | Safety-first decision-making with transparency, intellectual rigor, and democratic oversight |
| 7 | **kotlin-pro** | Kotlin code review, refactoring, and coroutines/Flow optimization |

---

## Core: SkillKit Creator

The `skillkit` skill is the engine that powers creation of new skills and subagents.

### Workflows

| Trigger | Workflow | Steps |
|---------|----------|-------|
| `create skill` | Full skill creation | 12 steps with research + validation |
| `create subagent` | Subagent creation | 8 steps with template-based workflow |
| `validate skill` | Validation only | Structure, references, quality checks |
| `Skills vs Subagents` | Decision helper | Recommends approach, then creates |
| `convert doc to skill` | Migration | Transform existing docs into skills |

### Quality Targets

- Quality score: **9.0+/10**
- 5-layer validation with automated checks
- Research phase with 3-5 web searches before building
- Multi-proposal generation (3-5 design options)

---

## Installation

### As a Claude Code Plugin

```bash
claude plugin marketplace add rfxlamia/claude-skillkit
```

### Manual Installation

Clone the repository into your Claude Code skills directory:

```bash
git clone https://github.com/rfxlamia/claude-skillkit.git
```

Then reference the skills/agents in your Claude Code configuration.

---

## Quick Start

### Create a New Skill

```
/skillkit create skill "my-awesome-skill"
```

### Create a New Subagent

```
/skillkit create subagent "my-subagent"
```

### Validate an Existing Skill

```bash
python3 skills/skillkit/scripts/validate_skill.py path/to/skill/ --format json
```

### Decide: Skill vs Subagent?

```bash
python3 skills/skillkit/scripts/decision_helper.py "code review assistant"
```

---

## Automation Scripts

14 Python scripts in `skills/skillkit/scripts/` for skill lifecycle management:

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

All scripts support `--format {text|json}` for standardized output.

---

## Knowledge Base

23 knowledge files organized in `skills/skillkit/knowledge/`:

| Category | Files | Topics |
|----------|-------|--------|
| **Foundation** (01-08) | 8 files | Why skills exist, Skills vs Subagents comparison, decision trees, hybrid patterns, token economics, platform constraints, security, when not to use skills |
| **Application** (09-13) | 5 files | Case studies, technical architecture, adoption strategy, testing and validation, competitive landscape |
| **Tools** (14-23) | 10 files | Guides for each automation script |

See [`skills/skillkit/knowledge/INDEX.md`](skills/skillkit/knowledge/INDEX.md) for the full navigation guide.

---

## Project Structure

```
claude-skillkit/
├── .claude-plugin/
│   ├── plugin.json            # Plugin metadata (v1.3.0)
│   └── marketplace.json       # Marketplace listing
├── skills/
│   ├── skillkit/              # Meta-skill: create skills & subagents
│   │   ├── SKILL.md           # Main skill definition
│   │   ├── CHANGELOG.md       # Version history
│   │   ├── scripts/           # 14 automation scripts
│   │   ├── knowledge/         # 23 knowledge files
│   │   └── references/        # Workflow documentation
│   ├── prompt-engineering/    # Prompting method selector
│   ├── creative-copywriting/  # Social media copywriting
│   ├── social-media-seo/      # SEO optimization with databases
│   ├── thread-pro/            # Viral thread creation
│   ├── humanize-docs/         # AI-to-human doc transformation
│   ├── imagine/               # Image generation prompts
│   ├── storyteller/           # Narrative to visual structure
│   ├── screenwriter/          # Screenplay creation
│   ├── diverse-content-gen/   # Verbalized Sampling technique
│   ├── coolhunter/            # Trend intelligence
│   ├── framework-critical-thinking/  # Agent critical thinking
│   ├── framework-initiative/  # STAR framework for agents
│   ├── baby-education/        # ELI5 explanations
│   ├── readme-expert/         # README creation & validation
│   ├── red-teaming/           # Security red teaming
│   ├── tinkering/             # Experimentation sandbox framework
│   ├── quick-spec/            # Technical spec creation
│   ├── pre-deploy-checklist/  # Pre-deployment QA checklist
│   ├── been-there-done-that/  # Developer progress logging
│   └── adversarial-review/    # Adversarial review protocol
├── agents/
│   ├── seo-manager.md
│   ├── creative-copywriter.md
│   ├── red-team.md
│   ├── doc-simplifier.md
│   ├── sam-altman.md
│   ├── dario-amodei.md
│   └── kotlin-pro.md
└── LICENSE                    # Apache 2.0
```

---

## License

[Apache 2.0](LICENSE) - Copyright 2025 rfxlamia
