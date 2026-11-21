"""Offline badge tests: never request the live endpoint or increment the counter."""
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from build_site import ROOT, build


class Images(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.images = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))


class ViewsBadgeTests(unittest.TestCase):
    def test_source_preview_does_not_contact_counter(self):
        text = (ROOT / 'index.html').read_text()
        self.assertNotIn('https://hits.sh/', text)
        self.assertEqual(Images(text).images[0]['src'], 'views-preview.svg')
        self.assertTrue((ROOT / 'views-preview.svg').is_file())
        self.assertGreater(text.index('views-badge'), text.index('<footer>'))

    def test_only_exact_production_homepage_activates_badge(self):
        for base in ('https://theranosfilm.com', 'https://example.org'):
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / 'release'
                build(output, base)
                image = Images((output / 'index.html').read_text()).images[0]
                if base != 'https://theranosfilm.com':
                    self.assertEqual(image['src'], 'views-preview.svg')
                    continue
                url = urlsplit(image['src'])
                self.assertEqual(url.netloc, 'hits.sh')
                self.assertEqual(url.path, '/theranosfilm.com.svg')
                self.assertEqual(parse_qs(url.query)['label'], ['page views'])
                self.assertEqual(set(parse_qs(url.query)), {'label', 'color', 'labelColor'})
                self.assertEqual(image['referrerpolicy'], 'no-referrer')
                self.assertIn('Approximate', image['alt'])
                self.assertNotIn('extraCount', image['src'])
                self.assertNotIn('views-preview.svg', (output / 'index.html').read_text())
                for page in output.glob('*.html'):
                    if page.name != 'index.html':
                        self.assertFalse(any(urlsplit(i.get('src', '')).netloc == 'hits.sh'
                                             for i in Images(page.read_text()).images))


if __name__ == '__main__':
    unittest.main()
