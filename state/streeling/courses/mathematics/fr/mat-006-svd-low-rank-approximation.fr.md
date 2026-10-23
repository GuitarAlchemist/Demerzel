---
module_id: mat-006-svd-low-rank-approximation
department: mathematics
course: Décomposition en valeurs singulières et approximation de rang faible
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms, mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Décomposition en valeurs singulières et approximation de rang faible — La meilleure simplification d'une matrice

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Énoncer la décomposition en valeurs singulières et la déduire du théorème spectral de MAT-005
- Calculer à la main la SVD d'une matrice 2 × 2
- Lire la norme, le rang, le conditionnement et le déterminant d'une matrice sur ses valeurs singulières
- Énoncer le théorème d'Eckart–Young–Mirsky et calculer l'erreur d'une meilleure approximation de rang k
- Choisir une tolérance de rang relative à la plus grande valeur singulière, et expliquer pourquoi une tolérance absolue échoue
- Expliquer comment la méthode de Jacobi unilatérale calcule la SVD, et dire ce que l'implémentation d'IX garantit ou non

---

## 1. Toute matrice est une rotation, un étirement et une rotation

**Décomposition en valeurs singulières.** Toute matrice réelle A de taille m × n s'écrit

A = U Σ Vᵀ,

où U (m × m) et V (n × n) sont orthogonales, et Σ (m × n) est nulle sauf sur sa diagonale, dont les coefficients σ₁ ≥ σ₂ ≥ … ≥ 0 sont les **valeurs singulières**. Les colonnes de V sont les **vecteurs singuliers à droite**, celles de U les **vecteurs singuliers à gauche**, et A vᵢ = σᵢ uᵢ pour i ≤ min(m, n) ; quand n > m, les colonnes restantes de V vérifient A vᵢ = 0.

Lue de droite à gauche : Vᵀ tourne l'entrée, Σ l'étire le long des axes de coordonnées, et U tourne le résultat. Quand A est de rang colonne plein, la sphère unité devient un ellipsoïde dont les demi-axes ont pour longueurs les σᵢ et pour directions les uᵢ. Avec k = min(m, n), la **SVD réduite** ne garde que les k premières colonnes de U et de V ; c'est la forme que renvoie IX.

La SVD découle du théorème spectral de MAT-005. La matrice AᵀA est symétrique, et xᵀAᵀAx = ‖Ax‖² ≥ 0, donc ses valeurs propres λᵢ sont réelles et positives ou nulles. Prenons une base orthonormée v₁, …, vₙ de vecteurs propres, rangés de sorte que λ₁ ≥ λ₂ ≥ … ≥ λₙ, et posons σᵢ = √λᵢ. Pour i ≠ j, (A vᵢ) · (A vⱼ) = vᵢᵀAᵀA vⱼ = λⱼ (vᵢ · vⱼ) = 0, et ‖A vᵢ‖² = λᵢ = σᵢ². Les vecteurs uᵢ = A vᵢ / σᵢ, pour σᵢ > 0, sont donc orthonormés, et A vᵢ = σᵢ uᵢ. Tout autre vᵢ vérifie ‖A vᵢ‖² = λᵢ = 0, donc A vᵢ = 0 ; quand n > m, c'est le cas au moins des n − m derniers, puisque AᵀA est de rang au plus m. Compléter les uᵢ en une base orthonormée de ℝᵐ et placer σ₁, …, σₖ, avec k = min(m, n), sur la diagonale de Σ donne A V = U Σ, c'est-à-dire A = U Σ Vᵀ.

Contrairement aux valeurs propres (MAT-005 §1), les valeurs singulières existent toujours et sont réelles et positives ou nulles, pour toute matrice : carrée ou non, symétrique ou non.

### Exercice pratique

Calculez la SVD de B = [[3, 0], [4, 5]].

