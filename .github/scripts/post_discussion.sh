#!/usr/bin/env bash
# post_discussion.sh — one place for "create a GitHub Discussion".
#
# Usage:   REPO_NODE_ID=<id> post_discussion.sh <category_id> <title> <body>
# Output:  the new discussion URL on stdout.
#
# Collapses the createDiscussion GraphQL ceremony re-typed across 9 workflows.
# Crucially it RAISES (non-zero exit) on failure instead of the `|| echo
# "Failed"` swallow those workflows used — a failed post is now a failed step,
# not a silent green. category_id is passed in (resolve it via the ecosystem
# action's cat_* outputs — Candidate 2), so this script owns the call, not the ids.
#
# Testability (Candidate 3): the GraphQL call is the single function _graphql.
# bats sources this file and overrides _graphql, so the build/validate/raise
# logic is unit-tested without hitting GitHub. main() runs only when executed.
set -euo pipefail

# _graphql <query> <repo> <cat> <title> <body> — THE seam. Prints the created
# discussion URL (or empty/"null" on failure). Overridden by tests.
_graphql() {
  gh api graphql \
    -f query="$1" \
    -f repo="$2" -f cat="$3" -f title="$4" -f body="$5" \
    --jq '.data.createDiscussion.discussion.url'
}

main() {
  local category_id="${1:?usage: post_discussion.sh <category_id> <title> <body>}"
  local title="${2:?title required}"
  local body="${3:?body required}"
  local repo="${REPO_NODE_ID:?REPO_NODE_ID env required}"

  # shellcheck disable=SC2016  # $repo/$cat/... are GraphQL variables, not shell — single quotes are intentional
  local query='mutation($repo: ID!, $cat: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {repositoryId: $repo, categoryId: $cat, title: $title, body: $body}) {
    discussion { url }
  }
}'

  local url
  url="$(_graphql "$query" "$repo" "$category_id" "$title" "$body")"
  if [[ -z "$url" || "$url" == "null" ]]; then
    echo "post_discussion: createDiscussion returned no URL (category=$category_id)" >&2
    exit 1
  fi
  echo "$url"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
