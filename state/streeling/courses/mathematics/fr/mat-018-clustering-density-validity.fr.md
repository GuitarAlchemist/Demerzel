---
module_id: mat-018-clustering-density-validity
department: mathematics
course: Partitionnement, densité et validité des clusters
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-013-distances-kernels-psd]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Partitionnement, densité et validité des clusters — Ce que minimise k-means, ce que garantit l'EM, et quand les scores trompent

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Énoncer l'objectif que minimise k-means, et montrer pourquoi l'algorithme de Lloyd s'arrête en un point fixe qui dépend du départ
- Définir les clusters fondés sur la densité, avec points cœurs, points frontières et bruit, et dire ce que contrôlent ε et minPts
- Déduire l'EM pour un mélange gaussien, prouver que la log-vraisemblance ne diminue jamais, et expliquer pourquoi la vraisemblance elle-même n'a pas de maximum
- Calculer le score de silhouette, et dire ce qu'il récompense
- Construire des cas où l'inertie, la vraisemblance et la silhouette préfèrent toutes la mauvaise partition
- Retracer ce que garantissent `KMeans`, `DBSCAN`, `GMM` et `silhouette_score` d'IX, et où leurs commentaires, leurs gestionnaires et leurs tests promettent plus que ce que le code fournit

---

## 1. Ce que minimise k-means

Étant donnés des points x_1, …, x_n de ℝ^p et un nombre k, k-means cherche une partition C_1, …, C_k et des centres μ_1, …, μ_k qui minimisent l'**inertie**, la somme des carrés intra-cluster W = Σ_c Σ_(i∈C_c) ‖x_i − μ_c‖². Pour une partition fixée, le meilleur centre de chaque cluster est sa moyenne, et alors W = Σ_c (1/(2|C_c|)) Σ_(i,j∈C_c) ‖x_i − x_j‖² : k-means récompense les clusters dont les points sont proches les uns des autres pour la distance euclidienne du MAT-013, quelle que soit leur forme. Pour des centres fixés, la meilleure partition envoie chaque point à son centre le plus proche, de sorte que les clusters sont les cellules d'un diagramme de Voronoï, et deux clusters sont séparés par la médiatrice de leurs centres, un hyperplan.

**L'algorithme de Lloyd** (Lloyd 1982) alterne ces deux étapes. Aucune ne peut augmenter W, et les partitions sont en nombre fini, donc, avec une règle fixe pour les égalités, l'itération atteint une partition que l'étape suivante laisse inchangée. Ce point fixe n'est pas forcément le minimum global, ni même un minimum local pour le déplacement d'un seul point vers un autre cluster (le rectangle ci-dessous montre les deux) : minimiser W est NP-difficile, déjà pour k = 2 quand la dimension fait partie de l'entrée (Aloise et al. 2009).

Pour un exemple chiffré, prenons les quatre coins d'un rectangle 4 × 1, (0, 0), (0, 1), (4, 0) et (4, 1), avec k = 2. La partition en une paire gauche et une paire droite a pour centres (0, 1/2) et (4, 1/2), et W = 4 · (1/2)² = 1. La partition en une paire du bas et une paire du haut a pour centres (2, 0) et (2, 1), et W = 4 · 2² = 16 ; c'est aussi un point fixe, puisque chaque coin est à distance au carré 4 de son propre centre et 5 de l'autre. Pourtant, déplacer le seul coin (0, 0) vers la paire du haut fait baisser W à 34/3 ≈ 11,3 : la moyenne de la paire du haut se rapproche du nouveau point, ce dont l'étape d'affectation de Lloyd, qui compare les distances aux centres courants, ne tient pas compte. Le point fixe qu'atteint Lloyd dépend du départ. **k-means++** (Arthur et Vassilvitskii 2007) tire le premier centre uniformément, et chaque suivant avec une probabilité proportionnelle à D(x)², le carré de la distance de x au plus proche centre déjà choisi. Depuis (0, 0), les autres coins ont D² = 1, 16 et 17, donc le mauvais deuxième centre (0, 1) a une probabilité 1/34, contre 1/3 pour un tirage uniforme ; par symétrie, il en va de même depuis chaque coin. En espérance, le départ k-means++ seul, avant toute étape de Lloyd, arrive à un facteur 8(ln k + 2) de l'inertie optimale, et relancer depuis plusieurs graines, comme dans l'échantillonnage reproductible du MAT-009, en gardant l'inertie la plus basse, réduit encore le risque.

### Exercice pratique

Pourquoi k-means avec k = n peut-il atteindre une inertie nulle tout en étant dénué de sens ?

> *Solution :* Chaque point devient son propre centroïde, donc W = 0. L'inertie optimale ne peut que baisser quand k croît : couper un cluster en deux et donner à chaque moitié sa propre moyenne ne peut pas augmenter W, puisque l'ancienne moyenne reste disponible pour les deux moitiés. L'inertie seule ne peut donc pas choisir k, et son minimum sur tous les k est la partition en singletons, qui ne dit rien des données.

