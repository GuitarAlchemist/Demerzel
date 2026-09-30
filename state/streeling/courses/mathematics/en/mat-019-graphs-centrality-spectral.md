---
module_id: mat-019-graphs-centrality-spectral
department: mathematics
course: Graphs, Centrality and Spectral Structure
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-018-clustering-density-validity]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Graphs, Centrality and Spectral Structure — Which Vertex Matters, and What the Laplacian Counts

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- Describe a graph by its adjacency, degree and Laplacian matrices, and read walks and components from them
- Define PageRank as the stationary distribution of a random surfer, bound the error of its power iteration, and say what becomes of the rank of a vertex without out-links
- Compute degree, closeness, betweenness and eigenvector centrality, and build a graph on which they disagree
- Prove that the Laplacian is positive semidefinite and that the multiplicity of its eigenvalue 0 is the number of connected components
- Split a graph with the Fiedler vector, and say when that vector is not determined
- Trace what IX's `Graph`, its handlers and `compute_laplacian_spectrum` guarantee, and where their comments, catalogue and tests promise more than the code delivers

---

## 1. Graphs as Matrices

A graph has n vertices, numbered 0 to n − 1, and a set of edges. In a directed graph an edge i → j has a direction; in an undirected graph an edge {i, j} is an unordered pair. The **adjacency matrix** A has A_ij = 1 when there is an edge from i to j and 0 otherwise, or a weight w_ij > 0 in a weighted graph; for an undirected graph A is symmetric. The **degree** of a vertex is d_i = Σ_j A_ij, and D = diag(d_1, …, d_n). In an unweighted graph, the entry (Aᵏ)_ij counts the walks of length k from i to j, since a walk i → l → j contributes A_il A_lj to (A²)_ij, and so on. Two vertices of an undirected graph lie in the same **connected component** when a walk joins them; a directed graph is weakly connected when its edges, with their direction ignored, connect it.

For an undirected graph, A is symmetric, so the spectral theorem of MAT-005 gives real eigenvalues λ_1 ≥ … ≥ λ_n and an orthonormal basis of eigenvectors. Since A has nonnegative entries, the Perron–Frobenius theorem adds more (Horn and Johnson 2013, ch. 8): λ_1 ≥ |λ_i| for every i, and when the graph is connected, λ_1 is simple and has an eigenvector with positive entries, the **Perron vector**. The bound |λ_n| ≤ λ_1 can be an equality: a connected graph has λ_n = −λ_1 exactly when it is **bipartite**, when its vertices split into two sides with every edge between them (Brouwer and Haemers 2012). A star, a path and an even cycle are bipartite; a triangle is not. This matters for power iteration (§3), which needs one eigenvalue strictly larger in modulus than all the others.

### Practice Exercise

Show that the spectrum of a bipartite graph is symmetric about 0: if λ is an eigenvalue, so is −λ, with the same multiplicity.

> *Solution:* Number the vertices of one side first, so that A = [[0, B], [Bᵀ, 0]]. If (u, v) is an eigenvector for λ, then B v = λ u and Bᵀ u = λ v. Then A (u, −v) = (−B v, Bᵀ u) = (−λ u, λ v) = −λ (u, −v), so −λ is an eigenvalue. The map (u, v) ↦ (u, −v) is invertible and sends the eigenspace of λ onto that of −λ, so the multiplicities are equal. For the star with centre 0 and leaves 1, 2 and 3, the eigenvalues are √3, 0, 0 and −√3.

---

## 2. PageRank

PageRank (Brin and Page 1998; Page, Brin, Motwani and Winograd 1999) ranks the vertices of a directed graph by the long-run behaviour of a random surfer. From vertex i, with probability α, the **damping factor**, the surfer follows one of the out-links of i, each with probability 1/out(i); with probability 1 − α, the surfer jumps to a vertex drawn uniformly. A vertex without out-links, a **dangling node**, needs a rule of its own, and the usual one sends the surfer from it to a uniform vertex. Write P for the matrix of the out-links, with P_ij = 1/out(i) for an edge i → j, whose rows for the dangling nodes are zero; S for P with those rows replaced by u = (1/n, …, 1/n); and 𝟙 for the column of ones. The **Google matrix** is M = α S + (1 − α) 𝟙u, and the PageRank vector is its stationary distribution: the row vector π ≥ 0 with Σ_i π_i = 1 and π M = π.

For 0 ≤ α < 1 every entry of M is positive, so by Perron–Frobenius π exists, is unique and is positive. Power iteration finds it, and its error is easy to bound. For two probability vectors x and y, x M − y M = α (x − y) S, because (x − y) 𝟙 = 0; S has nonnegative entries and rows that sum to 1, so ‖(x − y) S‖₁ ≤ ‖x − y‖₁, and ‖x M − y M‖₁ ≤ α ‖x − y‖₁. After k steps from any start, the error in the ℓ1 norm is at most 2αᵏ. With the usual α = 0.85, 100 steps leave at most 2 · 0.85^100 ≈ 1.7 × 10^-7; with α = 0.99 the same bound is 2 · 0.99^100 ≈ 0.73, and it can be nearly reached (§6). The second eigenvalue of M is at most α in modulus (Haveliwala and Kamvar 2003): α sets the speed.

