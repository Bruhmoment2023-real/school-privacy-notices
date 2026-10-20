"""Edtech/school-ERP frame via the public iTunes Search API (India storefront, software, Education genre). GET only."""
import requests, json, os, sys, csv, time
sys.path.insert(0, os.path.dirname(__file__)); from common import *
TERMS = ["CBSE", "ICSE", "NCERT", "JEE", "NEET", "CBSE class 10", "CBSE class 12", "ICSE class 10", "state board", "Class 9 maths",
 "class 6 learning", "olympiad", "UPSC", "CUET", "SSC exam", "banking exam preparation", "live classes India", "online tuition", "doubt solving",
 "kids learning app India", "kindergarten learning", "phonics", "abacus", "coding for kids", "spoken English India", "Hindi learning", "learn Kannada",
 "learn Tamil", "learn Telugu", "school app parents", "school management", "school ERP", "parent teacher communication", "student attendance fees app",
 "school bus tracking", "homework app", "digital classroom", "NCERT solutions", "textbook solutions", "mock test", "previous year papers",
 "board exam preparation", "CA foundation", "GATE exam", "CLAT", "NEET PG", "competitive exam India", "maths tutor", "science for kids India",
 "learning app for students", "e-learning", "tuition app", "Byju", "Vedantu", "Unacademy", "Physics Wallah", "Toppr", "Doubtnut", "Embibe", "Extramarks", "Teachmint", "LEAD School", "Classplus", "Meritnation", "Khan Academy India", "DIKSHA"]
fn = os.path.join(DATA, "frame", "itunes_raw.json")
raw = json.load(open(fn)) if os.path.exists(fn) else {}
for t in TERMS:
    if t in raw: continue
    for a in range(3):
        r = requests.get("https://itunes.apple.com/search", params={"term": t, "country": "in", "media": "software", "entity": "software", "limit": 200}, headers={"User-Agent": UA}, timeout=60)
        if r.status_code == 200: break
        time.sleep(30)
    raw[t] = r.json().get("results", []) if r.ok else []
    json.dump(raw, open(fn, "w")); print(t, len(raw[t]), flush=True); time.sleep(4)
apps = {}
for t, res in raw.items():
    for a in res:
        if a.get("primaryGenreName") != "Education" and "Education" not in a.get("genres", []): continue
        k = a["trackId"]
        if k not in apps: apps[k] = dict(a, _terms=[t])
        else: apps[k]["_terms"].append(t)
rows = [dict(track_id=k, app=a.get("trackName"), seller=a.get("sellerName"), artist=a.get("artistName"), seller_url=a.get("sellerUrl", ""),
             store_url=a.get("trackViewUrl"), rating_count=a.get("userRatingCount", 0), price=a.get("price"), bundle=a.get("bundleId"),
             content_rating=a.get("contentAdvisoryRating"), n_terms=len(a["_terms"]), description=(a.get("description") or "")[:600].replace("\n", " ")) for k, a in apps.items()]
with open(os.path.join(DATA, "frame", "itunes_apps.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("apps", len(rows), "sellers", len({r["seller"] for r in rows}))
