"""Research-data integrity, not an independent factual or legal review."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import ValidationError

from render_dossiers import PAGES, financial_checks, sections
from research import ROOT, load_dossiers, read_json
from render_research import render


class DossierTests(unittest.TestCase):
    def setUp(self):
        self.research = read_json(ROOT / 'data/research.json')
        self.data = read_json(ROOT / 'data/dossiers.json')

    def validate(self, data):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'data').mkdir()
            (root / 'data/dossiers.json').write_text(json.dumps(data))
            (root / 'dossiers.schema.json').write_text((ROOT / 'dossiers.schema.json').read_text())
            return load_dossiers(root, self.research)

    def test_all_six_workstreams_are_present_without_claimed_completion(self):
        data = self.validate(self.data)
        self.assertEqual({w['page'] for w in data['workstreams']}, set(PAGES))
        self.assertEqual(len(data['workstreams']), 6)
        self.assertTrue(all(w['gaps'] for w in data['workstreams']))
        self.assertTrue(all(s['start_seconds'] is None and s['end_seconds'] is None
                            for s in data['scene_records']))
        self.assertTrue(all(b['status'] == 'brief_prepared_no_contact' for b in data['expert_briefs']))

    def test_unknown_sources_duplicates_and_missing_workstreams_fail(self):
        changes = []
        bad = copy.deepcopy(self.data)
        bad['workstreams'][0]['sources'] = ['invented-source']
        changes.append(bad)
        bad = copy.deepcopy(self.data)
        bad['patent_elements'][0]['id'] = bad['financial_rows'][0]['id']
        changes.append(bad)
        bad = copy.deepcopy(self.data)
        bad['workstreams'].pop()
        changes.append(bad)
        for bad in changes:
            with self.assertRaises(ValueError):
                self.validate(bad)

    def test_timestamp_cannot_be_claimed_without_checked_recording(self):
        bad = copy.deepcopy(self.data)
        bad['scene_records'][0]['start_seconds'] = 123
        with self.assertRaises(ValueError):
            self.validate(bad)
        bad['scene_records'][0]['verification'] = 'checked_recording'
        with self.assertRaises(ValueError):
            self.validate(bad)
        bad['scene_records'][0].update(edition='Test-only edition', end_seconds=140)
        self.validate(bad)
        bad['scene_records'][0]['end_seconds'] = 100
        with self.assertRaises(ValueError):
            self.validate(bad)

    def test_forecasts_cannot_be_silently_marked_actual_spending(self):
        bad = copy.deepcopy(self.data)
        next(r for r in bad['financial_rows'] if r['id'] == 'forecast-revenue-2014')['basis'] = 'actual_spending'
        with self.assertRaises(ValidationError):
            self.validate(bad)
        rows = {r['id']: r for r in self.data['financial_rows']}
        self.assertEqual(rows['snapshot-cash']['amount_usd'], 162713000)
        self.assertEqual(rows['snapshot-deficit']['amount_usd'], -305787000)
        self.assertEqual(rows['forecast-rd-2015']['basis'], 'forecast')

    def test_settlement_claims_payments_and_original_spending_stay_distinct(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        self.assertIn('12 September 2018', findings['finance-assignment-followthrough']['text'])
        self.assertIn('not inspection of the original', findings['finance-assignment-followthrough']['text'])
        self.assertIn('$1,331,094.88', findings['finance-allowed-versus-paid']['text'])
        self.assertIn('not a receipt', findings['finance-allowed-versus-paid']['text'])
        self.assertIn('Walgreens to fund $44m', findings['finance-walgreens-separate-funds']['text'])
        self.assertNotIn('actual_spending', {r['basis'] for r in self.data['financial_rows']})

    def test_investor_chronology_does_not_backdate_later_achievements(self):
        page = render(ROOT)['investor-case.html']
        self.assertIn('id="dated-investor-comparison"', page)
        for date in ['December 2013', 'October 2014', 'July 2015', '2018 / miniLab']:
            self.assertIn(date, page)
        self.assertIn('not a finding that the later records were supplied', page)
        self.assertIn('source-trial-peterson-2021', page)
        self.assertIn('null protocol', page)
        self.assertIn('not our reconstruction of every visit', page)

    def test_committee_memo_keeps_authorship_counterevidence_and_film_limits(self):
        investor = next(w for w in self.data['workstreams'] if w['id'] == 'peterson-investor-case')
        findings = {f['id']: f for f in investor['findings']}
        self.assertIn('not a Theranos pitch deck', findings['peterson-committee-memo']['label'])
        self.assertIn('not evidence of actual military use', findings['peterson-technical-reliance']['text'])
        self.assertIn('not a bank receipt', findings['peterson-closing-chain']['text'])
        self.assertIn('$99,999,984', findings['peterson-investment-amount']['text'])
        self.assertIn('does not establish what Theranos spent', findings['peterson-investment-amount']['text'])
        self.assertIn('did not certify scientific performance', findings['peterson-pharma-validation']['text'])
        self.assertIn('neither establishes that no diligence', findings['peterson-cross-examination-limit']['text'])
        page = render(ROOT)['investor-case.html']
        for anchor in ['investor-claim-types', 'peterson-committee-memo', 'peterson-cross-examination-limit']:
            self.assertTrue(f'id="{anchor}"' in page, anchor)
        for source in ['rdv-memo-testimony', 'rdv-cross-testimony']:
            self.assertTrue(f'evidence.html#source-{source}' in page, source)
            self.assertTrue(f'id="source-{source}"' in render(ROOT)['evidence.html'], source)
        self.assertIn('does not yet label it true or false', page)
        self.assertIn('not every investor', page)

    def test_pharmaceutical_reports_keep_claims_defence_and_endorsement_separate(self):
        work = next(w for w in self.data['workstreams'] if w['id'] == 'peterson-investor-case')
        findings = {f['id']: f for f in work['findings']}
        self.assertIn('not independent verification', findings['pfizer-narrow-study']['text'])
        self.assertIn('company-reported limitations', findings['pfizer-calibration-limits']['text'])
        self.assertIn('not proof Pfizer approved', findings['holmes-logo-defence']['text'])
        self.assertIn('not an exhaustive audit', findings['weber-logo-counterrecord']['text'])
        page = render(ROOT)['investor-case.html']
        for source in ['pfizer-report-0143', 'peterson-pharma-binder', 'holmes-logo-explanation',
                       'weber-pharma-testimony', 'government-logo-comparison']:
            self.assertTrue(f'evidence.html#source-{source}' in page, source)
        self.assertIn('not two complete standalone reports', findings['pfizer-prepared-for-not-by']['text'])

    def test_film_and_comparator_limits_remain_explicit(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        self.assertIn('No frequency count or behavioural diagnosis', findings['companion-nodding-boundary']['text'])
        self.assertIn('absence from our notes is not proof', findings['companion-investor-comparison']['text'])
        self.assertIn('not direct-fingerstick universal', findings['patent-comparator-scope']['text'])
        self.assertEqual(findings['patent-comparator-scope']['sources'], ['filmarray-k160457'])
        self.assertIn('no further operator intervention', findings['engineer-automation-boundary']['text'])

    def test_new_expense_testimony_is_not_a_forecast_or_a_cash_ledger(self):
        rows = {r['id']: r for r in self.data['financial_rows']}
        for year, opex, rd in [(2011, 28200000, 22000000),
                               (2012, 67000000, 53000000),
                               (2013, 92000000, 68000000)]:
            for prefix, amount in [('opex', opex), ('rd', rd)]:
                row = rows[f'testified-{prefix}-{year}']
                self.assertEqual(row['basis'], 'court_account')
                self.assertEqual(row['amount_usd'], -amount)
                self.assertIn('approximate', row['label'])
                self.assertEqual(row['sources'], ['trial-spivey-2021'])
            self.assertLess(rd, opex)

    def test_investor_exhibit_and_film_identity_boundaries_stay_explicit(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        investor = findings['peterson-exhibit-1853']
        self.assertIn('Exhibit 1853', investor['text'])
        self.assertIn('exact scan identity remains unresolved', investor['text'])
        self.assertEqual(investor['sources'], ['trial-peterson-2021', 'balwani-4859', 'holmes-cross-rdv'])
        self.assertIn('does not identify', findings['engineer-cto-role']['text'])
        self.assertIn('not independent verification', findings['companion-two-part-account']['text'])
        self.assertIn('not clearance of a universal', findings['engineer-limited-clearance']['text'].lower())

    def test_historical_accounts_remain_separate_from_cash_and_forecasts(self):
        rows = {r['id']: r for r in self.data['financial_rows']}
        self.assertEqual(rows['aranca-opex-2014']['amount_usd'], -100031000)
        self.assertEqual(rows['aranca-loss-2014']['amount_usd'], -106666000)
        self.assertEqual(rows['aranca-revenue-2014']['amount_usd'], 150000)
        for key, row in rows.items():
            if key.startswith('aranca-') and '-cash-' not in key:
                self.assertEqual(row['basis'], 'reported_accounts')
                self.assertEqual(row['sources'], ['balwani-5209'])
            if key.endswith('2015-short'):
                self.assertIn('2 Mth-A', row['period'])
                self.assertIn('not assumed Q1', row['period'])
        self.assertEqual(rows['aranca-cash-2015']['basis'], 'reported_snapshot')
        sections_by_page = sections(self.validate(self.data), lambda ids: 'REFS:' + ','.join(ids))
        financial = sections_by_page['financial-records.html'][-1]
        self.assertIn('REFS:balwani-5209', financial)
        self.assertIn('not an independent audit or cash ledger', financial)

    def test_device_and_company_paper_limits_have_sources(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        self.assertIn('not independent replication', findings['engineer-platform-architecture']['text'])
        self.assertIn('not a Theranos-machine', findings['engineer-sampling-evidence']['text'])
        self.assertIn('not our independent identification', findings['companion-device-counteraccount']['text'])
        self.assertEqual(findings['grossman-existing-business']['sources'], ['trial-grossman-2021'])

    def test_platform_experiments_keep_integration_and_attempt_limits(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        self.assertIn('could not contain all modules', findings['engineer-integration-limits']['text'])
        self.assertIn('Do not divide by final specimen counts', findings['engineer-first-attempt-reliability']['text'])
        page = render(ROOT)['technology.html']
        self.assertIn('id="assay-demonstrations"', page)
        for time in ['140 minutes', '80 minutes', '45 minutes', '109 minutes']:
            self.assertIn(time, page)
        self.assertIn('separate assay configurations, not a combined workflow', page)
        self.assertIn('Run time is not patient turnaround time', page)
        self.assertIn('source-minilab-supplement', page)

    def test_closure_letter_is_not_a_final_settlement_or_spending_ledger(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        self.assertEqual(findings['finance-closure-letter']['sources'], ['closure-letter-2018'])
        self.assertIn('at least $60m', findings['finance-closure-letter']['text'])
        self.assertIn('not audited balances', findings['finance-closure-letter']['text'])
        self.assertIn('does not prove completed settlement', findings['finance-ip-settlement-proposal']['text'])

    def test_litigation_is_not_proven_patent_value(self):
        findings = {f['id']: f for w in self.data['workstreams'] for f in w['findings']}
        entry = findings['patent-postclosure-assertion']
        self.assertIn('without prejudice', entry['text'])
        self.assertIn('not proven infringement', entry['text'])
        self.assertEqual(entry['sources'], ['labrador-complaint-2020', 'labrador-dismissal-2020'])

    def test_arithmetic_differences_are_derived_not_hidden(self):
        checks = {c['id']: c for c in financial_checks(self.data)}
        self.assertEqual(checks['net-income-difference']['delta'], 7000000)
        self.assertEqual(checks['cash-2014-difference']['left'], 197369000)
        self.assertEqual(checks['cash-2014-difference']['delta'], 631000)
        self.assertEqual(checks['cash-2015-difference']['delta'], -200000)
        altered = copy.deepcopy(self.data)
        next(r for r in altered['financial_rows'] if r['id'] == 'income-net-2015')['amount_usd'] = 237000000
        self.assertEqual(financial_checks(altered)[0]['delta'], 0)

    def test_untrusted_text_is_escaped_in_all_six_pages(self):
        bad = copy.deepcopy(self.data)
        attack = '<img src=x onerror=alert(1)>'
        for work in bad['workstreams']:
            work['findings'][0]['text'] = attack
        bad['patent_elements'][0]['element'] = attack
        bad['financial_rows'][0]['label'] = attack
        bad['scene_records'][0]['question'] = attack
        bad['expert_briefs'][0]['deliverable'] = attack
        for part in sections(bad, lambda ids: '').values():
            self.assertIn('&lt;img', part[-1])
            self.assertNotIn(attack, part[-1])


if __name__ == '__main__':
    unittest.main()
