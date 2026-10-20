"""Add board (from the site's own text, S3) and city class (S3) and scope flags to the public sample table. Outputs data/sample/sample_enriched_public.csv"""
import os, sys, re, gzip, csv
import pandas as pd
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import citycls
pub = pd.read_csv(os.path.join(DATA, "sample", "sample_public.csv"), dtype=str).fillna("")
key = pd.read_csv(os.path.join(DATA, "sample", "sample_NOT_FOR_PUBLICATION.csv"), dtype=str).fillna("").set_index("unit_id")
osm = pd.read_csv(os.path.join(DATA, "frame", "osm_frame.csv"), dtype=str).fillna("").set_index("osm_id")
BOARD = [("CISCE", r"\bicse\b|\bisc\b|cisce|council for the indian school certificate"), ("CBSE", r"\bcbse\b|central board of secondary"), ("IB", r"international baccalaureate|\bib (diploma|pyp|myp)|\bibdp\b"),
         ("CAMBRIDGE", r"cambridge|igcse|cais\b"), ("STATE", r"state board|sslc|matriculation|maharashtra state board|samagra|karnataka state|kseeb|tn state|stateboard")]
def home_text(u):
    p = os.path.join(NOTICES, u, "home.html.gz")
    if not os.path.exists(p): return ""
    s = BeautifulSoup(gzip.open(p, "rt", encoding="utf8").read(), "lxml")
    for t in s(["script", "style", "noscript"]): t.decompose()
    return re.sub(r"\s+", " ", s.get_text(" ")).strip()
rows = []
for _, r in pub.iterrows():
    u = r.unit_id; b = r.board; c = r.city_class; cb = r.city_basis
    if r.stratum == "S3_OTHER":
        t = home_text(u).lower(); found = [n for n, pat in BOARD if re.search(pat, t)]
        b = "|".join(found) if found else "UNDETERMINED"
        o = osm.loc[key.loc[u, "frame_id"]]
        txt = (o.city + " " + o.district + " " + o.state + " " + home_text(u)[-2500:]).upper()
        c, cb = citycls.cls(txt, o.district, o.state); cb = "S3:" + cb; c = "UNKNOWN" if cb == "S3:none" else c
    if r.stratum == "S2_CISCE": b = "CISCE"
    scope = "OUT" if u in ("ED-051", "ED-056") else ("UNCERTAIN" if u in ("ED-025", "ED-052") else "IN")
    rows.append(dict(r, board_final=b, city_class_final=c, city_basis_final=cb, scope=scope))
out = pd.DataFrame(rows); out.to_csv(os.path.join(DATA, "sample", "sample_enriched_public.csv"), index=False)
print(out[out.stratum == "S3_OTHER"][["unit_id", "board_final", "city_class_final", "city_basis_final"]].to_string())
