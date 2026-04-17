---
name: domain-onboarding
description: "Interactive domain learning using the SEPA method (Structure, Enumeration, Process, Axiology). Guides the user through building a structured mental model of any unfamiliar domain — from VC and PE to transformer architectures to supply chains. Produces concrete artifacts: entity tables, Barker relationship sentences, state machines, stock-flow diagrams, and priority maps. Use when the user says 'learn a domain', 'domain onboarding', 'teach me about [domain]', 'SEPA method', 'help me understand [industry/field]', 'onboard me to [domain]', or wants to systematically build knowledge of an unfamiliar area. Also use when the user wants to model the structure and dynamics of a domain they're entering."
---

# Domain Onboarding (SEPA Method)

Interactive guided learning of any domain through progressive modeling: **Structure → Enumeration → Process → Axiology**. Each phase produces artifacts that feed the next. The method builds understanding through active modeling rather than passive absorption.

## Workflow Overview

```
1. SCOPE    → Define domain, check size, split if needed
2. PHASE S  → Entity discovery (guided: Claude drafts, user critiques)
3. PHASE E  → Relationship mapping with Barker sentences (guided)
4. PHASE P  → Dynamics and state machines (Socratic: Claude asks, user reasons)
5. PHASE A  → Values, metrics, tradeoffs (Socratic)
6. SAVE     → Optionally write all artifacts to a directory
```

The user can stop after any phase and resume later. Progress is tracked in-conversation.

## Step 1: Domain Scoping

When the user names a domain, evaluate its size before starting:

**Size check**: Can you enumerate the core entities in under 20 items? If yes, proceed. If no, the domain is too large — split it.

**Splitting procedure**: Propose 3-5 subdomains and ask the user which to start with. Example:
- "Machine Learning" → supervised learning, unsupervised learning, reinforcement learning, deep learning architectures, ML ops
- "Private Equity" → fund structure & operations, deal sourcing & execution, portfolio management, exits & returns, LP relations

**Competency questions**: Before modeling, ask the user to state 3-5 questions their domain model should answer. These constrain scope and provide a completeness check at the end.

Example: "What questions should your model of [domain] be able to answer? Give me 3-5."

Store these questions — revisit them after Phase E and Phase P to check coverage.

## Step 2: Phase S — Structure (Guided Mode)

**Goal**: Identify all entities and their attributes.

**Interaction mode**: GUIDED. Claude researches and drafts; user critiques and extends.

Read [references/barker-notation.md](references/barker-notation.md) for entity-vs-attribute test and attribute markers.

Procedure:

1. **Research the domain** using web search. Find 3-5 representative sources (industry overviews, Wikipedia, textbooks, practitioner guides). Extract the key nouns.

2. **Draft an entity list** with 8-15 candidate entities. For each entity, provide:
   - Name
   - 1-sentence description
   - 3-5 attributes with markers (`#` unique ID, `*` mandatory, `o` optional)

3. **Present to user** as a table. Ask:
   - "Does this capture the main things people track and manage in [domain]?"
   - "Is anything major missing?"
   - "Is anything here not really its own thing — more like a property of something else?"

4. **Iterate** based on feedback. Apply the Noy & McGuinness test on any disputed items: Does it have its own identity? Multiple instances? Would you store attributes about it?

5. **Completeness check**: Walk through a "day in the life" scenario. "If you're a [role] in this domain, what do you create, modify, look up, or report on in a typical day? Are all those things in our entity list?"

**Deliverable**: Entity-attribute inventory table (show in conversation as markdown table).

**Progress marker**: After completing Phase S, display:
```
--- SEPA Progress: [S] ████░░░░░░░░ 25% ---
Phase S complete. [X] entities identified, [Y] attributes mapped.
Ready for Phase E (Enumeration). Continue? Or save artifacts and pause?
```

## Step 3: Phase E — Enumeration (Guided Mode)

**Goal**: Map all relationships between entities using Barker sentences.

**Interaction mode**: GUIDED. Claude drafts sentences; user validates.

Read [references/barker-notation.md](references/barker-notation.md) for Barker sentence template, failure types, and many-to-many resolution.

Procedure:

1. **Draft Barker sentences** for all plausible entity pairs. Use the template:
   ```
   Each [ENTITY A] (must | may) be [RELATIONSHIP] (one and only one | one or more) [ENTITY B]
   ```
   Write BOTH directions for each relationship.

2. **Log failures openly**. For any sentence where optionality or cardinality is uncertain, flag it:
   - "I'm uncertain whether each [X] *must* or *may* have a [Y] — this depends on [specific business rule]. What's the rule here?"
   
   Classify failures by type (existence, connection, optionality, cardinality) so the user sees what kind of gap each represents.

3. **Present sentences in groups** (5-8 at a time) for validation. Ask the user to read each aloud mentally and check: "Is this grammatically correct and factually accurate?"

4. **Identify many-to-many relationships**. For each one, propose an intersection entity with its own attributes. These intersection entities often carry the most business-relevant data (amounts, dates, roles, percentages).

5. **Check for class hierarchies** (subtypes). Ask: "Are any of these entities really variants of a common parent type? Do any share most of their attributes but differ in a few?"

6. **Revisit competency questions** from Step 1. Can the entity-relationship model answer them? If not, what's missing?

**Deliverable**: Complete Barker sentences + failure log with resolutions.

**Progress marker**:
```
--- SEPA Progress: [S][E] ████████░░░░ 50% ---
Phase E complete. [X] relationships mapped, [Y] failures resolved, [Z] intersection entities created.
Ready for Phase P (Process). Continue?
```

## Step 4: Phase P — Process (Socratic Mode)

