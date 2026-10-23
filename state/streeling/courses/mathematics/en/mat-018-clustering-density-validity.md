---
module_id: mat-018-clustering-density-validity
department: mathematics
course: Clustering, Density and Cluster Validity
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-013-distances-kernels-psd]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Clustering, Density and Cluster Validity — What k-means Minimises, What EM Guarantees, and When Scores Mislead

> **Department of Mathematics** | Stage: Albedo (Intermediate) | Estimated duration: 50 minutes

## Objectives

After this lesson, you will be able to:
- State the objective k-means minimises, and show why Lloyd's algorithm stops at a fixed point that depends on the start
- Define density-based clusters, with core points, border points and noise, and say what ε and minPts control
- Derive EM for a Gaussian mixture, prove that the log-likelihood never decreases, and explain why the likelihood itself has no maximum
- Compute the silhouette score, and say what it rewards
- Build cases where inertia, likelihood and silhouette all prefer the wrong partition
- Trace what IX's `KMeans`, `DBSCAN`, `GMM` and `silhouette_score` guarantee, and where their comments, handlers and tests promise more than the code delivers

---

## 1. What k-means Minimises

Given points x_1, …, x_n in ℝ^p and a number k, k-means looks for a partition C_1, …, C_k and centres μ_1, …, μ_k that minimise the **inertia**, the within-cluster sum of squares W = Σ_c Σ_(i∈C_c) ‖x_i − μ_c‖². For a fixed partition, the best centre of each cluster is its mean, and then W = Σ_c (1/(2|C_c|)) Σ_(i,j∈C_c) ‖x_i − x_j‖²: k-means rewards clusters whose points are close to one another in the Euclidean distance of MAT-013, whatever their shape. For fixed centres, the best partition sends each point to its nearest centre, so the clusters are the cells of a Voronoi diagram, and two clusters are separated by the perpendicular bisector of their centres, a hyperplane.

**Lloyd's algorithm** (Lloyd 1982) alternates these two steps. Neither can increase W, and there are finitely many partitions, so with a fixed rule for ties the iteration reaches a partition that the next step leaves unchanged. That fixed point need not be the global minimum, nor even a local minimum for moving a single point to another cluster (the rectangle below shows both): minimising W is NP-hard, already for k = 2 when the dimension is part of the input (Aloise et al. 2009).

For a worked example, take the four corners of a 4 × 1 rectangle, (0, 0), (0, 1), (4, 0) and (4, 1), with k = 2. The split into a left and a right pair has centres (0, 1/2) and (4, 1/2), and W = 4 · (1/2)² = 1. The split into a bottom and a top pair has centres (2, 0) and (2, 1), and W = 4 · 2² = 16; it is also a fixed point, since each corner is at squared distance 4 from its own centre and 5 from the other. Yet moving the single corner (0, 0) to the top pair lowers W to 34/3 ≈ 11.3: the top pair's mean moves toward the new point, which Lloyd's assignment step, comparing distances to the current centres, does not take into account. Which fixed point Lloyd reaches depends on the start. **k-means++** (Arthur and Vassilvitskii 2007) draws the first centre uniformly and each next one with probability proportional to D(x)², the squared distance from x to the nearest centre already chosen. From (0, 0), the other corners have D² = 1, 16 and 17, so the bad second centre (0, 1) has probability 1/34, against 1/3 for a uniform draw; by symmetry the same holds from every corner. In expectation, the k-means++ start alone, before any Lloyd step, comes within a factor 8(ln k + 2) of the optimal inertia, and restarting from several seeds, as in the reproducible sampling of MAT-009, and keeping the lowest inertia lowers the risk further.

### Practice Exercise

Why can k-means with k = n reach zero inertia and still be meaningless?

> *Solution:* Every point becomes its own centroid, so W = 0. The optimal inertia can only fall as k grows: splitting a cluster in two and giving each half its own mean cannot increase W, since the old mean is still available to both halves. The inertia alone therefore cannot choose k, and its minimum over all k is the partition into singletons, which says nothing about the data.

