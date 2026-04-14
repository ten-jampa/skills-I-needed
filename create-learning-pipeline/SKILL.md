---
name: create-learning-pipeline
description: "Generate end-to-end learning curricula as Obsidian vault folders with staged roadmaps, portfolio tracks, framework verdicts, career targets, and reading lists — all as Obsidian-native markdown with wikilinks, callouts, checkboxes, and proper frontmatter. Use when the user says 'create a learning pipeline', 'build me a curriculum for [domain]', 'learning pipeline for [topic]', 'pipeline for [skill]', 'make me a pipeline like the LLM one', or invokes /create-learning-pipeline {domain}. Also trigger when the user wants a structured multi-week learning plan with portfolio artifacts for any technical or non-technical domain."
---

# Create Learning Pipeline

Generate a complete, research-backed learning pipeline as an Obsidian vault folder. The pipeline follows the pattern established in the user's existing `er-kg-pipeline` and `llm-pipeline-all` vaults.

**Vault path**: `/Users/tenzinjampa/Documents/great-vault/{domain}-pipeline/`

## Workflow

1. **Gather context** — read learner profile, ask domain-specific questions
2. **Deep research** — spawn 5 parallel subagents to research the domain
3. **Structure** — synthesize research into stages, sequencing, hours
4. **Generate** — write all vault files per spec
5. **Verify** — check URLs, run vault linter, validate wikilinks
6. **Present** — show structure, explain refinement options

---

## Step 1: Gather Context

Read the learner's profile from `~/.claude/CLAUDE.md` and any user-type memories. The user is a 25-26yo physics + philosophy graduate, data scientist at a VC firm, Python-focused, fundamentals-first learner who wants to work in AI.

Auto-populate the learner context. Only ask these domain-specific questions:

1. **Scope**: "For {domain} specifically: are you targeting theory, practice, or end-to-end?"
2. **Skip list**: "What can I skip? Anything you've already covered or decided to avoid?"
3. **Timeline**: "Timeline target? Your ER-KG pipeline was 3-4 weeks at 2h/day; the LLM pipeline was 13 weeks at 20-25h/week."
4. **Target outcome**: "What role or capability are you building toward with this?"

If the user passed arguments after the domain (e.g., `/create-learning-pipeline transformers --theory --4weeks`), extract answers from the arguments and skip redundant questions.

Also scan the vault for existing pipelines (`*-pipeline*/`) to avoid duplicating content and to cross-reference where relevant.

---

## Step 2: Deep Research

Spawn 5 subagents in parallel using the Agent tool. Each subagent uses WebSearch and WebFetch for research. Provide each with the domain name and learner context.

### Subagent 1: Tools & Frameworks
Research the current state of tools, libraries, and frameworks in {domain}:
- Current versions, maintenance status, last release dates
- Which are industry-standard vs. trendy vs. deprecated
- Installation/setup requirements and compatibility with Python/macOS

### Subagent 2: Job Market
Search for 10-15 real job postings at companies relevant to {domain}:
- Required and preferred skills/tools
- Experience level expectations
- Salary ranges where available
- Which companies are hiring for this

### Subagent 3: Learning Resources
Find the best current learning resources:
- Courses (free and paid), books, video series, blog posts, papers
- **Verify every URL exists via WebFetch** — do not hallucinate links
- Note: cost, format, estimated completion time, recency
- Prioritize resources updated within the last 18 months

### Subagent 4: Recent Changes
Research what changed in {domain} in the last 12 months:
- New tools, architectures, or approaches
- Deprecated or superseded approaches
- Shifts in community consensus or best practices
- What older curricula miss

### Subagent 5: Community Consensus
Search Reddit, HN, Twitter/X, and domain-specific forums:
- Recommended learning paths from practitioners
- Common mistakes beginners make
- What to learn vs. what to skip (and why)
- Controversial recommendations and the arguments for each side

---

## Step 3: Structure the Pipeline

Synthesize all 5 research outputs into a pipeline structure.

### Determine stages
- Typically 4-8 stages depending on domain breadth
- Sequence by dependency: what must be learned before what?
- Each stage should be completable in 1-2 weeks at the learner's stated pace
- First stage should connect to what the learner already knows (physics, math, Python, data science)

### Set hours and compute
- Estimate hours per stage (be realistic for someone with a full-time job)
- Mark each stage: local only, cloud needed, or both
- If any stage needs cloud compute, flag `hardware-strategy.md` for generation

### Establish file names
Lock down all filenames before generating any content. This prevents wikilink breakage.

```
00-pipeline-overview.md
01-{stage-1-slug}.md
02-{stage-2-slug}.md
...
NN-{stage-N-slug}.md
portfolio-track.md
framework-verdicts.md
career-targets.md
reading-list.md
hardware-strategy.md  (conditional — only if compute needed)
templates/blog-post-template.md
templates/{domain-artifact-template}.md  (domain-specific)
```

---

## Step 4: Generate Files

Read [references/pipeline-spec.md](references/pipeline-spec.md) for exact content specifications per file type.

### Generation order

Generate in this order to maintain wikilink consistency:

1. Create the pipeline folder and `templates/` subfolder
2. `00-pipeline-overview.md` — establishes stage names everything links to
3. Stage files `01-*.md` through `NN-*.md` — in order
4. `portfolio-track.md`
5. `framework-verdicts.md`
6. `career-targets.md`
7. `reading-list.md`
8. `hardware-strategy.md` (if needed)
9. Template files

### Writing each file

Use the Write tool for each file. Follow these rules:

