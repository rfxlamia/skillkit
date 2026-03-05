---
name: skillkit
description: >
  Research-driven toolkit for creating and validating skills and subagents with
  structured workflows, gates, and automation scripts.
  Use for: create skill, create subagent, validate skill quality, decide Skills
  vs Subagents, migrate docs to skills, estimate token cost, and security scan.
  Includes proposal generation, quality scoring, progressive disclosure checks,
  and packaging support. Built for consistent high-quality outputs with
  reusable scripts and production-tested tooling.
---

## Section 1: Intent Detection & Routing
**Detect user intent, route to appropriate workflow.**

| Intent | Keywords | Route To |
|--------|----------|----------|
| Full skill creation | "create skill", "build skill", "new skill" | Section 2 |
| Subagent creation | "create subagent", "build subagent", "new subagent" | Section 6 |
| Validation | "validate", "check quality" | Section 3 |
| Decision | "Skills vs Subagents", "decide", "which to use" | Section 4 |
| Migration | "convert", "migrate doc" | Section 5 |
| Single tool | "validate only", "estimate tokens", "scan" | Section 7 |

**PROCEED to corresponding section after intent detection.**

**Workflow Value:** Research-driven approach validates design before building.
Sequential steps with checkpoints produce 9.0/10+ quality vs ad-hoc creation.

---

## Section 2: Creation Workflows (Dual Mode)

**Prerequisites:** Skill description provided, workspace available.

### Mode Selection (Required at Start)

Agent MUST detect or prompt for workflow mode before running the creation flow.

| Mode | Steps | Validation | Quality Target | Time |
|------|-------|------------|----------------|------|
| **fast** | 12 | Structural only | >=9.0/10 | <10 min |
| **full** | 15 | Structural + Behavioral | >=9.0/10 and behavioral >=7.0 | <20 min |

Default mode is `fast` for backward compatibility.

### Workflow A: Fast Mode (12 Steps)

Use when `.skillkit-mode` contains `fast` or marker does not exist.

Phase 1: Decision and Research
- Step 0: Decide approach (`decision_helper.py`)
- Step 1: Research and proposals
- Step 2: User validation

Phase 2: Creation
- Step 3: Initialize skill (`init_skill.py --mode fast`)
- Step 4: Create content

Phase 3: Structural Validation
- Step 5: Validate structure (`validate_skill.py`)
- Step 6: Security audit (`security_scanner.py`)
- Step 7: Token optimization (`token_estimator.py`)

Phase 4: Packaging
- Step 8: Progressive disclosure check
- Step 9: Generate tests (`test_generator.py`)
- Step 10: Quality assessment (`quality_scorer.py`)
- Step 11: Package (`package_skill.py`)

### Workflow B: Full Mode (16 Steps)

Use when `.skillkit-mode` contains `full`.

Phase 1: Decision and Research
- Step 0: Decide approach (`decision_helper.py`)
- Step 1: Research and proposals
- Step 2: User validation

Phase 2: Behavioral Baseline (extra vs fast)
- Step 3 (RED): Run pressure scenarios without skill
- Step 4: Document baseline failures

Phase 3: Creation
- Step 5: Initialize skill (`init_skill.py --mode full`)
- Step 6: Create content addressing baseline failures

Phase 4: Behavioral Verification (extra vs fast)
- Step 7 (GREEN): Run scenarios with skill
- Step 8: Fix gaps

Phase 5: Structural Validation
- Step 9: Validate structure
- Step 10: Security audit
- Step 11: Token optimization

Phase 6: Refinement (extra vs fast)
- Step 12 (REFACTOR): Combined pressure tests
- Step 13: Close loopholes

Phase 7: Packaging
- Step 14: Quality assessment (`quality_scorer.py --behavioral`)
- Step 15: Package (`package_skill.py`)

### Mode Detection

Mode detection priority:
1. Explicit flag: `--mode fast` or `--mode full`
2. Skill marker: `.skillkit-mode` file
3. Default: `fast`

```python
def detect_mode(skill_path: str, cli_flag: Optional[str] = None) -> str:
    if cli_flag:
        return cli_flag

    marker_file = Path(skill_path) / ".skillkit-mode"
    if marker_file.exists():
        return marker_file.read_text().strip()

    return "fast"
```

---

## Section 3: Validation Workflow (Overview)

**Use when:** Validating existing skill

**Steps:** Execute validation subset (Steps 3-8)
1. Structure validation (validate_skill.py)
2. Security audit (security_scanner.py)
3. Token analysis (token_estimator.py)
4. Progressive disclosure check
5. Test generation (optional)
6. Quality assessment (quality_scorer.py)

**For detailed workflow:** [See references/section-3-validation-workflow-existing-skill.md](references/section-3-validation-workflow-existing-skill.md)

---

## Section 4: Decision Workflow (Overview)

**Use when:** Uncertain if Skills is right approach

**CRITICAL: Agent MUST create a temp JSON file first.** The `decision_helper.py` script does NOT accept inline JSON strings - it requires a file path to a JSON file.

**Step-by-step workflow (REQUIRED):**

