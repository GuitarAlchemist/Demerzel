---
module_id: mat-016-kernel-pca-misleading-projections
department: mathematics
course: ACP à noyau et projections trompeuses
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-013-distances-kernels-psd, mat-014-pca-variance-preservation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# ACP à noyau et projections trompeuses — Des composantes principales dans l'espace de caractéristiques, et des structures que le noyau invente

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Déduire l'ACP à noyau de la forme de l'ACP par la matrice de Gram, et dire ce que le noyau doit vérifier
- Centrer une matrice de noyau dans l'espace de caractéristiques, et expliquer pourquoi il existe au plus n − 1 composantes
- Normaliser les vecteurs propres, projeter les points d'apprentissage et de nouveaux points, et vérifier que les deux projections concordent
- Décrire comment la largeur de bande RBF fait passer l'ACP à noyau de l'ACP linéaire à une projection qui ne dit rien des données
- Distinguer une séparation fabriquée par la projection d'une structure des données, avec un balayage de la largeur de bande et un témoin négatif
- Retracer ce que garantit `KernelPca` d'IX, et où son test, sa documentation et un seuil numérique promettent plus que ce que le code fournit

---

## 1. De l'ACP à l'ACP à noyau

Le MAT-014 calcule l'ACP à partir de la matrice de covariance p × p. Les mêmes composantes s'obtiennent à partir de la matrice n × n des produits scalaires. Si X_c est la matrice de données centrée, de SVD X_c = UΣVᵀ comme au MAT-006, la matrice de Gram X_cX_cᵀ = UΣ²Uᵀ a pour valeurs propres λᵢ = σᵢ² et pour vecteurs propres unitaires les vᵢ, colonnes de U, et les scores sont X_cV_k = U_kΣ_k : le score du point j sur la composante i est √λᵢ (vᵢ)ⱼ. Cette forme n'utilise les données qu'à travers les produits scalaires xᵢ · xⱼ.

L'**ACP à noyau** (Schölkopf, Smola et Müller 1998) remplace chaque produit scalaire par une valeur de noyau k(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ), au sens du MAT-013 : c'est l'ACP des images φ(xᵢ) dans l'espace de caractéristiques, calculée sans jamais former φ. L'espace de caractéristiques du noyau polynomial (γ x · y + c)^d a une coordonnée par monôme de degré au plus d, ou exactement d quand c = 0 ; celui du noyau RBF est de dimension infinie, si bien que l'ACP n'y est possible qu'à travers la matrice de noyau K. Le noyau doit être semi-défini positif : sinon aucun φ n'existe, et K peut avoir des valeurs propres négatives, qui ne sont pas des variances. Une composante de l'ACP à noyau est une direction de l'espace de caractéristiques. Ses scores sont une fonction non linéaire de l'entrée, tandis que la méthode elle-même reste linéaire, dans l'espace de caractéristiques.

### Exercice pratique

Pour le noyau k(x, y) = (x · y)² sur ℝ², trouver une application de caractéristiques φ, et calculer k((1, 2), (3, 1)) des deux façons.

> *Solution :* (x · y)² = (x₁y₁ + x₂y₂)² = x₁²y₁² + 2x₁x₂y₁y₂ + x₂²y₂², donc φ(x) = (x₁², √2 x₁x₂, x₂²). Directement, (1 · 3 + 2 · 1)² = 5² = 25. Par φ, φ(1, 2) = (1, 2√2, 4) et φ(3, 1) = (9, 3√2, 1), dont le produit scalaire est 9 + 12 + 4 = 25. L'ACP des φ(xᵢ) cherche des directions parmi les trois monômes quadratiques : une ellipse centrée à l'origine de l'entrée devient un plan de l'espace de caractéristiques.

---

## 2. Centrer dans l'espace de caractéristiques

L'ACP demande des données centrées, et la moyenne φ̄ des images ne peut pas être formée. Ce n'est pas nécessaire : les produits scalaires des images centrées valent (φ(xᵢ) − φ̄) · (φ(xⱼ) − φ̄) = kᵢⱼ − rᵢ − rⱼ + g, où rᵢ est la moyenne de la ligne i de K et g la moyenne de tous ses coefficients. Sous forme matricielle, K_c = JKJ avec la matrice de centrage J = I − (1/n) 11ᵀ : le double centrage du MDS classique, appliqué à K au lieu de −½ D⁽²⁾. Pour le noyau RBF le lien est exact, puisque ‖φ(x) − φ(y)‖² = k(x, x) + k(y, y) − 2k(x, y) = 2 − 2k(x, y) : l'ACP à noyau RBF est le MDS classique sur les distances de l'espace de caractéristiques √(2 − 2kᵢⱼ), un lien qu'étudie Williams (2002).

