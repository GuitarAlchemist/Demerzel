---
module_id: mat-005-symmetric-eigenproblems
department: mathematics
course: Problèmes aux valeurs propres symétriques
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Problèmes aux valeurs propres symétriques — Les directions qu'une matrice ne fait qu'étirer

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Trouver à la main les valeurs propres et les vecteurs propres d'une matrice 2 × 2
- Énoncer le théorème spectral pour les matrices symétriques réelles, en démontrer les étapes clés, et montrer par des contre-exemples ce qui échoue sans symétrie
- Utiliser le quotient de Rayleigh pour encadrer les valeurs propres et pour en estimer une à partir d'un vecteur propre approché
- Effectuer une rotation de Jacobi et expliquer pourquoi la méthode de Jacobi cyclique converge
- Expliquer pourquoi une valeur propre multiple détermine son sous-espace propre mais pas ses vecteurs propres, et tester correctement un tel résultat
- Expliquer quand la méthode de la puissance échoue, et dire ce que les solveurs de valeurs propres d'IX garantissent ou non

---

## 1. Valeurs propres et vecteurs propres

Un vecteur non nul v est un **vecteur propre** d'une matrice carrée A, de **valeur propre** λ, si

A v = λ v.

Dans la direction de v, A ne fait qu'étirer, du facteur λ, et retourne la direction si λ < 0. Comme A v = λ v signifie (A − λI) v = 0 avec v ≠ 0, la matrice A − λI n'est pas inversible, donc λ est une racine du **polynôme caractéristique** det(A − λI) (MAT-004). Pour une matrice 2 × 2, ce polynôme est

λ² − (tr A) λ + det A,

où la trace tr A est la somme des coefficients diagonaux. Pour A = [[2, 1], [1, 2]], il vaut λ² − 4λ + 3 = (λ − 3)(λ − 1) : les valeurs propres sont 3, pour v = (1, 1), et 1, pour v = (1, −1).

Deux contre-exemples montrent qu'une matrice réelle ne donne pas toujours une image aussi nette :
- **Aucune valeur propre réelle.** La rotation de 90° de MAT-004, R = [[0, −1], [1, 0]], a pour polynôme caractéristique λ² + 1, qui n'a pas de racine réelle : aucune direction du plan n'est simplement étirée par un quart de tour.
- **Trop peu de vecteurs propres.** Le cisaillement [[1, 1], [0, 1]] a la valeur propre double 1, mais seuls les multiples de (1, 0) sont des vecteurs propres, donc aucune base de R² n'est formée de ses vecteurs propres.

### Exercice pratique

Trouvez les valeurs propres et les vecteurs propres de A = [[5, 2], [2, 2]], et vérifiez que les vecteurs propres sont orthogonaux.

> *Solution :* tr A = 7 et det A = 10 − 4 = 6, donc le polynôme caractéristique est λ² − 7λ + 6 = (λ − 6)(λ − 1). Pour λ = 6, A − 6I = [[−1, 2], [2, −4]], dont les deux lignes disent x = 2y : v = (2, 1), et en effet A (2, 1) = (12, 6) = 6 · (2, 1). Pour λ = 1, A − I = [[4, 2], [2, 1]], dont les deux lignes disent y = −2x : w = (1, −2), et A (1, −2) = (1, −2). Enfin v · w = 2 − 2 = 0.

---

## 2. Le théorème spectral

Une matrice est **symétrique** si Aᵀ = A, c'est-à-dire si son coefficient en ligne i et colonne j est égal à celui en ligne j et colonne i. Les deux contre-exemples du §1 ne sont pas symétriques, et ce n'est pas un hasard :

**Théorème spectral.** Une matrice symétrique réelle A de taille n × n a n valeurs propres réelles, comptées avec multiplicité, et une base orthonormée de vecteurs propres. De façon équivalente, A = Q Λ Qᵀ, où Q est **orthogonale** (QᵀQ = I ; ses colonnes sont les vecteurs propres) et Λ est la matrice diagonale des valeurs propres.

