---
module_id: mat-020-markov-chains-hmm
department: mathematics
course: Chaînes de Markov et modèles de Markov cachés
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-008-probability-conditional-reasoning, mat-019-graphs-centrality-spectral]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Chaînes de Markov et modèles de Markov cachés — Où une chaîne se stabilise, et ce qu'une chaîne cachée laisse voir

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Écrire une chaîne de Markov comme une matrice stochastique, faire avancer une distribution avec elle, et trouver sa distribution stationnaire
- Dire quand une chaîne finie a une unique distribution stationnaire et quand la distribution y converge, et reconnaître une chaîne périodique sur laquelle elle n'y converge pas
- Calculer exactement les temps d'atteinte, les temps de retour et les probabilités d'absorption, et dire ce qu'une simulation tronquée estime à la place
- Évaluer et décoder un modèle de Markov caché avec les algorithmes avant–arrière et de Viterbi, et expliquer quand les deux décodages divergent
- Obtenir Baum–Welch comme un cas de l'algorithme EM, et dire ce qu'il garantit et ce qu'il ne garantit pas
- Retracer ce que garantissent `MarkovChain`, `HiddenMarkovModel`, leurs gestionnaires et `model_code_evolution` d'IX, et où leurs guides, contrats et tests promettent plus que ce que le code tient

---

## 1. Les chaînes de Markov comme matrices

Une chaîne de Markov sur les états 0 à n − 1 passe à chaque pas de l'état i à l'état j avec une probabilité P_ij qui ne dépend que de i : l'état suivant ne dépend du passé qu'à travers le présent, c'est la **propriété de Markov**. La matrice P est **stochastique** : ses coefficients sont positifs ou nuls et chaque ligne a pour somme 1. Une distribution sur les états est un vecteur ligne μ, et un pas l'envoie sur μP, donc après t pas μ_t = μ_0 Pᵗ ; le coefficient (Pᵏ)_ij est la probabilité d'être en j k pas après avoir été en i, et Pᵏ⁺ˡ = Pᵏ Pˡ (l'équation de Chapman–Kolmogorov).

Une **distribution stationnaire** est une distribution π telle que πP = π : un vecteur propre à gauche de P pour la valeur propre 1. La valeur propre 1 existe toujours, puisque P𝟙 = 𝟙, et aucune valeur propre n'est plus grande en module : pour un vecteur ligne x, Σ_j |Σ_i x_i P_ij| ≤ Σ_i |x_i| Σ_j P_ij, donc ‖xP‖₁ ≤ ‖x‖₁. Que π soit unique, et que μ_t s'en approche, dépend de la chaîne (§2).

La chaîne à deux états, P = [[1 − a, a], [b, 1 − b]] avec a + b > 0, montre tout d'un coup. Sa distribution stationnaire est π = (b, a)/(a + b), son autre valeur propre est 1 − a − b, et μ_t − π = (μ_0 − π)(1 − a − b)ᵗ : une différence (δ, −δ) est envoyée sur (1 − a − b)(δ, −δ). Le test d'IX lui-même utilise la chaîne météo avec a = 0,3 et b = 0,4, dont la distribution stationnaire est (4/7, 3/7), et la distance à celle-ci est multipliée par 0,3 à chaque pas.

### Exercice pratique

Vérifier que π = (b, a)/(a + b) est stationnaire pour la chaîne à deux états, et que c'est la seule distribution stationnaire quand a + b > 0.

> *Solution :* Le premier coefficient de πP est (b(1 − a) + ab)/(a + b) = b/(a + b), et le second est (ba + a(1 − b))/(a + b) = a/(a + b). Une distribution stationnaire (x, 1 − x) doit envoyer à chaque pas autant de probabilité de 0 vers 1 que de 1 vers 0 : x a = (1 − x) b, donc x = b/(a + b), seule solution. Quand a = b = 0, rien ne bouge, et toute distribution est stationnaire.

---

## 2. Distributions stationnaires et convergence

Une chaîne est **irréductible** quand chaque état peut atteindre tous les autres : le graphe orienté qui a une arête i → j dès que P_ij > 0 est fortement connexe. La **période** d'un état i est le plus grand commun diviseur des k ≥ 1 tels que (Pᵏ)_ii > 0 ; tous les états d'une chaîne irréductible ont la même, et la chaîne est **apériodique** quand elle vaut 1. Deux théorèmes règlent alors les questions du §1 pour une chaîne finie (Norris 1997) :

- Une chaîne irréductible a exactement une distribution stationnaire, dont tous les coefficients sont strictement positifs. C'est le théorème de Perron–Frobenius de MAT-019 §1, dans sa forme pour les matrices positives irréductibles, appliqué à P.
- Si la chaîne est de plus apériodique, μ_0 Pᵗ → π depuis tout départ. P est alors **primitive** : une puissance Pᵏ a tous ses coefficients strictement positifs. Wielandt (1950) a montré que k = (n − 1)² + 1 suffit toujours, et que sa matrice en a besoin : i → i + 1 pour i < n − 1, et n − 1 → 0 ou 1 avec probabilité ½ chacun, dont les cycles ont pour longueurs n et n − 1.

