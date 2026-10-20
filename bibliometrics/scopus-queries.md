# Scopus and Web of Science search strings (ready to paste; NOT run: no Scopus or WoS login on this machine)

Mirror of the four sub-literatures in `search-protocol.md` (A policy measurement, B children's data, C India/DPDP, D edtech and school data). Date limit 2005-2026, English. Export CSV or BibTeX with abstracts and cited references into `scopus-drop\`; the pipeline merges them on the next run.

## Scopus (Advanced search)
```
A:  TITLE-ABS-KEY ( ( "privacy polic*" OR "privacy notice*" OR "privacy statement*" OR "data protection notice*" OR "privacy disclosure*" ) AND ( analy* OR audit* OR measur* OR compliance OR "content analysis" OR annotat* OR corpus OR "large-scale" OR automat* OR classif* OR readab* OR empirical ) ) AND PUBYEAR > 2004 AND LANGUAGE ( english )
B:  TITLE-ABS-KEY ( ( child* OR minor* OR kids OR youth OR student* ) AND ( COPPA OR "parental consent" OR "verifiable consent" OR "children's privacy" OR "children's data" OR "child-directed" ) ) AND PUBYEAR > 2004 AND LANGUAGE ( english )
C:  TITLE-ABS-KEY ( ( india* OR DPDP* OR "Digital Personal Data Protection" ) AND ( "data protection" OR privacy OR "personal data" OR consent OR "data fiduciar*" OR "data principal*" ) ) AND PUBYEAR > 2004 AND LANGUAGE ( english )
D:  TITLE-ABS-KEY ( ( edtech OR "ed-tech" OR "educational technolog*" OR "learning analytics" OR "K-12" OR school* ) AND ( "student data" OR "student privacy" OR "data protection" OR "privacy polic*" OR "privacy notice*" ) ) AND PUBYEAR > 2004 AND LANGUAGE ( english )
Intersections of interest (Sean's gap):
B∩C∩D:  ( TITLE-ABS-KEY ( india* OR DPDP* ) AND TITLE-ABS-KEY ( child* OR minor* OR student* ) AND TITLE-ABS-KEY ( school* OR edtech OR "educational technolog*" ) AND TITLE-ABS-KEY ( privacy OR "data protection" OR consent ) )
A∩C:     ( TITLE-ABS-KEY ( "privacy polic*" OR "privacy notice*" ) AND TITLE-ABS-KEY ( india* OR DPDP* ) )
Exclusion to apply after export (used in the OpenAlex run): drop titles with blockchain, differential privacy, federated learning, homomorphic, smart grid, IoT, facial recognition, cryptograph*, clinical/patient/hospital topics unless the paper analyses privacy policies or notices.
```

## Web of Science Core Collection (Advanced search, field tags)
```
A:  TS=(("privacy polic*" OR "privacy notice*" OR "privacy statement*" OR "data protection notice*") AND (analy* OR audit* OR measur* OR compliance OR "content analysis" OR annotat* OR corpus OR "large-scale" OR automat* OR classif* OR readab* OR empirical)) AND PY=(2005-2026) AND LA=(English)
B:  TS=((child* OR minor* OR kids OR youth OR student*) AND (COPPA OR "parental consent" OR "verifiable consent" OR "children's privacy" OR "children's data" OR "child-directed")) AND PY=(2005-2026) AND LA=(English)
C:  TS=((india* OR DPDP* OR "Digital Personal Data Protection") AND ("data protection" OR privacy OR "personal data" OR consent OR "data fiduciar*" OR "data principal*")) AND PY=(2005-2026) AND LA=(English)
D:  TS=((edtech OR "ed-tech" OR "educational technolog*" OR "learning analytics" OR "K-12" OR school*) AND ("student data" OR "student privacy" OR "data protection" OR "privacy polic*" OR "privacy notice*")) AND PY=(2005-2026) AND LA=(English)
```

## Notes
- The OpenAlex/Crossref/Semantic Scholar/ERIC/arXiv pipeline used looser phrase lists and a title/abstract screen (see `config.json`); expect Scopus to return fewer Indian legal-commentary records (many are in open repositories and low-indexed journals) and more health-app policy audits.
- ERIC adds education-law and student-privacy items that Scopus indexes unevenly.
- After a Scopus export, run `python\pipeline.py <bibliometrics dir> master` and the R script; compare with `tables\coverage_crosscheck.csv`.
