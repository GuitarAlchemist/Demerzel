---
module_id: mat-025-allocation-games-bandits-penalties
department: mathematics
course: Allocation sous contraintes, jeux, bandits et pénalités
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-009-estimation-uncertainty-sampling, mat-012-iterative-optimisation]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Allocation sous contraintes, jeux, bandits et pénalités — Ce que peuvent promettre un multiplicateur, un équilibre et une borne de regret

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Écrire les conditions KKT d'une allocation sous contraintes, en résoudre une petite, et lire chaque multiplicateur comme un prix implicite
- Énoncer la dualité de la programmation linéaire et la complémentarité des écarts, et résoudre à la main un programme à deux variables et son dual
- Trouver les équilibres de Nash d'un petit jeu bimatriciel par énumération des supports, et dire ce que le jeu fictif garantit et ne garantit pas
- Calculer la valeur de Shapley d'un jeu coopératif, tester une répartition contre le cœur, et expliquer pourquoi les deux peuvent diverger
- Définir le regret, comparer ε-glouton et UCB1, et dire ce que la borne d'UCB1 suppose sur l'échelle des récompenses
- Transformer une contrainte en pénalité pour une recherche qui ne connaît que des bornes de boîte, et dire quand la pénalité est exacte
- Retracer ce que calculent les crates `ix-game`, `ix-rl` et `ix-evolution` d'IX, lesquelles de leurs sorties un test fixe, et ce qu'elles laissent de côté

---

## 1. Multiplicateurs de Lagrange et conditions KKT

Une allocation choisit x pour maximiser un rendement f(x) sous des contraintes g_i(x) ≤ c_i. Quand f est concave, que chaque g_i est convexe et qu'un point satisfait strictement toutes les contraintes (**condition de Slater**), x* est optimal exactement quand il existe des multiplicateurs λ_i tels que :

```
∇f(x*) = Σ_i λ_i ∇g_i(x*)
g_i(x*) ≤ c_i
λ_i ≥ 0
λ_i (c_i − g_i(x*)) = 0
```

Ce sont les **conditions de Karush–Kuhn–Tucker** (Karush, 1939 ; Kuhn et Tucker, 1951) : stationnarité, réalisabilité primale, réalisabilité duale et complémentarité des écarts. La complémentarité des écarts dit qu'une contrainte non saturée a un multiplicateur nul. Un multiplicateur est aussi un prix : si V(c) est la valeur optimale en fonction des limites, alors, sous les mêmes hypothèses, ∂V/∂c_i = λ_i là où V est dérivable. λ_i est le **prix implicite** de la ressource i, ce que vaut à la marge une unité de plus de cette ressource.

Partageons un budget de 10 entre deux activités qui rapportent ln(1 + x) et 2 ln(1 + y) : maximiser ln(1 + x) + 2 ln(1 + y) sous la contrainte x + y ≤ 10, avec x, y ≥ 0. La stationnarité donne 1/(1 + x) = λ et 2/(1 + y) = λ, donc 1 + y = 2(1 + x). Budget dépensé, x = 3, y = 7 et λ = 1/4, et la valeur est ln 4 + 2 ln 8 = 8 ln 2 ≈ 5,545177. Un budget de 11 donne x = 10/3 et y = 23/3, et une valeur plus élevée d'environ 0,240128, proche de λ = 0,25 : le multiplicateur prédit le gain au premier ordre, et la concavité rend le gain réel un peu plus petit.

Plafonnons maintenant la seconde activité à y ≤ 5. L'ancienne solution viole le plafond, donc le plafond est saturé : y = 5 et x = 5. La stationnarité s'écrit 1/6 = λ pour x et 2/6 = λ + μ pour y, où μ est le multiplicateur du plafond, donc λ = μ = 1/6. Les deux sont positifs ou nuls, c'est donc un point KKT, et comme le problème est concave, c'est l'optimum. La valeur tombe à 3 ln 6 ≈ 5,375278.

### Exercice pratique

Le plafond y ≤ 5 étant en place, portez-le à 6 en gardant le budget à 10. Que prédit μ, et quel est le gain réel ?

> *Solution :* μ = 1/6 prédit un gain d'environ 0,166667. Le nouvel optimum est x = 4, y = 6, toujours sur les deux contraintes, puisque 1/5 = λ et 2/7 = λ + μ donnent λ = 1/5 et μ = 3/35, tous deux positifs. Sa valeur est ln 5 + 2 ln 7 ≈ 5,501258, soit un gain de 0,125980 : l'estimation au premier ordre surestime, comme elle le doit pour un rendement concave.

---

## 2. Programmation linéaire et dualité

Quand le rendement et les contraintes sont linéaires, le problème est un **programme linéaire** (P), et il a un **dual** (D) :

```
(P)  max { cᵀx : A x ≤ b, x ≥ 0 }
(D)  min { bᵀu : Aᵀu ≥ c, u ≥ 0 }
```

Tout u réalisable majore le primal, puisque cᵀx ≤ (Aᵀu)ᵀx = uᵀAx ≤ uᵀb : c'est la **dualité faible**. Si l'un des deux problèmes a un optimum, les deux en ont un, de même valeur : c'est la **dualité forte**. À l'optimum, chaque contrainte primale et sa variable duale satisfont la complémentarité des écarts, et les variables duales sont les prix implicites du §1. La méthode du simplexe (Dantzig) va de sommet en sommet du polygone réalisable, puisqu'un objectif linéaire qui y a un maximum l'atteint en un sommet.

