#!/usr/bin/env bats
# Tests post_discussion.sh through its interface by overriding the _graphql seam
# — exercises the build/validate/raise-on-fail logic without hitting GitHub.

setup() {
  export REPO_NODE_ID="R_test"
  source "$BATS_TEST_DIRNAME/../../.github/scripts/post_discussion.sh"
}

@test "prints the discussion URL on success" {
  _graphql() { echo "https://github.com/x/y/discussions/1"; }
  run main "CAT_ID" "A title" "A body"
  [ "$status" -eq 0 ]
  [ "$output" = "https://github.com/x/y/discussions/1" ]
}

@test "raises (exit 1) when the API returns an empty URL" {
  _graphql() { echo ""; }
  run main "CAT_ID" "t" "b"
  [ "$status" -eq 1 ]
}

@test "raises (exit 1) when the API returns null" {
  _graphql() { echo "null"; }
  run main "CAT_ID" "t" "b"
  [ "$status" -eq 1 ]
}

@test "fails when REPO_NODE_ID is unset" {
  unset REPO_NODE_ID
  _graphql() { echo "https://example/x"; }
  run main "CAT_ID" "t" "b"
  [ "$status" -ne 0 ]
}

@test "fails when category_id is missing" {
  run main
  [ "$status" -ne 0 ]
}