---

## 2. Clusters fondés sur la densité

DBSCAN (Ester, Kriegel, Sander et Xu 1996) définit les clusters par la densité plutôt que par des centres. Le ε-voisinage N_ε(x) est l'ensemble des points des données à distance au plus ε de x, x compris. Un point est un **point cœur** quand N_ε(x) compte au moins minPts points. Un point y est directement atteignable par densité depuis un point cœur x quand y ∈ N_ε(x), et atteignable par densité quand une chaîne de tels pas mène de x à y. Un **cluster** est un ensemble maximal de points reliés de cette façon à travers des points cœurs ; ceux de ses points qui ne sont pas des points cœurs sont des **points frontières**, et les points qui n'appartiennent à aucun cluster sont du **bruit**.

Quels points sont des points cœurs, comment les points cœurs se regroupent en clusters, et quels points sont du bruit ne dépend pas de l'ordre des données. Un point frontière, en revanche, peut se trouver à distance au plus ε de points cœurs de deux clusters différents ; la définition l'admet dans les deux, et une implémentation le donne au cluster qui l'atteint en premier (Schubert et al. 2017). Un cluster peut avoir n'importe quelle forme, pourvu qu'il soit connexe à travers des régions denses, mais un seul ε fixe un seul seuil de densité, de sorte que des clusters de densités très différentes ne peuvent pas tous être trouvés à la fois. Ester et al. suggèrent minPts = 4 pour des données en dimension 2, et de lire ε sur les distances triées de chaque point à son quatrième plus proche voisin.

k-means ne peut pas séparer deux demi-lunes entrelacées, puisque ses deux clusters sont toujours séparés par une droite (§5). DBSCAN le peut, quand ε se situe entre l'espacement des points au sein d'une lune et l'écart entre les lunes.

### Exercice pratique

Montrer qu'avec minPts = 2, les clusters de DBSCAN sont les composantes connexes, d'au moins deux points, du graphe qui relie les points à distance au plus ε, et que les autres points sont du bruit.

> *Solution :* Avec minPts = 2, un point est un point cœur exactement quand un autre point se trouve à distance au plus ε. Un point frontière devrait se trouver à distance au plus ε d'un point cœur sans avoir aucun autre point à distance au plus ε, ce qui est impossible, donc il n'y a pas de points frontières. L'atteignabilité par densité à travers des points cœurs est alors un chemin dans le graphe, de sorte que les clusters sont ses composantes connexes d'au moins deux points, et les points isolés sont du bruit. Ce sont les clusters de la classification hiérarchique à lien simple coupée à la hauteur ε, les singletons étant appelés bruit.

---

## 3. Mélanges gaussiens et EM

Un mélange gaussien modélise la densité par p(x) = Σ_c π_c N(x; μ_c, Σ_c), avec des poids π_c ≥ 0 de somme 1. Maximiser la log-vraisemblance ℓ(θ) = Σ_i ln p(x_i) n'a pas de forme close, mais en aurait une si l'on savait quelle composante a produit chaque point. **L'EM** (Dempster, Laird et Rubin 1977) alterne deux étapes. L'étape E calcule les **responsabilités** r_ic = π_c N(x_i; μ_c, Σ_c)/p(x_i), la probabilité a posteriori que la composante c ait produit x_i. L'étape M ajuste chaque composante aux points pondérés par leurs responsabilités : avec N_c = Σ_i r_ic, elle pose π_c = N_c/n, μ_c = Σ_i r_ic x_i/N_c, et Σ_c égale à la covariance pondérée ; pour une covariance diagonale, chaque variance vaut Σ_i r_ic (x_ij − μ_cj)²/N_c.

La log-vraisemblance ne diminue jamais. Pour tous poids q_ic ≥ 0 de somme 1 sur c, l'inégalité de Jensen donne ln p(x_i) = ln Σ_c q_ic π_c N(x_i; μ_c, Σ_c)/q_ic ≥ Σ_c q_ic ln(π_c N(x_i; μ_c, Σ_c)/q_ic), avec égalité quand q_ic = r_ic. L'étape E fait toucher ℓ à ce minorant au θ courant, et l'étape M maximise le minorant en θ, donc ℓ(θ_new) ≥ minorant(θ_new) ≥ minorant(θ_old) = ℓ(θ_old), un pas de minoration–maximisation. L'argument ne prouve que la monotonie. La convergence des itérés vers un point stationnaire demande d'autres conditions (Wu 1983), et un point stationnaire peut être un point selle ou un mauvais maximum local.

