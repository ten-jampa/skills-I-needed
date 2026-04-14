# Pipeline File Specifications

Exact content specs for every file type the skill generates. Read the relevant section when generating that file — do not load the entire document upfront.

## Table of Contents

1. [Pipeline Overview](#1-pipeline-overview)
2. [Stage Files](#2-stage-files)
3. [Portfolio Track](#3-portfolio-track)
4. [Framework Verdicts](#4-framework-verdicts)
5. [Career Targets](#5-career-targets)
6. [Reading List](#6-reading-list)
7. [Hardware Strategy](#7-hardware-strategy-conditional)
8. [Templates](#8-templates)
9. [Frontmatter Reference](#9-frontmatter-reference)
10. [Cross-Reference Patterns](#10-cross-reference-patterns)

---

## 1. Pipeline Overview

**File**: `00-pipeline-overview.md`

Structure:

```markdown
---
tags:
  - {pipeline-tag}
  - pipeline-overview
aliases:
  - 00-overview
  - Pipeline Overview
  - Master Roadmap
created: YYYY-MM-DD
status: not-started
---

# {Domain} Learning Pipeline

## Philosophy

3-4 numbered principles. Domain-specific, not generic platitudes.
Connect to the learner's existing background (physics, philosophy, data science).
Example: "1. Build from the math you already have — linear algebra and calculus transfer directly."

## Backbone Resources

The 2-3 resources that recur across multiple stages. Table format:

| Resource | Type | Stages | Why it's backbone |
|----------|------|--------|-------------------|
| ... | Book/Course/Repo | 1-4 | ... |

## Pipeline Stages

| Stage | Title | Est. Hours | Focus | Compute |
|-------|-------|------------|-------|---------|
| [[01-stage-name]] | ... | Xh | ... | Local/Cloud |
| [[02-stage-name]] | ... | Xh | ... | Local |

## Timeline

Week-by-week grid. Columns: Week, Stage(s), Key Milestone, Hours/Week.
Be realistic about the learner's stated availability.

## Quick Links

- [[portfolio-track]] — what to publish and when
- [[framework-verdicts]] — tools to learn vs. skip
- [[career-targets]] — where this pipeline gets you
- [[reading-list]] — all resources in one place
- [[hardware-strategy]] — compute setup (if generated)
```

Target length: 60-120 lines.

---

## 2. Stage Files

**Files**: `01-stage-name.md` through `NN-stage-name.md`

This is the most important spec. Each stage file follows this exact structure:

```markdown
---
tags:
  - {pipeline-tag}
  - {category-tag}
  - stage
aliases:
  - 01-stage-name
  - "Stage 1"
  - "{Stage Title}"
created: YYYY-MM-DD
status: not-started
---

# Stage N: {Title}

**Estimated hours:** X–Yh ({compute type})
**Prerequisites:** [[previous-stage]] checkpoint complete
**Note:** {One sentence connecting this stage to the learner's background or goals}

## N.1 {First Section Title}

Brief context paragraph — what this section covers and why it matters.
Connect to learner's existing knowledge where possible.

### Tasks

- [ ] {Specific, actionable task with clear deliverable}
- [ ] {Another task}
  - [ ] {Subtask if needed}
- [ ] {Task with specific resource}: [Resource Name](URL)

> [!tip] {Optional title}
> Insight connecting this to physics/philosophy/data science background.

## N.2 {Second Section Title}

...same pattern...

> [!hint]
> Common gotcha or trap. Be specific about what goes wrong and how to recognize it.

## N.D Design Decisions

**Design decision (yours to make):** {Description of a choice point where the learner
should explore and decide. State the options, trade-offs, and what to consider.
Do NOT prescribe the answer.}

## Learning Loop

Apply the five-step loop to this stage's core concept:

- [ ] **Read**: {Specific source, chapter, or section}
- [ ] **Implement**: {Minimal working version — specify what "minimal" means}
- [ ] **Evaluate**: {How to test/measure what you built — specific metric or behavior}
- [ ] **Ablate**: {One variable to change — specify which and what to observe}
- [ ] **Memo**: {Write 200-400 words explaining what happened and why}

## Checkpoint

Every criterion must be testable. Use action verbs. Never "understand" or "know."

- [ ] {Implement X from scratch without reference code}
- [ ] {Explain X to someone and have it make sense — record yourself if needed}
- [ ] {Run benchmark Y and interpret results: expected range is Z}
- [ ] {Debug a broken version of X — identify and fix the issue}

> [!portfolio]
> **Stage N artifact:** {What to build, format, where to publish.}
> See [[portfolio-track#stage-N]] for details.

---

*Previous: [[{prev-stage}]] · Next: [[{next-stage}]]*
```

Rules:
- First stage links Previous to `[[00-pipeline-overview]]`
- Last stage has no Next link
- Numbered sections use `N.1`, `N.2` format (N = stage number)
- At least one `[!tip]` or `[!hint]` per stage
- Exactly one `[!portfolio]` callout at the end before navigation
- Estimated hours must be realistic for the specific learner
- Every URL must be verified before writing

Target length: 80-180 lines per stage.

---

## 3. Portfolio Track

**File**: `portfolio-track.md`

```markdown
---
tags:
  - {pipeline-tag}
  - portfolio
aliases:
  - portfolio-track
  - Portfolio Track
  - Publishing Track
created: YYYY-MM-DD
status: not-started
---

# Portfolio Track

Parallel to the learning stages. Different pacing — finish exercises mid-week,
write the artifact on the weekend.

## Stage 1: {Title}

**Artifact:** {What to create — be specific about format and scope}
**Format:** {Blog post / GitHub repo / notebook / video / etc.}
**Publish to:** {Medium, dev.to, personal blog, GitHub, etc.}
**Share on:** {Twitter/X, LinkedIn, relevant subreddit, HN}

- [ ] Draft the artifact
- [ ] Get one person to review it (peer, mentor, or online community)
- [ ] Publish
- [ ] Share with brief commentary

## Stage 2: {Title}
...same pattern...

## Review Cadence

- [ ] **By week {X}:** Do you have {N} artifacts published? If not, why?
- [ ] **By week {Y}:** Review all artifacts. Which got engagement? What resonated?
- [ ] **Final:** Compile portfolio page / GitHub profile README linking all artifacts

## Quality Bar

{Domain-specific quality criteria. What makes an artifact impressive vs. tutorial output?}

- {Criterion 1}
- {Criterion 2}
- {Criterion 3}
```

Target length: 80-150 lines.

---

## 4. Framework Verdicts

**File**: `framework-verdicts.md`

```markdown
---
tags:
  - {pipeline-tag}
  - frameworks
aliases:
  - framework-verdicts
  - Framework Verdicts
  - Tool Verdicts
created: YYYY-MM-DD
status: not-started
---

# Framework Verdicts

Tools and frameworks assessed against actual hiring signals and industry usage.
Verdicts: **Learn** (core skill) · **Use** (use it, don't master it) ·
**Skim** (know what it does) · **Skip** (not worth your time) · **Later** (after pipeline)

| Tool/Framework | Version | Maintained? | Hiring Signal | Role in Pipeline | Verdict |
|----------------|---------|-------------|---------------|------------------|---------|
| ... | ... | Yes/No | High/Med/Low/None | Stage N | Learn |

## Key Takeaways

3-5 bullet points summarizing the most important tool decisions.

## Honest Truth

{Controversial or non-obvious tool decisions. Why you're recommending X over Y
when the internet argues about it. Be specific and cite evidence from job postings
or community discussions.}

## URLs Verified

As of: YYYY-MM-DD
```

Target length: 40-80 lines.

---

## 5. Career Targets

**File**: `career-targets.md`

```markdown
---
tags:
  - {pipeline-tag}
  - career
aliases:
  - career-targets
  - Career Targets
created: YYYY-MM-DD
status: not-started
---

# Career Targets

Where this pipeline gets you and what gaps remain.

## What This Pipeline Gives You

After completing all stages and portfolio artifacts, you can credibly claim:
- {Skill/credential 1}
- {Skill/credential 2}

## Roles This Unlocks

| Role | Company Tier | Salary Range | Pipeline Coverage | Gap |
|------|-------------|--------------|-------------------|-----|
| ... | Startup/Mid/FAANG | $X-Y | Full/Partial | ... |

## Bridge to AI Career

{How this domain connects to the learner's stated goal of working in AI.
Be specific — not "this is useful for AI" but "companies like X hire people
who can do Y, which you'll have after Stage Z."}

## Honest Assessment

{What this pipeline does NOT prepare you for. What else you'd need.
Don't oversell — the learner values honest feedback over encouragement.}

## Next Pipelines to Consider

- [[{suggested-pipeline-1}]] — {why, when}
- {Topic} pipeline — {why, when}
```

Target length: 50-90 lines.

---

## 6. Reading List

**File**: `reading-list.md`

```markdown
---
tags:
  - {pipeline-tag}
  - reading-list
aliases:
  - reading-list
  - Reading List
  - Resources
created: YYYY-MM-DD
status: not-started
---

# Reading List

All resources organized by stage. URLs verified as of YYYY-MM-DD.

## Stage 1: {Title}

### Core (must complete)

- [ ] [{Title}]({URL}) — {Author} · {Format: book/course/video/paper} · {Cost: free/$X} · {Est. hours}
- [ ] ...

### Supplementary (if time permits)

- [ ] ...

## Stage 2: {Title}
...same pattern...

## Cross-Stage Resources

Resources that span multiple stages (also listed in overview backbone):

- [ ] [{Title}]({URL}) — {relevant stages}
```

Rules:
- Every URL must be verified via WebFetch before writing
- Include cost (free, $X, subscription required)
- Include estimated time to complete
- Mark core vs. supplementary clearly

Target length: 60-180 lines.

---

## 7. Hardware Strategy (conditional)

**File**: `hardware-strategy.md`

Generate ONLY when the domain involves: GPU compute, model training, simulations,
large dataset processing, or server deployment.

Do NOT generate for: pure theory, data modeling, software design, business strategy.

```markdown
---
tags:
  - {pipeline-tag}
  - hardware
aliases:
  - hardware-strategy
  - Hardware Strategy
created: YYYY-MM-DD
status: not-started
---

# Hardware Strategy

What runs where and what it costs.

## Your Setup

{Based on learner's stated hardware from CLAUDE.md}

## What Runs Locally

| Task | RAM Needed | GPU Needed | Feasible? |
|------|-----------|------------|-----------|
| ... | ... | ... | Yes/No/With constraints |

## Cloud Options

| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| ... | ... | ... | ... |

## Stage-by-Stage Compute Guide

| Stage | Local? | Cloud Needed? | Est. Cloud Cost |
|-------|--------|---------------|-----------------|
| ... | ... | ... | ... |
```

Target length: 40-70 lines.

---

## 8. Templates

**Folder**: `templates/`

Always generate `templates/blog-post-template.md`:

```markdown
---
tags:
  - {pipeline-tag}
  - template
aliases:
  - blog-post-template
created: YYYY-MM-DD
status: template
---

# {Title}

## Hook (1-2 paragraphs)

What problem does this solve? Why should anyone care?
Start with a concrete scenario, not an abstract definition.

## Context (2-3 paragraphs)

What does the reader need to know to follow along?
Assume they're smart but unfamiliar with this specific topic.

## The Thing Itself (bulk of the post)

Walk through the implementation, concept, or finding.
Use code blocks, diagrams, or examples as appropriate.
Show your work — readers learn more from process than results.

## What I Learned / What Surprised Me (1-2 paragraphs)

The non-obvious takeaway. What would you tell past-you?

## What's Next (1 paragraph)

Where this leads. Link to the next stage or related work.

---

**Length target:** 800-1500 words
**Voice:** Technical but approachable. First person. Show uncertainty where it exists.
**Publish to:** {Suggested platform}
```

Generate additional domain-specific templates based on the portfolio artifacts
(e.g., model-card-template.md for ML, proof-template.md for math,
case-study-template.md for business).

---

## 9. Frontmatter Reference

All pipeline files use this schema:

```yaml
---
tags:        # YAML list. First tag = pipeline identifier (kebab-case domain).
             # Additional tags from: pipeline-overview, stage, portfolio,
             # frameworks, career, reading-list, hardware, template,
             # plus topic tags from vault taxonomy
aliases:     # YAML list. Include filename (without .md), display name, short name
created:     # YYYY-MM-DD (never timestamps)
status:      # not-started | in-progress | complete | template
---
```

Pipeline files deliberately omit the `type:` field. This matches the existing
er-kg-pipeline and llm-pipeline-all conventions.

The pipeline identifier tag should be kebab-case: `transformers`, `knowledge-graphs`,
`distributed-systems`, etc.

---

## 10. Cross-Reference Patterns

Wikilink rules for pipeline files:

- **Overview → Stages**: `[[01-stage-name]]` in the Pipeline Stages table
- **Overview → Support files**: `[[portfolio-track]]`, `[[framework-verdicts]]`, etc.
- **Stage → Adjacent stages**: Navigation footer `*Previous: [[X]] · Next: [[Y]]*`
- **Stage → Portfolio**: `[[portfolio-track#stage-N]]` in the portfolio callout
- **Stage → Overview**: `[[00-pipeline-overview]]` for first stage's Previous link
- **Career → Suggested pipelines**: `[[{pipeline-name}]]` if it exists in vault, plain text if not
- **Reading list → Stages**: Reference stage names in section headers (no wikilink needed since they're headers)

Every file must have at least one outgoing wikilink. The vault should form a connected graph — no orphan files within the pipeline folder.
