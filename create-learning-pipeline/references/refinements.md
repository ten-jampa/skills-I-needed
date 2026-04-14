# Refinement Workflows

Five refinement workflows available after initial pipeline generation. These are conversational — the user requests them naturally, not via separate commands.

---

## 1. Stage Deep-Dive

**Trigger phrases**: "expand stage N", "detailed walkthrough for stage N", "day-by-day for stage N", "I'm starting stage N"

**Process**:

1. Read the stage file (`NN-stage-name.md`)
2. Read the current state of tools/resources via WebSearch (they may have changed since generation)
3. Create `detailed-stage-pipeline/` subfolder if it doesn't exist
4. Generate `detailed-stage-pipeline/{stage-name}-walkthrough.md` containing:
   - Day-by-day or session-by-session breakdown
   - Exact commands to run (with code blocks)
   - Specific file/function names to create
   - Common pitfalls with symptoms and fixes
   - Time estimates per sub-task
   - The learning loop applied to each sub-section
   - Decision points marked explicitly
   - Checkboxes for granular tracking
5. Update the stage file to add a wikilink: `> [!tip] Detailed walkthrough available: [[{stage-name}-walkthrough]]`

**Do NOT**: Over-handhold. State objectives and constraints, provide hints for common pitfalls, but leave design decisions to the learner. Prevent 3-hour environment setup rabbit holes, but don't dictate architecture choices.

---

## 2. Job Market Calibration

**Trigger phrases**: "job market check", "calibrate against job postings", "what do companies actually want"

**Process**:

1. Use WebSearch to find 10-15 real job postings at target companies/roles relevant to the pipeline domain
2. Extract required skills and tools from each posting
3. Cross-compare with the pipeline's skill coverage
4. Generate or update `job-market-calibration.md`:

```markdown
| Skill | % of Postings | Companies | Pipeline Coverage |
|-------|---------------|-----------|-------------------|
| ... | X% | A, B, C | Full / Partial / Missing |
```

5. Identify gaps and recommend additions (new stages, expanded sections, or supplementary resources)
6. Update `career-targets.md` Roles table if new roles are discovered

---

## 3. Framework/Tool Audit

**Trigger phrases**: "audit the tools", "are these frameworks still current", "update framework verdicts"

**Process**:

1. For every tool in `framework-verdicts.md`:
   - WebSearch: current version, last release date, maintenance status
   - WebSearch: hiring signal (appears in job postings?)
   - WebSearch: community sentiment (is it recommended or criticized?)
2. Update the verdicts table with current data
3. Flag any tool that has:
   - Not been updated in >12 months
   - Been superseded by a widely-adopted alternative
   - Changed its licensing or pricing model
4. Update the "URLs Verified" date
5. If any tool changes affect stage files, list the changes needed but ask before modifying stage content

---

## 4. Cross-Pollination Check

**Trigger phrases**: "compare with [curriculum/resource]", "cross-pollinate", "what does [X] do better"

**Process**:

1. User provides another curriculum, course syllabus, or learning resource
2. Read or fetch the comparison material
3. Analyze against the current pipeline:
   - What does the comparison do better? (topic ordering, exercises, depth)
   - What should we steal? (specific resources, exercise ideas, stage structure)
   - What should we ignore? (outdated content, different target audience, filler)
4. For each "steal": classify as:
   - **Stage walkthrough addition** — goes into `detailed-stage-pipeline/`
   - **Structural change** — requires modifying stage files or adding a new stage
   - **Resource addition** — goes into `reading-list.md`
5. Present findings. Do NOT overhaul — report clearly and let the user decide what to adopt

---

## 5. Portfolio & Career Review

**Trigger phrases**: "review my portfolio plan", "are the artifacts right", "career review"

**Process**:

1. Read `portfolio-track.md` and `career-targets.md`
2. WebSearch: target role requirements, what hiring managers look for, impressive portfolio examples in this domain
3. Assess each portfolio artifact:
   - Is it the right type? (e.g., blog post when a repo would be more impressive)
   - Is it published in the right place? (e.g., Medium when the community uses dev.to)
   - Does it demonstrate the right skills for the target role?
4. Identify what's missing:
   - Artifacts that would stand out to hiring managers
   - Communities where the learner should be visible
   - Open-source contributions or collaborations
5. Update `portfolio-track.md` with specific, actionable changes
6. Update `career-targets.md` if the assessment reveals new role possibilities or gaps

---

## General Refinement Rules

- **Always verify URLs** when adding new resources during any refinement
- **Preserve existing checkboxes** — if the user has checked items off, don't overwrite their progress
- **Date-stamp changes** — add a `## Changelog` section at the bottom of modified files noting what changed and when
- **Ask before structural changes** — refinements that add/remove/reorder stages need user confirmation
- **Update the overview** — if refinements change the stage count, hours, or timeline, update `00-pipeline-overview.md` to match
