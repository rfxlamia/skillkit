---
title: "Subagent Creation Guide"
purpose: "Step-by-step guide for creating subagents using init_subagent.py"
token_estimate: "1800"
read_priority: "high"
read_when:
  - "User wants to create a subagent"
  - "Decision workflow recommended subagent"
  - "After understanding Skills vs Subagents difference"
  - "Need to create specialized AI worker"
avoid_reading_when:
  - "User only needs skills (not subagents)"
  - "User hasn't decided between Skills vs Subagents yet"
last_updated: "2025-02-06"
---

# Subagent Creation Guide

## Overview

This guide walks you through creating a subagent using `init_subagent.py` - the automation script for subagent initialization.

**What is a Subagent?**
A subagent is a pre-configured AI personality with specialized system prompts, designed for complex multi-step workflows requiring isolated context.

**Key Differences from Skills:**
- **Context:** Subagents have isolated context windows; Skills share main context
- **Invocation:** Subagents use Task tool; Skills use automatic discovery
- **Permissions:** Subagents define explicit tool permissions
- **Use Case:** Subagents for complex workflows; Skills for utilities

---

## Quick Start

### 1. Create Subagent File

Subagents are stored as individual `.md` files in `~/.claude/agents/`:

```
~/.claude/agents/
├── code-simplifier.md
├── typescript-pro.md
└── your-subagent.md
```

**Create new subagent:**
```bash
cd ~/.claude/skills/skillkit
python3 scripts/init_subagent.py <name> --path ~/.claude/agents
```

**Or manually create:**
```bash
touch ~/.claude/agents/kotlin-pro.md
```

### 2. Edit SUBAGENT.md

Open the generated `SUBAGENT.md` and fill in all `[TODO]` sections.

### 3. Test and Deploy

Test the subagent using Task tool, then deploy.

---

## SUBAGENT.md Structure

### YAML Frontmatter (Required)

```yaml
---
name: subagent-name
description: |
  Clear description of what this subagent does and when to use it.
  Include specific trigger conditions.

subagent_type: code-reviewer  # See types below

tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  # - Task  # Only if spawning nested subagents

# Optional: Skills this subagent can invoke
skills:
  - skill-name

# Optional: Model preference
# model: sonnet  # sonnet, opus, or haiku
---
```

### Subagent Types

| Type | Best For | Typical Tools |
|------|----------|---------------|
| `general-purpose` | Research, analysis | Read, Grep, Glob, Bash |
| `code-reviewer` | Code review | Read, Grep, Glob |
| `typescript-pro` | TS development | Read, Write, Edit, Bash |
| `flutter-expert` | Flutter development | Read, Write, Edit, Bash |
| `red-team` | Security testing | Read, Grep, Glob, Bash |
| `qa-expert` | QA and testing | Read, Grep, Glob |
| `seo-manager` | Social media SEO | Read, Write, Edit |
| `creative-copywriter` | Content creation | Read, Write, Edit |
| `decision-maker` | Strategic decisions | Read, Grep, Glob |
| `research` | Deep research | Read, Grep, Glob, Bash |
| `custom` | Specialized needs | Define as needed |

### Tool Permission Levels

**Minimal (Read-only):**
```yaml
tools:
  - Read
  - Grep
  - Glob
```

**Standard (Read + Write):**
```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
```

**Full (Including nested subagents):**
```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
  - Task
```

---

## Content Sections

### 1. Role Definition

Define the subagent's expertise and approach:

```markdown
## Role Definition

**Primary Role:** Security-focused code reviewer

**Specialization:** Web application vulnerabilities, performance issues

**Working Style:** Methodical, thorough, prioritizes security over convenience
```

### 2. Trigger Conditions

Specify when to invoke this subagent:

```markdown
## When to Use This Subagent

### Trigger Conditions

Invoke this subagent when:

1. **Code review requested** - Any PR or code change needs review
2. **Security concerns** - Suspicious patterns detected
3. **Performance optimization** - Hot paths need analysis

### Task Characteristics

**Ideal for:**
- Multi-file code reviews
- Security vulnerability scans
- Performance bottleneck analysis

**Not suitable for:**
- Simple syntax checks
- One-line changes
```

### 3. Workflow

Define the multi-phase workflow:

```markdown
## Workflow

### Phase 1: Initial Scan

1. Read all changed files
2. Identify file types and scope
3. Check for obvious issues

### Phase 2: Deep Analysis

1. Security vulnerability scan
2. Performance pattern analysis
3. Best practices compliance check

### Phase 3: Synthesis and Report

1. Prioritize findings by severity
2. Generate actionable recommendations
3. Format output consistently
```

