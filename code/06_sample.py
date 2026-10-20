"""Draw the stratified sample (seed fixed in 02-design.md). Schools only; edtech is drawn in 06b_sample_edtech.py.
Outputs: data/frame/frame_summary.csv, data/sample/schools_drawn.csv (internal)."""
import re, os, sys, csv, collections
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import citycls
SEED = 20261017
rng = np.random.RandomState(SEED)
SOCIAL = re.compile(r"(facebook|instagram|youtube|youtu\.be|linkedin|twitter|x\.com|gmail|yahoo|google\.com|goo\.gl|bit\.ly|whatsapp|wa\.me|play\.google|apple\.com|drive\.google|docs\.google)", re.I)
def clean_url(u):
    u = (u or "").strip().split()[0] if (u or "").strip() else ""
    u = u.replace("\\", "/").rstrip(".,;")
    if not u or "@" in u: return ""
    if not re.match(r"https?://", u, re.I): u = "https://" + u
    return u
def host(u):
    m = re.match(r"https?://([^/?#:]+)", u or "", re.I)
    h = m.group(1).lower().removeprefix("www.") if m else ""
    return h if re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", h) else ""
def regdom(h):
    p = h.split(".")
    if len(p) >= 3 and ".".join(p[-2:]) in ("co.in", "ac.in", "gov.in", "nic.in", "edu.in", "org.in", "net.in", "res.in", "co.uk", "ac.uk", "com.au", "org.uk"): return ".".join(p[-3:])
    return ".".join(p[-2:])
cb = pd.read_csv(os.path.join(DATA, "frame", "cbse_frame.csv"), dtype=str).fillna("")
ci = pd.read_csv(os.path.join(DATA, "frame", "cisce_frame.csv"), dtype=str).fillna("")
osm = pd.read_csv(os.path.join(DATA, "frame", "osm_frame.csv"), dtype=str).fillna("")
for d in (cb, ci, osm):
    d["url"] = d.website.map(clean_url); d["host"] = d.url.map(host); d["reg"] = d.host.map(regdom)
# ---- CBSE
cb["govsys"] = cb.name.str.contains(r"KENDRIYA VIDYALAYA|JAWAHAR NAVODAYA|NAVODAYA VIDYALAYA|SAINIK SCHOOL|ARMY PUBLIC|ARMY SCHOOL|EKLAVYA|PM SHRI", regex=True)
cb["is_gov_domain"] = cb.reg.str.contains(r"(gov\.in|nic\.in|ac\.in|kvs|navodaya|sainik)", regex=True) | cb.host.str.contains("kvs.ac.in|navodaya")
host_n = cb[cb.host != ""].groupby("host").size()
reg_n = cb[cb.reg != ""].groupby("reg").size()
cb["host_n"] = cb.host.map(host_n).fillna(0).astype(int); cb["reg_n"] = cb.reg.map(reg_n).fillna(0).astype(int)
cb["social"] = cb.host.map(lambda h: bool(SOCIAL.search(h)))
cb["kv_family"] = cb.host.str.endswith(".kvs.ac.in")
cb["nv_family"] = cb.host.str.contains("navodaya.gov.in")
def stratum_cbse(r):
    if r.host == "": return "NO_VALID_WEBSITE"
    if r.social: return "SOCIAL_OR_GENERIC_HOST"
    if r.kv_family or r.nv_family: return "S4_GOV_SYSTEM"
    if r.host_n >= 6 and r.is_gov_domain: return "S4_GOV_SYSTEM"
    if r.host_n >= 6: return "S1_CHAIN_OR_PORTAL_HOST"   # private chain host (counted as one unit) or shared portal
    return "S1_OWN_SITE"
