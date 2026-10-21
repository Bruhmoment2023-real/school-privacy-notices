# RESULTS SUMMARY (bullets; numbers from `results\tables\`, produced by `code\11*.py` on 17 Oct 2026; item rates updated on 21 Oct 2026 to the final codes after the full check of the 19 school notices, see RQ6)

Wilson 95% intervals in brackets. "Verified" = homepage reached and the privacy-notice search finished (found, found-but-not-a-notice, or not found). "Notice" = a dedicated privacy policy with substantive text (`kind = PRIV`). Strict = Y only; lenient = Y or P. **Readiness baseline: s.5, s.8, s.9 and Rules 3, 9, 10, 14 are not in force until 13 May 2027 (G.S.R. 843(E); Rule 1(4)).** A missing item is "not ready", not "unlawful".

## Sample and collection (T1)
- 240 units drawn (seed 20261017): CBSE 80, CISCE 50, other-board (OSM) 30, government school systems 20, edtech/school software 60. Collected 17 Oct 2026, robots.txt honoured, nothing contacted or submitted.
- Final status: notice found 60; page fetched but not a notice 7 (3 navigation-only, 2 soft-404/parked domain, 1 terms-of-use, 1 another company's policy); no notice found 92; unreachable 58 (DNS/connection/HTTP errors, 3 robots blocks); **unverified 21** (JavaScript pages the headless browser could not render: 5 CBSE, 3 CISCE, 1 other, 2 government, 10 edtech); out of scope 2 (a UK tutoring site, a Pakistan-based app).
- Unreachable share of those drawn: CBSE 27.5%, CISCE 30.0%, other 26.7%, government 40.0%, edtech 8.3%. School sites listed in public directories are often dead or unreachable by a plain request.
- Archive: 68 of 69 fetched notice pages archived with Wayback Save Page Now (one HTTP 520; 69 = the 60 notices plus 9 pages that turned out not to be notices); SHA-256 of every fetched notice is in the collection log.

## RQ1: presence of a dedicated notice (T2)
- **Schools (verified n = 116): 19 have a notice = 16.4% [10.7-24.2].** CBSE 9/53 = 17.0% [9.2-29.2]; CISCE 6/32 = 18.8% [8.9-35.3]; other 3/21 = 14.3% [5.0-34.6]; government systems 1/10 = 10.0% [1.8-40.4].
- Frame-weighted estimate for CBSE-listed own-site schools: 16.9% [4.1-29.8]; CISCE 13.9% [4.1-23.7] (T5; weights from frame cells by city class; normal-approximation CIs, small cells).
- Counting any page labelled privacy (including terms-only and empty pages) as a notice raises CBSE to 24.5% [14.9-37.6] and the other-board stratum to 19.0% (T8).
- **Edtech: 41/43 = 95.3% [84.5-98.7]** (sensitivity: 77.4% if the 10 unverified are counted as having no notice). This is not a like-for-like comparison with schools: edtech sellers were reached through their App Store listing, which carries a privacy-policy link, so presence is close to guaranteed by design.
- Re-check of the discovery step: 14 random NOT_FOUND school units re-inspected by hand from the saved homepage HTML (seed 20261020): 13 had no privacy or policy link at all; 1 had a "Privacy Policy" link with href "#" (inactive). See `data\coding\notfound_recheck_selection.txt`.

## RQ2: content among units with a notice (T3, Fig 2). Strict rates among notices; schools n = 19, edtech n = 41
| Item | Schools | Edtech |
|---|---|---|
| D1 itemised data | 17/19 = 89% [69-97] | 39/41 = 95% [84-99] |
| D2 specific purposes | 8/19 = 42% [23-64] | 28/41 = 68% [53-80] |
| D3 how to withdraw consent | 1/19 = 5% [1-25] | 15/41 = 37% [24-52] |
| D4 means to exercise rights | 5/19 = 26% [12-49] | 27/41 = 66% [51-78] |
| **D5 Data Protection Board complaint route** | **0/19 = 0% [0-17]** | **2/41 = 5% [1-16]** |
| D6 English/Eighth Schedule language | 19/19 | 41/41 (almost all English-only; no additional language version offered except one "on request") |
| D7 named privacy/grievance contact | 3/19 = 16% [6-38] | 15/41 = 37% [24-52] |
| D8a grievance mechanism | 2/19 = 11% | 9/41 = 22% |
| D8b response period <= 90 days | 2/19 | 7/41 = 17% |
| D9 stand-alone | 18/19 | 40/41 |
- **Core five (D1-D5 all Y): 2 of 60 notices = 3.3% [0.9-11.4] strict; 8/60 = 13.3% [6.9-24.2] lenient; 0 of 19 school notices, 2 of 41 edtech notices.** Of all 159 verified units: 2 = 1.3%.
- Mean core items met (strict, among notices): schools 1.63, edtech 2.71, of 5.
- 9 of 60 notices name the DPDP Act (15.0% [8.1-26.1]), all edtech (9/41 = 22%); no school notice does (0/19). A further text mirrors DPDP concepts (consent records, adult-parent verification) without naming the Act. Of 21 edtech notices that name any law, 12 name only the IT Act 2000 or a foreign regime (GDPR, CCPA, COPPA, UAE, Swiss/UK) and 9 name the DPDP Act (T7, T10).

## RQ3: children (T3, T7, T10). Among all 60 notices
- 32/60 = 53.3% [40.9-65.4] mention children or minors.
- Among those 32: parental consent stated (Y) 7 = 21.9% [11.0-38.8]; Y or P 21 = 65.6%; a parent-verification step (strict) **1 = 3.1% [0.6-15.7]**; Y or P 5.
- Age threshold stated in 26/60 notices: **15 of 26 (57.7%) use 13 or 16** (US/EU templates); 11 of 26 (42.3%) use 18 (DPDP s.2(f)).
- No tracking/behavioural monitoring/targeted advertising of children stated (K5): schools 0/19; edtech 5/41 = 12.2% [5.3-25.5]. One edtech notice states no behavioural tracking of minors while describing rewarded video ads (see coding notes in the internal file).
- School-ERP vendors (at least three notices) place parental-consent responsibility on the school or describe themselves as processors; this matters for who owes the s.5 notice.

## RQ4: template origin (T9)
- Text-similarity clusters (containment >= 0.35): one cluster of 5, two of 3, one of 2 among 61 notices with text; fingerprints: WordPress default "suggested text" 3 notices; a privacy-policy-generator text (capitalised "Your/We", under-13 clause) 4; an Indian coaching-platform template shared by 3 (one coaching institute in the other-board stratum, two edtech); COPPA/under-13 clause in 16 notices; GDPR-style rights block in 9; CCPA block in 7.
- Several notices are mislabelled or unfilled: a school linking another multinational's global policy; an empty "[Add Email ID]" placeholder; a school site whose policy page is a hacked page carrying injected spam links; a policy page that is website terms of use; a parked domain behind an app's policy link.

## RQ5: variation by type, board and city class (T4, T6; Fig 1, 3)
- CBSE vs CISCE presence: 17.0% vs 18.8% (Fisher p = 1.0).
- By city class, CBSE+CISCE own-site schools: X (8 metros) 9/31 = 29.0% [16.1-46.6]; Y 3/30 = 10.0% [3.5-25.6]; Z 3/24 = 12.5% [4.3-31.0]. X vs Z: OR 2.86, Fisher p = 0.19 (Holm 0.22); X vs Y+Z: OR 3.27, p = 0.073 (Holm 0.22). Direction as hypothesised (H6) but **not statistically established**; cells are small.
- Edtech vs all schools, notice presence: OR 105, p < 1e-19 (but see the selection caveat above). Core five: 2/43 vs 0/116, p = 0.072 (Holm 0.22).
- Edtech by App Store popularity tercile (T4b; sellers' total rating counts, 20 drawn per tercile): notice presence low 11/12 (92%), mid 17/17, high 13/14 (93%); DPDP Act named in 4 of 11, 4 of 17 and 1 of 13 notices respectively; core five met 1, 1 and 0. Eight of the nine notices naming the DPDP Act come from the lower two terciles; the high-popularity tercile has one. Unverified (JavaScript-only) units are concentrated in the lowest tercile (6 of 20). n is small: descriptive only.
- Kruskal-Wallis on core items met (0-5) across the five groups p < 1e-17 (driven by edtech vs the rest).

## RQ6: coding reliability (`results\tables\reliability_*.csv`)
- Pass 2 on a random 14 of 67 coded notices (20%), same agent, separate pass: strict (Y vs not) agreement 98.6% across 210 item-codings, kappa 0.970, Gwet AC1 0.973 (pass 1 before reconciliation). Differences: 4 (one D4, three D7), all traced to the D7 rule being tightened (v1.1); after reconciliation one difference remains (ED-017 D4, P vs N; pass 1 kept: the notice says it describes "access, and correction" but gives no list or means). **Intra-coder, same session: an upper bound on reliability, not inter-rater reliability.**
- Full check of the first-pass codes on the 19 school notices (21 Oct 2026; `checks/`): every code (19 x 15 = 285) was checked a second time against the notice text, with the first-pass code visible (a non-blind check). 282 checked, 3 marked unsure (kept as first pass). Met or not met: agreement 279/282 = 98.9% (exact 95% 96.9-99.8%), kappa 0.975, AC1 0.981; three levels: 95.4%, kappa 0.925. All 13 differences were cases where the first pass was stricter (10 N->P, 2 P->Y, 1 N->Y); they are applied in `data/coding/codes_final_checked.csv` (list in `data/coding/check_changes_log.csv`), which `11b_analyse.py` now reads. `pass1_reconciled.csv` is kept unchanged. Changes to the strict school rates: D1 16 -> 17, D8b 1 -> 2, K3 1 -> 2 of 19.
- Regex coder vs pass-1 consensus (n = 69 coded pages x 15 items): strict agreement 85.8%, kappa 0.70, AC1 0.73. Against the final checked codes (`reliability_regex_vs_final_checked.csv`): 85.9%, kappa 0.71, AC1 0.73; K3 kappa 0.42 (0.34 against pass 1). Item range: D1 92.8%, D5 98.6%, K5 98.6%, D9 91.3%, K1 88.4%, K2a 91.3%, D4 71.0%, D3 72.5%, **D2 59.4% (kappa 0.16)**, K3 84.1% (kappa 0.34), K4 82.6% (kappa 0.12). The regex coder over-calls D2, K3 and K4; it is adequate only for D1, D5, D9, K1, K2a, K5.
- A local LLM coder was not run (no Ollama binary installed; model blobs exist on D:\Ollama). Ready-to-run extension, not a result.

## Hypotheses (pre-specified in 02-design.md): outcome
- H1 fewer than half of reachable school sites have a notice; more than 80% of edtech: **supported** (16.4% [10.7-24.2]; edtech 95.3%, but 77.4% in the sensitivity case and with the selection caveat).
- H2 fewer than 20% of notices name the Board: **supported** (schools 0/19, upper bound 16.8%; edtech 2/41, upper bound 16.1%).
- H3 core five below 10% overall, edtech above school: **supported on level** (2/159 = 1.3% of verified units); direction edtech > school holds (4.7% vs 0%) but not significant.
- H4 fewer than 15% name the DPDP Act: **not supported at the margin** (9/60 = 15.0%, CI 8.1-26.1); edtech 22%. Second part (most law-citing edtech notices cite IT Act/foreign law only): 12 of 21 = 57%, marginal.
- H5 fewer than 25% of children-mentioning notices describe parent verification: **supported** (1/32, strict). Share with a non-18 threshold: 58%.
- H6 metro schools more likely to have a notice: direction yes (29% vs 12.5%) but **not significant**.

## Limits to carry into the paper
- Frame: schools with a listed website only; 58 of 240 units unreachable and 21 unverifiable (JavaScript), so rates are among reachable, verifiable units. No replacement was made.
- OSM stratum has no probability design and often lacks board and city data (board determined for 12 of 30; city class unknown for 12).
- Coder: one agent; hand coding read some long notices through a targeted view; regex-discrepancy review and pass 2 mitigate but do not replace a second human coder.
- Notices describe what organisations say, not what they do.
- Edtech frame is the Apple App Store India storefront; edtech presence is inflated by the store's privacy-link requirement.