Dans la base de ses vecteurs propres, une matrice symétrique n'est qu'une dilatation le long d'axes perpendiculaires. Deux étapes de la démonstration sont courtes :
- **Des vecteurs propres de valeurs propres différentes sont orthogonaux.** Si A u = λ u et A v = μ v avec λ ≠ μ, alors λ (u · v) = (A u) · v = u · (A v) = μ (u · v), où l'égalité du milieu utilise Aᵀ = A. Donc (λ − μ)(u · v) = 0, et u · v = 0.
- **Les valeurs propres sont réelles.** Si A x = λ x pour un vecteur complexe x ≠ 0, alors λ ‖x‖² = x̄ᵀ A x, et x̄ᵀ A x est égal à son propre conjugué parce que A est réelle et symétrique. Donc λ est réel.

L'étape restante, à savoir qu'il y a assez de vecteurs propres même quand des valeurs propres se répètent, est une récurrence sur n (MAT-001) ; le livre d'Axler, dans les Bases de recherche, la donne.

### Exercice pratique

Avec les vecteurs propres de l'exercice du §1, posez Q = (1/√5) [[2, 1], [1, −2]] et Λ = diag(6, 1), et vérifiez que Q Λ Qᵀ = [[5, 2], [2, 2]].

> *Solution :* Les colonnes (2, 1)/√5 et (1, −2)/√5 sont de longueur 1 et orthogonales, donc Q est orthogonale, et ici Qᵀ = Q. Puis [[2, 1], [1, −2]] · diag(6, 1) = [[12, 1], [6, −2]], et [[12, 1], [6, −2]] · [[2, 1], [1, −2]] = [[25, 10], [10, 10]]. Les deux facteurs 1/√5 donnent 1/5, et (1/5) · [[25, 10], [10, 10]] = [[5, 2], [2, 2]].

---

## 3. Le quotient de Rayleigh

Pour une matrice symétrique A et un vecteur x ≠ 0, le **quotient de Rayleigh** est

R(x) = (xᵀ A x) / (xᵀ x).

Si x est un vecteur propre de valeur propre λ, alors R(x) = λ. En général, écrivons x = c₁q₁ + … + cₙqₙ dans une base orthonormée de vecteurs propres, de valeurs propres λ₁ ≥ … ≥ λₙ. Alors

R(x) = (λ₁c₁² + … + λₙcₙ²) / (c₁² + … + cₙ²),

une moyenne pondérée des valeurs propres. Deux conséquences en découlent :
- **Encadrement.** λₙ ≤ R(x) ≤ λ₁ pour tout x ≠ 0, avec égalité aux vecteurs propres : la plus grande valeur propre est le maximum de R, et la plus petite en est le minimum. Pour une matrice symétrique, la norme 2 subordonnée de MAT-004 est le plus grand |λᵢ|.
- **Précision.** Si x est proche d'un vecteur propre, R(x) est bien plus proche de sa valeur propre : une erreur d'ordre ε sur la direction de x donne une erreur d'ordre ε² sur R(x).

### Exercice pratique

Pour A = diag(3, 1) et x = (1, 1/10), calculez R(x) et sa distance à la valeur propre 3.

> *Solution :* xᵀ A x = 3 · 1 + 1 · 1/100 = 301/100 et xᵀ x = 101/100, donc R(x) = 301/101. Sa distance à 3 est 3 − 301/101 = 2/101, environ 0,02, alors que la direction de x s'écarte du vecteur propre (1, 0) d'un angle d'environ 1/10. L'erreur sur la valeur propre vaut environ deux fois le carré de l'erreur sur la direction, comme le dit la seconde conséquence.

---

## 4. Les rotations de Jacobi

En 1846, Jacobi a proposé de diagonaliser une matrice symétrique par une suite de rotations planes. Chaque étape choisit un couple d'indices p < q et remplace A par JᵀAJ, où J fait tourner le plan des coordonnées p et q d'un angle choisi pour annuler le nouveau coefficient a_pq. Comme J est orthogonale, JᵀAJ a les mêmes valeurs propres que A.

