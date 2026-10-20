"""Assign random unit codes; write internal sample (name key + URLs) and public sample (codes only)."""
import os, sys, pandas as pd, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
sc = pd.read_csv(os.path.join(DATA, "sample", "schools_drawn_INTERNAL.csv"), dtype=str).fillna("")
ed = pd.read_csv(os.path.join(DATA, "sample", "edtech_drawn_INTERNAL.csv"), dtype=str).fillna("")
PRE = {"S1_CBSE": "CB", "S2_CISCE": "CI", "S3_OTHER": "OT", "S4_GOV_SYSTEM": "GV"}
rows = []
rng = np.random.RandomState(20261019)
for st, g in sc.groupby("stratum"):
    order = rng.permutation(len(g))
    for k, (_, r) in zip(order, g.iterrows()):
        rows.append(dict(unit_id=f"{PRE[st]}-{k+1:03d}", stratum=st, draw_stratum=r.draw_stratum, board=r.board, name=r["name"], state=r.state, district=r.district,
                         address=r.address, url=r.url, hint_url="", city_class=r.city_class, city_basis=r.city_basis, level=r.level, frame_id=r.frame_id, tercile="", n_apps=""))
order = rng.permutation(len(ed))
for k, (_, r) in zip(order, ed.iterrows()):
    rows.append(dict(unit_id=f"ED-{k+1:03d}", stratum="S5_EDTECH", draw_stratum=r.draw_stratum, board="", name=r.seller, state="", district="", address="", url=r.url,
                     hint_url=r.privacy_hint, city_class="", city_basis="", level="", frame_id=r.store_url, tercile=r.tercile, n_apps=r.n_apps))
d = pd.DataFrame(rows).sort_values("unit_id")
d.to_csv(os.path.join(DATA, "sample", "sample_NOT_FOR_PUBLICATION.csv"), index=False, encoding="utf8")
d[["unit_id", "stratum", "draw_stratum", "board", "state", "city_class", "city_basis", "level", "tercile", "n_apps"]].to_csv(os.path.join(DATA, "sample", "sample_public.csv"), index=False)
print(d.stratum.value_counts()); print(len(d))
