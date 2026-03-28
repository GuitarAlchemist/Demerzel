---
name: prime-radiant-control
description: Control Prime Radiant directly — send commands, add GIS pins/paths, open panels, navigate nodes, and validate state via HTTP API on port 5176.
---

# Prime Radiant Control — Claude ↔ PR Direct Link

Drive Prime Radiant programmatically from Claude. Send commands, query state, validate results — all via HTTP to the Vite dev server on `localhost:5176`.

## Usage

`/prime-radiant-control [action] [args...]`

**Examples:**
```
/prime-radiant-control state                     — get current PR state
/prime-radiant-control panel gis                 — open the GIS panel
/prime-radiant-control gis:pins governance       — add governance node pins preset
/prime-radiant-control gis:path NYC London       — draw a path between two points
/prime-radiant-control validate                  — full state validation
```

## Prerequisites

- **Vite dev server** running at `http://localhost:5176` (the React Prime Radiant app)
- The `usePrControl` hook active in ForceRadiant (auto-connected via SSE)

## API Endpoints

All endpoints are on `http://localhost:5176`:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/pr/command` | Send a command `{action, params}` |
| `GET` | `/pr/state` | Read current PR state snapshot |
| `GET` | `/pr/result?id=CMD_ID` | Check result of a specific command |
| `GET` | `/pr/events` | SSE stream (React connects here) |

## Supported Actions

### Panel Control
- `panel:open` `{panelId: "gis"|"godot"|"detail"|"activity"|...}`
- `panel:close`

### GIS Operations
- `gis:add-pin` `{planet: "earth", pin: {id, lat, lon, label, color?, icon?, pulse?}}`
- `gis:add-pins` `{planet: "earth", pins: [...]}`
- `gis:add-path` `{planet: "earth", path: {id, points: [{lat, lon}...], color?, animated?, dashed?}}`
- `gis:clear` `{planet: "earth"}`
- `gis:cluster` `{planet: "earth", enabled: true, radius?: 10}`

### Navigation
- `navigate:node` `{nodeId: "alignment-policy"}`

### State
- `state:report` — returns full state in result

### IXQL
- `ixql:exec` `{command: "SELECT * WHERE type = 'policy'"}`

## Execution Flow

```
Claude                    Vite Server              React (ForceRadiant)
  │                           │                          │
  ├─ POST /pr/command ───────►│                          │
  │  {action, params}         ├─ SSE push ──────────────►│
  │                           │                          ├─ execute action
  │                           │◄─ POST /pr/result ───────┤
  │                           │◄─ POST /pr/state ────────┤
  │◄─ GET /pr/state ──────────┤                          │
  │  (validate)               │                          │
```

## Validation Pattern

```bash
# 1. Send command
curl -s -X POST http://localhost:5176/pr/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-pin","params":{"planet":"earth","pin":{"id":"test","lat":40.7,"lon":-74,"label":"Test","pulse":true}}}'

# 2. Wait briefly for execution
sleep 1

# 3. Validate state
curl -s http://localhost:5176/pr/state | jq '.gis.earth.pins'
# Expected: 1
```

## Implementation

When this skill is invoked, follow these steps:

1. **Check connectivity**: `curl -s http://localhost:5176/pr/state` — if it fails, the Vite dev server isn't running.

2. **Parse the user's intent** into one or more commands from the supported actions list.

3. **Send each command** via `POST /pr/command` with `{action, params}`.

4. **Wait 1 second** for React to execute.

5. **Validate** by reading `/pr/state` and checking the expected changes occurred.

6. **Report results** to the user: what was sent, what state looks like now, whether it matches expectations.

For complex operations (multiple pins, paths, panel switches), batch commands sequentially with validation between each step.

## Quick Reference — curl Commands

```bash
# Open GIS panel
curl -sX POST localhost:5176/pr/command -H 'Content-Type: application/json' -d '{"action":"panel:open","params":{"panelId":"gis"}}'

# Add governance pins
curl -sX POST localhost:5176/pr/command -H 'Content-Type: application/json' -d '{"action":"gis:add-pins","params":{"planet":"earth","pins":[{"id":"d","lat":40.7,"lon":-74,"label":"Demerzel","icon":"🛡","color":"#FFD700","pulse":true},{"id":"ix","lat":37.4,"lon":-122,"label":"ix","icon":"⚙","color":"#73D117"}]}}'

# Draw path
curl -sX POST localhost:5176/pr/command -H 'Content-Type: application/json' -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp1","points":[{"lat":40.7,"lon":-74},{"lat":37.4,"lon":-122}],"color":"#FFD700","animated":true,"dashed":true}}}'

# Get state
curl -s localhost:5176/pr/state | python -m json.tool

# Navigate to node
curl -sX POST localhost:5176/pr/command -H 'Content-Type: application/json' -d '{"action":"navigate:node","params":{"nodeId":"alignment-policy"}}'
```
