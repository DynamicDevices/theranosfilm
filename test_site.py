"""Offline structure checks. Not a browser/accessibility or truth audit."""
import json
import re
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
    def test_homepage_update_history_is_dated_linked_and_server_readable(self):
        source = (ROOT / 'index.html').read_text()
        history = source.split('<section id="updates"', 1)[1].split('</section>', 1)[0]
        self.assertIn('aria-labelledby="updates-title"', history)
        self.assertIn('not new findings about Theranos', history)
        self.assertEqual(history.count('<time datetime="2026-11-21">'), 4)
        self.assertEqual(history.count('<time datetime="2026-11-22">'), 2)
        self.assertIn('source-guardian-bradshaw-20261119', history)
        self.assertIn('href="evidence.html#source-guardian-shoard-20261121"', history)
        positions = [history.index(f'/pull/{number}"') for number in (26, 25, 24, 22)]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(history.index('datetime="2026-11-22"'), positions[0])
        self.assertIn('/commits/main/', history)
        self.assertIn('href="contribute.html"', history)
        self.assertLess(source.index('class="participate"'), source.index('id="updates"'))
        self.assertLess(source.index('id="updates"'), source.index('<footer>'))

    def test_guardian_commentary_is_classified_and_connected_without_new_findings(self):
        from render_research import render
        research = json.loads((ROOT / 'data/research.json').read_text())
        source = next(s for s in research['sources'] if s['id'] == 'guardian-shoard-20261121')
        self.assertEqual(source['kind'], 'Critical opinion')
        self.assertIn('not independent authentication', source['limit'])
        pages = render(ROOT)
        self.assertIn('id="critical-responses"', pages['film-guide.html'])
        self.assertIn('evidence.html#source-guardian-shoard-20261121', pages['film-guide.html'])
        for name in ('film-guide.html', 'evidence.html'):
            self.assertIn('datetime="2026-11-22">Updated 22 November 2026', pages[name])

    def test_map_interaction_regressions(self):
        import subprocess
        subprocess.run(['node', '--test', str(ROOT / 'test_map_interactions.cjs')],
                       check=True, capture_output=True)

    def test_homepage_motion_is_optional_and_lifecycle_tests_pass(self):
        import subprocess
        source = (ROOT / 'index.html').read_text()
        self.assertIn('data-src="hero-loop.mp4"', source)
        video_tag = re.search(r'<video\b[^>]*>', source).group(0)
        self.assertNotRegex(video_tag, r'(?<![-\w])src=')
        self.assertIn('id="hero-video-toggle"', source)
        self.assertIn('preload="none"', source)
        css = (ROOT / 'editorial.css').read_text()
        self.assertIn('border-radius: 50%', css)
        self.assertIn('border-radius: inherit', css)
        subprocess.run(['node', '--check', str(ROOT / 'hero-motion.js')], check=True, capture_output=True)
        subprocess.run(['node', '--test', str(ROOT / 'test_hero_motion.cjs')], check=True, capture_output=True)

    def test_chapter_outline_preserves_anchors_and_disambiguates_duplicates(self):
        from render_research import chapter_outline
        outline, body = chapter_outline(
            '<section id="section-matched"><h2>Matched</h2></section>'
            '<h2 id="original">Existing &amp; explained</h2>'
            '<h2>Matched</h2><h2>A &lt;script&gt; claim</h2>')
        self.assertIn('id="original"', body)
        self.assertIn('href="#original"', outline)
        self.assertIn('id="section-matched-2"', body)
        self.assertIn('id="section-matched-3"', body)
        self.assertIn('Existing &amp; explained', outline)
        self.assertIn('A &lt;script&gt; claim', outline)
        self.assertNotIn('<script>', outline)
        ids = re.findall(r'\bid="([^"]+)"', body)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(chapter_outline('<h2>Only one</h2>')[0], '')

    def test_homepage_starts_with_the_explanation_and_keeps_deep_routes(self):
        source = (ROOT / 'index.html').read_text()
        opening = source.split('<main id="main">', 1)[1].lstrip()
        self.assertRegex(opening, r'^<section class="intro(?:\s[^\"]*)?"')
        self.assertIn('aria-labelledby="film-title"', opening)
        hero = opening.split('</section>', 1)[0]
        self.assertIn('href="start-here.html"', hero)
        self.assertIn('href="#connections-section"', hero)
        self.assertIn('Not affiliated with Theranos or the filmmakers', hero)
        self.assertIn('aria-label="Deeper investigations"', source)
        for name in ('engineer.html', 'patent-map.html', 'financial-records.html',
                     'scene-companion.html', 'specialists.html'):
            self.assertIn(f'href="{name}"', source)

    def test_static_local_links_and_fragments(self):
        for file in ROOT.glob('*.html'):
            page = Page(file.read_text())
            self.assertIn(page.lang, ('en', 'en-GB'))
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
