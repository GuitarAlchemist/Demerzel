# GitHub Pages with VexFlow Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create guitaralchemist.github.io with interactive music notation demos using VexFlow, audio playback, and Show & Tell integration.

**Architecture:** Static site with vanilla HTML/CSS/JS. VexFlow loaded via CDN renders notation as SVG. Web Audio API handles playback. Dark theme, mobile-responsive, card-based layout.

**Tech Stack:** HTML5, CSS3, JavaScript (ES6+), VexFlow 4.x (CDN), Web Audio API

---

## Phase 1: Foundation

### 1.1 Repository Setup

- [ ] **Create the repo.** Create `guitaralchemist.github.io` under the GuitarAlchemist GitHub org. Initialize with a `main` branch and no template.

- [ ] **Enable GitHub Pages.** In repo Settings > Pages, set source to `main` branch, root directory (`/`). HTTPS is enforced by default.

- [ ] **Create directory structure.** From the repo root, create the following empty directories:

```
css/
js/
demos/scales/
demos/chords/
demos/progressions/
demos/circle-of-fifths/
demos/fretboard/
showcase/
```

- [ ] **Add a placeholder index.html to verify deployment.** Create `index.html` at the repo root:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Guitar Alchemist</title>
</head>
<body>
  <h1>Guitar Alchemist</h1>
  <p>Site coming soon.</p>
</body>
</html>
```

- [ ] **Verify:** Push to `main`, wait ~60 seconds, visit `https://guitaralchemist.github.io`. The placeholder page should render.

### 1.2 Global Stylesheet

- [ ] **Create `css/style.css`.** This is the single shared stylesheet for the entire site.

```css
/* ── Reset ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Design tokens ─────────────────────────────────── */
:root {
  --bg:        #1a1a2e;
  --surface:   #16213e;
  --primary:   #e94560;
  --secondary: #0f3460;
  --text:      #eee;
  --gold:      #ffd700;
  --radius:    8px;
  --max-width: 1200px;
  --font:      -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ── Base ──────────────────────────────────────────── */
html { font-size: 16px; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}
a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Layout ────────────────────────────────────────── */
.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 1rem;
}

/* ── Nav ───────────────────────────────────────────── */
.site-nav {
  background: var(--surface);
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  border-bottom: 2px solid var(--secondary);
}
.site-nav .logo {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary);
}
.site-nav a { color: var(--text); font-size: 0.95rem; }
.site-nav a:hover { color: var(--primary); text-decoration: none; }
.nav-links { display: flex; gap: 1.25rem; flex-wrap: wrap; }

/* ── Cards ─────────────────────────────────────────── */
.card {
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--secondary);
}
.card h2, .card h3 { margin-bottom: 0.75rem; }

/* ── Controls ──────────────────────────────────────── */
.controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 1rem;
}
.controls label { font-size: 0.9rem; color: #ccc; }
.controls select, .controls button, .controls input[type="range"] {
  font-family: var(--font);
  font-size: 0.95rem;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius);
  border: 1px solid var(--secondary);
  background: var(--bg);
  color: var(--text);
  min-height: 44px;          /* touch-friendly */
  min-width: 44px;
}
.controls button {
  background: var(--primary);
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.controls button:hover { opacity: 0.85; }

/* ── VexFlow containers ────────────────────────────── */
.vf-container {
  width: 100%;
  max-width: 900px;
  overflow-x: auto;
  margin: 1rem 0;
  background: var(--surface);
  border-radius: var(--radius);
  padding: 1rem;
}
.vf-container svg { max-width: 100%; height: auto; }

/* ── Hero section (landing page) ───────────────────── */
.hero {
  text-align: center;
  padding: 3rem 1rem;
}
.hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
.hero p  { font-size: 1.1rem; color: #ccc; max-width: 600px; margin: 0 auto 2rem; }

/* ── Demo grid ─────────────────────────────────────── */
.demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0 3rem;
}
.demo-grid .card { display: flex; flex-direction: column; }
.demo-grid .card p { flex: 1; }
.demo-grid .card a.btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: var(--primary);
  color: #fff;
  border-radius: var(--radius);
  text-align: center;
  font-weight: 600;
}
.demo-grid .card a.btn:hover { opacity: 0.85; text-decoration: none; }

/* ── Footer ────────────────────────────────────────── */
.site-footer {
  text-align: center;
  padding: 2rem 1rem;
  font-size: 0.85rem;
  color: #888;
  border-top: 1px solid var(--secondary);
  margin-top: 3rem;
}

/* ── Responsive ────────────────────────────────────── */
@media (max-width: 768px) {
  .hero h1 { font-size: 1.75rem; }
  .site-nav { gap: 0.75rem; }
  .controls { flex-direction: column; align-items: stretch; }
}
```

- [ ] **Verify:** Open `index.html` locally with the stylesheet linked. Background should be dark navy (`#1a1a2e`), text white-ish.

### 1.3 Landing Page

- [ ] **Replace `index.html` with the full landing page.** This adds nav, hero, demo grid, and footer.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Guitar Alchemist</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav class="site-nav">
    <span class="logo">Guitar Alchemist</span>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container">
    <section class="hero">
      <h1>Guitar Alchemist</h1>
      <p>Interactive music theory demos powered by VexFlow. Explore scales, chords, progressions, and the fretboard — right in your browser.</p>
    </section>

    <section class="demo-grid">
      <div class="card">
        <h3>Scale Explorer</h3>
        <p>Visualize any scale on the staff and fretboard. Hear it played back with adjustable tempo.</p>
        <a href="/demos/scales/" class="btn">Explore Scales</a>
      </div>
      <div class="card">
        <h3>Chord Viewer</h3>
        <p>See chord voicings in standard notation with interval labels and common guitar fingerings.</p>
        <a href="/demos/chords/" class="btn">View Chords</a>
      </div>
      <div class="card">
        <h3>Progression Player</h3>
        <p>Play common chord progressions with real-time notation highlighting and audio playback.</p>
        <a href="/demos/progressions/" class="btn">Play Progressions</a>
      </div>
      <div class="card">
        <h3>Circle of Fifths</h3>
        <p>Interactive circle showing key relationships, key signatures, and diatonic chords.</p>
        <a href="/demos/circle-of-fifths/" class="btn">Explore Circle</a>
      </div>
      <div class="card">
        <h3>Fretboard Visualizer</h3>
        <p>See notes, intervals, and scale degrees across the entire fretboard in any tuning.</p>
        <a href="/demos/fretboard/" class="btn">View Fretboard</a>
      </div>
      <div class="card">
        <h3>Show &amp; Tell Showcase</h3>
        <p>Archive of biweekly showcase discussions with links to live demos and documentation.</p>
        <a href="/showcase/" class="btn">View Showcase</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; Part of the <a href="https://github.com/GuitarAlchemist">GuitarAlchemist</a> ecosystem.</p>
  </footer>
