# Stub store that succeeds AND prints to the output stream.
#
# This is the red fixture for the defect that shipped: the previous helper ran
# the store, then returned $LASTEXITCODE from a function, so the caller received
# an array of these output lines with the code appended. Comparing that array
# against zero is a filter, not a comparison, and it is truthy whenever the store
# printed anything - so every clean run reported failure. A checker whose exit
# code stays 0 against this stub is the assertion that the defect is gone.
Write-Output "stub store output line one"
Write-Output "stub store output line two"
exit 0
