# B2 — Data Coverage Audit (Constitution §11.2)

> **Status:** **EXECUTED 2026-08-26.** Results below are measured, not estimated.
> **Script:** `audit-job-data/scripts/audit_data_coverage.py` — run unmodified.
> **Raw outputs:** `docs/data/b2-audit-summary.json` (copied from the run).
> **Derived cross-tab:** `docs/data/b2-archetype-crosstab.py` — reuses the script's own
> `match_archetypes()`; adds no new methodology, only the granularity D12 requires.
> **Pool:** 11,569 unique jobs fetched from the three approved sources (§7.1).

---

## 1. Coverage by source

| | **JobsCollider** | **Arbeitnow** | **Jobicy** |
|---|---:|---:|---:|
| jobs (unique) | **7,919** | 2,191 | 1,459 |
| description | 100 % | 100 % | 99.9 % |
| avg description length | 6,778 ch | 6,477 ch | 7,061 ch |
| salary (structured) | 47.4 % | **0 %** | 47.3 % |
| seniority | **100 %** | 35.5 % † | **100 %** |
| remote (field present) | 100 % | 100 % | 100 % |
| **remote = true** | **100 %** | **7.8 %** | **100 %** |
| onsite / hybrid | 0 % | **92.2 %** | 0 % |
| location | 66.0 % | 97.5 % | 100 % ‡ |
| visa sponsorship (field) | 0 % | **6.9 %** (150 jobs) | 0 % |
| visa (text signal only) | 3.4 % | 1.2 % | 2.4 % |
| employment type | **0 %** | 68.5 % † | 100 % |
| categories | 16 | 2,026 † | 22 |
| **jobs mapping to archetypes** | **493** (6.2 %) | 68 (3.1 %) | 131 (9.0 %) |

† **Arbeitnow's structured fields are not usable as taxonomy.** Its "seniority" values are
free-text board tags mixed with noise — `berufserfahren`, `Student college`, `Werkstudent`,
`Social Media Manager`, `Team Leader`. Its 2,026 "categories" over 2,191 jobs means the field is
effectively a free-text tag cloud, not a classification.

‡ Jobicy's location is a **region tag** (`USA`, `Europe`, `EMEA`), not a city. JobsCollider and
Arbeitnow give city strings. The three sources do not share a location granularity.

**Descriptions are the one field that is universally excellent** — ~100 % present, ~6.5–7 k
chars, HTML in all three. That is the raw material RK3's skill-evidence extraction needs.

---

## 2. Jobs mapping to our archetypes (RK7)