La vraisemblance elle-même n'a pas de maximum quand les variances sont libres et k ≥ 2. Centrons une composante sur un point des données x_1 et faisons tendre ses variances vers 0 : sa densité en x_1 croît sans borne, tandis qu'une seconde composante de poids strictement positif, de moyenne et de variances fixés maintient la densité de chaque point au-dessus d'une borne positive, donc ℓ → ∞ (McLachlan et Peel 2000). Les implémentations imposent donc un plancher aux variances ou ajoutent un a priori, et le plancher décide alors jusqu'où ℓ peut monter. Des données à valeurs répétées rendent cela concret : une composante posée sur une valeur répétée peut garder un poids positif tandis que l'étape M pousse sa variance vers 0.

L'EM traite aussi les composantes de façon symétrique. Les permuter ne change rien, et deux composantes qui partent de paramètres identiques les gardent pour toujours (exercice ci-dessous). k-means est une limite de l'EM : avec toutes les covariances égales à σ²I et des poids égaux et fixés, les responsabilités tendent vers des affectations strictes au centre le plus proche quand σ → 0, et l'étape M pour les moyennes devient la mise à jour de Lloyd (Bishop 2006).

### Exercice pratique

Montrer que si deux composantes partent du même poids, de la même moyenne et de la même covariance, l'EM les garde identiques à chaque itération.

> *Solution :* Si les composantes a et b ont les mêmes π, μ et Σ, alors π_a N(x_i; μ_a, Σ_a) = π_b N(x_i; μ_b, Σ_b) pour tout i, donc r_ia = r_ib. L'étape M calcule N_c, la moyenne et la covariance de chaque composante à partir de ses propres responsabilités avec les mêmes formules, donc elle renvoie de nouveau des paramètres identiques. Par récurrence, les deux composantes restent identiques, et l'ajustement n'a en fait que k − 1 composantes ; seul quelque chose d'extérieur à l'EM, comme un autre départ, peut les séparer.

---

## 4. Scores de validité des clusters

Sans étiquettes, la qualité d'un partitionnement doit se juger à partir des seules données, par un **indice interne**. La **silhouette** (Rousseeuw 1987) compare, pour chaque point i, la distance moyenne a(i) aux autres points de son cluster avec la plus petite distance moyenne b(i) aux points d'un autre cluster : s(i) = (b(i) − a(i))/max(a(i), b(i)), qui est dans [−1, 1], et un point seul dans son cluster reçoit s(i) = 0 par convention. Le score de silhouette est la moyenne des s(i). Il est élevé quand les clusters sont compacts et éloignés pour la distance euclidienne, ce que récompense aussi l'inertie : il préfère des clusters ronds et bien séparés, et pénalise un cluster long et courbe dont les extrémités sont loin l'une de l'autre, même quand ce cluster est le bon.

D'autres indices internes encodent d'autres préférences. L'indice de Davies–Bouldin (Davies et Bouldin 1979) et l'indice de Calinski–Harabasz (Caliński et Harabasz 1974) comparent la dispersion au sein des clusters aux distances entre leurs centres, et pour les mélanges le BIC (Schwarz 1978) retranche de ℓ une pénalité qui croît avec le nombre de paramètres. Aucun n'est neutre : chacun définit ce qu'est un cluster, et une partition peut obtenir un bon score tout en manquant la structure qui compte. Quand une vérité de terrain existe, un **indice externe** comme l'indice de Rand ajusté (Hubert et Arabie 1985) compare directement la partition avec elle.

Choisir k par un score interne a ses propres pièges : l'inertie baisse toujours quand k croît (§1), la log-vraisemblance d'un mélange peut croître sans borne (§3), et une silhouette qui compte le bruit de DBSCAN comme un cluster le note comme s'il en était un (§6).

### Exercice pratique

Pour les points 0, 1 et 5 sur une droite, calculer le score de silhouette des partitions {0, 1}{5}, {0}{1, 5} et {0, 5}{1}. Laquelle préfère-t-il, et que donne-t-il pour trois singletons ?

> *Solution :* Pour {0, 1}{5} : s(0) = (5 − 1)/5 = 4/5, s(1) = (4 − 1)/4 = 3/4 et s(5) = 0, donc le score vaut 31/60 ≈ 0,517. Pour {0}{1, 5} : s(0) = 0, s(1) = (1 − 4)/4 = −3/4 et s(5) = (5 − 4)/5 = 1/5, donc le score vaut −11/60 ≈ −0,183. Pour {0, 5}{1} : s(0) = (1 − 5)/5 = −4/5, s(5) = (4 − 5)/5 = −1/5 et s(1) = 0, donc le score vaut −1/3 ≈ −0,333. La silhouette préfère {0, 1}{5}. Pour trois singletons, chaque s(i) vaut 0 par convention, donc le score vaut 0 ; contrairement à l'inertie, la silhouette ne récompense pas la partition en singletons.

---

## 5. Deux lunes

Prenons 20 points sur chacune de deux demi-lunes entrelacées : la lune A en (cos t_i, sin t_i) et la lune B en (1 − cos t_i, 1/2 − sin t_i), avec t_i = πi/19 pour i = 0, …, 19. Au sein d'une lune, deux points consécutifs sont à 2 sin(π/38) ≈ 0,165 l'un de l'autre, et la paire la plus proche entre les lunes est à environ 0,503. Les extrémités d'une lune, en revanche, sont à 2 l'une de l'autre.

