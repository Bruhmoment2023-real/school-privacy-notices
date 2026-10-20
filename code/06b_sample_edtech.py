"""Edtech stratum S5: eligible sellers from the App Store frame, tercile-stratified by total rating count, 20 per tercile.
Then fetch each drawn app's public App Store page (GET) to read the developer's own Privacy Policy and website links (hint URLs)."""
import os, re, sys, time, requests
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
SEED = 20261017
d = pd.read_csv(os.path.join(DATA, "frame", "itunes_apps.csv"), dtype=str).fillna("")
d["rc"] = pd.to_numeric(d.rating_count, errors="coerce").fillna(0)
txt = (d.app + " " + d.description).str.lower()
KW = r"cbse|icse|ncert|\bjee\b|\bneet\b|cuet|upsc|olympiad|\bssc\b|state board|\bindian?\b|class (6|7|8|9|10|11|12)\b|clat|school erp|parent portal"
PVT = r"\bpvt\b|private limited|\(india\)|\bindia\b|\bllp\b"
ORG = r"\bpvt\b|private limited|\bllp\b|\bltd\b|\blimited\b|\binc\b|india|technolog|solution|edu|learning|labs|foundation|trust|society|academy|institute|systems|infotech|software|ventures|services|school"
d["kw"] = txt.str.contains(KW); d["pvt"] = d.seller.str.contains(PVT, case=False); d["org"] = d.seller.str.contains(ORG, case=False)
d["eligible"] = d.org & (d.kw | d.pvt)
s = d[d.eligible].groupby("seller").agg(n_apps=("app", "size"), rc=("rc", "sum"), app=("app", "first"), store_url=("store_url", "first"), seller_url=("seller_url", "first")).reset_index()
s["tercile"] = pd.qcut(s.rc.rank(method="first"), 3, labels=["T1_low", "T2_mid", "T3_high"])
print("eligible sellers", len(s), s.tercile.value_counts().to_dict())
parts = []
for i, t in enumerate(["T1_low", "T2_mid", "T3_high"]):
    g = s[s.tercile == t].sort_values("seller")
    idx = np.random.RandomState(SEED + 40 + i).permutation(len(g))[:20]
    parts.append(g.iloc[idx].assign(draw_stratum="S5_EDTECH_" + t))
out = pd.concat(parts, ignore_index=True)
H = {"User-Agent": UA}; priv, dev = [], []
for u in out.store_url:
    try:
        t = requests.get(u, headers=H, timeout=40).text
        m = re.search(r'href="(https?://[^"]+)"[^>]*>\s*(?:<[^>]*>\s*)*Privacy\s*Policy', t, re.I)
        priv.append(m.group(1) if m else "")
        m = re.search(r'href="(https?://[^"]+)"[^>]*>\s*(?:<[^>]*>\s*)*(?:Developer\s*Website|App\s*Support)', t, re.I)
        dev.append(m.group(1) if m else "")
    except Exception as e:
        priv.append(""); dev.append("")
    time.sleep(3)
out["privacy_hint"] = priv; out["dev_site"] = dev
out["url"] = np.where(out.seller_url != "", out.seller_url, out.dev_site)
out["url"] = [u if u else (p if p else "") for u, p in zip(out.url, out.privacy_hint)]
out.to_csv(os.path.join(DATA, "sample", "edtech_drawn_INTERNAL.csv"), index=False, encoding="utf8")
print(out[["seller", "tercile", "url", "privacy_hint"]].head(10).to_string()); print("with privacy hint", (out.privacy_hint != "").sum(), "with url", (out.url != "").sum(), "of", len(out))
