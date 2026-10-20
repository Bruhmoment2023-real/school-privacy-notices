# Search protocol - 11-school-privacy-notices

- Paper question: Readiness baseline: public privacy notices of Indian schools and edtech services against the DPDP Act 2023 and Rules 2025
- Date of search and data pull: **2026-10-17**
- Years covered: 2005-2026; language: English (OpenAlex language field `en` or missing)
- Built by an AI agent (Claude) with the scripts in `python\` and `R\`; all numbers below are read from the run logs.

## 1. Databases

| Role | Database | Access | Note |
|---|---|---|---|
| Discovery | Crossref REST API | free, no key, `mailto` polite pool | relevance-ranked keyword search; top N per query |
| Discovery | Semantic Scholar Graph API (bulk search) | free, no key | boolean search on title/abstract; top N by citations per query |
| Discovery | ERIC API | free, no key | education topics only |
| Discovery | arXiv API | free, no key | preprints |
| Enrichment (authors, institutions, countries, topics, keywords, abstracts, references, citation counts, OA links) | **OpenAlex** single-record lookups (`/works/doi:...`, `/works/mag:...`, `/works/W...`) | free, no key | see limit 1 below |
| Forward citations for snowballing | OpenCitations Index API v2 | free, no key | DOI-to-DOI citations only |
| Cross-check | Crossref (per-DOI), Semantic Scholar (batch) | free, no key | citation counts and reference-list coverage compared in `tables\coverage_crosscheck.csv` |
| Not used | Scopus, Web of Science, Lens, Dimensions | need accounts | equivalent strings are in `scopus-queries.md` |
| Not usable | RePEc/IDEAS | its API needs a registered access code; the public search page returned no parseable result list to a script | economics working papers still enter via Crossref, Semantic Scholar and snowballing |

**Why OpenAlex was not the search engine.** Since 2026 OpenAlex charges keyless list/search calls against a small daily budget shared by everyone on the same IP address ($0.10/day). On the day of the pull that budget was already exhausted by other work on this network, and an API key needs an account (ruled out). Single-record lookups remain free and unlimited, so records were *discovered* in Crossref / Semantic Scholar / ERIC / arXiv and then *enriched* one by one from OpenAlex. Consequence: a work that is in OpenAlex but not found by any of the four discovery databases is missed, except where snowballing caught it.

## 2. Exact search strings

### A_policy_measurement: Privacy-policy measurement, annotation and compliance checking

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | privacy policy analysis compliance large-scale | 7153339.0 | 200 | ok |
| crossref | privacy policy corpus annotation | 1154772.0 | 200 | ok |
| crossref | automated analysis of privacy policies GDPR compliance | 5682475.0 | 200 | ok |
| crossref | readability of privacy policies | 316052.0 | 200 | ok |
| crossref | privacy notices compliance audit websites | 417521.0 | 200 | ok |
| crossref | privacy policy presence apps | 1266111.0 | 200 | ok |
| s2 | ("privacy policy" \| "privacy policies") + (compliance \| audit \| corpus \| annotation \| classification) | 1162.0 | 600 | ok |
| s2 | "privacy policies" + (GDPR \| COPPA \| CCPA) + (analysis \| measurement \| empirical) | 167.0 | 167 | ok |
| s2 | "privacy notice" + (compliance \| audit \| websites) | 99.0 | 99 | ok |
| eric | "privacy policy" AND (analysis OR audit OR compliance) | 8.0 | 5 | ok |

### B_children_apps: Children's data, COPPA and parental consent

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | COPPA compliance children's apps | 1046518.0 | 200 | ok |
| crossref | verifiable parental consent children's data | 3166805.0 | 200 | ok |
| crossref | children's privacy apps measurement | 1653421.0 | 200 | ok |
| crossref | child-directed apps privacy policies | 865252.0 | 200 | ok |
| crossref | parental consent age verification data protection law children | 5195463.0 | 200 | ok |
| s2 | COPPA + (apps \| compliance \| children) | 148.0 | 148 | ok |
| s2 | "parental consent" + (children \| minors) + (data protection \| privacy) | 136.0 | 136 | ok |
| s2 | "child-directed" + (apps \| privacy) | 18.0 | 18 | ok |
| eric | children AND privacy AND (apps OR online) AND (law OR policy) | 28.0 | 18 | ok |

### C_india_dpdp: India: DPDP Act 2023, data protection law and practice

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | Digital Personal Data Protection Act 2023 India | 13064508.0 | 200 | ok |
| crossref | DPDP Act children data parental consent | 3273520.0 | 200 | ok |
| crossref | India data protection law consent notice | 4246254.0 | 200 | ok |
| crossref | DPDP Rules 2025 | 9739199.0 | 200 | ok |
| crossref | India personal data protection bill privacy | 3483735.0 | 200 | ok |
| s2 | ("DPDP Act" \| "Digital Personal Data Protection Act") + (consent \| notice \| children) | 128.0 | 128 | ok |
| s2 | India + "data protection" + (law \| privacy \| consent) | 834.0 | 600 | ok |
| eric | India AND "data protection" AND (education OR schools OR students) | 2.0 | 2 | ok |

### D_edtech_schools: Education technology and school data privacy

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | edtech student data privacy | 2594769.0 | 200 | ok |
| crossref | school data protection children's data | 4137968.0 | 200 | ok |
| crossref | educational technology privacy policies | 4443703.0 | 200 | ok |
| crossref | student privacy K-12 apps | 4426391.0 | 200 | ok |
| crossref | India edtech privacy children | 1708278.0 | 200 | ok |
| crossref | learning analytics privacy schools | 2807577.0 | 200 | ok |
| s2 | (edtech \| "educational technology") + (privacy \| "data protection") | 695.0 | 600 | ok |
| s2 | "student data" + (privacy \| protection) + (schools \| K-12) | 226.0 | 226 | ok |
| eric | "student data" AND privacy | 157.0 | 145 | ok |
| eric | edtech AND privacy | 27.0 | 27 | ok |
| eric | "data protection" AND schools | 18.0 | 17 | ok |

Per-query retrieval caps: crossref = 200, s2 = 600, eric = 250, arxiv = 100. Crossref totals are large because its search is an OR-type relevance ranking; only the top-ranked records were taken. Raw responses for every query are in `data\raw\<database>\`.

### Seed papers (known key works, each verified to exist by a Crossref title match; they bypass the keyword rules)

| seed title | result |
|---|---|
| Won't Somebody Think of the Children? Examining COPPA Compliance at Scale | matched 10.1515/popets-2018-0021 |
| The Creation and Analysis of a Website Privacy Policy Corpus | matched 10.18653/v1/p16-1126 |
| The Privacy Policy Landscape After the GDPR | matched 10.2478/popets-2020-0004 |
| MAPS: Scaling Privacy Compliance Analysis to a Million Apps | matched 10.2478/popets-2019-0037 |
| The Effect of Platform Policies on App Privacy Compliance: A Study of Child-Directed Apps | matched 10.56553/popets-2025-0094 |
| Developers Say the Darnedest Things: Privacy Compliance Processes Followed by Developers of Child-Directed Apps | matched 10.56553/popets-2022-0108 |
| Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning | NOT MATCHED in Crossref |
| Large-scale readability analysis of privacy policies | matched 10.1145/3106426.3106427 |
| Ambiguity in Privacy Policies and the Impact of Regulation | matched 10.1086/688669 |
| We'll Fix It Later: Education, AI, and the Deferral of Privacy in EdTech | NOT MATCHED in Crossref |
| A Tale of Two Regulatory Regimes: Creation and Analysis of a Bilingual Privacy Policy Corpus | matched 10.63317/47t33yg9tkem |
| Hunting for the Privacy Policy: Hospital Website Design | matched 10.2139/ssrn.4068445 |
| The Googlization of the classroom: Is the UK effective in protecting children's data and rights? | matched 10.1016/j.caeo.2024.100195 |

Seed arXiv ids (from the PDFs the substance agent saved in the paper folder): 1802.02561, 2609.28137, 1809.08396

## 3. Inclusion and exclusion rules (applied identically to search hits and snowballed records)

A record is **included** if all of the following hold:
1. It resolves to an OpenAlex work record (by DOI, MAG id, or a Crossref title match of at least 93% similarity).
2. OpenAlex type is article, review, preprint, book chapter, book, dissertation, report or other (editorials, errata, paratext, datasets, peer reviews are dropped).
3. Publication year 2005-2026; language English or unrecorded.
4. It satisfies at least one sub-literature rule below: every `include` pattern must match in title + abstract, and every `title_must` pattern must match in the title.
5. Its title does not match the exclusion pattern.

Book-series and proceedings trap: a record whose abstract is a series/proceedings blurb (detected by wording such as 'this volume constitutes the refereed proceedings', or the same abstract shared by 3+ records) is screened on its title alone; whole-volume records (titles starting 'Proceedings of', 'Front matter', etc.) are dropped.

The patterns are case-insensitive regular expressions (`\b` = word boundary, `\w*` = any word ending, `.{0,80}` = within 80 characters).

**A_policy_measurement - Privacy-policy measurement, annotation and compliance checking**

- include (title+abstract): `\b(privacy (polic\w+|notices?|statements?)|data protection (notices?|polic\w+)|privacy disclosures?)\b`
- title_must (title): `(privacy|polic\w+|gdpr|coppa|compliance|notice|disclosure)`

**B_children_apps - Children's data, COPPA and parental consent**

- include (title+abstract): `\b(child\w*|minors?|kids|youth|young users|student\w*)\b`
- include (title+abstract): `\b(privacy|data protection|COPPA|parental consent|verifiable|personal data|tracking|SDKs?)\b`
- title_must (title): `(child\w*|COPPA|parental|minor\w*|kids|youth|student\w*)`

**C_india_dpdp - India: DPDP Act 2023, data protection law and practice**

- include (title+abstract): `\b(india\w*|DPDP\w*|digital personal data protection)\b`
- include (title+abstract): `\b(data protection|privacy|personal data|consent|data fiduciar\w+|data principal)\b`
- title_must (title): `(india\w*|DPDP\w*|digital personal data)`

**D_edtech_schools - Education technology and school data privacy**

- include (title+abstract): `\b(edtech|ed-tech|education(al)? technolog\w+|e-?learning|learning (apps?|platforms?)|school\w*|K-12|student data)\b`
- include (title+abstract): `\b(privacy|data protection|personal data|student data|surveillance|datafication|data governance)\b`
- title_must (title): `(privacy|data|surveillance|datafication|protection|governance)`

**Exclusion pattern (title):** `(blockchain|differential privacy|federated learning|homomorphic|smart grid|\bhealthcare\b|\bmedical\b|\bhospital|patient|genom|clinical|\bcovid|contact[- ]tracing|vehicle|iot\b|internet of things|quantum|facial recognition|biometric (authentication|template)|cryptograph|steganograph|anonymi[sz]ation algorithm)`

A record matching several rules is assigned to the first one in the order listed (its other matches are kept in `sublits_all`).

## 4. Snowballing (one round)

- Central papers: the 25 corpus records ranked highest on local citations + topical relevance + log(global citations) - listed in `data\clean\snowball_central_papers.csv`.
- Backward: every OpenAlex `referenced_works` entry of those papers not already in the corpus (507 candidates).
- Forward: citing DOIs from OpenCitations, up to 150 per central paper (775 candidates). OpenCitations only knows DOI-to-DOI links, so citing preprints and books without DOIs are missed.
- All candidates were looked up in OpenAlex and screened with the rules in section 3: 55 backward and 92 forward records were added.

## 5. PRISMA-style counts

| stage | n |
|---|---|
| Records identified through database searching (all query hits) | 7373 |
|    of which from crossref | 4400 |
|    of which from eric | 214 |
|    of which from s2 | 2722 |
|    of which from seed | 37 |
| Duplicates removed (same DOI / id / title across queries and databases) | 2518 |
| Unique records screened on title (+ abstract where the database supplied one) | 4855 |
| Removed at title pre-screen (off-topic) | 2626 |
| Records looked up in OpenAlex | 2229 |
| Duplicates removed after OpenAlex matching (same work / same title) | 7 |
| Excluded at full screen: year_out_of_range | 595 |
| Excluded at full screen: type_excluded | 363 |
| Excluded at full screen: offtopic_fails_inclusion_rule | 156 |
| Excluded at full screen: no_openalex_record (no DOI / not indexed) | 154 |
| Excluded at full screen: language_not_english | 11 |
| Excluded at full screen: paratext_or_container_record | 1 |
| Included after search screening | 942 |
| Snowball: central papers used | 25 |
| Snowball: backward-reference candidates | 507 |
| Snowball: forward-citation candidates (OpenCitations) | 775 |
| Snowball: duplicates of corpus records | 14 |
| Snowball excluded: type_excluded | 532 |
| Snowball excluded: offtopic_fails_inclusion_rule | 392 |
| Snowball excluded: year_out_of_range | 66 |
| Snowball excluded: offtopic_exclusion_term_in_title | 63 |
| Snowball excluded: no_openalex_record | 38 |
| Snowball excluded: language_not_english | 25 |
| Snowball excluded: paratext_or_container_record | 5 |
| Snowball: included (backward) | 55 |
| Snowball: included (forward) | 92 |
| Corpus before hand-screening | 1089 |
| Removed at hand-screening (see tables/hand_screen_removed.csv) | 179 |
| FINAL CORPUS | 910 |
|    with abstract | 792 |
|    with DOI | 826 |
|    with a reference list in OpenAlex | 494 |
| Distinct cited references / resolved to metadata | 13812 / 4953 |

Figure: `figures\py_01_prisma_flow.png`.

## 6. Hand-screening

After rule screening and snowballing, the agent read the titles (with source and year) of the whole corpus and removed 179 records as off-topic or mis-matched; every removal and its reason is in `tables\hand_screen_removed.csv`. This is a single-screener pass by an AI agent on titles, not a two-person human screen; borderline records were kept.

Removal reasons:
- hand-screen (title): no privacy / data-protection / consent / ethics term; generic education, AI or child-development paper: 119
- hand-screen (title): AI in criminal justice: 2
- hand-screen (title): special-education record consent in autism research: 1
- hand-screen (title): family-planning research IRB: 1
- hand-screen (title): organisational compliance climate, not notices: 1
- hand-screen (title): LGBTQ youth research: 1
- hand-screen (title): EHR management framework: 1
- hand-screen (title): AI criminal liability: 1
- hand-screen (title): transgender youth research ethics: 1
- hand-screen (title): children looked after data resource: 1
- hand-screen (title): health-research parental consent: 1
- hand-screen (title): privacy taxonomy for collaborative systems, not notices: 1
- hand-screen (title): LGBTQ research ethics: 1
- hand-screen (title): vaccine survey consent trial: 1
- hand-screen (title): STD treatment without parental consent (health): 1
- hand-screen (title): e-health in India: 1
- hand-screen (title): pharmaceutical regulation: 1
- hand-screen (title): deaf education demographics: 1
- hand-screen (title): research ethics for family studies: 1
- hand-screen (title): pharma patent law: 1
- hand-screen (title): national digital health ecosystem: 1
- hand-screen (title): health data API roadmap: 1
- hand-screen (title): HIV trial consent: 1
- hand-screen (title): mental health screening app pilot: 1
- hand-screen (title): thalassemia data ecosystems: 1
- hand-screen (title): bullying-detection CCTV AI: 1
- hand-screen (title): digital health regulation: 1
- hand-screen (title): transgender children health: 1
- hand-screen (title): digital health IDs: 1
- hand-screen (title): AI and children in conflict with law: 1
- hand-screen (title): juvenile justice AI: 1
- hand-screen (title): digital pHealth ethics, not notices: 1
- hand-screen (title): digital-health GDPR toolkit: 1
- hand-screen (title): biobanking: 1
- hand-screen (title): EHR ontology: 1
- hand-screen (title): digital banking frauds: 1
- hand-screen (title): health access review: 1
- hand-screen (title): digital health privacy frameworks (health, not notices): 1
- hand-screen (title): research-ethics handbook: 1
- hand-screen (title): unrelated education/media topic: 1
- hand-screen (title): algorithm disclosure and trade: 1
- hand-screen (title): rural banking service quality: 1
- hand-screen (title): AI training data trade secrets: 1
- hand-screen (title): health data interoperability: 1
- hand-screen (title): metaverse climate education: 1
- hand-screen (title): forensics AI: 1
- hand-screen (title): ecological law nexus: 1
- hand-screen (title): criminal-investigation privacy: 1
- hand-screen (title): health-systems CRM in schools: 1
- hand-screen (title): consent to research by mentally ill children: 1
- hand-screen (title): HIV adolescent consent: 1
- hand-screen (title): research consent on violence exposure: 1
- hand-screen (title): health privacy ontology: 1
- hand-screen (title): cyber law for trade: 1
- hand-screen (title): abortion parental involvement laws: 1
- hand-screen (title): paediatric clinical study: 1
- hand-screen (title): governmental liability: 1
- hand-screen (title): school sex surveys: 1
- hand-screen (title): formal-methods policy enforcement language, not notice content: 1
- hand-screen (title): summarisation for environmental sustainability: 1

## 7. Coverage and cross-checks

| item | value |
|---|---|
| corpus records | 910.0 |
| records with DOI | 826.0 |
| found in Crossref (DOI lookup) | 768.0 |
| found in Semantic Scholar (batch DOI lookup) | 785.0 |
| Spearman corr. OpenAlex vs Crossref cited-by | 0.964 |
| Spearman corr. OpenAlex vs Semantic Scholar cited-by | 0.91 |
| median cited-by: OpenAlex | 2.0 |
| median cited-by: Crossref | 2.0 |
| median cited-by: Semantic Scholar | 3.0 |
| records with no reference list in OpenAlex | 416.0 |
|   of which Crossref holds a reference list | 19.0 |
| records with no institution/country data | 229.0 |
| records without abstract | 118.0 |
| open-access records (OpenAlex) | 632.0 |
| origin: search | 759.0 |
| origin: snowball_forward | 84.0 |
| origin: snowball_backward | 54.0 |
| origin: seed | 13.0 |
| retrieved by: s2 | 751.0 |
| retrieved by: openalex_snowball | 138.0 |
| retrieved by: eric | 29.0 |
| retrieved by: seed | 13.0 |
| retrieved by: crossref | 1.0 |


- 154 title-screened candidates could not be matched to any OpenAlex record (no DOI or MAG id, or not indexed) and are **not** in the corpus. They are listed in `data\clean\unresolved_candidates.csv` (eric: 82, s2: 72). ERIC reports and theses and Indian or legal journal articles without DOIs dominate this list.

- Cited references: 13812 distinct works are cited by the corpus (18469 links); 4953 of the 5000 outside the corpus were resolved to metadata for the co-citation and RPYS analyses.


### Named prior work (seed list / the substance agent's saved papers) - is it in the corpus?

| id | kind | in_corpus | title |
|---|---|---|---|
| 10.1016/j.caeo.2024.100195 | doi | 1 |  |
| 10.1086/688669 | doi | 1 |  |
| 10.1145/3106426.3106427 | doi | 1 |  |
| 10.1515/popets-2018-0021 | doi | 1 |  |
| 10.18653/v1/p16-1126 | doi | 1 |  |
| 10.2139/ssrn.4068448 | doi | 0 |  |
| 10.2478/popets-2019-0037 | doi | 1 |  |
| 10.2478/popets-2020-0004 | doi | 1 |  |
| 10.56553/popets-2022-0108 | doi | 1 |  |
| 10.56553/popets-2025-0094 | doi | 1 |  |
| 10.63317/47t33yg9tkem | doi | 1 |  |
| arXiv:1802.02561 | arxiv | 1 | Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning |
| arXiv:1809.08396 | arxiv | 1 | The Privacy Policy Landscape After the GDPR |
| arXiv:2609.28137 | arxiv | 1 | "We'll Fix It Later": Education, AI, and the Deferral of Privacy in EdTech |

## 8. API failures during the run

- api.crossref.org: failed after retries:  (x4)


## 9. Scopus / Web of Science exports
- `scopus-drop\`: EMPTY - no Scopus/WoS export to merge; corpus is OpenAlex-only.
- Ready-to-paste strings: `scopus-queries.md`.
