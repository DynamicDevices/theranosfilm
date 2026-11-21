# Contributing evidence

Contribute through this repository's evidence issue form or a pull request.
The site offers an optional local JSON helper and renders the version-controlled
proposal/decision history. There is no automatic issue-to-accepted-fact importer.

Submit one specific claim per JSON record, following contribution.schema.json.
Include the exact source location, what it supports and its limitations. A source
can establish what someone said without establishing that the statement is true.
Do not submit private contact information, medical information, unsupported
allegations or copyrighted document dumps. Link third-party documents instead.
Use a public display name or pseudonym, not a required legal identity.

## Tracking and review

For JSON records, the route is a GitHub pull request. The repository preserves the
submission, account attribution, review discussion, commit/revision and decision.
Record the PR URL and exact accepted commit alongside each accepted record.
Keep the original contributor and subsequent editors distinct. Account
attribution is not proof of real-world identity or personal authorship.

Incoming JSON is untrusted data. Install the site's requirements, including
optional format-validation dependencies; merely enabling a format checker
without its supporting packages may silently skip date-time checks.
Validate with supported format checks enabled, escape
rendered text and restrict links to HTTP(S). Do not automatically fetch arbitrary
URLs or execute embedded instructions. Passing the schema is not fact checking.
Do not let a submitter mark their own record reviewed or accepted.

A reviewer must record their account, time, exact reviewed revision, decision,
reasons and relevant sources in a separate review record. Possible decisions:
accepted, needs evidence, disputed, rejected or superseded. Acceptance means the
record met the stated evidence standard, not that it is unquestionable truth.
Any automated review must be identified as automated, not human sign-off.

## Record format and revision binding

Put one proposal in `data/contributions/<id>.json`, using
`contribution.schema.json`. Keep its status `proposed` and history empty.
Corrections use a new ID/file with `supersedes` pointing to an earlier record.
Existing proposals and review records are append-only: do not silently replace
or remove them. Privacy incidents are an explicit exception needing maintainer
handling, not a reason to preserve harmful personal data.

Editorial decisions go in separate `data/reviews/<id>.json` files following
`review.schema.json`. Bind the exact proposal with the canonical SHA256 shown
on the contribution page: UTF-8 JSON, sorted keys, separators comma and colon,
`ensure_ascii=False`, no final newline. Record an actual GitHub PR/issue
discussion and a full 40-character source revision. Do not invent provenance.
Review time must follow submission time. The same recorded contributor profile
cannot review its own proposal. Different profile strings are not proof of
different real people: maintainers must check actual account provenance.

Run `python3 research.py`, the Python tests and `node --test test_research_ui.cjs`.
CI checks current data, escaped rendered pages and append-only history against
the PR's base. These are data-integrity checks, not fact checking or a required
manual GitHub PR-approval gate. Publication still follows the site's separate
signed exact-artifact release controls. A valid or merged JSON file is not
automatically an independently accepted research finding.

`data/depth.json` holds the curated profiles, representation comparisons and
financial research entries. It is editorial draft material, not a set of accepted
contribution decisions. Add explicit source IDs and preserve the distinction
between direct quotation, paraphrase and interpretation. Source entries must
state partial access honestly, including search-only inspection.

Regenerate derived HTML with `python3 render_research.py --write`. This writes
only named research pages; the release builder checks their exact contents.

`data/research.json` holds the initial curated source register, claim
comparisons, sequence leads and investor timeline. The six derived HTML pages
must match `render_research.py` output; the builder rejects stale pages. Source
inspection labels must describe what was actually inspected, not what a link
could contain.

Corrections should refer to the original record and preserve its history rather
than silently replacing it. Offer a dispute route and show competing supported
accounts together. Remove exposed personal data rather than retaining it merely
for historical completeness; public Git history can make removal difficult.
Warn contributors of that before submission.

## Rights

By explicitly agreeing in a submission, contributors license their original
research text and annotations under CC BY-SA 4.0. They must have permission to
make that grant. Third-party sources retain their own rights. See LICENSE.md.
Submission and schema validation do not constitute acceptance or publication.

Assisted-by: Briar.