- **Frontmatter**: Use the pipeline frontmatter schema (tags, aliases, created, status). No `type:` field.
- **Pipeline tag**: kebab-case domain name (e.g., `transformers`, `distributed-systems`)
- **Callouts**: `[!tip]` for insights, `[!hint]` for gotchas, `[!portfolio]` for portfolio artifacts, `[!check]` for checkpoints
- **Checkboxes**: `- [ ]` for all tasks and checkpoint criteria
- **Navigation**: `---` separator then `*Previous: [[prev]] · Next: [[next]]*`
- **Wikilinks**: Cross-reference everything. See pipeline-spec.md section 10 for patterns.
- **URLs**: Every URL must have been verified by a research subagent. If unsure, verify with WebFetch before writing.

### Content quality rules

- **Testable checkpoints**: Never "understand X." Always "implement X from scratch" or "explain X to someone" or "run benchmark Y."
- **Design decisions**: Mark choice points explicitly: `**Design decision (yours to make):** ...`
- **Learning loops**: Every stage includes: Read → Implement → Evaluate → Ablate → Memo
- **Exploration room**: State objectives and constraints, provide hints for pitfalls, but leave architecture/design choices to the learner
- **Existing knowledge bridges**: Connect to physics, philosophy, math, or data science where possible via `[!tip]` callouts
- **Honest assessments**: Don't oversell. The learner values honesty over encouragement.

---

## Step 5: Verify

After generating all files:

1. **URL spot-check**: Pick 5-10 URLs from `reading-list.md` and verify via WebFetch
2. **Wikilink audit**: Ensure every `[[link]]` in the pipeline folder resolves to an existing file
3. **Frontmatter check**: Every file has tags, aliases, created, status
4. **Vault linter** (if available): Run `python3 /Users/tenzinjampa/Documents/great-vault/00_System/scripts/vault_lint.py` and check for errors in the pipeline folder

---

## Step 6: Present

Show the user:

1. **Folder tree**: List all generated files
2. **Pipeline summary**: Stage names, estimated total hours, timeline
3. **Key research findings**: 2-3 surprising or non-obvious things from the research that shaped the pipeline
4. **Refinement options**: Explain what they can request next

Example:

```
Pipeline generated: transformers-pipeline/ (7 files + 2 templates)

Stages: 5 stages over 6 weeks (~15h/week)
  1. Linear Algebra & Attention Math (10h)
  2. Transformer Architecture from Scratch (20h)
  ...

Key findings from research:
- Flash Attention 3 is now the default — older tutorials still teach v1
- HuggingFace Trainer API has changed significantly since 2025
- Job postings increasingly ask for inference optimization, not just training

Refinements available:
- "Expand stage N" — get a detailed day-by-day walkthrough
- "Calibrate against job postings" — cross-compare with real listings
- "Audit the tools" — re-verify framework verdicts
- "Compare with [curriculum]" — cross-pollinate from another resource
- "Review portfolio plan" — audit artifacts against target roles
```

---

## Refinement Workflows

After initial generation, the user can request iterative improvements. See [references/refinements.md](references/refinements.md) for the 5 available refinement workflows:

1. **Stage Deep-Dive** — expand a stage into a detailed day-by-day walkthrough
2. **Job Market Calibration** — cross-compare pipeline skills with real job postings
3. **Framework/Tool Audit** — re-verify all tools are current, maintained, and worth learning
4. **Cross-Pollination Check** — compare with another curriculum, identify steals
5. **Portfolio & Career Review** — audit artifacts against target role requirements

These are conversational — the user requests them naturally, not via separate commands.

---

## Vault Conventions

### Frontmatter schema (all pipeline files)

```yaml
---
tags:
  - {pipeline-tag}        # kebab-case domain: transformers, knowledge-graphs
  - {category-tag}        # stage, portfolio, frameworks, career, reading-list, etc.
  - {topic-tags}          # from vault taxonomy: ai/llm, ai/agents, career, etc.
aliases:
  - {filename-without-ext}
  - "{Display Name}"
  - "{Short Name}"
created: YYYY-MM-DD
status: not-started       # not-started | in-progress | complete | template
---
```

Pipeline files deliberately omit the `type:` field. This matches existing pipeline conventions.

### Obsidian formatting

- `- [ ]` checkboxes for all tasks (never numbered lists for tasks)
- `> [!tip]`, `> [!hint]`, `> [!portfolio]`, `> [!check]` callouts
- Tables for comparisons (frameworks, hardware, resources, timeline)
- Code blocks with language tags: ` ```python `, ` ```bash `
- `[[wikilinks]]` for all internal cross-references
- `[[note#section]]` for anchor links to specific sections
- `---` horizontal rule before navigation footer
- Concise prose — working document, not a textbook

### Output folder structure

Flat layout (matching `er-kg-pipeline` convention):

```
{domain}-pipeline/
├── 00-pipeline-overview.md
├── 01-{stage-slug}.md
├── 02-{stage-slug}.md
├── ...
├── portfolio-track.md
├── framework-verdicts.md
├── career-targets.md
├── reading-list.md
├── hardware-strategy.md      (only if compute needed)
└── templates/
    ├── blog-post-template.md
    └── {domain-artifact}.md   (domain-specific)
```

---

## Anti-Patterns

- **No day-by-day walkthroughs** in the initial generation. Stage files give structure and tasks. Detailed walkthroughs are generated on-demand via the Stage Deep-Dive refinement.
- **No "understand X" checkpoints.** Every checkpoint must be testable with an action verb.
- **No unverified URLs.** If a URL wasn't checked by a research subagent, verify it before writing.
- **No generic platitudes** in the Philosophy section. Connect to the learner's specific background.
- **No micro-managing hours.** Estimate per-stage, not per-task. Leave room for exploration.
- **No `type:` field** in frontmatter. Pipeline files use their own schema.
- **No duplicate content** with existing vault pipelines. Cross-reference instead.
