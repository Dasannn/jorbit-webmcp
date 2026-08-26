import urllib.request
import json
import ssl
import sys
import time
import re
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'

def get_json_with_retry(url, max_retries=4, delay=1.0):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = delay * (2 ** attempt) + 1.5
                print(f"  [429 Rate Limit] Waiting {wait_time:.1f}s before retrying {url}...")
                time.sleep(wait_time)
            elif e.code == 400 or e.code == 404:
                return {"_error": f"HTTP {e.code}: {e.reason}"}
            else:
                print(f"  [HTTP {e.code}] Retrying in {delay}s...")
                time.sleep(delay)
        except Exception as e:
            print(f"  [Error {e}] Retrying in {delay}s...")
            time.sleep(delay)
    return {"_error": "Max retries exceeded"}

# -------------------------------------------------------------
# 1. FETCH JOBSCOLLIDER
# -------------------------------------------------------------
def fetch_jobscollider():
    print("\n=======================================================")
    print(">>> 1. INGESTING JOBSCOLLIDER")
    print("=======================================================")
    jobs_by_id = {}
    
    # 1. General feed
    for p in range(10):
        url = f"https://jobscollider.com/api/search-jobs?page={p}"
        res = get_json_with_retry(url, delay=0.5)
        if "_error" in res or not res.get("jobs"):
            break
        for job in res.get("jobs", []):
            jid = job.get("id") or job.get("url")
            if jid:
                jobs_by_id[jid] = job
        time.sleep(0.3)
        
    print(f"JC: after general pages (0..{p}), unique jobs = {len(jobs_by_id)}")
    
    # 2. Per category
    categories = [
        'all_others', 'business', 'customer_service', 'cybersecurity', 'data',
        'design', 'devops', 'finance_legal', 'human_resources', 'marketing',
        'product', 'project_management', 'qa', 'sales', 'software_development', 'writing'
    ]
    
    for cat in categories:
        cat_count = 0
        for p in range(10):
            url = f"https://jobscollider.com/api/search-jobs?category={cat}&page={p}"
            res = get_json_with_retry(url, delay=0.5)
            if "_error" in res or not res.get("jobs"):
                break
            jobs = res.get("jobs", [])
            for job in jobs:
                jid = job.get("id") or job.get("url")
                if jid:
                    jobs_by_id[jid] = job
            cat_count += len(jobs)
            time.sleep(0.3)
        print(f"  Category '{cat}': {cat_count} jobs fetched across pages")

    print(f"JC TOTAL UNIQUE JOBS: {len(jobs_by_id)}")
    return list(jobs_by_id.values())

# -------------------------------------------------------------
# 2. FETCH ARBEITNOW
# -------------------------------------------------------------
def fetch_arbeitnow():
    print("\n=======================================================")
    print(">>> 2. INGESTING ARBEITNOW")
    print("=======================================================")
    jobs_by_slug = {}
    visa_slugs = set()
    
    # 1. Standard full feed
    page = 1
    max_pages = 60
    while page <= max_pages:
        url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
        res = get_json_with_retry(url, delay=1.2)
        if "_error" in res:
            print(f"  AN page {page} error: {res['_error']}")
            break
        data = res.get("data", [])
        if not data:
            break
        for job in data:
            slug = job.get("slug") or job.get("url")
            if slug:
                jobs_by_slug[slug] = job
                
        next_link = res.get("links", {}).get("next")
        if not next_link:
            print(f"  AN reached last page at page {page}")
            break
        page += 1
        time.sleep(1.0)
        
    print(f"AN: general feed unique jobs = {len(jobs_by_slug)} across {page} pages")
    
    # 2. Query visa_sponsorship=true feed to identify exact visa offers
    page = 1
    while page <= max_pages:
        url = f"https://www.arbeitnow.com/api/job-board-api?visa_sponsorship=true&page={page}"
        res = get_json_with_retry(url, delay=1.2)
        if "_error" in res:
            print(f"  AN visa page {page} error: {res['_error']}")
            break
        data = res.get("data", [])
        if not data:
            break
        for job in data:
            slug = job.get("slug") or job.get("url")
            if slug:
                visa_slugs.add(slug)
                if slug in jobs_by_slug:
                    jobs_by_slug[slug]["_visa_sponsorship_api_flag"] = True
                else:
                    job["_visa_sponsorship_api_flag"] = True
                    jobs_by_slug[slug] = job
                    
        next_link = res.get("links", {}).get("next")
        if not next_link:
            print(f"  AN visa feed reached last page at page {page}")
            break
        page += 1
        time.sleep(1.0)

    print(f"AN: visa sponsorship offers identified = {len(visa_slugs)}")
    print(f"AN TOTAL UNIQUE JOBS: {len(jobs_by_slug)}")
    return list(jobs_by_slug.values())