Les images centrées ont une somme nulle, donc K_c 1 = 0 : le vecteur des uns est toujours vecteur propre de valeur propre 0, et au plus n − 1 valeurs propres sont non nulles. Si grand que soit l'espace de caractéristiques, n points centrés n'en engendrent qu'au plus n − 1 dimensions, donc l'ACP à noyau offre au plus n − 1 composantes, chacune combinaison des images d'apprentissage.

### Exercice pratique

Appliquer l'ACP à noyau avec le noyau linéaire aux points 0, 1 et 3 de la droite réelle. Calculer K, K_c et les scores.

> *Solution :* K = xxᵀ = [[0, 0, 0], [0, 1, 3], [0, 3, 9]], de moyennes de lignes 0, 4/3 et 4 et de moyenne globale 16/9. Alors (K_c)₁₁ = 0 − 0 − 0 + 16/9 = 16/9, et de même K_c = x̃x̃ᵀ avec x̃ = (−4/3, −1/3, 5/3), les points centrés. K_c est de rang 1, de seule valeur propre non nulle ‖x̃‖² = 14/3 et de vecteur propre unitaire x̃/‖x̃‖, donc les scores √(14/3) · x̃/‖x̃‖ = x̃ sont les points centrés, au signe près : avec le noyau linéaire, l'ACP à noyau est l'ACP.

---

## 3. Normalisation et projection hors échantillon

Soit v un vecteur propre unitaire de K_c de valeur propre λ > 0. La direction de l'espace de caractéristiques w = Σⱼ αⱼ (φ(xⱼ) − φ̄) avec α = v/√λ est de longueur 1, puisque ‖w‖² = αᵀK_cα = vᵀK_cv/λ = 1 ; c'est la normalisation de Schölkopf, Smola et Müller. Le score du point d'apprentissage i est le produit scalaire de son image centrée avec w, (K_cα)ᵢ = λvᵢ/√λ = √λ vᵢ, la formule du §1.

Un nouveau point x se projette de la même façon, avec les statistiques d'apprentissage. Son vecteur de noyau centré a pour coordonnées k̃ⱼ(x) = k(x, xⱼ) − m(x) − rⱼ + g, où m(x) est la moyenne des k(x, xⱼ) sur les points d'apprentissage, et son score est Σⱼ αⱼ k̃ⱼ(x). Pour un point d'apprentissage, k̃(xᵢ) est la ligne i de K_c et le score vaut de nouveau √λ vᵢ, donc les deux voies doivent concorder sur l'ensemble d'apprentissage : c'est la première vérification à faire sur toute implémentation. Quand λ = 0, v est dans le noyau de K_c, aucune direction unitaire w ne peut en être tirée, et la bonne sortie est une colonne de zéros, ou pas de colonne du tout.

Revenir d'un score à l'espace d'entrée est plus difficile, car un point de l'espace de caractéristiques n'est pas forcément l'image d'une entrée. Ce **problème de la préimage** ne se résout qu'approximativement : par itération pour le noyau RBF (Mika et al. 1999), ou à partir des distances (Kwok et Tsang 2004).

### Exercice pratique

Poursuivre l'exercice du §2 : projeter le nouveau point x = 2 avec le noyau linéaire, par k̃(x) et α.

> *Solution :* k(2, xⱼ) = (0, 2, 6), de moyenne m = 8/3. Avec les moyennes de lignes 0, 4/3 et 4 et g = 16/9, k̃ = (0 − 8/3 − 0 + 16/9, 2 − 8/3 − 4/3 + 16/9, 6 − 8/3 − 4 + 16/9) = (−8/9, −2/9, 10/9). Avec v = x̃/‖x̃‖ et λ = 14/3, α = x̃/λ = (−2/7, −1/14, 5/14), et le score vaut (−8/9)(−2/7) + (−2/9)(−1/14) + (10/9)(5/14) = 16/63 + 1/63 + 25/63 = 2/3 : le point 2 moins la moyenne d'apprentissage 4/3, comme le donnerait l'ACP.

---

## 4. La largeur de bande : de l'ACP linéaire à la projection de rien

