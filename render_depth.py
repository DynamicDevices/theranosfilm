"""Readable chapters built from curated, source-linked public records."""
from html import escape


def sections(research, depth, references, dossiers=None):
    def esc(value):
        return escape(str(value), quote=True)

    def correction(identifier):
        return (f'<p><a href="contribute.html?claim={esc(identifier)}">Challenge or correct this entry</a> · '
                '<a href="https://github.com/DynamicDevices/theranosfilm/commits/main/data/depth.json">'
                'Curated record revision history</a></p>')

    start = '''<div class="callout"><h2>Start with three separate questions</h2>
<ol><li>What kind of material am I watching: recording, archive, performance or reconstruction?</li>
<li>What exactly is being claimed, and about which date?</li>
<li>Which source could establish or contradict that particular claim?</li></ol></div>
<p><strong>Spoiler notice:</strong> this guide discusses the film's performance element. It is written for viewers who have finished watching. It is not a verified scene-by-scene synopsis.</p>
<h2>Why the two halves can feel confusing</h2>
<p>The festival synopsis describes documentary access to Holmes and Evans; a participant interview discusses Seyfried's performance. These support distinguishing documentary access from performance, but do not establish a clean boundary at the halfway point. Do not assume every earlier shot is unconstructed or every later shot is acted.</p>'''
    start += references(['flc', 'participants'])
    start += '''<h2>A short route through the investigation</h2>
<ol class="reading-route"><li><a href="analysis.html">Meet the people</a>: separate company executives, later personal relationships and the people constructing the film.</li>
<li><a href="film-guide.html">Check the recording and performance guide</a>: identify what a passage can establish before interpreting it.</li>
<li><a href="capabilities.html">Compare present capability with future potential</a>: read the investor wording and its limits.</li>
<li><a href="technology.html">Understand the technology</a>: collection, measurement, integration and validation are different achievements.</li>
<li><a href="money.html">Follow the money questions</a>: distinguish investment, valuation, revenue and actual expenditure.</li>
<li><a href="evidence.html">Inspect the sources</a> and <a href="contribute.html">submit a traceable correction</a>.</li></ol>
<h2>What the film cannot settle by itself</h2>
<p>A personal interview may illuminate someone's account without validating an instrument or reconstructing an investment decision. A performance can examine that account without becoming historical footage. Editing, sympathy, discomfort and visible behaviour do not determine whether a particular technical or financial statement was true.</p>
<h2>What we can say about the legal result</h2>
<p>The DOJ's January 2022 account reports four investor-related convictions for Holmes, together with acquittals and unresolved counts. Do not describe that mixed verdict as either total exoneration or proof of every accusation. This guide is not a current docket or appeal-status service.</p>'''
    start += references(['doj'])
    start += '''<h2>Still unresolved</h2><p>Exact scene times, the engineer's identity and the full “wrong technology” exchange are not authenticated here. Neither a complete spending audit nor a patent-to-product claim chart has been completed. These are visible research gaps, not findings against anybody.</p>'''

    people = ('<p>Profiles distinguish documented roles, attributed production accounts and editorial questions. '
              'A connection is a reason to inspect a record, not a finding of shared responsibility.</p>'
              '<nav aria-label="People"><ul>' + ''.join(
                  f'<li><a href="#{esc(p["id"])}">{esc(p["name"])}</a></li>' for p in depth['profiles']) + '</ul></nav>'
              '<section id="partners"><h2>Which kind of partner?</h2><p>Executive, romantic, investment and creative relationships are different. Dates and documented responsibilities matter more than the shared label.</p></section>')
    for p in depth['profiles']:
        people += (f'<article class="evidence-card" id="{esc(p["id"])}"><p class="status">{esc(p["role"])}</p>'
                   f'<h2>{esc(p["name"])}</h2><dl>' + ''.join(
                       f'<dt>{label}</dt><dd>{esc(p[key])}</dd>' for key, label in (
                           ('background', 'Sourced background'), ('involvement', 'Involvement'),
                           ('connection', 'Connection and its limits'), ('analysis', 'Editorial interpretation'),
                           ('gap', 'Still unverified'))) + '</dl>' + references(p['sources'])
                   + correction(p['id']) + '</article>')
    people += '''<section id="compare"><h2>Compare accounts, not personalities</h2><p>For each disputed statement record speaker, date, audience, exact wording, source and counterevidence. Do not diagnose a person from appearance, attribute guilt through family or professional links, or infer a filmmaker's motive from their genre.</p><p><a href="capabilities.html">Begin with present-versus-future technology claims</a>.</p></section>'''

    capability = '''<div class="callout"><h2>A useful ambition is not a working capability</h2><p>“We intend to develop” and “our system runs” make different representations. Neither tense alone settles a fraud allegation: the full communication, materiality, knowledge and relevant legal findings also matter.</p></div>
<p>This comparison separates actual source wording from our paraphrase. It does not quote the film without a checked transcript, and it does not assume every investor saw the same material.</p>'''
    for record in depth['representations']:
        capability += (f'<article class="evidence-card" id="{esc(record["id"])}"><h2>{esc(record["label"])}</h2>'
                       f'<p class="status">{esc(record["when"])}</p><p>{esc(record["wording_type"])}</p>'
                       + (f'<blockquote><p>{esc(record["wording"])}</p></blockquote>' if record['id'] == 'deck-present'
                          else f'<p>{esc(record["wording"])}</p>')
                       + f'<dl><dt>What this means</dt><dd>{esc(record["reading"])}</dd>'
                       f'<dt>Evidence to test</dt><dd>{esc(record["test"])}</dd>'
                       f'<dt>What it does not establish</dt><dd>{esc(record["limit"])}</dd></dl>'
                       + references(record['sources']) + correction(record['id']) + '</article>')
    capability += '''<h2>What would an investor normally need to see?</h2><p>There is no universal demonstration or single technical document that every private investment must include. A record of money invested does not show what was demonstrated or verified. Analyse the actual transaction, its disclosures and applicable obligations.</p>
<div class="table-scroll"><table><caption>Match a representation to the proof it needs</caption><thead><tr><th scope="col">Representation</th><th scope="col">Relevant evidence</th></tr></thead><tbody>
<tr><th scope="row">A working prototype</th><td>Defined device and protocol; repeatable runs; full failures and off-device steps disclosed.</td></tr>
<tr><th scope="row">Reliable clinical tests</th><td>Assay-specific validation for the stated sample, range, use and population.</td></tr>
<tr><th scope="row">A broad automated platform</th><td>Menu-level performance, integration, throughput, controls, staffing and realistic operational reliability.</td></tr>
<tr><th scope="row">A future opportunity</th><td>Explicit milestones, unresolved risks, credible resources and forecasts distinguishable from achieved performance.</td></tr>
</tbody></table></div><h2>Bring the film back into the comparison</h2><p>Record the full question and answer, film edition and timestamp. Determine whether the speaker is describing the earlier product, later architecture or an ambition. Then ask whether that account addresses the original representation or changes its meaning.</p><p><a href="timeline.html">Investor chronology</a> · <a href="claims.html#claim-now">Original claim record</a> · <a href="technology.html">Technical explanation</a></p>'''

    money = '''<div class="callout"><h2>We do not yet have a complete spending ledger</h2><p>The sources support some fundraising and legal statements. They do not justify a pie chart claiming where all the money went. This page separates known source accounts from the records still needed.</p></div>
<div class="table-scroll"><table><caption>Four different financial quantities</caption><thead><tr><th scope="col">Quantity</th><th scope="col">Meaning</th><th scope="col">Do not confuse it with</th></tr></thead><tbody>
<tr><th scope="row">Investment receipts</th><td>Cash received through financing.</td><td>Sales revenue or expenditure.</td></tr>
<tr><th scope="row">Valuation</th><td>An implied or assessed value of shares/company.</td><td>Money sitting in the company's bank.</td></tr>
<tr><th scope="row">Revenue</th><td>Income recognised from customers.</td><td>A forecast, fundraising receipt or profit.</td></tr>
<tr><th scope="row">Expenditure</th><td>Resources spent, with cash and accrual treatments distinguished.</td><td>Investment losses, restitution or a company's valuation.</td></tr></tbody></table></div>'''
    for record in depth['finances']:
        money += (f'<section class="evidence-card" id="{esc(record["id"])}"><p class="status">{esc(record["status"])}</p>'
                  f'<h2>{esc(record["label"])}</h2><p>{esc(record["account"])}</p>'
                  f'<p><strong>Records needed:</strong> {esc(record["needed"])}</p>'
                  + references(record['sources']) + correction(record['id']) + '</section>')
    money += '''<h2>Reconcile cash before allocating blame</h2><p>For one consistent period: opening cash + financing receipts + operating cash receipts + asset-sale proceeds − operating payments − capital payments − financing repayments = closing cash. Reconcile transfers and accounting classifications so the same item is not counted twice.</p><p>Document estimates as estimates, identify their source and avoid adding overlapping reported totals. A court's loss or restitution figure answers a different question from the company's expenditure.</p><h2>What a contribution should contain</h2><p>Bring a public filing or reliable account with its reporting period, currency, exact page and definition of the amount. Explain whether it records paid cash, an accrual, a forecast or a third party's estimate. Do not upload private banking records, personal employee data or unauthorised document copies.</p><p><a href="contribute.html?claim=cash-spending">Contribute financial evidence</a> · <a href="timeline.html">Read the investor timeline</a></p>'''

    evidence = '''<p>A source can prove that a statement was made without proving it true. These permanent source entries expose the inspected location and limitations. Expand citations within a claim to follow the same record here.</p><p><a href="data/research.json">Download the source/claim JSON</a> · <a href="data/depth.json">Download profiles and comparison JSON</a> · <a href="https://github.com/DynamicDevices/theranosfilm/commits/main/data/research.json">Source register revision history</a> · <a href="contribute.html">Proposal and editorial decision history</a></p>'''
    if dossiers:
        start += '<h2>Go deeper into the primary records</h2><ul>' + ''.join(
            f'<li><a href="{esc(work["page"])}">{esc(work["title"])}</a> — {esc(work["status"])}</li>'
            for work in dossiers['workstreams']) + '</ul>'
        money += '<h2>Read the actual source tables</h2><p><a href="financial-records.html">Inspect the first financial exhibit transcription and arithmetic checks</a>. Forecasts and reported balances remain distinct from actual expenditure.</p>'
        capability += '<p><a href="investor-case.html">Follow the Peterson investor evidence chain</a> · <a href="patent-map.html">Inspect the first granted-claim chart</a>.</p>'
    for source in research['sources']:
        uses = []
        if dossiers:
            uses += [f'<a href="{esc(work["page"])}">{esc(work["title"])}</a>'
                     for work in dossiers['workstreams'] if source['id'] in work['sources']]
        for group, filename, labelkey in [('profiles', 'analysis.html', 'name'), ('representations', 'capabilities.html', 'label'), ('finances', 'money.html', 'label')]:
            uses += [f'<a href="{filename}#{esc(item["id"])}">{esc(item[labelkey])}</a>' for item in depth[group] if source['id'] in item['sources']]
        for group, filename, labelkey in [('claims', 'claims.html', 'question'), ('scenes', 'film-guide.html', 'title'), ('timeline', 'timeline.html', 'event')]:
            uses += [f'<a href="{filename}#{esc(item["id"])}">{esc(item[labelkey])}</a>' for item in research[group] if source['id'] in item['sources']]
        evidence += (f'<article class="evidence-card" id="source-{esc(source["id"])}"><p class="status">{esc(source["kind"])}</p>'
                     f'<h2>{esc(source["title"])}</h2><dl>' + ''.join(f'<dt>{label}</dt><dd>{esc(source[key])}</dd>' for key, label in (
                         ('locator', 'Exact location'), ('inspected', 'Inspection scope'), ('limit', 'Limits')))
                     + f'</dl><p><a href="{esc(source["url"])}">Open the original source</a> · '
                     f'<a href="contribute.html?claim=source-{esc(source["id"])}">Correct this source entry</a></p>'
                     + ('<p>Used in: ' + ' · '.join(uses) + '</p>' if uses else '<p>Starting reference; full mapping pending.</p>') + '</article>')
    return {
        'start-here.html': ('You Can See Everything explained: start here', 'Finished the Theranos film? Understand recording versus performance, the people involved, investor claims and what remains unverified.', 'After the film / a short reading guide', 'Turn a confusing viewing experience into questions you can check.', start),
        'analysis.html': ('Who is involved in You Can See Everything?', 'Source-linked profiles of Elizabeth Holmes, Sunny Balwani, Billy Evans, Nathan Fielder, Lance Oppenheim and Amanda Seyfried, with documented connections and limits.', 'People / roles and relationships', 'Separate company responsibility, personal testimony and the authorship of the film.', people),
        'capabilities.html': ('Theranos claims: working now or possible later?', 'Compare Theranos investor presentation wording with technical evidence, civil allegations, later platform descriptions and the film questions still needing verification.', 'The central question / present versus future', 'What exactly was claimed, to whom, when—and what could the system demonstrate then?', capability),
        'money.html': ('Where did Theranos investor money go?', 'Separate Theranos fundraising, valuation, revenue and expenditure. Inspect the public-source evidence, the missing cash ledger and different meanings of failure.', 'Money / receipts, spending and missing records', 'Follow amounts to their definitions before treating them as an explanation.', money),
        'evidence.html': ('Theranos film evidence: sources and inspection limits', 'Inspect permanent source records, exact document locations, inspection scope, source-linked claims and version-controlled correction routes.', 'Evidence / inspect the record', 'Check what a source supports, what we inspected and what remains open.', evidence)
    }
