---
module_id: mat-017-nonnegative-matrix-factorisation
department: mathematics
course: Factorisation en matrices non négatives
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-006-svd-low-rank-approximation, mat-012-iterative-optimisation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Factorisation en matrices non négatives — Parties, mises à jour multiplicatives et facteurs qui ne sont pas uniques

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Énoncer le problème de la NMF, et minorer son erreur à l'aide de la SVD
- Déduire les mises à jour multiplicatives de Lee et Seung comme des pas de gradient mis à l'échelle, et dire ce que leur monotonie prouve et ce qu'elle ne prouve pas
- Montrer que les facteurs de la NMF ne sont définis, au mieux, qu'à l'échelle et à l'ordre près, et construire des factorisations exactes qui diffèrent davantage
- Expliquer pourquoi une tolérance absolue sur l'erreur de reconstruction rend une règle d'arrêt dépendante des unités des données
- Distinguer des parties identifiées d'un choix arbitraire parmi des solutions aussi bonnes, avec plusieurs graines et un témoin séparable
- Retracer ce que garantit `NonNegativeMatrixFactorization` d'IX, et où sa documentation, ses tests et sa règle d'arrêt promettent plus que ce que le code fournit

---

## 1. Le problème

Soit V une matrice n × p à coefficients positifs ou nuls : n échantillons, p caractéristiques. La **factorisation en matrices non négatives** (NMF) cherche une matrice W de taille n × k et une matrice H de taille k × p, toutes deux à coefficients positifs ou nuls, qui minimisent ‖V − WH‖_F². Paatero et Tapper (1994) l'ont introduite sous le nom de factorisation matricielle positive, et Lee et Seung (1999) l'ont popularisée. La ligne i de V est approchée par Σ_c W_ic h_c, une combinaison des k lignes h_c de H à poids positifs ou nuls : les lignes de H sont les **parties**, et W dit quelle quantité de chaque partie contient chaque échantillon. Rien ne peut être soustrait, donc aucune partie ne peut en annuler une autre. C'est pourquoi la NMF d'images de visages donne des traits localisés, comme le nez ou les yeux, et la NMF de comptages de mots donne des thèmes, alors que la SVD du MAT-006 donne des composantes de signes mélangés.

Le produit WH est de rang au plus k, donc le théorème d'Eckart–Young–Mirsky du MAT-006 minore l'erreur de toute factorisation, non négative ou non : ‖V − WH‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …). La NMF ne peut atteindre cette borne que si l'une des meilleures approximations de rang k est un produit de facteurs non négatifs de dimension intérieure k ; quand σₖ > σₖ₊₁, il n'y en a qu'une, la SVD tronquée V_k. Pour k ≤ 2, c'est le cas exactement quand l'une d'elles n'a aucun coefficient négatif, car une matrice non négative de rang au plus 2 admet toujours des facteurs non négatifs de même dimension intérieure (Cohen et Rothblum 1993). Pour k plus grand, cela peut échouer même pour une meilleure approximation non négative : le **rang non négatif** peut dépasser le rang. Le problème est en outre difficile en général : Vavasis (2009) a montré que décider si V admet une NMF exacte de dimension intérieure rang(V) est NP-difficile.

À W fixé, l'objectif est convexe en H : c'est un problème de moindres carrés non négatifs, comme ceux du MAT-007. Il en va de même en W à H fixé, mais pas dans les deux à la fois, puisque (W, H) et (WD, D⁻¹H) donnent le même produit (§3) ; les minimiseurs ne sont donc jamais des points isolés. Les algorithmes pratiques alternent entre les deux sous-problèmes convexes, et ce qu'ils trouvent dépend de leur point de départ.

### Exercice pratique

IX accepte toute valeur de k de 1 à min(n, p). Montrer que k = min(n, p) est trivial.

> *Solution :* Si k = p ≤ n, on prend W = V et H = I_p : les deux sont non négatives et WH = V, avec une erreur nulle. Si k = n ≤ p, on prend W = I_n et H = V. La borne de cette section concorde, puisque σₖ₊₁ = 0 dès que k ≥ rang(V). La NMF ne dit quelque chose des données que pour k < min(n, p), où les échantillons doivent partager des parties.

---

## 2. Les mises à jour multiplicatives

