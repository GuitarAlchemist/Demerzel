---
module_id: mat-009-estimation-uncertainty-sampling
department: mathematics
course: Estimation, incertitude et échantillonnage reproductible
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Estimation, incertitude et échantillonnage reproductible — Ce qu'un nombre tiré des données peut affirmer

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Définir le biais, la variance et l'erreur quadratique moyenne d'un estimateur, et montrer pourquoi la variance empirique divise par n − 1
- Dire ce qu'affirment un intervalle de confiance et une valeur p, et ce qu'ils n'affirment pas
- Choisir entre le test t de Welch, le test de Mann–Whitney et le test de Kolmogorov–Smirnov, et calculer une valeur p exacte sur de petits échantillons en comptant
- Estimer l'erreur sur de nouvelles données par validation croisée à k plis, et dire pourquoi la dispersion des scores des plis peut sous-estimer son incertitude
- Traiter la graine, le générateur et sa version comme des éléments de la spécification d'une expérience, et dire ce que garantissent les fonctions d'échantillonnage, de validation croisée et de test d'IX

---

## 1. Estimateurs, biais et variance

Un **estimateur** est une règle qui transforme un échantillon X₁, …, Xₙ en une estimation θ̂ d'une quantité inconnue θ. L'échantillon est aléatoire, donc θ̂ est une variable aléatoire, et deux nombres disent s'il est bon : son **biais** E[θ̂] − θ et sa **variance** Var(θ̂). Ensemble, ils donnent l'**erreur quadratique moyenne**, E[(θ̂ − θ)²] = biais² + variance ; développer (θ̂ − E[θ̂] + E[θ̂] − θ)² le montre, puisque le terme croisé est d'espérance nulle.

Pour des tirages indépendants de moyenne μ et de variance σ², la **moyenne empirique** X̄ = (X₁ + … + Xₙ)/n est sans biais, et Var(X̄) = σ²/n, puisque les variances de termes indépendants s'additionnent. Son écart-type σ/√n est l'**erreur type** : la diviser par deux demande quatre fois plus de données.

La variance est plus délicate. Les écarts Xᵢ − X̄ sont mesurés à partir de X̄, qui est ajustée sur les mêmes données, donc ils sont en moyenne plus petits que les écarts à μ : Σ(Xᵢ − X̄)² = Σ(Xᵢ − μ)² − n (X̄ − μ)², dont l'espérance vaut n σ² − n · σ²/n = (n − 1) σ². Diviser par n sous-estime donc σ² du facteur (n − 1)/n, et diviser par n − 1, la **correction de Bessel**, supprime le biais. Sans biais ne veut pas dire meilleur : pour des données normales, diviser par n donne la plus petite erreur quadratique moyenne. L'important est de dire laquelle un nombre utilise.

### Exercice pratique

Le test unitaire d'IX pour le test de Welch utilise les échantillons (1, 2, 3, 4, 5) et (2, 3, 4, 5, 6). Calculez la variance de chaque échantillon avec n − 1 et avec n, puis la statistique t = (X̄₁ − X̄₂)/√(s₁²/n₁ + s₂²/n₂) et les degrés de liberté de Welch–Satterthwaite (s₁²/n₁ + s₂²/n₂)²/((s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)).

> *Solution :* Les deux échantillons ont la somme des carrés des écarts 4 + 1 + 0 + 1 + 4 = 10, donc la variance vaut 10/4 = 5/2 avec n − 1 et 10/5 = 2 avec n. Avec 5/2, chaque moyenne a le carré d'erreur type (5/2)/5 = 1/2, le dénominateur vaut √(1/2 + 1/2) = 1, et t = (3 − 4)/1 = −1. Les degrés de liberté valent 1/((1/2)²/4 + (1/2)²/4) = 1/(1/8) = 8. Ce sont les valeurs du commentaire du test d'IX (§6).

---

## 2. Intervalles de confiance et valeurs p

