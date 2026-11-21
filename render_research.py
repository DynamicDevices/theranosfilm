"""Render readable, source-linked research pages. All incoming text is escaped."""
import html
import json
from datetime import datetime

from research import ROOT, digest, load, load_depth, load_dossiers
from render_depth import sections
from render_dossiers import PAGES as DOSSIER_PAGES, sections as dossier_sections

PAGES = ('film-guide.html', 'claims.html', 'timeline.html', 'contribute.html',
         'accessibility.html', 'technology.html', 'start-here.html',
         'analysis.html', 'capabilities.html', 'money.html', 'evidence.html') + DOSSIER_PAGES


def esc(value):
    return html.escape(str(value), quote=True)


def page(title, description, eyebrow, intro, body, active):
    nav = [('start-here.html', 'Start here'), ('film-guide.html', 'Film guide'), ('claims.html', 'Claims'),
           ('analysis.html', 'People'), ('technology.html', 'Technology'),
           ('timeline.html', 'Timeline'), ('money.html', 'Money'),
           ('evidence.html', 'Evidence'), ('contribute.html', 'Contribute')]
    links = ''.join(f'<a href="{href}"' + (' aria-current="page"' if href == active else '')
                    + f'>{label}</a>' for href, label in nav)
    return (f'<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex"><meta name="description" content="{esc(description)}">'
            f'<title>{esc(title)} — Theranos Film</title><link rel="stylesheet" href="editorial.css">'
            '<script src="research-ui.js" defer></script></head><body>'
            '<a class="skip-link" href="#article">Skip to analysis</a><header>'
            '<a class="wordmark" href="index.html">theranos<span>film / independent analysis</span></a>'
            f'<nav aria-label="Main">{links}</nav></header>'
            f'<main id="article" class="reading longform"><p class="eyebrow">{esc(eyebrow)}</p>'
            f'<h1>{esc(title)}</h1><p class="standfirst">{esc(intro)}</p>'
            '<p class="editorial-note">Edited by the Theranos Film project · Briar assisted · '
            '<time datetime="2026-11-21">Updated 21 November 2026</time>. '
            'Editorial draft; not independently fact-checked. '
            '<a href="about.html">About this independent project</a> · '
            '<a href="contribute.html">Corrections and review history</a>.</p>'
            f'{body}</main>'
            '<footer>Independent research in progress · 21 November 2026. '
            'Not affiliated with Theranos, the filmmakers or any agency. '
            '<a href="evidence.html">Source register and inspection limits</a> · '
            '<a href="accessibility.html">Access and reading options</a> · '
            '<a href="contribute.html">Corrections and history</a>.'
            '<span>Original research: <a href="LICENSE.md">CC BY-SA 4.0</a>. '
            'Third-party sources retain their rights. Assisted-by: Briar.</span></footer></body></html>\n')


