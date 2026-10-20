# 02 - Design (written before any notice was collected or coded)

Pre-specification date: 17 Oct 2026 (the frames had been downloaded and counted; **no sample had been drawn, no notice fetched, nothing coded** when this file was written). Any later change is logged in section 11.

## 1. Question and scope

Working title: *Readiness baseline: the public privacy notices of Indian schools and edtech services against the DPDP Act 2023 and DPDP Rules 2025 notice and children's-data requirements, seven months before the notice rule starts (13 May 2027).*

Framing constraint (from the Gazette): the Act's s.5, s.8, s.9 and Rules 3, 9, 10, 14 are **not in force until 13 May 2027** (G.S.R. 843(E); Rule 1(4)). The paper measures readiness of the published document, not unlawfulness. Section 7 "legitimate uses" may remove the s.5 notice duty for some school processing; so a missing item is "not ready", never "illegal".

### Research questions
- RQ1 (presence). What share of reachable school websites and edtech services publish a discoverable privacy notice at all?
- RQ2 (content). Among the units with a notice, what share meet each DPDP item (D1-D9, K1-K5 in `data\legal\LEGAL-CHECKLIST.md`), and the "core five" (D1-D5) jointly?
- RQ3 (children). Do notices address children's data in the way s.9 and Rule 10 will require (K1-K5)? Which age threshold do they state?
- RQ4 (template origin). Do notices cite the DPDP Act, or other regimes (IT Act/SPDI Rules 2011, GDPR, COPPA)? (descriptive, S1-S2)
- RQ5 (variation). How do rates differ by unit type (CBSE, CISCE, other-board, government system, edtech), by city size class, and for edtech by app popularity?
- RQ6 (measurement). How reliably can the checklist be coded (second pass on a random 20%; agreement of a transparent regex coder with the consensus)?

### Hypotheses (directional, stated now)
- H1: Fewer than half of reachable school websites (CBSE + CISCE + other) have a discoverable privacy notice; more than 80% of edtech services do.
- H2: Among units with a notice, fewer than 20% meet D5 (mention the Data Protection Board), because the Board and the s.5(1)(iii) route are new.
- H3: Fewer than 10% of all reachable units meet the core five (D1-D5) with strict coding; edtech rate > school rate.
- H4: Among notices, fewer than 15% name the DPDP Act (S1); a majority of edtech notices that name any law name IT Act/SPDI Rules or GDPR/COPPA rather than the DPDP Act.
- H5: Among units with a notice that mention children (K1), fewer than 25% describe a parental-verification step (K4); a non-trivial share state a threshold other than 18 (K2b, a template-origin marker).
- H6: Metro (HRA class X) schools have higher notice presence than class Z schools (one-sided; the sample is sized only to detect a large difference).
- Everything else (board differences, edtech type, school-ERP vs consumer) is exploratory and labelled so.

## 2. Population and sampling frames (all public, all read-only)

Unit = one organisation's public website (school) or one app developer ("seller") plus its web presence (edtech). **Population sampled = organisations with a listed website in the frame**; schools with no website cannot be assessed and are outside it (stated as the main coverage limit).

| Stratum | Frame | Source and access | Inclusion rule |
|---|---|---|---|
| S1 CBSE | CBSE SARAS "List of Affiliated Schools", state-wise, 37 read-only searches on 17 Oct 2026; 33,204 schools parsed (page says 33,205) | `https://saras.cbse.gov.in/SARAS/AffiliatedList/ListOfSchdirReport` | School lists a website; host is not a shared portal (a host shared by 6+ schools is a "system" - see S4); school not Kendriya Vidyalaya/Navodaya (system sites). Unit = unique host. |
| S2 CISCE | CISCE School Locator ("Locate a CISCE Affiliated School"), India, state-wise GET queries | `https://locate.cisce.org/` | Lists a website; same host rules. |
| S3 Other/unknown board | OpenStreetMap `amenity=school` with `website` or `contact:website` in India (Overpass snapshot dated in the file), ODbL | `https://overpass-api.de` | Host not already in S1/S2. Board read from the school's own site (state board, IB, Cambridge, NIOS, CBSE/CISCE not in the lists). |
| S4 Government school systems | Hosts shared by 6+ schools in the CBSE list that are government domains (.gov.in, .nic.in, .ac.in) or KV/JNV systems | derived from the SARAS frame | Census of up to ~20 system hosts (not sampled), each treated as one unit. KV and JNV subdomains share templates, so they enter as one unit each. |
| S5 Edtech and school-software services | Apple App Store India storefront, Education genre, results of 66 fixed search terms (list in `code\05_frame_edtech.py`), public iTunes Search API, 17 Oct 2026 | `https://itunes.apple.com/search` | Seller operates an India-targeted learning, exam-prep or school-management app (description mentions an Indian board, exam, language, school ERP, or the company is Indian by name/domain); unit = distinct seller. Google Play is not used (no public listing API; scraping would breach its terms). |

