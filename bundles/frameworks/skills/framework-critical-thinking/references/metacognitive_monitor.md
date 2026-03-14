# Metacognitive Monitor

## Purpose

The Metacognitive Monitor provides self-assessment and error detection capabilities for AI agents. It implements the Producer-Critic pattern to continuously evaluate the quality of reasoning and trigger corrective actions when needed.

## Architecture

### Producer-Critic Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    Master Agent                             │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────┐          ┌──────────────────────┐
│   Producer Agent     │          │    Critic Agent      │
│   (Generate)         │          │    (Evaluate)        │
└──────────┬───────────┘          └──────────┬───────────┘
           │                                 │
           │         ┌──────────────┐        │
           └────────►│   Output     │◄───────┘
                     │   Quality    │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Decision    │
                     │  Continue /  │
                     │  Refine /    │
                     │  Handoff     │
                     └──────────────┘
```

### Components

#### 1. Confidence Scorer

Evaluates confidence at multiple levels:

```python
class ConfidenceScorer:
    def assess_step(self, reasoning_step):
        return {
            'certainty_score': self.compute_certainty(reasoning_step),
            'consistency_check': self.check_internal_consistency(reasoning_step),
            'grounding_score': self.verify_grounding(reasoning_step),
            'overall_confidence': weighted_average([
                certainty * 0.4,
                consistency * 0.3,
                grounding * 0.3
            ])
        }
```

**Scoring dimensions:**
- **Certainty:** How definitive is the statement? (0.0 - 1.0)
- **Consistency:** Does it align with previous steps?
- **Grounding:** Is it supported by evidence/context?

#### 2. Anomaly Detector

Identifies unusual patterns in reasoning:

```python
class AnomalyDetector:
    def detect(self, thought_history):
        anomalies = []

        # Pattern 1: Sudden topic shift
        if self.topic_coherence_score(thought_history) < 0.5:
            anomalies.append(Anomaly.TOPIC_DRIFT)

        # Pattern 2: Repetitive reasoning
        if self.repetition_detected(thought_history):
            anomalies.append(Anomaly.LOOPING)

        # Pattern 3: Confidence degradation
        if self.confidence_trend(thought_history) == 'decreasing':
            anomalies.append(Anomaly.DEGRADING_QUALITY)

        # Pattern 4: Contradiction emergence
        if self.find_contradictions(thought_history):
            anomalies.append(Anomaly.CONTRADICTION)

        return anomalies
```

#### 3. Reflection Controller

Manages when and how to trigger reflection:

```python
class ReflectionController:
    def __init__(self):
        self.reflection_budget = 3  # Max reflections per task
        self.min_confidence_threshold = 0.7
        self.criticality_boost = 1.2  # Multiply threshold for critical tasks

    def should_reflect(self, current_state):
        if self.reflection_budget <= 0:
            return False, "Budget exhausted"

        adjusted_threshold = self.min_confidence_threshold
        if current_state.task_criticality == 'HIGH':
            adjusted_threshold *= self.criticality_boost

        if current_state.confidence < adjusted_threshold:
            return True, f"Confidence {current_state.confidence} below threshold {adjusted_threshold}"

        if current_state.anomalies_detected:
            return True, f"Anomalies detected: {current_state.anomalies}"

        return False, "No reflection needed"
```

## Implementation

### Basic Monitor Setup

```python
class MetacognitiveMonitor:
    def __init__(self, config):
        self.confidence_scorer = ConfidenceScorer()
        self.anomaly_detector = AnomalyDetector()
        self.reflection_controller = ReflectionController(config)
        self.thought_history = []

    def monitor(self, current_step, context):
        # Score the current step
        confidence = self.confidence_scorer.assess_step(current_step)

        # Update history
        self.thought_history.append({
            'step': current_step,
            'confidence': confidence,
            'timestamp': now()
        })

        # Detect anomalies
        anomalies = self.anomaly_detector.detect(self.thought_history)

        # Create state snapshot
        state = MonitorState(
            confidence=confidence['overall_confidence'],
            anomalies=anomalies,
            thought_count=len(self.thought_history),
            task_criticality=context.criticality
        )

        # Decide on action
        should_reflect, reason = self.reflection_controller.should_reflect(state)

        return MonitorResult(
            confidence=confidence,
            anomalies=anomalies,
            should_reflect=should_reflect,
            reflection_reason=reason,
            recommended_action=self.determine_action(state, should_reflect)
        )

    def determine_action(self, state, should_reflect):
        if state.confidence < 0.3:
            return Action.HUMAN_HANDOFF
        elif should_reflect:
            return Action.REFLECT_AND_REFINE
        elif state.anomalies:
            return Action.REVIEW_ANOMALIES
        else:
            return Action.CONTINUE