Another treatment of the dangling nodes drops their rank: iterate x ← α x P + (1 − α) u. The same argument, with P in place of S, shows that it converges, to x* = (1 − α) u (I − α P)^-1, whose entries sum to less than 1 as soon as a dangling node has positive rank. Take two papers, 0 and 1, that cite a third, 2, which cites nothing, with α = 0.85. After two steps the ranks of 0 and 1 are 0.15/3 = 0.05, that of 2 is 0.05 + 0.85 · (0.05 + 0.05) = 0.135, and nothing changes afterwards: the three sum to 0.235. Divided by that sum, x* becomes (10/47, 10/47, 27/47) ≈ (0.2128, 0.2128, 0.5745), which is exactly π with uniform jumps from the dangling node (exercise below; Langville and Meyer 2006).

On an undirected graph with m edges and no isolated vertex, where each edge counts in both directions, the walk without jumps, α = 1, has the transition matrix D^-1 A, and π_i = d_i/(2m) is stationary: Σ_i (d_i/(2m)) (A_ij/d_i) = d_j/(2m). The random surfer on an undirected graph is drawn toward the vertices of high degree.

### Practice Exercise

Show that when the rank of the dangling nodes is dropped, the fixed point x*, divided by the sum of its entries, is the PageRank π with uniform jumps from the dangling nodes.

> *Solution:* Let a be the column that is 1 at the dangling nodes and 0 elsewhere, so that S = P + a u. Since π 𝟙 = 1, π M = α π P + α (π a) u + (1 − α) u, so π = α π P + γ u with γ = α (π a) + 1 − α > 0. The matrix I − α P is invertible, because α P has nonnegative rows that sum to at most α < 1, so π = γ u (I − α P)^-1 = (γ/(1 − α)) x*. Thus π is a positive multiple of x*, and since the entries of π sum to 1, π = x*/Σ_i x*_i. On the citation graph, γ = 0.85 · 27/47 + 0.15 = 30/47, and γ/(1 − α) = 200/47 = 1/0.235.

---

## 3. The Family of Centralities

Centrality measures answer different questions about a vertex i of a connected undirected graph with n vertices:
- **Degree centrality**, d_i/(n − 1): how many neighbours, as a fraction of the possible.
- **Closeness centrality**, (n − 1)/Σ_j dist(i, j), with distances counted in edges: how near to all the others. On a disconnected graph that sum is infinite; the form r²/((n − 1) Σ_j dist(i, j)), with r the number of vertices other than i reachable from i and the sum over them, reduces to the first when every vertex is reachable (Wasserman and Faust 1994).
- **Betweenness centrality**, Σ σ_st(i)/σ_st over the unordered pairs {s, t} of other vertices, where σ_st counts the shortest paths between s and t and σ_st(i) those through i (Freeman 1977): how often i lies on the way. Dividing by (n − 1)(n − 2)/2, the number of pairs, puts it in [0, 1]. Brandes (2001) computes it for every vertex in O(nm) time for m edges, with one breadth-first search from each vertex.
- **Eigenvector centrality** (Bonacich 1972): the Perron vector of A, so that each vertex scores in proportion to the sum of its neighbours' scores, x_i = (1/λ_1) Σ_j A_ij x_j.

Krackhardt's kite (Krackhardt 1990) is the classic graph on which they disagree. Its ten vertices, Andre, Beverly, Carol, Diane, Ed, Fernando, Garth, Heather, Ike and Jane, are numbered 0 to 9, with the edges 0–1, 0–2, 0–3, 0–5, 1–3, 1–4, 1–6, 2–3, 2–5, 3–4, 3–5, 3–6, 4–6, 5–6, 5–7, 6–7, 7–8 and 8–9. Diane has the highest degree, 6 of 9, and the highest eigenvector centrality. Fernando and Garth are the closest, at 9/14 ≈ 0.643 against 3/5 for Diane. Heather, the only link between the dense part and the tail Ike–Jane, has the highest betweenness, 14 of the 36 pairs of other vertices, against 25/3 for Fernando and Garth and 11/3 for Diane. None of the four answers is wrong: each measures something else, and "the most central vertex" means nothing until one says which measure.

Eigenvector centrality is usually computed by power iteration (MAT-005 §6), which fails on bipartite graphs: by §1 their spectrum contains −λ_1 as well as λ_1, the two terms of largest modulus never separate, and the iterate oscillates. On the star with centre 0 and leaves 1, 2 and 3, from x = (1, 1, 1, 1), A x = (3, 1, 1, 1) and A² x = (3, 3, 3, 3): after every even number of steps the normalised iterate is uniform, and the hub looks like a leaf. The usual remedy iterates with A + I, whose eigenvalues are λ_i + 1, with the same eigenvectors. Since λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1 whenever λ_1 > 0, so the Perron vector now dominates strictly. The shifted eigenvalues need not be positive: on the star they are 1 + √3, 1, 1 and 1 − √3 ≈ −0.732. On a disconnected graph, the iteration from a positive start converges to a vector supported on the components whose λ_1 is largest, and every other vertex scores 0 in the limit.

