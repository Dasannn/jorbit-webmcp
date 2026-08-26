# Design Audit — Claude Design mockup

> **Status:** **APPROVED by owner 2026-08-26.** Non-binding on contracts; feeds `docs/spec.md`.
>
> Owner decisions on §17:
> 1. Direction = refined (A's orbit + C's clarity). **Direction 1b dropped entirely.**
> 2. Full Constraint Ledger (1c) **not built for v1**; the per-opportunity debugger is the v1 path.
> 3. 4 px spacing system **approved** (deviation from Nocturne's 0.7× scale recorded).
> 4. **All blocking changes B-1 … B-10 approved.**
> 5. Persona, archetypes and star constraint to be chosen from the B2 Data Coverage Audit.
> 6. Responsive target to be set from B1's real ChatGPT viewport measurement.
>
> Production UI is **not** authorised. See `docs/b1-b2-reconciliation.md` for what B1 and B2
> actually deliver against decisions 5 and 6.
> **Scope:** Track B (Design). Does not alter any contract, so it does not require owner
> approval to exist — but nothing here is implemented until the owner approves.
> **Subject:** `design/career-navigation-directions/` (read-only reference; never edited).
> **Audited against:** `docs/constitution.md` v0.3 FROZEN, `AGENTS.md`.
> **Date:** 2026-08-26

Written in English because it seeds `docs/spec.md`, component names and UI copy, all of
which R11 requires in English.

---

## 0. What the mockup actually contains

```text
design/career-navigation-directions/
├── Jorbit Design Directions.dc.html   50 KB — 3 competing design languages (A / B / C)
├── Jorbit.dc.html                     33 KB — the refined direction, interactive, 3 states
├── support.js                         69 KB — Claude Design canvas runtime (not ours)
└── _ds/nocturne-…/                    "Nocturne" design system
    ├── styles.css                     294 lines — tokens + component layer
    ├── readme.md                      the system's written guidance
    ├── theme.json / _ds_manifest.json machine-readable token record
    └── _ds_bundle.js
```

**First finding, mechanical:** `_ds/…/readme.md` documents 15 files — `foundations/type.html`,
`components/buttons.html`, `templates/landing/`, `theme.json`, `thumbnail.html`,
`assets/photo.jpg` — **none of which were exported into this folder**. `_ds_manifest.json`
lists them too. Only `styles.css` survived. So the "design system" we received is a token
sheet plus a prose guide, not a component library. That is fine — we want the tokens — but it
kills any plan to vendor Nocturne's component layer wholesale.

**Second finding, mechanical:** the mockups barely consume their own token layer.

| File | `var(--…)` uses | Hard-coded hex literals |
|---|---:|---:|
| `Jorbit Design Directions.dc.html` | 84 | 153 |
| `Jorbit.dc.html` | **2** | **70** |

The refined direction — the one closest to what we build — is effectively **detached from
Nocturne**. It re-states ramp steps as raw hex (`#b5abfc` instead of `--color-accent-400`) and
invents grounds that exist in no token (`#141621`, `#1a1c2b`, `#0e0f17`). Whatever we port,
we re-tokenise from scratch.

---

## 1. Screens and UX flow

### 1.1 What exists

`Jorbit Design Directions.dc.html` — one canvas turn, three 1340×840 boards, each frozen on the
same signature moment (*Location: Remote only → Flexible has just been simulated*), each with a
340px annotation panel stating metaphor / layout / opportunities / blocked / unlock / simulation
/ agent / strengths / risks.

| Board | Language | Core idea | Stated risk (theirs) |
|---|---|---|---|
| **1a** | Orbital / Spatial | Gravity well. Radius = effort-to-reach. Identity rail left, detail rail right, constraints as a bottom bar. | Crowds past ~40 nodes; needs label collision logic |
| **1b** | Radar / Constellation | Instrument. A rotating sweep "discovers" bodies; shared skills wire them into named clusters. Scan log right. | Radar implies live data that does not exist; sweep is decorative; three columns compete |
| **1c** | Analytical / Constraint-first | Stack trace for a career. 2/3 constraint ledger table, 1/3 live orbit panel. | Reads as an admin table; the wow depends entirely on the orbit panel |

`Jorbit.dc.html` — the resolution: **A's orbital canvas carrying C's constraint clarity**. One
1440×900 screen, three states driven by `state = { sim, sel }`:

| State | `sim` | `sel` | Right rail shows |
|---|---|---|---|
| **1 · Career Orbit** | false | null | `Closest to your boundary` — 4-row list |
| **2 · Selected opportunity** | false | `dsp` | Detail panel + Constraint debugger |
| **3 · Simulation & unlock** | true | `dsp` | Detail + debugger resolved + Opportunity unlock card |

Transitions are real (`setState`), not screenshots: boundary radius animates 262 → 318 over
1.1 s, gated nodes travel `r` → `rSim` inward, boundary hue swaps blurple → amber, the previous
boundary persists as a dashed ghost ring, counters roll 31 → 54.

### 1.2 The flow the mockup implies

```text
Career Orbit (browse)
      │  click a body  /  click a row in "Closest to your boundary"
      ▼
Selected opportunity  →  Constraint debugger lists what holds it out
      │  "Simulate flexible location"  /  constraint strip: Remote only → Flexible
      ▼
Simulation active  →  boundary re-inflates, ghost ring remains, Opportunity unlock card
      │  Close  /  (Keep · Revert exist only in board 1a)
      ▼
back to Career Orbit
```

Three of the four screens the product actually needs are missing from every board.

### 1.3 Screens that do not exist and must

| # | Screen | Why it is mandatory | Source |
|---|---|---|---|
| S0 | **Entry / landing** | Needs to state the thesis in one line before any data exists. §4.1's 60-second clock starts here. | §4.1 |
| S1 | **Profile intake** | The manual fallback form — current role, skills, experience, location, remote preference, salary. Not optional. | §7.5, P6 |
| S2 | **Agent-mode unavailable** | "Sin WebMCP disponible, la app **dice claramente** que el modo agente no está disponible en ese navegador." No board shows this. | **P6** |
| S3 | **Evidence drill-down** | The unlock card says "23 opportunities entered your orbit". P3 requires we can enumerate all 23 and cite each. No screen enumerates anything. | **P3** |
| S4 | **Opportunity source & original link** | Every posting must carry source, original link, and cache age. Appears on **zero** boards. | **P7** |
| S5 | **Empty / cold start** | No profile yet → what does the orbit render? | impl. detail |
| S6 | **Narrow viewport** | R2's target is the ChatGPT in-app browser. Nothing below 1340px exists. | **R2** |
| S7 | **Degraded mode** | Skill Unlocks are declared degradable (S1, §7.2). No board shows the screen with the SQL row absent. | §7.2, S1 |

---

## 2. Typography

**Loaded:** Inter 300/400/500/600 + JetBrains Mono 400/500 (directions); Inter 300/400/500
(refined), `font-feature-settings: "tnum" 1, "ss01" 1`.

**Nocturne says:** Inter over Inter, heading weight 500, *"Do not bolden headings past their 500
weight — hierarchy here is size and space."*

### Findings

- **No type scale exists.** Distinct `font:` sizes in the directions file: 9, 9.5, 10, 10.5,
  11, 11.5, 12, 12.5, 13, 14, 17, 20, 22, 30, 34, 42 px — **16 steps**. Refined: 12, 12.5, 13,
  13.5, 14, 15, 19, 20, 24, 26, 30, 44 — **12 steps**. Every one is an inline literal.
- **Half-pixel sizes** (9.5, 10.5, 11.5, 12.5, 13.5) buy nothing and rasterise inconsistently
  across the engines we must support.
- **Weight 300 is used for every large number** (`font:300 44px`) — the counters, the stat
  tiles. On a dark ground Inter 300 at display size thins badly. This is the mockup's most
  visible type liability and it appears on the single most important element in the product.
- **Weight 600 is loaded in the directions file and never used.** Dead payload.
- **JetBrains Mono, `letter-spacing: .14em`, ALL CAPS, 9–10.5 px, at 22–35 % opacity** is the
  directions file's default for every micro-label: `CENTRE OF ORBIT`, `SELECTED BODY`,
  `WHAT MOVED IT INWARD`, `SWEEP 04 · 12s AGO`, `REACH`, `GAP LEFT`, `BLOCKS`, `SIM`, `LOCKED`.
  Aimed at §3's **non-technical primary user**, this is register failure, not just decoration.
- **The refined direction already fixed this** — it drops mono from user-facing copy almost
  entirely and moves labels to Inter 12.5–13 px sentence case. That correction is the single
  best type decision in the mockup and must be preserved.

### Proposed scale (replaces all 16–28 ad-hoc steps)

| Token | px / line | Weight | Use |
|---|---|---|---|
| `display` | 44 / 1.0 | **400** (not 300) | The reachable counter, only |
| `stat` | 26 / 1.0 | 400 | Detail-panel stats |
| `title` | 24 / 1.25 | 500 | Selected opportunity title |
| `heading` | 15 / 1.3 | 500 | Rail and panel headings |
| `body` | 13 / 1.55 | 400 | All prose |
| `label` | 12 / 1.4 | 400 | Meta, captions, node meta |
| `micro` | 11 / 1.3 | 500 | Badges only (SIM, LIVE) |

Seven steps. `tnum` stays on globally — the counters animate and must not reflow.

---

## 3. Color

### 3.1 Inherited from Nocturne

Ground `#161826`, text `#e9e9ed`, accent `#9184d9` (blurple), plus 9-step OKLCH ramps for
neutral / accent / accent-2, `--color-section*` for deck fills, three shadows.
`--color-accent-2-*` is documented as *"a machine-derived stand-in kept only so both sets
resolve; treat them as one role"* — **do not wire it into the app.**

### 3.2 What the mockup added

**The amber unlock role.** *"Solar amber is introduced as a single reserved role — it only ever
means unlocked."* This is the mockup's best idea and it survives audit. But:

| Problem | Detail |
|---|---|
| **Two ambers** | `#e0a95c` (directions) vs `#d9a25f` (refined) |
| **Two amber texts** | `#f2d3a2` (directions) vs `#f0dcc0` (refined) |
| **No ramp** | Amber has no 100–900 scale, so tints are ad-hoc `rgba(224,169,92,.07 / .09 / .12 / .13 / .14 / .2 / .22 / .26 / .3 / .32 / .4 / .42 / .45 / .5)` |
| **Overloaded** | Amber means **both** "unlocked by this change" **and** "simulation is active". Those are different facts: a simulation can be active and unlock nothing. |

**Ad-hoc grounds.** `#0c0d14`, `#0d0e15`, `#0e0f17`, `#0e0f18`, `#101220`, `#12141f`, `#131522`,
`#14161f`, `#141621`, `#161826`, `#171927`, `#1b1e30`, `#1d2033` — thirteen background values,
one of which is the actual token. Every board wraps itself in a bespoke radial or linear
gradient.

**Alpha sprawl.** `rgba(233,233,237, α)` appears with **27 distinct α** in the directions file
and **29** in the refined file (.02 … .9). This is a text/border colour system with 29 values
and no names.

**Orphan hue.** `#9dd6c4` (mint) appears only inside the annotation panels to label
"Strengths". Not a product colour — do not carry it forward.

**Missing semantic roles.** No danger/error, no success, no neutral-warning distinct from the
amber unlock role. An app that fetches from three third-party APIs (§7.1) needs an error colour.

### 3.3 Proposed palette

```text
ground        #141621   (the refined canvas ground — promote it, retire the other 12)
surface       #1a1c2b
text          #e9e9ed
text-muted    rgba(233,233,237,.62)   ← 6.3:1  body prose floor
text-subtle   rgba(233,233,237,.50)   ← 4.6:1  meta only, never prose
border        rgba(233,233,237,.10)
border-strong rgba(233,233,237,.18)

reach         --color-accent-400  #b5abfc   boundary of reach, in-orbit nodes
reach-dim     --color-accent-600  #796cbf   inner shells
unlock        #d9a25f  + a 100–900 ramp we generate     "this changed"
unlock-text   #f0dcc0
sim           a *separate* role — reuse unlock hue but a distinct token, so
              "simulation active" and "unlocked" can be told apart later
danger        to be defined — none exists today
```

Five text alphas replace 29. Everything else comes from the Nocturne ramps by name.

---

## 4. Spacing

**Nocturne's scale:** `2.8 / 5.6 / 8.4 / 11.2 / 16.8 / 22.4 px` (density 0.70×). Fractional,
six steps, and the readme insists you use it.

**The mockup uses none of it.** Padding literals: 2, 3, 4, 5, 6, 8, 9, 11, 16, 18, 20, 22, 24,
26, 30, 44. Gaps: 2, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 22, 24, 26, 36, 40. That is a
free-form 1 px grid.

**Recommendation — deviate from Nocturne deliberately.** Adopt a plain 4 px base:
`4 / 8 / 12 / 16 / 24 / 32 / 48 / 64`. Reasons: fractional px produces subpixel seams on
1 px hairline borders (which this design uses everywhere); nobody can reason about 16.8; and
Tailwind's default scale already is this, so the token layer costs zero code. Nocturne's
*density intent* (compact) is preserved — we keep the small end of the ramp in heavy rotation.

`ponytail:` this is the one place we knowingly diverge from the supplied system. Record it.

---

## 5. Grid and layout

**Every board is `position:absolute` inside a fixed frame.** Refined canvas:

```text
1440 × 900
├── header            top 0,  height 58
├── identity rail     top 58, left 0,   width 252
├── orbit canvas      top 58, left 252, right 372   (SVG viewBox 860×800 → 816×760)
├── detail rail       top 58, right 0,  width 372
└── constraint strip  left 288, bottom 26   ← floating, absolutely placed
```

### Findings

- **Zero responsive behaviour.** No media query, no relative unit, no `minmax`, no wrap. Below
  ~1340 px the design does not degrade — it breaks.
- **R2 makes this the top implementation risk.** The delivery target is the ChatGPT in-app
  browser. Its viewport is not 1440 px wide, and we cannot assume it. A pixel-frozen 1440×900
  layout is the most likely single cause of a failed demo.
- **The orbit's node coordinates are polar constants** (`a` degrees, `r` px) resolved against a
  hard-coded centre `(430, 400)` in an 860×800 space. Responsiveness here is not CSS — it is
  recomputing `r` from the container's short side.
- The absolute frame is otherwise a clean three-column shell that CSS Grid expresses in ~6
  lines. Nothing about the *composition* is hard; only its encoding is.
- **Reading order is broken for assistive tech.** DOM order is header → identity rail → SVG →
  detail rail → constraint strip. The constraint strip is visually the primary control and comes
  last in the DOM with no landmark.

### Proposed grid

```text
≥1200px   grid-template-columns: 252px minmax(0,1fr) 372px      (as designed)
840–1199  grid-template-columns: 220px minmax(0,1fr)            detail rail → right slide-over
<840      single column: header / orbit (square, capped) / constraint strip / list
          orbit becomes secondary; the "Closest to your boundary" list becomes primary
```

The narrow layout is not a downgrade — it is Direction C's argument, which the annotation itself
calls *"most trustworthy and legible … cheapest to build well."* We already have that design.

---

## 6. Borders and radius

**Nocturne:** `--radius-sm 4 / --radius-md 8 / --radius-lg 14`.

**Mockup:** 2, 4, 5, 6, 7, 8, 9, 10, 12, 20, 22, 50% — twelve values, none referencing a token.

Borders are almost universally `1px solid rgba(233,233,237, .06 … .18)`. Consistent in kind,
arbitrary in value (8 distinct alphas).

Nocturne's hairline-fade rule (*"Rules fade to transparent at their ends"*) is honoured in the
rails via `linear-gradient(90deg, transparent, rgba(…), transparent)` — but the same readme also
says *"this system prefers whitespace; avoid it."* The mockup adds dividers the system tells you
to drop. Most can go.

**Proposed:** `sm 4` (badges, chips) · `md 8` (buttons, inputs, rows) · `lg 12` (cards, panels,
the floating strip) · `pill 999` (segmented control, status pills). Four values. Two border
alphas: `.10` default, `.18` emphasis.

---

## 7. Reusable components

Extracted from all four boards. Names are proposals. The proposed React/Next.js structure is
in **§18**.

| Component | Appears in | Notes |
|---|---|---|
| `AppHeader` | all | Brand lockup + agent status + avatar. **Avatar must go** — §8 forbids accounts. |
| `BrandMark` | all | Circle with an orbiting dot. Two lockups exist (see §9). |
| `AgentStatusLine` | all | See §10 — the most constitution-sensitive element in the mockup. |
| `IdentityRail` | 1a, refined | Name, role, counters, legend, freshness line |
| `StatCounter` | 1a, 1c, refined | Big number + delta + caption. `tnum`, animated roll. |
| `OrbitLegend` | 1a, refined | Ready now / One gap away / Beyond reach |
| `OrbitCanvas` | 1a, 1c, refined | SVG: field gradient, shells, boundary, ghost boundary, glow, core, leader line, node layer |
| `OrbitNode` | 1a, 1b, 1c, refined | 4 tiers × selected state. See §12. |
| `OrbitBoundary` | 1a, 1c, refined | Solid ring + blurred glow + animated `r` |
| `GhostBoundary` | 1a, 1c, refined | Dashed previous-state ring. **The thesis, drawn.** |
| `ConstraintStrip` | 1a, refined | Floating bottom bar: label + control + static chips + state |
| `SegmentedControl` | 1b, refined | Remote only / Flexible; Sweep / Clusters / List |
| `ConstraintChip` | 1a | Pill; active chip carries `+23` and an amber glow |
| `NearbyList` + `NearbyRow` | refined | title / company / state |
| `DetailPanel` | 1a, refined | Kicker, title, company, 3 stats, blockers, unlock card, actions |
| `StatRow` | refined | The three-up reachability / similar / median |
| `BlockerList` + `BlockerRow` | 1a, refined | label / detail / effect. **This is the Constraint Debugger.** |
| `UnlockCard` | 1a, 1c, refined | Amber panel: count, named roles, trade-off, what stays out |
| `ConstraintLedger` | 1c | 4-col table: CONSTRAINT / VALUE / BLOCKS / STATE |
| `LedgerRow` | 1c | With `SIM` / `SIMULATE` / `LOCKED` state |
| `ScanLog` | 1b | **Drop** — see §10 |
| `SectorList` | 1b | Drop with 1b |
| `Button` | all | Outlined primary + ghost. Nocturne's `.btn` is referenced but overridden inline. |
| `Badge` | 1c | SIM / LOCKED / LIVE |
| `MeterRow` | 1c | Label + value + thin bar |

---

## 8. Navigation

**Unresolved across the four boards.** Four different answers:

| Board | Navigation |
|---|---|
| 1a | Top-bar text tabs: `Orbit` · `Constraints` · `Unlocks` |
| 1b | Segmented control: `Sweep` · `Clusters` · `List` |
| 1c | None — single screen with a `Reset` / `Commit simulation` pair |
| refined | **None** — one screen, all state in-place |

The refined answer is right and should be frozen: **Jorbit is one screen.** Selection swaps the
right rail; simulation changes the canvas. No routes, no tabs, no modals. This matters beyond
aesthetics — a single-screen app with all domain state in one store is what makes P1 tractable
(one state, two drivers: UI and WebMCP tools).

Exceptions that will need somewhere to live: profile intake (S1), evidence drill-down (S3),
source/original link (S4). Recommend: intake as a first-run overlay, evidence and source as
in-rail expansion, never a route.

---

## 9. Inconsistencies

1. **Two brand lockups.** `JORBIT` uppercase, `letter-spacing .14–.16em`, 13–14 px/500
   (directions) vs `Jorbit` sentence case, `-.005em`, 15 px/500 (refined). Pick the refined one.
2. **Two ambers, two amber texts, thirteen grounds.** §3.2.
3. **Numbers do not reconcile across boards.**
   - 1a: `54 reachable (+23), 9 still outside`
   - 1c: `Six constraints hold 87 roles outside your orbit`; `54 reachable, was 31`; meters read
     `Inside orbit 54` / `Blocked by one constraint 27`
   - refined: `31 → 54`; `blockedCount 32 → 9`
   31 → 54 (+23) is consistent everywhere. Everything else is not.
4. **The BLOCKS column does not add up, and never says whether it should.** 1c lists
   23 + 14 + 19 + 21 + 18 + 6 = **101** against a stated total of **87**. Roles blocked by two
   constraints are presumably double-counted — but the UI never says so. This is precisely the
   P3 failure mode: a column of numbers whose semantics cannot be reconstructed.
5. **Dead code in the refined logic.** `boundaryLabel` and `boundaryLabelY` are computed and
   never consumed (three hard-coded `<text>` elements cross-fade instead). `tx` and `anchor` are
   computed per node, then every labelled node hard-codes its own `x` and `text-anchor`.
6. **`n_spa` hard-codes `r=8`** while the generic `dots` path reads `n.size`. Two rendering
   paths for the same concept: six labelled nodes are hand-written `<g>` blocks, eight unlabelled
   ones go through `<sc-for>`.
7. **Nocturne classes referenced then overridden.** `class="btn btn-primary"` immediately
   followed by `style="font-size:12px"`, and `class="seg"` with a full inline re-implementation.
8. **Persona drift vs the frozen universe.** §7.3 freezes v1 analysis to ~10–20 Operations-
   adjacent archetypes. The mockup's roles are *Data Scientist, Product · Staff Data Scientist ·
   ML Engineer · Quant Researcher · Growth PM · Solutions Engineer · Analytics Lead*. Only
   *Data Analyst / Business Analyst* would be in-family. The demo narrative is built on roles our
   engine is not scoped to analyse.

---

## 10. Constitution conflicts — the section that matters

These are not style opinions. Each names a falsifiable principle.

### C1 — The agent is portrayed as a background process Jorbit owns · **P6, P1**

Every board carries an agent telemetry line:

| Board | String |
|---|---|
| 1a | `agent · re-ranked 118 roles` |
| 1b | `agent idle · next sweep 06:00`, `Agent enriched 41 postings — via MCP` |
| 1c | `agent applied 2 edits` |
| refined | `Agent enriched 41 postings · 11m ago` / `Agent re-scored 118 roles · 12s ago` |

P6: *"Nunca simular un agente conectado, nunca fingir tool-calls."* A pill that reports agent
activity **when no agent is attached is a simulated agent**. `next sweep 06:00` is worse — it
asserts Jorbit schedules autonomous agent runs, which is a product Jorbit is not.

`Agent enriched 41 postings` also implies the agent **writes job data into Jorbit's corpus**.
That is not among the five candidate tools (S3), and it would make evidence provenance
non-reconstructible — P3 and P7 both.

**Fix:** the element stays, its semantics change. It becomes a **connection state**, not a
feed:

```text
no WebMCP in this browser  →  "Agent mode unavailable in this browser"   (P6's required notice)
WebMCP present, idle       →  "Agent connected"
tool call in flight        →  "set_candidate_profile · running"
last call completed        →  "debug_constraints · 12s ago"        ← real, logged, replayable
```

Only real tool calls we actually served may appear. That turns the mockup's weakest element into
the WebMCP Leverage evidence the jury's first criterion asks for (§9).

### C2 — Numbers without reconstructible evidence · **P3**

*"Jorbit nunca muestra un número de unlock que no pueda reconstruir."*

| Number shown | Reconstructible? |
|---|---|
| `+23`, `31 → 54` | **Yes** — Constraint Unlock, deterministic re-filter. Keep. |
| `SQL unlocks 14` / `+14 roles` | Only if skill-evidence extraction survives. **Degradable.** |
| `Six constraints hold 87 roles` with a BLOCKS column summing to 101 | **No** — §9.4 |
| `reach 0.92`, `conf 0.92`, `0.71`, `0.68`, `0.41` | **No.** A two-decimal score with no defined scale, no units, no drill-down. |
| `Median pay €71k · +4%` | Only if structured salary coverage clears B2. |
| `SQL · ~6 weeks of work` | **No.** Nothing in O\*NET or a job posting yields a training duration. Pure invention. |
| `lowers median pay 8%`, `+4%` | Requires salary coverage on **both** sets. |

### C3 — Reachability score is the matching UI P2 forbids · **P2**

*"Violación: una pantalla cuyo valor principal es una lista ordenada por % de match."*

`reach 0.92 · 14 open` set next to every node, and `reachability 0.71` as the first of three
detail stats, is a match score wearing a different noun. The mockup does *not* sort a list by it
— which is why this is a risk, not yet a violation — but it puts a compatibility number in the
most prominent slot of the detail panel.

**Fix:** replace the scalar with the *reason*. The mockup already writes the better version
itself, in the `ready` branch: *"Every constraint satisfied — remote, senior level, above your
salary floor."* That sentence is P2-compliant; `0.92` is not. Use radius for reachability (it
already encodes it, spatially and honestly) and delete the decimal.

