"""Focused process tests. No vault/store service, hook registration or model call.

Fixture hashes and write-command traps isolate unwanted effects; synthetic
canaries isolate input/argv echo. A static checker separately prohibits direct
.NET writes/reads that PowerShell command traps would not intercept.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL / 'test/fixtures/hooks'
CANARY = 'ALAA_TEST_CANARY_NEVER_ECHO_7c42'

def quote(value):
    return "'" + str(value).replace("'", "''") + "'"

def snapshot():
    return {str(p.relative_to(FIXTURES)): (hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory') for p in FIXTURES.rglob('*')}

TRAPS = '''
function New-Item { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
function Set-Content { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
function Add-Content { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
function Out-File { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
function Remove-Item { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
function Move-Item { [Console]::Error.WriteLine('FORBIDDEN_WRITE'); throw 'write blocked' }
'''

def run(exe, command, payload=''):
    before = snapshot()
    env = dict(os.environ, ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL='1', ALAA_MEMORY_VAULT=str(FIXTURES))
    encoded = base64.b64encode((TRAPS + command).encode('utf-16-le')).decode('ascii')
    result = subprocess.run([exe, '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded], input=payload, text=True, capture_output=True, timeout=20, env=env)
    assert snapshot() == before, 'fixture tree changed'
    assert 'FORBIDDEN_WRITE' not in result.stderr, 'write attempted'
    assert CANARY not in result.stdout + result.stderr, 'synthetic canary echoed'
    assert result.returncode == 0, f'child exit {result.returncode}'
    return result.stdout

def check_precompact(exe, source=None, payload='', vault=None):
    if source is None:
        command = '& ' + quote(SKILL/'scripts/precompact_checkpoint.ps1')
    else:
        command = '& {\n' + source + '\n}'
    command += ' -VaultPath ' + quote(vault or FIXTURES)
    value = json.loads(run(exe, command, payload))
    assert value.get('continue') is True, 'legacy continue field changed'
    assert '/alaa-workflow' in value.get('systemMessage', ''), 'workflow pointer missing'

def check_session(exe, directory, expected, prefix=''):
    command = prefix + '\n& ' + quote(SKILL/'scripts/session_start_context.ps1') + ' -RepoRoot ' + quote(FIXTURES) + ' -DriftDir ' + quote(directory)
    text = run(exe, command, CANARY)
    assert expected in text, 'drift observation mismatch'
    assert '/alaa-memory-os' in text and '/alaa-workflow' in text, 'conditional owners missing'
    assert 'five-second' not in text and 'search memory first' not in text, 'copied recall policy'

def check_common(exe):
    common = '. ' + quote(SKILL/'scripts/_common.ps1') + '\n'
    good = quote(FIXTURES)
    missing = quote(FIXTURES/('missing-'+CANARY))
    cases = [
        ('$env:ALAA_MEMORY_VAULT='+good+'; Resolve-VaultRoot -VaultPath '+missing+' -DocumentedDefault '+good, False),
        ('$env:ALAA_MEMORY_VAULT='+missing+'; Resolve-VaultRoot -DocumentedDefault '+good, False),
        ('$env:ALAA_MEMORY_VAULT=""; Resolve-VaultRoot', False),
        ('$env:ALAA_MEMORY_VAULT=""; Resolve-VaultRoot -DocumentedDefault '+good, True),
        ('$env:ALAA_MEMORY_VAULT='+good+'; Resolve-VaultRoot', True),
        ('$env:ALAA_MEMORY_VAULT='+missing+'; Resolve-VaultRoot -VaultPath '+good, True),
    ]
    for expression, expected in cases:
        setup, _, resolve = expression.partition('; ')
        value = json.loads(run(exe, common + setup+'; '+resolve+' | ConvertTo-Json -Compress'))
        assert value['Ok'] is expected, 'selected vault fell through or valid root failed'
    output = run(exe, common + '$code = Invoke-Store -Exe '+quote(FIXTURES/'silent-store.ps1')+' -StoreArgs @('+quote(CANARY)+'); if ($code -ne 0 -or $code -isnot [int]) { exit 1 }')
    assert 'exit 0' in output, 'store outcome missing'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    exe = shutil.which('pwsh') or shutil.which('powershell')
    if not exe:
        print('BLOCKED: PowerShell executable unavailable')
        return 2
    if args.self_test:
        source = (SKILL/'scripts/precompact_checkpoint.ps1').read_text(encoding='utf-8-sig')
        mutants = [source.replace('continue = $true', 'continue = $false'), source.replace('@{', "Write-Output '"+CANARY+"'\n@{", 1), source.replace('@{', "New-Item -Path 'unused'\n@{", 1)]
        for mutant in mutants:
            try:
                check_precompact(exe, source=mutant)
            except (AssertionError, json.JSONDecodeError):
                continue
            raise AssertionError('negative mutation escaped hook harness')
        print('PASS: continue, secret-echo and write-attempt mutants rejected')
        return 0
    for payload in ['', '{broken', json.dumps({'cwd':CANARY,'transcript_path':str(FIXTURES/'transcript.jsonl'),'custom_instructions':CANARY,'trigger':'auto'}), json.dumps({'trigger':'manual'})]:
        check_precompact(exe, payload=payload, vault=FIXTURES/('missing-'+CANARY))
    # Valid old vault parameter must also cause zero writes with tail opt-in set.
    check_precompact(exe, payload=json.dumps({'transcript_path':str(FIXTURES/'transcript.jsonl')}))
    check_session(exe, 'open', '2 unresolved repository drift')
    check_session(exe, 'closed', 'No unresolved records observed')
    check_session(exe, 'absent-'+CANARY, 'observation unavailable')
    check_session(exe, 'open', 'observation unavailable', 'function Get-Content { throw "synthetic unreadable" }')
    check_common(exe)
    print('PASS: hook exit0/JSON, no writes/canary echo, drift positive/zero/unknown, selected-vault precedence and argv secrecy')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f'BLOCKED: {type(error).__name__}')
        sys.exit(2)
    except (AssertionError, ValueError) as error:
        print(f'FAIL: {error}')
        sys.exit(1)
