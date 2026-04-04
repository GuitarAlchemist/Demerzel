# UI Chord Hydration Contract

**Status:** Draft
**Version:** v1
**Applies to:** Guitar Alchemist (ga) orchestrator, all GA client surfaces
**Related:** `contracts/ga-orchestrator-architecture.md`, `contracts/ga-mcp-tool-bundles.md`, `schemas/voicing-handle.schema.json`, `policies/mcp-context-budget.yaml`

This contract defines the **client-side hydration protocol** that lets the LLM emit compact handle-tagged markup in place of token-expensive fret/string matrices. Rich visuals are fetched **out-of-band** by the UI client, bypassing the LLM context window entirely.

---

## 1. The Token-Free Diagram Problem

Guitar chord diagrams are inherently visual. A single voicing has to communicate:

- 6 strings (or 4, 7, 8 depending on instrument)
- 15+ frets of potential positions
- Finger assignments (1-4, T for thumb)
- Muting, open strings, optional notes
- Barres, partial barres, capo offsets
- Dynamics: bends, slides, hammer-ons, vibrato

Even a **compact text representation** of a single chord burns tokens:

```
  E A D G B e
  ---------
  x 3 2 0 1 0    Cmaj7
    3 2   1        (fingers)
```

That's ~30-60 tokens per chord. A 10-chord progression eats **600 tokens** of pure chrome — before the LLM says anything musically useful. JSON-encoded voicings with full fingering metadata push **120+ tokens each**.

**The opportunity:** render visuals out-of-band. The LLM emits a tiny handle tag; the UI client intercepts it, fetches an SVG from GA, and substitutes rich visual content in place. The LLM's context stays clean. The user sees a beautiful interactive diagram.

This contract specifies the tag syntax, render API, client responsibilities, and migration path.

---

## 2. Hydration Tag Syntax

The LLM may emit the following self-closing XML-style tags. **Handle-backed tags** (`<ChordView>`, `<ProgressionView>`, `<VoiceLeadingView>`) reference content-addressable voicing handles per `schemas/voicing-handle.schema.json`. **Parameterized tags** (`<ScaleView>`, `<FretboardView>`) use descriptive attributes instead of handles because scales and fretboards are views over pitch-class collections, not fixed voicing objects.

In examples below, handles like `ga:vh:v3:sha256-7b91a4c2...` are shortened for readability. Real handles contain a full 64-character hexadecimal SHA-256 digest.

### 2.1 `<ChordView>`

Renders a single chord voicing as a fretboard diagram.

**Required attributes:**
- `id` — voicing handle URI (`ga:vh:v3:sha256-{64hex}`)

**Optional attributes:**
- `size` — `xs` | `sm` | `md` | `lg` (default: `md`)
- `theme` — `light` | `dark` | `auto` (default: `auto`)
- `layout` — `horizontal` | `vertical` (default: `vertical`)
- `show` — `frets` | `notes` | `fingers` | `all` (default: `all`)
- `highlight` — `string:fret` pair, e.g. `"3:5"` to emphasize a single note
- `tuning` — tuning identifier (e.g. `standard`, `dadgad`, `drop_d`)

**Example:**

```html
<ChordView id="ga:vh:v3:sha256-7b91a4c2..." tuning="dadgad" size="md"/>
```

---

### 2.2 `<ScaleView>`

Renders a scale across one or more positions on a fretboard.

**Required attributes:**
- `scale` — scale name or binary ID (e.g. `dorian`, `b:0xAB5`)
- `root` — root note (e.g. `D`, `F#`, `Bb`)
- `instrument` — instrument identifier (e.g. `guitar`, `ukulele`, `bass`)
- `tuning` — tuning identifier

**Optional attributes:**
- `positions` — comma list of CAGED positions, e.g. `"1,2,5"` (default: all)
- `pattern` — `caged` | `3nps` | `4nps` (default: `caged`)
- `highlight_root` — boolean, emphasize root notes (default: `true`)

**Example:**

```html
<ScaleView scale="dorian" root="D" instrument="guitar" tuning="standard" pattern="caged"/>
```

---

### 2.3 `<ProgressionView>`

Renders a chord progression with optional harmonic analysis and voice-leading.

**Required attributes:**
- `chords` — space-separated voicing handles OR chord symbols
- `key` — tonal center (e.g. `"C major"`, `"A minor"`)

