# B1 + B2 ↔ Design Audit — Reconciliation

> **Status:** DRAFT — for owner review. Nothing implemented. Spec not started.
> **Inputs:** `docs/design-audit.md` (APPROVED 2026-08-26), worktrees `spike-webMCP` (B1) and
> `audit-job-data` (B2).
> **Date:** 2026-08-26

---

> **UPDATE 2026-08-26, later same day.** §0 below is superseded: B2's results existed all along
> in a Gemini CLI scratch directory outside the repo, which my search missed. B2 has since been
> **re-run unmodified** and its outputs committed to the repo. B1 is **owner-confirmed VERIFIED**.
> **See §5 for D11–D16 resolutions** and `docs/data-coverage-audit.md` for the measurements.
> §0–§4 are kept as the record of what was known before the run.

---

## 0. Evidence check — read this first

The approval instructed me to reconcile "the completed B1 + B2 results". I searched both
worktrees, the shared repo, all four branches, every session scratchpad and `~/Downloads`.

| Blocker | What actually exists | Status |
|---|---|---|
| **B1** | `spike-webMCP/ARCHITECTURE.md` (verified API contract, dated 2026-08-26) + a working Next.js spike registering `update_test_state` + a Vercel deployment (`.vercel/`, `out/`) | **Partially recorded** |
| **B2** | `audit-job-data/scripts/audit_data_coverage.py` — 649 lines, untracked, complete and runnable | **NOT EXECUTED** |

### B1 — what is and is not recorded

**Recorded:** the runtime target, the API signature, the registration lifecycle, and the HTTPS
context. That is real, dated, and sourced.

**Not recorded:**

1. **No confirmation that the end-to-end chain was observed.** §11.1 requires the full sequence
   — *deploy → open in target ChatGPT browser → agent discovers tool → agent invokes → visible
   UI/state change* — and AGENTS.md requires explicit owner confirmation before it is marked
   passed. The spike is built to demonstrate exactly that (it has a `success` state), but
   nothing on disk says a human watched it fire.
2. **No viewport measurement.** Nothing anywhere records the ChatGPT built-in browser's actual
   width or height. Approval decision 6 — "use B1's real ChatGPT viewport information for the
   responsive target" — **cannot be executed against existing evidence.**

### B2 — not executed

`audit_data_coverage.py` fetches JobsCollider, Arbeitnow and Jobicy, computes per-field
coverage, matches titles against a hard-coded `ARCHETYPES` map built from §7.3, and writes
`audit_summary.json` plus per-source caches. **None of those output files exist**, in that
worktree or anywhere on this machine. The script has been written but never run — or run
without its output kept.

Approval decision 5 — "use the completed B2 audit to choose the real persona, archetypes and
star constraint" — **has no input to work from.**

I have not invented substitute numbers. Everything below separates what B1's real contract
settles from what remains genuinely blocked.

---

## 1. What B1 settles — and its design consequences

The verified contract has more design consequence than expected. Four items change the audit.

### 1.1 Tool registration is component-scoped — so scope becomes a contract

```ts
document.modelContext.registerTool(tool, options)   // imperative, per tool
// options.signal: aborting it unregisters the tool (used on React unmount)
```

Tools are registered from React effects and **unregistered when the owning component
unmounts**. That makes "which component owns which tool" a P1 decision, not a detail:

> If `debug_constraints` were registered by the detail rail, then closing the rail would
> silently remove a domain capability from the agent. The UI and the tools would no longer
> have equal reach — the exact P1 violation.

**Consequence:** every domain tool registers **once at the app root**, over the shared store,
independent of what is visible. This confirms `lib/domain/store.ts` as the single hinge
(audit §18.2) and adds a rule that belongs in spec.md.

### 1.2 The spike's status machine supersedes the audit's B-1 proposal

The audit (B-1) proposed four agent states. The spike, written against the real runtime, has
five and they are better:

```ts
"checking" | "waiting" | "success" | "unsupported" | "error"
```

