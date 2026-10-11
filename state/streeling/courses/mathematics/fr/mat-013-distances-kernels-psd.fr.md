---
module_id: mat-013-distances-kernels-psd
department: mathematics
course: Distances, noyaux et matrices semi-définies positives
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Distances, noyaux et matrices semi-définies positives — Quand une similarité est vraiment un produit scalaire

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Énoncer les axiomes d'une métrique, et décider si une distance donnée les vérifie
- Reconnaître les matrices semi-définies positives, les tester par leurs valeurs propres, et exhiber un témoin quand une matrice échoue
- Expliquer ce qui rend un noyau valide, et construire ou rejeter des noyaux à l'aide de matrices de Gram
- Décrire comment la largeur de bande du noyau gaussien fait passer sa matrice de Gram de l'identité à une matrice de rang un
- Utiliser la distance de Mahalanobis, et dire quelles matrices en font une métrique
- Retracer ce que garantissent les distances, les noyaux et le test par valeurs propres d'IX, et où un arrondi ou un écrêtage silencieux viole un axiome

---

## 1. Les métriques et ce qu'elles promettent

Une **métrique** sur un ensemble est une fonction d(x, y) dotée de quatre propriétés : d(x, y) ≥ 0 ; d(x, y) = 0 exactement quand x = y ; d(x, y) = d(y, x) ; et l'**inégalité triangulaire** d(x, z) ≤ d(x, y) + d(y, z). Une **pseudométrique** abandonne une moitié du deuxième axiome : des points distincts peuvent être à distance 0. Les algorithmes s'appuient sur ces axiomes : un index de plus proches voisins élague toute une région grâce à l'inégalité triangulaire, et une méthode de regroupement qui fusionne des points à distance 0 suppose qu'il s'agit du même point.

Les distances de Minkowski (Σ|xᵢ − yᵢ|^p)^(1/p) du MAT-004 sont des métriques pour p ≥ 1. Pour p = 1/2, l'inégalité triangulaire échoue : de (0, 0) à (1, 1), la formule donne (1 + 1)² = 4, alors que le détour par (1, 0) coûte 1 + 1 = 2. La distance euclidienne au carré échoue aussi, sur les points 0, 1 et 2 de la droite : 4 > 1 + 1. Elle sert à comparer des distances, puisque le carré préserve leur ordre, mais elle n'est pas elle-même une métrique.

### Exercice pratique

La distance cosinus vaut 1 − cos θ, où θ est l'angle entre deux vecteurs non nuls. Est-ce une métrique ? Et l'angle θ lui-même ?

> *Solution :* Non. Prenez des vecteurs unitaires à 0°, 45° et 90°. Les distances entre voisins valent chacune 1 − √2/2 ≈ 0,2929, leur somme 0,5858, alors que la distance de 0° à 90° vaut 1 : l'inégalité triangulaire échoue, donc ce n'est même pas une pseudométrique. L'angle θ = arccos(cos θ) est une métrique sur la sphère unité : c'est la longueur du plus court arc, et ici π/4 + π/4 = π/2, avec égalité. Sur des vecteurs non normalisés, l'angle n'est qu'une pseudométrique, puisque x et 2x forment un angle nul.

---

## 2. Matrices semi-définies positives

Une matrice symétrique A est **semi-définie positive** (SDP) si xᵀAx ≥ 0 pour tout vecteur x, et **définie positive** si xᵀAx > 0 pour tout x ≠ 0. Par le théorème spectral du MAT-005, A = QΛQᵀ avec Q orthogonale, donc xᵀAx = Σλᵢ(qᵢ · x)² : A est SDP exactement quand toutes ses valeurs propres sont ≥ 0, et définie positive quand toutes sont > 0. Toute **matrice de Gram** G = BBᵀ, dont le coefficient (i, j) est le produit scalaire des lignes i et j de B, est SDP, puisque xᵀGx = ‖Bᵀx‖² ≥ 0. Réciproquement, toute matrice SDP est une matrice de Gram : A = (QΛ^(1/2))(QΛ^(1/2))ᵀ.