> *Solution :* BᵀB = [[3 · 3 + 4 · 4, 3 · 0 + 4 · 5], [0 · 3 + 5 · 4, 0 · 0 + 5 · 5]] = [[25, 20], [20, 25]]. Sa trace vaut 50 et son déterminant 625 − 400 = 225, donc ses valeurs propres sont 45, pour v₁ = (1, 1)/√2, et 5, pour v₂ = (1, −1)/√2. Ainsi σ₁ = √45 = 3√5 et σ₂ = √5. Puis u₁ = B v₁/σ₁ = (3, 9)/(√2 · 3√5) = (1, 3)/√10 et u₂ = B v₂/σ₂ = (3, −1)/(√2 · √5) = (3, −1)/√10, qui sont orthogonaux : 3 − 3 = 0.

---

## 2. Ce que disent les valeurs singulières

Les valeurs singulières résument une matrice :
- **Norme.** ‖A‖₂ = σ₁ : la norme 2 induite de MAT-004 est le plus grand étirement.
- **Taille.** ‖A‖_F² = σ₁² + σ₂² + …, où la norme de Frobenius ‖A‖_F est la racine carrée de la somme des carrés de tous les coefficients ; la multiplication par des matrices orthogonales ne la change pas.
- **Rang.** Le rang de A est le nombre de valeurs singulières non nulles.
- **Conditionnement.** Pour A carrée inversible, le conditionnement de MAT-003 vaut κ₂(A) = σ₁/σₙ.
- **Volume.** Pour A carrée, |det A| = σ₁σ₂…σₙ : U et V conservent les longueurs et les angles, donc les volumes, et par la règle du produit de MAT-004 seule Σ les change, du produit de sa diagonale.

### Exercice pratique

Pour la matrice B du §1, donnez ‖B‖₂, ‖B‖_F, κ₂(B) et |det B| à partir de ses valeurs singulières, et vérifiez-en deux directement.

> *Solution :* ‖B‖₂ = 3√5, ‖B‖_F = √(45 + 5) = √50, κ₂(B) = 3√5/√5 = 3 et |det B| = 3√5 · √5 = 15. Directement, les carrés des coefficients totalisent 9 + 0 + 16 + 25 = 50, et det B = 3 · 5 − 0 · 4 = 15.

---

## 3. Approximation de rang faible

Écrite colonne par colonne, la SVD est une somme de matrices de rang 1 par ordre d'importance décroissant :

A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + … .

Garder les k premiers termes donne la **troncature de rang k** A_k.

**Théorème d'Eckart–Young–Mirsky.** Pour toute matrice X de rang au plus k, ‖A − X‖₂ ≥ σₖ₊₁ et ‖A − X‖_F ≥ √(σₖ₊₁² + σₖ₊₂² + …), avec égalité pour X = A_k.

L'erreur de la troncature elle-même se lit facilement : A − A_k = σₖ₊₁uₖ₊₁vₖ₊₁ᵀ + … est encore écrite comme une SVD, donc sa norme 2 est sa plus grande valeur singulière σₖ₊₁, et sa norme de Frobenius la racine carrée de la somme des carrés de ses valeurs singulières. La partie difficile du théorème est qu'aucune autre matrice de rang k ne fait mieux ; les Bases de recherche donnent les démonstrations. Deux conséquences en découlent : l'erreur décroît quand k augmente et atteint 0 en k = rang A, et une matrice est « presque de rang k » en norme 2 exactement quand σₖ₊₁ est petite devant σ₁ ; en norme de Frobenius, c'est toute la queue √(σₖ₊₁² + σₖ₊₂² + …) qui doit être petite devant ‖A‖_F. C'est ce qu'utilisent la compression, le débruitage et l'analyse sémantique latente.

### Exercice pratique

Donnez la meilleure approximation de rang 1 de A = diag(3, 2, 1) et son erreur dans les deux normes. Faites ensuite de même pour la matrice B du §1.

