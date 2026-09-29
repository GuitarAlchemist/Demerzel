---
module_id: mat-010-information-entropy-divergences
department: mathematics
course: Entropie, divergences et information mutuelle
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Entropie, divergences et information mutuelle — Mesurer l'incertitude et le coût d'un mauvais modèle

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Calculer l'entropie d'une loi discrète en bits et en nats, et montrer que la loi uniforme la maximise
- Relier entropie conjointe et entropie conditionnelle par la règle de chaînage, et calculer l'information mutuelle de deux variables
- Calculer la divergence de Kullback–Leibler, prouver qu'elle est positive ou nulle, et expliquer pourquoi ce n'est pas une distance
- Utiliser la divergence de Jensen–Shannon quand il faut une comparaison symétrique et bornée
- Dire comment les estimations d'entropie et d'information mutuelle tirées d'échantillons sont biaisées, et retracer ce que garantissent les fonctions d'entropie, de divergence et de délai d'IX

---

## 1. Surprise et entropie

Une issue de probabilité p porte la **surprise** −log p : une issue certaine n'en porte aucune, et chaque division de la probabilité par deux ajoute une unité. L'**entropie** d'une variable aléatoire discrète X de loi p₁, …, p_K est sa surprise moyenne, H(X) = −Σ pᵢ log pᵢ, avec 0 log 0 = 0, la limite de p log p quand p → 0. La base du logarithme fixe l'unité : la base 2 donne des **bits**, le logarithme naturel des **nats**, et 1 bit = ln 2 ≈ 0,693 nat.

L'entropie vaut 0 exactement quand une issue est certaine, et elle vaut au plus log K, avec égalité exactement pour la loi uniforme ; le §3 prouve cette borne. Le théorème de codage de source de Shannon lui donne un sens opérationnel : aucun code binaire uniquement décodable ne peut utiliser en moyenne moins de H(X) bits par symbole, et il existe des codes qui s'en approchent à moins d'un bit.

### Exercice pratique

Quelle est l'entropie de la loi uniforme sur 8 issues, en bits et en nats ? Quelle est l'entropie de (1/2, 1/4, 1/8, 1/8), et comment se compare-t-elle à celle de la loi uniforme sur 4 issues ?

> *Solution :* Chaque issue a la surprise log₂ 8 = 3 bits, donc H = 3 bits, soit 3 ln 2 ≈ 2,079 nats. Pour (1/2, 1/4, 1/8, 1/8), H = 1/2 · 1 + 1/4 · 2 + 1/8 · 3 + 1/8 · 3 = 1/2 + 1/2 + 3/8 + 3/8 = 7/4 bits, sous log₂ 4 = 2 bits. Le code 0, 10, 110, 111 a exactement cette longueur moyenne, 1,75 bit.

---

## 2. Entropie conjointe, entropie conditionnelle et information mutuelle

Pour deux variables, l'**entropie conjointe** H(X, Y) est l'entropie du couple, et l'**entropie conditionnelle** H(Y | X) = Σₓ p(x) H(Y | X = x) est l'incertitude qui reste sur Y une fois X connue. Elles vérifient la **règle de chaînage** H(X, Y) = H(X) + H(Y | X), et conditionner n'augmente jamais l'entropie en moyenne : H(Y | X) ≤ H(Y).

L'**information mutuelle** est la réduction d'incertitude sur une variable qu'apporte l'autre : I(X; Y) = H(Y) − H(Y | X) = H(X) + H(Y) − H(X, Y). Elle est symétrique, jamais négative, et nulle exactement quand X et Y sont indépendantes au sens de MAT-008. Contrairement à un coefficient de corrélation, elle détecte toute dépendance, pas seulement une dépendance linéaire, et aucun réétiquetage bijectif de l'une ou l'autre variable ne la change.

### Exercice pratique

X est un bit équilibré, et Y vaut X sauf qu'il est inversé avec probabilité 1/4. Calculez I(X; Y) en bits.

> *Solution :* Y est aussi un bit équilibré, donc H(Y) = 1. Sachant X, Y n'est incertain que par l'inversion, donc H(Y | X) = h(1/4), où h(q) = −q log₂ q − (1 − q) log₂(1 − q). h(1/4) = 1/4 · 2 + 3/4 · log₂(4/3) = 2 − (3/4) log₂ 3 ≈ 0,811, donc I(X; Y) = 1 − h(1/4) = (3/4) log₂ 3 − 1 ≈ 0,189 bit. La table conjointe (3/8, 1/8; 1/8, 3/8) donne la même valeur par H(X) + H(Y) − H(X, Y).