```bash
# STEP 1: Create temp directory (from repository root)
mkdir -p ./tmp/skillkit

# STEP 2: Create JSON file with answers (REQUIRED - cannot be inline)
cat > ./tmp/skillkit/decision-answers.json <<'EOF'
{
  "utility_task": false,
  "multi_step": true,
  "reusable": false,
  "specialized_personality": true,
  "missing_knowledge": false,
  "coordination": true,
  "isolated_context": true,
  "clutter_chat": true
}
EOF

# STEP 3: Call decision helper with FILE PATH (not JSON string)
cd skills/skillkit && source venv/bin/activate
python scripts/decision_helper.py --answers ../../tmp/skillkit/decision-answers.json
```

**Required JSON structure:**

- 8 keys (exact names): `utility_task`, `multi_step`, `reusable`, `specialized_personality`, `missing_knowledge`, `coordination`, `isolated_context`, `clutter_chat`
- All values MUST be boolean (`true` or `false`), not strings
- Missing/extra keys will cause validation error

**Accuracy:** Highest (90-95% confidence).

**Process:**

1. Run `decision_helper.py` with json file.
2. Answer interactive questions
3. Receive recommendation with confidence score
4. Proceed if Skills recommended (confidence >=75%)

**For detailed workflow:** [See references/section-4-decision-workflow-skills-vs-subagents.md](references/section-4-decision-workflow-skills-vs-subagents.md)

---

## Section 6: Subagent Creation Workflow (Overview)

**Use when:** Creating new subagent (user explicitly asks or decision workflow recommends)

**Prerequisites:** Role definition clear, workspace available
**Quality Target:** Clear role, comprehensive workflow, testable examples
**Time:** <15 min with template

### 8-Step Process:

**STEP 0: Requirements & Role Definition**
- Answer: Primary role? Trigger conditions? Tool requirements?
- Choose subagent_type from predefined list

**STEP 1: Initialize Subagent File**
- Tool: `python scripts/init_subagent.py subagent-name --path ~/.claude/agents`
- Creates: `~/.claude/agents/subagent-name.md` with template
- **Important:** Subagents are individual `.md` files (not directories)

**STEP 2: Define Configuration**
- Edit YAML frontmatter (name, description, type, tools, skills)
- Configure tool permissions (minimal but sufficient)

**STEP 3: Define Role and Workflow**
- Role definition section
- Trigger conditions (when to invoke)
- Multi-phase workflow

**STEP 4: Define Response Format**
- Output structure template
- Tone and style guidelines
- Error handling

**STEP 5: Add Examples**
- At least 1 complete example
- Input/Process/Output format

**STEP 6: Validation**
- YAML validity check
- Structure verification
- Completeness review

**STEP 7: Testing**
- Test invocation with Task tool
- Iterate based on results

**STEP 8: Documentation & Deployment**
- Create README.md
- Register in system

**For detailed workflow:** [See references/section-6-subagent-creation-workflow.md](references/section-6-subagent-creation-workflow.md)

---

## Section 5: Migration Workflow (Overview)

**Use when:** Converting document to skill

**Process:**
1. Decision check (Step 0)
2. Migration analysis (migration_helper.py)
3. Structure creation
4. Execute validation steps (3-8)
5. Package (Step 9)

**For detailed workflow:** [See references/section-5-migration-workflow-doc-to-skill.md](references/section-5-migration-workflow-doc-to-skill.md)

---

## Section 7: Individual Tool Usage
**Use when:** User needs single tool, not full workflow

**Entry Point:** User asks for specific tool like "estimate tokens" or "security scan"

### Available Tools

**Validation Tool:**
```bash
python scripts/validate_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/14-validation-tools-guide.md`

**Token Estimator:**
```bash
python scripts/token_estimator.py skill-name/ --format json
```
Guide: `knowledge/tools/15-cost-tools-guide.md`

**Security Scanner:**
```bash
python scripts/security_scanner.py skill-name/ --format json
```
Guide: `knowledge/tools/16-security-tools-guide.md`

**Pattern Detector:**
```bash
# Analysis mode with JSON output
python scripts/pattern_detector.py "convert PDF to Word" --format json

# List all patterns
python scripts/pattern_detector.py --list --format json

# Interactive mode (text only)
python scripts/pattern_detector.py --interactive
```
Guide: `knowledge/tools/17-pattern-tools-guide.md`

**Decision Helper:**
```bash
# Analyze use case (JSON output - agent-layer default)
python scripts/decision_helper.py --analyze "code review with validation"

# Show decision criteria (JSON output)
python scripts/decision_helper.py --show-criteria --format json

# Text mode for human reading (debugging)
python scripts/decision_helper.py --analyze "description" --format text
```
Guide: `knowledge/tools/18-decision-helper-guide.md`

**Test Generator (v1.2: Parameter update):**
```bash
python scripts/test_generator.py skill-name/ --test-format pytest --format json
```
- `--test-format`: Test framework (pytest/unittest/plain, default: pytest)
- `--format`: Output style (text/json, default: text)
- Backward compatible: Old `--output` parameter still works (deprecated)

Guide: `knowledge/tools/19-test-generator-guide.md`