> *Solution :* La SVD de diag(3, 2, 1) est la matrice elle-même, avec U = V = I, donc A₁ = diag(3, 0, 0), avec ‖A − A₁‖₂ = 2 et ‖A − A₁‖_F = √(4 + 1) = √5. Pour B, B₁ = 3√5 · u₁v₁ᵀ = 3√5 · [[1, 1], [3, 3]]/(√10 · √2) = (3/2) [[1, 1], [3, 3]]. Seule σ₂ = √5 reste, donc les deux erreurs valent √5. Vérification : B − B₁ = [[3/2, −3/2], [−1/2, 1/2]], dont les carrés des coefficients totalisent 9/4 + 9/4 + 1/4 + 1/4 = 5.

---

## 4. Rang numérique

En arithmétique flottante, une valeur singulière nulle en arithmétique exacte sort en général comme un minuscule nombre non nul. « Le rang est le nombre de σ non nulles » doit alors devenir « le nombre de σ au-dessus d'une tolérance », et la tolérance doit être **relative** à σ₁ : multiplier A par 10^6 multiplie chaque valeur singulière par 10^6 et ne change pas le rang. Une convention courante, celle de `matrix_rank` de NumPy, est max(m, n) · σ₁ · ε, où ε = 2^-52 est l'epsilon machine de MAT-003. Une tolérance absolue mesure l'échelle de la matrice, pas son rang.

La même tolérance gouverne la **pseudo-inverse** A⁺ = V Σ⁺ Uᵀ, où Σ⁺ inverse les valeurs singulières au-dessus de la tolérance et met les autres à 0. Quand seules les valeurs singulières nulles en arithmétique exacte sont écartées, A⁺b est la solution des moindres carrés de plus petite norme. Quand la tolérance écarte aussi de petites valeurs non nulles, A⁺ est la pseudo-inverse de la matrice tronquée, et A⁺b résout ce problème tronqué, pas le problème d'origine. Là, le choix compte doublement : une valeur singulière gardée juste au-dessus de la tolérance apporte le terme énorme 1/σ.

### Exercice pratique

Une bibliothèque déclare nulle toute valeur singulière inférieure à 10^-10. Quel rang annonce-t-elle pour 10^-12 · I₃, et lequel annonce la convention relative ?

> *Solution :* Les trois valeurs singulières de 10^-12 · I₃ valent toutes 10^-12, sous 10^-10, donc la bibliothèque annonce le rang 0 pour une matrice de rang 3. La tolérance relative vaut 3 · 10^-12 · ε, environ 6,7 · 10^-28, très en dessous de 10^-12, donc la convention relative annonce le rang 3. Seule la réponse relative reste la même quand on change l'échelle de la matrice.

---

## 5. Calculer la SVD par Jacobi unilatéral

La **méthode de Jacobi unilatérale** (Hestenes, 1958) ne forme jamais AᵀA, dont le conditionnement est le carré de celui de A quand A est de rang colonne plein (MAT-003). Elle fait tourner des couples de colonnes de A elle-même, ce qui multiplie A à droite par des rotations planes, jusqu'à ce que toutes les colonnes soient orthogonales. À ce stade A V = W, où V est le produit des rotations et où les colonnes de W sont orthogonales : leurs normes sont les valeurs singulières, avec n − m zéros de plus quand n > m, puisqu'au plus m d'entre elles peuvent être non nulles. Normaliser les colonnes de norme non nulle donne les colonnes correspondantes de U ; une colonne de norme 0 ne peut pas être normalisée, et le reste de U se complète par des vecteurs orthonormés quelconques.

Pour deux colonnes a_p et a_q, la rotation est la rotation de Jacobi de MAT-005 §4 appliquée à la matrice 2 × 2 [[a_p · a_p, a_p · a_q], [a_p · a_q, a_q · a_q]], un bloc de AᵀA calculé à partir des deux colonnes seules. Après la rotation, les deux colonnes sont orthogonales. Comme dans MAT-005, une rotation ultérieure peut défaire une rotation antérieure, donc la méthode balaie tous les couples à plusieurs reprises.

### Exercice pratique

Appliquez une rotation aux colonnes a_p = (3, 4) et a_q = (0, 5) de la matrice B du §1, avec la mise à jour a_p ← c a_p − s a_q et a_q ← s a_p + c a_q.