**Optional attributes:**
- `analysis` — `roman` | `function` | `none` (default: `roman`)
- `show_voice_leading` — boolean (default: `false`)

**Example:**

```html
<ProgressionView
  chords="ga:vh:v3:sha256-aaa... ga:vh:v3:sha256-bbb... ga:vh:v3:sha256-ccc..."
  key="C major"
  analysis="roman"/>
```

---

### 2.4 `<FretboardView>`

Renders an empty or overlaid fretboard across a fret range.

**Required attributes:**
- `instrument` — instrument identifier
- `tuning` — tuning identifier
- `fret_range` — range string, e.g. `"0-12"` or `"5-9"`

**Optional attributes:**
- `highlight` — comma list of notes to mark (e.g. `"C,E,G"`)
- `overlay` — scale or chord content to display (e.g. `"C major scale"`)

**Example:**

```html
<FretboardView instrument="guitar" tuning="standard" fret_range="0-12" overlay="C major scale"/>
```

---

### 2.5 `<VoiceLeadingView>`

Renders the transition between two voicings with motion arrows.

**Required attributes:**
- `from` — voicing handle URI
- `to` — voicing handle URI

**Optional attributes:**
- `animate` — boolean, render as animated transition (default: `false`)
- `show_motion_arrows` — boolean (default: `true`)

**Example:**

```html
<VoiceLeadingView from="ga:vh:v3:sha256-aaa..." to="ga:vh:v3:sha256-bbb..." show_motion_arrows="true"/>
```

---

## 3. Token Cost Analysis

| Content | Without hydration | With hydration | Reduction |
|---------|------------------|----------------|-----------|
| Single chord diagram | 60 tokens (ASCII) | 12 tokens (tag) | 80% |
| 10-chord progression | 600 tokens | 120 tokens | 80% |
| Full voicing with fingering | 120 tokens (JSON) | 15 tokens (tag) | 87% |
| Scale diagram across 5 positions | 500 tokens | 15 tokens (tag) | 97% |
| Voice leading visualization | 300+ tokens (description) | 20 tokens (tag) | 93% |

**Aggregate effect:** a typical guitar lesson conversation (20 diagrams, 5 scales, 3 voice-leading transitions) drops from **~3,500 tokens of chrome** to **~350 tokens** — a 90% reduction in visual content cost.

---

## 4. Hydration Flow

```
User:     "Show me Cmaj7 on guitar"

LLM:      Decides to use ga:vh handle, emits response:
          -> "Try this voicing: <ChordView id='ga:vh:v3:sha256-7b91...' tuning='standard'/>"

UI Middleware (chat client):
          -> Parses response stream
          -> Detects <ChordView> tag
          -> Fetches SVG from GA API:
               GET /api/render/chord?handle=ga:vh:v3:sha256-7b91...&size=md
          -> Substitutes rendered SVG in place of the tag
          -> Passes rest of response through unchanged

User sees: Text + beautiful interactive chord diagram

LLM context: Still just the 15-token tag. No rendering data ever
             entered or exited the model's context window.
```

Key property: **the rendering pipeline never round-trips through the LLM**. The LLM only ever sees and emits the handle tag. All visual data flows client <-> GA API directly.

---

## 5. Server-Side Rendering API

GA must expose the following endpoints to resolve hydration tags:

```
GET /api/render/chord?handle={vh_handle}&size=md&theme=auto
  -> returns image/svg+xml

GET /api/render/scale?scale={name}&root={note}&instrument={id}&tuning={id}
  -> returns image/svg+xml

GET /api/render/progression?chords={space_separated}&key={key}
  -> returns image/svg+xml

GET /api/render/fretboard?instrument={id}&tuning={id}&overlay={content}
  -> returns image/svg+xml

GET /api/render/voice-leading?from={vh}&to={vh}
  -> returns image/svg+xml (optionally animated GIF/video)
```

**All endpoints MUST:**

- Return content-addressable URLs when possible (handle-based paths are immutable and CDN-cacheable)
- Support `Accept` header negotiation:
  - `image/svg+xml` (default, preferred)
  - `image/png` (raster fallback)
  - `application/json` (raw structured data for native components)
- Set `Cache-Control: public, max-age=31536000, immutable` for content-addressed URLs
- Version-bump endpoints when rendering semantics change: `/api/render/v2/chord`, `/api/render/v3/chord`, ...
- Return `404` with a machine-readable JSON body when a handle cannot be resolved
- Return `410 Gone` when a handle is deliberately deprecated