Le MAT-013 a suivi la matrice de Gram RBF K quand γ varie. Le centrage change les deux limites. Pour γ petit, exp(−γd²) = 1 − γd² + O(γ²d⁴) ; le centrage retire la constante, et K_c ≈ −γ J D⁽²⁾ J = 2γB, où B est la matrice doublement centrée du MDS classique, la matrice de Gram des entrées centrées. L'ACP à noyau tend alors vers l'ACP linéaire, avec des valeurs propres environ 2γ fois celles de B et des scores environ √(2γ) fois ceux de l'ACP. Sur les points 0, 1 et 3 avec γ = 0,001, la plus grande valeur propre vaut environ 9,29 · 10^-3, contre 2γ · 14/3 ≈ 9,33 · 10^-3, et les scores divisés par √(2γ) valent −1,330, −0,334 et 1,663, contre −4/3, −1/3 et 5/3.

Pour γ grand, chaque kᵢⱼ hors diagonale tend vers 0, K tend vers I et K_c vers J, dont les valeurs propres sont 1, n − 1 fois, et 0. Tout vecteur unitaire orthogonal à 1 est alors vecteur propre, donc les composantes sont la base que renvoie le solveur, quelle qu'elle soit. Dans l'espace de caractéristiques, les images de points distincts deviennent orthogonales, toutes à distance √2 les unes des autres : un simplexe régulier, qui a le même aspect dans toutes les directions.

Entre ces limites, ce que montre l'ACP à noyau dépend de γ, et aucune valeur n'est juste en général. Le MAT-013 mentionne une valeur de départ courante, σ égal à la distance médiane entre les points, avec γ = 1/(2σ²) : un point de départ, pas une garantie que la structure cherchée apparaîtra.

### Exercice pratique

Pour n points distincts et γ → ∞, que renvoie l'ACP à noyau avec k composantes, et que dit-elle des données ?

> *Solution :* K_c tend vers J, donc les n − 1 valeurs propres non nulles tendent toutes vers 1, et toute base orthonormée des vecteurs orthogonaux à 1 est un jeu valide de vecteurs propres. Les k colonnes renvoyées sont les vecteurs que produit le solveur, quels qu'ils soient, multipliés par √1 = 1 : une projection d'un simplexe régulier, qui ne dit rien des données. Tout motif dans un tel graphique, groupes compris, vient du solveur.

---

## 5. Projections trompeuses : deux anneaux et un témoin négatif

Deux anneaux concentriques sont la vitrine classique de l'ACP à noyau. Aucune projection linéaire ne les sépare (voir l'exercice), mais le noyau RBF le peut, par une composante particulière. Prenons m points sur chaque anneau, aux mêmes angles. La configuration est inchangée par les rotations et réflexions d'un m-gone régulier, et K_c commute avec les permutations des points qu'elles induisent. Les vecteurs que fixent ces permutations sont ceux qui sont constants sur chaque anneau ; ils forment un plan qui contient 1 et que K_c envoie dans lui-même, donc l'autre direction de ce plan, s = (1, …, 1, −1, …, −1)/√(2m), est un vecteur propre exact, de valeur propre λ_rad = sᵀKs. Ses scores valent +√(λ_rad/(2m)) sur un anneau et −√(λ_rad/(2m)) sur l'autre : chaque anneau se réduit à une seule valeur, une séparation parfaite. Tout autre vecteur propre peut être choisi orthogonal à ce plan, donc ses scores ont une moyenne nulle sur chaque anneau. Sans s, toute fonction affine des scores gardés a la même moyenne sur les deux anneaux, donc elle ne peut pas être positive sur un anneau et négative sur l'autre : que les composantes gardées séparent les anneaux par une droite ou un hyperplan dépend seulement de la présence de s parmi elles, c'est-à-dire du rang de λ_rad, et ce rang dépend de γ et de la géométrie. Les anneaux peuvent encore différer par le rayon dans un tel graphique, comme ci-dessous, mais seule une règle non linéaire peut s'en servir.

Les données de test d'IX ont quatre points sur chacun des anneaux de rayons 1 et 2. À γ = 0,5, les valeurs propres de K_c valent environ 1,531 deux fois, 1,216, 0,672 = λ_rad, 0,333 deux fois, 0,148 et 0 : la composante radiale est quatrième, et elle est quatrième pour chaque γ du balayage du §7, de 0,001 à 10. Les deux premières composantes forment une paire égale qui enregistre l'angle de chaque point : chaque point intérieur arrive au même angle que son voisin extérieur, à un rayon d'environ 0,583 contre 0,653 pour l'anneau extérieur. Le rapport 2 entre les rayons se réduit à environ 1,12, et aucune droite ne sépare les deux carrés.

