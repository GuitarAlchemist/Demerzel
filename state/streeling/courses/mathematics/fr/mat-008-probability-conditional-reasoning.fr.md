---
module_id: mat-008-probability-conditional-reasoning
department: mathematics
course: Probabilités et raisonnement conditionnel
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies, mat-003-floating-point-conditioning]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Probabilités et raisonnement conditionnel — Réviser une croyance au vu des indices

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Énoncer les axiomes de Kolmogorov, et en déduire la règle du complémentaire et l'inclusion–exclusion
- Calculer des probabilités conditionnelles, et distinguer l'indépendance de l'indépendance conditionnelle
- Appliquer le théorème de Bayes, sous forme de probabilités et sous forme de cotes, et expliquer pourquoi le taux de base compte
- Mettre à jour une loi a priori Beta avec des données binomiales, et dire ce que cache la moyenne a posteriori
- Dire ce que calculent les poids bayésiens des règles d'IX et son classifieur bayésien naïf, et où ils cèdent

---

## 1. Les axiomes

Un modèle probabiliste comporte un **univers** Ω, l'ensemble des issues possibles ; une famille d'**événements**, des parties de Ω qui forment une **tribu** (ou σ-algèbre) ; et une probabilité P, définie sur les événements, qui vérifie les **axiomes de Kolmogorov**. Une tribu contient Ω, le complémentaire de chacun de ses éléments et la réunion de toute suite de ses éléments, donc aussi leurs intersections et leurs différences. Quand Ω est fini ou dénombrable, la tribu peut être l'ensemble de toutes les parties de Ω. Quand Ω n'est pas dénombrable, elle peut devoir être plus petite : la probabilité uniforme sur les réels compris entre 0 et 1 ne peut pas être prolongée à toutes les parties en restant invariante par translation modulo 1 (construction de Vitali). Les axiomes sont :
1. P(A) ≥ 0 pour tout événement A.
2. P(Ω) = 1.
3. Pour des événements deux à deux disjoints A₁, A₂, …, P(A₁ ∪ A₂ ∪ …) = P(A₁) + P(A₂) + ….

Tout le reste en découle. Comme A et son complémentaire sont disjoints et remplissent Ω, P(non A) = 1 − P(A), et P(∅) = 0. Si A ⊆ B, alors P(A) ≤ P(B). Découper A ∪ B en morceaux disjoints donne l'**inclusion–exclusion** : P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Quand Ω est fini et que ses issues sont équiprobables, P(A) = |A|/|Ω|, et calculer une probabilité revient à compter.

### Exercice pratique

Lancez deux dés équilibrés. Calculez P(la somme vaut 7) et P(au moins un six), la seconde de deux façons.

> *Solution :* Les 36 couples ordonnés sont équiprobables. La somme vaut 7 pour (1, 6), (2, 5), (3, 4), (4, 3), (5, 2) et (6, 1), donc P = 6/36 = 1/6. Pour au moins un six, le complémentaire « aucun six » compte 5 · 5 = 25 couples, donc P = 1 − 25/36 = 11/36. Par inclusion–exclusion, P(le premier vaut 6) + P(le second vaut 6) − P(les deux valent 6) = 1/6 + 1/6 − 1/36 = 11/36.

---

## 2. Probabilité conditionnelle et indépendance

La **probabilité conditionnelle** de A sachant B, pour P(B) > 0, est P(A | B) = P(A ∩ B)/P(B) : on restreint les issues à B et on renormalise. Elle donne la **règle du produit** P(A ∩ B) = P(A | B) P(B), et, quand les événements B₁, …, B_k découpent Ω en morceaux disjoints, la **formule des probabilités totales** P(A) = P(A | B₁) P(B₁) + … + P(A | B_k) P(B_k).

A et B sont **indépendants** quand P(A ∩ B) = P(A) P(B), ce qui, pour P(B) > 0, signifie P(A | B) = P(A) : apprendre B ne change pas la probabilité de A. L'indépendance n'est pas la disjonction. Deux événements disjoints de probabilité positive ne sont jamais indépendants, puisque apprendre l'un exclut l'autre. A et B sont **conditionnellement indépendants** sachant C quand P(A ∩ B | C) = P(A | C) P(B | C). Aucune des deux indépendances n'entraîne l'autre : deux tests sur le même patient peuvent être conditionnellement indépendants sachant son état, et pourtant dépendants dans l'ensemble, puisqu'un premier résultat positif rend la maladie, donc un second résultat positif, plus probable.

