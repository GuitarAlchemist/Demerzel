---
module_id: mat-012-iterative-optimisation
department: mathematics
course: Optimisation itérative
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-011-gradients-reverse-mode-autodiff]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Optimisation itérative — Pas, courbure et ce que veut dire converger

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Reconnaître les fonctions convexes, L-lisses et fortement convexes, et lire L, μ et le conditionnement κ sur une hessienne
- Montrer pourquoi la descente de gradient sur une quadratique converge exactement quand 0 < η < 2/L, et choisir le pas qui minimise son taux
- Énoncer les garanties de convergence de la descente de gradient pour les fonctions non convexes, convexes et fortement convexes, et ce qu'un petit gradient prouve ou ne prouve pas
- Expliquer comment l'inertie de la boule pesante améliore le taux asymptotique de (κ − 1)/(κ + 1) à (√κ − 1)/(√κ + 1) sur une quadratique
- Expliquer les estimations de moments d'Adam et sa correction du biais, et pourquoi son pas est de l'ordre de η quelle que soit la taille du gradient
- Retracer ce que rapportent les optimiseurs d'IX, son gradient numérique et son outil MCP, et quand « convergé » ne veut pas dire convergé

---

## 1. Convexité, régularité et conditionnement

Pour minimiser une fonction différentiable f : Rⁿ → R, les méthodes itératives cherchent un point où s'annule le gradient de MAT-011. Un tel **point stationnaire** peut être un minimum, un maximum ou un point selle. La fonction est **convexe** si f(y) ≥ f(x) + ∇f(x) · (y − x) pour tous x et y : elle est au-dessus de chacun de ses plans tangents, si bien que tout point stationnaire est un minimum global. Pour une f deux fois différentiable, cela a lieu exactement quand la hessienne ∇²f(x), la matrice symétrique des dérivées partielles secondes, est semi-définie positive partout.

Deux constantes règlent la vitesse des méthodes de descente. f est **L-lisse** si son gradient est L-lipschitzien, ‖∇f(x) − ∇f(y)‖ ≤ L‖x − y‖ ; pour une f deux fois différentiable, cela signifie que toute valeur propre de toute hessienne est dans [−L, L]. f est **μ-fortement convexe**, avec μ > 0, si toute valeur propre de toute hessienne vaut au moins μ. Leur rapport κ = L/μ ≥ 1 est le **conditionnement** du problème. Le cas modèle est la quadratique f(x) = ½xᵀAx − bᵀx avec A symétrique définie positive : sa hessienne vaut A partout, donc μ et L sont la plus petite et la plus grande valeur propre de A, comme dans MAT-005, et κ est le conditionnement κ₂(A) de MAT-003.

### Exercice pratique

Soit f(x, y) = x² + 10y². Trouvez sa hessienne, μ, L et κ.

> *Solution :* ∂²f/∂x² = 2, ∂²f/∂y² = 20 et la dérivée croisée est nulle, donc la hessienne est la matrice diagonale diag(2, 20) en tout point. Ainsi μ = 2, L = 20 et κ = 10. Les lignes de niveau sont des ellipses dont les axes sont dans le rapport √10 ≈ 3,16, plus longues selon x ; en un point comme (1, 1), le gradient (2, 20) pointe surtout selon y, en travers de la vallée, plutôt que vers le minimum.

---

## 2. La descente de gradient sur une quadratique

La **descente de gradient** fait le pas x_{k+1} = x_k − η∇f(x_k), avec un **pas** ou taux d'apprentissage η > 0. Sur la quadratique du §1, ∇f(x) = Ax − b et le minimiseur est x* = A⁻¹b, donc l'erreur e_k = x_k − x* vérifie e_{k+1} = (I − ηA)e_k. Dans la base des vecteurs propres de A, chaque composante est multipliée à chaque pas par son propre facteur 1 − ηλ, où λ est la valeur propre correspondante. L'itération converge depuis tout point de départ exactement quand |1 − ηλ| < 1 pour toute valeur propre, c'est-à-dire quand **0 < η < 2/L**.

