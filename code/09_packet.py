"""Print a coding packet for one or more units.
Short notices (<= LIMIT words) are printed in full; longer ones get a targeted view: headings, then the paragraphs that match each
checklist item's key terms. Hard-wrapped text is re-flowed into paragraphs first; navigation boilerplate is trimmed.
Usage: python -I 09_packet.py CB-008 CB-009 ... [--full]"""
import os, re, sys, csv, statistics
sys.stdout.reconfigure(encoding="utf8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
LIMIT = 1500; CAP = 12000
TARGET = {
 "DATA/PURPOSE": r"(we|you).{0,30}(collect|provide us|submit|share with us)|information (we|that we) collect|personal (data|information) (includes|such as|may include|we)|categories of|types of (personal|information|data)|purposes?\b|we (use|process)|how we use",
 "WITHDRAW/OPT-OUT": r"withdraw|revoke|opt[- ]?out|unsubscribe",
 "RIGHTS": r"right to|your rights|access, |correct|rectif|erasure|delete your|request.{0,30}(access|delet)",
 "BOARD/REGULATOR": r"data protection board|dpdp|digital personal data|supervisory|regulator|authority|commissioner|complain",
 "OFFICER/CONTACT/GRIEVANCE": r"officer|dpo|grievance|redress|nodal|privacy (team|contact)|within \d+ (working |business )?days|contact us",
 "CHILDREN": r"child|minor|under (the age of )?\d\d|below (the age of )?\d\d|parent|guardian|age of|kids|under 1\d|students? (under|below)",
 "LAWS": r"act,? 20\d\d|information technology|gdpr|coppa|ccpa|ferpa|spdi|rules,? 20\d\d|california|european",
 "RETENTION/SHARING/TRANSFER/BREACH/COOKIES": r"retain|retention|third[- ]part|transfer|outside india|breach|cookie|advertis|track|analytics"}
args = [a for a in sys.argv[1:] if not a.startswith("--")]; full = "--full" in sys.argv
log = {r["unit_id"]: r for r in csv.DictReader(open(os.path.join(NOTICES, "collection_log.csv"), encoding="utf8"))}
def reflow(L0):
    lens = [len(l) for l in L0 if l.strip()] or [0]
    if statistics.median(lens) >= 70: return L0
    out, cur = [], ""
    for l in L0:
        cur = (cur + " " + l.strip()).strip()
        if re.search(r"[.:;?!]$", l.strip()) and len(cur) > 60: out.append(cur); cur = ""
    return out + ([cur] if cur else [])
for uid in args:
    p = os.path.join(NOTICES, uid, "notice.txt")
    if not os.path.exists(p): print("##", uid, "NO NOTICE FILE"); continue
    txt = open(p, encoding="utf8").read(); n = len(txt.split())
    L = reflow(txt.split("\n")); big = [i for i, l in enumerate(L) if len(l.split()) >= 20]
    if big and n > 800: L = L[max(0, big[0] - 3): big[-1] + 6]
    print(f"\n=== {uid} | words={n} | type={log[uid]['content_type'][:25]} ===")
    if n <= LIMIT or full:
        out = "\n".join(L); print(out[:CAP] + ("\n[...CAPPED at %d chars of %d]" % (CAP, len(out)) if len(out) > CAP else ""))
    else:
        print(f"[TARGETED VIEW of a {n}-word notice]"); heads = [l for l in L if 1 <= len(l.split()) <= 9 and not l.endswith((".", ","))]
        print("HEADINGS:", " | ".join(h[:50] for h in heads[:70]))
        for k, pat in TARGET.items():
            hits = [l for l in L if len(l.split()) >= 6 and re.search(pat, l, re.I)]
            print(f"\n-- {k} ({len(hits)} paragraphs; first 6)")
            for l in hits[:6]: print("  *", l[:380])
