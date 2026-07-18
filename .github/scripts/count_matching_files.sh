#!/usr/bin/env bash

set -euo pipefail

count_matching_files() {
  local pattern=$1
  shift

  # grep exits 1 when no file matches. That is valid scanner data (a zero
  # reference count), not a workflow failure under `set -o pipefail`.
  grep -rl -- "$pattern" "$@" 2>/dev/null | wc -l || true
}

main() {
  if [[ $# -lt 2 ]]; then
    echo "usage: count_matching_files.sh PATTERN PATH..." >&2
    return 2
  fi

  count_matching_files "$@"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