Par le théorème central limite, X̄ est approximativement normale pour n grand, quelle que soit la loi des Xᵢ, pourvu que σ soit finie. Alors X̄ ± 1,96 σ/√n est un **intervalle de confiance à 95 %** approché : avant le tirage des données, la probabilité que cet intervalle aléatoire contienne μ vaut 0,95. Si les Xᵢ sont normales et que s remplace σ, (X̄ − μ)/(s/√n) suit exactement la loi t de Student à n − 1 degrés de liberté, donc le multiplicateur vient de cette loi, et il est plus grand pour n petit. Pour d'autres lois, l'intervalle t n'est qu'approché, et sur de petits échantillons sa couverture peut rester sous 95 %.

Les 95 % appartiennent à la procédure, pas à un intervalle donné. Une fois les données connues, un intervalle donné contient μ ou ne le contient pas. « μ est dans [a, b] avec la probabilité 0,95 » est l'énoncé d'un intervalle de crédibilité bayésien, lu sur une loi a posteriori comme dans MAT-008, et il demande une loi a priori.

Un **test d'hypothèse** fixe une hypothèse nulle H₀ et une statistique T. La **valeur p** est la probabilité, calculée sous H₀, d'une statistique au moins aussi extrême que celle observée. Ce n'est pas P(H₀ | données) : comme avec les taux de base de MAT-008, passer de l'une à l'autre demande la probabilité a priori de H₀. Quand T est continue et que H₀ est vraie, la valeur p est uniforme sur [0, 1], donc un test au niveau α = 0,05 rejette une hypothèse nulle vraie 5 % du temps. C'est toute sa garantie, et elle vaut pour un test choisi à l'avance. Lancer plusieurs tests et rapporter le plus petit p, ou essayer des analyses jusqu'à ce que l'une marche, multiplie les chances d'un faux positif : c'est le **jardin aux sentiers qui bifurquent**. La **correction de Bonferroni** teste chacune de m hypothèses au niveau α/m, ce qui garde la probabilité d'un rejet à tort au plus égale à α, par la borne de l'union.

### Exercice pratique

Vingt tests indépendants sont menés au niveau α = 0,05, et toutes les hypothèses nulles sont vraies. Quelle est la probabilité qu'au moins une valeur p passe sous 0,05 ? Quel seuil la correction de Bonferroni utilise-t-elle ?

> *Solution :* Chaque valeur p est uniforme, donc chaque test ne donne pas l'alerte avec la probabilité 19/20, et les vingt restent muets avec la probabilité (19/20)^20 ≈ 0,358. Au moins un faux positif a donc la probabilité 1 − (19/20)^20 ≈ 0,64. Bonferroni teste chaque hypothèse au niveau 0,05/20 = 0,0025, et la probabilité d'un rejet à tort est alors au plus 20 · 0,0025 = 0,05.

---

## 3. Tests à deux échantillons

Trois tests d'IX comparent deux échantillons, et ils répondent à des questions différentes :
- **Le test t de Welch** demande si les moyennes diffèrent. Sa statistique divise la différence des moyennes par son erreur type estimée, √(s₁²/n₁ + s₂²/n₂), sans supposer les variances égales, et sa loi sous l'hypothèse nulle est approchée par la loi t de Student aux degrés de liberté de Welch–Satterthwaite. Il suppose que les moyennes empiriques sont proches de la normale.
- **Le test de Mann–Whitney** n'utilise que les rangs. Sa statistique U compte les couples (X₁ᵢ, X₂ⱼ) tels que X₁ᵢ > X₂ⱼ, une égalité comptant pour un demi. Sous l'hypothèse nulle que les n₁ + n₂ observations sont échangeables, chaque choix des rangs qui reviennent au premier échantillon est équiprobable, ce qui donne à U une loi exacte par dénombrement. Pour de grands échantillons, elle est proche d'une loi normale de moyenne n₁ n₂/2.
- **Le test de Kolmogorov–Smirnov à deux échantillons** prend le plus grand écart vertical D entre les deux fonctions de répartition empiriques. Il réagit à toute différence de loi : de position, de dispersion ou de forme.