# -------------------------------------------------------------
# 3. FETCH JOBICY
# -------------------------------------------------------------
def fetch_jobicy():
    print("\n=======================================================")
    print(">>> 3. INGESTING JOBICY")
    print("=======================================================")
    jobs_by_id = {}
    
    # 1. General feed
    res = get_json_with_retry("https://jobicy.com/api/v2/remote-jobs?count=200", delay=0.5)
    if "_error" not in res and res.get("jobs"):
        for job in res.get("jobs", []):
            jid = str(job.get("id") or job.get("jobSlug"))
            if jid:
                jobs_by_id[jid] = job
    time.sleep(0.5)
    print(f"Jobicy: after general feed, unique jobs = {len(jobs_by_id)}")
    
    # 2. Industries
    industries = [
        'admin-support', 'business', 'copywriting', 'design-multimedia', 'supporting',
        'cybersecurity', 'data-science', 'admin', 'education', 'accounting-finance',
        'healthcare', 'hr', 'legal', 'marketing', 'management', 'project-management',
        'qa-testing', 'seller', 'seo', 'engineering', 'technical-support', 'web-app-design'
    ]
    
    for ind in industries:
        url = f"https://jobicy.com/api/v2/remote-jobs?count=200&industry={ind}"
        res = get_json_with_retry(url, delay=0.5)
        if "_error" not in res and res.get("jobs"):
            count = len(res.get("jobs", []))
            for job in res.get("jobs", []):
                jid = str(job.get("id") or job.get("jobSlug"))
                if jid:
                    jobs_by_id[jid] = job
            print(f"  Industry '{ind}': {count} jobs")
        time.sleep(0.5)

    # 3. Key geographic regions to ensure international depth
    geos = ['usa', 'canada', 'uk', 'europe', 'latam', 'apac', 'emea', 'anywhere']
    for g in geos:
        url = f"https://jobicy.com/api/v2/remote-jobs?count=200&geo={g}"
        res = get_json_with_retry(url, delay=0.5)
        if "_error" not in res and res.get("jobs"):
            count = len(res.get("jobs", []))
            for job in res.get("jobs", []):
                jid = str(job.get("id") or job.get("jobSlug"))
                if jid:
                    jobs_by_id[jid] = job
            print(f"  Geo '{g}': {count} jobs")
        time.sleep(0.5)

    print(f"Jobicy TOTAL UNIQUE JOBS: {len(jobs_by_id)}")
    return list(jobs_by_id.values())