Le gradient de f(W, H) = ½‖V − WH‖_F² par rapport à H vaut WᵀWH − WᵀV. Lee et Seung (2001) font un pas de gradient avec un pas distinct pour chaque coefficient, η_ij = H_ij/(WᵀWH)_ij, et le pas devient une multiplication : H_ij − η_ij(WᵀWH − WᵀV)_ij = H_ij (WᵀV)_ij/(WᵀWH)_ij. De même, W_ij devient W_ij (VHᵀ)_ij/(WHHᵀ)_ij. Chaque facteur est un quotient de nombres positifs ou nuls, donc W et H restent non négatives sans aucune projection, et il n'y a aucun pas à régler, alors qu'au MAT-012 le pas décide de tout.

Lee et Seung prouvent qu'aucune des deux mises à jour n'augmente ‖V − WH‖_F. Au H courant, ils construisent un majorant quadratique de f à hessienne diagonale, de coefficients (WᵀWH)_a/H_a. Ce majorant touche f au point courant, et son minimiseur est exactement la mise à jour : une **fonction auxiliaire**, ou pas de majoration–minimisation. La preuve donne une suite d'erreurs décroissante au sens large, minorée par 0, donc les erreurs convergent. Elle ne montre ni que les itérés convergent, ni que leur limite est un point stationnaire. Lin (2007) a signalé qu'aucune preuve de convergence vers un point stationnaire n'existait pour ces mises à jour, et a proposé des mises à jour modifiées pour lesquelles il l'a prouvée. Même un point stationnaire n'est qu'une condition nécessaire de minimum local.

La mise à jour multiplie chaque coefficient, donc un coefficient nul reste nul, quoi que dise le gradient. Les valeurs de départ doivent donc être strictement positives, et un coefficient dont la valeur optimale est 0 s'en approche peu à peu sans jamais l'atteindre. En exemple résolu, prenons V = [[2, 1], [1, 2]], k = 1, W₀ = (1, 1)ᵀ et H₀ = (1, 1). Alors W₀ᵀV = (3, 3) et W₀ᵀW₀H₀ = (2, 2), donc H₁ = (3/2, 3/2) ; puis VH₁ᵀ = (9/2, 9/2)ᵀ et W₀H₁H₁ᵀ = (9/2, 9/2)ᵀ, donc W₁ = W₀. L'erreur passe de ‖V − W₀H₀‖_F = √2 ≈ 1,414 à ‖V − W₁H₁‖_F = 1. Les valeurs singulières de V sont 3 et 1, donc 1 est la borne du §1 : un seul pas a atteint l'optimum.

### Exercice pratique

Soit V = uvᵀ avec u et v des vecteurs strictement positifs, et k = 1. Montrer qu'une paire de mises à jour, depuis n'importe quels w et h strictement positifs, donne exactement W₁H₁ = V.

> *Solution :* wᵀV = (w · u)vᵀ et wᵀwh = ‖w‖²h, donc H₁ = ((w · u)/‖w‖²) v : les coefficients de h se simplifient, et H₁ = αv avec α > 0. Alors VH₁ᵀ = α‖v‖²u et wH₁H₁ᵀ = α²‖v‖²w, donc W₁ = u/α, et W₁H₁ = uvᵀ. L'erreur est nulle après la première paire de mises à jour, quel que soit le départ ; le test de rang un d'IX utilise une telle matrice (§6).

---

## 3. Des facteurs qui ne sont pas uniques

Si WH = V, alors (WD)(D⁻¹H) = V pour toute matrice inversible D de taille k × k ; la seule question est de savoir si WD et D⁻¹H restent non négatives. Pour une matrice diagonale D à coefficients strictement positifs, une permutation, ou un produit des deux, c'est toujours le cas : la NMF ne peut pas distinguer la taille d'une partie du poids qui lui est donné, ni l'ordre des parties. Ces matrices monomiales sont les seules matrices non négatives dont l'inverse est aussi non négative. Avant de comparer des exécutions, on met donc chaque partie à l'échelle, par exemple à une somme de 1, et on apparie les parties.

Pour des facteurs particuliers, d'autres matrices gardent les deux facteurs non négatifs, et la factorisation n'est alors pas unique, même après mise à l'échelle. Prenons X = [[2, 1], [1, 2]], W = I et H = X, et D = [[1, a], [0, 1]], d'inverse [[1, −a], [0, 1]]. Alors W_a = [[1, a], [0, 1]] et H_a = [[2 − a, 1 − 2a], [1, 2]] vérifient W_aH_a = X, et les deux sont non négatives exactement quand 0 ≤ a ≤ 1/2 : un continuum de factorisations exactes, qu'aucune mise à l'échelle ni aucun réordonnancement ne relie. Pour a = 1/2, W = [[1, 1/2], [0, 1]] et H = [[3/2, 0], [1, 2]].