### Exercice pratique

Avec deux dés, soit A l'événement « le premier dé montre 6 ». Calculez P(A | la somme vaut 7), P(A | la somme vaut 11) et P(A | la somme vaut 12), et dites quelle condition laisse A indépendant.

> *Solution :* P(A) = 1/6. Parmi les 6 couples de somme 7, seul (6, 1) a un premier 6, donc P(A | somme 7) = 1/6 = P(A) : ces deux événements sont indépendants. La somme vaut 11 pour (5, 6) et (6, 5), donc P(A | somme 11) = 1/2. La somme vaut 12 seulement pour (6, 6), donc P(A | somme 12) = 1. Seule la somme 7 laisse A indépendant.

---

## 3. Le théorème de Bayes et les taux de base

Écrire P(H ∩ E) de deux façons avec la règle du produit donne le **théorème de Bayes** :

P(H | E) = P(E | H) P(H)/P(E), avec P(E) = P(E | H) P(H) + P(E | non H) P(non H).

P(H) est la **probabilité a priori**, P(E | H) la **vraisemblance** et P(H | E) la **probabilité a posteriori**. Diviser le théorème pour H par le théorème pour « non H » donne la **forme par les cotes** : la cote a posteriori égale la cote a priori multipliée par le **rapport de vraisemblance** P(E | H)/P(E | non H). Quand plusieurs indices sont conditionnellement indépendants sachant H et sachant « non H », leurs rapports de vraisemblance se multiplient, et l'ordre dans lequel ils arrivent n'importe pas.

Un test pour une affection qui touche 1 % des gens a une sensibilité P(+ | malade) de 99 % et un taux de faux positifs P(+ | sain) de 5 %. Alors P(+) = 0,99 · 0,01 + 0,05 · 0,99 = 0,0099 + 0,0495 = 0,0594, et P(malade | +) = 0,0099/0,0594 = 1/6. Après un résultat positif à un test sensible à 99 %, il reste cinq chances sur six que la personne soit saine, parce que les personnes saines sont 99 fois plus nombreuses. Ignorer ainsi la probabilité a priori est l'**oubli du taux de base**.

### Exercice pratique

La même personne passe un second test, conditionnellement indépendant du premier sachant son état, et il est positif lui aussi. Utilisez la forme par les cotes pour mettre à jour.

> *Solution :* Après le premier test, P(malade) = 1/6, soit une cote de 1 contre 5. Le rapport de vraisemblance d'un résultat positif vaut 0,99/0,05 = 19,8. La cote a posteriori vaut 19,8/5 = 3,96, donc P(malade | deux positifs) = 3,96/4,96 = 99/124, environ 0,80. Le théorème de Bayes avec la probabilité a priori 1/6 donne le même nombre.

---

## 4. La conjugaison : le modèle Beta–binomial

Soit θ une probabilité de succès inconnue. La loi **Beta(α, β)**, pour α, β > 0, a une densité proportionnelle à θ^(α−1) (1 − θ)^(β−1) sur [0, 1] ; Beta(1, 1) est la loi uniforme. Après s succès et f échecs, la vraisemblance est proportionnelle à θ^s (1 − θ)^f, donc la loi a posteriori est proportionnelle à θ^(α+s−1) (1 − θ)^(β+f−1) : c'est Beta(α + s, β + f). Une loi a priori dont la loi a posteriori reste dans la même famille est **conjuguée**, et ici α et β jouent le rôle de pseudo-comptes de succès et d'échecs. La moyenne a posteriori vaut (α + s)/(α + β + s + f), et Beta(a, b) a la variance ab/((a + b)² (a + b + 1)).

