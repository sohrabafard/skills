"""Focused process regressions for unavailable versus readable empty input.

Fault doubles inject failures that a real filesystem cannot reproduce reliably
across host permissions. Advanced cmdlets honor caller ErrorAction, reproducing
the nonterminating-error suppression bug instead of inventing a crash.
"""
import base64
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
FIXTURES = SKILL/'test/fixtures'

def quote(value):
    return "'"+str(value).replace("'","''")+"'"

def snapshot():
    return {p.relative_to(FIXTURES).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in FIXTURES.rglob('*')}

PARTIAL_SCAN = r'''
function Get-ChildItem {
  [CmdletBinding()]
  param($LiteralPath,[switch]$Recurse,$Filter,[switch]$File)
  Microsoft.PowerShell.Management\Get-ChildItem -LiteralPath $LiteralPath -Recurse -Filter $Filter -File
  Write-Error 'synthetic unreadable subtree'
}
'''
UNREADABLE_NOTE = '''
function Get-Content {
  [CmdletBinding()]
  param($LiteralPath,[switch]$Raw)
  Write-Error 'synthetic unreadable note'
}
'''
NULL_NOTE = '''
function Get-Content {
  [CmdletBinding()]
  param($LiteralPath,[switch]$Raw)
  $null
}
'''

def main():
    exe = shutil.which('pwsh') or shutil.which('powershell')
    if not exe:
        print('BLOCKED: PowerShell executable unavailable')
        return 2
    before = snapshot()
    cases = [('partial readable scan cannot be clean',PARTIAL_SCAN,'green-vault',2,''),
             ('unreadable note is unavailable',UNREADABLE_NOTE,'green-vault',2,''),
             ('nonempty note with null content is unavailable',NULL_NOTE,'green-vault',2,''),
             ('readable zero-byte note is not unavailable','','checker-empty',0,''),
             ('readable green input is clean','','green-vault',0,'')]
    count = 0
    for filename in ['alaa_memory_staleness.ps1','alaa_obsidian_linkcheck.ps1']:
        current = list(cases)
        if filename == 'alaa_obsidian_linkcheck.ps1':
            current.append(('readable empty note retains hygiene findings','','checker-empty',1,' -StrictHygiene'))
        for name,prefix,fixture,expected,flags in current:
            command = prefix+'\n& '+quote(SKILL/'scripts'/filename)+' -VaultPath '+quote(FIXTURES/fixture)+flags
            if filename == 'alaa_memory_staleness.ps1':
                command += ' -MaxAgeDays 365000'
            # -Command otherwise collapses any nonzero script exit to 1.
            command += '; exit $LASTEXITCODE'
            encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
            env = dict(os.environ,ALAA_MEMORY_VAULT='',ALAA_SOURCE_ROOT='')
            result = subprocess.run([exe,'-NoProfile','-NonInteractive','-EncodedCommand',encoded],capture_output=True,text=True,timeout=20,env=env)
            assert snapshot() == before, 'fixture files changed'
            assert result.returncode == expected, f'{filename}: {name}: expected {expected}, observed {result.returncode}'
            if expected == 2:
                assert 'BLOCKED:' in result.stdout, 'unavailable input lacks blocked report'
                assert 'linkcheck: clean' not in result.stdout and 'staleness: clean' not in result.stdout, 'partial coverage reported clean'
            count += 1
    print(f'PASS: {count} checker input-failure/empty-input process regressions; fixture tree unchanged')
    return 0

if __name__ == '__main__':
    try: sys.exit(main())
    except (OSError,subprocess.TimeoutExpired) as error:
        print('BLOCKED: '+type(error).__name__)
        sys.exit(2)
    except AssertionError as error:
        print('FAIL: '+str(error))
        sys.exit(1)