### Practice Exercise

Compute the betweenness of the centre of a star with k leaves, and of the middle vertex of the path 0–1–2, before and after dividing by the number of pairs.

> *Solution:* In a star, every pair of leaves has exactly one shortest path, through the centre, so the centre's betweenness is k(k − 1)/2, the number of pairs of leaves, and each leaf scores 0. With n = k + 1 vertices there are (n − 1)(n − 2)/2 = k(k − 1)/2 pairs of other vertices, so the normalised value is 1. For the path 0–1–2, the only pair not containing 1 is {0, 2}, whose one shortest path passes through 1: betweenness 1, normalised 1. Unnormalised, the centre of a star scores 3 with three leaves and 10 with five, although both lie on every shortest path they could lie on.

---

## 4. The Laplacian

The **Laplacian** of an undirected graph with weights w_ij ≥ 0 is L = D − A, where d_i = Σ_j w_ij. Its quadratic form is

xᵀ L x = Σ over the edges {i, j} of w_ij (x_i − x_j)²,

so L is positive semidefinite (exercise), and L 𝟙 = 0 because every row sums to 0. Its eigenvalues, in increasing order, are 0 = μ_1 ≤ μ_2 ≤ … ≤ μ_n.

**The zero eigenvalue counts the components.** For a positive semidefinite matrix, xᵀ L x = 0 holds exactly when L x = 0. With positive weights, xᵀ L x = 0 means x_i = x_j across every edge, that is, x constant on each connected component. So the null space of L is spanned by the indicator vectors of the components, and the multiplicity of the eigenvalue 0 is the number c of components. In particular μ_2 > 0 exactly when the graph is connected; Fiedler (1973) called μ_2 the **algebraic connectivity**.

**The Fiedler vector.** By the Rayleigh quotient of MAT-005, taken over the vectors orthogonal to 𝟙, the eigenvector of μ_1,

μ_2 = min over x ≠ 0 with Σ_i x_i = 0 of Σ over the edges of (x_i − x_j)² / Σ_i x_i²,

for an unweighted graph, and a minimiser is a **Fiedler vector**. Setting x_i = 1 on one half of the vertices and −1 on the other, when n is even, turns the numerator into 4 times the number of edges cut and the denominator into n, so μ_2 ≤ 4 · cut/n for every split into two halves. The Fiedler vector is the best real-valued relaxation of that balanced cut, and splitting the vertices by its sign is the simplest spectral partition. Fiedler (1975) proved that on a connected graph the vertices where the vector is ≥ 0 induce a connected subgraph, and so do those where it is ≤ 0. The vector is determined, up to sign and scale, only when μ_2 is simple. On a disconnected graph μ_2 = 0 is repeated; on the complete graph K_n, whose Laplacian eigenvalues are 0 and n, repeated n − 1 times, every vector orthogonal to 𝟙 is a Fiedler vector (MAT-005 §5).

Some spectra to keep in mind: the path with n vertices has the eigenvalues 2 − 2 cos(πk/n) for k = 0, …, n − 1, so μ_2 = 4 sin²(π/(2n)) ≈ π²/n²; the star with n vertices has 0, 1 repeated n − 2 times, and n. Chung (1997) and spectral clustering (Shi and Malik 2000; Ng, Jordan and Weiss 2002; von Luxburg 2007) use the **normalised Laplacians** L_sym = I − D^(-1/2) A D^(-1/2) and L_rw = I − D^-1 A, where D^-1 A is the walk of §2. Cheeger's inequality ties the second eigenvalue of L_sym to the conductance h of the best cut: h²/2 ≤ μ_2(L_sym) ≤ 2h. Spectral clustering embeds each vertex by its entries in the first k eigenvectors of such a Laplacian, and runs the k-means of MAT-018 on the embedding.

### Practice Exercise

Prove that xᵀ L x = Σ over the edges {i, j} of w_ij (x_i − x_j)², and deduce that L is positive semidefinite.

> *Solution:* xᵀ L x = Σ_i d_i x_i² − Σ_(i,j) w_ij x_i x_j, where the second sum runs over ordered pairs, so each edge {i, j} appears twice in it and contributes −2 w_ij x_i x_j. The degree d_i = Σ_j w_ij splits each edge's weight between its two ends, so the first sum contributes w_ij (x_i² + x_j²) for each edge. Together, each edge gives w_ij (x_i² − 2 x_i x_j + x_j²) = w_ij (x_i − x_j)². A sum of nonnegative terms is nonnegative, so xᵀ L x ≥ 0 for every x, and every eigenvalue of L, the Rayleigh quotient of its eigenvector, is ≥ 0.

