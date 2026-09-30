---
module_id: mat-019-graphs-centrality-spectral
department: mathematics
course: Graphes, centralité et structure spectrale
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-018-clustering-density-validity]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Graphes, centralité et structure spectrale — Quel sommet compte, et ce que compte le laplacien

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Décrire un graphe par ses matrices d'adjacence, des degrés et laplacienne, et y lire les marches et les composantes
- Définir PageRank comme la distribution stationnaire d'un surfeur aléatoire, borner l'erreur de son itération de la puissance, et dire ce que devient le rang d'un sommet sans lien sortant
- Calculer les centralités de degré, de proximité, d'intermédiarité et de vecteur propre, et construire un graphe sur lequel elles divergent
- Démontrer que le laplacien est semi-défini positif et que la multiplicité de sa valeur propre 0 est le nombre de composantes connexes
- Couper un graphe avec le vecteur de Fiedler, et dire quand ce vecteur n'est pas déterminé
- Retracer ce que garantissent le `Graph` d'IX, ses gestionnaires et `compute_laplacian_spectrum`, et où leurs commentaires, leur catalogue et leurs tests promettent plus que ce que le code fournit

---

## 1. Les graphes comme matrices

Un graphe a n sommets, numérotés de 0 à n − 1, et un ensemble d'arêtes. Dans un graphe orienté, une arête i → j a un sens ; dans un graphe non orienté, une arête {i, j} est une paire non ordonnée. La **matrice d'adjacence** A a A_ij = 1 quand une arête va de i à j et 0 sinon, ou un poids w_ij > 0 dans un graphe pondéré ; pour un graphe non orienté, A est symétrique. Le **degré** d'un sommet est d_i = Σ_j A_ij, et D = diag(d_1, …, d_n). Dans un graphe non pondéré, le coefficient (Aᵏ)_ij compte les marches de longueur k de i à j, puisqu'une marche i → l → j apporte A_il A_lj à (A²)_ij, et ainsi de suite. Deux sommets d'un graphe non orienté sont dans la même **composante connexe** quand une marche les relie ; un graphe orienté est faiblement connexe quand ses arêtes, sans tenir compte de leur sens, le relient.

Pour un graphe non orienté, A est symétrique, donc le théorème spectral du MAT-005 donne des valeurs propres réelles λ_1 ≥ … ≥ λ_n et une base orthonormée de vecteurs propres. Comme A a des coefficients positifs ou nuls, le théorème de Perron–Frobenius en dit plus (Horn et Johnson 2013, chap. 8) : λ_1 ≥ |λ_i| pour tout i, et quand le graphe est connexe, λ_1 est simple et a un vecteur propre à coefficients strictement positifs, le **vecteur de Perron**. La borne |λ_n| ≤ λ_1 peut être une égalité : un graphe connexe a λ_n = −λ_1 exactement quand il est **biparti**, quand ses sommets se répartissent en deux côtés avec chaque arête entre les deux (Brouwer et Haemers 2012). Une étoile, un chemin et un cycle pair sont bipartis ; un triangle ne l'est pas. Cela compte pour l'itération de la puissance (§3), qui a besoin d'une valeur propre strictement plus grande en module que toutes les autres.

### Exercice pratique

Montrer que le spectre d'un graphe biparti est symétrique par rapport à 0 : si λ est une valeur propre, −λ l'est aussi, avec la même multiplicité.

> *Solution :* Numérotons d'abord les sommets d'un côté, de sorte que A = [[0, B], [Bᵀ, 0]]. Si (u, v) est un vecteur propre pour λ, alors B v = λ u et Bᵀ u = λ v. Alors A (u, −v) = (−B v, Bᵀ u) = (−λ u, λ v) = −λ (u, −v), donc −λ est une valeur propre. L'application (u, v) ↦ (u, −v) est inversible et envoie le sous-espace propre de λ sur celui de −λ, donc les multiplicités sont égales. Pour l'étoile de centre 0 et de feuilles 1, 2 et 3, les valeurs propres sont √3, 0, 0 et −√3.

---

## 2. PageRank

PageRank (Brin et Page 1998 ; Page, Brin, Motwani et Winograd 1999) classe les sommets d'un graphe orienté d'après le comportement à long terme d'un surfeur aléatoire. Depuis le sommet i, avec la probabilité α, le **facteur d'amortissement**, le surfeur suit l'un des liens sortants de i, chacun avec la probabilité 1/out(i) ; avec la probabilité 1 − α, il saute vers un sommet tiré uniformément. Un sommet sans lien sortant, un **nœud pendant**, demande une règle à part, et la règle usuelle envoie le surfeur de là vers un sommet uniforme. Notons P la matrice des liens sortants, avec P_ij = 1/out(i) pour une arête i → j, dont les lignes des nœuds pendants sont nulles ; S la matrice P dont ces lignes sont remplacées par u = (1/n, …, 1/n) ; et 𝟙 la colonne de uns. La **matrice Google** est M = α S + (1 − α) 𝟙u, et le vecteur PageRank est sa distribution stationnaire : le vecteur ligne π ≥ 0 avec Σ_i π_i = 1 et π M = π.

Pour 0 ≤ α < 1, tous les coefficients de M sont strictement positifs, donc par Perron–Frobenius π existe, est unique et est strictement positif. L'itération de la puissance le trouve, et son erreur se borne facilement. Pour deux vecteurs de probabilité x et y, x M − y M = α (x − y) S, parce que (x − y) 𝟙 = 0 ; S a des coefficients positifs ou nuls et des lignes de somme 1, donc ‖(x − y) S‖₁ ≤ ‖x − y‖₁, et ‖x M − y M‖₁ ≤ α ‖x − y‖₁. Après k pas depuis n'importe quel départ, l'erreur en norme ℓ1 vaut au plus 2αᵏ. Avec l'usuel α = 0,85, 100 pas laissent au plus 2 · 0,85^100 ≈ 1,7 × 10^-7 ; avec α = 0,99, la même borne vaut 2 · 0,99^100 ≈ 0,73, et elle peut être presque atteinte (§6). La deuxième valeur propre de M est au plus α en module (Haveliwala et Kamvar 2003) : α fixe la vitesse.