> *Solution :* a_p · a_p = 25, a_q · a_q = 25 et a_p · a_q = 20, donc θ = (25 − 25)/(2 · 20) = 0, ce qui donne t = 1 et c = s = 1/√2. Les nouvelles colonnes sont ((3, 4) − (0, 5))/√2 = (3, −1)/√2 et ((3, 4) + (0, 5))/√2 = (3, 9)/√2. Elles sont orthogonales, puisque 9 − 9 = 0, de normes √10/√2 = √5 et √90/√2 = 3√5 : les valeurs singulières du §1. Les normaliser donne u₂ = (3, −1)/√10 et u₁ = (1, 3)/√10.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**Le solveur** (`crates/ix-math/src/svd.rs`). [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100) est la méthode de Jacobi unilatérale du §5, avec au plus 50 balayages et une tolérance de 10^-12. Il renvoie la SVD réduite, avec les valeurs singulières par ordre décroissant. Le test qui saute un couple déjà orthogonal est [relatif](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L136) aux tailles des deux colonnes, donc les rotations ne dépendent pas de l'échelle de A. Le commentaire du test d'arrêt revendique la même propriété, mot pour mot aux lignes 168 à 176 :

```rust
        // Scale-invariant stopping criterion: the off-diagonal Frobenius
        // mass should be a small fraction of the matrix's total Frobenius
        // mass. Using an absolute threshold (the old behavior) meant that
        // well-scaled matrices converged in 1-2 sweeps while any matrix
        // with entries much larger than `tol` stayed above the threshold
        // indefinitely.
        if off_diag_sum_sq < tol * tol * a_frob_sq {
            break;
        }
```

Son contrat a quatre limites à connaître :
- **Le test d'arrêt n'est pas invariant d'échelle.** `off_diag_sum_sq` additionne les carrés des produits a_p · a_q, qui sont des coefficients de AᵀA : multiplier A par s le multiplie par s⁴. `a_frob_sq` vaut ‖A‖_F², multiplié par s². Les deux membres n'ont pas le même degré : le test demande √`off_diag_sum_sq` < (10^-12/‖A‖_F) · ‖A‖_F², une tolérance de 10^-12/‖A‖_F relative à la taille de AᵀA, au lieu de 10^-12. Quand ‖A‖_F est grande, cette tolérance passe sous ce qui reste d'ordinaire une fois la méthode convergée : les couples que le test de saut laisse de côté, dont le produit est sous 10^-12 relativement aux tailles des colonnes mais non nul, et l'arrondi (MAT-003). Pour une telle matrice, le test n'est jamais satisfait, et l'appel effectue les 50 balayages : le résultat reste exact, puisque plus rien ne tourne, mais il coûte bien plus cher. Seuls des produits exactement nuls l'arrêtent encore tôt, comme pour un multiple de l'identité, dont le premier balayage trouve `off_diag_sum_sq` = 0. Quand ‖A‖_F est de l'ordre de 10^-12 ou moins, le test est satisfait à la fin du premier balayage, ce qui, avec plus de deux colonnes, peut les laisser loin d'être orthogonales. Comparer `off_diag_sum_sq` à `tol * tol * a_frob_sq * a_frob_sq` donnerait aux deux membres le degré 4.
- **La promesse n'est pas vérifiée.** Le commentaire de documentation dit [« Guaranteed to converge for any real matrix »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L97). La théorie le garantit bien, mais la [boucle de balayages](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L123) s'arrête après 50 balayages, et la fonction renvoie alors [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L209), que le test d'arrêt ait été satisfait ou non.
- **Un seuil absolu subsiste.** Les vecteurs singuliers à gauche sont extraits par la boucle ci-dessous, mot pour mot aux lignes 195 à 207. Une colonne de U n'est remplie que si sa valeur singulière dépasse `tol`, le 10^-12 absolu ; sinon elle reste nulle, et `reconstruct` omet alors ce terme. Les valeurs singulières suivent l'échelle de A, mais pas ce test, comme le seuil de pivot de `inverse` dans MAT-003. L'exercice ci-dessous en montre la conséquence.

