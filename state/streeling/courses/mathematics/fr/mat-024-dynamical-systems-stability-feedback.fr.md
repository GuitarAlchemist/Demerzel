---
module_id: mat-024-dynamical-systems-stability-feedback
department: mathematics
course: Systèmes dynamiques, stabilité et rétroaction
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Systèmes dynamiques, stabilité et rétroaction — Ce que peuvent dire une dérivée, un exposant et un rang

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Trouver les points fixes et les cycles d'une application, décider de leur stabilité à partir d'un multiplicateur, et dire quand la linéarisation ne décide rien
- Calculer un exposant de Lyapunov comme la moyenne de log|f′| le long d'une orbite, et dire ce que son signe dit et ne dit pas de l'attracteur
- Localiser les bifurcations de doublement de période, en estimer le δ de Feigenbaum, et expliquer pourquoi un balayage à tolérance fixe les place mal
- Stabiliser un point fixe instable par le contrôle OGY, et dire quand le contrôleur agit linéairement, sature, ou n'est pas nécessaire du tout
- Dériver le filtre de Kalman scalaire et son régime permanent, et expliquer pourquoi la forme de Joseph garde une covariance honnête là où la forme courte ne le fait pas
- Décider de la commandabilité et de l'observabilité par le critère du rang de Kalman, et lire la marge et la tolérance dont dépend un rang numérique
- Retracer ce que calculent les crates `ix-chaos` et `ix-signal` d'IX, lesquelles de leurs sorties un test fixe, et ce qu'elles laissent de côté

---

## 1. Points fixes et linéarisation

Un système dynamique discret itère une application : x_(k+1) = f(x_k). Un **point fixe** x* vérifie f(x*) = x*. Posons x_k = x* + e_k ; un développement de Taylor donne e_(k+1) = f′(x*) e_k + O(e_k²), si bien que près de x* l'erreur est multipliée à chaque pas par le **multiplicateur** f′(x*). Si |f′(x*)| < 1, le point fixe est asymptotiquement stable : les petites erreurs diminuent d'environ ce facteur à chaque pas, et quand le multiplicateur est négatif, elles alternent de signe. Si |f′(x*)| > 1, il est instable. Si |f′(x*)| = 1, la linéarisation ne décide rien, et ce sont les termes d'ordre supérieur qui tranchent. Si f′(x*) = 0, le point fixe est **superstable** : l'erreur est élevée au carré à chaque pas.

L'**application logistique** f(x) = r x (1 − x), avec 0 ≤ r ≤ 4, envoie [0, 1] dans lui-même. Pour r > 1, elle a un point fixe x* = 1 − 1/r en plus de 0, et comme f′(x) = r(1 − 2x), le multiplicateur y vaut f′(x*) = 2 − r. À r = 2,5, x* = 0,6 et le multiplicateur vaut −0,5 : les erreurs sont divisées par deux et alternent. À r = 2, x* = 1/2 est superstable. À r = 3,2, le multiplicateur vaut −1,2, et x* repousse.

Un **cycle** de période p est un point fixe de l'itérée p-ième f^p, et par la dérivation des fonctions composées, son multiplicateur est le produit de f′ le long du cycle. Pour l'application logistique, le cycle de période 2 existe pour r > 3, et son multiplicateur vaut 4 + 2r − r². Il est stable tant que |4 + 2r − r²| < 1, c'est-à-dire pour 3 < r < 1 + √6 ≈ 3,449490. Il est superstable à r = 1 + √5 ≈ 3,236068, où le cycle passe par x = 1/2. Il naît à r = 3, où le multiplicateur du point fixe passe par −1, et il perd sa stabilité là où son propre multiplicateur atteint −1.

En n dimensions, x_(k+1) = F(x_k) se linéarise avec la jacobienne J de F au point fixe, et le point fixe est stable quand toutes les valeurs propres de J sont de module inférieur à 1, c'est-à-dire quand le **rayon spectral** ρ(J) est inférieur à 1 (MAT-005). Pour un système linéaire x_(k+1) = A x_k, ρ(A) < 1 est nécessaire et suffisant pour que x_k → 0 depuis tout point de départ. Cela n'empêche pas une croissance transitoire. A = [[0.5, 10], [0, 0.5]] a ρ(A) = 0,5, mais depuis x_0 = (0, 1), la première composante de x_k vaut 10k · 0,5^(k−1) : 10 au premier et au deuxième pas, 7,5 au troisième, et moins de 1 seulement à partir du huitième. Les valeurs propres fixent le long terme ; pour une A non normale, la norme, ici d'environ 10,02, borne le court terme. CYB-002 décrit en mots l'amortissement des oscillations entre dépôts ; le multiplicateur en est la forme quantitative.

### Exercice pratique

À quelle valeur de r le point fixe x* = 1 − 1/r de l'application logistique perd-il sa stabilité ?

> *Solution :* Le multiplicateur est f′(x*) = 2 − r, et |2 − r| < 1 est vrai pour 1 < r < 3. À r = 3, le multiplicateur atteint −1 et le cycle de période 2 naît. À r = 3 même, la linéarisation ne décide rien : l'orbite s'approche encore de x*, mais si lentement que l'exposant du §2, moyenné sur 10 000 pas, vaut −0,000359.

---

## 2. Exposants de Lyapunov

Deux orbites d'une application unidimensionnelle qui partent à δ_0 l'une de l'autre sont, après n pas, écartées d'environ |δ_0| fois le produit des |f′(x_i)| le long de l'orbite. L'**exposant de Lyapunov** est le taux de croissance moyen par pas :