Deux produits rapportent 2 et 3 par unité. La machine A dispose de 4 heures (x + y ≤ 4) et la machine B de 6 heures (x + 3y ≤ 6). Les sommets (0, 0), (4, 0), (0, 2) et (3, 1) rapportent 0, 8, 6 et 9, donc l'optimum est (3, 1) avec 9. Le dual minimise 4u + 6v sous les contraintes u + v ≥ 2 et u + 3v ≥ 3. Les deux variables primales sont positives, donc les deux contraintes duales sont saturées : u = 3/2 et v = 1/2, de valeur 4 × 3/2 + 6 × 1/2 = 9. Une heure de plus sur la machine A déplace l'optimum en (4,5 ; 0,5), qui rapporte 10,5 = 9 + u.

Les jeux à somme nulle sont des programmes linéaires. Si A paie le joueur ligne, le théorème du minimax de von Neumann (1928) dit que max_p min_q pᵀAq = min_q max_p pᵀAq. Cette **valeur** commune est ce que le joueur ligne peut garantir, et un p optimal résout : maximiser v sous les contraintes Aᵀp ≥ v·1, Σ p_i = 1, p ≥ 0. À pierre-feuille-ciseaux, la valeur est 0, et la seule stratégie optimale est (1/3, 1/3, 1/3) pour chaque joueur.

### Exercice pratique

La capacité de la machine B passe de 6 à 7. Prédisez le nouvel optimum à partir du dual, puis vérifiez-le.

> *Solution :* v = 1/2 prédit 9,5. Les contraintes saturées sont maintenant x + y = 4 et x + 3y = 7, donc y = 1,5 et x = 2,5, qui rapportent 2 × 2,5 + 3 × 1,5 = 9,5. Les autres sommets, (4, 0) et (0, 7/3), rapportent 8 et 7, donc la prédiction tient. L'optimum s'est déplacé, mais les deux mêmes contraintes sont saturées ; la prédiction ne tomberait en défaut qu'une fois une autre paire saturée, ici dès que la capacité de B sortirait de l'intervalle de 4 à 12.

---

## 3. Équilibres de Nash et énumération des supports

Dans un jeu bimatriciel, le joueur A choisit une ligne i et le joueur B une colonne j ; A reçoit a_ij et B reçoit b_ij. Les stratégies mixtes p et q sont des vecteurs de probabilités, et le gain espéré de A est pᵀAq. Un couple (p, q) est un **équilibre de Nash** quand aucun joueur ne gagne à dévier seul. Comme un gain est linéaire en sa propre stratégie, il suffit de vérifier les déviations vers des stratégies pures. Nash (1950) a prouvé que tout jeu fini a un équilibre, éventuellement mixte.

À l'équilibre, chaque stratégie pure qu'un joueur utilise rapporte le même gain espéré contre le mélange de l'autre, et aucune stratégie inutilisée ne rapporte plus : c'est le **principe d'indifférence**. L'**énumération des supports** devine quelles stratégies chaque joueur utilise (les supports), résout les équations linéaires d'indifférence, et garde les solutions qui sont des vecteurs de probabilités et qu'aucune stratégie inutilisée ne bat. Un jeu m × n a (2^m − 1)(2^n − 1) couples de supports. Dans un jeu non dégénéré, seuls des supports de même taille peuvent porter un équilibre, et le nombre d'équilibres est impair, comme le montre l'algorithme de Lemke–Howson (1964).

- **Dilemme du prisonnier**, A = [[3, 0], [5, 1]] et B = Aᵀ. Trahir domine strictement coopérer pour les deux joueurs. Donc (trahir, trahir), qui vaut 1 à chacun, est le seul équilibre, alors que coopérer donnerait 3 à chaque joueur.
- **Pair ou impair**, A = [[1, −1], [−1, 1]] et B = −A. Il n'y a pas d'équilibre pur ; l'indifférence donne p = q = (1/2, 1/2).
- **Guerre des sexes**, A = [[3, 0], [0, 2]] et B = [[2, 0], [0, 3]]. Il y a deux équilibres purs, qui paient (3, 2) et (2, 3), et un équilibre mixte. B doit rendre A indifférent, 3q = 2(1 − q), donc q = 2/5. A doit rendre B indifférent, 2p = 3(1 − p), donc p = 3/5. Chaque joueur espère alors 6/5, moins que dans l'un ou l'autre équilibre pur.
- **Pierre-feuille-ciseaux.** Le seul équilibre utilise les trois stratégies, en (1/3, 1/3, 1/3) ; aucun support de taille 1 ou 2 n'en porte.

Le **jeu fictif** (Brown, 1951) est une règle d'apprentissage : à chaque tour, chaque joueur joue une meilleure réponse aux fréquences empiriques du jeu passé de l'autre. Robinson (1951) a prouvé que dans les jeux à somme nulle tout point limite de ces fréquences est une stratégie d'équilibre, si bien qu'elles convergent quand l'équilibre est unique. Shapley (1964) a montré qu'elles n'y sont pas tenues en général. Dans un jeu 3 × 3 du type qu'il a utilisé, avec A la matrice identité et B = [[0, 1, 0], [0, 0, 1], [1, 0, 0]], le seul équilibre est uniforme. Le jeu parcourt pourtant en cycle six profils purs, par séries dont les longueurs croissent géométriquement (§7), et les fréquences ne se stabilisent jamais.

