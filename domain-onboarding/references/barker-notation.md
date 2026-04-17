# Barker ER Notation Reference

## Table of Contents
- Barker Sentence Template
- The Four Commitments
- Failure Types and Question Generation
- Entity vs Attribute Test
- Attribute Markers
- Many-to-Many Resolution
- Class Hierarchy (Subtypes)
- Example: VC Fund Domain

## Barker Sentence Template

Every relationship is expressed as TWO sentences (one from each direction):

```
Each [ENTITY A] (must | may) be [RELATIONSHIP] (one and only one | one or more) [ENTITY B]
Each [ENTITY B] (must | may) be [RELATIONSHIP] (one and only one | one or more) [ENTITY A]
```

Rules:
- Relationship names are **prepositions**, not verbs. The implied verb is always "to be"
- `must` = mandatory (every instance has this relationship)
- `may` = optional (some instances lack it)
- `one and only one` = singular
- `one or more` = plural

Example:
```
Each FUND must be managed by one and only one GP_ENTITY
Each GP_ENTITY must be managing one or more FUND
```

## The Four Commitments

Every Barker sentence forces four knowledge claims:

| # | Commitment | What you're claiming |
|---|-----------|---------------------|
| 1 | **Existence** | Entity A and Entity B are distinct things |
| 2 | **Connection** | A named relationship exists between them |
| 3 | **Optionality** | The connection is necessary (must) or contingent (may) |
| 4 | **Cardinality** | The connection is singular (one and only one) or plural (one or more) |

## Failure Types and Question Generation

When you cannot complete a Barker sentence, the failure type tells you exactly what to ask:

| Failure | Symptom | Question to ask |
|---------|---------|-----------------|
| **Existence** | "Is X a separate thing or a property of Y?" | "Do people track [X] independently? Does it have its own ID?" |
| **Connection** | "I can't name how X relates to Y" | "How does [X] relate to [Y]? Is there a direct link?" |
| **Optionality** | "I don't know if every X must have a Y" | "Can a [X] exist without a [Y]? Are there examples?" |
| **Cardinality** | "Can X have many Ys or just one?" | "Can a [X] connect to multiple [Y]s? What's the maximum?" |

These failures are precise, typed questions — far more productive than "tell me about your business."

## Entity vs Attribute Test (Noy & McGuinness)

For each noun, ask three questions:
1. Does it have its own identity?
2. Could there be multiple instances?
3. Would you store attributes about it?

**Yes to all three** → candidate entity
**No to any** → likely an attribute of another entity

Edge case: if something is "just an attribute" but has 10+ possible values with their own properties, promote it to an entity (e.g., "Country" might start as an attribute of Company but deserves entity status if you track country-level data).

## Attribute Markers

For each entity's attributes, mark them:
- `#` — Unique identifier (picks out exactly one instance)
- `*` — Mandatory (every instance must have this)
- `o` — Optional (some instances may lack this)

Example:
```
COMPANY
  # company_id
  * name
  * sector
  o website
  o founding_year
```

## Many-to-Many Resolution

When both sides of a relationship are "one or more", you need an **intersection entity**.

Steps:
1. Identify the many-to-many: "Each FUND may be investing_in one or more COMPANY; Each COMPANY may be funded_by one or more FUND"
2. Create intersection entity: INVESTMENT
3. Identify intersection attributes (these are often the most business-relevant): amount, date, round, ownership_percentage
4. Rewrite as two one-to-many relationships through the intersection

## Class Hierarchy (Subtypes)

When entities share a common parent type:
- Identify shared attributes (belong to the supertype)
- Identify distinguishing attributes (belong to the subtype)
- Ask: "Is this a complete partition? Can something be in multiple subtypes?"

Example:
```
INVESTOR (supertype)
  ├── VC_FUND (subtype: has vintage_year, fund_size)
  ├── ANGEL (subtype: has personal_net_worth)
  └── CORPORATE_INVESTOR (subtype: has parent_company)
```

## Example: VC Fund Domain

Entities: FUND, GP_ENTITY, LP, PORTFOLIO_COMPANY, DEAL, PARTNER

Sample Barker sentences:
```
Each FUND must be managed by one and only one GP_ENTITY
Each GP_ENTITY may be managing one or more FUND

Each LP may be committed to one or more FUND
Each FUND must be backed by one or more LP

Each DEAL must be investing in one and only one PORTFOLIO_COMPANY
Each PORTFOLIO_COMPANY may be the subject of one or more DEAL

Each DEAL must be led by one and only one PARTNER
Each PARTNER may be leading one or more DEAL
```

Intersection entity example:
- LP_COMMITMENT (between LP and FUND): commitment_amount, commitment_date, called_amount, distribution_amount