Known frame limits (to be stated in the paper): SARAS and CISCE list only affiliated schools; state-board and unaffiliated schools are reached only through OSM, a volunteer map biased to cities; the app-store frame only sees apps that match the search terms and sit in the top 200 per term; sellers with several apps appear once.

## 3. Sample

- Total drawn: about 270 units; target 150-300 reachable. Seed fixed in `code\06_sample.py` (seed = 20261017).
- Allocation (before seeing any notice): S1 CBSE 80, S2 CISCE 50, S3 other 30, S4 system sites up to 20 (census), S5 edtech 60 (stratified by total rating count: terciles of the seller's apps, 20 each).
- S1 and S2 stratified by **city-size class**: HRA class X / Y / Z (below), roughly equal allocation (27/27/26 and 17/17/16). Equal allocation oversamples the metros; the pooled school estimate is re-weighted by frame size.
- City class: from the address text and district in the frame, matched to the X (8 cities) and Y (97 cities) lists of the Government of India HRA classification (Wikipedia page "Classification of Indian cities", wikitext revision pulled 17 Oct 2026; the underlying official source is the Department of Expenditure / 6th CPC list, not opened). Everything else = Z. The class is checked by eye for all sampled units.
- **No replacement** of unreachable sites: unreachable units are an outcome and are reported (this avoids biasing the sample toward working sites). Non-response categories: UNREACHABLE (DNS/timeouts/HTTP errors), ROBOTS_BLOCKED, NEEDS_RENDER (JavaScript shell, needs a browser), NOT_FOUND (homepage fine, no notice found).

## 4. Collection protocol

1. Fetch the homepage once (TLS verified; `http://` only if `https://` cannot connect or verify). Respect `robots.txt`. 1.5 s minimum gap per host. No logins, no forms, no JavaScript execution (a limited headless-render fallback is described in `code\README.md` if Chrome is available), no contact with any school or company.
2. Find privacy links: anchors whose href or text matches privacy / data protection / DPDP / personal data / GDPR. If none, probe up to 10 standard paths. Fetch up to the top 3 candidates; accept the first with 40+ words that mentions privacy or personal data.
3. Edtech: the App Store page's own "Privacy Policy" link is tried first (hint URL), then the company site.
4. Save: raw bytes, extracted text, SHA-256 of both, URL, final URL, content type, timestamp (UTC). Archive: Wayback "Save Page Now" request for each accepted notice URL (GET to `web.archive.org/save/<url>`, no login), recording the snapshot URL, or "existing snapshot" from the availability API.
5. A unit with no accepted notice is stored with its homepage HTML, anchor count and probe results, so that "not found" is auditable.

## 5. Coding protocol

- Instrument: `data\legal\LEGAL-CHECKLIST.md` (items D1-D9, K1-K5; descriptors S1-S9), with written Y / P / N rules. Strict = Y only; lenient = Y or P.
- Coders: **Coder A** = the analyst agent (Claude), pass 1, reading the whole notice text with regex-highlighted passages as aids. **Coder B** = the same agent on a separate later pass over a random 20% of notices (seed 20261018), blind to pass-1 codes (codes withheld from the working file). This measures intra-coder consistency, not inter-coder reliability; the paper must say so. **The checklist, rules and a blank coding sheet are written so that Sean (or a human second coder) can double-code a subset; that is the single most valuable addition before submission.**
- Automated coder: a regex/keyword coder (`code\10_autocode.py`), written from the coding rules before looking at the consensus codes, is run on every notice. Its agreement with the consensus is reported per item (precision, recall, kappa). A small local LLM is **not** used unless time allows (see 00-STATUS).
- Disagreements between pass 1 and pass 2 are resolved by reading the text again and applying the written rule; both versions are kept in the files.
- Coding is of the notice text only, never of what the organisation actually does.

## 6. Analysis plan

- Outcomes: notice presence (RQ1); item rates among notices and among all reachable units (unconditional); core-five joint rate; number of core items met (0-5).
- Estimates: proportion with Wilson 95% CI within each stratum and cell; pooled school estimate re-weighted by frame size (stratified variance); never a pooled schools-plus-edtech figure presented as one population.
- Comparisons: Fisher exact (2x2) for edtech vs school and X vs Z; chi-square or Fisher-Freeman-Halton for board and city class; Kruskal-Wallis for the 0-5 score; Spearman for app popularity. Holm correction across the H-tests; exploratory tests labelled exploratory.
- Reliability: percent agreement, Cohen's kappa and Gwet's AC1 per item (kappa is unstable for rare items, hence AC1), with bootstrap CIs; regex coder vs consensus.
- Sensitivity: strict vs lenient coding; excluding NEEDS_RENDER vs treating them as no notice; excluding chains; host-clustered CIs where several units share a template.
- Sizing: with n = 40 per cell, a Wilson 95% interval is about +/- 15 points at p = 0.5; the study can detect large differences only.

## 7. Threats to validity (to be stated, with how each is handled)

- Selection: only schools with a listed website; OSM and App Store frames are non-probability. Handled by naming the frame in every claim; no claim about "all Indian schools".
- Measurement: legal items interpreted from the Act and Rules text; where the text is open (e.g. "itemised"), the written rule is the interpretation, and strict vs lenient codings are both shown.
- Coder: one agent coder, intra-coder reliability only. Handled by publishing the rules, the sheets and the regex coder; recommending a human second coder.
- Discovery: a notice behind a menu, a PDF in a download centre, or JavaScript may be missed; "NOT_FOUND" means not found by this protocol. Handled by the NEEDS_RENDER class, the probe list, and a manual re-check of a random 10% of NOT_FOUND units by a second discovery pass (search of homepage links for "policy", "terms", "disclosure").
- Temporal: a snapshot on the collection date; notices will change before 13 May 2027. Archive copies and hashes fix the date.
- Legal: Rule 3/s.5 not in force; s.7 legitimate uses; Fourth Schedule item 3 for schools. A "fail" is a readiness gap.
- Ethics: public documents about institutions, no personal data of pupils, no contact; institutions identified by code; the name key is a separate file marked not for publication. SARAS and CISCE listings include principals' names; they were stripped from the working frame, and the raw pages are kept only in `data\raw_private\`.

## 8. Data sources, licences, access dates

| Data | Licence / terms | Accessed |
|---|---|---|
| DPDP Act 2023, DPDP Rules 2025, G.S.R. 843(E) (official Gazette PDFs) | Government of India publication | 17 Oct 2026 |
| CBSE SARAS affiliated-school list | public government directory; terms not stated on page; used read-only, 37 queries, no names retained | 17 Oct 2026 |
| CISCE School Locator | public directory; same handling | 17 Oct 2026 |
| OpenStreetMap via Overpass | ODbL 1.0 (attribution: (c) OpenStreetMap contributors) | 17 Oct 2026 |
| Apple iTunes Search API | public API; 66 queries, 4 s apart | 17 Oct 2026 |
| Notices | public web pages; copies kept only for research, not for redistribution (hashes and archive links are the public record) | collection dates in the log |
| HRA city list | Wikipedia (CC BY-SA) | 17 Oct 2026 |

## 9. Outputs promised

`data\frame\*` (frames), `data\sample\sample_public.csv` (codes only) and `data\sample\sample_NOT_FOR_PUBLICATION.csv` (name key and URLs), `data\notices\collection_log.csv`, `data\coding\*` (pass 1, pass 2, regex, consensus), `results\tables\*.csv`, `results\figures\*.png`, `results\RESULTS-SUMMARY.md`.

## 10. Confirmatory vs exploratory
Confirmatory: H1-H6 as written. Everything else exploratory.

## 11. Deviations log (append only)
- 17 Oct 2026, after collection and before coding: unit counts fixed as designed (240 drawn: S1 80, S2 50, S3 30, S4 20, S5 60). S4 was drawn as the 20 largest shared government-system hosts (one random school per family), not all distinct hosts.
- During coding: added a `kind` field (PRIV / TERMS / EMPTY / THIRD_PARTY / NONE / OUT_OF_SCOPE) because several "found" pages turned out not to be notices; only `PRIV` counts as a notice. Two edtech units were declared out of scope by hand (a UK tutoring site; a Pakistan-based app) and two flagged scope-uncertain (sensitivity table).
- Coding rules changed to v1.1 (D3, D7, D8b) after the regex-discrepancy review; five cell changes logged in `data\coding\reconciliation_log.csv`.
- Pass 2 drawn from 67 coded pages that existed at the time (14 units, seed 20261018); pass 2 is intra-coder only. S3-S8 descriptors left to the regex coder.
- The rendering fallback (headless Chrome) timed out on most JavaScript pages; 21 units are reported as UNVERIFIED and analysed as a separate outcome, with a sensitivity case.
- Analysis of the X-vs-Z hypothesis (H6) uses two-sided Fisher tests; the design text said one-sided direction was hypothesised.
- The read-only CBSE directory search is a POST form; the project brief said not to submit any form. It was judged to be a public directory query (the brief names these directories as frame sources) and is flagged here for his decision.