La transcription du code d'IX (§6) prédit ce qui suit. Le gestionnaire k-means d'IX, avec ses valeurs par défaut de graine 42 et d'un seul départ, coupe les lunes par une droite et place 11 des 40 points dans le cluster de l'autre lune, avec une inertie de 16,1871, contre 25,4358 pour les deux lunes elles-mêmes. Dix départs (n_init = 10) trouvent une inertie plus basse, 16,1554 depuis la graine 43, et placent encore mal 10 points. Un GMM à deux composantes avec la graine 42 en place mal 6. DBSCAN avec minPts = 3 renvoie exactement les deux lunes, sans bruit, à ε = 0,3, et à chaque ε de 0,166 à 0,503 par pas de 0,001 ; à 0,165 chaque point est du bruit, et à 0,504 les lunes fusionnent en un seul cluster.

La silhouette classe les partitions dans l'autre sens : 0,2792 pour les deux lunes, qui est aussi le score de DBSCAN, contre 0,4694 pour k-means avec un départ, 0,4728 avec dix, et 0,4375 pour le GMM. L'inertie et la silhouette s'accordent entre elles, et toutes deux préfèrent une mauvaise partition. Elles ne sont pas mal calculées : une lune est longue et courbe, ses extrémités sont plus éloignées que bien des paires de points de lunes différentes, et à la seule aune de la distance c'est un mauvais cluster. Un score mesure l'accord avec sa propre idée d'un cluster, pas avec la structure qui a produit les données.

### Exercice pratique

Montrer qu'aucune droite ne sépare les deux lunes, de sorte que k-means avec k = 2 ne peut pas les renvoyer, quel que soit le départ.

> *Solution :* Comme t_(19−i) = π − t_i, les points B_i = (1 − cos t_i, 1/2 − sin t_i) et B_(19−i) = (1 + cos t_i, 1/2 − sin t_i) de la lune B ont pour milieu (1, 1/2 − sin t_i), qui est dans l'enveloppe convexe de la lune B. Pour i = 0 c'est (1, 1/2), et pour i = 9 c'est (1, 1/2 − sin(9π/19)) ≈ (1 ; −0,497). Le point (1, 0) de la lune A, en i = 0, est sur le segment qui les joint, donc dans l'enveloppe convexe de la lune B. Deux clusters de k-means sont les points de part et d'autre de la médiatrice de leurs centres, un demi-plan fermé et le demi-plan ouvert opposé, tous deux convexes. Si la lune B était dans l'un d'eux, son enveloppe convexe et le point (1, 0) y seraient aussi, et celui-ci ne pourrait alors pas être dans l'autre avec le reste de la lune A.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de `KMeans`, `DBSCAN`, `GMM`, `silhouette_score` et de leurs gestionnaires MCP en Python, avec une réplique du `StdRng` de rand 0.9 (ChaCha12, amorcé par PCG32) qui reproduit les tirages de la crate elle-même, `random_range` compris. IX calcule les distances par des sommes séquentielles, comme la transcription ; quelques sommes de ndarray peuvent différer dans les derniers bits. Les décisions discrètes derrière chaque prédiction énoncée, comme un tirage de k-means++, une affectation, un test d'arrêt ou un test sur ε, ont des marges bien au-dessus de ces bits, sauf trois quasi-égalités parmi les dix départs de k-means du §5, qui mènent à la même inertie dans les deux cas. Ces nombres sont des prédictions, que le §7 propose de vérifier.

**k-means** (`crates/ix-unsupervised`). [`KMeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L25) exécute [un seul départ k-means++](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L23) depuis [la graine 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L40), avec au plus [300 itérations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L38). Le premier centre vient de [`random_range`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L95), et un cluster vide [garde son centroïde](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L159). Le gestionnaire MCP [`kmeans`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L303) prend par défaut [100 itérations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L313), exécute `n_init` départs depuis les graines seed, seed + 1, … et [garde l'inertie la plus basse](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L351), comme le vérifie le test [`kmeans_n_init_keeps_the_lowest_inertia_start`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L937). Les centres suivants viennent du tirage en D² du §1 :

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

**GMM** (`crates/ix-unsupervised`). [`GMM`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L10) n'a que des [covariances diagonales](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L19), initialise chaque variance à la [variance des données](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L109) et chaque poids à [1/k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L116), et s'arrête quand ℓ varie de moins de [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L28). Ses moyennes partent de k lignes des données :

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

**DBSCAN et la silhouette.** [`DBSCAN`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L14) étiquette les clusters 1, 2, … et [le bruit 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L4), compte un point dans son propre voisinage, et suit le §2. Son gestionnaire rejette [ε ≤ 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L427) et [minPts < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L443). [`silhouette_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L26) calcule exactement la définition de Rousseeuw, avec s(i) = 0 pour un singleton.

