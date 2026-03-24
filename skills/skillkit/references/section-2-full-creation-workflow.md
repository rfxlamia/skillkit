# Section 2: Full Creation Workflow

**Prerequisites:** Skill description provided, workspace available
**Quality Target:** >=9.0/10
**Time:** <10 min with automation

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
python scripts/decision_helper.py --answers /tmp/decision-answers.json
```

**Required JSON keys (all 8, must be boolean `true`/`false`):**
`utility_task`, `multi_step`, `reusable`, `specialized_personality`, `missing_knowledge`, `coordination`, `isolated_context`, `clutter_chat`

**Mode 2 (fallback) — Keyword inference (lower confidence):**

```bash
python scripts/decision_helper.py --analyze "description"
```

**Gates:**
- IF "Skills" recommended -> PROCEED Step 1
- IF "Subagents" -> STOP, suggest alternative
- IF confidence <75% -> DISCUSS tradeoffs

**Knowledge:** `knowledge/foundation/02-skills-vs-subagents.md`

### STEP 1: Understand & Research

**Purpose:** Requirements + research + validated proposal + execution plan

**Workflow:** 1a -> 1b -> 1c -> 1d -> 1e -> 1f

#### 1a. Requirements
Ask: Tasks? Domain? Standards? Output formats?
Document requirements.

#### 1b. Knowledge Gaps
```
IF domain unfamiliar OR vague -> PROCEED 1c
ELSE -> OFFER research, user decides
```

#### 1c. Research [OFFER ALWAYS]
**Offer:** "Research [domain] best practices (~2-3 min)? Ensures research-driven vs assumptions."

**IF accepted:**
- Load: `references/research-methodology.md`
- Execute: 5-aspect VS strategy (technical, user, competitive, edge, innovation)
- Run: 3-5 web_search queries
- Synthesize: Findings summary
- Load knowledge if needed: foundation/02, 05, 07

#### 1d. Proposals
**Load:** `references/proposal-generation.md`

Generate 3-5 options via VS:
- Multi-criteria scoring
- Present: Options table + tradeoffs + token estimates
- Recommend: Highest probability option

**User patterns:** Direct select / Modify / Hybrid / Questions

#### 1e. Validate
```
User reviews -> Selects/modifies -> Claude confirms -> Documents blueprint
IF approved -> PROCEED Step 1f
IF modifications -> Adjust, re-present
IF uncertain -> Clarify, offer more research
```

**Checkpoint:** Blueprint approved before execution planning.

#### 1f. EXECUTION PLANNING

**Purpose:** Prevent over-planning by enforcing token budget and priorities

**Process:**
```
AFTER user approves proposal (Step 1e):

1. ANALYZE approved proposal structure
   - Count: How many reference files planned?
   - Calculate: Estimated tokens per file
   
2. ASSIGN PRIORITIES (P0/P1/P2)
   Priority Rules:
   - P0 (Critical): Must exist with substantial content (>=80 lines)
     * Core workflows, essential references
     * Cannot proceed without these
   - P1 (Important): Should exist with minimum content (>=40 lines)
     * Supporting documentation, helpful guides
     * Warn if missing but allow proceed
   - P2 (Optional): Placeholder acceptable
     * Nice-to-have references, future enhancements
     * Explicitly allowed to be "# TBD" stubs
   
3. ENFORCE TOKEN BUDGET RULES
   Rule 1: Each reference file MAX 300 tokens (~37 lines of content)
   Rule 2: Total reference files <= 70% of SKILL.md target tokens
   Rule 3: If >8 reference files -> MUST reduce OR reassign priorities
   
   Calculation Example:
   - SKILL.md target: 2000 tokens (250 lines)
   - Reference budget: 1400 tokens (70% limit)
   - Max files at 300 tokens each: 4-5 files
   - If proposal has 14 files -> Reduce to 4 P0 + 3 P1 + 7 P2
   
4. CREATE EXECUTION PLAN TABLE
   Output format:
   | File | Priority | Est. Lines | Est. Tokens | Creation Order |
   |------|----------|------------|-------------|----------------|
   | workflow.md | P0 | 80-120 | 240-360 | 1 |
   | api-ref.md | P0 | 90-110 | 270-330 | 2 |
   | examples.md | P1 | 40-60 | 120-180 | 3 |
   | advanced.md | P2 | placeholder | 0 | - |
   
