# Agent Operating Rules

Project: **Jorbit** — a visual, specialized opportunity engine that an external AI agent
operates through WebMCP. Repo to be renamed `jorbit-webmcp`.

This repository may be developed by multiple AI agents concurrently.

## Sources of truth

Read in this order. Higher level wins on conflict.

```text
Constitution > Spec > Architecture > Plan > Tasks
```

1. `docs/constitution.md` — **v0.3 APPROVED / FROZEN**. Do not edit without owner approval.
2. `docs/spec.md` — not written yet
3. `ARCHITECTURE.md` — not written yet
4. `docs/plan.md` — not written yet
5. `docs/tasks.md` — not written yet

Read the documentation before implementing anything.

## Governance

Mirrors `docs/constitution.md` §13.

- **No core behavior, contract, scope change or architectural decision is implemented unless
  documented at the appropriate level. Implementation details that do not alter those
  contracts do not require owner approval.**
  Loading states, empty states, retries, microcopy and minor visual details are
  implementation details — just do them.
- Scope changes and core architecture changes require explicit owner approval.
- Volatile technical facts (WebMCP API signature, browser versions, data-access mechanism)
  live in `ARCHITECTURE.md`, never in the constitution.

## Git

- Never work directly on `main`.
- Never merge into `main` without approval.
- Do not modify another agent's worktree.
- Do not add yourself as contributor or committer.

## Hard product rules

Violating any of these is a constitution violation, not a style preference. Full text and
rationale in `docs/constitution.md` §5 and §8.

- **No embedded chatbot, copilot, prompt box or Jorbit-owned LLM/agent.** The agent is
  external and talks to Jorbit through WebMCP.
- **No scraping.** Public, documented job APIs only, consumed server-side, with source and
  original link cited.
- **No external side effects.** No auto-apply, no form submission, no emails, no messaging
  recruiters. Private generation is fine.
- **No number without reconstructible evidence.** If Jorbit cannot enumerate and justify the
  jobs behind an unlock count, it does not display the count.
- **No own CV parser.** The external agent interprets the CV and calls `set_candidate_profile`.
- **Domain actions go through WebMCP**, sharing state and logic with the UI. Purely visual
  interactions (zoom, collapse, layout) do not need tools.

## Current stage

Planning. Constitution frozen. Design audit approved (`docs/design-audit.md`). B1 verified,
B2 executed. `spec.md` is next and **not yet started — awaiting owner approval to write it**.

Two execution blockers must clear before the spec closes (`docs/constitution.md` §11):

| Blocker | Status | Owner |
|---|---|---|
| **B1 — WebMCP vertical slice** end-to-end in the target ChatGPT browser | **VERIFIED 2026-08-26** — owner-confirmed end-to-end in the target browser. Contract in `spike-webMCP/ARCHITECTURE.md`. | Human — needs a real browser |
| **B2 — Data Coverage Audit** across JobsCollider, Arbeitnow, Jobicy | **EXECUTED 2026-08-26** — results in `docs/data-coverage-audit.md`, raw output in `docs/data/`. | Agent-runnable |

Do not mark either as passed without explicit owner confirmation.

This table is the blocker registry. `docs/constitution.md` §11 is frozen and still reads
NOT VERIFIED / NOT EXECUTED by design — it records the state at freeze time, not current status.

**One B1 sub-measurement is still outstanding:** the target browser's real viewport. The spike
now renders it on the page (`spike-webMCP/app/page.tsx`); it needs a redeploy and one reading in
the ChatGPT built-in browser. Until then the responsive target (D16) stays undecided.

**Track A — Engineering** was blocked by B1: job API integration, O\*NET work, production UI,
Skill Unlock engine, any WebMCP-dependent production logic. B1 is now verified — but production
UI remains gated on owner approval of `docs/spec.md`, which is not written.

**Track B — Design** may proceed in parallel: visual identity, design system, UX exploration,
mockups, interactive prototypes, Career Orbit / Constraint Debugger / Opportunity Unlock
concepts, motion.

## Missing documentation

If required documentation does not exist yet, do not start implementation. Help define and
create it first, one stage at a time, waiting for owner review between stages.
