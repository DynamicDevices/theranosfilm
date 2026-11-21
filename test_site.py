"""Offline structure checks. Not a browser/accessibility or truth audit."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.h1, self.lang = set(), [], 0, None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'html':
            self.lang = attrs.get('lang')


class SiteTests(unittest.TestCase):
    def test_static_local_links_and_fragments(self):
        for file in ROOT.glob('*.html'):
            page = Page(file.read_text())
            self.assertEqual(page.lang, 'en')
            self.assertEqual(page.h1, 1)
            for href in page.links:
                parts = urlsplit(href)
                if parts.scheme or parts.netloc:
                    self.assertIn(parts.scheme, ('https', 'http'))
                    continue
                target = (file.parent / unquote(parts.path)).resolve() if parts.path else file
                self.assertTrue(target.is_relative_to(ROOT))
                self.assertTrue(target.is_file(), href)
                if parts.fragment and target.suffix == '.html':
                    self.assertIn(parts.fragment, Page(target.read_text()).ids)

    def test_project_state_is_explicit(self):
        project = json.loads((ROOT / 'project.json').read_text())
        self.assertEqual(project['selected_domain'], 'theranosfilm.com')
        self.assertEqual(len(project['priority_profiles']), 4)
        self.assertIsInstance(project['repository_governance']['protection_verified'], bool)
        self.assertEqual(project['licensing']['original_research'], 'CC-BY-SA-4.0')

    def test_issues_have_unique_ids_and_acceptance(self):
        issues = json.loads((ROOT / 'research-issues.json').read_text())['issues']
        self.assertEqual(len({i['id'] for i in issues}), len(issues))
        for issue in issues:
            self.assertTrue(issue['title'] and issue['body'] and issue['acceptance'])

    def test_submission_schema(self):
        from jsonschema import Draft202012Validator, FormatChecker
        schema = json.loads((ROOT / 'contribution.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        record = {
            'id': 'example-claim', 'claim': 'A proposed claim for testing only.',
            'contributor': {'display_name': 'Example', 'profile_url': 'https://example.org/person', 'identity_status': 'self_reported'},
            'submitted_at': '2026-11-21T00:00:00Z',
            'sources': [{'url': 'https://example.org/document', 'locator': 'page 1', 'supports': 'Test only', 'kind': 'other', 'rights_note': 'Link only'}],
            'limitations': 'Test fixture, not research evidence.', 'status': 'proposed',
            'license': 'CC-BY-SA-4.0', 'license_consent': True, 'history': []
        }
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertFalse(list(validator.iter_errors(record)))
        for key, bad_value in [('status', 'accepted'), ('submitted_at', 'yesterday'), ('license_consent', False), ('history', [{'decision': 'accepted'}])]:
            with self.subTest(key=key):
                self.assertTrue(list(validator.iter_errors(dict(record, **{key: bad_value}))))


if __name__ == '__main__':
    unittest.main()
