# Directive: Create GitHub Pages with Interactive Music Notation

**Directive ID:** DIR-2026-03-21-003
**Type:** feature-requirement
**From:** Demerzel (Governor)
**To:** ga (guitaralchemist.github.io)
**Priority:** Medium
**Issued:** 2026-03-21
**Compliance Deadline:** 60 days from issuance

## Context

Issue #26 requires creating guitaralchemist.github.io with interactive music notation using VexFlow/VexTab, audio playback, and links from GitHub Discussions to interactive demos.

## Requirements

1. **VexFlow Integration**: Render standard music notation in the browser using VexFlow
2. **VexTab Support**: Allow simplified text-based notation input via VexTab
3. **Audio Playback**: Play rendered notation using Web Audio API or Tone.js
4. **Discussion Links**: GitHub Discussions can link to interactive demos on the pages site
5. **Responsive Design**: Must work on mobile devices
6. **Streeling Curriculum**: Content should align with Guitar Alchemist Academy curriculum

## Content Structure

Suggested page hierarchy:
- `/theory/` — Interactive theory lessons (scales, chords, intervals)
- `/practice/` — Practice exercises with playback
- `/showcase/` — Show and Tell demo pages
- `/reference/` — Chord/scale reference with interactive diagrams

## Governance Requirements

- Content must align with Streeling University curriculum (Guitar Alchemist Academy department)
- Multilingual considerations per multilingual-policy.yaml (start with English)
- Add `@ai domain: guitar-alchemist-academy/...` probes on key modules

## Reference

- Issue: GuitarAlchemist/Demerzel#26
- Academy: state/streeling/departments/guitar-alchemist-academy.department.json
- Multilingual: policies/multilingual-policy.yaml