### C4 — No source, no original link, no cache age · **P7**

*"con fuente y enlace original citados … Cuando se sirve desde caché o snapshot, la UI lo indica
con su antigüedad."*

Zero boards show a source, a link, or a freshness stamp on a posting. `Updated 11 minutes ago ·
from 118 tracked roles` in the identity rail is app-level, not per-posting, and does not name
JobsCollider / Arbeitnow / Jobicy. The detail panel — the one place a user decides to act — has
no way out to the real job.

**Fix:** `DetailPanel` gains a required provenance block: source name, posting date, cache age
when served from snapshot, and "View original" as the panel's terminal action. Non-negotiable,
and it is the *only* external action P4 permits.

### C5 — No degraded variant · **§7.2, S1**

Skill Unlocks are declared **degradable**. The design gives them equal billing with Constraint
Unlocks (the SQL row sits in the ledger alongside Location; `Staff Data Scientist · needs
intermediate SQL` is a labelled node; `Plan the SQL step` is a primary action). If B2 shows the
evidence will not hold, we must be able to remove skill rows without the screen collapsing.

**Fix:** design the Constraint-only variant now, as the *default*, and treat skill rows as
additive.

### C6 — Register mismatch for the primary user · **§3**

Primary consumer is a **non-technical job seeker**. The mockup speaks: *constraint debugger ·
stack trace for a career · SIM · COMMIT SIMULATION · reach 0.92 · SWEEP 04 · bodies · contacts ·
BLOCKS · LOCKED*, set in mono caps.

