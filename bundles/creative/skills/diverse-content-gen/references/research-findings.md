# VS Research Findings & Benchmarks

**Purpose:** Research-backed performance data, model compatibility, and evidence base

**Load when:** User asks about effectiveness, model selection, or wants evidence

**Source:** "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity" (Zhang et al., 2025)

---

## Key Research Results

### Diversity Improvements

**Creative writing tasks (average across models):**

| Task | Direct Prompting | VS-Standard | VS-CoT | Improvement |
|------|-----------------|-------------|---------|-------------|
| **Poem** | 11.4% | 21.9% | **25.8%** | **+126% diversity** |
| **Story** | 22.2% | 34.7% | **38.2%** | **+72% diversity** |
| **Joke** | 30.0% | 62.5% | **62.9%** | **+110% diversity** |

**Key finding:** VS-CoT achieves **1.6-2.1× diversity improvement** while maintaining quality

### Quality Maintenance

**Quality scores remain high:**
- Poems: VS-CoT achieves highest quality AND diversity
- Stories: All VS variants within 3% of baseline quality
- Jokes: Quality scores 82-84/100 across all methods

**Conclusion:** Diversity gains don't sacrifice quality

### Human Evaluation

**30 annotators rated diversity (4-point Likert scale):**

| Task | Direct | Sequence | VS-Standard | Improvement |
|------|--------|----------|-------------|-------------|
| Poem | 1.90 | 2.07 | **2.39** | **+25.7%** |
| Story | 2.74 | 2.76 | **3.06** | **+11.7%** |
| Joke | 1.83 | 2.93 | **3.01** | **+64.5%** |

**Statistical significance:** p < 0.001 for all improvements

---

## Model Compatibility

### Tested Models (Research)

**Excellent compatibility:**
- GPT-4.1 series (GPT-4.1, GPT-4.1-mini)
- Claude 4 series (Claude 4 Sonnet)
- Gemini 2.5 series (Gemini 2.5 Pro, Flash)
- DeepSeek-R1
- o3
- Llama-3.1-70B and larger

**Limited compatibility:**
- Models < 70B parameters show quality degradation
- Smaller models may not follow VS format reliably

### Model-Specific Performance

| Model Family | Diversity Gain | Quality Impact | Best For |
|--------------|----------------|----------------|----------|
| **GPT-4.1** | ✅ Excellent (+15.4% large model) | Neutral | General purpose, balanced |
| **Claude 4** | ✅ Excellent | Slight improvement | Creative writing, narratives |
| **Gemini 2.5** | ✅ Excellent | Neutral | Balanced across tasks |
| **DeepSeek-R1** | ✅ Excellent | Improved factual accuracy | Reasoning tasks, QA |
| **o3** | ✅ Excellent | Improved | Complex prompts, CoT |
| **Llama-3.1-70B** | ✅ Good | -3 to -5% | Open source, cost-effective |
| **Smaller models** | ⚠️ Limited (-2% to -8%) | Quality drop | Not recommended |

### Emergent Trend: Larger Models Benefit More

**Diversity gain over direct prompting:**

| Model Size | Sequence | VS-Standard | VS-CoT | VS-Multi |
|------------|----------|-------------|---------|----------|
| **Small** (Mini, Flash) | +4.4% | +5.4% | +6.4% | +6.8% |
| **Large** (Full, Pro) | +9.6% | +15.4% | +9.9% | +7.7% |

**Ratio:** Large models gain **1.5-2.0× more diversity** than small models

**Quality improvements with scale:**
- Small models: VS-Multi +0.7% quality
- Large models: VS-Multi **+5.0% quality**

**Conclusion:** Frontier models turn prompt complexity into benefits

---

## Performance Benchmarks

### Open-Ended QA (CoverageQA dataset)

**Task:** Generate diverse valid answers (e.g., "Name a US state")

| Metric | Direct | Sequence | VS-Standard | VS-CoT |
|--------|--------|----------|-------------|---------|
| **KL Divergence** ↓ | 14.43 | 4.27 | 3.50 | **3.23** |
| **Coverage** ↑ | 0.10 | 0.64 | 0.67 | **0.68** |
| **Precision** ↑ | 1.00 | 0.96 | 0.96 | **0.96** |

**Key finding:** VS-CoT achieves **71% coverage** of valid answers (vs. 10% direct) while maintaining 96% precision

### Dialogue Simulation (PersuasionForGood)

**Task:** Simulate human persuadee in donation conversation

**Donation distribution alignment:**

