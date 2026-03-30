# Demerzel 3D Face — Blender Rig to Godot Pipeline

Design spec for replacing the procedural Three.js holographic face with a proper rigged 3D face model, driven by the same emotional system.

## Current State

`DemerzelFace.ts` is a procedural Three.js face with:
- 5 emotions: `calm`, `concerned`, `thinking`, `pleased`, `alert`
- 8 parametric axes: browRaise, browTilt, mouthCurve, mouthOpen, eyeWiden, pupilDilate, headTiltX, headTiltZ
- Holographic shader (gold wireframe, scanlines, Fresnel glow, flicker)
- Auto-cycling emotions every 8-14s, smooth 1-2s transitions
- Eye tracking (iris follows camera), blinking (2.5-6.5s intervals), breathing
- Speaking mode (rapid mouth open/close)

## Target Architecture

```
Blender (.blend)          Godot 4 (.tscn)              React (Prime Radiant)
┌──────────────┐         ┌──────────────────┐         ┌──────────────────────┐
│ Vincent head │  glTF   │ demerzel_face.gd │  post   │ GodotScene.tsx       │
│ + shape keys │ ──.glb──│ + expression     │  Msg    │ + GodotBridge        │
│ + android    │         │   system         │ ◄──────►│ + emotion commands   │
│   materials  │         │ + idle anims     │  iframe │ + speaking state     │
└──────────────┘         └──────────────────┘         └──────────────────────┘
```

## Phase 1: Blender Model

### Base Model
**Three.js facecap model** — MIT-licensed face mesh with 52 ARKit-compatible blend shapes.
Source: `three.js/examples/models/gltf/facecap.glb` (332KB, ~27K vertices).

This model ships with the full ARKit blend shape set, making it compatible with
facial motion capture, MediaPipe face tracking, and programmatic expression control.

### ARKit Blend Shapes (52 total)

The model includes the complete ARKit set:
- **Brows**: `browInnerUp`, `browDown_L/R`, `browOuterUp_L/R`
- **Eyes**: `eyeBlink_L/R`, `eyeSquint_L/R`, `eyeWide_L/R`, `eyeLookUp/Down/In/Out_L/R`
- **Cheeks**: `cheekPuff`, `cheekSquint_L/R`
- **Nose**: `noseSneer_L/R`
- **Jaw**: `jawOpen`, `jawForward`, `jawLeft`, `jawRight`
- **Mouth**: `mouthSmile_L/R`, `mouthFrown_L/R`, `mouthFunnel`, `mouthPucker`, `mouthLeft/Right`, `mouthRollUpper/Lower`, `mouthShrugUpper/Lower`, `mouthClose`, `mouthDimple_L/R`, `mouthUpperUp_L/R`, `mouthLowerDown_L/R`, `mouthPress_L/R`, `mouthStretch_L/R`
- **Tongue**: `tongueOut`