# -------------------------------------------------------------
# ARCHETYPE DEFINITIONS (Constitution §7.3)
# -------------------------------------------------------------
ARCHETYPES = {
    "Project Coordinator": [
        r"\bproject\s+coord",
        r"\bproject\s+assistant\b",
        r"\bproject\s+support\s+officer\b"
    ],
    "Project Manager": [
        r"\bproject\s+manager\b",
        r"\btechnical\s+project\s+manager\b",
        r"\bit\s+project\s+manager\b",
        r"\bdigital\s+project\s+manager\b"
    ],
    "Program Manager": [
        r"\bprogram\s+manager\b",
        r"\btechnical\s+program\s+manager\b",
        r"\btpm\b"
    ],
    "Customer Success Specialist": [
        r"\bcustomer\s+success\s+specialist\b",
        r"\bcustomer\s+success\s+associate\b",
        r"\bcustomer\s+success\s+representative\b",
        r"\bclient\s+success\s+specialist\b"
    ],
    "Customer Success Manager": [
        r"\bcustomer\s+success\s+manager\b",
        r"\bcsm\b",
        r"\bclient\s+success\s+manager\b",
        r"\benterprise\s+customer\s+success\b"
    ],
    "Customer Success Operations": [
        r"\bcustomer\s+success\s+operat",
        r"\bcs\s+ops\b",
        r"\bcustomer\s+operations\b",
        r"\bclient\s+operations\b"
    ],
    "Implementation Specialist": [
        r"\bimplementation\s+specialist\b",
        r"\bonboarding\s+specialist\b",
        r"\bclient\s+onboarding\s+specialist\b",
        r"\btechnical\s+implementation\s+specialist\b"
    ],
    "Implementation Consultant": [
        r"\bimplementation\s+consultant\b",
        r"\bimplementation\s+manager\b",
        r"\bsoftware\s+implementation\b"
    ],
    "Business Operations": [
        r"\bbusiness\s+operat",
        r"\bbizops\b",
        r"\boperations\s+generalist\b"
    ],
    "Product Operations": [
        r"\bproduct\s+operat",
        r"\bproduct\s+ops\b"
    ],
    "Revenue Operations": [
        r"\brevenue\s+operat",
        r"\brevops\b",
        r"\bsales\s+operat",
        r"\bmarketing\s+operat"
    ],
    "Business Analyst": [
        r"\bbusiness\s+analyst\b",
        r"\bbusiness\s+systems\s+analyst\b",
        r"\boperations\s+business\s+analyst\b"
    ],
    "Data Analyst": [
        r"\bdata\s+analyst\b",
        r"\bproduct\s+data\s+analyst\b",
        r"\bmarketing\s+data\s+analyst\b",
        r"\bbusiness\s+intelligence\s+analyst\b",
        r"\bbi\s+analyst\b"
    ],
    "Operations Analyst": [
        r"\boperations\s+analyst\b",
        r"\bprocess\s+analyst\b",
        r"\boperational\s+analyst\b"
    ]
}

def match_archetypes(title):
    t = title.lower()
    matched = []
    for arch, patterns in ARCHETYPES.items():
        for pat in patterns:
            if re.search(pat, t):
                matched.append(arch)
                break
    return matched

# Helper to normalize tags / types from list/dict/str
def normalize_list(val):
    if not val:
        return []
    if isinstance(val, list):
        out = []
        for item in val:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                out.extend([str(v) for v in item.values() if v])
            else:
                out.append(str(item))
        return out
    elif isinstance(val, dict):
        return [str(v) for v in val.values() if v]
    elif isinstance(val, str):
        return [val]
    return []