</body>
</html>
```

- [ ] **Verify:** Open locally. Dark theme visible. Six cards in a responsive grid. Nav links present. Resize browser below 768px — cards should stack to single column.

### 1.4 VexFlow Renderer (`js/vexflow-renderer.js`)

- [ ] **Create `js/vexflow-renderer.js`.** This shared module provides the two Phase 1 functions: `renderScale()` and `renderChord()`. VexFlow must already be loaded via `<script>` tag before this file runs.

```js
/* vexflow-renderer.js — Shared VexFlow rendering utilities
 *
 * Depends on: VexFlow 4.x loaded globally via CDN
 * Usage:      renderScale('container-id', 'C', 'major');
 *             renderChord('container-id', 'C', 'maj7');
 */

// ── Music-theory data ────────────────────────────────
const SCALE_INTERVALS = {
  'major':            [0,2,4,5,7,9,11],
  'natural-minor':    [0,2,3,5,7,8,10],
  'harmonic-minor':   [0,2,3,5,7,8,11],
  'melodic-minor':    [0,2,3,5,7,9,11],
  'pentatonic-major': [0,2,4,7,9],
  'pentatonic-minor': [0,3,5,7,10],
  'blues':            [0,3,5,6,7,10],
  'dorian':           [0,2,3,5,7,9,10],
  'mixolydian':       [0,2,4,5,7,9,10],
  'lydian':           [0,2,4,6,7,9,11],
};

const NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];

const CHORD_INTERVALS = {
  'maj':     [0,4,7],
  'min':     [0,3,7],
  '7':       [0,4,7,10],
  'maj7':    [0,4,7,11],
  'min7':    [0,3,7,10],
  'dim':     [0,3,6],
  'aug':     [0,4,8],
  'sus2':    [0,2,7],
  'sus4':    [0,5,7],
  'add9':    [0,4,7,14],
  'maj7#11': [0,4,7,11,18],
};

// ── Helpers ──────────────────────────────────────────
function noteNameToMidi(name, octave) {
  const idx = NOTE_NAMES.indexOf(name.charAt(0).toUpperCase() +
    (name.length > 1 ? name.charAt(1) : ''));
  return idx + (octave + 1) * 12;
}

function midiToVexKey(midi) {
  const name = NOTE_NAMES[midi % 12];
  const octave = Math.floor(midi / 12) - 1;
  // VexFlow key format: "c/4", "c#/4"
  return name.toLowerCase() + '/' + octave;
}

function midiToNoteName(midi) {
  return NOTE_NAMES[midi % 12];
}

// ── Public API ───────────────────────────────────────

/**
 * Render a scale on a staff.
 * @param {string} containerId  — DOM element id
 * @param {string} root         — e.g. 'C', 'F#'
 * @param {string} scaleType    — key into SCALE_INTERVALS
 */
function renderScale(containerId, root, scaleType) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  const { Renderer, Stave, StaveNote, Voice, Formatter, Annotation } = Vex.Flow;

  const renderer = new Renderer(container, Renderer.Backends.SVG);
  const width = Math.min(container.clientWidth || 800, 900);
  renderer.resize(width, 180);
  const context = renderer.getContext();

  const intervals = SCALE_INTERVALS[scaleType];
  if (!intervals) return;

  const rootMidi = noteNameToMidi(root, 4);
  // Ascending + root octave above
  const midiNotes = intervals.map(i => rootMidi + i).concat([rootMidi + 12]);

  const stave = new Stave(10, 20, width - 30);
  stave.addClef('treble');
  stave.setContext(context).draw();

  const notes = midiNotes.map(m => {
    const sn = new StaveNote({ keys: [midiToVexKey(m)], duration: 'q' });
    // Add note-name annotation below
    sn.addModifier(
      new Annotation(midiToNoteName(m))
        .setVerticalJustification(Annotation.VerticalJustify.BOTTOM)
    );
    return sn;
  });

  const voice = new Voice({ num_beats: notes.length, beat_value: 4 });
  voice.setStrict(false);
  voice.addTickables(notes);

  new Formatter().joinVoices([voice]).format([voice], width - 80);
  voice.draw(context, stave);
}

/**
 * Render a chord on a staff.
 * @param {string} containerId
 * @param {string} root         — e.g. 'A', 'Bb'
 * @param {string} quality      — key into CHORD_INTERVALS
 */
function renderChord(containerId, root, quality) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  const { Renderer, Stave, StaveNote, Voice, Formatter, Annotation } = Vex.Flow;

  const renderer = new Renderer(container, Renderer.Backends.SVG);
  renderer.resize(300, 180);
  const context = renderer.getContext();

  const intervals = CHORD_INTERVALS[quality];
  if (!intervals) return;

  const rootMidi = noteNameToMidi(root, 4);
  const midiNotes = intervals.map(i => rootMidi + i);
  const keys = midiNotes.map(m => midiToVexKey(m));

  const stave = new Stave(10, 20, 260);
  stave.addClef('treble');
  stave.setContext(context).draw();

  const chord = new StaveNote({ keys, duration: 'w' });
  // Label with chord name
  chord.addModifier(
    new Annotation(root + quality)
      .setVerticalJustification(Annotation.VerticalJustify.TOP)
  );

  const voice = new Voice({ num_beats: 4, beat_value: 4 });
  voice.setStrict(false);
  voice.addTickables([chord]);

  new Formatter().joinVoices([voice]).format([voice], 200);
  voice.draw(context, stave);
}
```

- [ ] **Verify:** Will be tested via the Scale Explorer page in step 1.6.

### 1.5 Audio Engine (`js/audio-engine.js`)

- [ ] **Create `js/audio-engine.js`.** Provides `playNote()`, `playSequence()`, and `stopAll()` for Phase 1. `playChord()` is added in Phase 2.

```js
/* audio-engine.js — Web Audio API playback engine
 *
 * No dependencies. Uses the browser's native Web Audio API.
 *
 * Exports (global):
 *   playNote(frequency, duration, waveType)
 *   playChord(frequencies[], duration, strum?)
 *   playSequence(notes[], tempo)
 *   stopAll()
 */

let audioCtx = null;
const activeNodes = [];

function getCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  return audioCtx;
}

/**
 * Convert MIDI note number to frequency (Hz).
 * @param {number} midi
 * @returns {number}
 */
function midiToFreq(midi) {
  return 440 * Math.pow(2, (midi - 69) / 12);
}

/**
 * Play a single note.
 * @param {number} frequency — Hz
 * @param {number} duration  — seconds (default 0.5)
 * @param {string} waveType  — 'triangle' | 'sine' | 'square' | 'sawtooth' (default 'triangle')
 * @param {number} startTime — AudioContext time to start (default: now)
 */
function playNote(frequency, duration = 0.5, waveType = 'triangle', startTime = null) {
  const ctx = getCtx();
  const t = startTime || ctx.currentTime;

  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.type = waveType;
  osc.frequency.value = frequency;

  // ADSR envelope
  gain.gain.setValueAtTime(0, t);
  gain.gain.linearRampToValueAtTime(0.3, t + 0.02);            // attack
  gain.gain.linearRampToValueAtTime(0.21, t + 0.12);           // decay -> sustain 0.7*0.3
  gain.gain.setValueAtTime(0.21, t + duration - 0.3);
  gain.gain.linearRampToValueAtTime(0, t + duration);           // release

  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start(t);
  osc.stop(t + duration);
  activeNodes.push(osc);
}

/**
 * Play a chord (multiple notes at once, optionally strummed).
 * @param {number[]} frequencies — array of Hz values
 * @param {number}   duration    — seconds
 * @param {boolean}  strum       — stagger onsets by ~30ms (default false)
 */
function playChord(frequencies, duration = 1.0, strum = false) {
  const ctx = getCtx();
  const now = ctx.currentTime;
  frequencies.forEach((freq, i) => {
    const offset = strum ? i * 0.03 : 0;
    playNote(freq, duration, 'triangle', now + offset);
  });
}

/**
 * Play a sequence of MIDI notes at a given tempo.
 * @param {number[]} midiNotes — array of MIDI note numbers
 * @param {number}   tempo     — BPM (default 120)
 */
function playSequence(midiNotes, tempo = 120) {
  const ctx = getCtx();
  const beatDuration = 60 / tempo;
  const now = ctx.currentTime;
  midiNotes.forEach((midi, i) => {
    playNote(midiToFreq(midi), beatDuration * 0.9, 'triangle', now + i * beatDuration);
  });
}

/**
 * Stop all active oscillators.
 */
function stopAll() {
  activeNodes.forEach(node => {
    try { node.stop(); } catch (e) { /* already stopped */ }
  });
  activeNodes.length = 0;
}
```

- [ ] **Verify:** Will be tested via the Scale Explorer page in step 1.6.

### 1.6 Scale Explorer Demo (`demos/scales/index.html`)

- [ ] **Create `demos/scales/index.html`.** This is the first fully functional demo page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scale Explorer — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Scale Explorer</h1>

    <div class="card">
      <div class="controls">
        <label for="root-select">Root:</label>
        <select id="root-select">
          <option>C</option><option>C#</option><option>D</option><option>D#</option>
          <option>E</option><option>F</option><option>F#</option><option>G</option>
          <option>G#</option><option>A</option><option>A#</option><option>B</option>
        </select>

        <label for="scale-select">Scale:</label>
        <select id="scale-select">
          <option value="major">Major</option>
          <option value="natural-minor">Natural Minor</option>
          <option value="harmonic-minor">Harmonic Minor</option>
          <option value="melodic-minor">Melodic Minor</option>
          <option value="pentatonic-major">Pentatonic Major</option>
          <option value="pentatonic-minor">Pentatonic Minor</option>
          <option value="blues">Blues</option>
          <option value="dorian">Dorian</option>
          <option value="mixolydian">Mixolydian</option>
          <option value="lydian">Lydian</option>
        </select>

        <label for="tempo-range">Tempo:</label>
        <input type="range" id="tempo-range" min="60" max="200" value="120">
        <span id="tempo-display">120 BPM</span>

        <button id="play-btn">Play</button>
        <button id="stop-btn">Stop</button>
      </div>

      <div id="notation-output" class="vf-container"></div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/vexflow@4/build/cjs/vexflow.js"></script>
  <script src="/js/audio-engine.js"></script>
  <script src="/js/vexflow-renderer.js"></script>
  <script>
    const rootSel  = document.getElementById('root-select');
    const scaleSel = document.getElementById('scale-select');
    const tempoRange = document.getElementById('tempo-range');
    const tempoDisp  = document.getElementById('tempo-display');
    const playBtn  = document.getElementById('play-btn');
    const stopBtn  = document.getElementById('stop-btn');

    function update() {
      renderScale('notation-output', rootSel.value, scaleSel.value);
    }

    rootSel.addEventListener('change', update);
    scaleSel.addEventListener('change', update);
    tempoRange.addEventListener('input', () => {
      tempoDisp.textContent = tempoRange.value + ' BPM';
    });

    playBtn.addEventListener('click', () => {
      const root = rootSel.value;
      const scaleType = scaleSel.value;
      const intervals = SCALE_INTERVALS[scaleType];
      if (!intervals) return;
      const rootMidi = noteNameToMidi(root, 4);
      const midiNotes = intervals.map(i => rootMidi + i).concat([rootMidi + 12]);
      playSequence(midiNotes, parseInt(tempoRange.value));
    });

    stopBtn.addEventListener('click', stopAll);

    // Initial render
    update();
  </script>
</body>
</html>
```

- [ ] **Verify (browser):** Open `demos/scales/index.html` via a local HTTP server (e.g., `python -m http.server` from repo root).
  - Staff notation renders with C major scale (8 notes, ascending with octave).
  - Changing root or scale re-renders immediately.
  - "Play" button produces audible triangle-wave tones at the displayed tempo.
  - "Stop" button silences playback.
  - Note names appear below each note on the staff.
  - Page looks correct on mobile width (controls stack vertically).

---

## Phase 2: Core Demos

### 2.1 Extend VexFlow Renderer — `renderProgression()`

- [ ] **Add `renderProgression()` to `js/vexflow-renderer.js`.** Append the following function at the end of the file:

```js
/**
 * Render a chord progression across multiple measures.
 * @param {string}   containerId
 * @param {Array}    chords      — e.g. [{root:'C', quality:'maj'}, ...]
 * @param {number}   highlightIdx — index of chord to highlight (or -1)
 */
function renderProgression(containerId, chords, highlightIdx = -1) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  const { Renderer, Stave, StaveNote, Voice, Formatter, Annotation } = Vex.Flow;

  const width = Math.min(container.clientWidth || 800, 900);
  const renderer = new Renderer(container, Renderer.Backends.SVG);
  renderer.resize(width, 180);
  const context = renderer.getContext();

  const stave = new Stave(10, 20, width - 30);
  stave.addClef('treble');
  stave.setContext(context).draw();

  const notes = chords.map((ch, idx) => {
    const intervals = CHORD_INTERVALS[ch.quality] || [0,4,7];
    const rootMidi = noteNameToMidi(ch.root, 4);
    const keys = intervals.map(i => midiToVexKey(rootMidi + i));
    const sn = new StaveNote({ keys, duration: 'w' });
    if (idx === highlightIdx) {
      sn.setStyle({ fillStyle: '#ffd700', strokeStyle: '#ffd700' });
    }
    sn.addModifier(
      new Annotation(ch.root + ch.quality)
        .setVerticalJustification(Annotation.VerticalJustify.TOP)
    );
    return sn;
  });

  const voice = new Voice({ num_beats: chords.length * 4, beat_value: 4 });
  voice.setStrict(false);
  voice.addTickables(notes);

  new Formatter().joinVoices([voice]).format([voice], width - 80);
  voice.draw(context, stave);
}
```

- [ ] **Verify:** Will be tested via Progression Player (step 2.4).

### 2.2 Chord Voicing Viewer (`demos/chords/index.html`)

- [ ] **Create `demos/chords/index.html`.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chord Viewer — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Chord Viewer</h1>

    <div class="card">
      <div class="controls">
        <label for="chord-root">Root:</label>
        <select id="chord-root">
          <option>C</option><option>C#</option><option>D</option><option>D#</option>
          <option>E</option><option>F</option><option>F#</option><option>G</option>
          <option>G#</option><option>A</option><option>A#</option><option>B</option>
        </select>

        <label for="chord-quality">Quality:</label>
        <select id="chord-quality">
          <option value="maj">Major</option>
          <option value="min">Minor</option>
          <option value="7">Dominant 7</option>
          <option value="maj7">Major 7</option>
          <option value="min7">Minor 7</option>
          <option value="dim">Diminished</option>
          <option value="aug">Augmented</option>
          <option value="sus2">Sus2</option>
          <option value="sus4">Sus4</option>
          <option value="add9">Add9</option>
          <option value="maj7#11">Maj7#11</option>
        </select>

        <button id="strum-btn">Strum</button>
        <button id="block-btn">Block Chord</button>
      </div>

      <div id="chord-output" class="vf-container"></div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/vexflow@4/build/cjs/vexflow.js"></script>
  <script src="/js/audio-engine.js"></script>
  <script src="/js/vexflow-renderer.js"></script>
  <script>
    const rootSel = document.getElementById('chord-root');
    const qualSel = document.getElementById('chord-quality');
    const strumBtn = document.getElementById('strum-btn');
    const blockBtn = document.getElementById('block-btn');

    function update() {
      renderChord('chord-output', rootSel.value, qualSel.value);
    }

    function getFreqs() {
      const intervals = CHORD_INTERVALS[qualSel.value] || [0,4,7];
      const rootMidi = noteNameToMidi(rootSel.value, 4);
      return intervals.map(i => midiToFreq(rootMidi + i));
    }

    rootSel.addEventListener('change', update);
    qualSel.addEventListener('change', update);
    strumBtn.addEventListener('click', () => playChord(getFreqs(), 1.5, true));
    blockBtn.addEventListener('click', () => playChord(getFreqs(), 1.5, false));

    update();
  </script>
</body>
</html>
```

- [ ] **Verify (browser):**
  - Chord renders on staff with chord name annotation.
  - Changing root/quality re-renders.
  - "Strum" plays notes with staggered onset (~30ms apart).
  - "Block Chord" plays all notes simultaneously.

### 2.3 Fretboard Visualizer Library (`js/fretboard.js`)

- [ ] **Create `js/fretboard.js`.** SVG fretboard generator.

```js
/* fretboard.js — SVG fretboard diagram generator
 *
 * Draws an interactive guitar fretboard as SVG.
 * Exports (global): drawFretboard(containerId, options)
 */

const TUNINGS = {
  'standard':  [40, 45, 50, 55, 59, 64],   // E2 A2 D3 G3 B3 E4
  'drop-d':    [38, 45, 50, 55, 59, 64],   // D2 A2 D3 G3 B3 E4
  'open-g':    [38, 43, 50, 55, 59, 62],   // D2 G2 D3 G3 B3 D4
  'dadgad':    [38, 45, 50, 55, 57, 62],   // D2 A2 D3 G3 A3 D4
};

/**
 * Draw a fretboard SVG into the given container.
 * @param {string} containerId
 * @param {Object} opts
 * @param {string} opts.tuning       — key into TUNINGS (default 'standard')
 * @param {number} opts.frets        — number of frets to show (default 15)
 * @param {number[]} opts.highlights — MIDI note numbers to highlight
 * @param {string} opts.displayMode  — 'notes' | 'intervals' | 'degrees' (default 'notes')
 * @param {number} opts.rootMidi     — root note for interval/degree calculation
 */