---

## 2. Density-Based Clusters

DBSCAN (Ester, Kriegel, Sander and Xu 1996) defines clusters by density instead of centres. The ε-neighbourhood N_ε(x) is the set of data points within distance ε of x, x itself included. A point is a **core point** when N_ε(x) has at least minPts points. A point y is directly density-reachable from a core point x when y ∈ N_ε(x), and density-reachable when a chain of such steps leads from x to y. A **cluster** is a maximal set of points connected in this way through core points; its points that are not core points are **border points**, and the points that belong to no cluster are **noise**.

Which points are core points, how the core points group into clusters, and which points are noise do not depend on the order of the data. A border point, though, can lie within ε of core points of two different clusters; the definition allows it in both, and an implementation gives it to the cluster that reaches it first (Schubert et al. 2017). A cluster can have any shape, as long as it is connected through dense regions, but a single ε sets a single density threshold, so clusters of very different densities cannot all be found at once. Ester et al. suggest minPts = 4 for 2-dimensional data, and reading ε from the sorted distances of each point to its fourth nearest neighbour.

k-means cannot separate two interleaved half-moons, since its two clusters are always separated by a line (§5). DBSCAN can, when ε lies between the spacing of the points within a moon and the gap between the moons.

### Practice Exercise

Show that with minPts = 2, the DBSCAN clusters are the connected components, with at least two points, of the graph that joins points at distance at most ε, and that the other points are noise.

> *Solution:* With minPts = 2, a point is a core point exactly when some other point lies within ε. A border point would have to lie within ε of a core point while having no other point within ε, which is impossible, so there are no border points. Density-reachability through core points is then a path in the graph, so the clusters are its connected components with at least two points, and the isolated points are noise. These are the clusters of single-linkage hierarchical clustering cut at height ε, with the singletons called noise.

---

## 3. Gaussian Mixtures and EM

A Gaussian mixture models the density as p(x) = Σ_c π_c N(x; μ_c, Σ_c), with weights π_c ≥ 0 that sum to 1. Maximising the log-likelihood ℓ(θ) = Σ_i ln p(x_i) has no closed form, but it would have one if we knew which component produced each point. **EM** (Dempster, Laird and Rubin 1977) alternates two steps. The E-step computes the **responsibilities** r_ic = π_c N(x_i; μ_c, Σ_c)/p(x_i), the posterior probability that component c produced x_i. The M-step fits each component to the points weighted by their responsibilities: with N_c = Σ_i r_ic, it sets π_c = N_c/n, μ_c = Σ_i r_ic x_i/N_c, and Σ_c to the weighted covariance; for a diagonal covariance, each variance is Σ_i r_ic (x_ij − μ_cj)²/N_c.

The log-likelihood never decreases. For any weights q_ic ≥ 0 that sum to 1 over c, Jensen's inequality gives ln p(x_i) = ln Σ_c q_ic π_c N(x_i; μ_c, Σ_c)/q_ic ≥ Σ_c q_ic ln(π_c N(x_i; μ_c, Σ_c)/q_ic), with equality when q_ic = r_ic. The E-step makes this lower bound touch ℓ at the current θ, and the M-step maximises the bound over θ, so ℓ(θ_new) ≥ bound(θ_new) ≥ bound(θ_old) = ℓ(θ_old), a minorise–maximise step. The argument proves monotonicity only. Convergence of the iterates to a stationary point needs further conditions (Wu 1983), and a stationary point can be a saddle or a poor local maximum.

The likelihood itself has no maximum when the variances are free and k ≥ 2. Centre one component on a data point x_1 and let its variances shrink: its density at x_1 grows without bound, while a second component with a fixed positive weight, mean and variances keeps the density of every point above a positive bound, so ℓ → ∞ (McLachlan and Peel 2000). Implementations therefore floor the variances or add a prior, and the floor then decides how large ℓ can get. Data with repeated values make this concrete: a component that sits on a repeated value can keep a positive weight while the M-step drives its variance toward 0.