Un autre traitement des nœuds pendants abandonne leur rang : itérer x ← α x P + (1 − α) u. Le même argument, avec P à la place de S, montre que l'itération converge, vers x* = (1 − α) u (I − α P)^-1, dont les coefficients ont une somme inférieure à 1 dès qu'un nœud pendant a un rang strictement positif. Prenons deux articles, 0 et 1, qui citent un troisième, 2, qui ne cite rien, avec α = 0,85. Après deux pas, les rangs de 0 et de 1 valent 0,15/3 = 0,05, celui de 2 vaut 0,05 + 0,85 · (0,05 + 0,05) = 0,135, et plus rien ne change ensuite : les trois ont pour somme 0,235. Divisé par cette somme, x* devient (10/47 ; 10/47 ; 27/47) ≈ (0,2128 ; 0,2128 ; 0,5745), qui est exactement π avec des sauts uniformes depuis le nœud pendant (exercice ci-dessous ; Langville et Meyer 2006).

Sur un graphe non orienté à m arêtes et sans sommet isolé, où chaque arête compte dans les deux sens, la marche sans saut, α = 1, a pour matrice de transition D^-1 A, et π_i = d_i/(2m) est stationnaire : Σ_i (d_i/(2m)) (A_ij/d_i) = d_j/(2m). Sur un graphe non orienté, le surfeur aléatoire est attiré par les sommets de fort degré.

### Exercice pratique

Montrer que, quand le rang des nœuds pendants est abandonné, le point fixe x*, divisé par la somme de ses coefficients, est le PageRank π avec des sauts uniformes depuis les nœuds pendants.

> *Solution :* Soit a la colonne qui vaut 1 aux nœuds pendants et 0 ailleurs, de sorte que S = P + a u. Comme π 𝟙 = 1, π M = α π P + α (π a) u + (1 − α) u, donc π = α π P + γ u avec γ = α (π a) + 1 − α > 0. La matrice I − α P est inversible, car α P a des coefficients positifs ou nuls et des lignes de somme au plus α < 1, donc π = γ u (I − α P)^-1 = (γ/(1 − α)) x*. Ainsi π est un multiple strictement positif de x*, et comme les coefficients de π ont pour somme 1, π = x*/Σ_i x*_i. Sur le graphe de citations, γ = 0,85 · 27/47 + 0,15 = 30/47, et γ/(1 − α) = 200/47 = 1/0,235.

---

## 3. La famille des centralités

Les mesures de centralité répondent à des questions différentes sur un sommet i d'un graphe non orienté connexe à n sommets :
- La **centralité de degré**, d_i/(n − 1) : combien de voisins, en fraction du possible.
- La **centralité de proximité**, (n − 1)/Σ_j dist(i, j), avec des distances comptées en arêtes : à quel point i est proche de tous les autres. Sur un graphe non connexe, cette somme est infinie ; la forme r²/((n − 1) Σ_j dist(i, j)), avec r le nombre de sommets accessibles depuis i et la somme sur eux, se ramène à la première quand tous les sommets sont accessibles (Wasserman et Faust 1994).
- La **centralité d'intermédiarité**, Σ σ_st(i)/σ_st sur les paires non ordonnées {s, t} d'autres sommets, où σ_st compte les plus courts chemins entre s et t et σ_st(i) ceux qui passent par i (Freeman 1977) : à quelle fréquence i se trouve sur le trajet. La division par (n − 1)(n − 2)/2, le nombre de paires, la ramène dans [0, 1]. Brandes (2001) la calcule pour tous les sommets en temps O(nm) pour m arêtes, avec un parcours en largeur depuis chaque sommet.
- La **centralité de vecteur propre** (Bonacich 1972) : le vecteur de Perron de A, de sorte que chaque sommet obtient un score proportionnel à la somme des scores de ses voisins, x_i = (1/λ_1) Σ_j A_ij x_j.

Le cerf-volant de Krackhardt (Krackhardt 1990) est le graphe classique sur lequel elles divergent. Ses dix sommets, Andre, Beverly, Carol, Diane, Ed, Fernando, Garth, Heather, Ike et Jane, sont numérotés de 0 à 9, avec les arêtes 0–1, 0–2, 0–3, 0–5, 1–3, 1–4, 1–6, 2–3, 2–5, 3–4, 3–5, 3–6, 4–6, 5–6, 5–7, 6–7, 7–8 et 8–9. Diane a le plus fort degré, 6 sur 9, et la plus forte centralité de vecteur propre. Fernando et Garth sont les plus proches, à 9/14 ≈ 0,643 contre 3/5 pour Diane. Heather, le seul lien entre la partie dense et la queue Ike–Jane, a la plus forte intermédiarité, 14 sur les 36 paires d'autres sommets, contre 25/3 pour Fernando et Garth et 11/3 pour Diane. Aucune des quatre réponses n'est fausse : chacune mesure autre chose, et « le sommet le plus central » ne veut rien dire tant qu'on n'a pas dit quelle mesure.

La centralité de vecteur propre se calcule d'ordinaire par l'itération de la puissance (MAT-005 §6), qui échoue sur les graphes bipartis : d'après le §1, leur spectre contient −λ_1 en plus de λ_1, les deux termes de plus grand module ne se séparent jamais, et l'itéré oscille. Sur l'étoile de centre 0 et de feuilles 1, 2 et 3, depuis x = (1, 1, 1, 1), A x = (3, 1, 1, 1) et A² x = (3, 3, 3, 3) : après tout nombre pair de pas, l'itéré normalisé est uniforme, et le centre ressemble à une feuille. Le remède usuel itère avec A + I, dont les valeurs propres sont λ_i + 1, avec les mêmes vecteurs propres. Comme λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1 dès que λ_1 > 0, donc le vecteur de Perron domine désormais strictement. Les valeurs propres décalées ne sont pas forcément positives : sur l'étoile, ce sont 1 + √3, 1, 1 et 1 − √3 ≈ −0,732. Sur un graphe non connexe, l'itération depuis un départ strictement positif converge vers un vecteur porté par les composantes dont le λ_1 est le plus grand, et tout autre sommet obtient 0 à la limite.