La périodicité n'est pas un détail technique. La marche aléatoire sur le chemin 0–1–2, P = [[0, 1, 0], [½, 0, ½], [0, 1, 0]], est irréductible de période 2, et sa distribution stationnaire est (1/4, 1/2, 1/4), le d_i/(2m) de MAT-019 §2 avec les degrés 1, 2, 1 et m = 2. Depuis le départ uniforme, un pas donne (1/6, 2/3, 1/6) et le suivant redonne (1/3, 1/3, 1/3) : la distribution alterne pour toujours, et π est la moyenne des deux. Pour toute chaîne irréductible, les moyennes (1/T) Σ_(t<T) μ_0 Pᵗ convergent vers π, et le théorème ergodique dit davantage : le long d'une seule trajectoire, la fraction des T premiers pas passée dans l'état j tend vers π_j avec probabilité 1, quelle que soit la période.

Une chaîne vérifie l'**équilibre détaillé** quand π_i P_ij = π_j P_ji pour tous i et j ; en sommant sur i, on obtient alors πP = π, si bien que l'équilibre détaillé est un moyen rapide de trouver π, et une telle chaîne est dite réversible. La marche aléatoire sur un graphe non orienté est réversible avec π_i = d_i/(2m), puisque les deux membres valent 1/(2m) sur chaque arête.

### Exercice pratique

Trouver la distribution stationnaire de P = [[0, 1], [1, 0]], et dire si μ_0 Pᵗ converge.

> *Solution :* D'après le §1 avec a = b = 1, π = (½, ½) est la seule distribution stationnaire. Depuis μ_0 = (x, 1 − x), μ_t alterne entre (x, 1 − x) et (1 − x, x), donc elle ne converge que si x = ½, où elle est constante dès le départ. La chaîne est de période 2, et la valeur propre −1 de P maintient en vie la différence μ_0 − π, dont le signe change à chaque pas.

---

## 3. Temps d'atteinte et chaînes absorbantes

Le **temps d'atteinte** d'un état j est T_j = min{t ≥ 1 : X_t = j}. Conditionner sur le premier pas donne, pour tout i ≠ j, h_i = 1 + Σ_(k≠j) P_ik h_k, où h_i est l'espérance du temps d'atteinte depuis i : un système linéaire avec une inconnue par état autre que j, dont la solution est unique et finie quand j est accessible depuis tout état. Depuis j lui-même, le même pas donne l'espérance du **temps de retour** m_jj = 1 + Σ_(k≠j) P_jk h_k, et la formule de Kac affirme que m_jj = 1/π_j pour une chaîne irréductible (Kac 1947). En rassemblant toutes les paires dans une matrice M, avec J la matrice de uns et M_dg la diagonale de M, le système s'écrit M = J + P(M − M_dg) (Kemeny et Snell 1960). La soustraction compte : le système M = J + PM n'a pas de solution (§6).

Un état j tel que P_jj = 1 est **absorbant**. Quand chaque état peut atteindre un état absorbant, on range d'abord les états transitoires, de sorte que P = [[Q, R], [0, I]]. La **matrice fondamentale** N = (I − Q)^-1 = I + Q + Q² + … compte les visites : N_ik est l'espérance du nombre de visites à l'état transitoire k depuis i. L'espérance du nombre de pas avant l'absorption est t = N𝟙, et la matrice des probabilités d'absorption est B = NR. Pour une ruine du joueur équitable sur 0 à 4, avec les états transitoires 1, 2, 3 et des pas de ±1 de probabilité ½,

N = [[3/2, 1, 1/2], [1, 2, 1], [1/2, 1, 3/2]], t = (3, 4, 3),

donc la partie dure en moyenne k(4 − k) pas depuis k, et la colonne de B pour l'état 4 est (1/4, 1/2, 3/4) = k/4.

Ces réponses exactes coûtent une résolution linéaire. Une simulation qui lance des marches depuis i et arrête chacune après L pas ne peut moyenner que les marches arrivées, donc elle estime E[T | T ≤ L], et non E[T]. Pour un état qui part à chaque pas avec probabilité p vers un état absorbant, T est géométrique, et avec q = 1 − p,

E[T | T ≤ L] = 1/p − L qᴸ/(1 − qᴸ).

Avec p = 0,1 et L = 10, cela vaut 4,6466, contre E[T] = 10, et seules 1 − 0,9^10 ≈ 65 % des marches arrivent. Lancer plus de marches réduit le bruit mais pas ce biais ; une simulation doit dire combien de marches sont arrivées, et quand la chaîne est connue, le système linéaire donne la valeur exacte.

### Exercice pratique

Trouver l'espérance du temps de retour à l'état 0 de la chaîne météo du §1 en conditionnant sur le premier pas, et vérifier la formule de Kac.