cb["frame_class"] = cb.apply(stratum_cbse, axis=1)
cc = cb.apply(lambda r: citycls.cls(r.address, r.district, r.state), axis=1)
cb["city_class"] = [c[0] for c in cc]; cb["city_basis"] = [c[1] for c in cc]
# ---- CISCE
ci["social"] = ci.host.map(lambda h: bool(SOCIAL.search(h)))
ci_n = ci[ci.host != ""].groupby("host").size(); ci["host_n"] = ci.host.map(ci_n).fillna(0).astype(int)
ci["frame_class"] = np.where(ci.host == "", "NO_VALID_WEBSITE", np.where(ci.social, "SOCIAL_OR_GENERIC_HOST", np.where(ci.host_n >= 6, "S2_CHAIN_OR_PORTAL_HOST", "S2_OWN_SITE")))
cc = ci.apply(lambda r: citycls.cls(r.address, "", r.state), axis=1)
ci["city_class"] = [c[0] for c in cc]; ci["city_basis"] = [c[1] for c in cc]
# ---- OSM (exclude hosts seen in CBSE/CISCE frames)
known = set(cb.host) | set(ci.host)
osm["social"] = osm.host.map(lambda h: bool(SOCIAL.search(h)))
osm["in_other_frame"] = osm.host.isin(known)
osm_n = osm[osm.host != ""].groupby("host").size(); osm["host_n"] = osm.host.map(osm_n).fillna(0).astype(int)
osm["frame_class"] = np.where(osm.host == "", "NO_VALID_WEBSITE", np.where(osm.social, "SOCIAL_OR_GENERIC_HOST", np.where(osm.in_other_frame, "IN_CBSE_OR_CISCE_FRAME", np.where(osm.host_n >= 4, "S3_CHAIN_HOST", "S3_OWN_SITE"))))
# ---- summary
summ = []
for nm, d in (("CBSE", cb), ("CISCE", ci), ("OSM", osm)):
    for k, v in d.frame_class.value_counts().items(): summ.append((nm, k, int(v)))
for c in "XYZ":
    summ.append(("CBSE_S1_OWN_SITE_by_city", c, int(((cb.frame_class == "S1_OWN_SITE") & (cb.city_class == c)).sum())))
    summ.append(("CISCE_S2_OWN_SITE_by_city", c, int(((ci.frame_class == "S2_OWN_SITE") & (ci.city_class == c)).sum())))
pd.DataFrame(summ, columns=["frame", "class", "n"]).to_csv(os.path.join(DATA, "frame", "frame_summary.csv"), index=False)
print(pd.DataFrame(summ, columns=["frame", "class", "n"]).to_string())
# ---- draws
def draw(df, n, label, seedshift=0):
    if len(df) <= n: return df.assign(draw_stratum=label)
    idx = np.random.RandomState(SEED + seedshift).permutation(len(df))[:n]
    return df.iloc[idx].assign(draw_stratum=label)
parts = []
for i, (c, n) in enumerate(zip("XYZ", (27, 27, 26))):
    d = cb[(cb.frame_class == "S1_OWN_SITE") & (cb.city_class == c)].sort_values("aff_no")
    parts.append(draw(d, n, f"S1_CBSE_{c}", i).assign(stratum="S1_CBSE", frame_id=lambda x: x.aff_no, board="CBSE"))
for i, (c, n) in enumerate(zip("XYZ", (17, 17, 16))):
    d = ci[(ci.frame_class == "S2_OWN_SITE") & (ci.city_class == c)].sort_values("cisce_code")
    parts.append(draw(d, n, f"S2_CISCE_{c}", 10 + i).assign(stratum="S2_CISCE", frame_id=lambda x: x.cisce_code, board="CISCE"))
d = osm[(osm.frame_class == "S3_OWN_SITE") & (osm.name != "")].sort_values("osm_id")
parts.append(draw(d, 30, "S3_OTHER", 20).assign(stratum="S3_OTHER", frame_id=lambda x: x.osm_id, board="UNKNOWN", city_class="", city_basis="manual_check"))
# S4: one unit per system family: KV (random subdomain), JNV/navodaya (random), plus each shared gov host
s4 = cb[cb.frame_class == "S4_GOV_SYSTEM"].copy()
s4["family"] = np.where(s4.kv_family, "kvs.ac.in", np.where(s4.nv_family, "navodaya.gov.in", s4.host))
fam_rows = []
for j, (fam, g) in enumerate(s4.sort_values("aff_no").groupby("family")):
    r = g.iloc[np.random.RandomState(SEED + 30 + j).randint(len(g))]
    r["family_n"] = len(g); fam_rows.append(r)
s4d = pd.DataFrame(fam_rows)
s4d = s4d.sort_values("family_n", ascending=False).head(20)
parts.append(s4d.assign(draw_stratum="S4_GOV_SYSTEM", stratum="S4_GOV_SYSTEM", frame_id=s4d.aff_no, board="CBSE_or_other_gov"))
out = pd.concat(parts, ignore_index=True)
keep = ["stratum", "draw_stratum", "board", "frame_id", "name", "state", "district", "address", "url", "host", "city_class", "city_basis", "level", "family_n", "host_n"]
for k in keep:
    if k not in out: out[k] = ""
out = out[keep]
out.to_csv(os.path.join(DATA, "sample", "schools_drawn_INTERNAL.csv"), index=False, encoding="utf8")
print(out.groupby(["stratum", "city_class"], dropna=False).size())
print("total school units", len(out))
