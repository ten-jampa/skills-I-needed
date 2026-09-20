---
name: experiment-driven-development
description: Validate load-bearing beliefs with the cheapest real check before building on them, and record the verdict in EXPERIMENTS.md. Use before writing a script, pipeline, module, or analysis that rests on an unverified belief about an external system (API shape, pagination, rate limits, auth), a data shape (field populated? category empty? schema stable?), a method's accuracy (does this heuristic or matching rule actually discriminate?), or a strategic premise (is this thesis true?). Also use when the user says "experiment-driven", "edd", "validate that first", "test the assumption", "smoketest it", or asks why a design was chosen. Prevents building a large, coherent-looking system on an assumption a five-minute check would have falsified.
---

# Experiment-Driven Development

A belief you have not checked is a hypothesis, not a fact. This skill is the loop that turns
hypotheses into recorded verdicts *before* real effort is spent on top of them.

The expensive mistake it avoids: a large, coherent-looking system built on an assumption a
five-minute check would have shown false.

**Read `EXPERIMENTS.md` (repo root) before forming beliefs about this project.** A claim already
recorded there is settled — do not re-test it, and do not resurrect a claim recorded as falsified.

## Phase 1 — State the beliefs plainly enough to be wrong

Enumerate **3–5** beliefs the plan rests on. Each must be phrased so it *could* come out false.

- ✅ "The list-entries endpoint returns all entries in one page for lists under 500."
- ❌ "The API works as expected." (unfalsifiable — no observation could contradict it)

Then rank them by one test:

> **If this belief is false, does the *plan* change, or just the *implementation*?**

Plan-changing beliefs are load-bearing. Rank those first.

**Show the ranked list to the user before testing anything.** This is not optional and it is not a
formality. A hallucinated plan arrives bundled with hallucinated-but-plausible hypotheses, and from
inside the hallucination the load-bearing belief looks like a detail. The user's ten seconds of
reading is the only point where knowledge of the actual goal enters the loop. They may re-rank.

**Test at most 3 per decision.** The cap is the guard against analysis paralysis.

## Phase 1.5 — System-1 triage gate (advisory only, local Laya)

The gate suggests. You decide. It never auto-passes or auto-fails a belief.
Run one belief per call — three beliefs in one state blur it (measured: type conf 0.03).

### Frozen questions (do not reword without a new batch run)

```python
QUESTIONS = {
    "claim_type": {
        "type": "choice",
        "instructions": "What kind of claim is `observation` plus `question`?",
        "criteria": {
            "factual": "settled by opening one file, reading one path, or timing one load",
            "statistical": "one case cannot settle it; needs counts across many varied cases",
            "comparative": "needs head-to-head counts on the same cases",
            "thesis": "needs known ground-truth cases",
        },
    },
    "run_check": {
        "type": "noul",
        "instructions": "Should we run one cheap local check now to settle `question`?",
        "criteria": {
            "true": "yes: run one cheap local check; it costs seconds and writes nothing",
            "false": "no: evidence is already in hand and trusted",
        },
    },
}
```

Any System-1 model with Choice/Score/Noul works here (hosted Jev or local Laya).
Evidence below is from local Laya (`laya.load("aac6fef/laya-mlx")`, Apple Silicon):
a 12-case batch moved type agreement 6/12 → 10/12 and check agreement 7/12 → 8/12
across five controlled runs (three word-tweaks, one state rewrite).

### State rule (states beat words)

- Facts, not conclusions. Name the path, file, or number to open.
- Never "may hold" / "may support". Hedged states read as thesis (measured: factual 0/4).
- The falsifier lives in `EXPERIMENTS.md`, written before running. Never inside the
  state — the same claim flipped run_check 0.07 → 0.86 when falsifier text entered it.

### Trust lines (ask human, do not decide)

- `claim_type` confidence below 0.30 → ask human. Reword state, re-run.
- `run_check` inside 0.40–0.60 → ask human regardless of side. Boundary is not a decision.
- Noul confidence is `max(p, 1-p)` with floor 0.5. Never rank it next to Choice
  confidence (which is `1 - entropy/log(k)`).
- A score is not proof. Code validates the pick, executes, re-observes fresh state.

### Rewording rule

