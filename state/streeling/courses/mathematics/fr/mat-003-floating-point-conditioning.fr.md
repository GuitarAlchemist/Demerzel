---
module_id: mat-003-floating-point-conditioning
department: mathematics
course: Fondements du calcul numérique
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Arithmétique flottante et conditionnement — Quand un ordinateur perd des chiffres

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Expliquer pourquoi la plupart des nombres réels, dont 0,1, ne peuvent pas être stockés exactement dans un ordinateur
- Énoncer le modèle standard de l'arrondi flottant et le sens de l'epsilon machine
- Distinguer l'erreur directe de l'erreur inverse, et un problème mal conditionné d'un algorithme instable
- Démontrer la borne qui définit le conditionnement d'un système linéaire
- Estimer à partir de κ(A) combien de chiffres un calcul peut perdre, et trouver où IX trace cette limite dans son code

---

## 1. Les nombres qu'un ordinateur peut stocker

Un ordinateur ne stocke pas les nombres réels. Il en stocke un ensemble **fini**. Le format courant, **binary64** de la norme IEEE 754 (`f64` en Rust, `double` en C), code un nombre sur 64 bits : 1 bit de signe, 11 bits d'exposant et 52 bits de fraction. Avec le 1 de tête implicite, chaque nombre stocké porte **53 bits significatifs**, soit environ 16 chiffres décimaux.

