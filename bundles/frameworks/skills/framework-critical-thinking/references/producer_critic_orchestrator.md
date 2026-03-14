# Producer-Critic Orchestrator

## Purpose

The Producer-Critic Orchestrator implements the Generate-Critique-Refine pattern for iterative improvement of AI outputs. It coordinates multiple specialized agents to produce higher quality results through structured feedback loops.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Master Agent (Orchestrator)                   │
└──────────────┬──────────────────────────────────────┬───────────┘
               │                                      │
               ▼                                      ▼
┌────────────────────────┐              ┌────────────────────────┐
│     Producer Agent     │              │      Critic Agent      │
│                        │              │                        │
│  - Generates initial   │─────────────►│  - Evaluates quality   │
│    output              │              │  - Identifies errors   │
│  - Incorporates        │◄─────────────│  - Suggests            │
│    feedback            │   critique   │    improvements        │
└────────────────────────┘              └────────────────────────┘
               ▲                                      │
               │                                      ▼
               │                         ┌────────────────────────┐
               │                         │   Refinement Decision  │
               └─────────────────────────│                        │
                  (if needs refinement)  │  - Satisfactory?       │
                                         │  - Budget exhausted?   │
                                         │  - Max iterations?     │
                                         └────────────────────────┘
```

## Components

### Master Agent (Orchestrator)

Coordinates the overall process:

```python
class ProducerCriticOrchestrator:
    def __init__(self, config):
        self.producer = ProducerAgent(config['producer'])
        self.critic = CriticAgent(config['critic'])
        self.max_iterations = config.get('max_iterations', 3)
        self.refinement_budget = config.get('budget', 5)
        self.satisfaction_threshold = config.get('threshold', 0.8)

    async def generate(self, task, context):
        iteration = 0
        history = []

        # Initial generation
        current_output = await self.producer.generate(task, context)

        while iteration < self.max_iterations:
            # Get critique
            critique = await self.critic.evaluate(current_output, task)

            history.append({
                'iteration': iteration,
                'output': current_output,
                'critique': critique
            })

            # Check if satisfactory
            if critique['satisfactory']:
                break

            # Check budget
            if self.refinement_budget <= 0:
                break

            # Refine
            current_output = await self.producer.refine(
                current_output,
                critique,
                context
            )
            self.refinement_budget -= 1
            iteration += 1

        return {
            'final_output': current_output,
            'iterations': iteration + 1,
            'history': history,
            'was_refined': iteration > 0
        }
```

### Producer Agent

Responsible for generation and refinement:

```python
class ProducerAgent:
    def __init__(self, config):
        self.model = config['model']
        self.temperature = config.get('temperature', 0.7)

    async def generate(self, task, context):
        prompt = self.build_generation_prompt(task, context)
        return await self.model.generate(prompt, temperature=self.temperature)

    async def refine(self, current_output, critique, context):
        refinement_prompt = f"""
Original task: {context['task']}

Current output:
{current_output}

Critique:
{critique['feedback']}

Issues identified:
{critique['issues']}

Please refine the output addressing all identified issues.
Maintain the strengths while fixing the weaknesses.
"""
        return await self.model.generate(
            refinement_prompt,
            temperature=self.temperature * 0.9  # Slightly lower for refinement
        )
```

### Critic Agent

Evaluates outputs and provides structured feedback:

```python
class CriticAgent:
    def __init__(self, config):
        self.model = config['model']
        self.evaluation_criteria = config.get('criteria', [
            'accuracy', 'completeness', 'clarity', 'relevance'
        ])

    async def evaluate(self, output, task):
        critique_prompt = f"""
Evaluate the following output for the given task.

Task: {task}

Output to evaluate:
{output}

Provide evaluation in this format:
1. Overall assessment: (satisfactory/needs improvement)
2. Scores (0-10):
   - Accuracy:
   - Completeness:
   - Clarity:
   - Relevance:
3. Strengths:
4. Issues identified:
5. Specific improvement suggestions:

Evaluation:
"""

        evaluation = await self.model.generate(critique_prompt)
        parsed = self.parse_evaluation(evaluation)

        return {
            'satisfactory': parsed['overall'] == 'satisfactory',
            'scores': parsed['scores'],
            'average_score': sum(parsed['scores'].values()) / len(parsed['scores']),
            'strengths': parsed['strengths'],
            'issues': parsed['issues'],
            'feedback': parsed['suggestions']
        }
