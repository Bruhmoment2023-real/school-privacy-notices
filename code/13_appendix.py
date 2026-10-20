"""Builds depth/appendix/data-dictionary.md (row/column counts computed from the files; meanings written here)."""
import os, sys, csv, glob, hashlib
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
def rc(path):
    try:
        d = pd.read_csv(path, dtype=str); return len(d), len(d.columns), list(d.columns)
    except Exception as e: return "?", "?", []
FILES = [
 ("data\\legal\\*.pdf, *.txt", "Official Gazette PDFs (Act 2023; Rules 2025 G.S.R. 846(E); G.S.R. 843(E), 844(E), 845(E)) and pdftotext output. Source: MeitY and egazette.gov.in. Accessed 17 Oct 2026. Hindi text is garbled in the .txt (English only was used).", None),
 ("data\\legal\\LEGAL-CHECKLIST.md", "The coding instrument with verbatim legal text and rules.", None),
 ("data\\frame\\cbse_frame.csv", "CBSE SARAS affiliated-school list, 37 state-wise read-only queries, 17 Oct 2026. aff_no = affiliation number; state, district, level (Middle / Secondary / Senior Secondary), name, address, website (as typed by the school; may be blank, a shared portal, or malformed). Principal names removed. The page states 33,205 schools; 33,204 were parsed.", os.path.join(DATA, "frame", "cbse_frame.csv")),
 ("data\\frame\\cisce_frame.csv", "CISCE School Locator, India, 33 state queries, paginated, 17 Oct 2026. cisce_code, name, state, address, website (a 'Visit Website' link when listed), badges (gender / classification / ICSE / ISC tags). Principal names removed. Only 1,324 of 3,337 list a website.", os.path.join(DATA, "frame", "cisce_frame.csv")),
 ("data\\frame\\osm_frame.csv", "OpenStreetMap amenity=school with website tags in India; Overpass snapshot dated 2026-10-16T21:39Z (ODbL). osm_id, name, website, addr tags (often empty), operator tags, lat/lon (WGS84 degrees).", os.path.join(DATA, "frame", "osm_frame.csv")),
 ("data\\frame\\itunes_apps.csv", "Apple iTunes Search API results, India storefront, Education genre, 66 search terms, up to 200 results per term, 17 Oct 2026. One row per app: seller, seller_url, store_url, rating_count (number of ratings), price, description (first 600 characters).", os.path.join(DATA, "frame", "itunes_apps.csv")),
 ("data\\frame\\frame_summary.csv", "Frame class counts used for stratification and weighting (S1/S2 own-site schools by HRA city class X/Y/Z; excluded classes).", os.path.join(DATA, "frame", "frame_summary.csv")),
 ("data\\frame\\hra_wikitext.json", "Wikipedia wikitext for 'Classification of Indian cities' (HRA X/Y lists), pulled 17 Oct 2026 (CC BY-SA). Secondary source for the official 6th/7th CPC list.", None),
 ("data\\sample\\sample_NOT_FOR_PUBLICATION.csv", "Name key and URLs for the 240 sampled units. NOT FOR PUBLICATION. unit_id (random code), stratum, draw_stratum, board, name, state, district, address, url, hint_url (App Store privacy-policy link), city_class (HRA X/Y/Z), city_basis (which text matched), level, frame_id, tercile (edtech popularity), n_apps.", os.path.join(DATA, "sample", "sample_NOT_FOR_PUBLICATION.csv")),
 ("data\\sample\\sample_enriched_public.csv", "Codes only: stratum, board_final, city_class_final, scope (IN / OUT / UNCERTAIN). No names or URLs.", os.path.join(DATA, "sample", "sample_enriched_public.csv")),
 ("E:\\Research-Staging\\11-school-privacy-notices\\notices\\collection_log.csv", "One row per unit: fetched_at (UTC), start_url, home_status (HTTP code or ERR/ROBOTS), n_anchors, status (FOUND / NOT_FOUND / UNREACHABLE / ROBOTS_BLOCKED / NEEDS_RENDER / RENDER_FAILED), notice_url, content_type, bytes, sha256_raw (SHA-256 of the fetched bytes), sha256_text (of the extracted text), n_words, discovery (homepage_link / path_probe / hint_url / rendered). Contains URLs: NOT FOR PUBLICATION.", os.path.join(NOTICES, "collection_log.csv")),
 ("data\\notices_archive_log_NOT_FOR_PUBLICATION.csv", "Wayback Machine Save Page Now result per notice URL: method, snapshot_url, 14-digit snapshot timestamp (UTC), HTTP code. Contains URLs: NOT FOR PUBLICATION.", os.path.join(DATA, "notices_archive_log_NOT_FOR_PUBLICATION.csv")),
 ("data\\coding\\pass1.csv / pass1_reconciled.csv", "Hand codes (Y / P / N; NA where not applicable; A = descriptive item left to the regex coder), kind (PRIV / TERMS / EMPTY / THIRD_PARTY / NONE / OUT_OF_SCOPE), note (free text; INTERNAL). Items per LEGAL-CHECKLIST.md.", os.path.join(DATA, "coding", "pass1_reconciled.csv")),
 ("data\\coding\\pass2.csv", "Second pass on a random 14 of the coded notices (seed 20261018), same columns. Same agent, same session: intra-coder only.", os.path.join(DATA, "coding", "pass2.csv")),
 ("data\\coding\\auto_codes.csv", "Regex coder output (2 = Y, 1 = P, 0 = N) for every notice found, plus n_words.", os.path.join(DATA, "coding", "auto_codes.csv")),
 ("results\\tables\\unit_level_results_PUBLIC.csv", "Unit-level analysis table with codes only (no names or URLs): stratum, board, city class, crawl status, final status, items (strict _S, lenient _L), core five.", os.path.join(ROOT, "results", "tables", "unit_level_results_PUBLIC.csv")),
]
out = ["# Data dictionary", "", "Counts computed at build time by `code\\13_appendix.py`. Dates are 17 Oct 2026 unless stated. Files marked NOT FOR PUBLICATION identify institutions.", "", "| File | Rows x columns | Meaning, source, access date, known problems |", "|---|---|---|"]
for name, desc, path in FILES:
    if path and os.path.exists(path):
        r, c, cols = rc(path); shape = f"{r} x {c}"
        extra = " Columns: " + ", ".join(cols[:40]) + "." if cols and len(cols) <= 40 else ""
    else: shape, extra = "-", ""
    out.append(f"| `{name}` | {shape} | {desc}{extra} |")
