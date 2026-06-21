#!/usr/bin/env bash
# llm_call.sh — one place for "call an LLM and get its text back".
#
# Usage:   llm_call.sh <provider> <prompt> [max_tokens]
#          provider ∈ claude | gemini | codex   (codex == openai)
# Output:  the model's text on stdout.
#
# Collapses the curl + auth-header + payload-escaping + response-extraction that
# was re-typed across 8 workflows (and 3x in cross-model-review.yml). The
# per-provider response shape (.content[0].text vs .candidates[].. vs
# .choices[]..) is the only real difference and it lives here, once.
#
# Testability (Candidate 3): the network call is the single function _http_post.
# bats sources this file and overrides _http_post with a fixture, so the auth +
# extraction logic is unit-tested without a live API. Endpoints + models are
# env-overridable for the same reason. main() runs only when executed, not when
# sourced.
set -euo pipefail

CLAUDE_URL="${LLM_CLAUDE_URL:-https://api.anthropic.com/v1/messages}"
GEMINI_URL="${LLM_GEMINI_URL:-https://generativelanguage.googleapis.com/v1beta/models}"
OPENAI_URL="${LLM_OPENAI_URL:-https://api.openai.com/v1/chat/completions}"
CLAUDE_MODEL="${LLM_CLAUDE_MODEL:-claude-sonnet-4-20250514}"
GEMINI_MODEL="${LLM_GEMINI_MODEL:-gemini-2.0-flash}"
OPENAI_MODEL="${LLM_OPENAI_MODEL:-gpt-4o}"

# _http_post <url> [curl-args...] — THE seam. Reads the request body on stdin,
# prints the raw response on stdout. Overridden by tests.
_http_post() {
  local url="$1"; shift
  curl -sS -X POST "$url" "$@" --data @-
}

_call_claude() {
  local prompt="$1" max="$2"
  jq -n --arg m "$CLAUDE_MODEL" --argjson mx "$max" --arg p "$prompt" \
      '{model:$m, max_tokens:$mx, messages:[{role:"user", content:$p}]}' \
    | _http_post "$CLAUDE_URL" \
        -H "x-api-key: ${ANTHROPIC_API_KEY:-}" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
    | jq -r '.content[0].text'
}

_call_gemini() {
  local prompt="$1" max="$2"
  jq -n --argjson mx "$max" --arg p "$prompt" \
      '{contents:[{parts:[{text:$p}]}], generationConfig:{maxOutputTokens:$mx}}' \
    | _http_post "${GEMINI_URL}/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY:-}" \
        -H "content-type: application/json" \
    | jq -r '.candidates[0].content.parts[0].text'
}

_call_openai() {
  local prompt="$1" max="$2"
  jq -n --arg m "$OPENAI_MODEL" --argjson mx "$max" --arg p "$prompt" \
      '{model:$m, max_completion_tokens:$mx, messages:[{role:"user", content:$p}]}' \
    | _http_post "$OPENAI_URL" \
        -H "authorization: Bearer ${OPENAI_API_KEY:-}" \
        -H "content-type: application/json" \
    | jq -r '.choices[0].message.content'
}

main() {
  local provider="${1:?usage: llm_call.sh <provider> <prompt> [max_tokens]}"
  local prompt="${2:?prompt required}"
  local max="${3:-1024}"
  case "$provider" in
    claude)       _call_claude "$prompt" "$max" ;;
    gemini)       _call_gemini "$prompt" "$max" ;;
    codex|openai) _call_openai "$prompt" "$max" ;;
    *) echo "llm_call: unknown provider '$provider' (claude|gemini|codex)" >&2; exit 2 ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
