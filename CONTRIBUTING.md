# Contributing evidence

This is the proposed contribution contract. No public repository, submission
service or verified contributor workflow is connected yet.

Submit one specific claim per JSON record, following contribution.schema.json.
Include the exact source location, what it supports and its limitations. A source
can establish what someone said without establishing that the statement is true.
Do not submit private contact information, medical information, unsupported
allegations or copyrighted document dumps. Link third-party documents instead.
Use a public display name or pseudonym, not a required legal identity.

## Tracking and review

The planned route is a GitHub pull request. The repository will preserve the
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