# -------------------------------------------------------------
# AUDIT FUNCTION
# -------------------------------------------------------------
def audit_dataset(source_name, jobs):
    total = len(jobs)
    print(f"\n=======================================================")
    print(f"AUDIT REPORT: {source_name} (Total Unique Jobs: {total})")
    print(f"=======================================================")
    
    if total == 0:
        return {}
    
    # 1. Description
    has_desc = 0
    desc_lengths = []
    desc_has_html = 0
    for j in jobs:
        desc = ""
        if source_name == "JobsCollider":
            desc = j.get("description") or ""
        elif source_name == "Arbeitnow":
            desc = j.get("description") or ""
        elif source_name == "Jobicy":
            desc = j.get("jobDescription") or j.get("jobExcerpt") or ""
            
        if desc and len(desc.strip()) > 30:
            has_desc += 1
            desc_lengths.append(len(desc))
            if "<p>" in desc or "<br" in desc or "<li>" in desc or "<div" in desc:
                desc_has_html += 1

    # 2. Structured Salary
    has_salary_structured = 0
    has_salary_min = 0
    has_salary_max = 0
    has_currency = 0
    has_period = 0
    salary_samples = []
    
    for j in jobs:
        if source_name == "JobsCollider":
            min_s = j.get("salary_min")
            max_s = j.get("salary_max")
            # In JC, 0 means not provided
            if (min_s and min_s > 0) or (max_s and max_s > 0):
                has_salary_structured += 1
                if min_s and min_s > 0: has_salary_min += 1
                if max_s and max_s > 0: has_salary_max += 1
                has_currency += 1 # JC defaults to USD
                if len(salary_samples) < 5:
                    salary_samples.append(f"${min_s:,} - ${max_s:,} (USD/yr)")
        elif source_name == "Arbeitnow":
            # Check if any salary is in description or tags
            pass
        elif source_name == "Jobicy":
            min_s = j.get("salaryMin")
            max_s = j.get("salaryMax")
            curr = j.get("salaryCurrency")
            period = j.get("salaryPeriod")
            if (min_s and min_s > 0) or (max_s and max_s > 0):
                has_salary_structured += 1
                if min_s and min_s > 0: has_salary_min += 1
                if max_s and max_s > 0: has_salary_max += 1
                if curr: has_currency += 1
                if period: has_period += 1
                if len(salary_samples) < 5:
                    salary_samples.append(f"{curr or '$'}{min_s:,} - {max_s:,} ({period})")

    # 3. Seniority
    has_seniority = 0
    seniority_dist = Counter()
    for j in jobs:
        sen = None
        if source_name == "JobsCollider":
            sen = j.get("seniority")
        elif source_name == "Arbeitnow":
            tags = normalize_list(j.get("tags"))
            types = normalize_list(j.get("job_types"))
            for t in tags + types:
                tl = t.lower()
                if any(x in tl for x in ['senior', 'junior', 'lead', 'entry', 'director', 'principal', 'intern', 'student', 'berufserfahren', 'manager', 'executive']):
                    sen = t
                    break
        elif source_name == "Jobicy":
            sen = j.get("jobLevel")
            
        if sen and str(sen).strip() and str(sen).lower() != "null" and str(sen).lower() != "none":
            has_seniority += 1
            seniority_dist[str(sen).strip()] += 1

    # 4. Remote
    has_remote_field = 0
    is_remote_count = 0
    is_onsite_count = 0
    remote_dist = Counter()
    
    for j in jobs:
        if source_name == "JobsCollider":
            # Remote-only API
            has_remote_field += 1
            is_remote_count += 1
            remote_dist["100% Remote"] += 1
        elif source_name == "Arbeitnow":
            has_remote_field += 1
            rem = j.get("remote")
            if rem is True:
                is_remote_count += 1
                remote_dist["Remote (true)"] += 1
            elif rem is False:
                is_onsite_count += 1
                remote_dist["Onsite/Hybrid (false)"] += 1
            else:
                remote_dist[f"Other ({rem})"] += 1
        elif source_name == "Jobicy":
            has_remote_field += 1
            is_remote_count += 1
            geo = j.get("jobGeo") or "Anywhere"
            remote_dist[f"Remote ({geo})"] += 1

    # 5. Location
    has_location = 0
    location_types = Counter()
    location_samples = []
    
    for j in jobs:
        loc = None
        if source_name == "JobsCollider":
            loc = j.get("locations")
            if loc and isinstance(loc, list) and len(loc) > 0 and loc != [""]:
                has_location += 1
                location_types["Structured Country/Region Array"] += 1
                if len(location_samples) < 5:
                    location_samples.append(", ".join(loc))
        elif source_name == "Arbeitnow":
            loc = j.get("location")
            if loc and str(loc).strip():
                has_location += 1
                location_types["City / Region String"] += 1
                if len(location_samples) < 5:
                    location_samples.append(str(loc).strip())
        elif source_name == "Jobicy":
            loc = j.get("jobGeo")
            if loc and str(loc).strip():
                has_location += 1
                location_types["Geo / Region Tag"] += 1
                if len(location_samples) < 5:
                    location_samples.append(str(loc).strip())

    # 6. Visa Sponsorship
    has_visa_flag = 0
    visa_mention_desc = 0
    
    for j in jobs:
        if source_name == "JobsCollider":
            desc = (j.get("description") or "").lower()
            if "visa sponsorship" in desc or "visa sponsor" in desc:
                visa_mention_desc += 1
        elif source_name == "Arbeitnow":
            # Did it match the visa endpoint or tags?
            if j.get("_visa_sponsorship_api_flag"):
                has_visa_flag += 1
            else:
                tags = [t.lower() for t in normalize_list(j.get("tags"))]
                if "visa sponsorship" in tags or "visa sponsor" in tags:
                    has_visa_flag += 1
            desc = (j.get("description") or "").lower()
            if "visa sponsorship" in desc or "visa sponsor" in desc:
                visa_mention_desc += 1
        elif source_name == "Jobicy":
            desc = (j.get("jobDescription") or "").lower()
            if "visa sponsorship" in desc or "visa sponsor" in desc:
                visa_mention_desc += 1

    # 7. Employment Type
    has_emp_type = 0
    emp_type_dist = Counter()
    
    for j in jobs:
        if source_name == "JobsCollider":
            pass
        elif source_name == "Arbeitnow":
            jt = normalize_list(j.get("job_types"))
            if jt:
                has_emp_type += 1
                for t in jt:
                    emp_type_dist[t] += 1
        elif source_name == "Jobicy":
            jt = normalize_list(j.get("jobType"))
            if jt:
                has_emp_type += 1
                for t in jt:
                    emp_type_dist[t] += 1

    # 8. Categories / Industries / Tags
    categories_dist = Counter()
    for j in jobs:
        if source_name == "JobsCollider":
            cat = j.get("category")
            if cat:
                categories_dist[cat] += 1
        elif source_name == "Arbeitnow":
            tags = normalize_list(j.get("tags"))
            for t in tags:
                categories_dist[t] += 1
        elif source_name == "Jobicy":
            ind = normalize_list(j.get("jobIndustry"))
            for i in ind:
                categories_dist[i] += 1

    # 9. Role Archetype Mapping
    archetype_matches = defaultdict(list)
    jobs_with_any_archetype = set()
    
    for idx, j in enumerate(jobs):
        title = ""
        if source_name == "JobsCollider":
            title = j.get("title") or ""
        elif source_name == "Arbeitnow":
            title = j.get("title") or ""
        elif source_name == "Jobicy":
            title = j.get("jobTitle") or ""
            
        matched = match_archetypes(title)
        if matched:
            jobs_with_any_archetype.add(idx)
            for arch in matched:
                archetype_matches[arch].append(title)

    res = {
        "source": source_name,
        "total_jobs": total,
        "description_pct": round(has_desc / total * 100, 2) if total else 0,
        "description_has_html_pct": round(desc_has_html / total * 100, 2) if total else 0,
        "avg_desc_length": round(sum(desc_lengths) / len(desc_lengths), 1) if desc_lengths else 0,
        "salary_structured_pct": round(has_salary_structured / total * 100, 2) if total else 0,
        "salary_min_pct": round(has_salary_min / total * 100, 2) if total else 0,
        "salary_max_pct": round(has_salary_max / total * 100, 2) if total else 0,
        "salary_samples": salary_samples,
        "seniority_pct": round(has_seniority / total * 100, 2) if total else 0,
        "seniority_distribution": dict(seniority_dist.most_common(10)),
        "remote_field_pct": round(has_remote_field / total * 100, 2) if total else 0,
        "remote_true_pct": round(is_remote_count / total * 100, 2) if total else 0,
        "onsite_true_pct": round(is_onsite_count / total * 100, 2) if total else 0,
        "remote_distribution": dict(remote_dist.most_common(6)),
        "location_pct": round(has_location / total * 100, 2) if total else 0,
        "location_types": dict(location_types),
        "location_samples": location_samples,
        "visa_field_pct": round(has_visa_flag / total * 100, 2) if total else 0,
        "visa_flag_count": has_visa_flag,
        "visa_mention_desc_pct": round(visa_mention_desc / total * 100, 2) if total else 0,
        "visa_mention_desc_count": visa_mention_desc,
        "employment_type_pct": round(has_emp_type / total * 100, 2) if total else 0,
        "employment_type_dist": dict(emp_type_dist.most_common(10)),
        "categories_count": len(categories_dist),
        "top_categories": dict(categories_dist.most_common(15)),
        "archetype_mapping_total_jobs": len(jobs_with_any_archetype),
        "archetype_mapping_pct": round(len(jobs_with_any_archetype) / total * 100, 2) if total else 0,
        "archetype_breakdown": {arch: len(titles) for arch, titles in sorted(archetype_matches.items(), key=lambda x: -len(x[1]))},
        "archetype_sample_titles": {arch: titles[:3] for arch, titles in archetype_matches.items()}
    }
    
    print(f"1. Description: {res['description_pct']}% (Avg length: {res['avg_desc_length']} chars, HTML: {res['description_has_html_pct']}%)")
    print(f"2. Structured Salary: {res['salary_structured_pct']}% (Min: {res['salary_min_pct']}%, Max: {res['salary_max_pct']}%) | Samples: {res['salary_samples']}")
    print(f"3. Seniority: {res['seniority_pct']}% | Top levels: {res['seniority_distribution']}")
    print(f"4. Remote: {res['remote_true_pct']}% remote, {res['onsite_true_pct']}% onsite/hybrid | Dist: {res['remote_distribution']}")
    print(f"5. Location: {res['location_pct']}% | Types: {res['location_types']} | Samples: {res['location_samples']}")
    print(f"6. Visa Sponsorship: explicit flag/field={res['visa_field_pct']}% ({res['visa_flag_count']} jobs), text signal={res['visa_mention_desc_pct']}% ({res['visa_mention_desc_count']} jobs)")
    print(f"7. Employment Type: {res['employment_type_pct']}% | Dist: {res['employment_type_dist']}")
    print(f"8. Categories count: {res['categories_count']} | Top: {list(res['top_categories'].keys())[:5]}")
    print(f"9. Jorbit Archetype Mapped Jobs: {res['archetype_mapping_total_jobs']} ({res['archetype_mapping_pct']}%)")
    print(f"   Breakdown: {res['archetype_breakdown']}")
    
    return res