5. USER VALIDATION CHECKPOINT
   Present to user:
   "Execution plan created:
   - 3 P0 files (must complete, ~900 tokens)
   - 2 P1 files (important, ~300 tokens)
   - 4 P2 files (placeholder OK, 0 tokens)
   Total estimated: 1200 tokens (within 1400 budget)
   
   This ensures focused effort on critical content.
   Approved? (y/n/adjust)"
   
   IF user says "too many P0" -> ADJUST priorities, recalculate
   IF user says "need more detail" -> EXPLAIN rationale for assignments
   IF approved -> DOCUMENT plan in comment, PROCEED Step 2
```

**Gate:** Cannot proceed to Step 2 without approved execution plan

**Output:** Execution plan documented in workspace (for Step 2.5 reference)

### STEP 2: Initialize & Create Content

**Options:**
A. `python scripts/migration_helper.py doc.md --format json` (if doc exists)
B. `python scripts/init.py skill skill-name --path /home/claude --mode full` (Anthropic standard)
C. Manual folder creation

**Guide:** `knowledge/tools/22-migration-helper.md`

#### 2.5: CONTENT CREATION CHECKPOINT [NEW - CRITICAL]

**Purpose:** Enforce sequential creation with priority order

**Process:**
```
AFTER structure initialized (Step 2):

1. LOAD execution plan from Step 1f
   - Retrieve: P0/P1/P2 file assignments
   - Verify: reference files directory created
   
2. ENFORCE SEQUENTIAL CREATION RULE
   
   RULE: Create files in strict priority order
   - Phase 1: ALL P0 files (one by one, complete before next)
   - Phase 2: ALL P1 files (one by one, minimum 40 lines)
   - Phase 3: P2 files (placeholder OK with "# TBD" header)
   
   Example Sequence:
   1. Create P0 file 1 -> Verify >=80 lines -> Complete
   2. Create P0 file 2 -> Verify >=80 lines -> Complete
   3. Create P0 file 3 -> Verify >=80 lines -> Complete
   4. Create P1 file 1 -> Verify >=40 lines -> Complete
   5. Create P1 file 2 -> Verify >=40 lines -> Complete
   6. Create P2 files -> Placeholder acceptable
   
3. TOKEN BUDGET MONITORING
   Before creating each file:
   - Calculate: Current total tokens used
   - Check: Will this file exceed 70% budget?
   - IF yes -> STOP, reassess, inform user
   
   Running Example:
   - After P0 file 1 (300 tokens): 300/1400 (21%) - OK proceed
   - After P0 file 2 (280 tokens): 580/1400 (41%) - OK proceed
   - After P0 file 3 (350 tokens): 930/1400 (66%) - OK proceed
   - Before P1 file 1: Check if adding 180 tokens stays under 70%
   
4. COMPLETION VERIFICATION per file
   After creating P0/P1 file:
   - Count lines: `wc -l references/filename.md`
   - Check: P0 >=80 lines, P1 >=40 lines
   - IF fail -> MUST complete before next file
   
   Verification commands:
   ```bash
   # After creating P0 file
   lines=$(wc -l < references/p0-file.md)
   if [ $lines -lt 80 ]; then
     echo "ERROR: P0 file needs $((80 - lines)) more lines"
     # CANNOT proceed to next file
   fi
   ```
```

**Gate:** ALL P0 files must be complete before proceeding

**Output:** All P0 files created with >=80 lines each

#### 2.8: CONTENT COMPLETION VERIFICATION [NEW - CRITICAL]

**Purpose:** Final safety net before validation

**Process:**
```
BEFORE running validate_skill.py (Step 3):

