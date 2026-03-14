# Advanced VS Techniques

**Purpose:** Advanced VS methods for higher quality, better control, and production use

**Load when:** Basic VS doesn't meet quality needs, or user requests refinement/polish

**Prerequisite:** Familiarity with core VS technique (`vs-core-technique.md`)

---

## VS-CoT: Chain-of-Thought Enhancement

### When to Use
- Complex creative tasks requiring reasoning
- When basic VS outputs lack coherence
- User requests "thoughtful" or "well-reasoned" variations

### How It Works

Add reasoning step **before** generating responses:

```
Before generating responses, first think through:
1. What are the different possible angles/perspectives for this request?
2. What styles/tones would work? (humorous, professional, casual, poetic, etc.)
3. What makes each response unique from the others?

Then generate {k} responses with probabilities as instructed.
```

### Complete VS-CoT Prompt Template

```
[REASONING SECTION]
Before generating responses, think through:
1. Different angles/perspectives for this request
2. Appropriate styles/tones
3. What makes each response unique

[STANDARD VS SECTION]
Generate {k} responses to the following user request. Each response should be approximately {target_words} words.

Return the responses in JSON format with the key: "responses" (list of dicts). Each dictionary must include:
• text: the response string only (no explanation or extra text)
• probability: the estimated probability from 0.0 to 1.0

Give ONLY the JSON object, with no explanations or extra text.

USER REQUEST:
{user_original_request}
```

### Research Results

**VS-CoT achieves:**
- **Highest quality+diversity balance** among all VS variants
- Creative writing: 25.8% diversity (vs. 21.9% for VS-Standard)
- Quality scores: Matches or exceeds baseline

**Best for:** Stories, essays, campaign briefs, product narratives

---

## VS-Multi: Multi-Turn Refinement

### When to Use
- Production content that needs polish
- User says "good but needs refinement"
- Quality is priority, diversity is secondary

### The VS-Multi Workflow

**3-round process combining diversity + quality:**

#### Round 1: Initial VS Generation (Diversity)
```
Parameters: k=5-10, threshold=0.10
Goal: Cast wide net, explore diverse options
```

**Agent action:** Generate 5-10 diverse candidates using standard VS

#### Round 2: User Selection + Refinement (Curation)
```
Agent: "Which 2-3 options resonate most? I'll refine them."
User: Selects top candidates
```

**Agent action:** For each selected candidate, generate 3 refined variations (k=3)

#### Round 3: Final Polish (Quality)
```
Agent: Standard high-quality rewrite of user's final selection
No VS needed - just quality optimization
```

**Agent action:** Traditional quality-focused generation on chosen option

### VS-Multi Benefits

**Research shows:**
- Large models: **+5.0 quality points** vs. single-shot VS
- Combines diversity (Round 1) + quality (Rounds 2-3)
- User involvement ensures alignment with intent

**Time investment:** ~2-3× longer than standard VS, but worth it for production content

---

## Parameter Tuning for Advanced Control

### Probability Threshold Tuning

**Purpose:** Control how far into the probability tail to sample

| Threshold | Effect | Use Case |
|-----------|--------|----------|
| **None** | Balanced diversity+quality | Standard brainstorming |
| **0.10** | Moderate tail sampling | More creative options |
| **0.01** | Deep tail sampling | Maximum creativity |
| **0.001** | Extreme tail sampling | Experimental/avant-garde |

**Prompt modification:**
```
[Add to VS prompt]
Randomly sample the responses from the distribution, with the probability of each response below {threshold}.
```

**Research optimal range:** 0.01-0.10 for most tasks

### k Value Tuning

**Quality-diversity tradeoff:**

| k | Diversity Gain | Quality Impact | Best For |
|---|----------------|----------------|----------|
| **3** | +15% | -2% | Quick tasks, time-sensitive |
| **5** | +35% | -3% | **Optimal balance (recommended)** |
| **10** | +52% | -5% | Deep exploration, ideation |
| **20** | +68% | -8% | Research, synthetic data |

**Recommendation:** Start with k=5, adjust based on results

### Temperature Combination

**VS is orthogonal to temperature** - can combine both:

| Configuration | Diversity | Quality | Use Case |
|--------------|-----------|---------|----------|
| VS only, temp=0.7 | Moderate | High | Production content |
| VS only, temp=1.0 | High | Moderate | Creative brainstorming |
| VS + temp=0.8 | Very High | Moderate | Maximum diversity |
| VS + temp=0.5 | Low-Moderate | Very High | Controlled variation |