### Future: Android Reskin in Blender
- Import the facecap.glb into Blender
- Replace skin materials with brushed titanium/synthetic (metallic=0.8, roughness=0.3)
- Add seam lines at jaw, temples, forehead (edge loops + bevel)
- Subtle amber emission along seams (Demerzel's gold accent `#d4a017`)
- Re-export as .glb — blend shapes transfer automatically

## Phase 2: Godot Integration

### Scene Structure
```
DemerzelFace (Node3D)
├── Camera3D (front-facing, for standalone use)
├── DirectionalLight3D (subtle rim light)
├── FaceMesh (MeshInstance3D — imported .glb)
└── AnimationPlayer (idle, blink, speak cycles)
```

### GDScript: `demerzel_face.gd`

```gdscript
extends Node3D

signal emotion_changed(emotion: String)

# ── Shape key index cache ──
var _shape_indices: Dictionary = {}
var _face_mesh: MeshInstance3D

# ── Emotion system (mirrors DemerzelFace.ts) ──
enum Emotion { CALM, CONCERNED, THINKING, PLEASED, ALERT }

var _current_emotion: Emotion = Emotion.CALM
var _target_weights: Dictionary = {}    # shape_name → float
var _current_weights: Dictionary = {}   # lerped values
var _blend_speed: float = 3.0           # weight/sec

# ── Idle behaviors ──
var _blink_timer: float = 0.0
var _next_blink: float = 4.0
var _emotion_timer: float = 0.0
var _next_emotion_change: float = 10.0
var _is_speaking: bool = false
var _speak_phase: float = 0.0

# ── Expression presets ──
const EXPRESSIONS = {
    Emotion.CALM: {
        "BrowRaiseL": 0.0, "BrowRaiseR": 0.0,
        "Smile": 0.1, "Frown": 0.0,
        "JawOpen": 0.0,
        "EyeWideL": 0.0, "EyeWideR": 0.0,
    },
    Emotion.CONCERNED: {
        "BrowRaiseL": 0.3, "BrowRaiseR": 0.3,
        "BrowTiltInner": 0.4,
        "Frown": 0.2, "JawOpen": 0.1,
        "EyeWideL": 0.2, "EyeWideR": 0.2,
    },
    Emotion.THINKING: {
        "BrowRaiseL": 0.2, "BrowTiltInner": 0.2,
        "EyeSquintL": 0.2, "EyeSquintR": 0.2,
    },
    Emotion.PLEASED: {
        "BrowRaiseL": 0.15, "BrowRaiseR": 0.15,
        "Smile": 0.5, "JawOpen": 0.1,
    },
    Emotion.ALERT: {
        "BrowRaiseL": 0.5, "BrowRaiseR": 0.5,
        "Frown": 0.1, "JawOpen": 0.2,
        "EyeWideL": 0.4, "EyeWideR": 0.4,
    },
}

func _ready() -> void:
    _face_mesh = $FaceMesh
    _cache_shape_indices()
    _set_emotion(Emotion.CALM)
    _next_blink = randf_range(2.5, 6.5)
    _next_emotion_change = randf_range(8.0, 14.0)

func _cache_shape_indices() -> void:
    var mesh = _face_mesh.mesh
    for i in range(mesh.get_blend_shape_count()):
        var name = mesh.get_blend_shape_name(i)
        _shape_indices[name] = i
        _current_weights[name] = 0.0

func _process(delta: float) -> void:
    _update_expression_blend(delta)
    _update_blink(delta)
    _update_speaking(delta)
    _update_auto_emotion(delta)

func _update_expression_blend(delta: float) -> void:
    for shape_name in _shape_indices:
        var target = _target_weights.get(shape_name, 0.0)
        var current = _current_weights.get(shape_name, 0.0)
        if absf(current - target) > 0.001:
            current = lerp(current, target, delta * _blend_speed)
            _current_weights[shape_name] = current
            _face_mesh.set_blend_shape_value(
                _shape_indices[shape_name], current
            )

func _update_blink(delta: float) -> void:
    _blink_timer += delta
    if _blink_timer >= _next_blink:
        _blink_timer = 0.0
        _next_blink = randf_range(2.5, 6.5)
        _do_blink()

func _do_blink() -> void:
    var tween = create_tween()
    for side in ["BlinkL", "BlinkR"]:
        if side in _shape_indices:
            tween.tween_method(
                func(val): _face_mesh.set_blend_shape_value(
                    _shape_indices[side], val),
                0.0, 1.0, 0.075
            )
            tween.tween_method(
                func(val): _face_mesh.set_blend_shape_value(
                    _shape_indices[side], val),
                1.0, 0.0, 0.075
            )

func _update_speaking(delta: float) -> void:
    if not _is_speaking:
        return
    _speak_phase += delta * 12.0
    var jaw_val = abs(sin(_speak_phase)) * 0.4
    if "JawOpen" in _shape_indices:
        _face_mesh.set_blend_shape_value(
            _shape_indices["JawOpen"], jaw_val
        )

func _update_auto_emotion(delta: float) -> void:
    _emotion_timer += delta
    if _emotion_timer >= _next_emotion_change:
        _emotion_timer = 0.0
        _next_emotion_change = randf_range(8.0, 14.0)
        var emotions = Emotion.values()
        _set_emotion(emotions[randi() % emotions.size()])

func _set_emotion(emotion: Emotion) -> void:
    _current_emotion = emotion
    _target_weights = {}
    # Reset all to 0
    for name in _shape_indices:
        _target_weights[name] = 0.0
    # Apply preset
    var preset = EXPRESSIONS.get(emotion, {})
    for name in preset:
        _target_weights[name] = preset[name]
    emit_signal("emotion_changed", Emotion.keys()[emotion])

# ── Public API (called from web bridge) ──

func set_emotion_by_name(name: String) -> void:
    match name.to_lower():
        "calm": _set_emotion(Emotion.CALM)
        "concerned": _set_emotion(Emotion.CONCERNED)
        "thinking": _set_emotion(Emotion.THINKING)
        "pleased": _set_emotion(Emotion.PLEASED)
        "alert": _set_emotion(Emotion.ALERT)

func set_speaking(speaking: bool) -> void:
    _is_speaking = speaking
    if not speaking and "JawOpen" in _shape_indices:
        _face_mesh.set_blend_shape_value(_shape_indices["JawOpen"], 0.0)
```

### Web Bridge Messages

Extend the existing `governance:*` protocol:

```
React → Godot:
{ type: "demerzel:emotion", emotion: "pleased" }
{ type: "demerzel:speaking", speaking: true }

Godot → React:
{ type: "demerzel:emotion-changed", emotion: "thinking" }
```

Add to `prime_radiant.gd` message handler:
```gdscript
"demerzel:emotion":
    $DemerzelFace.set_emotion_by_name(msg.emotion)
"demerzel:speaking":
    $DemerzelFace.set_speaking(msg.speaking)
```

## Phase 3: React Integration

### Bridge Extension in `GodotBridge.ts`

Add new event types:
```typescript
| 'demerzel-set-emotion'    // React → Godot
| 'demerzel-set-speaking'   // React → Godot
| 'demerzel-emotion-changed' // Godot → React
```

### Expression Control from ForceRadiant

```typescript
// Drive Demerzel's face from governance events
function handleAlgedonicSignal(signal: AlgedonicSignal) {
  if (signal.type === 'pain') {
    postToGodot({ type: 'demerzel:emotion', emotion: 'concerned' });
  } else {
    postToGodot({ type: 'demerzel:emotion', emotion: 'pleased' });
  }
}

// Speaking during LLM responses
function onChatStreamStart() {
  postToGodot({ type: 'demerzel:speaking', speaking: true });
}
function onChatStreamEnd() {
  postToGodot({ type: 'demerzel:speaking', speaking: false });
}
```

## Phase 4: Holographic Shader (Optional)

Preserve the current gold holographic aesthetic by applying a custom Godot shader:

```gdscript
# demerzel_holo.gdshader
shader_type spatial;
render_mode blend_add, unshaded, cull_back;

uniform vec4 base_color : source_color = vec4(1.0, 0.84, 0.0, 0.7); // #FFD700
uniform float scanline_density : hint_range(50, 500) = 200.0;
uniform float fresnel_power : hint_range(1, 8) = 3.0;
uniform float time_scale : hint_range(0.1, 2.0) = 0.5;

void fragment() {
    // Fresnel edge glow
    float fresnel = pow(1.0 - dot(NORMAL, VIEW), fresnel_power);

    // Scanlines
    float scan = sin(SCREEN_UV.y * scanline_density + TIME * time_scale * 20.0) * 0.5 + 0.5;
    scan = mix(0.6, 1.0, scan);

    // Flicker
    float flicker = step(0.92, fract(sin(TIME * 43.0) * 4357.0)) * 0.7;

    ALBEDO = base_color.rgb;
    ALPHA = base_color.a * scan * (1.0 - flicker) * (0.4 + fresnel * 0.6);
    EMISSION = base_color.rgb * (0.5 + fresnel);
}
```

Apply as `ShaderMaterial` on the face mesh to keep the holographic look while using proper 3D geometry + blend shapes.

## Web Export Performance Budget

| Metric | Target |
|--------|--------|
| Vertex count | < 10K |
| Shape keys | 15 |
| Texture size | 512x512 max |
| Draw calls | 1-2 (face + eyes) |
| Update frequency | On emotion change + 60fps blink/speak |
| .glb file size | < 2MB |

## Migration Path

1. **Phase 1**: Download Vincent, create android variant in Blender, export .glb
2. **Phase 2**: Import into Godot project, create `demerzel_face.gd` with expression system
3. **Phase 3**: Wire up web bridge messages, connect to React emotion triggers
4. **Phase 4**: Apply holographic shader for visual continuity
5. **Cutover**: Render Godot face in the existing GodotScene iframe; Three.js `DemerzelFace.ts` becomes fallback for non-Godot mode

## File Locations

```
ga-godot/
├── assets/models/demerzel_face.glb      (exported from Blender)
├── scenes/demerzel_face.tscn            (Godot scene)
├── scripts/demerzel_face.gd             (expression controller)
└── shaders/demerzel_holo.gdshader       (holographic material)

Blender source (not in repo, stored separately):
  demerzel_face.blend                     (Vincent-derived android head)
```
