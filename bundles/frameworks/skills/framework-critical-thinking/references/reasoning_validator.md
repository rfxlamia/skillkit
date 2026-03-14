# Reasoning Validator

## Purpose

The Reasoning Validator provides logical consistency checking and structural validation for reasoning chains to detect contradictions, gaps, and logical fallacies.

## Validation Types

### 1. Logical Consistency Checks

Verify that the reasoning does not contain contradictions.

```python
class LogicalConsistencyChecker:
    def check(self, reasoning_chain):
        issues = []
        contradictions = self.find_contradictions(reasoning_chain)
        issues.extend(contradictions)
        return {'valid': len(issues) == 0, 'issues': issues}

    def find_contradictions(self, chain):
        contradictions = []
        statements = extract_statements(chain)
        for i, stmt1 in enumerate(statements):
            for stmt2 in statements[i+1:]:
                if self.are_contradictory(stmt1, stmt2):
                    contradictions.append({
                        'type': 'contradiction',
                        'statement1': stmt1,
                        'statement2': stmt2
                    })
        return contradictions
```

### 2. Structural Completeness

Verify that the reasoning has all necessary components.

```python
class StructuralValidator:
    REQUIRED_COMPONENTS = [
        'problem_statement',
        'initial_assumptions',
        'reasoning_steps',
        'intermediate_conclusions',
        'final_conclusion'
    ]

    def validate(self, reasoning_chain):
        missing = []
        for component in self.REQUIRED_COMPONENTS:
            if not self.has_component(reasoning_chain, component):
                missing.append(component)
        return {'complete': len(missing) == 0, 'missing_components': missing}
```

### 3. Fallacy Detection

Identify common logical fallacies.

```python
class FallacyDetector:
    FALLACY_PATTERNS = {
        'circular_reasoning': {
            'check': lambda chain: chain['conclusion'] in chain['premises']
        },
        'false_dichotomy': {
            'check': self.check_false_dichotomy
        },
        'hasty_generalization': {
            'check': self.check_generalization
        }
    }

    def detect(self, reasoning_chain):
        detected = []
        for fallacy_name, pattern in self.FALLACY_PATTERNS.items():
            if pattern['check'](reasoning_chain):
                detected.append({'type': fallacy_name})
        return {'has_fallacies': len(detected) > 0, 'fallacies': detected}
```

## Usage Example

```python
validator = ReasoningValidator()
result = validator.validate(reasoning_chain)

if not result['valid']:
    for rec in result['recommendations']:
        print(f"Fix: {rec['action']}")
```

---

**Sources:**
- [Logical Reasoning in AI Systems](https://www.emergentmind.com/topics/logical-reasoning)
