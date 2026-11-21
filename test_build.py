import json
import re
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from build_site import build, PAGES


class BuildTests(unittest.TestCase):
    def test_publication_upload_is_gated_and_precedes_a_separate_deploy_job(self):
        workflow = (Path(__file__).parent / '.github/workflows/site.yml').read_text()
        checks, publish = workflow.split('\n  publish:\n', 1)
        dispatch_gate = "if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main'"
        binding, upload = checks.split('      # Keep upload and deployment', 1)
        binding = binding.split('      - name: Bind upload', 1)[1]
        self.assertIn(dispatch_gate, binding)
        self.assertIn('test "$GITHUB_SHA" = "$EXPECTED_SHA"', binding)
        self.assertIn('python release_manifest.py _site --expect "$EXPECTED_MANIFEST"', binding)
        self.assertIn('actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9', upload)
        self.assertIn(dispatch_gate, upload)
        self.assertNotIn('actions/upload-pages-artifact@', publish)
        self.assertEqual(workflow.count('actions/upload-pages-artifact@'), 1)
        self.assertIn('needs: checks', publish)
        self.assertIn(dispatch_gate, publish)
        self.assertIn('name: github-pages', publish)
        self.assertIn('actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346', publish)

    def test_publication_installs_builder_dependencies_before_build(self):
        workflow = (Path(__file__).parent / '.github/workflows/site.yml').read_text()
        publish = workflow.split('\n  publish:\n', 1)[1]
        self.assertLess(publish.index('python -m pip install -r requirements.txt'),
                        publish.index('python build_site.py'))
        self.assertIn('test "$GITHUB_SHA" = "$EXPECTED_SHA"', publish)
        self.assertIn('python release_manifest.py _site --expect "$EXPECTED_MANIFEST"', publish)

    def test_crawlable_release_has_consistent_canonicals_and_no_private_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'release'
            urls = build(output, 'https://theranosfilm.com')
            self.assertEqual(urls[0], 'https://theranosfilm.com/')
            for filename, url in zip(PAGES, urls):
                text = (output / filename).read_text()
                self.assertNotIn('noindex', text)
                self.assertIn(f'rel="canonical" href="{url}"', text)
                self.assertEqual(text.count('property="og:title"'), 1)
                self.assertIn('application/ld+json', text)
            xml = ET.parse(output / 'sitemap.xml')
            self.assertEqual(len(xml.getroot()), len(PAGES))
            self.assertIn('Sitemap: https://theranosfilm.com/sitemap.xml', (output / 'robots.txt').read_text())
            for private in ('config', '.git', 'DEVELOPMENT.md', 'build_site.py', 'test_site.py'):
                self.assertFalse((output / private).exists())
            self.assertIn('research is incomplete', (output / 'llms.txt').read_text().lower())

    def test_refuses_non_https_and_existing_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                build(Path(temporary) / 'release', 'http://theranosfilm.com')
            with self.assertRaises(ValueError):
                build(Path(temporary), 'https://theranosfilm.com')

    def test_viewer_discovery_metadata_matches_visible_source_linked_pages(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'release'
            build(output, 'https://theranosfilm.com')
            titles, descriptions = [], []
            for filename in PAGES:
                text = (output / filename).read_text()
                titles.append(re.search(r'<title>(.*?)</title>', text).group(1))
                descriptions.append(re.search(r'<meta name="description" content="([^"]+)"', text).group(1))
                schemas = [json.loads(value) for value in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
                self.assertEqual(schemas[0]['about']['name'], 'You Can See Everything')
                self.assertIn('name="twitter:description"', text)
                self.assertNotIn('SearchAction', text)
                if 'aria-label="Breadcrumb"' in text:
                    breadcrumb = schemas[1]['itemListElement']
                    self.assertEqual(breadcrumb[0]['item'], 'https://theranosfilm.com/')
                    self.assertEqual(breadcrumb[1]['position'], 2)
                    self.assertEqual(breadcrumb[1]['item'], f'https://theranosfilm.com/{filename}')
                    self.assertIn(breadcrumb[1]['name'], text)
            self.assertEqual(len(titles), len(set(titles)))
            self.assertEqual(len(descriptions), len(set(descriptions)))
            guide = (output / 'start-here.html').read_text()
            for question in ['Who is the interviewer?', 'What did the Theranos machine actually do?',
                             'What does the ending prove?']:
                self.assertIn(question, guide)
            self.assertIn('Questions after watching You Can See Everything', guide)
            self.assertNotIn('FAQPage', guide)  # No claim of eligibility for FAQ rich results.


if __name__ == '__main__':
    unittest.main()
