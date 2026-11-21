# Six improvements and the research they still need

## Viewer release — current candidate, 21 November 2026

The new candidate puts the film explanation before the deeper investigation
links, adds chapter contents with stable anchors, and improves phone navigation.
The relationship map updates its evidence panel without following the reading
list anchor; panel resizing can still move the layout. The film guide now cites
the different distributor/festival runtime listings without assuming a cinema cut.
Release CSS and JavaScript URLs are content-versioned to avoid stale assets.

Validation: 49 Python tests, four JavaScript tests, syntax and research-data
checks pass. Browser checks confirm chapter navigation and no horizontal overflow
at a 390px phone viewport. This is not a screen-reader audit or WCAG certification.
The candidate is not yet published; strict CI, protected merge and exact-build
production approval remain. The successful sitemap submission is already recorded;
discovery is not proof of indexing or ranking. No independent fact review is claimed.

Research still needs a checked film edition/transcript and engineer identification,
exact investor document delivery, complete assay validation and actual spending
records. Publish those limits plainly, not as answered questions.

## Primary-source follow-up — 21 November 2026

Alex subsequently asked Briar to work through the engineer identification,
investor case, patent/product mapping, scene companion, financial reconstruction
and specialist contributions. New source dossiers are in `data/dossiers.json`,
validated against `dossiers.schema.json` and rendered as six connected chapters.

The work adds selected appellate/court-exhibit evidence, a granted-claim chart,
classified financial figures and derived arithmetic checks. It does not identify
the engineer, authenticate scene timestamps, prove delivery of a particular
financial version to an investor, reconstruct all actual spending or recruit
specialists. Five review briefs and an unsent draft are prepared; direct outreach
needs chosen recipients and approved sends. These gaps must not be closed merely
because a page or schema exists.

The live site and the current source branch can differ. Use the actual deployment
receipt rather than treating a generated page as published.

## Earlier site structure

Alex requested these six changes on 21 November 2026. The implementation adds
readable chapters and evidence links; it does not make unresolved research
complete. This is independent commentary, not an official film site.

| Improvement | Source implementation | Still needed |
| --- | --- | --- |
| Start-here guide | `start-here.html`: spoiler notice, recording/performance distinction, reading route | Checked film copy/transcript and scene boundaries |
| People and connections | `analysis.html`: Holmes, Balwani, Evans, Fielder, Oppenheim, Seyfried | Fuller independently sourced biographies, editorial responsibility and commissioning history |
| Present versus future | `capabilities.html`: dated-source comparisons, excerpt/paraphrase labels, proof requirements | Investor-by-investor delivery, qualifications, technical records and checked film statements |
| Money investigation | `money.html`: receipts/valuation/revenue/spending distinctions, public-source accounts, cash reconciliation | Actual period-matched ledger and public expenditure evidence |
| Inspectable evidence | `evidence.html`: permanent source IDs, locators, scope, uses and correction links | More primary records and real separately recorded editorial reviews |
| Identity and discovery | Independent-site disclosures, editor/date/status, Article metadata, canonical pages, original social image | Actual deployment verification and indexing evidence; no ranking or AI-citation promises |

The engineer and the remembered “wrong technology” passage remain unidentified.
Patent scope, ownership and implementation still need claim-by-claim work.
Fielder's publicity page was inaccessible; its indexed extract is labelled and
must not be described as a full source inspection.

Do not infer dishonesty from nodding or other behaviour. Do not infer wrongdoing
from personal, family or creative connections. Distinguish civil allegations,
criminal verdicts, participant accounts and project interpretation.

Contributions use the existing issue/JSON PR route and separate exact-hash
editorial records. A schema pass is not fact checking; profile labels are not
authenticated identity. Preserve append-only submitted records and corrections.

Delivery retains strict genuine site CI and protected history. Preloop remains
paused for this repository; there is no required human approving review.
Source integration is not production publication. Changed build bytes need
separate exact-artifact approval. No DNS or HTTPS changes are part of this work.

Assisted-by: Briar