"Constraint Debugger" is a fine *internal* name — the constitution uses it. It is a poor
*user-facing* label. The refined canvas is already softer (`Closest to your boundary`,
`One gap away`, `Why this is in reach`), and it is measurably better copy.

### C7 — Account chrome with no accounts · **§8**

A 26 px avatar circle sits in the header of 1a, 1b and the refined canvas. §8 forbids accounts,
auth and persistent profiles in v1. Remove it, or replace it with the profile-source affordance
(*"Profile set by agent · edit"*).

### C8 — Star constraint is hard-coded to Location · **§7.2, §11.2**

Which constraint anchors the demo is explicitly **not frozen** and is decided by B2. The refined
canvas hard-codes `Location` into the strip's markup, into `setRemote` / `setFlexible`, into the
copy, and into `rSim` per node.

**Fix:** the constraint strip must be data-driven over a constraint list; `rSim` becomes a
computed value from a re-filter, not a per-node literal. Cheap now, expensive after B2 lands.

---

## 11. Accessibility

Measured against the refined canvas ground `#141621`.

### 11.1 Contrast — measured

| Foreground | Ratio | Verdict |
|---|---:|---|
| `rgba(233,233,237,.9)` node titles | 12.19 | pass |
| `.72` | 8.14 | pass |
| `.62` | 6.34 | pass |
| `.55` | 5.24 | pass |
| `.50` | 4.58 | pass (marginal) |
| `.48` detail company | 4.28 | **fail AA** |
| `.45` rail sub-copy, `reachableCaption` | 3.93 | **fail AA** |
| `.42` "still beyond the boundary" | 3.59 | **fail AA** |
| `.40` node meta, `nearby` company | 3.35 | **fail AA** |
| `.38` header agent note | 3.16 | **fail AA**, borderline for large |
| `.35` node state | 2.88 | **fail** even at 3:1 |
| `.30` `Updated 11 min ago`, SVG labels | 2.43 | **fail** |
| `.26` / `.22` blocked-node meta | 2.14 / 1.87 | **fail badly** |
| `#d9a25f` amber | 7.96 | pass |
| `#f0dcc0` amber text | 13.46 | pass |
| `#b5abfc` accent-400 | 8.74 | pass |
| `#9184d9` accent base | 5.58 | pass |
| `#796cbf` accent-600 (inner shells) | 4.04 | fail for text; fine as a hairline |

