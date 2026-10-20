"""Extra numbers for RESULTS-SUMMARY.md (printed and saved to results/tables/T10_extra_numbers.csv)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
RT = os.path.join(ROOT, "results", "tables")
def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0, c - h), min(1, c + h))
def f(k, n):
    p, lo, hi = wilson(k, n); return f"{k}/{n} = {p*100:.1f}% [{lo*100:.1f}-{hi*100:.1f}]"
u = pd.read_csv(os.path.join(RT, "unit_level_results_PUBLIC.csv"), dtype=str).fillna("")
N = u[u.fs == "NOTICE"]; E = N[N.group == "Edtech/school software"]; S = N[N.group != "Edtech/school software"]
rows = []
def add(k, v): rows.append((k, v)); print(k, "::", v)
add("units drawn", len(u)); add("units by final status", u.fs.value_counts().to_dict())
V = u[u.verified == "True"]
add("verified units (notice / page-not-a-notice / not found)", len(V))
add("schools verified; with dedicated notice", f(int((V[V.group != "Edtech/school software"].has_notice == "1").sum()), len(V[V.group != "Edtech/school software"])))
for g in ["CBSE", "CISCE", "Other/unknown board", "Govt school systems", "Edtech/school software"]:
    d = u[u.group == g]; add(f"{g}: unreachable share of drawn", f(int((d.fs == "UNREACHABLE").sum()), len(d)))
add("K1 children mentioned among notices (all)", f((N.K1 == "Y").sum(), len(N)))
K1 = N[N.K1 == "Y"]
add("among K1 notices: parental consent Y", f((K1.K3 == "Y").sum(), len(K1))); add("among K1 notices: parental consent Y or P", f(K1.K3.isin(["Y", "P"]).sum(), len(K1)))
add("among K1 notices: verification step Y (strict)", f((K1.K4 == "Y").sum(), len(K1))); add("among K1 notices: verification step Y or P", f(K1.K4.isin(["Y", "P"]).sum(), len(K1)))
T = N[N.K2a == "Y"]; add("age threshold stated", f(len(T), len(N))); add("threshold is 18 (K2b=Y) among stated", f((T.K2b == "Y").sum(), len(T))); add("threshold not 18 among stated", f((T.K2b == "N").sum(), len(T)))
add("names DPDP Act (S1=Y) all notices", f((N.S1 == "Y").sum(), len(N))); add("names DPDP Act edtech notices", f((E.S1 == "Y").sum(), len(E))); add("names DPDP Act school notices", f((S.S1 == "Y").sum(), len(S)))
any_law = E[(E.S1 == "Y") | E.S2.str.contains("IT|GDPR|CCPA|COPPA|UK_ICO|Swiss|PIPEDA|OAIC|UAE|FIP", na=False)]
dp = any_law[any_law.S1 == "Y"]; other = any_law[(any_law.S1 != "Y")]
add("edtech notices naming any law", len(any_law)); add("of those: name DPDP", len(dp)); add("of those: name only IT Act/foreign law (not DPDP)", len(other))
add("notice states a regulator complaint route: Y (Board) / P (any regulator)", f"Y {(N.D5=='Y').sum()}, P {(N.D5=='P').sum()} of {len(N)}")
add("D8b (response period <= 90 days) among notices", f((N.D8b == "Y").sum(), len(N)))
add("core five strict among notices", f((N.core5_S == "1").sum(), len(N))); add("core five lenient among notices", f((N.core5_L == "1").sum(), len(N)))
add("mean core items met (strict) among notices; schools; edtech", f"{N.core_n_S.astype(int).mean():.2f}; {S.core_n_S.astype(int).mean():.2f}; {E.core_n_S.astype(int).mean():.2f}")
add("notices with a date/version shown (regex S7=Y)", f((N.S7 == "Y").sum(), len(N)))
add("notices naming a retention period/practice (regex S3=Y)", f((N.S3 == "Y").sum(), len(N)))
add("kind of pages fetched but not notices", u[u.fs == "PAGE_NOT_A_NOTICE"].kind.value_counts().to_dict())
pd.DataFrame(rows, columns=["metric", "value"]).to_csv(os.path.join(RT, "T10_extra_numbers.csv"), index=False)