Un test **exact** calcule la valeur p à partir de la loi nulle finie. Un test **asymptotique** utilise sa limite pour les grands échantillons, qui peut être loin du compte pour de petits échantillons. Avec trois observations par échantillon, il y a C(6, 3) = 20 façons équiprobables de placer les rangs, et l'issue la plus extrême dans chaque sens, toutes les valeurs d'un échantillon sous toutes celles de l'autre, ne correspond qu'à une seule disposition.

### Exercice pratique

Avec trois observations par échantillon, un test de rangs exact bilatéral peut-il donner p < 0,05 ? Quelle est sa valeur p pour une séparation complète ?

> *Solution :* Non. Sous H₀, chacun des C(6, 3) = 20 ensembles de rangs du premier échantillon a la probabilité 1/20. La séparation complète donne U = 0 ou U = 9, une disposition chacune, donc sa valeur p bilatérale vaut 2/20 = 0,1, et toute autre issue en donne une plus grande. La séparation complète est aussi la seule façon d'obtenir D = 1 dans le test de Kolmogorov–Smirnov, dont la valeur p exacte vaut alors elle aussi 2/20 = 0,1. Un test de rangs exact bilatéral de trois contre trois ne peut pas atteindre 0,05, quelles que soient les données. Le test de Welch le peut, car sa valeur p vient d'un modèle normal et non d'un dénombrement des dispositions.

---

## 4. La validation croisée

L'erreur d'un modèle sur les données sur lesquelles il a été ajusté est optimiste, car l'ajustement s'est déjà adapté à leur bruit. La **validation croisée à k plis** estime l'erreur sur de nouvelles données : elle partage les n observations en k plis, ajuste le modèle k fois, chaque fois sur k − 1 plis, et le note sur le pli laissé de côté, de sorte que chaque observation est notée une fois, par un modèle qui ne l'a pas vue. Des plis **stratifiés** gardent dans chaque pli les proportions de classes de l'échantillon entier.

Deux précautions découlent de la construction. Les k scores ne sont pas indépendants, puisque deux ensembles d'entraînement partagent k − 2 plis, donc l'écart-type des scores des plis divisé par √k les traite comme indépendants et peut sous-estimer l'incertitude de leur moyenne ; Bengio et Grandvalet ont montré qu'aucun estimateur de cette variance n'est sans biais pour toute loi. Et la validation croisée estime l'erreur d'une seule procédure : choisir le meilleur de nombreux modèles sur les mêmes plis et rapporter son score rend le score à nouveau optimiste, ce qu'évite la validation croisée imbriquée.

La façon de combiner les scores des plis compte aussi. La moyenne des exactitudes des plis pèse chaque pli également, et l'exactitude des prédictions mises en commun pèse chaque observation également. Elles coïncident quand les plis ont la même taille.

### Exercice pratique

Quatre plis de test contiennent 6, 3, 3 et 3 observations, et un classifieur en classe correctement 6, 1, 1 et 1. Comparez la moyenne des exactitudes des plis avec l'exactitude globale.

> *Solution :* Les exactitudes des plis valent 1, 1/3, 1/3 et 1/3, de moyenne (1 + 1)/4 = 1/2. L'exactitude globale vaut (6 + 1 + 1 + 1)/15 = 9/15 = 3/5. Le grand pli compte pour un pli sur quatre dans le premier nombre et pour 6 observations sur 15 dans le second ; le §6 montre comment IX peut produire de tels plis.

---

## 5. Rééchantillonnage et graine

Le **bootstrap** estime la loi d'échantillonnage d'une statistique à partir de l'échantillon lui-même : tirer n observations avec remise, recalculer la statistique, recommencer de nombreuses fois, et lire la dispersion ou les quantiles des résultats. Un rééchantillon manque une observation donnée avec la probabilité (1 − 1/n)^n, qui tend vers 1/e ≈ 0,368, donc il contient environ 63 % des observations distinctes. L'**intervalle des percentiles**, entre les quantiles à 2,5 % et à 97,5 % des statistiques bootstrap, est l'intervalle de confiance bootstrap le plus simple. Il ne demande aucune formule d'erreur type, mais il hérite du biais de la statistique et peut être médiocre pour n petit.