function drawFretboard(containerId, opts = {}) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  const tuning    = TUNINGS[opts.tuning || 'standard'];
  const fretCount = opts.frets || 15;
  const highlights = new Set(opts.highlights || []);
  const displayMode = opts.displayMode || 'notes';
  const rootMidi  = opts.rootMidi ?? 0;

  const stringCount = tuning.length;
  const fretW = 60, stringH = 30;
  const padLeft = 40, padTop = 30;
  const width  = padLeft + (fretCount + 1) * fretW;
  const height = padTop + (stringCount + 1) * stringH;

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('width', '100%');
  svg.style.maxWidth = width + 'px';

  const INTERVAL_NAMES = ['R','b2','2','b3','3','4','b5','5','b6','6','b7','7'];

  // Draw fret lines
  for (let f = 0; f <= fretCount; f++) {
    const x = padLeft + f * fretW;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x); line.setAttribute('y1', padTop);
    line.setAttribute('x2', x); line.setAttribute('y2', padTop + (stringCount - 1) * stringH);
    line.setAttribute('stroke', f === 0 ? '#ccc' : '#555');
    line.setAttribute('stroke-width', f === 0 ? 4 : 1);
    svg.appendChild(line);
  }

  // Draw strings
  for (let s = 0; s < stringCount; s++) {
    const y = padTop + s * stringH;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', padLeft); line.setAttribute('y1', y);
    line.setAttribute('x2', padLeft + fretCount * fretW); line.setAttribute('y2', y);
    line.setAttribute('stroke', '#999');
    line.setAttribute('stroke-width', 1.5 - s * 0.1);
    svg.appendChild(line);
  }

  // Draw fret markers (dots at frets 3,5,7,9,12,15)
  [3,5,7,9,12,15].filter(f => f <= fretCount).forEach(f => {
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('cx', padLeft + (f - 0.5) * fretW);
    dot.setAttribute('cy', padTop + ((stringCount - 1) * stringH) / 2);
    dot.setAttribute('r', f === 12 ? 6 : 4);
    dot.setAttribute('fill', '#333');
    svg.appendChild(dot);
  });

  // Draw note dots for highlighted notes
  for (let s = 0; s < stringCount; s++) {
    for (let f = 0; f <= fretCount; f++) {
      const midi = tuning[stringCount - 1 - s] + f; // strings are high-to-low visually
      const noteClass = midi % 12;
      if (!highlights.has(noteClass)) continue;

      const cx = f === 0 ? padLeft - 15 : padLeft + (f - 0.5) * fretW;
      const cy = padTop + s * stringH;

      const isRoot = ((midi - rootMidi) % 12 + 12) % 12 === 0;
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', cx);
      circle.setAttribute('cy', cy);
      circle.setAttribute('r', 10);
      circle.setAttribute('fill', isRoot ? '#ffd700' : '#e94560');
      svg.appendChild(circle);

      let label = NOTE_NAMES[noteClass];
      if (displayMode === 'intervals') {
        label = INTERVAL_NAMES[((midi - rootMidi) % 12 + 12) % 12];
      } else if (displayMode === 'degrees') {
        label = INTERVAL_NAMES[((midi - rootMidi) % 12 + 12) % 12];
      }

      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', cx);
      text.setAttribute('y', cy + 4);
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('font-size', '9');
      text.setAttribute('fill', '#fff');
      text.setAttribute('font-family', 'sans-serif');
      text.textContent = label;
      svg.appendChild(text);
    }
  }

  container.appendChild(svg);
}
```

- [ ] **Verify:** Will be tested via the Fretboard demo page (step 2.5).

### 2.4 Chord Progression Player (`demos/progressions/index.html`)

- [ ] **Create `demos/progressions/index.html`.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Progression Player — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Chord Progression Player</h1>

    <div class="card">
      <div class="controls">
        <label for="key-select">Key:</label>
        <select id="key-select">
          <option>C</option><option>C#</option><option>D</option><option>D#</option>
          <option>E</option><option>F</option><option>F#</option><option>G</option>
          <option>G#</option><option>A</option><option>A#</option><option>B</option>
        </select>

        <label for="prog-select">Progression:</label>
        <select id="prog-select">
          <option value="pop">I - V - vi - IV (Pop)</option>
          <option value="jazz">ii - V - I (Jazz)</option>
          <option value="blues">I - IV - V (Blues)</option>
          <option value="emotional">vi - IV - I - V (Emotional)</option>
          <option value="fifties">I - vi - IV - V (50s)</option>
        </select>

        <label for="prog-tempo">Tempo:</label>
        <input type="range" id="prog-tempo" min="40" max="160" value="80">
        <span id="prog-tempo-display">80 BPM</span>

        <button id="prog-play">Play</button>
        <button id="prog-stop">Stop</button>
      </div>

      <div id="prog-output" class="vf-container"></div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/vexflow@4/build/cjs/vexflow.js"></script>
  <script src="/js/audio-engine.js"></script>
  <script src="/js/vexflow-renderer.js"></script>
  <script>
    // Progression definitions: scale degree offsets + qualities
    // Degrees relative to major scale: [0,2,4,5,7,9,11]
    const MAJOR_SCALE = [0,2,4,5,7,9,11];
    const PROG_DEFS = {
      'pop':       [{deg:0, q:'maj'},{deg:4, q:'maj'},{deg:5, q:'min'},{deg:3, q:'maj'}],
      'jazz':      [{deg:1, q:'min7'},{deg:4, q:'7'},{deg:0, q:'maj7'}],
      'blues':     [{deg:0, q:'7'},{deg:3, q:'7'},{deg:4, q:'7'}],
      'emotional': [{deg:5, q:'min'},{deg:3, q:'maj'},{deg:0, q:'maj'},{deg:4, q:'maj'}],
      'fifties':   [{deg:0, q:'maj'},{deg:5, q:'min'},{deg:3, q:'maj'},{deg:4, q:'maj'}],
    };

    const keySel   = document.getElementById('key-select');
    const progSel  = document.getElementById('prog-select');
    const tempoR   = document.getElementById('prog-tempo');
    const tempoD   = document.getElementById('prog-tempo-display');
    const playBtn  = document.getElementById('prog-play');
    const stopBtn  = document.getElementById('prog-stop');

    let playTimer = null;

    function getChords() {
      const keyRoot = NOTE_NAMES.indexOf(keySel.value);
      const def = PROG_DEFS[progSel.value];
      return def.map(d => {
        const midi = (keyRoot + MAJOR_SCALE[d.deg]) % 12;
        return { root: NOTE_NAMES[midi], quality: d.q };
      });
    }

    function update(highlightIdx) {
      renderProgression('prog-output', getChords(), highlightIdx ?? -1);
    }

    keySel.addEventListener('change', () => update());
    progSel.addEventListener('change', () => update());
    tempoR.addEventListener('input', () => {
      tempoD.textContent = tempoR.value + ' BPM';
    });

    playBtn.addEventListener('click', () => {
      stopPlayback();
      const chords = getChords();
      const bpm = parseInt(tempoR.value);
      const beatMs = (60 / bpm) * 4 * 1000; // whole-note duration in ms
      let idx = 0;

      function step() {
        update(idx);
        // Play chord audio
        const ch = chords[idx];
        const intervals = CHORD_INTERVALS[ch.quality] || [0,4,7];
        const rootMidi = noteNameToMidi(ch.root, 4);
        const freqs = intervals.map(i => midiToFreq(rootMidi + i));
        playChord(freqs, beatMs / 1000 * 0.9, true);
        idx = (idx + 1) % chords.length;
        playTimer = setTimeout(step, beatMs);
      }
      step();
    });

    stopBtn.addEventListener('click', stopPlayback);

    function stopPlayback() {
      if (playTimer) { clearTimeout(playTimer); playTimer = null; }
      stopAll();
      update();
    }

    update();
  </script>
</body>
</html>
```

