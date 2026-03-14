# VS + Tool Integration

**Purpose:** Combining Verbalized Sampling with file tools and batch operations

**Load when:** User requests file operations, batch processing, or automation workflows

**Prerequisite:** Familiarity with core VS technique (`vs-core-technique.md`)

---

## VS + File Writing Workflow

### Scenario
User wants to generate diverse content and save to file

### Example User Request
"Generate 20 product descriptions and save them to a file"

### Agent Workflow

#### Step 1: Execute VS
```
Parameters: k=5, make 4 calls
Total candidates: 20 product descriptions
```

#### Step 2: Parse All Results
```python
# Pseudo-code
all_candidates = []
for i in range(4):
    response = execute_vs_call(k=5)
    candidates = parse_json(response)
    all_candidates.extend(candidates)
```

#### Step 3: Format for File
```markdown
# Generated Product Descriptions

Generated: 2025-11-14
Technique: Verbalized Sampling (k=5, 4 calls)
Total: 20 descriptions

---

## Description 1 (p=0.08)
[Product description text...]

## Description 2 (p=0.07)
[Product description text...]

...
```

#### Step 4: Write to File
```python
# Use Write tool
write_file("product_descriptions.md", formatted_content)
```

#### Step 5: Confirm to User
```
✅ Generated 20 diverse product descriptions
📄 Saved to: product_descriptions.md
📊 Diversity metrics: 20 unique variations across tone, focus, audience
```

---

## VS + Batch Processing

### Scenario
Generate diverse content for multiple different prompts

### Example User Request
"Generate 5 tagline ideas for each of these 10 products (file: products.txt)"

### Agent Workflow

#### Step 1: Read Input File
```python
# Use Read tool
products = read_file("products.txt").split("\n")
# Example: ["Coffee Maker", "Wireless Headphones", "Yoga Mat", ...]
```

#### Step 2: Batch VS Execution
```python
all_results = {}

for product in products:
    # Execute VS for each product
    vs_prompt = format_vs_prompt(
        k=5,
        user_request=f"Generate a tagline for: {product}"
    )
    response = execute_vs(vs_prompt)
    all_results[product] = parse_json(response)["responses"]
```

#### Step 3: Format Results
```markdown
# Tagline Ideas - Batch Generation

Products: 10
Taglines per product: 5
Total generated: 50 taglines
Technique: Verbalized Sampling

---

## Coffee Maker

1. [p=0.09] "Brew happiness, one cup at a time"
2. [p=0.07] "Your morning just got an upgrade"
3. [p=0.06] "Café quality. Kitchen convenience."
...

## Wireless Headphones

1. [p=0.08] "Sound that moves you"
2. [p=0.07] "Unleash your audio"
...
```

#### Step 4: Write & Confirm
```python
write_file("batch_taglines.md", formatted_results)
```

---

## VS + Iterative File Refinement

### Scenario
User wants to review, select, and refine outputs iteratively

### Example User Request
"Generate blog post ideas, I'll pick my favorites, then expand them"

### Agent Workflow

#### Round 1: Initial VS Generation
```
Execute: VS with k=10
Write: ideas_initial.md
Agent: "I've generated 10 diverse ideas. Review ideas_initial.md and tell me which 2-3 you want to expand."
```

#### Round 2: User Selection
```
User: "I like ideas #3, #7, and #9"
Agent: [Reads selected ideas from file]
```

#### Round 3: Expansion
```
For each selected idea:
  Execute: VS with k=3 (3 variations of the idea)

Write: ideas_expanded.md (9 total: 3 ideas × 3 variations)
Agent: "Expanded your selections. See ideas_expanded.md for 3 variations of each."
```

#### Round 4: Final Refinement
```
User: "Perfect! Use #3 variation 2"
Agent: [Polish selected idea, write final version]
Write: blog_post_final.md
```

---

## VS + Multi-File Workflows

### Scenario
Organize VS outputs into structured file hierarchy

### Example User Request
"Generate 50 social media captions and organize them by platform"

### Agent Workflow

#### Step 1: Execute VS (Batch)
```
Execute: VS with k=5, make 10 calls
Total: 50 captions
```

#### Step 2: Categorize by Platform
```python
# Parse and categorize
instagram_captions = []  # Short, emoji-heavy
twitter_captions = []    # Concise, hashtag-ready
linkedin_captions = []   # Professional tone

for caption in all_captions:
    platform = detect_platform_fit(caption)
    categorize(caption, platform)
```

#### Step 3: Write Multiple Files
```python
write_file("social_media/instagram_captions.md", format_captions(instagram))
write_file("social_media/twitter_captions.md", format_captions(twitter))
write_file("social_media/linkedin_captions.md", format_captions(linkedin))
write_file("social_media/README.md", summary_doc)
```

#### Step 4: Directory Structure
```
social_media/
├── README.md (overview, usage instructions)
├── instagram_captions.md (20 captions)
├── twitter_captions.md (15 captions)
└── linkedin_captions.md (15 captions)
```

---

