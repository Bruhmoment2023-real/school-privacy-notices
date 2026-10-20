"""Collect each sampled unit's public privacy notice (no login, no forms, robots.txt respected).
Input : data/sample/sample_NOT_FOR_PUBLICATION.csv  (unit_id, stratum, url, hint_url)
Output: data/notices/<unit_id>/{home.html.gz, notice.raw, notice.txt}, data/notices/collection_log.csv (resumable)
Usage : python -I 07_collect.py [limit]
Each page is requested once per unit (homepage, then up to 3 candidate notice pages; up to 10 path probes only if
the homepage has no privacy link). TLS is always verified; http:// is tried only if https cannot connect or verify."""
import csv, os, re, sys, time, gzip, io, threading, urllib.parse, urllib.robotparser
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__)); from common import *
SAMPLE = os.path.join(DATA, "sample", "sample_NOT_FOR_PUBLICATION.csv"); OUTD = NOTICES; LOG = os.path.join(OUTD, "collection_log.csv")
os.makedirs(OUTD, exist_ok=True)
FIELDS = ["unit_id","fetched_at","start_url","home_status","home_final_url","robots_allowed","scheme_note","n_anchors","status","notice_url","notice_status","content_type","bytes","sha256_raw","sha256_text","n_words","discovery","other_policy_urls","error"]
lock = threading.Lock(); host_last = {}
def polite(host):
    with lock:
        t = max(time.time(), host_last.get(host, 0) + 1.5); w = t - time.time(); host_last[host] = t
    if w > 0: time.sleep(w)
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5", "Accept-Language": "en-IN,en;q=0.8"})
robots_cache = {}
def robots_ok(url):
    p = urllib.parse.urlparse(url); base = f"{p.scheme}://{p.netloc}"
    if base not in robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            polite(p.netloc); r = S.get(base + "/robots.txt", timeout=(8, 15))
            if r.status_code == 200 and "html" not in r.headers.get("content-type", "").lower()[:20]: rp.parse(r.text.splitlines())
            else: rp.parse([])
        except Exception: rp.parse([])
        robots_cache[base] = rp
    return robots_cache[base].can_fetch(UA, url)
def get(url, maxb=3_000_000):
    note = ""
    for attempt, u in enumerate([url] + ([("http://" + url[8:])] if url.startswith("https://") else [])):
        if not robots_ok(u): return ("ROBOTS", u, "", b"", "robots_disallow")
        try:
            polite(urllib.parse.urlparse(u).netloc)
            r = S.get(u, timeout=(10, 25), stream=True, allow_redirects=True)
            data = r.raw.read(maxb + 1, decode_content=True); r.close()
            return (r.status_code, r.url, r.headers.get("content-type", ""), data[:maxb], note or ("http_fallback" if attempt else ""))
        except requests.exceptions.SSLError: note = "tls_error"
        except Exception as e: note = type(e).__name__
    return ("ERR", url, "", b"", note)
PRIV = re.compile(r"privacy|data[\s_-]*protection|dpdp|personal[\s_-]*(data|information)|gdpr", re.I)
def decode(b, ct=""):
    m = re.search(r"charset=([\w-]+)", ct or "", re.I)
    for enc in ([m.group(1)] if m else []) + ["utf-8", "latin-1"]:
        try: return b.decode(enc)
        except Exception: pass
    return b.decode("utf-8", "replace")
def links(html, base):
    soup = BeautifulSoup(html, "lxml"); out = []
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.startswith(("mailto:", "tel:", "javascript:", "#")): continue
        out.append((urllib.parse.urljoin(base, h), re.sub(r"\s+", " ", a.get_text(" ", strip=True))[:100]))
    return out
def rank(u, t):
    path = urllib.parse.urlparse(u).path.lower(); s = 0
    if re.search(r"privacy", path): s += 6
    if re.search(r"privacy", t, re.I): s += 5
    if re.search(r"data[\s_-]*protection|dpdp", path + " " + t, re.I): s += 3
    if re.search(r"cookie", path + t, re.I): s -= 3
    if re.search(r"\.(jpg|png|zip|docx?)$", path): s -= 9
    return s
