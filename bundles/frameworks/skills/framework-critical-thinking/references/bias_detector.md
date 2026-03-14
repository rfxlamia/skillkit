# Bias Detector

## Purpose

The Bias Detector identifies cognitive biases in AI reasoning processes and provides mitigation strategies to ensure more objective and balanced analysis.

## Types of Cognitive Bias

### 1. Confirmation Bias

**Definition:** Tendency to search for, interpret, and recall information that confirms pre-existing beliefs.

**Detection indicators:**
- Only considering evidence supporting initial hypothesis
- Dismissing contradictory evidence without evaluation
- Selective citation of sources
- Premature conclusion after finding confirming evidence

**Detection:**
```python
def detect_confirmation_bias(reasoning_chain):
    flags = []

    # Check for one-sided evidence consideration
    evidence = extract_evidence(reasoning_chain)
    supporting = count_supporting_evidence(evidence)
    contradicting = count_contradicting_evidence(evidence)

    if contradicting == 0 and supporting > 0:
        flags.append("No contradictory evidence considered")

    if supporting / (supporting + contradicting + 1) > 0.8:
        flags.append("Highly imbalanced evidence consideration")

    # Check for premature stopping
    if stopped_after_first_confirmation(reasoning_chain):
        flags.append("Stopped reasoning after initial confirmation")

    return {
        'bias_detected': len(flags) > 0,
        'confidence': min(len(flags) * 0.3, 1.0),
        'flags': flags
    }
```

**Mitigation:**
```python
def mitigate_confirmation_bias(reasoning_chain):
    # Force consideration of alternatives
    alternatives = generate_alternative_hypotheses(reasoning_chain)

    # Require devil's advocate analysis
    counter_arguments = generate_counter_arguments(reasoning_chain)

    # Evidence balance check
    evidence_audit = audit_evidence_balance(reasoning_chain)

    return {
        'alternatives_considered': alternatives,
        'counter_arguments': counter_arguments,
        'evidence_balance': evidence_audit,
        'revised_reasoning': incorporate_perspective(reasoning_chain, alternatives)
    }
```

### 2. Anchoring Bias

**Definition:** Over-reliance on the first piece of information offered (the "anchor") when making decisions.

**Detection indicators:**
- First estimate heavily influences subsequent estimates
- Insufficient adjustment from initial value
- Sticky initial assumptions despite new evidence

**Detection:**
```python
def detect_anchoring_bias(reasoning_chain):
    flags = []

    # Check for early fixation
    if early_value_heavy_influence(reasoning_chain):
        flags.append("Early value dominates reasoning")

    # Check adjustment magnitude
    adjustments = extract_adjustments(reasoning_chain)
    if all(adj < 0.1 for adj in adjustments):  # Less than 10% adjustment
        flags.append("Minimal adjustment from initial estimates")

    # Check for anchoring language
    anchoring_phrases = ['based on the initial', 'starting from', 'given that']
    if count_phrases(reasoning_chain, anchoring_phrases) > 2:
        flags.append("Anchoring language detected")

    return {
        'bias_detected': len(flags) > 0,
        'confidence': min(len(flags) * 0.35, 1.0),
        'flags': flags
    }
```

**Mitigation:**
```python
def mitigate_anchoring_bias(reasoning_chain):
    # Generate multiple independent starting points
    alternative_anchors = generate_alternative_anchors(reasoning_chain)

    # Blind estimation (without initial anchor)
    blind_estimate = generate_estimate_without_anchor(reasoning_chain)

    # Triangulation from multiple sources
    triangulated = triangulate_estimates([reasoning_chain] + alternative_anchors)

    return {
        'alternative_anchors': alternative_anchors,
        'blind_estimate': blind_estimate,
        'triangulated_result': triangulated
    }
```

### 3. Availability Heuristic

**Definition:** Judging likelihood of events based on how easily examples come to mind.

**Detection indicators:**
- Overestimating recent or dramatic events
- Citing only readily available examples
- Ignoring base rates in favor of vivid anecdotes

**Detection:**
```python
def detect_availability_heuristic(reasoning_chain):
    flags = []

    examples = extract_examples(reasoning_chain)

    # Check recency bias
    if all(is_recent(example) for example in examples):
        flags.append("Only recent examples considered")

    # Check for vivid/violent event overrepresentation
    vivid_ratio = count_vivid_examples(examples) / len(examples)
    if vivid_ratio > 0.5:
        flags.append("Over-reliance on vivid/memorable examples")

    # Check base rate neglect
    if mentions_base_rate(reasoning_chain) == False:
        flags.append("No consideration of base rates")

    return {
        'bias_detected': len(flags) > 0,
        'confidence': min(len(flags) * 0.3, 1.0),
        'flags': flags
    }
```

**Mitigation:**
```python
def mitigate_availability_heuristic(reasoning_chain):
    # Systematic data gathering
    systematic_data = gather_representative_data(reasoning_chain)

    # Base rate information
    base_rates = lookup_base_rates(reasoning_chain)

    # Diverse example set
    diverse_examples = gather_diverse_examples(reasoning_chain)

    return {
        'systematic_data': systematic_data,
        'base_rates': base_rates,
        'diverse_examples': diverse_examples
    }
```

### 4. Framing Effects

**Definition:** Making different decisions based on how information is presented (gain vs loss frame).

**Detection indicators:**
- Inconsistent preferences based on wording
- Risk-seeking in loss domain, risk-averse in gain domain
- Identical outcomes evaluated differently

