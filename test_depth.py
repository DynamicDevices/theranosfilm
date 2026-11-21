"""Structure and data-integrity checks, not an independent factual review."""
import copy
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from build_site import build, PAGES
from render_depth import sections
from render_research import render
from research import ROOT, load_depth, read_json


class DepthTests(unittest.TestCase):
    def test_new_production_account_narrows_origin_but_not_final_cut(self):
        research = read_json(ROOT / 'data/research.json')
        depth = load_depth(ROOT, research)
        interviewer = next(p for p in depth['profiles'] if p['id'] == 'interviewer')
        self.assertIn('initially intended to produce', interviewer['involvement'])
        self.assertIn('final-cut authority', interviewer['gap'])
        self.assertIn('oppenheim-gq-2026', interviewer['sources'])

    def test_seven_profiles_have_attributed_roles_and_limits(self):
        research = read_json(ROOT / 'data/research.json')
        depth = load_depth(ROOT, research)
        self.assertEqual(len(depth['profiles']), 7)
        father = next(p for p in depth['profiles'] if p['id'] == 'christian-holmes')
        self.assertEqual(father['sources'], ['rice-holmes'])
        self.assertIn('not a comprehensive exoneration', father['analysis'])
        pages = render()
        for person in depth['profiles']:
            self.assertIn(f'id="{person["id"]}"', pages['analysis.html'])
            self.assertTrue(person['sources'])
            self.assertTrue(person['gap'])
        for name in ('start-here.html', 'capabilities.html', 'evidence.html', 'money.html'):
            self.assertIn(name, PAGES)
            self.assertIn('not independently fact-checked', pages[name])
        self.assertIn('Search extract', pages['evidence.html'])
        self.assertIn('2011–2013 expense testimony quantified', pages['money.html'])
        self.assertIn('not a complete payment ledger', pages['money.html'])

    def test_depth_rejects_missing_fields_duplicate_ids_and_unknown_sources(self):
        research = read_json(ROOT / 'data/research.json')
        original = read_json(ROOT / 'data/depth.json')
        bad_records = []
        bad = copy.deepcopy(original)
        bad['profiles'][0]['sources'] = ['invented-source']
        bad_records.append(bad)
        bad = copy.deepcopy(original)
        bad['profiles'][0]['gap'] = ''
        bad_records.append(bad)
        bad = copy.deepcopy(original)
        bad['profiles'][0]['id'] = bad['profiles'][1]['id']
        bad_records.append(bad)
        for bad in bad_records:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / 'data').mkdir()
                (root / 'data/depth.json').write_text(json.dumps(bad))
                with self.assertRaises(ValueError):
                    load_depth(root, research)

    def test_all_depth_text_is_escaped(self):
        research = read_json(ROOT / 'data/research.json')
        depth = read_json(ROOT / 'data/depth.json')
        attack = '<img src=x onerror=alert(1)>'
        for group, field in (('profiles', 'background'), ('representations', 'wording'), ('finances', 'account')):
            bad = copy.deepcopy(depth)
            bad[group][0][field] = attack
            rendered = '\n'.join(part[-1] for part in sections(research, bad, lambda ids: '').values())
            self.assertNotIn(attack, rendered)
            self.assertIn('&lt;img', rendered)

    def test_release_has_honest_article_metadata_and_public_records(self):
        class Schema(HTMLParser):
            def __init__(self, text):
                super().__init__()
                self.in_schema = False
                self.data = []
                self.feed(text)

            def handle_starttag(self, tag, attrs):
                self.in_schema = tag == 'script' and dict(attrs).get('type') == 'application/ld+json'

            def handle_endtag(self, tag):
                if tag == 'script':
                    self.in_schema = False

            def handle_data(self, data):
                if self.in_schema:
                    self.data.append(json.loads(data))

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'release'
            build(output, 'https://theranosfilm.com')
            self.assertEqual(len(PAGES), len(set(PAGES)))
            self.assertEqual(len(PAGES), 21)
            self.assertTrue((output / 'data/depth.json').is_file())
            self.assertTrue((output / 'social-card.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
            for name in ('analysis.html', 'money.html', 'start-here.html', 'capabilities.html', 'evidence.html'):
                text = (output / name).read_text()
                schema = Schema(text).data[0]
                self.assertEqual(schema['author']['name'], 'Theranos Film project')
                self.assertEqual(schema['creativeWorkStatus'], 'Editorial draft; research incomplete')
                self.assertNotIn('reviewRating', schema)
                self.assertIn('https://theranosfilm.com/social-card.png', text)


if __name__ == '__main__':
    unittest.main()
