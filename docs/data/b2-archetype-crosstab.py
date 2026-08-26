import sys, json
sys.path.insert(0, "C:/Users/ASUS/Desktop/Projects/webMCP-worktrees/audit-job-data/scripts")
from audit_data_coverage import match_archetypes   # reuse, do not redefine
sys.stdout.reconfigure(encoding='utf-8')

S = "C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/"
load = lambda n: json.load(open(S+n, encoding="utf-8"))

def norm_sen(v):
    if not v: return None
    v = str(v).strip().lower()
    m = {"middle":"mid","midweight":"mid","senior":"senior","manager":"manager",
         "director":"director","entry_level":"entry","entry-level, junior":"entry",
         "principal":"principal","executive":"executive","staff":"staff","intern":"intern","any":None}
    return m.get(v)

def rows(src, jobs):
    out = []
    for j in jobs:
        if not isinstance(j, dict): continue
        title = j.get("title") or j.get("position") or j.get("jobTitle") or ""
        arch = match_archetypes(title)
        if not arch: continue
        sen = None
        for k in ("seniority","level","jobLevel","experience_level"):
            if j.get(k): sen = norm_sen(j[k]); break
        smin = j.get("salaryMin") or j.get("annualSalaryMin") or j.get("salary_min")
        remote = j.get("remote")
        out.append({"src":src,"arch":arch,"sen":sen,"sal":bool(smin),"remote":remote})
    return out

all_rows = []
for name, f in [("JobsCollider","jobscollider_raw.json"),("Arbeitnow","arbeitnow_raw.json"),("Jobicy","jobicy_raw.json")]:
    d = load(f)
    jobs = list(d.values()) if isinstance(d, dict) else d
    r = rows(name, jobs)
    all_rows += r
    print(f"{name}: {len(r)} archetype rows")

print(f"\nTOTAL archetype rows: {len(all_rows)}")

from collections import Counter, defaultdict
print("\n--- seniority band across archetype pool ---")
c = Counter(r["sen"] for r in all_rows)
for k, v in c.most_common(): print(f"  {k or 'UNKNOWN':10s} {v:4d}  ({v/len(all_rows)*100:.1f}%)")

print("\n--- structured salary present, archetype pool ---")
sal = sum(1 for r in all_rows if r["sal"])
print(f"  with salary: {sal} / {len(all_rows)}  ({sal/len(all_rows)*100:.1f}%)")

print("\n--- salary present, by seniority band ---")
bysen = defaultdict(lambda: [0,0])
for r in all_rows:
    b = bysen[r["sen"] or "UNKNOWN"]; b[1]+=1
    if r["sal"]: b[0]+=1
for k,(s,t) in sorted(bysen.items(), key=lambda x:-x[1][1]):
    print(f"  {k:10s} {s:4d}/{t:4d}  ({s/t*100:.0f}% have salary)")

print("\n--- archetype x seniority (top archetypes) ---")
ax = defaultdict(Counter)
for r in all_rows:
    for a in ([r["arch"]] if isinstance(r["arch"],str) else r["arch"]):
        ax[a][r["sen"] or "UNK"] += 1
tot = {a: sum(c.values()) for a,c in ax.items()}
for a in sorted(tot, key=lambda x:-tot[x]):
    print(f"  {a:32s} n={tot[a]:4d}  {dict(ax[a].most_common(6))}")