def to_text(b, ct, url):
    if "pdf" in ct.lower() or url.lower().split("?")[0].endswith(".pdf") or b[:4] == b"%PDF":
        try:
            import pypdf; rd = pypdf.PdfReader(io.BytesIO(b)); return "\n".join((p.extract_text() or "") for p in rd.pages)[:200000]
        except Exception: return ""
    soup = BeautifulSoup(decode(b, ct), "lxml")
    for t in soup(["script", "style", "noscript", "svg", "iframe"]): t.decompose()
    main = soup.find("main") or soup.find(attrs={"role": "main"}) or soup.find("article")
    node = main if main and len(main.get_text(strip=True)) > 800 else (soup.body or soup)
    lines = [re.sub(r"\s+", " ", l).strip() for l in node.get_text("\n").split("\n")]
    out, prev = [], None
    for l in lines:
        if l and l != prev: out.append(l)
        prev = l
    return "\n".join(out)[:200000]
PATHS = ["/privacy-policy", "/privacy", "/privacy-policy/", "/privacy.html", "/privacy-policy.html", "/privacy_policy", "/policies/privacy-policy", "/legal/privacy", "/privacy-policy.php", "/privacypolicy"]
def run(row):
    uid, url = row["unit_id"], row["url"]; res = dict.fromkeys(FIELDS, ""); res.update(unit_id=uid, start_url=url, fetched_at=now_iso())
    d = os.path.join(OUTD, uid); os.makedirs(d, exist_ok=True)
    try:
        if not url.startswith("http"): url = "https://" + url.lstrip("/")
        cands = []; hint = row.get("hint_url", "")
        st, fu, ct, b, note = get(url)
        res.update(home_status=st, home_final_url=fu, scheme_note=note, robots_allowed="N" if st == "ROBOTS" else "Y")
        if st == 200 and b:
            html = decode(b, ct); gzip.open(os.path.join(d, "home.html.gz"), "wt", encoding="utf8").write(html)
            ls = links(html, fu); res["n_anchors"] = len(ls); seen = set()
            for u, t in ls:
                if u in seen: continue
                seen.add(u)
                if PRIV.search(u) or PRIV.search(t): cands.append((rank(u, t), u, "homepage_link"))
        if hint: cands.append((99, hint, "hint_url"))
        cands.sort(key=lambda x: -x[0])
        if not cands and st == 200:
            base = urllib.parse.urlparse(fu); root = f"{base.scheme}://{base.netloc}"
            for pth in PATHS:
                s2, f2, c2, b2, n2 = get(root + pth, 1_500_000)
                if s2 == 200 and b2 and len(b2) > 800 and (b"privacy" in b2.lower() or b"personal" in b2.lower()):
                    cands.append((1, f2, "path_probe")); break
        for sc, u, how in cands[:3]:
            s2, f2, c2, b2, n2 = get(u)
            if s2 == 200 and b2:
                txt = to_text(b2, c2, f2)
                if len(txt.split()) < 40 or not re.search(r"privacy|personal (data|information)|data protection", txt, re.I): continue
                open(os.path.join(d, "notice.raw"), "wb").write(b2); open(os.path.join(d, "notice.txt"), "w", encoding="utf8").write(txt)
                res.update(notice_url=f2, notice_status=s2, content_type=c2, bytes=len(b2), sha256_raw=sha256_bytes(b2), sha256_text=sha256_bytes(txt.encode("utf8")), n_words=len(txt.split()), discovery=how)
                break
        res["other_policy_urls"] = "|".join(u for _, u, _ in cands[:5])
        if res["sha256_raw"]: res["status"] = "FOUND"
        elif st == "ROBOTS": res["status"] = "ROBOTS_BLOCKED"
        elif st != 200: res["status"] = "UNREACHABLE"
        elif (res["n_anchors"] or 0) < 6: res["status"] = "NEEDS_RENDER"
        else: res["status"] = "NOT_FOUND"
    except Exception as e:
        res["status"] = "ERROR"; res["error"] = repr(e)[:200]
    return res
if __name__ == "__main__":
    rows = list(csv.DictReader(open(SAMPLE, encoding="utf8")))
    done = set(r["unit_id"] for r in csv.DictReader(open(LOG, encoding="utf8"))) if os.path.exists(LOG) else set()
    todo = [r for r in rows if r["unit_id"] not in done]
    if len(sys.argv) > 1: todo = todo[:int(sys.argv[1])]
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf8") as f, ThreadPoolExecutor(4) as ex:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new: w.writeheader()
        for res in ex.map(run, todo):
            w.writerow(res); f.flush(); print(res["unit_id"], res["status"], res["notice_url"][:70], flush=True)