The design's **entire secondary copy layer sits between .30 and .48** — all of it below AA.
This is not a few stray labels; it is the mockup's default body voice. Floor at `.62` for prose
and `.50` for meta (§3.3) and the problem disappears without touching the composition.

Worst case: blocked-node labels at `.26` — the roles the product exists to tell you about are
its least legible text.

### 11.2 Keyboard and semantics

- **The primary interaction is unreachable by keyboard.** Every node is
  `<g onClick=… style="cursor:pointer">` — not focusable, no `role`, no accessible name, no
  `tabindex`. A keyboard or screen-reader user cannot select an opportunity at all.
- **No focus styling anywhere.** Nocturne defines `:focus-visible { outline: 2px solid
  var(--color-accent) }` and the mockup's inline-styled buttons bypass `.btn` entirely.
- **The segmented control is two `<button>`s with no `role="radiogroup"`**, no
  `aria-pressed` / `aria-checked`. State is conveyed by background colour alone.
- **No text alternative for the orbit.** Boundary radius, node radius and node size carry
  quantitative meaning with no `<title>`/`<desc>`, no `role="img"`, no equivalent table.
- **DOM order ≠ visual priority** (§5).

### 11.3 Colour-only encoding

Amber is the sole carrier of "unlocked". A deuteranopic user watching the signature moment sees
nodes move inward and nothing else change — the product's central message is delivered in a hue
they cannot separate from the ground. Blocked nodes *do* get a redundant cue (hollow + dashed);
unlocked nodes do not.