Avec le rayon intérieur changé en 0,3 et l'extérieur en 1, la composante radiale est quatrième jusqu'à γ = 0,5, troisième à γ = 1, et première au-delà de γ ≈ 1,597. Son avance sur la valeur propre suivante atteint environ 0,357 à γ = 5 et tombe à environ 1,2 · 10^-4 à γ = 50. Les mêmes données ne montrent donc aucune séparation à γ = 1 et une séparation parfaite à γ = 5. Une séparation qui tient dans une fenêtre de γ est une propriété des données et de γ ensemble, et la rapporter exige de donner la fenêtre.

Un **témoin négatif** est un jeu de données sans la structure cherchée. Prenons les huit points régulièrement espacés 0, 1, …, 7 d'une droite : ils n'ont aucun groupe. À γ = 0,001 la première composante est pratiquement la droite, et son plus grand écart entre scores consécutifs vaut 0,145 de l'étendue, contre 1/7 ≈ 0,143 pour un espacement exactement régulier. À γ = 0,1 et à chaque γ plus grand du balayage, la première composante n'est plus monotone : les deux extrémités se replient tandis que le milieu s'étire, et pour γ = 2, 5 et 10 l'écart entre les points 3 et 4 atteint 0,347 de l'étendue, plus du double de l'écart régulier. Un histogramme de cette composante montre deux groupes de quatre points. C'est l'effet **fer à cheval** des noyaux locaux (Diaconis, Goel et Holmes 2008) : le noyau ne voit que les proches voisins, et les premiers vecteurs propres de telles matrices courbent une droite en arche, souvent aux extrémités recourbées vers l'intérieur. Tout critère qui déclare les anneaux séparés devrait être essayé sur un tel témoin, et doit y échouer.

### Exercice pratique

Pourquoi aucune projection linéaire ne peut-elle séparer deux anneaux concentriques centrés à l'origine ?

> *Solution :* Une projection linéaire envoie x sur u · x pour un vecteur unitaire u ; la première composante de l'ACP est une telle application. Un anneau complet de rayon r s'envoie sur tout l'intervalle [−r, r], donc l'intervalle de l'anneau intérieur est contenu dans celui de l'anneau extérieur, et tout seuil strictement compris entre −r₁ et r₁ a des points des deux anneaux de chaque côté. Pour les quatre points par anneau d'IX, chaque point extérieur est le double du point intérieur de même angle, donc chaque score extérieur est le double d'un score intérieur ; les scores intérieurs prennent les deux signes, donc les scores extérieurs les dépassent aux deux bouts, et aucun seuil ne sépare les anneaux. Garder plus de composantes linéaires n'aide pas : une application linéaire envoie les deux anneaux sur deux ellipses emboîtées, l'une copie réduite de l'autre.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de `fit_transform`, `transform`, `compute_kernel` et `symmetric_eigen` en Python, dont les flottants sont en binary64 IEEE comme le `f64` de Rust : ce sont des prédictions, que le §7 propose de vérifier.