**Optimal combo:** VS with temperature 0.8-1.0 for creative tasks

---

## Iterative Refinement Patterns

### Pattern 1: Expand-Then-Narrow

**Use case:** User unsure of direction

```
Round 1: VS with k=10, threshold=0.05 (wide exploration)
Round 2: User narrows to 3 favorites
Round 3: VS-Multi refinement on favorites (k=3 each)
Round 4: User picks final, agent polishes
```

### Pattern 2: Parallel Tracks

**Use case:** Exploring multiple distinct directions

```
Track A: Humorous tone
  - VS with k=5, emphasis on "playful, witty"

Track B: Professional tone
  - VS with k=5, emphasis on "authoritative, polished"

Track C: Inspirational tone
  - VS with k=5, emphasis on "uplifting, motivational"

User compares across tracks, selects best direction
```

### Pattern 3: Incremental Diversity

**Use case:** Gradually exploring creative space

```
Iteration 1: Standard VS (k=5)
Iteration 2: If outputs too similar → Lower threshold (0.10 → 0.01)
Iteration 3: If still similar → Increase k (5 → 10)
Iteration 4: If still similar → Add explicit diversity constraints
```

---

## Advanced Diversity Controls

### Explicit Diversity Instructions

**Add to VS prompt when needed:**

```
IMPORTANT: Ensure responses cover different:
- Tones: (humorous, professional, casual, inspirational)
- Perspectives: (consumer, expert, beginner, skeptic)
- Formats: (question, statement, story, call-to-action)

Avoid generating similar responses.
```

**Effect:** Pushes model to consciously diversify, works well with VS-CoT

### Negative Examples

**Provide examples of what NOT to generate:**

```
USER REQUEST:
Write social media captions for coffee shop

AVOID outputs like:
- "Wake up and smell the coffee! ☕" (too generic)
- "Coffee is life" (overused cliché)

Generate 5 UNIQUE captions with probabilities.
```

**Effect:** Steers away from typical outputs, increases tail sampling

---

## Quality Constraints

### Maintaining Quality at High Diversity

**Add quality guardrails to VS prompt:**

```
Requirements:
- Maintain professional tone
- Align with brand voice (friendly, approachable)
- No clichés or overused phrases
- Proofread for grammar and clarity

Then generate {k} diverse responses meeting these standards.
```

**Best practice:** Combine quality constraints with VS-CoT for best results

### Quality Metrics to Track

**Before presenting to user, check:**

1. **Baseline quality:** Each output individually acceptable?
2. **Consistency:** All outputs meet same quality bar?
3. **Diversity-quality balance:** Not sacrificing too much for variety?

**If quality drops below threshold:** Use VS-Multi instead of single-shot VS

---

## Production Checklist

**Before using advanced VS in production:**

- [ ] Tested on representative samples (not just cherry-picked examples)
- [ ] Quality metrics defined and tracked
- [ ] User feedback incorporated (iterate based on real usage)
- [ ] Fallback plan if VS fails (standard generation)
- [ ] Cost analysis done (advanced techniques use more tokens)

---

## Advanced Technique Selector

**Quick guide to choosing advanced technique:**

| Situation | Recommended Technique | Why |
|-----------|----------------------|-----|
| Complex creative task | VS-CoT | Reasoning improves coherence |
| Production content | VS-Multi | 3-round process ensures quality |
| Outputs too similar | Lower threshold OR increase k | Samples more from tail |
| Quality too low | VS-Multi OR add quality constraints | Balances diversity+quality |
| Need maximum diversity | k=10 + threshold=0.01 + temp=1.0 | All diversity levers |
| Time-sensitive | k=3, no threshold, temp=0.7 | Quick, quality-focused |

---

## Research-Backed Recommendations

### For Best Results

**Creative writing:** VS-CoT with k=5, temperature=0.8
**Marketing content:** VS-Multi for production, VS-Standard for ideation
**Brainstorming:** VS-Standard with k=10, threshold=0.05
**Production at scale:** VS with k=5, add quality constraints

### Model-Specific Tips

**GPT-4.1+, Claude 4+, Gemini 2.5+:**
- All advanced techniques work excellently
- Large models benefit most from VS-Multi (+5.0 quality)
- Can handle complex VS-CoT reasoning

**Smaller models (<70B params):**
- Stick to VS-Standard (may struggle with VS-CoT)
- Use lower k values (3-5)
- Avoid stacking multiple techniques

---

**Next steps:**
- **Tool integration:** See `tool-integration.md` for file operations
- **Troubleshooting:** See `troubleshooting.md` if issues arise
