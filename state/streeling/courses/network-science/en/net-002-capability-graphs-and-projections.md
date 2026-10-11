---
module_id: net-002-capability-graphs-and-projections
department: network-science
course: "Network Science for AI Ecosystems"
level: early-intermediate
prerequisites: [net-001-scale-free-tool-networks]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-002
version: "0.1.0"
---

# A Capability Catalog Is Not a Collaboration Graph

> **Department of Network Science** | Level: Early intermediate | Estimated duration: 30 minutes | Status: English draft; review and publication pending

## Objectives

After this lesson, you will be able to:

- Build a two-type graph from Demerzel's declared repo-to-tool-family catalog.
- Project that graph onto repos using an explicit edge rule and count its components.
- Explain why a catalog edge, a contract dependency, and an observed tool call are different evidence.
- Test the effect of removing one label without presenting it as a real service outage.

## The project question

A coordinator wants GA chord analysis and TARS grammar weighting in one workflow. Demerzel's [capability registry](../../../../../schemas/capability-registry.json) names tools for both repos. Does that catalog prove the two tools can be called in sequence through a working cross-repo handoff? **No.** It is a discovery index. We can build a graph of its declared labels and learn where descriptions overlap, but the graph does not encode an API contract, credentials, successful invocation, or current service presence.

This lesson uses only the registry at Demerzel commit `5c4967454ddc740ed937c87719ca4d71a3522e4b` (registry version `1.1.0`) and the [cross-repo contract note](../../../../../docs/architecture/cross-repo-contracts.md) at the same revision. The numbers below were recomputed from the pinned JSON. [NET-001](net-001-scale-free-tool-networks.md) introduces network degree, hubs, and the limits of a scale-free claim. Here the task is different: **choose what an edge means before counting it**. No live MCP endpoint was queried for this lesson.

## 1. Build the declared two-type graph

Open the JSON `repos` object. Its three repo keys are `ix`, `tars`, and `ga`. Under each, `tools` maps **family names** to arrays of named tools. Make a two-type, undirected graph: one node type is a repo, the other is an exact family-name string. Draw one edge from repo `r` to family `f` when `f` is a key in `repos[r].tools`. This counts *families*, not individual tool names. For example, `ix` has one edge to `grammar` even though that family lists three `ix_grammar_*` tools. `tars` also has one edge to `grammar`, where its listed tools have different names. The common label is evidence of a shared catalog word, not proof that the implementations accept the same inputs.

| Repo node | Declared family degree | One checked example |
|---|---:|---|
| `ix` | 27 | `grammar` contains `ix_grammar_weights`, `ix_grammar_evolve`, and `ix_grammar_search` |
| `tars` | 4 | `grammar` contains `tars_grammar_weight` and `tars_grammar_evolve` |
| `ga` | 5 | `music-theory` contains `ga_scale`, `ga_chord`, `ga_chord_atonal`, and `ga_interval` |

The degree sum on the repo side is `27 + 4 + 5 = 36`, so this definition yields **36 repo-to-family edges**. There are **35 distinct family-name nodes** because `grammar` is the sole repeated family key; all other family keys appear under just one of the three repos. Thus the graph has `3 + 35 = 38` nodes. This calculation is tied to the pinned registry; a later revision may add, rename, or remove declarations. It is also a deliberately narrow graph. It does not include Demerzel as a repo node just because Demerzel stores the registry.

### Practice exercise 1: count the right thing

A teammate reports “`ix` has three grammar edges” because three grammar tools are listed. Under this lesson's graph rule, what is `ix`'s degree, what is its grammar contribution, and how many nodes and edges are in the full two-type graph?

> **Answer:** `ix` has degree 27: one edge per `tools` family key, with exactly one `ix`–`grammar` edge. The whole pinned graph has 3 repo nodes and 35 distinct family nodes, hence 38 nodes; the repo-side degrees sum to 36 incidence edges. Counting tool entries would define a different graph and different degrees.

## 2. Project onto repos, then read the projection carefully

A **repo projection** replaces each two-step path `repo A → family → repo B` with an undirected A–B edge. State the rule exactly: connect two repos only if their `tools` objects share at least one **identical family key**. Inspecting the pinned sets gives `ix ∩ tars = {grammar}`, `ix ∩ ga = ∅`, and `tars ∩ ga = ∅`. The three-node projection therefore has one edge, `ix`–`tars`. It has two connected components: `{ix, tars}` and `{ga}`. In the original two-type graph, the same two components also contain their attached family nodes.

The projection has thrown away information. It does not show that `ix` has 27 families while `tars` has 4, or that their `grammar` implementations are different tools. GA appears isolated under this **exact-label rule** even though GA has five declared tool families and may participate in other cross-repo arrangements. Do not rename `ga`'s `spectral` family to `ix`'s `signal`, or `music-theory` to another label, solely to make a connecting line. Semantic similarity needs a reviewed mapping and a use case; string matching is reproducible precisely because it refuses to guess.

### Practice exercise 2: enumerate the projected edges

Which repo pairs share an exact family key? Give the projection's edge count, degrees, and connected components. Does isolated `ga` mean its MCP server is down?

> **Answer:** Only `ix` and `tars` share `grammar`, so the projection has one edge. Its degrees are `ix: 1`, `tars: 1`, `ga: 0`; its components are `{ix, tars}` and `{ga}`. `ga`'s zero projected degree says only that its five family **labels** do not exactly match the others in this registry. It says nothing about server uptime or whether a separate contract connects GA to another repo.

## 3. A graph cut is not an incident report