---

## 5. The Barbell

Join two complete graphs K_5, on the vertices 0–4 and 5–9, by the single edge 4–5. Here the centralities agree. The two ends of the bridge have degree 5 against 4, and betweenness 20 each, since each of the 4 × 5 pairs formed by another vertex of their own clique and a vertex of the other clique uses them. Their closeness is 9/13 ≈ 0.692 against 1/2, their eigenvector centrality is the highest, and the stationary distribution of the walk without jumps gives each of them 5/42, against 4/42 (§2).

The Laplacian has the eigenvalues 0, (7 − √41)/2 ≈ 0.2984, then 5 repeated seven times, and (7 + √41)/2 ≈ 6.7016 (exercise). A Fiedler vector takes a value a on the four inner vertices of the first clique, (1 − μ_2) a ≈ 0.7016 a on the end of the bridge, and the opposite values on the second clique, so its sign splits the barbell into its two bells, cutting one edge. The algebraic connectivity is small, 0.2984 against 5 inside each clique alone: one edge holds the two halves together, and μ_2 says so. Remove the bridge, and 0 becomes a double eigenvalue. The vectors equal to 1 on one clique and 0 on the other span the null space, every combination of them is a Fiedler vector, and the sign rule no longer means anything.

### Practice Exercise

Derive the eigenvalues (7 ± √41)/2 of the barbell's Laplacian from the vector that takes the value a on the four inner vertices of the first clique, b on vertex 4, −b on vertex 5 and −a on the four inner vertices of the second clique.

> *Solution:* At an inner vertex of the first clique, of degree 4, (L x)_i = 4a − 3a − b = a − b; at vertex 4, of degree 5, (L x)_4 = 5b − 4a − (−b) = 6b − 4a. On the second clique the equations are the same with opposite signs. So x is an eigenvector for μ when a − b = μ a and 6b − 4a = μ b. The first gives b = (1 − μ) a, and the second then 6(1 − μ) − 4 = μ(1 − μ), that is μ² − 7μ + 2 = 0, whose roots are (7 ± √41)/2 ≈ 0.2984 and 6.7016. The eigenvalue 5 has the vectors that vanish outside the inner vertices of one clique and sum to 0 there, three for each clique, and the vector equal to a on the eight inner vertices and −4a on the two ends of the bridge; with 𝟙 for the eigenvalue 0, that accounts for all ten.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription into Python of the `Graph` of `crates/ix-graph`, of `compute_laplacian_spectrum` with the Jacobi solver it calls (MAT-005 §4), and of the handlers below. `Graph` keeps its adjacency lists in a `HashMap` and its neighbour sets in `HashSet`s, which Rust iterates in an order drawn at random in each process; that order only changes the order of some floating-point sums, which can move the last bits of a score but none of the decimals stated here. These numbers are predictions, and §7 proposes to check them.

**The graph and its handlers.** [`Graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L8) stores, for each vertex, a list of (neighbour, weight) pairs, and [`add_undirected_edge`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L37) adds both directions. The MCP tool `ix_graph` calls [`graph_ops`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2815), which builds a graph with `n_nodes` vertices, rejects an edge whose ends are out of range, treats the edges as [directed unless told otherwise](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2832), takes a missing weight as [1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2860), and offers Dijkstra's algorithm, shortest paths, PageRank, breadth-first and depth-first search and a topological sort, with PageRank's [damping 0.85](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2889) and [100 iterations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2890) by default. The four centralities of §3 are available in SQL through a table function of `crates/ix-duck`, which computes, for instance, [the eigenvector centrality with 100 iterations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L482), whose edge parser [rejects negative weights](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L141); betweenness is also behind `ix_mesh_correlate`. The inner loop of [`pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L185) is:

```rust
            for (&node, edges) in &self.adjacency {
                let out = out_degree[&node] as f64;
                if out > 0.0 {
                    let share = damping * rank[&node] / out;
                    for &(neighbor, _) in edges {
                        *new_rank.get_mut(&neighbor).unwrap() += share;
                    }
                }
            }
```