```rust
    // Take top-k columns.
    let mut v_sorted = Array2::<f64>::zeros((n, k));
    for (rank, (sig, orig)) in sigma_col.into_iter().take(k).enumerate() {
        singular_values[rank] = sig;
        if sig > tol {
            for i in 0..m {
                u[[i, rank]] = work[[i, orig]] / sig;
            }
        }
        for i in 0..n {
            v_sorted[[i, rank]] = v[[i, orig]];
        }
    }
```

- **L'appelant choisit la tolérance de rang.** [`rank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) et [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) comparent les valeurs singulières à une tolérance absolue `tol` fournie par l'appelant, et c'est à l'appelant de la rendre relative. Deux appelants le font, différemment. Le gestionnaire de l'outil MCP `ix_svd`, [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L627), utilise [σ₁ · 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639). Le test de rang de l'espace d'états utilise [max(m, n) · σ₁ · ε](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L397), la convention du §4, avec une [note](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L395) selon laquelle la SVD de Jacobi laisse une valeur singulière nulle en arithmétique exacte vers 10^-16 · σ₁ plutôt qu'à 0.

[`truncated_svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L223) calcule la SVD complète et en garde les k premières composantes : la A_k du §3. L'outil MCP `ix_svd` ne la propose pas : son [schéma d'entrée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L435) prend une matrice et rien d'autre.

Deux tests méritent un examen plus attentif. [`test_svd_scale_invariance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L327) vérifie que multiplier A [par 10^6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L333) multiplie les valeurs singulières et garde la reconstruction exacte. Son commentaire dit que le critère relatif a corrigé l'ancien, qui « would have required many more sweeps to converge (or failed to converge within the default 50) ». Les assertions vérifient l'exactitude, pas les balayages : ‖10^6 · A‖_F vaut environ 10^7, donc d'après la première limite ci-dessus le test d'arrêt demande une tolérance relative d'environ 10^-19, sous le niveau d'arrondi de MAT-003, et l'appel devrait effectuer les 50 balayages, le cas que le commentaire présente comme corrigé. Le test ne change en outre l'échelle que vers le haut, alors que le seuil absolu ci-dessus agit vers le bas. [`test_truncated_svd_rank_1_approx`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L305) vérifie que la troncature de rang 1 de A = [[1, 2], [3, 4], [5, 6]] a une erreur relative de Frobenius [inférieure à 0,10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L315). Eckart–Young donne la valeur exacte : AᵀA = [[35, 44], [44, 56]] a pour polynôme caractéristique λ² − 91λ + 24, de racines (91 ± √8185)/2, donc σ₁ ≈ 9,53, σ₂ ≈ 0,514, ‖A‖_F = √91 et la meilleure erreur relative vaut σ₂/√91 ≈ 0,054. Le test accepterait aussi une approximation jusqu'à 1,8 fois moins bonne que la meilleure.

**La question ouverte de MAT-003.** Dans le laboratoire Learn, MAT-003 a mesuré que le κ₂ d'IX des matrices de Hilbert stockées fl(H_2) à fl(H_16) change, pour 10 des 15 tailles, quand on multiplie la matrice par 2^-20 ou 2^20, et en a laissé la cause ouverte. Le test d'arrêt l'explique. Multiplier par une puissance de deux est exact, et tant que rien ne sous-déborde ni ne déborde, comme ici, chaque opération de `svd` sur la matrice mise à l'échelle l'est aussi : chaque produit, chaque rotation et chaque décision de saut est celui de fl(H_n), multiplié par une puissance de deux. Seul le nombre de balayages peut différer, et là où les balayages supplémentaires font encore tourner des colonnes, les bits changent. Une transcription de `svd` en Python qui suit l'ordre de sommation de `ndarray` prédit de 2 à 4 balayages à 2^-20, de 2 à 6 à l'échelle 1, et les 50 à 2^20. Elle reproduit les 15 valeurs de κ₂ imprimées par le laboratoire, aux trois chiffres imprimés, et son décompte de 5 tailles identiques sur 15. C'est une analyse, pas une exécution d'IX ; l'étape 4 du §7 permet au laboratoire de la vérifier avec [`svd_with_opts`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L105), qui plafonne le nombre de balayages.