if __name__ == "__main__":
    # We already have raw files from previous run for JC, let's load or re-fetch
    # Let's load JC, re-fetch Arbeitnow with backoff, and load/refetch Jobicy
    print("Loading / Fetching datasets...")
    
    # JobsCollider: load from scratch if exists or fetch
    try:
        with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/jobscollider_raw.json", "r", encoding="utf-8") as f:
            jc_jobs = json.load(f)
            print(f"Loaded {len(jc_jobs)} JobsCollider jobs from disk.")
    except:
        jc_jobs = fetch_jobscollider()
        with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/jobscollider_raw.json", "w", encoding="utf-8") as f:
            json.dump(jc_jobs, f, indent=2)

    # Arbeitnow: fetch with robust backoff
    an_jobs = fetch_arbeitnow()
    with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/arbeitnow_raw.json", "w", encoding="utf-8") as f:
        json.dump(an_jobs, f, indent=2)

    # Jobicy: load or fetch
    try:
        with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/jobicy_raw.json", "r", encoding="utf-8") as f:
            ji_jobs = json.load(f)
            print(f"Loaded {len(ji_jobs)} Jobicy jobs from disk.")
    except:
        ji_jobs = fetch_jobicy()
        with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/jobicy_raw.json", "w", encoding="utf-8") as f:
            json.dump(ji_jobs, f, indent=2)

    # Run audits
    jc_audit = audit_dataset("JobsCollider", jc_jobs)
    an_audit = audit_dataset("Arbeitnow", an_jobs)
    ji_audit = audit_dataset("Jobicy", ji_jobs)
    
    # Save full summary
    summary = {
        "metadata": {
            "audit_date": "2026-08-26",
            "task": "B2 - Data Coverage Audit (Constitution §11.2)",
            "sources": ["JobsCollider", "Arbeitnow", "Jobicy"]
        },
        "audits": {
            "JobsCollider": jc_audit,
            "Arbeitnow": an_audit,
            "Jobicy": ji_audit
        }
    }
    
    with open("C:/Users/ASUS/.gemini/antigravity-cli/brain/a141a15f-33ed-4263-9270-9a923827fa25/scratch/audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print("\n=======================================================")
    print("ALL AUDITS COMPLETED SUCCESSFULLY! RESULTS IN audit_summary.json")
    print("=======================================================")