```

## Refinement Strategies

### 1. Full Regeneration

Discard current output and generate fresh with critique as context.

**When to use:** Major structural issues or fundamental errors

```python
def full_regenerate(task, critique_history):
    context = synthesize_critiques(critique_history)
    return generate_with_enhanced_context(task, context)
```

### 2. Targeted Revision

Keep valid portions, only revise problematic sections.

**When to use:** Localized errors or specific improvements needed

```python
def targeted_revision(output, critique):
    issues = critique['issues']
    for issue in issues:
        if issue['location']:  # If issue has specific location
            output = revise_section(output, issue)
    return output
```

### 3. Progressive Enhancement

Build upon previous output incrementally.

**When to use:** Minor improvements needed

```python
def progressive_enhancement(output, critique):
    enhancements = critique['suggestions']
    for enhancement in enhancements:
        output = apply_enhancement(output, enhancement)
    return output
```

## Budget Management

Control computational cost:

```python
class RefinementBudget:
    def __init__(self, max_tokens, max_time, max_iterations):
        self.max_tokens = max_tokens
        self.max_time = max_time
        self.max_iterations = max_iterations
        self.used_tokens = 0
        self.start_time = time.now()
        self.iterations = 0

    def can_continue(self):
        if self.iterations >= self.max_iterations:
            return False, "Max iterations reached"

        if self.used_tokens >= self.max_tokens:
            return False, "Token budget exhausted"

        elapsed = time.now() - self.start_time
        if elapsed >= self.max_time:
            return False, "Time budget exhausted"

        return True, "Can continue"

    def consume(self, tokens_used):
        self.used_tokens += tokens_used
        self.iterations += 1
```

## Early Stopping Conditions

Stop refinement when:

```python
STOP_CONDITIONS = {
    'satisfactory': lambda s: s['average_score'] >= SATISFACTION_THRESHOLD,
    'diminishing_returns': lambda h: score_improvement(h) < 0.05,
    'oscillation': lambda h: detect_oscillation(h),
    'budget_exhausted': lambda b: b.can_continue()[0] == False
}
```

## Usage Patterns

### Pattern 1: Quality-First

Maximize quality regardless of cost:

```python
config = {
    'max_iterations': 5,
    'budget': 10,
    'threshold': 0.9,
    'stop_on_satisfaction': True
}
```

### Pattern 2: Budget-Constrained

Best quality within budget:

```python
config = {
    'max_iterations': 3,
    'budget': 5,
    'threshold': 0.8,
    'early_stop': True
}
```

### Pattern 3: Fast Iteration

Quick improvements, accept "good enough":

```python
config = {
    'max_iterations': 2,
    'budget': 3,
    'threshold': 0.7,
    'parallel_critiques': True
}
```

## Evaluation Metrics

Track orchestration effectiveness:

- **Refinement Success Rate:** % of iterations that improve score
- **Average Iterations:** Mean iterations before satisfaction or stop
- **Quality Improvement:** Score delta from initial to final
- **Cost Efficiency:** Quality gain per token spent
- **Satisfaction Rate:** % of tasks reaching threshold

## Best Practices

1. **Start with strict criteria** and relax based on performance
2. **Log all critiques** for post-hoc analysis and pattern detection
3. **Vary temperatures** between generation and refinement
4. **Set hard limits** to prevent infinite loops
5. **Parallelize critiques** when multiple critics available
6. **Cache successful patterns** for similar future tasks

## Common Pitfalls

- **Over-refinement:** Excessive iterations with diminishing returns
- **Critique drift:** Critic becomes increasingly harsh over iterations
- **Oscillation:** Alternating between two imperfect solutions
- **Budget explosion:** Underestimating computational cost

---

**Sources:**
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
