# Lunar Lander Seamless Scene Integration

**Date:** 2026-03-28
**Status:** Design
**Scope:** Prime Radiant (ga-react-components)
**Affected files:** `SolarSystem.ts`, `LunarLanderEngine.ts`, `ForceRadiant.tsx`, `LunarLander.tsx`

## Problem

Double-clicking the Moon in the Prime Radiant solar system currently opens a fullscreen React overlay (`LunarLander.tsx`) that instantiates a completely separate `LunarLanderEngine` with its own `THREE.WebGLRenderer`, `THREE.Scene`, and `THREE.PerspectiveCamera`. The transition is jarring — a black panel appears over the governance graph. The user wants to fly from the solar system view directly down to the lunar surface within the same Three.js scene, with no overlay, no iframe, no second renderer.

## Current Architecture

### Solar System (`SolarSystem.ts`)
- `createSolarSystem(scale)` returns a `THREE.Group` added to the ForceGraph3D scene.
- Scale factor is `0.15` — everything is tiny relative to the governance graph.
- Earth: radius `0.35 * 0.15 = 0.0525` scene units. Moon: radius `0.1 * 0.15 = 0.015` scene units.
- Moon mesh sits inside `orbit-moon` group, which is a child of `orbit-earth`, which is a child of the solar system group.
- Moon orbits at distance `1.0 * 0.15 = 0.15` from Earth center.
- `updateSolarSystem()` animates orbital rotation each frame.

### Lunar Lander Engine (`LunarLanderEngine.ts`)
- Self-contained class: creates its own renderer, scene, camera, OrbitControls.
- Terrain: `PlaneGeometry(2000, 2000, 256, 256)` — 2000m across, sculpted with fbm + craters, flattened landing zone at origin.
- LM starts at altitude 500m, terrain is at y=0 (roughly).
- Physics: 1.625 m/s^2 gravity, 120Hz fixed timestep.
- Camera modes: ORBIT, CHASE, COCKPIT, SURFACE.
- Builds its own starfield, Earth globe, directional light, particle systems.
- All geometry is in real-ish meters.

### ForceRadiant (`ForceRadiant.tsx`)
- Main component. Uses `3d-force-graph` which owns the renderer/scene/camera.
- Access via `fg.scene()`, `fg.camera()`, `fg.renderer()`.
- Solar system group added to `fg.scene()`.
- Double-click Moon: `setActivePanel('lunar')` which renders `<LunarLander open={true} />` as a fullscreen overlay with its own engine.

## Scale Challenge

This is the central difficulty. The Moon in the solar system is radius `0.015` scene units. The lander terrain is `2000` units across. That is a ratio of roughly **133,000:1**.

Three approaches, in order of preference:

### Option A: Scale-Space Transition (Recommended)

Use a **nested group with progressive rescaling**. The terrain + LM exist as children of the Moon's orbit group, but at a local scale that maps lunar meters into the Moon's scene-unit bubble.

- Define a `lunarSurfaceGroup` added as a child of `orbit-moon`, positioned at the Moon mesh center.
- The group's scale is set so that `2000 lunar meters = ~0.03 scene units` (Moon diameter). That means `group.scale.set(s, s, s)` where `s = 0.03 / 2000 = 0.000015`.
- At solar system zoom, this group is invisible (sub-pixel). Only when the camera is extremely close does it resolve.
- During descent, the camera near/far planes are adjusted dynamically to handle the extreme scale.
- The Moon's spherical mesh fades out (opacity -> 0) as the camera enters the surface zone, replaced by the flat terrain patch.

**Pros:** Single scene graph, no teleportation, mathematically clean parent-child transform.
**Cons:** Floating-point precision at scale 0.000015 — terrain vertex positions may jitter. Mitigated by keeping the terrain centered at origin of its local group.

### Option B: Camera Teleport with Crossfade

- Keep terrain at a separate location in the scene (e.g., offset by 10000 units on Z).
- When descending, animate a crossfade: fade out solar system, fly camera to the terrain zone, fade in.
- Feels like a warp, not a continuous fly-down. Less immersive but avoids precision issues entirely.

### Option C: Dynamic Rescale on Enter

