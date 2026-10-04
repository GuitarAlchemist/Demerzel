---
module_id: vc-001-accessible-fretboard-paths
department: visual-computing
course: One Fretboard, Three Access Paths
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-04-001
version: "0.1.0"
---

# One Fretboard, Three Access Paths

> **Department of Visual Computing** | Level: Beginner | Estimated duration: 35 minutes | Status: review pending

## Objectives

After this lesson, you will be able to:

- describe a guitar position independently of its drawn marker;
- distinguish an informative diagram from an interactive control;
- give pointer, keyboard, and screen-reader users equivalent access to a position's information and available action;
- design checks that can reveal differences among SVG, Canvas, and 3D render modes.

## The project question and fixed fixture

Can a guitarist use a GA fretboard diagram to find a position and, where the diagram offers selection, activate it with a pointer, keyboard, or screen reader? The [shared GA `GuitarFretboard` component at commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx) draws an SVG marker for each position. A marker has mouse-enter, mouse-leave, and click handlers. The inspected marker has no keyboard activation or explicit accessible name, role, and focus target. The [Canvas renderer](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx) attaches pointer events to Pixi graphics. The [render-mode wrapper](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx) forwards position callbacks to its SVG, Canvas, and 3D branches.

This is a source inspection, not a completed browser or assistive-technology audit. The [GA voicing card](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx) uses the shared diagram without a position-click callback; that use is informative rather than a selection control. Do not announce an action where none exists.

Use this two-position fixture throughout the lesson with standard tuning. GA's position model uses zero-based string indexes, high E first. In the user-facing description, call them strings 1 and 2.

| GA position | User-facing description | Expected note |
|---|---|---|
| `{ string: 0, fret: 3, label: "G" }` | String 1 (high E), fret 3, G | G |
| `{ string: 1, fret: 1, label: "C" }` | String 2 (B), fret 1, C | C |

### Practice exercise

The SVG prints only `G` inside the first marker. What does that label omit, and why does the zero-based `string: 0` value need translation?

> **Answer:** `G` omits the string and fret, so it cannot identify this position by itself. The data index is 0, but a guitarist's string number is 1; expose "String 1, fret 3, G" rather than "String 0".

## 1. Keep a position model outside the renderer

A position should have one source of truth: instrument and tuning context, string, fret, note label when known, and whether selection is available. SVG circles, Pixi graphics, and 3D objects are views of that position. A text representation should derive from the same data, not from pixel coordinates or a separate hand-written caption. Otherwise a capo, left-handed view, tuning change, or hidden label can make the accessible description disagree with the picture.

For this fixture, a compact representation is: "Standard tuning. Two marked positions: string 1, fret 3, G; string 2, fret 1, C." A neighboring list can provide one item per position. If clicking a position selects it, each item needs an actual control that performs the same selection. If the diagram only illustrates a voicing, the items can be ordinary text. The [W3C non-text content guidance](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) supports conveying the purpose and information of a graphic through a text alternative; a short label alone cannot encode every position.

### Practice exercise

A developer adds `aria-label="Guitar fretboard"` to the SVG. Can a nonvisual reader identify the two marked positions from that label alone?

> **Answer:** No. It names the graphic but does not convey string, fret, or note for either position. Add a synchronized description or structured list, and expose any available selection controls.

## 2. Match the action to the diagram's purpose

When a marker calls `onPositionClick`, the user must be able to perform that selection through a keyboard interface as well. [WCAG 2.2 Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) concerns the functionality, so the keyboard path can be a nearby list of native buttons rather than the SVG circles themselves. Each button can be named "Select string 1, fret 3, G" and can invoke the same selection handler as the pointer marker. A visible focus indicator and an announced selected state belong in the acceptance check. Native buttons already support Tab, Enter, and Space; a custom grid should be introduced only if its focus and arrow-key behavior are fully implemented and tested against the [WAI-ARIA grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/).

The [GA SVG code](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx) makes every marker look pointer-clickable even when the callback is absent. In an informative voicing card, a control label such as "Select" would be misleading. The lesson's acceptance criterion is equivalent *available* behavior, not a promise that all diagrams are editable.

### Practice exercise

For an interactive version of the fixture, write two keyboard-accessible control names and say what Enter should do. Then state what changes for the read-only voicing card.

> **Answer:** "Select string 1, fret 3, G" and "Select string 2, fret 1, C" are suitable button names. Enter activates the same position callback as a pointer click. In the read-only card, present position descriptions without selection buttons or an invented selected state.

## 3. Give controls names and state

For a custom control, [WCAG 2.2 Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) requires a programmatically determinable name and role, plus relevant state. A circle with `onClick` is only a drawing node with an event handler; a visible `G` label does not necessarily tell assistive technology that the marker is actionable or which fret it represents. The safest small design is an HTML button list adjacent to the visual renderer. If selection persists, expose the chosen position in visible text and in the control state or an appropriate status announcement. Avoid announcing a hover-only highlight as selection.

Use the same wording in SVG, Canvas, and 3D views. Canvas pixels and 3D meshes do not by themselves provide a navigable text inventory of marked positions. A shared list also survives switching render modes. This is a proposed design for GA, not a claim that the current implementation contains it.

### Practice exercise

A screen reader announces "G" for a circle, while a pointer user sees it on the high E string at fret 3. Which information and control semantics are missing?

> **Answer:** The announcement needs at least the string and fret, plus the note in context. If the marker selects a position, the user also needs an actionable role, keyboard path, and any selected state. If it only illustrates a voicing, describe it as information without an action role.

## 4. Test all paths against the same facts

Create one test fixture with the two positions above and run it in every supported render mode. For an interactive variant, click the first marker, focus and activate its corresponding button with Enter and Space, and compare the resulting selected position. Check that a screen reader exposes the two complete names and any selected state. For a read-only variant, verify that both positions remain readable and that no fake controls are announced. Repeat after changing render mode, and check that focus remains predictable rather than disappearing into a replaced canvas. A browser accessibility-tree assertion is useful but does not replace a manual assistive-technology pass.

The [inspected Playwright file](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts) checks rendering and console errors; it does not establish this three-path behavior. Record the browser, screen reader, render mode, and observed result before claiming the behavior works. An accessibility fix is complete only when its interactions are actually exercised.

### Practice exercise

Your test can find the SVG and sees no console errors. Can you mark VC-001's acceptance criterion as passed? Name the missing observations.

> **Answer:** No. Verify the position descriptions, pointer selection where available, keyboard selection, names and state exposed to a screen reader, and consistency after switching to Canvas or 3D. Record any unsupported mode or untested assistive-technology combination.

## Key takeaways

- A position's musical meaning must remain available independently of pixels.
- Read-only diagrams need complete information; interactive diagrams also need equivalent keyboard action and control semantics.
- One shared position model can keep SVG, Canvas, 3D, and text representations consistent.
- Static code inspection identifies a risk; browser and assistive-technology checks establish behavior.

## Further reading and project evidence

- GA, [shared SVG fretboard](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx), [Canvas renderer](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx), [render-mode wrapper](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx), [voicing card](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx), and [Playwright checks](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts), pinned to commit `dc2e74c`.
- W3C, [Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html), [Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html), and [Grid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/).

*Research: `visual-computing-2026-10-04-001`. Subject review, localization review, and live assistive-technology testing are pending; do not present this draft as a verified course.*
