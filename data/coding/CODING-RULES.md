# Coding rules (version 1.1)

Instrument and verbatim legal text: `..\legal\LEGAL-CHECKLIST.md` (v1.0 rules for D1-D9, K1-K5). Values: Y / P / N (and NA where noted). Strict = Y only; lenient = Y or P.
`kind` (what the retrieved page is): PRIV = a dedicated privacy policy/notice with substantive text; TERMS = website terms of use labelled privacy; EMPTY = page or link with navigation only (no policy text); THIRD_PARTY = the link leads to another organisation's policy; NONE = soft-404 (the "privacy" URL returned the homepage); OUT_OF_SCOPE = not an India-targeted service. Only `kind = PRIV` counts as "has a notice"; every item is N for other kinds.

## Changes in v1.1 (made during coding, logged in `reconciliation_log.csv`)
- D3: a stated right to opt out, or a marketing-unsubscribe channel only, is P (not N).
- D7: a dedicated privacy or grievance address (for example privacy@..., grievance@...) counts as Y; a general support/info address is P.
- D8b: a stated response period of 90 days or less for rights requests, queries or grievances counts as Y; a processing time for account deletion alone does not.

## Operating notes
1. Code the notice text only. Never infer practice from other pages.
2. Boilerplate generator text counts as the organisation's own notice if it is the page the site links as its privacy policy.
3. Where the extracted text omits collapsed/accordion content (seen on at least one site), code what is in the text and note it.
4. S1 (names DPDP) is Y only if the Act or Rules are named; paraphrasing DPDP concepts without naming it is N (recorded in the note).
5. S3-S8 are descriptive and were coded by the regex coder only (`code\10_autocode.py`), except S1 and S2 (hand coded).
6. Pass 1: whole text for notices up to 1,500 words; for longer notices, a targeted view (headings plus the paragraphs matching each item's key terms) with context searches for contested items. Early notices were read with long lines truncated at 230-330 characters in the console; the regex-discrepancy review (D3, D4, D5, D7, K3, K4, K5, D8a) and pass 2 were run to catch misses.