```
λ = lim (1/n) Σ_{i<n} ln|f′(x_i)|
```

Si λ < 0, les orbites voisines convergent : l'orbite est attirée par un point fixe ou un cycle stable. Si λ > 0, les orbites voisines s'écartent exponentiellement tout en restant bornées, ce qui est la signature du chaos. λ = 0 marque un comportement marginal, comme un point de bifurcation ou un mouvement quasi périodique. En un point fixe stable, les termes ln|f′(x_i)| tendent vers ln|f′(x*)|, et leur moyenne aussi, donc λ = ln|f′(x*)|. Sur un cycle stable de période p, λ est ln|multiplicateur| divisé par p. Si l'orbite passe exactement par un point où f′ = 0, le logarithme vaut −∞, et λ aussi.

Pour l'application logistique, en partant de x_0 = 0,1, en écartant 1 000 pas et en moyennant les 10 000 suivants :

| r | 2,5 | 2,9 | 3,0 | 3,2 | 3,5 | 3,7 | 3,8 | 3,83 | 4,0 |
|---|---|---|---|---|---|---|---|---|---|
| λ | −0,693147 | −0,105361 | −0,000359 | −0,916291 | −0,872507 | 0,350235 | 0,428314 | −0,369511 | 0,693135 |
| Attracteur | point fixe | point fixe | point fixe, marginal | cycle de période 2 | cycle de période 4 | chaotique | chaotique | cycle de période 3 | chaotique |

La théorie se vérifie. À r = 2,5, λ = ln 0,5 = −0,693147, et à r = 2,9, λ = ln 0,9 = −0,105361. Sur le cycle de période 2 à r = 3,2, le multiplicateur vaut 4 + 6,4 − 10,24 = 0,16, et λ = (1/2) ln 0,16 = ln 0,4 = −0,916291. À r = 4, la valeur exacte est ln 2 = 0,693147, et l'exécution s'en approche à 0,000012 près. La valeur r = 3,83 se trouve dans la fenêtre de période 3 qui s'ouvre à 1 + √8 ≈ 3,828427, au sein de la plage chaotique : un exposant négatif n'y est pas une erreur. À r = 2 et r = 1 + √5, l'orbite tombe sur x = 1/2 et λ = −∞.

Le signe dit si les orbites voisines convergent, pas vers quoi elles convergent : un point fixe, un cycle de période 2 et un cycle de période 3 donnent tous λ < 0. Pour les distinguer, on compte la période (§3).

Pour un système en n dimensions, il y a n exposants. Benettin et ses collègues les calculent en faisant évoluer n vecteurs tangents avec la jacobienne le long de l'orbite, en les réorthonormalisant par une décomposition QR à chaque pas, et en moyennant les logarithmes de la diagonale de R. Pour un flot, qu'il faut intégrer en temps, le schéma d'intégration des vecteurs tangents entre dans le résultat (§7).

### Exercice pratique

Calculez λ à r = 2,9 sans itérer, et expliquez pourquoi le même raisonnement donne λ = (1/2) ln|4 + 2r − r²| sur le cycle de période 2.

> *Solution :* L'orbite converge vers x* = 1 − 1/2,9, où f′(x*) = 2 − 2,9 = −0,9, donc les termes de la moyenne tendent vers ln 0,9 et λ = ln 0,9 = −0,105361. Sur le cycle de période 2, les termes alternent entre ln|f′(p)| et ln|f′(q)|, dont la somme est le logarithme du multiplicateur |f′(p) f′(q)| = |4 + 2r − r²|, si bien que chaque pas en apporte la moitié en moyenne.

---

## 3. Doublement de période et constante de Feigenbaum

Quand r dépasse r_1 = 3, le point fixe cède la place à un cycle stable de période 2, qui cède la place à r_2 = 1 + √6 à un cycle stable de période 4, puis de période 8, et ainsi de suite : à r_k, le multiplicateur du cycle de période 2^(k−1) passe par −1. Résoudre cette condition par la méthode de Newton, avec 40 chiffres significatifs, donne :

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| r_k | 3 | 3,449489743 | 3,54409036 | 3,564407266 | 3,56875942 | 3,56969161 |

Les écarts diminuent géométriquement. Les rapports δ_k = (r_(k+1) − r_k) / (r_(k+2) − r_(k+1)) valent 4,7514 ; 4,6563 ; 4,6682 et 4,6687, et ils convergent vers la **constante de Feigenbaum** δ = 4,669201…, la même pour toute application lisse à une bosse avec un maximum quadratique (Feigenbaum, 1978). La cascade s'accumule en r_∞ ≈ 3,569946, valeur que donne l'extrapolation des écarts avec δ. Au-delà de r_∞, le chaos alterne avec des fenêtres périodiques, comme la fenêtre de période 3 du §2.

Trouver ces points à partir des orbites est plus difficile qu'il n'y paraît. Un test numérique de période itère au-delà d'un transitoire et renvoie le premier p pour lequel x_(k+p) revient à une tolérance près de x_k. Près de r_k, le multiplicateur du cycle est proche de −1, si bien que l'orbite s'approche lentement du cycle, et après un transitoire fixe, elle en est encore trop loin pour une tolérance fixe. Un balayage en r voit donc un doublement là où la convergence se trouve passer le test, ce qui peut arriver avant ou après le vrai r_k (§7).

### Exercice pratique

Prédisez r_6 à partir de r_3, r_4 et r_5 avec δ ≈ 4,669, et comparez avec le tableau.