EM also treats the components symmetrically. Permuting them changes nothing, and two components that start with identical parameters keep them forever (exercise below). k-means is a limit of EM: with all covariances equal to σ²I and equal fixed weights, the responsibilities tend to hard nearest-centre assignments as σ → 0, and the M-step for the means becomes Lloyd's update (Bishop 2006).

### Practice Exercise

Show that if two components start with the same weight, mean and covariance, EM keeps them identical at every iteration.

> *Solution:* If components a and b have the same π, μ and Σ, then π_a N(x_i; μ_a, Σ_a) = π_b N(x_i; μ_b, Σ_b) for every i, so r_ia = r_ib. The M-step computes N_c, the mean and the covariance of each component from its own responsibilities with the same formulas, so it returns identical parameters again. By induction the two components stay identical, and the fit has in effect k − 1 components; only something outside EM, such as a different start, can separate them.

---

## 4. Scores of Cluster Validity

Without labels, the quality of a clustering must be judged from the data alone, by an **internal index**. The **silhouette** (Rousseeuw 1987) compares, for each point i, the mean distance a(i) to the other points of its cluster with the smallest mean distance b(i) to the points of another cluster: s(i) = (b(i) − a(i))/max(a(i), b(i)), which lies in [−1, 1], and a point alone in its cluster gets s(i) = 0 by convention. The silhouette score is the mean of s(i). It is high when the clusters are compact and far apart in Euclidean distance, which is also what the inertia rewards: it prefers round, well-separated clusters, and penalises a long, curved cluster whose ends are far from each other, even when that cluster is right.

Other internal indices encode other preferences. The Davies–Bouldin index (Davies and Bouldin 1979) and the Calinski–Harabasz index (Caliński and Harabasz 1974) compare the spread within clusters with the distances between their centres, and for mixtures the BIC (Schwarz 1978) subtracts from ℓ a penalty that grows with the number of parameters. None of them is neutral: each defines what a cluster is, and a partition can score well while missing the structure one cares about. When a ground truth exists, an **external index** such as the adjusted Rand index (Hubert and Arabie 1985) compares the partition with it directly.

Choosing k by an internal score has its own traps: the inertia always falls as k grows (§1), the log-likelihood of a mixture can grow without bound (§3), and a silhouette that counts DBSCAN's noise as a cluster scores the noise as if it were one (§6).

### Practice Exercise

For the points 0, 1 and 5 on a line, compute the silhouette score of the partitions {0, 1}{5}, {0}{1, 5} and {0, 5}{1}. Which one does it prefer, and what does it give for three singletons?

> *Solution:* For {0, 1}{5}: s(0) = (5 − 1)/5 = 4/5, s(1) = (4 − 1)/4 = 3/4 and s(5) = 0, so the score is 31/60 ≈ 0.517. For {0}{1, 5}: s(0) = 0, s(1) = (1 − 4)/4 = −3/4 and s(5) = (5 − 4)/5 = 1/5, so the score is −11/60 ≈ −0.183. For {0, 5}{1}: s(0) = (1 − 5)/5 = −4/5, s(5) = (4 − 5)/5 = −1/5 and s(1) = 0, so the score is −1/3 ≈ −0.333. The silhouette prefers {0, 1}{5}. For three singletons every s(i) is 0 by convention, so the score is 0; unlike the inertia, the silhouette does not reward the partition into singletons.

---

## 5. Two Moons

Take 20 points on each of two interleaved half-moons: moon A at (cos t_i, sin t_i) and moon B at (1 − cos t_i, 1/2 − sin t_i), with t_i = πi/19 for i = 0, …, 19. Within a moon, consecutive points are 2 sin(π/38) ≈ 0.165 apart, and the closest pair across the moons is about 0.503 apart. The ends of a moon, though, are 2 apart.