### Exercice pratique

Trouvez tous les équilibres de A = [[2, 0], [0, 1]], B = [[1, 0], [0, 2]], et le gain espéré de chaque joueur dans l'équilibre mixte.

> *Solution :* Les deux équilibres purs sont (ligne 1, colonne 1) et (ligne 2, colonne 2). Pour l'équilibre mixte, le mélange de B rend A indifférent : 2q = 1 − q, donc q = 1/3. Le mélange de A rend B indifférent : p = 2(1 − p), donc p = 2/3. A espère 2q = 2/3 et B espère p = 2/3. Trois équilibres, un nombre impair, comme pour tout jeu non dégénéré.

---

## 4. La valeur de Shapley et le cœur

Un jeu coopératif donne à chaque coalition S des n joueurs une valeur v(S), avec v(∅) = 0, et une répartition x partage v(N), la valeur de la grande coalition. Shapley (1953) a montré qu'une seule règle satisfait quatre axiomes. Efficacité : les parts s'additionnent à v(N). Symétrie : des joueurs interchangeables reçoivent la même chose. Joueur nul : un joueur qui n'apporte rien ne reçoit rien. Additivité : les parts d'une somme de jeux sont les sommes des parts. Cette règle est la **valeur de Shapley** :

```
φ_i = Σ_{S ⊆ N∖{i}}  |S|! (n − |S| − 1)! / n!  ·  [v(S ∪ {i}) − v(S)]
```

c'est-à-dire la contribution marginale de i moyennée sur les n! ordres dans lesquels les joueurs peuvent arriver. Le **cœur** demande la stabilité plutôt que l'équité (Gillies, 1959) : x est dans le cœur s'il est efficace et qu'aucune coalition ne peut faire mieux seule, Σ_{i∈S} x_i ≥ v(S) pour tout S. Le cœur peut être vide. Quand il ne l'est pas, il ne contient pas forcément la valeur de Shapley ; pour un jeu convexe, il la contient (Shapley, 1971).

Dans le **jeu des gants**, les joueurs 1 et 2 détiennent chacun un gant gauche, le joueur 3 un gant droit, et une paire vaut 1. Le joueur 3 apporte 1 dans tous les ordres sauf les deux où il arrive en premier, donc φ_3 = 4/6 = 2/3. Le joueur 1 n'apporte 1 que dans l'ordre (3, 1, 2), donc φ_1 = φ_2 = 1/6. Le cœur exige x_1 + x_3 ≥ 1, x_2 + x_3 ≥ 1 et x_i ≥ 0 pour tout i, avec x_1 + x_2 + x_3 = 1, ce qui force x_1 = x_2 = 0 : le cœur est le point unique (0, 0, 1). La valeur de Shapley paie 1/6 à chaque gant gauche ; le cœur ne leur paie rien, parce que deux gants gauches se disputent un seul gant droit. Dans le **jeu majoritaire**, où deux joueurs quelconques sur trois peuvent se partager 1, le cœur est vide : les trois contraintes de paires s'additionnent en 2(x_1 + x_2 + x_3) ≥ 3, alors que les parts doivent s'additionner à 1. La valeur de Shapley est 1/3 chacun.

L'**indice de Banzhaf** (Banzhaf, 1965) compte, pour chaque joueur, les coalitions qu'il fait passer de perdantes à gagnantes, au lieu de moyenner sur les ordres. Dans un vote pondéré avec des poids 3, 3, 3, 1 et 1 et un quota de 10, une coalition gagnante a besoin des trois grands membres et d'un petit. La valeur de Shapley est (0,3 ; 0,3 ; 0,3 ; 0,05 ; 0,05), et l'indice de Banzhaf normalisé est (3/11, 3/11, 3/11, 1/11, 1/11).

### Exercice pratique

Deux joueurs, avec v({1}) = v({2}) = 0 et v({1, 2}) = 1. Donnez la valeur de Shapley et le cœur.

> *Solution :* La valeur de Shapley est 1/2 chacun, par symétrie et efficacité. Le cœur est l'ensemble des (x, 1 − x) avec 0 ≤ x ≤ 1, puisque chaque joueur seul ne peut garantir que 0. La valeur de Shapley en est le milieu.

---

## 5. Bandits et regret

Un bandit à K bras a K distributions de récompense de moyennes inconnues μ_1, …, μ_K. À chaque tour, l'apprenant tire un bras et n'observe que la récompense de ce bras. Le **regret** après T tours est le manque à gagner espéré par rapport au tirage constant du meilleur bras : R_T = T μ* − E[Σ_t r_t] = Σ_i Δ_i E[N_i(T)], où Δ_i = μ* − μ_i et N_i(T) compte les tirages du bras i. Lai et Robbins (1985) ont montré qu'un apprenant qui réussit sur tout bandit doit tirer chaque bras moins bon de l'ordre de ln T fois, donc que le regret croît au moins logarithmiquement.