> *Solution :* Depuis l'état 1, la chaîne passe en 0 avec probabilité 0,4 à chaque pas, donc h_1 = 1 + 0,6 h_1 et h_1 = 2,5. Depuis 0, le pas suivant reste en 0 avec probabilité 0,7, ce qui est un retour après un pas, ou passe en 1 avec probabilité 0,3 : m_00 = 1 + 0,3 · 2,5 = 1,75 = 7/4. La distribution stationnaire donne π_0 = 4/7, et 1/π_0 = 7/4.

---

## 4. Modèles de Markov cachés : évaluation et décodage

Dans un **modèle de Markov caché**, une chaîne d'états q_1, …, q_T n'est pas observée ; chaque état émet un symbole o_t, qui l'est. Le modèle a une distribution initiale ν, une matrice de transition A et une matrice d'émission B, où B_ik est la probabilité que l'état i émette le symbole k. La probabilité des observations et d'un chemin q est ν_(q_1) B_(q_1, o_1) Π_(t≥2) A_(q_(t−1), q_t) B_(q_t, o_t), et Rabiner (1989) énumère trois problèmes : la probabilité P(O) des observations, les états cachés les plus probables, et les paramètres qui rendent les observations probables.

L'**algorithme avant** calcule P(O) sans énumérer les nᵀ chemins. Avec α_1(i) = ν_i B_i(o_1) et α_(t+1)(j) = (Σ_i α_t(i) A_ij) B_j(o_(t+1)), α_t(i) est la probabilité des t premières observations avec q_t = i, et P(O) = Σ_i α_T(i), en O(T n²) opérations. Les variables arrière β_T(i) = 1 et β_t(i) = Σ_j A_ij B_j(o_(t+1)) β_(t+1)(j) donnent la probabilité des observations suivantes depuis q_t = i, et γ_t(i) = α_t(i) β_t(i)/P(O) est la probabilité a posteriori de l'état i au temps t. Comme α_t décroît à peu près géométriquement avec t, il sous-déborde sur les longues séquences ; les implémentations remettent chaque α_t à la somme 1 avec un facteur c_t et additionnent les logarithmes : log P(O) = Σ_t log c_t.

L'**algorithme de Viterbi** remplace la somme par un maximum. En logarithmes, δ_1(i) = log(ν_i B_i(o_1)) et δ_t(j) = max_i (δ_(t−1)(i) + log A_ij) + log B_j(o_t), avec un pointeur vers le i qui réalise le maximum ; remonter les pointeurs depuis le meilleur état final donne le chemin le plus probable dans son ensemble (Viterbi 1967 ; Forney 1973). Le **décodage a posteriori** prend à la place, à chaque t, l'état de plus grand γ_t(i). Il maximise l'espérance du nombre d'états justes, mais la suite qu'il renvoie n'est pas forcément un chemin possible.

Le modèle météo d'IX a les états cachés Pluvieux (0) et Ensoleillé (1), les symboles Marcher, Faire les courses et Nettoyer, ν = (0,6 ; 0,4), A = [[0,7 ; 0,3] ; [0,4 ; 0,6]] et B = [[0,1 ; 0,4 ; 0,5] ; [0,6 ; 0,3 ; 0,1]]. Pour Marcher, Faire les courses, Nettoyer, P(O) = 8403/250000 = 0,033612 ; le chemin le plus probable est Ensoleillé, Pluvieux, Pluvieux, de probabilité 42/3125 = 0,01344, et la probabilité a posteriori d'Ensoleillé vaut 0,7683, 0,3759 et 0,1360 aux trois pas. Ici, les deux décodages concordent. Ils divergent dans un modèle à trois états et un seul symbole, où les observations n'apportent donc aucune information : ν = (0,4 ; 0,3 ; 0,3), l'état 0 reste en 0, l'état 1 passe en 2, et l'état 2 reste en 2. Après deux pas, γ_1 = (0,4 ; 0,3 ; 0,3) et γ_2 = (0,4 ; 0 ; 0,6), donc le décodage a posteriori renvoie (0, 2), un chemin de probabilité 0, puisque 0 ne passe jamais en 2 ; Viterbi renvoie (0, 0), de probabilité 0,4.

### Exercice pratique

Montrer que Σ_i α_t(i) β_t(i) = P(O) pour tout t.

> *Solution :* α_t(i) est la probabilité de o_1, …, o_t et q_t = i, et β_t(i) est la probabilité de o_(t+1), …, o_T sachant q_t = i. Sachant l'état présent, les observations suivantes ne dépendent pas des précédentes (la propriété de Markov de la chaîne cachée, chaque symbole ne dépendant que de son état), donc le produit est la probabilité de toutes les observations et de q_t = i. La somme sur i donne P(O).

---

## 5. Apprentissage : Baum–Welch comme EM

L'**algorithme de Baum–Welch** ajuste ν, A et B à une séquence observée (Baum et al. 1970). Son étape E calcule les probabilités a posteriori γ_t(i) et ξ_t(i, j) = α_t(i) A_ij B_j(o_(t+1)) β_(t+1)(j)/P(O), la probabilité du passage de i à j entre t et t + 1. Son étape M pose ν̂_i = γ_1(i), Â_ij = Σ_(t<T) ξ_t(i, j)/Σ_(t<T) γ_t(i) et B̂_ik = Σ_(t : o_t = k) γ_t(i)/Σ_t γ_t(i) : des comptes espérés divisés par des totaux espérés. C'est l'algorithme EM de MAT-018 §3 avec le chemin caché comme donnée manquante (Dempster, Laird et Rubin 1977), et il en hérite la garantie et les limites : la vraisemblance ne diminue jamais, mais les itérés peuvent se fixer sur un maximum local ou un point selle au lieu du maximum global.

