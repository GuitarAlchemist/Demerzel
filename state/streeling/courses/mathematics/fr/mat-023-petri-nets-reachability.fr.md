---
module_id: mat-023-petri-nets-reachability
department: mathematics
course: Réseaux de Petri et accessibilité
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "55 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Réseaux de Petri et accessibilité — Ce que l'énumération prouve, et quand elle doit répondre Unknown

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 55 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Définir un réseau place/transition et sa règle de tir, et tirer des séquences à la main
- Construire un graphe d'accessibilité en largeur, et y lire les interblocages et leurs témoins les plus courts
- Compter les marquages accessibles avec une matrice de transfert, et expliquer pourquoi les espaces d'états croissent exponentiellement
- Prouver qu'un réseau est non borné avec un témoin de pompage, et dire ce que l'échec à en trouver un ne prouve pas
- Lire la vivacité et la réversibilité sur les composantes fortement connexes d'un graphe d'accessibilité fini
- Utiliser la matrice d'incidence et les P-invariants pour prouver la bornitude et l'exclusion mutuelle sans énumérer, et expliquer pourquoi l'équation d'état n'est qu'une condition nécessaire
- Retracer ce que décide la crate `ix-petri` d'IX, lesquels de ses verdicts survivent à une recherche tronquée, et où elle doit répondre `Unknown`

---

## 1. Places, transitions et règle de tir

Un **réseau place/transition** a un ensemble fini de places, un ensemble fini de transitions, et des arcs pondérés qui vont d'une place à une transition ou d'une transition à une place, jamais entre deux places ni entre deux transitions. Notons Pre(p, t) le poids de l'arc de la place p vers la transition t, et Post(p, t) le poids de l'arc de t vers p, avec 0 là où il n'y a pas d'arc. Un **marquage** m donne à chaque place un nombre de jetons m(p) ≥ 0, et le réseau part d'un marquage initial m0. Une transition t est **activée** en m lorsque m(p) ≥ Pre(p, t) pour toute place p. La **tirer** donne le marquage m′ = m − Pre(·, t) + Post(·, t) : elle consomme Pre(p, t) jetons dans chaque place d'entrée et en produit Post(p, t) dans chaque place de sortie. Une seule transition est tirée à la fois, et un tir est indivisible.

Un tampon à une case a deux places, `empty` avec un jeton et `full` sans jeton, et deux transitions : `produce` déplace le jeton de `empty` vers `full`, et `consume` le ramène. En m0 seule `produce` est activée ; la tirer donne full = 1, où seule `consume` est activée, et tirer celle-ci redonne m0. Une place peut être à la fois une entrée et une sortie d'une même transition, une **boucle** : la transition a besoin du jeton pour être tirée et le remet en place.

Deux faits découlent de la règle, et les sections suivantes reposent sur eux. **Monotonie** : si une séquence σ peut être tirée depuis m, et que m′ ≥ m place par place, alors σ peut être tirée depuis m′, car des jetons supplémentaires ne désactivent jamais une transition. **Linéarité** : le changement produit par σ est la somme des changements de ses transitions, quel que soit leur ordre, de sorte que σ modifie m′ exactement du même vecteur que m.

### Exercice pratique

La place p contient 2 jetons et a un arc de poids 3 vers la transition t, qui a un arc de sortie vers une place vide q. La transition t est-elle activée ? Et si p contenait 5 jetons ?

> *Solution :* Non : t a besoin de 3 jetons de p, et p en a 2. Avec 5 jetons, t est activée, et la tirer laisse 2 jetons dans p et 1 dans q. Ensuite t est de nouveau désactivée : elle est tirée exactement une fois.

---

## 2. Le graphe d'accessibilité

Un marquage est **accessible** lorsqu'une séquence de tir y mène depuis m0. Le **graphe d'accessibilité** a pour sommets les marquages accessibles, et un arc de m vers m′ étiqueté t chaque fois que tirer t en m donne m′. On le construit en largeur : partir de m0, prendre les marquages dans l'ordre où ils ont été trouvés, tirer chaque transition activée en chacun d'eux, et ajouter chaque nouveau marquage en fin de file. Un marquage est **mort** lorsqu'aucune transition n'y est activée, et un réseau est **sans interblocage** lorsqu'aucun marquage accessible n'est mort. La recherche en largeur trouve chaque marquage d'abord le long d'une séquence de tir la plus courte, si bien que remonter le parent de chaque marquage jusqu'à m0 donne un **témoin** le plus court : une séquence que chacun peut rejouer avec la règle de tir.

Dans le dîner des philosophes de Dijkstra, n philosophes sont assis autour d'une table, avec une fourchette entre chaque paire de voisins. Le philosophe i pense, prend la fourchette gauche i, puis la fourchette droite i + 1 (mod n), mange, et repose les deux fourchettes. Sous forme de réseau, il y a les places THINK_i, WAIT_i (fourchette gauche en main), EAT_i et FORK_i, avec un jeton dans chaque THINK_i et chaque FORK_i, et les transitions TAKE_LEFT_i, TAKE_RIGHT_i et RELEASE_i. Pour n = 3, le graphe d'accessibilité a 14 marquages et 27 arcs. Un seul marquage est mort : chaque philosophe tient une fourchette gauche et attend une fourchette droite que tient un voisin. Son témoin est TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2. Si chaque philosophe prend au contraire les deux fourchettes en une seule transition, il y a 4 marquages accessibles, où personne ne mange ou exactement un des trois mange, et aucun n'est mort.