Le seuil est net. En η = 2/L, la composante selon la direction la plus raide change de signe sans diminuer ; au-delà, cette composante croît comme |1 − ηL|^k tandis que les autres peuvent encore diminuer. Le taux vaut max(|1 − ημ|, |1 − ηL|). Le pas η = 1/L donne 1 − μ/L = 1 − 1/κ, et le meilleur pas fixe, η = 2/(L + μ), équilibre les deux extrêmes et donne **(κ − 1)/(κ + 1)**. Pour κ proche de 1, la méthode est rapide ; pour κ grand, le taux approche 1 et la méthode se traîne le long des directions plates, tandis que le pas est plafonné par la direction raide.

### Exercice pratique

Pour f(x) = (L/2)x², pour quels pas la descente de gradient converge-t-elle ? Prenez L = 20 et décrivez ce qui se passe pour η = 1/20, 3/40, 1/10 et 3/20.

> *Solution :* ∇f(x) = Lx, donc x ← (1 − ηL)x, et l'itération converge exactement quand |1 − ηL| < 1, c'est-à-dire 0 < η < 2/L = 1/10. Avec L = 20 : η = 1/20 donne le facteur 0 et atteint le minimum en un pas ; η = 3/40 donne −1/2, une oscillation qui se divise par deux à chaque pas ; η = 1/10 donne −1, une oscillation entre x₀ et −x₀ qui ne diminue jamais ; η = 3/20 donne −2, une oscillation qui double à chaque pas.

---

## 3. Le lemme de descente et les vitesses de convergence

Au-delà des quadratiques, la L-régularité majore encore f par une parabole : f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖². C'est le **lemme de descente**. Avec y = x − η∇f(x), il donne f(y) ≤ f(x) − η(1 − Lη/2)‖∇f(x)‖², une décroissance garantie dès que 0 < η < 2/L, maximale en η = 1/L, où elle vaut ‖∇f(x)‖²/(2L). Sommer ces décroissances sur K pas avec η = 1/L donne trois garanties, où f* est la valeur minimale, ou la borne inférieure :

- pour toute f L-lisse minorée, le minimum pour k < K de ‖∇f(x_k)‖² est ≤ 2L(f(x₀) − f*)/K : un itéré est presque stationnaire, ce qui n'est pas la même chose que presque minimal ;
- pour une f convexe ayant un minimiseur x*, f(x_K) − f* ≤ L‖x₀ − x*‖²/(2K) ;
- pour une f μ-fortement convexe, f(x_K) − f* ≤ (1 − μ/L)^K (f(x₀) − f*), un taux linéaire.

Deux mises en garde en découlent. D'abord, L borne la courbure partout où vont les itérés. Sur une fonction non quadratique, un pas sûr près du minimum peut être bien trop grand ailleurs, et c'est la courbure locale au point courant qui décide du pas suivant (§6). Ensuite, un critère d'arrêt de la forme ‖∇f(x)‖ < tol ne certifie que la quasi-stationnarité. Seule la forte convexité en fait une borne sur la distance au minimiseur, ‖x − x*‖ ≤ ‖∇f(x)‖/μ, et aucun critère ne peut certifier un gradient mal calculé.

### Exercice pratique

Pour f(x, y) = x² + 10y² du §1, combien d'itérations réduisent la composante d'erreur la plus lente d'un facteur 10^6, avec η = 1/L et avec η = 2/(L + μ) ?

> *Solution :* Avec η = 1/L = 1/20, les facteurs sont 1 − 2/20 = 0,9 selon x et 0 selon y, donc le taux vaut 0,9 et 0,9^k < 10^-6 demande k ≥ 132. Avec η = 2/(L + μ) = 1/11, les facteurs sont 1 − 2/11 = 9/11 et 1 − 20/11 = −9/11, le taux vaut (κ − 1)/(κ + 1) = 9/11, et (9/11)^k < 10^-6 demande k ≥ 69, environ deux fois moins.

---

## 4. L'inertie

