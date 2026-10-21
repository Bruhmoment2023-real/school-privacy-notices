"""Main analysis for the privacy-notice audit. Reads sample_enriched_public.csv, collection_log.csv, codes_final_checked.csv, auto_codes.csv.
Writes results/tables/*.csv and results/figures/*.png and prints the headline numbers. Seeded; deterministic.
Definitions are those pre-specified in 02-design.md (strict = Y only; lenient = Y or P)."""
import os, sys, numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
RT = os.path.join(ROOT, "results", "tables"); RF = os.path.join(ROOT, "results", "figures"); os.makedirs(RT, exist_ok=True); os.makedirs(RF, exist_ok=True)
def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0, c - h), min(1, c + h))
def fmt(k, n):
    p, lo, hi = wilson(k, n); return f"{k}/{n} = {p*100:.0f}% [{lo*100:.0f}-{hi*100:.0f}]" if n else "n=0"
# ---------------- build unit table
s = pd.read_csv(os.path.join(DATA, "sample", "sample_enriched_public.csv"), dtype=str).fillna("")
lg = pd.read_csv(os.path.join(NOTICES, "collection_log.csv"), dtype=str).fillna("")[["unit_id", "status", "discovery", "n_words", "content_type"]].rename(columns={"status": "crawl_status"})
# Final codes: pass1_reconciled.csv with the 13 corrections from the full check of the 19 school notices
# (checks/, data/coding/check_changes_log.csv). pass1_reconciled.csv itself is kept unchanged.
cd = pd.read_csv(os.path.join(DATA, "coding", "codes_final_checked.csv"), dtype=str).fillna("")
au = pd.read_csv(os.path.join(DATA, "coding", "auto_codes.csv")).set_index("unit_id")
u = s.merge(lg, on="unit_id", how="left").merge(cd, on="unit_id", how="left")
SIT = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8a", "D8b", "D9", "K1", "K2a", "K3", "K4", "K5"]
core = ["D1", "D2", "D3", "D4", "D5"]
# resolve 'A' descriptors with regex coder
for it, col in (("S3", "S3"), ("S4", "S4"), ("S5", "S5"), ("S6", "S6"), ("S7", "S7"), ("S8", "S8")):
    u[it] = [("Y" if au.loc[x, col] == 2 else "N") if (isinstance(x, str) and x in au.index and v == "A") else v for x, v in zip(u.unit_id, u[it])]
def final_status(r):
    if r.scope == "OUT": return "OUT_OF_SCOPE"
    cs, k = r.crawl_status, r.kind
    if cs == "FOUND": return "NOTICE" if k == "PRIV" else "PAGE_NOT_A_NOTICE"
    if cs in ("NOT_FOUND", "NOT_FOUND_AFTER_RENDER"): return "NOT_FOUND"
    if cs in ("UNREACHABLE", "ROBOTS_BLOCKED"): return "UNREACHABLE"
    return "UNVERIFIED"      # NEEDS_RENDER / RENDER_FAILED
u["fs"] = u.apply(final_status, axis=1)
u["verified"] = u.fs.isin(["NOTICE", "PAGE_NOT_A_NOTICE", "NOT_FOUND"])
u["has_notice"] = (u.fs == "NOTICE").astype(int)
for it in SIT:
    u[it + "_S"] = ((u[it] == "Y") & (u.fs == "NOTICE")).astype(int)
    u[it + "_L"] = (u[it].isin(["Y", "P"]) & (u.fs == "NOTICE")).astype(int)
