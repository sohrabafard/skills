param([Parameter(ValueFromRemainingArguments = $true)][string[]]$StoreArgs)
# Deterministic local store double: argv secrecy belongs to the wrapper, not
# third-party output. Deliberately emit nothing so that boundary is isolated.
exit 0
