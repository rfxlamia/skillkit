# Section 2: Fast Creation Workflow

**Prerequisites:** Skill description provided, workspace available
**Quality Target:** >=9.0/10 (structural)
**Time:** <10 min with automation

---

## Phase 1: Decision & Research

### STEP 0: Decide Approach

**Guide:** `knowledge/tools/18-decision-helper-guide.md`

**Mode 1 (preferred) — Pre-answered questions (90-95% confidence):**

```bash
# Step 1: Create answers file with all 8 boolean fields
cat > /tmp/decision-answers.json <<'EOF'
{
  "utility_task": false,
  "multi_step": true,
  "reusable": false,
  "specialized_personality": false,
  "missing_knowledge": false,
  "coordination": false,
  "isolated_context": false,
  "clutter_chat": false
}
EOF

# Step 2: Pass FILE PATH (not inline JSON) to --answers
python scripts/decision_helper.py --answers /tmp/decision-answers.json --format json
```

**Required JSON keys (all 8, must be boolean `true`/`false`):**
`utility_task`, `multi_step`, `reusable`, `specialized_personality`, `missing_knowledge`, `coordination`, `isolated_context`, `clutter_chat`

**Mode 2 (fallback) — Keyword inference (lower confidence):**

```bash
python scripts/decision_helper.py --analyze "description" --format json
```

**Gates:**
- IF "Skills" recommended → PROCEED Step 1
- IF "Subagents" → STOP, suggest alternative
- IF confidence <75% → DISCUSS tradeoffs

**Knowledge:** `knowledge/foundation/02-skills-vs-subagents.md`

---

### STEP 1: Research & Proposals

**Purpose:** Requirements + research + validated proposal

**Sub-steps:**
1. Gather requirements (tasks, domain, standards, output formats)
2. Identify knowledge gaps — if domain unfamiliar, offer research (~2 min)
3. If research accepted: load `references/research-methodology.md`, run 3-5 web searches
4. Generate 3-5 proposals via `references/proposal-generation.md`
5. Present options table with tradeoffs and token estimates
6. Recommend highest-probability option

---

### STEP 2: User Validation

**Purpose:** Confirm proposal before content creation

**Stop Condition (Mandatory):** Stop and request user approval before continuing to Step 3.

**Checkpoint:** User selects/modifies proposal → Claude confirms → documents blueprint.

---

## Phase 2: Creation

### STEP 3: Initialize Skill

**Tool:** `python3 scripts/init.py skill skill-name --mode fast --path /target/path`

**Gates:**
- IF target path already exists → STOP, ask user: overwrite, rename, or cancel
- IF init succeeds → PROCEED Step 4

**Guide:** `knowledge/tools/22-migration-helper-guide.md` (if converting from existing doc)

---

### STEP 4: Create Content

**Purpose:** Write SKILL.md and reference files per approved blueprint

**Process:**
1. Assign priorities inline: label each planned file as P0 (critical), P1 (important), or P2 (optional)
2. Create files in strict priority order: all P0 → all P1 → P2 placeholders
3. P0 files: >=80 lines each. P1 files: >=40 lines each. P2: `# TBD` placeholder OK.
4. Verify line count after each P0/P1 file before proceeding to next

**Verification per file:**
```bash
lines=$(wc -l < references/filename.md)
echo "Lines: $lines"
```

**Gate:** ALL P0 files must be complete before proceeding to Phase 3.

---

## Phase 3: Structural Validation

### STEP 5: Validate Skill

**Tool:** `python3 scripts/validate_skill.py skill-name/ --format json`

Runs structure validation + security scan + token analysis in one call. No flags needed for workflow use.
(`--security-only` and `--tokens-only` flags are for Section 7 individual tool use only.)

**Gates:**
- Structure PASS (no failures, no warnings) → PROCEED Step 6
- Structure failures → FIX, re-run
- Structure warnings only → REVIEW with user, PROCEED Step 6
- Security CRITICAL findings → FIX immediately, re-run
- Security MEDIUM findings → DOCUMENT and fix
- Tokens <3000 → PROCEED Step 6
- Tokens 3000–5000 → CONSIDER splitting
- Tokens >5000 → MUST split via `scripts/split_skill.py` before proceeding

**Guides:** `knowledge/tools/14-validation-tools-guide.md`, `knowledge/tools/15-cost-tools-guide.md`, `knowledge/foundation/07-security-concerns.md`

---

## Phase 4: Packaging

### STEP 6: Progressive Disclosure Check

**Tool:** `python3 scripts/split_skill.py skill-name/ --format json`

**Gates:**
- IF >350 lines → SPLIT to references/ via `scripts/split_skill.py`
- IF 200–350 lines → OPTIMAL, proceed
- IF <200 lines → CHECK if content is sufficient

**Guide:** `knowledge/tools/20-split-skill-guide.md`

---

### STEP 7: Generate Tests

**Tool:** `python3 scripts/test_generator.py skill-name/ --test-format pytest --format json`

**Gates:**
- IF tests generated → REVIEW output, PROCEED Step 8
- IF generation fails → CHECK skill structure, re-run validate_skill.py first

**Guide:** `knowledge/tools/19-test-generator-guide.md`

---

### STEP 8: Quality Assessment

**Tool:** `python3 scripts/quality_scorer.py skill-name/ --format json`

**Gates:**
- >=9.0 → PROCEED Step 9
- 8.0–8.9 → REVIEW improvements
- <8.0 → MUST improve before packaging

**Note:** 7.5/10 is the minimum to package (Step 9 checklist). The >=9.0 gate above is aspirational — if score is 7.5–8.9, review improvements but proceed if changes would not meaningfully raise quality.

**Guide:** `knowledge/tools/21-quality-scorer-guide.md`

---

### STEP 9: Package

**Tool:** `python3 scripts/package_skill.py skill-name/`

**Pre-flight checklist:**
- [ ] Structure validation passed
- [ ] Security audit passed
- [ ] Tokens within budget
- [ ] Progressive disclosure checked
- [ ] Quality score >=7.5

**Output:** `skill-name.skill` (deploy-ready ZIP)
