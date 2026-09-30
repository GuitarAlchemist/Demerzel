---
module_id: mat-015-classical-mds-distance-preservation
department: mathematics
course: MDS classique et préservation des distances
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# MDS classique et préservation des distances — Retrouver des points à partir de leurs distances, et savoir quand c'est impossible

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Transformer une matrice de distances en matrice de produits scalaires par double centrage, et expliquer pourquoi le résultat n'est fixé qu'à un mouvement rigide près
- Énoncer le critère de Schoenberg, Young et Householder : une matrice de distances est euclidienne exactement quand sa matrice doublement centrée est semi-définie positive
- Calculer une configuration de MDS classique, et montrer que sur des distances euclidiennes elle redonne les scores de l'ACP
- Reconnaître des dissimilarités non euclidiennes aux valeurs propres négatives de la matrice doublement centrée, et mesurer à quel point elles déforment la configuration
- Distinguer le MDS classique du MDS métrique par stress, du MDS non métrique et d'Isomap
- Retracer ce que garantit `classical_mds` d'IX, et où un écrêtage silencieux ou une tolérance absolue change la réponse

---

## 1. Des distances aux produits scalaires

Supposons que seules les distances dᵢⱼ entre n points soient connues, et non les points eux-mêmes. La loi des cosinus relie les distances aux produits scalaires : ‖xᵢ − xⱼ‖² = ‖xᵢ‖² + ‖xⱼ‖² − 2 xᵢ · xⱼ. Les produits scalaires dépendent de l'origine et les distances non, donc les distances déterminent les produits scalaires une fois l'origine choisie. Le positionnement classique choisit le centre de gravité x̄. Notons D⁽²⁾ la matrice des distances au carré d²ᵢⱼ, et J = I − (1/n) 11ᵀ la **matrice de centrage**. La **matrice doublement centrée** B = −½ J D⁽²⁾ J a pour coefficients bᵢⱼ = −½ (d²ᵢⱼ − rᵢ − rⱼ + g), où rᵢ est la moyenne de la ligne i de D⁽²⁾ et g la moyenne de tous ses coefficients, et elle est égale à la matrice de Gram des points centrés : bᵢⱼ = (xᵢ − x̄) · (xⱼ − x̄). Chaque ligne de B a une somme nulle, parce que les points centrés ont une somme nulle. Le centrage doit porter sur les distances au carré ; appliqué aux distances elles-mêmes, il n'a aucun sens géométrique.

Les distances ne changent pas quand on translate, fait tourner ou réfléchit les points, donc aucune méthode ne peut retrouver la configuration au-delà d'un tel **mouvement rigide**. Le double centrage élimine la translation en plaçant le centre de gravité à l'origine ; la rotation et la réflexion subsistent, et le §4 y revient.

### Exercice pratique

Trois points d'une droite sont à des distances mutuelles d₁₂ = 1, d₂₃ = 2 et d₁₃ = 3. Calculez B et retrouvez les points.

> *Solution :* D⁽²⁾ = [[0, 1, 9], [1, 0, 4], [9, 4, 0]], de moyennes de lignes 10/3, 5/3 et 13/3 et de moyenne globale 28/9. Alors b₁₁ = −½(0 − 20/3 + 28/9) = 16/9, et de la même façon B = xxᵀ avec x = (−4/3, −1/3, 5/3). B est de rang 1, d'unique valeur propre non nulle ‖x‖² = 14/3, donc les points sont sur une droite, en −4/3, −1/3 et 5/3 : les points 0, 1 et 3 décalés de leur moyenne 4/3. La réponse réfléchie (4/3, 1/3, −5/3) respecte les distances tout aussi bien.

---

## 2. Quand une matrice de distances est-elle euclidienne ?