Quand rang(V) = k, toute factorisation exacte est de la forme (WQ, Q⁻¹H) pour une matrice inversible Q, car les colonnes de tout autre W doivent engendrer l'espace des colonnes de V. Supposons que W contienne un multiple strictement positif de chaque ligne unitaire, de sorte que chaque partie apparaît pure dans un échantillon, et que H contienne un multiple strictement positif de chaque colonne unitaire, de sorte que chaque partie possède une caractéristique qu'aucune autre partie n'utilise. Les lignes de WQ comprennent alors des multiples des lignes de Q, donc Q ≥ 0, et les colonnes de Q⁻¹H des multiples des colonnes de Q⁻¹, donc Q⁻¹ ≥ 0 : Q est monomiale, et la factorisation est unique à l'échelle et à l'ordre près. Dans l'exemple ci-dessus, W = I remplit la première condition, mais H = X n'a aucune colonne unitaire, ce qui laisse de la place au cisaillement. Donoho et Stodden (2004) ont donné des conditions de ce type pour que la NMF retrouve les vraies parties. Arora, Ge, Kannan et Moitra (2012) ont montré que la seconde condition seule, qu'ils appellent séparabilité, rend la NMF calculable en temps polynomial.

### Exercice pratique

Montrer que (WD)(D⁻¹H) = WH pour toute matrice inversible D. Pourquoi une matrice diagonale D à coefficients strictement positifs garde-t-elle les deux facteurs non négatifs, alors qu'une matrice diagonale D ayant un coefficient négatif ne le fait pas ?

> *Solution :* Par associativité, (WD)(D⁻¹H) = W(DD⁻¹)H = WH. Une matrice diagonale D = diag(d_1, …, d_k) multiplie la colonne c de W par d_c et la ligne c de H par 1/d_c. Quand tous les d_c sont strictement positifs, aucun signe ne change. Quand d_c < 0, la colonne c de W change de signe ; elle est non négative et non nulle, donc elle acquiert un coefficient négatif. La factorisation n'est donc définie, au mieux, qu'aux mises à l'échelle positives et aux réordonnancements des parties près.

---

## 4. Règles d'arrêt et unités

Multiplions V par c > 0 et partons de √c W₀ et √c H₀. Dans la mise à jour de H, (√cW)ᵀ(cV) = c^(3/2) WᵀV et (√cW)ᵀ(√cW)(√cH) = c^(3/2) WᵀWH, donc le quotient ne change pas et le nouveau H vaut √c fois l'ancien ; la mise à jour de W se comporte de la même façon. Par récurrence, chaque itéré sur cV vaut √c fois l'itéré correspondant sur V, et chaque erreur est c fois plus grande. Les mises à jour ne dépendent pas des unités des données.

Une règle d'arrêt peut réintroduire les unités. Une règle qui s'arrête quand l'erreur varie de moins de τ, en valeur absolue, devient sur cV la règle de tolérance τ/c sur V : multiplier les données par 1000, comme quand des mètres deviennent des millimètres, rend la règle 1000 fois plus stricte, et les diviser par 1000 la rend 1000 fois plus lâche. Une règle relative, comme |e_t − e_(t+1)| ≤ τ e_t, donne le même nombre d'itérations dans toutes les unités, tout comme une tolérance sur une mesure de stationnarité rapportée à sa première valeur, le genre de règle qu'utilise Lin (2007). Comme au MAT-012, une petite variation certifie peu de chose : elle ne prouve aucun minimum et, après le §3, rien sur les facteurs, puisque l'erreur est constante le long de familles entières de factorisations.

Les constantes additives brisent l'équivariance de la même façon. Un plancher sur une valeur de départ, ou un ε ajouté à un dénominateur, est une longueur dans les unités des données, et compte quand les données sont petites devant lui. IX a les deux (§6).

### Exercice pratique

Compléter l'argument pour la mise à jour de W : si W_t et H_(t+1) sur cV valent √c fois les itérés sur V, montrer que la mise à jour de W sur cV donne √c W_(t+1). Qu'est-ce qui change quand ε est ajouté aux dénominateurs ?

> *Solution :* (cV)(√cH)ᵀ = c^(3/2) VHᵀ et (√cW)(√cH)(√cH)ᵀ = c^(3/2) WHHᵀ, donc le quotient ne change pas, et √cW multiplié par ce quotient donne √c W_(t+1). Avec ε, le dénominateur devient c^(3/2)(WHHᵀ)_ij + ε, et le quotient change d'une quantité relative de l'ordre de ε/(c^(3/2)(WHHᵀ)_ij) : négligeable pour des données ordinaires, mais plus du tout quand c^(3/2)(WHHᵀ)_ij approche ε.