Les nombres stockés ne sont pas régulièrement espacés. Entre 1 et 2, ils sont distants de 2^-52 ; entre 2 et 4, deux fois plus ; et ainsi de suite. Deux quantités décrivent cette grille :
- L'**epsilon machine** ε = 2^-52 ≈ 2,2 × 10^-16 est l'écart entre 1 et le nombre stocké suivant.
- L'**unité d'arrondi** u = ε/2 = 2^-53 ≈ 1,1 × 10^-16 est la plus grande erreur relative commise quand un réel (dans l'intervalle représentable) est arrondi au nombre stocké le plus proche.

Un nombre n'est stocké exactement que s'il est une fraction dont le dénominateur est une puissance de deux (et s'il tient dans l'intervalle et dans les 53 bits). **0,1 = 1/10 ne l'est pas** : son dénominateur contient le facteur 5, donc son développement binaire ne s'arrête jamais, tout comme 1/3 = 0,333… en décimal. L'ordinateur stocke à la place le nombre binary64 le plus proche. C'est pourquoi `0.1 + 0.2 == 0.3` n'est pas un test sûr : chaque littéral est arrondi, la somme est arrondie à nouveau, et rien ne garantit que le résultat tombe sur le même nombre stocké que 0,3.

### Exercice pratique

Parmi ces nombres, lesquels sont stockés exactement en binary64 : 0,5, 0,75, 0,1, 1/3, 2^60 ?

> *Solution :* 0,5 = 2^-1, 0,75 = 2^-1 + 2^-2 et 2^60 sont exacts : chacun est une somme de quelques puissances de deux, bien à l'intérieur de l'intervalle. 0,1 et 1/3 ne le sont pas : leurs dénominateurs (10 et 3) ne sont pas des puissances de deux, donc leurs développements binaires sont infinis et doivent être arrondis.

---

## 2. Le modèle standard de l'arrondi

IEEE 754 exige que chaque opération de base soit **correctement arrondie** : l'ordinateur renvoie le résultat exact, arrondi à un nombre stocké. Avec l'arrondi au plus proche, et tant que rien ne déborde ni ne sous-déborde, on obtient le **modèle standard** :

fl(x ∘ y) = (x ∘ y)(1 + δ), avec |δ| ≤ u, pour ∘ l'une des opérations +, −, ×, ÷.

Une opération *isolée* est donc presque exacte. Les ennuis viennent de deux sources :
- **L'accumulation.** Un long calcul commet beaucoup de petites erreurs, et elles peuvent s'additionner.
- **La cancellation** (ou élimination). Soustraire deux nombres presque égaux est exact ou presque, mais cela révèle les erreurs d'arrondi que les opérandes portaient *déjà*. Les premiers chiffres s'annulent ; ce qui reste est surtout du bruit.

### Exercice pratique

Le nombre a = 1 + 10^-8 est stocké avec une erreur relative d'au plus u, et b = 1 est stocké exactement. Bornez l'erreur relative de la différence calculée â − b, en négligeant l'erreur (minime) de la soustraction elle-même.

> *Solution :* La valeur stockée est â = a(1 + δ) avec |δ| ≤ u. Alors â − b = (a − b) + aδ, donc l'erreur relative vaut |aδ| / |a − b| ≤ u(1 + 10^-8) / 10^-8 ≈ 10^8 · u ≈ 1,1 × 10^-8. Le résultat a environ 8 chiffres corrects, pas 16 : la soustraction en a perdu la moitié.

---

## 3. Erreur directe, erreur inverse et conditionnement

Supposons que l'on veuille y = f(x) et que l'ordinateur renvoie ŷ.
- L'**erreur directe** (forward error) demande : à quelle distance la réponse est-elle de la vérité ? Elle vaut |ŷ − y| / |y|.
- L'**erreur inverse** (backward error) demande : pour quelle entrée voisine ŷ est-il la réponse *exacte* ? C'est la plus petite perturbation relative |Δx| / |x| telle que ŷ = f(x + Δx).

Un algorithme est **inversement stable** (backward stable) si son erreur inverse est toujours de l'ordre de u : il donne la réponse exacte à une question légèrement différente. Que cette réponse soit *proche de la vérité* dépend du problème, pas de l'algorithme. Le **conditionnement** mesure à quel point le problème amplifie une variation relative de son entrée. Les deux se combinent dans la règle la plus utile de l'analyse numérique :

erreur directe ≲ conditionnement × erreur inverse.

Cette règle sépare deux échecs différents : un **problème mal conditionné** (aucun algorithme ne peut faire beaucoup mieux) et un **algorithme instable** (un meilleur algorithme ferait mieux).

### Exercice pratique

Pour une fonction dérivable, le conditionnement relatif vaut |x · f′(x) / f(x)|. Calculez-le pour f(x) = x − 1 et évaluez-le en x = 1 + 10^-8.

> *Solution :* f′(x) = 1, donc le conditionnement vaut |x / (x − 1)|. En x = 1 + 10^-8, il vaut (1 + 10^-8) / 10^-8 ≈ 10^8. C'est la cancellation du §2 vue du côté du problème : toute erreur relative sur x est amplifiée environ 10^8 fois, quel que soit l'algorithme qui calcule x − 1.

---

## 4. Le conditionnement d'une matrice

Résolvons maintenant un système linéaire A x = b, avec A carrée et inversible. Supposons le second membre perturbé : A(x + Δx) = b + Δb. Quelle peut être la taille de la variation relative de x ?

**Théorème.** Pour toute norme vectorielle et sa norme matricielle subordonnée,

‖Δx‖ / ‖x‖ ≤ κ(A) · ‖Δb‖ / ‖b‖, où κ(A) = ‖A‖ · ‖A⁻¹‖.

*Démonstration (directe, comme dans MAT-001) :*
- En soustrayant A x = b de A(x + Δx) = b + Δb, on obtient A Δx = Δb, donc Δx = A⁻¹ Δb et ‖Δx‖ ≤ ‖A⁻¹‖ · ‖Δb‖.
- De b = A x, on tire ‖b‖ ≤ ‖A‖ · ‖x‖, donc 1 / ‖x‖ ≤ ‖A‖ / ‖b‖ (pour b ≠ 0).
- En multipliant les deux inégalités, on obtient ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. ∎

En norme euclidienne, κ₂(A) = σ_max / σ_min, le rapport entre la plus grande et la plus petite **valeur singulière** de A. Géométriquement, A envoie la sphère unité sur un ellipsoïde ; les valeurs singulières sont les longueurs de ses demi-axes, donc κ₂ mesure à quel point cet ellipsoïde est aplati. Cette leçon utilise les valeurs singulières comme une boîte noire ; leur calcul (la SVD) fera l'objet d'un module ultérieur.

**Règle empirique.** Un solveur inversement stable en binary64 donne une erreur directe relative d'environ κ(A) · u. Avec u ≈ 10^-16, on peut s'attendre à perdre environ **log₁₀ κ(A)** des quelque 16 chiffres significatifs. Quand κ(A) approche 1/u ≈ 10^16, aucun chiffre de la réponse n'est fiable. C'est une estimation tirée d'une borne supérieure, pas un théorème valable dans tous les cas.

### Exercice pratique

Calculez κ₂ de A = diag(1, 10^-8). Combien des 16 chiffres une résolution de A x = b peut-elle perdre ?

> *Solution :* Les valeurs singulières d'une matrice diagonale sont les valeurs absolues de ses coefficients diagonaux : 1 et 10^-8. Donc κ₂(A) = 1 / 10^-8 = 10^8, et une résolution peut perdre environ 8 des 16 chiffres significatifs.

---

## 5. Où IX trace la limite

IX est la bibliothèque Rust d'apprentissage automatique de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce comportement et ne le modifie pas.

- [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) utilise l'élimination de Gauss–Jordan avec pivot partiel. Elle renvoie `MathError::Singular` quand le plus grand pivot disponible a une valeur absolue inférieure à 10^-12 ([ligne 110](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110)). Ce seuil est **absolu** : il dépend de l'échelle de A, pas de κ(A).
- [`SvdResult::rank(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L67) et [`pseudo_inverse(tol)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73) ne gardent que les valeurs singulières strictement supérieures à `tol`, une tolérance absolue choisie par l'appelant. L'outil d'agent `ix_svd` en choisit une **relative**, σ₁ · 10^-10 ([`handlers.rs` ligne 639](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L639)).
- IX n'a **aucune fonction de conditionnement**. κ₂ doit être calculé comme σ_max / σ_min à partir de [`svd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L100).
- [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L68) résout les équations normales XᵀX w = Xᵀy avec `inverse(...).expect("X^T X is singular")`, si bien que tout verdict `Singular` devient une panique plutôt qu'une erreur. Former XᵀX élève aussi le conditionnement au carré : pour X de rang colonne plein, κ₂(XᵀX) = κ₂(X)², car les valeurs singulières de XᵀX sont les carrés de celles de X.

Le test de pivot, verbatim depuis `linalg.rs`, lignes 110–112 :

```rust
        if max_val < 1e-12 {
            return Err(MathError::Singular);
        }
```

### Exercice pratique

En vous servant uniquement du code ci-dessus, prédisez ce que renvoie `inverse` pour A = 10^-13 · I₂ (l'identité 2 × 2 multipliée par 10^-13) et pour A = [[1, 2], [2, 4]]. Quel verdict dit quelque chose de la matrice, et lequel seulement de son échelle ?

> *Solution :* Les deux renvoient `Singular`. Pour 10^-13 · I₂, le premier pivot vaut 10^-13 < 10^-12 en valeur absolue, donc `inverse` s'arrête, alors que κ₂ = 1 (conditionnement parfait) et que l'inverse, 10^13 · I₂, est facile à calculer. Pour [[1, 2], [2, 4]], la deuxième ligne vaut deux fois la première, donc la matrice est exactement singulière ; le test d'IX [`test_singular_matrix`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L219) vérifie ce cas. Seul le second verdict décrit la matrice. Le premier décrit son échelle, et inversement une matrice au κ énorme mais aux pivots supérieurs à 10^-12 est inversée sans le moindre avertissement.

---

## 6. Expérience : les matrices de Hilbert dans IX

La matrice de Hilbert H_n est la matrice n × n de coefficients 1 / (i + j − 1). C'est le test classique du mauvais conditionnement :
- H_n est symétrique définie positive, donc **inversible pour tout n** en arithmétique exacte.
- Son inverse exacte a des **coefficients entiers** (Choi 1983), ce qui fournit une référence exacte pour mesurer les erreurs.
- κ₂(H_n) croît comme (1 + √2)^(4n) / √n, soit environ e^(3,5n) (Todd 1954) : chaque ligne et colonne supplémentaire le multiplie par environ (1 + √2)^4 ≈ 34.
- La H_n *stockée* n'est déjà plus H_n, car des coefficients comme 1/3 sont arrondis. D'après le §4, même un algorithme parfait hérite alors d'une erreur pouvant atteindre environ κ · u.

**Protocole.** Pour n = 2 à 12, un laboratoire Learn qui épingle IX à `e35138b9` construit H_n, calcule κ₂ avec la `svd` d'IX, inverse H_n avec `inverse` et avec `pseudo_inverse`, mesure les résidus et l'erreur par rapport à l'inverse entière exacte, et consigne le premier n, s'il existe, pour lequel `inverse` renvoie `Singular`.

**Prédictions, écrites avant l'exécution :**
1. κ₂ calculé à partir de `svd` croît à peu près géométriquement en n.
2. Le nombre de chiffres corrects de l'inverse calculée diminue à peu près comme 16 − log₁₀ κ₂.
3. Tout verdict `Singular` pour H_n reflète le seuil de pivot absolu du §5, pas une vraie singularité, puisque H_n est inversible pour tout n.

<!-- MAT003-LAB-RESULTS: pending. Fill only by pasting the Learn lab output and cite its artefact hash. -->
> **Résultats mesurés en attente.** Le tableau des valeurs mesurées sera recopié de l'exécution du laboratoire Learn, avec l'empreinte de son artefact, avant publication. Aucun nombre de cette section n'est estimé à la main.

### Exercice pratique

En utilisant κ₂(H_n) ≈ e^(3,5n) et la règle empirique du §4, estimez la taille n à partir de laquelle une inverse calculée de H_n n'a plus aucun chiffre fiable.

> *Solution :* Plus aucun chiffre ne survit quand κ₂ atteint environ 1/u ≈ 10^16. Résoudre e^(3,5n) = 10^16 donne n = 16 · ln 10 / 3,5 ≈ 36,8 / 3,5 ≈ 10,5. La loi de croissance cache un facteur constant et le terme 1 / √n, donc c'est une estimation d'ordre de grandeur ; le tableau mesuré indique où cela se produit réellement.

---

## 7. Pièges courants

- **Comparer des flottants calculés avec `==`.** Comparez avec une tolérance tirée du problème, et rendez-la relative quand l'échelle varie.
- **Se fier à un petit résidu.** Un petit résidu r = b − A x̂ ne signifie pas une petite erreur : d'après le théorème du §4 avec Δb = −r, l'erreur relative peut atteindre κ(A) · ‖r‖ / ‖b‖.
- **Lire « non singulière » comme « bien conditionnée ».** Un seuil de pivot absolu, comme celui d'`inverse`, mesure l'échelle, pas le conditionnement.
- **Inverser pour résoudre.** Calculer A⁻¹ puis A⁻¹ b demande plus de travail que résoudre A x = b directement et est généralement moins précis ; former XᵀX élève κ au carré.
- **Croire les chiffres affichés.** Afficher 17 chiffres ne les rend pas corrects ; log₁₀ κ d'entre eux peuvent être du bruit.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **binary64** | Le format flottant 64 bits de la norme IEEE 754 : 53 bits significatifs, environ 16 chiffres décimaux |
| **Epsilon machine (ε)** | L'écart entre 1 et le nombre stocké suivant : 2^-52 en binary64 |
| **Unité d'arrondi (u)** | La plus grande erreur relative de l'arrondi au plus proche : u = ε/2 = 2^-53 |
| **Cancellation** | Perte de chiffres corrects lors de la soustraction de nombres presque égaux qui portent déjà des erreurs |
| **Erreur directe** | La distance entre la réponse calculée et la vraie réponse |
| **Erreur inverse** | La plus petite perturbation de l'entrée pour laquelle la réponse calculée est exacte |
| **Inversement stable** | Se dit d'un algorithme dont l'erreur inverse est toujours de l'ordre de u |
| **Conditionnement** | À quel point un problème amplifie les variations relatives de son entrée ; pour une matrice, κ(A) = ‖A‖ · ‖A⁻¹‖ |
| **Valeur singulière** | La longueur d'un demi-axe de l'image de la sphère unité par A ; κ₂(A) = σ_max / σ_min |
| **Matrice de Hilbert** | La matrice de coefficients 1 / (i + j − 1) : inversible mais extrêmement mal conditionnée |

---

## Auto-évaluation

**1. Pourquoi 0,1 n'est-il pas stocké exactement en binary64, alors que 0,75 l'est ?**
> 0,75 = 3/4 a un dénominateur puissance de deux, donc son développement binaire est fini. 0,1 = 1/10 a le facteur 5 dans son dénominateur, donc son développement binaire est infini et doit être arrondi.

**2. Un algorithme est inversement stable, mais sa réponse n'a que 4 chiffres corrects. L'algorithme est-il en cause ?**
> Pas forcément. Erreur directe ≲ conditionnement × erreur inverse. Avec une erreur inverse proche de 10^-16, 4 chiffres corrects indiquent un conditionnement proche de 10^12 : c'est le problème, pas l'algorithme, qui perd les chiffres.

**3. Énoncez et démontrez la borne qui définit κ(A) pour A x = b.**
> ‖Δx‖ / ‖x‖ ≤ ‖A‖ · ‖A⁻¹‖ · ‖Δb‖ / ‖b‖. Démonstration : Δx = A⁻¹ Δb donne ‖Δx‖ ≤ ‖A⁻¹‖ ‖Δb‖, et b = A x donne 1 / ‖x‖ ≤ ‖A‖ / ‖b‖ ; on multiplie les deux.

**4. La fonction `inverse` d'IX renvoie une matrice sans erreur. Le résultat est-il pour autant précis ?**
> Non. `inverse` ne refuse que lorsqu'un pivot passe sous le seuil absolu 10^-12. Une matrice au grand κ et aux pivots plus grands est inversée en silence, et le résultat peut perdre environ log₁₀ κ chiffres. Calculez κ₂ avec `svd` pour le savoir.

**Critères de réussite :** Expliquer la grille binary64 et le modèle standard, distinguer l'erreur directe de l'erreur inverse, démontrer la borne sur κ(A), et utiliser κ pour prédire et expliquer la perte de chiffres, y compris dans la fonction `inverse` d'IX.

---

## Bases de recherche

- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019 : le format binary64 et les opérations correctement arrondies
- D. Goldberg, « What Every Computer Scientist Should Know About Floating-Point Arithmetic », *ACM Computing Surveys* 23(1), 5–48, 1991, doi:10.1145/103162.103163
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2e éd., SIAM, 2002 : le modèle standard, les erreurs directe et inverse, et le conditionnement des systèmes linéaires
- J. Todd, 1954, National Bureau of Standards Applied Mathematics Series 39 : la croissance du conditionnement des matrices de Hilbert
- M.-D. Choi, « Tricks or Treats with the Hilbert Matrix », *American Mathematical Monthly* 90(5), 1983 : les coefficients entiers de l'inverse
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §5 renvoie à sa ligne
- Mesures : en attente du laboratoire Learn `code/streeling-mathematics/`, qui épingle IX au même commit
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.80) F(0.02) U(0.15) C(0.03)