One line per experiment. Same twelve states. Re-run all twelve. Compare counts.
Criterion lines compete for mass: strengthening one steals from neighbours
(measured: statistical fixed 0/3 → 2/3 while factual broke 2/4 → 0/4).

## Phase 2 — Pick the experiment shape from the claim type

The check must touch reality, and its result must be stated in a form that could have come out the
other way. What "cheapest real check" means depends on what kind of claim it is:

| Claim type | Looks like | Experiment shape |
|---|---|---|
| **Factual** | "this endpoint paginates with `next_page_token`" | One real call or lookup. Read the actual response. `N=1` is correct here. |
| **Statistical / accuracy** | "this keyword rule discriminates useful papers" | A real, **varied** batch + count outcomes. A hand-picked good/bad pair hides over-firing. |
| **Comparative** | "name search is good enough vs DOI-first" | Head-to-head on the **same** cases. Count both. |
| **Thesis** | "papers predict who will found startups" | Known ground-truth cases. Does the signal appear when the thesis says it should? |

If the cheapest real check requires **writing throwaway code** rather than making a call or a
lookup, use the `prototype` skill for that step. Most checks need neither — a lookup against a
known record and a hand-labelled batch of 16 are not prototypes.

### Do not run an experiment when

- The decision is **cheaply reversible** — just do it and change it if wrong.
- The claim is **already in `EXPERIMENTS.md`** with a verdict.
- Nobody doubted it. Proving the obvious for an hour is a tax, not a discipline.

## Phase 3 — Write the falsifier, then run

**Before running, write down what result would falsify the belief.** In `EXPERIMENTS.md`, as a
committed prediction:

> "Falsified if the rule fires on more than 30% of a varied batch."

This ordering is load-bearing. Writing the falsifier first is what stops the observed result from
being retrofitted into a pass.

Then, gated by cost:

- **Cheap and side-effect-free** (a read call, a lookup, a local count) — run it now, no permission needed.
- **Costs real time, real money, or writes data** — state the plan and the cost, then stop and ask.

## Phase 4 — Record the verdict, with receipts

Append to `EXPERIMENTS.md` at repo root. Create the file if absent. **Append-only** — a falsified
belief never stops being useful. Never prune it.

````markdown
## [YYYY-MM-DD] <the claim, stated falsifiably>

**Falsifier**: <what result would have proven this wrong — written before running>
**Experiment**: <what was actually run>
**Receipts**:
```
$ <the actual command or tool call>
<raw output excerpt — pasted, not summarized>
```
**Result**: <outcome; include N for statistical claims — "9 of 16 (56%)">
**Verdict**: SURVIVED / FALSIFIED / UNVERIFIED
**Unblocked**: <which decision now rests on this>
````

Rules:

- **A verdict without receipts is `UNVERIFIED`**, and an `UNVERIFIED` claim is still an open
  assumption — treat it as untested. Raw output is cheap to include when the check was real and
  expensive to fabricate convincingly. If you reasoned instead of checking, say so and mark it
  `UNVERIFIED`. That path must stay available, or the pressure is to invent receipts.
- **Record surviving beliefs too**, not just falsified ones — with their falsifier. That is how a
  later reader knows it was actually checked rather than assumed.
- `N` is required for statistical, comparative, and thesis claims. Factual claims record `N=1` and
  the authoritative source. The slot is mandatory even at `N=1`: it forces the question *what
  actually convinced me?*

## When a check kills a load-bearing belief

**Stop. Do not patch around it.** This is the clause most easily weaseled out of and the one that
matters most.

1. State the correction loudly and explicitly — do not quietly reword the plan to save face.
2. Record it in `EXPERIMENTS.md` as `FALSIFIED`, with the number that killed it.
3. Propose a **revised plan** built on what is now known, and change the downstream design rather
   than working around the disagreement.
4. Wait for the user.

A thesis that dies should rewrite the mental model, not get reworded. See example 2 in
`references/examples.md`: "predict founders early" was falsified at 32/33, and the correct response
was to rebuild the product's framing around low-cost tracking — not to soften the pitch.

## Worked examples

`references/examples.md` — four real cases, each tagged with its claim type: a method race
(5/21 vs 134/134), a thesis check (32/33), a heuristic calibration (56% → 25%), and a corrections
ledger. Read it when the shape of a cheap real check is not obvious.