Il en découle trois tests pratiques. Le test par valeurs propres calcule la plus petite valeur propre et la compare à une tolérance, puisque l'arrondi déplace les valeurs propres d'environ u‖A‖ (MAT-003). La **factorisation de Cholesky** A = LLᵀ, avec L triangulaire inférieure, réussit exactement pour les matrices définies positives et coûte environ n³/3 opérations, bien moins qu'une décomposition spectrale. Enfin, un seul vecteur x tel que xᵀAx < 0 est un **témoin** que A n'est pas SDP, facile à vérifier à la main. Le critère de Sylvester, selon lequel les mineurs principaux dominants sont positifs, caractérise uniquement les matrices définies positives ; pour SDP, tous les mineurs principaux doivent être ≥ 0, pas seulement les dominants.

### Exercice pratique

Une « similarité » donne 1 aux points distants d'au plus un pas sur la droite : T = [[1, 1, 0], [1, 1, 1], [0, 1, 1]] pour les points 0, 1 et 2, écrite ligne par ligne. T est-elle SDP ?

> *Solution :* Non. Pour x = (1, −1, 1), Tx = (0, 1, 0), donc xᵀTx = −1 < 0 : x est un témoin. Les valeurs propres sont 1 − √2 ≈ −0,414, 1 et 1 + √2 ≈ 2,414 ; leur somme est la trace 3, et leur produit le déterminant −1. Tous les coefficients diagonaux sont positifs et chaque ligne ressemble à une similarité, et pourtant T n'est la matrice de Gram d'aucune famille de vecteurs.

---

## 3. Noyaux

Un **noyau** k(x, y) est une similarité qui est un produit scalaire dans un certain espace de caractéristiques : k(x, y) = φ(x) · φ(y) pour une application φ. Une fonction k est un **noyau défini positif** quand toute matrice de Gram Kᵢⱼ = k(xᵢ, xⱼ), pour tout ensemble fini de points, est SDP ; par le théorème de Moore–Aronszajn, c'est exactement la condition d'existence d'une telle φ, éventuellement à valeurs dans un espace de dimension infinie. Le théorème de Mercer énonce la même condition pour les noyaux continus au moyen de leur opérateur intégral. Les sommes, les produits et les multiples positifs de noyaux sont des noyaux, et c'est ainsi que l'on construit la plupart d'entre eux.

Les trois noyaux classiques sont le noyau **linéaire** x · y ; le noyau **polynomial** (γ x · y + c)^d, qui est un noyau quand d est un entier positif, γ > 0 et c ≥ 0 ; et le noyau **gaussien** ou **RBF** exp(−γ‖x − y‖²), qui est un noyau pour tout γ > 0. Tout noyau définit une distance dans l'espace de caractéristiques, d_k(x, y)² = k(x, x) + k(y, y) − 2k(x, y), une pseudométrique en général et une métrique quand φ est injective. La similarité cosinus est le noyau linéaire des vecteurs normalisés x/‖x‖, et sa distance de noyau est √(2 − 2 cos θ), la corde qui les joint : la racine carrée du double de la distance cosinus du §1 est une métrique sur la sphère unité, alors que la distance cosinus elle-même n'en est pas une.

### Exercice pratique

k(x, y) = (xy − 1)² est-il un noyau sur la droite réelle ? Utilisez les points 0, 1 et 2.

> *Solution :* Non. Sa matrice de Gram sur 0, 1 et 2 est [[1, 1, 1], [1, 0, 1], [1, 1, 9]]. Le mineur principal sur les points 0 et 1, [[1, 1], [1, 0]], a pour déterminant −1 < 0, donc la matrice n'est pas SDP. Ici c = −1 < 0 : le développement donne (xy)² − 2xy + 1, et le terme −2xy retranche un noyau. Avec c = +1, (xy + 1)² = φ(x) · φ(y) pour φ(x) = (x², √2 x, 1).

---

## 4. La largeur de bande du noyau gaussien

Le paramètre γ du noyau RBF fixe l'échelle à laquelle des points comptent comme similaires, et s'écrit souvent γ = 1/(2σ²) avec une largeur de bande σ. Quand γ croît, chaque coefficient hors diagonale tend vers 0 et K tend vers l'identité : chaque point n'est similaire qu'à lui-même, et une méthode fondée sur K apprend par cœur ses données d'entraînement. Quand γ décroît, chaque coefficient tend vers 1 et K tend vers la matrice dont tous les coefficients valent 1, de valeurs propres n, 0, …, 0 : chaque point ressemble à tous les autres.

