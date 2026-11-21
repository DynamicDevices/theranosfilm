"""Render six research workstreams; empty evidence stays visibly empty."""
from html import escape

PAGES = ('engineer.html', 'investor-case.html', 'patent-map.html',
         'scene-companion.html', 'financial-records.html', 'specialists.html')


def esc(value):
    return escape(str(value), quote=True)


def dollars(amount):
    return ('−' if amount < 0 else '') + f'${abs(amount):,}'


def financial_checks(data):
    rows = {row['id']: row['amount_usd'] for row in data['financial_rows']}
    pairs = [
        ('net-income-difference', '2015 net income: income statement versus cash-flow label',
         rows['income-net-2015'], rows['cash-net-2015']),
        ('cash-2014-difference', '2014 opening cash plus stated cash movement versus printed closing cash',
         rows['cash-open-2014'] + rows['cash-movement-2014'], rows['cash-close-2014']),
        ('cash-2015-difference', '2015 opening cash plus stated cash movement versus printed closing cash',
         rows['cash-open-2015'] + rows['cash-movement-2015'], rows['cash-close-2015'])
    ]
    return [{'id': key, 'label': label, 'left': left, 'right': right, 'delta': right - left}
            for key, label, left, right in pairs]


def sections(data, references):
    def refs(ids):
        return references(ids) if ids else ('<p class="limit">Project process or technical interpretation; '
                                           'no external source is cited for this paragraph.</p>')

    def correction(identifier):
        return (f'<p><a href="contribute.html?claim={esc(identifier)}">Correct or challenge this entry</a> · '
                '<a href="https://github.com/DynamicDevices/theranosfilm/commits/main/data/dossiers.json">'
                'Curated revision history</a></p>')

    index = ('<nav aria-label="Research workstreams"><ul>' + ''.join(
        f'<li><a href="{esc(work["page"])}">{esc(work["title"])}</a></li>' for work in data['workstreams']) + '</ul></nav>')
    definitions = {}
    for work in data['workstreams']:
        body = (f'<div class="callout"><h2>Current evidence status</h2><p>{esc(work["status"])}</p></div>'
                + index)
        for finding in work['findings']:
            body += (f'<section class="evidence-card" id="{esc(finding["id"])}"><h2>{esc(finding["label"])}</h2>'
                     f'<p>{esc(finding["text"])}</p>' + refs(finding['sources'])
                     + correction(finding['id']) + '</section>')
        if work['page'] == 'engineer.html':
            body += '''<h2>Test the competing explanations</h2>
<div class="table-scroll" tabindex="0" role="region" aria-label="Technical hypotheses"><table><caption>Hypotheses to check against the full passage—not attributed conclusions</caption>
<thead><tr><th scope="col">Possible meaning</th><th scope="col">What would distinguish it</th></tr></thead><tbody>
<tr><th scope="row">Wrong sample/preparation</th><td>Collection, dilution, damage, stability and available original sample volume.</td></tr>
<tr><th scope="row">Wrong measurement principle</th><td>Target analyte, signal/background, selectivity, detection range and interferents.</td></tr>
<tr><th scope="row">Wrong platform architecture</th><td>Integration, module compatibility, throughput, controls and failed-run recovery.</td></tr>
<tr><th scope="row">Wrong development strategy</th><td>Proof of an assay versus a menu, sequence of milestones, resources and economics.</td></tr>
</tbody></table></div><p>None of these possibilities has been established as the speaker's meaning. An optical patent is a research lead, not proof that a new venture solves the earlier system's problems.</p>
<p><a href="scene-companion.html#companion-engineer">Supply a lawful scene locator</a> · <a href="specialists.html#expert-engineering">Engineering review brief</a></p>'''
            body += '<p><a href="technology.html#assay-demonstrations">Inspect the assay materials, sample volumes, run times and reliability limits.</a></p>'
        elif work['page'] == 'investor-case.html':
            body += '''<section id="investor-claim-types"><h2>Was it a future promise or an existing capability?</h2>
<p>The following is our comparison of the records above, not a quotation from the film. A pitch can mix present claims, future plans and forecasts. They need different tests.</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="Investor claim types"><table><caption>Separate the promise from the evidence needed to support it</caption>
<thead><tr><th scope="col">Representation</th><th scope="col">Question to test</th><th scope="col">What the record adds</th></tr></thead><tbody>
<tr><th scope="row">Proprietary analyser and portable station</th><td>Which tests could the specified instrument reliably perform at the investment date, under which conditions?</td><td><a href="#peterson-technical-reliance">Peterson's memo testimony</a> describes its importance. <a href="engineer.html#engineer-deployed-device">The court's device account</a> distinguishes twelve Edison assays from the wider service. Neither proves every proposed deployment.</td></tr>
<tr><th scope="row">Already validated by pharmaceutical companies</th><td>Who authored the reports, what did they test and did the named companies independently endorse the conclusions?</td><td><a href="#peterson-pharma-validation">The contrary company evidence</a> challenges the assurance. <a href="#peterson-cross-examination-limit">Cross-examination</a> limits reconstruction of the investor's scientific review.</td></tr>
<tr><th scope="row">900 Walgreens locations the following year</th><td>Was this a future plan, and was the existing partnership accurately described?</td><td><a href="#peterson-rollout-forecast">Forecast and partnership evidence</a> must be separated. Missing a target alone does not prove deception.</td></tr>
<tr><th scope="row">Future revenue and profit</th><td>What assumptions and qualifications accompanied the model, and what was represented about its starting position?</td><td><a href="#peterson-forecast-starting-point">Peterson acknowledged projections</a>. <a href="financial-records.html">The financial chapter</a> keeps projections distinct from reported accounts and cash spending.</td></tr>
</tbody></table></div><p>A “platform” describes an architecture or business ambition; it does not itself establish a validated assay menu. A prototype, patent or later result cannot retrospectively prove earlier capability. The date, device, specimen, assay, conditions and actual investor disclosure matter.</p></section>'''
            body += '''<section id="dated-investor-comparison"><h2>What existed when investors heard the claims?</h2>
<div class="table-scroll" tabindex="0" role="region" aria-label="Dated investor comparison"><table>
<caption>Different dates, different records—not one pitch or one machine</caption>
<thead><tr><th scope="col">Date / record</th><th scope="col">Claim or achievement</th><th scope="col">What it does not establish</th></tr></thead><tbody>
<tr><th scope="row">December 2013 / Grossman testimony</th><td>Executives described technology already used on human samples and generating reimbursement.</td><td>A meeting recording, identical disclosures to every investor, or independent validation of the claimed performance.</td></tr>
<tr><th scope="row">October 2014 / Peterson testimony</th><td>Financial forecasts received and discussed; investor-authored Exhibit 2166 records proprietary equipment, portability, claimed validation and future rollout.</td><td>A guaranteed outcome, independent scientific validation or the complete committee deliberations. Her interpretation of the starting position must be distinguished from the forecast itself.</td></tr>
<tr><th scope="row">July 2015 / FDA HSV-1 clearance</th><td>A specific assay and defined specimen/use conditions.</td><td>Clearance of the whole menu, or proof that a broad platform worked in 2013–2014.</td></tr>
<tr><th scope="row">2018 / miniLab engineering paper</th><td>Selected assay/module results; integration still identified as future work.</td><td>Independent clinical replication or retrospective proof of earlier deployed capability.</td></tr>
</tbody></table></div><p>This is an editorial comparison of the sources below, not a finding that the later records were supplied to earlier investors. Present capability, development plans and forecasts require separate evidence.</p></section>'''
            body += refs(['trial-grossman-2021', 'trial-peterson-2021', 'fda-hsv1', 'minilab-paper'])
            body += '''<h2>The evidence chain—and its missing link</h2>
<div class="table-scroll" tabindex="0" role="region" aria-label="Investor evidence chain"><table><caption>Records must be linked, not merely placed next to one another</caption><thead><tr><th scope="col">Record</th><th scope="col">What it establishes here</th><th scope="col">Still missing</th></tr></thead><tbody>
<tr><th scope="row">Peterson's selected direct/cross-examination</th><td>Receipt and discussion of Exhibit 1853; investing entity named in testimony.</td><td>Complete testimony, exact scan identity and complete delivery history.</td></tr>
<tr><th scope="row">Investor-authored Exhibit 2166 and Defence closing Exhibit 2170</th><td>Testimony identifies the memo's author, relevant investment considerations, signatures and closing authority.</td><td>Standalone exhibits, committee minutes and bank evidence. Witness recollection does not establish independent scientific validation.</td></tr>
<tr><th scope="row">15 July 2014 internal email, Exhibit 15031</th><td>A particular financial version circulated internally.</td><td>Proof that this version reached Peterson, when, and with which qualifications.</td></tr>
<tr><th scope="row">Surviving technology presentation, Exhibit 3696</th><td>Wording presenting a testing capability.</td><td>Investor-specific delivery and a dated, validated demonstration.</td></tr>
<tr><th scope="row">Investment decision</th><td>Dynasty Financial II LLC identified in testimony; reliance described by the witness.</td><td>All beneficial owners, payment reconciliation and complete decision records.</td></tr></tbody></table></div>
<h2>Provisional conclusion</h2><p>This investor's account was not simply a bet that an invention might work one day. Peterson describes reliance on proprietary equipment, portability and purported existing pharmaceutical validation, alongside future financial and rollout forecasts. The memo testimony narrows why those propositions mattered, while cross-examination limits how precisely scientific diligence can be reconstructed. This remains one investor case, not every investor's motives or a complete transaction file. A matching dollar figure does not close the delivery gap.</p>
<h2>What this lets us ask of the film</h2><p>When a scene discusses what the invention “could do”, check whether it means demonstrated performance then, a proposed use, or future development. Compare like dates and devices. We have not authenticated that scene's exact words, edition or timestamp, so this research does not yet label it true or false or establish that the filmmakers omitted these records. <a href="scene-companion.html#companion-investor-comparison">Help locate and check the passage.</a></p>
<p><a href="financial-records.html">Inspect the financial records and arithmetic</a> · <a href="capabilities.html">Present versus future claims</a> · <a href="timeline.html">Investor chronology</a></p>'''
        elif work['page'] == 'patent-map.html':
            body += ('<h2>A first granted-claim chart</h2><p>These are concise paraphrases, not replacement claim language or a legal opinion. '
                     'Read the complete granted wording and dependencies.</p>'
                     '<div class="table-scroll" tabindex="0" role="region" aria-label="Patent claim chart"><table>'
                     '<caption>US8283155B2: selected elements and unverified implementation</caption>'
                     '<thead><tr><th scope="col">Claim</th><th scope="col">Element</th><th scope="col">Product evidence</th></tr></thead><tbody>')
            for element in data['patent_elements']:
                body += (f'<tr id="{esc(element["id"])}"><th scope="row">{esc(element["claim"])}</th>'
                         f'<td>{esc(element["element"])}<br>{esc(element["locator"])}</td>'
                         f'<td>{esc(element["product_mapping"])}</td></tr>')
            body += ('</tbody></table></div>' + refs(['patent'])
                     + '<p><a href="specialists.html#expert-patent">Review this claim chart</a> · '
                     '<a href="technology.html">Technology and validation explanation</a></p>')
        elif work['page'] == 'financial-records.html':
            body += '<h2>Transcribed figures with their accounting status</h2><p>Amounts below are USD. Expenses and losses are presented as negative, including positive expense magnitudes converted to negative here as noted in the locator. Company accounts and balances are not independent verification or cash payments. Forecast values must not be added up as money actually spent.</p>'
            for basis, title in [('forecast', 'Projected/proforma figures — not actual spending'),
                                 ('reported_accounts', 'Historical/actual-labelled company accounts — not an independent audit or cash ledger'),
                                 ('reported_snapshot', 'Company-reported balance sheet — not independently audited here'),
                                 ('court_account', 'Court-described trial figures — not a reconstructed ledger')]:
                if not any(row['basis'] == basis for row in data['financial_rows']):
                    continue
                body += (f'<div class="table-scroll" tabindex="0" role="region" aria-label="{esc(title)}"><table>'
                         f'<caption>{esc(title)}</caption><thead><tr><th scope="col">Item</th><th scope="col">Period</th>'
                         '<th scope="col">Amount (USD)</th><th scope="col">Source location</th></tr></thead><tbody>')
                for row in data['financial_rows']:
                    if row['basis'] == basis:
                        body += (f'<tr id="{esc(row["id"])}"><th scope="row">{esc(row["label"])}</th>'
                                 f'<td>{esc(row["period"])}</td><td>{dollars(row["amount_usd"])}</td>'
                                 f'<td>{esc(row["locator"])}</td></tr>')
                body += '</tbody></table></div>'
                body += refs(sorted({source for row in data['financial_rows'] if row['basis'] == basis for source in row['sources']}))
            body += '<h2>Reproducible arithmetic checks</h2><p>Difference means printed comparison minus the first value/calculation. We do not silently correct the document. These checks concern Exhibit 15031 forecasts only, not the separate historical accounts. They are arithmetic observations, not findings about motive, accounting intent or investor delivery.</p>'
            for check in financial_checks(data):
                body += (f'<section class="evidence-card" id="{esc(check["id"])}"><h3>{esc(check["label"])}</h3>'
                         f'<dl><dt>First value / calculation</dt><dd>{dollars(check["left"])}</dd>'
                         f'<dt>Printed comparison</dt><dd>{dollars(check["right"])}</dd>'
                         f'<dt>Difference</dt><dd>{dollars(check["delta"])}</dd></dl>'
                         '<p>Check source workbook, definitions, rounding and any omitted adjustments before interpreting.</p></section>')
            body += '''<h2>What this does not answer</h2><p>These records do not allocate all investor receipts between employees, research, equipment, retail operations and legal costs. Capitalised equipment, operating expense, net loss, accumulated deficit, cash payments and court loss measures are not interchangeable. No complete spending total has been reconstructed.</p><p><a href="data/dossiers.json">Inspect the numeric JSON</a> · <a href="money.html">Financial definitions</a> · <a href="specialists.html#expert-accounting">Ask an accountant to check one calculation</a></p>'''
        elif work['page'] == 'scene-companion.html':
            body += '<h2>Untimed verification records</h2><p>These entries are research leads, not a verified edit order. Empty time fields are intentional and machine-readable as null.</p>'
            for scene in data['scene_records']:
                timing = ('Not verified — no timestamp supplied' if scene['start_seconds'] is None else
                          f'{scene["start_seconds"]}–{scene["end_seconds"]} seconds')
                body += (f'<article class="evidence-card" id="{esc(scene["id"])}"><h3>{esc(scene["title"])}</h3>'
                         f'<dl><dt>Edition</dt><dd>{esc(scene["edition"] or "Not established")}</dd>'
                         f'<dt>Timing</dt><dd>{esc(timing)}</dd><dt>Verification</dt><dd>{esc(scene["verification"])}</dd>'
                         f'<dt>Question to resolve</dt><dd>{esc(scene["question"])}</dd></dl>'
                         + refs(scene['sources']) + correction(scene['id']) + '</article>')
            body += '''<h2>Scene-note template</h2><ol><li>Identify the lawful viewing source, edition, stated runtime and date watched.</li><li>Define zero time: distributor cards included or excluded; record start and end.</li><li>Separate exact quotation, paraphrase and recollection. Include surrounding question and qualifications.</li><li>Identify visible speaker, voice, source of reconstructed words and any production disclosure separately.</li><li>Give a short necessary description and source locator, not the film or an unauthorised transcript dump.</li><li>Mark your note proposed; another editor records any decision against its exact revision.</li></ol><p><a href="contribute.html">Prepare a scene-evidence proposal</a> · <a href="film-guide.html">Recording and performance guide</a></p>'''
        elif work['page'] == 'specialists.html':
            body += '<h2>Five focused review briefs</h2>'
            for brief in data['expert_briefs']:
                body += (f'<article class="evidence-card" id="{esc(brief["id"])}"><p class="status">Prepared brief; nobody contacted</p>'
                         f'<h3>{esc(brief["specialty"])}</h3><dl><dt>Question</dt><dd>{esc(brief["question"])}</dd>'
                         f'<dt>Useful contribution</dt><dd>{esc(brief["deliverable"])}</dd>'
                         f'<dt>Conflicts and confidentiality</dt><dd>{esc(brief["conflicts"])}</dd></dl>'
                         '<p><a href="https://github.com/DynamicDevices/theranosfilm/issues/new?template=evidence.yml">'
                         'Offer one source-backed correction</a></p></article>')
            body += '''<h2>Invitation draft — not sent</h2><blockquote><p>We are building an independent, public-source analysis of You Can See Everything and Theranos. Would you be interested in checking one specific claim in your field? We welcome counterevidence and corrections, not an endorsement. Please use public sources, disclose relevant interests and do not share confidential material. Contributions and editorial decisions are recorded separately; we would agree attribution before identifying you as a reviewer.</p></blockquote>
<p>This is a project draft prepared with Briar's assistance, not a message from Alex already sent to anyone. No affiliation or endorsement is implied.</p>
<h2>From expertise to a recorded finding</h2><ol><li>Contributor proposes one correction with an exact source locator and limitations.</li><li>Maintainers check the actual GitHub provenance, declared interests and relevant source.</li><li>A separate reviewer records a decision bound to the proposal's exact hash and discussion/revision.</li><li>The original proposal, disagreement and later corrections remain visible, subject to privacy handling.</li></ol><p>Expertise helps evaluate a source; it does not replace it. Editorial acceptance remains open to challenge.</p><p><a href="contribute.html">Submission rules and actual decision history</a></p>'''
        body += ('<section class="callout"><h2>What is still needed</h2><ul>'
                 + ''.join(f'<li>{esc(gap)}</li>' for gap in work['gaps']) + '</ul></section>'
                 + '<p><a href="data/dossiers.json">Read the curated dossier JSON</a> · '
                 '<a href="evidence.html">Inspect the full source register</a></p>')
        definitions[work['page']] = (work['title'], work['summary'], 'Research / primary records and open questions', work['summary'], body)
    return definitions