Quatre conséquences découlent des formules :
- **Les zéros restent nuls.** Un zéro dans A, B ou ν annule chaque terme du compte espéré correspondant (voir l'exercice).
- **La symétrie est conservée.** Si échanger deux états laisse le modèle inchangé, leurs probabilités a posteriori sont égales, et leurs paramètres réestimés aussi, comme pour les composantes identiques de MAT-018 §3.
- **Une séquence donne un seul départ.** ν̂ = γ_1 vient du premier instant de l'unique séquence, donc à mesure que le modèle s'affine, elle finit souvent par mettre toute la probabilité sur un seul état.
- **Les états n'ont pas de nom.** Tout réétiquetage des états donne la même vraisemblance ; les états ne sont identifiables qu'à une permutation près.

Prenons la séquence 0, 1, 0, 1, … de longueur 100, deux états et deux symboles. Le modèle qui alterne sans faute, avec A = [[0, 1], [1, 0]], B l'identité et ν = (1, 0), lui donne la probabilité 1, le maximum. Depuis le départ entièrement symétrique, ν = (½, ½), tous les coefficients de A égaux à ½ et les deux lignes d'émission (0,6 ; 0,4), une étape M donne aux deux lignes d'émission les fréquences (½, ½) des données et laisse tout le reste à ½. Sous ce modèle, toute séquence de longueur 100 a la probabilité 2^-100, donc la log-vraisemblance vaut 100 ln ½ ≈ −69,3147, et l'étape M suivante ne change rien : un point fixe qui n'est pas un maximum. Le test d'IX part plutôt d'un modèle légèrement asymétrique (§6).

### Exercice pratique

Montrer qu'une étape M ne rend jamais strictement positif un zéro de A, de B ou de ν, tant que l'état concerné a une masse a posteriori strictement positive, pour que le rapport soit défini.

> *Solution :* Si A_ij = 0, chaque ξ_t(i, j) contient le facteur A_ij, donc chacun est nul, leur somme aussi, et Â_ij = 0. Si B_ik = 0, alors α_t(i) = 0 à chaque t où o_t = k, donc γ_t(i) = 0 à ces instants et le numérateur de B̂_ik est nul. Si ν_i = 0, alors α_1(i) = 0 et ν̂_i = γ_1(i) = 0. Un zéro introduit par erreur est donc définitif, et un zéro structurel, un passage que le modèle doit interdire, est conservé.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python de `crates/ix-graph/src/markov.rs`, de `crates/ix-graph/src/hmm.rs`, des deux gestionnaires ci-dessous et de `model_code_evolution`, avec une réplique du `StdRng` de rand 0.9 pour les simulations, vérifiée sur des tirages de rand lui-même. Ces nombres sont des prédictions, et le §7 propose de les vérifier.

**La chaîne et son gestionnaire.** [`MarkovChain::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L20) vérifie que la matrice est carrée et que chaque ligne a pour somme 1 [à 10^-6 près](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L27) ; comme les contrats d'IX le [disent](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L8), elle ne rejette pas les coefficients négatifs. [`stationary_distribution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L56) part de la [distribution uniforme](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L58) et exécute :

```rust
        for _ in 0..max_iter {
            let new_dist = dist.dot(&self.transition);
            let diff = (&new_dist - &dist).mapv(f64::abs).sum();
            dist = new_dist;
            if diff < tol {
                break;
            }
        }
```

L'outil MCP `ix_markov` appelle [`markov`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1320), qui transmet son paramètre `steps` comme `max_iter` avec une [tolérance de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1327) et ajoute [`is_ergodic(100)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1328) à sa réponse. [`mean_first_passage`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L94) simule des marches, arrête chacune après `max_steps`, et se termine par :

```rust
        if reached == 0 {
            f64::INFINITY
        } else {
            total_steps as f64 / reached as f64
        }
```

- **Sur une chaîne périodique, la réponse dépend de la parité de `steps`.** Sur le chemin 0–1–2 du §2, les itérés alternent entre le vecteur uniforme et (1/6, 2/3, 1/6), le changement vaut 2/3 à chaque passe, et la boucle va jusqu'à `max_iter` : `ix_markov` renvoie (1/6, 2/3, 1/6) pour un `steps` impair et (1/3, 1/3, 1/3) pour un pair, jamais (1/4, 1/2, 1/4), et rien dans la réponse ne dit que la boucle n'a pas convergé. Les contrats d'IX préviennent bien que l'appelant [ne peut pas distinguer](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L11) la convergence de la coupure ; `is_ergodic` vaut false ici, ce qui est le seul indice. Sur [[0, 1], [1, 0]], la fonction renvoie (½, ½) après une passe, parce que le départ uniforme est déjà stationnaire : ce succès ne dit rien de la convergence. Le guide d'IX dit de cette chaîne qu'elle [« never actually converges »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L195), ce qui est vrai de `state_distribution` depuis d'autres départs, pas de cette fonction.
- **Les coefficients négatifs passent.** Les lignes de [[1,1 ; −0,1] ; [0,5 ; 0,5]] ont pour somme 1, et `ix_markov` renvoie environ (1,25 ; −0,25) comme distribution stationnaire, une vraie solution de πP = π avec un coefficient négatif, accompagnée de `is_ergodic` à false. `HiddenMarkovModel::new` [rejette les valeurs négatives](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L80).
- **`is_ergodic` teste si chaque coefficient de Pᵏ dépasse [10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L144)**, et le gestionnaire prend toujours k = 100. Une chaîne irréductible et apériodique peut échouer de deux façons. La matrice de Wielandt sur 11 états demande (11 − 1)² + 1 = 101 pas, donc P^100 a encore un coefficient nul et la réponse est false ; sur 10 états, elle en demande 82, et la réponse est true. La chaîne [[1 − ε, ε], [ε, 1 − ε]] avec ε = 10^-12 se mélange si lentement que les coefficients hors diagonale de P^100 sont juste sous 100ε = 10^-10, et la réponse est encore false. Une réponse positive est juste, puisqu'une puissance strictement positive prouve que la chaîne est irréductible et apériodique ; il n'y a aucun test d'irréductibilité ni de période.
- **`mean_first_passage` ne moyenne que les marches arrivées.** Une marche qui n'a pas atteint la cible après `max_steps` est [abandonnée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L119) sans être comptée, donc le résultat estime le E[T | T ≤ L] du §3, avec L = `max_steps`. Sur [[0,9 ; 0,1] ; [0 ; 1]], de 0 à 1 avec 10 000 marches et la graine 42, la transcription prédit 4,6178 avec `max_steps` 10, où 6449 marches arrivent, et 10,1787 avec 1000, contre la valeur exacte 10. Le guide d'IX demande [« at least 10,000 simulations »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/markov-chains.md#L189), ce qui réduit le bruit et non ce biais, et nomme le système exact « M = 1 + P * M », qui n'a pas de solution (voir l'exercice). Il n'y a ni temps d'atteinte exact, ni matrice fondamentale, ni probabilité d'absorption ; [`AbsorbingChain`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L149) se contente de lister les états dont le [coefficient diagonal vaut exactement 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/markov.rs#L157).
- **`model_code_evolution` prédit une chute que ses données n'ont jamais montrée.** Dans `crates/ix-code`, [`model_code_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L303) répartit un historique de scores de qualité en classes, compte les transitions, ajoute [10^-6 à chaque case](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L356) avant de normaliser, et donne comme temps moyen jusqu'à la classe de qualité la plus basse la valeur de [`mean_first_passage` avec 200 marches d'au plus 1000 pas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L381). Une classe qui n'a jamais été quittée n'a aucun compte, donc sa ligne est uniforme. Pour l'historique croissant 0, 1, 2, 3 avec 4 états, la classe du haut n'a jamais été quittée, et le modèle prédit une chute vers la classe la plus basse en environ 7 pas (6,99998 exactement pour cette matrice, 7,53 par la simulation), pour une qualité qui n'a fait que monter. Pour 1, 2, …, 8, la classe du haut n'a jamais été suivie que d'elle-même : le temps moyen exact est d'environ 1,0 × 10^6 pas, mais une seule des 200 marches atteint la classe la plus basse en 1000 pas, et la fonction renvoie 878. Son test, [`test_markov_evolution`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L591), ne vérifie que les sommes des lignes et les longueurs, et rien d'autre n'appelle la fonction.
- **Le gestionnaire de Viterbi vérifie le modèle mais pas les symboles.** [`viterbi`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1339) construit le modèle avec [`HiddenMarkovModel::new`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1353) mais ne compare jamais les observations au nombre de colonnes d'émission, donc un symbole hors bornes indexe au-delà de la matrice d'émission, ce qui panique dans `ndarray`. La fonction DuckDB `ix_viterbi` le [rejette](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L531) avec une erreur SQL, comme son [invariant](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L517) le promet. Pour une séquence impossible, comme 0 puis 1 sous un modèle dont les états ne changent jamais et émettent toujours leur propre indice, chaque score vaut −∞, la [comparaison stricte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L268) ne se déclenche jamais, le chemin retombe sur l'état 0 à chaque pas, et la sortie JSON écrit la log-probabilité −∞ comme `null`.
- **NaN passe les deux constructeurs.** Une somme NaN rend [`(row_sum - 1.0).abs() > 1e-6`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L57) faux, et un coefficient NaN rend [`v < 0.0`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L77) faux, donc aucune des deux vérifications ne le rejette, dans `HiddenMarkovModel::new` comme dans `MarkovChain::new`. JSON ne peut pas transporter NaN, donc seuls des appelants Rust peuvent y arriver.
- **Le code, le guide et les contrats se contredisent sur Baum–Welch.** [`baum_welch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L330) clone le modèle, renvoie la copie entraînée comme `Result<Self, String>`, et s'arrête quand la log-vraisemblance change de [moins de `tol`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L353). Les contrats d'IX disent qu'elle [« MUTATES the HMM in place and returns the final log-likelihood »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L14), sans garantie d'amélioration monotone « due to numerical underflow », et qu'elle ne renvoie [pas de Result](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/CONTRACTS.md#L24). Les récurrences remises à l'échelle existent pour éviter le sous-débordement, et d'après le §5 EM ne fait jamais baisser la vraisemblance, comme le dit le [guide des HMM](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/sequence-models/hidden-markov-models.md#L214) d'IX lui-même ; sur la séquence du test d'IX, la transcription trouve une hausse à chacun des 50 pas.
- **Certains tests passeraient sur du code faux.** [`test_baum_welch_improves_likelihood`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L627) affirme que la log-vraisemblance après l'entraînement est au moins celle d'avant [moins 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L637), ce que satisferait un `baum_welch` renvoyant son entrée inchangée. La transcription prédit −14,6565 avant et −13,0797 après 50 pas, avec une distribution initiale effondrée sur (0, 1) à 10^-55 près, l'effet de séquence unique du §5. [`test_forward_backward_consistency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L738) annonce que la log-probabilité avant [« should match what we compute from alpha alone »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L739), puis vérifie seulement que γ est dans [0, 1] et que la log-probabilité est finie. [`test_baum_welch_recovers_parameters`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L687) s'entraîne sur la séquence alternée du §5 depuis un départ légèrement asymétrique ; la transcription prédit qu'il atteint le modèle alterné du §5, de log-vraisemblance 0, après 7 réestimations. Ce test [vérifie seulement que les émissions se spécialisent](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/hmm.rs#L709), ce qui est la bonne vérification, puisqu'aucun vrai paramètre n'a engendré les données.
- **Le catalogue nomme la mauvaise crate.** Le catalogue qu'envoie `ix_explain_algorithm` liste le HMM comme [« ix_probabilistic::HMM (viterbi) »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5844) ; `ix-probabilistic` contient des filtres de Bloom, count-min et coucou et HyperLogLog, et le HMM se trouve dans `ix_graph::hmm`.
- **Autres lacunes.** Il n'y a ni distribution stationnaire exacte par résolution linéaire, ni test d'irréductibilité ou de période, ni temps d'atteinte exact ou analyse d'absorption, ni Baum–Welch sur plusieurs séquences, ni tirage depuis un modèle de Markov caché, ni opération MCP pour l'algorithme avant, le décodage a posteriori ou Baum–Welch : `ix_markov` et `ix_viterbi` sont les deux seules.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Montrer que le système M = J + PM nommé dans le guide d'IX n'a pas de solution, et que le système du §3 donne la formule de Kac.

> *Solution :* Soit π une distribution stationnaire. Multiplier M = J + PM à gauche par π donne πM = πJ + πM, puisque πP = π ; comme les coefficients de π ont pour somme 1, πJ est la ligne de uns, donc 0 = (1, …, 1), ce qui est impossible. Le système du §3, M = J + P(M − M_dg), donne au contraire πM = πJ + πM − πM_dg, donc πM_dg = (1, …, 1) : π_j m_jj = 1 pour tout j, ce qui est la formule de Kac.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Parité.** Appeler `markov` avec la chaîne du chemin du §2 et `steps` 1, puis 100. Prédiction : (1/6, 2/3, 1/6), puis (1/3, 1/3, 1/3), avec `is_ergodic` à false les deux fois ; la moyenne des deux est (1/4, 1/2, 1/4).
2. **Ergodicité.** Appeler `is_ergodic(100)` sur la matrice de Wielandt à 10 et à 11 états, et sur la chaîne à deux états avec ε = 10^-12. Prédiction : true, false, false ; et true pour 11 états avec `is_ergodic(101)`.
3. **Troncature.** Appeler `mean_first_passage` sur [[0,9 ; 0,1] ; [0 ; 1]] de 0 à 1 avec 10 000 marches et la graine 42, et `max_steps` 10, puis 1000 ; puis de 0 à 0 sur la chaîne météo du §1, avec 10 000 marches d'au plus 1000 pas et la graine 7. Prédiction : 4,6178, 10,1787, et 1,7538 contre le 7/4 de Kac.
4. **Évolution du code.** Appeler `model_code_evolution` sur 0, 1, 2, 3 et sur 1, 2, …, 8, avec 4 états. Prédiction : l'état courant 3 les deux fois, et un temps moyen jusqu'à l'état critique de 7,53, puis 878.
5. **Météo.** Construire le modèle météo d'IX et appeler `forward`, `viterbi` et `forward_backward` sur Marcher, Faire les courses, Nettoyer. Prédiction : l'exponentielle de la log-probabilité vaut 0,033612, le chemin Ensoleillé, Pluvieux, Pluvieux a pour log-probabilité ln 0,01344, et la probabilité a posteriori d'Ensoleillé vaut 0,7683, 0,3759 et 0,1360.
6. **Décodeurs.** Appeler `map_estimate` et `viterbi` sur le modèle à trois états du §4 avec deux observations ; puis appeler le gestionnaire `viterbi` sur les observations 0, 1 du modèle dont les états ne changent jamais, puis avec le symbole 2, dans un processus enfant. Prédiction : (0, 2), puis (0, 0) de probabilité 0,4 ; le chemin (0, 0) avec une log-probabilité `null` ; puis une panique.
7. **Baum–Welch.** Lancer `baum_welch` sur la séquence alternée de longueur 100 depuis le départ symétrique du §5 et depuis le départ du test d'IX, avec 100 pas et une tolérance de 10^-10. Prédiction : tous les paramètres à ½ et la log-vraisemblance −69,3147 après 2 pas ; le modèle alterné et la log-vraisemblance 0 après 7.

### Exercice pratique

Pourquoi la prédiction pour `max_steps` 1000 à l'étape 3 ne vaut-elle pas exactement 10, et est-elle biaisée ?

> *Solution :* Une marche manque la cible en 1000 pas avec probabilité 0,9^1000, environ 1,7 × 10^-46, donc le biais de troncature y est négligeable. L'écart est un bruit d'échantillonnage : T a pour écart-type √0,9/0,1 ≈ 9,49, donc la moyenne de 10 000 marches a une erreur type d'environ 0,095, et 10,1787 est à environ 1,9 erreur type au-dessus de 10. Une autre graine tomberait ailleurs autour de 10, alors qu'avec `max_steps` 10 toute graine tombe près de 4,6466.

---

## 8. Pièges courants

- **Lire un résultat d'itération de puissance comme stationnaire sans le vérifier.** Calculer ‖πP − π‖₁ ; sur une chaîne périodique, les itérés oscillent, et moyenner de nombreux itérés consécutifs, ou résoudre le système linéaire, donne π.
- **Faire confiance à une convergence depuis le départ uniforme.** Sur une chaîne dont la distribution stationnaire est uniforme, la première passe s'arrête déjà, quelle que soit la période.
- **Prendre « tous les coefficients de P^100 au-dessus de 10^-10 » pour l'ergodicité.** L'irréductibilité est une question de forte connexité sur le graphe des coefficients strictement positifs, et la période est un plus grand commun diviseur de longueurs de cycles ; répondre directement aux deux.
- **Moyenner seulement les marches arrivées.** Dire combien sont arrivées, ou résoudre le système linéaire du §3.
- **Prédire à partir de lignes que les données n'ont jamais remplies.** Un état jamais quitté n'a aucune donnée pour sa ligne, et le lissage rend cette ligne uniforme ; donner les comptes derrière chaque ligne.
- **Lire un décodage a posteriori comme un chemin.** Chaque état est le plus probable à son propre pas, et la suite peut être impossible ; utiliser Viterbi pour un chemin.
- **Lancer Baum–Welch depuis un modèle symétrique ou avec des zéros non voulus.** La symétrie est un point fixe et les zéros sont définitifs ; partir de plusieurs points aléatoires et garder la meilleure vraisemblance.
- **Apprendre la distribution initiale sur une seule séquence.** Elle s'effondre sur un seul état ; la fixer, ou entraîner sur plusieurs séquences.
- **Envoyer à `ix_viterbi` un symbole supérieur ou égal au nombre de colonnes d'émission.** Le gestionnaire MCP panique ; vérifier d'abord les symboles, ou utiliser la fonction DuckDB, qui renvoie une erreur.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Matrice stochastique** | Une matrice à coefficients positifs ou nuls dont chaque ligne a pour somme 1 |
| **Distribution stationnaire** | Une distribution π telle que πP = π |
| **Chaîne irréductible** | Une chaîne dans laquelle chaque état peut atteindre tous les autres |
| **Période** | Le plus grand commun diviseur des longueurs des retours d'un état sur lui-même |
| **Matrice primitive** | Une matrice positive dont une puissance a tous ses coefficients strictement positifs |
| **Équilibre détaillé** | π_i P_ij = π_j P_ji pour tous i et j, ce qui rend π stationnaire |
| **Temps d'atteinte** | Le premier instant t ≥ 1 où la chaîne se trouve dans un état donné |
| **Matrice fondamentale** | N = (I − Q)^-1 d'une chaîne absorbante, dont les coefficients comptent les visites espérées |
| **Modèle de Markov caché** | Une chaîne de Markov d'états non observés, dont chacun émet un symbole observé |
| **Algorithme avant** | La récurrence qui calcule la probabilité des observations en O(T n²) opérations |
| **Chemin de Viterbi** | La suite d'états cachés la plus probable sachant les observations |
| **Algorithme de Baum–Welch** | L'algorithme EM pour les paramètres d'un modèle de Markov caché |

---

## Auto-évaluation

**1. `ix_markov` renvoie (1/6, 2/3, 1/6) comme distribution stationnaire d'une chaîne, avec `is_ergodic` à false. Qu'en concluez-vous, et comment obtenez-vous π ?**
> Vérifier d'abord πP = π : ici le résultat est envoyé sur (1/3, 1/3, 1/3), donc il n'est pas stationnaire. La chaîne est le chemin périodique du §2, la boucle est allée jusqu'à `steps` sans converger, et avec un `steps` pair la réponse aurait été uniforme. Moyenner deux itérés consécutifs, ou résoudre π(P − I) = 0 avec des coefficients de π de somme 1 : (1/4, 1/2, 1/4).

**2. Un rapport affirme, d'après `model_code_evolution`, qu'une crate atteindra une qualité critique en 878 commits en moyenne. Que demandez-vous avant d'y croire ?**
> Combien des 200 marches ont atteint la classe la plus basse : la valeur ne moyenne que celles-là, et sur l'historique croissant du §6 une seule y est arrivée, alors que la moyenne exacte pour cette matrice est d'environ 10^6. Puis quelles lignes de la matrice reposent sur des données : une classe jamais quittée reçoit une ligne uniforme, qui peut à elle seule créer un chemin vers la classe la plus basse. Enfin, si une chaîne à quelques classes convient seulement à cet historique.

**3. Viterbi et le décodage a posteriori divergent sur une séquence. Lequel rapportez-vous ?**
> Cela dépend de la question. Pour la suite d'états la plus probable dans son ensemble, par exemple pour segmenter un signal, rapporter le chemin de Viterbi ; pour avoir juste le plus d'états possible, rapporter le décodage a posteriori, avec ses probabilités, et dire que sa suite peut être impossible, comme (0, 2) l'est dans le modèle du §4.

**4. Baum–Welch s'arrête après deux pas avec tous les paramètres égaux à ½. L'implémentation est-elle cassée ?**
> Pas forcément. Un départ où échanger les états laisse le modèle inchangé reste symétrique sous EM (§5), et sur la séquence alternée il atteint un point fixe de log-vraisemblance 100 ln ½, très en dessous du maximum 0. Briser la symétrie, lancer plusieurs départs aléatoires et garder la meilleure vraisemblance, et confronter la réponse aux données.

**Critères de réussite :** Écrire une chaîne comme une matrice stochastique et trouver sa distribution stationnaire ; dire quand elle est unique et quand la distribution y converge ; calculer les temps d'atteinte, les temps de retour et les probabilités d'absorption, et dire ce qu'estime une simulation tronquée ; évaluer et décoder un modèle de Markov caché et expliquer quand les décodages divergent ; obtenir Baum–Welch comme EM et énoncer sa garantie et ses limites ; et retracer où les guides, contrats, gestionnaires et tests d'IX promettent plus que ce que le code tient.

---

## Bases de recherche

- A. A. Markov, « Extension of the law of large numbers to dependent quantities » (en russe), *Izvestiya of the Physico-Mathematical Society at Kazan University* 15, 1906 : les premières chaînes
- M. Kac, « On the notion of recurrence in discrete stochastic processes », *Bulletin of the American Mathematical Society* 53, 1947 : le temps moyen de retour
- H. Wielandt, « Unzerlegbare, nicht negative Matrizen », *Mathematische Zeitschrift* 52, 1950 : l'exposant d'une matrice primitive
- J. G. Kemeny et J. L. Snell, *Finite Markov Chains*, Van Nostrand, 1960 : la matrice fondamentale et les temps moyens de premier passage
- A. J. Viterbi, « Error bounds for convolutional codes and an asymptotically optimum decoding algorithm », *IEEE Transactions on Information Theory* 13, 1967 : l'algorithme de Viterbi
- L. E. Baum, T. Petrie, G. Soules et N. Weiss, « A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains », *Annals of Mathematical Statistics* 41, 1970 : l'algorithme de Baum–Welch et sa monotonie
- G. D. Forney, « The Viterbi algorithm », *Proceedings of the IEEE* 61, 1973 : l'algorithme comme plus court chemin
- A. P. Dempster, N. M. Laird et D. B. Rubin, « Maximum likelihood from incomplete data via the EM algorithm », *Journal of the Royal Statistical Society, Series B* 39, 1977 : EM
- L. R. Rabiner, « A tutorial on hidden Markov models and selected applications in speech recognition », *Proceedings of the IEEE* 77, 1989 : les trois problèmes, la remise à l'échelle et le décodage a posteriori
- J. R. Norris, *Markov Chains*, Cambridge University Press, 1997 : irréductibilité, périodicité, convergence et théorème ergodique
- O. Cappé, E. Moulines et T. Rydén, *Inference in Hidden Markov Models*, Springer, 2005 : lissage, décodage et identifiabilité
- D. A. Levin, Y. Peres et E. L. Wilmer, *Markov Chains and Mixing Times*, American Mathematical Society, 2009 : les vitesses de convergence
- R. A. Horn et C. R. Johnson, *Matrix Analysis*, 2e éd., Cambridge University Press, 2013 : les matrices primitives et la borne de Wielandt
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