| Model | Method | KS Test ↓ | L1 Distance ↓ |
|-------|--------|-----------|---------------|
| GPT-4.1 | Direct | 0.373 | 0.613 |
| GPT-4.1 | **VS** | **0.211** | **0.579** |
| DeepSeek-R1 | Direct | 0.368 | 0.684 |
| DeepSeek-R1 | **VS** | **0.114** | **0.642** |

**Linguistic diversity:**

| Metric | Direct | VS-Standard | Human | Fine-tuned |
|--------|--------|-------------|--------|------------|
| Distinct-1 | 0.178 | **0.269** | 0.419 | 0.400 |
| Distinct-2 | 0.633 | **0.763** | 0.809 | 0.791 |
| Semantic Diversity | 0.577 | **0.664** | 0.721 | 0.696 |

**Key finding:** VS with GPT-4.1 matches fine-tuned model performance, no training needed

### Synthetic Data Generation (Math problems)

**Task:** Generate 1K math problems, train models on synthetic data

**Downstream accuracy (average across 3 benchmarks):**

| Method | Qwen2.5-7B | Qwen3-1.7B | Qwen3-4B | Average |
|--------|------------|------------|----------|---------|
| Baseline (no synth) | 27.2 | 30.5 | 40.7 | 32.8 |
| Direct | 26.1 | 31.4 | 34.5 | 30.6 ⚠️ |
| Sequence | 30.5 | 31.0 | 42.1 | 34.3 |
| **VS-Standard** | 32.7 | 33.6 | 45.5 | **36.1** |
| **VS-CoT** | 33.4 | 33.7 | 45.9 | **36.9** |
| **VS-Multi** | **34.8** | **34.9** | **45.0** | **37.5** |

**Key finding:** VS-Multi achieves **37.5% accuracy** vs. 32.8% baseline (+4.7%). Direct prompting can actually **hurt** performance (-2.2%) due to mode collapse.

---

## Safety & Factual Accuracy

### Safety Evaluation (StrongReject benchmark)

**Task:** 353 harmful prompts, measure refusal rate

| Method | Refusal Rate | Δ vs. Direct |
|--------|--------------| -------------|
| Direct | 98.22% | - |
| VS-Standard | 97.45% | -0.77% |
| VS-CoT | 97.81% | -0.41% |
| VS-Multi | 97.91% | -0.31% |

**Conclusion:** VS maintains **97%+ safety**, only minor (0.3-0.8%) decrease in refusal rate

### Factual Accuracy (SimpleQA)

**Task:** 300 factual questions

| Metric | Direct | CoT | VS-Standard | VS-CoT |
|--------|--------|-----|-------------|---------|
| **Top@1 Accuracy** | 0.310 | 0.342 | 0.329 | **0.348** |
| **Pass@N Accuracy** | 0.430 | 0.473 | 0.448 | **0.485** |

**Conclusion:** VS-CoT achieves **highest accuracy** on both metrics. Diversity doesn't compromise correctness.

---

## Optimal Hyperparameters (Research-Backed)

### k (Candidates per Call)

**Quality-diversity tradeoff:**

| k | Diversity Gain | Quality Impact | Recommended For |
|---|----------------|----------------|-----------------|
| **3** | +15% | -2% | Quick tasks, time-sensitive |
| **5** | +35% | -3% | **Optimal balance ✅** |
| **10** | +52% | -5% | Deep exploration, ideation |
| **20** | +68% | -8% | Research, synthetic data |

**Recommendation:** k=5 provides best practical balance

### Probability Threshold

**Diversity tuning (poem generation):**

| Threshold | Diversity | Notes |
|-----------|-----------|-------|
| None | 17.0% | Baseline VS |
| 0.10 | 17.8% | +5% diversity |
| **0.01** | **18.2%** | **+7% diversity (optimal)** |
| 0.001 | 17.4% | Diminishing returns |

**Optimal range:** 0.01-0.10 for most tasks

### Temperature Combination

**VS is orthogonal to temperature** - can combine both:

- VS alone achieves **1.6-2.1× diversity**
- VS + temperature 0.8-1.0 pushes Pareto front further
- Optimal: VS with temperature 0.8-1.0

---

## Post-Training Stage Analysis

**Using Tulu-3 family (Llama-3.1-70B base → SFT → DPO → RLVR):**

| Stage | Direct Diversity | VS Diversity | Base Model Diversity |
|-------|------------------|--------------|---------------------|
| Base | - | - | 45.4% |
| After SFT | 20.8% | 30.3% | - |
| After DPO | **10.8%** | **30.2%** | - |
| After RLVR | 10.8% | 30.3% | - |

