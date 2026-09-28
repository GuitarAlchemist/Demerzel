---
module_id: mat-004-vectors-matrices-norms
department: mathematics
course: Vecteurs, matrices, normes et applications linéaires
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Vecteurs, matrices, normes et applications linéaires — Ce qu'une matrice fait à l'espace

> **Département de mathématiques** | Stade : Nigredo (Débutant) | Durée estimée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Décrire un espace vectoriel et écrire un vecteur en coordonnées dans une base
- Reconnaître une application linéaire et construire sa matrice à partir des images des vecteurs de base
- Expliquer pourquoi le produit matriciel est la composition des applications linéaires, et pourquoi il est associatif mais pas commutatif
- Lire le déterminant comme un volume orienté et estimer le coût de son calcul par développement en cofacteurs
- Énoncer les axiomes d'une norme, utiliser les normes p, et montrer pourquoi la « norme » p = 1/2 n'en est pas une
- Dire ce que les fonctions d'algèbre linéaire et de distance d'IX garantissent, et ce qu'elles ne garantissent pas

---

## 1. Vecteurs et espaces vectoriels

Un **vecteur** de Rⁿ est une liste de n nombres réels, x = (x₁, …, xₙ). On additionne les vecteurs et on les multiplie par des nombres (des **scalaires**) composante par composante : (1, 2) + (3, 4) = (4, 6) et 3 · (1, 2) = (3, 6).

Un **espace vectoriel** est tout ensemble muni d'une telle addition et d'une telle multiplication par un scalaire, qui obéissent aux règles habituelles : l'addition est associative et commutative, il existe un vecteur nul et chaque vecteur a un opposé, et la multiplication par un scalaire est distributive par rapport aux deux additions. Rⁿ en est l'exemple principal, mais pas le seul : les polynômes a₀ + a₁t + a₂t² de degré au plus 2 forment aussi un espace vectoriel, et se comportent exactement comme les triplets (a₀, a₁, a₂).

Une **combinaison linéaire** des vecteurs v₁, …, vₖ est une somme c₁v₁ + … + cₖvₖ. Une **base** est une liste de vecteurs telle que tout vecteur de l'espace en est une combinaison linéaire d'une seule façon ; les nombres cᵢ sont alors les **coordonnées** du vecteur dans cette base. La **base canonique** de R² est e₁ = (1, 0), e₂ = (0, 1), et les coordonnées de (3, 4) y sont simplement 3 et 4. Dans une autre base, le même vecteur a d'autres coordonnées.

### Exercice pratique

Trouvez les coordonnées de (3, 4) dans la base u = (1, 1), w = (1, −1).

> *Solution :* On cherche a et b tels que a · (1, 1) + b · (1, −1) = (3, 4), c'est-à-dire a + b = 3 et a − b = 4. En additionnant les équations, 2a = 7, donc a = 7/2 ; en les soustrayant, 2b = −1, donc b = −1/2. Vérification : 7/2 · (1, 1) − 1/2 · (1, −1) = (7/2 − 1/2, 7/2 + 1/2) = (3, 4).

---

## 2. Applications linéaires et leurs matrices

Une application L d'un espace vectoriel dans un autre est **linéaire** si elle respecte les deux opérations :

L(u + v) = L(u) + L(v) et L(c · v) = c · L(v), pour tous vecteurs u, v et tout scalaire c.

Les rotations autour de l'origine, les réflexions par rapport à une droite passant par l'origine et les homothéties sont linéaires. Une translation x ↦ x + b avec b ≠ 0 ne l'est pas : toute application linéaire envoie 0 sur 0, car L(0) = L(0 · 0) = 0 · L(0) = 0.

Une application linéaire est déterminée par ce qu'elle fait d'une base. Si x = x₁e₁ + … + xₙeₙ, alors L(x) = x₁L(e₁) + … + xₙL(eₙ). On écrit donc les images L(e₁), …, L(eₙ) comme les **colonnes** d'une matrice A, et calculer L(x) devient le produit matrice–vecteur A x : x₁ fois la première colonne, plus x₂ fois la deuxième, et ainsi de suite. Par exemple, la rotation de 90° envoie e₁ = (1, 0) sur (0, 1) et e₂ = (0, 1) sur (−1, 0), donc sa matrice est

