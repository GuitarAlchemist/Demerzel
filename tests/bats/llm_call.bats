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
