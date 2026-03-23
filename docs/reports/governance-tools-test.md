# Governance Tools Live Test Report

**Date:** 2026-03-22
**Tester:** Claude Agent (via Claude Code MCP)
**Bot version:** demerzel-bot@master (commit d6acbbe — added create_channel + list_channels)
**Channel:** #demerzel-dev-ops (1485342580299530272)

## Test Objective

Validate that the Discord bot's new governance tools (`create_channel`, `list_channels`) work end-to-end when a user asks Demerzel to create a channel.

## Pre-conditions

- Bot restarted with new tools confirmed via restart announcement at 00:54:30 UTC
- Restart message: "Bot restarted with new capabilities: create_channel, list_channels"
- Bot registered 2 governance tools at startup (`getGovernanceTools()`)

## Test Steps and Results

### Step 1: Confirm bot restart

**Result: PASS**
Fetched 10 recent messages. Bot restart announcement present at 00:54:30 UTC (message id: 1485441577076785182) confirming `create_channel` and `list_channels` tools registered.

### Step 2: Send channel creation request

**Action:** Sent message via MCP reply tool: "Hey Demerzel, please create a #clarity-lab channel for articulation and BS decoding"
**Message ID:** 1485441757704355921
**Timestamp:** 00:55:13 UTC

**Note:** This message was sent as the bot account (via MCP plugin), so the bot's `shouldRespond()` function would only process it if prefixed with `[DEMERZEL-TEST]`. The message was NOT prefixed with the self-test marker.

### Step 3: User also sent direct request

The actual user (spareilleux) separately sent a direct @mention at 00:55:37 UTC (message id: 1485441860943085578): "@Demerzel create the #clarity-lab channel"

### Step 4: Bot response

**Result: PARTIAL — Bot responded but content not readable via fetch**

The bot produced 9 embed messages between 00:55:47 and 00:55:53 UTC (message ids 1485441900612681822 through 1485441926646988881). All messages show empty content in `fetch_messages` output.

**Root cause:** The bot uses `EmbedBuilder` (bot.js line 358) to wrap ALL responses in Discord embeds. The `fetch_messages` MCP tool returns `message.content` which is empty for embed-only messages — the actual text is in `embed.description`, which the fetch tool does not surface.

### Step 5: Channel creation outcome

**Result: INCONCLUSIVE**

Unable to definitively confirm whether `#clarity-lab` was created because:
1. The fetch_messages tool cannot read embed content
2. No separate MCP tool exists to list Discord server channels
3. The bot's `create_channel` handler (bot.js line 178-197) requires `Manage Channels` permission

**Possible outcomes:**
- **Success:** Channel created, bot reported it in an embed we can't read
- **Permission failure:** Bot lacks `Manage Channels` permission, error reported in embed (this was the failure mode in the earlier attempt at 21:26 UTC where the bot said "I don't have the Manage Channels permission")
- **Tool not invoked:** Claude API did not select the `create_channel` tool

## Key Findings

### 1. MCP-sent messages are filtered out (Critical)

Messages sent via the Discord MCP plugin arrive as the bot's own account. The bot's `shouldRespond()` (bot.js line 246-276) ignores bot messages unless prefixed with `[DEMERZEL-TEST]`. Our test message lacked this prefix and was therefore **ignored by the bot**.

**Fix:** Test messages sent via MCP must use the `[DEMERZEL-TEST]` prefix for the bot to process them.

### 2. Embed content invisible to fetch_messages (Moderate)

All bot responses use `EmbedBuilder`, making them invisible to the `fetch_messages` tool which only returns `message.content`. This makes automated testing of bot responses impossible.

**Fix:** The bot should include a plain-text fallback in `message.content` alongside the embed, or the MCP fetch tool should surface embed descriptions.

### 3. Permission issue likely persists

The earlier bot response at 21:26 UTC (before the restart with tools) explicitly stated: "I don't have the Manage Channels permission." Adding the tool code does not grant Discord permissions — the bot's role in the Discord server must have `Manage Channels` enabled.

**Fix:** In Discord server settings > Roles, grant the Demerzel bot role the "Manage Channels" permission.

## Bot Architecture Notes

- **Tool registration:** `getGovernanceTools()` from context.js provides tool definitions to Claude API
- **Tool execution:** bot.js lines 178-208 handle `create_channel` and `list_channels` via discord.js `guild.channels.create()`
- **Persona routing:** Channel name containing "clarity" routes to BS Detector persona (bot.js line 80)
- **Self-test bypass:** Messages from bot with `[DEMERZEL-TEST]` prefix are processed (bot.js line 251)

## Recommendations

| Priority | Action | Owner |
|----------|--------|-------|
| P0 | Grant bot "Manage Channels" permission in Discord server | User |
| P1 | Add embed.description to fetch_messages output | MCP plugin |
| P1 | Document [DEMERZEL-TEST] prefix requirement for MCP testing | Bot docs |
| P2 | Add plain-text content alongside embeds for observability | Bot code |
| P2 | Create automated governance tool test suite | Demerzel |

## Conclusion

The bot code correctly implements `create_channel` and `list_channels` governance tools (bot.js lines 178-208). The bot was restarted and confirmed the tools are registered. However, **three issues prevented full validation:**

1. MCP-sent messages lack the `[DEMERZEL-TEST]` prefix needed for self-processing
2. The bot likely lacks Discord `Manage Channels` permission (same error as pre-restart)
3. Embed-only responses are invisible to the fetch_messages diagnostic tool

The user's direct @mention did trigger the bot (9 embed responses observed), but the content of those responses cannot be read through the MCP fetch tool to confirm success or failure.

**Next step:** User should check Discord directly to see the bot's embed responses, grant "Manage Channels" permission if needed, and retry.