Suppose an analyst removes the **`grammar` family node from this model** to see which label carries the projected connection. The original two-type graph then has 34 family nodes and 34 incidence edges: deleting the shared family deletes its two repo edges. Its repo degrees become `ix: 26`, `tars: 3`, and `ga: 5`. The repo projection has no edges and three isolated repo nodes. This is a small articulation example: the catalog's one shared word is the only two-step path between `ix` and `tars` under the chosen rule.

That is a sensitivity result about a **static taxonomy**. It does not simulate stopping an MCP server or prove that an agent loses a working grammar capability. Removing a label from a JSON document could mean a rename, a catalog cleanup, or a real removal; the graph alone cannot tell which. To study operational resilience, define nodes as actual services or calls, obtain observed dependency edges, and test the failure mode against those receipts.

### Practice exercise 3: remove one family

After deleting the `grammar` family node, calculate the two-type graph's node and edge counts and the repo projection's component count. What operational conclusion is unsupported?

> **Answer:** The two-type graph has `3 + 34 = 37` nodes and `36 - 2 = 34` incidence edges. The repo projection has zero edges and three components, one per repo. This does **not** show that a live grammar service failed or that work stopped; only a declared family-name node was removed from the analytical graph.

## 4. Change the edge rule, change the claim

The pinned [cross-repo contracts note](../../../../../docs/architecture/cross-repo-contracts.md) describes a *different* graph. For its BAML seam, Demerzel owns [`baml_src/schema.baml`](../../../../../baml_src/schema.baml) and names `ix`, `ga`, and `hari` as intended consumers. If the question is “Who would have to react to a BAML schema change?”, model directed **declared producer → intended consumer** edges: `Demerzel → ix`, `Demerzel → ga`, and `Demerzel → hari`. That graph has four named repo nodes and three declared edges. It does not follow from shared `tools` labels. `hari` and Demerzel are absent from the registry's three-repo projection because that projection uses a different input and node rule.

The contract note explicitly labels consumer generation from this BAML contract **undelivered** at the time of the pinned document: it says no consumer generates from it yet. It also warns that its liveness statements age. Thus the three arrows are **intended coordination edges**, not three observed working integrations. A useful project diagram draws declared and observed edges with different line styles, dates, and supporting receipts; it does not silently promote a design arrow into a runtime call. Nor does the absence of a BAML arrow to `tars` prove there is no other TARS relationship: this paragraph discusses one named seam only.

### Practice exercise 4: compare two graphs

Draw the BAML producer-to-consumer graph named in the contract note. Why is it incorrect to add its three arrows to the 36 repo-to-family edges and call the sum one network? Which of those arrows has a confirmed live generation receipt in the pinned note?

> **Answer:** The declared BAML graph has `Demerzel → ix`, `Demerzel → ga`, and `Demerzel → hari`: four repo nodes and three directed, intended edges. The 36 catalog edges join repo nodes to family-name nodes and are undirected declarations, so adding unlike edges produces a count with no stable meaning. The pinned note calls consumer generation undelivered; it confirms **no** live consumer-generation arrow.

## 5. Turn the graph into a bounded routing question

The registry lists `ga_chord` under GA's `music-theory` family and `tars_grammar_weight` under TARS's `grammar` family. A coordinator could *propose* a two-step task: ask GA for chord data, then ask TARS to weight a grammar based on an explicitly defined input. The catalog identifies candidate tools; it does not specify whether their outputs and inputs fit together. Before treating the route as executable, record the exact tool versions and schemas, the transform between their payloads, authorization, error handling, and a successful test invocation at a stated time. If any of that is missing, label the link proposed or unknown. A diagram that records that uncertainty is more useful than a visually complete but unverified route.

### Practice exercise 5: make a route claim falsifiable

A plan says, “GA and TARS are disconnected because the registry projection has no edge; therefore `ga_chord` cannot feed `tars_grammar_weight`.” Rewrite it as a testable statement. What result would establish only the narrow route, rather than a general claim about the whole ecosystem?

> **Answer:** “The pinned registry has no **shared-family-label** edge between GA and TARS. Whether `ga_chord` output can be transformed into valid `tars_grammar_weight` input is unknown until their current schemas and an authorized test call are checked.” A versioned input/output mapping plus one successful, recorded invocation would support that specific route under the tested conditions. It would not prove every GA/TARS integration or permanent service availability.

## Key takeaways

- Name the node types and edge rule before computing degree, paths, or components.
- Exact-label projection is reproducible but loses tool details and says nothing by itself about runtime connectivity.
- A catalog family, an intended contract seam, and an observed call require separate graph layers and evidence.
- Removing a catalog node demonstrates model sensitivity, not a live outage.
- Three repo nodes cannot establish the power-law behavior discussed in NET-001.

## Project evidence and limits

- Demerzel commit `5c4967454ddc740ed937c87719ca4d71a3522e4b`: [capability registry v1.1.0](../../../../../schemas/capability-registry.json), [cross-repo contracts note](../../../../../docs/architecture/cross-repo-contracts.md), and [BAML source contract](../../../../../baml_src/schema.baml). The 27/4/5 family counts and shared-label intersection were recomputed from that pinned JSON before authoring.
- This lesson treats family names as exact strings. It does not measure live MCP tool availability, schema compatibility, actual traffic, latency, or failure propagation. The contract note's undelivered/liveness statements are historical and must be rechecked before an operational decision.
- No learner attempt, subject review, fluent localization, Learn sync/build, or anonymous public readback has been completed for NET-002.