**Fix:** unlocked nodes gain a redundant non-colour mark — a filled ring where in-orbit nodes
are hollow-cored, plus a `NEW` affix on the label — and the unlock card states the count in
words. Also: `text-decoration: line-through` on `Remote only` conveys "superseded" by decoration
only; add the word.

### 11.4 Motion

Five infinite animations — `jb-sweep 9s` (a full-circle conic rotation), `jb-pulse 2.6–3s`,
`jb-dash`, `jb-alive 6.5s`, `jb-breathe` — and **no `prefers-reduced-motion` guard anywhere in
either file**. Vestibular-trigger risk, plus continuous repaint on a mobile in-app browser.

`filter: blur(9px)` on an animated stroked SVG circle (the boundary glow) is the single most
expensive paint in the design and it runs forever.

**Fix:** one `@media (prefers-reduced-motion: reduce)` block that kills all ambient loops and
collapses the 1.1 s state transition to an instant swap — the *information* survives (ghost ring,
counter, colours), only the travel is removed. Replace the animated blur glow with a static
radial gradient.

---

## 12. The three product concepts

### 12.1 Career Orbit

**What works, keep exactly:**

- **Radius = effort-to-reach.** Position is data, not decoration. This is the whole reason a
  spatial view beats a list here, and it is honest: the same number that drives the count drives
  the geometry.
- **Three tiers with distinct visual grammar:** `ready` (filled core, bright ring),
  `gated` (filled, dimmer), `blocked` (hollow, dashed, unlabelled until probed). Blocked is a
  *place*, not a greyed-out row. Direction A's annotation states the rule explicitly and it is
  the right rule.
- **The ghost boundary.** A dashed ring holding the pre-simulation state while the live boundary
  inflates past it. This is "what changes if I change X" rendered in one mark. **The most
  on-thesis element in the entire mockup.**
- **Selection leader line** from core to selected node at `.32` opacity — cheap, effective.
- **Data shape.** `{ id, title, meta, a, r, rSim, size, tier, reach, similar, pay }` ports to
  React unchanged.

**What breaks:**

