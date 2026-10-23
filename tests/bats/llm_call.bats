#!/usr/bin/env bats
# Tests llm_call.sh through its interface by overriding the _http_post seam with
# fixtures — exercises the per-provider extraction without any network call.

setup() {
  source "$BATS_TEST_DIRNAME/../../.github/scripts/llm_call.sh"
  FIX="$BATS_TEST_DIRNAME/fixtures"
}

@test "claude: extracts .content[0].text" {
  _http_post() { cat >/dev/null; cat "$FIX/claude.json"; }
  run _call_claude "hi" 100
  [ "$status" -eq 0 ]
  [ "$output" = "hello from claude" ]
}

@test "gemini: extracts .candidates[0].content.parts[0].text" {
  _http_post() { cat >/dev/null; cat "$FIX/gemini.json"; }
  run _call_gemini "hi" 100
  [ "$status" -eq 0 ]
  [ "$output" = "hello from gemini" ]
}

@test "codex/openai: extracts .choices[0].message.content" {
  _http_post() { cat >/dev/null; cat "$FIX/openai.json"; }
  run _call_openai "hi" 100
  [ "$status" -eq 0 ]
  [ "$output" = "hello from codex" ]
}

@test "main dispatches by provider" {
  _http_post() { cat >/dev/null; cat "$FIX/claude.json"; }
  run main claude "hi" 100
  [ "$status" -eq 0 ]
  [ "$output" = "hello from claude" ]
}

@test "unknown provider exits 2" {
  run main bogus "hi"
  [ "$status" -eq 2 ]
}

@test "missing prompt fails" {
  run main claude
  [ "$status" -ne 0 ]
}

@test "API error response -> exit 3 with stderr diagnostic" {
  _http_post() { cat >/dev/null; cat "$FIX/error.json"; }
  run _call_claude "hi" 100
  [ "$status" -eq 3 ]
  [[ "$output" == *"API error"* ]]
  [[ "$output" == *"Overloaded"* ]]
}

@test "empty/blocked response -> exit 4" {
  _http_post() { cat >/dev/null; cat "$FIX/empty.json"; }
  run _call_claude "hi" 100
  [ "$status" -eq 4 ]
  [[ "$output" == *"no text in response"* ]]
}

@test "transport failure (empty body) -> exit 3" {
  _http_post() { cat >/dev/null; printf ''; }
  run _call_claude "hi" 100
  [ "$status" -eq 3 ]
}

@test "LLM_SYSTEM adds a system field to the claude payload" {
  _http_post() { cat > "$BATS_TEST_TMPDIR/p.json"; cat "$FIX/claude.json"; }
  LLM_SYSTEM="be terse" _call_claude "hi" 100
  run jq -er '.system == "be terse"' "$BATS_TEST_TMPDIR/p.json"
  [ "$status" -eq 0 ]
}

@test "no LLM_SYSTEM omits the system field" {
  _http_post() { cat > "$BATS_TEST_TMPDIR/p.json"; cat "$FIX/claude.json"; }
  _call_claude "hi" 100
  run jq -er 'has("system") | not' "$BATS_TEST_TMPDIR/p.json"
  [ "$status" -eq 0 ]
}

# --- model currency (#703) -------------------------------------------------
# A dated snapshot silently becomes a 404 on its retirement date, taking every
# caller of this seam with it. That is how capability-expansion died.

@test "default claude model is not a dated snapshot" {
  [[ ! "$CLAUDE_MODEL" =~ -[0-9]{8}$ ]]
}

@test "default claude model is not one of the known-retired ids" {
  for retired in claude-sonnet-4-20250514 claude-3-5-sonnet-20241022 \
                 claude-3-5-sonnet-20240620 claude-3-opus-20240229 \
                 claude-3-7-sonnet-20250219 claude-3-5-haiku-20241022; do
    [ "$CLAUDE_MODEL" != "$retired" ]
  done
}

@test "LLM_CLAUDE_MODEL still overrides the default" {
  _http_post() { cat > "$BATS_TEST_TMPDIR/p.json"; cat "$FIX/claude.json"; }
  CLAUDE_MODEL="claude-opus-5" _call_claude "hi" 100
  run jq -er '.model == "claude-opus-5"' "$BATS_TEST_TMPDIR/p.json"
  [ "$status" -eq 0 ]
}

# --- thinking contract (#703) ----------------------------------------------
# From sonnet-5 on, omitting `thinking` means *adaptive*, and max_tokens caps
# thinking + text together. Callers here pass 1024..4096, so an omitted field
# would truncate answers. It must be disabled explicitly, not by omission.

@test "claude payload disables thinking explicitly" {
  _http_post() { cat > "$BATS_TEST_TMPDIR/p.json"; cat "$FIX/claude.json"; }
  _call_claude "hi" 100
  run jq -er '.thinking.type == "disabled"' "$BATS_TEST_TMPDIR/p.json"
  [ "$status" -eq 0 ]
}

@test "claude payload sends no sampling parameters" {
  # temperature/top_p/top_k are rejected outright on sonnet-5 and later.
  _http_post() { cat > "$BATS_TEST_TMPDIR/p.json"; cat "$FIX/claude.json"; }
  _call_claude "hi" 100
  run jq -er 'has("temperature") or has("top_p") or has("top_k") | not' "$BATS_TEST_TMPDIR/p.json"
  [ "$status" -eq 0 ]
}