La **méthode de la boule pesante** de Polyak ajoute au pas de gradient une fraction β du pas précédent : v_{k+1} = βv_k − η∇f(x_k) et x_{k+1} = x_k + v_{k+1}, ou de façon équivalente x_{k+1} = x_k − η∇f(x_k) + β(x_k − x_{k−1}). La vitesse v s'accumule selon les directions où le gradient garde son signe et s'annule selon celles où il alterne, ce qui est exactement la vallée du §1 : une progression régulière selon l'axe plat, une oscillation amortie en travers de l'axe raide.

Sur une quadratique, le choix η = 4/(√L + √μ)² et β = ((√κ − 1)/(√κ + 1))² donne le taux asymptotique **(√κ − 1)/(√κ + 1)**. Prenons x² + 100y² depuis (1, 1), donc κ = 100. La descente de gradient avec son meilleur pas multiplie les deux coordonnées par ±99/101 ≈ ±0,980 à chaque pas et demande 691 pas pour les amener sous 10^-6. Pour la boule pesante, (9/11)^k ≈ 0,818^k suggère 69 pas, mais ce taux n'est qu'asymptotique : avec ces paramètres, la récurrence a une racine double, et avec une vitesse initiale nulle les coordonnées valent exactement (1 + 2k/11)(9/11)^k et (1 + 20k/11)(−9/11)^k. Le facteur linéaire retarde le gain, et les deux coordonnées ne passent sous 10^-6 qu'après 95 pas, soit tout de même environ sept fois moins que 691. Le gain croît avec κ, puisque le nombre d'itérations croît comme κ pour l'une et comme √κ pour l'autre. Ce taux n'est garanti que sur les quadratiques : Lessard, Recht et Packard donnent une fonction régulière et fortement convexe sur laquelle la boule pesante avec ces paramètres ne converge pas. Le gradient accéléré de Nesterov atteint un taux du même ordre, 1 − 1/√κ, avec une garantie pour toute fonction régulière et fortement convexe.

### Exercice pratique

Avec β = 0,9, vers quoi tend la vitesse quand le gradient est une constante g, comme sur une longue pente droite ?

> *Solution :* v_k = −ηg(1 + β + … + β^(k−1)), qui tend vers −ηg/(1 − β) = −10ηg. Sur une pente constante, l'inertie multiplie le pas effectif par 1/(1 − β) = 10 ; c'est son avantage sur les directions plates et son danger quand la pente change, puisque la vitesse met environ 1/(1 − β) pas à tourner.

---

## 5. Pas adaptatifs : Adam

**Adam**, de Kingma et Ba, tient deux moyennes mobiles exponentielles par coordonnée : celle du gradient, m_k = β₁m_{k−1} + (1 − β₁)g_k, et celle de son carré, v_k = β₂v_{k−1} + (1 − β₂)g_k², avec les valeurs par défaut β₁ = 0,9 et β₂ = 0,999. Il divise la première par la racine carrée de la seconde : x_{k+1} = x_k − η m̂_k/(√v̂_k + ε), coordonnée par coordonnée, avec ε = 10^-8.

Les deux moyennes partent de 0, donc elles sont d'abord biaisées vers 0 : si le gradient était constant, m_k vaudrait (1 − β₁^k) fois ce gradient. La **correction du biais** divise par ce facteur, m̂_k = m_k/(1 − β₁^k) et v̂_k = v_k/(1 − β₂^k). Au premier pas, m̂₁ = g₁ et v̂₁ = g₁², donc le pas vaut η g₁/(|g₁| + ε), environ η en taille, dans la direction opposée au signe du gradient. Plus généralement, Kingma et Ba montrent que le pas est approximativement borné par η, quelle que soit l'échelle du gradient. C'est l'inverse de la descente de gradient, dont le pas est proportionnel au gradient. Cela signifie qu'Adam ne peut pas exploser comme la descente de gradient au-delà de 2/L ; cela signifie aussi qu'il n'a ni seuil comme 2/L ni garantie générale. Près d'un minimum où le gradient change de signe, m̂ moyenne les signes jusqu'à les annuler alors que v̂ ne le fait pas, et les pas diminuent. Reddi, Kale et Kumar donnent un problème convexe simple sur lequel Adam ne converge pas, et proposent une variante corrigée, AMSGrad.

