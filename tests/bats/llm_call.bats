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