Pour le bloc 2 × 2 [[a_pp, a_pq], [a_pq, a_qq]] avec a_pq ≠ 0, posons θ = (a_qq − a_pp) / (2a_pq). La tangente t de l'angle de rotation est une racine de t² + 2θt − 1 = 0, et la racine de plus petite valeur absolue, t = 1 / (θ + √(1 + θ²)) quand θ ≥ 0 et t = 1 / (θ − √(1 + θ²)) quand θ < 0, garde la rotation petite. Avec c = 1/√(1 + t²) et s = t c, la rotation donne les nouveaux coefficients diagonaux

a_pp − t a_pq et a_qq + t a_pq,

et un zéro en position (p, q).

Pourquoi la méthode converge : une similitude orthogonale conserve la somme des carrés de tous les coefficients. La rotation change les deux coefficients hors diagonale a_pq en zéros et reporte leur poids sur la diagonale, donc la somme des carrés hors de la diagonale baisse d'exactement 2a_pq². Une rotation ultérieure peut rendre non nul un coefficient déjà annulé ; la **méthode de Jacobi cyclique** balaie donc tous les couples à plusieurs reprises. La somme hors diagonale décroît quand même, et la méthode converge ; quand les valeurs propres sont distinctes, la convergence devient finalement quadratique (Golub et Van Loan, ch. 8). Le produit V = J₁J₂J₃… des rotations contient les vecteurs propres dans ses colonnes.

### Exercice pratique

Appliquez une rotation de Jacobi à A = [[5, 2], [2, 2]].

> *Solution :* θ = (2 − 5)/(2 · 2) = −3/4, donc √(1 + θ²) = √(25/16) = 5/4 et t = −1/(3/4 + 5/4) = −1/2. Les nouveaux coefficients diagonaux sont 5 − (−1/2) · 2 = 6 et 2 + (−1/2) · 2 = 1, et le coefficient hors diagonale vaut 0. Une seule rotation diagonalise toute matrice symétrique 2 × 2 : ici elle trouve les valeurs propres 6 et 1 du §1, et la somme des carrés hors diagonale passe de 2 · 2² = 8 à 0.

---

## 5. Valeurs propres multiples

Pour une matrice symétrique, quand une valeur propre se répète, son **sous-espace propre**, l'ensemble des v tels que A v = λ v, a une dimension égale à la multiplicité, donc supérieure à 1. Sans symétrie, cela peut échouer : le cisaillement du §1 a la valeur propre double 1 mais un sous-espace propre de dimension 1. Toute base orthonormée du sous-espace propre est alors un ensemble de vecteurs propres tout aussi correct.

Prenons B = I + J, où J est la matrice 3 × 3 remplie de uns. Comme J (1, 1, 1) = 3 · (1, 1, 1), et J v = 0 dès que les composantes de v ont une somme nulle, B a la valeur propre 4 pour (1, 1, 1) et la valeur propre double 1 sur tout le plan des vecteurs dont les composantes ont une somme nulle. Deux vecteurs orthonormés quelconques de ce plan sont une réponse correcte.

Ce qui est unique, c'est le sous-espace propre, et avec lui le **projecteur orthogonal** sur ce sous-espace, P = uuᵀ + wwᵀ, qui ne dépend pas de la base orthonormée u, w choisie. Un test de solveur de valeurs propres doit donc vérifier des **invariants**, A v = λ v, VᵀV = I et A = V Λ Vᵀ, ou comparer des projecteurs, et ne jamais comparer les vecteurs propres à une liste attendue fixe : même un vecteur propre simple n'est déterminé qu'au signe près.

Les valeurs propres sont bien conditionnées (MAT-003) : ajouter une matrice symétrique E à une matrice symétrique déplace chaque valeur propre d'au plus ‖E‖₂, c'est l'inégalité de Weyl. Les vecteurs propres ne le sont pas : quand deux valeurs propres sont proches, une petite modification de la matrice peut faire tourner leurs vecteurs propres de beaucoup dans le plan qu'ils engendrent.