### Exercice pratique

Calculer l'intermédiarité du centre d'une étoile à k feuilles, et du sommet du milieu du chemin 0–1–2, avant et après la division par le nombre de paires.

> *Solution :* Dans une étoile, chaque paire de feuilles a exactement un plus court chemin, par le centre, donc l'intermédiarité du centre vaut k(k − 1)/2, le nombre de paires de feuilles, et chaque feuille obtient 0. Avec n = k + 1 sommets, il y a (n − 1)(n − 2)/2 = k(k − 1)/2 paires d'autres sommets, donc la valeur normalisée est 1. Pour le chemin 0–1–2, la seule paire qui ne contient pas 1 est {0, 2}, dont l'unique plus court chemin passe par 1 : intermédiarité 1, normalisée 1. Sans normalisation, le centre d'une étoile obtient 3 avec trois feuilles et 10 avec cinq, alors que les deux sont sur tous les plus courts chemins où ils peuvent être.

---

## 4. Le laplacien

Le **laplacien** d'un graphe non orienté de poids w_ij ≥ 0 est L = D − A, où d_i = Σ_j w_ij. Sa forme quadratique est

xᵀ L x = Σ sur les arêtes {i, j} de w_ij (x_i − x_j)²,

donc L est semi-défini positif (exercice), et L 𝟙 = 0 parce que chaque ligne a pour somme 0. Ses valeurs propres, dans l'ordre croissant, sont 0 = μ_1 ≤ μ_2 ≤ … ≤ μ_n.

**La valeur propre nulle compte les composantes.** Pour une matrice semi-définie positive, xᵀ L x = 0 exactement quand L x = 0. Avec des poids strictement positifs, xᵀ L x = 0 signifie x_i = x_j le long de chaque arête, c'est-à-dire x constant sur chaque composante connexe. Le noyau de L est donc engendré par les vecteurs indicateurs des composantes, et la multiplicité de la valeur propre 0 est le nombre c de composantes. En particulier μ_2 > 0 exactement quand le graphe est connexe ; Fiedler (1973) a appelé μ_2 la **connectivité algébrique**.

**Le vecteur de Fiedler.** Par le quotient de Rayleigh du MAT-005, pris sur les vecteurs orthogonaux à 𝟙, le vecteur propre de μ_1,

μ_2 = min sur les x ≠ 0 tels que Σ_i x_i = 0 de Σ sur les arêtes de (x_i − x_j)² / Σ_i x_i²,

pour un graphe non pondéré, et un minimiseur est un **vecteur de Fiedler**. Poser x_i = 1 sur une moitié des sommets et −1 sur l'autre, quand n est pair, change le numérateur en 4 fois le nombre d'arêtes coupées et le dénominateur en n, donc μ_2 ≤ 4 · coupe/n pour tout partage en deux moitiés. Le vecteur de Fiedler est la meilleure relaxation à valeurs réelles de cette coupe équilibrée, et partager les sommets selon son signe est la plus simple des partitions spectrales. Fiedler (1975) a démontré que, sur un graphe connexe, les sommets où le vecteur est ≥ 0 induisent un sous-graphe connexe, et ceux où il est ≤ 0 aussi. Le vecteur n'est déterminé, au signe et à l'échelle près, que quand μ_2 est simple. Sur un graphe non connexe, μ_2 = 0 est répétée ; sur le graphe complet K_n, dont les valeurs propres du laplacien sont 0 et n, répétée n − 1 fois, tout vecteur orthogonal à 𝟙 est un vecteur de Fiedler (MAT-005 §5).

Quelques spectres à garder en tête : le chemin à n sommets a les valeurs propres 2 − 2 cos(πk/n) pour k = 0, …, n − 1, donc μ_2 = 4 sin²(π/(2n)) ≈ π²/n² ; l'étoile à n sommets a 0, 1 répétée n − 2 fois, et n. Chung (1997) et le partitionnement spectral (Shi et Malik 2000 ; Ng, Jordan et Weiss 2002 ; von Luxburg 2007) utilisent les **laplaciens normalisés** L_sym = I − D^(-1/2) A D^(-1/2) et L_rw = I − D^-1 A, où D^-1 A est la marche du §2. L'inégalité de Cheeger relie la deuxième valeur propre de L_sym à la conductance h de la meilleure coupe : h²/2 ≤ μ_2(L_sym) ≤ 2h. Le partitionnement spectral plonge chaque sommet par ses coefficients dans les k premiers vecteurs propres d'un tel laplacien, et lance le k-means du MAT-018 sur ce plongement.

### Exercice pratique

Démontrer que xᵀ L x = Σ sur les arêtes {i, j} de w_ij (x_i − x_j)², et en déduire que L est semi-défini positif.

> *Solution :* xᵀ L x = Σ_i d_i x_i² − Σ_(i,j) w_ij x_i x_j, où la seconde somme porte sur les paires ordonnées, de sorte que chaque arête {i, j} y apparaît deux fois et apporte −2 w_ij x_i x_j. Le degré d_i = Σ_j w_ij répartit le poids de chaque arête entre ses deux extrémités, donc la première somme apporte w_ij (x_i² + x_j²) pour chaque arête. Ensemble, chaque arête donne w_ij (x_i² − 2 x_i x_j + x_j²) = w_ij (x_i − x_j)². Une somme de termes positifs ou nuls est positive ou nulle, donc xᵀ L x ≥ 0 pour tout x, et chaque valeur propre de L, le quotient de Rayleigh de son vecteur propre, est ≥ 0.

---

## 5. L'haltère

Joignons deux graphes complets K_5, sur les sommets 0–4 et 5–9, par la seule arête 4–5. Ici, les centralités sont d'accord. Les deux extrémités du pont ont le degré 5 contre 4, et l'intermédiarité 20 chacune, puisque chacune des 4 × 5 paires formées d'un autre sommet de leur propre clique et d'un sommet de l'autre clique passe par elles. Leur proximité vaut 9/13 ≈ 0,692 contre 1/2, leur centralité de vecteur propre est la plus forte, et la distribution stationnaire de la marche sans saut donne à chacune 5/42, contre 4/42 (§2).