Entre les deux, K est SDP mais peut être mal conditionnée. Sur les points 0, 1 et 2 de la droite, la plus petite valeur propre de K vaut environ 0,489 pour γ = 1, 0,0124 pour γ = 0,1, 1,3 · 10^-4 pour γ = 0,01 et 1,3 · 10^-6 pour γ = 10^-3, où le conditionnement atteint environ 2,2 · 10^6 : par la règle du MAT-003, une résolution avec K peut perdre six chiffres. Avec plus de points ou un γ plus petit, une matrice exactement SDP peut avoir une valeur propre calculée légèrement sous 0 ; un test par valeurs propres doit donc accepter des valeurs jusqu'à une tolérance proportionnelle à n u ‖K‖, et ne pas traiter chaque nombre négatif comme un verdict. Une valeur de départ courante prend pour σ la distance médiane entre les points.

### Exercice pratique

Pour n points distincts, vers quoi tendent la matrice de Gram RBF et ses valeurs propres quand γ → ∞ et quand γ → 0 ?

> *Solution :* Quand γ → ∞, exp(−γ‖xᵢ − xⱼ‖²) → 0 pour i ≠ j, donc K → I, avec toutes ses valeurs propres égales à 1 : parfaitement conditionnée, et aucun couple de points similaires. Quand γ → 0, chaque coefficient tend vers 1, donc K → 11ᵀ, de valeurs propres n et 0 répétée n − 1 fois : les plus petites valeurs propres tendent vers 0 et le conditionnement croît sans borne.

---

## 5. La distance de Mahalanobis

Pour un vecteur aléatoire de matrice de covariance S, la **distance de Mahalanobis** est d_M(x, y) = √((x − y)ᵀ M (x − y)) avec M = S⁻¹. Elle mesure les écarts en unités de la dispersion dans chaque direction : avec S = diag(4, 1), les points (2, 0) et (0, 0) sont à distance 1, aussi éloignés que (0, 1) et (0, 0). Si S = LLᵀ est une factorisation de Cholesky, d_M(x, y) = ‖L⁻¹(x − y)‖ : la distance de Mahalanobis est la distance euclidienne après **blanchiment** des données.

C'est la matrice M qui décide si d_M est une métrique. Si M est symétrique définie positive, c'en est une. Si M est seulement SDP, les directions de son noyau sont invisibles, et d_M est une pseudométrique. Si M a une valeur propre négative, la quantité sous la racine peut être négative, et d_M n'est pas du tout une distance. Seule la partie symétrique (M + Mᵀ)/2 entre dans la forme quadratique, si bien qu'une M non symétrique cache ce qu'elle mesure réellement.

### Exercice pratique

Soit M = [[1, 2], [0, 1]]. Son déterminant vaut 1, donc elle est inversible. √((x − y)ᵀ M (x − y)) est-elle une métrique ?

> *Solution :* Non. Avec d = x − y, dᵀMd = d₁² + 2d₁d₂ + d₂² = (d₁ + d₂)². Elle n'est jamais négative, mais elle s'annule dès que d₂ = −d₁ : les points (1, −1) et (0, 0) sont distincts et à distance 0. La partie symétrique [[1, 1], [1, 1]] a pour valeurs propres 2 et 0, donc la « distance » est une pseudométrique qui ne voit que d₁ + d₂. L'inversibilité de M n'est pas la condition ; c'est le caractère défini positif de sa partie symétrique qui l'est.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne des fonctions ci-dessous en Python, dont les flottants sont en binary64 IEEE comme le `f64` de Rust : ce sont des prédictions, que le §7 propose de vérifier.