### Exercice pratique

Vérifiez que u = (1, −1, 0)/√2 et w = (1, 1, −2)/√6 sont des vecteurs propres orthonormés de B = I + J pour la valeur propre 1, et que uuᵀ + wwᵀ = I − J/3.

> *Solution :* Les composantes de u, comme celles de w, ont une somme nulle, donc J u = J w = 0, d'où B u = u et B w = w. De plus u · w = (1 − 1 + 0)/√12 = 0, ‖u‖² = 2/2 = 1 et ‖w‖² = 6/6 = 1. Puis uuᵀ = (1/2) [[1, −1, 0], [−1, 1, 0], [0, 0, 0]] et wwᵀ = (1/6) [[1, 1, −2], [1, 1, −2], [−2, −2, 4]]. Leur somme a 1/2 + 1/6 = 2/3 ou 0 + 4/6 = 2/3 sur la diagonale, et −1/2 + 1/6 = −1/3 ou 0 − 2/6 = −1/3 ailleurs : c'est I − J/3, dont les coefficients diagonaux valent 1 − 1/3 = 2/3 et les autres −1/3. Une autre base orthonormée du plan donne la même matrice.

---

## 6. La méthode de la puissance et son angle mort

La **méthode de la puissance** est le plus simple des solveurs de valeurs propres : on part d'un vecteur unitaire v₀, on répète v ← A v / ‖A v‖, et on estime la valeur propre par le quotient de Rayleigh de v. Si v₀ = c₁q₁ + … + cₙqₙ et |λ₁| > |λ₂| ≥ …, alors

Aᵏ v₀ = c₁λ₁ᵏ q₁ + … + cₙλₙᵏ qₙ,

et le premier terme l'emporte, avec une erreur qui décroît comme |λ₂/λ₁|ᵏ, **à condition que c₁ ≠ 0**. Deux choses peuvent mal tourner :
- **Un départ aveugle.** Si v₀ est orthogonal à q₁, alors c₁ = 0, et en arithmétique exacte l'itération ne trouve jamais q₁. L'arrondi peut introduire une minuscule composante selon q₁, qui a ensuite besoin de nombreuses étapes pour grandir.
- **Un test d'arrêt qui ne peut pas trancher.** « S'arrêter quand l'estimation ne change plus » est satisfait par une itération bloquée sur le mauvais vecteur propre tout autant que par une itération qui a convergé vers le bon.

Pour trouver le couple propre suivant, la **déflation** remplace A par A − λ₁ v vᵀ, ce qui envoie la valeur propre trouvée sur 0 ; toute erreur sur le premier couple se transmet au suivant.

### Exercice pratique

Appliquez la méthode de la puissance à A = [[2, −1], [−1, 2]] à partir de v₀ = (1, 1)/√2. Quelle valeur propre annonce-t-elle, et quelle est la plus grande ?

> *Solution :* A (1, 1) = (1, 1), donc v₀ est un vecteur propre pour la valeur propre 1. Chaque étape renvoie v₀ lui-même, le quotient de Rayleigh vaut 1 à chaque étape, et un test sur sa variation s'arrête aussitôt en annonçant 1. Mais A (1, −1) = (3, −3) : la plus grande valeur propre est 3, pour (1, −1)/√2, qui est orthogonal à v₀. L'itération y était aveugle dès le départ.

---

## 7. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**Le solveur symétrique** (`crates/ix-math/src/eigen.rs`). [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46) est la méthode de Jacobi cyclique du §4, avec au plus 100 balayages et une tolérance de 10^-12. Il renvoie les valeurs propres par ordre décroissant et les vecteurs propres comme colonnes d'une matrice. Sa rotation, reproduite telle quelle des lignes 92 à 109, est la formule du §4 :