---

## 3. La divergence de Kullback–Leibler

La **divergence de Kullback–Leibler** de p par rapport à q est KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), sommée sur les issues où pᵢ > 0. Elle vaut +∞ dès que q donne la probabilité 0 à une issue que p permet. L'**inégalité de Gibbs** affirme que KL(p ‖ q) ≥ 0, avec égalité exactement quand p = q. Comme ln x ≤ x − 1, −KL(p ‖ q) = Σ pᵢ ln(qᵢ/pᵢ) ≤ Σ pᵢ (qᵢ/pᵢ − 1) = Σ qᵢ − 1 ≤ 0, où les sommes portent sur pᵢ > 0. Avec q uniforme, KL(p ‖ q) = log K − H(p), ce qui prouve la borne du §1.

KL mesure le coût d'un mauvais modèle. L'**entropie croisée** H(p, q) = −Σ pᵢ log qᵢ vaut H(p) + KL(p ‖ q) : coder des données issues de p avec les longueurs de code idéales −log₂ qᵢ de q coûte en moyenne KL(p ‖ q) bits de plus par symbole, et minimiser la perte logarithmique d'un classifieur minimise la divergence de son modèle par rapport aux données. KL n'est pas une distance : elle n'est pas symétrique, et elle ne vérifie pas l'inégalité triangulaire. L'information mutuelle est elle-même une divergence, I(X; Y) = KL(p(x, y) ‖ p(x) p(y)), le coût de supposer l'indépendance.

### Exercice pratique

Soit p = (3/4, 1/4) et q = (1/2, 1/2). Calculez KL(p ‖ q) et KL(q ‖ p) en nats.

> *Solution :* KL(p ‖ q) = 3/4 · ln(3/2) + 1/4 · ln(1/2) = (3/4) ln 3 − ln 2 ≈ 0,131, qui vaut aussi ln 2 − H(p). KL(q ‖ p) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3) ≈ 0,144. Les deux sens diffèrent, et échanger les arguments peut même transformer une valeur finie en +∞ : KL((1, 0) ‖ (1/2, 1/2)) = ln 2, alors que KL((1/2, 1/2) ‖ (1, 0)) est infinie.

---

## 4. La divergence de Jensen–Shannon

La **divergence de Jensen–Shannon** compare p et q à leur mélange m = (p + q)/2 : JS(p, q) = ½ KL(p ‖ m) + ½ KL(q ‖ m) = H(m) − (H(p) + H(q))/2. Elle est symétrique, et toujours finie, puisque m est positive partout où p ou q l'est. Elle est bornée par ln 2 : m ≥ p/2, donc chaque pᵢ/mᵢ ≤ 2 et KL(p ‖ m) ≤ ln 2, et il en va de même pour q. La borne est atteinte exactement quand p et q ont des supports disjoints. JS est l'information mutuelle entre une pièce équilibrée qui choisit p ou q et l'issue tirée ensuite, et sa racine carrée est une métrique.

### Exercice pratique

Calculez JS((1, 0), (1/2, 1/2)) en nats et en bits, et comparez-la à la borne.

> *Solution :* m = (3/4, 1/4). KL((1, 0) ‖ m) = ln(4/3), et KL((1/2, 1/2) ‖ m) = 1/2 · ln(2/3) + 1/2 · ln 2 = (1/2) ln(4/3). Donc JS = (1/2) ln(4/3) + (1/4) ln(4/3) = (3/4) ln(4/3) ≈ 0,216 nat, soit (3/4) log₂(4/3) ≈ 0,311 bit, bien sous ln 2 ≈ 0,693 nat, un bit. Elle est finie alors que l'une des deux divergences KL entre ces lois ne l'est pas.

---

## 5. Estimer l'information à partir d'échantillons

En pratique p est inconnue, et l'**estimateur par substitution** la remplace par les fréquences observées. L'entropie par substitution est biaisée vers le bas : les fréquences s'ajustent à l'échantillon, et les issues non observées ne contribuent pas. Pour N observations de K issues, le développement au premier ordre de Miller donne E[Ĥ] ≈ H − (K − 1)/(2N) nats. L'information mutuelle par substitution est biaisée vers le haut : pour des variables indépendantes avec B_X et B_Y classes, 2N Î est la statistique G d'un test d'indépendance, approximativement de loi χ² à (B_X − 1)(B_Y − 1) degrés de liberté, donc E[Î] ≈ (B_X − 1)(B_Y − 1)/(2N) nats alors que la vraie valeur est 0.

