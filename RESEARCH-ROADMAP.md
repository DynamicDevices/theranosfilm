# Six improvements and the research they still need

## Viewer release — published, 21 November 2026

The published release puts the film explanation before the deeper investigation
links, adds chapter contents with stable anchors, and improves phone navigation.
The relationship map updates its evidence panel without following the reading
list anchor; panel resizing can still move the layout. The film guide now cites
the different distributor/festival runtime listings without assuming a cinema cut.
Release CSS and JavaScript URLs are content-versioned to avoid stale assets.

Validation: 49 Python tests, four JavaScript tests, syntax and research-data
checks pass. Browser checks confirm chapter navigation and no horizontal overflow
at a 390px phone viewport. This is not a screen-reader audit or WCAG certification.
PR [22](https://github.com/DynamicDevices/theranosfilm/pull/22) passed strict CI,
merged and was published through separate exact-build approval. All 41 public
HTTPS files matched the independent approved build. Deployment:
[44945025551](https://github.com/DynamicDevices/theranosfilm/actions/runs/44945025551).
The sitemap submission succeeded with 21 discovered pages. Google's page indexing
report was still processing at closeout; discovery is not proof of indexing or
ranking. No independent fact review is claimed.

Research still needs a checked film edition/transcript and engineer identification,
exact investor document delivery, complete assay validation and actual spending
records. Publish those limits plainly, not as answered questions.

## Workstream closeout

Implementation and publication are complete for this release. Further research
is separate from release acceptance. Keep these issues open until their own
evidence requirements are satisfied; a completed web page is not a completed
investigation.

| Workstream | Delivered | Remaining evidence / owning issue |
| --- | --- | --- |
| Film construction | Credits, edition-aware guide, recording/performance distinctions | Checked copy, scene locators and engineer identity; [#1](https://github.com/DynamicDevices/theranosfilm/issues/1) |
| Holmes and claims | Sourced background, document comparisons, allegations/findings separated | Timestamped film assertions and exact context; [#2](https://github.com/DynamicDevices/theranosfilm/issues/2) |
| Partners | Separate personal/business roles and dated source-linked profiles | Further involvement/knowledge evidence without inferred culpability; [#3](https://github.com/DynamicDevices/theranosfilm/issues/3) |
| Interviewer and filmmakers | Fielder/Oppenheim credits and attributed production accounts | Fuller direct background/commissioning sources; [#4](https://github.com/DynamicDevices/theranosfilm/issues/4) |
| Actress | Seyfried identification and attributed involvement account | Verified scenes and preparation/direction evidence; [#5](https://github.com/DynamicDevices/theranosfilm/issues/5) |
| Technology and patents | Platform explanation, patent chart and evidence limits | Complete assay validation and patent-title instruments |
| Investors and money | Dated claims, selected exhibits, competing accounts and classified figures | Exact document versions/delivery and actual period-matched spending ledger |
| Corrections and specialist input | Tracked JSON/PR route and separate review records supported | Genuine independent reviews; prepared briefs are not endorsements |
| Search discovery | Viewer-focused pages, canonical links, structured data and submitted sitemap | Google's processing/indexing outcome; no automated checks or ranking promise |

The separate cursor-config research skill remains committed and pushed but not
reviewed, merged or installed. Notifier instrumentation also remains separate.
Neither is a dependency of this published release. No outreach, monitoring,
credential change or new research programme is authorised by this closeout.

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