Comme la mise à jour ne fait qu'ajouter des comptes, la loi a posteriori ne dépend des données qu'à travers s et f : les mises à jour **commutent**, et une observation à la fois donne la même loi a posteriori que toutes à la fois. La moyenne seule cache ce que l'on sait. Beta(2, 2) et Beta(501, 501) ont toutes deux la moyenne 1/2, mais leurs variances valent 1/20 et environ 2,5 · 10^-4. Une règle qui doit continuer d'explorer les options incertaines, comme l'**échantillonnage de Thompson**, qui tire θ selon chaque loi a posteriori et choisit le plus grand tirage, a besoin de toute la loi, pas seulement de sa moyenne.

### Exercice pratique

Partez de Beta(1, 1) et observez 3 succès et 1 échec. Donnez la loi a posteriori, sa moyenne et sa variance.

> *Solution :* Beta(1 + 3, 1 + 1) = Beta(4, 2), de moyenne 4/6 = 2/3 et de variance 4 · 2/(6² · 7) = 8/252 = 2/63.

---

## 5. Bayes naïf et calcul en échelle logarithmique

Le théorème de Bayes classe : P(classe c | x) est proportionnelle à P(c) p(x | c). Le **bayésien naïf** suppose que les variables x₁, …, x_p sont conditionnellement indépendantes sachant la classe, de sorte que p(x | c) = p(x₁ | c) · … · p(x_p | c). Le **bayésien naïf gaussien** modélise chaque p(x_j | c) par une densité normale, avec une moyenne et une variance par classe estimées sur les données d'entraînement.

Deux points numériques décident si cela marche. D'abord, un produit de nombreuses petites densités sous-déborde, donc le calcul additionne plutôt des log-probabilités, et il normalise avec l'astuce **log-sum-exp** : soustraire le plus grand score logarithmique avant d'exponentier, ce qui ne change pas les rapports et fait du plus grand terme exp(0) = 1. Ensuite, la formule de variance E[x²] − E[x]² soustrait deux nombres presque égaux quand la moyenne est grande devant la dispersion, et l'annulation de MAT-003 détruit la différence. Soustraire d'abord la moyenne, la formule **en deux passes** moyenne((x − x̄)²), ou la mise à jour en une passe de Welford l'évitent.

### Exercice pratique

Deux classes ont les scores logarithmiques −1000 et −1002. Que se passe-t-il si vous les exponentiez directement, et quelles probabilités donne log-sum-exp ?

> *Solution :* e^-1000 est sous le plus petit nombre binary64 positif, environ 4,9 · 10^-324, donc les deux exponentielles s'arrondissent à 0 et la normalisation vaut 0/0. Soustraire le maximum donne exp(0) = 1 et e^-2, donc les probabilités valent 1/(1 + e^-2) ≈ 0,881 et 0,119.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**Les poids bayésiens des règles** (`crates/ix-grammar/src/weighted.rs`). Une `WeightedRule` part de la [loi a priori uniforme Beta(1, 1)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L31) et stocke comme poids la [moyenne de la loi Beta](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L13). [`bayesian_update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L57) est la mise à jour conjuguée du §4, mot pour mot aux lignes 57 à 66 :

```rust
pub fn bayesian_update(rule: &WeightedRule, success: bool) -> WeightedRule {
    let mut updated = rule.clone();
    if success {
        updated.alpha += 1.0;
    } else {
        updated.beta += 1.0;
    }
    updated.weight = updated.alpha / (updated.alpha + updated.beta);
    updated
}
```

