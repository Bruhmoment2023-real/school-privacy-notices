"""Transparent regex/keyword coder for the checklist in data/legal/LEGAL-CHECKLIST.md.
Written from the coding rules, before the consensus codes were produced. Codes: 2 = Y, 1 = P, 0 = N.
Usage: python -I 10_autocode.py   -> data/coding/auto_codes.csv (one row per notice found)"""
import re, os, sys, csv, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

DATA_ITEMS = {
 "name": r"\bname\b|full name", "address": r"\baddress\b|residential|postal", "email": r"e-?mail", "phone": r"phone|mobile|contact number|telephone",
 "dob_age": r"date of birth|\bdob\b|\bage\b|birth", "gender": r"\bgender\b|\bsex\b", "photo": r"photograph|\bphoto|\bimage|picture|selfie|video", "id": r"aadhaar|aadhar|\bpan\b|passport|id proof|identity (proof|document|card)|identification",
 "academic": r"marks|grades?|academic|report card|result|exam|transcript|school records?", "attendance": r"attendance", "payment": r"payment|fee|bank|card|upi|transaction",
 "device": r"device (id|identifier|information)|\bip address|browser|operating system|imei|advertising id|mac address", "location": r"location|gps|geolocation",
 "login": r"username|user name|password|login|credentials|account", "parent": r"parent|guardian|father|mother", "health": r"health|medical|disabilit",
 "biometric": r"biometric|fingerprint|face", "usage": r"usage (data|information)|log data|clickstream|interaction|pages visited|time spent", "voice": r"voice|audio|microphone", "contacts": r"contact list|contacts", "cookies": r"cookie"}
PURPOSES = {
 "admission": r"admission|enrol", "fees": r"fee|payment|billing|invoice", "attendance": r"attendance", "communication": r"communicat|notif|alert|circular|newsletter|respond to|reply",
 "academic": r"report card|academic record|progress|assessment|examination|result|grading", "personalise": r"personali[sz]", "improve": r"improv|enhanc|develop",
 "provide": r"provid(e|ing) (our|the) (service|app|platform|course|content|product)|deliver|operate|manage your account|account", "marketing": r"marketing|promotion|advertis|offers", "analytics": r"analytic|statistic|research",
 "security": r"security|fraud|abuse|safety|prevent", "legal": r"legal obligation|comply with|applicable law|law enforcement|regulat", "support": r"support|customer service|queries|enquir|grievance", "transport": r"transport|bus", "events": r"event|photograph|publication|website|social media"}
CHANNEL = r"@|e-?mail|write to|click|link|form|portal|setting|dashboard|contact (us|the)|phone|call|helpline|visit|address"
def paras(txt): return [p for p in re.split(r"\n+", txt) if p.strip()]
def window_has(txt, a, b, span=200):
    return re.search(r"(%s)(.{0,%d})(%s)|(%s)(.{0,%d})(%s)" % (a, span, b, b, span, a), txt, re.S | re.I) is not None