### Exercice pratique

Deux voies de travail partagent un arbre de travail et une pile de stash. La voie 0 prend l'arbre, puis le stash ; la voie 1 prend le stash, puis l'arbre. Chaque voie rend les deux à la fin de son travail et redevient prête. Trouvez un marquage mort et un témoin le plus court. Combien de marquages sont accessibles ?

> *Solution :* La voie 0 prend l'arbre et la voie 1 prend le stash. Chaque voie tient alors sa première ressource et attend celle que tient l'autre voie, et plus rien n'est activé. Le témoin a deux tirs, une prise par voie. Les marquages accessibles sont : les deux voies prêtes ; la voie 0 tenant l'arbre ; la voie 0 tenant les deux ; la voie 1 tenant le stash ; la voie 1 tenant les deux ; et le marquage mort. Cela fait six.

---

## 3. Compter les marquages accessibles

L'espace d'états d'un réseau croît bien plus vite que le réseau. Quand les philosophes prennent les deux fourchettes à la fois, un marquage accessible est un ensemble de philosophes qui mangent, dont aucun n'est voisin d'un autre, puisque des voisins partagent une fourchette, et chacun de ces ensembles est accessible en laissant ses membres prendre leurs fourchettes l'un après l'autre. Compter ces ensembles est un calcul de **matrice de transfert**. On fait le tour de la table en notant si chaque philosophe mange, avec la règle qu'un mangeur est suivi d'un non-mangeur. La matrice A = [[1, 1], [1, 0]] liste les pas permis, et le nombre de marches permises qui se referment après n pas est la trace de A^n. Cette trace vaut φ^n + ψ^n, où φ = (1 + √5)/2 et ψ = (1 − √5)/2 sont les valeurs propres de A : ce sont les nombres de Lucas.

Quand les philosophes prennent d'abord la fourchette gauche, chacun pense (T), attend en tenant la fourchette gauche (W) ou mange (E). La fourchette i est tenue par le philosophe i en W ou en E, et par le philosophe i − 1 en E. Le seul motif interdit est donc un E suivi d'un W ou d'un E. Dans l'ordre T, W, E, la matrice de transfert est M = [[1, 1, 1], [1, 1, 1], [1, 0, 0]]. Son polynôme caractéristique est λ(λ² − 2λ − 1), de valeurs propres 0 et 1 ± √2, si bien que le nombre de configurations permises est Q(n) = (1 + √2)^n + (1 − √2)^n, les nombres de Pell-Lucas, qui vérifient Q(n) = 2Q(n − 1) + Q(n − 2). Toute configuration permise est accessible : laisser les mangeurs prendre d'abord leurs deux fourchettes, puis ceux qui attendent prendre leur fourchette gauche. Le §6 montre qu'aucun autre marquage ne l'est. L'énumération en largeur concorde :

| n | 2 | 3 | 4 | 5 | 6 | 12 | 13 |
|---|---|---|---|---|---|---|---|
| Fourchette gauche d'abord : marquages accessibles | 6 | 14 | 34 | 82 | 198 | 39 202 | 94 642 |
| Deux fourchettes à la fois : marquages accessibles | 3 | 4 | 7 | 11 | 18 | 322 | 521 |

Chaque philosophe supplémentaire multiplie la première ligne par environ 1 + √2, et la seconde par environ φ. Treize philosophes ont déjà 94 642 marquages accessibles, plus que les 50 000 que l'analyseur d'IX explore par défaut (§7).

### Exercice pratique

Calculez Q(6) à partir de Q(4) = 34 et Q(5) = 82, et vérifiez le résultat avec (1 + √2)^6 + (1 − √2)^6.

> *Solution :* Q(6) = 2 × 82 + 34 = 198. Comme (1 + √2)² = 3 + 2√2, le cube donne (1 + √2)^6 = (3 + 2√2)³ = 27 + 54√2 + 72 + 16√2 = 99 + 70√2. De même (1 − √2)^6 = 99 − 70√2, et la somme vaut 198.

---

## 4. Bornitude et témoin de pompage

Une place est **k-bornée** lorsqu'aucun marquage accessible n'y met plus de k jetons, et un réseau est **borné** lorsqu'un même k convient pour toutes les places. Un réseau 1-borné est dit **sauf**. Un réseau borné a un nombre fini de marquages accessibles, donc la recherche en largeur se termine. Un réseau non borné en a une infinité, et aucune énumération de ceux-ci ne se termine.

Supposons que m soit accessible, que m′ soit accessible depuis m par une séquence σ, et que m′ **couvre strictement** m : m′ ≥ m place par place, et m′ ≠ m. Alors le réseau est non borné. Par monotonie, σ peut être tirée de nouveau depuis m′, et par linéarité elle ajoute le même vecteur d = m′ − m, positif ou nul et non nul. Répéter σ atteint m + kd pour tout k, donc une place croît sans limite. La paire (m, m′), avec la séquence qui les relie, est un **témoin de pompage**.