**Detection:**
```python
def detect_framing_effects(reasoning_chain):
    flags = []

    # Check for frame-dependent reasoning
    frame_type = detect_frame_type(reasoning_chain)

    if frame_type == 'loss' and risk_seeking_behavior(reasoning_chain):
        flags.append("Loss frame with risk-seeking behavior")

    if frame_type == 'gain' and risk_averse_behavior(reasoning_chain):
        flags.append("Gain frame with risk-averse behavior")

    # Check for logically equivalent but differently evaluated options
    equivalent_options = find_equivalent_options(reasoning_chain)
    if different_evaluations(equivalent_options):
        flags.append("Inconsistent evaluation of equivalent options")

    return {
        'bias_detected': len(flags) > 0,
        'detected_frame': frame_type,
        'confidence': min(len(flags) * 0.4, 1.0),
        'flags': flags
    }
```

**Mitigation:**
```python
def mitigate_framing_effects(reasoning_chain):
    # Reframe in opposite direction
    opposite_frame = reframe_opposite(reasoning_chain)

    # Neutral frame
    neutral_frame = create_neutral_frame(reasoning_chain)

    # Expected value calculation
    ev_analysis = calculate_expected_values(reasoning_chain)

    return {
        'original_frame': reasoning_chain,
        'opposite_frame': opposite_frame,
        'neutral_frame': neutral_frame,
        'expected_value_analysis': ev_analysis
    }
```

### 5. Recency Bias

**Definition:** Giving more weight to recent events than historical data.

**Detection:**
```python
def detect_recency_bias(reasoning_chain):
    flags = []

    temporal_references = extract_temporal_references(reasoning_chain)

    # Check recency concentration
    recent_ratio = count_recent_references(temporal_references) / len(temporal_references)
    if recent_ratio > 0.7:
        flags.append("Heavy weighting of recent information")

    # Check historical context
    if lacks_historical_context(reasoning_chain):
        flags.append("Insufficient historical context")

    return {
        'bias_detected': len(flags) > 0,
        'confidence': min(len(flags) * 0.35, 1.0),
        'flags': flags
    }
```

## Implementation

### Bias Detection Pipeline

```python
class BiasDetector:
    def __init__(self):
        self.detectors = {
            'confirmation': detect_confirmation_bias,
            'anchoring': detect_anchoring_bias,
            'availability': detect_availability_heuristic,
            'framing': detect_framing_effects,
            'recency': detect_recency_bias
        }

    def detect_all(self, reasoning_chain):
        results = {}
        detected_biases = []

        for bias_name, detector in self.detectors.items():
            result = detector(reasoning_chain)
            results[bias_name] = result

            if result['bias_detected']:
                detected_biases.append({
                    'type': bias_name,
                    'confidence': result['confidence'],
                    'flags': result['flags']
                })

        return {
            'detected_biases': detected_biases,
            'bias_count': len(detected_biases),
            'overall_risk': self.calculate_risk_score(detected_biases),
            'details': results
        }

    def calculate_risk_score(self, detected_biases):
        if not detected_biases:
            return 0.0

        # Weight by confidence and number
        total_confidence = sum(b['confidence'] for b in detected_biases)
        return min(total_confidence / len(detected_biases) * (1 + len(detected_biases) * 0.1), 1.0)
```

### Mitigation Strategies

```python
def apply_mitigation(detection_result, reasoning_chain):
    mitigations = {
        'confirmation': mitigate_confirmation_bias,
        'anchoring': mitigate_anchoring_bias,
        'availability': mitigate_availability_heuristic,
        'framing': mitigate_framing_effects,
        'recency': mitigate_recency_bias
    }

    applied_mitigations = []

    for bias in detection_result['detected_biases']:
        bias_type = bias['type']
        if bias_type in mitigations:
            mitigation_result = mitigations[bias_type](reasoning_chain)
            applied_mitigations.append({
                'bias_type': bias_type,
                'mitigation': mitigation_result
            })

    return {
        'original': reasoning_chain,
        'mitigations': applied_mitigations,
        'revised_reasoning': synthesize_mitigations(reasoning_chain, applied_mitigations)
    }
```

## Bias Prevention Checklist

Before finalizing any analysis:

- [ ] Have I considered evidence that contradicts my conclusion?
- [ ] Did I evaluate multiple hypotheses, not just the first one?
- [ ] Am I relying on recent or vivid examples rather than systematic data?
- [ ] Have I checked base rates and historical context?
- [ ] Would I reach the same conclusion if the problem were framed differently?
- [ ] Am I anchored to an initial estimate without sufficient adjustment?
- [ ] Have I sought diverse perspectives on this issue?
- [ ] Is my confidence level calibrated to the actual evidence strength?

## Usage Example

```python
# Initialize detector
detector = BiasDetector()

# Analyze reasoning
reasoning = agent.generate_reasoning(problem)
bias_result = detector.detect_all(reasoning)

if bias_result['bias_count'] > 0:
    print(f"⚠️  Detected {bias_result['bias_count']} potential biases:")
    for bias in bias_result['detected_biases']:
        print(f"   - {bias['type']} (confidence: {bias['confidence']:.2f})")

    # Apply mitigations
    mitigated = apply_mitigation(bias_result, reasoning)

    # Use revised reasoning
    final_output = mitigated['revised_reasoning']
else:
    final_output = reasoning
```

---

**Sources:**
- [Thinking, Fast and Slow - Daniel Kahneman](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)
- [Cognitive Bias Mitigation](https://en.wikipedia.org/wiki/Cognitive_bias_mitigation)
