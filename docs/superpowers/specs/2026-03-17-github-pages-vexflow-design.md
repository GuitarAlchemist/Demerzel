# GitHub Pages with Interactive VexFlow Music Notation

**Date:** 2026-03-17
**Status:** Draft
**GitHub Issue:** #26
**Target Repo:** `guitaralchemist.github.io` (new, separate from Demerzel)

## Overview

A static GitHub Pages site for the Guitar Alchemist ecosystem, providing interactive music notation demos powered by VexFlow. The site serves as both a standalone learning tool and the visual companion to Demerzel's biweekly Show & Tell discussions. No build tooling required — vanilla HTML, CSS, and JavaScript only.

## Goals

1. Render interactive music notation (scales, chords, progressions) in the browser
2. Play notation back via Web Audio API
3. Link Show & Tell discussion posts to live interactive demos
4. Provide a musician-friendly, mobile-responsive experience
5. Zero build dependencies — deploy directly from `main` branch

## Site Architecture

### Page Structure

```
guitaralchemist.github.io/
├── index.html                  # Landing page — project overview, nav to demos
├── css/
│   └── style.css               # Global styles (dark theme, responsive grid)
├── js/
│   ├── vexflow-renderer.js     # Shared VexFlow rendering utilities
│   ├── audio-engine.js         # Web Audio API playback engine
│   └── fretboard.js            # SVG fretboard diagram generator
├── demos/
│   ├── scales/
│   │   └── index.html          # Interactive scale explorer
│   ├── chords/
│   │   └── index.html          # Chord voicing viewer
│   ├── progressions/
│   │   └── index.html          # Chord progression player
│   ├── circle-of-fifths/
│   │   └── index.html          # Interactive Circle of Fifths diagram
│   └── fretboard/
│       └── index.html          # Fretboard note/interval visualizer
├── showcase/
│   └── index.html              # Show & Tell archive — links to discussions + demos
└── 404.html                    # Custom 404 with navigation back to home
```

### Navigation

A persistent top nav bar across all pages:

- **Home** — landing page
- **Demos** — dropdown: Scales, Chords, Progressions, Circle of Fifths, Fretboard
- **Showcase** — Show & Tell archive
- **GitHub** — link to GuitarAlchemist org

## VexFlow Integration

### Loading Strategy

Load VexFlow via CDN in each page that needs notation. No bundler required.

```html
<script src="https://cdn.jsdelivr.net/npm/vexflow@4/build/cjs/vexflow.js"></script>
```

### Rendering Approach

A shared `vexflow-renderer.js` module wraps VexFlow's API to provide:

- `renderScale(container, root, scaleType)` — draws a scale on a staff with note names
- `renderChord(container, root, quality, voicing)` — draws a chord on a staff
- `renderProgression(container, chords[], key)` — draws a multi-measure progression
- `renderInterval(container, note1, note2)` — draws two notes with interval label

Each function takes a container element ID and renders an SVG into it. VexFlow 4.x uses its own SVG renderer — no Canvas needed.

### Rendering Container Pattern

Each demo page includes placeholder `<div>` elements. On page load, JavaScript calls the renderer functions to populate them. User interactions (dropdowns, buttons) re-render into the same containers.

```html
<div id="notation-output" class="vf-container"></div>
<script>
  renderScale('notation-output', 'C', 'major');
</script>
```

## Interactive Demo Pages

### 1. Scale Explorer (`demos/scales/`)

- **Controls:** Root note selector (C through B), scale type dropdown (major, natural minor, harmonic minor, melodic minor, pentatonic major/minor, blues, dorian, mixolydian, lydian)
- **Output:** Staff notation showing the scale ascending and descending, with note names below each note
- **Fretboard:** SVG fretboard diagram highlighting scale positions
- **Audio:** Play button to hear the scale ascending, with adjustable tempo
- **Connects to showcase topics:** Guitar Mathematics (topic 0), Circle of Fifths (topic 4)

### 2. Chord Voicing Viewer (`demos/chords/`)

