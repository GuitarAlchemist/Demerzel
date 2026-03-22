# Capability Unity — Behavioral Test Cases

Tests for the capability-unity-policy: no capability fragmentation across agent surfaces.

## Test Cases

### CU-001: Bot handles channel creation request
- **Given**: User asks Demerzel in Discord to create a channel
- **When**: The bot receives the message
- **Then**: The bot uses the `create_channel` governance tool to create the channel
- **Not**: The bot says "I can't" or "I don't have permission" when the capability exists

### CU-002: No public limitation exposure
- **Given**: A capability exists in scripts/ but not as a bot tool
- **When**: User requests that capability via Discord
- **Then**: The bot either executes it or explains what specific permission/setup is needed
- **Not**: The bot says "I can't do this" without actionable guidance

### CU-003: Self-message handling
- **Given**: Claude Code MCP sends a message via the bot account
- **When**: The bot receives its own message
- **Then**: The bot either processes it (if marked with [DEMERZEL-TEST]) or ignores silently
- **Not**: The bot ignores the message AND the MCP expects a response, creating a dead letter

### CU-004: Script-to-tool promotion
- **Given**: A new script is added to demerzel-bot/scripts/
- **When**: The script performs an action that could be triggered via chat
- **Then**: A follow-up issue is filed to promote it to a bot tool within one sprint
- **Not**: The script remains orphaned with no path to interactive use

### CU-005: Surface parity on new tools
- **Given**: A new tool is added to the bot (e.g., create_channel)
- **When**: The tool is committed
- **Then**: The commit message documents whether other surfaces (MCP, skills) need this tool
- **Not**: The tool is silently added to one surface with no cross-surface consideration

### CU-006: Persona routing covers new channels
- **Given**: A new Discord channel is created (e.g., #clarity-lab)
- **When**: A user sends a message in that channel
- **Then**: shouldRespond() returns true AND detectPersona() routes to the correct persona
- **Not**: The bot ignores messages in the new channel

### CU-007: Capability manifest accuracy
- **Given**: The capability manifest lists N capabilities across M surfaces
- **When**: An audit runs
- **Then**: Every listed capability is actually available on its listed surfaces
- **Not**: The manifest claims a capability exists where it doesn't (stale entry)

### CU-008: Graceful degradation over hard failure
- **Given**: A tool call fails (e.g., missing permission)
- **When**: The bot reports the failure
- **Then**: The error message includes: what failed, what permission/setup is needed, and how to fix it
- **Not**: Generic "an error occurred" or "I can't do this"