Les variables continues ajoutent un choix de classes. Avec des classes de largeur Δ, l'entropie par classes est proche de h(X) − log Δ, où h est l'entropie différentielle, donc elle croît sans borne quand les classes rétrécissent ; deux entropies par classes ne sont comparables qu'avec les mêmes classes et le même intervalle. Une divergence KL par substitution est infinie dès qu'une classe est vide dans l'échantillon de q et pas dans celui de p, et lisser les effectifs la rend finie, mais sa valeur dépend alors du lissage.

### Exercice pratique

On lance deux fois une pièce équilibrée, et on estime l'entropie à partir des deux résultats. Quelle est l'estimation par substitution attendue en nats, et comment se compare-t-elle à la vraie entropie ?

> *Solution :* Avec probabilité 1/2 les deux lancers concordent, les fréquences sont (1, 0) et Ĥ = 0 ; avec probabilité 1/2 ils diffèrent, les fréquences sont (1/2, 1/2) et Ĥ = ln 2. Donc E[Ĥ] = (ln 2)/2 ≈ 0,347, la moitié de la vraie valeur ln 2 ≈ 0,693. La correction au premier ordre (K − 1)/(2N) = 1/4 ne l'amènerait qu'à environ 0,60 : le développement suppose N grand devant K.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**Divergences** (`crates/ix-math/src/inference.rs`). [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L176), [`kl_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L187) et [`js_divergence`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L212) travaillent en nats, et elles font d'abord passer leurs entrées par `normalize`, donc tout poids positif ou nul est accepté, et multiplier les poids par une constante ne change rien. `kl_divergence` [renvoie une erreur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L199) quand q est nulle là où p est positive, au lieu de +∞, et le commentaire de documentation de `js_divergence` [énonce la borne](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L211) [0, ln 2]. Le test [`entropy_and_divergences`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L569) vérifie la loi uniforme sur 4 issues, une masse ponctuelle, KL((1, 0) ‖ (1/2, 1/2)) = ln 2, JS de supports disjoints et le cas d'erreur. L'extension DuckDB expose les trois fonctions en SQL sous les noms [`ix_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L143), [`ix_kl`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L192) et [`ix_js`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/inference.rs#L205).

```rust
fn normalize(p: &[f64]) -> Result<Vec<f64>, MathError> {
    if p.is_empty() {
        return Err(MathError::EmptyInput);
    }
    if p.iter().any(|&v| v < 0.0 || v.is_nan()) {
        return Err(MathError::InvalidParameter(
            "probability vector must be non-negative".into(),
        ));
    }
    let total: f64 = p.iter().sum();
    if total <= 0.0 {
        return Err(MathError::InvalidParameter(
            "probability vector sums to zero".into(),
        ));
    }
    Ok(p.iter().map(|v| v / total).collect())
}
```

- **Un total qui déborde donne trois réponses différentes.** `normalize` rejette [les poids négatifs et NaN](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L161) mais pas +∞, et sa [somme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/inference.rs#L166) peut déborder. Pour les poids (10^308, 10^308), le total 2 · 10^308 dépasse le plus grand `f64`, environ 1,8 · 10^308, donc il devient +∞ et chaque poids normalisé devient 0. `shannon_entropy` saute alors tous les termes et renvoie −0.0 au lieu de ln 2, `kl_divergence` contre (1, 3) renvoie 0 au lieu d'environ 0,144, et `js_divergence` renvoie l'erreur « probability vector sums to zero », parce qu'elle normalise de nouveau le vecteur nul. Un poids +∞ passe la vérification et se normalise en NaN : pour (+∞, 1), l'entropie vaut de nouveau −0.0, KL contre (1, 1) vaut 0, et JS échoue avec « must be non-negative ». Ce sont des prédictions tirées d'une transcription ligne à ligne, pas d'une exécution ; MAT-003 traite du débordement, et le §7 les vérifie.
- **Les bornes ne tiennent qu'aux arrondis près.** KL ≥ 0 et JS ≤ ln 2 sont des théorèmes sur des sommes exactes, et les sommes calculées sont arrondies. La transcription renvoie une KL légèrement sous 0, jusqu'à environ −5 · 10^-16, sur plus d'un tiers de 10^5 paires aléatoires presque égales, et une JS légèrement au-dessus de ln 2, d'au plus environ 3 · 10^-16, sur quelques paires presque disjointes. Le test d'IX compare avec une tolérance, comme il se doit ; un appelant qui teste `kl >= 0.0` exactement peut échouer.
- **Le même nom mesure autre chose dans `ix-code`.** Sa fonction [`shannon_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L145) prend des valeurs brutes, les compte dans des classes de même largeur, et [divise l'entropie en bits par log₂ du nombre de classes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L176), ce qui donne un nombre dans [0, 1]. Elle renvoie 0 quand l'étendue vaut au plus [`f64::EPSILON`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/aggregate.rs#L152) en valeur absolue, donc les valeurs 10^-20 et 2 · 10^-20, qui diffèrent d'un facteur 2, reçoivent l'entropie 0, alors que 1 et 2 reçoivent 1/log₂ 10 ≈ 0,301 avec 10 classes.
- **La perplexité est cohérente.** Les deux implémentations de t-SNE comparent une entropie en nats au logarithme naturel de la perplexité visée, [dans `ix-manifold`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L182), dont [`entropy_of`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-manifold/src/lib.rs#L242) utilise `ln`, et [dans `ix-unsupervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/tsne.rs#L75). La perplexité est donc e^H avec H en nats, le même nombre que 2^H avec H en bits.
- **La perte d'entropie croisée est bornée.** [`binary_cross_entropy`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L18) ramène les prédictions [à 10^-12 de 0 et de 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-nn/src/loss.rs#L19), donc une prédiction fausse et sûre d'elle coûte environ 27,63 nats par élément au lieu de +∞.
- **L'information mutuelle n'existe qu'à l'intérieur de `optimal_delay`.** Aucune fonction d'IX ne calcule I(X; Y). [`optimal_delay`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L29) estime l'information mutuelle entre une série et sa copie décalée à partir d'un [histogramme à deux dimensions](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L71), et renvoie le dernier décalage avant que l'estimation [remonte pour la première fois](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L77), la règle de Fraser et Swinney. Son estimation est celle par substitution, avec le biais vers le haut du §5.
- **Son test accepte tous les résultats possibles.** [`test_optimal_delay_sine`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L188) passe 2000 échantillons d'une sinusoïde de période 100, avec au plus 50 décalages et 16 classes. Son [commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L194) attend environ 25, un quart de période, mais il [affirme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L197) seulement un décalage entre 1 et 50, et sur cette entrée la fonction ne peut rien renvoyer d'autre : son résultat est compris entre 1 et le plus petit de la limite de décalage et de n/2, ici 50. Une transcription prédit 5. L'estimation par classes descend à 1,584 nat au décalage 5 et remonte à 1,628 au décalage 6, donc la règle de la première remontée s'arrête là. Avec 1 classe, chaque estimation vaut 0, l'estimation ne remonte jamais, et la fonction renvoie la limite de décalage, 50. Avec 0 classe, [`num_bins - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/embedding.rs#L43) passe sous zéro et l'appel panique : sur la soustraction quand les contrôles de débordement sont actifs, comme dans le build de débogage par défaut, et sinon sur un indice hors limites.

```rust
        let delay = optimal_delay(&data, 50, 16);
        // Optimal delay for a sine wave should be around T/4 = 25
        // The mutual information method can vary; accept a wider range
        assert!(
            (1..=50).contains(&delay),
            "Optimal delay for sine: {}",
            delay
        );
```

Corriger tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pourquoi `shannon_entropy` renvoie-t-elle −0.0 pour les poids (10^308, 10^308), et que renverrait-elle si `normalize` divisait d'abord chaque poids par le plus grand ?

> *Solution :* La somme 10^308 + 10^308 = 2 · 10^308 dépasse le plus grand `f64`, environ 1,8 · 10^308, donc elle s'arrondit à +∞, et chaque poids divisé par +∞ vaut 0. Le filtre ne garde que les poids positifs, la somme de zéro terme vaut 0, et son opposé vaut −0.0. Diviser d'abord par le plus grand poids donne (1, 1), dont la somme 2 est exacte, puis (1/2, 1/2), dont l'entropie vaut ln 2 ≈ 0,693. C'est de l'arithmétique sur le code, pas une exécution ; le §7 le vérifie.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **Valeurs nominales.** Appelez `shannon_entropy` sur huit poids égaux, `kl_divergence` sur (3, 1) contre (1, 1) et en sens inverse, et `js_divergence` sur (1, 0) et (1, 1). Prédiction : 3 ln 2 ≈ 2,079, puis 0,131 et 0,144, puis (3/4) ln(4/3) ≈ 0,216, chacune à 10^-12 près.
2. **Débordement et infini.** Appelez les trois fonctions sur (10^308, 10^308), avec (1, 3) comme second argument, puis sur (+∞, 1) avec (1, 1). Prédiction : −0.0, 0 et l'erreur « sums to zero », puis −0.0, 0 et l'erreur « must be non-negative ».
3. **Bornes et arrondis.** Tirez 10^5 paires de vecteurs de poids presque égaux et presque disjoints avec un générateur à graine. Prédiction : quelques valeurs de KL sous 0 et quelques valeurs de JS au-dessus de ln 2, toutes à moins de 10^-15 de la borne.
4. **Biais par substitution.** Pour 100 graines, tirez 1999 couples de valeurs uniformes indépendantes, rangez chaque coordonnée dans 16 classes égales, et calculez Î = Ĥ(X) + Ĥ(Y) − Ĥ(X, Y) avec `shannon_entropy` sur les effectifs. Prédiction : chaque Î est positive, et leur moyenne est proche de 15²/(2 · 1999) ≈ 0,056 nat.
5. **Le délai.** Appelez `optimal_delay` sur la sinusoïde de `test_optimal_delay_sine` avec 16 classes, 1 classe et 0 classe. Prédiction : 5, puis 50, puis une panique.
6. **L'entropie par classes.** Appelez la fonction `shannon_entropy` de `ix-code` sur (0, 1) avec 2 classes, sur (10^-20, 2 · 10^-20) avec 10 classes, et sur (1, 2) avec 10 classes. Prédiction : 1, puis 0, puis 1/log₂ 10 ≈ 0,301.
7. **Le bornage.** Appelez `binary_cross_entropy` avec la prédiction 0 et la cible 1. Prédiction : 12 ln 10 ≈ 27,63.

### Exercice pratique

À l'étape 4, pourquoi la moyenne reste-t-elle positive alors que les variables sont indépendantes, et quelle moyenne donneraient dix fois plus de couples ?

> *Solution :* L'estimation par substitution est la divergence des fréquences conjointes observées par rapport au produit des marges observées, et le seul bruit d'échantillonnage les rend différentes, donc Î > 0 sur presque tout échantillon. Sa moyenne vaut environ (B_X − 1)(B_Y − 1)/(2N) = 225/3998 ≈ 0,056 nat. Avec dix fois plus de couples, elle est divisée par dix, à environ 0,0056 : le biais décroît comme 1/N, et une estimation positive n'indique une dépendance que si elle dépasse nettement ce que donnent des données indépendantes, par exemple après avoir mélangé l'une des variables.

---

## 8. Pièges courants

- **Mélanger bits et nats.** Un bit vaut ln 2 ≈ 0,693 nat. `inference.rs` d'IX travaille en nats, et `ix-code` rend des bits normalisés.
- **Traiter KL comme une distance.** Elle n'est pas symétrique et n'a pas d'inégalité triangulaire ; utilisez JS, ou sa racine carrée, quand il faut une comparaison symétrique.
- **Laisser q s'annuler là où p ne s'annule pas.** KL est alors infinie, et le lissage ne la rend finie qu'au prix d'une valeur qui dépend du lissage.
- **Se fier à une estimation par substitution tirée de peu d'échantillons.** L'entropie sort trop basse et l'information mutuelle trop haute ; comparez avec des données mélangées.
- **Comparer des entropies par classes calculées avec des classes différentes.** L'entropie par classes d'une variable continue dépend autant de la largeur des classes que des données.
- **Tester une borne exactement en virgule flottante.** Une KL calculée peut valoir −10^-16 ; comparez avec une tolérance.
- **Écrire un test dont l'intervalle accepté contient tous les résultats possibles.** Vérifiez la valeur qu'attend le commentaire, avec la tolérance que permet la méthode.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Surprise** | −log p, l'information portée par une issue de probabilité p |
| **Entropie** | La surprise moyenne d'une variable aléatoire, −Σ pᵢ log pᵢ |
| **Bit et nat** | Les unités d'entropie pour les logarithmes en base 2 et naturel ; 1 bit = ln 2 nat |
| **Entropie conditionnelle** | H(Y \| X), l'incertitude qui reste sur Y une fois X connue |
| **Information mutuelle** | I(X; Y) = H(X) + H(Y) − H(X, Y), nulle exactement en cas d'indépendance |
| **Divergence KL** | KL(p ‖ q) = Σ pᵢ log(pᵢ/qᵢ), le coût d'utiliser q quand les données suivent p |
| **Entropie croisée** | H(p, q) = H(p) + KL(p ‖ q), la perte logarithmique du modèle q sur des données issues de p |
| **Inégalité de Gibbs** | KL(p ‖ q) ≥ 0, avec égalité exactement quand p = q |
| **Divergence de Jensen–Shannon** | La divergence KL moyenne de p et q par rapport à leur mélange ; symétrique et au plus ln 2 |
| **Estimateur par substitution** | Une estimation qui remplace la loi inconnue par les fréquences observées |
| **Perplexité** | e^H avec H en nats, le nombre effectif d'issues équiprobables |

---

## Auto-évaluation

**1. Pourquoi l'entropie d'une loi sur K issues vaut-elle au plus log K, avec égalité seulement pour la loi uniforme ?**
> KL(p ‖ u) = log K − H(p) pour la loi uniforme u, et l'inégalité de Gibbs la rend positive ou nulle, avec égalité exactement quand p = u.

**2. KL(p ‖ q) = 0,131 et KL(q ‖ p) = 0,144. Laquelle est la distance entre p et q ?**
> Aucune. KL n'est pas symétrique : chaque sens répond à sa propre question, le coût de supposer q pour des données issues de p ou l'inverse. Une comparaison symétrique demande JS ou sa racine carrée.

**3. Deux variables, rangées chacune en 16 classes, donnent une information mutuelle par substitution de 0,05 nat sur 2000 observations. Est-ce un signe de dépendance ?**
> Non. Des variables indépendantes donnent en moyenne environ 15²/(2 · 2000) ≈ 0,056 nat avec ces classes, donc 0,05 est ce à quoi ressemble l'absence totale de dépendance. Une comparaison avec des couples mélangés le montrerait.

**4. Le test `test_optimal_delay_sine` d'IX passe. Que vous apprend-il sur `optimal_delay` ?**
> Seulement que l'appel ne panique pas sur cette entrée : le test accepte tout décalage de 1 à 50, c'est-à-dire toute valeur que la fonction peut renvoyer, et non le quart de période qu'attend son commentaire.

**Critères de réussite :** Calculer l'entropie, l'entropie conditionnelle et l'information mutuelle en bits et en nats, calculer et interpréter les divergences KL et de Jensen–Shannon, prouver l'inégalité de Gibbs et la borne log K, expliquer les biais des estimations par substitution, et retracer ce que garantissent les fonctions d'entropie, de divergence, de perte et de délai d'IX.

---

## Bases de recherche

- C. E. Shannon, « A mathematical theory of communication », *Bell System Technical Journal* 27, 1948 : entropie, information mutuelle et codage de source
- S. Kullback et R. A. Leibler, « On information and sufficiency », *Annals of Mathematical Statistics* 22, 1951 : la divergence
- T. M. Cover et J. A. Thomas, *Elements of Information Theory*, 2e éd., Wiley, 2006 : règles de chaînage, inégalité de Gibbs, codage et entropie différentielle
- J. Lin, « Divergence measures based on the Shannon entropy », *IEEE Transactions on Information Theory* 37, 1991 : la divergence de Jensen–Shannon et sa borne
- D. M. Endres et J. E. Schindelin, « A new metric for probability distributions », *IEEE Transactions on Information Theory* 49, 2003 : la racine carrée de JS est une métrique
- G. A. Miller, « Note on the bias of information estimates », dans *Information Theory in Psychology*, Free Press, 1955 : le biais de l'entropie par substitution
- L. Paninski, « Estimation of entropy and mutual information », *Neural Computation* 15, 2003 : le biais des estimateurs par substitution
- A. M. Fraser et H. L. Swinney, « Independent coordinates for strange attractors from mutual information », *Physical Review A* 33, 1986 : le délai au premier minimum de l'information mutuelle
- L. van der Maaten et G. Hinton, « Visualizing data using t-SNE », *Journal of Machine Learning Research* 9, 2008 : la perplexité
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
