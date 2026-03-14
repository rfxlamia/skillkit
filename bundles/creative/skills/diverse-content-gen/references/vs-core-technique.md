# VS Core Technique

**Purpose:** Core Verbalized Sampling concepts, prompt templates, and execution workflow

**Load when:** Agent needs to execute VS for the first time or needs template reference

---

## Why VS Works: The Theory

### The Mode Collapse Problem

Aligned LLMs suffer from **typicality bias** - they favor more typical, familiar text because:
- Human annotators prefer fluent, predictable content
- RLHF training amplifies this bias
- Result: **50-70% diversity reduction** vs. base models

### The VS Solution

**Different prompts collapse to different modes:**

| Prompt Type | Example | Collapses To |
|------------|---------|--------------|
| **Instance** | "Tell me a joke" | Single most typical joke |
| **List** | "Tell 5 jokes" | Uniform distribution of related items |
| **Distribution (VS)** | "Tell 5 jokes with probabilities" | Base model's learned distribution |

**Key insight:** By asking for a probability distribution, VS recovers the diverse pre-training distribution that alignment compressed.

---

## VS Prompt Template (Production-Ready)

### Standard Template

**Use this exact format for JSON-parseable output:**

```
Generate {k} responses to the following user request. Each response should be approximately {target_words} words.

Return the responses in JSON format with the key: "responses" (list of dicts). Each dictionary must include:

• text: the response string only (no explanation or extra text)
• probability: the estimated probability from 0.0 to 1.0 of this response given the input prompt (relative to the full distribution)

[OPTIONAL: Randomly sample the responses from the distribution, with the probability of each response below {threshold}.]

Give ONLY the JSON object, with no explanations or extra text.

USER REQUEST:
{user_original_request}
```

### Template Variables

**Required:**
- `{k}`: Number of candidates (typically 5)
- `{target_words}`: Expected length (e.g., "50", "200", "500")
- `{user_original_request}`: The actual user query

**Optional:**
- `{threshold}`: Probability threshold (0.01, 0.05, 0.10) - include bracketed line only if tuning for more diversity

### Concrete Example

**User request:** "Write 10 social media captions for a coffee shop's new latte"

**Agent formats VS prompt:**

```
Generate 5 responses to the following user request. Each response should be approximately 20 words.

Return the responses in JSON format with the key: "responses" (list of dicts). Each dictionary must include:

• text: the response string only (no explanation or extra text)
• probability: the estimated probability from 0.0 to 1.0 of this response given the input prompt (relative to the full distribution)

Randomly sample the responses from the distribution, with the probability of each response below 0.10.

Give ONLY the JSON object, with no explanations or extra text.

USER REQUEST:
Write a social media caption for a coffee shop's new caramel cloud latte
```

**Expected output:**
```json
{
  "responses": [
    {"text": "Sip on cloud nine ☁️ Our new Caramel Cloud Latte is here to make your mornings magical ✨", "probability": 0.08},
    {"text": "Warning: Dangerously smooth. The Caramel Cloud Latte has arrived and it's causing serious caffeine crushes 💛", "probability": 0.06},
    {"text": "Fluffy. Creamy. Caramel-y. The Caramel Cloud Latte is basically a hug in a cup 🤗", "probability": 0.05},
    {"text": "Plot twist: clouds ARE edible. Try our new Caramel Cloud Latte and taste the sky ☁️☕", "probability": 0.04},
    {"text": "New latte just dropped and it's lighter than air. Introducing: Caramel Cloud Latte 🌤️", "probability": 0.03}
  ]
}
```

---

## Execution Workflow

### Step 1: Parameter Planning

**Before executing VS, determine:**

**1.1 Content Parameters**
- Content type: (blog post, caption, story, campaign idea, etc.)
- Target word count: (20 words for captions, 500 for blog posts, etc.)
- Total outputs needed: N (user wants 10 captions? 5 blog posts?)

**1.2 VS Parameters**

| Parameter | Default | Notes |
|-----------|---------|-------|
| k (candidates per call) | 5 | Use 3 for quick, 10 for deep exploration |
| Temperature | 0.7-1.0 | Can combine with VS for extra boost |
| Probability threshold | 0.10 (optional) | Lower = more creative tail sampling |

