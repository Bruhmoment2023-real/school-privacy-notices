# code\ - how to regenerate (resumable; run in order; Python = D:\Research-Publishing\_tools\biblio-venv\Scripts\python.exe, always `-I`)

| Step | Script | Output | Notes |
|---|---|---|---|
| 0 | `00_prior_search.py`, `00b_prior_openalex_s2.py` | followup\raw\prior | literature searches (Crossref, arXiv, OpenAlex, S2) |
| 1 | (pdftotext on the MeitY/eGazette PDFs) | data\legal\*.txt | legal text; hashes in LEGAL-CHECKLIST.md |
| 2 | `02_frame_cbse.py` | data\frame\cbse_frame.csv | CBSE SARAS directory, 37 read-only searches; raw pages gz in data\raw_private (not for publication) |
| 3 | `03_frame_cisce.py` | data\frame\cisce_frame.csv | CISCE School Locator, paginated GET |
| 4 | `04_frame_osm.py` | data\frame\osm_frame.csv | OpenStreetMap via Overpass (ODbL) |
| 5 | `05_frame_edtech.py` | data\frame\itunes_apps.csv | Apple iTunes Search API, India storefront, Education genre |
| 6 | `06_sample.py`, `06b_sample_edtech.py`, `06c_make_sample_files.py`, `06d_enrich.py` | data\sample\* | seed 20261017; unit codes randomised; `sample_NOT_FOR_PUBLICATION.csv` is the name key |
| 7 | `07_collect.py`, `07b_render.py` | E:\Research-Staging\...\notices (see STAGING.md) | robots.txt honoured; headless Chrome fallback for JavaScript pages (slow, many timeouts on this laptop) |
| 8 | `08_archive.py` | data\notices_archive_log_NOT_FOR_PUBLICATION.csv | Wayback Save Page Now (anonymous GET), 15 s apart |
| 9 | `09_packet.py`, `09b_addcodes.py`, `09c_find.py`, `09d_reconcile.py` | data\coding\pass1*.csv, pass2.csv | coding tools |
| 10 | `10_autocode.py` | data\coding\auto_codes.csv | regex coder |
| 11 | `11a_reliability.py`, `11b_analyse.py` | results\tables, results\figures | analysis |
Seeds: sampling 20261017 (+offsets in code), unit codes 20261019, pass-2 selection 20261018, NOT_FOUND re-check 20261020, bootstraps seed 1. Shared helpers: `common.py`, `citycls.py`.