def render(root=ROOT):
    research, proposals, reviews = load(root)
    depth = load_depth(root, research)
    dossiers = load_dossiers(root, research)
    sources = {s['id']: s for s in research['sources']}

    def references(ids):
        if not ids:
            return '<p class="limit">No source yet verifies this observation. Treat it as an open question.</p>'
        return '<details class="source-notes"><summary>Sources and inspection limits</summary><ul>' + ''.join(
            f'<li><a href="evidence.html#source-{esc(i)}">{esc(sources[i]["title"])}</a>'
            f' · <a href="{esc(sources[i]["url"])}">Original source</a>'
            f'<p>{esc(sources[i]["kind"])} · {esc(sources[i]["locator"])}</p>'
            f'<p>{esc(sources[i]["inspected"])}. {esc(sources[i]["limit"])}</p></li>' for i in ids) + '</ul></details>'

    film = ('<div class="callout"><h2>Was the first half acted?</h2>'
            '<p>The festival account describes documentary access to Holmes and Evans. '
            'The participant interview identifies a later performance element involving Seyfried. '
            'That does not justify calling every first-half shot unstaged, or every later shot a recreation. '
            'Check each sequence, not just which half it belongs to.</p></div>'
            '<p><strong>Spoiler notice:</strong> this guide discusses changes of form and performance. '
            'No film copy or authenticated transcript was available for a timed scene audit. '
            'The entries below are research anchors, not a complete shot list; their order is not a verified edit timeline.</p>'
            '<nav aria-label="Film guide sections"><ul>' + ''.join(
                f'<li><a href="#{esc(s["id"])}">{esc(s["title"])}</a></li>' for s in research['scenes']) + '</ul></nav>')
    for s in research['scenes']:
        film += (f'<section class="evidence-card" id="{esc(s["id"])}"><p class="status">{esc(s["type"])}</p>'
                 f'<h2>{esc(s["title"])}</h2><p>{esc(s["account"])}</p>'
                 f'<dl><dt>Scene locator</dt><dd>{esc(s["timecode"] or "Not verified — timestamp needed")}</dd>'
                 f'<dt>Inspection status</dt><dd>{esc(s["verification"])}</dd>'
                 f'<dt>Question to test</dt><dd>{esc(s["question"])}</dd></dl>' + references(s['sources'])
                 + f'<p><a href="contribute.html?claim={esc(s["id"])}">Add a source or scene reference for this entry</a></p></section>')
    film += ('<h2>How to verify a scene</h2><ol><li>Record the edition, total runtime and your timecode convention '
             '(including whether distributor cards are counted).</li><li>Record the speaker and exact words only after checking '
             'the recording; otherwise label a recollection or paraphrase.</li><li>Identify camera footage, inserted archive, '
             'performance and reconstructed speech separately. Note captions and disclosed reconstruction sources.</li>'
             '<li>Compare the passage with a dated source. Preserve surrounding questions, edits and qualifications.</li>'
             '<li>Submit a locator and short necessary description, not an unauthorised copy of the film.</li></ol>'
             '<h2>Nodding is an observation, not a verdict</h2><p>A useful coding exercise would count visible nods in a '
             'defined passage, identify cuts and listening/speaking context, and state uncertainty. It cannot establish '
             'dishonesty, diagnosis or motive. <a href="claims.html#claim-nodding">Read the evidence limits.</a></p>')

    claims = ('<p>These entries separate a film question, source evidence, counterweight and a provisional assessment. '
              'The assessment is the project’s analysis—not an independent review decision. '
              'Each entry has a permanent link and a correction route.</p>'
              '<div class="enhancement" data-enhancement hidden><label for="claim-search">Find a claim</label>'
              '<input type="search" id="claim-search" placeholder="Try patents, investor or platform">'
              '<label for="claim-category">Topic</label><select id="claim-category">'
              '<option value="all">All topics</option><option value="technology">Technology</option>'
              '<option value="investors">Investors</option><option value="film">Film</option>'
              '<option value="law">Law</option></select><p id="claim-count" role="status" aria-live="polite"></p></div>'
              '<nav aria-label="Claim index"><ul>' + ''.join(
                  f'<li><a href="#{esc(c["id"])}">{esc(c["question"])}</a></li>' for c in research['claims']) + '</ul></nav>')
    for c in research['claims']:
        claims += (f'<article id="{esc(c["id"])}" class="evidence-card" data-claim data-category="{esc(c["category"])}">'
                   f'<p class="status">{esc(c["basis"])}</p><h2>{esc(c["question"])}</h2>'
                   '<dl class="claim-comparison">' + ''.join(
                       f'<dt>{label}</dt><dd>{esc(c[key])}</dd>' for key, label in (
                           ('presentation', 'The question raised'), ('evidence', 'What the evidence supports'),
                           ('qualification', 'Qualifications and counterweight'), ('finding', 'Provisional assessment'),
                           ('next', 'What would resolve the gap'))) + '</dl>' + references(c['sources'])
                   + f'<p><a href="contribute.html?claim={esc(c["id"])}">Correct or challenge {esc(c["id"])}</a></p></article>')

    timeline = ('<p>This is a source-linked chronology, not a complete transaction ledger. Periods are labelled as periods; '
                'a year-only entry does not imply an exact day. A later account must not be silently substituted for a contemporaneous representation.</p>'
                '<ol class="timeline">')
    for event in sorted(research['timeline'], key=lambda e: e['sort']):
        timeline += (f'<li id="{esc(event["id"])}"><p class="status">{esc(event["date"])} · {esc(event["kind"])}</p>'
                     f'<h2>{esc(event["event"])}</h2><p>{esc(event["meaning"])}</p>'
                     f'<p class="limit"><strong>Still needed:</strong> {esc(event["gap"])}</p>'
                     + references(event['sources']) + '</li>')
    timeline += ('</ol><h2>Reconstruct an investor’s information, not a general mood</h2>'
                 '<div class="table-scroll"><table><caption>Evidence needed for each investment decision</caption>'
                 '<thead><tr><th scope="col">Record</th><th scope="col">Why it matters</th></tr></thead><tbody>'
                 '<tr><th scope="row">Investor and decision date</th><td>Sets the relevant information window; protect private personal data.</td></tr>'
                 '<tr><th scope="row">Exact deck and delivery</th><td>Separates a surviving version from what that investor actually received.</td></tr>'
                 '<tr><th scope="row">Demonstration protocol</th><td>Identifies device, samples, external processing, failures and selection of results.</td></tr>'
                 '<tr><th scope="row">Oral qualifications and correspondence</th><td>Tests whether a capability was present, future, conditional or contradicted elsewhere.</td></tr>'
                 '<tr><th scope="row">Technical evidence available then</th><td>Maps each assay claim to its validation, limitations and known problems at that date.</td></tr>'
                 '<tr><th scope="row">Subscription and cash records</th><td>Distinguishes commitment, money received, share price and valuation.</td></tr>'
                 '</tbody></table></div><h2>Why did people invest?</h2>'
                 '<p>Do not infer a particular investor’s motives from the size of a cheque or a famous name. '
                 'A documented pitch can suggest proposed attractions—market need, intellectual property, convenience, '
                 'business forecasts or endorsements—but an explanation of actual reliance needs that investor’s records and testimony.</p>'
                 '<h2>Where did the money go?</h2><p>Money raised is not the amount spent, and valuation is not cash. '
                 'A defensible reconciliation needs opening cash, dated financing receipts, operating and capital payments, '
                 'asset-sale proceeds, liabilities and closing cash. Payroll, development, premises, retail rollout and '
                 'legal costs are categories to investigate, not verified spending allocations. '
                 '<a href="money.html">Read the expenditure framework and its gaps.</a></p>')

    technology = ('''<div class="callout"><h2>The core idea—and the hard part</h2>
<p>Offer useful blood testing from a very small sample, with an automated system that could make testing easier to access. That is a service promise plus an engineering programme, not a single discovery. The hard part is reliably delivering every advertised test, on the stated sample, in the stated workflow.</p></div>
<h2>Five layers that must not be collapsed into “the invention”</h2>
<div class="table-scroll"><table><caption>From finger-prick to clinically usable information</caption>
<thead><tr><th scope="col">Layer</th><th scope="col">What must work</th><th scope="col">What could invalidate the claim</th></tr></thead><tbody>
<tr><th scope="row">1. Collection</th><td>Obtain sufficient, representative material in a suitable container.</td><td>Clotting, cell damage, contamination, tissue-fluid admixture, or an insufficient sample.</td></tr>
<tr><th scope="row">2. Preparation</th><td>Transport, separate, mix or dilute the sample as required by the assay.</td><td>Timing, temperature, retained volume, dilution uncertainty and unreported manual steps.</td></tr>
<tr><th scope="row">3. Measurement</th><td>Use an appropriate detection method for each intended analyte.</td><td>Interference, inadequate signal, calibration errors or the wrong measurement range.</td></tr>
<tr><th scope="row">4. Instrument and workflow</th><td>Integrate modules and controls with repeatable operation and realistic throughput.</td><td>Carryover, failed runs, selected demonstrations, undisclosed off-device processing or third-party instruments.</td></tr>
<tr><th scope="row">5. Report and intended use</th><td>Translate validated measurements into an accurate, usable report within the claimed scope.</td><td>Misleading reference ranges, unsupported interpretation, missing limitations or unjustified test-menu claims.</td></tr>
</tbody></table></div>
<p>This is a general engineering framework, not an assertion that each listed failure occurred in every Theranos device. Each mechanism needs device-, assay- and date-specific evidence.</p>
<h2>What does “platform” actually mean?</h2>
<p>A platform can be a common sample-handling system, a shared cartridge, several instruments in one enclosure, software linking modules, or a laboratory service. Those are different architectures. Cell counting, chemical concentration measurements, antibody-based assays and nucleic-acid tests require different measurement principles and often different preparation.</p>
<p>Integration is useful engineering, but it does not make every module clinically validated. A proposed later system must not be used as proof that an earlier product could already do the same things.</p>'''
                  + references(['minilab']) + '''
<h2>Why a tiny sample is not a universal shortcut</h2>
<p>A usable sample has a budget: collection losses and retained material reduce what can be divided between tests, quality controls and repeat measurements. The relevant volume is the amount of original sample reaching each assay, not merely the amount collected.</p>
<p>Adding diluent increases liquid volume, not the amount of target material originally present. Whether a diluted sample is usable depends on the validated assay range, preparation uncertainty and detection performance. Some tests can work at small volumes; that does not establish that all tests can share one tiny sample under one protocol.</p>
<p>Miniaturising a reaction also leaves transport, mixing, contamination control, calibration, maintenance, waste handling and failed-run recovery to solve. The service has to work across realistic patients and samples, not just in a selected demonstration.</p>
<h2>How to test the claim properly</h2>
<ol><li><strong>Freeze the claim:</strong> assay, device/version, sample type and volume, preparation, turnaround, throughput and intended use.</li>
<li><strong>Choose the comparison:</strong> an appropriate reference/comparator method and justified acceptance criteria, not simply a visually similar number.</li>
<li><strong>Measure performance:</strong> bias and repeatability, reportable range, interference, sample stability, invalid results and relevant sensitivity/specificity measures.</li>
<li><strong>Test realistic operation:</strong> different operators, sites, lots and clinically relevant samples; include failures and repeats rather than hiding them.</li>
<li><strong>Keep the scope:</strong> a validated assay is not a validated menu, and analytical agreement is not automatically clinical usefulness or regulatory permission.</li></ol>
<h2>Did any Theranos technology genuinely work?</h2>
<p>FDA K143236 cleared the HSV-1 IgG assay for specified uses and specimen types, including fingerstick whole blood, in July 2015. The 7 July letter corrects a 2 July letter. That is a real, limited regulatory achievement—not clearance of a universal testing platform, every earlier claim or every result. “Nothing worked” is too broad.</p>'''
                  + references(['fda-hsv1']) + '''
<h2>What the independent comparison found</h2>
<p>The 2016 JCI study compared 22 measurements in 60 healthy adults using Theranos, Quest and LabCorp. It found significant interservice differences and more out-of-range flags at Theranos. This supports concerns about the delivered service, not a claim every result was wrong. It is not a complete instrument teardown, a study of every assay, or proof of which machine produced each result.</p>'''
                  + references(['jci']) + '''
<p>The SEC alleged that Theranos used third-party analyzers for most patient tests while representing broader proprietary capability. The DOJ’s trial account describes limitations in the proprietary technology. Keep the civil allegations, reported trial evidence and actual verdict distinct.</p>'''
                  + references(['sec-release', 'doj']) + '''
<h2>What was the intellectual property?</h2>
<p>Start with a claim chart, not a patent count. For each relevant patent, record the priority date, inventors, owner at the relevant date, granted claims and any later assignment. Compare each claimed component with the actual product configuration and the capability pitched at the time.</p>
<p>A specification can describe embodiments and aspirations broader than the legal protection ultimately granted. Neither a patent grant nor an application is a clinical performance certificate. Trade secrets, software, know-how, contracts and regulatory evidence are separate assets and separate questions.</p>'''
                  + references(['patent', 'exhibit']) + '''
<h2>Was it “the wrong technology”?</h2>
<p>We have not authenticated the engineer’s identity or the remembered exchange. It would be misleading to attribute a technical verdict to an unidentified speaker. The phrase could concern sample preparation, detection method, engineering architecture, development sequence or economics; those remain hypotheses.</p>
<p>The next useful step is the full passage and a precise comparison: what was being measured, why the chosen method was said to fail, which alternative was proposed, and what evidence supports that alternative. A later patent or successful method does not prove the earlier task was impossible; a promising experiment does not prove a commercial platform was ready.</p>
<p><a href="film-guide.html#sequence-engineer">Contribute the scene locator</a> · <a href="claims.html#claim-platform">Compare platform claims with their evidence</a> · <a href="timeline.html">Place the claim in its investor timeline</a></p>''')

    contributions = '''<div class="callout"><h2>A correction should leave a trace</h2>
<p>Proposals stay proposals. A separate editorial record names the reviewed JSON digest, decision, reasons, sources and the GitHub discussion/revision. That is an accountable record—not proof that the contributor is a particular real-world person, or that acceptance makes a claim unquestionably true.</p></div>
<h2>Two ways to contribute</h2><ol><li><a href="https://github.com/DynamicDevices/theranosfilm/issues/new?template=evidence.yml">Open a source-backed evidence issue on GitHub</a>. GitHub records the submitting account and discussion; you decide what to submit.</li>
<li>Prepare one JSON proposal below and add it in a pull request under <code>data/contributions/</code>. Read <a href="CONTRIBUTING.md">the contribution rules</a> and <a href="contribution.schema.json">the schema</a>.</li></ol>
<p>No account or token is collected by this website. Nothing in the form is sent automatically, stored by this page or fetched from a submitted source URL. GitHub submission is a separate, explicit action.</p>
<div class="enhancement" data-enhancement hidden><h2>Prepare a JSON proposal</h2>
<form id="contribution-form"><p><label for="proposal-id">Short unique record ID (lowercase letters, numbers and hyphens)</label><input id="proposal-id" name="id" required pattern="[a-z0-9][a-z0-9-]+" placeholder="film-runtime-correction"></p>
<p><label for="proposal-claim">One specific claim or correction</label><textarea id="proposal-claim" name="claim" required rows="4"></textarea></p>
<p><label for="proposal-name">Public display name or pseudonym</label><input id="proposal-name" name="display_name" required autocomplete="off"></p>
<p><label for="proposal-profile">Public profile URL (self-reported)</label><input id="proposal-profile" name="profile_url" type="url" required placeholder="https://github.com/your-account"></p>
<p><label for="proposal-source">Source URL</label><input id="proposal-source" name="source_url" type="url" required></p>
<p><label for="proposal-locator">Exact page, paragraph or scene locator</label><input id="proposal-locator" name="locator" required></p>
<p><label for="proposal-supports">What this source supports</label><textarea id="proposal-supports" name="supports" required rows="3"></textarea></p>
<p><label for="proposal-kind">Source type</label><select id="proposal-kind" name="kind"><option value="primary_document">Primary document</option><option value="legal_allegation">Legal allegation</option><option value="judicial_finding">Judicial finding</option><option value="reporting">Reporting</option><option value="patent">Patent</option><option value="film">Film</option><option value="other">Other</option></select></p>
<p><label for="proposal-limits">Limitations, alternative explanations and unresolved points</label><textarea id="proposal-limits" name="limitations" required rows="3"></textarea></p>
<p><label for="proposal-parent">Existing record this corrects, if any</label><input id="proposal-parent" name="supersedes" pattern="[a-z0-9][a-z0-9-]+"></p>
<p><label for="proposal-rights">Rights note (link rather than copy third-party documents)</label><textarea id="proposal-rights" name="rights_note" required rows="2"></textarea></p>
<p><label class="consent" for="proposal-consent"><input type="checkbox" id="proposal-consent" name="consent" required> I have the right to contribute this original text under CC BY-SA 4.0. I understand it will be public and may remain in Git history. I have not included private medical/contact information or unauthorised document copies.</label></p>
<button type="submit">Prepare JSON locally</button><p id="proposal-status" role="status" aria-live="polite"></p></form>
<label for="proposal-output">Prepared JSON—inspect before submitting</label><textarea id="proposal-output" rows="14" readonly></textarea>
<p><a id="proposal-download" hidden download="contribution.json">Download the JSON proposal</a></p></div>
<noscript><p>The optional JSON helper needs JavaScript. The GitHub evidence form, contribution rules, source-linked entries and history below do not.</p></noscript>
<h2>Public proposals and decision history</h2><p>Names/profile links below are recorded labels, not independently authenticated identities. Editorial decisions are version-controlled maintainer records. Acceptance is an editorial state, not a legal finding. An automated decision is labelled as automated.</p>'''
    for identifier, proposal in proposals.items():
        record_hash = digest(proposal)
        events = sorted((r for r in reviews.values() if r['contribution_id'] == identifier), key=lambda r: (datetime.fromisoformat(r['reviewed_at'].replace('Z', '+00:00')), r['id']))
        contributions += (f'<article id="{esc(identifier)}" class="evidence-card"><p class="status">Submitted as proposed</p>'
                          f'<h3>{esc(proposal["claim"])}</h3><p>Contributor label: <a href="{esc(proposal["contributor"]["profile_url"])}">'
                          f'{esc(proposal["contributor"]["display_name"])}</a> · {esc(proposal["contributor"]["identity_status"])}</p>'
                          f'<p>Recorded submission time: {esc(proposal["submitted_at"])}</p><p>{esc(proposal["limitations"])}</p>'
                          f'<p>Canonical submission SHA256: <code class="digest">{record_hash}</code></p>'
                          f'<p><a href="data/contributions/{esc(identifier)}.json">Read the submitted JSON</a> · '
                          f'<a href="https://github.com/DynamicDevices/theranosfilm/commits/main/data/contributions/{esc(identifier)}.json">Git revision history</a></p>')
        for source in proposal['sources']:
            contributions += f'<p><a href="{esc(source["url"])}">Source · {esc(source["locator"])}</a>: {esc(source["supports"])}</p>'
        if proposal.get('supersedes'):
            contributions += f'<p>Corrects <a href="#{esc(proposal["supersedes"])}">{esc(proposal["supersedes"])}</a>; the earlier record remains visible.</p>'
        children = [p['id'] for p in proposals.values() if p.get('supersedes') == identifier]
        if children:
            contributions += '<p>Later correction proposals: ' + ', '.join(f'<a href="#{esc(c)}">{esc(c)}</a>' for c in children) + '.</p>'
        if not events:
            contributions += '<p><strong>No editorial decision recorded.</strong> This is not an accepted finding.</p>'
        for review in events:
            reviewer = review['reviewer']
            contributions += (f'<section class="review-event"><h4>{esc(review["decision"].replace("_", " "))}</h4>'
                              f'<p>{esc(review["reviewed_at"])} · {esc(reviewer["kind"])} · '
                              f'<a href="{esc(reviewer["profile_url"])}">{esc(reviewer["display_name"])}</a></p>'
                              f'<p>{esc(review["reasons"])}</p><p><a href="{esc(review["provenance"]["url"])}">Recorded review discussion</a> · '
                              f'<a href="https://github.com/DynamicDevices/theranosfilm/tree/{esc(review["provenance"]["revision"])}">Exact recorded source revision</a> · '
                              f'<a href="data/reviews/{esc(review["id"])}.json">Review JSON</a></p>')
            for source in review['sources']:
                contributions += f'<p><a href="{esc(source["url"])}">Review source · {esc(source["locator"])}</a></p>'
            contributions += '</section>'
        contributions += '</article>'
    contributions += '''<h2>How decisions and disputes work</h2><ol><li>A proposal is validated as data, not accepted as fact. Public GitHub account history supplies attribution; profile fields alone do not.</li>
<li>A maintainer records a separate decision using <a href="review.schema.json">review.schema.json</a>, the exact proposal hash and a source revision/discussion. Self-review under the same recorded profile is rejected. This check cannot prove distinct real people.</li>
<li>Keep source support, counterevidence and reasons visible. Correct an existing record with a new proposal referencing <code>supersedes</code>; append a decision rather than overwriting history.</li>
<li>Schema checks do not prevent a deceptive person inventing a different profile. Maintainers must check the actual GitHub provenance and evidence before publication; there is no automatic issue-to-accepted-fact importer.</li>
<li>Privacy takes priority over preserving an exposed person's data. Report exposure without repeating the sensitive content; do not put secrets into public issues.</li></ol>'''

    accessibility = '''<h2>Reading and navigation</h2><ul><li>The film guide, evidence comparisons, timeline, technology explanation and contribution history are static HTML. They remain readable with JavaScript and WebGL disabled.</li>
<li>Use the skip link at the beginning of each page to reach the main content. Headings and permanent fragment links let you share individual questions.</li>
<li>The optional claim search announces the result count. Clear the search to restore all entries; opening a claim fragment restores its entry if a filter hid it.</li>
<li>The map has readable evidence entries. Positions, colour and connecting lines are not the only way to understand a relationship or its status.</li>
<li>Print styles produce a reading copy. Forms and search controls are optional; GitHub's native evidence form is available without this site's JavaScript.</li></ul>
<h2>What has been tested</h2><p>Structural automated checks cover page titles, links and fragment targets, source references, unsafe URL handling, schema formats, review-to-proposal hashes, append-only records and release metadata. On 21 November 2026, browser checks covered 390-pixel and 1280-pixel layouts, keyboard skip-link access, claim filtering and direct links, script-free homepage/claim reading, reduced-motion behaviour and safe local JSON preparation. Phone map-target overlaps were found and corrected; the checked phone targets exceeded 44 pixels in height. No page-level horizontal overflow was found in the checked new pages.</p>
<h2>What is not claimed</h2><p>This is not a WCAG certification or a substitute for testing with disabled readers. Automated checks cannot establish screen-reader usability, clear language or a fully accessible WebGL map. Report a barrier with the page, device/browser, assistive technology if relevant and what you expected—without sharing private information.</p>
<p><a href="https://github.com/DynamicDevices/theranosfilm/issues/new?template=accessibility.yml">Report an access barrier</a> · <a href="film-guide.html">Read the film guide</a> · <a href="claims.html">Read the evidence without the map</a></p>'''

    film += '<h2>Continue the scene investigation</h2><p><a href="scene-companion.html">Use the edition-aware scene companion</a> · <a href="engineer.html">Investigate the remembered wrong-technology exchange</a>.</p>'
    technology += '<h2>Inspect a granted claim</h2><p><a href="patent-map.html">Read the first patent claim chart</a> and keep legal scope separate from product validation.</p>'
    timeline += '<h2>Follow one investor evidence chain</h2><p><a href="investor-case.html">Read the Peterson case study</a>: court-described testimony, an internal financial version and the delivery link still missing.</p>'
    definitions = {
        'film-guide.html': ('What is real footage in You Can See Everything?', 'A source-backed guide to documentary access, performance, uncertain scene boundaries and the evidence needed to distinguish them.', 'Film / recording and performance', 'Separate who is speaking, what was recorded, what was performed and what we still need to verify.', film),
        'claims.html': ('Claims, evidence and qualifications', 'Compare Theranos and film questions with original documents, qualifications, provisional analysis and specific gaps.', 'Evidence / claim by claim', 'Follow a claim to its source—and keep its limits in view.', claims),
        'timeline.html': ('What did investors know—and when?', 'A dated Theranos evidence timeline separating investor representations, later accounts, civil allegations and the mixed criminal verdict.', 'History / investor information', 'A promise, a demonstration and a later explanation belong at different points in the evidence.', timeline),
        'technology.html': ('What was the Theranos technology?', 'Understand blood sampling, preparation, assays, platforms, patents, validation and what the wrong-technology question would need to establish.', 'Technology / from sample to claim', 'A small sample, a working assay, a patented system and a validated platform are different achievements.', technology),
        'contribute.html': ('Contribute evidence. Keep the history.', 'Prepare a source-backed JSON contribution, inspect attribution and exact revision hashes, and follow separate editorial decisions and corrections.', 'Participation / sources and corrections', 'Make one claim precise, show its source, explain its limits—and leave room for correction.', contributions),
        'accessibility.html': ('Read, navigate and question the evidence', 'Accessible reading alternatives, keyboard navigation, optional search, testing scope and an access-barrier reporting route.', 'Access / readable by design', 'The evidence should remain available without graphics, scripts or a particular way of navigating.', accessibility)
    }
    definitions.update(sections(research, depth, references, dossiers))
    definitions.update(dossier_sections(dossiers, references))
    return {name: page(*parts, active=name) for name, parts in definitions.items()}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regenerate only the named derived HTML pages')
    args = parser.parse_args()
    if args.write:
        for name, content in render().items():
            (ROOT / name).write_text(content)
        print(f'Rendered {len(PAGES)} research pages')
    else:
        print(json.dumps(render(), ensure_ascii=False))
