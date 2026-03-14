# VS Troubleshooting Guide

**Purpose:** Solutions to common VS issues and error patterns

**Load when:** VS execution fails, outputs unsatisfactory, or errors encountered

---

## Issue 1: JSON Parsing Failures

### Symptoms
- LLM returns explanation text before/after JSON
- Invalid JSON structure
- Missing quotes or brackets

### Root Cause
Model not following "ONLY JSON" instruction strictly

### Solutions

#### Solution A: Emphasize JSON-Only Output
```
[Add to VS prompt, in bold/caps]
**CRITICAL: Give ONLY the JSON object with no explanations, no extra text before or after.**

Expected format EXACTLY:
{"responses": [{"text": "...", "probability": 0.XX}, ...]}
```

#### Solution B: Structured Output Mode
```
# If model supports structured output
Use structured output API with schema:
{
  "type": "object",
  "properties": {
    "responses": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "probability": {"type": "number", "minimum": 0, "maximum": 1}
        }
      }
    }
  }
}
```

#### Solution C: Regex Extraction
```python
# Fallback: Extract JSON from mixed text
import re
import json

def extract_json(text):
    # Find JSON object in text
    match = re.search(r'\{[\s\S]*"responses"[\s\S]*\}', text)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON found")
```

### Prevention
Always include explicit "ONLY JSON" instruction in every VS prompt

---

## Issue 2: Probabilities Don't Make Sense

### Symptoms
- All probabilities are identical (e.g., all 0.20)
- Probabilities sum to unexpected values (2.5, 10.0, etc.)
- Negative probabilities or values > 1.0

### Root Cause
Model estimating probabilities imperfectly (expected behavior)

### Understanding

**Important:** Probabilities in VS are **estimates**, not ground truth.

✅ **What to trust:**
- Relative ordering (higher p = more typical)
- General magnitude (0.08 vs 0.01 = significant difference)

❌ **What NOT to expect:**
- Perfect calibration
- Probabilities summing to exactly 1.0
- Absolute precision

### Solutions

#### Solution A: Focus on Relative Ranking
```python
# Sort by probability, ignore absolute values
candidates.sort(key=lambda x: x["probability"], reverse=True)
# Present: highest p = most typical, lowest p = most creative
```

#### Solution B: Normalize If Needed
```python
# Only if required for downstream use
total = sum(c["probability"] for c in candidates)
for c in candidates:
    c["probability_normalized"] = c["probability"] / total
```

#### Solution C: Don't Show Probabilities to User
```
# Simple presentation (hide probabilities)
Here are 5 diverse options:
1. [Option 1 text]
2. [Option 2 text]
...
```

### Prevention
Set expectation: probabilities are guidance, not precise measurements

---

## Issue 3: Outputs Still Too Similar

### Symptoms
- VS outputs lack diversity despite using technique
- All variations sound alike
- No meaningful angle/style differences

### Root Causes
1. Task itself has limited diversity space
2. Parameters not tuned for diversity
3. Model constraints (smaller models struggle more)

### Solutions

#### Solution A: Lower Probability Threshold
```
# Add to VS prompt
Randomly sample from the distribution, with probability of each response below 0.01.
```

**Effect:** Samples more from tail (creative outputs)

#### Solution B: Increase k Value
```
# Generate more candidates
k = 10  # Instead of 5
```

**Effect:** Wider exploration of possibility space

#### Solution C: Add Explicit Diversity Instruction
```
IMPORTANT: Ensure responses cover DIFFERENT:
- Tones: (humorous, professional, inspirational, casual)
- Perspectives: (beginner, expert, skeptic, enthusiast)
- Formats: (question, statement, story, instruction)

Avoid generating similar responses.
```

#### Solution D: Use VS-CoT
```
# Add reasoning step (see advanced-techniques.md)
Before generating, think through different angles...
```

**Effect:** Model consciously diversifies

#### Solution E: Check Task Viability
```
# Some tasks genuinely have limited diversity
Example: "Generate the capital of France" → Only 1 valid answer

Ask: Does this task have multiple valid approaches?
If NO → VS may not be appropriate
```

### Prevention
Start with k=5, threshold=0.10. Adjust if diversity insufficient.

---

## Issue 4: Quality Drop on Complex Tasks

### Symptoms
- VS outputs diverse but lower quality
- Errors, incoherence, or off-topic responses
- User prefers single-shot standard prompting quality

### Root Cause
Diversity-quality tradeoff, especially with high k or low threshold

### Solutions

#### Solution A: Use VS-Multi
```
# See advanced-techniques.md
Round 1: VS (diversity)
Round 2: User selects favorites
Round 3: Refine selected (quality)
```

**Effect:** Best of both worlds

#### Solution B: Add Quality Constraints
```
Requirements for ALL responses:
- Professional tone maintained
- Grammatically correct
- On-topic and relevant
- No clichés or filler

Then generate {k} responses meeting these standards.
```