Le laplacien a les valeurs propres 0, (7 − √41)/2 ≈ 0,2984, puis 5 répétée sept fois, et (7 + √41)/2 ≈ 6,7016 (exercice). Un vecteur de Fiedler prend une valeur a sur les quatre sommets intérieurs de la première clique, (1 − μ_2) a ≈ 0,7016 a sur l'extrémité du pont, et les valeurs opposées sur la seconde clique, de sorte que son signe coupe l'haltère en ses deux boules, en coupant une arête. La connectivité algébrique est petite, 0,2984 contre 5 à l'intérieur de chaque clique seule : une arête tient les deux moitiés ensemble, et μ_2 le dit. Retirons le pont, et 0 devient une valeur propre double. Les vecteurs égaux à 1 sur une clique et à 0 sur l'autre engendrent le noyau, toute combinaison des deux est un vecteur de Fiedler, et la règle du signe ne veut plus rien dire.

### Exercice pratique

Retrouver les valeurs propres (7 ± √41)/2 du laplacien de l'haltère à partir du vecteur qui vaut a sur les quatre sommets intérieurs de la première clique, b sur le sommet 4, −b sur le sommet 5 et −a sur les quatre sommets intérieurs de la seconde clique.

> *Solution :* En un sommet intérieur de la première clique, de degré 4, (L x)_i = 4a − 3a − b = a − b ; au sommet 4, de degré 5, (L x)_4 = 5b − 4a − (−b) = 6b − 4a. Sur la seconde clique, les équations sont les mêmes avec les signes opposés. Donc x est un vecteur propre pour μ quand a − b = μ a et 6b − 4a = μ b. La première donne b = (1 − μ) a, et la seconde alors 6(1 − μ) − 4 = μ(1 − μ), c'est-à-dire μ² − 7μ + 2 = 0, dont les racines sont (7 ± √41)/2 ≈ 0,2984 et 6,7016. La valeur propre 5 a les vecteurs nuls hors des sommets intérieurs d'une clique et de somme 0 sur eux, trois pour chaque clique, et le vecteur égal à a sur les huit sommets intérieurs et à −4a sur les deux extrémités du pont ; avec 𝟙 pour la valeur propre 0, cela fait bien dix.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python du `Graph` de `crates/ix-graph`, de `compute_laplacian_spectrum` avec le solveur de Jacobi qu'elle appelle (MAT-005 §4), et des gestionnaires ci-dessous. `Graph` garde ses listes d'adjacence dans une `HashMap` et ses ensembles de voisins dans des `HashSet`, que Rust parcourt dans un ordre tiré au hasard à chaque processus ; cet ordre ne change que l'ordre de quelques sommes en virgule flottante, ce qui peut déplacer les derniers bits d'un score mais aucune des décimales données ici. Ces nombres sont des prédictions, que le §7 propose de vérifier.

**Le graphe et ses gestionnaires.** [`Graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L8) stocke, pour chaque sommet, une liste de paires (voisin, poids), et [`add_undirected_edge`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L37) ajoute les deux sens. L'outil MCP `ix_graph` appelle [`graph_ops`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2815), qui construit un graphe à `n_nodes` sommets, rejette une arête dont une extrémité sort de l'intervalle, traite les arêtes comme [orientées sauf indication contraire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2832), prend un poids absent pour [1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2860), et propose l'algorithme de Dijkstra, les plus courts chemins, PageRank, les parcours en largeur et en profondeur et un tri topologique, avec pour PageRank un [amortissement de 0,85](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2889) et [100 itérations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2890) par défaut. Les quatre centralités du §3 sont disponibles en SQL par une fonction table de `crates/ix-duck`, qui calcule par exemple [la centralité de vecteur propre avec 100 itérations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L482), et dont l'analyseur d'arêtes [rejette les poids négatifs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L141) ; l'intermédiarité est aussi derrière `ix_mesh_correlate`. La boucle intérieure de [`pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L185) est :

```rust
            for (&node, edges) in &self.adjacency {
                let out = out_degree[&node] as f64;
                if out > 0.0 {
                    let share = damping * rank[&node] / out;
                    for &(neighbor, _) in edges {
                        *new_rank.get_mut(&neighbor).unwrap() += share;
                    }
                }
            }
```

