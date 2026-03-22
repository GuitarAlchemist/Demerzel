# Governance Dashboard — Status and Roadmap

**Date:** 2026-03-23
**Related issues:** #159 (architecture navigator), #103 (ix CLI), Rust dashboard (deferred)

---

## Current State: D3.js Dashboard Live

The primary governance dashboard is a D3.js compounding visualization deployed to GitHub Pages:

**URL:** https://guitaralchemist.github.io/demos/compounding/

It is part of the `ga-client` gh-pages demos and visualizes the compounding metrics that drive Demerzel's governance cycles — belief state evolution, cycle effectiveness, and compounding dimension (D_c). The dashboard is live and accessible without any build toolchain.

---

## Architecture Navigator — Specced (#159)

The architecture navigator spec (`docs/superpowers/specs/2026-03-24-architecture-navigator-design.md`) defines an interactive D3.js graph of the full Demerzel + ix + tars + ga ecosystem. It will show:

- All repos as nodes, with governance relationships as edges
- Live CI/health status per node (fetched from GitHub API)
- Clickable artifact drill-down (policies, personas, pipelines)
- Tetravalent belief states as node color overlays (T=green, F=red, U=grey, C=amber)

The navigator is the richer, ecosystem-wide complement to the compounding dashboard. It is specced and ready to build; it does not depend on the ix CLI.

---

## ix Rust Dashboard — Deferred

The original "Rust Governance Dashboard App (ix)" board item envisioned a native Rust TUI or web server running inside ix to render governance state. This has been deferred for the following reasons:

1. **D3.js dashboard already covers the primary use case.** Live visualization is available at the gh-pages URL above. A Rust reimplementation would duplicate functionality without adding governance value.

2. **ix CLI (#103) must come first.** The ix CLI is the foundation for all ix runtime capabilities, including any dashboard server. Building a dashboard before the CLI exists would require a separate binary with no shared infrastructure.

3. **Architecture navigator (#159) is a better investment.** The navigator covers the ecosystem-wide view that a Rust dashboard would target, and it can be built with D3.js without waiting for ix CLI.

**Decision:** ix Rust dashboard deferred until after ix CLI (#103) ships. At that point, the CLI's `--serve` flag (specced in `docs/superpowers/specs/2026-03-24-ix-cli-design.md`) can expose governance metrics over HTTP and feed the architecture navigator directly.

---

## Summary

| Dashboard | Status | Location |
|---|---|---|
| D3.js compounding dashboard | Live | guitaralchemist.github.io/demos/compounding/ |
| Architecture navigator | Specced (#159) | Pending build |
| ix Rust dashboard | Deferred | After ix CLI (#103) |
