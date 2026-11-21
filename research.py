"""Validate public evidence and append-only contribution/review records.

No URL is fetched. A valid record is not a verified fact or an authenticated person.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent


def read_json(path):
    if Path(path).is_symlink():
        raise ValueError('Public records must be regular files, not symlinks')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def digest(record):
    raw = json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def safe_url(value):
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 for c in value):
        raise ValueError('Invalid URL characters')
    parsed = urlsplit(value)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Only absolute HTTP(S) links without credentials are permitted')
    # Reject malformed ports as well as malformed hosts.
    parsed.port
    return value


def validate_links(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('url', 'profile_url'):
                safe_url(child)
            else:
                validate_links(child)
    elif isinstance(value, list):
        for child in value:
            validate_links(child)


def records(root, group):
    result = {}
    if (root / 'data').is_symlink() or (root / 'data' / group).is_symlink():
        raise ValueError('Public record directories must not be symlinks')
    for path in sorted((root / 'data' / group).glob('*.json')):
        record = read_json(path)
        identifier = record.get('id')
        if identifier != path.stem or identifier in result:
            raise ValueError(f'Filename/duplicate ID mismatch: {path.name}')
        result[identifier] = record
    return result


def load(root=ROOT):
    root = Path(root)
    research = read_json(root / 'data/research.json')
    sources = {s['id']: s for s in research['sources']}
    if len(sources) != len(research['sources']):
        raise ValueError('Duplicate source ID')
    validate_links(research)
    seen = set()
    for group in ('claims', 'scenes', 'timeline'):
        for item in research[group]:
            if item['id'] in seen:
                raise ValueError('Duplicate evidence ID')
            seen.add(item['id'])
            if any(s not in sources for s in item['sources']):
                raise ValueError('Unknown source reference')
    proposals = records(root, 'contributions')
    reviews = records(root, 'reviews')
    for group, schema_name in ((proposals, 'contribution.schema.json'), (reviews, 'review.schema.json')):
        schema = read_json(root / schema_name)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for record in group.values():
            validator.validate(record)
            validate_links(record)
    for proposal in proposals.values():
        parent = proposal.get('supersedes')
        if parent is not None and parent not in proposals:
            raise ValueError('Correction references an unknown proposal')
        visited = {proposal['id']}
        while parent is not None:
            if parent in visited:
                raise ValueError('Cyclic correction history')
            visited.add(parent)
            parent = proposals[parent].get('supersedes')
    for review in reviews.values():
        proposal = proposals.get(review['contribution_id'])
        if proposal is None or digest(proposal) != review['submission_sha256']:
            raise ValueError('Review does not bind the exact proposal')
        author = proposal['contributor']['profile_url'].rstrip('/').lower()
        reviewer = review['reviewer']['profile_url'].rstrip('/').lower()
        if author == reviewer:
            raise ValueError('Submitter cannot record their own editorial review')
        if datetime.fromisoformat(review['reviewed_at'].replace('Z', '+00:00')) < datetime.fromisoformat(proposal['submitted_at'].replace('Z', '+00:00')):
            raise ValueError('Review predates the proposal')
    return research, proposals, reviews


def check_history(root, base):
    """Existing public records are immutable; corrections use new IDs/files."""
    for group in ('contributions', 'reviews'):
        current = records(Path(root), group)
        for key, old in records(Path(base), group).items():
            if key not in current or current[key] != old:
                raise ValueError(f'Existing {group} record changed or removed: {key}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-history', type=Path)
    args = parser.parse_args()
    research, proposals, reviews = load()
    if args.check_history:
        check_history(ROOT, args.check_history)
    print(f'Validated {len(research["claims"])} evidence entries, {len(proposals)} proposals, {len(reviews)} separate review records; no fact acceptance implied')