- When entering lunar mode, rescale the entire solar system group to `0` (hide it) and rescale the terrain to fill the scene.
- Reverse on exit. Camera position is remapped mathematically.
- Avoids precision issues but solar system disappears. Cannot look up and see Earth from the surface.

**Decision: Option A** with a fallback to Option B if floating-point precision proves unworkable. Option A is tested first because Three.js uses Float32 for positions but the local-space transform means terrain vertices stay near origin in their own coordinate frame.

## Detailed Design

### 1. New Class: `LunarLanderSceneMode`

A mode controller that plugs into ForceRadiant's existing scene/camera/renderer. Not a standalone engine.

```
class LunarLanderSceneMode {
  // Receives ForceGraph's shared resources — does NOT create its own
  constructor(config: {
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    renderer: THREE.WebGLRenderer;
    moonOrbitGroup: THREE.Group;       // orbit-moon from SolarSystem
    moonMesh: THREE.Mesh;              // the Moon sphere
    onStateChange: (state: LanderState) => void;
    onLanded: (success: boolean, stats: LanderStats) => void;
  })

  // Lifecycle
  enter(): Promise<void>    // build terrain, animate camera descent
  exit(): Promise<void>     // fly camera back out, dispose terrain
  update(dt: number): void  // called each frame from ForceRadiant's animation loop
  dispose(): void           // full cleanup

  // Input delegation
  handleKeyDown(e: KeyboardEvent): void
  handleKeyUp(e: KeyboardEvent): void

  // State
  readonly active: boolean
  readonly phase: 'entering' | 'flying' | 'landed' | 'crashed' | 'exiting'
}
```

### 2. Terrain + LM as Moon Children

On `enter()`:

