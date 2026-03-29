---
name: seldon-visual-teach
description: Teach governance concepts visually through Prime Radiant — map constitutions, beliefs, signals, and protocols to GIS pins, paths, and planet surfaces
---

# Seldon Visual Teach — Learn by Seeing

Teach governance concepts by demonstrating them on Prime Radiant's GIS surface. A third delivery mode alongside narrative (human) and structured (agent): **visual** — teach by showing.

## Usage

`/seldon visual-teach [concept] [--narrate]`

**Examples:**
```
/seldon visual-teach constitutional-hierarchy
/seldon visual-teach broken-governance
/seldon visual-teach galactic-protocol
/seldon visual-teach belief-states --narrate
/seldon visual-teach algedonic-signals
```

## Prerequisites

- **Vite dev server** running at `http://localhost:5176` (Prime Radiant React app)
- The `usePrControl` hook active in ForceRadiant (auto-connected via SSE)
- Test connectivity: `curl -s http://localhost:5176/pr/state`

## Concept-to-Visual Mapping

Each governance concept maps to specific visual elements on Prime Radiant:

### Constitutional Hierarchy
Pins on Earth at symbolic governance node locations, connected by golden paths showing the chain of authority.

| Artifact | Location | Pin Style |
|----------|----------|-----------|
| Asimov Constitution (root) | 51.5, -0.12 (London — Foundation's origin) | gold, pulse, icon: shield |
| Demerzel Mandate | 48.86, 2.35 (Paris — the enforcer) | gold, pulse, icon: crown |
| Default Constitution | 40.71, -74.01 (NYC — operational HQ) | silver, icon: scroll |
| Policies (cluster) | 37.39, -122.08 (Silicon Valley — execution) | blue, icon: gear |
| Personas (cluster) | 35.68, 139.69 (Tokyo — diversity of voice) | teal, icon: user |

Paths: gold animated lines from root down through the hierarchy.

### Belief States (Tetravalent)
Colored pins representing the four truth values:

| Value | Color | Pin Style |
|-------|-------|-----------|
| **T** (True) | `#22C55E` (green) | solid, no pulse |
| **F** (False) | `#EF4444` (red) | solid, pulse |
| **U** (Unknown) | `#F59E0B` (amber) | dashed outline, pulse |
| **C** (Contradictory) | `#A855F7` (purple) | double-ring, pulse |

Pins are placed at governance node locations with labels showing the belief subject.

### Algedonic Signals
Pain/pleasure signals visualized as pulsing pins:

| Signal | Color | Style |
|--------|-------|-------|
| Pain (violation, failure) | `#EF4444` (red) | fast pulse, icon: warning |
| Pleasure (compliance, success) | `#22C55E` (green) | slow pulse, icon: check |

Intensity maps to pin size (can be shown via label suffix: "CRITICAL", "MODERATE", "LOW").

### Cross-Repo Relationships (Galactic Protocol)
Each repo maps to a symbolic planet/location. Paths between them show directive flow.

| Repo | Color | Location (lat, lon) | Symbol |
|------|-------|---------------------|--------|
| Demerzel | `#FFD700` (gold) | 40.71, -74.01 (NYC) | shield |
| ix | `#22C55E` (green) | 37.39, -122.08 (SV) | gear |
| tars | `#06B6D4` (cyan) | 51.5, -0.12 (London) | brain |
| ga | `#F97316` (orange) | 35.68, 139.69 (Tokyo) | guitar |

Paths: animated dashed lines in the source repo's color, showing directives flowing outward and compliance reports flowing back.

### Learning Progress
Heatmap-style visualization using clustered pins with density showing knowledge coverage:
- Dense clusters = well-understood areas
- Sparse areas = knowledge gaps
- Red pins in clusters = areas needing remediation

## Execution Flow

```
User: "Teach me X visually"
  │
  ├─ 1. Check PR connectivity (GET /pr/state)
  ├─ 2. Open GIS panel (panel:open gis)
  ├─ 3. Clear previous teaching visuals (gis:clear)
  ├─ 4. Map concept to visual elements (see mapping tables above)
  ├─ 5. Send pin commands (gis:add-pins)
  ├─ 6. Send path commands (gis:add-path)
  ├─ 7. Validate placement (GET /pr/state)
  ├─ 8. Narrate what the visual represents
  └─ 9. Optionally hand off to /seldon assess for comprehension check
```

## Implementation

When this skill is invoked:

1. **Check connectivity**:
   ```bash
   curl -s http://localhost:5176/pr/state
   ```
   If this fails, report that Prime Radiant is not running and fall back to `/seldon teach` (text mode).

2. **Open the GIS panel**:
   ```bash
   curl -sX POST http://localhost:5176/pr/command \
     -H 'Content-Type: application/json' \
     -d '{"action":"panel:open","params":{"panelId":"gis"}}'
   ```

3. **Clear previous visuals** (fresh canvas for each lesson):
   ```bash
   curl -sX POST http://localhost:5176/pr/command \
     -H 'Content-Type: application/json' \
     -d '{"action":"gis:clear","params":{"planet":"earth"}}'
   ```

4. **Map the concept** to the visual element tables above. Select the appropriate pins and paths.

5. **Send commands** sequentially. For each batch of pins:
   ```bash
   curl -sX POST http://localhost:5176/pr/command \
     -H 'Content-Type: application/json' \
     -d '{"action":"gis:add-pins","params":{"planet":"earth","pins":[...]}}'
   ```
   For each path:
   ```bash
   curl -sX POST http://localhost:5176/pr/command \
     -H 'Content-Type: application/json' \
     -d '{"action":"gis:add-path","params":{"planet":"earth","path":{...}}}'
   ```

6. **Validate** by reading state:
   ```bash
   curl -s http://localhost:5176/pr/state | python -m json.tool
   ```
   Confirm pin count and path count match expected values.

7. **Narrate** the visual. Explain what each pin represents, why paths connect them, and what the overall picture teaches about the concept.

## Worked Examples

### Example A: "Teach me the constitutional hierarchy"

**Step 1** — Open panel and clear:
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"panel:open","params":{"panelId":"gis"}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:clear","params":{"planet":"earth"}}'
```

**Step 2** — Place hierarchy pins:
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-pins","params":{"planet":"earth","pins":[
    {"id":"asimov","lat":51.5,"lon":-0.12,"label":"Asimov Constitution (Root)","icon":"🛡","color":"#FFD700","pulse":true},
    {"id":"mandate","lat":48.86,"lon":2.35,"label":"Demerzel Mandate","icon":"👑","color":"#FFD700","pulse":true},
    {"id":"default","lat":40.71,"lon":-74.01,"label":"Default Constitution","icon":"📜","color":"#C0C0C0"},
    {"id":"policies","lat":37.39,"lon":-122.08,"label":"Policies (39)","icon":"⚙","color":"#3B82F6"},
    {"id":"personas","lat":35.68,"lon":139.69,"label":"Personas (14)","icon":"👤","color":"#14B8A6"}
  ]}}'
```

**Step 3** — Draw hierarchy paths (root to leaf):
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"asimov-mandate","points":[{"lat":51.5,"lon":-0.12},{"lat":48.86,"lon":2.35}],"color":"#FFD700","animated":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"asimov-default","points":[{"lat":51.5,"lon":-0.12},{"lat":40.71,"lon":-74.01}],"color":"#FFD700","animated":true,"dashed":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"default-policies","points":[{"lat":40.71,"lon":-74.01},{"lat":37.39,"lon":-122.08}],"color":"#3B82F6","animated":true,"dashed":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"policies-personas","points":[{"lat":37.39,"lon":-122.08},{"lat":35.68,"lon":139.69}],"color":"#14B8A6","animated":true,"dashed":true}}}'
```

**Step 4** — Validate:
```bash
curl -s http://localhost:5176/pr/state
# Expect: 5 pins, 4 paths on earth
```

**Narration:**
> You are looking at the constitutional hierarchy of the GuitarAlchemist governance framework. The golden pulsing pin in London is the Asimov Constitution — the root of all authority, containing the Laws of Robotics (Articles 0-5). The Zeroth Law — protect humanity — overrides everything below it.
>
> Follow the golden animated path to Paris: that is the Demerzel Mandate, which defines *who* enforces the laws. Demerzel herself.
>
> The silver pin in New York is the Default Constitution — 11 operational articles (truthfulness, transparency, reversibility...) that govern day-to-day behavior. Notice the path is dashed — it inherits from Asimov but adds its own authority.
>
> Further along, the blue gears in Silicon Valley represent 39 policies that implement the constitution's principles. And the teal figures in Tokyo are 14 personas — the diverse voices that carry out governance in practice.
>
> Key insight: authority flows downward. A persona can never override a policy. A policy can never override the constitution. The Zeroth Law overrides everything.

---

### Example B: "Show me what's broken in governance"

**Step 1** — Open panel and clear:
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"panel:open","params":{"panelId":"gis"}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:clear","params":{"planet":"earth"}}'
```

