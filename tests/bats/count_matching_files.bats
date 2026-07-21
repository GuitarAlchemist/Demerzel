#!/usr/bin/env bats
# Regression coverage for the self-improvement scanner's zero-match boundary.

setup() {
  SCRIPT="$BATS_TEST_DIRNAME/../../.github/scripts/count_matching_files.sh"
  mkdir -p "$BATS_TEST_TMPDIR/fixture"
  printf 'references known-policy\n' > "$BATS_TEST_TMPDIR/fixture/referenced.txt"
}

@test "zero references are scanner data, not a pipefail error" {
  run bash "$SCRIPT" orphan-policy "$BATS_TEST_TMPDIR/fixture"
  [ "$status" -eq 0 ]
  [ "$output" = "0" ]
}

@test "matching references are counted" {
  run bash "$SCRIPT" known-policy "$BATS_TEST_TMPDIR/fixture"
  [ "$status" -eq 0 ]
  [ "$output" = "1" ]
}

@test "missing arguments fail with usage" {
  run bash "$SCRIPT" known-policy
  [ "$status" -eq 2 ]
  [[ "$output" == *"usage:"* ]]
}