u["core5_S"] = u[[c + "_S" for c in core]].min(axis=1); u["core5_L"] = u[[c + "_L" for c in core]].min(axis=1)
u["core_n_S"] = u[[c + "_S" for c in core]].sum(axis=1)
u["group"] = u.stratum.map({"S1_CBSE": "CBSE", "S2_CISCE": "CISCE", "S3_OTHER": "Other/unknown board", "S4_GOV_SYSTEM": "Govt school systems", "S5_EDTECH": "Edtech/school software"})
u.drop(columns=[c for c in ("note",) if c in u]).to_csv(os.path.join(RT, "unit_level_results_PUBLIC.csv"), index=False)
GROUPS = ["CBSE", "CISCE", "Other/unknown board", "Govt school systems", "Edtech/school software"]
# K2b (threshold is 18) only counts where a threshold is stated (K2a); added to Table 3 after K2a, not to the unit-level file
u["K2b_S"] = ((u.K2a == "Y") & (u.K2b == "Y") & (u.fs == "NOTICE")).astype(int); u["K2b_L"] = (u.K2a.isin(["Y", "P"]) & u.K2b.isin(["Y", "P"]) & (u.fs == "NOTICE")).astype(int)
T3_ITEMS = SIT[:SIT.index("K2a") + 1] + ["K2b"] + SIT[SIT.index("K2a") + 1:] + ["core5"]
# ---------------- Table 1: crawl outcomes
t1 = pd.crosstab(u.group, u.fs).reindex(GROUPS).fillna(0).astype(int); t1["drawn"] = t1.sum(axis=1); t1.to_csv(os.path.join(RT, "T1_crawl_outcomes_by_group.csv")); print(t1)
# ---------------- Table 2: presence among verified
rows = []
for g in GROUPS + ["All schools (S1-S4)", "All units"]:
    d = u[u.verified] if g == "All units" else u[u.verified & (u.group.isin(GROUPS[:4]) if g.startswith("All schools") else (u.group == g))]
    k = int(d.has_notice.sum()); n = len(d); lo = wilson(k, n)
    k2 = int(((d.fs != "NOT_FOUND")).sum()); rows.append(dict(group=g, verified_n=n, dedicated_notice=k, pct=round(lo[0] * 100, 1), ci_lo=round(lo[1] * 100, 1), ci_hi=round(lo[2] * 100, 1), any_privacy_page=k2, pct_any=round(k2 / n * 100, 1) if n else None))
t2 = pd.DataFrame(rows); t2.to_csv(os.path.join(RT, "T2_notice_presence.csv"), index=False); print(t2.to_string())
# ---------------- Table 3: item rates (strict and lenient), among notices and among verified units
rows = []
for g in GROUPS + ["All schools (S1-S4)", "All units"]:
    m = u.group.isin(GROUPS[:4]) if g.startswith("All schools") else (u.group == g if g != "All units" else u.group.notna())
    dn = u[m & (u.fs == "NOTICE")]; dv = u[m & u.verified]
    for it in T3_ITEMS:
        sn = int(dn[it + "_S"].sum()); ln = int(dn[it + "_L"].sum()); sv = int(dv[it + "_S"].sum()); lv = int(dv[it + "_L"].sum())
        a = wilson(sn, len(dn)); b = wilson(sv, len(dv))
        rows.append(dict(group=g, item=it, n_notices=len(dn), strict_among_notices=sn, strict_pct=round(a[0] * 100, 1) if len(dn) else None, s_lo=round(a[1] * 100, 1) if len(dn) else None, s_hi=round(a[2] * 100, 1) if len(dn) else None,
                         lenient_among_notices=ln, n_verified=len(dv), strict_among_verified=sv, strict_ver_pct=round(b[0] * 100, 1) if len(dv) else None, sv_lo=round(b[1] * 100, 1) if len(dv) else None, sv_hi=round(b[2] * 100, 1) if len(dv) else None, lenient_among_verified=lv))
t3 = pd.DataFrame(rows); t3.to_csv(os.path.join(RT, "T3_item_rates.csv"), index=False)
# ---------------- Table 4: presence by city class and board (CBSE+CISCE pooled and separately)
rows = []
sch = u[u.verified & u.group.isin(["CBSE", "CISCE"])]
for g, d in (("CBSE", sch[sch.group == "CBSE"]), ("CISCE", sch[sch.group == "CISCE"]), ("CBSE+CISCE", sch)):
    for c in "XYZ":
        dd = d[d.city_class_final == c]; k = int(dd.has_notice.sum()); n = len(dd); w = wilson(k, n)
        rows.append(dict(group=g, city_class=c, verified_n=n, notices=k, pct=round(w[0] * 100, 1) if n else None, ci_lo=round(w[1] * 100, 1) if n else None, ci_hi=round(w[2] * 100, 1) if n else None,
                         core5_strict=int(dd.core5_S.sum()), mean_core_items=round(dd.core_n_S.mean(), 2) if n else None))