**ACP à noyau** (`crates/ix-unsupervised`). [`fit_transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L96) construit K, la centre avec la [formule du §2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L129), confie K_c à [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L135), la méthode de Jacobi du MAT-005, et garde les `n_components` premières paires. [`transform`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L169) centre les vecteurs de noyau des nouveaux points avec les [statistiques d'apprentissage](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L205) et [les multiplie par les alphas stockés](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L210). Le module n'est qu'une bibliothèque : [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/lib.rs#L7) l'exporte et aucun autre fichier Rust du dépôt n'y fait référence, donc aucun outil MCP, aucune fonction DuckDB et aucune étape de pipeline n'offre l'ACP à noyau. La normalisation et la projection d'apprentissage s'écrivent :

```rust
        // Take top-k alphas and lambdas.
        let mut alphas = Array2::<f64>::zeros((n, self.n_components));
        let mut lambdas = Array1::<f64>::zeros(self.n_components);
        for r in 0..self.n_components {
            let lambda = eigenvalues[r].max(0.0);
            lambdas[r] = lambda;
            // Normalize alphas so that lambda * alpha.alpha = 1 (standard Kernel PCA convention)
            let norm = if lambda > 1e-12 { lambda.sqrt() } else { 1.0 };
            for i in 0..n {
                alphas[[i, r]] = eigenvectors[[i, r]] / norm;
            }
        }
```

```rust
        // Project training data. The closed form is
        // X_projected[i, r] = sqrt(lambda_r) * eigenvector[i, r]
        let mut projected = Array2::<f64>::zeros((n, self.n_components));
        for r in 0..self.n_components {
            let scale = lambdas[r].sqrt();
            for i in 0..n {
                projected[[i, r]] = eigenvectors[[i, r]] * scale;
            }
        }
```

- **Le test des anneaux ne teste pas une séparation.** [`test_rbf_kernel_separates_rings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L264) ajuste [deux composantes avec γ = 0,5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L276) sur les anneaux du §5 et vérifie seulement que la [moyenne des carrés de la première composante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L283) est [au-dessus de 10^-4](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L285). La transcription prédit l'image du §5 : deux carrés concentriques de rayons d'environ 0,583 et 0,653, qu'aucune droite ne sépare, et une moyenne des carrés d'environ 0,191, qui passe. L'exemple du module exécute les mêmes données et les mêmes réglages sous le commentaire [« Two rings of points — impossible to separate with linear PCA »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L29), et ne vérifie que [le nombre de colonnes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L42).
- **La note d'IX sur ce test rend le bon verdict pour une mauvaise raison.** La note [`kernel-pca-symmetric-centroid-trap.md`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L7) explique pourquoi une version antérieure du test, qui comparait les centres des anneaux sur la première composante, échouait : toute [« component of the projection has zero mean within each symmetric ring »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L45). Son verdict, [« This is not a Kernel PCA bug. »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L47), tient, mais pas sa raison : le §5 montre que l'affirmation vaut pour toutes les composantes sauf une : la composante radiale, quatrième à γ = 0,5, a pour moyennes sur les anneaux ±0,290 et aucune dispersion au sein d'un anneau. Le test antérieur échouait parce que cette composante n'était pas parmi les deux gardées, et non parce que la symétrie interdit une séparation. L'alternative de la note, la [séparation par paires](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L65), aurait échoué sur les deux composantes gardées : un point intérieur est à environ 0,070 de son voisin extérieur et à 0,824 du point intérieur suivant. La note recommande aussi de se demander [« what would this assertion look like on completely random data? »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/solutions/test-failures/kernel-pca-symmetric-centroid-trap.md#L77) L'assertion de remplacement échoue à cette vérification : la moyenne des carrés de la première composante vaut λ₁/n pour toutes données, et sur la droite régulièrement espacée du §5 avec γ = 0,5 elle vaut environ 0,250, plus que sur les anneaux.
- **Une composante de valeur propre minuscule est projetée de deux façons.** Le [seuil](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L144) garde α = v au lieu de v/√λ quand 0 < λ ≤ 10^-12, donc sur les points d'apprentissage `transform` renvoie λv là où `fit_transform` renvoie √λ v, un facteur √λ d'écart. Pour les points (±1, 0) et (0, ±5 · 10^-7) avec le noyau linéaire et deux composantes, λ₂ = 5 · 10^-13 : `fit_transform` donne les deuxièmes coordonnées ±5 · 10^-7, les vraies projections, et `transform` donne environ ±3,54 · 10^-13. Aucun test ne compare les deux voies : [`test_transform_out_of_sample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L308) ne vérifie que [la forme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L314) de sa sortie.
- **La documentation décrit des alphas que le code ne stocke pas.** La documentation du module donne la projection comme [`alpha_r[i] * sqrt(lambda_r)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L17) et appelle les alphas stockés les [vecteurs propres de la matrice de noyau centrée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L71), mais le code stocke les [vecteurs propres divisés par √λ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L146), comme le veut son propre [commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L143). Avec les alphas stockés, la formule documentée renvoie vᵢ au lieu de √λ vᵢ. La [projection d'apprentissage](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L156) du code multiplie les vecteurs propres par √λ et elle est juste.
- **Un noyau NaN renvoie quand même `Ok`.** Le MAT-013 a noté que le noyau polynomial, avec un [degré de type `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) élevé avec [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), donne NaN quand une base négative rencontre un degré fractionnaire. L'ajustement ne s'arrête pas là. La moyenne globale propage le NaN à tous les coefficients de K_c, `symmetric_eigen` effectue tous ses [100 balayages](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) sur des NaN, et l'[écrêtage](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) change chaque valeur propre NaN en 0, parce que `f64::max` de Rust renvoie l'autre opérande quand l'un est NaN. Sur le carré (±1, 0), (0, ±1) avec le degré 1,5, γ = 1 et c = 0, où k((1, 0), (−1, 0)) = (−1)^1,5, la transcription prédit 600 rotations, puis `Ok`, avec toutes les projections NaN et tous les λ nuls.
- **Les tests vérifient des formes plus que des propriétés.** Sur les six tests, le [test linéaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L243) vérifie une vraie propriété, des scores monotones le long d'une droite. Le test des anneaux vérifie une moyenne des carrés que presque toutes les données satisfont, le [test polynomial](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L292) et le test de `transform` vérifient des formes, et les deux derniers vérifient que `n_components` = 0 et `n_components` ≥ n sont rejetés. Aucun ne fait varier γ, ne compare `transform` à `fit_transform`, ni n'emploie de témoin négatif.
- **Ni préimage ni choix de la largeur de bande.** `KernelPca` n'a pas de préimage, pas de règle ni de recherche pour γ, et aucune vérification que la matrice de noyau est semi-définie positive.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Le test des anneaux d'IX garde deux composantes avec γ = 0,5. Calculer λ_rad = sᵀKs pour ses données, avec s = (1, 1, 1, 1, −1, −1, −1, −1)/√8, et expliquer pourquoi les moyennes sur les anneaux de la première composante sont égales alors que celles de la quatrième ne le sont pas.

> *Solution :* Dans l'anneau intérieur, les carrés des distances valent 2 entre voisins et 4 entre points opposés ; dans l'anneau extérieur, 8 et 16 ; entre les anneaux, 1 au même angle, 5 à angle droit et 9 à l'opposé. En sommant K sur les paires ordonnées avec γ = 0,5, le bloc intérieur donne 4 + 8e^−1 + 4e^−2 ≈ 7,484, le bloc extérieur 4 + 8e^−4 + 4e^−8 ≈ 4,148 et chaque bloc entre les anneaux 4e^−0,5 + 8e^−2,5 + 4e^−4,5 ≈ 3,127, donc λ_rad ≈ (7,484 + 4,148 − 2 × 3,127)/8 ≈ 0,672. C'est moins que 1,531, 1,531 et 1,216, donc s est le quatrième vecteur propre, et un ajustement à deux composantes ne le garde pas. La première composante appartient à la paire égale, orthogonale au plan des vecteurs constants sur chaque anneau, donc sa moyenne sur chaque anneau est nulle ; la quatrième est s lui-même, de scores ±√(0,672/8) ≈ ±0,290.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Noyau linéaire.** Appeler `fit_transform` avec le noyau linéaire et une composante sur les points 0, 1 et 3, puis `transform` sur le point 2. Prédiction : ±(−4/3, −1/3, 5/3) et ±2/3, de même signe, à 10^-12 près.
2. **Les anneaux.** Appeler `fit_transform` sur les données de `test_rbf_kernel_separates_rings` avec sept composantes, pour chaque γ du balayage 0,001, 0,01, 0,05, 0,1, 0,2, 0,5, 1, 2, 5 et 10, et trouver la composante dont les scores sont constants sur chaque anneau. Prédiction : c'est la quatrième pour chaque γ ; à γ = 0,5 les valeurs propres sont celles du §5, la quatrième composante a pour moyennes sur les anneaux ±0,290, et les deux premières placent les anneaux à des rayons d'environ 0,583 et 0,653.
3. **Anneaux de rayon intérieur 0,3.** Refaire l'étape 2 avec l'anneau intérieur de rayon 0,3 et l'extérieur de rayon 1, en ajoutant γ = 1,5, 1,6 et 50. Prédiction : la composante radiale est quatrième jusqu'à γ = 0,5, troisième à 1 et 1,5, et première à partir de 1,6, avec une avance d'environ 0,357 à γ = 5 et 1,2 · 10^-4 à γ = 50.
4. **Témoin négatif.** Appeler `fit_transform` avec deux composantes sur les points 0, 1, …, 7 d'une droite, sur le même balayage. Prédiction : la première composante est monotone jusqu'à γ = 0,05 et se replie aux deux bouts à partir de 0,1 ; son plus grand écart est entre les points 3 et 4 et vaut 0,145 de l'étendue à γ = 0,001 et 0,347 à γ = 2, 5 et 10 ; à γ = 0,5, la moyenne des carrés de la première composante vaut environ 0,250, au-dessus du 0,191 des anneaux.
5. **Transformation contre ajustement.** Sur les points (±1, 0) et (0, ±ε) avec le noyau linéaire et deux composantes, comparer `transform` sur les points d'apprentissage à `fit_transform`, pour ε = 10^-6 et 5 · 10^-7. Prédiction : concordance à 10^-15 près pour ε = 10^-6 ; pour ε = 5 · 10^-7, des deuxièmes coordonnées d'environ ±5 · 10^-7 et ±3,54 · 10^-13.
6. **Un degré fractionnaire.** Appeler `fit_transform` avec deux composantes et le noyau polynomial de degré 1,5, γ = 1 et c = 0 sur les points (±1, 0) et (0, ±1). Prédiction : `Ok`, avec toutes les projections NaN et les deux λ nuls.

### Exercice pratique

À l'étape 5, pour quels ε le seuil d'IX fait-il diverger `transform` de `fit_transform`, et de quel facteur ?

> *Solution :* Les points sont déjà centrés, et les valeurs propres non nulles de K_c = XXᵀ sont 2 et 2ε², avec le vecteur propre unitaire v₂ = (0, 0, 1, −1)/√2 pour 2ε². Le seuil garde α = v₂ quand 2ε² ≤ 10^-12, c'est-à-dire quand ε ≤ (5 · 10^-13)^(1/2) ≈ 7,07 · 10^-7. `fit_transform` renvoie alors √(2ε²) v₂, les vraies coordonnées ±ε, tandis que `transform` renvoie K_c v₂ = 2ε² v₂, les coordonnées ±√2 ε² : un facteur √2 ε, environ 7,07 · 10^-7 à ε = 5 · 10^-7, où les coordonnées valent ±5 · 10^-7 et environ ±3,54 · 10^-13. Renvoyer une colonne de zéros pour de telles composantes, dans les deux voies, les ferait concorder.

---

## 8. Pièges courants

- **Lire une séparation sur une seule valeur de γ.** Rapporter l'intervalle de γ sur lequel elle tient, et le rang de la composante qui la porte.
- **Sauter le témoin négatif.** Faire passer des données sans la structure par la même chaîne ; un critère qui y réussit ne mesure rien.
- **Vérifier une propriété que toute entrée possède.** Une variance non nulle, une forme correcte ou une valeur finie valent pour presque toutes les données ; un test doit pouvoir échouer quand la propriété manque.
- **Supposer que les premières composantes portent la structure.** La composante qui sépare peut être troisième ou quatrième ; regarder plus de composantes, et les valeurs propres, avant de conclure qu'un noyau a échoué.
- **Centrer un nouveau point avec ses propres statistiques.** Un nouveau point doit être centré avec les moyennes de lignes et la moyenne globale d'apprentissage, sinon son score n'est pas comparable aux scores d'apprentissage.
- **Se fier à une projection à γ grand.** Quand K est proche de l'identité, les valeurs propres non nulles sont toutes proches de 1 et les composantes sont arbitraires.
- **Comparer deux exécutions de l'ACP à noyau coordonnée par coordonnée.** Des valeurs propres égales, comme pour les anneaux, font de toute rotation de la paire égale une réponse également valide.
- **Employer un noyau qui n'est pas semi-défini positif.** Ses valeurs propres négatives n'ont aucune variance à expliquer, et les écrêter à 0 cache le problème.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **ACP à noyau** | L'ACP des images φ(xᵢ) dans l'espace de caractéristiques, calculée à partir de la matrice de noyau |
| **Astuce du noyau** | Remplacer les produits scalaires par des valeurs de noyau, de sorte que φ n'est jamais formée |
| **Matrice de noyau centrée** | K_c = JKJ, les produits scalaires des images centrées |
| **Coefficients duaux** | Les poids α = v/√λ qui expriment une direction unitaire de l'espace de caractéristiques à travers les images d'apprentissage |
| **Projection hors échantillon** | Le score Σⱼ αⱼ k̃ⱼ(x) d'un nouveau point, centré avec les statistiques d'apprentissage |
| **Largeur de bande** | L'échelle fixée par γ dans le noyau RBF exp(−γ‖x − y‖²) |
| **Composante radiale** | Pour des anneaux aux mêmes angles, le vecteur propre constant sur chaque anneau et orthogonal à 1, qui les sépare |
| **Témoin négatif** | Des données sans la structure cherchée, sur lesquelles un critère de détection doit échouer |
| **Effet fer à cheval** | La courbure d'une droite en arche par les premiers vecteurs propres d'un noyau local |
| **Problème de la préimage** | Trouver une entrée dont l'image est la plus proche d'un point donné de l'espace de caractéristiques |

---

## Auto-évaluation

**1. Un collègue montre un graphique d'ACP à noyau de données d'expression génique à γ = 3, avec deux groupes nets, et rien d'autre. Que demandez-vous ?**
> Le même graphique sur une plage de γ, avec la plage où les groupes restent séparés ; les valeurs propres, pour voir quelle composante porte la séparation et si elle est à égalité avec d'autres ; et la même chaîne sur un témoin négatif, comme les données avec chaque variable permutée indépendamment, ce qui garde la distribution de chaque variable et détruit la structure conjointe. Les groupes ne doivent pas y apparaître. Comme le montre le §5, des points régulièrement espacés sur une droite peuvent montrer un écart de plus du double de l'espacement régulier à γ grand.

**2. Pourquoi l'ACP à noyau avec le noyau linéaire ne peut-elle jamais séparer deux anneaux concentriques, alors qu'un noyau RBF le peut parfois ?**
> Avec le noyau linéaire, l'ACP à noyau est l'ACP, une projection linéaire, et aucune projection linéaire ne sépare les anneaux. L'espace de caractéristiques RBF contient, pour des anneaux aux mêmes angles, une direction dont les scores sont constants sur chaque anneau ; elle les sépare parfaitement, mais seulement quand sa valeur propre se classe parmi les composantes gardées, ce qui dépend de γ et de la géométrie.

**3. `transform` et `fit_transform` d'IX divergent sur les points d'apprentissage pour une composante. Que vérifiez-vous ?**
> La valeur propre de cette composante. IX garde α = v quand 0 < λ ≤ 10^-12, donc `transform` renvoie λv là où `fit_transform` renvoie √λ v. Une telle composante ne porte aucune variance utilisable : l'abandonner, ou réduire `n_components`.

**4. Un test nommé `test_rbf_kernel_separates_rings` vérifie que la première composante a une moyenne des carrés au-dessus de 10^-4. À quoi ressemblerait une assertion qui a un sens ?**
> À une assertion qui échoue quand les anneaux ne sont pas séparés : par exemple, qu'une composante gardée a tous les scores intérieurs d'un côté d'un seuil et tous les scores extérieurs de l'autre, avec une marge, en même temps que la même vérification échoue sur un témoin négatif. Avec les données d'IX et deux composantes à γ = 0,5, ce test échouerait, ce qui est le résultat honnête ; avec quatre composantes, il passerait sur la quatrième.

**Critères de réussite :** Déduire l'ACP à noyau de la forme de Gram de l'ACP, centrer une matrice de noyau et expliquer la borne de n − 1 composantes, normaliser les coefficients duaux et projeter de nouveaux points, décrire les limites en γ, analyser les anneaux par symétrie, concevoir un balayage de la largeur de bande avec un témoin négatif, et retracer où le test, la documentation et le seuil de `KernelPca` d'IX promettent plus que ce que le code fournit.

---

## Bases de recherche

- J. Mercer, « Functions of positive and negative type, and their connection with the theory of integral equations », *Philosophical Transactions of the Royal Society A* 209, 1909 : les noyaux positifs
- B. Schölkopf, A. Smola et K.-R. Müller, « Nonlinear component analysis as a kernel eigenvalue problem », *Neural Computation* 10, 1998 : l'ACP à noyau, le centrage dans l'espace de caractéristiques et la normalisation des coefficients duaux
- S. Mika, B. Schölkopf, A. Smola, K.-R. Müller, M. Scholz et G. Rätsch, « Kernel PCA and de-noising in feature spaces », *Advances in Neural Information Processing Systems* 11, 1999 : les préimages par itération
- C. K. I. Williams, « On a connection between kernel PCA and metric multidimensional scaling », *Machine Learning* 46, 2002 : l'ACP à noyau isotrope et le MDS
- B. Schölkopf et A. J. Smola, *Learning with Kernels*, MIT Press, 2002 : les noyaux, le centrage et la projection hors échantillon
- J. T. Kwok et I. W. Tsang, « The pre-image problem in kernel methods », *IEEE Transactions on Neural Networks* 15, 2004 : les préimages à partir des distances
- P. Diaconis, S. Goel et S. Holmes, « Horseshoes in multidimensional scaling and local kernel methods », *Annals of Applied Statistics* 2, 2008 : l'effet fer à cheval
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
