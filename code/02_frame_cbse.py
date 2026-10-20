"""Build CBSE frame from the public SARAS 'List of Affiliated Schools' (state-wise, read-only search).
Keeps: affiliation no., name, state, district, level, address, website. Drops head/principal names.
Raw HTML (contains principal names) is gzipped to data/raw_private (not for publication)."""
import re, os, sys, gzip, time, csv, requests
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__)); from common import *
URL = "https://saras.cbse.gov.in/SARAS/AffiliatedList/ListOfSchdirReport"
s = requests.Session(); s.headers["User-Agent"] = UA
t = s.get(URL, timeout=60).text
tok = re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"', t).group(1)
sel = re.search(r'<select[^>]*id="State".*?</select>', t, flags=re.S).group(0)
states = [(v, re.sub('&amp;', '&', l)) for v, l in re.findall(r'<option value="(\d+)">([^<]*)', sel)]
out = os.path.join(DATA, "frame", "cbse_frame.csv"); rows = []; prov = []
for v, name in states:
    rawp = os.path.join(DATA, "raw_private", f"saras_state_{v}.html.gz")
    if os.path.exists(rawp): html = gzip.open(rawp, "rt", encoding="utf8").read()
    else:
        r = s.post(URL, data={"__RequestVerificationToken": tok, "MainRadioValue": "State_wise", "State": v, "District": "", "Region": "", "SchoolStatusWise": "0", "InstName_orAddress": "", "RegiAffNo": ""}, timeout=120)
        html = r.text; gzip.open(rawp, "wt", encoding="utf8").write(html); time.sleep(4)
        prov.append((v, name, now_iso(), len(r.content), sha256_bytes(r.content)))
    soup = BeautifulSoup(html, "lxml"); n0 = len(rows)
    for tr in soup.select("table tbody tr"):
        txt = tr.get_text("|", strip=True)
        m = re.search(r"Aff\. No\. :\|(\d+)", txt)
        if not m: continue
        def g(k):
            mm = re.search(k + r"\s*:\|?([^|]*)", txt); return mm.group(1).strip() if mm else ""
        lvl = re.search(r"\|((?:Senior Secondary|Secondary|Middle|Primary|Elementary)[^|]*)\|", txt)
        web = re.search(r"Website\s*:\|?([^|]*)", txt)
        rows.append(dict(aff_no=m.group(1), state=name, district=g("District"), level=lvl.group(1) if lvl else "",
                         name=g("Name"), address=g("Address"), website=("" if (not web or web.group(1).strip().lower() in ("view","")) else web.group(1).strip())))
    print(name, len(rows) - n0, flush=True)
with open(out, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
if prov:
    with open(os.path.join(DATA, "frame", "cbse_fetch_log.csv"), "a", newline="") as f:
        csv.writer(f).writerows(prov)
print("total", len(rows), "with website", sum(1 for r in rows if r["website"]))