**Split Skill:**
```bash
python scripts/split_skill.py skill-name/ --format json
```
Guide: `knowledge/tools/20-split-skill-guide.md`

**Quality Scorer:**
```bash
python scripts/quality_scorer.py skill-name/ --format json
```
Guide: `knowledge/tools/21-quality-scorer-guide.md`

**Migration Helper:**
```bash
python scripts/migration_helper.py doc.md --format json
```
Guide: `knowledge/tools/22-migration-helper-guide.md`

**Subagent Initializer (NEW):**
```bash
python scripts/init_subagent.py subagent-name --path /path/to/subagents
```
Guide: `references/section-6-subagent-creation-workflow.md`

### Tool Output Standardization (v1.0.1+)

**All 9 tools now support `--format json` parameter:**
- ✅ Consistent JSON schema across all automation tools
- ✅ Parseable with `python -m json.tool` for validation
- ✅ Backward compatible - text mode still available as default (or via `--format text`)
- ✅ Agent-layer tools (decision_helper) default to JSON for automation

**JSON Output Structure (Standardized):**
```json
{
  "status": "success" | "error",
  "tool": "tool_name",
  "timestamp": "ISO-8601",
  "data": { /* tool-specific results */ }
}
```

### Quality Assurance Enhancements (v1.2+)

**File & Reference Validation:**
- `validate_skill.py` now comprehensively checks file references (markdown links, code refs, path patterns)
- `package_skill.py` validates references before packaging, detects orphaned files
- Prevents broken references and incomplete files in deployed skills

**Content Budget Enforcement (v1.2+):**
- Hard limits on file size: P0 ≤150 lines, P1 ≤100 lines, P2 ≤60 lines
- Real-time token counting with progress indicators
- Prevents file bloat that previously caused 4-9x target overruns

**Execution Planning (v1.2+):**
- P0/P1/P2 prioritization prevents over-scoping
- Token budget allocated per file to maintain efficiency
- Research phase respects Verbalized Sampling probability thresholds (p>0.10)

**Quality Scorer Context:**
- Scores calibrated for general skill quality heuristics
- Target: 70%+ is good, 80%+ is excellent
- Style scoring may not fit all skill types (educational vs technical)
- Use as guidance, supplement with manual review for edge cases

---

## Section 8: Mode Selection Guide

### When to Use Fast Mode

Use fast mode when:
- simple utility or conversion skills
- quick prototypes
- API or reference-focused skills
- internal tooling with low behavioral risk

Do not use fast mode when:
- skill enforces discipline (TDD, strict verification, no-shortcut rules)
- skill has many decision points and loophole risk
- production-grade compliance is mandatory

### When to Use Full Mode

Use full mode when:
- discipline enforcement is core behavior
- workflow is multi-step and error-sensitive
- skill will be reused broadly by multiple agents
- quality and compliance are both critical

Full mode may be overkill for:
- very small one-step techniques
- personal one-off reference notes

### Decision Matrix

| Skill Type | Recommended Mode | Why |
|------------|------------------|-----|
| TDD or discipline skill | **full** | must resist rationalization under pressure |
| Code pattern skill | **fast** | structural checks are usually sufficient |
| API reference skill | **fast** | primarily retrieval accuracy |
| Workflow orchestration skill | **full** | complex flow benefits from pressure checks |
| Debugging technique skill | **fast** | concise technique with clear method |

---

## Section 9: Knowledge Reference Map (Overview)

**Strategic context loaded on-demand.**

### Foundation Concepts (Files 01-08):
- Why Skills exist vs alternatives
- Skills vs Subagents decision framework
- Token economics and efficiency
- Platform constraints and security
- When NOT to use Skills

### Application Knowledge (Files 09-13):
- Real-world case studies (Rakuten, Box, Notion)
- Technical architecture patterns
- Adoption and testing strategies
- Competitive landscape analysis

### Tool Guides (Files 14-22):
- One guide per automation script
- Usage patterns and parameters
- JSON output formats
- Integration examples

**For complete reference map:** [See references/section-7-knowledge-reference-map.md](references/section-7-knowledge-reference-map.md)

---

## Workflow Compliance Reinforcement
**This skill works best when workflows are followed sequentially.**

**Why compliance matters:**
1. Research validation reduces iteration (validate before build)
2. Security checks prevent vulnerabilities (catch issues early)
3. Token optimization ensures efficiency (avoid bloat)
4. Quality gates maintain standards (9.0/10+ target)

**Mechanisms encouraging compliance:**
- Frontmatter priming: "WORKFLOW COMPLIANCE" statement
- Section routing: Explicit "PROCEED to Section X"
- Validation gates: IF/THEN with checkpoints
- Quality target: ">=9.0/10 requires following workflow"

**Flexible when needed:**
- Single tool usage (Section 7) skips full workflow
- Validation-only (Section 3) runs subset of steps
- Subagent creation (Section 6) has streamlined workflow
- User can request deviations with justification

**Goal:** Strong encouragement through design, not strict enforcement.

---

## Additional Resources

**Detailed implementations available in references/ directory:**

All section overviews above link to detailed reference files for deep-dive information.
Load references on-demand when detailed implementation guidance needed.