**Distances** (`crates/ix-math`). [`distance.rs`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L60) fournit les fonctions euclidienne, de Manhattan, de Minkowski, de Chebyshev et cosinus ; la distance de Minkowski [rejette p < 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L48), la condition du §1. L'outil MCP `ix_distance`, par le gestionnaire [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L148), propose les métriques euclidienne, de Manhattan et [cosinus](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L163). [`GeometricSpace`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L38) place onze distances derrière une seule fonction [`distance`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L87), parmi lesquelles la [distance de Mahalanobis](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L61), qui reçoit de l'appelant une covariance inverse ; le module est [exporté](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/lib.rs#L14), et aucun code hors de ses propres tests ne l'appelle. Les fonctions cosinus s'écrivent :

```rust
/// Cosine similarity (not distance). Returns value in [-1, 1].
pub fn cosine_similarity(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    check_same_len(a, b)?;
    let dot: f64 = a.dot(b);
    let norm_a = a.dot(a).sqrt();
    let norm_b = b.dot(b).sqrt();
    if norm_a < 1e-12 || norm_b < 1e-12 {
        return Ok(0.0);
    }
    Ok(dot / (norm_a * norm_b))
}

/// Cosine distance = 1 - cosine_similarity.
pub fn cosine_distance(a: &Array1<f64>, b: &Array1<f64>) -> Result<f64, MathError> {
    cosine_similarity(a, b).map(|s| 1.0 - s)
}
```

- **Une distance cosinus peut être négative.** Pour x = (1, 1, 1), le produit scalaire vaut 3 et chaque norme √3, mais le produit des deux normes arrondies vaut 2,9999999999999996, si bien que la similarité de x avec lui-même vaut 1 + 2^-52 et sa [distance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L73) à lui-même −2^-52 ≈ −2,2 · 10^-16. Rien n'écrête la valeur, donc l'intervalle documenté [−1, 1] et l'axiome d ≥ 0 sont tous deux violés ; pour x = (1, 1), la distance à soi-même vaut au contraire +2^-52. La distance sphérique de `GeometricSpace`, elle, [écrête son cosinus](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L113). L'extension DuckDB énonce l'[invariant](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/udf.rs#L224) « identical vectors -> 0.0 », et son test utilise [(1, 2, 3)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/lib.rs#L311), pour lequel l'arrondi se trouve être exact.
- **Un vecteur nul est à distance 1 de lui-même.** Quand une norme est inférieure à 10^-12, la similarité [renvoie 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L66), donc la distance cosinus de 0 à 0 vaut 1. La distance sphérique fait le [choix inverse](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L111) : le vecteur nul est à distance 0 de tout vecteur, y compris de (1, 0) et de (0, 1), qui sont à π/2 l'un de l'autre, si bien que l'inégalité triangulaire échoue en passant par lui.
- **Une forme de Mahalanobis négative est écrêtée à 0.** La branche Mahalanobis ci-dessous ne vérifie [que la forme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L136) de la matrice, ni sa symétrie ni son caractère défini, et [prend le maximum avec 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L145) avant la racine carrée. Avec la « covariance inverse » diag(1, −1), les points (1, 1) et (0, 0) sont à distance 0, et de même (0, 1) et (0, 0), dont la forme quadratique vaut −1 : aucune erreur n'est levée, et chaque couple de points distincts reçoit la distance 0. Avec [[1, 2], [0, 1]], la matrice du §5, le couple (1, −1) et (0, 0) reçoit aussi 0.
- **La tolérance de Hamming viole l'inégalité triangulaire.** La distance de Hamming compte les coordonnées qui [diffèrent de plus de 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/geometric_space.rs#L168). L'égalité à une tolérance près n'est pas transitive : pour les points à une coordonnée 0, 6 · 10^-13 et 1,2 · 10^-12, les distances valent 0, 0 et 1.
- **Chebyshev ignore NaN.** La distance de Chebyshev prend un [maximum courant avec `f64::max`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/distance.rs#L82), qui renvoie l'autre opérande quand l'un est NaN : (NaN, 0) et (0, 0) sont à distance de Chebyshev 0, alors que leur distance euclidienne est NaN.
- **Les noyaux ne sont pas validés, et les valeurs propres négatives sont écrêtées.** L'ACP à noyau propose les variantes de [`Kernel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L53) du §3, avec un [degré polynomial de type `f64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L57) appliqué par [`powf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L225), et un [RBF](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L232) qui accepte γ de l'un ou l'autre signe. Rien ne rejette c < 0, un degré fractionnaire ou γ < 0, qui peuvent donner des matrices de Gram non SDP, ou des coefficients NaN quand une base négative est élevée à une puissance fractionnaire, et l'ajustement [remplace chaque valeur propre négative par 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L141) sans le signaler. La documentation du module dit qu'on peut ajouter des noyaux personnalisés en [implémentant le trait `Kernel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/kernel_pca.rs#L20), mais `Kernel` est une énumération, pas un trait.
- **Le test par valeurs propres dépend de l'échelle.** IX n'a ni test SDP ni factorisation de Cholesky, donc le test par valeurs propres du §2 doit passer par [`symmetric_eigen`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L46), la méthode de Jacobi du MAT-005, dont la tolérance de [10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L47) est absolue. Son [test d'arrêt](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/eigen.rs#L82) est satisfait avant la première rotation pour 10^-13 T, la matrice du §2 réduite d'échelle, si bien que la fonction renvoie la diagonale, trois fois 10^-13, et qu'une matrice indéfinie passe pour SDP. À 8 · 10^-13 T, elle s'arrête après un balayage de trois rotations avec environ −2,9 · 10^-13 au lieu de la valeur exacte 8 · 10^-13 (1 − √2) ≈ −3,3 · 10^-13.

La branche Mahalanobis de `distance` :

```rust
        GeometricSpace::Mahalanobis { inv_cov } => {
            let n = a.len();
            if inv_cov.shape() != [n, n] {
                return Err(MathError::DimensionMismatch {
                    expected: n,
                    got: inv_cov.shape()[0],
                });
            }
            let diff = a - b;
            let sx = inv_cov.dot(&diff);
            let acc = diff.dot(&sx);
            Ok(acc.max(0.0).sqrt())
        }
```

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pourquoi la distance cosinus de (1, 1, 1) à lui-même est-elle négative, alors que celle de (1, 2, 3) à lui-même vaut exactement 0 ?

> *Solution :* Le code divise le produit scalaire par le produit de deux racines carrées arrondies séparément. Pour (1, 1, 1), √3 s'arrondit en un double dont le carré, 2,9999999999999996, est juste sous 3, donc 3 divisé par ce carré donne 1 + 2^-52, et 1 moins ce résultat donne −2^-52. Pour (1, 2, 3), le produit scalaire vaut 14, et le carré de √14 arrondi se trouve s'arrondir exactement à 14, donc la similarité vaut exactement 1. Que la distance à soi-même soit nulle, légèrement positive ou légèrement négative dépend de la façon dont tombe un arrondi ; c'est pourquoi une distance construite à partir d'une similarité doit être écrêtée à 0, ou calculée comme ‖x/‖x‖ − y/‖y‖‖²/2, qui n'est jamais négative.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Matrices de Gram.** Sur les points (0, 0), (1, 0), (0, 1), (1, 1) et (2, 1), construire les matrices de Gram du noyau linéaire, du noyau RBF avec γ = 0,5 et du noyau polynomial (x · y + 1)², et passer chacune à `symmetric_eigen`. Prédiction : la matrice linéaire est de rang 2, ses trois plus petites valeurs propres à moins de 10^-12 de 0 ; les plus petites valeurs propres des deux autres valent environ 0,133 et 0,298. Avec c = −1 dans le noyau polynomial, et avec γ = −0,5 dans le noyau RBF, les plus petites valeurs propres valent environ −1,08 et −12,6.
2. **La similarité à seuil et son échelle.** Passer la T du §2 à `symmetric_eigen`. Prédiction : sa plus petite valeur propre est 1 − √2 à 10^-12 près. Passer ensuite 10^-13 T et 8 · 10^-13 T. Prédiction : la première renvoie trois fois 10^-13 ; la seconde renvoie une plus petite valeur propre proche de −2,9 · 10^-13.
3. **Mahalanobis.** Appeler `distance` avec `Mahalanobis` et `inv_cov` égale à diag(1, −1), sur (1, 1) et (0, 0), puis sur (0, 1) et (0, 0) ; puis avec [[1, 2], [0, 1]] sur (1, −1) et (0, 0). Prédiction : les trois renvoient `Ok(0.0)`.
4. **Cosinus.** Appeler le gestionnaire `distance` avec `metric` réglé sur `cosine` pour a = b = (1, 1, 1), puis pour a = b = (1, 1), puis pour deux vecteurs nuls. Prédiction : −2^-52, +2^-52 et 1.
5. **Hamming et Chebyshev.** Calculer les distances de Hamming entre les points à une coordonnée 0, 6 · 10^-13 et 1,2 · 10^-12, et la distance de Chebyshev entre (NaN, 0) et (0, 0). Prédiction : 0, 0 et 1, puis 0.
6. **La largeur de bande.** Sur les points 0, 1 et 2, passer à `symmetric_eigen` les matrices de Gram RBF pour γ = 1, 0,1, 0,01 et 10^-3. Prédiction : plus petites valeurs propres d'environ 0,489, 0,0124, 1,3 · 10^-4 et 1,3 · 10^-6, chacune à moins de 10^-12 d'un solveur de référence, et toutes positives.

### Exercice pratique

À l'étape 2, pour quels facteurs d'échelle c la fonction `symmetric_eigen` renvoie-t-elle la diagonale de cT sans une seule rotation ?

> *Solution :* La boucle somme les carrés au-dessus de la diagonale, ici 2c², et s'arrête quand la racine carrée est inférieure à 10^-12, c'est-à-dire quand √2 c < 10^-12, soit c < 10^-12/√2 ≈ 7,07 · 10^-13. Pour tous ces c, la fonction renvoie trois fois c et la matrice semble définie positive. Le seuil est absolu, donc il n'a rien à voir avec le caractère SDP de la matrice ; un test relatif, qui comparerait la norme hors diagonale à la norme de la matrice, ne dépendrait pas de c.

---

## 8. Pièges courants

- **Appeler distance toute dissimilarité.** 1 − cos θ, la distance euclidienne au carré et la formule de Minkowski avec p < 1 violent toutes l'inégalité triangulaire ; vérifiez les axiomes avant d'utiliser un index ou une méthode qui s'appuie sur eux.
- **Faire confiance à une matrice de similarité parce qu'elle a l'air correcte.** Une diagonale positive et des coefficients raisonnables ne rendent pas une matrice SDP ; cherchez sa plus petite valeur propre ou un témoin x tel que xᵀAx < 0.
- **Tester le caractère SDP avec les mineurs dominants.** Le critère de Sylvester caractérise les matrices définies positives ; pour SDP, tous les mineurs principaux doivent être ≥ 0.
- **Prendre une valeur propre négative minuscule pour un verdict.** L'arrondi déplace les valeurs propres d'environ u‖A‖ ; comparez à une tolérance proportionnée à la matrice, pas à 0 ni à une constante absolue.
- **Utiliser un noyau hors de son domaine.** Un noyau polynomial avec c < 0 ou un degré fractionnaire, ou un RBF avec γ < 0, peut donner des matrices de Gram non SDP ; écrêter ensuite les valeurs propres négatives masque l'erreur.
- **Inverser une covariance en espérant que tout ira bien.** La distance de Mahalanobis exige une matrice symétrique définie positive ; l'inversibilité ne suffit pas, et un écrêtage à 0 transforme une erreur en distance nulle.
- **Construire une distance à partir d'une similarité sans écrêtage.** 1 − s peut être négatif par arrondi quand s devrait valoir 1 ; écrêtez à 0 ou utilisez une formule qui ne peut pas devenir négative.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Métrique** | Une fonction positive ou nulle, nulle seulement entre points égaux, symétrique, et qui vérifie l'inégalité triangulaire |
| **Pseudométrique** | Une métrique qui peut donner la distance 0 à des points distincts |
| **Inégalité triangulaire** | d(x, z) ≤ d(x, y) + d(y, z) |
| **Matrice semi-définie positive** | Une matrice symétrique telle que xᵀAx ≥ 0 pour tout x, autrement dit sans valeur propre négative |
| **Matrice de Gram** | La matrice des produits scalaires d'une famille de vecteurs, toujours SDP |
| **Témoin** | Un vecteur x tel que xᵀAx < 0, qui prouve que A n'est pas SDP |
| **Factorisation de Cholesky** | A = LLᵀ avec L triangulaire inférieure, qui existe exactement pour les matrices définies positives |
| **Noyau défini positif** | Une fonction dont toutes les matrices de Gram sont SDP, autrement dit un produit scalaire de vecteurs de caractéristiques |
| **Noyau RBF** | exp(−γ‖x − y‖²), un noyau pour tout γ > 0, de largeur de bande σ donnée par γ = 1/(2σ²) |
| **Distance de Mahalanobis** | √((x − y)ᵀ S⁻¹ (x − y)), la distance euclidienne après blanchiment par la covariance S |
| **Blanchiment** | Un changement de coordonnées linéaire qui transforme une matrice de covariance en l'identité |

---

## Auto-évaluation

**1. Une bibliothèque de regroupement accepte n'importe quelle « distance ». Sur quels axiomes s'appuie-t-elle, et lesquelles de 1 − cos θ, de l'angle θ et de la distance euclidienne au carré les vérifient ?**
> La positivité, la séparation, la symétrie et l'inégalité triangulaire ; c'est cette dernière qui permet à un index d'élaguer une recherche. L'angle est une métrique sur la sphère unité. 1 − cos θ viole l'inégalité triangulaire, comme le montrent 0°, 45° et 90°, et la distance euclidienne au carré la viole sur 0, 1 et 2.

**2. Une matrice de noyau 500 × 500 a une plus petite valeur propre calculée de −3 · 10^-14, et sa plus grande vaut 400. Le noyau est-il invalide ?**
> Pas sur cette seule base. Un solveur spectral inverse-stable déplace les valeurs propres d'un petit multiple de u‖K‖, ici u‖K‖ ≈ 400 · 1,1 · 10^-16 ≈ 4,4 · 10^-14, et ce multiple croît avec n, donc −3 · 10^-14 est nul aux arrondis près. Un noyau valide sur des points presque dépendants produit exactement cela. Une valeur propre nettement négative, ou un témoin x qui reste négatif en arithmétique exacte, trancherait la question.

**3. Pourquoi la distance de Mahalanobis exige-t-elle une matrice définie positive, et que renvoie IX quand elle ne l'est pas ?**
> Avec une M définie positive, (x − y)ᵀM(x − y) > 0 pour x ≠ y et d_M est la distance euclidienne après blanchiment. Une M SDP mais singulière écrase les directions de son noyau, et une M indéfinie rend la forme négative pour certains couples. IX ne vérifie que la forme et écrête les formes négatives à 0, si bien que les deux défauts reviennent sous la forme d'une distance nulle, sans erreur.

**4. `ix_distance` renvoie une distance cosinus de −2,2 · 10^-16 pour deux vecteurs identiques. Est-ce un défaut de vos données ?**
> Non. C'est un arrondi dans la formule d'IX : le produit des deux normes arrondies peut tomber juste sous le produit scalaire, ce qui fait dépasser 1 à la similarité. Écrêtez le résultat à 0 avant de l'utiliser comme distance, et ne comptez pas sur des zéros exacts pour des entrées identiques.

**Critères de réussite :** Énoncer et vérifier les axiomes d'une métrique, tester le caractère semi-défini positif d'une matrice et produire un témoin quand il fait défaut, décider à partir de ses matrices de Gram si une fonction est un noyau, expliquer l'effet de la largeur de bande RBF sur le conditionnement, donner la condition pour que la distance de Mahalanobis soit une métrique, et retracer où les distances et le test par valeurs propres d'IX violent un axiome.

---

## Bases de recherche

- M. Fréchet, « Sur quelques points du calcul fonctionnel », *Rendiconti del Circolo Matematico di Palermo* 22, 1906 : les espaces métriques
- J. Mercer, « Functions of positive and negative type, and their connection with the theory of integral equations », *Philosophical Transactions of the Royal Society A* 209, 1909 : les noyaux définis positifs et les opérateurs intégraux
- P. C. Mahalanobis, « On the generalised distance in statistics », *Proceedings of the National Institute of Sciences of India* 2, 1936 : la distance de Mahalanobis
- I. J. Schoenberg, « Metric spaces and positive definite functions », *Transactions of the American Mathematical Society* 44, 1938 : quand une distance provient d'un produit scalaire, et le noyau gaussien
- N. Aronszajn, « Theory of reproducing kernels », *Transactions of the American Mathematical Society* 68, 1950 : l'espace de caractéristiques d'un noyau défini positif
- B. Schölkopf et A. J. Smola, *Learning with Kernels*, MIT Press, 2002 : les noyaux, les matrices de Gram et leur construction
- R. A. Horn et C. R. Johnson, *Matrix Analysis*, 2e éd., Cambridge University Press, 2013 : les matrices semi-définies positives, Cholesky et le critère de Sylvester
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