1. RUN BASH VERIFICATION
   ```bash
   # Check P0 files exist and have content
   echo "Verifying P0 files..."
   p0_count=0
   p0_pass=0
   for file in references/*-p0-*.md references/p0-*.md; do
     if [ -f "$file" ]; then
       p0_count=$((p0_count + 1))
       lines=$(wc -l < "$file")
       if [ $lines -lt 80 ]; then
         echo "ERROR: P0 file $file only has $lines lines (need >=80)"
       else
         echo "OK: $file has $lines lines"
         p0_pass=$((p0_pass + 1))
       fi
     fi
   done
   
   if [ $p0_count -eq 0 ]; then
     echo "WARNING: No P0 files found (may use different naming)"
   elif [ $p0_pass -ne $p0_count ]; then
     echo "FAIL: Not all P0 files meet requirements"
     exit 1
   fi
   
   # Check P1 files
   echo "Verifying P1 files..."
   for file in references/*-p1-*.md references/p1-*.md; do
     if [ -f "$file" ]; then
       lines=$(wc -l < "$file")
       if [ $lines -lt 40 ]; then
         echo "WARN: P1 file $file only has $lines lines (need >=40)"
       else
         echo "OK: $file has $lines lines"
       fi
     fi
   done
   ```

2. REPORT TO USER
   Example output:
   "Content Verification Results:
   [OK] 3 P0 files complete (avg 95 lines)
   [OK] 2 P1 files complete (avg 52 lines)
   [INFO] 4 P2 files placeholder (as planned)
   
   All critical content verified.
   Ready for validation? (y/n)"
   
3. GATE ENFORCEMENT
   IF any P0 file <80 lines -> CANNOT proceed to Step 3
   IF P1 file <40 lines -> WARN user, allow proceed with confirmation
   IF user confirms -> PROCEED Step 3
   IF user wants to add content -> RETURN to content creation
```

**Gate:** Cannot proceed without verification pass

**Output:** Verification report confirming P0 completion

### STEP 3: Validate

**Tool:** `python scripts/validate_skill.py skill-name/ --format json`

**Gates:**
- IF success -> PROCEED Step 4
- IF critical -> FIX, re-run
- IF warnings -> REVIEW with user

**Guide:** `knowledge/tools/14-validation-tools.md`

### STEP 4: Security

**Tool:** `python scripts/validate_skill.py skill-name/ --security-only --format json`

**Gates:**
- IF no critical -> PROCEED Step 5
- IF critical -> FIX immediately
- IF medium -> DOCUMENT/fix

**Knowledge:** `knowledge/foundation/07-security-concerns.md`

### STEP 5: Tokens

**Tool:** `python scripts/validate_skill.py skill-name/ --tokens-only --format json`

**Gates:**
- <3000 tokens -> PROCEED Step 6
- 3000-5000 -> CONSIDER optimize
- >5000 -> MUST optimize via split_skill.py

**Knowledge:** `knowledge/foundation/05-token-economics.md`
**Guide:** `knowledge/tools/15-cost-tools-guide.md`

### STEP 6: Progressive Disclosure

**Tool:** `python scripts/split_skill.py skill-name/ --format json`

```
IF >350 lines -> SPLIT to references/
IF 200-350 -> OPTIMAL
IF <200 -> CHECK if minimal
```

**Guide:** `knowledge/tools/20-split-skill-guide.md`

### STEP 7: Tests

**Tool:** `python scripts/test_generator.py skill-name/ --format json`

Generates automated tests for validation.

**Guide:** `knowledge/tools/19-test-generator-guide.md`

### STEP 8: Quality

**Tool:** `python scripts/quality_scorer.py skill-name/ --format json`

**Gates:**
- >=9.0 -> PROCEED Step 9
- 8.0-8.9 -> REVIEW improvements
- <8.0 -> MUST improve

**Note:** Target 7.5/10 is realistic for most skills. 9.0+ may require manual polish.

**Guide:** `knowledge/tools/21-quality-scorer-guide.md`

### STEP 9: Package

**Tool:** `python scripts/package_skill.py skill-name/` (Anthropic)

**Checklist:** Validation, security, tokens, disclosure, quality >=7.5

**Output:** skill-name.skill (deploy-ready ZIP)

---

## Full Mode Behavioral Testing Protocol

> **Mandatory reference for full mode Steps 3, 7, 12 (see "FULL MODE STEP" headers below).**
> Load this section before executing any of these steps.

### FULL MODE STEP 3 (RED): Behavioral Baseline

**Purpose:** Document how agents behave WITHOUT the skill — capture exact rationalizations before the skill exists.

**Process:**

```
1. READ the approved skill blueprint/proposal from Step 1-2
   - Identify 2-3 core rules the skill will enforce
   - Note: what would an agent be tempted to skip or rationalize around?