t4 = pd.DataFrame(rows); t4.to_csv(os.path.join(RT, "T4_presence_by_city_class.csv"), index=False); print(t4.to_string())
# ---------------- edtech by App Store popularity tercile (T4b)
rows = []
ed = u[(u.group == "Edtech/school software") & u.verified]
for tr in ["T1_low", "T2_mid", "T3_high"]:
    dd = ed[ed.tercile == tr]; k = int(dd.has_notice.sum()); n = len(dd); w = wilson(k, n); nn_ = dd[dd.fs == "NOTICE"]
    rows.append(dict(tercile=tr, verified_n=n, notices=k, pct=round(w[0] * 100, 1) if n else None, ci_lo=round(w[1] * 100, 1) if n else None, ci_hi=round(w[2] * 100, 1) if n else None,
                     mean_core_items=round(nn_.core_n_S.mean(), 2) if len(nn_) else None, core5_strict=int(nn_.core5_S.sum()), names_DPDP=int((nn_.S1 == "Y").sum()), D5_Board=int(nn_.D5_S.sum()),
                     drawn=int((u.tercile == tr).sum()), unverified=int(((u.tercile == tr) & (u.fs == "UNVERIFIED")).sum())))
pd.DataFrame(rows).to_csv(os.path.join(RT, "T4b_edtech_by_popularity_tercile.csv"), index=False); print(pd.DataFrame(rows).to_string())
# ---------------- frame-weighted school estimates (CBSE, CISCE cells X/Y/Z)
fs_ = pd.read_csv(os.path.join(DATA, "frame", "frame_summary.csv"))
def N(frame, c): return int(fs_[(fs_.frame == frame) & (fs_["class"] == c)].n.iloc[0])
rows = []
for outcome in ("has_notice", "core5_S"):
    est = {}
    for lab, groups, frames in (("CBSE", ["CBSE"], ["CBSE_S1_OWN_SITE_by_city"]), ("CISCE", ["CISCE"], ["CISCE_S2_OWN_SITE_by_city"]), ("CBSE+CISCE", ["CBSE", "CISCE"], ["CBSE_S1_OWN_SITE_by_city", "CISCE_S2_OWN_SITE_by_city"])):
        num = 0; den = 0; var = 0
        cells = []
        for gname, fr in zip(groups, frames):
            for c in "XYZ":
                d = u[u.verified & (u.group == gname) & (u.city_class_final == c)]
                if len(d) < 2: continue
                Nh = N(fr, c); p = d[outcome].mean(); cells.append((Nh, p, len(d)))
        den = sum(x[0] for x in cells); num = sum(x[0] * x[1] for x in cells); var = sum((x[0] / den) ** 2 * x[1] * (1 - x[1]) / max(x[2] - 1, 1) for x in cells)
        p = num / den; se = var ** 0.5
        rows.append(dict(outcome=outcome, frame=lab, weighted_pct=round(p * 100, 1), ci_lo=round(max(0, p - 1.96 * se) * 100, 1), ci_hi=round(min(1, p + 1.96 * se) * 100, 1), frame_N=den))
t5 = pd.DataFrame(rows); t5.to_csv(os.path.join(RT, "T5_frame_weighted_school_estimates.csv"), index=False); print(t5.to_string())
# ---------------- tests
tests = []
def fisher(lab, a, b):
    k1, n1, k2, n2 = int(a.sum()), len(a), int(b.sum()), len(b)
    if min(n1, n2) == 0: return
    o, p = stats.fisher_exact([[k1, n1 - k1], [k2, n2 - k2]]); tests.append(dict(test=lab, group1=f"{k1}/{n1}", group2=f"{k2}/{n2}", odds_ratio=round(o, 2) if np.isfinite(o) else None, p=p))
