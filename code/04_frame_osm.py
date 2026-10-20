"""OSM frame: amenity=school with a website/contact:website tag inside India (ODbL). Single Overpass query, cached."""
import requests, json, os, sys, csv
sys.path.insert(0, os.path.dirname(__file__)); from common import *
fn = os.path.join(DATA, "frame", "osm_raw.json")
Q = """[out:json][timeout:240];
area["ISO3166-1"="IN"][admin_level=2]->.in;
( nwr["amenity"="school"]["website"](area.in); nwr["amenity"="school"]["contact:website"](area.in); );
out tags center;"""
if not os.path.exists(fn):
    r = requests.post("https://overpass-api.de/api/interpreter", data={"data": Q}, headers={"User-Agent": UA, "Accept": "*/*"}, timeout=300)
    r.raise_for_status(); open(fn, "wb").write(r.content)
d = json.load(open(fn, encoding="utf8"))
print("timestamp", d["osm3s"]["timestamp_osm_base"], "elements", len(d["elements"]))
rows = []
for e in d["elements"]:
    t = e.get("tags", {}); c = e.get("center", {"lat": e.get("lat"), "lon": e.get("lon")})
    rows.append(dict(osm_id=f'{e["type"]}/{e["id"]}', name=t.get("name", ""), website=t.get("website") or t.get("contact:website", ""),
                     city=t.get("addr:city", ""), district=t.get("addr:district", ""), state=t.get("addr:state", ""),
                     operator_type=t.get("operator:type", ""), operator=t.get("operator", ""), isced=t.get("isced:level", ""),
                     lat=c.get("lat"), lon=c.get("lon")))
with open(os.path.join(DATA, "frame", "osm_frame.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows))