- **La tolérance de k-means est en unités des données au carré.** Le test d'arrêt compare le [déplacement au carré des centroïdes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L164) à [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L39), avec un `<` strict. L'itération de Lloyd atteint un point fixe exact, où le déplacement vaut exactement 0, donc sur des données de taille ordinaire la tolérance importe rarement. Sur de petits nombres, elle importe : un déplacement de δ compte pour δ², de sorte que sur les lunes du §5 multipliées par 10^-6, la transcription prédit un arrêt après la première itération, avec une inertie de 20,1421 dans les unités des lunes d'origine au lieu de 16,1871, et une silhouette de 0,4248 au lieu de 0,4694. Avec un facteur 10^-3, l'exécution est inchangée.
- **Le gestionnaire k-means ne vérifie pas k.** Le schéma demande [k ≥ 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L104), mais `ix-agent` n'a aucun validateur de JSON Schema parmi ses dépendances, et le gestionnaire [lit k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L307) sans le vérifier, contrairement à `n_init` et contrairement au gestionnaire GMM, qui rejette [k < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L662). Avec k = 0, `init_centroids` [affecte la ligne 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kmeans.rs#L96) d'un tableau de centroïdes sans aucune ligne, et ndarray panique sur cet indice.
- **Le `predict` de DBSCAN ne fait pas ce que dit son commentaire.** Le commentaire dit que `predict` affecte un nouveau point à [« the nearest core point's cluster, »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L112) mais la [condition](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L129) accepte n'importe quel point d'entraînement à distance au plus ε dont l'étiquette n'est pas le bruit, points frontières compris. La [surcharge de `fit_predict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L149) renvoie à la place les étiquettes de `fit`, de sorte que le gestionnaire, qui [l'appelle](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L450), n'est pas affecté ; `predict` sur de nouvelles données l'est. Sur les données du propre test d'IX [`fit_predict_returns_canonical_fit_labels_not_predict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L290), avec ε = 1 et minPts = 4, `fit` étiquette le point [(2,2 ; 0)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/dbscan.rs#L297) comme bruit, tandis que `predict` place un nouveau point au même endroit dans le cluster 1, parce qu'il est à distance au plus ε du point frontière (1,3 ; 0).
- **Le départ du GMM n'est pas k-means++, et des lignes distinctes ne sont pas des points distincts.** Le commentaire dit [« K-Means++ style »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L89), mais le code ci-dessus tire uniformément k indices de lignes distincts ; quand k > n, la boucle ne termine jamais, ce que le gestionnaire empêche en [rejetant k > n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L665) et que la bibliothèque n'empêche pas. Deux lignes distinctes de valeurs égales font partir deux composantes avec la même moyenne, la même variance et le même poids, et d'après le §3 elles restent identiques. Sur les dix notes 1, 2, 2, 3, 3, 3, 4, 4, 5, 5 avec k = 2, la transcription le prédit pour 15 des graines 0 à 99 : deux composantes identiques de moyenne 3,2 et de variance 1,56, chaque point étiqueté 0, après 2 itérations.
- **Le plancher de variance décide de la vraisemblance.** L'étape M [impose à chaque variance un plancher de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L171), et des garde-fous maintiennent l'arithmétique finie : l'étape E [ne normalise une ligne que si sa somme dépasse 10^-300](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L138), N_c a un [plancher de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L149), et ℓ impose un plancher de 10^-300 à [la densité de chaque point](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L63). Tant que ces garde-fous restent inactifs, la boucle est un EM exact pour des gaussiennes diagonales dont les variances sont maintenues à 10^-6 ou plus, puisque ramener une variance au plancher est l'étape M contrainte, et ℓ ne peut pas diminuer. La dégénérescence du §3 demeure. Sur les dix notes, 76 des graines 0 à 99, dont la graine 42, posent d'après la prédiction une composante sur les deux 5, avec une variance d'exactement 10^-6, un poids de 0,19994 pour la graine 42, et ℓ = −4,1192, contre −16,4128 pour les composantes identiques et −15,86 ou −15,85 pour les 9 ajustements à deux composantes propres. L'ajustement effondré l'emporte parce que sa densité en 5 vaut environ 0,2/√(2π · 10^-6) ≈ 79,8 ; un plancher 100 fois plus petit ajouterait environ ln 10 ≈ 2,30 pour chacun des deux 5.
- **Le test de log-vraisemblance ne teste pas l'EM.** [`test_gmm_log_likelihood_increases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L249) ajuste les mêmes données avec [une itération](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L259) et avec [au plus 50](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L263), et affirme que la seconde log-vraisemblance [n'est pas inférieure à la première moins 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/gmm.rs#L267). La transcription prédit −19,5684 après une itération et −7,1398 après trois, quand l'ajustement s'arrête. Une étape M qui renverrait son entrée inchangée donnerait des valeurs égales et passerait : le test ne vérifie ni que l'EM améliore quoi que ce soit, ni que ℓ ne diminue jamais au fil des itérations.
- **Le gestionnaire GMM accepte silencieusement des valeurs malformées.** Il lit [`seed`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L671) et `max_iter` avec un repli sur la valeur par défaut, de sorte qu'une valeur négative ou non entière devient 42 ou 100 sans erreur, là où le gestionnaire k-means [la rejette](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L322). Un `max_iter` de 0, sous le [minimum de 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L499) du schéma, renvoie les paramètres de départ sans aucune étape de l'EM.
- **La silhouette compte le bruit de DBSCAN comme un cluster.** Le schéma de la silhouette suggère de lui fournir les étiquettes de k-means ou de DBSCAN : [« wire the `labels` output of kmeans/dbscan »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L325). Le score traite l'étiquette 0 comme n'importe quelle autre, tout comme le [décompte des clusters](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L540) du gestionnaire. Ajoutons quatre points aberrants en (−1,5 ; 1,5), (2,5 ; 1,5), (−1,5 ; −1) et (2,5 ; −1) aux lunes du §5 : DBSCAN avec ε = 0,3 et minPts = 3 renvoie les deux lunes et étiquette les points aberrants comme bruit, et le gestionnaire de silhouette rapporte alors 3 clusters et un score de 0,2126, contre 0,2792 une fois le bruit écarté. Le `silhouette_score` de scikit-learn a la même convention ; le pipeline doit d'abord retirer le bruit, et indiquer combien il en a retiré.
- **Autres lacunes.** Il n'y a ni indice de Davies–Bouldin ou de Calinski–Harabasz, ni BIC ou AIC, ni estimateur de densité à noyau, ni OPTICS ou HDBSCAN, ni covariance pleine ni redémarrage pour le GMM, ni indice externe : les diagnostics d'embeddings d'IX notent qu'[il n'y a pas d'indice de Rand ajusté natif](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-embedding-diagnostics/src/main.rs#L799). Pour k = n, la silhouette renvoie 0 là où scikit-learn lève une erreur, comme sa documentation l'[indique](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/eval/silhouette.rs#L8).

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Sur le rectangle du §1, pourquoi le tirage en D² donne-t-il le mauvais départ avec une probabilité 1/34 quel que soit le premier coin, et que fait la boucle ci-dessus quand toutes les distances restantes sont nulles ?

> *Solution :* Les deux symétries axiales du rectangle et leur composée préservent les distances et envoient n'importe quel coin sur n'importe quel autre, donc depuis chaque premier coin les trois autres ont D² = 1, 16 et 17, et seul le coin à distance 1 mène à la partition bas–haut : 1/(1 + 16 + 17) = 1/34. Quand toutes les distances sont nulles, par exemple quand k dépasse le nombre de points distincts, total vaut 0, donc r = 0, et le premier passage dans la boucle rencontre r ≤ 0 et choisit la ligne 0, qui peut déjà être un centre. Le test d'IX sur le cluster vide repose là-dessus : avec les valeurs 10, 10, 14, 14 et k = 3, le troisième centre est la ligne 0, en 10, et son cluster reste vide.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Le rectangle.** Appeler le gestionnaire k-means sur le rectangle du §1 avec k = 2 et les graines 0 à 999. Prédiction : 26 exécutions finissent à une inertie de 16, à commencer par les graines 3, 22 et 55, et les autres à 1 ; le nombre attendu est 1000/34 ≈ 29,4.
2. **Deux lunes, k-means.** Construire les lunes du §5 et appeler le gestionnaire k-means avec k = 2, puis avec n_init = 10. Prédiction : une inertie de 16,1871 avec 11 points mal placés, puis 16,1554 avec 10.
3. **Deux lunes, DBSCAN.** Appeler le gestionnaire DBSCAN sur les lunes avec min_points = 3 et ε valant 0,165 ; 0,166 ; 0,3 ; 0,503 et 0,504. Prédiction : tout est du bruit à 0,165 ; les deux lunes et aucun bruit à 0,166, à 0,3 et à 0,503 ; un seul cluster à 0,504.
4. **Scores.** Appeler le gestionnaire de silhouette sur les lunes avec les vraies étiquettes, les étiquettes de l'étape 2 avec un départ, et celles du gestionnaire GMM avec k = 2. Prédiction : 0,2792 ; 0,4694 et 0,4375.
5. **Bruit.** Ajouter les quatre points aberrants du §6, appeler le gestionnaire DBSCAN avec ε = 0,3 et min_points = 3, et passer ses étiquettes au gestionnaire de silhouette telles quelles, puis sans les lignes de bruit. Prédiction : `n_noise` à 4 et `n_clusters` à 2 ; puis 3 clusters et 0,2126, et 2 clusters et 0,2792.
6. **Mélanges dégénérés.** Appeler le gestionnaire GMM sur les dix notes du §6 avec k = 2 et les graines 0 à 99. Prédiction : 76 ajustements avec une variance d'exactement 10^-6 en la moyenne 5, 15 avec deux composantes identiques de moyenne 3,2 et de variance 1,56, et 9 avec deux composantes propres.
7. **Le `predict` de DBSCAN.** Ajuster `DBSCAN` avec ε = 1 et minPts = 4 sur les six points de son test, et appeler `predict` sur le point (2,2 ; 0). Prédiction : `fit` l'étiquette 0 et `predict` renvoie 1.

### Exercice pratique

À l'étape 6, pourquoi les ajustements effondrés ont-ils la plus haute log-vraisemblance, et pourquoi cela ne devrait-il pas en faire le modèle préféré ?

> *Solution :* Une composante posée sur les deux 5 a une densité π/√(2πσ²) en 5, qui croît sans borne quand σ² diminue (§3). IX l'arrête à σ² = 10^-6, où la densité vaut environ 79,8 avec π ≈ 0,2, de sorte que chaque 5 apporte environ ln 79,8 ≈ 4,38 à ℓ, là où une composante propre donne à chaque point une contribution négative. Ce gain vient du plancher, pas des données : un plancher plus petit donnerait un ℓ plus grand, sans limite. Les notes sont discrètes, et un modèle de densité peut leur donner une vraisemblance non bornée en empilant de la masse sur des valeurs répétées. Une comparaison par ℓ, ou par le BIC, dont la pénalité est la même pour tout ajustement à deux composantes, choisirait l'ajustement dégénéré.

---

## 8. Pièges courants

- **Lire des clusters dans la sortie de k-means sur des données courbes ou allongées.** Ses clusters sont des cellules de Voronoï ; vérifier avec une méthode qui admet d'autres formes, ou sur des données de structure connue.
- **Choisir k d'après la seule inertie.** Elle baisse toujours quand k croît, jusqu'à 0 pour k = n.
- **Se fier à un seul départ.** Lancer plusieurs graines, garder l'inertie la plus basse, et regarder à quel point les partitions diffèrent.
- **Noter la sortie de DBSCAN avec le bruit comme cluster.** Retirer les lignes de bruit avant de calculer un indice interne, et indiquer combien il y en avait.
- **Comparer des mélanges par leur log-vraisemblance quand une variance peut s'effondrer.** Vérifier la plus petite variance et le poids de sa composante, et imposer un plancher aux variances ou les régulariser dans les unités des données.
- **Prendre une silhouette élevée pour une preuve de structure.** Elle récompense les clusters ronds et séparés ; sur les lunes, elle préfère la mauvaise partition.
- **Utiliser une tolérance absolue sur des données en unités arbitraires.** Remettre d'abord les données à l'échelle, ou utiliser une règle relative.
- **Ignorer l'ordre des lignes dans DBSCAN.** Les points frontières vont au premier cluster qui les atteint ; les signaler à part quand ils comptent.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Inertie** | La somme, sur les clusters, des carrés des distances aux moyennes des clusters, que minimise k-means |
| **Algorithme de Lloyd** | L'alternance de l'affectation au centre le plus proche et de la mise à jour des moyennes, jusqu'à ce que la partition cesse de changer |
| **k-means++** | Un départ qui tire chaque nouveau centre avec une probabilité proportionnelle au carré de sa distance au plus proche centre déjà choisi |
| **Point cœur** | Un point qui a au moins minPts points, lui compris, à distance au plus ε |
| **Point frontière** | Un point d'un cluster de DBSCAN qui n'est pas un point cœur |
| **Bruit** | Un point qui n'appartient à aucun cluster de DBSCAN |
| **Responsabilité** | La probabilité a posteriori qu'une composante du mélange ait produit un point |
| **EM** | L'alternance des responsabilités et du maximum de vraisemblance pondéré, qui ne diminue jamais la log-vraisemblance |
| **Composante dégénérée** | Une composante de mélange dont la variance tend vers 0 sur quelques points, ce qui fait croître la vraisemblance sans borne |
| **Silhouette** | La moyenne sur les points de (b − a)/max(a, b), qui compare les distances au sein des clusters et entre eux |
| **Indice interne** | Un score d'un partitionnement calculé à partir des seules données |
| **Indice externe** | Un score qui compare un partitionnement à des étiquettes connues, comme l'indice de Rand ajusté |

---

## Auto-évaluation

**1. Un collègue lance k-means avec k = 2 sur deux arcs entrelacés et présente une silhouette de 0,47 comme preuve de deux clusters. Que lui répondez-vous ?**
> Que la silhouette et l'inertie partagent l'idée que k-means se fait d'un cluster, compact et rond, de sorte qu'un score élevé dit que la partition convient à cette idée, pas qu'elle retrouve les arcs. Sur les lunes du §5, k-means obtient 0,4694 en plaçant mal 11 des 40 points, et les vraies lunes obtiennent 0,2792. Demander une méthode qui admet des clusters courbes, comme DBSCAN avec ε entre l'espacement et l'écart, et une comparaison avec une structure connue, par un indice externe, quand il en existe une.

**2. Pourquoi la log-vraisemblance de l'EM ne peut-elle jamais diminuer, et pourquoi cela ne rend-il pas l'ajustement bon ?**
> Chaque étape E construit un minorant qui touche ℓ aux paramètres courants, et chaque étape M le maximise, donc ℓ ne peut pas baisser. Mais un ℓ non décroissant peut converger vers un point selle ou un mauvais maximum local, et ℓ lui-même n'a pas de maximum quand une variance peut se resserrer sur un point : les ajustements d'IX sur les dix notes du §6 atteignent leur ℓ le plus haut en effondrant une composante sur les deux 5.

**3. Le gestionnaire DBSCAN d'IX rapporte 2 clusters et 4 points de bruit, et le gestionnaire de silhouette, avec les mêmes étiquettes, rapporte 3 clusters. Pourquoi ?**
> DBSCAN étiquette le bruit 0, et la silhouette traite l'étiquette 0 comme un cluster comme les autres, comme le fait scikit-learn. Les 4 points de bruit dispersés forment un troisième « cluster », très lâche, qui fait baisser le score de 0,2792 à 0,2126 sur les lunes du §6. Retirer d'abord les lignes de bruit, et indiquer leur nombre.

**4. Pourquoi des valeurs répétées dans les données menacent-elles l'ajustement d'un mélange gaussien, et que fait le plancher d'IX à ce sujet ?**
> Une composante peut se poser sur une valeur répétée avec un poids positif tandis que sa variance tend vers 0, et sa densité en ce point, donc ℓ, croît sans borne. Le plancher de 10^-6 d'IX arrête l'effondrement à un ℓ fini, mais c'est alors le plancher, exprimé en unités des données au carré, qui décide de la hauteur de ℓ, et l'ajustement effondré a toujours le ℓ le plus haut.

**Critères de réussite :** Énoncer l'objectif de k-means et pourquoi Lloyd s'arrête en un point fixe qui dépend du départ, définir les points cœurs, les points frontières et le bruit de DBSCAN, déduire l'EM et sa monotonie et dire pourquoi la vraisemblance n'a pas de maximum, calculer une silhouette à la main, montrer sur les deux lunes que des scores internes peuvent préférer la mauvaise partition, et retracer où les commentaires, les gestionnaires et les tests d'IX promettent plus que ce que le code fournit.

---

## Bases de recherche

- T. Caliński et J. Harabasz, « A dendrite method for cluster analysis », *Communications in Statistics* 3, 1974 : l'indice de Calinski–Harabasz
- A. P. Dempster, N. M. Laird et D. B. Rubin, « Maximum likelihood from incomplete data via the EM algorithm », *Journal of the Royal Statistical Society, Series B* 39, 1977 : l'EM et sa monotonie
- G. Schwarz, « Estimating the dimension of a model », *Annals of Statistics* 6, 1978 : le BIC
- D. L. Davies et D. W. Bouldin, « A cluster separation measure », *IEEE Transactions on Pattern Analysis and Machine Intelligence* 1, 1979 : l'indice de Davies–Bouldin
- S. P. Lloyd, « Least squares quantization in PCM », *IEEE Transactions on Information Theory* 28, 1982 : l'algorithme de Lloyd
- C. F. J. Wu, « On the convergence properties of the EM algorithm », *Annals of Statistics* 11, 1983 : la convergence des itérés
- L. Hubert et P. Arabie, « Comparing partitions », *Journal of Classification* 2, 1985 : l'indice de Rand ajusté
- P. J. Rousseeuw, « Silhouettes: a graphical aid to the interpretation and validation of cluster analysis », *Journal of Computational and Applied Mathematics* 20, 1987 : la silhouette
- M. Ester, H.-P. Kriegel, J. Sander et X. Xu, « A density-based algorithm for discovering clusters in large spatial databases with noise », *Proceedings of the Second International Conference on Knowledge Discovery and Data Mining*, 1996 : DBSCAN
- G. McLachlan et D. Peel, *Finite Mixture Models*, Wiley, 2000 : la vraisemblance non bornée et les composantes dégénérées
- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006 : k-means comme limite de l'EM
- D. Arthur et S. Vassilvitskii, « k-means++: the advantages of careful seeding », *Proceedings of the ACM-SIAM Symposium on Discrete Algorithms*, 2007 : k-means++ et sa garantie
- D. Aloise, A. Deshpande, P. Hansen et P. Popat, « NP-hardness of Euclidean sum-of-squares clustering », *Machine Learning* 75, 2009 : la NP-difficulté pour k = 2
- E. Schubert, J. Sander, M. Ester, H.-P. Kriegel et X. Xu, « DBSCAN revisited, revisited: why and how you should (still) use DBSCAN », *ACM Transactions on Database Systems* 42, 2017 : les points frontières et le choix des paramètres
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