---

## 5. Graines, parties et témoin séparable

Le test `test_nmf_error_decreases` d'IX (§6) factorise V = [[1, 0, 2], [0, 3, 1], [2, 1, 0], [1, 2, 1]] avec k = 2 et 300 itérations. D'après le §1, aucune factorisation de dimension intérieure 2 n'a une erreur inférieure à σ₃ ≈ 1,699561. La SVD tronquée V₂ a pour plus petit coefficient environ 0,158, donc, d'après Cohen et Rothblum, elle admet des facteurs non négatifs de dimension intérieure 2, qui atteignent la borne. Toute factorisation qui atteint la borne vérifie WH = V₂, puisque la meilleure approximation de rang 2 est unique quand σ₂ > σ₃. Et comme V₂ n'a aucun coefficient nul, il reste de la place pour incliner ses parties comme dans le cisaillement du §3 : V₂ a toute une famille de factorisations optimales.

La transcription du code d'IX (§6) prédit, pour les graines 42, 0 et 100, les erreurs 1,6996, 1,6997 et 1,6997 après 51, 46 et 56 itérations, toutes à moins de 0,0002 de la borne. Mettons chaque partie à une somme de 1, et appelons partie B celle qui a le plus de poids sur la deuxième caractéristique. Elle vaut (0,035 ; 0,793 ; 0,173), (0,031 ; 0,789 ; 0,180) et (0,000 ; 0,832 ; 0,167), et le poids de l'échantillon 1, la ligne (1, 0, 2), sur la partie B vaut 0,174, 0,011 et 0,000. Les trois exécutions s'accordent sur l'erreur, et divergent sur la question de savoir si l'échantillon 1 contient la partie B.

Un arrêt prématuré ne l'explique pas. Avec une tolérance nulle et 20 000 itérations, les trois exécutions devraient atteindre 1,699561, la borne elle-même, avec les poids 0,185, 0,007 et 0,000 pour l'échantillon 1 : elles convergent vers trois factorisations optimales différentes.

Un **témoin séparable** est un jeu de données dont on sait que la factorisation est unique. Prenons V = [[1, 0, 2], [0, 1, 1], [1, 1, 3], [2, 1, 5]], qui vaut WH pour W = [[1, 0], [0, 1], [1, 1], [2, 1]] et H = [[1, 0, 2], [0, 1, 1]]. W contient les deux lignes unitaires et H les deux colonnes unitaires, donc, d'après le §3, la factorisation est unique à l'échelle et à l'ordre près, avec les parties (1/3, 0, 2/3) et (0, 1/2, 1/2) une fois mises à une somme de 1. Avec les 200 itérations par défaut d'IX, les graines 42, 0 et 100 devraient renvoyer les deux parties à 0,01 près, avec des erreurs de 0,018, 0,027 et 0,018. Aucune des trois exécutions ne s'arrête avant le plafond : les coefficients qui devraient valoir 0 s'en approchent lentement (§2), et la variation sur les cinq dernières itérations reste au-dessus de 10^-4, à 0,00044, 0,00096 et 0,00040.

Les deux cas séparent deux choses qu'on aimerait voir signifiées par un arrêt. Sur la matrice du test, la règle d'IX s'arrête alors que les parties sont arbitraires ; sur le témoin, elle ne s'arrête jamais alors que les parties sont justes. Donner un sens aux parties exige des indices qu'elles sont identifiées, comme un accord entre graines après mise à l'échelle et appariement, et non un arrêt ou une petite erreur.

### Exercice pratique

Au deuxième paragraphe, pourquoi les trois exécutions peuvent-elles diverger sur le poids de l'échantillon 1 tout en s'accordant sur l'erreur ?

> *Solution :* Les trois produits sont tous proches de V₂, l'unique meilleure approximation de rang 2, donc les trois erreurs sont proches de σ₃. Le produit ne détermine pas les facteurs : V₂ n'a aucun coefficient nul, donc, comme pour le cisaillement du §3, ses parties peuvent s'incliner dans le plan qu'elles engendrent tandis que les deux facteurs restent non négatifs. Le long d'une telle famille, le produit, et donc l'erreur, reste le même, tandis que le poids de chaque échantillon sur chaque partie change ; le poids de l'échantillon 1 sur la partie B est l'une des quantités qui changent.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de `fit_transform` et `transform` en Python, avec une réplique du `StdRng` de rand 0.9 (ChaCha12, amorcé par PCG32) qui reproduit les tirages de la crate elle-même. Les flottants de Python sont en binary64 IEEE comme le `f64` de Rust ; les sommes peuvent différer de celles de ndarray dans les derniers bits, bien en deçà des marges des valeurs énoncées. Ces nombres sont des prédictions, que le §7 propose de vérifier.