La réciproque est ce qui rend la bornitude décidable. Si le réseau est non borné, l'arbre en largeur des marquages accessibles distincts est infini, et chaque marquage a un nombre fini d'enfants, donc par le lemme de Kőnig l'arbre a une branche infinie m0, m1, m2, …. Par le **lemme de Dickson**, toute suite infinie de vecteurs d'entiers naturels a des indices i < j avec m_i ≤ m_j, et sur une branche de marquages distincts m_i ≠ m_j : la branche contient un témoin de pompage. Karp et Miller ont tiré de cet argument l'arbre de couverture, qui décide la bornitude pour tout réseau. Aucun des deux lemmes ne borne l'écart entre i et j, si bien qu'une recherche qui ne cherche la paire qu'à un nombre fixe de pas en arrière peut la manquer (§7).

### Exercice pratique

Un réseau a une place `queue` et une transition `grow`, sans arc d'entrée et avec un arc de sortie vers `queue`. Donnez un témoin de pompage. Ajoutez ensuite une place `ticket` contenant un jeton, avec un arc de `ticket` vers `grow` et un arc de `grow` vers `ticket`. Le réseau est-il toujours non borné ?

> *Solution :* En m0 la file est vide, et tirer `grow` donne queue = 1, qui couvre strictement m0 : le témoin est m0, queue = 1, et la séquence `grow`. Avec le ticket, `grow` prend le ticket et le remet, donc elle peut toujours être tirée indéfiniment. Le témoin devient ticket = 1, puis ticket = 1 et queue = 1, toujours avec `grow`. Une boucle ne limite pas le nombre de tirs d'une transition.

---

## 5. Vivacité, réversibilité et composantes fortement connexes

Une transition est **morte** lorsqu'aucun marquage accessible ne l'active, et un réseau sans transition morte est **quasi-vivant** (niveau L1 dans la classification de Murata). Un réseau est **vivant** (niveau L4) lorsque, depuis tout marquage accessible, toute transition peut encore être tirée après une certaine séquence. Un réseau est **réversible** lorsque m0 peut être atteint de nouveau depuis tout marquage accessible. Ces propriétés diffèrent. Prenez une place `q` avec un jeton, une transition `loop` qui prend le jeton et le remet, et une transition `never` dont la place d'entrée est vide. Ce réseau est sans interblocage, puisque `loop` est toujours activée, mais il n'est ni quasi-vivant ni vivant.

Sur un graphe d'accessibilité fini, ces propriétés se lisent sur les **composantes fortement connexes**, les ensembles maximaux de marquages qui peuvent tous s'atteindre mutuellement. Les composantes forment un graphe acyclique, et une composante est **terminale** lorsqu'aucun arc n'en sort.

**Théorème.** Un réseau dont le graphe d'accessibilité est fini est vivant exactement lorsque chaque transition étiquette un arc à l'intérieur de chaque composante terminale. *Preuve.* Depuis tout marquage accessible, une composante terminale est accessible : suivre des arcs de composante en composante doit s'arrêter, puisque le graphe des composantes est fini et acyclique. Si t est tirée à l'intérieur de chaque composante terminale, alors depuis tout marquage on atteint une composante terminale, et à l'intérieur de celle-ci chaque marquage atteint chaque autre, y compris un marquage où t est activée. Donc t peut encore être tirée. Réciproquement, supposons que t n'étiquette aucun arc à l'intérieur d'une composante terminale K. Alors t n'est activée en aucun marquage de K, car la tirer ajouterait un arc, et aucun arc ne sort de K. Depuis un marquage de K, le réseau ne quitte jamais K, donc t n'est plus jamais tirée.

Le réseau est réversible exactement lorsque le graphe entier est une seule composante, puisque tout marquage est accessible depuis m0 par construction. Un marquage mort est à lui seul une composante terminale, sans arc, donc un réseau qui a un interblocage et au moins une transition n'est pas vivant. Pour trois philosophes qui prennent d'abord la fourchette gauche, les 14 marquages forment deux composantes : le marquage mort, qui est terminal, et les 13 autres, depuis lesquels il est accessible. La vivacité échoue donc pour les neuf transitions, et la réversibilité échoue aussi, puisque m0 n'est pas accessible depuis le marquage mort.

### Exercice pratique

Montrez qu'un réseau vivant qui a au moins une transition est sans interblocage, et donnez un réseau sans interblocage qui n'est pas réversible.

> *Solution :* Soit m accessible et t une transition. La vivacité dit qu'une certaine séquence depuis m se termine par t. Si m était mort, seule la séquence vide pourrait être tirée depuis m, et elle ne contient pas t. Pour la seconde partie, prenez une place p avec un jeton, une place vide q, une transition `go` de p vers q, et une transition `stay` qui prend le jeton de q et le remet. `stay` continue d'être tirée, donc aucun marquage n'est mort, mais une fois `go` tirée, le jeton ne revient jamais en p : le réseau n'est pas réversible, et il n'est pas vivant non plus.

---

## 6. La matrice d'incidence et les invariants

