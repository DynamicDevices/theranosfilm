"""Research-data integrity, not an independent factual or legal review."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import ValidationError

from render_dossiers import PAGES, financial_checks, sections
from research import ROOT, load_dossiers, read_json


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
        bad['financial_rows'][0]['basis'] = 'actual_spending'
        with self.assertRaises(ValidationError):
            self.validate(bad)
        rows = {r['id']: r for r in self.data['financial_rows']}
        self.assertEqual(rows['snapshot-cash']['amount_usd'], 162713000)
        self.assertEqual(rows['snapshot-deficit']['amount_usd'], -305787000)
        self.assertEqual(rows['forecast-rd-2015']['basis'], 'forecast')

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