1. **Create `lunarSurfaceGroup`** — a `THREE.Group` added as a child of the Moon's orbit group, at the Moon mesh's local position.
2. **Compute local scale**: `LUNAR_SURFACE_SCALE = moonRadius / (TERRAIN_SIZE / 2)` where `moonRadius = 0.1 * 0.15 = 0.015` and `TERRAIN_SIZE = 2000`. Result: `0.015 / 1000 = 0.000015`.
3. **Set** `lunarSurfaceGroup.scale.set(LUNAR_SURFACE_SCALE, LUNAR_SURFACE_SCALE, LUNAR_SURFACE_SCALE)`.
4. **Build terrain geometry** inside this group — same fbm + crater algorithm from `LunarLanderEngine.buildTerrain()`, same 2000x2000 plane. In local coordinates, everything is at the same scale as the existing engine (meters). The group transform handles the mapping.
5. **Build LM geometry** inside this group — same `buildLunarModule()` logic.
6. **Build particles** inside this group — exhaust, dust, RCS jets.
7. **Build surface lighting** — a directional light added to the group (sunlight direction derived from the Sun's world position).
8. **Fade out Moon sphere mesh** — animate opacity to 0, or swap to transparent material. The terrain now represents the surface.

On `exit()`:

1. Fly camera back up (reverse of descent).
2. Fade Moon mesh back in.
3. Remove and dispose `lunarSurfaceGroup` and all children.
4. Restore camera near/far to solar system defaults.

### 3. Camera Transition Sequence

The camera transition has three phases:

**Phase 1: Approach (2-3 seconds)**
- Starting point: current camera position (wherever the user is in the solar system/graph view).
- Target: a point ~5 Moon radii from Moon center, looking at the Moon.
- Technique: cubic ease-in-out interpolation of camera position and lookAt target.
- During this phase, freeze solar system orbital animation so the Moon does not drift.
- Disable ForceGraph3D orbit controls.

**Phase 2: Descent (3-5 seconds)**
- Camera moves from 5 Moon radii to ~0.5 Moon radii from surface.
- Progressively adjust `camera.near` from `0.01` down to `0.000001` and `camera.far` from `10000` down to `0.1` — matching the shrinking scale.
- Moon mesh fades out, terrain fades in.
- Camera rotation gradually shifts from "looking at Moon sphere" to "looking down at terrain."
- At the end, camera is positioned at the LM's starting altitude (500m in local coords = 500 * 0.000015 = 0.0075 scene units above surface).

**Phase 3: Handoff**
- Camera control transfers to `LunarLanderSceneMode`.
- Camera mode starts as ORBIT (same as current engine default).
- HUD overlay appears (React components, same as current `LunarLander.tsx` but positioned as overlay, not fullscreen takeover).
- Input mode switches to lander controls.
- Game state transitions to `'flying'`.

**Near/Far Plane Management:**
This is critical. At lunar surface scale, the camera near plane must be extremely small (in scene units). Recommended approach:
- Store original near/far on enter.
- During descent, lerp `camera.near` and `camera.far` logarithmically.
- At surface level: `near = 0.0000001`, `far = 0.05` (enough to see terrain extent in scene units).
- On exit, restore original values.

### 4. Input Mode Switching

ForceRadiant currently has these input consumers:
- ForceGraph3D orbit controls (trackball rotation, zoom)
- Solar system click/double-click handlers
- Panel keyboard shortcuts

When lander mode is active:

| Input | Solar System Mode | Lander Mode |
|-------|------------------|-------------|
| WASD / Arrows | Not used | Pitch/Roll RCS |
| Shift / Ctrl | Not used | Throttle up/down |
| Space | Not used | Start engine |
| C | Not used | Cycle camera |
| Escape | Close panel | Exit lander mode |
| Mouse drag | OrbitControls rotate | Disabled (camera follows LM) |
| Scroll | OrbitControls zoom | Disabled |

Implementation:
- `ForceRadiant` tracks a `sceneMode: 'graph' | 'lunar'` state.
- When `sceneMode === 'lunar'`:
  - Disable `fg.controls()` (the ForceGraph3D OrbitControls).
  - Route keyboard events to `LunarLanderSceneMode.handleKeyDown/Up`.
  - Suppress solar system mouse handlers.
- When exiting, re-enable everything.

### 5. Rendering: Shared Everything

| Resource | Current (overlay) | Proposed (integrated) |
|----------|------------------|----------------------|
| Renderer | LunarLanderEngine creates its own | Use `fg.renderer()` |
| Scene | LunarLanderEngine creates its own | Use `fg.scene()` — terrain is a child of Moon orbit group |
| Camera | LunarLanderEngine creates its own | Use `fg.camera()` |
| OrbitControls | LunarLanderEngine creates its own | Disabled; camera controlled by LunarLanderSceneMode |
| Animation loop | LunarLanderEngine has its own `requestAnimationFrame` | ForceRadiant calls `lunarMode.update(dt)` in its existing frame loop |
| Canvas | Separate canvas in overlay div | Same canvas — already rendering |

The existing `LunarLanderEngine` class is NOT reused directly. Instead, its geometry-building methods (`buildTerrain`, `buildLunarModule`, `buildParticleSystems`) and physics logic (`physicsStep`) are extracted into the new `LunarLanderSceneMode` class. The engine's renderer/scene/camera/controls creation is stripped out.

### 6. Performance: Lazy Load + Dispose

**Loading strategy:**
- Terrain geometry (256x256 = 65K vertices) is built only when entering lunar mode. Not preloaded.
- LM geometry (~50 meshes in the group) built on enter.
- Particle systems (exhaust: 120 points, dust: 250, RCS: 30 each) created on enter.
- Total additional draw calls: ~60. Manageable.

**Disposal strategy:**
- On exit, all terrain/LM/particle geometry and materials are disposed.
- `lunarSurfaceGroup` is removed from the Moon orbit group.
- GPU memory returns to pre-entry levels.

**LOD consideration:**
- While approaching (Phase 1-2), the terrain could start at lower resolution (64x64) and swap to full (256x256) when close. But 65K vertices is small — probably not worth the complexity. Skip LOD for v1.

**Frame budget impact:**
- During lander mode, the governance graph nodes are still rendering but the camera is zoomed into the Moon — most graph nodes are culled by frustum. Performance should be similar to the current standalone engine.
- Solar system orbital animation can be paused during lander mode to save CPU.

### 7. What Gets Extracted from `LunarLanderEngine`

Methods to port into `LunarLanderSceneMode` (logic only, no renderer/scene creation):

| Method | What changes |
|--------|-------------|
| `buildTerrain()` | Adds to `lunarSurfaceGroup` instead of `this.scene` |
| `buildLunarModule()` | Same — adds to surface group |
| `buildParticleSystems()` | Same — adds to surface group |
| `buildLighting()` | Adds directional light to surface group; ambient from solar system suffices |
| `buildStarfield()` | **Removed** — solar system skybox already has stars |
| `buildEarth()` | **Removed** — real Earth is visible in the solar system |
| `physicsStep()` | Unchanged — operates in local (meter) coordinates |
| `updateCamera()` | Adapted: writes to shared camera, positions in world space via `lunarSurfaceGroup.localToWorld()` |
| `tickParticles()` | Unchanged — particles are in local coords |
| Audio system | Ported as-is |
| `dispose()` | Simplified — only disposes what it created, not renderer/scene |

### 8. React Integration

```
// ForceRadiant.tsx — changes

// State
const [sceneMode, setSceneMode] = useState<'graph' | 'lunar'>('graph');
const lunarModeRef = useRef<LunarLanderSceneMode | null>(null);

// Double-click Moon handler (replaces setActivePanel('lunar'))
if (currentHoveredPlanet === 'moon') {
  const moonOrbit = solarSystem.getObjectByName('orbit-moon');
  const moonMesh = solarSystem.getObjectByName('moon');
  lunarModeRef.current = new LunarLanderSceneMode({
    scene: fg.scene(),
    camera: fg.camera(),
    renderer: fg.renderer(),
    moonOrbitGroup: moonOrbit,
    moonMesh: moonMesh,
    onStateChange: setLanderState,
    onLanded: handleLanded,
  });
  lunarModeRef.current.enter();
  setSceneMode('lunar');
}

// In the ForceRadiant animation loop (extraRenderers or d3AlphaDecay callback):
if (lunarModeRef.current?.active) {
  lunarModeRef.current.update(dt);
}

// HUD overlay — same React components from LunarLander.tsx,
// but rendered as a transparent overlay, not a fullscreen panel.
{sceneMode === 'lunar' && <LunarHUD state={landerState} />}
```

The `<LunarLander>` overlay component and `LunarLanderEngine` class remain in the codebase for now (deprecation, not deletion) until the integrated mode is proven stable.

### 9. Edge Cases

- **Moon drifts during descent**: Freeze `updateSolarSystem` orbital animation while in lander mode. The Moon's world position must not change or the camera transition breaks.
- **Graph forces still running**: ForceGraph3D simulation (`d3Force`) continues. Node positions may shift. This is fine — the camera is zoomed in on the Moon, graph is off-screen.
- **Resize during lander mode**: `LunarLanderSceneMode` must handle resize events (camera aspect ratio update). The renderer resize is already handled by ForceRadiant.
- **Returning from lander**: Camera must fly back to approximately where it was before descent. Store pre-descent camera position/target.
- **Floating point precision**: If terrain vertices jitter due to the `0.000015` scale, mitigate by temporarily repositioning the entire solar system group so the Moon is at world origin during lander mode, then restoring on exit. This keeps all active geometry near origin where float32 precision is best.

### 10. Implementation Order

1. **Extract physics + geometry builders** from `LunarLanderEngine` into pure functions (no side effects on a private scene/renderer). This is a refactor of the existing file.
2. **Create `LunarLanderSceneMode`** class using extracted functions. Test by manually calling `enter()` with the ForceRadiant scene.
3. **Implement camera transition** (Phases 1-3). Test with hardcoded camera path first, then smooth interpolation.
4. **Wire input switching** in ForceRadiant. Test keyboard routing.
5. **Build HUD overlay** as standalone React component (extract from `LunarLander.tsx`).
6. **Float32 precision testing** — fly to surface, check for vertex jitter. If unacceptable, implement the "reposition to origin" mitigation.
7. **Polish**: fade transitions, audio handoff, "look up and see Earth" from surface.
8. **Deprecate** `LunarLander.tsx` overlay and direct `LunarLanderEngine` usage.

### 11. Open Questions

- **Should the governance graph fade out during lander mode?** It is off-screen anyway (camera is at the Moon). Hiding it would save draw calls but adds visual complexity on enter/exit.
- **Multiplayer potential?** If two users are viewing Prime Radiant, one enters lander mode — does the other see the LM on the Moon? Out of scope for v1 but the architecture (terrain as scene child) supports it.
- **Skybox**: ForceRadiant has a nebula skybox. The lander engine uses pure black + starfield. Should the skybox change during descent? Probably yes — fade to black sky with stars, matching the lunar environment.