**NMF** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L105) rejette [k = 0 et k > min(n, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L112) ainsi que les [coefficients négatifs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119). Elle tire W puis H de [`StdRng::seed_from_u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L129), applique les mises à jour du §2 avec ε dans les dénominateurs, et mesure l'erreur avec [`frobenius_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L241), la norme elle-même et non son carré, toutes les cinq itérations. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L183) garde H, tire un nouveau W [avec la même graine](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L202) et effectue [50 mises à jour de W](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L213). Les valeurs par défaut sont [200 itérations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L74) et la [graine 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L77). Le module n'est qu'une bibliothèque : [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L11) l'exporte et aucun autre fichier Rust du dépôt n'y fait référence, donc aucun outil MCP et aucune étape de pipeline n'offre la NMF. L'initialisation et le test d'arrêt s'écrivent :

```rust
        let mean = v.mean().unwrap_or(1.0).abs().max(1e-3);
        let scale = (mean / self.n_components as f64).sqrt();
        let mut rng = StdRng::seed_from_u64(self.seed);
        let mut w = Array2::<f64>::zeros((n_samples, self.n_components));
        for e in w.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
        let mut h = Array2::<f64>::zeros((self.n_components, n_features));
        for e in h.iter_mut() {
            *e = rng.random::<f64>() * scale + self.eps;
        }
```

```rust
            if iter % 5 == 0 || iter == self.max_iterations - 1 {
                let err = frobenius_distance(v, &w.dot(&h));
                final_err = err;
                if convergence.converged((prev_err - err).abs()) {
                    break;
                }
                prev_err = err;
            }
```

