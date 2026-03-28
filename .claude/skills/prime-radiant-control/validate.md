# Prime Radiant Visual Validation Loop

Full visual validation pattern for verifying Prime Radiant state matches expected visual output. Combines programmatic state checks with screenshot-based visual analysis.

## Loop Pattern

```
1. Send command(s)      POST /pr/command  {action, params}
2. Wait 2 seconds       Allow React render + Three.js frame
3. Take screenshot      Windows MCP Screenshot tool
4. Analyze screenshot   Check for expected visual elements
5. Read state           GET /pr/state — programmatic truth
6. Compare              Visual vs programmatic agreement
7. Correct if needed    Send corrective commands, repeat from 1
8. Report               Pass/fail with evidence
```

## Implementation Steps

### Step 1 — Send Command

```bash
curl -sX POST localhost:5176/pr/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-pin","params":{"planet":"earth","pin":{"id":"v1","lat":40.7,"lon":-74,"label":"Validate","color":"#ff0000","pulse":true}}}'
```

### Step 2 — Wait

Wait 2 seconds for React to process the SSE event, update Three.js scene graph, and render at least one frame.

### Step 3 — Screenshot

Use the Windows MCP `Screenshot` tool to capture the current desktop. The Prime Radiant window must be visible and focused.

### Step 4 — Analyze

Examine the screenshot for:
- Pin markers visible on the globe at approximately correct positions
- Pin labels readable and matching expected text
- Pulse animations active (ring visible around pulsing pins)
- Panel state matches (correct panel open, tabs active)
- Path arcs visible between expected points
- Cluster bubbles showing correct counts
- No rendering errors (black rectangles, missing textures, WebGL errors)

### Step 5 — Read State

```bash
curl -s localhost:5176/pr/state | python -m json.tool
```

Check the returned JSON for:
- `gis.earth.pins` count matches expected
- `gis.earth.paths` count matches expected
- `panels.active` matches expected panel
- `selectedNode` matches expected selection

### Step 6 — Compare

If the screenshot shows visual elements that contradict the programmatic state (e.g., state says 5 pins but screenshot shows none), the render pipeline has a bug. If state is correct but visuals are wrong, the issue is in Three.js rendering. If state is wrong, the command was not processed.

### Step 7 — Correct

Send corrective commands. Common fixes:
- Pins not visible: check planet name, verify lat/lon in valid range
- Panel not open: resend `panel:open` command
- Cluster count wrong: toggle clustering off and on

### Step 8 — Report

Report with:
- Commands sent
- State snapshot (JSON)
- Visual analysis (what was seen in screenshot)
- Pass/fail verdict
- Corrective actions taken (if any)

## Example Scenarios

### Scenario 1: Add 5 Governance Pins and Verify They Appear on Earth

**Goal:** Add pins for Demerzel, ix, tars, ga, and Seldon at known coordinates and confirm all 5 render visually on the globe.

```
1. POST /pr/command  gis:add-pins  planet=earth  pins=[
     {id:"demerzel", lat:40.7, lon:-74.0, label:"Demerzel", icon:"\ud83d\udee1", color:"#FFD700", pulse:true},
     {id:"ix",       lat:37.4, lon:-122.0, label:"ix",       icon:"\u2699", color:"#73D117"},
     {id:"tars",     lat:51.5, lon:-0.1,   label:"tars",     icon:"\ud83e\udde0", color:"#8B5CF6"},
     {id:"ga",       lat:48.9, lon:2.3,    label:"ga",       icon:"\ud83c\udfb8", color:"#F97316"},
     {id:"seldon",   lat:35.7, lon:139.7,  label:"Seldon",   icon:"\ud83d\udcda", color:"#06B6D4"}
   ]
2. Wait 2 seconds
3. Screenshot — expect 5 colored markers visible on Earth
4. GET /pr/state — expect gis.earth.pins == 5
5. Visual check: golden pulsing marker near NYC, green near SF,
   purple near London, orange near Paris, cyan near Tokyo
6. If any pin missing: check console for errors, resend individual pin
7. PASS if 5 pins visible AND state reports 5
```

### Scenario 2: Open GIS Panel, Add Path, Toggle Clustering, Verify Cluster Count

**Goal:** Open the GIS panel, add 6 pins close together plus a path, enable clustering, and verify the cluster count.

```
1. POST /pr/command  panel:open  panelId=gis
2. Wait 1 second, screenshot — verify GIS panel is open
3. POST /pr/command  gis:add-pins  planet=earth  pins=[
     {id:"c1", lat:40.7, lon:-74.0, label:"C1", color:"#ff4444"},
     {id:"c2", lat:40.8, lon:-73.9, label:"C2", color:"#ff4444"},
     {id:"c3", lat:40.6, lon:-74.1, label:"C3", color:"#ff4444"},
     {id:"c4", lat:40.75, lon:-73.95, label:"C4", color:"#ff4444"},
     {id:"c5", lat:40.65, lon:-74.05, label:"C5", color:"#ff4444"},
     {id:"c6", lat:40.85, lon:-73.85, label:"C6", color:"#ff4444"}
   ]
4. POST /pr/command  gis:add-path  planet=earth  path={
     id:"test-path", points:[{lat:40.7,lon:-74},{lat:48.9,lon:2.3}],
     color:"#33ccff", animated:true, dashed:true
   }
5. POST /pr/command  gis:cluster  planet=earth  enabled=true  radius=10
6. Wait 2 seconds, screenshot
7. GET /pr/state — expect:
   - gis.earth.pins == 6
   - gis.earth.paths == 1
   - gis.earth.clusters >= 1 (all 6 pins within 10-degree radius)
8. Visual check: single purple cluster bubble with "6" label near NYC,
   dashed animated arc from NYC to Paris
9. POST /pr/command  gis:cluster  planet=earth  enabled=false
10. Wait 2 seconds, screenshot — expect 6 individual pins visible again
11. PASS if cluster appeared, count matched, and individual pins restored
```

### Scenario 3: Navigate to Node, Verify Detail Panel Opens

**Goal:** Navigate to a governance node and confirm the detail panel opens with correct content.

```
1. POST /pr/command  navigate:node  nodeId=alignment-policy
2. Wait 2 seconds
3. Screenshot — expect the force graph to center on the alignment-policy node
4. GET /pr/state — expect selectedNode == "alignment-policy"
5. POST /pr/command  panel:open  panelId=detail
6. Wait 1 second, screenshot
7. Visual check: detail panel visible with "alignment-policy" title,
   node metadata displayed, connections listed
8. If selectedNode is null: node ID may not exist, try listing nodes first
9. PASS if node is selected AND detail panel shows correct node info
```

## Failure Taxonomy

| Failure | Likely Cause | Fix |
|---------|-------------|-----|
| State correct, visuals wrong | Three.js render issue, camera angle | Rotate camera, force re-render |
| State wrong, command sent | SSE not connected, hook not active | Check `/pr/events` stream |
| Screenshot blank/black | WebGL context lost, Godot crash | Reload page, check console |
| Pin at wrong position | lat/lon swapped or out of range | Verify coordinate order |
| Cluster count mismatch | Radius too small/large | Adjust cluster radius parameter |
| Panel not visible | Panel ID typo, panel already open | Check supported panel IDs |