Rééchantillonner, mélanger des plis et initialiser des modèles consomment tous des nombres aléatoires, donc leurs résultats dépendent du générateur. Un **générateur pseudo-aléatoire** est une fonction déterministe : le même algorithme, démarré à partir de la même **graine**, produit la même suite. La graine seule ne spécifie pas cette suite. Ce que tire une exécution est spécifié par la graine, l'algorithme, la version de la bibliothèque qui l'implémente, et l'ordre dans lequel le programme consomme les nombres ; changez l'un d'eux et les tirages peuvent changer. Un résultat qui tient pour une graine est un résultat sur cette graine. Le rapporter après avoir essayé plusieurs graines est un autre sentier du jardin qui bifurque, donc une exécution doit fixer sa graine avant de voir les données, ou rapporter la dispersion sur de nombreuses graines.

### Exercice pratique

Pour un échantillon de n = 10 observations, quelle est la probabilité qu'une observation donnée manque dans un rééchantillon bootstrap, et combien d'observations distinctes un rééchantillon contient-il en moyenne ?

> *Solution :* Chacun des 10 tirages la manque avec la probabilité 9/10, donc elle manque avec la probabilité (9/10)^10 ≈ 0,349, un peu moins que 1/e ≈ 0,368. Par linéarité de l'espérance, le nombre d'observations distinctes vaut en moyenne 10 · (1 − (9/10)^10) ≈ 6,51.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**L'échantillonnage** (`crates/ix-math/src/random.rs`). [`seeded_rng`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L10) construit un `StdRng` à partir d'une graine `u64`, et [`shuffle_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L35) et [`sample_indices`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L43) prennent un tel générateur en argument. Les quatre fonctions définies entre elles n'en prennent aucun. Les lignes 9 à 17, mot pour mot, montrent le constructeur à graine et la première de ces fonctions ; les trois autres ont la même forme :

```rust
/// Create a seeded RNG for reproducibility.
pub fn seeded_rng(seed: u64) -> StdRng {
    StdRng::seed_from_u64(seed)
}

/// Random matrix from uniform distribution [low, high).
pub fn uniform_matrix(rows: usize, cols: usize, low: f64, high: f64) -> Array2<f64> {
    Array2::random((rows, cols), Uniform::new(low, high).unwrap())
}
```

- **Les fonctions aléatoires publiques ne sont pas reproductibles.** `uniform_matrix`, [`normal_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L20), `uniform_vector` et `normal_vector` appellent [`random`](https://docs.rs/ndarray-rand/0.16.0/ndarray_rand/trait.RandomExt.html) de `ndarray-rand`, qui initialise à chaque appel un nouveau générateur à partir du générateur local au thread de `rand`, lui-même initialisé par le système d'exploitation. Aucun argument ne peut faire concorder deux appels, et les tests de `random.rs` ne vérifient que leurs dimensions. `Uniform::new` échoue quand low ≥ high, donc l'[`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L16) panique pour un intervalle vide, comme `uniform_matrix(2, 2, 1.0, 1.0)`.
- **Une graine n'est pas encore une spécification portable.** La documentation de `rand` 0.9 décrit [`StdRng`](https://docs.rs/rand/0.9.2/rand/rngs/struct.StdRng.html) comme non portable : « any future library version may replace the algorithm and results may be platform-dependent ». Elle renvoie à [`rand_chacha`](https://docs.rs/rand_chacha/0.9.0/rand_chacha/), dont elle dit les générateurs portables. L'espace de travail d'IX demande [`rand = "0.9"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L102), une plage de versions, et son [`.gitignore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.gitignore#L3) exclut `Cargo.lock`, le fichier qui enregistrerait la version utilisée par une compilation. Ainsi `seeded_rng(42)` répète sa suite au sein d'une même compilation, mais épingler IX à `e35138b9` ne fixe pas à lui seul cette suite. L'espace de travail dépend déjà de [`rand_chacha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L103).
- **`sample_indices` raccourcit sa réponse sans prévenir.** Elle [tire `k.min(n)` indices](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/random.rs#L45), donc demander 10 indices parmi 5 en renvoie 5, sans erreur.
- **La validation croisée a une graine, avec une valeur par défaut cachée.** [`KFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L64) et `StratifiedKFold` mélangent par défaut avec la [graine 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L76), et [`cross_val_score`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L245) transmet son argument `seed` à un [`StratifiedKFold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L312). Ce découpage [distribue chaque classe à tour de rôle](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/validation.rs#L193) en repartant chaque fois du premier pli, donc trois classes de 5 observations avec k = 4 donnent des plis de test de 6, 3, 3 et 3, le cas de l'exercice du §4. Avec les étiquettes (0, 0, 1, 1) et k = 3, le troisième pli est vide bien que n ≥ k, et si le modèle accepte une entrée vide, [`accuracy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/metrics.rs#L98) divise alors 0 par 0, ce qui donne NaN en binary64.
- **Aucun intervalle de confiance.** Les crates d'IX n'ont aucune fonction de bootstrap ni d'intervalle de confiance. Le seul rééchantillonnage se trouve dans la forêt aléatoire, qui [tire n indices avec remise](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-ensemble/src/random_forest.rs#L66) pour chaque arbre à partir d'un générateur à graine, et ne rapporte pas l'erreur hors sac que permettraient les observations laissées hors de chaque rééchantillon, environ 37 %.

**Les tests à deux échantillons** (`crates/ix-math/src/inference.rs`). Le fichier dit suivre les conventions de SciPy et épingle ses tests sur des valeurs de SciPy. [`welch_t_test`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L340) utilise la [variance en n − 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L349) du §1, et [`welch_t_test_matches_scipy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L624) vérifie le t = −1 de l'exercice du §1, et une valeur p à 2 · 10^-3 près du 0,3466 de SciPy. Les deux tests de rangs ne calculent que des valeurs p asymptotiques. La valeur p de Mann–Whitney passe par cette fonction de queue, mot pour mot aux lignes 386 à 389 :

```rust
/// Upper tail of the standard normal: `P(Z > z)`.
fn normal_sf(z: f64) -> f64 {
    0.5 * (1.0 - erf(z / std::f64::consts::SQRT_2))
}
```

- **Les petites valeurs p deviennent exactement 0.** [`erf`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L373) est l'approximation 7.1.26 d'Abramowitz et Stegun, à 1,5 · 10^-7 près de la vraie valeur. Pour z grand, l'erf calculée s'arrondit à 1 et 1 − erf vaut exactement 0 : une transcription de ces lignes prédit que [`mann_whitney_u`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L283) renvoie p = 0 dès que z dépasse environ 8,38, là où la vraie queue normale vaut encore environ 5 · 10^-17. Pour 50 observations contre 50, la séparation complète donne z ≈ 8,61 et p = 0, alors que sa valeur p exacte est 2/C(100, 50), minuscule mais positive. Une valeur p de 0 renvoyée par cette fonction signifie « sous environ 10^-16 », pas « impossible » ; calculer directement la fonction d'erreur complémentaire évite l'annulation.
- **La valeur p de Kolmogorov–Smirnov n'est pas celle de SciPy.** Le [commentaire de documentation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L242) cite `method='asymp'` de SciPy, mais le code [applique la correction de Stephens](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L273) à l'intérieur de la série de Kolmogorov, comme le fait Numerical Recipes. Dans SciPy 1.17.1, cette option évalue plutôt la loi de D pour une taille d'échantillon N = n₁ n₂/(n₁ + n₂), arrondie, donc les deux valeurs p diffèrent. Sur de tout petits échantillons, celle d'IX peut être bien trop petite : pour (0, 1, 2) contre (10, 11, 12), les échantillons du [test d'IX](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L590), la formule donne environ 0,033, alors que la valeur p exacte vaut 0,1 (§3). Le test [affirme seulement p < 0,2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L592), ce que les deux valeurs satisfont.

**Un test qui ne peut pas échouer.** [`test_hurst_random_walk`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L208) tire ses pas ±1 de [`rand::rng()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L211), un générateur initialisé par le système d'exploitation, donc chaque exécution teste des données différentes. Son commentaire attend H ≈ 0,5 pour une marche aléatoire. Mais [`hurst_exponent`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L97) [cumule lui-même les écarts](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L116), donc il attend les pas, et le test lui passe la marche, leur somme cumulée. Pour une telle série intégrée, l'étendue normalisée croît comme la taille de la fenêtre elle-même, ce qui prédit H proche de 1, pas de 0,5. L'assertion [0,1 < H < 1,5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/fractal.rs#L221) accepte les deux valeurs, donc le test ne peut pas détecter la confusion. Corriger tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pour (0, 1, 2) contre (10, 11, 12), D = 1 et N = 3 · 3/6 = 3/2. Calculez la valeur p de la formule d'IX, 2 e^(−2t²) avec t = (√N + 0,12 + 0,11/√N) · D, puisque les termes suivants de la série sont ici négligeables, et comparez-la avec la valeur p exacte du §3.

> *Solution :* √(3/2) ≈ 1,225, donc t ≈ 1,225 + 0,12 + 0,090 ≈ 1,435, 2t² ≈ 4,12, et 2 e^(−4,12) ≈ 0,033. Le terme suivant, 2 e^(−8t²), vaut environ 10^-7. La valeur p exacte vaut 2/20 = 0,1 : la formule annonce une significativité à 0,05 là où le §3 a montré que le test exact ne le peut jamais. C'est de l'arithmétique sur le code, pas une exécution ; le §7 le vérifie.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **Même graine, même suite.** Pour s = 0, …, 999, appeler deux fois `shuffle_indices(10, &mut seeded_rng(s))`. Prédiction : les deux permutations sont identiques pour chaque s. Noter la version de `rand` lue dans le `Cargo.lock` de la compilation à côté des résultats.
2. **Graines différentes, statistique stable.** Pour les mêmes 1000 graines, compter les points fixes de chaque permutation. Prédiction : les comptes varient avec la graine, et leur moyenne est à moins de 0,1 de 1, le nombre moyen de points fixes d'une permutation aléatoire uniforme.
3. **Les fonctions sans graine.** Appeler deux fois `uniform_vector(5, 0.0, 1.0)`. Prédiction : les deux vecteurs diffèrent. Puis appeler `uniform_matrix(2, 2, 1.0, 1.0)`. Prédiction : une panique venant de l'`unwrap` de `Uniform::new`.
4. **Échantillonnage tronqué.** Appeler `sample_indices(5, 10, &mut seeded_rng(0))`. Prédiction : 5 indices distincts et aucune erreur.
5. **Queues des tests.** Appeler `mann_whitney_u` sur 0, …, 49 contre 100, …, 149, puis sur 0, …, 39 contre 100, …, 139. Prédiction : U₁ = 0 les deux fois, avec p = 0 exactement pour 50 contre 50 et un p positif de l'ordre de 10^-14 pour 40 contre 40. Appeler `ks_two_sample` sur (0, 1, 2) contre (10, 11, 12). Prédiction : D = 1 et p ≈ 0,033.
6. **Plis.** Découper les étiquettes (0, 0, 1, 1) avec `StratifiedKFold::new(3)`, et cinq étiquettes de chacune de trois classes avec `StratifiedKFold::new(4)`. Prédiction : des plis de test de tailles 2, 2 et 0, puis 6, 3, 3 et 3. Puis lancer `cross_val_score` avec `KNN::new(1)` sur quatre points portant les premières étiquettes, et rapporter si le troisième score vaut NaN ou si l'appel panique.
7. **Le test de Hurst.** Construire les marches de `test_hurst_random_walk` à partir de 100 générateurs à graine au lieu de `rand::rng()`, et appliquer `hurst_exponent` aux marches et à leurs pas. Prédiction : H proche de 1 pour les marches et proche de 0,5 pour les pas, tous dans (0,1 ; 1,5).

### Exercice pratique

L'étape 2 prédit une moyenne à moins de 0,1 de 1 sur 1000 graines. D'où vient cette marge ?

> *Solution :* Soit Iᵢ l'indicatrice du fait que la position i est fixe. Chaque Iᵢ a l'espérance 1/10, donc le nombre de points fixes a l'espérance 10 · 1/10 = 1. Chaque Iᵢ a la variance (1/10)(9/10), et pour i ≠ j, P(les deux fixes) = 1/90, donc la covariance vaut 1/90 − 1/100 = 1/900. La variance vaut 10 · 9/100 + 90 · 1/900 = 9/10 + 1/10 = 1. La moyenne sur 1000 graines indépendantes a l'écart-type 1/√1000 ≈ 0,032, et trois écarts-types, environ 0,095, tiennent dans 0,1. Cela suppose que les graines donnent des permutations uniformes indépendantes, ce qu'un bon générateur approche ; la graine rend l'exécution répétable, pas plus aléatoire.

---

## 8. Pièges courants

- **Rapporter une estimation sans son incertitude.** Une moyenne sans erreur type ni intervalle ne se compare à rien.
- **Lire une valeur p comme la probabilité que l'hypothèse nulle soit vraie.** Elle se calcule en supposant cette hypothèse.
- **Lire « non significatif » comme « aucun effet ».** Un petit échantillon peut manquer de puissance pour détecter quoi que ce soit : un test de rangs exact bilatéral de trois contre trois ne peut jamais atteindre 0,05.
- **Choisir le test après avoir vu les données.** Fixer d'abord le test, la métrique et le seuil, ou corriger pour le nombre de tests.
- **Faire confiance aux valeurs p asymptotiques sur de tout petits échantillons.** Dénombrer la loi nulle exacte quand les échantillons sont petits.
- **Traiter les scores des plis comme indépendants.** Leur écart-type divisé par √k peut sous-estimer l'incertitude de la moyenne de validation croisée.
- **Traiter une graine comme toute la spécification.** Noter aussi le générateur, la version de la bibliothèque et l'ordre des tirages, et rapporter les résultats sur plusieurs graines.
- **Écrire un test que son alternative réussit aussi.** Une borne assez large pour accepter à la fois H ≈ 0,5 et H ≈ 1 ne vérifie ni l'un ni l'autre.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Estimateur** | Une règle qui transforme un échantillon en une estimation d'une quantité inconnue |
| **Biais** | E[θ̂] − θ, l'erreur moyenne d'un estimateur |
| **Erreur type** | L'écart-type d'un estimateur, σ/√n pour la moyenne empirique |
| **Correction de Bessel** | Diviser la somme des carrés des écarts par n − 1, ce qui rend l'estimateur de la variance sans biais |
| **Intervalle de confiance** | Un intervalle aléatoire qui contient la vraie valeur avec une probabilité donnée, avant le tirage des données |
| **Valeur p** | La probabilité sous l'hypothèse nulle d'une statistique au moins aussi extrême que celle observée |
| **Test exact** | Un test dont la valeur p vient de la loi nulle finie, souvent par dénombrement |
| **Validation croisée** | Estimer l'erreur sur de nouvelles données en ajustant sur une partie des données et en notant sur le reste, à tour de rôle |
| **Bootstrap** | Estimer une loi d'échantillonnage en rééchantillonnant les données avec remise |
| **Graine** | L'état initial d'un générateur pseudo-aléatoire ; avec l'algorithme et sa version, elle fixe la suite |
| **Jardin aux sentiers qui bifurquent** | L'inflation des faux positifs quand l'analyse est choisie après avoir vu les données |

---

## Auto-évaluation

**1. Pourquoi diviser par n sous-estime-t-il la variance ?**
> Les écarts sont mesurés à partir de X̄, ajustée sur les mêmes données et plus proche d'elles que μ : E[Σ(Xᵢ − X̄)²] = (n − 1) σ², donc diviser par n donne (n − 1) σ²/n en moyenne.

**2. Une étude rapporte p = 0,03. Pourquoi la probabilité que l'hypothèse nulle soit vraie n'est-elle pas 0,03 ?**
> La valeur p est la probabilité de données au moins aussi extrêmes sachant H₀, pas la probabilité de H₀ sachant les données. Passer de l'une à l'autre demande la probabilité a priori de H₀ et le comportement des données sous l'alternative, comme avec le théorème de Bayes de MAT-008.

**3. Deux exécutions du même programme avec la même graine donnent des résultats différents. Citez trois causes possibles.**
> Une autre version de la bibliothèque du générateur, un autre algorithme sous le même nom, un autre ordre ou nombre de tirages, ou un aléa qui ne vient pas du tout du générateur à graine, comme `uniform_matrix` d'IX.

**4. Le test `test_hurst_random_walk` d'IX passe. Que vous apprend-il sur `hurst_exponent` ?**
> Peu de chose : la borne 0,1 < H < 1,5 accepte à la fois la valeur 0,5 qu'attend son commentaire et la valeur proche de 1 que devrait donner la marche qu'il construit, et ses données changent à chaque exécution.

**Critères de réussite :** Calculer le biais et l'erreur type d'estimateurs simples, interpréter un intervalle de confiance et une valeur p, dénombrer une loi nulle exacte sur de petits échantillons, expliquer ce qu'estime la validation croisée à k plis et ce que manque la dispersion de ses plis, dire ce qu'une graine fixe et ne fixe pas, et retracer ce que garantissent l'échantillonnage, la validation croisée et les tests à deux échantillons d'IX.

---

## Bases de recherche

- L. Wasserman, *All of Statistics*, Springer, 2004 : estimateurs, intervalles de confiance, tests et bootstrap
- B. Efron et R. J. Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993 : le bootstrap et les intervalles des percentiles
- B. L. Welch, « The generalization of 'Student's' problem when several different population variances are involved », *Biometrika* 34, 1947 : le test de Welch
- H. B. Mann et D. R. Whitney, « On a test of whether one of two random variables is stochastically larger than the other », *Annals of Mathematical Statistics* 18, 1947 : le test U
- N. Smirnov, « Table for estimating the goodness of fit of empirical distributions », *Annals of Mathematical Statistics* 19, 1948 : la statistique à deux échantillons
- M. A. Stephens, « Use of the Kolmogorov–Smirnov, Cramér–von Mises and related statistics without extensive tables », *Journal of the Royal Statistical Society B* 32, 1970 : la correction pour petits échantillons
- M. Abramowitz et I. A. Stegun, *Handbook of Mathematical Functions*, National Bureau of Standards, 1964, formule 7.1.26 : l'approximation d'erf
- W. H. Press, S. A. Teukolsky, W. T. Vetterling et B. P. Flannery, *Numerical Recipes*, 3e éd., Cambridge University Press, 2007 : la routine de Kolmogorov–Smirnov que suit IX
- Y. Bengio et Y. Grandvalet, « No unbiased estimator of the variance of K-fold cross-validation », *Journal of Machine Learning Research* 5, 2004 : pourquoi aucune estimation de l'incertitude d'une moyenne de validation croisée n'est sans biais pour toute loi
- A. Gelman et E. Loken, « The garden of forking paths », 2013 : l'analyse qui dépend des données
- A. A. Anis et E. H. Lloyd, « The expected value of the adjusted rescaled Hurst range of independent normal summands », *Biometrika* 63, 1976 : le comportement de l'étendue normalisée sur de petits échantillons
- La documentation de `rand` 0.9 et de `rand_chacha` 0.9, citée au §6 : la portabilité des générateurs à graine
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