> *Solution :* r_6 ≈ r_5 + (r_5 − r_4)/4,669 = 3,56875942 + 0,00435215/4,669 ≈ 3,569692. Le tableau donne 3,56969161 : la loi géométrique tient déjà à environ une partie sur dix millions de r.

---

## 4. Contrôler le chaos : OGY et Pyragas

Un attracteur chaotique contient une infinité d'orbites périodiques instables, parmi lesquelles le point fixe x*. Ott, Grebogi et Yorke (1990) ont proposé d'en stabiliser une par de petites modifications d'un paramètre. Linéarisons à la fois en l'état et en le paramètre : x_(k+1) − x* ≈ f_x (x_k − x*) + f_r (r_k − r_0), où f_x et f_r sont les dérivées partielles en (x*, r_0). La perturbation

```
δr_k = −(f_x / f_r) (x_k − x*)
```

annule le terme linéaire, si bien que l'écart suivant est du second ordre. Comme la perturbation doit rester petite, elle est bornée à |δr| ≤ δr_max, et le contrôleur n'agit linéairement qu'à l'intérieur de la fenêtre |x − x*| ≤ δr_max |f_r| / |f_x|. Hors de la fenêtre, il sature, et c'est l'orbite chaotique elle-même qui finit par amener l'état dans la fenêtre.

Pour l'application logistique à r_0 = 3,8 : x* = 0,736842 ; f_x = 2 − r_0 = −1,8 ; f_r = x*(1 − x*) = 0,193906 ; et avec δr_max = 0,1, la fenêtre a une demi-largeur de 0,010773. En partant de x_0 = 0,5 avec un contrôle à partir du pas 50, la perturbation sature aux pas 50 à 55. Au pas 56, l'écart vaut 1,0407e-2, à l'intérieur de la fenêtre, et les suivants valent 8,7741e-4 ; 6,3042e-6 ; 3,2578e-10 et 2,2204e-16. Chacun vaut environ 8,2 fois le carré du précédent, et le rapport tend vers 8,1971 : une fois le terme linéaire annulé, ce sont les termes quadratiques −r_0 e² + (1 − 2x*) e δr qui restent.

Pyragas (1992) a proposé pour les flots un contrôle qui ne demande aucun modèle : ajouter K (x(t − τ) − x(t)) à la dynamique, où τ est la période de l'orbite à stabiliser. Sur cette orbite, le terme s'annule, si bien que le contrôle ne coûte rien une fois qu'il a réussi ; τ doit correspondre à la période.

### Exercice pratique

Avec δr_max = 0,05 au lieu de 0,1, quelle est la demi-largeur de la fenêtre, et qu'est-ce qui change ?

> *Solution :* 0,05 × 0,193906 / 1,8 ≈ 0,005386, deux fois plus étroite. L'orbite chaotique entre moins souvent dans une fenêtre plus étroite, si bien que l'attente avant la capture est en moyenne plus longue. Une fois l'orbite à l'intérieur, la convergence est la même, puisque le terme linéaire est annulé quel que soit δr_max.

---

## 5. Le filtre de Kalman comme estimation linéaire optimale

Un modèle linéaire a un état caché x_k = F x_(k−1) + w_k, observé sous la forme z_k = H x_k + v_k, avec des bruits indépendants w ~ N(0, Q) et v ~ N(0, R). Le **filtre de Kalman** alterne deux étapes :

```
predict:  x⁻ = F x            P⁻ = F P Fᵀ + Q
update:   S = H P⁻ Hᵀ + R     K = P⁻ Hᵀ S⁻¹
          x = x⁻ + K (z − H x⁻)
          P = (I − K H) P⁻
```

Le gain K minimise la variance de l'erreur a posteriori parmi toutes les mises à jour linéaires, et avec un bruit gaussien, l'estimation est l'espérance conditionnelle de l'état sachant les mesures (Kalman, 1960).

Dans le cas scalaire F = H = 1, une constante mesurée avec du bruit, prenons Q = 0,01 et R = 1. En régime permanent, P⁻ = P + Q et P = P⁻ R / (P⁻ + R), donc P⁻² − Q P⁻ − Q R = 0 et P⁻ = (Q + √(Q² + 4QR)) / 2 = 0,105125. Le gain permanent est K = P⁻ / (P⁻ + R) = 0,095125, et la variance a posteriori est P = K R = 0,095125. Chaque nouvelle mesure reçoit alors un poids de 0,095, soit un oubli exponentiel sur environ 1/K ≈ 10,5 mesures. En partant de x = 0 avec P = 1, les mesures 5,2 ; 4,8 ; 5,1 ; 4,9 ; 5,0 ; 5,3 ; 4,7 ; 5,1 ; 4,9 et 5,0, dont la moyenne est 5,0, donnent les estimations 2,6129 ; 3,3540 ; 3,8055 ; 4,0373 ; 4,2120 ; 4,3869 ; 4,4325 ; 4,5225 ; 4,5703 et 4,6219, tandis que le gain descend de 0,5025 à 0,1201. Après dix mesures, l'estimation est encore à 0,3781 de 5 : l'a priori x = 0 pèse encore.

La mise à jour P = (I − KH) P⁻ n'est juste que pour le gain optimal. La **forme de Joseph** P = (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ vaut pour tout gain et reste symétrique et semi-définie positive en virgule flottante. Avec P⁻ = 1 et R = 1, le gain optimal 0,5 donne P = 0,5 des deux façons. Avec un gain de 0,8, imposé ou dégradé par les arrondis, la vraie variance a posteriori est 0,2² × 1 + 0,8² × 1 = 0,68, mais la forme courte annonce 0,2 : elle sous-estime l'incertitude de plus d'un facteur trois.

