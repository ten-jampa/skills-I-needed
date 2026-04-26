# ML Paper Guide Reference

Use this reference when you need detailed guidance beyond the core workflow in `SKILL.md`.

## Canonical structure

### Abstract

Cover four things quickly:

- What the paper is trying to do and why it matters
- Why the problem is hard
- What the paper contributes
- How the paper validates the contribution through experiments, theory, or both

Treat the abstract as a compressed version of the full paper.

### Introduction

Expand the abstract into a fuller narrative:

- Problem and relevance
- Difficulty
- Proposed solution
- Validation strategy
- Main results
- Explicit contribution bullets when helpful

If space permits, mention future work briefly. A first-page overview figure is often valuable.

### Related Work

Frame prior work as alternative attempts to solve the same problem. Compare and contrast; do not merely summarize.

For each relevant baseline or prior line of work, clarify:

- What assumptions it makes
- How its method differs
- Whether it applies to the current setting
- Whether it should appear in experiments

If a method is not comparable, state why.

### Background

Explain the concepts, notation, and assumptions needed to understand the paper. Include a problem-setting subsection unless the problem setting is itself novel enough to justify its own section.

### Problem Setting

Make this a separate section only when the problem setting is a contribution.

### Method

Describe what the paper does, why the design choices exist, and how the method connects to the formalism introduced earlier.

### Experimental Setup

State how the claims are tested:

- Data or environments
- Metrics
- Baselines
- Implementation details
- Hyperparameters where material
- Evaluation protocol

### Results and Discussion

Show outcomes and interpret them. Include:

- Baseline comparisons
- Uncertainty estimates or confidence intervals when appropriate
- Fairness notes on hyperparameters and tuning budgets
- Ablations
- Failure modes and limitations

### Conclusion

Recap the problem, contribution, and evidence. Keep future work realistic.

## Recommended drafting process

### Start with an outline

Write one line per paragraph before drafting. Each line should capture one idea that will later become one paragraph.

This prevents expensive rewrites later. It also makes collaboration easier because people can review the logic before the prose hardens.

### Keep paragraph TL;DRs visible

In LaTeX drafts, keep a comment above each paragraph:

```tex
% One-line paragraph claim
Paragraph text that expands that claim clearly.
```

This helps both the writer and reviewers verify flow quickly.

### Write the abstract early

Draft the abstract before all results are final. This often exposes missing logic, weak experiments, or an incoherent story earlier than a late-stage writeup would.

## Authorship guidance

Use this as a rule of thumb, not law:

- First author: did most of the work and led writing
- Second author: made substantial contributions, often equal-contribution territory if the work split was comparable
- Middle authors: contributed meaningfully, even if some results did not survive to the final paper
- Second senior author: gave day-to-day guidance
- Senior author: carried overall responsibility for the project

Be generous but explicit. Set authorship expectations early.

## Writing checks

### Style

- Prefer active voice unless passive voice clearly reduces reader load
- Keep tense consistent
- Cut filler words such as `can`, `in order to`, and `shall`
- Use simple language over ornate language
- Split long sentences
- Avoid repeated words within a sentence or paragraph

### Contribution boundaries

- State clearly what prior work did
- State clearly what this paper adds
- Never blur those lines for rhetorical effect

### Terminology and notation

- Introduce terminology that is specific to the work
- Avoid synonyms for work-specific terms
- Introduce acronyms before first use
- Introduce only symbols and acronyms that you actually use
- Be consistent about bold and italics

### Claims

- Cite claims not established by your experiments
- Avoid grandiose language and subjective adjectives
- Avoid anthropomorphizing AI systems
- Keep problem statements and conclusions calibrated to evidence

### LaTeX and citation hygiene

- Use proper LaTeX quotation marks: ``quoted text''
- Consider `\enquote{}` from `csquotes`
- Punctuate equations like normal prose
- Use `\citet{}` when authors are part of the sentence
- Use `~\citep{}` otherwise
- Prefer `\usepackage[backref=page]{hyperref}` over plain `hyperref`
- Use `cleveref` for cross-references
- Check the PDF for broken references shown as `??`
- Cite the published version of a paper when appropriate, not just the arXiv version

### Presentation

- Avoid ugly page breaks and obvious whitespace waste
- Fill the page limit cleanly
- Pick British or American English and stay consistent
- Use change tracking in collaborative editing tools

## Final pass checklist

- Does each section do one distinct job?
- Are the contributions explicit and defensible?
- Does each experiment answer a paper claim?
- Are baselines fair and justified?
- Are limitations acknowledged?
- Can roughly one third of the words still be cut?