`checking` (feature detection in flight) and `error` (registration rejected) are states the
audit missed and the real API produces. The spike also already carries `aria-live="polite"`.

**Consequence:** `AgentStatus` adopts the spike's machine verbatim, mapped to product copy —
this is proven code, not a design guess. Supersedes the audit's four-state sketch.

### 1.3 "Agent mode unavailable" is a first-class state with *several distinct causes*

ARCHITECTURE.md records three separate ways WebMCP is absent on a supported product:

- the model is **GPT-5.6 Luna** (WebMCP disabled),
- the workspace is **Enterprise or Edu** (site tools unavailable),
- rollout has not reached the user — or they are simply in an ordinary browser.

The audit treated S2 as one notice. It is not: from `document.modelContext === undefined` these
causes are **indistinguishable at runtime**. The honest notice therefore states the condition
and lists the requirements, and must not assert a cause it cannot detect — P6 forbids faking
agent state in either direction.

**Consequence:** S2 gets real copy naming the requirements (ChatGPT desktop app · built-in
browser · Sol or Terra · non-Enterprise/Edu), never a diagnosis. Raises S2 from an edge case to
a designed screen, exactly as B-1 required.

### 1.4 `inputSchema` + structured `execute` return → the P3/P1 hinge is the payload

Tools take a JSON Schema input and return a structured object. Combined with B-3/B-4:

> If `debug_constraints` returns `{ unlocked: 23 }`, the agent has a number it cannot cite —
> P3's stated violation, reached through the tool surface instead of the UI.

**Consequence, and the strongest single finding of this reconciliation:** every tool that
returns a count must return **the enumerated evidence behind it**, and that payload must be the
**same selector output** the UI renders in `UnlockEvidenceList`. One selector, two consumers.
That is P1 and P3 satisfied by the same piece of code, and it is a contract for spec.md.

It also reinforces B-8: a data-driven constraint list in the UI is the same list that becomes
the tool's `inputSchema` enum. Two reasons for one decision.

### 1.5 Responsive risk — reduced, not resolved

The target is the **ChatGPT desktop app's built-in browser**, not a phone. The audit's H-1
ranked a phone tier as the top delivery risk; that ranking was too pessimistic.

But the built-in browser is a panel inside an app window, so it is **narrower than the desktop
viewport the mockup assumes (1440 px)**. How much narrower is unmeasured. I will not guess a
breakpoint.

**Consequence:** H-1 stands, re-scoped — the question is no longer "does it work on a phone"
but "what is the panel's real width, and does the 252 / 1fr / 372 three-column shell survive
it". One measurement answers it. Until then the design targets a fluid centre column with both
rails collapsible, which is correct under any plausible answer.

---

## 2. Where the approved decisions collide with missing evidence

| Approved | Depends on | Can proceed? |
|---|---|---|
| B-1 agent state redefined | B1 ✔ | **Yes** — improved by §1.2 / §1.3 |
| B-2 drop the reachability scalar | nothing | **Yes** |
| B-3 provenance block | B2 (which sources, which fields are actually populated) | **Design yes, content no** |
| B-4 enumerable unlock list | B1 ✔ | **Yes** — §1.4 strengthens it |
| B-5 BLOCKS arithmetic | — | **Moot** — the ledger was cut (§17.2). The overlap-semantics rule still binds any count the debugger shows. |
| B-6 delete invented durations | nothing | **Yes** |
| B-7 Constraint-only default | **B2** — whether skill evidence survives at all | **Design yes, decision no** |
| B-8 data-driven constraint strip | **B2** — which constraint is the star | **Design yes, choice no** |
| B-9 remove avatar | nothing | **Yes** |
| B-10 re-cast persona/archetypes | **B2** — blocked outright | **No** |
| 4 px spacing | nothing | **Yes** |
| Responsive target | **B1 viewport measurement** — not captured | **No** |

Seven of twelve proceed now. Five are gated on two missing measurements.

