# Memory Curator

## Table of Contents

- [Purpose](#purpose)
- [Memory Types (CoALA Model)](#memory-types-coala-model)
- [Episodic Memory Structure](#episodic-memory-structure)
- [Quality Weighting System](#quality-weighting-system)
- [Memory Operations](#memory-operations)
- [Memory Consolidation](#memory-consolidation)
- [Experience Replay](#experience-replay)
- [Usage Example](#usage-example)
- [Best Practices](#best-practices)

## Purpose

The Memory Curator manages episodic memory with quality weighting to enable agents to learn from past experiences while preventing memory pollution from unsuccessful episodes.

## Memory Types (CoALA Model)

Following the CoALA (Cognitive Architectures for Language Agents) framework:

```
┌─────────────────────────────────────────────────────────────┐
│                     Memory Systems                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Working    │   Episodic   │   Semantic   │   Procedural   │
│   Memory     │   Memory     │   Memory     │   Memory       │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ - Current    │ - Past       │ - Facts      │ - Skills       │
│   context    │   experiences│ - Concepts   │ - Procedures   │
│ - Active     │ - Specific   │ - Relations  │ - Tool usage   │
│   task       │   episodes   │              │                │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ Limited      │ Large,       │ Large,       │ Learned        │
│ capacity     │ selectable   │ queryable    │ patterns       │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

This module focuses primarily on **Episodic Memory** management.

## Episodic Memory Structure

```python
class EpisodicMemory:
    def __init__(self):
        self.episodes = []

class Episode:
    def __init__(self):
        self.id = generate_id()
        self.timestamp = datetime.now()
        self.task = None
        self.reasoning_trace = []
        self.outcome = None
        self.quality_score = 0.0
        self.retrieval_count = 0
        self.last_accessed = None
        self.tags = []
        self.embedding = None
```

## Quality Weighting System

### Scoring Dimensions

```python
class QualityScorer:
    def score_episode(self, episode):
        scores = {
            'outcome_success': self.outcome_score(episode),
            'reasoning_quality': self.reasoning_score(episode),
            'efficiency': self.efficiency_score(episode),
            'reusability': self.reusability_score(episode)
        }

        # Weighted combination
        weights = {
            'outcome_success': 0.4,
            'reasoning_quality': 0.3,
            'efficiency': 0.2,
            'reusability': 0.1
        }

        episode.quality_score = sum(
            scores[k] * weights[k] for k in scores
        )

        return episode.quality_score
```

### Quality Tiers

```python
QUALITY_TIERS = {
    'exemplar': (0.9, 1.0),      # Always retain, priority retrieval
    'good': (0.7, 0.9),          # Standard retention
    'acceptable': (0.5, 0.7),    # Conditional retention
    'poor': (0.0, 0.5)           # Flag for review or discard
}
```

## Memory Operations

### Storage

```python
def store_episode(self, task, reasoning_trace, outcome):
    episode = Episode()
    episode.task = task
    episode.reasoning_trace = reasoning_trace
    episode.outcome = outcome
    episode.embedding = self.compute_embedding(task + " " + str(reasoning_trace))
    episode.quality_score = self.quality_scorer.score_episode(episode)
    episode.tags = self.auto_tag(task, reasoning_trace)

    if self.should_retain(episode):
        self.episodes.append(episode)
        self.maintain_capacity()

    return episode
```

### Retrieval

```python
def retrieve_similar(self, query, k=5, quality_threshold=0.6):
    query_embedding = self.compute_embedding(query)
    scored_episodes = []

    for episode in self.episodes:
        if episode.quality_score < quality_threshold:
            continue
        similarity = cosine_similarity(query_embedding, episode.embedding)
        adjusted_score = similarity * (0.5 + 0.5 * episode.quality_score)
        scored_episodes.append((episode, adjusted_score))

    scored_episodes.sort(key=lambda x: x[1], reverse=True)
    return [ep for ep, _ in scored_episodes[:k]]
```

## Usage Example

```python
curator = MemoryCurator(max_episodes=1000, quality_threshold=0.5)

# Store experience
episode = curator.store_episode(
    task="Solve differential equation",
    reasoning_trace=[...],
    outcome={'success': True, 'quality': 0.9}
)

# Retrieve similar
similar = curator.retrieve_similar("Solve differential equation", k=3)
```

---

**Sources:**
- [Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427)
