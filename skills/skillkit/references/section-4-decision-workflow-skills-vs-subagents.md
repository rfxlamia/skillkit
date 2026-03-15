# Section 4: Decision Workflow (Skills vs Subagents)

**Use when:** User uncertain if Skills is right approach

**Entry Point:** User asks "should I use Skills or Subagents?" or "decide approach"

### Decision Process

**Tool:** `scripts/decision_helper.py`

```bash
python scripts/decision_helper.py --format json
```

**Interactive Questions:**
1. "Describe the use case and requirements"
2. "How often will this be used?"
3. "What's the complexity level?"
4. "Do you need persistent knowledge?"
5. "What's the typical context size?"

**JSON Output Example:**
```json
{
  "recommendation": "Skills",
  "confidence": 0.85,
  "rationale": "Use case fits Skills pattern: reusable knowledge, moderate complexity, clear scope",
  "tradeoffs": {
    "skills_advantages": ["Reusable", "Token efficient", "Clear scope"],
    "skills_disadvantages": ["Limited context awareness"],
    "subagents_advantages": ["Context-aware", "Flexible"],
    "subagents_disadvantages": ["Higher token cost", "Complex orchestration"]
  },
  "next_steps": "Proceed with Skills creation"
}
```

**Decision Gates:**
```
IF recommendation = "Skills" AND confidence >=0.75:
    -> PROCEED to Section 2 (Full Creation)

IF recommendation = "Subagents":
    -> EXPLAIN why Subagents better
    -> PROCEED to Section 6 (Subagent Creation)

IF recommendation = "Hybrid":
    -> EXPLAIN hybrid approach
    -> DISCUSS with user which to create first
    -> PROCEED to chosen path

IF confidence <0.75:
    -> DISCUSS tradeoffs with user
    -> CLARIFY requirements
    -> RE-RUN decision helper
```

**Knowledge Loading:**
- Load `knowledge/foundation/02-skills-vs-subagents.md`
- Load `knowledge/foundation/03-decision-tree.md`
- Load `knowledge/foundation/04-hybrid-patterns.md`
- Present decision framework to user

---

## Step-by-Step Invocation

**CRITICAL: Agent MUST create a temp JSON file first.** The `decision_helper.py` script does NOT accept inline JSON strings - it requires a file path to a JSON file.

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
python3 scripts/decision_helper.py --answers ../../tmp/skillkit/decision-answers.json
```

### Required JSON Structure

- 8 keys (exact names): `utility_task`, `multi_step`, `reusable`, `specialized_personality`, `missing_knowledge`, `coordination`, `isolated_context`, `clutter_chat`
- All values MUST be boolean (`true` or `false`), not strings
- Missing/extra keys will cause validation error

---