**Le laplacien.** [`compute_laplacian_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L420) construit L à partir d'une liste d'arêtes non pondérées, appelle le [solveur de Jacobi complet](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L449) du MAT-005, [ramène à 0 les valeurs propres négatives](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L454), renvoie les trois plus petites avec μ_2, μ_2 − μ_1 et un [vecteur de Fiedler](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L477), et compte les composantes ainsi :

```rust
    let zero_tol = 1e-6;
    let n_components = eigenvalues_all
        .iter()
        .filter(|&&e| e < zero_tol)
        .count()
        .max(1);
```

- **PageRank abandonne le rang des nœuds pendants.** Dans la boucle ci-dessus, un sommet avec `out` = 0 ne transmet rien : c'est l'itération du §2 qui abandonne leur rang, avec pour n [le nombre de sommets de la table](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L186). Sur le graphe de citations du §2, `ix_graph` renvoie 0,05, 0,05 et 0,135, de somme 0,235. La fonction DuckDB `ix_pagerank` divise par la somme, comme le dit son commentaire, [« so dangling-node mass leakage doesn't break the probability-distribution contract »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L161). D'après l'exercice du §2, c'est plus que cosmétique : une fois la convergence atteinte, elle renvoie exactement PageRank avec des sauts uniformes depuis les nœuds pendants, ici 10/47, 10/47 et 27/47. L'outil MCP renvoie le vecteur brut. Le propre test de fumée d'IX [fournit le graphe des dépendances](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L183) de `ix_cargo_deps` à `ix_graph`, avec une arête de chaque crate vers chaque crate d'IX dont elle dépend, de sorte que toute crate sans dépendance IX est un nœud pendant ; le test se contente de [compter les entrées](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/cargo_deps_smoke.rs#L200).
- **PageRank ignore les poids.** La boucle lit chaque arête comme [`(neighbor, _)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L207) : chaque lien sortant reçoit la même part, quel que soit son poids, de sorte qu'une liste d'arêtes pondérées donne les mêmes rangs que la liste non pondérée. Le pas-à-pas d'IX sur le maillage exécutable [l'a rencontré](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/walkthroughs/executable-pipeline-mesh.md#L57) : un PageRank sur les distances deux à deux d'un graphe complet est sorti uniforme, et le pas-à-pas l'explique comme une propriété des graphes complets. L'uniformité vient de ce code, pour lequel un graphe complet est régulier quels que soient ses poids ; une marche pondérée, de probabilités w_ij/Σ_k w_ik, est attirée par les sommets de plus grand poids total, comme d'après le §2 elle l'est par le fort degré.
- **Le nombre d'itérations est fixe.** `pagerank` fait exactement `iterations` passes et ne teste rien. D'après le §2, l'erreur vaut au plus 2αᵏ : négligeable pour α = 0,85 et 100 passes, pas pour α = 0,99. Sur l'étoile à trois feuilles, avec chaque arête dans les deux sens, α = 0,99 et 100 passes, la transcription prédit 0,4077 pour le centre et 0,1974 pour chaque feuille, contre les valeurs exactes 0,4987 et 0,1671, une erreur de 0,1821 en norme ℓ1. L'étoile est bipartie, donc l'erreur change de signe à chaque passe et ne diminue que du facteur 0,99. Le catalogue que `ix_explain_algorithm` envoie au client donne comme hyperparamètres de PageRank [« damping » et « tol »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5861) ; il n'y a aucune tolérance.
- **Le gestionnaire ne vérifie ni α ni le nombre d'itérations.** Il lit les deux avec un repli sur la valeur par défaut, de sorte qu'un amortissement non numérique devient 0,85, et il accepte n'importe quel nombre, là où `ix_pagerank` rejette [α hors de [0, 1]](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L165) et [moins d'une itération](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L169). Avec α = 1,5 sur le graphe de citations, `ix_graph` renvoie −1/6, −1/6 et −2/3 ; avec 0 itération, il renvoie le départ uniforme.
- **Le commentaire du vecteur propre donne une mauvaise raison à une bonne méthode.** [`eigenvector_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L333) itère avec A + I, comme au §3, et son commentaire dit que A + I [« has strictly positive eigenvalues »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L330). Sur l'étoile du propre test d'IX, l'une d'elles vaut 1 − √3 ≈ −0,732. La méthode converge quand même, pour la raison donnée au §3 : depuis le départ uniforme, l'erreur du rapport centre sur feuille diminue du facteur (√3 − 1)/(√3 + 1) = 2 − √3 ≈ 0,268 par passe, et la transcription prédit √3 ≈ 1,7321 à la précision double après 30 des 100 passes. Le test exige [un rapport supérieur à 1,5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L498), condition que l'itération non décalée, uniforme après 100 passes, ne remplit pas. Sur le triangle 0–1–2 avec l'arête séparée 3–4, les scores de 3 et de 4 diminuent du facteur 2/3 par passe, et la transcription prédit environ 1,4 × 10^-18 après 100 passes.
- **L'intermédiarité est un compte, pas une fraction.** Le commentaire de [`betweenness_centrality`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L363) parle de [« the fraction of shortest paths through each node »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L361), mais le code additionne les fractions sur toutes les paires et [divise le total par deux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L400), pour les paires vues depuis leurs deux extrémités, sans diviser par le nombre de paires : 3 pour le centre de l'étoile du test, 10 avec cinq feuilles, 20 pour les extrémités du pont de l'haltère. Les scores de graphes de tailles différentes ne se comparent pas. Le test de l'étoile exige seulement que le score du centre soit [strictement positif](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L508).
- **`ix_mesh_correlate` désigne un centre quand il n'y en a pas.** [`mesh_correlate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1214) relie les séries dont la corrélation de Pearson atteint le seuil en valeur absolue, calcule leur [intermédiarité](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1239), et renvoie comme `hub` le sommet choisi par [`max_by`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1244), qui renvoie le dernier de plusieurs maxima égaux. Quand aucune paire n'atteint le seuil, ou quand toutes l'atteignent, tous les scores valent 0 et `hub` est la dernière série : pour les trois séries (1, −1, 1, −1), (1, 1, −1, −1) et (1, −1, −1, 1), deux à deux non corrélées, la transcription prédit `hub` = 2. Sur un chemin 0–1–2–3, où 1 et 2 sont à égalité, il renvoie aussi 2.
- **Dijkstra accepte des poids négatifs.** [`dijkstra`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L92) est la variante paresseuse : elle [saute une entrée périmée du tas](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L108) et développe de nouveau un sommet chaque fois que sa distance baisse. Avec des poids négatifs et sans cycle négatif, elle renvoie encore les bonnes distances, éventuellement après un nombre exponentiel de pas (Johnson 1973). Le catalogue d'IX recommande Dijkstra pour des [« non-negative weights »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5853), mais le gestionnaire prend n'importe quel nombre pour poids. L'analyseur DuckDB rejette les poids négatifs, et son commentaire dit qu'un poids négatif [« gives wrong paths and a negative cycle never settles »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L140) : la seconde moitié est juste, mais cette variante paresseuse donne encore les bons chemins, au pire lentement, et le PageRank que nomme le même commentaire ignore les poids. Avec `directed` à false, une seule arête négative est un cycle négatif de deux arêtes, et la boucle abaisse les deux distances tour à tour : sur la seule arête 0–1 de poids −1, la transcription atteint −12 et −11 après douze pas, et la boucle ne s'arrêterait que vers −2^53, où soustraire 1 ne change plus un double, après environ 9 × 10^15 pas. C'est prédit à partir du code, pas exécuté ; le §7 l'exécute sous un délai limite.
- **Le gestionnaire vérifie les arêtes mais pas la source.** Une extrémité d'arête hors du graphe est une erreur, mais [`source`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L2870) n'est pas vérifiée : depuis la source 7 sur un graphe à trois sommets, Dijkstra renvoie la distance 0 pour un sommet 7 qui n'existe pas et ∞ pour les trois autres, que la sortie JSON écrit `null`, comme pour tout sommet inaccessible.
- **Les commentaires du laplacien décrivent un autre algorithme.** Ils annoncent une itération [« inverse power »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L400), puis une itération de la puissance sur une matrice décalée [avec déflation de Gram–Schmidt](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L417), alors que le code exécute la méthode de Jacobi complète, en O(n³) opérations par balayage. Les boucles et les arêtes hors de l'intervalle sont [ignorées sans un mot](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L436). Comme les valeurs propres sont ramenées à 0, `spectral_gap`, μ_2 − μ_1, vaut μ_2 aux arrondis près et répète `algebraic_connectivity`. Rien en dehors de `physics.rs` n'appelle la fonction, et aucun outil MCP ne l'expose.
- **Les composantes sont comptées avec un seuil absolu.** Une valeur propre compte comme nulle sous [10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L462). Un graphe connexe de diamètre D a μ_2 ≥ 4/(n · D) (Mohar 1991), et n · D ≤ n(n − 1) < 4 × 10^6 quand n ≤ 2000, donc aucun graphe connexe d'au plus 2000 sommets ne descend aussi bas. De plus grands le peuvent : le chemin à n sommets a μ_2 = 4 sin²(π/(2n)), sous 10^-6 à partir de n = 3142, où il vaut 0,99974 × 10^-6, de sorte que la fonction compterait un chemin connexe de 3142 sommets comme 2 composantes. Un parcours en largeur, comme dans [`connected_components`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L224), les compte exactement.
- **Le vecteur de Fiedler est renvoyé même quand il n'est pas déterminé.** Quand μ_2 est répétée, le vecteur renvoyé est un vecteur du sous-espace propre, choisi par les rotations. Sur K_4, la transcription prédit (−0,2887 ; −0,2887 ; −0,2887 ; 0,866), soit (−1, −1, −1, 3)/√12. Sur l'haltère sans son pont, elle prédit 1/√5 ≈ 0,4472 sur la première clique et 0 sur la seconde : un vecteur du noyau, qui sépare les cliques par des coefficients nuls et non nuls, pas par le signe. Rien ne signale l'un ou l'autre cas.
- **Certains tests passeraient sur un code faux.** [`test_pagerank`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L574) utilise un 3-cycle orienté, sur lequel le vecteur uniforme est un point fixe pour tout α, et exige des rangs égaux [à 0,01 près](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-graph/src/graph.rs#L585) : la transcription renvoie exactement 1/3 pour α = 0,85, 0 et 1, et après 0 itération. Un PageRank qui ignorerait α, abandonnerait les sauts ou n'itérerait jamais passerait. [`test_laplacian_disconnected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L617) exige [au moins 2 composantes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L621) pour les arêtes 0–1 et 2–3, dont les valeurs propres sont 0, 0, 2 et 2 : un seuil de 3 donnerait 4 composantes et passerait encore. [`test_laplacian_connected`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L606) exige μ_2 [supérieure à 0,5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/physics.rs#L610) sur K_4, où elle vaut 4.
- **Autres lacunes.** Il n'y a ni laplacien normalisé, ni partitionnement spectral, ni constante de Cheeger, ni PageRank pondéré ou personnalisé, ni test de convergence dans PageRank ou dans la centralité de vecteur propre, ni intermédiarité normalisée, ni plus courts chemins avec poids négatifs, ni opération MCP pour les centralités, les composantes ou le laplacien.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Montrer qu'au point fixe du PageRank d'IX, la somme s des rangs vérifie s = (1 − α) + α (s − x_D), où x_D est le rang total des nœuds pendants, et le vérifier sur le graphe de citations.

> *Solution :* Chaque passe fixe chaque sommet à (1 − α)/n plus les parts qu'il reçoit. Sommés sur les n sommets, les premiers termes donnent 1 − α, et les parts donnent α fois le rang des sommets qui ont des liens sortants, puisqu'un tel sommet transmet α fois tout son rang, alors qu'un nœud pendant ne transmet rien : α (s − x_D). Au point fixe, s = (1 − α) + α (s − x_D), donc s = 1 − α x_D/(1 − α) : avec α = 0,85, il manque à la somme, pour atteindre 1, 17/3 ≈ 5,67 fois le rang des nœuds pendants. Sur le graphe de citations, x_D = 0,135, et s = 1 − (17/3) · 0,135 = 1 − 0,765 = 0,235.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **La fuite.** Appeler `graph_ops` avec l'opération `pagerank` sur le graphe de citations du §2, puis `ix_pagerank` dans une connexion DuckDB du même processus sur les mêmes arêtes. Prédiction : 0,05, 0,05 et 0,135, de somme 0,235 ; puis 10/47, 10/47 et 27/47, environ 0,2128, 0,2128 et 0,5745.
2. **La convergence lente.** Appeler `graph_ops` avec `pagerank` sur l'étoile à trois feuilles, `directed` à false, un amortissement de 0,99, et 100 puis 2000 itérations. Prédiction : 0,4077 pour le centre, puis 0,4987.
3. **Le cerf-volant.** Construire le cerf-volant de Krackhardt et appeler les quatre centralités et `pagerank`. Prédiction : centralités de degré et de vecteur propre maximales en Diane (3), proximité maximale en Fernando et Garth (5 et 6), avec 9/14, intermédiarité maximale en Heather (7), avec 14, et PageRank maximal en Diane, avec 0,1471.
4. **Le décalage.** Appeler `eigenvector_centrality` sur l'étoile avec 30 puis 100 itérations, puis sur le triangle avec l'arête séparée du §6. Prédiction : un rapport centre sur feuille de √3 ≈ 1,7321 les deux fois, puis des scores d'environ 1,4 × 10^-18 sur l'arête.
5. **Les spectres.** Appeler `compute_laplacian_spectrum` sur l'haltère du §5, sur l'haltère sans son pont, sur le triangle 0–1–2 avec l'arête 3–4 et le sommet isolé 5, et sur K_4. Prédiction : 1 composante, μ_2 = 0,2984 et un vecteur de Fiedler d'environ ±0,3336 sur les sommets intérieurs et ±0,2341 sur les extrémités du pont, avec un signe par boule ; 2 composantes et le vecteur du §6 ; 3 composantes ; 1 composante, μ_2 = 4 et le vecteur du §6.
6. **Le centre du maillage.** Appeler `mesh_correlate` sur les trois séries non corrélées du §6 avec le seuil par défaut de 0,5. Prédiction : aucune arête, toutes les intermédiarités à 0, et `hub` = 2.
7. **Les poids négatifs.** Appeler `graph_ops` avec `dijkstra` depuis le sommet 0 sur les arêtes 0 → 1 de poids 2, 0 → 2 de poids 5 et 2 → 1 de poids −4, puis, dans un processus enfant avec un délai limite de 10 secondes, sur la seule arête 0–1 de poids −1 avec `directed` à false. Prédiction : les distances 0, 1 et 5 ; puis le délai limite expire.

### Exercice pratique

Pourquoi l'étape 1 ne dépend-elle pas du nombre d'itérations, pourvu qu'il y en ait au moins 2, alors que l'étape 2 en demande des milliers ?

> *Solution :* Le graphe de citations n'a pas de cycle. Après une passe, les rangs de 0 et de 1 valent 0,05 pour de bon, puisque rien ne pointe vers eux, et après la deuxième, le rang de 2 ne dépend que des leurs : chaque passe ultérieure répète les mêmes valeurs. L'étoile est bipartie, donc l'erreur change de signe à chaque passe et sa taille diminue du facteur α = 0,99 par passe. Après 100 passes, il reste 0,99^100 ≈ 0,366 de l'erreur initiale, et après 2000, environ 2 × 10^-9.

---

## 8. Pièges courants

- **Lire un vecteur PageRank brut comme une distribution.** Avec des nœuds pendants, sa somme est inférieure à 1 ; diviser par la somme, ce qui donne PageRank avec des sauts uniformes depuis eux, et rapporter le rang qu'ils détenaient.
- **Attendre des poids qu'ils changent le PageRank d'IX.** Ils ne le changent pas ; construire soi-même les probabilités de transition pondérées, ou dire que le classement est non pondéré.
- **Désigner le sommet le plus central sans nommer la mesure.** Les centralités de degré, de proximité, d'intermédiarité et de vecteur propre répondent à des questions différentes, et sur le cerf-volant elles désignent trois sommets différents.
- **Comparer des intermédiarités brutes d'un graphe à l'autre.** Diviser d'abord par le nombre de paires, (n − 1)(n − 2)/2 pour un graphe non orienté.
- **Lancer l'itération de la puissance avec A sur un graphe biparti.** Décaler de l'identité, ou détecter une oscillation de période 2, avant de se fier au résultat.
- **Se fier à un nombre fixe d'itérations avec α proche de 1.** La borne d'erreur est 2αᵏ ; avec α = 0,99, 100 passes sont loin de suffire.
- **Compter les composantes à partir des valeurs propres.** Un seuil absolu confond de grands graphes faiblement connexes avec des graphes non connexes ; un parcours en largeur les compte exactement.
- **Lire un vecteur de Fiedler quand μ_2 est nulle ou répétée.** C'est alors un vecteur d'un sous-espace propre, et ses signes ne veulent rien dire ; vérifier d'abord la multiplicité.
- **Passer une liste d'arêtes non orientées à `ix_graph` sans mettre `directed` à false.** Le gestionnaire traite alors chaque arête comme un sens unique.
- **Donner des poids négatifs à l'algorithme de Dijkstra.** Utiliser plutôt Bellman–Ford ; une arête négative non orientée est déjà un cycle négatif.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Matrice d'adjacence** | La matrice A avec A_ij = 1, ou un poids, pour une arête de i à j, et 0 sinon |
| **Degré** | Le nombre de voisins d'un sommet, ou la somme des poids de ses arêtes |
| **Vecteur de Perron** | Le vecteur propre à coefficients strictement positifs de la plus grande valeur propre de la matrice d'adjacence d'un graphe connexe |
| **Graphe biparti** | Un graphe dont les sommets se répartissent en deux côtés avec chaque arête entre les deux ; son spectre est symétrique par rapport à 0 |
| **Facteur d'amortissement** | La probabilité α que le surfeur aléatoire suive un lien au lieu de sauter |
| **Nœud pendant** | Un sommet sans lien sortant |
| **PageRank** | La distribution stationnaire de la matrice Google |
| **Centralité d'intermédiarité** | La somme, sur les paires d'autres sommets, de la fraction de leurs plus courts chemins qui passent par un sommet |
| **Centralité de vecteur propre** | Le coefficient d'un sommet dans le vecteur de Perron |
| **Laplacien** | L = D − A, dont la forme quadratique somme (x_i − x_j)² sur les arêtes |
| **Connectivité algébrique** | La deuxième plus petite valeur propre μ_2 du laplacien, strictement positive exactement quand le graphe est connexe |
| **Vecteur de Fiedler** | Un vecteur propre de μ_2, dont les signes donnent un partage spectral du graphe |

---

## Auto-évaluation

**1. Un collègue classe les crates d'un espace de travail avec le PageRank de `ix_graph` sur le graphe de `ix_cargo_deps`, et constate que les rangs n'ont pas pour somme 1. Quelque chose est-il cassé ?**
> Pas forcément. IX abandonne le rang des nœuds pendants, et toute crate sans dépendance IX en est un, donc le vecteur brut a pour somme 1 − α x_D/(1 − α), où x_D est leur rang total (§6). Diviser par la somme donne PageRank avec des sauts uniformes depuis ces crates (§2), ce que renvoie `ix_pagerank`. Signaler aussi que les poids sont ignorés, et que les arêtes vont d'une crate vers ses dépendances, de sorte que le rang s'écoule vers les crates dont les autres dépendent.

**2. Pourquoi l'itération de la puissance avec A ne trouve-t-elle pas la centralité de vecteur propre d'une étoile, et pourquoi l'itération d'IX avec A + I fonctionne-t-elle alors que son commentaire donne la mauvaise raison ?**
> Une étoile est bipartie, donc −λ_1 est une valeur propre en plus de λ_1, et l'itéré alterne : depuis (1, 1, 1, 1), il redevient uniforme après tout nombre pair de pas. Avec A + I, les valeurs propres deviennent λ_i + 1, et comme λ_n ≥ −λ_1, |λ_n + 1| < λ_1 + 1 : le vecteur de Perron domine strictement. Les valeurs propres décalées ne sont pas toutes positives, contrairement à ce que dit le commentaire, puisque l'une de celles de l'étoile vaut 1 − √3 ; c'est la domination stricte en module dont l'itération a besoin.

**3. `compute_laplacian_spectrum` annonce 2 composantes et renvoie un vecteur de Fiedler. Que vérifiez-vous avant de vous en servir ?**
> Que le graphe est vraiment non connexe : une valeur propre compte comme nulle sous un seuil absolu de 10^-6, qu'atteint aussi un chemin connexe de 3142 sommets ou plus, donc compter les composantes par un parcours en largeur. Si le graphe est non connexe, μ_2 = 0 est répétée et le vecteur est l'un des nombreux vecteurs du noyau, dont les signes ne veulent rien dire : couper d'abord par composantes, et prendre le vecteur de Fiedler de chaque composante.

**4. Sur le cerf-volant de Krackhardt, quel sommet est le plus central ?**
> Cela dépend de la question. Diane a le plus de liens et la plus forte centralité de vecteur propre, Fernando et Garth sont les plus proches de tous, à 9/14, et Heather contrôle le seul passage vers Ike et Jane, avec une intermédiarité de 14. Un rapport doit nommer la mesure et dire pourquoi elle convient à la question.

**Critères de réussite :** Décrire un graphe par A, D et L ; définir PageRank, son traitement des nœuds pendants et la borne de son erreur ; calculer et comparer les quatre centralités ; démontrer que L est semi-défini positif et que ses valeurs propres nulles comptent les composantes ; couper un graphe avec le vecteur de Fiedler et dire quand il n'est pas déterminé ; et retracer où les commentaires, le catalogue, les gestionnaires et les tests d'IX promettent plus que ce que le code fournit.

---

## Bases de recherche

- E. W. Dijkstra, « A note on two problems in connexion with graphs », *Numerische Mathematik* 1, 1959 : l'algorithme de plus court chemin
- P. Bonacich, « Factoring and weighting approaches to status scores and clique identification », *Journal of Mathematical Sociology* 2, 1972 : la centralité de vecteur propre
- D. B. Johnson, « A note on Dijkstra's shortest path algorithm », *Journal of the ACM* 20, 1973 : un travail exponentiel avec des poids négatifs
- M. Fiedler, « Algebraic connectivity of graphs », *Czechoslovak Mathematical Journal* 23, 1973 : la connectivité algébrique
- M. Fiedler, « A property of eigenvectors of nonnegative symmetric matrices and its application to graph theory », *Czechoslovak Mathematical Journal* 25, 1975 : les côtés connexes du vecteur de Fiedler
- L. C. Freeman, « A set of measures of centrality based on betweenness », *Sociometry* 40, 1977 : l'intermédiarité
- D. Krackhardt, « Assessing the political landscape: structure, cognition, and power in organizations », *Administrative Science Quarterly* 35, 1990 : le cerf-volant
- B. Mohar, « Eigenvalues, diameter, and mean distance in graphs », *Graphs and Combinatorics* 7, 1991 : la borne inférieure de μ_2
- S. Wasserman et K. Faust, *Social Network Analysis: Methods and Applications*, Cambridge University Press, 1994 : les centralités, et la proximité sur les graphes non connexes
- F. R. K. Chung, *Spectral Graph Theory*, American Mathematical Society, 1997 : le laplacien normalisé et l'inégalité de Cheeger
- S. Brin et L. Page, « The anatomy of a large-scale hypertextual Web search engine », *Computer Networks and ISDN Systems* 30, 1998 : PageRank
- L. Page, S. Brin, R. Motwani et T. Winograd, « The PageRank citation ranking: bringing order to the Web », rapport technique du Stanford InfoLab, 1999 : le surfeur aléatoire et le facteur d'amortissement
- J. Shi et J. Malik, « Normalized cuts and image segmentation », *IEEE Transactions on Pattern Analysis and Machine Intelligence* 22, 2000 : les coupes normalisées
- U. Brandes, « A faster algorithm for betweenness centrality », *Journal of Mathematical Sociology* 25, 2001 : l'algorithme de Brandes
- A. Y. Ng, M. I. Jordan et Y. Weiss, « On spectral clustering: analysis and an algorithm », *Advances in Neural Information Processing Systems* 14, 2002 : le partitionnement spectral
- T. H. Haveliwala et S. D. Kamvar, « The second eigenvalue of the Google matrix », rapport technique de l'université Stanford, 2003 : la deuxième valeur propre vaut au plus α en module
- A. N. Langville et C. D. Meyer, *Google's PageRank and Beyond: The Science of Search Engine Rankings*, Princeton University Press, 2006 : les nœuds pendants et la forme en système linéaire
- U. von Luxburg, « A tutorial on spectral clustering », *Statistics and Computing* 17, 2007 : le partitionnement spectral et les laplaciens de graphe
- A. E. Brouwer et W. H. Haemers, *Spectra of Graphs*, Springer, 2012 : les spectres des matrices d'adjacence et des laplaciens
- R. A. Horn et C. R. Johnson, *Matrix Analysis*, 2e éd., Cambridge University Press, 2013 : le théorème de Perron–Frobenius
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