- **Label collision is unsolved and the annotation admits it.** Six labelled nodes are
  hand-placed `<g>` blocks with hard-coded `x` / `text-anchor`. At 14 nodes it is already
  hand-tuned; at 118 tracked roles it is impossible.
  **Fix (lazy):** cap labels at the top N by relevance (N ≈ 6), everything else renders as an
  unlabelled dot that labels on hover/focus/selection. No collision solver needed — the mockup's
  own `east = cos(rad) >= -0.15` side-flip plus a hard cap is enough.
- **Density.** 14 nodes on an 816×760 canvas is already near-full. §7.3 implies dozens.
  **Fix:** the canvas shows a *sample*, and says so — "showing 14 of 118 · closest to your
  boundary". Honest, and it is the P3-safe framing.
- **Fixed 860×800 viewBox** with absolute polar constants (§5).
- **`filter: blur(9px)`** on the animated boundary glow (§11.4).

### 12.2 Constraint Debugger

Two designs exist, and they are not the same product.

| | **1c — full ledger** | **refined — per-opportunity blockers** |
|---|---|---|
| Scope | Global: all constraints, all counts | Local: what holds *this* role out |
| Form | 4-column table, per-row SIM/SIMULATE/LOCKED | List of label / detail / effect |
| Strength | Trade-offs visible; comparable; scannable | Concrete; causal; reads as an explanation |
| Weakness | Reads as an admin tool; the BLOCKS column has the §9.4 arithmetic problem | Cannot answer "what is blocking me overall" |

**Recommendation: build both, in this order.** The refined per-opportunity version is the
60-second-test path (§4.1) and ships first. The ledger is the "what is blocking me overall"
view and is the natural home for S3's evidence drill-down. It is also, per its own annotation,
*"cheapest to build well"* — and it is the layout that survives a narrow viewport (§5).

**Keep from 1c:**
- `LOCKED` for user-declared non-negotiables. Respecting a stated hard constraint, visibly, is
  the difference between advice and nagging.
- The trade-off clause: *"Accepting mid-level opens 19, lowers median pay 8%."* §3 makes the
  human the trade-off arbiter; this is the only element that gives them both sides.
- Per-row `SIM` badges — simulated rows are marked in place, so an agent-made edit is reviewable
  exactly where a user-made one is (a genuine P1 win).

