"""Build an allowlisted static release. Never copy the working directory wholesale."""
import argparse
import html
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
PAGES = ('index.html', 'analysis.html', 'technology.html', 'investors.html',
         'money.html', 'sources.html', 'about.html')
ASSETS = ('style.css', 'editorial.css', 'map.js', 'LICENSE.md',
          'CONTRIBUTING.md', 'contribution.schema.json', 'project.json',
          'research-issues.json')


class Metadata(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.in_title = False
        self.title = ''
        self.description = ''
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content', '')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title += text


def build(destination, base_url, source=ROOT):
    parsed = urlsplit(base_url)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or any(c.isspace() for c in base_url)):
        raise ValueError('An explicit HTTPS deployment base URL is required')
    base = base_url.rstrip('/') + '/'
    destination = Path(destination).resolve()
    source = Path(source).resolve()
    if destination == source or source.is_relative_to(destination):
        raise ValueError('Build destination must not overwrite the source')
    if destination.exists():
        raise ValueError('Use a new empty release directory; existing output is not overwritten')
    project = json.loads((source / 'project.json').read_text())
    destination.mkdir(parents=True)
    urls = []
    for filename in PAGES:
        text = (source / filename).read_text()
        meta = Metadata(text)
        if not meta.title.strip() or not meta.description.strip():
            raise ValueError(f'Missing title/description: {filename}')
        canonical = base if filename == 'index.html' else base + filename
        urls.append(canonical)
        # Local previews remain noindex. Only the reviewed release becomes crawlable.
        text = re.sub(r'<meta\s+name="robots"[^>]*>', '', text)
        text = re.sub(r'<meta\s+property="og:[^"]+"[^>]*>', '', text)
        schema = {
            '@context': 'https://schema.org',
            '@type': 'WebSite' if filename == 'index.html' else 'Article',
            'name': meta.title, 'description': meta.description,
            'url': canonical, 'inLanguage': 'en-GB',
            'isAccessibleForFree': True
        }
        if filename != 'index.html':
            schema.update(headline=meta.title,
                          mainEntityOfPage=canonical,
                          dateModified=project['updated'])
        tags = [
            '<meta name="robots" content="index,follow,max-image-preview:large">',
            f'<link rel="canonical" href="{html.escape(canonical, quote=True)}">',
            f'<meta property="og:url" content="{html.escape(canonical, quote=True)}">',
            f'<meta property="og:title" content="{html.escape(meta.title, quote=True)}">',
            f'<meta property="og:description" content="{html.escape(meta.description, quote=True)}">',
            f'<meta property="og:type" content="{"website" if filename == "index.html" else "article"}">',
            '<meta property="og:locale" content="en_GB">',
            '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
        ]
        text = text.replace('</head>', '\n' + '\n'.join(tags) + '\n</head>', 1)
        (destination / filename).write_text(text)
    for filename in ASSETS:
        shutil.copyfile(source / filename, destination / filename)
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in urls:
        entry = ET.SubElement(sitemap, 'url')
        ET.SubElement(entry, 'loc').text = url
        ET.SubElement(entry, 'lastmod').text = project['updated']
    ET.ElementTree(sitemap).write(destination / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (destination / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')
    (destination / 'llms.txt').write_text(
        '# Theranos Film: independent research\n\n'
        '> Public-source analysis of You Can See Everything, Theranos technology, '
        'investor representations and the people involved. Research is incomplete; '
        'read the source limitations. Not affiliated with Theranos, filmmakers or UK agencies.\n\n'
        + '\n'.join(f'- [{Metadata((source / f).read_text()).title}]({u})' for f, u in zip(PAGES, urls))
        + '\n\nOriginal research text and annotations: CC BY-SA 4.0. '
        'Third-party material and software excluded. See LICENSE.md.\n'
        'AI assistance: Briar. Source citations are not guarantees of claim truth.\n')
    (destination / '.nojekyll').write_text('')
    return urls


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.output, args.base_url)
    print(f'Built {len(PAGES)} indexable pages in {args.output}')
