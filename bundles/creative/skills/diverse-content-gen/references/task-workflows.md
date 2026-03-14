# Task-Specific VS Workflows

**Purpose:** Pre-configured VS workflows for common creative content types

**Load when:** Agent knows VS basics and needs task-specific implementation guidance

**Prerequisite:** Familiarity with core VS technique (`vs-core-technique.md`)

---

## Blog Post Ideas Workflow

### Typical User Request
"Give me 10 blog post ideas about sustainable fashion"

### Agent Workflow

**1. Parameters:**
- k = 5
- Threshold = 0.10
- Target length = "50-100 words" (idea + brief description)

**2. Execution:**
- Make 2 VS calls (10 ideas / 5 per call)

**3. Diversity Dimensions:**
Ensure variety across:
- **Angles:** Consumer perspective / Industry analysis / Environmental impact
- **Formats:** How-to guides / Listicles / Case studies / Opinion pieces
- **Audiences:** Beginners / Fashion professionals / Environmental activists

**4. Presentation:**
```
Here are 10 diverse blog post ideas about sustainable fashion:

1. [Consumer angle, How-to] "5 Simple Swaps to Build a Sustainable Wardrobe on a Budget"
2. [Industry angle, Analysis] "The Hidden Environmental Cost of Fast Fashion Supply Chains"
3. [Environmental angle, Case study] "How Patagonia's Worn Wear Program Reduces Textile Waste"
...
```

---

## Social Media Captions Workflow

### Typical User Request
"Write 5 Instagram captions for our new product launch"

### Agent Workflow

**1. Parameters:**
- k = 5
- Threshold = None (want quality + diversity balance)
- Target length = "20-30 words"

**2. Execution:**
- Single VS call (5 captions)

**3. Diversity Dimensions:**
Ensure variety across:
- **Tones:** Playful / Professional / Inspirational / Humorous
- **CTAs:** Shop now / Learn more / Share / Tag a friend
- **Formats:** Question / Statement / Story / Challenge

**4. Presentation:**
```
Here are 5 diverse Instagram captions:

😊 PLAYFUL: "New day, new you! Our latest drop just landed and it's giving ✨main character energy✨ Shop now!"

💼 PROFESSIONAL: "Innovation meets design. Introducing our newest product, engineered for your success."

💡 INSPIRATIONAL: "What if you could change your routine for the better? Today's the day. Link in bio."

😄 HUMOROUS: "Warning: This product may cause extreme happiness and compliments from strangers. You've been warned!"

🤔 QUESTION: "Ready to level up? Tag someone who needs to see this! 👇"
```

**Pro tip:** Add emoji indicators to help user quickly scan tone variations.

---

## Campaign/Strategy Ideas Workflow

### Typical User Request
"Brainstorm marketing campaign ideas for Q2"

### Agent Workflow

**1. Parameters:**
- k = 10
- Threshold = 0.05 (exploration mode)
- Target length = "100-150 words" (campaign brief)

**2. Execution:**
- Make 1-2 VS calls (10-20 ideas)

**3. Diversity Dimensions:**
Ensure variety across:
- **Channels:** Social media / Email / Events / Partnerships / Content series
- **Themes:** Seasonal / Product-focused / Value-driven / Community-building
- **Tactics:** Contest / Influencer campaign / User-generated content / Educational series

**4. Presentation:**
Group by feasibility:

```
QUICK WINS (2-4 weeks):
• Social Media Challenge: "30 Days of [Product]" user-generated content campaign
• Email Series: "Spring Refresh" featuring customer success stories

MID-TERM (1-2 months):
• Influencer Partnership: Collaborate with 5 micro-influencers for authentic reviews
• Community Event: Local pop-up shop with exclusive Q2 products

AMBITIOUS (3+ months):
• Content Hub: Launch educational blog series establishing thought leadership
• Brand Partnership: Co-marketing campaign with complementary brand
```

---

## Story/Narrative Generation Workflow

### Typical User Request
"Write 3 different opening paragraphs for a mystery novel"

### Agent Workflow

**1. Parameters:**
- k = 3
- VS-CoT variant (with reasoning step)
- Target length = "100-150 words"

