---
title: "Behavioral Testing with pressure_tester.py"
purpose: "Run RED->GREEN->REFACTOR behavioral checks for skill quality"
tool_name: "pressure_tester.py"
tool_type: "validation-layer"
read_priority: "high"
read_when:
  - "Using full-mode workflow"
  - "Creating discipline-enforcing skills"
  - "Need evidence that agents comply under pressure"
---

# Behavioral Testing Guide

## What This Is For

Use this guide when you need to prove a skill changes agent behavior under pressure.

Behavioral testing in skill writing follows TDD:
- RED: observe baseline failures without the skill
- GREEN: verify improved behavior with the skill
- REFACTOR: close loopholes and re-test

## Critical v2 Limitation

`pressure_tester.py` in v2 is a structural stub.
- `run_scenario()` returns hardcoded `compliance_score=8.5`
- Current output validates data shape and integration flow
- Do not treat score as real compliance evidence

Use output as a workflow signal, not as final proof of discipline quality.

## Pressure Types

| Type | Scenario | Primary Risk |
|------|----------|--------------|
| `time` | "I need this now" | shortcut behavior |
| `sunk_cost` | "already wrote 100 lines" | unwilling to restart |
| `authority` | "manager says skip" | authority override |
| `exhaustion` | "it's 2 AM" | low-discipline compromise |
| `combined` | all above | multi-pressure failure |

## Execution Workflow

### Step 1: RED (Baseline)

Run before writing or editing the target skill:

```bash
python3 scripts/pressure_tester.py /path/to/skill \
  --pressure combined \
  --skill-type discipline \
  --format json
```

Record:
- rationalizations the agent used
- where the skill content currently fails to block those rationalizations

### Step 2: GREEN (Verification)

After updating the skill content:

```bash
python3 scripts/pressure_tester.py /path/to/skill \
  --pressure combined \
  --skill-type discipline \
  --format json
```

Check:
- output schema is complete
- rationalization counters are now present in skill text

### Step 3: REFACTOR (Loophole Closure)

Run targeted pressure checks to tighten specific weak points:

```bash
python3 scripts/pressure_tester.py /path/to/skill --pressure time --skill-type discipline --format json
python3 scripts/pressure_tester.py /path/to/skill --pressure sunk_cost --skill-type discipline --format json
python3 scripts/pressure_tester.py /path/to/skill --pressure authority --skill-type discipline --format json
python3 scripts/pressure_tester.py /path/to/skill --pressure exhaustion --skill-type discipline --format json
```

## Output Contract

Expected JSON keys:
- `status`
- `compliance_score`
- `rationalizations_found`
- `fixes_needed`
- `skill_type`
- `pressure_type`

If any key is missing, treat run as failed integration.

## Integration with quality_scorer.py

In full mode, `quality_scorer.py` combines:
- structural score: 60%
- behavioral score: 40%

Run:

```bash
python3 scripts/quality_scorer.py /path/to/skill \
  --behavioral \
  --skill-type discipline \
  --format json
```

Use result fields:
- `mode`
- `final_score`
- `structural_score`
- `behavioral_score`
- `weights`

## Failure Handling

If behavioral run is invalid:
- verify `pressure_tester.py` imports correctly
- verify `--skill-type` is one of: `discipline`, `technique`, `pattern`, `reference`
- re-run with `--format json` and inspect missing fields

If run is valid but skill still weak:
- update rationalization table in SKILL
- add explicit "no exceptions" counters
- add red-flags section
- rerun RED/GREEN/REFACTOR