**Note on B-5:** cutting the ledger removed the screen where 101 ≠ 87 appeared, but not the
defect. Any count the per-opportunity debugger shows inherits the same rule — state whether
counts overlap, or make them a non-overlapping decomposition. Carried forward as a spec item,
not closed.

---

## 3. Decisions that must enter `docs/spec.md`

### 3.1 Resolvable now — B1 settles them or they need no measurement

| # | Decision | Source |
|---|---|---|
| D1 | **Tool registration scope.** All domain tools register once at the app root over the shared store; never per-panel. Unmount-abort applies to the app, not to views. | §1.1, P1 |
| D2 | **Agent status contract.** The five spike states, plus the product copy for each. `unsupported` states requirements, never a diagnosed cause. | §1.2, §1.3, P6 |
| D3 | **Every count-returning tool returns its evidence.** Tool payload and UI list are one selector. Defines the return shape of `debug_constraints` and `search_opportunities`. | §1.4, **P3 + P1** |
| D4 | **Which ~3 tools ship.** S3 prefers 3 done well over 5 half-done. The approved design needs `set_candidate_profile`, `search_opportunities`, `debug_constraints`; D3 arguably absorbs `inspect_unlock` into `debug_constraints`' return payload. `compare_career_worlds` has no screen in the approved direction. **Owner decision.** | S3, §7.5 |
| D5 | **Constraint model schema.** B-8 makes the strip data-driven, so the constraint shape becomes a contract: kind, current value, candidate values, locked flag, simulated value. It is simultaneously the UI model and the tool `inputSchema`. | §1.4, B-8 |
| D6 | **What replaces the reachability scalar.** B-2 deleted the number; the reason-sentence takes its slot. Its *generation rule* is a P3 contract, not copywriting — which facts compose it, in what order, from what evidence. | B-2, P2, P3 |
| D7 | **Count semantics.** Any displayed count states whether it overlaps with others, or is a non-overlapping decomposition. | B-5 carried forward, P3 |
| D8 | **Provenance fields.** Source name, original URL, posting date, cache age — required on every rendered opportunity; a job missing them is not rendered. | B-3, P7 |
| D9 | **Simulation is client-side and reversible.** The approved design has no Keep/Revert (that was 1a); the refined canvas reverts via the constraint strip. Whether a simulation can be committed at all in v1, and what "committed" would mean without persistence (P5), is undecided. **Owner decision.** | §7.2, P5 |
| D10 | **Single-screen navigation frozen.** Intake as first-run overlay, evidence and source as in-rail expansion, no routes, no modals. | audit §8, M-1 |

**Not spec material** — §13 classes these as implementation details that proceed without
approval: the type scale, the amber ramp values, the five text alphas, radii, loading and empty
states, microcopy, motion timings.

### 3.2 Blocked on B2

| # | Decision | Why it cannot be taken |
|---|---|---|
| D11 | **Persona and archetype family** (B-10) | Needs `archetype_breakdown` — which of §7.3's archetypes have real job volume |
| D12 | **Star constraint** (B-8) | §7.2's rule is explicit: pick the constraint with sufficient real data and the most convincing counterfactual. Needs per-field coverage %. |
| D13 | **Do Skill Unlocks ship?** (B-7) | S1 declares them degradable. Needs description coverage to judge whether evidence extraction can clear P3. |
| D14 | **Is the pay trade-off showable?** | Needs structured-salary coverage on both the before and after sets. Without it, C2's `median pay €71k · +4%` stays deleted. |
| D15 | **Primary source, and the "showing N of M" framing** (M-6) | Needs totals and archetype-mapped counts per source (RK7). |

### 3.3 Blocked on a B1 viewport measurement

| # | Decision | Why |
|---|---|---|
| D16 | **Responsive tiers** (H-1) | Whether the 252 / 1fr / 372 shell survives the built-in browser's real width; whether a sub-840 tier is needed at all, or a phone tier is out of scope. One number decides all three. |

---

## 4. What I recommend next