**1.3 Calculate Calls Needed**

```
Number of LLM calls = ⌈N / k⌉
```

Example: User wants 15 ideas → k=5 → Need 3 calls

### Step 2: Execute VS Prompt

1. **Format the prompt** using template with variables filled in
2. **Make LLM call** (use regular message, no special tools)
3. **Parse JSON response** - extract responses array
4. **Repeat if needed** for additional candidates (when N > k)
5. **Collect all candidates** from multiple calls into single pool

### Step 3: Parse & Validate Output

**After receiving VS response:**

```python
# Pseudo-code for agent processing
import json

response_text = llm_output  # The JSON string from LLM
data = json.loads(response_text)
candidates = data["responses"]

# Validate structure
for item in candidates:
    assert "text" in item and "probability" in item
    assert 0.0 <= item["probability"] <= 1.0
```

**Handle errors:**
- If JSON parsing fails → See `troubleshooting.md`
- If structure invalid → Retry with emphasis on "ONLY JSON"

### Step 4: Present Results to User

**Three presentation options:**

**Option A: Ranked by Probability**
```
Here are 5 diverse caption ideas (ordered by probability):

1. [p=0.08] Sip on cloud nine ☁️ Our new Caramel Cloud Latte...
2. [p=0.06] Warning: Dangerously smooth. The Caramel Cloud Latte...
3. [p=0.05] Fluffy. Creamy. Caramel-y. The Caramel Cloud Latte...
```

**Option B: Grouped by Tiers**
```
HIGH PROBABILITY (typical, safer):
• Sip on cloud nine ☁️ Our new Caramel Cloud Latte...

MEDIUM PROBABILITY (balanced):
• Warning: Dangerously smooth. The Caramel Cloud Latte...
• Fluffy. Creamy. Caramel-y. The Caramel Cloud Latte...

LOW PROBABILITY (creative, unique):
• Plot twist: clouds ARE edible. Try our new Caramel Cloud...
```

**Option C: Simple List (Hide Probabilities)**
```
Here are 5 diverse caption ideas:

1. Sip on cloud nine ☁️ Our new Caramel Cloud Latte...
2. Warning: Dangerously smooth. The Caramel Cloud Latte...
3. Fluffy. Creamy. Caramel-y. The Caramel Cloud Latte...
```

**Default:** Use Option C for cleaner user experience, unless user asks for probability insights.

---

## Parameter Selection Guide

### Quick Decision Matrix

| Scenario | k | Threshold | Temperature |
|----------|---|-----------|-------------|
| **Quick ideation** | 3 | None | 0.7 |
| **Standard brainstorming** | 5 | 0.10 | 0.8 |
| **Deep exploration** | 10 | 0.01 | 1.0 |
| **Production content** | 5 | None | 0.8 |

### When to Adjust Parameters

**If outputs too similar:**
- ✅ Lower threshold (0.10 → 0.01)
- ✅ Increase k (5 → 10)
- ✅ Add explicit diversity instruction to prompt

**If outputs too wild/low quality:**
- ✅ Raise threshold (0.01 → 0.10)
- ✅ Reduce k (10 → 5)
- ✅ Add quality constraints to prompt

---

## Quality Control Checklist

**Before presenting VS results to user, verify:**

- [ ] **Diversity achieved:** Outputs cover genuinely different angles/styles/approaches
- [ ] **Quality maintained:** Each output meets baseline quality standards
- [ ] **User intent matched:** Outputs address the original request accurately
- [ ] **Formatting correct:** Clean presentation, no JSON artifacts in user-facing text
- [ ] **Probabilities sensible:** If shown, probabilities are reasonable (don't need to sum to 1.0)

---

## Next Steps

**After mastering core VS:**
- **Task-specific workflows:** Load `task-workflows.md` for pre-configured templates
- **Advanced techniques:** Load `advanced-techniques.md` for VS-CoT, VS-Multi, refinement
- **Tool integration:** Load `tool-integration.md` for file operations, batch processing
- **Troubleshooting:** Load `troubleshooting.md` if encountering issues