### Exercice pratique

Avec Q = 0,04 et R = 1, trouvez P⁻ et K en régime permanent. Le filtre suit-il maintenant les changements plus vite ou plus lentement ?

> *Solution :* P⁻ = (0,04 + √(0,0016 + 0,16)) / 2 ≈ 0,220998, et K = 0,220998 / 1,220998 ≈ 0,180998. Le gain est presque deux fois plus grand : le filtre fait moins confiance au modèle, suit les changements plus vite, et laisse passer davantage de bruit de mesure dans son estimation.

---

## 6. Commandabilité et observabilité

Un système linéaire invariant dans le temps x_(k+1) = A x_k + B u_k, y_k = C x_k, à n états, est **commandable** quand l'entrée peut amener n'importe quel état à n'importe quel autre en un nombre fini de pas, et **observable** quand les sorties déterminent l'état initial. Après n pas depuis x_0 = 0, les états atteignables forment l'espace engendré par les colonnes de la **matrice de commandabilité** [B, AB, …, A^(n−1) B]. D'après le théorème de Cayley–Hamilton, A^n est une combinaison de I, A, …, A^(n−1), si bien que les puissances suivantes n'ajoutent rien, et le système est commandable exactement quand cette matrice est de rang n (Kalman). De même, il est observable exactement quand la **matrice d'observabilité** [C; CA; …; C A^(n−1)] est de rang n. Les deux notions sont duales : (A, C) est observable exactement quand (Aᵀ, Cᵀ) est commandable. Le critère de Hautus désigne le coupable : (A, B) est commandable exactement quand [A − λI, B] est de rang n pour toute valeur propre λ de A. Pour une A diagonale à valeurs propres distinctes, le mode i est commandable exactement quand la ligne i de B est non nulle, et observable exactement quand la colonne i de C est non nulle.

Le double intégrateur discret A = [[1, 1], [0, 1]], B = [0; 1], C = [1, 0] a [B, AB] = [[0, 1], [1, 1]] et [C; CA] = [[1, 0], [1, 1]], toutes deux de rang 2, de valeurs singulières φ = 1,618034 et 1/φ = 0,618034. Le système modal A = diag(1, 2, 3), B = [1; 1; 0], C = [1, 1, 0] a [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [0, 0, 0]], de rang 2, de valeurs singulières 4,838 ; 0,7735 et 0 : son troisième mode n'est ni atteignable ni visible, et [A − 3I, B] est de rang 2.

Un ordinateur décide du rang en comptant les valeurs singulières au-dessus d'une tolérance. La convention de LAPACK et de NumPy prend max(lignes, colonnes) × σ_max × ε, avec ε = 2^(−52) : 3,22e-15 pour le système modal. Un changement de base x → Tx, avec T = [[1, 2, 0], [0, 1, 1], [1, 0, 2]] (det T = 4), transforme (A, B, C) en (TAT⁻¹, TB, CT⁻¹), où il ne reste plus aucun zéro à lire. Les rangs ne changent pas : la matrice de commandabilité transformée a pour valeurs singulières 11,76 et 0,7791, et une troisième qui vaut 0 en arithmétique exacte et un résidu d'arrondi de l'ordre de 1e-16 en virgule flottante, face à une tolérance de 7,84e-15.

La plus petite valeur singulière, la **marge**, est la distance en norme 2 à la matrice de rang inférieur la plus proche (Eckart–Young, MAT-006). Avec A = diag(1, 1 + 1e-10) et C = [1, 1], la matrice d'observabilité a des valeurs singulières d'environ 2 et 5e-11 : le système est observable, mais avec deux modes que la sortie ne peut pratiquement pas distinguer. Avec A = diag(1, 3), elles valent 3,414214 et 0,585786.

Les puissances de A dégradent aussi le calcul. Pour A = diag(1, 2, …, n) et B une colonne de uns, la matrice de commandabilité est une matrice de Vandermonde, et les matrices de Vandermonde sont notoirement mal conditionnées (Gautschi, 1975). Avec des valeurs singulières calculées à 60 chiffres et la tolérance ci-dessus, n = 12 donne σ_max = 8,057e11 ; σ_min = 1,139e-4 et une tolérance de 2,147e-3, d'où un rang 11, pour un système qui est commandable : ses valeurs propres sont distinctes et B touche chaque mode. Mettre A à l'échelle par 1/12 ramène σ_max à 5,143, la tolérance à 1,37e-14, et le rang à 12. La mise à l'échelle aide sans guérir : à la même échelle, n = 20 a σ_min = 1,541e-16 face à une tolérance de 3,009e-14, et un rang 18. Les algorithmes en escalier de Paige et de Van Dooren (1981) réduisent (A, B) par des transformations orthogonales et ne forment jamais les puissances.

### Exercice pratique

Dans le système modal, remplacez B par [1; 1; 1]. Est-il commandable maintenant ? Et observable ?

> *Solution :* Commandable : B touche chaque mode et les valeurs propres sont distinctes, et [B, AB, A²B] = [[1, 1, 1], [1, 2, 4], [1, 3, 9]] est une matrice de Vandermonde de déterminant (2 − 1)(3 − 1)(3 − 2) = 2. Toujours pas observable : C = [1, 1, 0] manque le troisième mode, et la matrice d'observabilité garde le rang 2.

---