1. **Run B2.** It is agent-runnable (AGENTS.md), the script is complete, and it unblocks D11–D15
   — five of the six remaining decisions. It fetches only public documented APIs server-side,
   exactly as §7.1 approves. Say the word and I run it and write `docs/data-coverage-audit.md`.
2. **Capture the viewport during your next B1 pass.** `window.innerWidth / innerHeight` printed
   on the spike page, read once in the ChatGPT built-in browser. Unblocks D16. The spike is
   already deployed; this is a two-line change to a page that exists.
3. **Confirm B1 formally.** §11.1 needs your explicit word that you watched the chain complete.
   Until then Track A stays blocked regardless of what this document settles.
4. **Answer D4 and D9** — the two owner decisions in §3.1 that no measurement will resolve.

Spec not started, per instruction.

---

## 5. D11–D16 after the B2 run and the B1 confirmation

B1 is owner-confirmed VERIFIED (recorded in `AGENTS.md`, not in the frozen constitution).
B2 executed — full measurements in `docs/data-coverage-audit.md`.

| # | Decision | Status | Resolution |
|---|---|---|---|
| **D11** | Persona and archetype family | **Resolvable** | 12 archetypes in two tiers (core 570 jobs / supported 110); drop Product Operations and Project Coordinator as *targets*. Persona: mid-level project/operations coordinator. **Owner sign-off needed.** |
| **D12** | Star constraint | **Resolvable** | **Seniority.** 88.9 % coverage (98.6 % without Arbeitnow), three bands ≥150 jobs, `mid → mid+senior = 154 → 312 (+158)`. Salary floor secondary at 44.7 %. **Owner sign-off needed.** |
| **D13** | Do Skill Unlocks ship? | **STILL OPEN** | B2 measured field coverage, not extraction quality. Descriptions are ~100 % present at ~7 k chars, so the raw material exists; whether *required* vs *preferred* vs *mentioned* can be separated deterministically is untested. RK3 fully open. Needs its own spike. |
| **D14** | Is the pay trade-off showable? | **Resolvable — yes, with a stated denominator** | 44.7 % of the pool has structured salary, and coverage is known per seniority band (mid 45 %, senior 58 %). Showable only alongside its coverage, per P3. |
| **D15** | Primary source and "showing N of M" | **Resolvable** | JobsCollider primary (71 % of pool) + Jobicy secondary. **Recommend dropping Arbeitnow** — 68 archetype jobs, 0 % salary, unusable seniority; dropping it lifts seniority coverage to 98.6 %. This is a §7.1 scope change → **explicit owner approval required.** |
| **D16** | Responsive tiers | **STILL OPEN** | The spike now renders `innerWidth × innerHeight @ dpr` on the page. Needs a redeploy and one reading in the ChatGPT built-in browser. Two minutes of owner time. |

### What B2 forces back into the design

The audit approved B-8 (make the constraint strip data-driven) as a precaution. B2 turned it
into a requirement:

> The approved signature moment — `Location · Remote only → Flexible · +23` — is built on the
> **least supported variable in the data**. Its ceiling is ~63 jobs, all from the source we
> recommend dropping. Seniority replaces it: `mid → mid + senior, +158`.

Consequences for `docs/design-audit.md`, to be applied when the spec is written:

1. **B-10 resolves** — persona and roles re-cast to the measured archetype family.
2. **B-8 resolves** — seniority is the star; the strip stays data-driven so salary can join it.
3. **The orbit's node data changes shape.** `rSim` was a per-node literal for a location unlock;
   it becomes a computed re-filter over a seniority band.
4. **A new element is needed that the mockup never had:** the taxonomy expansion (8 → 154) is
   not an unlock and must not be counted as one. It is the "what you'd never have searched for"
   moment, and it is the strongest number the audit produced. It needs its own treatment,
   distinct from `UnlockCard`.
5. **D14's denominator becomes visible copy.** Any pay figure carries "computed over N of M
   postings that publish salary".
