"""Coding reliability: pass 1 vs pass 2 (14 units, 20% random); regex coder vs pass-1 reconciled. Writes results/tables/reliability_*.csv and prints diffs."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
SC = ["D1","D2","D3","D4","D5","D6","D7","D8a","D8b","D9","K1","K2a","K3","K4","K5"]
M = {"Y": 2, "P": 1, "N": 0}
def load(fn): return pd.read_csv(os.path.join(DATA, "coding", fn), dtype=str).fillna("").set_index("unit_id")
def kappa_ac1(a, b):
    a = np.asarray(a, int); b = np.asarray(b, int); n = len(a)
    po = (a == b).mean(); p1a, p1b = a.mean(), b.mean()
    pe = p1a * p1b + (1 - p1a) * (1 - p1b); k = (po - pe) / (1 - pe) if pe < 1 else np.nan
    pi = (p1a + p1b) / 2; pe_g = 2 * pi * (1 - pi); ac1 = (po - pe_g) / (1 - pe_g) if pe_g < 1 else np.nan
    return po, k, ac1
def boot_ci(a, b, B=2000, seed=1):
    rng = np.random.RandomState(seed); a = np.asarray(a, int); b = np.asarray(b, int); n = len(a)
    if n == 0: return (np.nan, np.nan)
    v = [(a[i] == b[i]).mean() for i in (rng.randint(0, n, n) for _ in range(B))]
    return tuple(np.percentile(v, [2.5, 97.5]))
def compare(x, y, label, outfn):
    ids = x.index.intersection(y.index); rows = []; diffs = []
    allA, allB = [], []
    for it in SC:
        xa = x.loc[ids, it].map(M); ya = y.loc[ids, it] if pd.api.types.is_numeric_dtype(y[it]) else y.loc[ids, it].map(M)
        ok = xa.notna() & ya.notna(); xa, ya = xa[ok], ya[ok]
        exact = (xa == ya).mean(); sb_x, sb_y = (xa == 2).astype(int), (ya == 2).astype(int)
        po, k, ac1 = kappa_ac1(sb_x, sb_y); lo, hi = boot_ci(sb_x, sb_y)
        rows.append(dict(item=it, n=len(xa), exact3=round(exact, 3), agree_strict=round(po, 3), ci_lo=round(lo, 3), ci_hi=round(hi, 3), kappa_strict=round(k, 3) if k == k else None, gwet_ac1=round(ac1, 3) if ac1 == ac1 else None))
        allA += list(sb_x); allB += list(sb_y)
        for u in xa.index[xa != ya]: diffs.append((u, it, {2: "Y", 1: "P", 0: "N"}[xa[u]], {2: "Y", 1: "P", 0: "N"}[ya[u]]))
    po, k, ac1 = kappa_ac1(allA, allB)
    rows.append(dict(item="ALL_ITEMS_POOLED", n=len(allA), exact3=None, agree_strict=round(po, 3), ci_lo=None, ci_hi=None, kappa_strict=round(k, 3), gwet_ac1=round(ac1, 3)))
    pd.DataFrame(rows).to_csv(outfn, index=False); return pd.DataFrame(rows), diffs
os.makedirs(os.path.join(ROOT, "results", "tables"), exist_ok=True)
p1 = load("pass1_reconciled.csv"); p1raw = load("pass1.csv"); p2 = load("pass2.csv"); au = pd.read_csv(os.path.join(DATA, "coding", "auto_codes.csv")).set_index("unit_id")
t, d = compare(p1raw, p2, "pass1raw_vs_pass2", os.path.join(ROOT, "results", "tables", "reliability_pass1raw_vs_pass2.csv")); print(t.to_string()); print("DIFFS raw p1 -> p2:", d)
t2, d2 = compare(p1, p2, "pass1rec_vs_pass2", os.path.join(ROOT, "results", "tables", "reliability_pass1reconciled_vs_pass2.csv")); print(t2.tail(1).to_string()); print("DIFFS rec p1 -> p2:", d2)
t3, d3 = compare(p1, au, "pass1rec_vs_regex", os.path.join(ROOT, "results", "tables", "reliability_regex_vs_pass1reconciled.csv")); print(t3.to_string())
# regex coder against the final (checked) codes used by 11b_analyse.py
fin = load("codes_final_checked.csv")
t4, d4 = compare(fin, au, "final_vs_regex", os.path.join(ROOT, "results", "tables", "reliability_regex_vs_final_checked.csv")); print(t4.to_string())
