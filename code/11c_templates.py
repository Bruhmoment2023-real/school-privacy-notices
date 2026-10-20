"""Template reuse: pairwise 5-word-shingle Jaccard between notice texts (kind PRIV), connected components at >= 0.35 similarity,
plus regex fingerprints of well-known generators. Writes results/tables/T9_template_clusters.csv (codes only)."""
import os, re, sys, itertools
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
RT = os.path.join(ROOT, "results", "tables")
c = pd.read_csv(os.path.join(DATA, "coding", "pass1_reconciled.csv"), dtype=str).fillna("")
ids = list(c[c.kind == "PRIV"].unit_id)
def shingles(t, k=5):
    w = re.findall(r"[a-z0-9]+", t.lower()); return {" ".join(w[i:i + k]) for i in range(0, max(0, len(w) - k + 1))}
S = {u: shingles(open(os.path.join(NOTICES, u, "notice.txt"), encoding="utf8").read()) for u in ids}
pairs = []
for a, b in itertools.combinations(ids, 2):
    if not S[a] or not S[b]: continue
    inter = len(S[a] & S[b]); j = inter / min(len(S[a]), len(S[b]))      # containment of the smaller in the larger
    if j >= 0.35: pairs.append((a, b, round(j, 2)))
parent = {u: u for u in ids}
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
for a, b, j in pairs: parent[find(a)] = find(b)
groups = {}
for u in ids: groups.setdefault(find(u), []).append(u)
FP = {"WordPress default 'suggested text'": r"Suggested text|When visitors leave comments on the site we collect the data shown in the comments form",
      "Privacy-policy generator (Termly/FreePrivacyPolicy style, 'Your/We' capitalised, under-13 clause)": r"has been created with the help of the|Interpretation and Definitions|Collecting and Using Your Personal Data",
      "Apple-style template ('COLLECTION AND USE OF PERSONAL INFORMATION')": r"COLLECTION AND USE OF NON-PERSONAL INFORMATION|Collection and Use of Non-Personal Information",
      "Google AdSense/DART generic policy (CCPA/GDPR block)": r"DoubleClick DART Cookie|DART cookies",
      "Indian coaching-platform template ('Grievance Officer ... Information Technology Act 2000' + 'proper reason' list)": r"We will only collect your Personal (Data|Information) if we have a proper reason",
      "Mobile-app generator ('This SERVICE is provided by ... at no cost')": r"This SERVICE is provided by",
      "COPPA under-13 clause": r"under the age of 13|under 13",
      "GDPR/EU rights block": r"right to (erasure|be forgotten)|data portability|supervisory authority",
      "CCPA block": r"California|CCPA"}
rows = []
for name, pat in FP.items():
    hit = [u for u in ids if re.search(pat, open(os.path.join(NOTICES, u, "notice.txt"), encoding="utf8").read(), re.I)]
    rows.append(dict(kind="fingerprint", label=name, n_notices=len(hit), units="|".join(hit)))
for g, us in groups.items():
    if len(us) > 1: rows.append(dict(kind="text_similarity_cluster", label=f"cluster of {len(us)} (containment >= 0.35)", n_notices=len(us), units="|".join(sorted(us))))
pd.DataFrame(rows).to_csv(os.path.join(RT, "T9_template_clusters.csv"), index=False)
print(pd.DataFrame(rows)[["kind", "label", "n_notices"]].to_string()); print("pairs", len(pairs), "of", len(ids))
