---
title: "Validation Tools: Usage Guide"
purpose: "Quick start for validate_skill.py automation"
token_estimate: "800"
read_priority: "high"
read_when: ["Before skill deployment", "CI/CD setup", "Quality checks"]
related_files:
  concepts: ["02-description-patterns", "07-security", "10-architecture", "12-validation-theory"]
  tools: ["validate_skill.py", "security_scanner.py", "token_estimator.py"]
last_updated: "2025-11-05"
---

# Validation Tools: Quick Start

## Overview

`validate_skill.py` automates 8 quality checks, catches issues early (saves 2-4 hours), zero token cost.

**Theory:** File 12. **This guide:** Usage only.

---

## Installation

### Using Virtual Environment (Recommended)

```bash
cd ~/.claude/skills/skillkit
source venv/bin/activate
python scripts/validate_skill.py --help
```

### Without Virtual Environment

```bash
pip install pyyaml
python3 /path/to/skillkit/scripts/validate_skill.py --help
```

---

## Basic Usage

> **Note:** Make sure venv is activated: `source venv/bin/activate`

```bash
python scripts/validate_skill.py <skill_path> [--strict] [--format text|json]
```

**Example:**
```bash
# With venv activated
python scripts/validate_skill.py ./my-skill/

# Full path without venv
python3 "$HOME/.claude/skills/skillkit/scripts/validate_skill.py" ./my-skill/
```

**Output:**
```
âœ“ YAML Frontmatter
âœ“ File Structure
âš  Description Quality (missing trigger)
âœ“ Token Efficiency (347 lines)
âœ“ Security Basics
âœ“ Writing Style
âœ“ Progressive Disclosure
âœ“ Cross-References

Score: 7/8 (1 warning)
```

**Exit Codes:** 0=pass, 1=warnings, 2=failures

---

## Workflows

**Pre-Deployment:** `python3 validate_skill.py ./my-skill/` â†’ Fix issues â†’ Re-validate until 8/8

**Fixes:** Description (File 02) | Tokens (File 10) | Security (File 07)

**CI/CD:** `source venv/bin/activate && python scripts/validate_skill.py ./my-skill/ --strict --format json; exit $?`

**Batch:** `source venv/bin/activate && for skill in skills/*/; do python scripts/validate_skill.py "$skill" --strict; done`

---

## Validation Checks

| Check | Validates | Reference |
|-------|-----------|-----------|
| YAML | Valid syntax, required fields | File 02 |
| Structure | SKILL.md, scripts/, references/ | File 10 |
| Description | WHAT + WHEN triggers | File 02 |
| Tokens | <500 lines, <5000 tokens | File 05 |
| Security | No secrets, safe patterns | File 07 |
| Style | Imperative, scannable | All files |
| Disclosure | Proper splits, TOCs | File 10 |
| References | No broken links | Phase 1-2 |

**Note:** Use `security_scanner.py` for comprehensive audit (File 16).

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SKILL.md not found" | `ls my-skill/SKILL.md` - verify path |
| "YAML invalid" | Check `---` markers, File 02 format |
| "Module yaml not found" | Activate venv: `source venv/bin/activate` or install: `pip install pyyaml` |
| Many warnings | Run without `--strict` first, fix failures, then enable |

---

## Toolchain Integration

```bash
validate_skill.py â†’ security_scanner.py â†’ token_estimator.py â†’ deploy
```

**Best Practices:**
- âœ… Validate before `package_skill.py`
- âœ… Use `--strict` in CI/CD
- âœ… Fix all failures before deploy
- âœ… Validate frequently during dev

---

## Quick Reference

```bash
# Make sure venv is active first
source venv/bin/activate

# Standard
python scripts/validate_skill.py ./my-skill/

# Strict (CI)
python scripts/validate_skill.py ./my-skill/ --strict

# JSON output
python scripts/validate_skill.py ./my-skill/ --format json

# Full path (tanpa venv)
python3 "$HOME/.claude/skills/skillkit/scripts/validate_skill.py" ./my-skill/
```

**Next:** security_scanner.py (File 16) â†’ token_estimator.py (File 15)