**ε-glouton** tire un bras uniformément au hasard avec probabilité ε, et sinon le bras de meilleure moyenne. Son exploration ne s'arrête jamais. Une fois que ses moyennes classent correctement les bras, chaque tour coûte ε fois l'écart moyen d'un tirage uniforme. Avec des moyennes 1, 2 et 3 et ε = 0,1, cela fait 0,1 × (2 + 1 + 0)/3 = 0,1 par tour, un regret qui croît linéairement en T. **UCB1** (Auer, Cesa-Bianchi et Fischer, 2002) tire chaque bras une fois, puis le bras de plus grand q_i + √(2 ln t / n_i), où q_i est la moyenne du bras, n_i son nombre de tirages, et t le total. Pour des récompenses dans [0, 1], il tire un bras moins bon au plus 8 ln T / Δ_i² + 1 + π²/3 fois en espérance, un regret logarithmique. L'**échantillonnage de Thompson** (Thompson, 1933) tire une moyenne pour chaque bras selon sa loi a posteriori et tire le bras dont le tirage est le meilleur.

La borne suppose des récompenses dans [0, 1]. Le bonus √(2 ln t / n_i) n'a pas d'unité, alors que q_i a l'unité de la récompense, si bien que multiplier toutes les récompenses par c change les choix d'UCB1, à moins de multiplier aussi le bonus par c. Deux bras qui paient toujours 0,5 et 0,4 le montrent sans aucun hasard. Après 10 000 tours, UCB1 a tiré le moins bon bras 877 fois. S'ils paient 50 et 40, il tire le moins bon bras une fois, pendant le démarrage, et plus jamais. S'ils paient 0,005 et 0,004, il tire le moins bon bras 4 918 fois, près de la moitié. Une grande échelle n'est pas sûre non plus. Que le premier paiement du meilleur bras soit malchanceux, 30 au lieu de 50, et tous les suivants 50. UCB1 n'y revient alors jamais : un tirage, puis 9 999 du moins bon bras, un regret de 10 par tour. Pour combler un écart de 10, le bonus √(2 ln t) a besoin de ln t proche de 50.

### Exercice pratique

Pour deux bras de récompenses dans [0, 1] et Δ = 0,1, combien de tirages du moins bon bras la borne d'UCB1 autorise-t-elle après T = 10 000 tours ? Comparez avec les 877 des bras déterministes.

> *Solution :* 8 ln(10 000)/0,01 + 1 + π²/3 ≈ 7 372,6. La borne vaut pour toute distribution dans [0, 1], y compris les pires, donc sur cette paire facile et sans bruit elle est lâche d'un facteur d'environ 8.

---

## 6. Pénalités : des contraintes pour une recherche qui ne connaît que des boîtes

Une recherche qui ne connaît que des bornes de boîte l ≤ x ≤ u, comme beaucoup d'algorithmes évolutionnaires, peut tout de même respecter d'autres contraintes si on les fait passer dans l'objectif. Pour une contrainte d'égalité h(x) = 0, la **pénalité quadratique** minimise f(x) + (ρ/2) h(x)² ; pour g(x) ≤ 0, elle utilise max(0, g(x))². Quand ρ croît, ses minimiseurs s'approchent du minimiseur contraint, et ρ h(x_ρ) s'approche du multiplicateur au signe près. Pour tout ρ fini, cependant, ils violent la contrainte dès que son multiplicateur est non nul. La **pénalité ℓ1** f(x) + ρ |h(x)| est **exacte** : dès que ρ dépasse le module du multiplicateur, le minimiseur contraint est un minimiseur local de la fonction pénalisée et, pour un problème convexe comme ceux d'ici, son minimiseur global (Nocedal et Wright, chap. 17). Le prix en est un point anguleux à la solution, où les méthodes de gradient peinent.

Minimisons x² + y² sous la contrainte x + y = 2. La solution est x = y = 1, de multiplicateur λ* = 2, puisque la stationnarité s'écrit 2x = λ. Avec la pénalité quadratique, la symétrie donne x = y = t avec 2t + ρ(2t − 2) = 0, donc t = ρ/(1 + ρ). ρ = 10 donne t ≈ 0,909091 et une violation de 2/11 ≈ 0,181818. ρ = 100 donne 0,990099 et 0,019802. L'estimation ρ(2 − 2t) = 2ρ/(1 + ρ), soit 1,818182 puis 1,980198, s'approche de λ* = 2. Avec la pénalité ℓ1, minimisons 2t² + ρ|2t − 2|. En dessous de t = 1, la dérivée est 4t − 2ρ, donc le minimiseur est t = min(ρ/2, 1). Il est exact à partir de ρ = 2 = λ*, et non réalisable en dessous.

Ramener chaque coordonnée dans son intervalle, comme le fait une recherche bornée par une boîte, n'est pas une pénalité mais une projection. Cela traite exactement une boîte, et rien d'autre.

### Exercice pratique

Le problème de budget du §1, écrit pour un minimiseur qui ne connaît que la boîte [0, 10]², devient : minimiser −ln(1 + x) − 2 ln(1 + y) + ρ max(0, x + y − 10). Quels poids ρ rendent cette pénalité ℓ1 exacte ?

> *Solution :* Tout ρ supérieur à λ* = 1/4. En dessous, une unité de budget de plus au-delà de 10 rapporte davantage, à la marge 1/(1 + x) = 1/4, que ce que coûte la pénalité, donc le minimiseur dépense trop.