### Exercice pratique

Avec A = [[1, 2], [3, 4], [5, 6]], prédisez ce que renvoient `svd(10^-13 · A).reconstruct()` et `svd(10^-12 · A).reconstruct()`.

> *Solution :* A a deux colonnes, donc une seule rotation les rend orthogonales, quoi que décide le test d'arrêt, et cette rotation ne dépend que de rapports entre les produits des colonnes : c'est la rotation utilisée pour A. Les valeurs singulières sortent donc comme celles de A multipliées par l'échelle, aux arrondis près. Pour 10^-13 · A, elles valent environ 9,53 · 10^-13 et 5,14 · 10^-14, toutes deux sous 10^-12 : les deux colonnes de U restent nulles, et `reconstruct` renvoie la matrice nulle, une erreur relative de 1. Pour 10^-12 · A, elles valent environ 9,53 · 10^-12, gardée, et 5,14 · 10^-13, écartée : `reconstruct` renvoie en silence la troncature de rang 1, avec une erreur relative d'environ 0,054, qui est exactement l'erreur d'Eckart–Young du test ci-dessus et semble plausible. C'est une prédiction tirée de la lecture du code, pas une exécution ; le §7 la vérifie.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **Eckart–Young pour chaque k.** Sur A = [[1, 2], [3, 4], [5, 6]] et sur M = [[1, 2, 3], [4, 5, 6], [7, 8, 10]], la matrice du [test MCP](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1311) d'IX, calculez ‖A − A_k‖_F avec `truncated_svd` pour chaque k, et comparez-la à √(σₖ₊₁² + …) calculée à partir de `svd`. Prédiction : égales à 10^-9 · ‖A‖_F près, décroissantes en k, et nulles aux arrondis près en k = rang A.
2. **Un balayage d'échelles.** Pour s = 10^-14, 10^-13, …, 10^12, calculez les valeurs singulières de s · A et de s · M divisées par s, et l'erreur relative de `reconstruct`. Prédiction pour A : les valeurs singulières coïncident avec celles de A à 10^-12 près en relatif à toutes les échelles ; l'erreur relative est inférieure à 10^-12 pour s ≥ 10^-11, environ 0,054 pour s = 10^-12, et exactement 1 pour s ≤ 10^-13. Prédiction pour M : les valeurs singulières coïncident à 10^-12 près en relatif pour s ≥ 10^-10 ; pour s ≤ 10^-13, où la boucle s'arrête après le premier balayage, au moins l'une d'elles est fausse de plus de 100 %.
3. **Le coût de l'échelle.** Chronométrez de nombreux appels de `svd` sur A et sur 10^6 · A, et sur M et 10^6 · M. Prédiction : les appels mis à l'échelle prennent plusieurs fois plus de temps, puisqu'ils effectuent les 50 balayages.
4. **L'énigme de MAT-003.** Pour n = 2 à 16, calculez `svd_with_opts(2^20 · fl(H_n), k, 10^-12)` pour k = 1 à 6 et divisez ses valeurs singulières par 2^20. À cette échelle, le test d'arrêt n'est jamais satisfait, donc exactement k balayages s'exécutent. Prédiction : le résultat reproduit bit à bit les valeurs singulières de `svd(fl(H_n))` pour une première valeur de k, et celles de `svd(2^-20 · fl(H_n))` divisées par 2^-20 pour une seconde : k = 2 et 2 pour n = 2, 4 et 3 pour n = 3 à 6, 5 et 4 pour n = 7 à 14, et 6 et 4 pour n = 15 et 16.
5. **Conventions de rang.** Appelez `ix_svd` sur [[1, 2], [2, 4]]. Prédiction : rang 1. Appelez `rank` avec la tolérance 10^-10 sur la SVD de 10^-12 · I₃. Prédiction : 0, contre 3 avec la convention relative du §4.
6. **La borne du test.** Calculez l'erreur relative de la troncature de rang 1 de la matrice du test. Prédiction : 0,054 à trois décimales près, contre la borne 0,10 que vérifie le test.

