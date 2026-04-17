# Systems Thinking Reference (Meadows)

## Table of Contents
- Core Vocabulary
- Stock Identification
- Flow Identification
- Feedback Loops
- Delays
- State Machine Modeling
- Leverage Points
- Socratic Probes for Process Phase

## Core Vocabulary

| Concept | Definition | Example |
|---------|-----------|---------|
| **Stock** | Something that accumulates or depletes over time | Pipeline deals, AUM, headcount |
| **Flow** | Rate at which a stock changes (inflow or outflow) | Deal sourcing rate, capital deployment rate |
| **Feedback loop** | Causal chain where a stock's level influences its own flows | Reputation → deal flow → returns → reputation |
| **Delay** | Time gap between cause and effect | Investment → exit → realized returns (5-10 years) |
| **Leverage point** | Place where small change produces large effect | Information flows, rules of the system |

## Stock Identification

Not every entity is a stock. Apply this test:
- **Is a stock**: Things that accumulate/deplete, have quantity, change over time (pipeline deals, capital committed, headcount, inventory)
- **Not a stock**: Categories, labels, static reference data (sector, country, deal type)

For each stock, ask:
1. What is the current level? (Can it be measured?)
2. What adds to it? (Inflows)
3. What removes from it? (Outflows)
4. What is the natural equilibrium, if any?

## Flow Identification

For each stock, name the flows:

```
INFLOWS → [STOCK] → OUTFLOWS

deal_sourcing_rate → [PIPELINE_DEALS] → deal_closed_rate, deal_passed_rate
hiring_rate → [HEADCOUNT] → attrition_rate, firing_rate
capital_calls → [DEPLOYED_CAPITAL] → distributions, write_offs
```

For each flow, identify:
- **What controls the rate?** (decisions, policies, external factors)
- **Is the rate constant, variable, or event-driven?**
- **Who has authority over it?**

## Feedback Loops

### Reinforcing Loops (R)
More of X produces more of X. These drive growth or collapse.

Pattern: Stock A ↑ → causes → Flow B ↑ → increases → Stock A ↑

Example:
```
Brand reputation ↑ → attracts better deal flow ↑ → better returns ↑ → brand reputation ↑
```

Warning sign: "The rich get richer" or "vicious cycle" dynamics.

### Balancing Loops (B)
More of X produces less of X. These drive toward equilibrium.

Pattern: Stock A ↑ → causes → Flow B ↑ → decreases → Stock A ↓

Example:
```
Workload ↑ → forces selectivity ↑ → fewer deals accepted → workload ↓
```

Warning sign: "We can't grow past this point" or "something always pulls us back."

### Detection Questions (Socratic)
- "If [stock] doubled overnight, what would change about how fast it grows or shrinks?"
- "Does having more of [X] make it easier or harder to get even more?"
- "What keeps [X] from growing/shrinking forever?"
- "When [X] gets too high, what happens that brings it back down?"

## Delays

Delays make systems hard to manage because you cannot see the results of your decisions.

For each feedback loop, estimate:
- **Short delay** (days-weeks): Hiring → onboarding → productivity
- **Medium delay** (months): Marketing → pipeline → revenue
- **Long delay** (years): Investment → company growth → exit → realized returns

Key question: "How long after you take action X do you see the result? What happens if you over-correct during the wait?"

## State Machine Modeling

For entities that change state over time:

1. **List all states** (use past conversations, documents, or domain expert input)
2. **Map transitions**: What event triggers moving from state A to state B?
3. **Authority**: Who can trigger each transition?
4. **Information**: What data is created or consumed at each transition?

Template:
```
ENTITY: [name]
STATES: state_1 → state_2 → state_3 → ... → terminal_state

TRANSITIONS:
  state_1 → state_2:
    Trigger: [event]
    Authority: [who/what]
    Creates: [data/artifact]
    Consumes: [data/artifact]
```

Probes:
- "What states can a [entity] be in?"
- "What causes it to move from [state A] to [state B]?"
- "What happens when a transition fails or gets delayed?"
- "Where do things get stuck? Why?"

## Leverage Points (Meadows, ranked by increasing effectiveness)

12. Constants, parameters, numbers (subsidies, taxes, standards)
11. Buffer sizes (stabilizing stocks)
10. Stock-and-flow structures (physical systems)
9. Delays (relative to rate of change)
8. Balancing feedback loops (strength relative to impacts)
7. Reinforcing feedback loops (driving growth)
6. Information flows (who has access to what)
5. Rules of the system (incentives, constraints, punishments)
4. Power to add/change/evolve system structure
3. Goals of the system
2. Mindset or paradigm behind the system
1. Power to transcend paradigms

Use this during Phase A (Axiology) to identify where change has the most impact.

## Socratic Probes for Process Phase

These questions force the learner to reason about dynamics rather than passively receiving information:

**Stock probes:**
- "You said [entity] exists in the domain. Does it accumulate? Can there be more or fewer of them over time?"
- "If I asked you 'how many [entity] do you have right now?', would that be a meaningful question?"

**Flow probes:**
- "What causes new [stock] to appear? What makes existing ones disappear?"
- "Is the rate constant or does something control how fast it happens?"

**Feedback probes:**
- "You identified [flow] as an inflow to [stock]. Does the current level of [stock] affect [flow]? How?"
- "What prevents [stock] from growing without limit?"

**Delay probes:**
- "You said [action] causes [result]. How long is the gap? What happens during the wait?"
- "If you could see the result of [action] instantly, would you do anything differently?"

**Failure mode probes:**
- "What happens when this transition fails or gets delayed?"
- "Where do things get stuck between states? What's the typical reason?"
- "What's the worst thing that happens if [stock] gets too high? Too low?"