**Response headers (example):**

```
Content-Type: image/svg+xml
Cache-Control: public, max-age=31536000, immutable
ETag: "sha256-7b91a4c2..."
X-GA-Handle: ga:vh:v3:sha256-7b91a4c2...
X-GA-Alt-Text: Cmaj7 voicing, open position, standard tuning
```

---

## 6. Client Responsibilities

Any UI client implementing hydration MUST:

1. **Parse LLM responses** for hydration tags (HTML parser preferred; avoid brittle regex where possible)
2. **Fetch rendered content in parallel** — do not block on individual requests; batch where the API supports it
3. **Cache locally by handle URI** — handles are immutable and content-addressable, so local caches never need invalidation
4. **Provide fallback** for tags that fail to render (show raw tag text, or an image fallback, never a silent blank)
5. **Support accessibility** — auto-generate `alt` text from handle metadata (see Section 7)
6. **Support mobile** — honor `size` attribute and provide responsive SVG scaling
7. **Support dark mode** — `theme="auto"` MUST read system preference via `prefers-color-scheme`
8. **Stream-safe parsing** — if the LLM response streams token-by-token, buffer partial tags until fully formed before fetching

---

## 7. Accessibility Requirements

Every hydration tag MUST carry auto-generated accessibility metadata:

- **Alt text** is derived from handle metadata (returned in the `X-GA-Alt-Text` response header or embedded in the SVG `<title>` and `<desc>` elements)
- **Example:** `"Cmaj7 voicing, open position, standard tuning, fingers 3-2-1 on strings A-D-B"`
- **Screen readers** receive alt text instead of raw SVG contents
- **Keyboard navigation:** hydrated tags MUST be focusable (`tabindex="0"`) and respond to arrow keys for note-by-note exploration
- **High contrast mode:** clients MUST honor the OS high-contrast preference and GA MUST supply a high-contrast theme variant
- **Reduced motion:** `animate="true"` MUST be ignored when `prefers-reduced-motion: reduce` is set

Alt text is **non-negotiable** — it is the primary output for screen-reader users and the primary fallback for clients that cannot render.

---

## 8. Browser/Client Compatibility

| Client | Rendering mode |
|--------|----------------|
| GA web app | React `<ChordView>` component, native SVG with interactivity |
| GA Discord bot | Server-render to PNG, post as message attachment |
| GA mobile app (iOS/Android) | Native view component bound to GA API |
| GA VS Code extension | Webview panel with inline SVG |
| Terminal / CLI | Degrade to ASCII tab representation |
| Email | Server-render to inline PNG (CID attachment) |
| Slack / Teams / other chat | Server-render to PNG, post as attachment |
| Markdown export | Image link to content-addressed URL |

Each client surface is responsible for implementing the Client Responsibilities in Section 6, adapted to its native idioms.

---

## 9. Fallback Strategy

When a client does not fully support hydration, it degrades in this order:

```
Tier 1 (full support):     [rendered interactive SVG]
Tier 2 (image fallback):   ![Cmaj7 voicing](https://ga-api/render/chord?handle=ga:vh:v3:sha256-7b91...)
Tier 3 (code fallback):    `<ChordView id="ga:vh:v3:sha256-7b91..." tuning="standard"/>`
Tier 4 (accessibility):    alt text rendered as plain text
```

**Tier selection rules:**
- Unknown-tag tier: if a client sees a tag it does not recognize, it MUST default to Tier 2 (image fallback via the GA API) rather than dropping the tag silently
- Offline tier: if the GA API is unreachable, clients MUST show Tier 3 (raw tag as code block) plus Tier 4 (alt text), never a blank
- A11y tier: alt text MUST be shown in all tiers, even when visual content renders successfully

---

## 10. Security Considerations

- **Handle URIs are public.** They are content-addressable hashes; no authentication is required to resolve them.
- **Render endpoints are rate-limited.** Default: 100 requests/minute per client IP or API key. Burst allowance configurable per deployment.
- **SVG sanitization is server-side.** GA MUST strip `<script>`, `<foreignObject>`, and event-handler attributes before returning SVG.
- **Client CSP:** embedding applications MUST allow the GA render domain in `img-src` and `style-src` (for inline SVG styles).
- **No user-supplied handles.** All handles MUST be server-generated by GA. Clients MUST NOT construct handle URIs from arbitrary user input — they are opaque identifiers.
- **No PII in handles.** Handles are hashes of musical content, not users. Tag rendering leaks nothing about the requester.
- **Referer policy:** GA's render endpoints SHOULD set `Referrer-Policy: no-referrer` on SVG responses to avoid leaking parent page URLs.

