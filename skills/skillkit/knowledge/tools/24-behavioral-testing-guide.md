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

> **DEPRECATED (v2.1):** `pressure_tester.py` has been superseded by the Full Mode Behavioral Testing Protocol.
> For full mode Steps 3, 7, 12: Load `references/section-2-full-creation-workflow.md` → section "Full Mode Behavioral Testing Protocol".
> The bash commands below are no longer functional.

## What This Is For

Use this guide when you need to prove a skill changes agent behavior under pressure.

Behavioral testing in skill writing follows TDD:
- RED: observe baseline failures without the skill
- GREEN: verify improved behavior with the skill
- REFACTOR: close loopholes and re-test

## Critical v2 Limitation

`pressure_tester.py` was a structural stub in v2 and has been removed in v2.1.
- `run_scenario()` returned hardcoded `compliance_score=8.5`
- Output validated data shape and integration flow only
- Score was never real compliance evidence

As of v2.1, the replacement is the **subagent dispatch protocol** documented in
`references/section-2-full-creation-workflow.md` under "Full Mode Behavioral Testing Protocol".
Use that section for all RED/GREEN/REFACTOR cycles going forward.

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

```
# DEPRECATED: pressure_tester.py exits with error in v2.1
# Use Full Mode Behavioral Testing Protocol in section-2-full-creation-workflow.md instead
```

Record:
- rationalizations the agent used
- where the skill content currently fails to block those rationalizations

### Step 2: GREEN (Verification)

After updating the skill content:

```
# DEPRECATED: pressure_tester.py exits with error in v2.1
# Use Full Mode Behavioral Testing Protocol in section-2-full-creation-workflow.md instead
```

Check:
- output schema is complete
- rationalization counters are now present in skill text

### Step 3: REFACTOR (Loophole Closure)

Run targeted pressure checks to tighten specific weak points:

```
# DEPRECATED: pressure_tester.py exits with error in v2.1
# Use Full Mode Behavioral Testing Protocol in section-2-full-creation-workflow.md instead
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

```
# DEPRECATED: quality_scorer.py --behavioral is no longer functional in v2.1
# Use Full Mode Behavioral Testing Protocol in section-2-full-creation-workflow.md instead
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
