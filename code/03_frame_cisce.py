"""CISCE frame from the public School Locator (GET, state-wise, paginated). Head names are dropped."""
import re, os, sys, csv, gzip, time, requests
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__)); from common import *
B = "https://locate.cisce.org/"
s = requests.Session(); s.headers["User-Agent"] = UA
t = s.get(B, timeout=60).text
tok = re.search(r'name="_token" value="([^"]+)"', t).group(1)
states = ["Andaman and Nicobar Islands","Andhra Pradesh","Telangana","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Chandigarh","New Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Jammu and Kashmir","Ladakh","Karnataka","Kerala","Maharashtra","Meghalaya","Manipur","Madhya Pradesh","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
rows = []
def fetch(st, page):
    rawp = os.path.join(DATA, "raw_private", "cisce_%s_p%d.html.gz" % (re.sub(r"\W+", "_", st), page))
    if os.path.exists(rawp): return gzip.open(rawp, "rt", encoding="utf8").read()
    r = s.get(B + "result", params={"_token": tok, "country": "India", "state": st, "page": page}, timeout=90)
    html = r.text; gzip.open(rawp, "wt", encoding="utf8").write(html); time.sleep(2); return html
def parse(html, st):
    out = []
    soup = BeautifulSoup(html, "lxml")
    for card in soup.select("div.school-card"):
        h = re.sub(r"\s+", " ", card.select_one("h6").get_text(" ", strip=True))
        m = re.match(r"([A-Z]{2}\d+)\s*-\s*(.*)", h)
        if not m: continue
        ps = card.select_one("p.mb-1")
        lines = [re.sub(r"\s+", " ", x).strip() for x in ps.get_text("\n").split("\n") if x.strip()]
        addr = " ".join(lines[1:]) if len(lines) > 1 else ""
        a = [x for x in card.find_all("a") if "website" in x.get_text().lower()]
        badges = [b.get_text(strip=True) for b in card.select("span.badge")]
        out.append(dict(cisce_code=m.group(1), name=m.group(2), state=st, address=addr,
                        website=a[0]["href"].strip() if a and a[0].has_attr("href") else "", badges="|".join(badges)))
    return out
for st in states:
    html = fetch(st, 1); n0 = len(rows); rows += parse(html, st)
    mm = re.search(r"of\s+(\d+)\s+entries", html); tot = int(mm.group(1)) if mm else 0
    for pg in range(2, -(-tot // 10) + 1): rows += parse(fetch(st, pg), st)
    print(st, tot, len(rows) - n0, flush=True)
with open(os.path.join(DATA, "frame", "cisce_frame.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("total", len(rows), "with website", sum(1 for r in rows if r["website"]))
