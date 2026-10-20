import requests, json, os, time
OUT = r"D:\Research-Publishing\11-school-privacy-notices\followup\raw\prior"
H = {"User-Agent": "SchoolPrivacyNoticeAudit/0.1 (academic literature search)"}
Q = ["privacy policies Indian edtech apps", "DPDP Act children data schools", "privacy policy content analysis educational technology children",
     "student data privacy India edtech", "COPPA children's apps privacy policy compliance", "privacy policy school websites compliance audit",
     "EdTech products children's rights privacy investigation", "automated privacy policy analysis compliance checklist legal requirements"]
for i, q in enumerate(Q):
    fn = os.path.join(OUT, f"openalex_{i}.json")
    if not os.path.exists(fn):
        for attempt in range(4):
            r = requests.get("https://api.openalex.org/works", params={"search": q, "per-page": 15, "select": "id,doi,title,publication_year,primary_location,cited_by_count,type,authorships"}, headers=H, timeout=60)
            if r.status_code == 200: break
            time.sleep(20 * (attempt + 1))
        json.dump({"q": q, "status": r.status_code, "res": r.json().get("results") if r.ok else None}, open(fn, "w"), indent=1); time.sleep(8)
    fn = os.path.join(OUT, f"s2_{i}.json")
    if not os.path.exists(fn):
        for attempt in range(4):
            r = requests.get("https://api.semanticscholar.org/graph/v1/paper/search", params={"query": q, "limit": 10, "fields": "title,year,venue,externalIds,citationCount,url,abstract"}, headers=H, timeout=60)
            if r.status_code == 200: break
            time.sleep(15 * (attempt + 1))
        json.dump({"q": q, "status": r.status_code, "res": r.json().get("data") if r.ok else None}, open(fn, "w"), indent=1); time.sleep(6)
print("done")