#### Solution C: Reduce k or Raise Threshold
```
# More conservative parameters
k = 3  # Instead of 10
threshold = 0.10  # Instead of 0.01
```

**Effect:** Less aggressive diversity, better quality

#### Solution D: Use VS-CoT for Coherence
```
# Reasoning step helps with complex tasks
# See advanced-techniques.md
```

### Prevention
For production content, default to VS-Multi workflow

---

## Issue 5: Model Not Following VS Format

### Symptoms
- Returns single response instead of k responses
- Generates list without probabilities
- Ignores JSON format entirely

### Root Cause
1. Smaller/weaker models struggle with complex instructions
2. Prompt too complex for model capabilities

### Solutions

#### Solution A: Simplify Prompt
```
# Minimal VS prompt
Generate 5 different responses to: {request}

Return JSON:
{"responses": [
  {"text": "response 1", "probability": 0.X},
  {"text": "response 2", "probability": 0.X},
  ...
]}

ONLY JSON, no extra text.
```

#### Solution B: Use Stronger Model
```
# Check model compatibility (see research-findings.md)
Recommended: GPT-4.1+, Claude 4+, Gemini 2.5+
Avoid: Models < 70B parameters
```

#### Solution C: Fallback to Standard + Repetition
```
# If VS fails, alternative:
for i in range(k):
    response = standard_prompt_with_variation(request)
    candidates.append(response)
```

**Effect:** Less research-backed but more reliable for weak models

### Prevention
Use frontier models (GPT-4, Claude 4, Gemini 2.5) for best VS results

---

## Issue 6: VS Taking Too Long / Expensive

### Symptoms
- High latency for VS calls
- Token costs exceeding budget
- User impatient with wait times

### Root Causes
- High k value (10-20) requires long generation
- Multiple calls for large N
- Using expensive models

### Solutions

#### Solution A: Reduce k
```
k = 3  # Quick mode, still gets diversity benefit
```

**Effect:** ~40% faster, 60% token cost reduction

#### Solution B: Batch Optimization
```
# If generating for multiple prompts:
# Execute VS calls in parallel (if API allows)

import asyncio
results = await asyncio.gather(*vs_calls)
```

#### Solution C: Use Smaller Model for Initial Pass
```
Round 1: VS with smaller/faster model (GPT-4.1-mini)
Round 2: Refine selected with flagship model
```

**Effect:** Cost reduction while maintaining quality

#### Solution D: Cache Results
```
# For repeated similar prompts:
if prompt in cache:
    return cache[prompt]
else:
    result = execute_vs(prompt)
    cache[prompt] = result
    return result
```

### Prevention
Set expectations: VS trades tokens/time for diversity gains

---

## Issue 7: Probabilities All Very Low

### Symptoms
- All probabilities < 0.05
- No clear high-probability responses

### Root Cause
This is actually **expected with low probability threshold**

### Understanding

```
# If you use threshold=0.01
Randomly sample with probability < 0.01

Result: All responses will be < 0.01 (tail sampling)
This is working as intended!
```

### Solutions

#### Solution A: Remove/Raise Threshold
```
# For more typical outputs:
threshold = 0.10  # Or remove threshold entirely
```

#### Solution B: Interpret Correctly
```
# Low probabilities = creative/unique outputs
# This is a feature, not a bug!

Present to user:
"Here are 5 creative (low-probability) options..."
```

### Prevention
Understand that low threshold → low probabilities (by design)

---

## Debugging Checklist

**When VS doesn't work as expected:**

1. [ ] Check prompt formatting (exact template used?)
2. [ ] Verify model supports complex instructions (frontier model?)
3. [ ] Review parameters (k, threshold, temperature sensible?)
4. [ ] Test with simpler request (does basic VS work?)
5. [ ] Check JSON parsing (is response valid JSON?)
6. [ ] Verify task suitability (does it have diversity potential?)
7. [ ] Review quality requirements (diversity-quality tradeoff?)

---

## Error Message Quick Reference

| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| "Invalid JSON" | Model didn't follow format | Emphasize "ONLY JSON" OR use regex extraction |
| "Missing 'probability' field" | Model skipped probabilities | Simplify prompt OR use stronger model |
| "All outputs identical" | Not using VS correctly | Check prompt has VS template |
| "Probabilities sum to 10" | Misunderstanding (not an error) | Focus on relative ranking, not absolute |
| "Quality too low" | High diversity, low quality | Use VS-Multi OR add quality constraints |
| "Too slow" | High k or multiple calls | Reduce k OR use smaller model |

---

## When to Give Up on VS

**VS may not be suitable if:**

1. Task has single correct answer (factual QA)
2. Model too weak to follow instructions (< 70B params)
3. User explicitly wants deterministic output
4. Real-time latency critical (< 1 second response needed)
5. Quality degradation unacceptable

**Alternative:** Use standard prompting with explicit variation instructions

---

**For advanced VS techniques:** See `advanced-techniques.md`
**For research-backed insights:** See `research-findings.md`