**692 unique jobs** across all three sources (697 archetype matches — 5 jobs match two
archetypes, a 0.7 % overlap; **relevant to D7's overlap rule**).

| Archetype | JC | AN | Jobicy | **Total** |
|---|---:|---:|---:|---:|
| Project Manager | 132 | 17 | 22 | **171** |
| Customer Success Manager | 74 | 11 | 54 | **139** |
| Program Manager | 85 | 3 | 16 | **104** |
| Revenue Operations | 42 | 6 | 9 | **57** |
| Data Analyst | 36 | 12 | 8 | **56** |
| Business Analyst | 29 | 8 | 6 | **43** |
| Operations Analyst | 23 | 2 | 1 | **26** |
| Implementation Specialist | 20 | 1 | 4 | **25** |
| Customer Success Operations | 12 | 1 | 6 | **19** |
| Implementation Consultant | 15 | 1 | 2 | **18** |
| Business Operations | 9 | 3 | — | **12** |
| Customer Success Specialist | 5 | 2 | 3 | **10** |
| Product Operations | 6 | 1 | 2 | **9** |
| **Project Coordinator** | 8 | — | — | **8** |

JobsCollider supplies **493 of 692 (71 %)**. Top six archetypes hold 570 (82 %).

**RK7 verdict: the pool holds.** 692 jobs over 14 archetypes is enough for credible unlock
counts in the tens — not the hundreds. Numbers in demo copy must be sized to this reality.

**One sharp finding:** `Project Coordinator` — the constitution's own headline persona (§1) —
returns **8 jobs in 11,569**. The identity the problem statement is written around barely exists
as a job title. That is not a defect in the data; **it is the product thesis, measured.** See §6.

---

## 3. Best source / combination

| Source | Keep? | Why |
|---|---|---|
| **JobsCollider** | **Primary** | 71 % of the archetype pool, 100 % descriptions, 100 % clean seniority, 47 % salary |
| **Jobicy** | **Secondary** | Highest archetype *density* (9.0 %), best field hygiene (100 % seniority, 100 % employment type, 47 % salary) |
| **Arbeitnow** | **Recommend dropping from v1** | Only 68 archetype jobs (3.1 %), **0 % salary**, unusable seniority, tag-cloud categories |

Dropping Arbeitnow costs the only non-remote coverage and the only visa signal — both of which
§4 shows are not viable constraints anyway. It buys a large gain in data quality:

> Seniority coverage across the archetype pool rises from **88.9 % to 98.6 %** — 68 of the 77
> unknown-seniority jobs are Arbeitnow's.

**Recommended universe: JobsCollider + Jobicy = 624 archetype jobs.** This is a scope decision
(§7.1 froze no hierarchy but did approve all three) → **owner call**.

---

## 4. Which constraints are actually computable

Measured against the 692-job archetype pool.

| Constraint | Coverage | Deterministic? | Verdict |
|---|---:|---|---|
| **Seniority** | **88.9 %** (98.6 % without Arbeitnow) | Yes — clean multi-band enum | ✅ **Strong** |
| **Salary floor** | **44.7 %** (309 / 692) | Yes — structured min/max | ⚠️ **Usable, half-blind** |
| Employment type | JC 0 % | — | ❌ Primary source has no data |
| Location | mixed granularity (city vs region tag) | No shared unit | ❌ Not comparable across sources |
| **Remote** | pool is **~90 % remote** | Yes, but | ❌ **No counterfactual exists** |
| Visa sponsorship | 150 / 11,569 = 1.3 %, all Arbeitnow | Yes | ❌ Too sparse at archetype scale |

### Seniority — the distribution that makes it work

| Band | Jobs | Share | Have salary |
|---|---:|---:|---:|
| manager | 242 | 35.0 % | 42 % |
| senior | 158 | 22.8 % | 58 % |
| mid | 154 | 22.3 % | 45 % |
| *(unknown)* | 77 | 11.1 % | 5 % |
| director | 26 | 3.8 % | 77 % |
| entry | 20 | 2.9 % | 60 % |
| principal | 10 | 1.4 % | 70 % |
| staff / intern / executive | 5 | 0.7 % | — |

Three bands each hold 150+ jobs. Every adjacent pair is a real, reconstructible counterfactual.

### Remote — the measured death of the mockup's signature moment

The approved design's signature moment is `Location · Remote only → Flexible · +23`.

- JobsCollider: **100 %** remote. Jobicy: **100 %** remote.
- Arbeitnow is the only non-remote source: 92.2 % onsite/hybrid, but only **68** archetype jobs.
- Ceiling for the entire counterfactual: **~63 jobs** — and every one of them comes from the
  source with **0 % salary** and **35 % unusable seniority**, so we could count them but barely
  describe them.

> RK4 warned that two of three sources are remote-only and that a remote counterfactual might not
> survive. **Measured: it does not.** The mockup's star variable is the least supported one in
> the data.

This is the finding that forces B-8 and a redesign of the signature moment.

---

## 5. Recommended star constraint: **Seniority**

| | Seniority | Salary floor | Remote *(mockup's choice)* |
|---|---|---|---|
| Coverage | 88.9 / 98.6 % | 44.7 % | ~10 % non-remote |
| Reconstructible (P3) | Yes | Yes, on the covered half | Yes, but ~63 jobs |
| Counterfactual size | **+158** (mid → mid+senior) | mid-sized, half-blind | ≤ 63, poorly described |
| Trade-off available | **Yes** — salary by band is known | itself | No — Arbeitnow has 0 % salary |
| Confidence | **High** | Medium | Low |

The concrete demo counterfactual, reconstructible from the data as measured:

> **mid only → mid + senior : 154 → 312 opportunities (+158)**

And Direction C's trade-off clause is available for the same move, because salary coverage is
known per band (mid 45 %, senior 58 %) — so the pay delta is computable *and* its coverage is
declarable, which is what P3 requires.

**Salary floor becomes the secondary constraint** — the trade-off half of the story, never the
headline, and every screen showing it must state that it is computed over 44.7 % of the pool.

---

## 6. Recommended archetypes and persona

### Archetypes — keep the top 6, support the next 6, drop the tail

| Tier | Archetypes | Jobs |
|---|---|---:|
| **Core** (full analysis) | Project Manager · Customer Success Manager · Program Manager · Revenue Operations · Data Analyst · Business Analyst | **570** |
| **Supported** (counted, less depth) | Operations Analyst · Implementation Specialist · CS Operations · Implementation Consultant · Business Operations · CS Specialist | 110 |
| **Too thin for a claim** | Product Operations (9) · Project Coordinator (8) | 17 |

Twelve archetypes with real support — inside §7.3's ~10–20 target, and P12-compliant.

### Persona — grounded in the measurement, not invented

The mockup's Maya Okonjo (Product Analyst → Data Scientist, Lagos → Europe, visa, €) fails on
three measured counts: Data Scientist is outside the archetype family, visa is 1.3 % of the
data, and the EU/€ framing rests on Arbeitnow, the source we recommend dropping.

**Recommended persona:** a **mid-level project/operations coordinator** — the constitution's own
§1 protagonist, now with numbers behind them.

The 60-second demo (§4.1) writes itself from the data:

> She searches the title she owns — **Project Coordinator: 8 jobs.**
> Jorbit shows the mid-level band of her real adjacent family — **154 jobs.**
> She relaxes one constraint, seniority, from mid-only to mid-and-senior — **312 jobs (+158)**,
> and the strongest new arrivals are Revenue Operations, Implementation Specialist and Customer
> Success Operations: titles she was never going to type.

That is P2's counterfactual, P3's reconstructibility and §2.1's identity rule in one move, and
every number in it is measured above.

**Note the 8 → 154 step is not a constraint unlock** — it is the taxonomy expansion, and it is
the single most persuasive number the audit produced. It must be labelled as what it is
(*"roles your experience already reaches"*), never folded into an unlock count.

---

## 7. What this audit does *not* settle

- **Skill Unlocks (D13).** Descriptions are ~100 % present and ~7 k chars, so the raw material
  exists. Whether deterministic extraction can distinguish *required* from *preferred* from
  *mentioned* well enough to clear P3 is **untested** — this audit measured field coverage, not
  extraction quality. RK3 stays fully open.
- **Per-posting freshness.** Not measured; needed for P7's cache-age labelling.
- **Licence and attribution terms** per source. §7.1 already flags that no legal review was done.
