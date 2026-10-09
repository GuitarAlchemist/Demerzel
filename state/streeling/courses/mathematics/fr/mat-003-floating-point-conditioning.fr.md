---
module_id: mat-003-floating-point-conditioning
department: mathematics
course: Arithmétique flottante et conditionnement
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Arithmétique flottante et conditionnement — Quand un ordinateur perd des chiffres

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Expliquer pourquoi la plupart des nombres réels, dont 0,1, ne peuvent pas être stockés exactement dans un ordinateur
- Énoncer le modèle standard de l'arrondi flottant et le sens de l'epsilon machine
- Distinguer l'erreur directe de l'erreur inverse, et un problème mal conditionné d'un algorithme instable
- Démontrer la borne qui définit le conditionnement d'un système linéaire
- Estimer à partir de κ(A) combien de chiffres un calcul peut perdre, et trouver où IX trace cette limite dans son code

---

## 1. Les nombres qu'un ordinateur peut stocker

Un ordinateur ne stocke pas les nombres réels. Il en stocke un ensemble **fini**. Le format courant, **binary64** de la norme IEEE 754 (`f64` en Rust, `double` en C), code un nombre sur 64 bits : 1 bit de signe, 11 bits d'exposant et 52 bits de fraction. Avec le 1 de tête implicite, chaque nombre stocké **normal** porte **53 bits significatifs**, soit environ 16 chiffres décimaux. Les minuscules nombres **sous-normaux** proches de zéro renoncent à ce 1 de tête et en ont moins.

Les nombres stockés ne sont pas régulièrement espacés. Entre 1 et 2, ils sont distants de 2^-52 ; entre 2 et 4, deux fois plus ; et ainsi de suite. Deux quantités décrivent cette grille :
- L'**epsilon machine** ε = 2^-52 ≈ 2,2 × 10^-16 est l'écart entre 1 et le nombre stocké suivant.
- L'**unité d'arrondi** u = ε/2 = 2^-53 ≈ 1,1 × 10^-16 est la plus grande erreur relative commise quand un réel du **domaine normal** est arrondi au nombre stocké le plus proche. En dessous, parmi les sous-normaux, l'erreur relative peut être bien plus grande : 2^-1075 est arrondi à 0, soit une erreur relative de 1.

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
- La H_n *stockée* n'est déjà plus H_n, car des coefficients comme 1/3 sont arrondis : fl(H_n) = H_n + ΔH avec ‖ΔH‖ ≤ u‖H_n‖ en norme ∞. Le §4 borne les perturbations de b, pas de A. Pour A, le résultat classique est le suivant : si κ(A) · δ < 1 avec δ = ‖ΔA‖ / ‖A‖, alors ‖(A + ΔA)⁻¹ − A⁻¹‖ / ‖A⁻¹‖ ≤ κ(A)δ / (1 − κ(A)δ) (Higham 2002). Même une inversion parfaite de fl(H_n) a donc une erreur relative pouvant atteindre environ κ · u tant que κ · u est petit, et non bornée dès que κ · u ≥ 1, où la matrice arrondie peut même être singulière.
- Pour une matrice symétrique A, κ∞(A) / n ≤ κ₂(A) ≤ κ∞(A), où κ∞ utilise la norme du maximum des sommes de lignes. Cette **bande** est un théorème sur les normes d'**une seule et même** matrice.