Une matrice symétrique D de diagonale nulle et de coefficients positifs ou nuls est une **matrice de distances euclidienne** s'il existe des points x₁, …, xₙ d'un certain ℝᵐ avec dᵢⱼ = ‖xᵢ − xⱼ‖. Le critère de Schoenberg (1935) et de Young et Householder (1938) affirme qu'une telle D est euclidienne exactement quand B est semi-définie positive, et que la plus petite dimension m qui convient est le rang de B. Un sens est le §1 : une matrice de Gram est SDP (MAT-013). Pour l'autre, une matrice B SDP se factorise en B = YYᵀ avec Y = QΛ^(1/2) (MAT-005), et les lignes de Y sont des points aux bonnes distances, puisque bᵢᵢ + bⱼⱼ − 2bᵢⱼ = d²ᵢⱼ pour toute D symétrique de diagonale nulle, et que la racine carrée de d²ᵢⱼ est dᵢⱼ car dᵢⱼ ≥ 0. La condition de signe est indispensable : B ne voit que les carrés, donc [[0, −1], [−1, 0]] a la même matrice B semi-définie positive que [[0, 1], [1, 0]] et n'est pourtant pas une matrice de distances (§6).

Comme B1 = 0, et que Jx = x dès que les coordonnées de x ont une somme nulle, xᵀBx = −½ xᵀD⁽²⁾x pour de tels x : une D symétrique de diagonale nulle et de coefficients positifs ou nuls est euclidienne exactement quand xᵀD⁽²⁾x ≤ 0 pour tout x dont les coordonnées ont une somme nulle. Un seul vecteur x avec xᵀBx < 0 est un **témoin** qu'aucune configuration, en aucune dimension, n'a ces distances.

L'inégalité triangulaire est nécessaire mais pas suffisante. Dans un espace euclidien, l'égalité d(a, c) = d(a, b) + d(b, c) force b à se trouver sur le segment de a à c, aux distances prescrites des deux. Les distances de plus court chemin dans un graphe atteignent souvent cette égalité, et les contraintes peuvent alors se contredire.

### Exercice pratique

Le graphe étoile K₁,₃ a un centre relié à trois feuilles. Ses distances de plus court chemin valent 1 du centre à chaque feuille et 2 entre feuilles, et elles vérifient l'inégalité triangulaire. Sont-elles euclidiennes ?

> *Solution :* Non. Chaque paire de feuilles est à distance 2 = 1 + 1 en passant par le centre, donc dans un espace euclidien le centre serait le milieu de chaque paire de feuilles. Le milieu des feuilles 1 et 2 et celui des feuilles 1 et 3 ne coïncident que si les feuilles 2 et 3 coïncident, or elles sont à distance 2. En chiffres : D⁽²⁾ a pour moyennes de lignes 3/4 pour le centre et 9/4 pour les feuilles, et pour moyenne globale 15/8, donc le coefficient diagonal du centre dans B est b₀₀ = −½(0 − 3/2 + 15/8) = −3/16 < 0. Le vecteur unitaire e₀ est un témoin, et les valeurs propres de B sont 2, 2, 0 et −1/4.

---

## 3. MDS classique et ACP

Le **positionnement multidimensionnel classique** (Torgerson 1952), que Gower (1966) appelle analyse en coordonnées principales, calcule la décomposition propre B = QΛQᵀ avec λ₁ ≥ λ₂ ≥ …, garde les k plus grandes valeurs propres, et renvoie la configuration n × k Y = Q_kΛ_k^(1/2) : la ligne i contient les coordonnées du point i. Quand D est euclidienne, YYᵀ est la meilleure approximation de rang k de B en norme de Frobenius (Eckart–Young, MAT-006) ; en général, c'est la meilleure approximation semi-définie positive. Ce critère sur B, souvent appelé **strain**, est ce que le MDS classique optimise, plutôt que les distances elles-mêmes.

