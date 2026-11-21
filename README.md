# Theranos Film — Independent Evidence Analysis

[![Site CI](https://github.com/DynamicDevices/theranosfilm/actions/workflows/site.yml/badge.svg?branch=main)](https://github.com/DynamicDevices/theranosfilm/actions/workflows/site.yml?query=branch%3Amain)

An independent, public research project examining *You Can See Everything* and the Theranos story: what the film shows, what the underlying sources establish, and what remains unanswered.

**Website:** [theranosfilm.com](https://theranosfilm.com) · **Research and corrections:** [GitHub issues](https://github.com/DynamicDevices/theranosfilm/issues)

The public website is live over HTTPS. Source changes reach it only through a separate approved release. This repository contains the analysis, source register, contribution records and publishing code. It is not affiliated with Theranos, the filmmakers or the people discussed.

## What we investigate

- **The film and its construction:** interviews, recordings, performances and recreations; what can and cannot be established scene by scene.
- **The people:** Elizabeth Holmes, Billy Evans, Ramesh “Sunny” Balwani, Nathan Fielder, Lance Oppenheim and Amanda Seyfried, keeping personal and professional roles distinct.
- **The technology:** blood sampling, assays, the proposed platform, patents, clinical validation and the claim that Theranos used the wrong technology.
- **The investor claims:** what was represented as working at the time, what was a future ambition, and what original documents actually say.
- **The money and the failure:** financing and expenditure questions, without inventing a spending breakdown or treating an open question as an established finding.

This is an initial, evolving analysis—not a completed biography, scene audit, patent review, clinical evaluation or forensic accounting exercise.

## Follow the evidence

The site connects claims, people, chronology and sources. Its interactive relationship map has readable HTML alternatives; the chapters remain available without WebGL or JavaScript. Visual proximity or connections do not establish guilt or evidential strength.

Read the [film sequence guide](film-guide.html), [claim-to-evidence comparisons](claims.html), [people analysis](analysis.html), [technology explanation](technology.html), [investor timeline](timeline.html), [investor representations](investors.html), [money questions](money.html) and [source register](sources.html). Scene timestamps and the unidentified engineer remain explicit gaps, not invented facts.

We distinguish allegations, court findings, source observations and interpretation. A document can establish what someone claimed without proving that the claimed technology worked. Inspection limits, uncertainty and competing supported accounts belong alongside the evidence. We do not infer dishonesty from body language, diagnose participants or imply guilt by association.

The latest research adds selected filed-trial testimony identifying investor-facing Exhibit 1853 and Dynasty Financial II LLC, reported 2011–2013 operating expenses and R&D, the limited FDA HSV-1 assay clearance, independent comparative testing, and the filmmakers' account of the film's two-part structure. The people chapter documents Christian Holmes's specific Enron role without implying involvement in its fraud. Sources retain exact locations and access limits: these advances do not complete the cash ledger, authenticate the engineer or supply checked scene timestamps.

## Contribute or correct something

[Open an evidence issue](https://github.com/DynamicDevices/theranosfilm/issues/new?template=evidence.yml) with one specific claim or correction, an exact source location, what it supports and its limitations. The [contribution page](contribute.html) offers a local JSON helper and readable record history. Source-backed JSON contributions can be proposed through a pull request using [contribution.schema.json](contribution.schema.json). Read [CONTRIBUTING.md](CONTRIBUTING.md) for evidence, attribution, review and rights requirements.

Submissions are proposals, not automatically accepted facts. GitHub records the submitting account, discussion and revisions; an account is not proof of real-world identity. Separate editorial records use [review.schema.json](review.schema.json) to bind a decision to the exact proposal hash and recorded source revision. Corrections preserve earlier records. Schema checks are not fact checking, and there is no automatic issue-to-accepted-fact importer.

The source register, claims, sequence leads and timeline live in [data/research.json](data/research.json). Readable pages are deterministically rendered from those records with escaped text. CI rejects stale pages, invalid links, changed historical contribution records and mismatched review hashes. See [the access page](accessibility.html) for reading alternatives and testing limits; no WCAG certification is claimed.

Do not submit private medical or contact information, unsupported allegations or copyrighted document dumps. Public Git history can be difficult to remove; link to third-party sources rather than copying them wholesale.

## Publication and access

The site is static, with readable chapters, accessible relationship links and no advertising, tracking scripts or remote fonts. The next release adds a Hits.sh counter image to the homepage footer: its provider receives visitors' IP addresses and request metadata. The figure represents approximate badge loads, not unique readers or an audited audience. Local source previews use an inactive placeholder. See [counter and privacy](about.html#views-privacy). Releases include canonical URLs, a sitemap and structured metadata to help readers and search engines find the analysis; inclusion or ranking is not guaranteed.

Changes use pull requests and genuine current-base CI, without required manual PR approval. Preloop is paused for this project at Alex's request. Publication separately checks the approved main commit and exact build manifest. See [Actions](https://github.com/DynamicDevices/theranosfilm/actions) for the actual workflow state; a passing check is not proof that the public domain is live.

## Rights and independence

Original research text and annotations are licensed under **CC BY-SA 4.0**; see [LICENSE.md](LICENSE.md). Third-party documents, trademarks and images retain their owners' rights. The Creative Commons grant does not license the software; no software licence has been selected.

Theranos-inspired colours identify the subject of the research, not an official affiliation. Private working research and authority records are excluded from this repository and the published site.

Assisted-by: Briar.

## New analysis chapters

This independent analysis of **You Can See Everything** follows the people,
Theranos technology, investor representations and money questions that need
more than a film account to resolve. It is not affiliated with Theranos or the
filmmakers. Editorial draft; not independently fact-checked. Briar assisted.

The reading chapters include:

- [Start after watching](start-here.html): a short, spoiler-labelled reading route.
- [People and connections](analysis.html): six attributed profiles, with roles and limits kept separate.
- [Working now or possible later?](capabilities.html): investor wording, technical proof and later accounts.
- [Where did the money go?](money.html): financial definitions, source accounts and missing records—not an invented spending chart.
- [Inspect the evidence](evidence.html): source locations, inspection scope, uses and correction routes.
- Search/social metadata, an original preview image and visible editorial attribution.

These source files do not establish that the changed build is live. Production
publication requires its own exact-build approval and verification.

Curated profiles and comparisons are in [data/depth.json](data/depth.json).
The [research roadmap](RESEARCH-ROADMAP.md) records what remains unfinished.
Original research is CC BY-SA 4.0; third-party sources retain their rights.

## Primary-source investigations

The next research update adds six connected dossiers, backed by
[validated public JSON](data/dossiers.json):

- [Engineer investigation](engineer.html): technical hypotheses and a later-company patent lead; speaker and exchange remain unauthenticated.
- [Peterson investor case](investor-case.html): a court-described projection and an internal financial exhibit, with the delivery/reliance gap visible.
- [Patent claim chart](patent-map.html): selected granted elements of US8283155B2; product implementation and legal title remain unverified.
- [Scene companion](scene-companion.html): edition-aware verification records with deliberately empty timestamps until a lawful recording is checked.
- [Financial records](financial-records.html): visually checked figures, forecast/snapshot distinctions and reproducible arithmetic—not a complete spending ledger.
- [Specialist briefs](specialists.html): five focused review tasks and an invitation draft. Nobody has been contacted or endorsed the work through this workstream.

The source includes an amended appellate opinion and public trial Exhibit 15031.
The latter's projected income, proforma cash flow and reported balance sheet are
not interchangeable. The balance sheet's thousands-of-dollars units are explicitly
converted; forecasts are never presented as actual payments.

These dossiers do not complete every research question. Direct specialist
outreach needs selected recipients and approved sends; publication of changed
site bytes retains separate exact-build controls.
