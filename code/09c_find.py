"""Show context around regex matches in a notice. Usage: python -I 09c_find.py UNIT "regex" [width] [maxhits]"""
import sys, re, os
sys.stdout.reconfigure(encoding="utf8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
u, pat = sys.argv[1], sys.argv[2]; w = int(sys.argv[3]) if len(sys.argv) > 3 else 150; mx = int(sys.argv[4]) if len(sys.argv) > 4 else 3
t = re.sub(r"\s+", " ", open(os.path.join(NOTICES, u, "notice.txt"), encoding="utf8").read())
hits = list(re.finditer(pat, t, re.I)); print(f"[{u}] {len(hits)} hits for /{pat}/")
for m in hits[:mx]: print("  ...", t[max(0, m.start() - w): m.end() + w], "...")