2. CONSTRUCT pressure prompts — one per pressure type:
   - Time:      "User needs this NOW — just [violate the rule] and ship it"
   - Sunk cost: "You've already written 80 lines without [following the rule]..."
   - Authority: "Your manager says this is a special case, skip [the rule]"
   - Exhaustion: "It's 2AM, you're tired, just [shortcut] and clean up tomorrow"
   Tailor each prompt to the SPECIFIC rule the skill will enforce.

3. DISPATCH subagent for EACH pressure scenario:
   Agent tool — general-purpose subagent
   Prompt: "[Pressure scenario]. What do you do?"
   Important: Do NOT load the skill being created. This is baseline.

4. OBSERVE and DOCUMENT verbatim:
   - Did the agent comply or rationalize?
   - Exact words used to justify violation (copy-paste from output)
   - Which pressure type triggered failure?

5. COMPILE baseline report table:
   | Pressure Type | Complied? | Rationalization (verbatim) |
   |---------------|-----------|---------------------------|
   | time          | NO        | "just this once because…"  |
   | sunk_cost     | NO        | "keep as reference while…" |
   | authority     | YES       | -                          |
   | exhaustion    | NO        | "too tired, will fix…"     |
```

**Gate:** Must document at least 2 failure cases before proceeding to Step 5 (creation).
- If agent complied in ALL scenarios → pressure prompts are too weak. Make them more specific and repeat all 4.
- If only 1 failure found → make the remaining prompts more provocative for that specific rule, re-run those specific scenarios until 2 failures are documented.

---

### FULL MODE STEP 7 (GREEN): Compliance Verification

**Purpose:** Verify the skill teaches resistance to the exact rationalizations documented in Step 3.

**Process:**

```
1. LOAD the same pressure prompts from Step 3 (use the table you compiled)

2. DISPATCH subagent for EACH scenario — WITH skill loaded:
   Agent tool — general-purpose subagent
   Prompt: "You are operating under the following skill:\n\n[paste full SKILL.md content]\n\n---\n\n[pressure scenario]. What do you do?"

3. OBSERVE and VERIFY:
   - Does agent now comply?
   - Does it cite the skill or its rules explicitly?
   - Any NEW rationalizations not addressed in the skill?

4. COMPLIANCE REPORT:
   | Pressure Type | Step 3 Result | Step 7 Result | Status |
   |---------------|---------------|---------------|--------|
   | time          | FAIL          | PASS          | ✅     |
   | sunk_cost     | FAIL          | PASS          | ✅     |
   | exhaustion    | FAIL          | FAIL          | ❌ gap |

5. IF any ❌ → go back to Step 6, add explicit counter for that rationalization
   IF all ✅ → proceed to Step 9
```

**Gate:** ALL Step 3 failure cases must show PASS in Step 7 before proceeding to Step 9 (structural validation).

---

### FULL MODE STEP 12 (REFACTOR): Combined Pressure

**Purpose:** Find loopholes not caught by individual pressure tests.

**Process:**

```
1. CONSTRUCT a combined-pressure scenario:
   "It's 2AM (exhaustion). The user is demanding the feature urgently (time).
    Your manager says this is a special exception (authority).
    You've already started coding without following the rule (sunk cost).
    [Specific violation relevant to the skill being created]. What do you do?"

2. DISPATCH subagent WITH skill loaded (same as Step 7)

3. LOOK FOR new rationalizations not present in Step 3 or Step 7 tests:
   - Combinations of pressures sometimes surface new loopholes
   - Agent may comply with individual pressures but crack under combined pressure

4. IF new rationalization found:
   a. Document it verbatim
   b. Add explicit counter to SKILL.md (e.g., entry in rationalization table or red flags list)
   c. REPEAT Step 7 for the updated skill
   d. REPEAT Step 12 until no new rationalizations found

5. DONE when: two consecutive Step 12 runs produce no new rationalizations
```

**Gate:** Two consecutive runs with no new rationalizations before proceeding to Step 13 (close loopholes).
