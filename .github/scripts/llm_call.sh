#!/usr/bin/env bash
# llm_call.sh — one place for "call an LLM and get its text back".
#
# Usage:   llm_call.sh <provider> <prompt> [max_tokens]
#          provider ∈ claude | gemini | codex   (codex == openai)
#          LLM_SYSTEM (env, optional) — system prompt, carried per-provider.
#          LLM_<PROVIDER>_MODEL (env, optional) — override the default model.
#
# Contract (so callers never parse the raw JSON themselves):
#   stdout      — the model's text (only on success)
#   stderr      — a human diagnostic (only on failure)
#   exit code   — 0 ok · 2 usage · 3 API/transport error · 4 empty/blocked response
#
# Use the if-form, which is set -e safe (GitHub runs run: blocks with -eo pipefail):
#   if TEXT=$(llm_call.sh claude "$p" 2>/tmp/err); then ... ; else <fallback>; fi
#
# Collapses the curl + auth-header + payload-escaping + response-extraction that
# was re-typed across 8 workflows (and 3x in cross-model-review.yml). The
# per-provider request/response shapes are the only real difference; they live
# here, once.
#
# Testability (Candidate 3): the network call is the single function _http_post.
# bats sources this file and overrides _http_post with a fixture, so the auth,
# extraction, AND error-classification logic are unit-tested without a live API.
# Endpoints + models are env-overridable. main() runs only when executed.
set -euo pipefail

CLAUDE_URL="${LLM_CLAUDE_URL:-https://api.anthropic.com/v1/messages}"
GEMINI_URL="${LLM_GEMINI_URL:-https://generativelanguage.googleapis.com/v1beta/models}"
OPENAI_URL="${LLM_OPENAI_URL:-https://api.openai.com/v1/chat/completions}"
# Use undated model ids. A dated snapshot is a time bomb: the previous default
# here passed its retirement date and every caller of this seam started 404ing,
# which is what killed demerzel-capability-expansion (#703). Guarded by
# scripts/test_no_retired_models.py.
CLAUDE_MODEL="${LLM_CLAUDE_MODEL:-claude-sonnet-5}"
GEMINI_MODEL="${LLM_GEMINI_MODEL:-gemini-2.0-flash}"
OPENAI_MODEL="${LLM_OPENAI_MODEL:-gpt-4o}"

# _http_post <url> [curl-args...] — THE seam. Reads the request body on stdin,
# prints the raw response on stdout. Overridden by tests.
_http_post() {
  local url="$1"; shift
  curl -sS -X POST "$url" "$@" --data @-
}

# _emit <raw> <text_filter> <error_filter> — classify a raw response into the
# contract. stdout+return 0 on success; stderr+return 3/4 on failure. All three
# providers route through here so the error contract is identical.
_emit() {
  local raw="$1" text_filter="$2" error_filter="$3"
  if [ -z "$raw" ]; then
    echo "llm_call: transport failure (no response body)" >&2
    return 3
  fi
  local apierr
  apierr=$(printf '%s' "$raw" | jq -r "$error_filter" 2>/dev/null || true)
  if [ -n "$apierr" ] && [ "$apierr" != "null" ]; then
    echo "llm_call: API error: $apierr" >&2
    return 3
  fi
  local text
  text=$(printf '%s' "$raw" | jq -r "$text_filter" 2>/dev/null || true)
  if [ -z "$text" ] || [ "$text" = "null" ]; then
    echo "llm_call: no text in response: $(printf '%s' "$raw" | tr -d '\n' | head -c 300)" >&2
    return 4
  fi
  printf '%s\n' "$text"
}

_call_claude() {
  local prompt="$1" max="$2" raw
  # thinking is disabled explicitly, not by omission. On sonnet-4 omitting it meant
  # "no thinking"; from sonnet-5 on, omitting it means *adaptive* thinking — and
  # max_tokens caps thinking + text together, so callers passing 1024..4096 would
  # start getting truncated answers. Disabling preserves the pre-#703 contract.
  # A caller that wants thinking should raise max_tokens and opt in deliberately.
  raw=$(jq -n --arg m "$CLAUDE_MODEL" --argjson mx "$max" --arg p "$prompt" --arg s "${LLM_SYSTEM:-}" \
      '{model:$m, max_tokens:$mx, thinking:{type:"disabled"}, messages:[{role:"user", content:$p}]}
       + (if $s == "" then {} else {system:$s} end)' \
    | _http_post "$CLAUDE_URL" \
        -H "x-api-key: ${ANTHROPIC_API_KEY:-}" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json") || true
  _emit "$raw" '.content[0].text' '.error.message // empty'
}

_call_gemini() {
  local prompt="$1" max="$2" raw
  raw=$(jq -n --argjson mx "$max" --arg p "$prompt" --arg s "${LLM_SYSTEM:-}" \
      '{contents:[{parts:[{text:$p}]}], generationConfig:{maxOutputTokens:$mx}}
       + (if $s == "" then {} else {systemInstruction:{parts:[{text:$s}]}} end)' \
    | _http_post "${GEMINI_URL}/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY:-}" \
        -H "content-type: application/json") || true
  _emit "$raw" '.candidates[0].content.parts[0].text' '.error.message // empty'
}

_call_openai() {
  local prompt="$1" max="$2" raw
  raw=$(jq -n --arg m "$OPENAI_MODEL" --argjson mx "$max" --arg p "$prompt" --arg s "${LLM_SYSTEM:-}" \
      '{model:$m, max_completion_tokens:$mx,
        messages: ((if $s == "" then [] else [{role:"system", content:$s}] end) + [{role:"user", content:$p}])}' \
    | _http_post "$OPENAI_URL" \
        -H "authorization: Bearer ${OPENAI_API_KEY:-}" \
        -H "content-type: application/json") || true
  _emit "$raw" '.choices[0].message.content' '.error.message // empty'
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