L'énumération visite les marquages un par un ; l'algèbre linéaire raisonne sur tous à la fois. La **matrice d'incidence** C = Post − Pre a une ligne par place et une colonne par transition, et la colonne t est le changement que produit le tir de t. Si σ mène de m0 à m et que le vecteur x compte combien de fois chaque transition apparaît dans σ, la linéarité donne l'**équation d'état** m = m0 + C x.

Un **P-invariant** est un vecteur non nul y tel que yᵀ C = 0. Multiplier l'équation d'état par yᵀ donne yᵀ m = yᵀ m0 pour tout marquage accessible : une somme pondérée de jetons est conservée. Si y ≥ 0 et y(p) > 0, alors y(p) m(p) ≤ yᵀ m = yᵀ m0, donc la place p ne contient jamais plus de yᵀ m0 / y(p) jetons. Un réseau dont toutes les places sont couvertes par des P-invariants positifs ou nuls est donc borné, depuis n'importe quel marquage initial, sans rien énumérer.

Pour les philosophes qui prennent d'abord la fourchette gauche, deux familles de P-invariants valent pour tout n :
- THINK_i + WAIT_i + EAT_i = 1 : chaque philosophe est dans exactement un état ;
- FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1 : la fourchette i est sur la table, tenue par le philosophe i, ou tenue par le philosophe i − 1 comme fourchette droite.

Chaque place figure dans au moins l'une d'elles avec le poids 1, donc le réseau est sauf pour tout n, y compris 13, où l'énumération ne peut pas se terminer dans le budget par défaut. La seconde famille prouve aussi l'exclusion mutuelle : EAT_i + EAT_(i−1) ≤ 1, donc des voisins ne mangent jamais en même temps, et c'est pourquoi le §3 n'a trouvé aucun marquage hors des configurations permises. Pour n = 3, les 12 places et les 9 transitions donnent une matrice de rang 6, et ces six invariants engendrent tous les P-invariants.

Un **T-invariant** est un vecteur non nul x ≥ 0 tel que C x = 0 : une séquence dont les nombres d'occurrences sont x revient au marquage d'où elle est partie, si elle peut être tirée. TAKE_LEFT_i, TAKE_RIGHT_i, RELEASE_i en est un.

L'équation d'état est nécessaire à l'accessibilité, pas suffisante. Prenez les places `gate` et `out`, toutes deux vides, et une transition t avec des arcs de `gate` vers t, de t vers `gate` et de t vers `out`. La colonne t de C est (0, 1), puisque la boucle s'annule. Le marquage out = 1 vérifie l'équation d'état avec x = (1), et pourtant t n'est jamais activée, et m0 est le seul marquage accessible. La matrice d'incidence ne voit pas une boucle. Décider exactement l'accessibilité est possible (Mayr, 1981), mais aucun algorithme ne peut le faire en temps primitif récursif : le problème est Ackermann-complet, avec la borne supérieure de Leroux et Schmitz (2019) et la borne inférieure de Czerwiński et Orlikowski, ainsi que de Leroux (2021).

### Exercice pratique

Dans la pompe à deux voies du §2, trouvez un P-invariant qui contient la place des arbres libres, et un qui contient le stash. Vérifiez que le marquage mort satisfait les deux. Ces invariants auraient-ils pu à eux seuls prédire l'interblocage ?

> *Solution :* L'arbre est libre, tenu par la voie 0 pendant qu'elle attend le stash ou travaille, ou tenu par la voie 1 pendant qu'elle travaille : arbres libres + voie 0 tenant sa première ressource + voie 0 tenant les deux + voie 1 tenant les deux = 1. De même, stash + voie 0 tenant les deux + voie 1 tenant sa première ressource + voie 1 tenant les deux = 1. Dans le marquage mort, les deux voies tiennent leur première ressource, ce qui donne 0 + 1 + 0 + 0 = 1 et 0 + 0 + 1 + 0 = 1. Les invariants disent quels marquages sont possibles, pas lesquels sont accessibles ou morts : l'interblocage est montré par son témoin, et les invariants ne peuvent pas l'exclure.

---

## 7. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription en Python de `net.rs`, `analysis.rs` et `models.rs` dans `crates/ix-petri`, et du réseau construit dans `tests/worktree_pump.rs`. La transcription reproduit les assertions des tests de ces fichiers, avec deux exceptions : elle omet le test qui compare deux sérialisations JSON, et pour les réseaux mal formés elle vérifie qu'ils sont refusés, pas quelle erreur est levée. Ces nombres sont des prédictions, et le §8 propose de les vérifier.

