# Pipeline Integration Guide

This reference provides detailed guidance for integrating screenwriter output with downstream AI tools (imagine, arch-v) in video generation pipelines.

## Table of Contents
1. [Scene Metadata Standards](#scene-metadata-standards)
2. [Imagine-Ready Visual Descriptions](#imagine-ready-visual-descriptions)
3. [Character Consistency Tracking](#character-consistency-tracking)
4. [Scene Numbering Conventions](#scene-numbering-conventions)
5. [Duration Estimation Guidelines](#duration-estimation-guidelines)
6. [Output Format Validation](#output-format-validation)
7. [Pipeline Handoff Checklist](#pipeline-handoff-checklist)

---

## Scene Metadata Standards

### Metadata Completeness

Every scene MUST include all required metadata fields for reliable pipeline processing:

**Required Fields:**
- `number`: Integer, sequential scene numbering
- `slugline`: Full scene heading (INT/EXT. LOCATION - TIME)
- `location`: Extracted location name for tracking
- `time`: Time of day (affects lighting in image generation)
- `characters`: All characters present in scene
- `mood`: Emotional tone/atmosphere descriptor
- `key_visuals`: 3-5 specific visual elements
- `action`: Full action/description text

**Optional Fields:**
- `dialogue`: Include only if dialogue exists
- `duration`: Scene duration estimate (helpful for pacing)

### Metadata Quality Guidelines

**Location Specificity:**
```xml
<!-- ❌ Too vague -->
<location>Building</location>

<!-- ✅ Specific and descriptive -->
<location>Abandoned Subway Station</location>
```

**Mood Descriptors:**
Use 1-3 adjectives that guide visual tone:
- Good: "tense, claustrophobic"
- Good: "serene, hopeful"
- Avoid: "the character feels anxious" (this describes internal state, not mood)

**Character Lists:**
```xml
<!-- Single character -->
<characters>Unit-7</characters>

<!-- Multiple characters -->
<characters>Sarah, Marcus, Tech-Bot</characters>
```

---

## Imagine-Ready Visual Descriptions

### Visual Element Extraction

The `key_visuals` array should contain discrete, image-generation-friendly descriptions:

**Example Scene Action:**
```
A BOXY ROBOT (Unit-7, weathered chrome with a single blue optical sensor) rolls through fog-shrouded streets. Neon signs flicker overhead, casting pink and cyan reflections on wet pavement.
```

**Extracted key_visuals:**
```xml
<key_visuals>
  <visual>boxy robot with weathered chrome body and single blue optical sensor</visual>
  <visual>fog-shrouded cyberpunk street with flickering neon signs</visual>
  <visual>pink and cyan neon reflections on wet pavement</visual>
</key_visuals>
```

### Visual Description Best Practices

**Composition Elements:**
- Subject: Main focus (character, object)
- Setting: Environment and background
- Lighting: Light quality, direction, color
- Atmosphere: Weather, air quality, mood
- Details: Significant props or textures

**Example - Layered Visual:**
```
Subject: "weathered robot with blue optical sensor"
Setting: "abandoned industrial warehouse, broken windows"
Lighting: "harsh afternoon sunlight streaming through gaps"
Atmosphere: "dust particles floating in light beams"
Details: "rusted machinery, scattered tools"
```

### Color and Lighting Vocabulary

**Color Descriptors:**
- Warm: amber, golden, crimson, burnt orange
- Cool: azure, ice blue, slate gray, mint
- Neon: electric pink, cyan, magenta, lime
- Natural: earth tones, moss green, sand, clay

**Lighting Descriptors:**
- Quality: soft, harsh, diffused, dappled, dramatic
- Direction: overhead, backlighting, side-lit, rim light
- Color: warm glow, cool blue, golden hour, neon-lit
- Intensity: dim, bright, shadowy, high-contrast

---

## Character Consistency Tracking

### First Appearance Template

Establish complete visual identity on first appearance:

```
CHARACTER NAME (age if relevant, defining physical trait, primary wardrobe)
```

**Examples:**
```
MAYA (early 30s, kind eyes, wearing a faded denim jacket and cargo pants)
COMMANDER REED (50s, grizzled with close-cropped gray hair, military uniform with rank insignia)
THE STRANGER (tall figure in a long black coat, face obscured by wide-brimmed hat)
```

### Subsequent References

After first appearance, use consistent identifiers:

**Preferred Pattern:**
- Use character name only: "Maya checks her phone"
- Add action-relevant details: "Maya pulls her jacket tighter against the wind"

**Avoid:**
- Re-describing appearance: "Maya, the woman in the denim jacket..."
- Changing character names: "Maya" → "the woman" → "she"

### Character Tracking Checklist

For each character, track:
- [ ] Full name and any aliases
- [ ] Age or age range
- [ ] Key physical identifiers (height, build, distinctive features)
- [ ] Primary wardrobe (consistent across scenes unless story requires change)
- [ ] Unique mannerisms or movement style

---

## Scene Numbering Conventions

### Sequential Numbering

Number scenes sequentially from 1 to N:
```xml
<scene number="1" ...>
<scene number="2" ...>
<scene number="3" ...>
```

**No Scene 0:** Start at 1, not 0 (industry standard)

### Scene Splits and Inserts

If a scene needs to be split or inserted during revision:
- Option A: Renumber all subsequent scenes
- Option B: Use fractional numbering (1, 2, 2A, 3...)

For pipeline simplicity, prefer Option A (complete renumbering).

---

## Duration Estimation Guidelines

### Per-Scene Duration

Estimate based on scene complexity:

**30-45 seconds:** Simple scenes
- Single action
- Minimal dialogue
- One primary visual

**45-60 seconds:** Standard scenes
- Multiple actions or dialogue exchanges
- 2-3 visual beats
- Character interaction

**60-90 seconds:** Complex scenes
- Extended dialogue
- Multiple visual beats
- Scene climax or key moment

### Total Film Duration

Track cumulative duration across all scenes:

```
Scene 1: 30s
Scene 2: 45s
Scene 3: 40s
...
Total: 8 minutes 20 seconds
```

Adjust scene count or duration to hit target length (5-10 min).

---

## Output Format Validation

### XML Well-Formedness

Ensure valid XML structure:
- All opening tags have closing tags
- Proper nesting (no overlapping tags)
- Special characters escaped (&lt; &gt; &amp;)

### Common XML Errors

**❌ Missing closing tag:**
```xml
<scene number="1">
  <action>Text here
</scene>
```

**✅ Properly closed:**
```xml
<scene number="1">
  <action>Text here</action>
</scene>
```

**❌ Unescaped special characters:**
```xml
<action>She thinks: "I'm < 10 years old"</action>
```

**✅ Properly escaped:**
```xml
<action>She thinks: "I'm &lt; 10 years old"</action>
```

---

## Pipeline Handoff Checklist

Before passing screenplay to next pipeline stage:

- [ ] All scenes have complete metadata
- [ ] key_visuals array populated (3-5 per scene)
- [ ] Character names consistent throughout
- [ ] XML well-formed and parseable
- [ ] Total duration within target range (5-10 min)
- [ ] Scene numbers sequential with no gaps
- [ ] Visual descriptions rich and specific
- [ ] No technical camera directions (use visual descriptions instead)