R = [[0, −1], [1, 0]],

écrite ligne par ligne.

### Exercice pratique

Trouvez la matrice S de la réflexion par rapport à la droite y = x, et vérifiez qu'elle envoie (1, 2) sur (2, 1).

> *Solution :* La réflexion échange les deux coordonnées, donc elle envoie e₁ = (1, 0) sur (0, 1) et e₂ = (0, 1) sur (1, 0). Ces images sont les colonnes : S = [[0, 1], [1, 0]]. Alors S (1, 2) = 1 · (0, 1) + 2 · (1, 0) = (2, 1).

---

## 3. La composition est le produit matriciel

Si B est la matrice d'une application linéaire M et A celle de L, appliquer M puis L est encore linéaire, et sa matrice est le **produit** AB : par définition, (AB) x = A (B x). En calculant les colonnes, on obtient la règle habituelle

(AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ,

qui exige que le nombre de colonnes de A soit égal au nombre de lignes de B. Notez l'ordre : dans (AB) x, c'est l'application B qui agit **en premier**.

Deux propriétés découlent de cette définition :
- **Le produit est associatif** : (AB)C = A(BC). Les deux membres sont la composition « C, puis B, puis A », et la composition des fonctions est toujours associative. Aucun calcul sur les coefficients n'est nécessaire.
- **Le produit n'est pas commutatif** : en général AB ≠ BA, car faire deux choses dans l'ordre inverse revient d'ordinaire à faire autre chose.

### Exercice pratique

Avec R = [[0, −1], [1, 0]] (rotation de 90°) et F = [[1, 0], [0, −1]] (réflexion par rapport à l'axe des x), calculez RF et FR et décrivez chacune comme une transformation géométrique.

> *Solution :* RF = [[0 · 1 + (−1) · 0, 0 · 0 + (−1) · (−1)], [1 · 1 + 0 · 0, 1 · 0 + 0 · (−1)]] = [[0, 1], [1, 0]], la réflexion par rapport à la droite y = x. FR = [[1 · 0 + 0 · 1, 1 · (−1) + 0 · 0], [0 · 0 + (−1) · 1, 0 · (−1) + (−1) · 0]] = [[0, −1], [−1, 0]], la réflexion par rapport à la droite y = −x. Comme RF ≠ FR, l'ordre compte : « réfléchir, puis tourner » n'est pas « tourner, puis réfléchir ».

---

## 4. Le déterminant comme volume

Pour une matrice 2 × 2, det [[a, b], [c, d]] = ad − bc. Sa valeur absolue est l'**aire** du parallélogramme engendré par les deux colonnes (a, c) et (b, d), et son signe dit si l'application conserve l'orientation du plan (+) ou l'inverse (−). En dimension n, |det A| est le facteur par lequel A multiplie les volumes. Trois faits découlent de cette image :
- det(AB) = det A · det B : appliquer B puis A multiplie les volumes par les deux facteurs.
- det A = 0 exactement quand A écrase l'espace sur une dimension inférieure, c'est-à-dire quand ses colonnes sont linéairement dépendantes et que A n'a pas d'inverse.
- Une rotation a pour déterminant 1 et une réflexion −1 : toutes deux conservent les aires, et seule la réflexion inverse l'orientation.

Pour des matrices plus grandes, le **développement en cofacteurs** selon la première ligne ramène un déterminant n × n à n déterminants de taille n − 1 :

det A = Σⱼ (−1)ʲ⁺¹ a₁ⱼ det A₁ⱼ,

où A₁ⱼ est A privée de sa première ligne et de sa colonne j. C'est une définition correcte mais un algorithme coûteux. L'**élimination de Gauss** demande un nombre d'opérations de l'ordre de n³. Elle ajoute à une ligne un multiple d'une autre, ce qui ne change pas le déterminant, et échange des lignes, ce qui change son signe. Ainsi det A est le produit des pivots, multiplié par −1 pour chaque échange de lignes : pour [[0, 1], [1, 0]], un échange donne les pivots 1 et 1, et det = −1.

### Exercice pratique

Une implémentation applique le développement en cofacteurs de façon récursive et s'arrête aux matrices 2 × 2, qu'elle calcule directement. Combien de déterminants 2 × 2 évalue-t-elle pour une matrice n × n ? Comparez ce nombre pour n = 10 avec 10³.

> *Solution :* Notons D(n) ce nombre. D(2) = 1, et une matrice n × n fait n appels de taille n − 1, donc D(n) = n · D(n − 1). Par récurrence (MAT-001), D(n) = n!/2 : c'est vrai pour n = 2, puisque 2!/2 = 1, et si D(n − 1) = (n − 1)!/2, alors D(n) = n · (n − 1)!/2 = n!/2. Pour n = 10, cela fait 10!/2 = 1 814 400 déterminants de taille 2, contre un nombre d'étapes d'élimination de l'ordre de 10³ = 1000. Pour n = 20, 20!/2 vaut environ 1,2 × 10^18.

---

## 5. Les normes : mesurer une longueur

Une **norme** associe une longueur ‖x‖ à chaque vecteur et obéit à trois axiomes :
- **Positivité :** ‖x‖ ≥ 0, et ‖x‖ = 0 seulement pour x = 0.
- **Homogénéité :** ‖c · x‖ = |c| · ‖x‖ pour tout scalaire c.
- **Inégalité triangulaire :** ‖x + y‖ ≤ ‖x‖ + ‖y‖.

Toute norme donne une **distance** d(x, y) = ‖x − y‖, et l'inégalité triangulaire de la norme devient celle des distances : d(x, z) ≤ d(x, y) + d(y, z). Faire le détour par y n'est jamais plus court qu'aller directement.

Les **normes p** sur Rⁿ sont ‖x‖ₚ = (|x₁|ᵖ + … + |xₙ|ᵖ)^(1/p), pour p ≥ 1, et ‖x‖∞ = maxᵢ |xᵢ|, qui est leur limite quand p grandit. Pour x = (3, 4) :
- ‖x‖₁ = 3 + 4 = 7, la longueur de Manhattan ;
- ‖x‖₂ = √(9 + 16) = 5, la longueur euclidienne ;
- ‖x‖∞ = 4, la plus grande composante.

Pour p ≥ 1, l'inégalité triangulaire est vraie : c'est l'**inégalité de Minkowski**. Pour 0 < p < 1, la même formule donne encore un nombre, mais pas une norme.

Une matrice a aussi des normes. Celle qui est **subordonnée** à une norme vectorielle est ‖A‖ = max ‖A x‖ / ‖x‖ sur les x ≠ 0, le plus grand facteur par lequel A étire un vecteur. C'est la norme qui sous-tend le conditionnement de MAT-003.

### Exercice pratique

Pour p = 1/2, définissons d(x, y) = (|x₁ − y₁|^(1/2) + |x₂ − y₂|^(1/2))². Montrez qu'elle viole l'inégalité triangulaire pour x = (0, 0), y = (1, 0) et z = (1, 1).

> *Solution :* d(x, y) = (1 + 0)² = 1 et d(y, z) = (0 + 1)² = 1, alors que d(x, z) = (1 + 1)² = 4. Donc d(x, z) = 4 > 2 = d(x, y) + d(y, z) : faire le détour par y est plus court qu'aller directement. Ce seul contre-exemple montre que la formule avec p = 1/2 n'est pas une norme.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**Algèbre linéaire** (`crates/ix-math/src/linalg.rs`) :
- [`matmul`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L8) et [`matvec`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L19) calculent AB et A x, et renvoient `DimensionMismatch` quand le nombre de colonnes de A ne correspond pas à l'autre opérande.
- [`trace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L151) additionne la diagonale d'une matrice carrée.
- [`determinant`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L35) est documentée comme « développement en cofacteurs, adapté aux petites matrices ». Sa récursion, reproduite telle quelle depuis les lignes 43 à 59 de `linalg.rs`, est l'algorithme de l'exercice du §4 :

```rust
fn det_recursive(a: &Array2<f64>) -> f64 {
    let n = a.nrows();
    if n == 1 {
        return a[[0, 0]];
    }
    if n == 2 {
        return a[[0, 0]] * a[[1, 1]] - a[[0, 1]] * a[[1, 0]];
    }

    let mut det = 0.0;
    for j in 0..n {
        let minor = minor_matrix(a, 0, j);
        let sign = if j % 2 == 0 { 1.0 } else { -1.0 };
        det += sign * a[[0, j]] * det_recursive(&minor);
    }
    det
}
```

- `linalg.rs` n'a aucune fonction qui renvoie une norme matricielle. Dans `ix-math`, la norme de Frobenius n'apparaît qu'à l'intérieur d'algorithmes, comme critère d'arrêt, et comme [fonction auxiliaire de test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L237) dans `svd.rs`.

**Distances** (`crates/ix-math/src/distance.rs`) : [`euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L18), [`manhattan`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L37) et [`chebyshev`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L77) sont les distances des normes 2, 1 et ∞. [`minkowski`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L46) calcule la distance p et refuse p < 1, comme le montrent les lignes 46 à 57, reproduites telles quelles :

```rust
pub fn minkowski(a: &Array1<f64>, b: &Array1<f64>, p: f64) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    if p < 1.0 {
        return Err(MathError::InvalidParameter("p must be >= 1".into()));
    }
    let sum: f64 = a
        .iter()
        .zip(b.iter())
        .map(|(x, y)| (x - y).abs().powf(p))
        .sum();
    Ok(sum.powf(1.0 / p))
}
```

Cette garde traduit le §5 : elle rejette tout p inférieur à 1, où la formule n'est pas une norme. Elle laisse pourtant passer deux valeurs non finies : `f64::NAN`, car toute comparaison avec NaN est fausse, après quoi les puissances renvoient NaN en général, qui n'est pas une distance ; et p = ∞, comme le montre l'exercice ci-dessous. Le contre-exemple avec p = 1/2 ne peut donc pas être calculé avec la fonction `minkowski` d'IX, qui renvoie une erreur ; c'est un calcul à la main, comme dans l'exercice du §5.

Les tests vérifient des exemples, pas des propriétés. [`test_minkowski_equals_euclidean`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L116) compare `minkowski` avec p = 2 et `euclidean` sur un seul couple de points, (0, 0) et (3, 4) ; les autres tests de distance utilisent eux aussi un ou deux couples fixés chacun. Aucun test de `distance.rs` n'énonce l'inégalité triangulaire ni un autre axiome de norme. Ailleurs dans IX, [`test_cpu_triangle_inequality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-gpu/src/distance.rs#L193) l'énonce pour la matrice de distances euclidiennes propre au crate GPU, mais ne vérifie qu'un seul triplet de points. Comme l'explique MAT-001, de tels exemples peuvent réfuter une propriété mais pas la démontrer.

**Toute « distance » n'est pas une métrique.** [`cosine_distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L72) renvoie 1 − cos θ, où θ est l'angle entre les vecteurs. Elle ne vérifie pas l'inégalité triangulaire : pour x = (1, 0), y = (1, 1) et z = (0, 1), elle donne d(x, z) = 1, mais d(x, y) + d(y, z) = 2 − √2 ≈ 0,59.

### Exercice pratique

La garde de `minkowski` rejette p < 1, mais laisse passer p = ∞ (`f64::INFINITY`). En utilisant les règles usuelles des puissances en virgule flottante — x^0 = 1 pour tout x, et pour p = ∞, t^p vaut 0 quand 0 ≤ t < 1, 1 quand t = 1 et ∞ quand t > 1 —, prédisez ce que renvoie `minkowski` pour p = ∞, et comparez avec `chebyshev`.

> *Solution :* Avec p = ∞, chaque terme |x − y|^p vaut 0, 1 ou ∞, donc `sum` vaut 0, un entier positif ou ∞. La dernière étape l'élève à la puissance 1/p = 1/∞ = 0, et x^0 = 1 pour tout x, y compris 0 et ∞. Donc `minkowski` renvoie 1 pour tout couple de vecteurs, même pour a = b, où une distance doit valoir 0. La limite de la distance p quand p grandit est la distance ∞, mais remplacer p par ∞ dans la formule ne calcule pas cette limite : `chebyshev` est la bonne fonction, et elle renvoie 0 pour a = b et 4 pour (0, 0) et (3, 4). C'est une prédiction tirée des règles ci-dessus, pas une exécution : l'expérience du §7 la vérifie.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **L'inégalité triangulaire sur une grille.** Pour les 25 points de R² à coordonnées entières de −2 à 2, vérifier d(x, z) ≤ d(x, y) + d(y, z) sur les 15 625 triplets pour `manhattan`, `euclidean`, `chebyshev` et `minkowski` avec p = 3. Prédiction : aucune violation supérieure à 10^-12. Là où les valeurs exactes sont égales, l'arrondi peut encore faire différer les deux membres dans leurs derniers bits, d'où la nécessité d'une tolérance dans la comparaison (MAT-003).
2. **p inférieur à 1.** Appeler `minkowski` avec p = 1/2 sur les points de l'exercice du §5. Prédiction : `InvalidParameter("p must be >= 1")`.
3. **p = ∞.** Appeler `minkowski` avec p = `f64::INFINITY` sur (0, 0) et (0, 0), et sur (0, 0) et (3, 4). Prédiction : 1 dans les deux cas, contre 0 et 4 pour `chebyshev`.
4. **Grand p.** Appeler `minkowski` avec p = 1000 sur (0, 0) et (3, 4). Prédiction : ∞, car 3^1000 dépasse le plus grand nombre binary64, alors que le résultat exact est un peu supérieur à 4.
5. **Le coût du développement en cofacteurs.** Chronométrer `determinant` pour n = 2 à 11 sur des matrices fixées, et vérifier det(AB) = det A · det B sur des matrices 3 × 3 à petits coefficients entiers. Prédictions : à partir de n = 3, chaque pas multiplie le temps par environ n, comme le suggère le nombre n!/2 de l'exercice du §4 ; et la règle du produit est vérifiée exactement, car chaque valeur intermédiaire est un entier assez petit pour être stocké exactement.

### Exercice pratique

L'étape 1 vérifie chaque triplet de la grille. Démontre-t-elle l'inégalité triangulaire pour ces distances sur R² ?

> *Solution :* Non. La grille a 25 points, alors que R² est infini : la vérification n'est exhaustive que sur un sous-ensemble fini (MAT-001). Ce qui démontre l'inégalité, c'est l'inégalité de Minkowski, pour tout p ≥ 1. La vérification teste autre chose : que le code d'IX calcule ces distances sans erreur assez grande pour violer l'inégalité sur ces points.

---

## 8. Pièges courants

- **Multiplier dans le mauvais ordre.** Dans (AB) x, l'application B agit en premier, et AB ≠ BA en général.
- **Qualifier toute application de « linéaire ».** Une application linéaire envoie 0 sur 0 ; une translation, non.
- **Calculer de grands déterminants par développement en cofacteurs.** Le coût croît comme n! ; l'élimination coûte de l'ordre de n³.
- **Lire un petit déterminant comme « presque singulier ».** det(10^-1 · I₂₀) = 10^-20, et pourtant cette matrice ne fait que multiplier par 10^-1 et a un conditionnement de 1 (MAT-003).
- **Prendre toute formule de distance pour une métrique.** La formule p avec 0 < p < 1 et la distance cosinus violent toutes deux l'inégalité triangulaire.
- **Remplacer p par ∞ dans une formule.** Une limite n'est pas une valeur de la formule : utilisez la norme ∞ elle-même.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Espace vectoriel** | Un ensemble muni d'une addition et d'une multiplication par un scalaire obéissant aux règles habituelles, comme Rⁿ |
| **Base** | Une liste de vecteurs grâce à laquelle tout vecteur s'écrit comme combinaison linéaire d'une seule façon |
| **Application linéaire** | Une application telle que L(u + v) = L(u) + L(v) et L(c · v) = c · L(v) |
| **Matrice d'une application linéaire** | La matrice dont les colonnes sont les images des vecteurs de base |
| **Produit matriciel** | La matrice d'une composition : (AB) x = A (B x) |
| **Déterminant** | Le facteur orienté par lequel une matrice carrée multiplie les volumes ; nul exactement quand la matrice n'est pas inversible |
| **Norme** | Une fonction longueur positive, homogène et qui vérifie l'inégalité triangulaire |
| **Norme p** | ‖x‖ₚ = (Σ |xᵢ|ᵖ)^(1/p) pour p ≥ 1, et ‖x‖∞ = max |xᵢ| |
| **Inégalité triangulaire** | ‖x + y‖ ≤ ‖x‖ + ‖y‖, ou pour les distances d(x, z) ≤ d(x, y) + d(y, z) |
| **Norme matricielle subordonnée** | ‖A‖ = max ‖A x‖ / ‖x‖ sur les x ≠ 0 : le plus grand facteur d'étirement de A |

---

## Auto-évaluation

**1. Pourquoi l'application x ↦ x + (1, 0) n'est-elle pas linéaire ?**
> Une application linéaire envoie 0 sur 0, puisque L(0) = L(0 · 0) = 0 · L(0) = 0. Cette application envoie 0 sur (1, 0).

**2. Pourquoi le produit matriciel est-il associatif mais pas commutatif ?**
> C'est la composition des applications linéaires. La composition des fonctions est toujours associative, donc (AB)C = A(BC). L'ordre de deux applications compte en général : la rotation R et la réflexion F du §3 donnent RF ≠ FR.

**3. Démontrez que ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ pour tout x de Rⁿ.**
> Si la plus grande composante en valeur absolue est xₖ, alors ‖x‖∞² = xₖ² ≤ x₁² + … + xₙ² = ‖x‖₂². Et ‖x‖₁² = (|x₁| + … + |xₙ|)² est la somme des carrés xᵢ² et des produits 2|xᵢ||xⱼ|, qui sont ≥ 0, donc ‖x‖₁² ≥ ‖x‖₂². En prenant les racines carrées de ces nombres positifs, on obtient l'énoncé.

**4. La fonction `minkowski` d'IX refuse p = 1/2. Est-ce une limitation ou une garantie ?**
> Une garantie : en dessous de p = 1, la formule n'est pas une norme (§5), et la refuser écarte ces résultats. La garde ne couvre pas les valeurs non finies : elle laisse passer p = ∞, pour lequel la formule renvoie 1 quels que soient les points, et `f64::NAN`, pour lequel elle renvoie NaN en général (§6).

**Critères de réussite :** Écrire des vecteurs dans une base, construire la matrice d'une application linéaire, multiplier des matrices et expliquer pourquoi l'ordre compte, lire un déterminant et compter son coût, et utiliser les axiomes de norme pour distinguer une norme d'une formule qui n'en est pas une, y compris dans les fonctions de distance d'IX.

---

## Bases de recherche

- S. Axler, *Linear Algebra Done Right*, 4e éd., Springer, 2024 : espaces vectoriels, applications linéaires et leurs matrices, déterminants
- G. Strang, *Introduction to Linear Algebra*, 6e éd., Wellesley-Cambridge Press, 2023 : le produit matriciel comme composition, l'élimination, les déterminants et les normes
- G. H. Hardy, J. E. Littlewood et G. Pólya, *Inequalities*, Cambridge University Press, 1934 : l'inégalité de Minkowski
- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019 : les valeurs particulières de la fonction puissance utilisées au §6
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
