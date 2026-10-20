"""Hand-screen the literature corpus (1,089 records) by title: writes bibliometrics/data/clean/handscreen_exclusions.json.
Reviewer judgement was applied to the printed title list; this script records it as (a) an explicit list of record indices judged off-topic by eye
and (b) one rule for sub-literatures B and D (records whose title has no privacy / data-protection / consent term are generic education or AI papers)."""
import re, json, os
B = r"D:\Research-Publishing\11-school-privacy-notices\bibliometrics\data\clean"
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(B, "handscreen_titles.tsv"), encoding="utf8")][1:]
EYE = {10: "organisational compliance climate, not notices", 21: "formal-methods policy enforcement language, not notice content", 66: "privacy taxonomy for collaborative systems, not notices", 84: "EHR ontology", 88: "digital-health GDPR toolkit",
       194: "EHR management framework", 295: "digital pHealth ethics, not notices", 309: "health privacy ontology", 347: "summarisation for environmental sustainability",
       413: "research-ethics handbook", 417: "deaf education demographics", 426: "children looked after data resource", 422: "research ethics for family studies", 436: "health-research parental consent", 443: "vaccine survey consent trial", 470: "LGBTQ research ethics",
       497: "HIV trial consent", 500: "HIV adolescent consent", 501: "research consent on violence exposure", 504: "family-planning research IRB", 511: "STD treatment without parental consent (health)", 518: "LGBTQ youth research", 526: "consent to research by mentally ill children",
       533: "mental health screening app pilot", 534: "unrelated education/media topic", 543: "abortion parental involvement laws", 544: "paediatric clinical study", 549: "transgender youth research ethics", 597: "transgender children health", 605: "biobanking",
       631: "metaverse climate education", 653: "health-systems CRM in schools", 673: "school sex surveys", 684: "health data API roadmap", 690: "AI criminal liability", 691: "pharmaceutical regulation", 698: "digital health IDs", 700: "e-health in India",
       706: "pharma patent law", 721: "AI in criminal justice", 767: "AI in criminal justice", 801: "national digital health ecosystem", 808: "thalassemia data ecosystems", 810: "digital health regulation", 860: "digital banking frauds", 865: "health access review",
       868: "digital health privacy frameworks (health, not notices)", 878: "algorithm disclosure and trade", 879: "rural banking service quality", 910: "AI training data trade secrets", 911: "health data interoperability", 917: "forensics AI", 929: "ecological law nexus",
       964: "criminal-investigation privacy", 988: "cyber law for trade", 990: "governmental liability", 1063: "bullying-detection CCTV AI", 599: "AI and children in conflict with law", 600: "juvenile justice AI", 1058: "special-education record consent in autism research"}
KEEP_TERM = re.compile(r"privacy|private|data protection|personal (data|information)|consent|COPPA|FERPA|tracking|surveillance|datafication|data governance|data (rights?|ownership|brokers?|breach\w*|security|literacy|colonial\w*|justice|sovereignty)|confidential|GDPR|DPDP|digital rights|rights? of (the )?child|children'?s? (rights?|data|online)|cyber ?security|protect\w*|ethic\w*", re.I)
ex = {}
for i, r in enumerate(rows):
    oa, sub, title = r[0], r[4], r[6]
    if i in EYE: ex[oa] = "hand-screen (title): " + EYE[i]
    elif sub[0] in "BD" and not KEEP_TERM.search(title): ex[oa] = "hand-screen (title): no privacy / data-protection / consent / ethics term; generic education, AI or child-development paper"
json.dump(ex, open(os.path.join(B, "handscreen_exclusions.json"), "w", encoding="utf8"), indent=1)
print(len(ex), "exclusions;", sum(1 for v in ex.values() if "no privacy" in v), "by rule;", sum(1 for v in ex.values() if "no privacy" not in v), "by eye")