---

## 7. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python de `nash.rs` et `cooperative.rs` dans `crates/ix-game`, et de `UCB1` et du choix glouton d'`EpsilonGreedy` dans `crates/ix-rl`. Aucun de ces codes ne tire de nombre aléatoire. La transcription reproduit les assertions des tests déterministes que cite cette section. Elle ne reproduit pas les exécutions qui tirent dans le `StdRng` à graine d'IX, dont le flux, comme l'explique le §6 de MAT-009, n'est pas une spécification portable ; pour celles-là, le §8 n'énonce que des prédictions qualitatives.

**Énumération des supports : deux sortes de supports parmi beaucoup.** [`support_enumeration`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L152) parcourt tous les couples de supports, mais [`solve_support`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L177) n'en résout que deux sortes : un couple de stratégies pures, et le support complet d'un jeu 2 × 2.

```rust
        // For 2x2 mixed strategy: solve indifference conditions
        if m == 2 && n == 2 && support_a.len() == 2 && support_b.len() == 2 {
            return self.solve_2x2_mixed();
        }

        None // General case would need linear programming
```

La documentation du module annonce [Lemke–Howson](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L3), que le fichier ne contient pas, et l'espace de travail n'a aucun solveur de programmation linéaire. Sur les jeux 2 × 2 du §3, la transcription trouve tous les équilibres : 1 pour pair ou impair, dont le [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L365) vérifie seulement qu'un équilibre proche de (1/2, 1/2) figure parmi ceux trouvés, et non leur nombre, et 3 pour la guerre des sexes, dont le test affirme seulement [au moins 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L398). Pierre-feuille-ciseaux et le jeu de Shapley sont des jeux 3 × 3 qui n'ont qu'un équilibre mixte, donc la fonction renvoie une liste vide. L'outil MCP [`ix_game_nash`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1406) répond alors `count: 0` pour des jeux qui, par le théorème de Nash, ont un équilibre, et rien dans la réponse ne dit que la recherche était partielle. Le guide d'IX énonce clairement la limite dans son [deuxième piège](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L175), mais son [quatrième](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L179) dit que l'énumération des supports les trouve tous.