**Key findings:**
- Direct prompting: **182.6% diversity drop** after DPO (45.4% → 10.8%)
- VS: Maintains ~30% diversity across all stages
- VS recovers **66.8%** of base model diversity (vs. 23.8% for direct)

**Conclusion:** Alignment dramatically reduces diversity, but VS recovers most of it

---

## Use Case Suitability

### Highly Effective For:

✅ **Creative writing** (poems, stories, scripts)
- Research shows: +60-120% diversity improvement
- Quality maintained or improved

✅ **Marketing content** (campaigns, taglines, ad copy)
- Multiple valid approaches
- Benefits from exploring creative space

✅ **Brainstorming & ideation**
- Open-ended exploration
- No single "correct" answer

✅ **Open-ended QA** (tasks with multiple valid answers)
- Research shows: +400% coverage increase
- Example: "Name a US state" → covers 71% vs. 10%

✅ **Synthetic data generation**
- Diverse training data improves model performance
- Research shows: +4.7% downstream accuracy

### Less Effective For:

⚠️ **Single-answer factual questions**
- Example: "What's the capital of France?" → Only Paris is correct
- VS adds no value

⚠️ **Deterministic outputs**
- Tasks requiring exact, reproducible results
- Diversity is not desired

⚠️ **Real-time low-latency applications**
- VS requires k× more generation time
- Not suitable for < 1 second response requirements

⚠️ **Weak models** (< 70B parameters)
- Quality degradation observed
- May not follow VS format reliably

---

## Cost-Benefit Analysis

### Token Usage

**Typical VS call:**
- Prompt: ~200 tokens (template + request)
- Response: ~300 tokens (k=5, JSON format)
- **Total: ~500 tokens per VS call**

**Comparison:**
- Direct prompting: 1 call × 100 tokens = 100 tokens
- VS: 1 call × 500 tokens = 500 tokens
- **Multiplier: 5× tokens for 2× diversity**

### When Worth the Cost

✅ **High value per output** (production content, campaigns, key messaging)
✅ **Diversity critical** (avoiding repetitive content, exploring options)
✅ **User satisfaction** (25.7% higher ratings in human evaluation)
✅ **Downstream quality** (better synthetic training data)

⚠️ **Not worth for:**
- High-volume low-value content
- Single-answer tasks
- Extremely tight budgets

---

## Comparative Methods

### VS vs. Temperature Tuning

| Method | Diversity Gain | Quality Impact | Works with API? |
|--------|----------------|----------------|-----------------|
| Temperature ↑ | Moderate | Can degrade | ✅ Yes |
| **VS** | **High (2×)** | **Maintained** | ✅ Yes |
| VS + Temp | **Very High** | Moderate | ✅ Yes |

**Conclusion:** VS and temperature are complementary, can combine

### VS vs. Multiple Sampling

| Method | API Calls | Diversity | Token Cost |
|--------|-----------|-----------|------------|
| Sample 5× | 5 | Low (mode collapse) | 5× |
| **VS (k=5)** | **1** | **High** | **1× (but larger)** |

**Conclusion:** VS more token-efficient than repeated sampling

### VS vs. Fine-Tuning

| Method | Setup Cost | Inference Cost | Flexibility |
|--------|------------|----------------|-------------|
| Fine-tune for diversity | High (data + compute) | Same as base | Low |
| **VS** | **Zero** | **Higher tokens** | **High** |

**Conclusion:** VS is training-free, more flexible

---

## Research Methodology Notes

**Dataset sizes:**
- Creative writing: 100 samples per task
- Open-ended QA: 40 questions, 100 samples each
- Dialogue simulation: 200 test dialogues
- Factual accuracy: 300 questions (SimpleQA)
- Safety: 353 harmful prompts (StrongReject)

**Models tested:**
- GPT-4.1 series, Gemini 2.5 series, Claude 4 series
- DeepSeek-R1, o3, Llama-3.1-70B
- Tulu-3 family (for post-training analysis)

**Metrics:**
- Diversity: Self-BLEU, distinct-n, semantic diversity, coverage
- Quality: GPT-4-as-judge, human evaluation (Likert scale)
- Accuracy: Exact match, pass@N
- Safety: Refusal rate

---

## Citation

```bibtex
@article{zhang2025verbalized,
  title={Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity},
  author={Zhang, Jiayi and Yu, Simon and Chong, Derek and Sicilia, Anthony and Tomz, Michael R. and Manning, Christopher D. and Shi, Weiyan},
  journal={arXiv preprint arXiv:2510.01171},
  year={2025}
}
```

**Project page:** https://verbalized-sampling.github.io

---

**For practical implementation:** See `vs-core-technique.md`
**For task-specific workflows:** See `task-workflows.md`
