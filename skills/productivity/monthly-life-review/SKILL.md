---
name: monthly-life-review
description: "Use for monthly life reviews grounded in real evidence."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [monthly-review, reflection, planning, productivity, second-brain, akiflow]
    related_skills: [weekly-review-planning, second-brain-context, cron-scheduling-automations]
---

# Monthly Life Review

Run a grounded monthly or month-to-date review that helps the user decide what to continue, change, stop, or prioritise. This is a reflective operating review, not a productivity scorecard and not a raw task dump.

## When to Use

- "Run my monthly life review."
- "Test the monthly review now."
- "What happened in my life this month?"
- "What should I focus on next month?"
- A scheduled monthly review fires.

Use `weekly-review-planning` for a narrower weekly reset. This skill owns the broader monthly synthesis and the interactive reflection that follows it. See `references/akiflow-test-run-pattern.md` for the validated Akiflow month-to-date test-run pattern.

## Core Principles

1. **Ground every observation in inspected evidence.** Use Akiflow tasks/events, Obsidian notes, calendar, email, finances, health logs, or other connected sources only when actually available and inspected.
2. **Distinguish facts from interpretations.** Report counts, completed items, overdue items, events, and named projects as observations. Mark broader conclusions as interpretations or hypotheses.
3. **Bound the review honestly.** If the month is still in progress, label it `month-to-date`. Never imply that finances, health, relationships, private conversations, or notes were reviewed unless those sources were actually inspected.
4. **Prefer signal over volume.** Summarise workload, project concentration, recurring friction, waiting states, capacity mismatch, and meaningful progress. Do not paste raw records or large task lists.
5. **Do not carry everything forward.** Recommend one of: do now, schedule realistically, clarify, delegate, convert to waiting, pause, archive, or delete.
6. **End in decisions.** Produce a small number of outcomes and system changes rather than an exhaustive wish list.
7. **Reflect interactively.** For this user, ask one question at a time after the evidence-based summary. Do not present a long questionnaire.

## Procedure

### 1. Establish the review window

- Resolve the user's local timezone before interpreting dates.
- Use the previous calendar month for a completed review.
- Use the first day of the current month through today for a test or in-progress review, explicitly labelled month-to-date.
- Include a short statement of the window and sources inspected.

### 2. Inspect the available systems

Start with the user's authoritative task/calendar system. For Akiflow, inspect tasks and events with completed and overdue state where possible. Then inspect declared second-brain notes and any additional source the user has approved.

Do not infer a complete life picture from task data alone. State coverage gaps at the end.

### 3. Synthesize patterns

Look for:

- meaningful wins and completed commitments
- overdue items and repeated rescheduling
- too many simultaneous projects
- work that is actually waiting or blocked
- vague tasks with no clear next action
- mismatch between planned capacity and scheduled commitments
- recurring event/project workflows worth templating
- learning/content ideas that never became outputs
- lifestyle or energy patterns, only when supported by evidence

Use cautious language: `The data shows...`, `A possible pattern is...`, and `This is a hypothesis because...`.

### 4. Convert friction into choices

For each important open loop, recommend a disposition:

- do now
- reschedule to a realistic date
- clarify the next action
- delegate
- convert to waiting/follow-up
- pause
- archive/delete

Avoid automatically editing tasks, notes, or calendars. Propose changes first; apply only after approval and read changed records back.

### 5. Choose a small focus set

Recommend roughly 3–5 outcomes for the next month or remaining month. Rank by consequence, deadline, dependencies, and real capacity. Explicitly name what is deferred or intentionally stopped.

### 6. Ask one reflective question

After delivering the initial review, ask exactly one high-value question, such as:

- "What are you most proud of completing this month?"
- "Which unfinished item should stop being carried forward?"
- "Which area of life felt most neglected?"
- "What deserves more investment next month?"

Wait for the answer before asking the next question.

## Output Shape

Use a relaxed, medium-length, bullet-oriented format:

```markdown
# Monthly Life Review — <month or month-to-date>

## Scope
- Review window
- Sources inspected
- Coverage gaps

## Wins
- ...

## Observed patterns
- ...

## Friction and open loops
- ...

## Provisional lessons
- Facts first; label interpretations as hypotheses.

## Recommended focus
1. ...
2. ...
3. ...

## Proposed system changes
- ...

**Question:** <one question only>
```

For Discord, collapse tool noise, omit raw IDs and URLs unless useful, and keep the report readable in one message where practical.

## Test-Run Rules

A test run during an incomplete month should:

- say `month-to-date` in the title
- use current evidence rather than pretending to have historical completeness
- include concrete counts when available
- avoid unsupported claims about the user's whole life
- explain which sources were not inspected
- provide provisional recommendations, not permanent conclusions

A good test run can use Akiflow alone, but must say that the result is primarily a workload/calendar review.

## Pitfalls

- Calling August 15 data a complete August review.
- Treating a large task list as proof of poor discipline rather than checking capacity, ambiguity, and waiting states.
- Presenting hypotheses as facts.
- Claiming to have reviewed finance, health, relationship, or note data without inspecting those sources.
- Treating every overdue task as equally urgent.
- Leaving waiting-for-support items as overdue action tasks.
- Carrying every unfinished task into the next month.
- Asking ten reflection questions at once.
- Using a generic motivational tone instead of concrete evidence and relaxed bullets.
- Mutating the source systems during reflection without explicit approval.

## Verification

- [ ] Window is labelled completed-month or month-to-date correctly.
- [ ] Local timezone was used for date interpretation.
- [ ] Every factual count/pattern traces to an inspected source.
- [ ] Interpretations are visibly qualified.
- [ ] Coverage gaps are explicit.
- [ ] Recommendations are limited and capacity-aware.
- [ ] No source was mutated without approval.
- [ ] Exactly one reflective question is asked at the end.