- [ ] **Verify (browser):**
  - Progression renders as a series of whole-note chords with labels.
  - Changing key transposes all chord names correctly.
  - "Play" cycles through chords with the currently highlighted chord shown in gold.
  - Audio plays strummed chords in time.
  - "Stop" halts playback and clears the highlight.

### 2.5 Fretboard Visualizer Demo (`demos/fretboard/index.html`)

- [ ] **Create `demos/fretboard/index.html`.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fretboard Visualizer — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Fretboard Visualizer</h1>

    <div class="card">
      <div class="controls">
        <label for="fb-tuning">Tuning:</label>
        <select id="fb-tuning">
          <option value="standard">Standard (EADGBE)</option>
          <option value="drop-d">Drop D</option>
          <option value="open-g">Open G</option>
          <option value="dadgad">DADGAD</option>
        </select>

        <label for="fb-root">Root:</label>
        <select id="fb-root">
          <option>C</option><option>C#</option><option>D</option><option>D#</option>
          <option>E</option><option>F</option><option>F#</option><option>G</option>
          <option>G#</option><option>A</option><option>A#</option><option>B</option>
        </select>

        <label for="fb-scale">Pattern:</label>
        <select id="fb-scale">
          <option value="major">Major</option>
          <option value="natural-minor">Natural Minor</option>
          <option value="pentatonic-major">Pentatonic Major</option>
          <option value="pentatonic-minor">Pentatonic Minor</option>
          <option value="blues">Blues</option>
          <option value="dorian">Dorian</option>
          <option value="mixolydian">Mixolydian</option>
        </select>

        <label for="fb-display">Display:</label>
        <select id="fb-display">
          <option value="notes">Notes</option>
          <option value="intervals">Intervals</option>
          <option value="degrees">Degrees</option>
        </select>
      </div>

      <div id="fretboard-output" class="vf-container" style="overflow-x:auto;"></div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>

  <script src="/js/vexflow-renderer.js"></script>
  <script src="/js/fretboard.js"></script>
  <script>
    const tuningSel  = document.getElementById('fb-tuning');
    const rootSel    = document.getElementById('fb-root');
    const scaleSel   = document.getElementById('fb-scale');
    const displaySel = document.getElementById('fb-display');

    function update() {
      const rootIdx = NOTE_NAMES.indexOf(rootSel.value);
      const intervals = SCALE_INTERVALS[scaleSel.value] || [0,2,4,5,7,9,11];
      const highlights = intervals.map(i => (rootIdx + i) % 12);

      drawFretboard('fretboard-output', {
        tuning: tuningSel.value,
        highlights: highlights,
        displayMode: displaySel.value,
        rootMidi: rootIdx,
      });
    }

    [tuningSel, rootSel, scaleSel, displaySel].forEach(el =>
      el.addEventListener('change', update)
    );

    update();
  </script>
</body>
</html>
```

- [ ] **Verify (browser):**
  - Fretboard SVG renders with 15 frets and 6 strings.
  - Fret markers visible at frets 3, 5, 7, 9, 12, 15.
  - Scale notes highlighted: root in gold, other degrees in red.
  - Switching to "Intervals" display shows R, b3, 5, etc. instead of note names.
  - Changing tuning repositions the dots correctly.
  - Horizontal scrolling works on mobile widths.

---

## Phase 3: Circle of Fifths + Showcase

### 3.1 Circle of Fifths Demo (`demos/circle-of-fifths/index.html`)

- [ ] **Create `demos/circle-of-fifths/index.html`.** The circle is rendered as an SVG with click interaction. Clicking a key shows its key signature and diatonic chords via VexFlow.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Circle of Fifths — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
  <style>
    .cof-layout { display: flex; gap: 2rem; flex-wrap: wrap; align-items: flex-start; }
    .cof-circle { flex: 0 0 auto; }
    .cof-detail { flex: 1; min-width: 280px; }
    .cof-wedge { cursor: pointer; transition: opacity 0.15s; }
    .cof-wedge:hover { opacity: 0.8; }
    .cof-info h3 { margin-bottom: 0.5rem; }
    .cof-info p  { color: #ccc; margin-bottom: 0.5rem; }
  </style>
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Circle of Fifths</h1>

    <div class="card cof-layout">
      <div class="cof-circle" id="cof-svg"></div>

      <div class="cof-detail">
        <div class="cof-info" id="cof-info">
          <h3 id="cof-key-name">Click a key to explore</h3>
          <p id="cof-key-sig"></p>
        </div>
        <div id="cof-notation" class="vf-container"></div>
        <div id="cof-diatonic" style="margin-top:1rem;">
          <h4>Diatonic Chords</h4>
          <p id="cof-chords-list" style="color:#ccc;font-family:monospace;"></p>
        </div>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/vexflow@4/build/cjs/vexflow.js"></script>
  <script src="/js/vexflow-renderer.js"></script>
  <script>
    // Circle of fifths order
    const COF_MAJOR = ['C','G','D','A','E','B','F#','Db','Ab','Eb','Bb','F'];
    const COF_MINOR = ['Am','Em','Bm','F#m','C#m','G#m','D#m','Bbm','Fm','Cm','Gm','Dm'];
    const SHARPS_FLATS = [0,1,2,3,4,5,6,-5,-4,-3,-2,-1]; // sharps (+) or flats (-)

    // Diatonic chord qualities for major keys
    const DIATONIC_Q = ['maj','min','min','maj','maj','min','dim'];
    const DEGREE_LABELS = ['I','ii','iii','IV','V','vi','vii°'];
    const MAJOR_INTERVALS = [0,2,4,5,7,9,11];

    const size = 340, cx = size/2, cy = size/2;
    const outerR = 150, innerR = 100, labelR = 125, minorR = 80;

    function buildCircleSVG() {
      const el = document.getElementById('cof-svg');
      const ns = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(ns, 'svg');
      svg.setAttribute('viewBox', `0 0 ${size} ${size}`);
      svg.setAttribute('width', size);
      svg.setAttribute('height', size);

      // Background circle
      const bg = document.createElementNS(ns, 'circle');
      bg.setAttribute('cx', cx); bg.setAttribute('cy', cy);
      bg.setAttribute('r', outerR); bg.setAttribute('fill', '#16213e');
      svg.appendChild(bg);

      const innerBg = document.createElementNS(ns, 'circle');
      innerBg.setAttribute('cx', cx); innerBg.setAttribute('cy', cy);
      innerBg.setAttribute('r', innerR); innerBg.setAttribute('fill', '#0f3460');
      svg.appendChild(innerBg);

      for (let i = 0; i < 12; i++) {
        const angle = (i * 30 - 90) * Math.PI / 180;

        // Major key label (outer ring)
        const tx = cx + labelR * Math.cos(angle);
        const ty = cy + labelR * Math.sin(angle);
        const text = document.createElementNS(ns, 'text');
        text.setAttribute('x', tx); text.setAttribute('y', ty + 5);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '14'); text.setAttribute('font-weight', '600');
        text.setAttribute('fill', '#eee');
        text.setAttribute('cursor', 'pointer');
        text.setAttribute('data-index', i);
        text.textContent = COF_MAJOR[i];
        text.addEventListener('click', () => selectKey(i));
        svg.appendChild(text);

        // Minor key label (inner ring)
        const mx = cx + minorR * Math.cos(angle);
        const my = cy + minorR * Math.sin(angle);
        const mtext = document.createElementNS(ns, 'text');
        mtext.setAttribute('x', mx); mtext.setAttribute('y', my + 4);
        mtext.setAttribute('text-anchor', 'middle');
        mtext.setAttribute('font-size', '10');
        mtext.setAttribute('fill', '#aaa');
        mtext.textContent = COF_MINOR[i];
        svg.appendChild(mtext);

        // Divider lines
        const a1 = ((i - 0.5) * 30 - 90) * Math.PI / 180;
        const line = document.createElementNS(ns, 'line');
        line.setAttribute('x1', cx + innerR * Math.cos(a1));
        line.setAttribute('y1', cy + innerR * Math.sin(a1));
        line.setAttribute('x2', cx + outerR * Math.cos(a1));
        line.setAttribute('y2', cy + outerR * Math.sin(a1));
        line.setAttribute('stroke', '#333'); line.setAttribute('stroke-width', 1);
        svg.appendChild(line);
      }

      el.appendChild(svg);
    }

    function selectKey(index) {
      const key = COF_MAJOR[index];
      const sf = SHARPS_FLATS[index];
      const sigText = sf === 0 ? 'No sharps or flats'
        : sf > 0 ? sf + ' sharp' + (sf > 1 ? 's' : '')
        : Math.abs(sf) + ' flat' + (Math.abs(sf) > 1 ? 's' : '');

      document.getElementById('cof-key-name').textContent = key + ' Major / ' + COF_MINOR[index];
      document.getElementById('cof-key-sig').textContent = 'Key signature: ' + sigText;

      // Render the scale
      // Map COF key name to NOTE_NAMES-compatible name
      const rootMap = {'Db':'C#','Ab':'G#','Eb':'D#','Bb':'A#','F#':'F#'};
      const root = rootMap[key] || key;
      renderScale('cof-notation', root, 'major');

      // Show diatonic chords
      const rootIdx = NOTE_NAMES.indexOf(root);
      const chords = MAJOR_INTERVALS.map((interval, deg) => {
        const noteName = NOTE_NAMES[(rootIdx + interval) % 12];
        return DEGREE_LABELS[deg] + ': ' + noteName + DIATONIC_Q[deg];
      });
      document.getElementById('cof-chords-list').textContent = chords.join('   ');
    }

    buildCircleSVG();
  </script>
</body>
</html>
```

