# Reasoning Router

## Purpose

The Reasoning Router analyzes task characteristics and automatically selects the optimal reasoning method (CoT, ToT, GoT, or Self-Consistency) based on complexity, structure, and criticality of the task.

## Decision Matrix

### Selection Criteria

| Factor | CoT | ToT-BFS | ToT-DFS | GoT | Self-Consistency |
|--------|-----|---------|---------|-----|------------------|
| **Complexity** | Low | High | High | Very High | Medium |
| **Path Count** | Single | Multiple | Multiple | Interconnected | Single |
| **Backtracking** | No | Yes | Yes | Yes | No |
| **Exploration** | Linear | Breadth | Depth | Graph | Parallel |
| **Cost** | Low | High | High | Very High | Medium |
| **Latency** | Fast | Slow | Slow | Very Slow | Medium |

### Selection Algorithm

```
function select_reasoning_method(problem):
    complexity_score = analyze_complexity(problem)
    path_diversity = estimate_path_count(problem)
    criticality = assess_criticality(problem)
    interconnectivity = check_interconnections(problem)

    if criticality == HIGH and path_diversity == SINGLE:
        return SELF_CONSISTENCY

    if interconnectivity == HIGH:
        return GRAPH_OF_THOUGHTS

    if path_diversity == MULTIPLE:
        if requires_deep_exploration(problem):
            return TREE_OF_THOUGHTS_DFS
        else:
            return TREE_OF_THOUGHTS_BFS

    return CHAIN_OF_THOUGHT
```

## Implementation

### Complexity Analysis

```python
def analyze_complexity(problem):
    factors = {
        'step_count': estimate_reasoning_steps(problem),
        'domain_knowledge': assess_domain_requirements(problem),
        'ambiguity_level': detect_ambiguity(problem),
        'constraint_density': count_constraints(problem)
    }

    # Weighted scoring
    score = (
        factors['step_count'] * 0.3 +
        factors['domain_knowledge'] * 0.2 +
        factors['ambiguity_level'] * 0.3 +
        factors['constraint_density'] * 0.2
    )

    if score < 0.3:
        return COMPLEXITY.LOW
    elif score < 0.7:
        return COMPLEXITY.MEDIUM
    else:
        return COMPLEXITY.HIGH
```

### Method Configurations

#### Chain-of-Thought (CoT)

**Use when:**
- Straightforward arithmetic or logic
- Single solution path
- Well-defined problem space
- Low ambiguity

**Template:**
```
Let's solve this step by step:
1. [First step with explanation]
2. [Second step with explanation]
...
Therefore, [final answer]
```

#### Tree-of-Thoughts - BFS (ToT-BFS)

**Use when:**
- Multiple viable approaches exist
- Need to compare alternatives at each step
- Problem requires exploration of options

**Configuration:**
```python
ToTConfig(
    branching_factor=3,        # Number of candidates per step
    beam_width=2,              # Keep top N candidates
    max_depth=5,               # Maximum reasoning depth
    search_algorithm='BFS',
    evaluation_criteria='progress_toward_goal'
)
```

#### Tree-of-Thoughts - DFS (ToT-DFS)

**Use when:**
- Deep reasoning chains needed
- Early decisions strongly influence outcome
- Problem has hierarchical structure

**Configuration:**
```python
ToTConfig(
    branching_factor=2,
    max_depth=10,
    search_algorithm='DFS',
    backtrack_threshold=0.3,   # Backtrack if score below this
    evaluation_criteria='path_viability'
)
```

#### Graph-of-Thoughts (GoT)

**Use when:**
- Interconnected reasoning required
- Thoughts can merge or aggregate
- Non-linear problem structure

**Configuration:**
```python
GoTConfig(
    node_types=['premise', 'inference', 'conclusion'],
    edge_types=['supports', 'contradicts', 'aggregates'],
    aggregation_functions=['sum', 'max', 'graph_attention'],
    max_nodes=50
)
```

#### Self-Consistency

**Use when:**
- High-stakes decisions
- Single answer required
- Need confidence estimation

**Configuration:**
```python
SelfConsistencyConfig(
    sample_count=10,           # Number of reasoning paths
    temperature=0.7,           # Variation in sampling
    aggregation_method='majority_vote',
    confidence_threshold=0.8
)
```

## Usage Examples

### Example 1: Simple Math Problem

**Problem:** "What is 25 * 48?"

**Analysis:**
- Complexity: Low (single arithmetic operation)
- Path diversity: Single
- Criticality: Low

**Selection:** Chain-of-Thought

**Reasoning:**
```
25 * 48 = 25 * (50 - 2)
        = 25 * 50 - 25 * 2
        = 1250 - 50
        = 1200
```

### Example 2: Game of 24

**Problem:** "Make 24 using 4, 9, 10, 13"

**Analysis:**
- Complexity: High (multiple operations needed)
- Path diversity: Multiple (different operation combinations)
- Criticality: Medium

**Selection:** Tree-of-Thoughts (BFS)

**Exploration:**
```
Level 0: [4, 9, 10, 13]
Level 1: [(4+9), 10, 13], [(13-9), 4, 10], [(10*4), 9, 13], ...
Level 2: ... continue until 24 reached or max depth
```

### Example 3: Complex Planning

**Problem:** "Plan a 5-day trip to Japan considering budget, weather, and preferences"

**Analysis:**
- Complexity: Very High
- Interconnectivity: High (decisions affect each other)
- Multiple constraints

**Selection:** Graph-of-Thoughts

**Graph Structure:**
- Nodes: Destinations, activities, accommodations, transport
- Edges: Temporal dependencies, budget constraints, preferences

## Best Practices

1. **Start Simple:** Default to CoT unless complexity indicators are present
2. **Monitor Performance:** Track success rates per method for your domain
3. **Adaptive Switching:** Allow runtime method switching if initial choice underperforms
4. **Budget Awareness:** Consider computational cost vs accuracy trade-offs
5. **Hybrid Approaches:** Combine methods (e.g., ToT with Self-Consistency for final answer)

## Common Pitfalls

- **Over-engineering:** Using ToT for simple problems wastes compute
- **Under-exploring:** Using CoT for complex multi-path problems leads to dead ends
- **Fixed Configuration:** Not adapting parameters to problem specifics
- **Ignoring Latency:** ToT/GoT may be too slow for real-time applications

---

**Sources:**
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
