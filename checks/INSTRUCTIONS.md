# Paper 11 check: the first-pass codes on the 19 school notices

**What it is for.** The paper's school results rest on only 19 school privacy notices, all coded by one coder (the first pass). This check asks you to look at every code on those 19 notices and say whether it is right. It is a check by the author, and you can see the first-pass code, so the paper must call it a non-blind author check of the first-pass coding, not an independent or blind second coder.

**What you have.**
- `11-check-sheet.xlsx`: the sheet "Checks" has 285 rows (19 notices x 15 checklist items). Each row gives the item, its rule, the first-pass code (Y = met, P = partly met, N = not met) and the passage of the notice that the code rests on. "Items" lists the 15 rules, and "Notices" lists the 19 notices.
- `notice-texts\<unit>.txt`: the full text of each notice, with line numbers. The sheet's "lines" column points into these files.

**What to do for each row.**
1. Read the item and its rule.
2. Read the quote. If you need more, open the notice's text file at the given lines. Judge only what the notice *says*.
3. In the yellow column "agree?", type **Y** if the first-pass code is right under the rule, or **N** if it is wrong.
4. If you typed N, put the correct code (**Y**, **P** or **N**) in the next yellow column.
5. Add a short note if it helps, for example the line that shows the code is wrong.

Tip: the rows are grouped by notice, 15 per notice. Read a notice once, then do its 15 rows.

**If you are unsure,** type **?** and say why in the note. Those rows are counted separately and not as agreement.

**Good to know.**
- The first pass did not record its evidence. The quotes were picked afterwards, so a weak quote alone is not a reason for N. Judge the code against the whole notice.
- On N rows, "Closest text found" is only there to help you, and "no matching text found" means nothing relevant was spotted. If you find something that changes the code, mark N and give the line.
- Names, e-mails, web addresses and phone numbers are blanked in the sheet. The text files are not blanked, so keep them on this machine, for research only. Do not share or upload them.

**How long it takes:** about 2.5 to 3.5 hours (about 25,000 words of notices). You can split it over several sittings, saving as you go.

**When done:** save the file under the same name and tell Claude: **11 check done**.
