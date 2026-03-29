---
name: build-filter
description: Go/no-go filter for pet projects and personal project ideas. Use when the user proposes a new project, pitches an idea, brainstorms features, or is about to commit time to building something. Also use when the user asks to evaluate, vet, or stress-test an idea. Prevents over-ideation with nothing to show by enforcing 7 hard gates before commitment.
---

# Build Filter

Run every proposed project or feature idea through these 7 gates. Require "yes" on most before proceeding. If fewer than 5 pass, recommend narrowing scope or changing direction.

## The 7 Gates

Score each gate YES / NO / UNCLEAR with a one-line rationale.

| # | Gate | What "yes" means |
|---|------|-------------------|
| 1 | **Real recurring pain?** | The user (or clear audience) hits this problem repeatedly, not once |
| 2 | **Deterministic core?** | The main execution logic is reliable and testable, not fuzzy heuristics |
| 3 | **Useful artifact?** | Produces a tangible output: file, report, config, deployed thing |
| 4 | **Explicit context boundaries?** | Inputs, outputs, and scope are well-defined — no unbounded sprawl |
| 5 | **Compounds over time?** | Gets better through memory, skills, data, or network effects |
| 6 | **Demo in <15 seconds?** | Value is immediately obvious to someone watching |
| 7 | **Hard metric?** | At least one measurable success criterion exists |

## Procedure

1. State the project idea in one sentence.
2. Score all 7 gates — be honest, not generous. UNCLEAR counts as NO.
3. Tally: **5+ YES** = proceed. **4 or fewer** = stop and narrow.
4. For each NO/UNCLEAR, suggest a concrete scope change that would flip it to YES.
5. If the idea survives, restate the narrowed version in one sentence.

## Tone

Be direct. The point is to kill bad ideas fast so good ones get built. Do not soften NO verdicts. If the user is excited but the gates say no, say so — then help them find the version that passes.