- **La règle d'arrêt dépend des unités des données.** La [tolérance de 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L75), documentée comme une [« Convergence tolerance on the Frobenius reconstruction error »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L55), est comparée par [`converged`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/convergence.rs#L46), avec un `<` strict, à la variation de l'erreur entre deux contrôles. Les contrôles ont lieu après les itérations 1, 6, 11 et ainsi de suite, donc la première variation couvre une itération et les suivantes cinq. L'échelle de départ s = √(moyenne/k) croît comme √c, donc tant que la moyenne reste au-dessus du plancher de 10^-3 et que ε reste négligeable, toute l'exécution est équivariante (§4), et la tolérance est absolue. Sur la matrice du §5 avec la graine 42, multipliée par 0,001, 1 et 1000, la transcription prédit 16, 51 et 86 itérations, avec des erreurs de 1,7360, 1,6996 et 1,69956 fois le facteur, pour une borne de 1,699561.
- **La documentation promet plus que ce que l'on sait des mises à jour.** La documentation du module dit que la convergence est [« guaranteed (not necessarily to a global optimum, but to a local one). »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L24) Lee et Seung prouvent que l'erreur n'augmente jamais. Que les itérés convergent vers un point stationnaire, a fortiori vers un minimum local, n'est pas prouvé pour ces mises à jour (§2), et la règle d'arrêt d'IX ne teste ni l'un ni l'autre (§4, §5). La transcription concorde avec la monotonie : sur 30 graines pour chacune des trois matrices de test de tailles 3 × 3, 4 × 3 et 4 × 4 avec k = 2, à 300 itérations chacune, la plus forte hausse d'une itération à la suivante vaut environ 6,7 · 10^-16, une erreur d'arrondi.
- **Le test d'erreur ne peut pas échouer.** [`test_nmf_error_decreases`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L320) ne compare jamais l'erreur finale à l'erreur initiale. Il affirme que l'erreur est [inférieure](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L332) à la [somme des coefficients](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L330), Σvᵢⱼ = 14. La factorisation nulle a déjà l'erreur ‖V‖_F = √26 ≈ 5,10, et ‖V‖_F ≤ Σvᵢⱼ pour toute V non négative. Avant toute mise à jour, l'erreur est inférieure à √1083/6 ≈ 5,485 pour toute graine (voir l'exercice ci-dessous), et par monotonie toute erreur ultérieure l'est aussi. Le test passe donc pour toute graine, et passerait encore si la boucle de mise à jour était supprimée. Avec la graine 42, la transcription prédit une erreur initiale de 4,545 et une erreur finale de 1,6996, après 51 itérations.
- **Le test de rang un est résolu par la première mise à jour.** [`test_nmf_rank_one_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L258) et l'exemple du module utilisent V = uuᵀ avec u = (1, 2, 3). D'après l'exercice du §2, la première paire de mises à jour la reproduit depuis tout départ strictement positif, à l'effet de ε près. Le premier contrôle voit une variation égale à toute l'erreur initiale, environ 12,363 pour la graine 42, et ne peut pas s'arrêter ; le deuxième le peut. La transcription prédit 6 itérations pour toute graine, et une erreur d'environ 4 · 10^-11 pour la graine 42, très en dessous du [seuil de 0,1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L267). Le test vérifie une vraie propriété, mais pas l'itération : toute méthode qui fait un pas exact de rang un le passe. L'exemple n'affirme que [le nombre de colonnes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L39).
- **Rien n'avertit que les parties ne sont pas uniques.** La documentation recommande la NMF parce qu'elle [« produces a parts-based »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L7) [« decomposition that is often more interpretable »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L8). La graine a un [constructeur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L97), mais aucun test ne la fait varier et aucun document ne mentionne le §3. Le §5 donne la conséquence prédite sur la matrice du test d'erreur lui-même : des poids de 0,174, 0,011 et 0,000 pour l'échantillon 1 sur la même partie, avec les graines 42, 0 et 100.
- **Les coefficients NaN et +∞ sont acceptés.** Le [contrôle](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L119) `x < 0.0` est faux pour NaN et pour +∞, donc une matrice ayant un tel coefficient le passe ; −∞ est rejeté. Sa moyenne est NaN, et le [plancher](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L127) la change en 10^-3, car le `f64::max` de Rust renvoie l'autre opérande quand l'un est NaN. Après la première mise à jour, tous les coefficients de W et H valent NaN ; la variation vaut NaN, `converged` n'est jamais vrai, et la transcription prédit les 200 itérations, puis `Ok`, avec W, H et l'erreur entièrement NaN. Un coefficient égal à +∞ donne le même résultat, et [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L196) a le même contrôle.
- **Autres lacunes.** [`test_nmf_transform_matches_shape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L302) ne vérifie que [les formes et les signes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L316), et aucun test ne compare `transform` sur les données d'apprentissage au W renvoyé par `fit_transform`. Il n'y a pas d'initialisation structurée comme NNDSVD, pas de redémarrage sur plusieurs graines, pas de tolérance relative, pas de régularisation, pas d'autre objectif que la norme de Frobenius, et pas d'indicateur pour une exécution qui a atteint le plafond : [`n_iter`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/nmf.rs#L66) égal à `max_iterations` en est le seul signe.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Le test d'erreur d'IX part de W₀ et H₀ de coefficients u · s + ε, où u suit la loi uniforme sur [0, 1) et s = √(moyenne/k). Montrer qu'avant toute mise à jour, l'erreur est inférieure à √1083/6 ≈ 5,485 quelle que soit la graine.

> *Solution :* Les 12 coefficients ont pour somme 14, donc la moyenne vaut 7/6 et s² = 7/12 pour k = 2. Chaque coefficient de W₀H₀ est une somme de deux produits de nombres de [ε, s + ε), donc il est strictement compris entre 0 et 2(s + ε)², qui vaut 7/6 plus quelques fois ε. Un coefficient v de V diffère donc du coefficient correspondant de W₀H₀ de moins de max(v, 7/6 − v) : 7/6 pour chacun des trois zéros, et v pour les cinq uns, les trois deux et le trois. Le carré de l'erreur est inférieur à 3 · 49/36 + 5 + 12 + 9 = 1083/36, à des termes de l'ordre de ε près, donc l'erreur est inférieure à √1083/6 ≈ 5,485, moins de la moitié de 14.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **La matrice du test d'erreur.** Appeler `fit_transform` avec k = 2, 300 itérations et la graine 42 sur la matrice du §5. Prédiction : `n_iter` égal à 51 et une erreur de 1,6996, à 10^-4 près.
2. **Une erreur monotone.** Pour i = 1, …, 300, répéter l'étape 1 avec `with_tolerance(0.0)` et `with_max_iterations(i)`. Comme `converged` est un `<` strict, chaque exécution s'arrête après exactement i itérations et rapporte l'erreur après i. Prédiction : l'erreur ne monte jamais de plus de 10^-15, et décroît vers 1,699561.
3. **Graines.** Répéter l'étape 1 avec les graines 0 à 9, mettre chaque partie à une somme de 1, et trouver le poids de l'échantillon 1 sur la partie B. Prédiction : toutes les erreurs à moins de 0,00024 de 1,699561, et des poids allant de 0,000 à 0,112.
4. **Unités.** Répéter l'étape 1 sur 0,001 V et sur 1000 V. Prédiction : 16 et 86 itérations, contre 51 pour V, avec des erreurs de 1,7360 et 1,69956 fois le facteur.
5. **Témoin séparable.** Répéter l'étape 3 sur le témoin du §5 avec les 200 itérations par défaut. Prédiction : chaque exécution utilise les 200 itérations, et les deux parties concordent avec (1/3, 0, 2/3) et (0, 1/2, 1/2) à 0,01 près.
6. **Un coefficient NaN.** Remplacer un coefficient de la matrice du §5 par NaN, et appeler `fit_transform` avec k = 2 et les réglages par défaut. Prédiction : `Ok`, `n_iter` égal à 200, et W, H et l'erreur entièrement NaN.

### Exercice pratique

À l'étape 4, pourquoi 0,001 V s'arrête-t-il après 16 itérations avec une erreur plus élevée, alors que ses itérés sont ceux de V mis à l'échelle ?

> *Solution :* Sur 0,001 V, chaque erreur vaut 0,001 fois l'erreur sur V (§4), donc la tolérance de 10^-4 revient à 0,1 dans les unités de V. Dans ces unités, la transcription prédit des variations de 2,363, 0,208, 0,143 et 0,094 aux contrôles qui suivent les itérations 1, 6, 11 et 16. La variation 0,094 est la première inférieure à 0,1, donc l'exécution s'arrête après 16 itérations, à 1,7360 dans les unités de V, tandis que l'exécution sur V continue jusqu'à ce que la variation passe sous 10^-4, après 51 itérations. Une tolérance relative donnerait la même réponse dans les deux unités.

---

## 8. Pièges courants

- **Donner un sens aux parties d'une seule exécution.** Lancer plusieurs graines, mettre à l'échelle et apparier les parties, et rapporter ce qui concorde.
- **Prendre un arrêt pour une solution.** Une variation inférieure à une tolérance ne prouve aucun minimum et n'identifie aucun facteur ; sur la matrice de test du §5, l'arrêt survient alors que les parties sont arbitraires.
- **Utiliser une tolérance absolue sur des données en unités arbitraires.** Remettre les données à une norme fixée, ou utiliser une règle relative.
- **Choisir k d'après la seule erreur.** La meilleure erreur ne peut que baisser quand k croît, et elle atteint 0 pour k = min(n, p), où la factorisation est triviale.
- **Démarrer un coefficient à 0.** Les mises à jour multiplicatives ne le déplacent jamais ; partir de valeurs strictement positives.
- **Comparer des facteurs colonne par colonne.** L'échelle et l'ordre sont arbitraires ; mettre chaque partie à l'échelle et apparier les parties d'abord.
- **Écrire un test que la factorisation nulle réussit.** Comparer à l'erreur initiale, ou à la borne du §1.
- **Passer NaN à un ajustement qui ne rejette que les coefficients négatifs.** Vérifier que chaque coefficient est fini avant l'ajustement.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Factorisation en matrices non négatives (NMF)** | Approcher V ≥ 0 par WH avec W ≥ 0 et H ≥ 0 de dimension intérieure k |
| **Partie** | Une ligne de H ; chaque échantillon est une combinaison non négative des parties |
| **Mise à jour multiplicative** | Un pas de gradient à pas par coefficient qui devient une multiplication par un quotient de termes non négatifs |
| **Fonction auxiliaire** | Un majorant de l'objectif qui le touche au point courant, de sorte que le minimiser ne peut pas augmenter l'objectif |
| **Rang non négatif** | Le plus petit k tel que V = WH exactement avec des facteurs non négatifs ; il vaut au moins rang(V) |
| **Ambiguïté d'échelle** | (WD)(D⁻¹H) = WH pour toute matrice diagonale D à coefficients strictement positifs |
| **Identifiabilité** | La propriété que V détermine les facteurs, à l'échelle et à l'ordre près |
| **Séparabilité** | La condition que chaque partie possède une caractéristique qu'aucune autre partie n'utilise |
| **Tolérance absolue** | Un seuil d'arrêt exprimé dans les unités des données |
| **Témoin séparable** | Des données dont on sait que la factorisation est unique, sur lesquelles une méthode doit renvoyer les mêmes parties pour toute graine |

---

## Auto-évaluation

**1. Un collègue montre les thèmes d'une exécution de NMF avec la graine 42, et interprète le thème 3. Que demandez-vous ?**
> Des exécutions avec d'autres graines, thèmes mis à l'échelle et appariés, pour voir si le thème 3 revient ; les erreurs de ces exécutions, et la borne du §1 ; le nombre d'itérations comparé au plafond ; et la même chaîne sur un témoin séparable, où les thèmes doivent concorder d'une graine à l'autre. Comme le montre le §5, des exécutions dont les erreurs concordent à 0,0002 près peuvent diverger sur les échantillons qui contiennent une partie.

**2. Pourquoi une mise à jour multiplicative ne peut-elle pas déplacer un coefficient nul, et qu'est-ce que cela implique pour le départ ?**
> La mise à jour multiplie le coefficient par un quotient, donc 0 reste 0 quoi que dise le gradient. Le départ doit donc être strictement positif, comme le garantit le petit décalage ε d'IX, et un coefficient qui devrait finir à 0 ne s'en approche que peu à peu, ce qui retarde l'arrêt, comme sur le témoin séparable du §5.

**3. Les mêmes mesures demandent 86 itérations à la NMF d'IX quand elles sont exprimées en grammes, 51 en kilogrammes et 16 en tonnes. Quelle exécution est la bonne ?**
> Aucune n'est privilégiée : les mises à jour sont les mêmes à l'échelle près, et seule la règle d'arrêt diffère, parce que la tolérance de 10^-4 d'IX est absolue. En tonnes, elle revient à une tolérance 1000 fois plus lâche qu'en kilogrammes. Remettre les données à une norme fixée, ou utiliser une règle relative, et rapporter l'erreur relativement à ‖V‖_F.

**4. `test_nmf_error_decreases` affirme que l'erreur finale est inférieure à la somme des coefficients. À quoi ressemblerait une assertion utile ?**
> À une assertion qui échoue quand les mises à jour ne fonctionnent pas : par exemple, que l'erreur finale est inférieure à l'erreur initiale avec une marge, ou à un petit facteur près de la borne σ₃ du §1, 1,699561 sur la matrice du test. L'assertion actuelle tient même pour la factorisation nulle, dont l'erreur vaut √26 ≈ 5,10, moins de 14.

**Critères de réussite :** Énoncer le problème de la NMF et sa borne par la SVD, déduire les mises à jour multiplicatives et dire ce que leur monotonie prouve, montrer pourquoi les facteurs ne sont pas uniques et quand ils le sont, expliquer pourquoi une tolérance absolue dépend des unités, concevoir une comparaison de graines avec un témoin séparable, et retracer où la documentation, les tests et la règle d'arrêt d'IX promettent plus que ce que le code fournit.

---

## Bases de recherche

- J. E. Cohen et U. G. Rothblum, « Nonnegative ranks, decompositions, and factorizations of nonnegative matrices », *Linear Algebra and its Applications* 190, 1993 : le rang non négatif, et le cas du rang 2
- P. Paatero et U. Tapper, « Positive matrix factorization: a non-negative factor model with optimal utilization of error estimates of data values », *Environmetrics* 5, 1994 : le problème
- D. D. Lee et H. S. Seung, « Learning the parts of objects by non-negative matrix factorization », *Nature* 401, 1999 : les représentations par parties
- D. D. Lee et H. S. Seung, « Algorithms for non-negative matrix factorization », *Advances in Neural Information Processing Systems* 13, 2001 : les mises à jour multiplicatives et leur monotonie
- D. Donoho et V. Stodden, « When does non-negative matrix factorization give a correct decomposition into parts? », *Advances in Neural Information Processing Systems* 16, 2004 : des conditions pour des parties uniques
- C.-J. Lin, « On the convergence of multiplicative update algorithms for nonnegative matrix factorization », *IEEE Transactions on Neural Networks* 18, 2007 : la stationnarité de la limite, et des mises à jour modifiées
- C. Boutsidis et E. Gallopoulos, « SVD based initialization: a head start for nonnegative matrix factorization », *Pattern Recognition* 41, 2008 : l'initialisation NNDSVD
- S. A. Vavasis, « On the complexity of nonnegative matrix factorization », *SIAM Journal on Optimization* 20, 2009 : la NP-difficulté
- S. Arora, R. Ge, R. Kannan et A. Moitra, « Computing a nonnegative matrix factorization — provably », *Proceedings of the ACM Symposium on Theory of Computing*, 2012 : la séparabilité
- N. Gillis, *Nonnegative Matrix Factorization*, SIAM, 2020 : algorithmes, identifiabilité et règles d'arrêt
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