**Fix in 1c:** the BLOCKS column must state its semantics ("roles blocked by *at least* this
constraint; a role may appear in more than one row") or become a non-overlapping decomposition.
As drawn, it violates P3.

### 12.3 Opportunity Unlock

The refined `UnlockCard` is the strongest single piece of copy in the mockup:

> **23 opportunities entered your orbit**
> Data Scientist · Analytics Lead · Insights Partner, EU — and 20 more across 14 companies.
> Median pay rises to €71k.
> One role stays out: Staff Data Scientist still needs intermediate SQL.

Four moves, all correct: the count, **named** examples, the trade-off, and **what did not
unlock**. That last line is what separates Jorbit from a filter — it is §2.1's identity rule
written out.

**What is missing — and P3 requires it:** "and 20 more" is a dead end. There must be a way to
see all 23 with the evidence for each (S3). Without it we are showing a number we cannot
reconstruct *in the UI*, which is exactly the stated violation:
*"mostrar '27 roles unlocked' sin poder enumerar esos 27."*

**Fix:** `and 20 more across 14 companies` becomes the affordance that expands the full
enumerated list, each row citing its source and original link (C4).

---

## 13. What is generic or reads as AI-generated

Ranked by how much deleting it improves the product.

1. **Starfield background** — `radial-gradient(1px 1px at 14% 22%, …)` × 5–6, on 1a and the
   refined canvas. Space-theme cliché. Adds nothing, costs a composite layer. **Delete.**
2. **The rotating radar sweep** (1b) — a 9-second infinite conic gradient. Decorative, and it
   *lies*: it implies continuous live scanning of a corpus we refresh from a cache. **Delete
   with 1b.**
3. **Mono micro-labels in caps at .14em** — `CENTRE OF ORBIT`, `SELECTED BODY`, `SWEEP FILTERS`,
   `WHAT MOVED IT INWARD`, `ORBIT RESPONSE`. Technical-dashboard pastiche aimed at a
   non-technical user. **Delete** (the refined canvas already did).
4. **Two-decimal scores** — `reach 0.92`, `conf 0.92`. Fake precision, and P2-adjacent (§10 C3).
   **Delete.**
5. **Fake telemetry** — `SWEEP 04 · 12s AGO`, `next sweep 06:00`, `23 NEW CONTACTS`,
   `agent applied 2 edits`. Invented liveness (§10 C1). **Replace with real state.**
6. **Gradient-fade hairline dividers**, used ~8 times where Nocturne's own guidance says prefer
   whitespace. **Mostly delete.**
7. **The blurple→amber gradient meter fill** (1c, bottom right). A two-hue gradient across a bar
   whose two ends mean nothing. **Delete.**
8. **The account avatar** (§10 C7). **Delete.**
9. **Generic placeholder companies** — Vessel, Northbeam, Ravel, Corvid, Halden, Lumen, Meridian,
   Sable. Correct for a mockup; must be real cited postings in the build (P7).
10. **`Maya Okonjo · Lagos → remote · Product Analyst → Data Scientist`** — a competent persona,
    but outside the frozen archetype family (§9.8) and the Lagos→Europe visa framing quietly
    assumes visa-sponsorship coverage that B2 has not measured. **Re-cast after B2.**

**What is emphatically *not* generic** and should be defended: the reserved amber role, the
ghost boundary, "what stays out", `LOCKED` for non-negotiables, radius-as-effort, and the
refined canvas's copy voice.

---

## 14. Hard or unnecessarily complex to implement

| Item | Cost | Verdict |
|---|---|---|
| Fixed 1440×900 absolute layout → responsive | High, unavoidable | **Rebuild as CSS Grid.** Not a port. |
| Polar label collision avoidance | High if solved properly | **Sidestep:** cap labelled nodes at ~6 + hover/focus labels |
| 1b's constellation edges + cluster detection | High (graph layout + clustering) | **Drop 1b entirely** |
| Animated `blur(9px)` on a stroked circle | Medium runtime cost, forever | Replace with a static radial gradient |
| 14 simultaneous SVG `r` + `transform` transitions | **Low** — this is cheap and it works | **Keep.** Prefer `transform` over animating `r`. |
| `<sc-for>` / `<sc-if>` / `{{ }}` / `DCLogic` | N/A — canvas runtime, not React | Discard the syntax; **the logic ports 1:1** |
| Counter roll 31 → 54 | Low (`tnum` is already set) | Keep, guard with `prefers-reduced-motion` |
| Per-node hand-written `<g>` blocks | Medium, and it does not scale | Collapse to one `<OrbitNode>` over data |
| Nocturne's fractional 0.7× spacing | Low but permanently annoying | **Replace with 4 px base** (§4) |
| Vendoring `_ds/styles.css` wholesale | Low, but its companion files are absent | **Take the tokens, drop the component layer** |

`renderVals()` in `Jorbit.dc.html:290–445` is genuinely good code: pure, derives every visual
value from `{ sim, sel }` + a static `NODES` array, no side effects. It becomes a `useMemo` and a
selector module almost verbatim. **This is the highest-value thing in the folder to copy.**

---

## 15. Copy directly vs rebuild in React

### Copy (values, not markup)

- The **token values** we keep: Nocturne's ramps, `#d9a25f` amber, `#141621` ground.
- The **`NODES` data shape**: `{ id, title, meta, a, r, rSim, size, tier, reach, similar, pay }`.
- The **tier → visual mapping table** inside `renderVals()` (stroke / fill / innerFill /
  titleFill / metaFill / dash per tier). Hand-tuned and correct.
- The **polar math**: `cx + r·cos(a/D)`, `cy + r·sin(a/D)`; the `east = cos(rad) >= -0.15`
  side-flip.
- The **transition curve**: `1.1s cubic-bezier(.22,.61,.36,1)`.
- The **copy strings**, after the C3/C6 corrections. Especially: *"Four roles sit one constraint
  outside your current orbit."* · *"One role stays out."* · *"Why this is in reach."*
- The **state machine**: `{ sim, sel }`. Two booleans-ish drive the entire screen. Do not grow it.

### Rebuild

- **Layout** — absolute → CSS Grid + container queries (§5).
- **`OrbitCanvas`** — one `<OrbitNode>` mapped over data; no hand-written `<g>` per node.
- **Polar layout** — `useOrbitLayout(nodes, { width, height })` returning screen coords from a
  radius scale derived at runtime, so it survives any viewport.
- **State** — `{ sim, sel }` moves into the **shared domain store that WebMCP tools also write**.
  This is the P1 hinge: `search_opportunities`, `debug_constraints`, `set_candidate_profile` and
  the UI's own handlers must land on the same reducer. The mockup's `setState` calls mark exactly
  where those tools attach.
- **Every interactive element** — real `<button>` / `role="radiogroup"` / focusable nodes with
  accessible names (§11.2).
- **Detail rail** — same content, but with the provenance block (C4) and the evidence expansion
  (S3) the mockup lacks.

### Discard

`support.js`, `_ds_bundle.js`, `_adherence.oxlintrc.json`, the `dv-*` canvas chrome, the three
340px annotation panels, the starfield, the radar sweep, all mono micro-labels, the avatar.

---

## 16. Recommended changes before implementation

Ordered. **Blocking** items are constitution conflicts; the rest are quality.

### Blocking

| # | Change | Principle |
|---|---|---|
| B-1 | Redefine the agent line as **connection + real tool-call state**. Add the "Agent mode unavailable in this browser" state (S2). Delete `next sweep`, `enriched N postings`, `re-ranked N roles`. | **P6, P1** |
| B-2 | Delete `reach 0.92` / `conf 0.xx` as a displayed scalar. Radius already encodes it; the reason-sentence replaces the number. | **P2, P3** |
| B-3 | Add per-posting **provenance**: source name, posting date, cache age, "View original". Required on `DetailPanel` and on every enumerated row. | **P7, P4** |
| B-4 | Make `and 20 more` **enumerable** — the unlock card expands to all N with evidence per row. | **P3** |
| B-5 | Fix or remove the `BLOCKS` column arithmetic (101 ≠ 87). State overlap semantics explicitly. | **P3** |
| B-6 | Delete `~6 weeks of work` and any other invented effort/duration estimate. | **P3** |
| B-7 | Design the **Constraint-only default**; skill rows become additive, removable without collapse. | §7.2, S1 |
| B-8 | Make the constraint strip **data-driven**; no constraint hard-coded as the star. `rSim` becomes computed, not a per-node literal. | §7.2, §11.2 |
| B-9 | Remove the account avatar. | §8 |
| B-10 | Re-cast the persona and role set into the frozen archetype family (§7.3), after B2 confirms the pool. | §7.3, P12 |

### High

| # | Change |
|---|---|
| H-1 | **Responsive plan** — three layouts (§5). Verify the narrow one against R2's target browser *before* building the wide one. Highest delivery risk in the design. |
| H-2 | **Contrast floor** — prose ≥ `.62` (6.3:1), meta ≥ `.50` (4.6:1). Deletes ~24 of 29 alpha values (§3.3). |
| H-3 | **Keyboard access to nodes** — focusable, named, `Enter`/`Space` selects, arrow-key traversal by orbit ring. |
| H-4 | **`prefers-reduced-motion`** — one media block killing all ambient loops and collapsing the 1.1 s transition. Replace the animated `blur(9px)` glow with a static gradient. |
| H-5 | **Redundant non-colour cue for `unlocked`** (§11.3). |
| H-6 | **Collapse the scales:** 7 type steps, 4 radii, 4-px spacing base, 5 text alphas, 2 border alphas, 1 amber, 1 ground. |
| H-7 | **Add the missing screens** S0–S2, S5 as designs before any of them is coded. |

### Medium

| # | Change |
|---|---|
| M-1 | Freeze the single-screen navigation model (§8). Intake as first-run overlay; evidence and source as in-rail expansion; no routes. |
| M-2 | Move the display counter from Inter 300 to 400. |
| M-3 | Pick one brand lockup — the refined sentence-case `Jorbit`. |
| M-4 | Delete the starfield, the fade dividers, the gradient meter fill. |
| M-5 | Split `unlock` and `simulation-active` into two colour roles sharing one hue. |
| M-6 | Cap labelled nodes at ~6; label the rest on hover/focus. State the sample honestly: "showing 14 of 118". |
| M-7 | Restore Nocturne's `:focus-visible` ring on every interactive element. |
| M-8 | Generate a real 100–900 amber ramp; retire the 14 ad-hoc amber alphas. |

---

## 17. Open questions for the owner — RESOLVED 2026-08-26

1. **Direction:** refined canvas (A's orbit + C's clarity). **1b dropped.** ✔
2. **Ledger:** not in v1. Per-opportunity debugger only. `ConstraintLedger` / `LedgerRow` leave
   §18's component map for v1; `UnlockEvidenceList` (B-4) absorbs the enumeration duty the
   ledger would have carried. ✔
3. **Spacing:** 4 px base approved. ✔
4. **Persona:** deferred to B2. ✔ (see `docs/b1-b2-reconciliation.md` — B2 has no results yet)
5. **Narrow viewport:** deferred to B1. ✔ (see reconciliation — no viewport was measured)

---

## 18. Proposed React / Next.js component map

Proposal only. Nothing here is built until B1 clears (§11.1 blocks production UI) and the owner
approves. R8 fixes the stack: TypeScript + React/Next.js.

### 18.1 Shape

```text
app/
  layout.tsx                    fonts, tokens, <html data-theme>
  page.tsx                      the one screen (§8: Jorbit is single-screen)

components/
  chrome/
    AppHeader.tsx               brand + agent state + profile source
    BrandMark.tsx               circle + orbiting dot (sentence-case lockup)
    AgentStatus.tsx             B-1 · connection + last real tool call + "unavailable" state
  identity/
    IdentityRail.tsx            composition only
    StatCounter.tsx             tnum, animated roll, reduced-motion aware
    OrbitLegend.tsx
    ProfileSummary.tsx          name / role / location  (no avatar — B-9)
  orbit/
    OrbitCanvas.tsx             <svg>, role="img", <desc>, sizing via container query
    OrbitField.tsx              radial field gradient + inner shells
    OrbitBoundary.tsx           live ring + static glow gradient (H-4)
    GhostBoundary.tsx           dashed previous-state ring  ← the thesis
    OrbitNode.tsx               one component, 4 tiers × selected; focusable, named
    OrbitLeaderLine.tsx
    OrbitSampleNote.tsx         "showing 14 of 118 · closest to your boundary"  (M-6)
  constraints/
    ConstraintStrip.tsx         data-driven over constraints[] (B-8), not Location-hardcoded
    ConstraintControl.tsx       renders segmented / range / toggle by constraint kind
    SegmentedControl.tsx        role="radiogroup", aria-checked  (H-3)
    SimulationState.tsx         "Live orbit" | "Simulation · +23 unlocked, unsaved"
                                — ConstraintLedger / LedgerRow cut from v1 (owner, §17.2)
  detail/
    DetailRail.tsx              swaps Browse ↔ Detail; no route, no modal
    NearbyList.tsx              "Closest to your boundary"
    NearbyRow.tsx
    OpportunityDetail.tsx       kicker / title / company / stats / blockers / unlock / actions
    ReasonStats.tsx             similar · median — reachability scalar removed (B-2)
    BlockerList.tsx             ← the Constraint Debugger, per-opportunity
    BlockerRow.tsx              label / detail / effect
    ProvenanceBlock.tsx         B-3 · source, posted, cache age, "View original"
    UnlockCard.tsx              count / named / trade-off / what stays out
    UnlockEvidenceList.tsx      B-4 · expands "and 20 more" to all N, cited
  primitives/
    Button.tsx                  outlined primary + ghost, :focus-visible
    Badge.tsx                   SIM / LOCKED / LIVE
    Meter.tsx
    Panel.tsx
  states/
    AgentUnavailableNotice.tsx  S2 · P6's required notice
    ProfileIntakeForm.tsx       S1 · manual fallback (§7.5) — first-run overlay
    EmptyOrbit.tsx              S5
    ErrorState.tsx              source fetch failed / serving snapshot

lib/
  domain/
    store.ts                    ← THE P1 HINGE. UI handlers and WebMCP tools both write here.
    selectors.ts                port of renderVals(): { sim, sel } + jobs → every visual value
    types.ts                    Job, CandidateProfile, Constraint, SkillEvidence, Unlock
  orbit/
    useOrbitLayout.ts           polar → screen coords from live container size (§5)
    tiers.ts                    tier → { stroke, fill, inner, titleFill, metaFill, dash }
  webmcp/
    registry.ts                 thin isolation layer over the volatile API (RK1)
    tools/                      set_candidate_profile · search_opportunities · debug_constraints
                                (+ inspect_unlock · compare_career_worlds, S3 says ~3 well done)

styles/
  tokens.css                    re-tokenised from Nocturne + amber ramp + 4px spacing (§3.3, §4)
```

### 18.2 State ownership

```text
                 ┌──────────────────────────┐
   UI handlers ─▶│  lib/domain/store.ts     │◀─ WebMCP tools
                 │  { profile, jobs,        │
                 │    constraints, sim,     │
                 │    sel }                 │
                 └────────────┬─────────────┘
                              │ selectors.ts  (pure, memoised)
                              ▼
        OrbitCanvas · IdentityRail · DetailRail · ConstraintStrip
```

One store, two drivers, one set of selectors. **P1 is satisfied structurally, not by
convention** — there is no second code path a tool could take. This is the single most important
architectural consequence of the audit, and it is exactly what the mockup's `renderVals()`
already models: a pure function from `{ sim, sel }` to every rendered value.

Purely visual state — hover, panel collapse, zoom — stays local in components and is deliberately
**not** in the store and **not** exposed as a tool (P1: *"Exponerlas sería ruido para el
agente"*).

### 18.3 Where the mockup maps in

| Mockup source | Becomes |
|---|---|
| `NODES` array (`Jorbit.dc.html:~288`) | fixture for `lib/domain/types.ts`; replaced by normalized `Job[]` |
| `renderVals()` tier branch | `lib/orbit/tiers.ts` — copy near-verbatim |
| `renderVals()` polar math | `lib/orbit/useOrbitLayout.ts` — rewritten to take container size |
| `renderVals()` blockers branch | `selectors.ts` → `BlockerList` |
| `setState({ sim })` / `pick(id)` | `store.ts` actions — **also** the WebMCP tool handlers |
| `<sc-for>` / `<sc-if>` / `{{ }}` | discarded; plain JSX |
| hand-written `<g>` per node | one `OrbitNode` mapped over `useOrbitLayout()` output |
| `_ds/styles.css` `:root` | `styles/tokens.css`, re-scaled per §3.3 / §4 |

### 18.4 Build order (after B1 clears)

1. `tokens.css` + `primitives/` — no product logic, unblocks everything.
2. `lib/domain/store.ts` + `selectors.ts` against the mockup's static fixture. **Before any
   pixels**: it is the P1 contract.
3. `OrbitCanvas` + `useOrbitLayout` + `OrbitNode` at one viewport.
4. `DetailRail` (browse ↔ detail ↔ blockers) — completes the 60-second path (§4.1).
5. `ConstraintStrip` + the simulation transition — the signature moment.
6. `ProvenanceBlock` + `UnlockEvidenceList` — B-3 and B-4, before the number is ever shown.
7. `webmcp/registry.ts` + the first tool onto the existing store.
8. Responsive pass (H-1) — verified in R2's real browser, not emulated.
9. `states/` — S1, S2, S5, errors.
