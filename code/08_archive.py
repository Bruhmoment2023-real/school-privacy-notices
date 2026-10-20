"""Archive each collected notice URL with the Internet Archive 'Save Page Now' (anonymous GET, no login).
Falls back to recording the closest existing snapshot from the availability API. Sequential, slow, resumable.
Output: data/notices_archive_log_NOT_FOR_PUBLICATION.csv (contains institution URLs)."""
import csv, os, sys, time, re, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
LOG = os.path.join(NOTICES, "collection_log.csv"); OUT = os.path.join(DATA, "notices_archive_log_NOT_FOR_PUBLICATION.csv")
H = {"User-Agent": UA}
rows = [r for r in csv.DictReader(open(LOG, encoding="utf8")) if r["status"] == "FOUND"]
done = {r["unit_id"] for r in csv.DictReader(open(OUT, encoding="utf8"))} if os.path.exists(OUT) else set()
new = not os.path.exists(OUT)
with open(OUT, "a", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["unit_id", "notice_url", "method", "snapshot_url", "snapshot_ts", "http", "note", "at"])
    if new: w.writeheader()
    for r in rows:
        if r["unit_id"] in done: continue
        u = r["notice_url"]; rec = dict(unit_id=r["unit_id"], notice_url=u, method="", snapshot_url="", snapshot_ts="", http="", note="", at=now_iso())
        try:
            for attempt in range(3):
                resp = requests.get("https://web.archive.org/save/" + u, headers=H, timeout=150, allow_redirects=True)
                rec["http"] = resp.status_code
                if resp.status_code == 429: time.sleep(60 * (attempt + 1)); continue
                break
            loc = resp.headers.get("Content-Location", "") or ""
            m = re.search(r"/web/(\d{14})/", loc) or re.search(r"/web/(\d{14})/", resp.url)
            if resp.status_code == 200 and m:
                rec.update(method="save_page_now", snapshot_ts=m.group(1), snapshot_url="https://web.archive.org" + (loc if loc.startswith("/web/") else "/web/%s/%s" % (m.group(1), u)))
            else:
                a = requests.get("https://archive.org/wayback/available", params={"url": u}, headers=H, timeout=60).json()
                c = (a.get("archived_snapshots") or {}).get("closest")
                if c: rec.update(method="existing_snapshot", snapshot_url=c["url"], snapshot_ts=c["timestamp"], note="SPN http %s" % rec["http"])
                else: rec.update(method="none", note="SPN http %s; no snapshot" % rec["http"])
        except Exception as e:
            rec.update(method="error", note=repr(e)[:150])
        w.writerow(rec); f.flush(); print(rec["unit_id"], rec["method"], rec["http"], flush=True)
        time.sleep(15)
