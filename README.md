# How ready are Indian schools and edtech services to give privacy notices? A baseline against the DPDP Act and Rules before May 2027

Archived on Zenodo: https://doi.org/10.5281/zenodo.23537751 (this DOI always points to the latest version).

**Author:** Sean Solano Paul, Independent researcher, Bengaluru, India.
**Funding:** none. **Competing interests:** none.

## Summary

India's Digital Personal Data Protection Act 2023 and its 2025 Rules will require a notice of what personal data is collected and why, and how to withdraw consent, exercise rights and complain to the Data Protection Board, with stricter duties for children's data, from 13 May 2027. This repository contains the code, coding rules and de-identified results of a readiness baseline: a stratified sample of 240 school websites and edtech services drawn from public directories and the Apple App Store, each searched for a privacy notice, and every notice found coded item by item (D1-D9, K1-K5, S1-S8) against a checklist built from the Gazette text. Hand coding (pass 1, a second pass on a random subset, reconciliation, then a check of every code on the 19 school notices, whose 13 corrections give the final codes in `data/coding/codes_final_checked.csv`) was compared with a transparent regex coder.

## Repository layout

| Path | Contents |
|---|---|
| `docs/design.md` | Pre-specification written before any notice was collected or coded (questions, hypotheses, frames, sampling, coding plan) |
| `code/` | Sampling, collection, coding and analysis scripts in run order (`code/README.md`) |
| `data/legal/` | Checklist (`LEGAL-CHECKLIST.md`) with Act and Rules text extractions |
| `data/coding/` | Coding rules, hand codes (`pass1*.csv`, `pass2.csv`, final `codes_final_checked.csv` with its `check_changes_log.csv`), regex codes (`auto_codes.csv`), reconciliation log, blank second-coder sheet |
| `checks/` | Check of every first-pass code on the 19 school notices: the filled check sheet (notice quotes with names, e-mails, addresses and phone numbers blanked), its instructions, the scripts that built and tallied it, and the tally output |
| `data/frame/frame_summary.csv` | Aggregate counts of the sampling frames only, including the number of government-system families (20) and of eligible App Store sellers (558, the edtech frame) |
| `results/tables/`, `results/figures/` | All paper tables and figures; `RESULTS-SUMMARY.md`; `unit_level_results_PUBLIC.csv` (240 units, codes only) |
| `bibliometrics/` | Literature map: search protocol, OpenAlex/Crossref/ERIC corpus, bibliometrix and Python analyses, VOSviewer files, tables, figures. See `bibliometrics/README.md` |
| `depth/` | Data dictionary, BibTeX/RIS references |
| `followup/raw/prior/` | Raw API responses of the prior-work search (Crossref, arXiv, OpenAlex) |

## De-identification of the unit-level table

`results/tables/unit_level_results_PUBLIC.csv` is **not** the original working file. The working file carried `state`, `city_basis` and `city_basis_final` columns, which hold state names and city names taken from school addresses. Those three columns were **removed** from this copy (the file name is unchanged). Location is represented only by the coarse HRA class (`city_class`, `city_class_final`: X, Y, Z). The remaining columns contain only random unit codes, strata, crawl outcomes and item codes.

## How to reproduce

- Python 3.12; `pip install -r requirements.txt`. R 4.5.3 with `bibliometrix` 5.3.0, `igraph` 2.2.2, `ggplot2` 4.0.3, `dplyr` 1.2.0 for the literature map.
- Script order is in `code/README.md`. Seeds: sampling 20261017 (+offsets in code), unit codes 20261019, pass-2 selection 20261018, NOT_FOUND re-check 20261020, bootstraps seed 1.
- Steps 2 to 8 (frames, sample, collection, archiving) re-download public directories and school websites; anyone rebuilding the frame must re-run them, and they write the institution-identifying files that this repository does not distribute. The analysis steps (`10_autocode.py`, `11a_reliability.py`, `11b_analyse.py` and the table scripts) read those local files, so the published tables in `results/` are the reproducible record and the scripts document exactly how they were made.
- Scripts use absolute paths under the original working folder (`D:\Research-Publishing\11-school-privacy-notices`); adjust the path constants (see `code/common.py`).
- Collection honoured robots.txt and sent no personal identifier.

## Data sources and licences

| Source | Use | Licence / terms |
|---|---|---|
| CBSE SARAS affiliated-school directory, CISCE School Locator, OpenStreetMap (Overpass), Apple iTunes Search API | Sampling frames (not redistributed) | Public directories and APIs under their own terms; OpenStreetMap data is ODbL |
| Public school and edtech websites | Privacy notices read and coded (text not redistributed) | Each site owner's rights |
| DPDP Act 2023, DPDP Rules 2025 (Gazette of India) | Checklist and text extractions in `data/legal/` | Government of India publication |
| OpenAlex, Crossref, ERIC, arXiv, OpenCitations | Literature map | CC0 or openly available metadata; Semantic Scholar raw responses not redistributed |
| Author-derived codes, tables, figures, documents | Everything else | CC BY 4.0 (`LICENSE-DATA.md`) |

Third-party author e-mail addresses that appeared in retrieved API records were replaced with `[email removed]`.

## Not included and why

- Abstract text of third-party papers (the `abstract`/`AB` columns and abstract-derived quote columns of the bibliographic tables, and abstract fields in the OpenAlex JSON). Identifiers, titles, years, venues, keywords and citation data are kept; re-fetch abstracts with the bibliometrics pipeline if needed.
- Per-paper reading notes on the literature (they contain quotations from copyrighted papers) and the literature gap-analysis note (scoping). The scripts that built the notes are kept; run them on your own copies of the papers.
- Sampling frames with institution names, addresses and website addresses (`data/frame/*` except the aggregate summary, `data/frame_probe/`), the sample files and name key (`data/sample/*`), raw directory pages (`data/raw_private/`), the notice archive log, the collected notices (`data/notices/`) and the zipped notice text: they identify institutions and contain third-party text. Regenerate the frames with `code/02_frame_cbse.py` to `code/05_frame_edtech.py` (public directories).
- Web-archive snapshot records for the notices: not distributed.
- The `state`, `city_basis` and `city_basis_final` columns of the unit-level table: removed (see above).
- Official Gazette PDFs (`data/legal/*.pdf`): download from the official sources listed in `data/legal/LEGAL-CHECKLIST.md`; the text extractions are included.
- Full-text PDFs of papers and their text extractions (`bibliometrics/pdfs/`, one prior-work PDF), and Semantic Scholar raw responses: copyrighted or restricted. `bibliometrics/python/pdfs.py` re-fetches open-access copies.
- R object files (`*.rds`) for the literature corpus: regenerate from the CSV files with the scripts in `bibliometrics/R/`.
- Run logs from the scratch staging folder, the prior-work memo, the gap analysis, and the script that zipped notice text.
- Nothing exceeded 50 MB.

## Limits

The paper measures the readiness of a published document, not legal compliance: the notice duties are not in force until 13 May 2027. Only organisations with a listed website could be sampled. Several documents (for example `bibliometrics/README.md` and `depth/appendix/data-dictionary.md`) describe the original working folder and mention files listed above as not included.

## Citation

Solano Paul, S. (2026). *How ready are Indian schools and edtech services to give privacy notices? A baseline against the DPDP Act and Rules before May 2027* [Software and data]. Independent researcher. See `CITATION.cff`. A DOI will be added when the repository is archived.
