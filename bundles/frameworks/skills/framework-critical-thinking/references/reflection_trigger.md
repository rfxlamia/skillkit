# Reflection Trigger

## Purpose

The Reflection Trigger provides rule-based conditions for activating self-correction loops. It determines when an agent should pause, evaluate its progress, and potentially adjust its approach.

## Trigger Conditions

### 1. Confidence Threshold Violations

```python
class ConfidenceTrigger:
    def __init__(self, thresholds):
        self.thresholds = {
            'critical': 0.3,
            'warning': 0.5,
            'caution': 0.7
        }

    def check(self, current_state):
        confidence = current_state.get('confidence', 1.0)
        if confidence < self.thresholds['critical']:
            return TriggerResult(
                should_reflect=True,
                priority='critical',
                reason=f"Confidence {confidence:.2f} critically low"
            )
        return TriggerResult(should_reflect=False)
```

### 2. Repeated Action Patterns

```python
class PatternTrigger:
    def check(self, action_history):
        if len(action_history) < 3:
            return TriggerResult(should_reflect=False)

        recent = action_history[-3:]
        if self.are_identical(recent):
            return TriggerResult(
                should_reflect=True,
                priority='high',
                reason="Same action repeated 3 times"
            )
        return TriggerResult(should_reflect=False)
```

### 3. Latency Spikes

```python
class LatencyTrigger:
    def check(self, elapsed_time, expected_time):
        if elapsed_time > expected_time * 5:
            return TriggerResult(
                should_reflect=True,
                priority='critical',
                reason="Latency 5x expected - possible infinite loop"
            )
        return TriggerResult(should_reflect=False)
```

## Usage Example

```python
trigger = ReflectionTrigger(config={'confidence': {'critical': 0.3}})

for step_number, state in enumerate(agent_states):
    result = trigger.should_reflect(state, step_number)
    if result.should_reflect:
        reflection = generate_reflection(state)
        state = apply_reflection(state, reflection)
```

---

**Sources:**
- [Self-Corrective Agent Architecture](https://www.emergentmind.com/topics/self-corrective-agent-architecture)