v = u[u.verified]
fisher("H1 notice presence: edtech vs all schools", v[v.group == "Edtech/school software"].has_notice, v[v.group.isin(GROUPS[:4])].has_notice)
fisher("notice presence: CBSE vs CISCE", v[v.group == "CBSE"].has_notice, v[v.group == "CISCE"].has_notice)
fisher("H6 notice presence: class X vs class Z (CBSE+CISCE)", v[v.group.isin(["CBSE", "CISCE"]) & (v.city_class_final == "X")].has_notice, v[v.group.isin(["CBSE", "CISCE"]) & (v.city_class_final == "Z")].has_notice)
fisher("H6b notice presence: class X vs Y+Z (CBSE+CISCE)", v[v.group.isin(["CBSE", "CISCE"]) & (v.city_class_final == "X")].has_notice, v[v.group.isin(["CBSE", "CISCE"]) & (v.city_class_final.isin(["Y", "Z"]))].has_notice)
fisher("H3 core five met: edtech vs all schools", v[v.group == "Edtech/school software"].core5_S, v[v.group.isin(GROUPS[:4])].core5_S)
nn = u[u.fs == "NOTICE"]
fisher("D5 Board named (strict): edtech notices vs school notices", nn[nn.group == "Edtech/school software"].D5_S, nn[nn.group.isin(GROUPS[:4])].D5_S)
fisher("K4 parent verification (strict): edtech vs school notices", nn[nn.group == "Edtech/school software"].K4_S, nn[nn.group.isin(GROUPS[:4])].K4_S)
fisher("S1 names DPDP: edtech vs school notices", (nn[nn.group == "Edtech/school software"].S1 == "Y").astype(int), (nn[nn.group.isin(GROUPS[:4])].S1 == "Y").astype(int))
kw = stats.kruskal(*[v[v.group == g].core_n_S for g in GROUPS if (v.group == g).sum() > 1]); tests.append(dict(test="Kruskal-Wallis core items met (0-5) across groups (all verified units)", group1="", group2="", odds_ratio=None, p=kw.pvalue))
tt = pd.DataFrame(tests); tt["p_holm"] = np.nan
conf = tt.test.str.startswith("H"); ps = tt.loc[conf, "p"].values; order = np.argsort(ps); holm = np.empty(len(ps)); run = 0
for r, i in enumerate(order): run = max(run, min(1, (len(ps) - r) * ps[i])); holm[i] = run
tt.loc[conf, "p_holm"] = holm; tt.to_csv(os.path.join(RT, "T6_tests.csv"), index=False); print(tt.to_string())
# ---------------- template / law descriptors among notices
rows = []
for g in GROUPS + ["All units"]:
    d = nn if g == "All units" else nn[nn.group == g]
    r = dict(group=g, n_notices=len(d), names_DPDP=int((d.S1 == "Y").sum()), cites_IT_Act=int(d.S2.str.contains("IT", na=False).sum()), cites_GDPR_like=int(d.S2.str.contains("GDPR|UK_ICO|Swiss|CCPA|COPPA|CalOPPA|FIP_US|PIPEDA|OAIC", na=False).sum()),
             stated_age_threshold=int((d.K2a == "Y").sum()), threshold_18=int(((d.K2a == "Y") & (d.K2b == "Y")).sum()), threshold_13_or_16=int(((d.K2a == "Y") & (d.K2b == "N")).sum()),
             mentions_children=int((d.K1 == "Y").sum()), parental_consent_Y=int((d.K3 == "Y").sum()), parental_consent_YorP=int(d.K3.isin(["Y", "P"]).sum()), board_named=int((d.D5 == "Y").sum()), grievance_officer_named=int((d.D7 == "Y").sum()))
    rows.append(r)
t7 = pd.DataFrame(rows); t7.to_csv(os.path.join(RT, "T7_law_and_children_descriptors.csv"), index=False); print(t7.T.to_string())
# ---------------- sensitivity
rows = []
base = u[u.verified]
for lab, d in (("base (verified, in scope)", base), ("treat UNVERIFIED as no notice", u[u.verified | (u.fs == "UNVERIFIED")]), ("exclude uncertain-scope edtech", base[base.scope != "UNCERTAIN"]),
               ("treat all PAGE_NOT_A_NOTICE as notices", None)):
    if d is None:
        d = base.copy(); d["has_notice"] = (d.fs.isin(["NOTICE", "PAGE_NOT_A_NOTICE"])).astype(int)
    for g in GROUPS:
        dd = d[d.group == g]; k = int(dd.has_notice.sum()); n = len(dd); w = wilson(k, n)
        rows.append(dict(scenario=lab, group=g, n=n, notices=k, pct=round(w[0] * 100, 1) if n else None, lo=round(w[1] * 100, 1) if n else None, hi=round(w[2] * 100, 1) if n else None))
