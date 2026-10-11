---
module_id: inf-002-optick-compact-vector-information-loss
department: information-theory
course: Information Loss in OPTIC-K Compact Vectors
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-002
version: "0.1.0"
---

# Information Loss in OPTIC-K Compact Vectors

> **Department of Information Theory** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Name the information GA retains, discards, and normalizes when it builds a compact OPTIC-K similarity vector.
- Translate an offset in GA's 240-slot raw schema into its 124-slot compact layout without mixing the two coordinate systems.
- Exhibit two different raw vectors with the same compact vector, and explain why that proves reconstruction is impossible.
- Check a weighted similarity claim with a fixed fixture and state what the check does **not** say about full retrieval.

## The project question

GA stores musical embeddings for voicing retrieval. Its [pinned `EmbeddingSchema.cs`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs) declares `OPTIC-K-v1.8`, a 240-dimensional raw vector, partition roles, weights, and the `ExtractCompact` operation. A compact index should preserve the similarity calculation that its reader needs. But what can a reader infer about the original raw vector after this transformation?

Here is the falsifiable question: **If two raw vectors produce the same compact vector, must they contain the same musical and identity data?** The answer is no. We will construct three explicit counterexamples. This matters when an agent inspects a search artifact: a compact index entry is evidence about a specific scoring representation, not a copy of every source feature. The distinction also prevents an engineer from treating two equal compact scores as proof that an entire search request, including possible filters, behaves identically.

[INF-001](inf-001-entropy-of-governance.md) estimated uncertainty in policy-token sequences. This lesson uses a different information-theory idea: a **many-to-one map**. If distinct inputs become the same output, the output cannot uniquely determine the input. A dimension count signals possible loss, but the counterexample is the proof. Even a representation with the same number of slots could lose information through normalization.

## 1. Read the pinned contract, not the slot count alone

The schema's [partition registry](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L117-L148) gives each raw interval an inclusive start and end, a role, and a similarity weight. The `Similarity` partitions are packed in registry order. The `Identity` and `Info` partitions are absent from the compact vector. The table below computes compact offsets by adding the retained dimensions; those offsets are **not** raw offsets.

| Partition | Raw slots | Role | Weight | Compact slots |
|---|---:|---|---:|---:|
| IDENTITY | 0–5 | Identity | 0 | omitted |
| STRUCTURE | 6–29 | Similarity | 0.45 | 0–23 |
| MORPHOLOGY | 30–53 | Similarity | 0.25 | 24–47 |
| CONTEXT | 54–65 | Similarity | 0.20 | 48–59 |
| SYMBOLIC | 66–77 | Similarity | 0.10 | 60–71 |
| EXTENSIONS | 78–95 | Info | 0 | omitted |
| SPECTRAL | 96–108 | Info | 0 | omitted |
| MODAL | 109–148 | Similarity | 0.10 | 72–111 |
| HIERARCHY | 149–163 | Info | 0 | omitted |
| ATONAL_MODAL | 164–227 | Info | 0 | omitted |
| ROOT | 228–239 | Similarity | 0.05 | 112–123 |

The six retained widths add to `24 + 24 + 12 + 12 + 40 + 12 = 124`. The five omitted widths add to `6 + 18 + 13 + 15 + 64 = 116`. Together they account for all 240 raw slots. This is a count of coordinates, **not** a count of bits or measured compression ratio: numeric precision, headers, and the index file format would have to be specified for a storage claim. The code builds a layout string beginning `optk-v4-pp-r:` and hashes it for schema compatibility. A reader should establish that version and layout before interpreting index bytes; the exercise below does not open a production index.

### Practice exercise 1: account for every slot

Using inclusive endpoints, how many coordinates does MODAL contribute? How many raw coordinates are left out of the compact vector? Is “116 bits lost” a justified statement?

> **Answer:** MODAL contributes `148 - 109 + 1 = 40` coordinates. Retained widths total 124, so `240 - 124 = 116` raw coordinates are omitted. “116 bits lost” is unjustified because each coordinate is a numeric value, not one bit, and normalization also loses information inside retained partitions.

### Practice exercise 2: change coordinate systems

Where do raw ROOT slots 228 and 239 land in the compact layout? Does compact slot 112 name raw slot 112?

> **Answer:** ROOT begins after 112 retained coordinates, so raw 228 maps to compact 112 and raw 239 maps to compact 123. Compact slot 112 is the first ROOT coordinate, while raw slot 112 lies inside MODAL. A label must say which coordinate system it uses.

## 2. What the transformation keeps

[`ExtractCompact`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L235-L266) reads each similarity partition separately. For a nonzero partition slice, it divides every value by that slice's Euclidean norm and multiplies by the square root of the partition weight. It then appends the scaled slice to the compact vector. A zero slice contributes zeros. In symbols, for similarity partition `p` with raw slice `x_p` and weight `w_p`, the nonzero compact slice is:

```text
c_p(x) = sqrt(w_p) * x_p / ||x_p||_2
```

The result retains the **direction** of each nonzero similarity slice and its allotted weight. It discards the slice's original positive magnitude. A positive rescaling of one slice gives the same compact slice, provided the slice remains nonzero. It also discards the values in roles not selected by `SimilarityPartitions`. Neither kind of loss can be undone from the compact coordinates alone.