**Protocole.** Le laboratoire Learn [`code/streeling-mathematics`](https://github.com/spareilleux/learn/tree/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics) épingle IX à `e35138b9`. Ses prédictions ont été écrites et hachées avant toute compilation ([`preregistration.md`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/preregistration.md), SHA-256 `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20`). Pour n = 2 à 16, il construit fl(H_n) et les mêmes matrices multipliées par 2^-20 et 2^20. Multiplier par une puissance de deux est exact en virgule flottante binaire : cela change l'échelle, pas le conditionnement. Pour chaque matrice, il consigne :
- `kappa_inf` : κ∞ de la H_n exacte, à partir de l'inverse entière exacte ; `kappa_2` : σ₁ / σ_n selon la `svd` d'IX appliquée à la fl(H_n) stockée ; `band` : si `kappa_2` est entre `kappa_inf` / n et `kappa_inf`. **Correction :** ces deux colonnes décrivent deux matrices différentes, donc `band` est une comparaison mixte, pas le théorème ci-dessus ;
- `inverse` : la réponse d'IX, `ok` ou `Singular` ; `fwd_err` : son erreur directe ‖X − H_n⁻¹‖∞ / ‖H_n⁻¹‖∞ par rapport à l'inverse exacte ; `residual` : ‖H_n X − I‖∞ ;
- `rank` : le rang à la tolérance de `ix_svd`, σ₁ · 10^-10 ; `pinv_res` : le résidu de ce `pseudo_inverse` tronqué ; `pinv0_fwd` : l'erreur directe de `pseudo_inverse(0.0)`.

**Mesuré** sous Windows 11 x86-64 (rustc 1.94.0), recopié de [`expected/mat003_conditioning.txt`](https://github.com/spareilleux/learn/blob/c8135fa508fcb9d35593e8dedbb925c44282b3a2/code/streeling-mathematics/expected/mat003_conditioning.txt) (SHA-256 `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`) :

```text
 n  kappa_inf  kappa_2    band  inverse   fwd_err   residual  rank  pinv_res  pinv0_fwd
 2  2.70e1     1.93e1     ok    ok        2.96e-16  0.00e0       2  4.44e-16  4.44e-16
 3  7.48e2     5.24e2     ok    ok        5.97e-15  1.51e-14     3  3.02e-14  5.64e-15
 4  2.84e4     1.55e4     ok    ok        5.55e-14  5.19e-13     4  1.28e-12  1.59e-13
 5  9.44e5     4.77e5     ok    ok        7.26e-13  1.14e-11     5  3.84e-11  4.79e-12
 6  2.91e7     1.50e7     ok    ok        8.89e-11  9.57e-10     6  7.61e-10  1.62e-10
 7  9.85e8     4.75e8     ok    ok        3.02e-9   5.51e-8      7  1.01e-8   2.22e-9
 8  3.39e10    1.53e10    ok    ok        4.82e-9   1.04e-6      7  1.39e0    5.78e-8
 9  1.10e12    4.93e11    ok    ok        3.05e-6   2.54e-4      8  1.36e0    2.55e-4
10  3.54e13    2.10e12    out   ok        1.10e-4   9.91e-3      8  1.47e0    1.00e0
11  1.23e15    2.72e12    out   Singular  -         -            8  1.66e0    1.00e0
12  4.12e16    1.51e12    out   Singular  -         -            9  1.52e0    1.00e0
13  1.32e18    4.31e12    out   Singular  -         -            9  1.83e0    1.00e0
14  4.54e19    7.66e13    out   Singular  -         -           11  3.62e0    1.00e0
15  1.54e21    1.26e14    out   Singular  -         -            9  1.90e0    1.00e0
16  5.06e22    9.71e14    out   Singular  -         -            9  1.98e0    1.00e0
```

```text
Refusal boundary, by scale (the true kappa does not change with scale)
  scale 1      first Singular: 11             worst accepted fwd_err: 1.10e-4 at n = 10
  scale 2^-20  first Singular: 6              worst accepted fwd_err: 7.26e-13 at n = 5
  scale 2^20   first Singular: none up to 16  worst accepted fwd_err: 1.04e0 at n = 14
  scale 1 verdicts: 2:ok 3:ok 4:ok 5:ok 6:ok 7:ok 8:ok 9:ok 10:ok 11:S 12:S 13:S 14:S 15:S 16:S

Scaling by 2^k is exact in binary floating point; is the answer?
  inverse(2^k H) == inverse(H) / 2^k bit for bit: 13 of 13 accepted pairs
  IX kappa_2 bit-identical at the three scales: 5 of 15

Controls
  I * 2^-40: kappa = 1, inverse Singular
  I * 2^-39: kappa = 1, inverse ok, inverse == I * 2^39: true
  [[1,2],[2,4]]: inverse Singular, rank(sigma_1 * 1e-10) = 1
  exact H_3^-1 = [[9, -36, 30], [-36, 192, -180], [30, -180, 180]], H_3 * H_3^-1 == I exactly: Some(true)
  checker on a wrong inverse (I for H_3^-1): residual 1.42e0
```

**Prédictions préenregistrées et verdicts :**

| Prédiction | Mesuré | Verdict |
|---|---|---|
| `inverse(H_n)` renvoie `Singular` pour la première fois à n = 11 | premier `Singular` à n = 11, puis pour tout n jusqu'à 16 | confirmée |
| Le refus suit l'échelle, pas le conditionnement | I · 2^-40 (κ = 1) refusée, I · 2^-39 acceptée ; 2^-20 · H_n refusée dès n = 6 ; 2^20 · H_n jamais refusée jusqu'à n = 16, avec une erreur directe de 1.04e0 à n = 14 | confirmée |
| Toute inverse acceptée a une erreur directe ≤ n · κ∞ · u | vérifié ; la pire est 1.10e-4, à n = 10 | confirmée |
| `inverse(2^k H_n)` = `inverse(H_n)` / 2^k, bit à bit | 13 paires acceptées sur 13 | confirmée |
| `rank(σ₁ · 10^-10)` passe sous n pour la première fois à n = 8 | rang 7 à n = 8 ; le résidu tronqué vaut au moins 1.36 à partir de là | confirmée |
| Le κ₂ d'IX reste dans la bande jusqu'à n = 11 | dans la bande pour n = 2 à 9 seulement ; sous κ∞ / n dès n = 10 | **réfutée** telle que préenregistrée, mais la bande mélange H_n et fl(H_n) : voir la correction ci-dessous |
| Le κ₂ d'IX est identique bit à bit aux trois échelles | 5 tailles sur 15 | **réfutée** |

**Ce que montre l'exécution :**
- La frontière `Singular` est fixée par le seuil de pivot absolu, pas par la matrice. Les mêmes matrices, seulement remises à l'échelle, sont refusées dès n = 6 ou jamais refusées. À l'échelle 2^20, `inverse` répond à n = 14 avec une erreur directe de 1.04e0 — aucun chiffre correct — sans signaler d'erreur.
- **Correction.** Une version antérieure de cette leçon lisait les sorties de bande comme la preuve que la `svd` d'IX renvoie un κ₂ faux. Une revue a fait remarquer que la bande compare κ∞ de la H_n exacte au κ₂ qu'IX calcule pour la fl(H_n) stockée, alors que le théorème ne relie que les normes d'une même matrice. Pour une H_n mal conditionnée, arrondir les coefficients peut changer nettement le conditionnement. Le fait que `kappa_2` passe sous `kappa_inf` / n dès n = 10 est donc une **observation** : la valeur rapportée n'est pas κ₂(H_n), mais l'exécution ne permet pas de dire quelle part de l'écart vient de l'arrondi de l'entrée et quelle part de la SVD. Trancher demanderait une référence pour la même matrice stockée, comme le κ de fl(H_n) calculé en précision supérieure, que ce laboratoire n'a pas. La colonne `rank` n'est plus monotone non plus (11 à n = 14, puis 9 à n = 15), ce qui n'est aussi qu'une observation.
- Le κ₂ d'IX change sous une remise à l'échelle exacte pour toutes les tailles sauf 5 sur 15. La cause **n'est pas identifiée** ; elle reste une reproduction ouverte pour IX, ni expliquée ni corrigée ici.
- `pseudo_inverse(0.0)`, qui garde toutes les valeurs singulières, a une erreur directe de 1.00e0 dès n = 10 : aucun chiffre correct non plus.
- La règle empirique du §4 reste de la théorie, pas une loi mesurée : les erreurs mesurées restent sous n · κ∞ · u, et à n = 10 (κ∞ = 3.54e13) l'erreur vaut 1.10e-4.

**Plateformes.** Les nombres ont été mesurés sur une seule machine. La CI hébergée a ensuite relancé le laboratoire sous Linux x86-64, Windows x86-64 et macOS arm64 (rustc 1.98.1 ; [PR Learn n° 24](https://github.com/spareilleux/learn/pull/24), [exécution 36335008098](https://github.com/spareilleux/learn/actions/runs/36335008098)) et a reproduit cette sortie octet pour octet, y compris un condensat des bits bruts de chaque valeur calculée (`0ffcce71a1dffe45`). Une sortie identique montre que le calcul est **reproductible** sur ces plateformes. Elle ne montre pas qu'il est **correct** : la justesse demande une référence indépendante pour le même problème, comme l'inverse exacte derrière `fwd_err`, et une sortie identique signifie seulement que chaque plateforme commet exactement les mêmes erreurs.

### Exercice pratique

En utilisant κ₂(H_n) ≈ e^(3,5n) et la règle empirique du §4, estimez la taille n à partir de laquelle une inverse calculée de H_n n'a plus aucun chiffre fiable.

> *Solution :* Plus aucun chiffre ne survit quand κ₂ atteint environ 1/u ≈ 10^16. Résoudre e^(3,5n) = 10^16 donne n = 16 · ln 10 / 3,5 ≈ 36,8 / 3,5 ≈ 10,5. La loi de croissance cache un facteur constant et le terme 1 / √n, donc ce n'est qu'un ordre de grandeur. Dans le tableau mesuré, κ∞ dépasse 10^16 pour la première fois à n = 12 (4.12e16), avec le vrai κ₂ entre κ∞ / n et κ∞ ; `inverse` répond encore à n = 10 avec une erreur directe de 1.10e-4 et refuse dès n = 11.

---

## 7. Pièges courants

- **Comparer des flottants calculés avec `==`.** Comparez avec une tolérance tirée du problème, et rendez-la relative quand l'échelle varie.
- **Se fier à un petit résidu.** Un petit résidu r = b − A x̂ ne signifie pas une petite erreur : d'après le théorème du §4 avec Δb = −r, l'erreur relative peut atteindre κ(A) · ‖r‖ / ‖b‖.
- **Se fier à un conditionnement calculé proche de 1/u.** κ se calcule lui aussi en virgule flottante, à partir d'une entrée arrondie : au §6, le κ₂ qu'IX rapporte pour la fl(H_n) stockée passe sous la borne inférieure de la H_n exacte dès n = 10. Ce n'est donc pas le conditionnement du problème visé, quelle que soit la part de l'arrondi et de la SVD dans l'écart.
- **Lire « non singulière » comme « bien conditionnée ».** Un seuil de pivot absolu, comme celui d'`inverse`, mesure l'échelle, pas le conditionnement.
- **Inverser pour résoudre.** Calculer A⁻¹ puis A⁻¹ b demande plus de travail que résoudre A x = b directement et est généralement moins précis ; former XᵀX élève κ au carré.
- **Croire les chiffres affichés.** Afficher 17 chiffres ne les rend pas corrects ; log₁₀ κ d'entre eux peuvent être du bruit.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **binary64** | Le format flottant 64 bits de la norme IEEE 754 : 53 bits significatifs pour les nombres normaux, environ 16 chiffres décimaux |
| **Epsilon machine (ε)** | L'écart entre 1 et le nombre stocké suivant : 2^-52 en binary64 |
| **Unité d'arrondi (u)** | La plus grande erreur relative de l'arrondi au plus proche dans le domaine normal : u = ε/2 = 2^-53 |
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
> Non. `inverse` ne refuse que lorsqu'un pivot passe sous le seuil absolu 10^-12. Une matrice au grand κ et aux pivots plus grands est inversée en silence, et le résultat peut perdre environ log₁₀ κ chiffres. Un κ₂ calculé avec la `svd` d'IX n'est qu'un diagnostic, pas une preuve de précision : près de 1/u, cette estimation peut elle-même être peu fiable (§6). Vérifiez avec une référence indépendante, comme une inverse exacte connue ou une estimation du conditionnement validée indépendamment, avant de vous fier aux chiffres.

**Critères de réussite :** Expliquer la grille binary64 et le modèle standard, distinguer l'erreur directe de l'erreur inverse, démontrer la borne sur κ(A), et utiliser κ pour prédire et expliquer la perte de chiffres, y compris dans la fonction `inverse` d'IX.

---

## Bases de recherche

- IEEE Computer Society, *IEEE Standard for Floating-Point Arithmetic*, IEEE Std 754-2019 : le format binary64 et les opérations correctement arrondies
- D. Goldberg, « What Every Computer Scientist Should Know About Floating-Point Arithmetic », *ACM Computing Surveys* 23(1), 5–48, 1991, doi:10.1145/103162.103163
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2e éd., SIAM, 2002 : le modèle standard, les erreurs directe et inverse, et le conditionnement des systèmes linéaires
- J. Todd, 1954, National Bureau of Standards Applied Mathematics Series 39 : la croissance du conditionnement des matrices de Hilbert
- M.-D. Choi, « Tricks or Treats with the Hilbert Matrix », *American Mathematical Monthly* 90(5), 1983 : les coefficients entiers de l'inverse
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §5 renvoie à sa ligne
- Mesures : laboratoire Learn `code/streeling-mathematics/` au commit `c8135fa508fcb9d35593e8dedbb925c44282b3a2` (PR Learn n° 24), qui épingle IX au même commit ; SHA-256 de la sortie attendue `6d2a9590b9a37577dd1c4b670d23dbfca55a8fef529e590a246ffa33c675bedb`, SHA-256 du préenregistrement `a70179d8a698f835aec724181066823368f0b38f76fe8dcb994494495e412f20` ; mesuré sous Windows 11 x86-64 (rustc 1.94.0), sortie reproduite par la CI hébergée sous Linux, Windows et macOS (exécution 36335008098)
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