---

## 11. Worked Examples

### Example 1: Chord lookup

```
User: "What's Dm7 on ukulele?"

LLM:  "Dm7 on ukulele (standard tuning) is played
       <ChordView id='ga:vh:v3:sha256-d8f2...' tuning='ukulele_standard' size='md'/>.
       Notes: D, F, A, C."

LLM context cost: ~40 tokens
User sees: Text + rendered ukulele fretboard with Dm7 fingering
```

### Example 2: Progression visualization

```
User: "Show me ii-V-I in C"

LLM:  "Here's ii-V-I in C:
       <ProgressionView
         chords='ga:vh:v3:sha256-aaa... ga:vh:v3:sha256-bbb... ga:vh:v3:sha256-ccc...'
         key='C major'
         analysis='roman'
         show_voice_leading='true'/>"

LLM context cost: ~80 tokens
User sees: Three rendered chord diagrams with Roman numerals and voice-leading arrows
```

### Example 3: Scale position

```
User: "D Dorian in 5th position"

LLM:  "Play D Dorian at the 5th fret:
       <ScaleView scale='dorian' root='D' instrument='guitar'
                  tuning='standard' positions='5' highlight_root='true'/>"

LLM context cost: ~30 tokens
User sees: Full scale diagram on guitar neck at 5th fret
```

### Example 4: Voice-leading transition

```
User: "How do I move from Cmaj7 to Am7 smoothly?"

LLM:  "Minimal motion voice-leading from Cmaj7 to Am7:
       <VoiceLeadingView from='ga:vh:v3:sha256-c7m...' to='ga:vh:v3:sha256-a7m...'
                         show_motion_arrows='true' animate='true'/>
       Only two voices move: B -> A and G -> G (held)."

LLM context cost: ~55 tokens
User sees: Animated voicing transition with motion arrows
```

---

## 12. Integration with Existing Artifacts

- **`schemas/voicing-handle.schema.json`** — defines the `ga:vh:v3:*`, `ga:qr:v2:*`, `ga:mh:v1:*`, and `ga:view:v1:*` URI formats consumed by every hydration tag
- **`contracts/ga-orchestrator-architecture.md`** — tag emission is part of the orchestrator's output pipeline; the orchestrator is responsible for choosing handles over text
- **`contracts/ga-mcp-tool-bundles.md`** — tools that return voicing handles (theory, technique, composer bundles) feed directly into `<ChordView>` tags
- **`policies/mcp-context-budget.yaml`** — hydration is the **primary technique** listed for guitar visual content token reduction
- **`contracts/directives/ga-kinematic-pathfinder.directive.md`** — pathfinder output is a sequence of voicing handles, which the orchestrator wraps in `<ProgressionView>` or chained `<VoiceLeadingView>` tags
- **`contracts/socratic-tool-design.md`** — Socratic teaching tools use hydration tags in their prompts instead of ASCII fingering descriptions

---

## 13. Migration Path

### Server-side (GA orchestrator) phases

| Phase | LLM output behavior |
|-------|---------------------|
| **Phase 1** | Hydration tags added as OPTIONAL additions alongside existing text/ASCII fingering |
| **Phase 2** | Text fingering deprecated; tags become primary output; text kept only as fallback |
| **Phase 3** | Text fingering removed entirely from LLM responses; tags only |

### Client-side phases

| Phase | Client behavior |
|-------|-----------------|
| **Phase 1** | Unknown tags gracefully ignored or passed through as text |
| **Phase 2** | Tags rendered as images via markdown image fallback (Tier 2) |
| **Phase 3** | Native component rendering with interactivity (Tier 1), keyboard navigation, theme switching |

### Rollout constraints

- Server-side and client-side phases advance **independently**. A Phase 3 server can still serve Phase 1 clients via Tier 3 fallback.
- **No phase 3 server deploy** until at least one first-party client (web or Discord) has reached Phase 2.
- **Deprecation windows** are minimum 90 days between phases for first-party clients, minimum 180 days for third-party integrators.
- Each phase transition MUST be announced via Galactic Protocol directive from the GA repo, with migration notes.

---

**End of contract.**