### Exercice pratique

Supposons que l'étape 2 confirme que les valeurs singulières de s · A sont proportionnelles à s à toutes les échelles. Pourquoi cela ne suffit-il pas pour faire confiance à `svd` à toutes les échelles ?

> *Solution :* D'abord, les valeurs singulières peuvent être justes alors que U est fausse : sous 10^-12, les colonnes de U restent nulles bien que les valeurs singulières soient correctes. Ensuite, A n'a que deux colonnes, donc une rotation règle tout, et un arrêt prématuré après le premier balayage ne peut pas s'y voir ; M, avec trois colonnes, devrait le montrer. Une vérification digne de confiance teste les invariants de la décomposition entière, A = U Σ Vᵀ et des colonnes de U orthonormées pour chaque valeur singulière non nulle, comme dans MAT-005 §5, sur des matrices de plus de deux colonnes, et à toutes les échelles, pas seulement celle qu'utilisent les tests.

---

## 8. Pièges courants

- **Calculer les valeurs singulières comme racines carrées des valeurs propres de AᵀA.** Former AᵀA élève au carré le conditionnement d'une matrice de rang colonne plein, et les petites valeurs singulières perdent leur précision en premier.
- **Utiliser un seuil de rang absolu.** Il mesure l'échelle de la matrice, pas son rang.
- **Se fier aux seules valeurs singulières.** U et V peuvent être fausses alors que les valeurs singulières sont justes : testez A = U Σ Vᵀ.
- **Tester une quantité connue avec une borne lâche.** Quand un théorème donne l'erreur exacte, un test avec une borne presque deux fois plus grande laisse passer des erreurs.
- **Confondre valeurs singulières et valeurs propres.** Pour une matrice symétrique, les valeurs singulières sont les valeurs absolues des valeurs propres, mais pas en général : le cisaillement de l'auto-évaluation 2 a les valeurs propres 1 et 1.
- **Comparer des quantités de degrés différents.** Un test n'est invariant d'échelle que si ses deux membres varient de la même façon : une somme de carrés de coefficients de AᵀA est de degré 4 en A, ‖A‖_F² de degré 2.
- **Prendre un commentaire pour une garantie.** « Guaranteed to converge » est un théorème sur la méthode, et « scale-invariant » une affirmation sur le code ; le code doit encore signaler le premier, et un test vérifier la seconde.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Décomposition en valeurs singulières** | A = U Σ Vᵀ, avec U et V orthogonales et Σ diagonale de coefficients σ₁ ≥ σ₂ ≥ … ≥ 0 |
| **Valeurs singulières** | Les coefficients diagonaux de Σ : les racines carrées des valeurs propres de AᵀA |
| **Vecteurs singuliers à gauche et à droite** | Les colonnes uᵢ de U et vᵢ de V, avec A vᵢ = σᵢ uᵢ pour i ≤ min(m, n) |
| **SVD réduite** | La SVD qui ne garde que les min(m, n) premières colonnes de U et de V |
| **Norme de Frobenius** | ‖A‖_F, la racine carrée de la somme des carrés de tous les coefficients, égale à √(σ₁² + σ₂² + …) |
| **Troncature de rang k** | A_k = σ₁u₁v₁ᵀ + … + σₖuₖvₖᵀ |
| **Théorème d'Eckart–Young–Mirsky** | A_k est une meilleure approximation de rang au plus k, d'erreurs σₖ₊₁ en norme 2 et √(σₖ₊₁² + …) en norme de Frobenius |
| **Rang numérique** | Le nombre de valeurs singulières au-dessus d'une tolérance relative à σ₁ |
| **Pseudo-inverse** | A⁺ = V Σ⁺ Uᵀ, qui inverse les valeurs singulières au-dessus de la tolérance |
| **Jacobi unilatéral** | La rotation de couples de colonnes de A jusqu'à ce qu'elles soient orthogonales ; leurs normes sont les valeurs singulières |