### Exercice pratique

Avec η = 0,01 et les valeurs par défaut de β₁, β₂ et ε, quel est le premier pas d'Adam pour un gradient g = 10^-6 ? Que serait-il pour un g plus grand sans correction du biais ?

> *Solution :* Le premier pas corrigé vaut η g/(|g| + ε) = 0,01 · 10^-6/(10^-6 + 10^-8) = 0,01/1,01 ≈ 0,0099 : presque η entier, alors que le gradient est minuscule. Sans correction du biais, m₁ = 0,1g et v₁ = 0,001g², et le pas vaut η · 0,1|g|/(√0,001 |g|) ≈ 3,16η quand |g| est très supérieur à ε : plus de trois fois la taille voulue, parce que √v₁ ≈ 0,0316|g| sous-estime |g| davantage que m₁ = 0,1g ne sous-estime g.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de sa boucle en Python, dont les flottants sont en binary64 IEEE comme le `f64` de Rust : ce sont des prédictions, que le §7 propose de vérifier.

**Les optimiseurs** (`crates/ix-optimize`). [`SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L21) fait le pas du §2 ; [`Momentum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L49) est la boule pesante du §4, avec une vitesse initialisée à −η∇f ; et [`Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L111) est le §5, avec les [constantes par défaut](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L77) et la [correction du biais](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L107). À moins qu'un objectif ne fournisse son propre gradient, la [valeur par défaut du trait](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L12) est [`numerical_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/calculus.rs#L7) avec ε = 10^-7, et l'enveloppe de fermeture [`ClosureObjective`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/traits.rs#L43) n'en fournit aucun. [`minimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L124) exécute la boucle ci-dessous : elle garde la meilleure valeur vue, et déclare la convergence dès que la norme du gradient qu'elle vient d'utiliser passe sous la tolérance.

```rust
    for i in 0..criteria.max_iterations {
        let grad = objective.gradient(&params);
        let new_params = optimizer.step(&params, &grad);
        let value = objective.evaluate(&new_params);

        if value < best_value {
            best_value = value;
            best_params = new_params.clone();
        }

        // Check gradient norm convergence
        let grad_norm: f64 = grad.dot(&grad).sqrt();
        if grad_norm < criteria.tolerance {
            return OptimizeResult {
                best_params,
                best_value,
                iterations: i + 1,
                converged: true,
            };
        }
```

**L'outil MCP.** `ix_optimize` appelle le gestionnaire [`optimize`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L181). L'appelant choisit une fonction parmi sphère, Rosenbrock et Rastrigin, une dimension, une méthode et un plafond d'itérations, selon son [schéma](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L20). Pour les méthodes à gradient, le gestionnaire fixe le reste : [η = 0,01 pour `SGD`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L221) et [pour `Adam`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L230), une [tolérance de 10^-8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L224) sur la norme du gradient, et un [départ à 5 dans chaque coordonnée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L226). Il renvoie le meilleur point, la meilleure valeur, le nombre d'itérations et le [drapeau `converged`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L259). Les méthodes `pso` et `annealing` n'utilisent pas de gradient et sont laissées de côté ici.

- **Une divergence est rapportée comme une convergence.** La fonction de Rosenbrock f(x, y) = 100(y − x²)² + (1 − x)² vaut f(5, 5) = 40 016 au départ, avec le gradient (40 008, −4000). Sa hessienne y a ∂²f/∂x² = 28 002 et une plus grande valeur propre proche de 28 145, donc le seuil 2/L de la courbure locale vaut environ 7,1 · 10^-5 et η = 0,01 est environ 140 fois trop grand. `SGD` envoie x en −395,08, puis vers 2,5 · 10^8, puis vers −5,5 · 10^25. Là, l'écart entre doubles voisins est 2^33 ≈ 8,6 · 10^9, donc x + 10^-7 et x − 10^-7 s'arrondissent tous deux à x ; et y, encore environ 3,1 · 10^5, se perd à côté de x² ≈ 3 · 10^51 quand y − x² est arrondi, avec ou sans 10^-7. Chaque quotient différentiel du gradient numérique vaut alors exactement 0. La boucle voit un gradient nul et renvoie `converged` vrai après 4 itérations, avec le meilleur point (5, 5), le départ, et la meilleure valeur 40 016. En dimension 3, il se passe la même chose avec la valeur 80 032.
- **Le pas est le même pour les trois fonctions.** Sur la [sphère](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L195), la somme des carrés, L = 2, donc η = 0,01 est cinquante fois plus petit que le pas 1/L = 1/2 qui atteint le minimum d'un coup. Chaque itération multiplie l'erreur par 1 − 2η = 0,98, et la transcription s'arrête après 1027, 1044 et 1054 itérations en dimensions 1, 2 et 3. Sur Rosenbrock, le même η est bien trop grand au départ.
- **Les minima de Rastrigin repoussent SGD.** La fonction de Rastrigin ajoute, par coordonnée, x² − 10 cos(2πx) + 10, dont le [terme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L211) a pour courbure 2 + 40π² cos(2πx), jusqu'à 2 + 40π² ≈ 396,8. En chacun de ses 55 minima locaux entre −27 et 27, le minimum global en 0 compris, η fois cette courbure dépasse 2, la plus petite valeur étant environ 2,07, si bien que, par le §2, chacun de ces minima repousse l'itération. Les premiers minima stables, vers ±27,8, sont loin de la région que visitent les itérés : depuis 5, la transcription reste dans |x| < 5,5 et renvoie `converged` faux après 5000 itérations. `Adam`, dont le pas n'est pas proportionnel au gradient, se pose dans le minimum local proche de 4,975, avec une valeur d'environ 24,87 par coordonnée : convergé, vers un point stationnaire qui n'est pas le minimum global 0.
- **Rosenbrock en dimension 1 est identiquement nulle.** L'objectif somme sur [`0..x.len() - 1`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L200), vide pour une seule coordonnée, et le schéma [autorise la dimension 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch2.rs#L24). Les deux méthodes rapportent alors une convergence après 1 itération, en 5, avec la valeur 0.
- **Le gradient numérique a un pas absolu.** ε = 10^-7 est environ cinquante fois sous le meilleur pas centré u^(1/3) ≈ 5 · 10^-6 de MAT-011, donc son erreur est surtout d'arrondi, de l'ordre de u|f|/ε ≈ 1,1 · 10^-9 |f| par composante, face à une tolérance de 10^-8. Et ε n'est pas mis à l'échelle de |x| : dès qu'une coordonnée dépasse 2^30 ≈ 1,07 · 10^9 en valeur absolue, x ± 10^-7 s'arrondit à x et cette composante vaut exactement 0, ce qui est le mécanisme du premier constat.
- **« SGD » est déterministe.** Le type est [documenté](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L8) comme « Stochastic Gradient Descent », mais il avance selon le gradient complet qu'on lui donne, et rien dans la boucle n'échantillonne : c'est la descente de gradient du §2.
- **Les tests ne vérifient que la valeur.** [`test_adam_rosenbrock`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L193) exécute `Adam` avec η = 0,01 depuis (0, 0) et [affirme une meilleure valeur inférieure à 0,1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L205), avec le commentaire « Adam may not converge perfectly on Rosenbrock » ; la transcription prédit une convergence à moins de 10^-7 de (1, 1), avec une meilleure valeur inférieure à 10^-15. Le test quadratique, `test_sgd_quadratic`, [n'affirme lui aussi qu'une valeur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-optimize/src/gradient.rs#L189). Aucun des deux ne vérifie `converged` ni `iterations`, les deux champs dont le premier constat montre qu'ils peuvent induire en erreur.

Le gradient numérique perturbe une coordonnée à la fois du même ε absolu :

```rust
    let n = x.len();
    let mut grad = Array1::zeros(n);
    for i in 0..n {
        let mut x_plus = x.clone();
        let mut x_minus = x.clone();
        x_plus[i] += epsilon;
        x_minus[i] -= epsilon;
        grad[i] = (f(&x_plus) - f(&x_minus)) / (2.0 * epsilon);
    }
    grad
```

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Dans le premier constat, pourquoi le gradient numérique vaut-il exactement 0 en x ≈ −5,5 · 10^25, alors que le vrai gradient y est énorme ?

> *Solution :* Vers 5,5 · 10^25, deux doubles consécutifs sont à 2^33 ≈ 8,6 · 10^9 l'un de l'autre, donc `x_plus[i] += epsilon` et `x_minus[i] -= epsilon` laissent tous deux x inchangé. Les deux évaluations de f ont alors lieu au même point, leur différence vaut exactement 0, et le quotient aussi. Pour la composante en y, les deux points diffèrent bien, mais vers x² ≈ 3 · 10^51 deux doubles consécutifs sont à 2^119 ≈ 6,6 · 10^35 l'un de l'autre, donc y + 10^-7 − x² et y − 10^-7 − x² s'arrondissent au même nombre, et f prend deux fois la même valeur. La vraie dérivée par rapport à x, de l'ordre de 400|x|³, n'intervient jamais : le quotient différentiel ne voit que les valeurs que renvoie f. Un pas mis à l'échelle de |x|, ou un gradient calculé par le mode inverse de MAT-011, ne s'annulerait pas.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Le seuil 2/L.** Minimisez f(x) = 10x², écrite `10.0 * x[0] * x[0]` dans un `ClosureObjective`, donc L = 20 et 2/L = 0,1, avec `SGD` depuis x = 1, une tolérance de 10^-8 et un plafond de 400 itérations. Prédiction : η = 0,05 converge après 2 itérations ; η = 0,09 converge après 97 ; η = 0,1 ne converge pas, et |x| reste à moins de 10^-6 de 1 ; η = 0,2 renvoie `converged` vrai après 20 itérations avec le meilleur point 1 et la meilleure valeur 10, bien que x ait crû comme 3^k.
2. **Le gestionnaire MCP, appelé dans le processus.** Appelez `optimize` avec Rosenbrock en dimensions 2 et 3, avec `sgd` et un plafond de 5000. Prédiction : `converged` vrai après 4 itérations, meilleur point 5 dans chaque coordonnée, meilleures valeurs 40 016 et 80 032. Rosenbrock en dimension 1, avec `sgd` et avec `adam` : convergence après 1 itération avec la valeur 0. Rastrigin en dimensions 1 à 3 : `sgd` non convergé après 5000 itérations ; `adam` convergé, chaque coordonnée proche de 4,975 et la valeur proche de 24,87 fois la dimension. La sphère avec `sgd` : 1027, 1044 et 1054 itérations.
3. **L'inertie.** Minimisez x² + 10y² depuis (1, 1), avec une tolérance de 10^-8 et un plafond de 2000. Prédiction : `SGD` avec η = 1/20 converge après 183 itérations et avec η = 1/11 après 108 ; `Momentum` avec η = 4/(√20 + √2)² et β = ((√10 − 1)/(√10 + 1))² après 40.
4. **Le test d'Adam, en enregistrant le résultat.** Relancez le réglage de `test_adam_rosenbrock` et enregistrez `converged`, `iterations` et le meilleur point. Prédiction : convergence après environ 1300 itérations, entre 1200 et 1400, en un point à moins de 10^-7 de (1, 1), avec une meilleure valeur inférieure à 10^-15.
5. **Le premier pas d'Adam.** Appelez `step` une fois sur un `Adam::new(0.01)` neuf au point 0 avec le gradient 10^-6, et une fois sur un autre avec le gradient 10^6. Prédiction : des pas de −0,01/1,01 et de −0,01, chacun à 10^-12 près.

### Exercice pratique

Prédisez le nombre d'itérations pour η = 0,09 à l'étape 1, en prenant le gradient numérique pour exact.

> *Solution :* Le facteur vaut 1 − 0,09 · 20 = −0,8, donc après i pas |x| = 0,8^i et le gradient que vérifie la boucle vaut 20 · 0,8^i. Il passe sous 10^-8 quand 0,8^i < 5 · 10^-10, c'est-à-dire i > ln(2 · 10^9)/ln(1,25) ≈ 95,98, donc pour la première fois en i = 96 ; la boucle compte à partir de 0 et rapporte i + 1 = 97 itérations. La marge en i = 96 est inférieure à 1 %, bien plus grande que l'erreur d'arrondi relative du gradient numérique.

---

## 8. Pièges courants

- **Un seul taux d'apprentissage pour tous les problèmes.** Le pas sûr est fixé par la courbure, 2/L ; un η fixe peut être plus de cent fois trop grand pour une fonction et cinquante fois trop petit pour une autre.
- **Lire « convergé » comme « minimisé ».** Une petite norme du gradient ne certifie que la quasi-stationnarité : un point selle, un minimum local ou un gradient calculé comme nul passent tous le test.
- **Un pas de différences finies absolu.** Un pas de 10^-7 disparaît dans l'arrondi dès que |x| dépasse 2^30 ; mettez-le à l'échelle de x, ou utilisez la différentiation automatique.
- **Ignorer la direction raide.** Sur un problème mal conditionné, la direction la plus raide plafonne le pas et la plus plate fixe l'allure ; le nombre d'itérations croît comme κ.
- **L'inertie sans garantie.** Le taux de la boule pesante est prouvé pour les quadratiques ; sur d'autres fonctions, elle peut osciller ou ne pas converger là où la méthode de Nesterov convergerait.
- **Traiter le pas d'Adam comme un pas de gradient.** Sa taille vaut environ η quel que soit le gradient, donc η fixe une distance par pas, pas une fraction de la pente.
- **Ne tester que la valeur.** Un test qui borne la meilleure valeur mais pas `converged` ni `iterations` passe même quand la boucle rapporte une fausse convergence.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Point stationnaire** | Un point où le gradient s'annule : un minimum, un maximum ou un point selle |
| **Fonction convexe** | Une fonction au-dessus de chacun de ses plans tangents ; tout point stationnaire est un minimum global |
| **L-lisse** | Qui a un gradient L-lipschitzien ; les valeurs propres de la hessienne sont dans [−L, L] |
| **Fortement convexe** | Dont toute valeur propre de la hessienne vaut au moins μ > 0 |
| **Conditionnement** | κ = L/μ, le rapport de la courbure la plus raide à la plus plate |
| **Pas** | Le facteur η qui multiplie le gradient dans un pas de descente, aussi appelé taux d'apprentissage |
| **Lemme de descente** | f(y) ≤ f(x) + ∇f(x) · (y − x) + (L/2)‖y − x‖² pour une f L-lisse |
| **Inertie de la boule pesante** | La descente de gradient plus une fraction β du pas précédent |
| **Correction du biais** | La division des moyennes mobiles d'Adam par 1 − β^k pour annuler leur départ en 0 |
| **Adam** | Une méthode qui divise une moyenne des gradients par la racine d'une moyenne de leurs carrés, coordonnée par coordonnée |
| **Critère d'arrêt sur la norme du gradient** | S'arrêter quand ‖∇f‖ passe sous une tolérance, un test de quasi-stationnarité seulement |

---

## Auto-évaluation

**1. Une quadratique a μ = 2 et L = 50. Pour quels pas la descente de gradient converge-t-elle, et quel pas fixe minimise son taux ?**
> Elle converge exactement pour 0 < η < 2/L = 0,04 ; la borne elle-même échoue, puisqu'en η = 0,04 la composante la plus raide ne fait que changer de signe. Le meilleur pas fixe est 2/(L + μ) = 2/52 ≈ 0,038, avec le taux (κ − 1)/(κ + 1) = 24/26 ≈ 0,92 pour κ = 25.

**2. Une exécution s'arrête avec ‖∇f‖ < 10^-8. Que savez-vous du point qu'elle renvoie ?**
> Que le dernier gradient calculé par la boucle était petit. Si f est μ-fortement convexe et que ce gradient était exact, le point est à moins de 10^-8/μ du minimiseur ; sinon, ce peut être un point selle, un minimum local ou, comme dans le cas Rosenbrock d'IX, un point où le gradient numérique s'est arrondi à zéro. Dans IX, le point renvoyé est en outre le meilleur vu, qui n'est pas forcément le point où le gradient était petit.

**3. Pourquoi l'inertie de la boule pesante aide-t-elle sur x² + 100y², et où s'arrête sa garantie ?**
> Avec κ = 100, la boule pesante bien réglée a le taux asymptotique 9/11 au lieu de 99/101, parce que la vitesse s'accumule selon la direction plate et s'annule en travers de la raide. Depuis (1, 1) avec une vitesse initiale nulle, elle amène les deux coordonnées sous 10^-6 en 95 pas au lieu de 691 ; l'estimation asymptotique, 69, néglige un facteur transitoire qui croît linéairement avec k. Le taux n'est prouvé que pour les quadratiques ; Lessard, Recht et Packard donnent une fonction fortement convexe sur laquelle elle échoue, alors que la méthode de Nesterov garde un taux d'ordre 1 − 1/√κ sur toute fonction régulière et fortement convexe.

**4. `ix_optimize` renvoie `converged` vrai après 4 itérations pour Rosenbrock. Pouvez-vous lui faire confiance ?**
> Pas sur la foi de ce drapeau seul. Comparez le meilleur point au départ et regardez la meilleure valeur : ici, ce sont (5, 5) et 40 016, les valeurs de départ, ce qui veut dire qu'aucune itération n'a amélioré le départ. Le gradient s'est annulé parce que les itérés sont devenus si grands que le pas numérique s'est perdu dans l'arrondi, non parce qu'ils ont atteint le minimum en (1, 1).

**Critères de réussite :** Lire μ, L et κ sur une hessienne, établir le seuil 2/L et le meilleur pas fixe sur une quadratique, énoncer les garanties de la descente de gradient et ce que prouve un petit gradient, expliquer les taux de l'inertie de la boule pesante et le pas d'Adam, et retracer quand la boucle d'IX rapporte une convergence qui n'a pas eu lieu.

---

## Bases de recherche

- H. H. Rosenbrock, « An automatic method for finding the greatest or least value of a function », *The Computer Journal* 3, 1960 : la vallée en forme de banane utilisée comme fonction de test
- B. T. Polyak, « Some methods of speeding up the convergence of iteration methods », *USSR Computational Mathematics and Mathematical Physics* 4, 1964 : la méthode de la boule pesante et son taux sur les quadratiques
- Y. Nesterov, « A method of solving a convex programming problem with convergence rate O(1/k²) », *Soviet Mathematics Doklady* 27, 1983 : les méthodes de gradient accéléré
- S. Boyd et L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004 : convexité, forte convexité et convergence de la descente de gradient
- J. Nocedal et S. J. Wright, *Numerical Optimization*, 2e éd., Springer, 2006 : pas, recherches linéaires et gradients par différences finies
- D. P. Kingma et J. Ba, « Adam: A method for stochastic optimization », *International Conference on Learning Representations*, 2015 : Adam, sa correction du biais et la borne sur son pas
- L. Lessard, B. Recht et A. Packard, « Analysis and design of optimization algorithms via integral quadratic constraints », *SIAM Journal on Optimization* 26, 2016 : une fonction fortement convexe sur laquelle la boule pesante ne converge pas
- S. J. Reddi, S. Kale et S. Kumar, « On the convergence of Adam and beyond », *International Conference on Learning Representations*, 2018 : un problème convexe sur lequel Adam échoue, et AMSGrad
- Y. Nesterov, *Lectures on Convex Optimization*, 2e éd., Springer, 2018 : le lemme de descente et les vitesses de convergence du §3
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
