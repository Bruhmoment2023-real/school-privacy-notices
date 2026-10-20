"""Append compact hand codes to a pass file.  Usage: python -I 09b_addcodes.py pass1|pass2 < lines
Line: UNIT kind=PRIV|TERMS|COOKIE|OTHER D1=Y D2=P ... S2=IT,GDPR | note text"""
import sys, os, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
ITEMS = ["kind","D1","D2","D3","D4","D5","D6","D6b","D7","D8a","D8b","D9","K1","K2a","K2b","K3","K4","K5","S1","S2","S3","S4","S5","S6","S7","S8"]
fn = os.path.join(DATA, "coding", sys.argv[1] + ".csv"); os.makedirs(os.path.dirname(fn), exist_ok=True)
new = not os.path.exists(fn); done = {r["unit_id"] for r in csv.DictReader(open(fn, encoding="utf8"))} if not new else set()
with open(fn, "a", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["unit_id"] + ITEMS + ["note"]);
    if new: w.writeheader()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        body, _, note = line.partition("|"); parts = body.split(); uid = parts[0]
        if uid in done: print("skip existing", uid); continue
        row = {k: "" for k in ITEMS}
        for p in parts[1:]:
            k, _, v = p.partition("=")
            assert k in ITEMS, (uid, k)
            row[k] = v
        miss = [k for k in ITEMS if row[k] == ""]
        assert not miss, (uid, "missing", miss)
        row.update(unit_id=uid, note=note.strip()); w.writerow(row)
print("ok")