Quand D provient de points de matrice de données centrée X_c de taille n × p, B = X_cX_cᵀ. Avec la SVD X_c = UΣVᵀ du MAT-006, B = UΣ²Uᵀ, donc les valeurs propres non nulles de B sont les σᵢ², qui valent n − 1 fois les variances du MAT-014, et Y = U_kΣ_k = X_cV_k : le MDS classique redonne exactement les scores de l'ACP, au signe de chaque colonne près. Gower a décrit cette dualité entre les problèmes propres n × n et p × p. Le MDS est le choix naturel quand seules les distances sont connues, ou quand p est bien plus grand que n. L'ACP est moins coûteuse quand n est grand et p petit : son problème propre est p × p, et elle ne forme jamais les n² distances.

### Exercice pratique

Le MAT-014 a trouvé les variances 8/3 et 2/3 pour les quatre points (±2, 0) et (0, ±1). Quelles sont les valeurs propres de B pour ces points, et quelle configuration le MDS classique renvoie-t-il avec k = 2 ?

> *Solution :* Les points sont déjà centrés, donc B = X_cX_cᵀ, dont les valeurs propres non nulles sont celles de X_cᵀX_c = diag(8, 2) : n − 1 = 3 fois 8/3 et 2/3. Les deux autres valeurs propres sont nulles, puisque B est de rang 2. Les vecteurs propres sont (1, −1, 0, 0)/√2 pour 8 et (0, 0, 1, −1)/√2 pour 2, et les multiplier par √8 et √2 redonne les points (±2, 0) et (0, ±1), au signe de chaque coordonnée près.

---

## 4. Ce que les distances ne disent pas : mouvements rigides et égalités

La configuration renvoyée par le MDS classique est centrée, mais les données ne déterminent pas son orientation. Chaque vecteur propre peut être remplacé par son opposé, ce qui réfléchit la configuration. Quand deux valeurs propres sont égales, toute base orthonormée de leur espace propre en vaut une autre, donc la configuration peut tourner librement dans ce plan. Le carré unité est le cas le plus simple : sa matrice B a pour valeurs propres 1, 1, 0 et 0, et toute rotation du carré autour de son centre est une réponse également valide. Deux cartes MDS des mêmes données, issues de deux bibliothèques ou de deux exécutions, peuvent donc différer d'une rotation ou d'une réflexion sans que l'une soit fausse.

Pour comparer deux configurations Y₁ et Y₂, comparez leurs distances, ou alignez-les d'abord : la matrice orthogonale R qui minimise ‖Y₁ − Y₂R‖_F est R = WZᵀ, où Y₂ᵀY₁ = WΣZᵀ est une SVD (Schönemann 1966). Cet alignement de **Procrustes orthogonal** supprime exactement l'ambiguïté que laissent les distances.

### Exercice pratique

Pourquoi le MDS classique ne peut-il retrouver une configuration qu'à un mouvement rigide près, et quelle part de ce mouvement fixe-t-il ?

> *Solution :* Les translations, rotations et réflexions préservent toutes les distances, donc deux configurations reliées par l'une d'elles ont la même matrice de distances, et rien de ce qu'on calcule à partir des distances ne peut les distinguer. Le double centrage fixe la translation en plaçant le centre de gravité à l'origine. Le reste est laissé au solveur propre : le signe de chaque vecteur propre et, quand des valeurs propres sont égales comme pour le carré, le choix de la base dans leur espace propre.

---

## 5. Dissimilarités non euclidiennes, stress et Isomap

Quand B a des valeurs propres négatives, aucune configuration en aucune dimension ne reproduit D, et le MDS classique ne garde que des valeurs propres positives. Écarter les négatives change les distances, et leur taille mesure à quel point D est loin d'être euclidienne. Mardia (1978) a proposé la fraction Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ|, qui reste sous 1 dès que des valeurs propres négatives sont présentes. Un graphique de toutes les valeurs propres, négatives comprises, est le meilleur guide pour choisir k.

