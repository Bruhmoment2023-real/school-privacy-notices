"""Second pass for NEEDS_RENDER units: render JavaScript pages with headless Chrome (--dump-dom; no login, no input, robots.txt honoured).
Edtech units render the App Store privacy-policy URL (hint); school units render the homepage, then the privacy link found in the DOM.
Updates the status/fields of those rows in collection_log.csv in place (a backup is written first)."""
import csv, os, sys, re, subprocess, shutil, importlib.util, tempfile, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
spec = importlib.util.spec_from_file_location("collect", os.path.join(os.path.dirname(os.path.abspath(__file__)), "07_collect.py")); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = r"E:\Research-Staging\11-school-privacy-notices\chrome-profile"
def render(url):
    if not C.robots_ok(url): return None, "robots"
    try:
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", "--virtual-time-budget=9000", f"--user-data-dir={PROFILE}", f"--user-agent={UA}", url],
                           capture_output=True, timeout=170)
        return r.stdout.decode("utf8", "replace"), ""
    except Exception as e: return None, repr(e)[:100]
rows = list(csv.DictReader(open(C.LOG, encoding="utf8")))
shutil.copy(C.LOG, C.LOG + ".bak_before_render")
samp = {r["unit_id"]: r for r in csv.DictReader(open(C.SAMPLE, encoding="utf8"))}
for r in rows:
    if r["status"] != "NEEDS_RENDER": continue
    uid = r["unit_id"]; d = os.path.join(NOTICES, uid); target = samp[uid].get("hint_url") or r["home_final_url"] or r["start_url"]
    html, err = render(target); found = None
    if html and not samp[uid].get("hint_url"):
        ls = C.links(html, target); cands = sorted([(C.rank(u, t), u) for u, t in ls if C.PRIV.search(u) or C.PRIV.search(t)], reverse=True)
        gzip.open(os.path.join(d, "home_rendered.html.gz"), "wt", encoding="utf8").write(html)
        r["n_anchors"] = len(ls)
        if cands:
            target = cands[0][1]; html, err = render(target)
        else: html = None
    if html:
        txt = C.to_text(html.encode("utf8"), "text/html", target)
        if len(txt.split()) >= 40 and re.search(r"privacy|personal (data|information)|data protection", txt, re.I):
            open(os.path.join(d, "notice.raw"), "wb").write(html.encode("utf8")); open(os.path.join(d, "notice.txt"), "w", encoding="utf8").write(txt)
            r.update(notice_url=target, notice_status="200", content_type="text/html (rendered)", bytes=len(html), sha256_raw=sha256_bytes(html.encode("utf8")),
                     sha256_text=sha256_bytes(txt.encode("utf8")), n_words=len(txt.split()), discovery="rendered", status="FOUND")
    if r["status"] != "FOUND": r["status"] = "NOT_FOUND_AFTER_RENDER" if (r.get("n_anchors") and int(r["n_anchors"] or 0) >= 6) else "RENDER_FAILED"
    print(uid, r["status"], target[:70], err, flush=True)
with open(C.LOG, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=C.FIELDS); w.writeheader(); w.writerows(rows)