out += ["", "## Variable notes", "- Items D1-D9, K1-K5, S1-S9: see `data\\legal\\LEGAL-CHECKLIST.md`; values Y / P / N.",
        "- `core5_S` = 1 only if D1-D5 are all Y (strict); `core_n_S` = number of D1-D5 coded Y (0-5).",
        "- `fs` (final status): NOTICE (dedicated privacy notice found and coded), PAGE_NOT_A_NOTICE (a page was fetched but is terms-only, navigation-only, a third party's policy, a soft-404 or a parked domain), NOT_FOUND, UNREACHABLE (DNS/connection/HTTP error or robots disallow), UNVERIFIED (JavaScript page that could not be rendered), OUT_OF_SCOPE.",
        "- `city_class_final`: HRA X (Ahmedabad, Bengaluru, Chennai, Delhi, Hyderabad, Kolkata, Mumbai, Pune), Y (about 117 named cities), Z (all else); UNKNOWN for OSM units without address data.",
        "- Known problems: school-listed website fields are free text (typos, shared portals, social pages); OSM units rarely carry addresses; the HRA list is a secondary source; some notices were retrieved from a different domain than the school's (e.g. a vendor-hosted policy).", ""]
open(os.path.join(ROOT, "depth", "appendix", "data-dictionary.md"), "w", encoding="utf8").write("\n".join(out))
print("ok")