pd.DataFrame(rows).to_csv(os.path.join(RT, "T8_sensitivity_presence.csv"), index=False)
# ---------------- figures
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=220)
d = t2[t2.group.isin(GROUPS)].reset_index(drop=True); y = np.arange(len(d))[::-1]
ax.barh(y, d.pct, color="#4C78A8", height=0.6, xerr=[d.pct - d.ci_lo, d.ci_hi - d.pct], error_kw=dict(ecolor="#222", capsize=3, lw=1))
for yi, (_, r) in zip(y, d.iterrows()): ax.text(min(r.ci_hi, 99) + 1.5, yi, f"{int(r.dedicated_notice)}/{int(r.verified_n)}", va="center", fontsize=8)
ax.set_yticks(y); ax.set_yticklabels(d.group); ax.set_xlim(0, 112); ax.set_xlabel("Units with a dedicated privacy notice (% of reachable units, Wilson 95% CI)")
ax.set_title("Fig 1. Dedicated privacy notice found, by stratum"); plt.tight_layout(); plt.savefig(os.path.join(RF, "fig1_notice_presence_by_group.png")); plt.close()
# fig 2: item heatmap among notices
items = SIT; mat = []
for g in GROUPS:
    dn = nn[nn.group == g]; mat.append([dn[i + "_S"].mean() * 100 if len(dn) else np.nan for i in items])
fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=220)
im = ax.imshow(np.array(mat), cmap="Blues", vmin=0, vmax=100, aspect="auto")
ax.set_xticks(range(len(items))); ax.set_xticklabels(items, rotation=45, ha="right"); ax.set_yticks(range(len(GROUPS))); ax.set_yticklabels([f"{g} (n={len(nn[nn.group==g])})" for g in GROUPS])
for i in range(len(GROUPS)):
    for j in range(len(items)):
        if not np.isnan(mat[i][j]): ax.text(j, i, f"{mat[i][j]:.0f}", ha="center", va="center", fontsize=7, color="white" if mat[i][j] > 55 else "black")
plt.colorbar(im, ax=ax, label="% of notices meeting item (strict)"); ax.set_title("Fig 2. Checklist items met (strict) among units with a notice"); plt.tight_layout(); plt.savefig(os.path.join(RF, "fig2_item_heatmap.png")); plt.close()
# fig 3: presence by city class
fig, ax = plt.subplots(figsize=(5.2, 3.4), dpi=220)
d = t4[t4.group == "CBSE+CISCE"]; x = np.arange(3)
ax.bar(x, d.pct, yerr=[d.pct - d.ci_lo, d.ci_hi - d.pct], color="#F58518", capsize=3, width=0.55)
for xi, (_, r) in zip(x, d.iterrows()): ax.text(xi, r.ci_hi + 2, f"{int(r.notices)}/{int(r.verified_n)}", ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(["X (8 metros)", "Y (tier-2)", "Z (other)"]); ax.set_ylim(0, 100); ax.set_ylabel("% with dedicated notice"); ax.set_title("Fig 3. CBSE+CISCE schools: notice presence by city class"); plt.tight_layout(); plt.savefig(os.path.join(RF, "fig3_presence_by_city_class.png")); plt.close()
# fig 4: number of core items met
fig, ax = plt.subplots(figsize=(6, 3.4), dpi=220)
bottom = np.zeros(6); cols = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#9D755D"]
w = 0.16
for gi, g in enumerate(GROUPS):
    dd = v[v.group == g]; cnt = np.array([(dd.core_n_S == k).sum() for k in range(6)]) / max(len(dd), 1) * 100
    ax.bar(np.arange(6) + (gi - 2) * w, cnt, width=w, label=f"{g} (n={len(dd)})", color=cols[gi])
ax.set_xlabel("Core items D1-D5 met (strict), of 5"); ax.set_ylabel("% of reachable units"); ax.legend(fontsize=6.5, frameon=False); ax.set_title("Fig 4. Distribution of core-item score"); plt.tight_layout(); plt.savefig(os.path.join(RF, "fig4_core_score_distribution.png")); plt.close()
print("done")