**Jeu fictif : un premier coup fantôme, et les égalités au dernier.** [`fictitious_play`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L247) commence chaque compte [avec un coup de la stratégie 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L253). Parmi des meilleures réponses à égalité, il prend la dernière, parce que `max_by` de Rust [renvoie le dernier de maxima égaux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L262). Son test joue le dilemme du prisonnier pendant 1 000 tours et affirme une fréquence de trahison [supérieure à 0,9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L413) ; la transcription trahit à chaque tour, donc la seule coopération sur 1 001 comptes est la coopération fantôme. À pair ou impair, les fréquences des deux joueurs après 100, 1 000, 10 000 et 100 000 tours sont à moins de 0,054455 ; 0,016484 ; 0,006649 et 0,001605 de 1/2, comme le prédit le théorème de Robinson. Au jeu de Shapley, elles ne se stabilisent jamais. Les séries de profils identiques ont pour longueurs 1, 2, 3, 6, 9, 13, 20, 30, 44, 65 et ainsi de suite, et le rapport de chacune à la précédente tend vers environ 1,466. Après 100 000 tours, les fréquences de A sont (0,3822 ; 0,4399 ; 0,1779), loin de (1/3, 1/3, 1/3). La fonction renvoie les fréquences sans dire si elles ont convergé, même si sa documentation prévient qu'elle [peut ne pas converger pour tous les jeux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/nash.rs#L246). Le guide d'IX dit que le jeu fictif est [garanti de converger](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/game-theory/nash-equilibria.md#L177) pour les jeux à somme nulle et pour les jeux à équilibre unique. Le jeu de Shapley, que le même piège cite juste après, a un équilibre unique et tourne en cycle.

**Valeur de Shapley : exacte, exponentielle, et hors du cœur.** [`shapley_value`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L53) somme la formule du §4 sur les 2^(n−1) coalitions sans chaque joueur, avec des factorielles en [`u64`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L168). Le [test du jeu des gants](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L194) affirme seulement que le gant droit reçoit [plus qu'un gant gauche](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L206) et que les parts s'additionnent à 1. La transcription donne (1/6, 1/6, 2/3), que [`is_in_core`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L82) rejette, alors qu'elle accepte (0, 0, 1). Pour le jeu du test du cœur, avec 7, 5 et 3 pour les paires et 10 pour les trois, la valeur de Shapley (13/3, 10/3, 7/3) est dans le cœur. La documentation du module mentionne le [nucléole](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/cooperative.rs#L1), que le fichier n'implémente pas. Les contrats de la crate disent de ne pas appeler la fonction [au-delà d'environ 20 joueurs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L39), à cause d'un cache de valeurs de coalitions que la fonction n'alloue pas. La limite est réelle pour une autre raison : 21! vaut environ 2,77 fois 2^64, donc à partir de 21 joueurs la factorielle de n dépasse `u64`. `product` de Rust panique alors quand les contrôles de dépassement sont actifs, comme dans une compilation de débogage, et boucle modulo 2^64 sinon.

**Bandits : les égalités au dernier bras, et un bonus sans unité.** [`EpsilonGreedy::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L26) choisit la meilleure moyenne [avec `max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L33), donc son premier choix glouton, toutes les moyennes étant à 0, est le dernier bras ; les contrats de la crate promettent [le premier](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L8). Il en va de même pour l'action gloutonne du [Q-learning](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/q_learning.rs#L55), dont le contrat promet aussi [le plus petit indice](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L14). Il en va de même encore pour [`first_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L29), dont le contrat dit qu'elle [départage au profit du premier enchérisseur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/CONTRACTS.md#L12). [`second_price_auction`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-game/src/auction.rs#L46) trie de façon stable et donne bien une égalité au premier enchérisseur. Dans le test d'ε-glouton, le meilleur bras est [le dernier](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L143), celui que le départage favorise. [`UCB1::select_arm`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L62) ajoute le bonus du §5 sans paramètre d'échelle :

```rust
    pub fn select_arm(&self) -> usize {
        // Play each arm at least once
        for (i, &c) in self.counts.iter().enumerate() {
            if c == 0 {
                return i;
            }
        }

        let total = self.total_count as f64;
        self.q_values
            .iter()
            .enumerate()
            .map(|(i, &q)| {
                let bonus = (2.0 * total.ln() / self.counts[i] as f64).sqrt();
                (i, q + bonus)
            })
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
            .unwrap()
            .0
    }
```

Les bras déterministes du §5 sont des exécutions d'une transcription de cette fonction. Son test vérifie seulement que [chacun de 5 bras est joué une fois d'abord](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L164), et aucun test ne mesure le regret. L'[échantillonnage de Thompson](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L91) fixe la variance de chaque bras à [1/n](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/src/bandit.rs#L131). C'est la variance a posteriori de la moyenne pour des récompenses de variance 1 sous une loi a priori plate, et les contrats l'appellent [une simplification](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-rl/CONTRACTS.md#L13). L'outil MCP [`ix_bandit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2333) tire les récompenses avec un [écart type de 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2355) dans un générateur [de graine 42](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2342), et rapporte les tirages et la récompense totale, pas le regret.

**Évolution : des boîtes seulement.** L'algorithme génétique et l'évolution différentielle prennent un seul intervalle pour toutes les coordonnées ([`with_bounds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L57)) et y [ramènent](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/genetic.rs#L120) chaque enfant. Il n'y a aucune autre contrainte ni aucune aide pour les pénalités, donc les pénalités du §6 sont à écrire par l'appelant. Le `mutation_rate` de l'algorithme génétique n'est pas un taux. C'est l'[écart type d'un pas gaussien](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L56), et chaque gène fait ce pas [avec probabilité 0,3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/traits.rs#L58). Le [`pick_three`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L132) de l'évolution différentielle tire trois indices distincts autres que l'indice courant, et [recommence jusqu'à les avoir](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-evolution/src/differential.rs#L134). Avec un, deux ou trois individus, il ne rend jamais la main. L'outil MCP `ix_evolution` transmet le [`population_size`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2417) de l'appelant sans le vérifier.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon ne fait que le décrire.

### Exercice pratique

`ix_game_nash` répond `count: 0` pour pierre-feuille-ciseaux. Quel est l'équilibre, et comment pourriez-vous l'approcher avec IX en l'état ?

> *Solution :* (1/3, 1/3, 1/3) pour chaque joueur, la stratégie minimax du §2. IX ne sait pas la calculer, mais le jeu est à somme nulle, donc `fictitious_play` s'en approche : après 100 000 tours, chaque fréquence est à moins de 0,001077 de 1/3. `is_nash_equilibrium` confirme le profil uniforme lui-même, aucune déviation ne rapportant quoi que ce soit.

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Énumération des supports.** Exécuter `support_enumeration` sur pair ou impair, la guerre des sexes, pierre-feuille-ciseaux et le jeu de Shapley. Prédiction : 1, 3, 0 et 0 équilibres ; pour la guerre des sexes, l'équilibre mixte en (0,6 ; 0,4) et (0,4 ; 0,6).
2. **Jeu fictif.** Exécuter `fictitious_play` sur pair ou impair et sur le jeu de Shapley pendant 100, 1 000, 10 000 et 100 000 tours. Prédiction : à pair ou impair, la fréquence de la première stratégie de A 0,554455 ; 0,483516 ; 0,499550 et 0,500625 ; au jeu de Shapley, les fréquences de A après 100 000 tours (0,3822 ; 0,4399 ; 0,1779).
3. **Valeur de Shapley et cœur.** Exécuter `shapley_value` et `is_in_core` sur le jeu des gants et sur le jeu du test du cœur, et `shapley_value` et `banzhaf_index` sur le vote pondéré du §4. Prédiction : les valeurs du §4 et du §7, (1/6, 1/6, 2/3) rejetée et (0, 0, 1) acceptée, (13/3, 10/3, 7/3) acceptée.
4. **Égalités.** Appeler `select_arm` sur un nouvel `EpsilonGreedy` à trois bras et ε = 0, et lancer les deux enchères sur deux offres égales. Prédiction : le bras 2 ; l'enchère au premier prix va au second enchérisseur, l'enchère au second prix au premier.
5. **UCB1 et l'unité de la récompense.** Exécuter `UCB1` pendant 10 000 tours sur les bras déterministes du §5, aux trois échelles et avec le premier paiement malchanceux. Prédiction : 877, 1 et 4 918 tirages du moins bon bras ; avec le premier paiement malchanceux à l'échelle 100, 1 tirage du meilleur bras.
6. **Regret sur des bras bruités.** Exécuter `EpsilonGreedy` avec ε = 0,1 et `UCB1` sur trois bras de moyennes 1, 2 et 3 et de bruit gaussien d'écart type 1, comme le fait `ix_bandit`, pendant 1 000, 10 000 et 100 000 tours sur 20 graines, et calculer le regret à partir des tirages. Prédiction, qualitative seulement, puisque cette leçon ne reproduit pas le générateur d'IX : le regret par tour d'ε-glouton reste proche de 0,1, tandis que celui d'UCB1 baisse quand T croît.
7. **Évolution différentielle à trois individus.** Exécuter `DifferentialEvolution` avec une population de 4, puis de 3, dans un thread séparé, en attendant son résultat au plus 10 secondes. Prédiction : la première rend la main, la seconde non.

### Exercice pratique

L'étape 6 compare le regret sur un seul modèle de bruit fixé. Comment rendre la comparaison équitable entre les deux algorithmes ?

> *Solution :* Tirer les récompenses à l'avance, un flux par bras, pour que le k-ième tirage d'un bras rende la même récompense quel que soit l'algorithme qui le tire. Calculer le regret à partir des tirages et des vraies moyennes, pas des récompenses reçues, et rapporter sa dispersion sur les graines, pas une seule exécution.

---

## 9. Pièges courants

- **Lire une liste d'équilibres vide comme « pas d'équilibre ».** Tout jeu fini en a un ; une liste vide issue d'une énumération partielle dit seulement que la recherche ne l'a pas trouvé.
- **Croire que le jeu fictif converge.** Dans les jeux à somme nulle, ses fréquences s'approchent des stratégies d'équilibre ; en général, rien ne les y oblige, même avec un équilibre unique. Vérifiez les fréquences contre les meilleures réponses.
- **Prendre la valeur de Shapley pour une répartition stable.** L'équité et la stabilité sont des axiomes différents ; testez le cœur à part.
- **Utiliser un multiplicateur loin de la marge.** C'est une dérivée ; un grand changement d'une ressource demande de résoudre le problème à nouveau.
- **Tenir la réponse d'une pénalité quadratique pour réalisable.** Sauf si le multiplicateur est nul, elle viole la contrainte pour tout poids fini ; une pénalité ℓ1 de poids supérieur au multiplicateur, non.
- **Appeler un écrêtage un traitement des contraintes.** Il traite une boîte, et rien d'autre.
- **Comparer des algorithmes de bandit par la récompense totale sur une seule graine.** Le regret par rapport au meilleur bras est la mesure, et une graine est un seul échantillon.
- **Donner à UCB1 des récompenses hors de [0, 1].** Remettez à l'échelle les récompenses, ou le bonus, selon l'étendue de la récompense.
- **Supposer qu'une égalité va au premier indice.** `max_by` de Rust renvoie le dernier de maxima égaux et `min_by` le premier ; un tri stable garde l'ordre d'entrée.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Conditions KKT** | Stationnarité, réalisabilité, multiplicateurs positifs ou nuls et complémentarité des écarts ; nécessaires et suffisantes pour un problème concave sous la condition de Slater |
| **Prix implicite** | Le multiplicateur d'une contrainte : la valeur marginale d'une unité de plus de sa ressource |
| **Dualité de la programmation linéaire** | Le dual majore le primal, et à l'optimum les deux ont la même valeur |
| **Équilibre de Nash** | Un profil de stratégies dont aucun joueur ne gagne à dévier seul |
| **Énumération des supports** | Deviner les stratégies que chaque joueur utilise et résoudre les équations d'indifférence |
| **Jeu fictif** | Chaque joueur joue une meilleure réponse aux fréquences empiriques du jeu passé de l'autre |
| **Valeur de Shapley** | La contribution marginale moyenne sur tous les ordres d'arrivée ; la seule règle qui ait efficacité, symétrie, joueur nul et additivité |
| **Cœur** | Les répartitions efficaces qu'aucune coalition ne peut améliorer seule |
| **Regret** | Le manque à gagner espéré par rapport au tirage constant du meilleur bras |
| **UCB1** | Tirer le bras de plus grande moyenne plus √(2 ln t / n_i), après un tirage de chacun |
| **Pénalité quadratique** | f + (ρ/2) h² : non réalisable pour tout ρ fini quand le multiplicateur est non nul, ρ h s'approchant du multiplicateur |
| **Pénalité exacte** | f + ρ \|h\| : exacte dès que ρ dépasse le module du multiplicateur |

---

## Auto-évaluation

**1. `support_enumeration` renvoie une liste vide pour un jeu 3 × 3. Que savez-vous ?**
> Rien sur l'existence : par le théorème de Nash, le jeu a un équilibre. IX ne résout que les supports purs et le support complet d'un jeu 2 × 2, donc un équilibre qui mélange dans un jeu 3 × 3 est hors de sa portée. Pierre-feuille-ciseaux en est un exemple, avec son seul équilibre en (1/3, 1/3, 1/3).

**2. Dans le jeu des gants, pourquoi la valeur de Shapley n'est-elle pas dans le cœur ?**
> Les deux sont efficaces, mais le cœur exige aussi que chaque coalition reçoive au moins sa valeur. La valeur de Shapley donne aux joueurs 1 et 3 ensemble 1/6 + 2/3 = 5/6, moins que le 1 qu'ils peuvent obtenir seuls. La seule répartition qui satisfait toutes les coalitions est (0, 0, 1).

**3. Un service donne à UCB1 des récompenses mesurées en millisecondes gagnées, de l'ordre de la centaine. Qu'est-ce qui ne va pas ?**
> Le bonus √(2 ln t / n_i) reste de l'ordre de 1 alors que les moyennes diffèrent de dizaines. Après le démarrage, UCB1 est glouton : un seul premier résultat malchanceux peut écarter le meilleur bras pour de bon. Remettez les récompenses à l'échelle de [0, 1], ou multipliez le bonus par l'étendue.

**4. Un algorithme génétique à bornes de boîte doit respecter x + y ≤ 10. Que pouvez-vous faire ?**
> Ajouter une pénalité à l'objectif. La pénalité ℓ1 ρ max(0, x + y − 10) est exacte dès que ρ dépasse le multiplicateur de la contrainte. Une pénalité quadratique n'est réalisable qu'approximativement. L'écrêtage traite la boîte et ne fait rien pour la somme.

**Critères de réussite :** Écrire et résoudre les conditions KKT d'une petite allocation et lire ses multiplicateurs comme des prix ; résoudre un programme linéaire à deux variables et son dual ; trouver les équilibres d'un petit jeu bimatriciel et dire quand le jeu fictif converge ; calculer une valeur de Shapley et tester le cœur ; définir le regret et dire ce que suppose la borne d'UCB1 ; choisir un poids de pénalité exacte ; et dire lesquelles des sorties d'IX ses tests fixent.

---

## Bases de recherche

- W. Karush, *Minima of Functions of Several Variables with Inequalities as Side Constraints*, mémoire de M.Sc., Université de Chicago, 1939, et H. W. Kuhn et A. W. Tucker, « Nonlinear programming », *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*, 1951 : les conditions KKT
- S. Boyd et L. Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004, chapitre 5 : dualité, condition de Slater et prix implicites
- G. B. Dantzig, *Linear Programming and Extensions*, Princeton University Press, 1963 : la méthode du simplexe et la dualité de la programmation linéaire
- J. von Neumann, « Zur Theorie der Gesellschaftsspiele », *Mathematische Annalen* 100, 1928 : le théorème du minimax
- J. F. Nash, « Equilibrium points in n-person games », *Proceedings of the National Academy of Sciences* 36, 1950 : tout jeu fini a un équilibre
- C. E. Lemke et J. T. Howson, « Equilibrium points of bimatrix games », *Journal of the Society for Industrial and Applied Mathematics* 12, 1964 : l'algorithme de Lemke–Howson et le nombre impair d'équilibres
- G. W. Brown, « Iterative solution of games by fictitious play », dans *Activity Analysis of Production and Allocation*, Wiley, 1951, et J. Robinson, « An iterative method of solving a game », *Annals of Mathematics* 54, 1951 : le jeu fictif, et sa convergence dans les jeux à somme nulle
- L. S. Shapley, « Some topics in two-person games », dans *Advances in Game Theory*, Annals of Mathematics Studies 52, 1964 : un jeu où le jeu fictif tourne en cycle
- L. S. Shapley, « A value for n-person games », dans *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28, 1953 : la valeur de Shapley
- D. B. Gillies, « Solutions to general non-zero-sum games », dans *Contributions to the Theory of Games IV*, Annals of Mathematics Studies 40, 1959 : le cœur
- L. S. Shapley, « Cores of convex games », *International Journal of Game Theory* 1, 1971 : la valeur de Shapley d'un jeu convexe est dans son cœur
- J. F. Banzhaf III, « Weighted voting doesn't work: a mathematical analysis », *Rutgers Law Review* 19, 1965 : l'indice de Banzhaf
- T. L. Lai et H. Robbins, « Asymptotically efficient adaptive allocation rules », *Advances in Applied Mathematics* 6, 1985 : la borne inférieure logarithmique du regret
- P. Auer, N. Cesa-Bianchi et P. Fischer, « Finite-time analysis of the multiarmed bandit problem », *Machine Learning* 47, 2002 : UCB1 et sa borne
- W. R. Thompson, « On the likelihood that one unknown probability exceeds another in view of the evidence of two samples », *Biometrika* 25, 1933 : l'échantillonnage de Thompson
- T. Lattimore et C. Szepesvári, *Bandit Algorithms*, Cambridge University Press, 2020 : regret, ε-glouton et UCB
- J. Nocedal et S. J. Wright, *Numerical Optimization*, 2e édition, Springer, 2006, chapitre 17 : méthodes de pénalité quadratique et exacte
- N. Nisan, T. Roughgarden, É. Tardos et V. V. Vazirani (dir.), *Algorithmic Game Theory*, Cambridge University Press, 2007 : l'énumération des supports et le calcul des équilibres
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §7 renvoie à sa ligne
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
