# Stub store that ran fine and reports a problem: exit 1 is expected from the
# caller (findings), never exit 2 (could not run) and never the raw code 3.
Write-Output "stub store reports a validation problem"
exit 3