## 7. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python de `lyapunov.rs`, `bifurcation.rs` et `control.rs` dans `crates/ix-chaos`, et de `kalman.rs` et `state_space.rs` dans `crates/ix-signal`. La transcription reproduit les assertions des tests que cite cette section. Elle ne couvre pas `bifurcation_diagram`, `drive_response_sync`, le filtre à vitesse constante, ni les tests de construction et de simulation du modèle d'état. Ces nombres sont des prédictions, et le §8 propose de les vérifier.

**L'exposant d'une application, et le nom qu'on lui donne.** [`mle_1d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L8) moyenne ln|f′| le long de l'orbite après un transitoire, et [renvoie −∞](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L23) au premier |f′| inférieur à 1e-15. L'outil MCP `ix_chaos_lyapunov` est le gestionnaire [`chaos_lyapunov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1436), qui l'exécute sur l'application logistique [depuis x_0 = 0,1 avec un transitoire de 1 000](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1449) et nomme le résultat avec [un seuil de 0,01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1450), par [`classify_dynamics`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L160) :

```rust
pub fn classify_dynamics(mle: f64, threshold: f64) -> DynamicsType {
    if mle > threshold {
        if mle > 10.0 {
            DynamicsType::Divergent
        } else {
            DynamicsType::Chaotic
        }
    } else if mle > -threshold {
        DynamicsType::Periodic
    } else {
        DynamicsType::FixedPoint
    }
}
```

La documentation de l'énumération décrit [`FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L150) comme une convergence vers un point fixe et [`Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L152) comme une orbite quasi périodique ou un cycle limite, ce qui correspond à la lecture des exposants d'un flot. Pour une application, le §2 montre que tout cycle stable a λ < 0. L'outil nomme donc `FixedPoint` le cycle de période 2 à r = 3,2, le cycle de période 4 à r = 3,5 et le cycle de période 3 à r = 3,83. Il nomme `Periodic` la valeur r = 3, où le point fixe est sur le point de perdre sa stabilité et où aucun cycle n'existe encore. Les tests de métriques de boucle d'IX fixent eux-mêmes deux conséquences de plus : un exposant NaN échoue à toutes les comparaisons et [retombe sur `FixedPoint`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L279), et une [boucle bloquée est `Periodic`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/tests/loop_metrics.rs#L256). Les tests de `mle_1d` vérifient que [r = 4 donne ln 2 à 0,05 près](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L179), là où la transcription est à 0,000012 près, et que [r = 3,2 donne une valeur négative](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L195).