```rust
                let app = m[[p, p]];
                let aqq = m[[q, q]];
                // Compute Jacobi rotation angle that zeros the (p, q) entry
                // of the 2x2 submatrix [[app, apq], [apq, aqq]].
                let theta = (aqq - app) / (2.0 * apq);
                let t = if theta >= 0.0 {
                    1.0 / (theta + (1.0 + theta * theta).sqrt())
                } else {
                    1.0 / (theta - (1.0 + theta * theta).sqrt())
                };
                let c = 1.0 / (1.0 + t * t).sqrt();
                let s = t * c;

                // Update diagonal entries and zero the off-diagonal.
                m[[p, p]] = app - t * apq;
                m[[q, q]] = aqq + t * apq;
                m[[p, q]] = 0.0;
                m[[q, p]] = 0.0;
```

Son contrat a trois limites qu'il faut connaître :
- **Il ne vérifie pas la symétrie.** Il rejette une entrée vide ou [non carrée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L64), mais lit les coefficients au-dessus de la diagonale comme si la matrice était symétrique. L'exercice ci-dessous montre ce qu'il renvoie alors.
- **Il ne signale pas la convergence.** La [boucle des balayages](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L74) s'arrête après au plus 100 balayages, et la fonction renvoie alors [`Ok`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L151), que la tolérance ait été atteinte ou non.
- **Son test d'arrêt n'est pas celui qu'annonce son commentaire.** Le commentaire parle de la norme de Frobenius de la partie hors diagonale, mais la [boucle](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L78) ne somme que les carrés au-dessus de la diagonale. Pour une matrice symétrique, c'est la moitié de la somme des carrés hors diagonale, donc le seuil réel sur cette norme est √2 · 10^-12 : sans conséquence ici, et un rappel qu'il faut lire le code plutôt que le commentaire.

Les tests vérifient le bon type de propriété. [`test_eigenvectors_are_orthonormal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L189) et [`test_reconstruction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L210) vérifient VᵀV = I et A = V Λ Vᵀ, les invariants du §5, sur une matrice 3 × 3. [`test_repeated_eigenvalues`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L231), en revanche, utilise l'identité 4 × 4 : sa partie hors diagonale est déjà nulle, donc la boucle s'arrête avant la première rotation et renvoie l'identité dont elle est partie. Le test passe sans exercer une seule rotation sur une valeur propre multiple ; une matrice comme le I + J du §5 forcerait des rotations.