**2. Execution:**
- Single VS call with chain-of-thought reasoning

**3. Enhanced Prompt:**
```
Before generating responses, first think through:
1. What are the different possible angles for mystery novel openings?
2. What POV options work? (1st person, 3rd limited, 3rd omniscient)
3. What settings create intrigue? (time period, location, atmosphere)
4. What tones? (dark/noir, cozy, psychological, quirky)

Then generate 3 opening paragraphs with probabilities.
```

**4. Diversity Dimensions:**
- **POV:** 1st person / 3rd person limited / 3rd person omniscient
- **Setting:** Time period (contemporary, historical) / Location (urban, rural, exotic)
- **Tone:** Dark noir / Cozy mystery / Psychological thriller / Quirky detective

**5. Presentation:**
```
Here are 3 distinct opening paragraphs for your mystery novel:

**Option 1: Dark Noir (1st Person, Contemporary Urban)**
[p=0.08] "The rain hammered the city like it had a grudge. I watched from my office window as the neon signs bled their colors into the wet pavement below..."

**Option 2: Cozy Mystery (3rd Limited, Small Town)**
[p=0.06] "Margaret had lived in Willow Creek for forty-three years, and never once had she seen Mrs. Henderson's garden gate left open. Until this morning..."

**Option 3: Psychological Thriller (3rd Omniscient, Suburban)**
[p=0.04] "The house at the end of Maple Street looked like all the others—same beige siding, same manicured lawn. No one suspected what had happened in the basement three days ago..."

What makes each unique:
- Option 1: Hard-boiled detective feel, urban atmosphere
- Option 2: Small-town charm, observational protagonist
- Option 3: Suburban gothic, ominous foreshadowing
```

---

## Product Descriptions Workflow

### Typical User Request
"Generate 5 different product descriptions for our wireless headphones"

### Agent Workflow

**1. Parameters:**
- k = 5
- Threshold = 0.10
- Target length = "75-100 words"

**2. Execution:**
- Single VS call

**3. Diversity Dimensions:**
- **Focus:** Sound quality / Comfort / Battery life / Design / Value
- **Tone:** Technical specs / Lifestyle benefits / Emotional appeal / Professional use
- **Audience:** Audiophiles / Commuters / Fitness enthusiasts / Remote workers

**4. Presentation:**
```
5 diverse product description angles:

1. AUDIOPHILE FOCUS (Technical):
"Experience studio-grade sound with 40mm neodymium drivers delivering crystal-clear highs and deep, resonant bass..."

2. LIFESTYLE FOCUS (Commuter):
"Your daily commute just got an upgrade. Active noise cancellation blocks out train noise while 30-hour battery life lasts all week..."

3. EMOTIONAL APPEAL (Music lover):
"Rediscover your favorite songs. Every note, every beat, every whispered lyric comes alive with immersive 3D audio..."

4. FITNESS FOCUS (Active lifestyle):
"Sweat-proof, secure-fit, and unstoppable. IPX7 waterproof rating and ear hooks that stay put during any workout..."

5. VALUE FOCUS (Budget-conscious):
"Premium features without premium prices. Get flagship-level sound quality, comfort, and battery life for half the cost..."
```

---

## Quick Workflow Selector

**Use this to quickly choose the right workflow:**

| User Request Contains | Use Workflow | Key Settings |
|-----------------------|--------------|--------------|
| "blog post ideas / topics" | Blog Post Ideas | k=5, threshold=0.10 |
| "captions / social media / Instagram" | Social Media Captions | k=5, no threshold |
| "campaign / strategy / brainstorm" | Campaign Ideas | k=10, threshold=0.05 |
| "story / opening / narrative" | Story Generation | k=3, VS-CoT |
| "product description / copy" | Product Descriptions | k=5, threshold=0.10 |

---

## Customization Tips

**All workflows can be adapted by adjusting:**

1. **k value:** Increase for more options, decrease for quality focus
2. **Threshold:** Add/lower for more creative outputs
3. **Diversity dimensions:** Swap out categories based on domain
4. **Presentation format:** Grouped, ranked, or simple list

**For advanced customization:** See `advanced-techniques.md`
