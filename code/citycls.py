"""HRA-style city size class (X / Y / Z) from address text and district. X = 8 cities; Y = list parsed from the Wikipedia
'Classification of Indian cities' wikitext (saved in data/frame/hra_wikitext.json). Z = everything else. Address match first, district second."""
import re, os, sys, json, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
fn = os.path.join(DATA, "frame", "hra_wikitext.json")
if not os.path.exists(fn):
    r = requests.get("https://en.wikipedia.org/w/api.php", params={"action": "parse", "page": "Classification_of_Indian_cities", "prop": "wikitext", "format": "json"}, headers={"User-Agent": UA}, timeout=60)
    json.dump(r.json(), open(fn, "w"))
wt = json.load(open(fn))["parse"]["wikitext"]["*"]
i = wt.index("|X"); j = wt.index("||Z")
seg = wt[i:j]
xpart, ypart = seg.split("||Y")
def names(s): return [re.sub(r"\s+", " ", m.split("|")[-1]).strip() for m in re.findall(r"\[\[([^\]]+)\]\]", s)]
X = {n.upper() for n in names(xpart)} | {"NEW DELHI", "BANGALORE"}
Y = {n.upper() for n in names(ypart) if "(" not in n and "style" not in n.lower()}
Y -= {"HAMIRPUR"}  # ambiguous: Hamirpur (HP) vs Hamirpur (UP); handled by state
SYN = {"BANGALORE": "BENGALURU", "BANGLORE": "BENGALURU", "BOMBAY": "MUMBAI", "CALCUTTA": "KOLKATA", "MADRAS": "CHENNAI", "GURUGRAM": "GURGAON", "BELGAUM": "BELAGAVI",
       "MYSORE": "MYSURU", "MANGALORE": "MANGALURU", "ALLAHABAD": "PRAYAGRAJ", "TRIVANDRUM": "THIRUVANANTHAPURAM", "COCHIN": "KOCHI", "VIZAG": "VISAKHAPATNAM",
       "BARODA": "VADODARA", "PONDICHERRY": "PUDUCHERRY", "TRICHY": "TIRUCHIRAPPALLI", "CALICUT": "KOZHIKODE", "GREATER NOIDA": "NOIDA", "BELLARY": "BALLARI",
       "GULBARGA": "KALABURAGI", "VIJAYAWADA": "VIJAYAWADA", "HUBLI": "HUBBALLI", "DHARWAD": "HUBBALLI", "PIMPRI": "PIMPRI-CHINCHWAD", "CHINCHWAD": "PIMPRI-CHINCHWAD",
       "BURDWAN": "BARDHAMAN", "TIRUCHIRAPALLI": "TIRUCHIRAPPALLI", "NAVI MUMBAI": "NAVI MUMBAI", "RAJAHMUNDRY": "RAJAMAHENDRAVARAM"}
Y |= {"BALLARI", "HUBBALLI", "BELAGAVI"} - X
def cls(address, district="", state=""):
    a = " " + re.sub(r"[^A-Z0-9 -]", " ", (address or "").upper()) + " "
    d = " " + re.sub(r"[^A-Z0-9 -]", " ", (district or "").upper()) + " "
    if (state or "").upper() in ("DELHI", "NEW DELHI"): return "X", "state"
    def find(txt):
        txt = txt
        for k, v in SYN.items(): txt = re.sub(r"\b%s\b" % re.escape(k), " " + v + " ", txt)
        best = None
        for c in sorted(X | Y, key=len, reverse=True):
            if re.search(r"(?<![A-Z])%s(?![A-Z])" % re.escape(c), txt):
                lvl = "X" if c in X and c != "MUMBAI" or (c == "MUMBAI" and "NAVI MUMBAI" not in txt) else "Y"
                if c == "NAVI MUMBAI": lvl = "Y"
                return lvl, c
        return None
    f = find(a)
    if f: return f[0], "address:" + f[1]
    f = find(d)
    if f: return f[0], "district:" + f[1]
    return "Z", "none"
if __name__ == "__main__":
    print(len(X), sorted(X)); print(len(Y), sorted(Y)[:20])
    for t in [("12 MG ROAD BANGALORE 560001", "", ""), ("SECTOR 5 GURUGRAM HARYANA", "GURGAON", "HARYANA"), ("TADONG GANGTOK", "EAST SIKKIM", ""), ("NAVI MUMBAI MAHARASHTRA", "", ""), ("VILLAGE X", "PUNE", "")]:
        print(t, cls(*t))