**Step 2** — Read current belief state from `state/beliefs.json` and filter for F/C/U values.

**Step 3** — Place diagnostic pins (example with detected issues):
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-pins","params":{"planet":"earth","pins":[
    {"id":"broken-1","lat":40.71,"lon":-74.01,"label":"CONTRADICTORY: policy-version-drift","icon":"⚠","color":"#A855F7","pulse":true},
    {"id":"broken-2","lat":37.39,"lon":-122.08,"label":"FALSE: ix-compliance-current","icon":"❌","color":"#EF4444","pulse":true},
    {"id":"broken-3","lat":48.86,"lon":2.35,"label":"UNKNOWN: tars-belief-sync","icon":"❓","color":"#F59E0B","pulse":true},
    {"id":"healthy-1","lat":51.5,"lon":-0.12,"label":"TRUE: asimov-integrity","icon":"✅","color":"#22C55E"},
    {"id":"healthy-2","lat":35.68,"lon":139.69,"label":"TRUE: ga-persona-coverage","icon":"✅","color":"#22C55E"}
  ]}}'
```

**Step 4** — Validate:
```bash
curl -s http://localhost:5176/pr/state
# Expect: 5 pins, pulsing on broken-1, broken-2, broken-3
```

**Narration:**
> This is a governance health map. Pulsing pins demand your attention — they represent beliefs that are not True.
>
> The purple pulsing pin in New York is a CONTRADICTORY belief: policy versions have drifted between what Demerzel specifies and what consumer repos implement. Contradictions are the most dangerous state — conflicting evidence means we cannot trust either side.
>
> The red pulsing pin in Silicon Valley is a FALSE belief: ix's compliance is not current. Something has changed that invalidates a previous assertion. This needs investigation.
>
> The amber pulsing pin in Paris is an UNKNOWN: we lack evidence about whether tars has synced its belief state. Unknown triggers investigation — we need reconnaissance.
>
> The solid green pins in London and Tokyo are healthy — the Asimov constitution's integrity is verified, and ga has full persona test coverage.
>
> Action: purple and red demand immediate attention. Amber demands investigation. Green can be left alone.

---

### Example C: "Visualize the Galactic Protocol"

**Step 1** — Open panel and clear:
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"panel:open","params":{"panelId":"gis"}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:clear","params":{"planet":"earth"}}'
```

