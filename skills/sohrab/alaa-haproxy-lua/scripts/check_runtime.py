#!/usr/bin/env python3
"""Offline embedded-unit/parser/loopback gate. 0 pass, 1 assertion, 2 unavailable."""
import argparse
from pathlib import Path
import subprocess
import sys
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True, help='Already cached HAProxy 3.4.6 image; never pulled')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    container = 'alaa-lua-probe-' + uuid.uuid4().hex
    try:
        result = subprocess.run([
            'docker', 'run', '--rm', '--name', container, '-i', '--pull=never', '--network', 'none',
            '--cpus', '1', '--memory', '128m', '--mount',
            f'type=bind,source={root},target=/pkg,readonly',
            '--entrypoint', 'sh', args.image, '-s',
        ], input=(root / 'test/runtime/run.sh').read_bytes().replace(b'\r\n', b'\n'),
           timeout=90, check=False)
    except subprocess.TimeoutExpired as exc:
        # The Docker client timing out does not prove its container stopped.
        try:
            cleanup = subprocess.run(['docker', 'rm', '-f', container], timeout=10,
                                     stdout=subprocess.DEVNULL, check=False)
            if cleanup.returncode != 0:
                print(f'cleanup unconfirmed for task container {container}', file=sys.stderr)
        except (OSError, subprocess.TimeoutExpired):
            print(f'cleanup unconfirmed for task container {container}', file=sys.stderr)
        print(f'could not run: {exc}', file=sys.stderr)
        return 2
    except OSError as exc:
        print(f'could not run: {exc}', file=sys.stderr)
        return 2
    return result.returncode if result.returncode in (0, 1, 2) else 2


if __name__ == '__main__':
    sys.exit(main())
