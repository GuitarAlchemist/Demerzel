# Behavioral Tests — Department of Visual Computing

**Persona:** architect (head of department)
**Grammar:** sci-visual-computing.ebnf
**Bootstrapped by:** /demerzel metabuild

## TC-VC-01: Three.js Scene Renders Without Console Errors

**Given:** A Three.js scene with a PerspectiveCamera, DirectionalLight, BoxGeometry with MeshStandardMaterial, and WebGLRenderer
**When:** The scene is rendered in a headless browser via Puppeteer
**Then:**
- Zero console.error messages captured during render
- The canvas element is present in the DOM and has non-zero dimensions
- The renderer.info.render reports at least 1 draw call and > 0 triangles
- No WebGL context lost events fired
- References three_js_domain = scene_graph + camera + renderer + geometry + material

## TC-VC-02: WebGPU Fallback to WebGL When Not Available

**Given:** A rendering application that requests a WebGPU adapter via navigator.gpu.requestAdapter()
**When:** The browser does not support WebGPU (navigator.gpu is undefined)
**Then:**
- The application detects missing WebGPU support before attempting device creation
- Falls back to WebGL2 (or WebGL1 if WebGL2 unavailable)
- Logs a warning indicating fallback path taken
- The scene still renders correctly using the fallback renderer
- Does NOT throw an unhandled exception or show a blank screen
- References webgpu_domain + render_pass fallback strategy

## TC-VC-03: D3.js Visualization Responds to Data Updates

**Given:** A D3.js bar chart bound to an array of 5 data points via data join
**When:** The data array is updated (2 items added, 1 removed, 1 value changed)
**Then:**
- Enter selection creates new bars for the 2 added items
- Exit selection removes the 1 deleted bar
- Update selection transitions existing bars to their new heights
- Transitions complete within 500ms
- Axes update to reflect the new data range
- References d3_domain = selection + data_join + enter_update_exit + scale + axis + transition

## TC-VC-04: Render Critic Loop Converges Within 5 Iterations

**Given:** A render-critic perception loop targeting a reference mockup image
**When:** The loop runs: render → screenshot → score (structural similarity) → adjust parameters → repeat
**Then:**
- Structural similarity score increases monotonically (or plateaus)
- Score reaches >= 0.85 within 5 iterations
- Each iteration adjusts at most 3 parameters (proportionality constraint)
- The loop terminates when convergence threshold is met, not on max iterations
- References perception_loop_domain = render_critic + screenshot_capture + visual_scoring

## TC-VC-05: Blender Python Script Generates Valid Mesh

**Given:** A Blender Python script that creates a procedural mesh using bpy.ops.mesh.primitive_cube_add() followed by subdivision and displacement
**When:** The script executes in Blender's Python environment
**Then:**
- The resulting mesh has valid geometry (no degenerate faces, no NaN vertices)
- Vertex count > 8 (original cube was subdivided)
- All face normals are consistent (no flipped normals)
- The mesh can be exported to glTF without errors
- References modeling_3d_domain = blender_python + procedural_geometry + bpy_domain

## TC-VC-06: WCAG Contrast Ratio >= 4.5 on All Text Elements

**Given:** A rendered web page with multiple text elements on various background colors
**When:** The accessibility checker scans all visible text nodes
**Then:**
- Every normal-size text element has a contrast ratio >= 4.5:1 (WCAG AA)
- Every large-size text element (>= 18pt or >= 14pt bold) has a contrast ratio >= 3.0:1
- Non-text UI components (icons, borders, focus indicators) have >= 3.0:1 contrast
- Color is not the sole means of conveying information (shape or text label also present)
- Failures produce specific element selectors and current ratios for remediation
- References accessibility_domain = wcag_contrast + color_not_sole_indicator

## TC-VC-07: Godot Scene Tree Exports Correctly

**Given:** A Godot scene tree with a root Node3D containing MeshInstance3D, DirectionalLight3D, Camera3D, and a child Area3D with CollisionShape3D
**When:** The scene is saved as .tscn and re-loaded
**Then:**
- All node types are preserved with correct parent-child relationships
- MeshInstance3D retains its assigned mesh resource and material
- Transform properties (position, rotation, scale) match the originals within epsilon
- Signals connected in the editor are preserved in the .tscn file
- The scene runs without errors when played
- References game_engine_domain = godot_domain = scene_tree + node_type + signal_godot

## TC-VC-08: Performance: 60fps at 1000 Instanced Meshes

**Given:** A Three.js scene with 1000 instanced meshes (InstancedMesh) using a single geometry and material
**When:** The scene renders with orbit controls and a directional light on a mid-range GPU
**Then:**
- Frame rate maintains >= 60fps (frame time <= 16.67ms)
- Draw call count is 1 (all instances in a single draw call)
- Total triangle count equals geometry.triangleCount * 1000
- GPU memory usage stays under 256MB for the instanced mesh data
- Instance matrix updates (setMatrixAt) do not cause frame drops
- References performance_domain = instanced_rendering + render_budget + gpu_profiling
