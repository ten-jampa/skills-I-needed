---
name: ml-paper-writing
description: Draft, structure, revise, and tighten machine learning research papers, workshop papers, rebuttals, and paper outlines. Use when Codex needs to turn notes or results into a clear paper structure, improve section flow, sharpen contributions, reduce fluff, enforce terminology and citation hygiene, or critique an ML paper draft section by section.
---

# ML Paper Writing

## Overview

Use this skill to turn research material into a readable ML paper with a conventional structure and a defensible story. Favor clarity over flourish, keep claims calibrated to evidence, and make the contribution boundaries explicit.

## Working Mode

Start by identifying the paper stage:

- Outline stage: build a one-line-per-paragraph outline before drafting prose
- Draft stage: improve structure, contribution framing, and paragraph logic
- Revision stage: tighten wording, fix consistency, and pressure-test claims

If the user supplies only raw notes, start from an outline. If the user supplies a draft, preserve the core content and improve ordering, clarity, and support.

## Core Workflow

### 1. Lock the paper story

Extract and state, in plain language:

- The problem: what the paper is trying to do and why it matters
- The difficulty: why the problem is non-trivial
- The contribution: what is actually new in this work
- The evidence: how the paper shows the contribution works

If any of these are weak or missing, say so directly before polishing prose. A clean story matters more than local sentence edits.

### 2. Build or repair the structure

Default to this section order unless the venue or paper type demands otherwise:

1. Abstract
2. Introduction
3. Related Work
4. Background
5. Problem Setting if the setting itself is novel
6. Method
7. Experimental Setup
8. Results and Discussion
9. Conclusion

Use [references/ml-paper-guide.md](references/ml-paper-guide.md) for section-level expectations and writing checks.

### 3. Draft from paragraph summaries

When writing new prose, use one summary line per paragraph first. In LaTeX drafts, keep that summary as a comment immediately above the paragraph until the section stabilizes.

Use this pattern:

```tex
% Paragraph claim in one line
Paragraph text that says exactly that claim, with no filler and no scope creep.
```

This is worth knowing: paragraph-level summaries make reordering cheap. They separate thinking from polishing, which is why outlines improve faster than full prose.

### 4. Separate content roles

Apply these distinctions consistently:

- Related Work: compare against alternative attempts to solve the same problem
- Background: explain prerequisites, notation, and concepts needed to understand the method
- Method: describe what this paper does and why
- Experimental Setup: specify datasets, metrics, baselines, implementation details, and protocol
- Results and Discussion: interpret outcomes, compare fairly, report uncertainty, and discuss limitations

Do not let Related Work collapse into summaries of prior papers. Compare and contrast assumptions, method, and applicability.

### 5. Pressure-test claims

For every strong claim, ask:

- Is this supported by experiments, theory, or citation?
- Is the scope too broad?
- Is the contribution clearly separated from prior work?

If not, narrow the claim or add support. Prefer precise claims over impressive-sounding ones.

## Revision Priorities

Revise in this order:

1. Story coherence across sections
2. Contribution clarity
3. Experimental fairness and evidence quality
4. Terminology, notation, and tense consistency
5. Sentence-level concision and style

Do not spend time polishing sentences that belong in a different paragraph or section.

## Common Deliverables

Use this skill for outputs like:

- A full paper outline from notes or experiment results
- A rewritten abstract or introduction
- A critique of a draft with section-by-section findings
- A checklist pass for style, citations, and LaTeX hygiene
- A contribution rewrite that sharpens novelty and evidence

## Reference Use

Read [references/ml-paper-guide.md](references/ml-paper-guide.md) when you need:

- The canonical ML paper structure
- Section-by-section drafting guidance
- Author ordering guidance from the source material
- A detailed list of writing pitfalls, citation rules, and LaTeX conventions