The transcription of IX's code (§6) predicts the following. IX's k-means handler, with its defaults of seed 42 and one start, splits the moons with a straight line and puts 11 of the 40 points in the other moon's cluster, with inertia 16.1871, against 25.4358 for the two moons themselves. Ten starts (n_init = 10) find a lower inertia, 16.1554 from seed 43, and still misplace 10 points. A two-component GMM with seed 42 misplaces 6. DBSCAN with minPts = 3 returns the two moons exactly, with no noise, at ε = 0.3, and at every ε from 0.166 to 0.503 in steps of 0.001; at 0.165 every point is noise, and at 0.504 the moons merge into one cluster.

The silhouette ranks the partitions the other way round: 0.2792 for the two moons, which is also DBSCAN's score, against 0.4694 for k-means with one start, 0.4728 with ten, and 0.4375 for the GMM. The inertia and the silhouette agree with each other, and both prefer a wrong partition. They are not miscomputed: a moon is long and curved, its ends are farther apart than many pairs of points from different moons, and by distance alone it is a poor cluster. A score measures agreement with its own idea of a cluster, not with the structure that produced the data.

### Practice Exercise

Show that no line separates the two moons, so that k-means with k = 2 cannot return them, whatever the start.

> *Solution:* Since t_(19−i) = π − t_i, the points B_i = (1 − cos t_i, 1/2 − sin t_i) and B_(19−i) = (1 + cos t_i, 1/2 − sin t_i) of moon B have the midpoint (1, 1/2 − sin t_i), which lies in the convex hull of moon B. For i = 0 it is (1, 1/2), and for i = 9 it is (1, 1/2 − sin(9π/19)) ≈ (1, −0.497). The point (1, 0) of moon A, at i = 0, lies on the segment between them, so in the convex hull of moon B. Two k-means clusters are the points on either side of the bisector of their centres, a closed half-plane and the open half-plane opposite, both convex. If moon B lay in one of them, so would its convex hull and the point (1, 0), which then could not lie in the other with the rest of moon A.

---

## 6. Where IX Stands

IX is the Rust machine-learning library of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d); this lesson documents that code and does not change it, and it has not run IX or its tests. The numbers attributed to IX's behaviour come from a line-by-line transcription of `KMeans`, `DBSCAN`, `GMM`, `silhouette_score` and their MCP handlers into Python, with a replica of rand 0.9's `StdRng` (ChaCha12, seeded through PCG32) that reproduces the crate's own draws, `random_range` included. IX computes distances with sequential sums, as the transcription does; a few ndarray sums can differ in the last bits. The discrete decisions behind every stated prediction, such as a k-means++ draw, an assignment, a stopping test or an ε test, have margins far above those bits, except three near-ties among the ten k-means starts of §5, which lead to the same inertia either way. These numbers are predictions, and §7 proposes to check them.

**k-means** (`crates/ix-unsupervised`). [`KMeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L25) runs [one k-means++ start](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L23) from [seed 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L40), with at most [300 iterations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L38). The first centre comes from [`random_range`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L95), and an empty cluster [keeps its centroid](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L159). The MCP handler [`kmeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L303) defaults to [100 iterations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L313), runs `n_init` starts from the seeds seed, seed + 1, … and [keeps the lowest inertia](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L351), as the test [`kmeans_n_init_keeps_the_lowest_inertia_start`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L937) checks. The later centres come from the D² draw of §1:

```rust
            // Weighted random selection
            let total: f64 = distances.sum();
            let mut r = rng.random::<f64>() * total;
            for i in 0..n {
                r -= distances[i];
                if r <= 0.0 {
                    centroids.row_mut(c).assign(&x.row(i));
                    break;
                }
            }
```

**GMM** (`crates/ix-unsupervised`). [`GMM`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L10) has [diagonal covariances only](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L19), starts every variance at the [variance of the data](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L109) and every weight at [1/k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L116), and stops when ℓ changes by less than [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L28). Its means start at k data rows:

```rust
        // Initialize with K-Means++ style: pick k random points as means
        use rand::Rng;
        let indices: Vec<usize> = {
            let mut idxs = Vec::with_capacity(self.k);
            for _ in 0..self.k {
                let mut idx = rng.random_range(0..n);
                while idxs.contains(&idx) {
                    idx = rng.random_range(0..n);
                }
                idxs.push(idx);
            }
            idxs
        };
```