def code(txt):
    t = txt.lower(); t1 = re.sub(r"\s+", " ", t); P = [re.sub(r"\s+", " ", p) for p in paras(t)]
    r = {}
    n_items = sum(1 for k, v in DATA_ITEMS.items() if re.search(v, t1))
    cue = re.search(r"(we|school|institution|company)[^.]{0,40}(collect|obtain|gather|receive|store)|information (we|that we|collected)|data (we|that we) collect|personal (information|data) (includes|such as|may include)", t1)
    r["D1"] = 2 if (n_items >= 6 and cue) else 1 if (n_items >= 2 and cue) else 0
    n_pur = sum(1 for k, v in PURPOSES.items() if re.search(v, t1))
    pcue = re.search(r"purpose|we use|used to|used for|use of (your|the) (information|data)|how we use", t1)
    r["D2"] = 2 if (n_pur >= 4 and pcue) else 1 if (n_pur >= 1 and pcue) else 0
    w_re = r"withdraw|revoke|opt[- ]?out|unsubscribe|withdrawal of consent"
    paras_w = [p for p in P if re.search(w_re, p)]
    r["D3"] = 2 if any(re.search(CHANNEL, p) and re.search(r"consent|opt|subscribe|marketing|communication", p) for p in paras_w) else 1 if paras_w else 0
    rights = r"right to (access|correct|rectif|erase|delet|port|object|restrict)|access, (correct|update|rectif)|(correct|update|rectif|erase|delete)[^.]{0,50}(your|personal) (data|information)|request[^.]{0,40}(access|correct|delet|erasure)|(access|review|update|delete) (your|the) (personal )?(information|data)"
    paras_r = [p for p in P if re.search(rights, p)]
    r["D4"] = 2 if any(re.search(CHANNEL, p) for p in paras_r) else 1 if paras_r else 0
    r["D5"] = 2 if re.search(r"data protection board", t1) else 1 if re.search(r"data protection authority|supervisory authority|regulator|information commissioner|attorney general", t1) else 0
    r["D6"] = 2 if sum(c.isascii() and c.isalpha() for c in txt) / max(1, sum(c.isalpha() for c in txt)) > 0.9 else 1
    r["D6b"] = 2 if re.search(r"available in (hindi|tamil|telugu|kannada|marathi|bengali|gujarati|malayalam)|हिन्दी|हिंदी|தமிழ்|తెలుగు|ಕನ್ನಡ", txt, re.I) else 0
    officer = r"data protection officer|\bdpo\b|grievance officer|privacy officer|nodal officer|privacy (team|contact)|data (privacy|protection) (lead|team)"
    near_contact = any(re.search(officer, p) and re.search(r"@|\+?\d[\d\s-]{7,}|e-?mail|phone", p) for p in P)
    r["D7"] = 2 if near_contact else 1 if re.search(r"@[a-z0-9.-]+\.[a-z]{2,}|\+?\d[\d\s-]{9,}", t1) else 0
    gp = [p for p in P if re.search(r"grievance|complaint|redress", p)]
    r["D8a"] = 2 if any(re.search(CHANNEL, p) for p in gp) else 1 if gp else 0
    days = [int(m.group(1)) for p in gp for m in re.finditer(r"within\s+(?:a\s+period\s+of\s+)?(\d{1,3})\s*(?:\(\w+\)\s*)?(?:working\s+|business\s+|calendar\s+)?days?", p)]
    hours = any(re.search(r"within\s+\d+\s*(hours?|hrs)|within (a )?(week|month)", p) for p in gp)
    r["D8b"] = 2 if (any(d <= 90 for d in days) or hours) else 0
    nw = len(txt.split())
    r["D9"] = 2 if nw >= 150 else 1 if nw >= 60 else 0
    r["K1"] = 2 if re.search(r"\bchild(ren)?\b|\bminors?\b|under (the age of )?1\d\b|below (the age of )?1\d\b|under 18|below 18|young (people|users)|kids", t1) else 0
    th = [int(m.group(m.lastindex)) for m in re.finditer(r"(?:under|below|less than|younger than|not (?:yet )?(?:completed|attained|reached)(?: the age of)?)\s*(?:the age of\s*|age\s*)?(\d{1,2})", t1)]
    th = [x for x in th if 5 <= x <= 21]
    r["K2a"] = 2 if th else 0
    r["K2b"] = 2 if (th and 18 in th) else (0 if th else 0)
    cons = [p for p in P if re.search(r"(parent|guardian)", p) and re.search(r"consent|permission|approv|authori[sz]", p)]
    r["K3"] = 2 if any(re.search(r"obtain|requir|prior|before|must|verif|need", p) for p in cons) else 1 if cons else 0
    r["K4"] = 2 if re.search(r"verifiable|verif(y|ied|ication)[^.]{0,80}(parent|guardian|age|identity)|(parent|guardian)[^.]{0,80}verif|age verification|digilocker|digital locker|virtual token|otp", t1) and r["K3"] else 0
    r["K5"] = 2 if re.search(r"(do|does|will|shall)\s+not[^.]{0,80}(track|profile|behaviou?ral|target(ed)? (ads|advertis)|advertis)[^.]{0,80}(child|minor|student|under)|(no|not|never)[^.]{0,30}(behaviou?ral|targeted) advertis", t1) else 0
    r["S1"] = 2 if re.search(r"dpdp|digital personal data protection", t1) else 0
    r["S2_it"] = 2 if re.search(r"information technology act|it act,? 2000|spdi|sensitive personal data or information|reasonable security practices", t1) else 0
    r["S2_gdpr"] = 2 if re.search(r"gdpr|general data protection regulation|european (union|economic)|\beea\b", t1) else 0
    r["S2_us"] = 2 if re.search(r"coppa|children'?s online privacy|ccpa|california|ferpa", t1) else 0
    r["S3"] = 2 if re.search(r"retain|retention|keep (your|the)[^.]{0,40}(for|until)|stored for|delet(e|ed) (after|when|within)", t1) else 0
    r["S4"] = 2 if re.search(r"third[- ]part(y|ies)|service providers?|processors?|share (your|the|with)|partners|affiliates|disclose", t1) else 0
    r["S5"] = 2 if re.search(r"outside (of )?india|transfer[^.]{0,60}(countr|abroad|overseas|international)|cross[- ]border|servers? (located )?(in|outside)", t1) else 0
    r["S6"] = 2 if re.search(r"breach|unauthori[sz]ed (access|disclosure)[^.]{0,80}notif|notify[^.]{0,60}(breach|incident)", t1) else 0
    r["S7"] = 2 if re.search(r"last (updated|modified|revised)|effective (date|from)|updated on|version\s*\d|dated\s*:|\b(20[12]\d)\b", t1) else 0
    r["S8"] = 2 if re.search(r"cookie|google analytics|facebook pixel|tracking technolog|advertis(ing|ers)|ad networks?|web beacon", t1) else 0
    return r
if __name__ == "__main__":
    out = []
    for p in sorted(glob.glob(os.path.join(NOTICES, "*", "notice.txt"))):
        uid = os.path.basename(os.path.dirname(p)); txt = open(p, encoding="utf8").read()
        c = code(txt); c["unit_id"] = uid; c["n_words"] = len(txt.split()); out.append(c)
    os.makedirs(os.path.join(DATA, "coding"), exist_ok=True)
    if out:
        with open(os.path.join(DATA, "coding", "auto_codes.csv"), "w", newline="", encoding="utf8") as f:
            w = csv.DictWriter(f, fieldnames=["unit_id", "n_words"] + [k for k in out[0] if k not in ("unit_id", "n_words")]); w.writeheader(); w.writerows(out)
    print("coded", len(out))
