"""Prior-work searches: Crossref + arXiv + Semantic Scholar (slow, cached). Writes JSON per query."""
import requests, json, os, time, sys, urllib.parse, re
OUT = r"D:\Research-Publishing\11-school-privacy-notices\followup\raw\prior"
H = {"User-Agent": "SchoolPrivacyNoticeAudit/0.1 (academic literature search)"}
Q = ["privacy policy analysis Indian edtech DPDP Act", "Digital Personal Data Protection Act 2023 children verifiable parental consent",
     "privacy policies of educational apps content analysis", "school privacy notices audit compliance data protection",
     "COPPA compliance education apps privacy policy analysis", "India school websites privacy policy DPDP readiness",
     "edtech student data privacy India", "automated analysis privacy policies India GDPR compliance apps",
     "children's privacy policies readability compliance mobile apps", "GDPR privacy notice compliance schools websites audit",
     "Human Rights Watch EdTech children's rights pandemic apps data practices", "Digital Personal Data Protection Act 2023 notice requirements consent critique",
     "privacy policy completeness Indian websites legal requirements", "DPDP Act educational institutions children data"]
def save(name, obj): json.dump(obj, open(os.path.join(OUT, name), "w", encoding="utf8"), indent=1)
for i, q in enumerate(Q):
    fn = f"crossref_{i}.json"
    if not os.path.exists(os.path.join(OUT, fn)):
        r = requests.get("https://api.crossref.org/works", params={"query.bibliographic": q, "rows": 12, "select": "DOI,title,author,issued,container-title,type,URL,abstract"}, headers=H, timeout=60)
        save(fn, {"q": q, "items": r.json()["message"]["items"] if r.ok else r.status_code}); time.sleep(1.5)
    fn = f"arxiv_{i}.json"
    if not os.path.exists(os.path.join(OUT, fn)):
        r = requests.get("http://export.arxiv.org/api/query", params={"search_query": "all:" + q.replace(" ", "+AND+all:") if False else "all:" + q, "max_results": 8}, headers=H, timeout=60)
        save(fn, {"q": q, "atom": r.text if r.ok else r.status_code}); time.sleep(3.5)
print("done")
