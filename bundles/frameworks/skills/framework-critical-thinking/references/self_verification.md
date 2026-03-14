# Self-Verification

## Table of Contents

- [Purpose](#purpose)
- [Core Techniques](#core-techniques)
  - [Chain-of-Verification (CoVe)](#1-chain-of-verification-cove)
  - [Backward Verification](#2-backward-verification)
  - [Self-Consistency Check](#3-self-consistency-check)
  - [Cross-Verification](#4-cross-verification-with-external-sources)
- [Verification Strategies by Task Type](#verification-strategies-by-task-type)
- [Self-Refine Loop](#self-refine-loop)
- [Implementation Example](#implementation-example)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)

## Purpose

Self-Verification provides mechanisms for AI agents to validate their own outputs before delivery. It implements techniques like Chain-of-Verification (CoVe), backward verification, and cross-verification to catch errors and hallucinations.

## Core Techniques

### 1. Chain-of-Verification (CoVe)

A multi-stage verification process where the model generates verification questions and answers them to validate its initial output.

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Baseline Response                                 │
│  Generate initial answer to the query                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Plan Verification                                 │
│  Generate verification questions based on baseline          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Execute Verification                              │
│  Answer verification questions independently                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 4: Generate Final Verified Response                  │
│  Incorporate verification results into final output         │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
class ChainOfVerification:
    def verify(self, query, baseline_response):
        # Stage 2: Generate verification questions
        verification_questions = self.generate_verification_questions(
            query, baseline_response
        )

        # Stage 3: Execute verification
        verified_facts = []
        for question in verification_questions:
            # Answer independently, without reference to baseline
            answer = self.answer_independently(question)
            verified_facts.append({
                'question': question,
                'answer': answer,
                'matches_baseline': self.check_consistency(
                    answer, baseline_response
                )
            })

        # Stage 4: Generate final response
        if all(f['matches_baseline'] for f in verified_facts):
            return baseline_response
        else:
            return self.revise_response(baseline_response, verified_facts)

    def generate_verification_questions(self, query, response):
        """Extract claims and generate questions to verify them."""
        claims = self.extract_claims(response)
        questions = []
        for claim in claims:
            questions.extend(self.claim_to_questions(claim))
        return questions
```

**Template for Verification Planning:**
```
Given the following claim from a response:
"{claim}"

Generate 2-3 specific questions that would verify the accuracy of this claim.
Questions should be answerable independently without referencing the original claim.

Verification questions:
1.
2.
3.
```

### 2. Backward Verification

For mathematical or logical problems, verify by working backward from the conclusion to see if it leads to the original problem conditions.

```python
class BackwardVerification:
    def verify(self, problem, solution_steps, final_answer):
        """Verify by reversing the solution."""
        # Start from final answer
        current = final_answer

        # Apply inverse operations in reverse order
        for step in reversed(solution_steps):
            inverse_op = self.get_inverse_operation(step.operation)
            current = inverse_op.apply(current, step.operand)

        # Check if we return to original problem conditions
        return self.matches_original(current, problem)

    def get_inverse_operation(self, operation):
        inverses = {
            'add': 'subtract',
            'multiply': 'divide',
            'square': 'square_root',
            'append': 'remove_last'
        }
        return inverses.get(operation)
```

**Example:**
```
Problem: "If x + 5 = 12, what is x?"
Forward: x = 12 - 5 = 7
Backward: 7 + 5 = 12 ✓ (matches original equation)
```

### 3. Self-Consistency Check

Generate multiple reasoning paths and check if they converge to the same answer.

```python
class SelfConsistency:
    def __init__(self, sample_count=10, temperature=0.7):
        self.sample_count = sample_count
        self.temperature = temperature

    def verify(self, problem):
        # Generate multiple reasoning paths
        answers = []
        for i in range(self.sample_count):
            reasoning, answer = self.generate_with_temperature(
                problem, self.temperature
            )
            answers.append({
                'reasoning': reasoning,
                'answer': answer,
                'confidence': self.assess_reasoning_quality(reasoning)
            })

        # Aggregate answers
        answer_counts = Counter(a['answer'] for a in answers)
        most_common = answer_counts.most_common(1)[0]

        # Calculate consistency score
        consistency_score = most_common[1] / len(answers)

        return {
            'final_answer': most_common[0],
            'consistency_score': consistency_score,
            'all_answers': answers,
            'confidence': self.compute_aggregate_confidence(answers)
        }
```

### 4. Cross-Verification with External Sources

When external knowledge bases or tools are available, verify claims against them.

```python
class CrossVerification:
    def __init__(self, knowledge_base, tools):
        self.kb = knowledge_base
        self.tools = tools

    def verify_claim(self, claim):
        verification_result = {
            'claim': claim,
            'verified': False,
            'sources': [],
            'confidence': 0.0
        }

        # Query knowledge base
        kb_results = self.kb.query(claim)
        if kb_results:
            verification_result['sources'].extend(kb_results)
            verification_result['kb_match'] = self.check_match(
                claim, kb_results
            )

        # Use tools if applicable
        if self.is_computable(claim):
            tool_result = self.compute_with_tools(claim)
            verification_result['tool_result'] = tool_result
            verification_result['tool_match'] = self.check_match(
                claim, tool_result
            )

        # Aggregate verification
        verification_result['verified'] = self.aggregate_verification(
            verification_result
        )

        return verification_result
```

## Verification Strategies by Task Type

### Factual Claims

Use CoVe with web search or knowledge base verification:

```python
factual_verification = {
    'technique': 'CoVe',
    'question_generation': 'claim_extraction',
    'verification_source': ['knowledge_base', 'web_search'],
    'revision_strategy': 'correct_or_hedge'
}
```

### Mathematical Reasoning

Use backward verification + computation tools:

```python
math_verification = {
    'technique': 'backward_verification',
    'tools': ['calculator', 'sympy', 'wolfram_alpha'],
    'check_steps': True,
    'precision_tolerance': 1e-10
}
```

### Logical Arguments

Use consistency checking and counter-example search:

```python
logic_verification = {
    'technique': 'consistency_checking',
    'methods': ['truth_table', 'counter_example_search'],
    'validate_premises': True,
    'check_entailment': True
}
```

### Code Generation

Use execution and test validation:

```python
code_verification = {
    'technique': 'execution_based',
    'steps': [
        'syntax_check',
        'static_analysis',
        'test_execution',
        'edge_case_testing'
    ],
    'timeout': 30
}
```

## Self-Refine Loop

Iterative improvement through self-critique:

```python
class SelfRefine:
    def __init__(self, max_iterations=3):
        self.max_iterations = max_iterations

    def refine(self, initial_output, task_description):
        current = initial_output

        for iteration in range(self.max_iterations):
            # Generate critique
            critique = self.generate_critique(current, task_description)

            # Check if satisfactory
            if critique['is_satisfactory']:
                break

            # Refine based on critique
            current = self.apply_refinement(current, critique)

        return {
            'final_output': current,
            'iterations': iteration + 1,
            'critiques': critique_history
        }

    def generate_critique(self, output, task):
        critique_prompt = f"""
Task: {task}
Output: {output}

Critique this output. Identify:
1. Factual errors or hallucinations
2. Logical inconsistencies
3. Missing information
4. Unclear explanations
5. Areas for improvement

Is this output satisfactory? (Yes/No with explanation)
"""
        return self.llm.generate(critique_prompt)
```

## Implementation Example

```python
class SelfVerificationSystem:
    def __init__(self):
        self.cove = ChainOfVerification()
        self.backward = BackwardVerification()
        self.consistency = SelfConsistency()
        self.refine = SelfRefine()

    def verify_output(self, task_type, problem, output):
        verification_pipeline = self.get_pipeline(task_type)

        results = {}
        for technique in verification_pipeline:
            if technique == 'CoVe':
                results['cove'] = self.cove.verify(problem, output)
            elif technique == 'backward':
                results['backward'] = self.backward.verify(
                    problem, output['steps'], output['answer']
                )
            elif technique == 'consistency':
                results['consistency'] = self.consistency.verify(problem)

        # Aggregate verification results
        final_confidence = self.aggregate_confidence(results)

        # Refine if needed
        if final_confidence < 0.8:
            refined = self.refine.refine(output, problem)
            return {
                'verified_output': refined['final_output'],
                'confidence': final_confidence,
                'verification_details': results,
                'was_refined': True
            }

        return {
            'verified_output': output,
            'confidence': final_confidence,
            'verification_details': results,
            'was_refined': False
        }
```

## Best Practices

1. **Independent Verification:** Answer verification questions without reference to the baseline response
2. **Multiple Techniques:** Combine different verification methods for robust validation
3. **Graceful Degradation:** If verification fails, hedge claims or request human review
4. **Budget Management:** Limit verification iterations to control computational cost
5. **Calibration:** Track verification success rates and adjust confidence thresholds

## Common Pitfalls

- **Verification Hallucination:** Model hallucinates during verification phase
- **Confirmation Bias:** Verification favors the baseline response
- **Over-Verification:** Spending too much compute on simple, reliable outputs
- **False Confidence:** High verification scores for incorrect but internally consistent outputs

---

**Sources:**
- [Chain-of-Verification Reduces Hallucination in LLMs](https://arxiv.org/abs/2309.11495)
- [Self-Verification Prompting](https://learnprompting.org/docs/advanced/self_criticism/self_verification)