- [ ] **Verify (browser):**
  - Circle renders with 12 major keys in the outer ring and 12 relative minors in the inner ring.
  - Clicking a key name updates the detail panel: key name, signature description, scale on staff, and diatonic chords.
  - Layout wraps on narrow screens (circle stacks above detail).

### 3.2 Showcase Archive Page (`showcase/index.html`)

- [ ] **Create `showcase/index.html`.** Static archive page linking Show & Tell topics to demos and discussions.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Show &amp; Tell Showcase — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container" style="padding-top:2rem;">
    <h1>Show &amp; Tell Showcase</h1>
    <p style="color:#ccc; margin-bottom:2rem;">
      Biweekly showcase discussions exploring music theory, AI governance, and the Guitar Alchemist ecosystem.
      Music topics link to interactive demos you can try right now.
    </p>

    <section class="demo-grid">
      <!-- Music-focused topics — link to demos -->
      <div class="card">
        <h3>Guitar Mathematics</h3>
        <p>How 2^(1/12) defines fret spacing, tuning ratios, and the geometry of the fretboard.</p>
        <a href="/demos/fretboard/" class="btn">Try Fretboard Demo</a>
      </div>

      <div class="card">
        <h3>Chord Progressions</h3>
        <p>Common patterns (I-V-vi-IV, ii-V-I) and why they work — hear them played back in any key.</p>
        <a href="/demos/progressions/" class="btn">Try Progression Player</a>
      </div>

      <div class="card">
        <h3>Circle of Fifths</h3>
        <p>The master map of key relationships — explore key signatures and diatonic chords interactively.</p>
        <a href="/demos/circle-of-fifths/" class="btn">Try Circle of Fifths</a>
      </div>

      <div class="card">
        <h3>OPTIC-K Embeddings</h3>
        <p>Representing chords and voicings as vectors — see how chord qualities map to intervals.</p>
        <a href="/demos/chords/" class="btn">Try Chord Viewer</a>
      </div>

      <!-- Governance / AI topics — link to Demerzel docs -->
      <div class="card">
        <h3>AI Governance (Asimov's Laws)</h3>
        <p>How the Zeroth Law and constitutional hierarchy keep AI agents aligned.</p>
        <a href="https://github.com/GuitarAlchemist/Demerzel" class="btn" target="_blank">View Governance Docs</a>
      </div>

      <div class="card">
        <h3>Multi-Agent Teams</h3>
        <p>How Demerzel, TARS, ix, and GA collaborate through the Galactic Protocol.</p>
        <a href="https://github.com/GuitarAlchemist/Demerzel" class="btn" target="_blank">View Architecture</a>
      </div>

      <div class="card">
        <h3>Neuro-Symbolic AI (TARS)</h3>
        <p>Combining neural embeddings with symbolic reasoning for music theory understanding.</p>
        <a href="https://github.com/GuitarAlchemist/tars" class="btn" target="_blank">View TARS</a>
      </div>

      <div class="card">
        <h3>Meta-Compounding</h3>
        <p>How every interaction compounds — continuous improvement through kaizen and knowledge states.</p>
        <a href="https://github.com/GuitarAlchemist/Demerzel" class="btn" target="_blank">View Compounding Docs</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>
</body>
</html>
```

- [ ] **Verify (browser):**
  - 8 cards render in a grid.
  - Music topics (first 4) link to local demo pages.
  - Governance topics (last 4) link to GitHub repos in new tabs.

### 3.3 Update Show & Tell Workflow

- [ ] **Update `demerzel-showcase.yml` in the Demerzel repo.** Add a "Try it live" footer link to discussion posts for music-related topics (indices 0, 2, 4, 7). The exact edit depends on the current workflow file structure, but the change is: for topics at indices 0, 2, 4, and 7, append a line to the discussion body:

```
**Try it live:** [Interactive Demo](https://guitaralchemist.github.io/demos/...)
```

Map:
  - Topic 0 (Guitar Mathematics) -> `https://guitaralchemist.github.io/demos/fretboard/`
  - Topic 2 (Chord Progressions) -> `https://guitaralchemist.github.io/demos/progressions/`
  - Topic 4 (Circle of Fifths) -> `https://guitaralchemist.github.io/demos/circle-of-fifths/`
  - Topic 7 (OPTIC-K Embeddings) -> `https://guitaralchemist.github.io/demos/chords/`

- [ ] **Verify:** Review the workflow diff. Confirm the demo links are correct for the topic indices.

---

## Phase 4: Polish

### 4.1 Responsive Pass

- [ ] **Test every page at three widths** (use browser DevTools responsive mode):
  - **Mobile (375px):** Nav wraps, controls stack vertically, cards single-column, fretboard scrolls horizontally.
  - **Tablet (768px):** Cards 2-column, controls side-by-side where space allows.
  - **Desktop (1200px):** Full layout, max-width container centered.

- [ ] **Fix any layout issues found.** Common fixes to check for:
  - VexFlow SVG overflowing its container on mobile (fix: `overflow-x: auto` on `.vf-container`).
  - Circle of Fifths SVG too large on mobile (fix: set `max-width: 100%` on the SVG).
  - Touch targets smaller than 44x44px (fix: increase padding on buttons/selects).

- [ ] **Add a hamburger menu for mobile nav** (optional enhancement). If the nav links overflow on very narrow screens, add a toggle button that shows/hides `.nav-links` on mobile. Implementation:

  Add to `css/style.css`:
  ```css
  .nav-toggle { display: none; background: none; border: none; color: var(--text); font-size: 1.5rem; cursor: pointer; min-height: 44px; }
  @media (max-width: 768px) {
    .nav-toggle { display: block; }
    .nav-links { display: none; width: 100%; }
    .nav-links.open { display: flex; flex-direction: column; }
  }
  ```

  Add a `<button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">&#9776;</button>` before `.nav-links` in each page's nav.

- [ ] **Verify:** Resize browser across breakpoints. All pages readable and interactive at each size.

### 4.2 Cross-Browser Testing

- [ ] **Test in Chrome, Firefox, and Edge** (all support VexFlow 4, Web Audio API, and modern CSS). For each browser, verify:
  - VexFlow SVGs render correctly.
  - Audio playback works (click play, hear sound).
  - CSS grid/flexbox layout is correct.
  - Circle of Fifths click interaction works.
  - Fretboard SVG renders with correct dot positions.

- [ ] **Test in Safari** (if available). Known consideration: Web Audio API requires a user gesture to start. Ensure the play buttons create the `AudioContext` on first click (already handled by lazy init in `audio-engine.js`).

- [ ] **Fix any browser-specific issues found.** Document any unfixable issues as known limitations in a comment at the top of the affected JS file.

### 4.3 Performance Optimization

- [ ] **Lazy-load VexFlow on demo pages only.** The landing page and showcase page do not need VexFlow. Verify that only pages in `demos/` include the VexFlow CDN `<script>` tag. (This is already the case if the plan was followed — the landing page and showcase page do not include VexFlow.)

- [ ] **Add `defer` attribute to script tags** where possible. For scripts that do not need to run before DOM is ready, add `defer`:
  ```html
  <script defer src="/js/audio-engine.js"></script>
  <script defer src="/js/vexflow-renderer.js"></script>
  ```
  Note: The VexFlow CDN script must load before `vexflow-renderer.js`, so ordering matters. Using `defer` preserves order.

- [ ] **Verify:** Open Chrome DevTools Network tab. Confirm VexFlow (~300KB) only loads on demo pages, not on the landing page or showcase page.

### 4.4 Custom 404 Page

- [ ] **Create `404.html` at the repo root.**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Not Found — Guitar Alchemist</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <a class="logo" href="/">Guitar Alchemist</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="/demos/scales/">Scales</a>
      <a href="/demos/chords/">Chords</a>
      <a href="/demos/progressions/">Progressions</a>
      <a href="/demos/circle-of-fifths/">Circle of Fifths</a>
      <a href="/demos/fretboard/">Fretboard</a>
      <a href="/showcase/">Showcase</a>
      <a href="https://github.com/GuitarAlchemist" target="_blank">GitHub</a>
    </div>
  </nav>

  <main class="container">
    <section class="hero">
      <h1>404 — Lost in the Circle of Fifths</h1>
      <p>The page you are looking for does not exist. Perhaps it modulated to a different key.</p>
      <a href="/" class="btn" style="display:inline-block;padding:0.75rem 1.5rem;background:var(--primary);color:#fff;border-radius:var(--radius);font-weight:600;margin-top:1rem;">Back to Home</a>
    </section>
  </main>

  <footer class="site-footer">
    <p>Guitar Alchemist &mdash; <a href="https://github.com/GuitarAlchemist">GitHub</a></p>
  </footer>
</body>
</html>
```

- [ ] **Verify:** Navigate to a non-existent URL (e.g., `https://guitaralchemist.github.io/nope`). GitHub Pages should serve the custom 404 page with navigation back to home.

### 4.5 Final Smoke Test

- [ ] **Walk through every page** on the deployed site and confirm:
  - Landing page: 6 cards visible, all links work.
  - Scale Explorer: renders, plays, stops, all 10 scale types work.
  - Chord Viewer: renders, strum and block play, all 11 qualities work.
  - Progression Player: renders, plays with highlight, stops, all 5 presets work in all 12 keys.
  - Circle of Fifths: all 12 keys clickable, detail updates, scale renders.
  - Fretboard: all 4 tunings render, all display modes work, dots positioned correctly.
  - Showcase: 8 cards, 4 link to demos, 4 link to GitHub.
  - 404: renders with back-to-home link.
  - Mobile: spot-check 2-3 pages at 375px width.
