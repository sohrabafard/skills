#!/usr/bin/env bats

@test "help exits successfully" {
  run ./__SCRIPT_NAME__ --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"Usage:"* ]]
}

@test "short help also works" {
  run ./__SCRIPT_NAME__ -h
  [ "$status" -eq 0 ]
}
