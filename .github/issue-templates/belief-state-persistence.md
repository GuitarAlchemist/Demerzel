## Belief State Persistence Required

This repo does not have a `state/` directory for governance belief persistence per the [Galactic Protocol](https://github.com/GuitarAlchemist/Demerzel/blob/master/contracts/galactic-protocol.md).

### Directory Structure
```
state/
  beliefs/       — tetravalent belief states (*.belief.json)
  pdca/          — PDCA cycle tracking (*.pdca.json)
  knowledge/     — knowledge transfer records (*.knowledge.json)
  snapshots/     — belief snapshots for reconnaissance (*.snapshot.json)
```

### Setup
Copy the [state directory template](https://github.com/GuitarAlchemist/Demerzel/tree/master/templates/state) to this repo.

### File Naming
`{date}-{short-description}.{type}.json`

*Created by Demerzel governance auto-scan*