**La règle de tir et son ordre.** [`is_enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L216) vérifie m(p) ≥ Pre(p, t) place par place, et [`fire`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L239) [consomme les entrées avant de produire les sorties](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L237), si bien qu'une boucle se comporte comme le dit le §1 :

```rust
        let mut next = marking.0.clone();
        for &(p, w) in &tr.pre {
            next[p] -= w;
        }
        for &(p, w) in &tr.post {
            next[p] = next[p].checked_add(w).ok_or_else(|| PetriError::Overflow {
                transition: tr.id.clone(),
                place: self.places[p].id.clone(),
            })?;
        }
        Ok(Marking(next))
```

[`build`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L389) [trie les places](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L402) et les transitions par identifiant et rejette les identifiants en double, et [`enabled`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/net.rs#L229) renvoie les transitions dans cet ordre. La numérotation en largeur et chaque témoin sont donc les mêmes à chaque exécution.

**L'exploration, et ce que signifie la troncature.** [`explore`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L225) construit en largeur le graphe du §2. Un nouveau marquage au-delà de [`max_states`, 50 000 par défaut](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L67), est [refusé, et le graphe est marqué tronqué](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L260) ; de même pour un tir dont le [nombre de jetons dépasserait](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L245) un entier de 64 bits. Un graphe tronqué contient des marquages dont certains successeurs ont été refusés et jamais enregistrés, et IX ne les prend pas pour des marquages morts : il demande [au réseau, pas au graphe](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L464), si un marquage active quelque chose.

**Quels verdicts survivent à la troncature.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) renvoie `Holds`, `Fails` ou `Unknown` pour chaque propriété, à l'aide des arguments des §2 à §5. Le tableau montre quels verdicts il rend après une exécution tronquée :

| Propriété | IX décide après une exécution tronquée | IX ne décide qu'après une exécution complète |
|---|---|---|
| Absence d'interblocage | `Fails`, avec le nombre de marquages morts trouvés et, [par défaut, au plus 8](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L68) d'entre eux avec leurs témoins les plus courts | `Holds` |
| Bornitude | `Fails`, avec un témoin de pompage | `Holds`, avec la borne de chaque place |
| Quasi-vivacité | `Holds`, dès que chaque transition a été tirée | `Fails`, avec les transitions jamais tirées |
| Vivacité (L4) et réversibilité | Rien | `Holds` ou `Fails`, à partir des composantes du §5 |

C'est l'asymétrie de MAT-002. Une affirmation existentielle se règle par un exemple, trouvé à n'importe quel moment de la recherche : un marquage accessible est mort, une séquence pompe, chaque transition est tirée quelque part. Une affirmation universelle ne se règle que par le graphe entier. Les verdicts d'[interblocage](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L483), de [bornitude](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L494), de [quasi-vivacité](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L527), et de [vivacité et réversibilité](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L538) suivent le tableau ligne à ligne. La dernière ligne est un choix d'IX, pas une nécessité logique, comme l'explique *Autres lacunes* plus bas. Un réseau non borné n'est jamais exploré complètement, donc seule la colonne du milieu peut s'appliquer à lui.

**Vivacité et réversibilité, telles que le §5 les prouve.** [`liveness_and_reversibility`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L604) marque une composante comme terminale lorsqu'aucun arc n'en sort, et fait échouer la vivacité pour chaque transition qui n'étiquette aucun arc à l'intérieur d'une composante terminale. La réversibilité vaut lorsqu'il y a [une seule composante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L640). Les composantes viennent d'un [Tarjan itératif](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L367), si bien qu'un graphe profond ne peut pas faire déborder la pile.

**Le témoin de pompage est cherché sur un seul chemin, au plus 512 pas en arrière.** Quand un marquage est découvert, [`strictly_covered_ancestor`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L300) remonte ses parents en largeur, [au plus 512 d'entre eux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L51), à la recherche d'un ancêtre qu'il couvre strictement :

```rust
    fn strictly_covered_ancestor(&self, state: usize) -> Option<usize> {
        let wide_total = |m: &Marking| -> u128 { m.tokens().iter().map(|&t| u128::from(t)).sum() };
        let total = wide_total(&self.markings[state]);
        let mut cursor = self.parent[state].map(|(p, _)| p);
        let mut walked = 0usize;
        while let Some(a) = cursor {
            if walked >= MAX_COVERING_WALK {
                return None;
            }
            walked += 1;
            if wide_total(&self.markings[a]) < total
                && self.markings[state].strictly_covers(&self.markings[a])
            {
                return Some(a);
            }
            cursor = self.parent[a].map(|(p, _)| p);
        }
        None
    }
```

Une paire qu'il signale est une preuve, par le §4. Une paire qu'il manque laisse la bornitude à `Unknown`, comme le dit le commentaire : couper court la remontée [« can only *miss* a witness »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L292). Cet échec ne dépend pas du budget. Prenez un anneau de L places autour duquel circule un jeton, et laissez une transition de l'anneau ajouter aussi un jeton à une place compteur. La plus proche paire strictement couvrante sur tout chemin est alors à L tirs d'écart. Avec L = 512, la transcription trouve le témoin au 513e marquage ; avec L = 513, elle n'en trouve aucun, quel que soit le budget, et le réseau, bien que non borné, est déclaré `Unknown`.

**Réponses connues.** [`dining_philosophers`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L32) construit les deux protocoles du §2. Un test vérifie, [pour n = 2 à 5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L110), que prendre d'abord la fourchette gauche mène à un interblocage et que prendre les deux à la fois n'y mène pas ; un autre fixe [le marquage mort pour n = 3](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/models.rs#L153). La pompe du §2 est [`opposite_acquisition_orders_wedge_the_pump`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L92). D'autres tests y montrent qu'un [ordre d'acquisition canonique](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L138) supprime l'interblocage pour 2 à 4 voies, et qu'[une voie hors de l'ordre](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/tests/worktree_pump.rs#L162) le fait revenir. Le plan de la crate consigne une exécution sur le fichier à six philosophes publié par pnml.org : [729 marquages et 3 402 arcs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/plans/2026-09-08-feat-ix-petri-place-transition-nets.md#L111), avec deux marquages morts. Lu avec l'analyseur XML standard de Python et fourni à la transcription, le même fichier donne les mêmes nombres.

**Où s'arrête le budget par défaut.** Treize philosophes qui prennent d'abord la fourchette gauche ont 94 642 marquages accessibles (§3). Le marquage mort est à 13 tirs de m0, et l'ordre en largeur découvre 94 121 marquages avant lui. Avec le budget par défaut de 50 000, l'analyse s'arrête parmi les marquages situés à neuf tirs de m0, et elle déclare l'absence d'interblocage `Unknown`. Pourtant l'interblocage est dans le modèle, et son témoin, TAKE_LEFT_00 à TAKE_LEFT_12, est facile à écrire et à rejouer. La quasi-vivacité vaut, puisque chaque transition est tirée dans le budget ; la bornitude est `Unknown`, alors que les P-invariants du §6 prouvent en une ligne que le réseau est sauf. Le guide d'IX range [les P- et T-invariants, les siphons et les pièges](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L201) parmi ce qui n'est pas implémenté, et juge utile de les ajouter [« the day a net in this repository is too big for `max_states` »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/guides/petri-nets-in-ix.md#L203).

**Autres lacunes.** La crate promet chaque propriété [« with a witness »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/lib.rs#L6), et les interblocages comme la non-bornitude en ont un. Un `Holds` de quasi-vivacité [n'en porte aucun](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L528), pas même un tir de chaque transition. Un verdict de vivacité en échec nomme des transitions, mais aucun marquage depuis lequel elles ne peuvent plus jamais être tirées. Le verdict de réversibilité est un [`Verdict<()>`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L201), si bien que son échec ne porte aucun marquage depuis lequel m0 est inaccessible. Pour les philosophes qui prennent d'abord la fourchette gauche, l'échec de vivacité liste toutes les transitions, parce que la composante terminale est le marquage mort ; c'est le verdict d'interblocage qui est informatif. La vivacité et la réversibilité ne sont calculées qu'à partir d'un graphe complet, si bien qu'une exécution tronquée qui trouve un marquage mort les déclare toutes deux `Unknown`. Pourtant, par le §5, ce marquage prouve déjà que toutes deux échouent : rien n'y est tiré, et m0, depuis lequel une exécution tronquée a tiré quelque chose, n'est pas accessible depuis lui. Il n'y a pas d'arbre de couverture, donc un réseau non borné dont la remontée manque le témoin reste `Unknown`. La même analyse est exposée à SQL sous le nom [`ix_petri_analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/petri.rs#L10) et aux agents comme l'outil MCP `ix_petri_analyze`, enregistré comme la compétence [`petri.analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/petri.rs#L137). Les deux refusent un budget dont la mémoire dans le pire cas dépasse [512 Mio](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/json.rs#L123).

Corriger quoi que ce soit ici revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Une exécution sur les treize philosophes avec un budget de 94 122 marquages est tronquée. Quels verdicts peut-elle décider ?

> *Solution :* Le marquage mort est le 94 122e marquage découvert, donc il tient dans le budget : l'absence d'interblocage échoue, avec le témoin des treize tirs TAKE_LEFT. La quasi-vivacité vaut, puisque chaque transition est tirée dans le budget. La bornitude reste `Unknown` : la prouver par énumération exige le graphe entier, et il lui manque 520 marquages. IX laisse aussi la vivacité et la réversibilité à `Unknown`, alors que le marquage mort prouve déjà que toutes deux échouent (§5).

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Compter.** Lancer `analyze` avec les limites par défaut sur les deux protocoles pour n = 2 à 12. Prédiction : les effectifs du §3, des exécutions complètes, un marquage mort quand la fourchette gauche est prise d'abord et aucun sinon.
2. **La limite du budget.** Lancer les treize philosophes qui prennent d'abord la fourchette gauche avec `max_states` fixé à 50 000, 94 121, 94 122 et 94 642. Prédiction : absence d'interblocage `Unknown` pour les deux premiers budgets ; `Fails` à 94 122, tronquée, avec le marquage mort à l'état 94 121 ; à 94 642, une exécution complète, sauf, ni vivant ni réversible.
3. **La limite de la remontée.** Construire l'anneau du §7 avec L = 512 et L = 513, et le lancer avec `max_states` fixé à 5 000. Prédiction : avec L = 512, bornitude `Fails` avec un témoin de pompage de l'état 0 à l'état 512 sur 512 tirs ; avec L = 513, bornitude `Unknown` et aucun témoin.
4. **Invariants.** Construire la matrice d'incidence à partir des champs `pre` et `post` de `transitions()` pour n = 3 et n = 5, et vérifier les 2n invariants du §6. Prédiction : yᵀ C = 0 pour chacun d'eux, et C est de rang 2n.
5. **Un fichier qu'IX n'a pas écrit.** Lire le fichier à six philosophes de pnml.org avec `read_pnml` et l'analyser. Prédiction : 30 places, 30 transitions, 729 marquages, 3 402 arcs, deux marquages morts, sauf, ni vivant ni réversible.
6. **Deux réseaux de GA.** Lire les deux exemples PNML du composant IxqlViewer de GA, [`petri-producer-consumer.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-producer-consumer.pnml) et [`petri-pipeline-lifecycle.pnml`](https://github.com/GuitarAlchemist/ga/blob/b030c3f05e92189f9cb569d0fe0457ba6269e564/ReactComponents/ga-react-components/src/components/IxqlViewer/examples/petri-pipeline-lifecycle.pnml), et les analyser. Prédiction : le réseau producteur-consommateur, à 6 places et 4 transitions, a 12 marquages et 20 arcs, et il est 2-borné, sans interblocage, vivant et réversible. Le réseau du cycle de vie du pipeline, à 12 places et 8 transitions, a 8 marquages et 8 arcs ; il est sauf et quasi-vivant, mais ni vivant ni réversible, et l'absence d'interblocage donne `Fails` avec trois marquages morts, succès, échec et annulation, atteints en quatre tirs, deux tirs et un tir.

### Exercice pratique

À l'étape 2, un seul marquage de budget sépare `Unknown` de `Fails`. Pourquoi n'est-ce pas un signe d'instabilité ?

> *Solution :* L'ordre de découverte est fixe (§7), donc le marquage mort est toujours le 94 122e découvert, et un budget de 94 121 s'arrête un marquage avant lui. `Unknown` y est un refus, pas une supposition, et ne contredit aucun des deux verdicts. Un budget plus grand explore d'abord les mêmes marquages, puis d'autres, donc il peut changer `Unknown` en verdict mais jamais inverser un verdict.

---

## 9. Pièges courants

- **Lire `Unknown` comme `Holds`.** Une recherche arrêtée tôt n'a trouvé aucun interblocage parmi les marquages qu'elle a vus, ce qui ne dit rien des autres.
- **Prendre un nombre d'états tronqué pour la taille de l'espace d'états.** Une exécution arrêtée à 50 000 marquages a vu 50 000 marquages, et l'espace complet peut être bien plus grand.
- **Attendre d'une remontée d'ancêtres qu'elle trouve tout témoin de pompage.** Une paire plus éloignée que ce que la remontée atteint est manquée quel que soit le budget ; seule une méthode complète, comme l'arbre de couverture de Karp et Miller, décide la bornitude.
- **Lire tout marquage mort comme un bogue.** Les états finaux d'un flux de travail sont des marquages morts par construction, comme dans le cycle de vie du pipeline de GA (§8) ; un verdict d'interblocage ne signale un défaut que là où le modèle dit que le travail doit continuer.
- **Utiliser l'équation d'état comme test d'accessibilité.** Elle est nécessaire, pas suffisante, et elle ne voit pas les boucles.
- **Lire « non vivant » comme « a un interblocage ».** Un réseau peut être sans interblocage et avoir pourtant une transition qui n'est plus jamais tirée.
- **Lire un P-invariant comme une preuve d'accessibilité.** Un invariant exclut des marquages ; seul un témoin montre qu'un marquage est atteint.
- **Oublier à quelle vitesse l'espace croît.** Chaque philosophe qui prend d'abord la fourchette gauche multiplie les marquages accessibles par environ 2,4, si bien qu'un modèle petit sur le papier peut dépasser n'importe quel budget.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Réseau place/transition** | Des places, des transitions, et des arcs pondérés entre une place et une transition dans un sens ou dans l'autre |
| **Marquage** | Un nombre de jetons pour chaque place ; l'état du réseau |
| **Règle de tir** | Une transition est activée quand chaque place d'entrée contient au moins le poids de l'arc ; la tirer consomme et produit des jetons en conséquence |
| **Graphe d'accessibilité** | Les marquages accessibles, avec un arc pour chaque tir |
| **Marquage mort** | Un marquage où aucune transition n'est activée |
| **Témoin** | Une séquence de tir depuis m0 que chacun peut rejouer pour vérifier une affirmation |
| **k-borné, sauf** | Aucun marquage accessible ne met plus de k jetons dans une place ; sauf signifie 1-borné |
| **Témoin de pompage** | Un marquage accessible m et un marquage m′ accessible depuis m et le couvrant strictement, qui prouvent la non-bornitude |
| **Quasi-vivant (L1)** | Chaque transition est tirée dans un marquage accessible |
| **Vivant (L4)** | Depuis tout marquage accessible, toute transition peut encore être tirée |
| **Réversible** | m0 peut être atteint de nouveau depuis tout marquage accessible |
| **Composante terminale** | Une composante fortement connexe du graphe d'accessibilité dont aucun arc ne sort |
| **Matrice d'incidence** | C = Post − Pre ; la colonne t est le changement produit par le tir de t |
| **Équation d'état** | m = m0 + C x, une condition nécessaire pour atteindre m |
| **P-invariant** | Un vecteur non nul y tel que yᵀ C = 0 ; la somme pondérée de jetons yᵀ m est conservée |
| **T-invariant** | Un vecteur non nul x ≥ 0 tel que C x = 0 ; une séquence avec ces nombres d'occurrences revient à son marquage de départ |
| **Matrice de transfert** | Une matrice des pas permis, dont les puissances comptent les suites permises |

---

## Auto-évaluation

**1. Un analyseur s'arrête à 50 000 marquages, ne trouve aucun marquage mort, et déclare l'absence d'interblocage `Unknown`, mais chaque transition a été tirée. Que pouvez-vous conclure ?**
> Que le réseau est quasi-vivant : chaque transition est tirée dans un marquage accessible, et chaque tir est un témoin. Rien ne s'ensuit sur l'absence d'interblocage, puisqu'un marquage mort peut se trouver parmi les marquages non explorés ; pour treize philosophes, c'est le cas.

**2. Pourquoi un marquage accessible m, avec un marquage m′ accessible depuis m qui le couvre strictement, prouve-t-il la non-bornitude, alors que l'échec à trouver une telle paire ne prouve rien ?**
> La séquence de m à m′ peut être tirée de nouveau depuis m′, par monotonie, et ajoute chaque fois le même vecteur non nul, par linéarité. L'échec à trouver une paire ne prouve rien, parce que la recherche a pu s'arrêter avant que la paire n'apparaisse, ou, comme dans IX, n'a regardé qu'un nombre fixe de pas en arrière le long d'un seul chemin.

**3. Comment le dîner des philosophes peut-il être sauf pour tout n alors que l'analyseur ne peut pas finir pour n = 13 ?**
> Les P-invariants THINK_i + WAIT_i + EAT_i = 1 et FORK_i + WAIT_i + EAT_i + EAT_(i−1) = 1 valent pour tout n, et ils couvrent chaque place avec le poids 1. Ils bornent chaque place par 1 sans lister un seul marquage.

**4. IX signale que la vivacité échoue pour les neuf transitions de trois philosophes. Qu'est-ce que cela ajoute au verdict d'interblocage ?**
> Rien. La seule composante terminale est le marquage mort, où aucune transition n'est tirée, donc chaque transition en est absente. Le verdict d'interblocage en dit plus, puisqu'il donne le marquage et le témoin TAKE_LEFT_0, TAKE_LEFT_1, TAKE_LEFT_2.

**Critères de réussite :** Tirer un réseau place/transition à la main ; construire son graphe d'accessibilité et donner un témoin le plus court pour un interblocage ; compter les marquages accessibles avec une matrice de transfert ; prouver la non-bornitude avec un témoin de pompage et expliquer ce que son absence ne montre pas ; lire la vivacité et la réversibilité sur les composantes terminales ; prouver la bornitude et l'exclusion mutuelle avec des P-invariants et expliquer pourquoi l'équation d'état ne suffit pas ; et dire lesquels des verdicts d'IX une exécution tronquée peut décider.

---

## Bases de recherche

- C. A. Petri, *Kommunikation mit Automaten*, thèse de doctorat, 1962 : l'origine des réseaux de Petri
- T. Murata, « Petri nets: Properties, analysis and applications », *Proceedings of the IEEE* 77, 1989 : la règle de tir, les niveaux de vivacité L0 à L4, la matrice d'incidence et les invariants
- R. M. Karp et R. E. Miller, « Parallel program schemata », *Journal of Computer and System Sciences* 3, 1969 : l'arbre de couverture et la décidabilité de la bornitude
- L. E. Dickson, « Finiteness of the odd perfect and primitive abundant numbers with n distinct prime factors », *American Journal of Mathematics* 35, 1913 : le lemme sur les vecteurs d'entiers naturels
- D. Kőnig, « Über eine Schlussweise aus dem Endlichen ins Unendliche », *Acta Scientiarum Mathematicarum* 3, 1927 : un arbre infini à branchement fini a une branche infinie
- E. W. Mayr, « An algorithm for the general Petri net reachability problem », *Proceedings of the 13th ACM Symposium on Theory of Computing*, 1981 : l'accessibilité est décidable
- W. Czerwiński et Ł. Orlikowski, « Reachability in vector addition systems is Ackermann-complete », et J. Leroux, « The reachability problem for Petri nets is not primitive recursive », tous deux dans *Proceedings of the 62nd IEEE Symposium on Foundations of Computer Science*, 2021 : la borne inférieure
- J. Leroux et S. Schmitz, « Reachability in vector addition systems is primitive-recursive in fixed dimension », *Proceedings of the 34th Annual ACM/IEEE Symposium on Logic in Computer Science*, 2019 : la borne supérieure d'Ackermann
- R. E. Tarjan, « Depth-first search and linear graph algorithms », *SIAM Journal on Computing* 1, 1972 : les composantes fortement connexes
- E. W. Dijkstra, « Hierarchical ordering of sequential processes », *Acta Informatica* 1, 1971 : le dîner des philosophes
- E. G. Coffman, M. J. Elphick et A. Shoshani, « System deadlocks », *ACM Computing Surveys* 3, 1971 : les conditions de l'interblocage, dont l'attente circulaire
- ISO/IEC 15909-2:2011, *High-level Petri nets — Part 2: Transfer format* : PNML, le format d'échange que lit IX
- OEIS A000032 (nombres de Lucas) et A002203 (nombres de Pell-Lucas) : les effectifs du §3
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §7 renvoie à sa ligne
- Code source de GA au commit `b030c3f05e92189f9cb569d0fe0457ba6269e564` : les deux exemples PNML du §8
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
