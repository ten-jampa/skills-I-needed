# Worked Examples

Four real cases from a research-enrichment project (academic papers → author identification →
downstream prioritization). Each is tagged with its **claim type** from the taxonomy in `SKILL.md`.
The domain is specific; the pattern is not. What transfers is the *shape* of the cheap real check.

The numbers are the point. "Method A performed worse than method B" teaches nothing. "5 of 21
versus 134 of 134" teaches the discipline.

---

## 1. Racing two methods instead of picking one by intuition

**Claim type: Comparative**

**The belief under test**: "To confirm that a paper's listed author ('J. Smith') is the same real
person as some external profile (LinkedIn, homepage, ORCID), searching by name and seeing what
comes back is good enough."

This is the intuitive-seeming approach, and it is exactly the kind of belief that ships unexamined.

**The experiment**: Instead of trusting the intuition, run it against real cases and *count*. Then
run the alternative — entering through a hard identifier — against **the same cases**.

**The result**:

| Method | Correct resolutions |
|---|---|
| Name-only search | **5 of 21** (16 failures) |
| DOI → structured record → person | **134 of 134** |

**Why it worked**: The gap between "seems reasonable" and "measured" was enormous, and it only
appeared because both methods were run and outcomes counted. Shipping the first plausible idea
would have built an entire pipeline on a 24%-accurate resolver.

**Transferable move**: When two approaches are available and one *feels* obvious, race them on the
same cases and count. The comparative claim is cheap to test and expensive to get wrong.

---

## 2. Testing a whole product thesis, not just a technical detail

**Claim type: Thesis**

**The belief under test**: "We can read research papers and predict which authors will go on to
found startups, ahead of the market."

A strategic bet, not an implementation choice — expensive to build against, expensive to be wrong
about. Precisely the class of belief that normally goes untested because testing it feels
premature.

**The experiment**: Check the thesis against known ground truth — people who are *already* known
PhD-founder-turned-CEOs. If the thesis holds, their papers should have carried a signal *before*
they were visible as founders.

**The result**: In **32 of 33** cases, the person already had a visible paper trail before anyone
would have needed to predict anything. The papers were documenting an already-visible signal, not
forecasting a hidden one.

**Why it worked**: One check against known cases invalidated the entire "predict early" framing
before it absorbed real engineering effort.

**Transferable move — the response matters as much as the check**: The team did not quietly rework
the pitch to save face. They rewrote the product's whole mental model around the finding: *the
value isn't prediction, it's broad, low-cost tracking that a human can later query when they
already have a reason to look.* A falsified thesis should change the downstream design, not get
softened into survival.

---

## 3. Calibrating a noisy heuristic against a real, varied batch

**Claim type: Statistical / accuracy**

**The belief under test**: "This keyword-matching rule flags whether a paper is about real
infrastructure/systems work" — useful for prioritizing which papers to look at closely.

**The experiment**: Before trusting the rule, run it against **16 real, varied papers** and check
by hand.

**The result**:

| Version | Fire rate | Quality of flagged papers |
|---|---|---|
| v1 — common words (`system`, `deploy`) | **9 of 16 (56%)** | Meaningless — those words appear in almost any ML paper |
| v2 — tightened, specific terms | **4 of 16 (25%)** | Noticeably stronger, more specific evidence |

**Why it worked**: The diagnosis followed from the number — the words were too generic to
discriminate. And critically, the batch was **real and varied**, not a couple of hand-picked
good/bad cases. A hand-picked pair hides exactly the kind of over-firing that a varied batch
exposes.

**Transferable move**: A heuristic is not trusted until it has been checked against real, messy
examples with a counted fire rate. Two cherry-picked examples prove nothing.

---

## 4. Writing down disproven beliefs so they don't quietly return

**Claim type: Ledger discipline (applies to all four)**

**The belief under test**: "This category in the working dataset is nearly empty" — implying almost
no relevant activity existed there.

**The experiment**: Inspect the real numbers.

**The result**: False. The category was **undercounted** because most of the underlying records
simply had not been filled in yet — not because the activity did not exist. A missing-data artifact
had been read as a substantive finding.

**Why it worked, and what made it compound**: The team did not just fix the number quietly. They
wrote an explicit list of *"corrections made this session — do not resurrect these,"* so that later
readers — including other AI agents working on the same project later — would not re-adopt a belief
that had already been tested and shown false.

**Transferable move**: A correction that lives only in a conversation evaporates. `EXPERIMENTS.md`
is append-only for exactly this reason: the value of a falsified belief does not decay, because the
next agent is equally likely to find it plausible.

---

## The pattern, stated once

Not "be careful" in the abstract. A specific discipline:

1. **State the belief plainly enough that it could be wrong.**
2. **Find the cheapest available real-world check** — a small batch of real cases, a head-to-head
   comparison of two methods, a lookup against known ground truth.
3. **Run it before** spending real engineering or strategic effort on top of the belief.
4. **When the check disagrees, treat that as valuable information to record and propagate** — not
   an inconvenience to smooth over.