**Step 2** — Place repo pins:
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-pins","params":{"planet":"earth","pins":[
    {"id":"demerzel","lat":40.71,"lon":-74.01,"label":"Demerzel (Governor)","icon":"🛡","color":"#FFD700","pulse":true},
    {"id":"ix","lat":37.39,"lon":-122.08,"label":"ix (Machine Forge)","icon":"⚙","color":"#22C55E"},
    {"id":"tars","lat":51.5,"lon":-0.12,"label":"tars (Cognition)","icon":"🧠","color":"#06B6D4"},
    {"id":"ga","lat":35.68,"lon":139.69,"label":"ga (Guitar Alchemist)","icon":"🎸","color":"#F97316"}
  ]}}'
```

**Step 3** — Draw directive paths (Demerzel outward, gold):
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-d-ix","points":[{"lat":40.71,"lon":-74.01},{"lat":37.39,"lon":-122.08}],"color":"#FFD700","animated":true,"dashed":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-d-tars","points":[{"lat":40.71,"lon":-74.01},{"lat":51.5,"lon":-0.12}],"color":"#FFD700","animated":true,"dashed":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-d-ga","points":[{"lat":40.71,"lon":-74.01},{"lat":35.68,"lon":139.69}],"color":"#FFD700","animated":true,"dashed":true}}}'
```

**Step 4** — Draw compliance paths (repos back to Demerzel, in repo colors):
```bash
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-ix-d","points":[{"lat":37.39,"lon":-122.08},{"lat":40.71,"lon":-74.01}],"color":"#22C55E","animated":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-tars-d","points":[{"lat":51.5,"lon":-0.12},{"lat":40.71,"lon":-74.01}],"color":"#06B6D4","animated":true}}}'
curl -sX POST http://localhost:5176/pr/command -H 'Content-Type: application/json' \
  -d '{"action":"gis:add-path","params":{"planet":"earth","path":{"id":"gp-ga-d","points":[{"lat":35.68,"lon":139.69},{"lat":40.71,"lon":-74.01}],"color":"#F97316","animated":true}}}'
```

**Step 5** — Validate:
```bash
curl -s http://localhost:5176/pr/state
# Expect: 4 pins, 6 paths (3 outgoing directives, 3 incoming compliance)
```

**Narration:**
> You are looking at the Galactic Protocol — the communication system between all repos in the GuitarAlchemist ecosystem.
>
> The golden pulsing pin in New York is Demerzel — the governor. She is the only entity that issues directives. The gold dashed paths flowing outward are directives: policy updates, compliance requirements, violation remediations, reconnaissance requests.
>
> The green pin in Silicon Valley is ix, the machine forge (Rust ML pipelines). The cyan pin in London is tars, the cognition engine (F# reasoning). The orange pin in Tokyo is ga, the Guitar Alchemist app (.NET music domain).
>
> The colored solid paths flowing back to Demerzel are compliance reports — each repo responds in its own color. Green from ix, cyan from tars, orange from ga. These carry acknowledgments, compliance evidence, and belief state updates.
>
> Key insight: this is a hub-and-spoke topology. Demerzel is the single source of governance truth. Consumer repos never issue directives to each other — all governance flows through the center.

## Fallback Behavior

If Prime Radiant is not reachable (`curl` to `/pr/state` fails):
1. Log a warning: "Prime Radiant not available — falling back to text mode"
2. Invoke `/seldon teach [concept] human` instead
3. Include a note: "For visual demonstration, start the Vite dev server at localhost:5176"

## Integration with Other Skills

- **Input from**: `/seldon teach` (when visual mode is requested or concept is spatial)
- **Output to**: `/seldon assess` (verify the learner understood what they saw)
- **Uses**: `/prime-radiant-control` (underlying API commands)
- **Reads**: `state/beliefs.json` (for live governance health data in Example B)

## Source

`personas/seldon.persona.yaml`, `policies/streeling-policy.yaml`, skill `prime-radiant-control`