Le cycle C₄, quatre points en anneau avec des distances de plus court chemin de 1 entre voisins et de 2 en travers, est le plus petit exemple. Comme pour l'étoile, d(0, 2) = d(0, 1) + d(1, 2) et d(0, 2) = d(0, 3) + d(3, 2) feraient des points 1 et 3 tous deux le milieu de 0 et 2, or ils sont à distance 2. B a pour valeurs propres 2, 2, 0 et −1, et la fraction de Mardia pour k = 2 vaut 4/5.

Le MDS classique est un membre d'une famille. Le **MDS métrique** minimise un **stress**, par exemple Σ (dᵢⱼ − ‖yᵢ − yⱼ‖)², directement sur les distances et par itération ; SMACOF, qui procède par majoration, est l'algorithme de référence, et la solution classique est un point de départ courant (Borg et Groenen 2005). Le **MDS non métrique** (Kruskal 1964) n'utilise que l'ordre des dissimilarités : il ajuste une transformation monotone de celles-ci en même temps que la configuration, ce qui convient aux notes et aux classements dont les valeurs numériques signifient peu. **Isomap** (Tenenbaum, de Silva et Langford 2000) applique le MDS classique aux distances de plus court chemin d'un graphe de voisinage, pour déplier des données posées sur une surface courbe ; ces distances sont des distances de graphe et, comme celles de C₄, elles ne sont pas forcément euclidiennes.

### Exercice pratique

Pour C₄, calculez B, ses valeurs propres, et les distances de la configuration de MDS classique avec k = 2.

> *Solution :* Chaque ligne de D⁽²⁾ est une rotation de (0, 1, 4, 1), de moyenne 3/2, et la moyenne globale vaut 3/2, donc bᵢᵢ = 3/4, bᵢⱼ = 1/4 entre voisins et −5/4 en travers. Le vecteur (1, −1, 1, −1)/2 est un vecteur propre pour −1, le vecteur de uns pour 0, et le plan orthogonal aux deux porte la valeur propre double 2. Écarter −1 ajoute ¼ vvᵀ à B, avec v = (1, −1, 1, −1), ce qui donne des coefficients diagonaux 1, des coefficients 0 entre voisins et −1 en travers : la configuration est un carré de côté √2 ≈ 1,414 et de diagonale 2. Les distances en travers sont exactes, celles entre voisins sont étirées de 1 à 1,414, et la fraction de Mardia vaut 4/(2 + 2 + 0 + 1) = 4/5.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de `classical_mds`, `pairwise_euclidean` et `symmetric_eigen` en Python, dont les flottants sont en binary64 IEEE comme le `f64` de Rust : ce sont des prédictions, que le §7 propose de vérifier.

**MDS** (`crates/ix-unsupervised`). [`classical_mds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L49) rejette [k = 0 et k ≥ n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L60), élève l'entrée au carré après en avoir fait la moyenne avec sa transposée, la centre doublement avec la [formule du §1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L89), et passe B à [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L95), la méthode de Jacobi du MAT-005. Son seul appelant hors des tests est la fonction de table DuckDB `ix_mds_project`, qui [plafonne k](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L344) au nombre de variables et à n − 1, et [construit les distances](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/tablefn.rs#L345) à partir des vecteurs d'entrée avec `pairwise_euclidean` ; aucun outil MCP n'expose le MDS. Par les interfaces d'IX, le MDS classique ne voit donc que des distances euclidiennes calculées à partir de variables, où le §3 montre qu'il redonne les scores de l'ACP. La mise au carré et la configuration s'écrivent :

```rust
    // Square and symmetrize the distance matrix.
    let mut sq = Array2::<f64>::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            let d = 0.5 * (distances[[i, j]] + distances[[j, i]]);
            sq[[i, j]] = d * d;
        }
    }
```

```rust
    // Full symmetric eigendecomposition via ix-math::eigen — returns pairs
    // already sorted in descending order, so we just take the top k.
    let (eigenvalues, eigenvectors) = symmetric_eigen(&b)?;

    let mut embedding = Array2::<f64>::zeros((n, k));
    for r in 0..k {
        let lambda = eigenvalues[r].max(0.0);
        let scale = lambda.sqrt();
        for i in 0..n {
            embedding[[i, r]] = eigenvectors[[i, r]] * scale;
        }
    }