**Le spectre : RK4 pour l'état, Euler pour les tangentes.** [`lyapunov_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L43) intègre l'état avec [un pas de Runge–Kutta d'ordre quatre](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L65), mais déplace les vecteurs tangents par [un pas d'Euler, avec la jacobienne prise en l'état déjà mis à jour](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L92), puis les réorthonormalise par [Gram–Schmidt modifié](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/lyapunov.rs#L106). Pour le flot linéaire ẋ = a x, l'exposant exact est a, mais un pas d'Euler multiplie un vecteur tangent par 1 + a dt, si bien que la fonction renvoie ln|1 + a dt| / dt. Avec dt = 0,01, cela donne −1,005034 pour a = −1 et 0,995033 pour a = +1 : un biais d'environ a² dt / 2 que davantage de pas n'éliminent pas. La fonction n'a pas de test, et rien dans l'espace de travail ne l'appelle ; seuls les guides de théorie du chaos d'IX la montrent dans des exemples.

**Détection de période à tolérance fixe.** [`detect_period`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L61) compare les itérés après le transitoire avec [le premier d'entre eux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L77). Son test vérifie [les périodes 1 et 2 à r = 2,5 et 3,2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L159) ; avec les réglages du test, la transcription trouve aussi 4 à r = 3,5, 8 à 3,55, 16 à 3,566, 3 à 3,83, et aucune période à 3,8. [`find_period_doublings`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L92) balaie r uniformément, détecte la période [avec une tolérance de 1e-8 et au plus 64](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L108), et enregistre r partout où la période est le double de celle du point précédent ; [un point sans période réinitialise la comparaison](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L110). Sur [2,9 ; 3,57] depuis x_0 = 0,5, la transcription donne :

| Points de balayage | Transitoire | Doublements signalés | Rapports qui en découlent |
|---|---|---|---|
| 68 | 1 000 | 3,55 | aucun |
| 68 | 10 000 | 3,45 ; 3,55 | aucun |
| 671 | 1 000 | 2,985 ; 3,444 ; 3,542 ; 3,569 | 4,684 ; 3,63 |
| 671 | 10 000 | 2,999 ; 3,449 ; 3,565 ; 3,569 | 3,879 ; 29,0 |

Le premier doublement est à r = 3, et pourtant la troisième ligne signale 2,985, où le point fixe est encore stable. Le multiplicateur y vaut −0,985, et après 1 000 pas, l'orbite est encore à environ 1e-8 de x*. Un pas plus tard, elle se trouve de l'autre côté, à environ 1,99e-8 de l'itéré de départ, ce qui échoue à la tolérance ; deux pas plus tard, elle en est à 2,99e-10, ce qui passe, si bien que le balayage voit une période 2. Aucune des lignes ne s'approche de δ. [`feigenbaum_delta`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L124) ne fait que prendre les rapports. Son [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/bifurcation.rs#L170) lui fournit quatre points codés en dur, dont il tire 4,7515 et 4,6578, et affirme seulement que le premier rapport est compris entre 3 et 6. `find_period_doublings` n'a pas de test.

**OGY : le test passe sans contrôle.** [`ogy_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L17) calcule la perturbation du §4 et [la borne](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L42). Son [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L154) est l'exécution du §4, et il affirme que le dernier état est [à moins de 0,1 de x*](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L176). La transcription se verrouille à 2,2e-16 près à partir du pas 60. Sans aucun contrôle, l'état au pas 199 est à 0,0892 de x*, ce qui passe aussi. Depuis x_0 = 0,3 ; 0,6 et 0,9, les distances sans contrôle valent 0,0876 ; 0,1653 et 0,1481. Sur 10 000 points de départ tirés uniformément (`random` de Python, graine 0), 28,28 % finissent à moins de 0,1 sans aucun contrôle, et tous se verrouillent à 1e-12 près avec lui. La tolérance du test ne peut pas distinguer le contrôle du hasard.

**Pyragas : un retard trop court d'un pas.** [`pyragas_control`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L57) garde les états retardés dans un tampon circulaire qui commence par [`delay_steps` copies de x_0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-chaos/src/control.rs#L68) :

```rust
    for step in 0..steps {
        trajectory.push(x.clone());

        let mut dx = dynamics(&x);

        // Apply Pyragas control after startup
        if step >= control_start && step >= delay_steps {
            let delayed = &history[step % delay_steps];
            for i in 0..n {
                dx[i] += gain * (delayed[i] - x[i]);
            }
        }

        // Euler integration (simple for demonstration)
        for i in 0..n {
            x[i] += dt * dx[i];
        }

        history[step % delay_steps] = x.clone();
    }
```

Au pas k, il lit la case k mod d, que le pas k − d a écrite après sa mise à jour, avec l'état x_(k−d+1). Le terme de contrôle utilise donc x(t − (d − 1) dt), et non x(t − d dt). Avec `delay_steps` = 1, il lit l'état courant et le terme de contrôle est nul, quel que soit le gain. Avec 0, le premier calcul de reste provoque une panique : à la ligne 78 si le contrôle commence au pas 0, à la ligne 89 sinon. L'exemple du guide d'IX passe [628 pas pour une période de 2π à dt = 0,01](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/chaos-theory/chaos-control.md#L112), si bien que le retard effectif est de 627 pas. La fonction n'a pas de test.

**Kalman : la forme courte, et un garde-fou construit autour de sa panique.** [`KalmanFilter::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L36) fixe [H = 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L39), Q = 0,01 I, R = I et P = I, et les contrats du crate disent que ces [valeurs par défaut ne forment pas un filtre utilisable](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L12). [`update`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L65) inverse S [avec `expect("Innovation covariance singular")`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L76) et met à jour P par [la forme courte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L82). Le [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L134) est l'exécution scalaire du §5, et il affirme que la dernière estimation est [à moins de 0,5 de 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/kalman.rs#L161) ; la transcription finit à 4,6219, à 0,3781 de distance. Les gestionnaires MCP refusent un bruit de mesure inférieur à [1e-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L956). Leur documentation explique que ce plancher empêche la panique, note que la mise à jour [« utilise `P = (I − KH)P`, pas la forme de Joseph »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L937), et consigne [un tableau mesuré](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L940) dans lequel q = r = 1e-13 provoque une panique à partir de quatre échantillons.

**Tests de rang avec une marge et une tolérance.** [`StateSpaceModel`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L121) construit les matrices de [commandabilité](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L265) et d'[observabilité](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L282) avec n blocs, ce que ses commentaires justifient par Cayley–Hamilton. [`rank_report`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L372) utilise [la tolérance du §6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L396) et renvoie la [plus petite valeur singulière comme marge](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L400). Les tests fixent les exemples du §6 : le [double intégrateur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L232), le [troisième mode obscur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L241), le [même système après le changement de base](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L257), et les [deux marges](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L391). Un filtre dont la matrice de commande n'a jamais été fixée [donne le rang 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L475). Le commentaire sur le changement de base du test indique [det = −3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/tests/state_space.rs#L53) ; le déterminant vaut 4, ce qui ne nuit pas, puisque toute matrice inversible convient. La documentation du module avertit que pour un grand rayon spectral, [le rang peut être sous-estimé](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L66) et qu'aucun algorithme en escalier n'est implémenté. Le §6 montre l'effet dès n = 12, avec les valeurs propres 1 à 12. Le modèle d'état n'est pas exposé par MCP.

**Ce qui manque.** Rien dans `ix-signal` ni dans `ix-chaos` ne teste la stabilité par le rayon spectral. Le seul champ nommé `spectral_radius` dans l'espace de travail, dans un [réseau à réservoir](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L12), [remet les poids à l'échelle par leur plus grand coefficient en valeur absolue](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/memristive-markov/src/reservoir.rs#L34), ce qui n'est pas le rayon spectral. Il n'y a ni équation de Lyapunov, ni LQR, ni régulateur PID. La matrice des lacunes d'IX distingue les [deux Lyapunov](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L171) : l'exposant, qu'IX possède, et la fonction de Lyapunov, un certificat de stabilité obtenu en résolvant AᵀPA − P = −Q, qu'il [prévoit](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/research/tars-v1-advanced-math-ix-gap-matrix.md#L314).

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon ne fait que le décrire.

### Exercice pratique

L'outil `ix_chaos_lyapunov` répond `FixedPoint` pour l'application logistique à r = 3,5. Quel est l'attracteur, et comment le découvririez-vous avec IX ?

> *Solution :* Un cycle stable de période 4. Son exposant, −0,872507, est inférieur à −0,01, d'où le nom, qui dit seulement que les orbites voisines convergent. `detect_period` avec les réglages du test renvoie 4.

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Un balayage de λ(r).** Exécuter `mle_1d` sur l'application logistique pour r de 2,5 à 4,0 par pas de 0,001, depuis x_0 = 0,1 avec 10 000 itérations après un transitoire de 1 000, et nommer chaque valeur avec `classify_dynamics` à 0,01. Prédiction : aux r du tableau du §2, ses valeurs à six décimales. `Chaotic` à 3,7 ; 3,8 et 4,0. `FixedPoint` à 3,2 ; 3,5 et 3,83. `Periodic` à 3,0.
2. **Le balayage des doublements.** Exécuter `find_period_doublings` sur [2,9 ; 3,57] depuis x_0 = 0,5 avec les quatre réglages du §7. Prédiction : les quatre lignes de son tableau, y compris le doublement à 2,985.
3. **OGY avec et sans contrôle.** Exécuter le test d'IX tel qu'il est écrit, puis avec `control_start` = 200, de sorte que le contrôle ne commence jamais. Prédiction : une distance finale de 2,2e-16 avec contrôle, de 0,0892 sans ; les deux passent la tolérance de 0,1 du test.
4. **Le retard de Pyragas.** Exécuter `pyragas_control` sur un oscillateur bidimensionnel avec `delay_steps` = 1, une fois avec un gain de 0 et une fois avec un gain de 5. Puis l'exécuter avec `delay_steps` = 0. Prédiction : les deux exécutions avec un retard de 1 donnent la même trajectoire bit pour bit ; un retard de 0 provoque une panique.
5. **Le filtre scalaire.** Exécuter le filtre du test, puis le même filtre sur 200 mesures valant 0. Prédiction : les dix estimations du §5 à quatre décimales ; après 200 pas, un gain et une covariance de 0,095125.
6. **Le rang sous les puissances.** Construire A = diag(1, …, n) avec B une colonne de uns, et exécuter `controllability` pour n = 12, puis avec A mise à l'échelle par 1/12, et pour n = 14 mise à l'échelle par 1/14. Prédiction : les rangs 11, 12 et 14. Les valeurs singulières les plus proches de la tolérance en sont éloignées d'un facteur 3 ou plus, si bien qu'une SVD en virgule flottante ne devrait pas changer ces rangs. Le n = 20 du §6 est laissé de côté : l'une de ses valeurs singulières se trouve à moins d'un facteur 2,5 sous la tolérance.

### Exercice pratique

L'étape 3 prédit que le test passe avec et sans contrôle. Quel test séparerait les deux ?

> *Solution :* Un test qui affirme ce que seul le contrôle obtient. Par exemple : une distance finale inférieure à 1e-12, que l'exécution contrôlée atteint dès le pas 60 et que l'exécution sans contrôle n'atteint pas ; ou la capture depuis de nombreux points de départ. Avec contrôle, les 10 000 départs aléatoires se verrouillent tous à 1e-12 près, tandis que sans lui, 28,28 % finissent à moins de 0,1 par hasard.

---

## 9. Pièges courants

- **Lire un exposant négatif comme un point fixe.** Tout cycle stable d'une application a λ < 0 ; la période doit être comptée à part.
- **Lire « Periodic » comme « un cycle ».** Pour une application, un exposant proche de zéro marque un comportement marginal, comme un point de bifurcation, pas un cycle stable.
- **Se fier à la linéarisation en |f′(x*)| = 1.** Là, les termes d'ordre supérieur décident, et la convergence, s'il y en a une, est lente.
- **Prendre ρ(A) < 1 pour « ne croît jamais ».** Une A non normale peut amplifier un état de nombreuses fois avant qu'il ne décroisse.
- **Localiser les bifurcations avec une seule tolérance et un seul transitoire.** Près d'une bifurcation, la convergence est la plus lente, et c'est donc là qu'un test fixe se trompe.
- **Accepter un test de contrôle qui passe sans contrôle.** Une tolérance plus lâche que la dispersion sans contrôle ne prouve rien.
- **Utiliser la mise à jour courte de la covariance avec un gain non optimal.** Seule la forme de Joseph reste correcte pour tout gain.
- **Lire un rang plein comme « bien commandable » ou « bien observable ».** La marge dit à quelle distance le système est de perdre la propriété ; mettez le système à l'échelle avant de comparer des marges.
- **Former de hautes puissances de A.** Les matrices de Kalman héritent du conditionnement des puissances de A ; les réductions orthogonales en escalier les évitent.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Point fixe** | Un état x* tel que f(x*) = x* |
| **Multiplicateur** | f′(x*) en un point fixe, ou le produit de f′ le long d'un cycle ; la stabilité exige un module inférieur à 1 |
| **Superstable** | Un point fixe ou un cycle de multiplicateur 0, où les erreurs sont élevées au carré à chaque pas |
| **Rayon spectral** | Le plus grand module d'une valeur propre ; ρ(A) < 1 fait converger x_(k+1) = A x_k vers 0 |
| **Exposant de Lyapunov** | La moyenne de ln\|f′\| le long d'une orbite : le taux exponentiel auquel les orbites voisines s'écartent |
| **Bifurcation de doublement de période** | Une valeur du paramètre où le multiplicateur d'un cycle passe par −1 et où naît un cycle de période double |
| **Constante de Feigenbaum** | δ = 4,669201…, la limite des rapports des écarts successifs entre doublements |
| **Contrôle OGY** | De petites modifications d'un paramètre qui annulent l'écart linéaire à un point fixe instable |
| **Filtre de Kalman** | L'estimateur linéaire récursif qui minimise la variance de l'erreur a posteriori |
| **Forme de Joseph** | La mise à jour de la covariance (I − KH) P⁻ (I − KH)ᵀ + K R Kᵀ, valable pour tout gain |
| **Commandabilité, observabilité** | L'entrée peut amener n'importe quel état à n'importe quel autre ; les sorties déterminent l'état initial |
| **Critère du rang de Kalman** | La commandabilité et l'observabilité valent exactement quand les matrices [B, …, A^(n−1) B] et [C; …; C A^(n−1)] sont de rang n |
| **Marge** | La plus petite valeur singulière d'une matrice de test : sa distance à une matrice de rang inférieur |

---

## Auto-évaluation

**1. Un outil indique λ = −0,37 et « FixedPoint » pour une application unidimensionnelle. Que savez-vous de l'attracteur ?**
> Que les orbites voisines convergent, donc que l'attracteur est stable : un point fixe ou un cycle stable de période quelconque. À r = 3,83, l'application logistique donne exactement cette réponse pour un cycle de période 3. La période doit être comptée à part.

**2. Pourquoi OGY converge-t-il quadratiquement une fois qu'il a capturé l'orbite, et pourquoi a-t-il besoin d'une fenêtre ?**
> La perturbation annule le terme linéaire de l'écart, si bien que ce qui reste est du second ordre. La fenêtre vient de la borne sur la perturbation : ce n'est qu'à l'intérieur de |x − x*| ≤ δr_max |f_r| / |f_x| que le contrôleur peut annuler exactement le terme linéaire, et hors de celle-ci, il attend que l'orbite chaotique amène l'état à l'intérieur.

**3. Un filtre utilise la mise à jour P = (I − KH) P⁻ avec un gain que les arrondis ont éloigné de l'optimum. Qu'est-ce qui ne va pas ?**
> La forme courte ne vaut que pour le gain optimal. Avec tout autre gain, elle donne une covariance fausse ; avec P⁻ = 1, R = 1 et K = 0,8, elle annonce 0,2 au lieu des 0,68 réels, si bien que le filtre devient trop confiant. La forme de Joseph donne 0,68 pour tout gain.

**4. Le système A = diag(1, …, 12), avec B une colonne de uns, est commandable, et pourtant un test de rang indique 11. Le test a-t-il tort ?**
> En arithmétique exacte, le rang est 12, puisque les valeurs propres sont distinctes et que B touche chaque mode. Mais la matrice de commandabilité est une matrice de Vandermonde avec σ_max ≈ 8,1e11 et σ_min ≈ 1,1e-4. La plus petite valeur singulière est inférieure à la tolérance relative de 2,1e-3, si bien que numériquement, la matrice ne peut pas être distinguée d'une matrice de rang 11. Mettre A à l'échelle par 1/12 rétablit le rang 12 ; un algorithme en escalier évite complètement les puissances.

**Critères de réussite :** Décider de la stabilité d'un point fixe ou d'un cycle à partir de son multiplicateur ; calculer un exposant de Lyapunov et dire ce que son signe ne dit pas ; estimer le δ de Feigenbaum à partir de points de bifurcation et expliquer pourquoi un balayage les place mal ; calculer la fenêtre d'OGY et expliquer la convergence quadratique ; dériver le régime permanent du filtre de Kalman scalaire et expliquer la forme de Joseph ; décider de la commandabilité et de l'observabilité par le critère du rang, et lire la marge et la tolérance ; et dire lesquelles des sorties d'IX ses tests fixent.

---

## Bases de recherche

- S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2e édition, Westview Press, 2015 : points fixes, linéarisation, application logistique et bifurcations
- R. M. May, « Simple mathematical models with very complicated dynamics », *Nature* 261, 1976 : l'application logistique
- M. J. Feigenbaum, « Quantitative universality for a class of nonlinear transformations », *Journal of Statistical Physics* 19, 1978 : la constante δ
- G. Benettin, L. Galgani, A. Giorgilli et J.-M. Strelcyn, « Lyapunov characteristic exponents for smooth dynamical systems and for Hamiltonian systems », *Meccanica* 15, 1980 : le spectre par orthonormalisation répétée
- E. Ott, C. Grebogi et J. A. Yorke, « Controlling chaos », *Physical Review Letters* 64, 1990 : le contrôle OGY
- K. Pyragas, « Continuous control of chaos by self-controlling feedback », *Physics Letters A* 170, 1992 : le contrôle par rétroaction retardée
- R. E. Kalman, « A new approach to linear filtering and prediction problems », *Journal of Basic Engineering* 82, 1960 : le filtre de Kalman
- R. E. Kalman, « On the general theory of control systems », *Proceedings of the First IFAC Congress*, 1960 : commandabilité, observabilité et dualité
- R. S. Bucy et P. D. Joseph, *Filtering for Stochastic Processes with Applications to Guidance*, Interscience, 1968 : la forme de Joseph
- M. L. J. Hautus, « Controllability and observability conditions of linear autonomous systems », *Indagationes Mathematicae* 31, 1969 : le critère par les valeurs propres
- C. C. Paige, « Properties of numerical algorithms related to computing controllability », *IEEE Transactions on Automatic Control* 26, 1981, et P. Van Dooren, « The generalized eigenstructure problem in linear system theory », même volume : pourquoi il ne faut pas former les puissances de A, et la réduction en escalier
- W. Gautschi, « Norm estimates for inverses of Vandermonde matrices », *Numerische Mathematik* 23, 1975 : le conditionnement des matrices de Vandermonde
- C. Eckart et G. Young, « The approximation of one matrix by another of lower rank », *Psychometrika* 1, 1936 : la marge comme distance
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §7 renvoie à sa ligne
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
