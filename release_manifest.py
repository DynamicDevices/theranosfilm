"""Hash an exact static release using relative paths and SHA256 file digests."""
import argparse
import hashlib
import json
from pathlib import Path


def manifest(root):
    root = Path(root)
    entries = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Release artifacts must not contain symbolic links')
        if path.is_file():
            entries[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not entries:
        raise ValueError('Release is empty')
    serialized = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(serialized).hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--expect')
    args = parser.parse_args()
    digest = manifest(args.directory)
    if args.expect and digest != args.expect:
        raise SystemExit('Release manifest does not match the approved artifact')
    print(digest)