- **La mise à jour est correcte, et elle commute exactement.** Les comptes sont des entiers, exacts en binary64 jusqu'à 2^53, donc tout ordre des mêmes observations donne les mêmes α, β et poids, bit pour bit. [`test_bayesian_update_success`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L145) vérifie un succès à partir de Beta(1, 1).
- **La sélection ne voit que la moyenne, à travers un softmax plat.** [`softmax`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L83) donne à chaque règle une probabilité proportionnelle à exp(poids/T), et [`select_weighted`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-grammar/src/weighted.rs#L111) tire à T = 1. Les poids que `bayesian_update` tire d'une loi a priori Beta sont compris entre 0 et 1, donc à T = 1 aucune de ces règles n'est plus de e ≈ 2,72 fois plus probable qu'une autre : une règle de poids 0,99 face à une règle de poids 0,01 est choisie avec la probabilité 1/(1 + e^-0,98) ≈ 0,727. Beta(2, 2) et Beta(501, 501) donnent le même poids, donc une règle essayée deux fois et une règle essayée mille fois sont traitées de la même façon ; ce n'est pas de l'échantillonnage de Thompson.
- **L'outil MCP fait confiance à son entrée.** Le gestionnaire de `ix_grammar_weights` lit [`alpha`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1559) et `beta` sans vérifier qu'ils sont positifs, comme l'exige une loi Beta, et accepte un [`weight`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1561) qui peut les contredire, voire sortir de [0, 1] ; le softmax utilise ce poids pour toute règle que la requête ne met pas à jour. Sa température [vaut 1 par défaut](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1601).

**Le bayésien naïf** (`crates/ix-supervised/src/naive_bayes.rs`). `GaussianNaiveBayes` travaille en échelle logarithmique et soustrait le [plus grand score logarithmique](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L101) avant d'exponentier, comme le recommande le §5. Sa variance est l'autre formule du §5, mot pour mot aux lignes 52 à 59 :

```rust
            let mean = class_data.mean_axis(ndarray::Axis(0)).unwrap();
            let var = class_data
                .mapv(|v| v * v)
                .mean_axis(ndarray::Axis(0))
                .unwrap()
                - &mean.mapv(|v| v * v);
            // Add small epsilon to avoid division by zero
            let var = var.mapv(|v| v.max(1e-9));
```

- **La variance s'annule pour des variables décalées.** Pour les données de classe c + (0, 1, 2), de variance 2/3, une transcription de ces lignes, avec les sommes séquentielles qu'utilise `ndarray` pour moins de 8 lignes, prédit la variance calculée 0,671875 à c = 10^7, 2 à c = 10^8, et exactement 0 à c = 10^9. La fonction `var_axis` du crate `ndarray` utilise elle-même la mise à jour de Welford.
- **Le plancher est absolu.** Une variance calculée nulle ou négative devient 10^-9, quelle que soit l'échelle de la variable, comme les seuils absolus de MAT-003. À c = 10^9, il transforme le 0 calculé en 10^-9 là où la vraie variance vaut 2/3, et le classifieur devient certain.
- **Une classe manquante panique.** `fit` fixe le nombre de classes à [la plus grande étiquette plus un](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L37). Si une étiquette inférieure n'a aucun exemple, cette classe n'a aucune ligne, `mean_axis` renvoie `None` pour un axe vide, et le [`unwrap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L52) panique.
- **Le test reste dans le cas facile.** [`test_gaussian_nb`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/naive_bayes.rs#L127) ajuste six points bien séparés près de l'origine et vérifie une exactitude d'entraînement supérieure à 0,8. Il ne vérifie aucune probabilité, aucun décalage et aucune étiquette manquante.

**À travers le serveur MCP.** L'opération `naive_bayes` de `ix_supervised` convertit les étiquettes avec [`as usize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2615), qui tronque 1,5 en 1 et sature −1 en 0, et elle appelle `fit` sans protection. L'outil est déclaré comme le skill [`supervised`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L665), et [chaque skill du registre](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L320) devient un outil MCP adossé au registre, dont les appels s'exécutent pendant que `dispatch_action` tient un `Mutex` global. La lecture de ce code prédit qu'une panique dans `fit` laisse l'appel sans réponse et empoisonne ce mutex, après quoi chaque appel adossé au registre panique sur le [`expect`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238) du verrou, jusqu'au redémarrage du serveur. Corriger tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pour les classes c + (0, 1, 2) et c + (4, 5, 6) et le point c + 2,5, la probabilité a posteriori exacte de la première classe vaut 1/(1 + e^-3) ≈ 0,953. Avec les variances calculées ci-dessus, prédisez ce que `predict_proba` renvoie à c = 10^8 et à c = 10^9.

> *Solution :* Les deux classes reçoivent la même variance calculée v, donc les termes de normalisation se compensent et seules les distances au carré comptent : 1,5² = 2,25 jusqu'à la première moyenne et 2,5² = 6,25 jusqu'à la seconde, puisque les moyennes c + 1 et c + 5 sont calculées exactement ici. L'écart entre les scores logarithmiques vaut (6,25 − 2,25)/(2v) = 2/v, soit 3 pour la vraie valeur v = 2/3. À c = 10^8, v = 2 donne l'écart 1 et la probabilité 1/(1 + e^-1) ≈ 0,731. À c = 10^9, v = 10^-9 donne l'écart 2 · 10^9, e^(−2 · 10^9) sous-déborde vers 0, et la probabilité vaut exactement 1. La première réponse est trop hésitante et la seconde certaine ; toutes deux viennent de la variance, pas des données. C'est une prédiction tirée de la lecture du code, pas une exécution ; le §7 la vérifie.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **La commutation.** Appliquez `bayesian_update` à partir de Beta(1, 1) aux mêmes 10^3 observations dans trois ordres : tel qu'enregistré, inversé, et tous les succès d'abord. Prédiction : des α, β et poids identiques, bit pour bit.
2. **Le softmax plat.** Construisez deux règles avec α, β = 99, 1 et 1, 99, de poids 0,99 et 0,01, et appelez `select_weighted` 10^5 fois avec un générateur à graine fixe. Prédiction : la fréquence de la première règle vaut 0,727 à 0,005 près.
3. **Le balayage des décalages.** Pour c = 10^0, …, 10^9, ajustez `GaussianNaiveBayes` sur les classes c + (0, 1, 2) et c + (4, 5, 6), et appelez `predict_proba` en c + 2,5. Prédiction : à moins de 10^-4 de 0,9526 pour c ≤ 10^6, environ 0,9515 à c = 10^7, environ 0,7311 à c = 10^8, et exactement 1 à c = 10^9. Soustraire d'abord de chaque valeur la moyenne de la variable d'entraînement, c + 3, donne 0,9526 pour tout c.
4. **La classe manquante.** Appelez `fit` avec les étiquettes (0, 0, 2, 2). Prédiction : la panique « called `Option::unwrap()` on a `None` value ». Puis, dans un processus `ix-mcp` jetable, jamais dans un processus partagé, envoyez à `ix_supervised` l'opération `naive_bayes` avec ces étiquettes, suivie d'un appel `ix_stats` bien posé. Prédiction : aucun des deux appels ne reçoit de réponse, et la sortie d'erreur du serveur montre cette panique, puis « middleware chain mutex poisoned ».

### Exercice pratique

L'étape 2 prédit 0,727 à 0,005 près pour 10^5 tirages. D'où vient cette marge ?

> *Solution :* Chaque tirage choisit la première règle avec la probabilité p ≈ 0,727, indépendamment des autres, donc le compte est binomial et la fréquence a l'écart-type √(p (1 − p)/n) = √(0,727 · 0,273/10^5) ≈ 0,0014. Trois écarts-types, environ 0,0042, tiennent dans 0,005. Cela suppose que le générateur se comporte comme des tirages uniformes indépendants ; la graine rend l'exécution reproductible, pas plus aléatoire.

---

## 8. Pièges courants

- **Confondre P(E | H) et P(H | E).** La sensibilité d'un test n'est pas la probabilité de la maladie après un résultat positif.
- **Ignorer le taux de base.** Le même indice fait bien moins bouger une hypothèse rare qu'une hypothèse courante.
- **Tenir des événements disjoints pour indépendants.** Des événements disjoints de probabilité positive sont toujours dépendants.
- **Multiplier les rapports de vraisemblance d'indices dépendants.** Deux résultats ne se multiplient que s'ils sont conditionnellement indépendants sachant chaque hypothèse.
- **Donner une moyenne a posteriori sans sa dispersion.** Beta(2, 2) et Beta(501, 501) ont la même moyenne ; ce que l'on sait diffère.
- **Calculer une variance par E[x²] − E[x]².** Soustrayez d'abord la moyenne.
- **Multiplier directement de nombreuses petites probabilités.** Additionnez leurs logarithmes, et normalisez avec log-sum-exp.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Univers** | L'ensemble Ω des issues possibles ; les événements en sont des parties qui forment une tribu |
| **Axiomes de Kolmogorov** | P(A) ≥ 0, P(Ω) = 1, et l'additivité sur les événements disjoints |
| **Probabilité conditionnelle** | P(A \| B) = P(A ∩ B)/P(B), pour P(B) > 0 |
| **Indépendance** | P(A ∩ B) = P(A) P(B) : apprendre l'un des événements ne change pas la probabilité de l'autre |
| **Indépendance conditionnelle** | P(A ∩ B \| C) = P(A \| C) P(B \| C) |
| **Théorème de Bayes** | P(H \| E) = P(E \| H) P(H)/P(E) |
| **Rapport de vraisemblance** | P(E \| H)/P(E \| non H), le facteur par lequel un indice multiplie la cote de H |
| **Oubli du taux de base** | Juger P(H \| E) d'après P(E \| H) en ignorant la probabilité a priori P(H) |
| **Loi a priori conjuguée** | Une loi a priori dont la loi a posteriori reste dans la même famille, comme Beta pour des données binomiales |
| **Bayésien naïf** | Un classifieur qui suppose les variables conditionnellement indépendantes sachant la classe |
| **Log-sum-exp** | La normalisation de scores logarithmiques par soustraction de leur maximum avant l'exponentiation |

---

## Auto-évaluation

**1. Pourquoi deux événements disjoints de probabilité positive ne peuvent-ils pas être indépendants ?**
> P(A ∩ B) = P(∅) = 0, alors que P(A) P(B) > 0.

**2. Un test a une sensibilité de 99 %. Pourquoi la probabilité de la maladie après un résultat positif n'est-elle pas de 99 % ?**
> La probabilité a posteriori dépend aussi de la probabilité a priori et du taux de faux positifs. Avec une prévalence de 1 % et un taux de faux positifs de 5 %, elle vaut 1/6 : la plupart des résultats positifs viennent des nombreuses personnes saines.

**3. Pourquoi les mises à jour Beta–binomiales commutent-elles ?**
> La loi a posteriori Beta(α + s, β + f) ne dépend des données qu'à travers les nombres de succès s et d'échecs f, qui ne dépendent pas de l'ordre des observations.

**4. Le test `test_gaussian_nb` d'IX passe. Que vous dit-il sur des variables décalées ?**
> Rien : ses points sont près de l'origine, où E[x²] − E[x]² ne perd rien. L'annulation demande une moyenne grande devant la dispersion de la classe.

**Critères de réussite :** Déduire des conséquences des axiomes de Kolmogorov, calculer des probabilités conditionnelles et vérifier une indépendance, appliquer le théorème de Bayes sous ses deux formes avec un taux de base, mettre à jour une loi a priori Beta et donner sa moyenne et sa variance, normaliser des scores logarithmiques avec log-sum-exp, et suivre ce que calculent les poids des règles et le bayésien naïf d'IX et où ils cèdent.

---

## Bases de recherche

- A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung*, Springer, 1933 : les axiomes
- J. K. Blitzstein et J. Hwang, *Introduction to Probability*, 2e éd., CRC Press, 2019 : la probabilité conditionnelle, le théorème de Bayes et le modèle Beta–binomial
- E. T. Jaynes, *Probability Theory: The Logic of Science*, Cambridge University Press, 2003 : la probabilité comme logique étendue, et la forme par les cotes du théorème de Bayes
- D. Kahneman et A. Tversky, « On the psychology of prediction », *Psychological Review* 80, 1973 : l'oubli des taux de base
- W. R. Thompson, « On the likelihood that one unknown probability exceeds another in view of the evidence of two samples », *Biometrika* 25, 1933 : l'échantillonnage de Thompson
- B. P. Welford, « Note on a method for calculating corrected sums of squares and products », *Technometrics* 4, 1962 : une variance stable en une passe
- T. F. Chan, G. H. Golub et R. J. LeVeque, « Algorithms for computing the sample variance: analysis and recommendations », *The American Statistician* 37, 1983 : pourquoi E[x²] − E[x]² échoue
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