---

## Auto-évaluation

**1. Pourquoi les valeurs singulières de toute matrice réelle sont-elles réelles et positives ou nulles, alors que ses valeurs propres peuvent ne pas l'être ?**
> Ce sont les racines carrées des valeurs propres de AᵀA, qui est symétrique, donc de valeurs propres réelles (MAT-005), et qui vérifie xᵀAᵀAx = ‖Ax‖² ≥ 0, donc de valeurs propres positives ou nulles.

**2. Le cisaillement S = [[1, 1], [0, 1]] a la valeur propre 1, deux fois. Quelles sont ses valeurs singulières, et que vaut κ₂(S) ?**
> SᵀS = [[1, 1], [1, 2]] a pour polynôme caractéristique λ² − 3λ + 1, de racines (3 ± √5)/2. Leurs racines carrées sont σ₁ = (1 + √5)/2, le nombre d'or, et σ₂ = (√5 − 1)/2, son inverse, puisque ((1 ± √5)/2)² = (3 ± √5)/2. Donc κ₂(S) = σ₁/σ₂ = (3 + √5)/2, environ 2,62, bien que les deux valeurs propres valent 1 : pour une matrice non symétrique, les valeurs propres ne montrent pas le conditionnement.

**3. Pourquoi l'erreur en norme 2 de la meilleure approximation de rang k vaut-elle σₖ₊₁ et non √(σₖ₊₁² + σₖ₊₂² + …) ?**
> Les valeurs singulières de A − A_k sont σₖ₊₁, σₖ₊₂, …, et la norme 2 d'une matrice est sa plus grande valeur singulière, σₖ₊₁. La norme de Frobenius additionne les carrés de toutes.

**4. Le test `test_svd_scale_invariance` d'IX passe. Que garantit-il sur l'échelle, et que manque-t-il ?**
> Il vérifie que multiplier par 10^6 garde les valeurs singulières et la reconstruction exactes. Il manque le coût : à cette échelle, le test d'arrêt n'est jamais satisfait, et l'appel devrait effectuer les 50 balayages. Il manque aussi la réduction d'échelle, où le seuil absolu de 10^-12 sur les valeurs singulières laisse des colonnes de U à zéro, et où `reconstruct` omet des termes en silence (§6).

**Critères de réussite :** Déduire et calculer une SVD à la main, lire la norme, le rang, le conditionnement et le déterminant sur les valeurs singulières, calculer les meilleures approximations de rang faible et leurs erreurs, choisir une tolérance de rang relative, effectuer une rotation de Jacobi unilatérale, et repérer où la SVD d'IX dépend de l'échelle de son entrée.

---

## Bases de recherche

- C. Eckart et G. Young, « The approximation of one matrix by another of lower rank », *Psychometrika* 1, 1936 : la meilleure approximation de rang faible en norme de Frobenius
- L. Mirsky, « Symmetric gauge functions and unitarily invariant norms », *Quarterly Journal of Mathematics* 11, 1960 : le même résultat pour toute norme unitairement invariante, dont la norme 2
- M. R. Hestenes, « Inversion of matrices by biorthogonalization and related results », *Journal of the Society for Industrial and Applied Mathematics* 6, 1958 : la méthode de Jacobi unilatérale
- J. Demmel et K. Veselić, « Jacobi's method is more accurate than QR », *SIAM Journal on Matrix Analysis and Applications* 13, 1992 : la précision des méthodes de Jacobi
- L. N. Trefethen et D. Bau, *Numerical Linear Algebra*, SIAM, 1997, leçons 4 et 5 : la SVD, sa géométrie et l'approximation de rang faible
- G. H. Golub et C. F. Van Loan, *Matrix Computations*, 4e éd., Johns Hopkins University Press, 2013, ch. 2 et 8 : la SVD, le rang numérique et les méthodes de Jacobi pour la SVD
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