```

- **Une entrée non euclidienne est plongée sans signal.** La documentation du module dit que le MDS est [« a perfect fit »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L16) pour les [« Non-metric similarity data »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L17) et pour les [graphes par leurs distances de plus court chemin](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L18). La fonction ne signale jamais de valeur propre négative : elle [remplace chacune par 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L99) avant la racine carrée. Sur C₄ avec k = 2, elle renvoie le carré de côté √2 du §5, avec une erreur moyenne de distance de 2(√2 − 1)/3 ≈ 0,276 ; k = 3 donne les mêmes distances, puisque la troisième valeur propre est nulle. Sur l'étoile, avec k = 2 ou 3, les feuilles forment un triangle équilatéral de côté 2 et le centre se place en son centre de gravité, à 2/√3 ≈ 1,155 de chaque feuille au lieu de 1, soit une erreur moyenne d'environ 0,077. Sur le cycle à 6 sommets, dont la matrice B a pour valeurs propres 6, 6, 3/2, 0, −2 et −2, k = 5 renvoie une cinquième colonne de zéros. Des données non métriques, au sens de la méthode de Kruskal, demandent un ajustement aux rangs, que la fonction n'effectue pas ; elle traite chaque nombre comme une distance.
- **Les coefficients négatifs et asymétriques passent en silence.** La documentation dit que la fonction [« symmetrizes defensively »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L48). Elle [fait la moyenne de dᵢⱼ et dⱼᵢ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L71) quel que soit leur écart, et [élève le résultat au carré](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L72), donc un coefficient négatif perd son signe : [[0, −1], [−1, 0]] donne le même plongement ±0,5 que [[0, 1], [1, 0]], et une paire de coefficients 0 et 2 devient une distance de 1, sans erreur. Ni le signe, ni la symétrie, ni la diagonale nulle ne sont vérifiés.
- **Une tolérance absolue écrase les petites configurations.** `symmetric_eigen` s'arrête quand la norme hors diagonale est [sous 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47), un [test absolu](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82), comme le MAT-013 l'a montré pour le test SDP. Pour le carré unité mis à l'échelle s, les seuls coefficients hors diagonale de B sont −s²/2 en (0, 2) et (1, 3), de norme s²/√2. À s = 2^-19 ≈ 1,91 · 10^-6, deux rotations retrouvent le carré. À 2^-20 ≈ 9,54 · 10^-7 et en dessous, aucune rotation n'a lieu : les valeurs propres sont les coefficients diagonaux s²/2, les vecteurs propres sont des vecteurs de coordonnées, et avec k = 2 deux coins voisins se placent à s/√2 de l'origine, sur des axes différents, tandis que les deux autres se placent à l'origine. L'erreur moyenne de distance vaut alors 0,5 s, la moitié du côté. `ix_mds_project` calcule les mêmes distances, bit pour bit, à partir des coins du carré mis à l'échelle, donc des points distants d'environ un micromètre, avec des coordonnées en mètres, suffisent à le déclencher.
- **Les tests n'utilisent que des entrées euclidiennes.** Le [test du carré](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L150) exige une erreur moyenne [sous 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L162) là où l'erreur prédite est d'environ 1,5 · 10^-16, et le [test coplanaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/mds.rs#L166) utilise cinq points d'un plan. Aucun des cinq tests de `mds.rs` ne plonge une matrice non euclidienne ou une petite configuration, ni ne compare le résultat à l'ACP.
- **Le MDS classique seulement.** `crates/ix-unsupervised` n'offre ni minimisation du stress, ni SMACOF, ni MDS non métrique, ni Isomap ; la documentation ne mentionne Isomap que comme utilisateur du MDS.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

IX plonge l'étoile avec k = 2 et avec k = 3 et renvoie les mêmes distances. Pourquoi, et où va le centre ?

> *Solution :* B a pour valeurs propres 2, 2, 0 et −1/4. Avec k = 3, la troisième colonne vient de la valeur propre 0, à l'arrondi près, et son vecteur propre (1, 1, 1, 1)/2 décale chaque point de la même quantité infime, ce qui ne change aucune distance. La valeur propre −1/4 est écartée dans les deux cas, et rien dans le résultat ne le dit. L'écarter ajoute ¼ vvᵀ à B, avec v = (3, −1, −1, −1)/√12, ce qui annule la ligne du centre et donne aux feuilles bᵢᵢ = 4/3 et bᵢⱼ = −2/3 : les feuilles forment un triangle équilatéral de côté 2 autour de l'origine, et le centre est à l'origine, à 2/√3 ≈ 1,155 de chaque feuille. La fraction de Mardia, 4/(4 + 1/4) = 16/17 ≈ 0,941, aurait signalé la perte.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Entrée euclidienne.** Appeler `classical_mds` sur les distances des points 0, 1 et 3 avec k = 1, et sur `pairwise_euclidean` de (±2, 0) et (0, ±1) avec k = 2. Prédiction : ±(−4/3, −1/3, 5/3) à 10^-12 près, et les quatre points eux-mêmes, au signe de chaque colonne près, à 10^-12 près.
2. **Face à l'ACP.** Appeler `ix_mds_project` avec k = 2 sur les dix points du tutoriel de Lindsay Smith, et calculer les scores de l'ACP par la SVD des données centrées. Prédiction : les colonnes concordent au signe près à 10^-12 près.
3. **Le carré unité.** Appeler `classical_mds` avec k = 2 sur la matrice de distances de `test_mds_recovers_2d_square`. Prédiction : une erreur moyenne de distance sous 10^-15, d'environ 1,5 · 10^-16.
4. **Distances de graphe.** Appeler `classical_mds` sur C₄ et sur l'étoile avec k = 2 et k = 3, calculer leurs matrices B comme au §1, et les passer à `symmetric_eigen`. Prédiction : les valeurs propres du §5 et du §2 à 10^-12 près, négatives comprises ; pour C₄, un carré de côté √2 et une erreur moyenne d'environ 0,276 pour les deux valeurs de k ; pour l'étoile, des feuilles à distance 2, un centre à environ 1,155 de chacune, et une erreur moyenne d'environ 0,077. Sur le cycle à 6 sommets avec k = 5, une cinquième colonne de zéros.
5. **Entrée invalide.** Appeler `classical_mds` avec k = 1 sur [[0, −1], [−1, 0]], sur [[0, 1], [1, 0]] et sur [[0, 0], [2, 0]]. Prédiction : les trois renvoient `Ok`, avec le plongement ±0,5.
6. **L'échelle.** Appeler `classical_mds` avec k = 2 sur le carré unité mis à l'échelle 2^-19, 2^-20 et 2^-21, et `ix_mds_project` avec k = 2 sur les coins (0, 0), (s, 0), (s, s) et (0, s) pour s = 2^-19 et 2^-20. Prédiction : à 2^-19 le carré est retrouvé ; à 2^-20 et 2^-21, deux coins sont à l'origine et l'erreur moyenne vaut 0,5 s.

### Exercice pratique

Pour quels facteurs d'échelle s `symmetric_eigen` renvoie-t-il la diagonale de B inchangée pour le carré unité mis à l'échelle s, et pourquoi 2^-20 est-elle alors la première puissance de deux en échec ?

> *Solution :* B varie comme s², et ses coefficients hors diagonale valent −s²/2 en (0, 2) et (1, 3) et 0 ailleurs, donc la norme que la boucle compare à 10^-12 est √(2 · s⁴/4) = s²/√2. Elle est sous 10^-12 quand s < (√2 · 10^-12)^(1/2) ≈ 1,19 · 10^-6. La puissance 2^-20 ≈ 9,54 · 10^-7 est en dessous, alors que 2^-19 ≈ 1,91 · 10^-6 est au-dessus. Sous le seuil, les quatre valeurs propres valent toutes s²/2 à l'arrondi près, et les deux vecteurs propres gardés sont des vecteurs de coordonnées, qui laissent les deux autres coins à l'origine. Un test relatif, comparant la norme hors diagonale à la norme de B, ne dépendrait pas de s.

---

## 8. Pièges courants

- **Centrer les distances au lieu de leurs carrés.** Le double centrage transforme des distances au carré en produits scalaires ; appliqué aux distances brutes, il donne une matrice sans aucun sens géométrique.
- **Faire confiance à une carte construite sur des dissimilarités non euclidiennes.** Regardez les valeurs propres négatives de B avant de lire des distances sur l'image ; une valeur propre négative comparable aux valeurs gardées signifie que la carte déforme les données.
- **Tenir l'inégalité triangulaire pour suffisante.** Des distances de graphe, comme celles d'une étoile ou d'un cycle, la vérifient et ne sont pourtant pas euclidiennes.
- **Comparer deux cartes coordonnée par coordonnée.** Les signes et, pour des valeurs propres égales, des rotations entières sont arbitraires ; alignez les cartes par Procrustes, ou comparez les distances.
- **Appeler le MDS classique « MDS métrique » ou « MDS non métrique ».** Il minimise le strain sur B ; la minimisation du stress et les ajustements aux rangs sont des méthodes différentes, aux résultats différents sur des données non euclidiennes.
- **Demander plus de dimensions qu'il n'y a de valeurs propres positives.** Les colonnes en trop viennent de valeurs propres nulles ou de valeurs propres négatives écrêtées ; elles n'apportent rien.
- **Utiliser une tolérance absolue.** Un test d'arrêt qui ignore la taille de B fait dépendre la réponse des unités des distances.
- **Symétriser sans regarder.** Une « distance » négative ou fortement asymétrique est en général une erreur de données ; la moyenne et la mise au carré la cachent.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Matrice de centrage** | J = I − (1/n) 11ᵀ, qui soustrait la moyenne |
| **Matrice doublement centrée** | B = −½ J D⁽²⁾ J, la matrice de Gram des points centrés quand D est euclidienne |
| **Matrice de distances euclidienne** | Une matrice des distances entre des points d'un certain ℝᵐ |
| **Critère de Schoenberg** | Une D symétrique de diagonale nulle et de coefficients positifs ou nuls est euclidienne exactement quand B est semi-définie positive ; la dimension nécessaire est le rang de B |
| **MDS classique** | La configuration Q_kΛ_k^(1/2) construite sur les k plus grandes valeurs propres de B, appelée aussi analyse en coordonnées principales |
| **Strain** | L'écart entre B et la matrice de Gram de la configuration, que le MDS classique minimise |
| **Stress** | L'écart entre les distances données et celles de la configuration, que le MDS métrique minimise |
| **MDS non métrique** | Un MDS qui n'ajuste que l'ordre des dissimilarités |
| **Critère de Mardia** | La part Σᵢ≤ₖ λᵢ / Σᵢ |λᵢ| des valeurs propres de B gardée par une configuration de dimension k |
| **Procrustes orthogonal** | La rotation ou réflexion qui aligne au mieux une configuration sur une autre, calculée par une SVD |
| **Isomap** | Le MDS classique appliqué aux distances de plus court chemin d'un graphe de voisinage |

---

## Auto-évaluation

**1. Une carte MDS de 50 produits semble convaincante, et sa matrice doublement centrée a une plus grande valeur propre de 40 et une plus petite de −25. Qu'en concluez-vous ?**
> Les dissimilarités sont loin d'être euclidiennes : aucune configuration ne les reproduit, et écarter une valeur propre négative de plus de la moitié de la plus grande déplace beaucoup de distances. Comme la deuxième valeur propre vaut au plus 40, la fraction de Mardia pour une carte en deux dimensions vaut au plus 80/105 ≈ 0,76. Lisez la carte avec prudence ; un MDS métrique ou non métrique par stress peut mieux ajuster les données, ou la dissimilarité elle-même peut être à repenser.

**2. Pourquoi le MDS classique sur les distances euclidiennes d'un jeu de données donne-t-il la même image que l'ACP, et quand utiliseriez-vous quand même le MDS ?**
> Parce que B = X_cX_cᵀ, dont les vecteurs propres multipliés par les valeurs singulières sont les scores de l'ACP X_cV_k. Utilisez le MDS quand seules les distances sont disponibles, ou quand les variables sont bien plus nombreuses que les observations ; utilisez l'ACP quand les observations sont nombreuses et les variables peu nombreuses.

**3. Deux exécutions du MDS sur les mêmes données renvoient des cartes qui diffèrent d'une rotation de 30°. L'une d'elles est-elle fausse ?**
> Pas forcément. Si les deux plus grandes valeurs propres de B sont égales, ou presque, toute rotation dans leur plan respecte aussi bien les distances, et le solveur propre en choisit une. Comparez les distances des deux cartes, ou alignez-les par Procrustes orthogonal ; si elles concordent, les deux sont justes.

**4. `classical_mds` d'IX renvoie un plongement pour des distances de plus court chemin sur un cycle, sans aucun avertissement. Que vérifiez-vous avant de l'utiliser ?**
> Calculez B et ses valeurs propres avec `symmetric_eigen`, puisque `classical_mds` écrête les valeurs propres négatives à 0 sans les signaler. Pour C₄, la valeur propre −1 à côté de deux valeurs propres 2 montre que la carte étire les côtés de 1 à √2. Vérifiez aussi l'échelle : avec des distances autour de 10^-6 ou moins, la tolérance absolue du solveur propre peut sauter entièrement les rotations.

**Critères de réussite :** Centrer doublement une matrice de distances et retrouver une configuration, décider si une matrice de distances est euclidienne et produire un témoin quand elle ne l'est pas, relier le MDS classique à l'ACP, expliquer les ambiguïtés de réflexion et de rotation, mesurer l'effet des valeurs propres négatives, distinguer les MDS classique, métrique et non métrique, et retracer où `classical_mds` d'IX cache une valeur propre négative ou écrase une petite configuration.

---

## Bases de recherche

- I. J. Schoenberg, « Remarks to Maurice Fréchet's article … », *Annals of Mathematics* 36, 1935 : quels espaces de distances se plongent dans l'espace de Hilbert
- G. Young et A. S. Householder, « Discussion of a set of points in terms of their mutual distances », *Psychometrika* 3, 1938 : la matrice de Gram des distances et la dimension nécessaire
- W. S. Torgerson, « Multidimensional scaling: I. Theory and method », *Psychometrika* 17, 1952 : le positionnement classique
- J. B. Kruskal, « Multidimensional scaling by optimizing goodness of fit to a nonmetric hypothesis », *Psychometrika* 29, 1964 : le stress et le MDS non métrique
- J. C. Gower, « Some distance properties of latent root and vector methods used in multivariate analysis », *Biometrika* 53, 1966 : les coordonnées principales et la dualité avec l'ACP
- P. H. Schönemann, « A generalized solution of the orthogonal Procrustes problem », *Psychometrika* 31, 1966 : l'alignement de deux configurations
- K. V. Mardia, « Some properties of classical multi-dimensional scaling », *Communications in Statistics — Theory and Methods* 7, 1978 : la qualité d'ajustement en présence de valeurs propres négatives
- J. B. Tenenbaum, V. de Silva et J. C. Langford, « A global geometric framework for nonlinear dimensionality reduction », *Science* 290, 2000 : Isomap
- I. Borg et P. J. F. Groenen, *Modern Multidimensional Scaling*, 2e éd., Springer, 2005 : le stress, SMACOF et le positionnement classique
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
