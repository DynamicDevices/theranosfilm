import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser

from render_research import render
from research import ROOT, check_history, digest, load, safe_url


class ResearchTests(unittest.TestCase):
    def test_landmarks_unique_ids_and_form_labels(self):
        class Structure(HTMLParser):
            def __init__(self, text):
                super().__init__()
                self.ids, self.labels, self.fields, self.main = [], [], [], 0
                self.feed(text)

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.append(attrs['id'])
                if tag == 'label':
                    self.labels.append(attrs.get('for'))
                if tag in ('input', 'textarea', 'select'):
                    self.fields.append(attrs.get('id'))
                if tag == 'main':
                    self.main += 1
        for name, html in render().items():
            structure = Structure(html)
            self.assertEqual(structure.main, 1, name)
            self.assertEqual(len(structure.ids), len(set(structure.ids)), name)
            self.assertTrue(set(structure.fields).issubset(structure.labels), name)
            self.assertIn('href="#article"', html)

    def fixture(self, folder):
        root = Path(folder)
        shutil.copytree(ROOT / 'data', root / 'data')
        for name in ('contribution.schema.json', 'review.schema.json', 'dossiers.schema.json'):
            shutil.copyfile(ROOT / name, root / name)
        return root

    def save(self, root, group, item):
        path = root / 'data' / group / (item['id'] + '.json')
        path.write_text(json.dumps(item))

    def review(self, proposal):
        return {'id':'test-review', 'contribution_id':proposal['id'],
                'submission_sha256':digest(proposal), 'reviewed_at':'2026-11-21T14:00:00Z',
                'reviewer':{'display_name':'Test fixture only','profile_url':'https://github.com/test-reviewer','kind':'automated'},
                'decision':'needs_evidence','reasons':'Test fixture, not an actual review.',
                'provenance':{'url':'https://github.com/DynamicDevices/theranosfilm/pull/9','revision':'a'*40},
                'sources':[{'url':'https://example.org','locator':'test fixture'}]}

    def test_static_pages_match_validated_data(self):
        for name, expected in render().items():
            self.assertEqual((ROOT / name).read_text(), expected, name)

    def test_scene_times_are_not_invented(self):
        data, _, _ = load()
        self.assertTrue(all(item['timecode'] is None for item in data['scenes']))
        self.assertIn('Not verified', render()['film-guide.html'])

    def test_url_schemes_credentials_and_controls_rejected(self):
        for value in ('javascript:alert(1)', '//example.org', 'https://u:p@example.org',
                      'data:text/html,x', 'https://example.org/has space', 'https://example.org:bad'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_url(value)

    def test_unknown_source_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            path = root / 'data/research.json'
            data = json.loads(path.read_text())
            data['claims'][0]['sources'] = ['invented-source']
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                load(root)

    def test_proposal_and_review_text_is_html_escaped(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            _, proposals, _ = load(root)
            proposal = next(iter(proposals.values()))
            proposal['claim'] = '<img src=x onerror=alert(1)>'
            self.save(root, 'contributions', proposal)
            review = self.review(proposal)
            review['reasons'] = '<script>alert(1)</script>'
            self.save(root, 'reviews', review)
            rendered = render(root)['contribute.html']
            self.assertIn('&lt;img', rendered)
            self.assertIn('&lt;script&gt;', rendered)
            self.assertNotIn('<img src=x', rendered)
            self.assertNotIn('<script>alert', rendered)
            self.assertIn('automated', rendered)

    def test_review_hash_and_same_profile_review_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            _, proposals, _ = load(root)
            proposal = next(iter(proposals.values()))
            review = self.review(proposal)
            review['submission_sha256'] = '0'*64
            self.save(root, 'reviews', review)
            with self.assertRaises(ValueError):
                load(root)
            review['submission_sha256'] = digest(proposal)
            proposal['contributor']['profile_url'] = review['reviewer']['profile_url']
            self.save(root, 'contributions', proposal)
            review['submission_sha256'] = digest(proposal)
            self.save(root, 'reviews', review)
            with self.assertRaises(ValueError):
                load(root)

    def test_existing_records_cannot_be_changed_or_removed(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            base, current = self.fixture(first), self.fixture(second)
            check_history(current, base)
            path = current / 'data/contributions/film-runtime.json'
            proposal = json.loads(path.read_text())
            proposal['claim'] = 'Changed in place'
            path.write_text(json.dumps(proposal))
            with self.assertRaises(ValueError):
                check_history(current, base)
            path.unlink()
            with self.assertRaises(ValueError):
                check_history(current, base)

    def test_corrections_preserve_both_sides(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            _, proposals, _ = load(root)
            old = next(iter(proposals.values()))
            new = copy.deepcopy(old)
            new['id'] = 'film-runtime-correction'
            new['supersedes'] = old['id']
            new['claim'] = 'Test correction only'
            self.save(root, 'contributions', new)
            output = render(root)['contribute.html']
            self.assertIn('Later correction proposals', output)
            self.assertIn('earlier record remains visible', output)

    def test_duplicate_json_keys_and_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            path = root / 'data/contributions/film-runtime.json'
            path.write_text('{"id":"film-runtime","id":"other"}')
            with self.assertRaises(ValueError):
                load(root)
            path.unlink()
            path.symlink_to(ROOT / 'data/contributions/film-runtime.json')
            with self.assertRaises(ValueError):
                load(root)


if __name__ == '__main__':
    unittest.main()
