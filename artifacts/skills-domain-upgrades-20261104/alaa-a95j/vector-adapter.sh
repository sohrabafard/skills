#!/usr/bin/env bash
set -eu
args=(run --rm --pull never --network none --cpus 4 --memory 1g --label alaa.task=alaa-a95j)
args+=(--mount "type=bind,src=$VECTOR_STAGE,dst=$VECTOR_STAGE")
args+=(--mount "type=bind,src=$VECTOR_SKILL,dst=$VECTOR_SKILL,readonly")
{
  printf '%q ' timeout 120s docker "${args[@]}" "$VECTOR_IMAGE" "$@"
  printf '\n'
} >> "$VECTOR_RUN_LOG"
set +e
timeout 120s docker "${args[@]}" "$VECTOR_IMAGE" "$@" >"$VECTOR_STAGE/last.stdout" 2>"$VECTOR_STAGE/last.stderr"
rc=$?
printf 'exit=%s\n' "$rc" >> "$VECTOR_RUN_LOG"
cat "$VECTOR_STAGE/last.stdout" >> "$VECTOR_RUN_LOG"
cat "$VECTOR_STAGE/last.stderr" >> "$VECTOR_RUN_LOG"
cat "$VECTOR_STAGE/last.stdout"
cat "$VECTOR_STAGE/last.stderr" >&2
exit "$rc"