### 4. Response Format

Define expected output structure:

```markdown
## Response Format

### Structure

```markdown
## Summary
[Brief overview of findings]

## Critical Issues
[High priority items]

## Recommendations
[Actionable improvements]

## References
[Files analyzed]
```

### Tone and Style

- Professional and constructive
- Specific with line references
- Prioritize security and correctness
```

### 5. Error Handling

Document common issues and resolutions:

```markdown
## Error Handling

### Common Issues

| Issue | Detection | Resolution |
|-------|-----------|------------|
| Binary files | File extension check | Skip, note in report |
| Large diffs | Line count >500 | Focus on critical sections |
| Missing context | Import not found | Request additional files |

### Escalation Criteria

Escalate to parent when:
- Architectural decisions needed
- Business logic unclear
- External dependencies involved
```

### 6. Examples

Provide concrete usage examples:

```markdown
## Examples

### Example 1: Security Review

**Input:**
```
Review this authentication module for security issues
```

**Process:**
1. Scan for SQL injection patterns
2. Check for XSS vulnerabilities
3. Verify input validation
4. Review session handling

**Output:**
```markdown
## Summary
Found 2 critical security issues

## Critical Issues
1. SQL injection in login() (line 45)
2. XSS vulnerability in display_name (line 78)

## Recommendations
- Use parameterized queries
- Implement output encoding
```
```
```

---

## Validation Checklist

Before deploying your subagent:

- [ ] YAML frontmatter is valid (test with `python3 -c "import yaml; yaml.safe_load(open('SUBAGENT.md'))"`)
- [ ] Name is descriptive and hyphenated
- [ ] Description is clear and specific
- [ ] Subagent type is appropriate
- [ ] Tool permissions are minimal but sufficient
- [ ] Role definition is clear
- [ ] Trigger conditions are specific
- [ ] Workflow has multiple phases
- [ ] Response format is defined
- [ ] At least one example is complete
- [ ] Error handling is documented

---

## Testing Your Subagent

### Test Invocation

```python
# Test with Task tool
Task(
    description="Test subagent",
    prompt="""Test the [subagent-name] subagent with this request:

[Your test case here]

Verify it:
1. Follows the defined workflow
2. Uses correct tone/style
3. Returns properly formatted output
4. Handles the task appropriately
""",
    subagent_type="[subagent-name]"
)
```

### Iteration

1. Run test
2. Review output
3. Update SUBAGENT.md if needed
4. Re-test
5. Repeat until satisfied

---

## Integration with Skills

Subagents can invoke Skills for utilities:

```markdown
## Using with Skills

This subagent can invoke:
- `coding-standards` - Apply style guidelines
- `security-checklist` - Run security validation
- `documentation-formatter` - Format docs consistently
```

See `knowledge/foundation/04-hybrid-patterns.md` for hybrid patterns.

---

## Deployment

### Personal Use

1. Save subagent definition
2. Document in personal notes
3. Use via Task tool

### Team Sharing

1. Add to team subagents registry
2. Document usage patterns
3. Share examples

### Project-Specific

1. Add to project docs
2. Document in README
3. Configure CI/CD if needed

---

## Best Practices

1. **Start Simple:** Begin with minimal tool set, add as needed
2. **Be Specific:** Clear trigger conditions prevent misuse
3. **Define Output:** Consistent format improves usability
4. **Test Thoroughly:** Multiple test cases catch edge cases
5. **Iterate:** Refine based on real usage
6. **Document:** Good examples save time later

---

## Troubleshooting

### YAML Validation Errors

```bash
# Test YAML validity
python3 -c "import yaml; yaml.safe_load(open('SUBAGENT.md'))"
```

### Subagent Not Found

- Verify `subagent_type` matches directory name
- Check file is named `SUBAGENT.md`
- Ensure YAML frontmatter is at the very top

### Tool Permission Denied

- Add required tool to `tools:` list
- Restart conversation if tool list changed

### Output Not As Expected

- Review response format section
- Check examples are clear
- Refine workflow steps

---

## Related Resources

- **Decision Framework:** `foundation/03-skills-vs-subagents-decision-tree.md`
- **Comparison:** `foundation/02-skills-vs-subagents-comparison.md`
- **Hybrid Patterns:** `foundation/04-hybrid-patterns.md`
- **Full Workflow:** `references/section-6-subagent-creation-workflow.md`

---

**FILE END**