**The Laplacian.** [`compute_laplacian_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L420) builds L from an unweighted edge list, calls the [full Jacobi eigensolver](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L449) of MAT-005, [clamps the eigenvalues at 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L454), returns the three smallest with μ_2, μ_2 − μ_1 and a [Fiedler vector](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L477), and counts the components as follows:

```rust
    let zero_tol = 1e-6;
    let n_components = eigenvalues_all
        .iter()
        .filter(|&&e| e < zero_tol)
        .count()
        .max(1);
```

- **PageRank drops the rank of dangling nodes.** In the loop above, a vertex with `out` = 0 passes nothing on: this is the iteration of §2 that drops their rank, with n [the number of vertices in the map](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L186). On the citation graph of §2, `ix_graph` returns 0.05, 0.05 and 0.135, which sum to 0.235. The DuckDB function `ix_pagerank` divides by the sum, as its comment says, ["so dangling-node mass leakage doesn't break the probability-distribution contract"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L161). By the exercise of §2 this is more than cosmetic: once converged, it returns exactly PageRank with uniform jumps from the dangling nodes, 10/47, 10/47 and 27/47 here. The MCP tool returns the raw vector. IX's own smoke test [feeds the dependency graph](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L183) of `ix_cargo_deps` to `ix_graph`, with an edge from each crate to each IX crate it depends on, so that every crate without an IX dependency is a dangling node; the test only [counts the entries](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L200).
- **PageRank ignores the weights.** The loop reads each edge as [`(neighbor, _)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L207): every out-link gets the same share, whatever its weight, so a weighted edge list gives the same ranks as the unweighted one. IX's walkthrough of the executable mesh [met this](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/walkthroughs/executable-pipeline-mesh.md#L57): a PageRank over the pairwise distances of a complete graph came out uniform, and the walkthrough explains it as a property of complete graphs. The uniformity comes from this code, for which a complete graph is regular whatever its weights; a weighted walk, with probabilities w_ij/Σ_k w_ik, is drawn toward the vertices with the largest total weight, as by §2 it is drawn toward high degree.
- **The number of iterations is fixed.** `pagerank` runs exactly `iterations` passes and tests nothing. By §2 the error is at most 2αᵏ: negligible for α = 0.85 and 100 passes, not for α = 0.99. On the star with three leaves, with each edge in both directions, α = 0.99 and 100 passes, the transcription predicts 0.4077 for the hub and 0.1974 for each leaf, against the exact 0.4987 and 0.1671, an error of 0.1821 in the ℓ1 norm. The star is bipartite, so the error changes sign at each pass and shrinks only by the factor 0.99. The catalogue that `ix_explain_algorithm` sends to the client lists PageRank's hyperparameters as ["damping" and "tol"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5861); there is no tolerance.
- **The handler checks neither α nor the number of iterations.** It reads both with a fallback to the default, so a non-numeric damping becomes 0.85, and it accepts any number, where `ix_pagerank` rejects [α outside [0, 1]](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L165) and [fewer than 1 iteration](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L169). With α = 1.5 on the citation graph, `ix_graph` returns −1/6, −1/6 and −2/3; with 0 iterations it returns the uniform start.
- **The eigenvector comment gives a wrong reason for a right method.** [`eigenvector_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L333) iterates with A + I, as in §3, and its comment says that A + I ["has strictly positive eigenvalues"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L330). On the star of IX's own test one of them is 1 − √3 ≈ −0.732. The method converges anyway, for the reason given in §3: from the uniform start, the error of the hub-to-leaf ratio shrinks by the factor (√3 − 1)/(√3 + 1) = 2 − √3 ≈ 0.268 per pass, and the transcription predicts √3 ≈ 1.7321 to double precision after 30 of the 100 passes. The test asserts [a ratio above 1.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L498), which the unshifted iteration, uniform after 100 passes, fails. On the triangle 0–1–2 with the separate edge 3–4, the scores of 3 and 4 shrink by the factor 2/3 per pass, and the transcription predicts about 1.4 × 10^-18 after 100 passes.
- **Betweenness is a count, not a fraction.** The comment of [`betweenness_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L363) speaks of ["the fraction of shortest paths through each node"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L361), but the code adds the fractions over all pairs and [halves the total](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L400), for pairs seen from both ends, without dividing by the number of pairs: 3 for the centre of the star of the test, 10 with five leaves, 20 for the ends of the barbell's bridge. Scores from graphs of different sizes cannot be compared. The star test asserts only that the hub's score is [positive](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L508).
- **`ix_mesh_correlate` names a hub when there is none.** [`mesh_correlate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1214) joins the series whose Pearson correlation reaches the threshold in absolute value, computes their [betweenness](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1239), and returns as `hub` the vertex chosen by [`max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1244), which returns the last of several equal maxima. When no pair reaches the threshold, or when every pair does, every score is 0 and `hub` is the last series: for the three series (1, −1, 1, −1), (1, 1, −1, −1) and (1, −1, −1, 1), pairwise uncorrelated, the transcription predicts `hub` = 2. On a path 0–1–2–3, where 1 and 2 tie, it also returns 2.
- **Dijkstra accepts negative weights.** [`dijkstra`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L92) is the lazy variant: it [skips a stale heap entry](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L108) and expands a vertex again whenever its distance drops. With negative weights and no negative cycle, it still returns the right distances, possibly after exponentially many steps (Johnson 1973). IX's catalogue recommends Dijkstra for ["non-negative weights"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5853), but the handler takes any number as a weight. The DuckDB parser rejects negative weights, and its comment says that a negative weight ["gives wrong paths and a negative cycle never settles"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L140): the second half holds, but this lazy variant still gives right paths, at worst slowly, and the PageRank that the same comment names ignores the weights. With `directed` set to false, one negative edge is a negative cycle of two edges, and the loop lowers the two distances in turn: on the single edge 0–1 of weight −1, the transcription reaches −12 and −11 after twelve steps, and the loop would only stop near −2^53, where subtracting 1 no longer changes a double, after about 9 × 10^15 steps. This is predicted from the code, not run; §7 runs it under a timeout.
- **The handler checks the edges but not the source.** An edge end outside the graph is an error, but [`source`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2870) is not checked: from source 7 on a graph with three vertices, Dijkstra returns the distance 0 for a vertex 7 that does not exist and ∞ for the three others, which the JSON output writes as `null`, as for every unreachable vertex.
- **The Laplacian's comments describe another algorithm.** They announce ["inverse power"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L400) iteration, then power iteration on a shifted matrix [with Gram–Schmidt deflation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L417), while the code runs the full Jacobi method, O(n³) operations per sweep. Self-loops and edges out of range are [skipped without a word](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L436). Since the eigenvalues are clamped at 0, `spectral_gap`, μ_2 − μ_1, is μ_2 up to rounding and repeats `algebraic_connectivity`. Nothing outside `physics.rs` calls the function, and no MCP tool exposes it.
- **Components are counted with an absolute threshold.** An eigenvalue counts as zero below [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L462). A connected graph with diameter D has μ_2 ≥ 4/(n · D) (Mohar 1991), and n · D ≤ n(n − 1) < 4 × 10^6 when n ≤ 2000, so no connected graph with at most 2000 vertices comes that low. Larger ones can: the path with n vertices has μ_2 = 4 sin²(π/(2n)), below 10^-6 from n = 3142 on, where it is 0.99974 × 10^-6, so the function would count a connected path of 3142 vertices as 2 components. A breadth-first search, as in [`connected_components`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L224), counts them exactly.
- **The Fiedler vector comes back even when it is not determined.** When μ_2 is repeated, the returned vector is one vector of the eigenspace, chosen by the rotations. On K_4 the transcription predicts (−0.2887, −0.2887, −0.2887, 0.866), that is (−1, −1, −1, 3)/√12. On the barbell without its bridge it predicts 1/√5 ≈ 0.4472 on the first clique and 0 on the second: a vector of the null space, which separates the cliques by zero and nonzero entries, not by sign. Nothing flags either case.
- **Some tests would pass on wrong code.** [`test_pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L574) runs a directed 3-cycle, on which the uniform vector is a fixed point for every α, and asserts equal ranks [within 0.01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L585): the transcription returns exactly 1/3 for α = 0.85, 0 and 1, and after 0 iterations. A PageRank that ignored α, dropped the jumps or never iterated would pass. [`test_laplacian_disconnected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L617) asserts [at least 2 components](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L621) for the edges 0–1 and 2–3, whose eigenvalues are 0, 0, 2 and 2: a threshold of 3 would report 4 components and still pass. [`test_laplacian_connected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L606) asserts μ_2 [above 0.5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L610) on K_4, where it is 4.
- **Other gaps.** There is no normalised Laplacian, no spectral clustering, no Cheeger constant, no weighted or personalised PageRank, no convergence test in PageRank or in the eigenvector centrality, no normalised betweenness, no shortest paths with negative weights, and no MCP operation for the centralities, the components or the Laplacian.

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

Show that at the fixed point of IX's PageRank, the sum s of the ranks satisfies s = (1 − α) + α (s − x_D), where x_D is the total rank of the dangling nodes, and check it on the citation graph.

> *Solution:* Each pass sets every vertex to (1 − α)/n plus the shares it receives. Summed over the n vertices, the first terms give 1 − α, and the shares give α times the rank of the vertices with out-links, since such a vertex passes on α times all its rank, while a dangling node passes on nothing: α (s − x_D). At the fixed point, s = (1 − α) + α (s − x_D), so s = 1 − α x_D/(1 − α): with α = 0.85, the sum falls short of 1 by 17/3 ≈ 5.67 times the rank of the dangling nodes. On the citation graph x_D = 0.135, and s = 1 − (17/3) · 0.135 = 1 − 0.765 = 0.235.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **The leak.** Call `graph_ops` with the operation `pagerank` on the citation graph of §2, then `ix_pagerank` in an in-process DuckDB connection on the same edges. Prediction: 0.05, 0.05 and 0.135, summing to 0.235; then 10/47, 10/47 and 27/47, about 0.2128, 0.2128 and 0.5745.
2. **Slow convergence.** Call `graph_ops` with `pagerank` on the star with three leaves, `directed` false, damping 0.99, and 100 then 2000 iterations. Prediction: 0.4077 for the hub, then 0.4987.
3. **The kite.** Build Krackhardt's kite and call the four centralities and `pagerank`. Prediction: degree and eigenvector centrality highest at Diane (3), closeness at Fernando and Garth (5 and 6), with 9/14, betweenness at Heather (7), with 14, and PageRank highest at Diane, with 0.1471.
4. **The shift.** Call `eigenvector_centrality` on the star with 30 and with 100 iterations, then on the triangle with the separate edge of §6. Prediction: a hub-to-leaf ratio of √3 ≈ 1.7321 both times, then scores of about 1.4 × 10^-18 on the edge.
5. **Spectra.** Call `compute_laplacian_spectrum` on the barbell of §5, on the barbell without its bridge, on the triangle 0–1–2 with the edge 3–4 and the isolated vertex 5, and on K_4. Prediction: 1 component, μ_2 = 0.2984 and a Fiedler vector of about ±0.3336 on the inner vertices and ±0.2341 on the ends of the bridge, with one sign per bell; 2 components and the vector of §6; 3 components; 1 component, μ_2 = 4 and the vector of §6.
6. **The mesh hub.** Call `mesh_correlate` on the three uncorrelated series of §6 with the default threshold of 0.5. Prediction: no edge, every betweenness 0, and `hub` = 2.
7. **Negative weights.** Call `graph_ops` with `dijkstra` from vertex 0 on the edges 0 → 1 of weight 2, 0 → 2 of weight 5 and 2 → 1 of weight −4, then, in a child process with a timeout of 10 seconds, on the single edge 0–1 of weight −1 with `directed` false. Prediction: the distances 0, 1 and 5; then the timeout fires.

### Practice Exercise

Why does step 1 not depend on the number of iterations, as long as there are at least 2, while step 2 needs thousands?

> *Solution:* The citation graph has no cycle. After one pass, the ranks of 0 and 1 are 0.05 for good, since nothing links to them, and after the second, the rank of 2 depends only on theirs: every later pass repeats the same values. The star is bipartite, so the error changes sign at each pass and its size shrinks by the factor α = 0.99 per pass. After 100 passes 0.99^100 ≈ 0.366 of the initial error remains, and after 2000 about 2 × 10^-9 of it.

---

## 8. Common Pitfalls

- **Reading a raw PageRank vector as a distribution.** With dangling nodes it sums to less than 1; divide by the sum, which gives PageRank with uniform jumps from them, and report how much rank they held.
- **Expecting edge weights to change IX's PageRank.** They do not; build the weighted transition probabilities yourself, or say that the ranking is unweighted.
- **Naming the most central vertex without naming the measure.** Degree, closeness, betweenness and eigenvector centrality answer different questions, and on the kite they pick three different vertices.
- **Comparing raw betweenness across graphs.** Divide by the number of pairs, (n − 1)(n − 2)/2 for an undirected graph, first.
- **Running power iteration with A on a bipartite graph.** Shift by the identity, or check for an oscillation of period 2, before trusting the result.
- **Trusting a fixed number of iterations with α close to 1.** The error bound is 2αᵏ; with α = 0.99, 100 passes are far from enough.
- **Counting components from eigenvalues.** An absolute threshold confuses large, weakly connected graphs with disconnected ones; a breadth-first search counts them exactly.
- **Reading a Fiedler vector when μ_2 is 0 or repeated.** It is then one vector of an eigenspace, and its signs mean nothing; check the multiplicity first.
- **Passing an undirected edge list to `ix_graph` without setting `directed` to false.** The handler then treats every edge as one-way.
- **Giving Dijkstra's algorithm negative weights.** Use Bellman–Ford instead; an undirected negative edge is already a negative cycle.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Adjacency matrix** | The matrix A with A_ij = 1, or a weight, for an edge from i to j, and 0 otherwise |
| **Degree** | The number of neighbours of a vertex, or the sum of the weights of its edges |
| **Perron vector** | The eigenvector with positive entries of the largest eigenvalue of the adjacency matrix of a connected graph |
| **Bipartite graph** | A graph whose vertices split into two sides with every edge between them; its spectrum is symmetric about 0 |
| **Damping factor** | The probability α that the random surfer follows a link instead of jumping |
| **Dangling node** | A vertex without out-links |
| **PageRank** | The stationary distribution of the Google matrix |
| **Betweenness centrality** | The sum, over the pairs of other vertices, of the fraction of their shortest paths that pass through a vertex |
| **Eigenvector centrality** | A vertex's entry in the Perron vector |
| **Laplacian** | L = D − A, whose quadratic form sums (x_i − x_j)² over the edges |
| **Algebraic connectivity** | The second smallest eigenvalue μ_2 of the Laplacian, positive exactly when the graph is connected |
| **Fiedler vector** | An eigenvector of μ_2, whose signs give a spectral split of the graph |

---

## Self-Check Assessment

**1. A colleague ranks the crates of a workspace with the PageRank of `ix_graph` on the graph of `ix_cargo_deps`, and finds that the ranks do not sum to 1. Is something broken?**
> Not necessarily. IX drops the rank of dangling nodes, and every crate without an IX dependency is one, so the raw vector sums to 1 − α x_D/(1 − α), where x_D is their total rank (§6). Dividing by the sum gives PageRank with uniform jumps from those crates (§2), which is what `ix_pagerank` returns. Also point out that the weights are ignored, and that the edges go from a crate to its dependencies, so the rank flows toward the crates that others depend on.

**2. Why does power iteration with A fail to find the eigenvector centrality of a star, and why does IX's iteration with A + I work although its comment gives the wrong reason?**
> A star is bipartite, so −λ_1 is an eigenvalue as well as λ_1, and the iterate alternates: from (1, 1, 1, 1) it is uniform again after every even number of steps. With A + I the eigenvalues become λ_i + 1, and since λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1: the Perron vector dominates strictly. The shifted eigenvalues are not all positive, as the comment claims, since one of the star's is 1 − √3; strict dominance in modulus is what the iteration needs.

**3. `compute_laplacian_spectrum` reports 2 components and returns a Fiedler vector. What do you check before using them?**
> Whether the graph is really disconnected: an eigenvalue counts as zero below an absolute 10^-6, which a connected path of 3142 vertices or more also reaches, so count the components by breadth-first search. If the graph is disconnected, μ_2 = 0 is repeated and the vector is one of many in the null space, whose signs mean nothing: split by components first, and take the Fiedler vector of each component.

**4. On Krackhardt's kite, which vertex is the most central?**
> It depends on the question. Diane has the most ties and the highest eigenvector centrality, Fernando and Garth are the closest to everyone, at 9/14, and Heather controls the only way to Ike and Jane, with betweenness 14. A report should name the measure and say why it fits the question.

**Pass criteria:** Describe a graph by A, D and L; define PageRank, its treatment of dangling nodes and the bound on its error; compute and compare the four centralities; prove that L is positive semidefinite and that its zero eigenvalues count the components; split a graph with the Fiedler vector and say when it is not determined; and trace where IX's comments, catalogue, handlers and tests promise more than the code delivers.

---

## Research Basis

- E. W. Dijkstra, "A note on two problems in connexion with graphs", *Numerische Mathematik* 1, 1959: the shortest-path algorithm
- P. Bonacich, "Factoring and weighting approaches to status scores and clique identification", *Journal of Mathematical Sociology* 2, 1972: eigenvector centrality
- D. B. Johnson, "A note on Dijkstra's shortest path algorithm", *Journal of the ACM* 20, 1973: exponential work with negative weights
- M. Fiedler, "Algebraic connectivity of graphs", *Czechoslovak Mathematical Journal* 23, 1973: the algebraic connectivity
- M. Fiedler, "A property of eigenvectors of nonnegative symmetric matrices and its application to graph theory", *Czechoslovak Mathematical Journal* 25, 1975: the connected sides of the Fiedler vector
- L. C. Freeman, "A set of measures of centrality based on betweenness", *Sociometry* 40, 1977: betweenness
- D. Krackhardt, "Assessing the political landscape: structure, cognition, and power in organizations", *Administrative Science Quarterly* 35, 1990: the kite
- B. Mohar, "Eigenvalues, diameter, and mean distance in graphs", *Graphs and Combinatorics* 7, 1991: the lower bound on μ_2
- S. Wasserman and K. Faust, *Social Network Analysis: Methods and Applications*, Cambridge University Press, 1994: centralities, and closeness on disconnected graphs
- F. R. K. Chung, *Spectral Graph Theory*, American Mathematical Society, 1997: the normalised Laplacian and Cheeger's inequality
- S. Brin and L. Page, "The anatomy of a large-scale hypertextual Web search engine", *Computer Networks and ISDN Systems* 30, 1998: PageRank
- L. Page, S. Brin, R. Motwani and T. Winograd, "The PageRank citation ranking: bringing order to the Web", Stanford InfoLab technical report, 1999: the random surfer and the damping factor
- J. Shi and J. Malik, "Normalized cuts and image segmentation", *IEEE Transactions on Pattern Analysis and Machine Intelligence* 22, 2000: normalised cuts
- U. Brandes, "A faster algorithm for betweenness centrality", *Journal of Mathematical Sociology* 25, 2001: Brandes' algorithm
- A. Y. Ng, M. I. Jordan and Y. Weiss, "On spectral clustering: analysis and an algorithm", *Advances in Neural Information Processing Systems* 14, 2002: spectral clustering
- T. H. Haveliwala and S. D. Kamvar, "The second eigenvalue of the Google matrix", Stanford University technical report, 2003: the second eigenvalue is at most α in modulus
- A. N. Langville and C. D. Meyer, *Google's PageRank and Beyond: The Science of Search Engine Rankings*, Princeton University Press, 2006: dangling nodes and the linear-system form
- U. von Luxburg, "A tutorial on spectral clustering", *Statistics and Computing* 17, 2007: spectral clustering and the graph Laplacians
- A. E. Brouwer and W. H. Haemers, *Spectra of Graphs*, Springer, 2012: spectra of adjacency matrices and Laplacians
- R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013: the Perron–Frobenius theorem
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