The [weighted scorer](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L269-L302) sums `w_p * cosine(a_p, b_p)` over similarity partitions. For full-length vectors and nonzero slices, the dot product of the two compact vectors equals that weighted sum up to the precision of the stored weights. The pinned [schema contract test](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.ML.Tests/SchemaLayoutContractTests.cs#L31-L50) asserts that relationship within `1e-6` for deterministic nonzero inputs. The test is source evidence for the intended contract; this lesson does not claim a fresh C# test run.

This is a **score-preserving representation for the defined similarity function**, not a general-purpose archive of the raw embedding. “Preserves similarity” needs that qualifier. An application may use IDENTITY for hard filtering, other fields for display or analysis, or a different search path. Equality of these compact vectors alone cannot establish equality of full search results or of musical meaning.

## 3. A fixed synthetic fixture

The following vectors are **constructed classroom data**, not observed guitar embeddings or stored index entries. All 240 slots start at zero. `A` puts 1 in the first slot of each similarity partition: raw slots `6, 30, 54, 66, 109, 228`. It also puts 1 in IDENTITY slot `0` and EXTENSIONS slot `78`. `B` copies A's similarity values but moves IDENTITY's 1 from raw `0` to `1` and EXTENSIONS' 1 from raw `78` to `79`. `C` copies A except that ROOT's 1 moves from raw `228` to `229`. `D` copies A except that raw STRUCTURE slot `6` changes from 1 to 2.

An independent Python calculation read the partition rows from the **pinned GA source revision** and reproduced `ExtractCompact`'s per-partition normalization and weighted cosine for these inputs. It observed the following values; they are fixture calculations, not a production retrieval measurement. Scores are displayed to two decimal places because float weights and square roots can introduce tiny rounding differences.

| Pair | Raw relationship | Compact relationship | Weighted score | Compact dot product |
|---|---|---|---:|---:|
| A/A | identical | identical | 1.15 | 1.15 |
| A/B | IDENTITY and EXTENSIONS differ | identical | 1.15 | 1.15 |
| A/C | ROOT one-hot directions differ | different | 1.10 | 1.10 |
| A/D | STRUCTURE magnitude differs | identical | 1.15 | 1.15 |

Each vector has one nonzero value in each similarity partition. The six self-comparison contributions are therefore `0.45 + 0.25 + 0.20 + 0.10 + 0.10 + 0.05 = 1.15`. A score above 1 is not an error here: this weighted sum is not a probability, and the weights in the pinned registry total 1.15. In A/C, ROOT's one-hot vectors are orthogonal, so its contribution falls from 0.05 to zero while all other contributions stay fixed.

### Practice exercise 3: omission is a real collision

Can the compact vector distinguish A from B? Can you conclude that a complete GA search request treats A and B identically?

> **Answer:** No compact coordinate can distinguish them, because their six similarity slices are equal; both compact vectors and their weighted scores are equal. Their raw vectors differ at IDENTITY and EXTENSIONS, which proves compact-to-raw reconstruction is not unique. A complete search request might use IDENTITY as a hard filter, so full search equivalence does not follow.

### Practice exercise 4: loss within a retained partition

Why does D have the same compact vector as A although STRUCTURE is retained? Would changing raw slot 6 from 1 to 0 have the same explanation?

> **Answer:** A's STRUCTURE slice has norm 1; D's slice has norm 2. Dividing each by its own norm gives the same unit direction, then both receive the same `sqrt(0.45)` scale. Changing 1 to 0 would produce an all-zero STRUCTURE slice instead, which the code leaves zero, so that change would alter the compact vector and its score. Positive magnitude loss is the demonstrated collision.

### Practice exercise 5: make a prediction that can fail

Before reading the fixture table, predict `WeightedPartitionCosine(A,C)` and the compact dot product. State one concrete observation that would refute your prediction under the pinned algorithm.

> **Answer:** The five unchanged similarity slices contribute `0.45 + 0.25 + 0.20 + 0.10 + 0.10 = 1.10`; orthogonal ROOT slices contribute zero, so both calculations should be about **1.10** and agree within floating-point tolerance. A computed A/C score near 1.15, with the specified nonzero slots and pinned weights, would refute either the fixture construction or the claimed scoring behavior and require inspecting the source and calculation.

## 4. Limits and next check

The fixture proves a narrow mapping claim for a pinned source revision. It does not test index serialization, schema-hash rejection, actual encoded guitar voicings, query construction, filter behavior, ranking ties, or the current deployment. Those need their own artifact and tests. The pinned source says whole STRUCTURE is **not transposition-invariant** because it contains pitch-class chroma; this lesson does not use its compact equality examples to claim otherwise. ROOT's role here is a 12-slot similarity partition with low weight, not proof that a particular musician will prefer one result.

For a real index investigation, record the GA commit, the index header's schema hash, the raw and compact coordinate systems, any filters, and the exact query and candidate artifacts. Then compare the scorer and compact dot product on that fixed case. If they disagree beyond the contract tolerance, the useful next action is a reproducible mismatch report, not an interpretation of the score as musical quality. This English lesson remains a draft until subject review, a learner attempt, localization, and publication review are complete.

## Pinned sources

- [GA `EmbeddingSchema.cs` at `dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs): version and registry, compact layout, extraction, and weighted scorer.
- [GA `SchemaLayoutContractTests.cs` at the same commit](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.ML.Tests/SchemaLayoutContractTests.cs): intended compact-dot and weighted-score relationship, identical-vector weight sum, and ROOT offset guard.