**DBSCAN and the silhouette.** [`DBSCAN`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L14) labels clusters 1, 2, … and [noise 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L4), counts a point in its own neighbourhood, and follows §2. Its handler rejects [ε ≤ 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L427) and [minPts < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L443). [`silhouette_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L26) computes Rousseeuw's definition exactly, with s(i) = 0 for a singleton.

- **The k-means tolerance is in squared units of the data.** The stopping test compares the [squared shift of the centroids](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L164) with [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L39), with a strict `<`. Lloyd's iteration reaches an exact fixed point, where the shift is exactly 0, so on data of ordinary size the tolerance rarely matters. On small numbers it does: a shift of δ counts as δ², so on the moons of §5 multiplied by 10^-6, the transcription predicts a stop after the first iteration, with an inertia of 20.1421 in the units of the original moons instead of 16.1871, and a silhouette of 0.4248 instead of 0.4694. Multiplied by 10^-3, the run is unchanged.
- **The k-means handler does not check k.** The schema asks for [k ≥ 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L104), but `ix-agent` has no JSON Schema validator among its dependencies, and the handler [reads k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L307) without checking it, unlike `n_init` and unlike the GMM handler, which rejects [k < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L662). With k = 0, `init_centroids` [assigns row 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L96) of a centroid array with no rows, and ndarray panics on that index.
- **DBSCAN's `predict` does not do what its comment says.** The comment says that `predict` assigns a new point to ["the nearest core point's cluster,"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L112) but the [condition](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L129) accepts any training point within ε whose label is not noise, border points included. The [`fit_predict` override](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L149) returns the labels of `fit` instead, so the handler, which [calls it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L450), is not affected; `predict` on new data is. On the data of IX's own test [`fit_predict_returns_canonical_fit_labels_not_predict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L290), with ε = 1 and minPts = 4, `fit` labels the point [(2.2, 0)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L297) noise, while `predict` puts a new point at the same place in cluster 1, because it lies within ε of the border point (1.3, 0).
- **The GMM start is not k-means++, and distinct rows are not distinct points.** The comment says ["K-Means++ style"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L89), but the code above draws k distinct row indices uniformly; when k > n the loop never ends, which the handler prevents by [rejecting k > n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L665) and the library does not. Two distinct rows with equal values start two components with the same mean, the same variance and the same weight, and by §3 they stay identical. On the ten ratings 1, 2, 2, 3, 3, 3, 4, 4, 5, 5 with k = 2, the transcription predicts this for 15 of the seeds 0 to 99: two identical components with mean 3.2 and variance 1.56, every point labelled 0, after 2 iterations.
- **The variance floor decides the likelihood.** The M-step [floors each variance at 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L171), and guards keep the arithmetic finite: the E-step [normalises a row only if its sum exceeds 10^-300](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L138), N_c is [floored at 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L149), and ℓ floors [the density of each point](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L63) at 10^-300. While those guards stay inactive, the loop is exact EM for diagonal Gaussians whose variances are held at 10^-6 or more, since clamping a variance to the floor is the constrained M-step, and ℓ cannot decrease. The degeneracy of §3 remains. On the ten ratings, 76 of the seeds 0 to 99, seed 42 included, are predicted to put one component on the two 5s, with variance exactly 10^-6, weight 0.19994 for seed 42, and ℓ = −4.1192, against −16.4128 for the identical components and −15.86 or −15.85 for the 9 fits with two proper components. The collapsed fit wins because its density at 5 is about 0.2/√(2π · 10^-6) ≈ 79.8; a floor 100 times smaller would add about ln 10 ≈ 2.30 for each of the two 5s.
- **The log-likelihood test does not test EM.** [`test_gmm_log_likelihood_increases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L249) fits the same data with [one iteration](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L259) and with [at most 50](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L263), and asserts that the second log-likelihood is [not below the first minus 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L267). The transcription predicts −19.5684 after one iteration and −7.1398 after three, when the fit stops. An M-step that returned its input unchanged would give equal values and pass: the test checks neither that EM improves anything nor that ℓ never decreases along the iterations.
- **The GMM handler accepts malformed values silently.** It reads [`seed`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L671) and `max_iter` with a fallback to the default, so a negative or non-integer value becomes 42 or 100 without an error, where the k-means handler [rejects it](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L322). A `max_iter` of 0, below the schema's [minimum of 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L499), returns the starting parameters without any EM step.
- **The silhouette counts DBSCAN's noise as a cluster.** The silhouette schema suggests feeding it the labels of k-means or DBSCAN: ["wire the `labels` output of kmeans/dbscan"](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L325). The score treats label 0 like any other, and so does the handler's [cluster count](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L540). Add four outliers at (−1.5, 1.5), (2.5, 1.5), (−1.5, −1) and (2.5, −1) to the moons of §5: DBSCAN with ε = 0.3 and minPts = 3 returns the two moons and labels the outliers noise, and the silhouette handler then reports 3 clusters and a score of 0.2126, against 0.2792 once the noise is left out. scikit-learn's `silhouette_score` has the same convention; the pipeline has to drop the noise first, and report how much it dropped.
- **Other gaps.** There is no Davies–Bouldin or Calinski–Harabasz index, no BIC or AIC, no kernel density estimate, no OPTICS or HDBSCAN, no full covariance and no restart for the GMM, and no external index: IX's embedding diagnostics note that [there is no native adjusted Rand index](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-embedding-diagnostics/src/main.rs#L799). For k = n the silhouette returns 0 where scikit-learn raises an error, as its documentation [states](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L8).

Fixing any of this is for IX's owners; this lesson only describes it.

### Practice Exercise

On the rectangle of §1, why does the D² draw give the bad start with probability 1/34 whichever corner comes first, and what does the loop above do when every remaining distance is 0?

> *Solution:* The rectangle's two mirror symmetries and their product preserve distances and map any corner to any other, so from every first corner the other three have D² = 1, 16 and 17, and only the corner at distance 1 leads to the bottom–top split: 1/(1 + 16 + 17) = 1/34. When every distance is 0, for instance when k exceeds the number of distinct points, total is 0, so r = 0, and the first pass through the loop meets r ≤ 0 and picks row 0, which may already be a centre. IX's test of the empty cluster relies on this: with the values 10, 10, 14, 14 and k = 3, the third centre is row 0, at 10, and its cluster stays empty.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for the Learn lab, which pins IX at the same commit. Nothing in it is a measurement: the predictions are written down before any run, and a later version of this lesson will report the results. Every step runs in the lab's own process and calls the functions directly, never a running MCP server.

1. **The rectangle.** Call the k-means handler on the rectangle of §1 with k = 2 and the seeds 0 to 999. Prediction: 26 runs end at inertia 16, starting with the seeds 3, 22 and 55, and the others at 1; the expected number is 1000/34 ≈ 29.4.
2. **Two moons, k-means.** Build the moons of §5 and call the k-means handler with k = 2, then with n_init = 10. Prediction: inertia 16.1871 with 11 points misplaced, then 16.1554 with 10.
3. **Two moons, DBSCAN.** Call the DBSCAN handler on the moons with min_points = 3 and ε = 0.165, 0.166, 0.3, 0.503 and 0.504. Prediction: all noise at 0.165; the two moons and no noise at 0.166, 0.3 and 0.503; one cluster at 0.504.
4. **Scores.** Call the silhouette handler on the moons with the true labels, the labels of step 2 with one start, and those of the GMM handler with k = 2. Prediction: 0.2792, 0.4694 and 0.4375.
5. **Noise.** Add the four outliers of §6, call the DBSCAN handler with ε = 0.3 and min_points = 3, and pass its labels to the silhouette handler unchanged, then without the noise rows. Prediction: `n_noise` 4 and `n_clusters` 2; then 3 clusters and 0.2126, and 2 clusters and 0.2792.
6. **Degenerate mixtures.** Call the GMM handler on the ten ratings of §6 with k = 2 and the seeds 0 to 99. Prediction: 76 fits with a variance of exactly 10^-6 at mean 5, 15 with two identical components of mean 3.2 and variance 1.56, and 9 with two proper components.
7. **DBSCAN's `predict`.** Fit `DBSCAN` with ε = 1 and minPts = 4 on the six points of its test, and call `predict` on the point (2.2, 0). Prediction: `fit` labels it 0 and `predict` returns 1.

### Practice Exercise

In step 6, why do the collapsed fits have the highest log-likelihood, and why should that not make them the preferred model?

> *Solution:* A component on the two 5s has density π/√(2πσ²) at 5, which grows without bound as σ² shrinks (§3). IX stops it at σ² = 10^-6, where the density is about 79.8 with π ≈ 0.2, so each 5 contributes about ln 79.8 ≈ 4.38 to ℓ, where a proper component gives each point a negative contribution. That gain comes from the floor, not from the data: a smaller floor would give a larger ℓ, without limit. The ratings are discrete, and a density model can give them unbounded likelihood by piling mass on repeated values. A comparison by ℓ, or by the BIC, whose penalty is the same for every fit with two components, would pick the degenerate fit.

---

## 8. Common Pitfalls

- **Reading clusters into k-means output on curved or elongated data.** Its clusters are Voronoi cells; check with a method that allows other shapes, or on data with a known structure.
- **Choosing k by the inertia alone.** It always falls as k grows, down to 0 at k = n.
- **Trusting one start.** Run several seeds, keep the lowest inertia, and look at how much the partitions differ.
- **Scoring DBSCAN output with the noise as a cluster.** Drop the noise rows before computing an internal index, and report how many there were.
- **Comparing mixtures by their log-likelihood when a variance can collapse.** Check the smallest variance and the weight of its component, and floor or regularise the variances in the units of the data.
- **Taking a high silhouette as proof of structure.** It rewards round, separated clusters; on the moons it prefers the wrong partition.
- **Using an absolute tolerance on data in arbitrary units.** Rescale the data first, or use a relative rule.
- **Ignoring the order of the rows in DBSCAN.** Border points go to the first cluster that reaches them; report them separately when they matter.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Inertia** | The within-cluster sum of squared distances to the cluster means, which k-means minimises |
| **Lloyd's algorithm** | Alternating nearest-centre assignment and mean update until the partition stops changing |
| **k-means++** | A start that draws each new centre with probability proportional to its squared distance to the nearest centre already chosen |
| **Core point** | A point with at least minPts points, itself included, within distance ε |
| **Border point** | A point of a DBSCAN cluster that is not a core point |
| **Noise** | A point that belongs to no DBSCAN cluster |
| **Responsibility** | The posterior probability that a mixture component produced a point |
| **EM** | Alternating responsibilities and weighted maximum likelihood, which never decreases the log-likelihood |
| **Degenerate component** | A mixture component whose variance shrinks toward 0 on a few points, along which the likelihood grows without bound |
| **Silhouette** | The mean over points of (b − a)/max(a, b), comparing distances within and between clusters |
| **Internal index** | A score of a clustering computed from the data alone |
| **External index** | A score comparing a clustering with known labels, such as the adjusted Rand index |

---

## Self-Check Assessment

**1. A colleague runs k-means with k = 2 on two interleaved arcs and reports a silhouette of 0.47 as evidence of two clusters. What do you answer?**
> That the silhouette and the inertia share k-means' idea of a cluster, compact and round, so a high score says the partition suits that idea, not that it recovers the arcs. On the moons of §5, k-means scores 0.4694 while misplacing 11 of 40 points, and the true moons score 0.2792. Ask for a method that allows curved clusters, such as DBSCAN with ε between the spacing and the gap, and for a comparison with known structure, by an external index, where one exists.

**2. Why can EM's log-likelihood never decrease, and why does that not make the fit good?**
> Each E-step builds a lower bound that touches ℓ at the current parameters, and each M-step maximises it, so ℓ cannot fall. But a non-decreasing ℓ can converge to a saddle or a poor local maximum, and ℓ itself has no maximum when a variance can shrink onto a point: IX's fits on the ten ratings of §6 reach their highest ℓ by collapsing a component onto the two 5s.

**3. IX's DBSCAN handler reports 2 clusters and 4 noise points, and the silhouette handler, fed the same labels, reports 3 clusters. Why?**
> DBSCAN labels noise 0, and the silhouette treats label 0 as a cluster like any other, as scikit-learn does. The 4 scattered noise points form a third, very loose "cluster", which lowers the score from 0.2792 to 0.2126 on the moons of §6. Drop the noise rows first, and report their number.

**4. Why do repeated values in the data threaten a Gaussian mixture fit, and what does IX's floor do about it?**
> A component can sit on a repeated value with a positive weight while its variance goes to 0, and its density there, so ℓ, grows without bound. IX's floor of 10^-6 stops the collapse at a finite ℓ, but then the floor, stated in squared units of the data, decides how large ℓ gets, and the collapsed fit still has the highest ℓ.

**Pass criteria:** State the k-means objective and why Lloyd stops at a start-dependent fixed point, define DBSCAN's core points, border points and noise, derive EM and its monotonicity and say why the likelihood has no maximum, compute a silhouette by hand, show on the two moons that internal scores can prefer the wrong partition, and trace where IX's comments, handlers and tests promise more than the code delivers.

---

## Research Basis

- T. Caliński and J. Harabasz, "A dendrite method for cluster analysis", *Communications in Statistics* 3, 1974: the Calinski–Harabasz index
- A. P. Dempster, N. M. Laird and D. B. Rubin, "Maximum likelihood from incomplete data via the EM algorithm", *Journal of the Royal Statistical Society, Series B* 39, 1977: EM and its monotonicity
- G. Schwarz, "Estimating the dimension of a model", *Annals of Statistics* 6, 1978: the BIC
- D. L. Davies and D. W. Bouldin, "A cluster separation measure", *IEEE Transactions on Pattern Analysis and Machine Intelligence* 1, 1979: the Davies–Bouldin index
- S. P. Lloyd, "Least squares quantization in PCM", *IEEE Transactions on Information Theory* 28, 1982: Lloyd's algorithm
- C. F. J. Wu, "On the convergence properties of the EM algorithm", *Annals of Statistics* 11, 1983: convergence of the iterates
- L. Hubert and P. Arabie, "Comparing partitions", *Journal of Classification* 2, 1985: the adjusted Rand index
- P. J. Rousseeuw, "Silhouettes: a graphical aid to the interpretation and validation of cluster analysis", *Journal of Computational and Applied Mathematics* 20, 1987: the silhouette
- M. Ester, H.-P. Kriegel, J. Sander and X. Xu, "A density-based algorithm for discovering clusters in large spatial databases with noise", *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining*, 1996: DBSCAN
- G. McLachlan and D. Peel, *Finite Mixture Models*, Wiley, 2000: unbounded likelihood and degenerate components
- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006: k-means as a limit of EM
- D. Arthur and S. Vassilvitskii, "k-means++: the advantages of careful seeding", *Proceedings of the ACM-SIAM Symposium on Discrete Algorithms*, 2007: k-means++ and its guarantee
- D. Aloise, A. Deshpande, P. Hansen and P. Popat, "NP-hardness of Euclidean sum-of-squares clustering", *Machine Learning* 75, 2009: NP-hardness for k = 2
- E. Schubert, J. Sander, M. Ester, H.-P. Kriegel and X. Xu, "DBSCAN revisited, revisited: why and how you should (still) use DBSCAN", *ACM Transactions on Database Systems* 42, 2017: border points and the choice of parameters
- IX source at commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d`: every code fact in §6 links to its line
- Experiment: proposed in §7, not run; this lesson contains no measurement
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
