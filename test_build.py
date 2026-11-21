import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from build_site import build, PAGES


class BuildTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