```

### Confidence Calibration

Calibrate confidence scores to match actual accuracy:

```python
def calibrate_confidence(raw_confidence, task_type):
    # Use historical performance data
    calibration_map = {
        'arithmetic': lambda x: x * 0.95,      # Usually overconfident
        'reasoning': lambda x: x * 0.85,       # Often overconfident
        'creative': lambda x: x * 0.70,        # Highly overconfident
        'factual': lambda x: min(x * 1.1, 1.0) # Often underconfident
    }

    calibrator = calibration_map.get(task_type, lambda x: x)
    return calibrator(raw_confidence)
```

## Monitoring Heuristics

### 1. Reasoning Quality Indicators

**Positive indicators:**
- Progressive narrowing of solution space
- Increasing specificity in claims
- Consistent terminology usage
- Appropriate uncertainty acknowledgment

**Negative indicators:**
- Circular reasoning
- Unjustified leaps
- Confusing correlation with causation
- Overgeneralization

### 2. Confidence-Accuracy Correlation

Track the relationship between stated confidence and actual correctness:

```python
def compute_calibration_error(confidence_history, accuracy_history):
    # Perfect calibration: confidence == accuracy
    # Overconfidence: confidence > accuracy
    # Underconfidence: confidence < accuracy

    expected_accuracy = sum(confidence_history) / len(confidence_history)
    actual_accuracy = sum(accuracy_history) / len(accuracy_history)

    return abs(expected_accuracy - actual_accuracy)
```

## Human Handoff Protocols

### When to Handoff

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Very low confidence | < 0.3 | Immediate handoff |
| Repeated reflection failures | > 3 attempts | Handoff with context |
| Critical task + uncertainty | Confidence < 0.8 | Request verification |
| Anomaly cluster | > 2 anomalies | Handoff for review |

### Handoff Context

Include in handoff:
- Current reasoning chain
- Confidence trajectory
- Detected anomalies
- Attempted corrections
- Specific uncertainty points

## Usage Example

```python
# Initialize monitor
monitor = MetacognitiveMonitor(config={
    'reflection_budget': 3,
    'confidence_threshold': 0.7,
    'enable_human_handoff': True
})

# Use in agent loop
for step in reasoning_process:
    result = monitor.monitor(step, context={'criticality': 'HIGH'})

    if result.recommended_action == Action.HUMAN_HANDOFF:
        await handoff_to_human(result)
        break

    elif result.recommended_action == Action.REFLECT_AND_REFINE:
        reflection = generate_reflection(result.anomalies)
        refined_step = refine_with_reflection(step, reflection)
        step = refined_step

    elif result.recommended_action == Action.REVIEW_ANOMALIES:
        for anomaly in result.anomalies:
            log_warning(f"Anomaly detected: {anomaly}")

    # Continue with (possibly refined) step
    execute(step)
```

## Performance Metrics

Track these metrics to evaluate monitor effectiveness:

1. **False Positive Rate:** Reflection triggered when not needed
2. **False Negative Rate:** Missed errors that should have been caught
3. **Calibration Error:** Difference between confidence and accuracy
4. **Reflection Success Rate:** % of reflections that improve output
5. **Average Reflections per Task:** Efficiency measure

## Best Practices

1. **Start with high thresholds** and gradually lower based on performance
2. **Log all monitoring decisions** for post-hoc analysis
3. **Calibrate confidence** per task type using historical data
4. **Respect the reflection budget** to avoid infinite loops
5. **Provide clear handoff reasons** for human reviewers

---

**Sources:**
- [Self-Corrective Agent Architecture](https://www.emergentmind.com/topics/self-corrective-agent-architecture)
- [Building Metacognitive AI Agents](https://rewire.it/blog/building-metacognitive-ai-agents-complete-guide/)