## VS + CSV/JSON Export

### For Data Processing Pipelines

#### JSON Export Format
```json
{
  "metadata": {
    "technique": "Verbalized Sampling",
    "generated_at": "2025-11-14T10:30:00Z",
    "parameters": {"k": 5, "threshold": 0.10},
    "total_candidates": 20
  },
  "candidates": [
    {
      "id": 1,
      "text": "Product description text...",
      "probability": 0.08,
      "metadata": {
        "tone": "professional",
        "length": 95
      }
    },
    ...
  ]
}
```

#### CSV Export Format
```csv
id,text,probability,tone,length
1,"Product description text...",0.08,professional,95
2,"Another description...",0.07,casual,87
...
```

**Use case:** Feeding VS outputs into downstream analysis, A/B testing systems, CMS imports

---

## VS + Edit Tool Integration

### Scenario
Update existing file with new VS-generated content

### Example Workflow

#### Step 1: Read Existing File
```python
content = read_file("marketing_copy.md")
```

#### Step 2: Execute VS for New Section
```
user_request = "Generate 5 new value propositions for Section 3"
Execute: VS with k=5
```

#### Step 3: Edit File (Replace Section)
```python
# Use Edit tool
edit_file(
    "marketing_copy.md",
    old_string="## Section 3: Value Propositions\n[old content]",
    new_string="## Section 3: Value Propositions\n[new VS-generated content]"
)
```

---

## Automation Patterns

### Pattern 1: Schedule-Triggered Generation

**Setup for recurring content needs:**

```bash
# Cron job or scheduled task
# Monday 9am: Generate weekly social media captions

1. Execute VS (k=5, 7 calls for 35 captions)
2. Write to: content/weekly_captions_2025-11-14.md
3. Notify user: "35 captions ready for week of Nov 14"
```

### Pattern 2: Template-Based Generation

**Use VS to fill content templates:**

```markdown
# Email Template
Subject: {VS: generate 5 subject lines}
Opening: {VS: generate 5 opening paragraphs}
CTA: {VS: generate 5 call-to-action variations}

# Execute VS 3 times (subject, opening, CTA)
# Mix and match for A/B testing (5×5×5 = 125 combinations)
```

### Pattern 3: Continuous Content Pipeline

```
Input Queue → VS Generation → Quality Filter → Output Storage
     ↓              ↓                ↓              ↓
  prompts.txt   VS execution    top 50%     approved_content/
```

---

## File Organization Best Practices

### Recommended Structure

```
project/
├── generated/
│   ├── raw/                    # Unfiltered VS outputs
│   │   ├── 2025-11-14_ideas.md
│   │   └── 2025-11-15_captions.md
│   ├── curated/               # User-selected favorites
│   │   └── selected_ideas.md
│   └── final/                 # Polished, production-ready
│       └── blog_post.md
├── parameters/                # VS config for reproducibility
│   └── vs_config.json
└── README.md                  # Documentation
```

### File Naming Convention

```
{date}_{content_type}_{status}.md

Examples:
- 2025-11-14_taglines_raw.md
- 2025-11-14_taglines_curated.md
- 2025-11-14_taglines_final.md
```

---

## Performance Optimization

### For Large-Scale Operations

**Batch processing 1000+ items:**

1. **Chunk processing:** Process in batches of 100 (20 VS calls per batch, k=5)
2. **Parallel execution:** If API allows, run VS calls in parallel
3. **Progress tracking:** Log completion status every 100 items
4. **Error handling:** Retry failed VS calls with exponential backoff
5. **Streaming writes:** Write to file incrementally, don't hold all in memory

### Cost Estimation

**Calculate before executing:**

```python
items = 1000
k = 5
calls_needed = items / k  # 200 calls

tokens_per_call = 500  # Avg VS prompt + response
total_tokens = calls_needed * tokens_per_call  # 100,000 tokens

cost_per_million = 3.00  # Input tokens
estimated_cost = (total_tokens / 1_000_000) * cost_per_million  # $0.30
```

---

## Tool Integration Checklist

**Before executing VS + tool workflow:**

- [ ] Input files exist and are readable
- [ ] Output directory exists or can be created
- [ ] File naming conflicts resolved (won't overwrite existing)
- [ ] Sufficient disk space for outputs
- [ ] User confirmed workflow (especially for batch operations)
- [ ] Error handling in place (what if VS call fails mid-batch?)

---

## Common Integration Patterns

| User Request | Tools Needed | Workflow |
|-------------|--------------|----------|
| "Generate & save to file" | VS + Write | Execute → Format → Write |
| "Read file, generate variations" | Read + VS + Write | Read → VS for each → Write |
| "Update section in file" | Read + VS + Edit | Read → VS → Edit section |
| "Batch process CSV" | Read + VS + Write | Read CSV → VS per row → Write CSV |
| "Organize by category" | VS + Multiple Writes | VS → Categorize → Write per category |

---

**For advanced VS techniques:** See `advanced-techniques.md`
**For troubleshooting file operations:** See `troubleshooting.md`