**Goal**: Identify how key entities change over time — states, flows, feedback loops.

**Interaction mode**: SOCRATIC. Claude asks probing questions; user reasons through the answers. Claude corrects misconceptions and fills gaps only after the user has attempted.

Read [references/systems-thinking.md](references/systems-thinking.md) for stock/flow vocabulary, feedback loop patterns, and Socratic probes.

Procedure:

1. **Stock identification** (Socratic). Present the entity list and ask:
   - "Looking at our entities, which ones *accumulate* — where asking 'how many do we have right now?' is a meaningful question?"
   - "Which are static categories vs. things that grow and shrink?"
   
   Let the user identify stocks. Correct if they miss obvious ones or misclassify.

2. **State machine modeling** (Socratic). For the 2-3 most important entities:
   - "What states can a [entity] be in? Walk me through its lifecycle from creation to completion."
   - "What triggers each transition? Who has the authority?"
   - "What happens when a transition fails or gets delayed? Where do things get stuck?"
   
   Build the state machine from the user's answers. Present it back for validation.

3. **Flow identification** (Socratic). For each stock:
   - "What adds to this stock? What removes from it?"
   - "Is the rate constant, or does something control how fast it happens?"
   - "Who decides the rate?"

4. **Feedback loop detection** (Socratic). For each stock-flow pair:
   - "Does the current level of [stock] affect its own inflow or outflow?"
   - "If [stock] doubled overnight, what would change about how fast it grows or shrinks?"
   - "What prevents [stock] from growing forever? What's the natural brake?"
   
   Help the user classify each loop as reinforcing (R) or balancing (B).

5. **Delay mapping** (Socratic):
   - "How long after you take [action] do you see the result?"
   - "What happens if you over-correct during the wait?"

**Deliverable**: State machine diagrams (as text/markdown) for 2-3 key entities + stock-flow descriptions with feedback loops.

**Progress marker**:
```
--- SEPA Progress: [S][E][P] ████████████░ 75% ---
Phase P complete. [X] state machines, [Y] stocks, [Z] feedback loops identified.
Ready for Phase A (Axiology). Continue?
```

## Step 5: Phase A — Axiology (Socratic Mode)

**Goal**: Understand what people in this domain optimize for, argue about, and measure.

**Interaction mode**: SOCRATIC.

Procedure:

1. **Metric inventory** (Socratic):
   - "Based on what we've modeled, what numbers do you think people in this domain check regularly?"
   - "If a leader in this domain opened their dashboard every morning, what would they look at?"
   
   After the user answers, supplement with any major metrics they missed (use web search if needed).

2. **Tradeoff identification** (Socratic):
   - "Can you optimize [metric A] and [metric B] at the same time, or does improving one hurt the other?"
   - "What's the fundamental tension in this domain? Where do smart people disagree?"

3. **Incentive mapping** (guided — this is often politically sensitive):
   - Research and present: "Here's what I've found about how people in this domain are typically rewarded..."
   - Ask: "Does this match your understanding? Where do incentives diverge from stated values?"

4. **Debate register** (Socratic):
   - "What are 3-5 questions that smart people in this domain genuinely disagree about?"
   - "What's the 'open problem' equivalent in this field?"

5. **Connect to structure**:
   - For each metric, trace it back through the process and structure models.
   - "Which stocks does [metric] measure? Which flows does it depend on? Which feedback loops amplify or dampen it?"

**Deliverable**: Priority map (metrics + tradeoffs) + debate register.

**Progress marker**:
```
--- SEPA Progress: [S][E][P][A] ████████████████ 100% ---
All four phases complete! You now have:
- Entity-attribute inventory (the vocabulary)
- Barker sentences + relationships (the structure)
- State machines + stock-flow diagrams (the dynamics)
- Priority map + debate register (the values)
```

## Step 6: Save Artifacts

After any phase (or at the end), if the user wants to save:

1. Ask for a directory path (suggest `~/domains/[domain-name]/`)
2. Create the directory
3. Write these files:

```
[domain-name]/
├── 00-scope.md          # Domain definition, competency questions, subdomains
├── 01-structure.md      # Entity-attribute inventory table
├── 02-enumeration.md    # Barker sentences, failure log, ER relationships
├── 03-process.md        # State machines, stock-flow diagrams, feedback loops
├── 04-axiology.md       # Metrics, tradeoffs, incentives, debate register
└── 05-summary.md        # Integration: how all four layers connect
```

Each file should be self-contained markdown that makes sense on its own.

## Interaction Guidelines

**Pacing**: One phase at a time. Never rush ahead. Check understanding before moving on.

**Guided mode (S, E)**: Claude does the heavy lifting (research, drafting) and the user validates, corrects, extends. This is appropriate because the user doesn't yet know the domain's entities and relationships — they can't discover what they don't know exists.

**Socratic mode (P, A)**: Claude asks questions and the user reasons through answers. Claude only fills gaps after the user has attempted. This works here because by Phase P, the user knows the entities and relationships — now they need to *think* about dynamics and values, which builds deeper understanding than being told.

**When the user is stuck in Socratic mode**: Don't immediately give the answer. Try:
1. Rephrase the question
2. Offer a simpler version or a concrete example from an adjacent domain
3. Give a partial answer and ask them to extend it
4. Only after 2-3 attempts, provide the answer with explanation of *why*

**Domain too small?** If the domain has fewer than 5 entities, it's likely a subdomain. Note this and offer to expand scope.

**Domain too abstract?** If the user names something like "complexity theory" or "epistemology", note that SEPA works best for structured domains with clear entities and processes. Offer to apply it to the *practice* of the field instead (e.g., "how a research group in complexity theory operates" rather than the theory itself).
