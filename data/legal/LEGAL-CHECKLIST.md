# Legal checklist: DPDP Act 2023 and DPDP Rules 2025 (notice and children's data)

Built item by item from the official text. No manuscript prose; this is a coding instrument.

## Sources read (all opened in full from the official publisher, text extracted with pdftotext)

| Document | Where read | SHA-256 of the file in `data\legal\` |
|---|---|---|
| Digital Personal Data Protection Act, 2023 (No. 22 of 2023), Gazette of India Extraordinary, Part II Sec 1, no. 25, 11 Aug 2023 | MeitY `https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf` | `4deb2398...72a7d15` (`DPDP-Act-2023_meity.pdf`) |
| Digital Personal Data Protection Rules, 2025, G.S.R. 846(E), Gazette Part II Sec 3(i), New Delhi, Thursday 13 Nov 2025 (Gazette ID CG-DL-E-14112025-267650) | MeitY `https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf` and eGazette `https://egazette.gov.in/WriteReadData/2025/267650.pdf` (byte-identical, same hash) | `eabc7d05...e5f08` (`DPDP-Rules-2025_meity.pdf`, `egaz_267650.pdf`) |
| Commencement notification G.S.R. 843(E), 13 Nov 2025 (Act) | eGazette `https://egazette.gov.in/WriteReadData/2025/267647.pdf` | `GSR843E_commencement_egazette.pdf` |
| G.S.R. 844(E) (Board established), G.S.R. 845(E) | eGazette 267648, 267649 | files in `data\legal\` |

## Commencement dates (verified from the Gazette text, not from secondary sources)

- Rules, rule 1(2): "Rules 1, 2 and 17 to 21 shall come into force on the date of their publication in the Official Gazette."
- Rule 1(3): "Rule 4 shall come into force one year after the date of publication of this Gazette."
- Rule 1(4): "Rules 3, 5 to 16, 22 and 23 shall come into force eighteen months after the date of publication of this Gazette."
- Gazette dated 13 November 2025, so rule 4 = 13 Nov 2026 and rules 3, 5-16 = **13 May 2027**. The reported date is confirmed (arithmetic from the Gazette date; the Rules do not print the date).
- G.S.R. 843(E) (Act): sections 1(2), 2, 18-26, 35, 38-43, 44(1) and (3) from publication; section 6(9) and 27(1)(d) after one year; "sections 3 to 5, sub-sections (1) to (8) and (10) of section 6, sections 7 to 10, sections 11 to 17, section 27 except clause (d) of sub-section (1)..., sections 28 to 34, 36, 37 and sub-section (2) of section 44" after eighteen months. **So section 5 (notice), section 8 and section 9 are not in force until 13 May 2027.** This is a readiness baseline, not a finding of illegality.
- Not verified from a Gazette: a corrigendum reported as G.S.R. 892(E) of 10 Dec 2025 (two wording fixes on one page, per the DPDP Wiki, a secondary site) and a corrigendum listed as G.S.R. 113(E) (Simpliance page, no content; login wall). Neither is believed to change the dates.
- Reported but not enacted as far as found: a January-February 2026 MeitY proposal to shorten the 18-month window to 12 months (Takshashila blog 26 Jan 2026; S.S. Rana; Mondaq). Officials were reported as saying no decision had been taken. **No notified amendment was found in searches on 17 Oct 2026; Sean should check egazette.gov.in once more before submission.**

## Items (ID, requirement, verbatim text, coding rule)

"Y" = met, "P" = partly met, "N" = not met or not stated. A unit with **no discoverable notice** is coded "N" on every item (`NONE` in the notice-presence field) and reported separately, so that both population-level and conditional rates can be given.

### A. Core notice content (section 5(1) and rule 3)

| ID | Requirement | Verbatim source text | Coding rule (Y / P / N) |
|---|---|---|---|
| D1 | Itemised description of the personal data | s.5(1)(i): "the personal data and the purpose for which the same is proposed to be processed". Rule 3(b)(i): "an itemised description of such personal data" | Y: lists at least three distinct, specific data items or categories collected from the user (for example name, phone number, email, photograph, marks, device ID, location). P: names one or two specific items, or only broad classes ("personal information", "contact details") without itemising. N: no description, or only "personal data/information" in general. |
| D2 | Specified purposes and what services or uses they enable | s.5(1)(i) as above. Rule 3(b)(ii): "the specified purpose or purposes of, and specific description of the goods or services to be provided or uses to be enabled by, such processing" | Y: at least two concrete purposes tied to what the service does (for example admissions, fee collection, attendance, report cards, personalised lessons). P: only generic purposes ("to provide and improve our services", "for educational purposes"). N: none. |
| D3 | How to withdraw consent | s.6(4): "such Data Principal shall have the right to withdraw her consent at any time, with the ease of doing so being comparable to the ease with which such consent was given." Rule 3(c)(i): "withdraw her consent, with the ease of doing so being comparable to that with which such consent was given" | Y: states that consent can be withdrawn AND gives a channel (email, form, in-app setting, link). P: states a right to withdraw/opt out with no channel, or a channel for unsubscribing from marketing only. N: neither. |
| D4 | How to exercise the Data Principal's rights | s.5(1)(ii): "the manner in which she may exercise her rights under sub-section (4) of section 6 and section 13". Rule 3(c)(ii): "exercise her rights under the Act". Rule 14(1)(a): publish "the details of the means using which a Data Principal may make a request for the exercise of such rights" | Y: names at least access or correction or erasure rights AND a means (email, form, portal, address) to request them. P: lists rights with no means, or a means ("contact us") with no rights named. N: neither. |
| D5 | How to complain to the Data Protection Board | s.5(1)(iii): "the manner in which the Data Principal may make a complaint to the Board". Rule 3(c)(iii): "make a complaint to the Board" | Y: refers to the Data Protection Board of India (or "the Board" under the DPDP Act) as a complaint route. P: refers to a regulator/authority generically ("data protection authority") or to a court/cyber-cell only. N: no complaint route to a regulator. |

Composite "core five" = D1 to D5 all Y (strict) or all Y/P (lenient).

### B. Related publication duties (read with the notice)

| ID | Requirement | Verbatim source text | Coding rule |
|---|---|---|---|
| D6 | Option to read the notice in English or an Eighth Schedule language | s.5(3): "The Data Fiduciary shall give the Data Principal the option to access the contents of the notice referred to in sub-sections (1) and (2) in English or any language specified in the Eighth Schedule to the Constitution." (also s.6(3)) | Y: notice is in English or an Eighth Schedule language (almost all are). Descriptive sub-field D6b: an additional Eighth Schedule language version is offered (Y/N). |
| D7 | Business contact of a DPO or other person who can answer | s.8(9): "publish ... the business contact information of a Data Protection Officer, if applicable, or a person who is able to answer on behalf of the Data Fiduciary, the questions, if any, raised by the Data Principal about the processing of her personal data." Rule 9: "prominently publish on its website or app" | Y: a named role or designation (DPO, grievance officer, privacy contact) with an email or phone for privacy questions. P: generic "contact us" address/form with no privacy role. N: none. |
| D8 | Grievance redressal mechanism | s.8(10): "A Data Fiduciary shall establish an effective mechanism to redress the grievances of Data Principals." s.13(1). Rule 14(3): publish "within a reasonable period not exceeding ninety days under its grievance redressal system" | D8a: mechanism for privacy grievances described (Y/P/N). D8b: a response period is stated and is 90 days or less (Y/N). |
| D9 | Notice understandable independently of other information | Rule 3(a): "be presented and be understandable independently of any other information that has been, is or may be made available by such Data Fiduciary" | Y: stand-alone privacy page or document that does not depend on another document (terms, admission form, circular) for its core content. P: privacy content is a section inside general terms/website disclaimer. N: only a one-line reference to another document. Judged from the notice text, not from whether a consent request exists. |

### C. Children's data (section 9, rule 10; "child" is under 18, s.2(f))

s.2(f): "child" means an individual who has not completed the age of eighteen years.

| ID | Requirement | Verbatim source text | Coding rule |
|---|---|---|---|
| K1 | Notice acknowledges that it covers children or minors | s.9(1) (below) | Y: states how it treats data of children/minors/students under 18. N: silent on children (a school notice that never mentions students counts as N). |
| K2 | Age threshold stated, and it is 18 | s.2(f) above | K2a: an age threshold is stated (Y/N). K2b: threshold is 18 (Y), or 13/14/16 or other (N) — a foreign-template marker. |
| K3 | Parental or guardian consent before processing a child's data | s.9(1): "The Data Fiduciary shall, before processing any personal data of a child ... obtain verifiable consent of the parent of such child or the lawful guardian, as the case may be, in such manner as may be prescribed." Rule 10(1): "ensure that verifiable consent of the parent is obtained before the processing of any personal data of a child" | Y: says parent/guardian consent is obtained or required before processing a child's data. P: says parents "may" review/contact, or school obtains consent via admission form without saying so for processing. N: not stated. |
| K4 | How the parent is verified as an adult | Rule 10(1): "observe due diligence, for checking that the individual identifying herself as the parent is an adult who is identifiable ... by reference to (a) reliable details of identity and age ... available with the Data Fiduciary; or (b) details of identity and age, voluntarily provided (i) by the individual; or (ii) through a virtual token mapped to such details, which is issued by an authorised entity." | Y: describes any verification step (ID/age check, OTP-to-registered-adult, DigiLocker token, existing records). P: says it "verifies" with no method. N: not stated. |
| K5 | No tracking, behavioural monitoring or targeted advertising of children | s.9(3): "A Data Fiduciary shall not undertake tracking or behavioural monitoring of children or targeted advertising directed at children." (Fourth Schedule Part A item 3 relaxes s.9(1) and (3) for an educational institution only for "tracking and behavioural monitoring (a) for the educational activities of such institution; or (b) in the interests of safety of children enrolled with such institution".) | Y: states it does not track, profile, behaviourally monitor or target ads at children. P: says it limits ads/analytics for children without a flat statement. N: silent, or says it uses ad/behavioural trackers on users generally. Applicability caution: schools are partly exempt (Fourth Schedule item 3); report K5 for edtech and for schools separately. |

### D. Descriptive (not scored against the law; context)

| ID | Variable |
|---|---|
| S1 | Names the DPDP Act 2023 or DPDP Rules (Y/N) |
| S2 | Names another regime: IT Act 2000 / SPDI Rules 2011 / GDPR / COPPA / CCPA / other (multi-label) |
| S3 | Retention or deletion period stated (Y/N); relevant to s.8(7), rule 8 |
| S4 | Third-party or processor sharing disclosed, with named categories (Y/N); relevant to s.8(2), s.11(1)(b) |
| S5 | Cross-border transfer mentioned (Y/N); s.16 |
| S6 | Data breach intimation mentioned (Y/N); s.8(6), rule 7 |
| S7 | Date or version shown (Y/N), and the date |
| S8 | Cookies, analytics or advertising trackers disclosed (Y/N) |
| S9 | Notice language(s) |

## What the Act and Rules do NOT require in a published web notice (so the paper must not over-claim)

- Section 5(1) ties the notice to "every request ... for consent under section 6". A school that relies on a "legitimate use" under section 7 (for example 7(a), voluntarily provided data for a specified purpose) is not required to give a section 5 notice for that processing. This audit therefore measures **readiness of the public document**, not breach of the law. Rule 3 and section 5 are not in force until 13 May 2027.
- The Fourth Schedule item 3 exemption (educational institutions) disapplies only section 9(1) and (3), and only for "tracking and behavioural monitoring"; it does not remove the section 5 notice. Whether other school processing (admissions, fees, photographs) needs verifiable parental consent is contested in the commentary and is not decided here.
- Rule 3 does not itself contain the language requirement; that is in section 5(3).
