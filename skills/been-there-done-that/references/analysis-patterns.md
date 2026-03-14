# Cross-Entry Analysis Patterns

Rules for Phase 2. Applied only when been-there-done-that.md has ≥1 prior entry.
Goal: surface factual observations useful for portfolio positioning and self-tracking.
Strict rule: if data does not clearly support a pattern, write nothing.

## Table of Contents
- [Pattern A — First Time Flag](#pattern-a--first-time-flag)
- [Pattern B — Recurring Blocker](#pattern-b--recurring-blocker)
- [Pattern C — Domain Depth](#pattern-c--domain-depth)
- [Pattern D — Portfolio Note](#pattern-d--portfolio-note)
- [Gig Positioning Statement](#gig-positioning-statement-optional-generated-on-request)
- [What Analysis Must NEVER Do](#what-analysis-must-never-do)

---

## Pattern A — First Time Flag

**Condition:** A technology, tool, or integration appears in the new entry's
Stack or answers, and does NOT appear in any prior entry.

**Output format:**
```
📊 First time working with <tech> (not in any prior entry)
```

**Examples:**
```
📊 First time working with SQLx async (not in any prior entry)
📊 First time deploying to production with custom domain (not in any prior entry)
```

**Do NOT flag:**
- Generic terms: "backend", "frontend", "database"
- Languages user has used for years (if visible in multiple prior entries)
- Frameworks used in >1 prior entry

---

## Pattern B — Recurring Blocker

**Condition:** A blocker in the new entry is semantically similar to a blocker
in ≥1 prior entry.

**Similarity criteria (match any):**
- Same root cause category: auth flow, CORS, SSL/TLS, timeout, config management
- Same third-party system: Cloudflare, Supabase, Docker, specific API
- Same class of problem: "encrypted data I can't read", "proxy cuts connection"

**Output format:**
```
📊 Recurring blocker: <category> (also appeared in: <prior project, date>)
```

**Examples:**
```
📊 Recurring blocker: Cloudflare proxy behavior (also in: WooMaps, 2025-11-14)
📊 Recurring blocker: third-party encrypted data formats (also in: FSTrack, 2025-09-03)
```

**Threshold:** Must appear in ≥2 entries total (prior + current). Not ≥2 prior.

---

## Pattern C — Domain Depth

**Condition:** ≥3 entries (including current) involve the same technical domain.

**Domain categories:**
```
real-time systems      → WebSocket, SSE, Supabase Realtime, MQTT, live tracking
IoT / telemetry        → GPS, GNSS, tractor data, sensor parsing, Teltonika
authentication         → JWT, OAuth, multi-tenant, RBAC, session management
agricultural systems   → autosteer, field mapping, precision farming
team tooling           → dashboards, task tracking, mandor systems
AI/agent systems       → LLM integration, agent workflows, prompt engineering
Rust systems           → Rust backend, async Rust, SQLx, Actix
```

**Output format:**
```
📊 Emerging depth: <domain> (entries: <project1>, <project2>, <project3>)
```

**Examples:**
```
📊 Emerging depth: real-time systems (entries: WooMaps, FSTrack, Yagura)
📊 Emerging depth: Rust backend (entries: Centotype, Yagura, FSTrack)
```

---

## Pattern D — Portfolio Note

**Condition (ALL must be true):**
- The entry represents a complete, usable deliverable (not a WIP or internal experiment)
- AND at least one of:
  - Production deployment (live URL, app store, server)
  - Solo delivery (no team, user is sole developer)
  - Novel technical integration (tech combination not commonly documented)

**Output format:**
```
🎯 Portfolio: <one factual sentence describing the deliverable>
```

**Examples:**
```
🎯 Portfolio: Solo delivery — Yagura Phase 1 live at yagura.space (auth + realtime + calendar)
🎯 Portfolio: Production GPS tracking system for agricultural mandors, handling concurrent sessions
🎯 Portfolio: Open-source CLI (skillkit) with GitHub traction and external adoption
```

**Do NOT generate portfolio note for:**
- Bug fixes only
- Config changes / dependency updates
- Internal tools not yet deployed
- Work that is clearly WIP ("started implementing", "began migrating")
- Any entry where the user said "Shipped: nothing yet"

---

## Gig Positioning Statement (Optional, generated on request)

If user asks "generate my portfolio summary" or "what's my positioning":

Scan ALL entries and produce:

```
## Developer Profile (from been-there-done-that)

**Stack fingerprint:** <top 5 technologies by frequency across entries>

**Delivery track record:**
- <N> production deployments documented
- <N> entries represent solo delivery
- <N> open-source projects

**Domain exposure:**
- <domain A>: <N> entries (<project list>)
- <domain B>: <N> entries (<project list>)

**Recurring strengths (by evidence):**
- <pattern observed in ≥3 entries, stated factually>

**Recurring friction:**
- <recurring blocker, if any>
```

This is generated on explicit request only, not automatically on every write.

---

## What Analysis Must NEVER Do

- Predict: "You're becoming an expert in X" → forbidden
- Praise: "Great progress on Y" → forbidden
- Encourage: "Keep it up with Z" → forbidden
- Extrapolate: "Based on this trajectory..." → forbidden
- Quantify growth rate: "30% faster than last sprint" → forbidden (no baseline)

Analysis output is descriptive of the past. Never prescriptive about the future.
