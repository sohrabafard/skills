#!/usr/bin/env bats
#
# Tests for __TARGET_SCRIPT__.
#
# Override the subject when the layout differs:
#   SCRIPT_UNDER_TEST=./scripts/__TARGET_SCRIPT__ bats tests

setup() {
  SCRIPT_UNDER_TEST="${SCRIPT_UNDER_TEST:-./__TARGET_SCRIPT__}"
}

@test "help exits successfully" {
  run "${SCRIPT_UNDER_TEST}" --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"Usage:"* ]]
}

@test "short help also works" {
  run "${SCRIPT_UNDER_TEST}" -h
  [ "$status" -eq 0 ]
}