**Deux appelants, deux façons de respecter la précondition.** Le gestionnaire de l'outil MCP `ix_eigen`, [`eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L469), rejette les [coefficients non finis](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L483) et toute asymétrie supérieure à une [tolérance relative](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L491) de 10^-9, et [`eigen_rejects_non_symmetric`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L1173) teste ce rejet sur [[1, 2], [3, 4]]. L'optimiseur CMA-ES, lui, [remplace sa matrice de covariance C par (C + Cᵀ)/2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-acoustic-tune/src/cmaes.rs#L181) avant d'appeler le solveur ; la question 3 de l'auto-évaluation montre pourquoi c'est la bonne réparation.

**L'ACP simple n'utilise pas ce solveur.** Le commentaire de module d'`eigen.rs` demande au reste de l'espace de travail de [l'appeler](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L8) plutôt que de le dupliquer, mais `crates/ix-unsupervised/src/pca.rs` extrait encore les composantes principales par la méthode de la puissance et par [déflation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). Sa méthode de la puissance, reproduite telle quelle des lignes 103 à 137 :

```rust
fn power_iteration(matrix: &Array2<f64>, max_iter: usize, tol: f64) -> (f64, Array1<f64>) {
    let n = matrix.nrows();

    // Initialize with a non-zero vector
    let mut v = Array1::from_elem(n, 1.0 / (n as f64).sqrt());

    let mut eigenvalue = 0.0;

    for _ in 0..max_iter {
        // Multiply: v_new = M * v
        let v_new = matrix.dot(&v);

        // Compute eigenvalue (Rayleigh quotient)
        let new_eigenvalue = v.dot(&v_new);

        // Normalize
        let norm = v_new.dot(&v_new).sqrt();
        if norm < 1e-15 {
            break;
        }
        let v_normalized = &v_new / norm;

        // Check convergence
        if (new_eigenvalue - eigenvalue).abs() < tol {
            eigenvalue = new_eigenvalue;
            v = v_normalized;
            break;
        }

        eigenvalue = new_eigenvalue;
        v = v_normalized;
    }

    (eigenvalue, v)
}
```

Le vecteur de départ est toujours (1, …, 1)/√n, et la boucle s'arrête quand l'estimation de Rayleigh varie de moins de `tol`, que [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176) fixe à 10^-10 : ce sont les deux angles morts du §6. Considérons les six points (1, −1), (−1, 1), (1, 0), (−1, 0), (0, 1) et (0, −1). Leur moyenne est 0 et leur matrice de covariance est [[4, −2], [−2, 4]]/5, de valeur propre 6/5 pour (1, −1)/√2 et 2/5 pour (1, 1)/√2. Le vecteur de départ (1, 1)/√2 est le vecteur propre de la plus petite, comme dans l'exercice du §6. Après déflation, la matrice est proche de [[3/5, −3/5], [−3/5, 3/5]], qui envoie le vecteur de départ presque sur zéro, donc le second appel devrait s'arrêter à son premier test de norme, en gardant le vecteur de départ et l'estimation 0. Notre lecture du code prédit donc que `PCA` avec deux composantes renvoie (1, 1)/√2 comme première composante, de variance 2/5, et de nouveau le même vecteur comme seconde, de variance 0. Un tel couple échouerait à [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288), qui vérifie l'orthogonalité sur un autre jeu de données. Les valeurs propres 6/5 et 2/5 sont bien séparées : l'échec vient du vecteur de départ fixe, pas de valeurs propres proches. C'est une prédiction, pas une exécution (§8), et une limite du code épinglé que les responsables d'IX ont à corriger, pas un comportement à copier.

### Exercice pratique

Déroulez `symmetric_eigen` à la main sur la matrice non symétrique A = [[1, 2], [3, 4]]. Que renvoie-t-il, et comment une vérification de A v = λ v détecterait-elle le problème ?

> *Solution :* Le premier balayage n'a qu'un couple, (0, 1). La boucle lit a_pq = 2, le coefficient au-dessus de la diagonale, avec a_pp = 1 et a_qq = 4, donc θ = 3/(2 · 2) = 3/4, √(1 + θ²) = 5/4 et t = 1/(3/4 + 5/4) = 1/2. La nouvelle diagonale vaut 1 − (1/2) · 2 = 0 et 4 + (1/2) · 2 = 5, les coefficients hors diagonale sont mis à 0, et le balayage suivant s'arrête. La fonction renvoie les valeurs propres (5, 0), sans erreur : ce sont les valeurs propres de [[1, 2], [2, 4]], la matrice dont le coefficient du bas reproduit celui du haut. Les vraies valeurs propres de A sont (5 ± √33)/2, environ 5,37 et −0,37. Pour λ = 5, le vecteur renvoyé est v = (1, 2)/√5, et A v = (5, 11)/√5 ≠ 5 v = (5, 10)/√5 : le résidu A v − λ v = (0, 1)/√5 est loin de 0. Les valeurs dont dépendent les valeurs propres, θ, √(1 + θ²), t et la nouvelle diagonale, sont toutes exactes en binary64, donc cette lecture prédit exactement (5, 0) ; le §8 le vérifie.

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **Les invariants.** Appeler `symmetric_eigen` sur [[5, 2], [2, 2]], sur la matrice 3 × 3 des tests d'IX, et sur I + J de tailles 3 et 4. Vérifier A v = λ v, VᵀV = I et A = V Λ Vᵀ coefficient par coefficient à 10^-9 près, la tolérance des tests d'IX. Prédiction : tout est vérifié, avec les valeurs propres 6 et 1, puis 4, 1, 1, puis 5, 1, 1, 1.
2. **Le sous-espace propre, pas les vecteurs.** Pour I + J de taille 3, construire uuᵀ + wwᵀ à partir des deux vecteurs propres renvoyés pour la valeur propre 1, et le comparer à I − J/3. Prédiction : égalité à 10^-9 près, quels que soient les vecteurs choisis par le solveur.
3. **Une entrée non symétrique.** Appeler `symmetric_eigen` sur [[1, 2], [3, 4]]. Prédiction : exactement (5, 0), sans erreur. Appeler `ix_eigen` sur la même matrice. Prédiction : une erreur dont le message contient « symmetric ».
4. **L'angle mort de l'ACP.** Ajuster `PCA` avec deux composantes sur les six points du §7. Prédiction : les deux composantes valent (1, 1)/√2 au signe et à l'arrondi près, les variances sont proches de 2/5 et de 0, et `explained_variance_ratio` renvoie 1 et 0. Pour comparaison, `symmetric_eigen` sur la même matrice de covariance renvoie 6/5 et 2/5.

### Exercice pratique

Si l'étape 4 se passe comme prévu, la première composante « explique » toute la variance. Pourquoi n'est-ce pas une preuve qu'elle est le bon axe, et quelle vérification simple révèle le problème ?

> *Solution :* Le rapport divise chaque variance renvoyée par la somme des variances renvoyées, et non par la variance totale des données, donc une méthode qui manque l'axe principal peut quand même annoncer la totalité. La variance totale est la trace de la matrice de covariance, qui est aussi la somme de ses valeurs propres (§1) : 4/5 + 4/5 = 8/5. Les variances renvoyées totalisent 2/5, donc 6/5 de la variance, soit les trois quarts, ne sont pas expliqués.

---

## 9. Pièges courants

- **Donner une matrice non symétrique à un solveur symétrique.** Il répond à une autre question, sans erreur : vérifiez la symétrie, ou réparez-la, d'abord.
- **Comparer les vecteurs propres à une liste attendue fixe.** Leur signe est libre, et avec une valeur propre multiple toute la base l'est aussi : testez des invariants ou des projecteurs.
- **Se fier à « l'estimation ne change plus ».** Une itération bloquée sur le mauvais vecteur propre ne change plus non plus.
- **Lancer la méthode de la puissance depuis un vecteur « neutre » fixe.** Quel que soit ce vecteur, certaines matrices ont leur vecteur propre dominant orthogonal à lui.
- **Écrire un test qui n'exécute jamais l'algorithme.** Sur l'identité, un solveur de Jacobi n'effectue aucune rotation.
- **Lire le commentaire au lieu du code.** Les deux peuvent diverger, comme pour le test d'arrêt de `symmetric_eigen`.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Vecteur propre, valeur propre** | Un v non nul tel que A v = λ v : une direction que A ne fait qu'étirer, du facteur λ |
| **Polynôme caractéristique** | det(A − λI), dont les racines sont les valeurs propres |
| **Matrice symétrique** | Une matrice carrée telle que Aᵀ = A |
| **Matrice orthogonale** | Une matrice carrée Q telle que QᵀQ = I : ses colonnes sont orthonormées |
| **Théorème spectral** | Une matrice symétrique réelle s'écrit A = Q Λ Qᵀ, avec Q orthogonale et Λ réelle et diagonale |
| **Quotient de Rayleigh** | R(x) = xᵀAx / xᵀx, une moyenne pondérée des valeurs propres d'une matrice symétrique A |
| **Rotation de Jacobi** | Une rotation plane J choisie pour que JᵀAJ ait un zéro en une position hors diagonale choisie |
| **Sous-espace propre** | Tous les v tels que A v = λ v pour un λ donné ; sa dimension peut dépasser 1 |
| **Projecteur orthogonal** | uuᵀ + wwᵀ + … pour une base orthonormée u, w, … d'un sous-espace ; il ne dépend pas de la base |
| **Méthode de la puissance** | La répétition de v ← A v / ‖A v‖, qui trouve le vecteur propre dominant si le départ a une composante selon lui |
| **Déflation** | Le remplacement de A par A − λ v vᵀ pour retirer un couple propre déjà trouvé |

---

## Auto-évaluation

**1. Pourquoi les vecteurs propres d'une matrice symétrique pour les valeurs propres 3 et 1 sont-ils forcément orthogonaux ?**
> Si A u = 3u et A v = v, alors 3 (u · v) = (A u) · v = u · (A v) = u · v, en utilisant Aᵀ = A. Donc 2 (u · v) = 0, et u · v = 0.

**2. Pour une matrice symétrique A de valeurs propres λ₁ ≥ … ≥ λₙ, pourquoi le maximum du quotient de Rayleigh est-il λ₁, et où est-il atteint ?**
> R(x) est une moyenne pondérée des valeurs propres, de poids cᵢ² ≥ 0 (§3), donc il vaut au plus λ₁. Il vaut λ₁ en x = q₁, un vecteur propre pour λ₁.

**3. CMA-ES remplace une matrice de covariance C par S = (C + Cᵀ)/2 avant d'appeler `symmetric_eigen`. Pourquoi S est-elle la matrice symétrique la plus proche de C ?**
> Écrivons C = S + K avec K = (C − Cᵀ)/2, de sorte que Kᵀ = −K. Pour toute matrice symétrique X, la matrice S − X est symétrique, et une matrice symétrique est orthogonale à K pour le produit scalaire Σ xᵢⱼyᵢⱼ qui définit la norme de Frobenius : les termes en (i, j) et (j, i) se compensent, et K a des zéros sur sa diagonale. Donc ‖C − X‖² = ‖S − X‖² + ‖K‖², qui est minimal exactement pour X = S. Pour une matrice de covariance que l'arrondi a éloignée de la symétrie, K est minuscule, et S est la réparation naturelle.

**4. Le test `test_repeated_eigenvalues` d'IX passe. Que montre-t-il sur les valeurs propres multiples ?**
> Bien peu de chose : sur l'identité, la partie hors diagonale est nulle, donc le solveur s'arrête avant toute rotation et renvoie l'identité dont il est parti. Un test avec I + J forcerait des rotations, et devrait vérifier des invariants ou le projecteur, puisque les vecteurs propres pour la valeur propre 1 ne sont pas uniques.

**Critères de réussite :** Trouver à la main les couples propres d'une matrice 2 × 2, utiliser le théorème spectral et ses contre-exemples, encadrer et estimer des valeurs propres avec le quotient de Rayleigh, effectuer une rotation de Jacobi, tester le résultat d'un solveur de valeurs propres par des invariants quand des valeurs propres se répètent, et repérer les préconditions et les angles morts des solveurs de valeurs propres d'IX.

---

## Bases de recherche

- G. H. Golub et C. F. Van Loan, *Matrix Computations*, 4e éd., Johns Hopkins University Press, 2013, ch. 8 : le problème aux valeurs propres symétrique, la méthode de Jacobi, la méthode de la puissance et l'inégalité de Weyl
- B. N. Parlett, *The Symmetric Eigenvalue Problem*, SIAM Classics in Applied Mathematics, 1998 : le quotient de Rayleigh et la sensibilité des vecteurs propres
- L. N. Trefethen et D. Bau, *Numerical Linear Algebra*, SIAM, 1997, leçons 24 à 30 : les algorithmes de valeurs propres, la méthode de la puissance et la méthode de Jacobi
- C. G. J. Jacobi, « Über ein leichtes Verfahren, die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen », *Journal für die reine und angewandte Mathematik* 30, 1846 : la méthode des rotations
- S. Axler, *Linear Algebra Done Right*, 4e éd., Springer, 2024 : le théorème spectral et sa démonstration
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §7 renvoie à sa ligne
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
