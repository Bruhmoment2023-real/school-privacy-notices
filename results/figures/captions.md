# Figure captions (what, data and settings, one caution)

## fig1_notice_presence_by_group.png
- **Shows:** share of reachable, verified units with a dedicated privacy notice, by stratum, with Wilson 95% intervals and counts.
- **Data and settings:** `results\tables\T2_notice_presence.csv`; verified = homepage reached and notice search completed; units unreachable (58) or unverifiable (21) are excluded; 17 Oct 2026.
- **Caution:** the edtech bar is not comparable with the school bars: edtech units were reached through App Store listings that carry a privacy-policy link.

## fig2_item_heatmap.png
- **Shows:** percentage of units with a notice that meet each checklist item (strict = Y only), by stratum.
- **Data and settings:** `T3_item_rates.csv`; denominators are units with a coded notice (CBSE 9, CISCE 6, other 3, government 1, edtech 41); items D1-D9, K1-K5 as defined in `data\legal\LEGAL-CHECKLIST.md`.
- **Caution:** rows with n of 1 to 9 are descriptive only; the intervals in T3 are wide.

## fig3_presence_by_city_class.png
- **Shows:** notice presence among CBSE and CISCE own-site schools by HRA city class (X = 8 metros, Y = about 117 named cities, Z = all other).
- **Data and settings:** `T4_presence_by_city_class.csv`; class from address text and district against a Wikipedia copy of the HRA list; Wilson intervals.
- **Caution:** the X-versus-Z difference (29.0% vs 12.5%) is not statistically established (Fisher p = 0.19); class is an administrative classification, not a population measure.

## fig4_core_score_distribution.png
- **Shows:** distribution of the number of core items (D1-D5) met (strict) among reachable verified units, by stratum.
- **Data and settings:** unit-level table; units without a notice score 0.
- **Caution:** bars are percentages within strata of very different sizes (verified n = 53 CBSE, 32 CISCE, 21 other, 10 government, 43 edtech).