- **Controls:** Root note selector, chord quality dropdown (maj, min, 7, maj7, min7, dim, aug, sus2, sus4, add9, maj7#11)
- **Output:** Staff notation showing the chord in close voicing, with interval labels
- **Fretboard:** Common guitar voicings shown as fretboard diagrams (up to 3 voicings per chord)
- **Audio:** Strum button (arpeggiated playback) and block chord button
- **Connects to showcase topics:** Chord Progressions (topic 2), OPTIC-K embeddings (topic 7)

### 3. Chord Progression Player (`demos/progressions/`)

- **Preset progressions:** I-V-vi-IV (pop), ii-V-I (jazz), I-IV-V (blues), vi-IV-I-V (emotional), I-vi-IV-V (50s)
- **Controls:** Key selector, tempo slider, play/pause/stop
- **Output:** Multi-measure staff notation with chord symbols above, current chord highlighted during playback
- **Audio:** Playback loops the progression with basic piano/guitar tone
- **Connects to showcase topics:** Chord Progressions (topic 2), Multi-Agent Teams (topic 3)

### 4. Circle of Fifths (`demos/circle-of-fifths/`)

- **Visualization:** SVG circle with all 12 keys arranged by fifths, inner ring showing relative minors
- **Interaction:** Click a key to highlight it, show its key signature on a staff, display diatonic chords
- **Relationships:** Highlight adjacent keys (closely related), opposite keys (tritone), and common progressions as arcs
- **Staff output:** VexFlow renders the key signature and diatonic chord scale for the selected key
- **Connects to showcase topics:** Circle of Fifths (topic 4), Guitar Mathematics (topic 0)

### 5. Fretboard Visualizer (`demos/fretboard/`)

- **Controls:** Tuning selector (standard, drop-D, open G, DADGAD), display mode (notes, intervals, scale degrees)
- **Output:** Full SVG fretboard (frets 0-15) with interactive note dots
- **Interaction:** Click a root note, then select a scale or chord to highlight the pattern
- **Math overlay:** Toggle to show fret distance ratios (connecting to the 2^(1/12) showcase topic)
- **Connects to showcase topics:** Guitar Mathematics (topic 0), OPTIC-K embeddings (topic 7)

## Audio Playback

### Engine: Web Audio API (native)

Use the browser's built-in Web Audio API rather than a library like Tone.js. This keeps the dependency count at zero and is sufficient for the playback needs.

```
audio-engine.js exports:
  - playNote(frequency, duration, waveType)
  - playChord(frequencies[], duration, strum?)
  - playSequence(notes[], tempo)
  - stopAll()
```

### Sound Design

- **Waveform:** Triangle wave for a clean, guitar-like tone. Optional sine wave for a mellow alternative.
- **Envelope:** Simple ADSR (attack 0.02s, decay 0.1s, sustain 0.7, release 0.3s) via gain node scheduling.
- **Frequency calculation:** `f = 440 * 2^((midiNote - 69) / 12)` — standard equal temperament from MIDI note numbers.

### Strum Simulation

For chord playback, stagger note onsets by 20-40ms each to simulate a guitar strum. Direction (up/down) can be toggled.

## Show & Tell Integration

### How It Works

The biweekly Show & Tell workflow (`demerzel-showcase.yml`) posts discussions to the GuitarAlchemist org. The 8 rotating topics map to demo pages:

| Topic Index | Showcase Topic | Linked Demo Page |
|-------------|---------------|------------------|
| 0 | Guitar Mathematics (tuning, frets) | `/demos/fretboard/` + `/demos/scales/` |
| 1 | AI Governance (Asimov's Laws) | `/showcase/` (governance overview, no notation) |
| 2 | Chord Progressions | `/demos/progressions/` |
| 3 | Multi-Agent Teams | `/showcase/` (architecture overview, no notation) |
| 4 | Circle of Fifths | `/demos/circle-of-fifths/` |
| 5 | Neuro-Symbolic AI (TARS) | `/showcase/` (architecture overview, no notation) |
| 6 | Meta-Compounding | `/showcase/` (governance overview, no notation) |
| 7 | OPTIC-K Embeddings | `/demos/chords/` + `/demos/fretboard/` |

### Showcase Archive Page

`showcase/index.html` provides:

- A chronological list of past Show & Tell topics with links to the GitHub Discussion posts
- For music-focused topics (0, 2, 4, 7): direct "Try it live" buttons linking to the relevant demo page
- For governance/AI topics (1, 3, 5, 6): summary cards with links to Demerzel repo documentation

### Discussion Post Enhancement

Future Show & Tell discussion posts can include a footer line:

```
**Try it live:** [Interactive Demo](https://guitaralchemist.github.io/demos/circle-of-fifths/)
```

This requires a minor update to the `demerzel-showcase.yml` workflow to append the link for music-related topics.

## Deployment

### GitHub Pages Configuration

- **Source:** Deploy from `main` branch, root directory (`/`)
- **Custom domain:** None initially (use `guitaralchemist.github.io`)
- **HTTPS:** Enforced by default on GitHub Pages

### Repository Setup

1. Create `guitaralchemist.github.io` repo under the GuitarAlchemist org
2. Enable GitHub Pages in repo settings (source: main branch, root)
3. Push the static files — site is live immediately

### No Build Step

All files are served as-is. VexFlow loads from CDN. CSS and JS are vanilla. No Node.js, no npm, no webpack, no framework.

## Mobile-Responsive Design

### Approach

CSS media queries with a mobile-first strategy.

### Breakpoints

- **Mobile** (< 768px): Single column, stacked notation + controls, full-width fretboard (horizontal scroll if needed)
- **Tablet** (768px - 1024px): Two-column layout where appropriate, side-by-side notation and controls
- **Desktop** (> 1024px): Full layout with sidebar navigation, spacious notation rendering

### Notation Responsiveness

- VexFlow SVG output scales naturally with container width
- Set `width: 100%` on notation containers with a `max-width` for readability
- Fretboard diagrams: allow horizontal scroll on mobile rather than squashing

### Touch Considerations

- Minimum tap target size: 44x44px for all interactive elements
- Fretboard note dots enlarged on touch devices
- Swipe gestures: none initially (keep interaction model simple)

### Typography

- Body: system font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`)
- Headings: same stack, semibold
- Code/music terms: monospace where appropriate
- Base size: 16px, scale up for headings

## Visual Design

### Theme

Dark theme with warm accents — suitable for musicians and easy on the eyes.

- **Background:** `#1a1a2e` (dark navy)
- **Surface:** `#16213e` (slightly lighter)
- **Primary accent:** `#e94560` (warm red — for interactive elements)
- **Secondary accent:** `#0f3460` (deep blue — for secondary UI)
- **Text:** `#eee` on dark backgrounds
- **Note highlights:** `#ffd700` (gold — for selected/active notes)

### Layout Principles

- Max content width: 1200px, centered
- Generous whitespace around notation (music needs breathing room)
- Controls grouped above their output, clearly labeled
- Consistent card-based layout for demo sections

## Future Considerations

These are out of scope for the initial release but worth noting:

- **MIDI input:** Accept MIDI keyboard input to highlight played notes on the fretboard
- **Preset sharing:** URL-encoded state so users can share specific scale/chord configurations
- **GA domain integration:** Once GA's .NET domain engine has a REST API, replace hardcoded music theory data with live API calls
- **Tone.js upgrade:** If audio needs grow beyond simple playback (effects, recording), migrate from raw Web Audio API to Tone.js
- **PWA support:** Add a service worker for offline access to demos

## Implementation Phases

### Phase 1: Foundation

- Repository setup and GitHub Pages deployment
- Landing page with navigation
- `vexflow-renderer.js` with `renderScale()` and `renderChord()`
- Scale Explorer demo (fully functional)
- Basic `audio-engine.js` with `playNote()` and `playSequence()`

### Phase 2: Core Demos

- Chord Voicing Viewer
- Chord Progression Player with playback
- Fretboard Visualizer (SVG generation)

### Phase 3: Circle of Fifths + Showcase

- Interactive Circle of Fifths diagram
- Showcase archive page
- Update `demerzel-showcase.yml` to include demo links

### Phase 4: Polish

- Mobile responsiveness pass
- Cross-browser testing
- Performance optimization (lazy-load VexFlow on demo pages only)
- 404 page
