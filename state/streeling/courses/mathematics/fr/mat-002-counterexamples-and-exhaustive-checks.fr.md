---
module_id: mat-002-counterexamples-and-exhaustive-checks
department: mathematics
course: Contre-exemples, témoins et vérifications exhaustives
level: beginner
alchemical_stage: nigredo
prerequisites: [mat-001-proof-strategies]
estimated_duration: "35 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Contre-exemples, témoins et vérifications exhaustives — Quand vérifier des cas est une preuve

> **Département de mathématiques** | Stade : Nigredo (Débutant) | Durée estimée : 35 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Distinguer un énoncé universel d'un énoncé existentiel, et dire ce qui réfute ou établit chacun
- Réfuter un énoncé universel par un seul contre-exemple, et vérifier un témoin pour un énoncé existentiel
- Expliquer quand vérifier des cas est une preuve : sur un domaine fini, ou sur un domaine infini ramené à un nombre fini de cas
- Expliquer pourquoi les tests aléatoires et les recherches inachevées peuvent trouver des contre-exemples mais ne peuvent pas démontrer un énoncé universel
- Lire ce qu'établissent réellement les tests d'IX sur le groupe diédral et son analyseur de réseaux de Petri

---

## 1. Énoncés universels et contre-exemples

Un **énoncé universel** affirme qu'une propriété P vaut pour tout élément d'un domaine D : « pour tout x de D, P(x) ». MAT-001 a montré qu'aucun nombre d'exemples ne démontre un tel énoncé. L'autre sens est bien moins coûteux : **un seul** x pour lequel P(x) est faux le réfute. Un tel x est un **contre-exemple**. En logique, un contre-exemple est un témoin de la négation : « non (pour tout x, P(x)) » dit la même chose que « il existe un x tel que non P(x) ».

Deux exemples classiques :
- **Le polynôme d'Euler.** n² + n + 41 est premier pour n = 0, 1, 2, …, 39 : quarante succès d'affilée. En n = 40, il donne 40² + 40 + 41 = 40 · 41 + 41 = 41 · 41 = 1681, qui n'est pas premier. Quarante confirmations n'ont pas démontré l'énoncé ; un seul contre-exemple l'a réfuté.
- **La conjecture d'Euler sur les sommes de puissances.** Euler a conjecturé que, pour k ≥ 3, il faut au moins k puissances k-ièmes positives pour obtenir une puissance k-ième en les additionnant. L'énoncé a tenu près de deux siècles, jusqu'à ce que Lander et Parkin trouvent, par une recherche sur ordinateur, quatre puissances cinquièmes dont la somme est une puissance cinquième : 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵ = 61 917 364 224. Trouver ce contre-exemple a demandé une recherche sur machine ; le vérifier demande cinq puissances et une addition.

### Exercice pratique

Montrez, sans calculatrice, que n² + n + 41 n'est pas premier pour n = 41.

> *Solution :* Pour n = 41, chaque terme est un multiple de 41 : 41² + 41 + 41 = 41 · (41 + 1 + 1) = 41 · 43. Le nombre a les facteurs 41 et 43, donc il n'est pas premier.

---

## 2. Énoncés existentiels et témoins

Un **énoncé existentiel** affirme qu'au moins un élément a la propriété : « il existe x dans D tel que P(x) ». On le démontre par un **témoin** : un x explicite, accompagné d'une vérification que P(x) est vrai. Un témoin ne vaut que par sa vérification, qui doit donc être à la portée du lecteur.

- **Les nombres de Fermat.** Fermat pensait que tout nombre 2^(2^n) + 1 est premier. Euler l'a réfuté avec le témoin n = 5 : 2^32 + 1 = 4 294 967 297 = 641 × 6 700 417. N'importe qui peut vérifier le produit sans refaire la recherche qui a trouvé 641. Le même témoin démontre l'énoncé existentiel « un nombre 2^(2^n) + 1 au moins est composé » et réfute l'énoncé universel « tout nombre 2^(2^n) + 1 est premier ».
- **Les vérifications nécessaires.** Une vérification nécessaire est un test rapide que toute réponse correcte doit passer. L'échouer réfute la réponse aussitôt ; le passer ne démontre rien. Comparer les derniers chiffres en est une : deux entiers égaux finissent par le même chiffre, mais c'est aussi le cas de beaucoup d'entiers différents.

Certaines preuves d'existence, comme certaines preuves par l'absurde, ne construisent jamais de témoin. Cette leçon ne traite que de celles qui en construisent un.

### Exercice pratique

Sans calculer entièrement les puissances, vérifiez que 27⁵ + 84⁵ + 110⁵ + 133⁵ et 144⁵ finissent par le même chiffre. Cela démontre-t-il l'identité de Lander et Parkin ?

> *Solution :* Le dernier chiffre d'une puissance ne dépend que du dernier chiffre de la base. Les derniers chiffres de 7, 7², …, 7⁵ sont 7, 9, 3, 1, 7 ; ceux de 4, 4², …, 4⁵ sont 4, 6, 4, 6, 4 ; ceux de 3, 3², …, 3⁵ sont 3, 9, 7, 1, 3 ; et 0⁵ finit par 0. Le membre de gauche finit donc par le dernier chiffre de 7 + 4 + 0 + 3 = 14, soit 4, et 144⁵ finit aussi par 4. La vérification passe, mais elle n'est que nécessaire : elle passerait aussi pour une fausse identité dont les deux membres finiraient par hasard par le même chiffre. L'identité se démontre en calculant les deux membres, qui valent tous deux 61 917 364 224.

---

## 3. Vérifications exhaustives sur des domaines finis

Quand le domaine est **fini**, la règle de MAT-001 a une exception : vérifier P(x) pour **chaque** x de D est une preuve, appelée **preuve par exhaustion**. Un énoncé universel sur un domaine fini est une liste finie d'énoncés reliés par « et », et chacun d'eux a été vérifié.

La taille de la vérification dépend du nombre de variables sur lesquelles porte l'énoncé. Prenons le **groupe diédral D12** : les 24 rotations et réflexions d'un dodécagone régulier, dont la théorie musicale se sert pour les transpositions et les inversions des 12 classes de hauteurs.
- Un énoncé sur un élément, comme « tout élément a un inverse », demande 24 vérifications.
- Un énoncé sur deux éléments, comme « g · h = h · g », en demande 24² = 576.
- Un énoncé sur trois éléments, comme l'**associativité**, (g · h) · f = g · (h · f), en demande 24³ = 13 824.

Un énoncé sur un domaine **infini** peut parfois se ramener à un nombre fini de cas. Cette réduction est une étape de preuve ; les vérifications font le reste.

### Exercice pratique

Démontrez que pour tout entier n, le reste de la division de n² par 4 vaut 0 ou 1.

> *Solution :* Écrivons n = 4q + r avec r ∈ {0, 1, 2, 3}. Alors n² = 16q² + 8qr + r², donc n² et r² ont le même reste dans la division par 4. Cela ramène le domaine infini à quatre cas : r² = 0, 1, 4, 9 laissent les restes 0, 1, 0, 1. L'énoncé vaut dans chaque cas, donc pour tout entier. Conséquence : une somme de deux carrés laisse le reste 0, 1 ou 2 dans la division par 4, jamais 3.

---

## 4. Preuve ou vérification ?

Écrivons chaque élément de D12 comme un couple (i, a), où i compte les pas de rotation (de 0 à 11) et a = 1 marque une réflexion. Avec σ(a) = (−1)^a, le produit est

(i, a) · (k, b) = (i + σ(a) · k mod 12, a ⊕ b),

où ⊕ est l'addition modulo 2. Le changement de signe traduit la règle selon laquelle une réflexion inverse le sens d'une rotation. C'est la règle qu'implémente IX (§6).

**Théorème.** Ce produit est associatif, et la preuve vaut pour tout module, pas seulement 12.

*Preuve (directe, comme dans MAT-001) :* prenons g₁ = (i, a), g₂ = (k, b) et g₃ = (m, c), toutes les parties de rotation étant prises modulo 12.
- (g₁ · g₂) · g₃ = (i + σ(a)k, a ⊕ b) · (m, c) = (i + σ(a)k + σ(a ⊕ b)m, a ⊕ b ⊕ c).
- g₁ · (g₂ · g₃) = (i, a) · (k + σ(b)m, b ⊕ c) = (i + σ(a)k + σ(a)σ(b)m, a ⊕ b ⊕ c).
- Les deux coïncident car σ(a ⊕ b) = σ(a)σ(b) : le signe de deux marques de réflexion combinées est le produit de leurs signes. ∎

La preuve et une vérification exhaustive ne font pas le même travail :
- La **preuve** couvre la formule, pour tout module. Elle ne dit rien sur la question de savoir si un programme donné implémente la formule.
- Une **vérification exhaustive** du produit d'un programme sur les 13 824 triplets couvre ce programme, pour D12 seulement.

Une vérification ne détecte d'ailleurs que les erreurs auxquelles elle est sensible. Supprimez le changement de signe, (i, a) · (k, b) = (i + k, a ⊕ b), et le produit reste associatif : c'est un autre groupe, Z12 × Z2. Une vérification d'associativité ne peut pas voir le signe manquant. Une vérification de la relation « réflexion, puis rotation, puis réflexion donne la rotation inverse » le peut.

Il existe un second chemin des couples aux triplets. Faisons agir chaque élément g = (i, a) sur les 12 classes de hauteurs par la fonction π_g(p) = i + σ(a)p mod 12. Si π_{g·h} = π_g ∘ π_h pour tout couple, et si deux éléments distincts donnent deux fonctions distinctes, alors l'associativité est héritée de la composition des fonctions, qui est toujours associative : π_{(g·h)·f} = π_g ∘ π_h ∘ π_f = π_{g·(h·f)}, d'où (g · h) · f = g · (h · f). Une vérification sur les couples, jointe à cet argument, démontre un énoncé sur les triplets. Le §6 montre qu'IX a un test exactement de cette forme.

### Exercice pratique

Une implémentation fautive prend le signe du second facteur : (i, a) · (k, b) = (i + σ(b) · k mod 12, a ⊕ b). Montrez qu'elle n'est pas associative, avec g₁ = (0, 0), g₂ = (1, 0) et g₃ = (0, 1).

> *Solution :* À gauche, g₁ · g₂ = (0 + 1, 0) = (1, 0), puis (1, 0) · (0, 1) = (1 − 0, 1) = (1, 1). À droite, g₂ · g₃ = (1 − 0, 1) = (1, 1), puis g₁ · (1, 1) = (0 − 1, 1) = (11, 1). Comme (1, 1) ≠ (11, 1), ce seul triplet réfute l'associativité : un contre-exemple parmi les 13 824 triplets suffit.

---

## 5. Quand la recherche est incomplète

Les recherches sont asymétriques :
- Un contre-exemple trouvé par une recherche **partielle** est concluant. Il réfute l'énoncé universel, si petite que soit la part du domaine explorée.
- Une recherche partielle qui ne trouve **aucun** contre-exemple ne démontre rien sur la part qu'elle n'a pas explorée.

Les **tests aléatoires** sont une recherche partielle. QuickCheck (Claessen et Hughes, 2000) en a fait un outil courant : on énonce une propriété, et l'outil la vérifie sur de nombreuses entrées tirées au hasard, en signalant toute entrée sur laquelle elle échoue. Un échec signalé est un contre-exemple. Mille succès sont un indice, pas une preuve : sur un domaine infini, la part inexplorée reste infinie. Sur un petit domaine fini, une vérification exhaustive fait mieux, car c'est une preuve ; pour l'associativité dans D12, elle ne compte que 13 824 cas.

Un outil honnête garde la différence visible. Un **réseau de Petri** modélise un système par des jetons qui circulent entre des places ; un *marquage* est un état du système, et un marquage est *mort* quand plus rien ne peut s'y produire. L'analyseur de réseaux de Petri d'IX, sujet de MAT-023, explore les marquages qu'un réseau peut atteindre et renvoie l'un de trois verdicts pour chaque propriété ([`Verdict`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L89)) :
- `Holds` : la propriété est vraie, et voici ce qui a été mesuré ;
- `Fails` : la propriété est fausse, et voici le contre-exemple ;
- `Unknown` : la propriété n'a pas été tranchée dans les limites de l'exploration, et voici pourquoi.

`Unknown` n'est jamais compté comme un succès : la méthode [`holds`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L100) n'est vraie que pour `Holds`.

### Exercice pratique

Un analyseur s'arrête à sa limite d'états après avoir exploré un million de marquages, dont aucun n'est mort, et rend pour l'absence de blocage le verdict `Unknown`. Une collègue en conclut que le réseau est sans blocage. Qu'est-ce qui cloche ? Et si l'analyseur avait trouvé un marquage mort parmi ses dix premiers états, l'arrêt prématuré affaiblirait-il ce résultat ?

> *Solution :* « Aucun marquage accessible n'est mort » est un énoncé universel sur tous les marquages accessibles, et l'analyseur n'en a exploré qu'une partie. Un marquage mort peut se trouver parmi les autres : `Unknown` est donc la réponse honnête, et la conclusion de la collègue ne suit pas. Un marquage mort trouvé est un contre-exemple : la séquence de tirs qui l'atteint peut être rejouée depuis le marquage initial, quoi qu'il reste d'inexploré. L'arrêt prématuré ne l'affaiblit pas.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas. Elle n'a pas exécuté les tests d'IX : savoir s'ils passent à ce commit relève de l'expérience du §7.

**Le groupe diédral.** [`DihedralElement`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L16) stocke une rotation de 0 à 11 et une marque de réflexion, et implémente le trait [`Group`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L6). Son produit, reproduit tel quel depuis les lignes 66 à 77 de `dihedral.rs`, est la règle du §4 :

```rust
    fn compose(&self, other: &Self) -> Self {
        // (r^i s^j)(r^k s^l) = r^(i + (-1)^j · k) s^(j+l).
        // The sign flip encodes sr = r^(-1)s: rotation "conjugates" through reflection.
        let i = self.rotation as i16;
        let k = other.rotation as i16;
        let sign: i16 = if self.reflected { -1 } else { 1 };
        let new_rot = (i + sign * k).rem_euclid(12) as u8;
        Self {
            rotation: new_rot,
            reflected: self.reflected ^ other.reflected,
        }
    }
```

Le test [`group_law_exhaustive_closure_and_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L137) est exhaustif sur les éléments et les couples, pas sur les triplets :
- pour chacun des 24 éléments, il affirme g · g⁻¹ = e, g⁻¹ · g = e, e · g = g et g · e = g ;
- pour chacun des 576 couples, il affirme que la rotation de g · h est inférieure à 12 ([ligne 148](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L148)) ;
- il affirme que les 576 produits contiennent les 24 éléments ([ligne 158](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L158)).

Aucun test de `dihedral.rs` n'énonce l'associativité. Le test [`action_composition_matches_group_composition`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L135) en fait plus qu'il n'y paraît. Pour chacun des 576 couples et chacun de neuf ensembles de classes de hauteurs x pris en échantillon, il affirme (g · h) · x = g · (h · x), où l'action [`apply`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L40) est écrite indépendamment de `compose` : elle envoie chaque classe de hauteurs p sur −p si l'élément est une réflexion, puis effectue la rotation. C'est la fonction π_g du §4. L'un des ensembles de l'échantillon, l'accord de do majeur {0, 4, 7}, est envoyé par les 24 éléments sur 24 ensembles différents : les 12 accords majeurs et les 12 accords mineurs. Pour chaque couple, un seul élément envoie donc {0, 4, 7} sur g · (h · {0, 4, 7}), à savoir le vrai produit de D12, et le test oblige `compose` à le renvoyer. Si ce test passe, les 576 produits sont tous corrects, et l'associativité découle de la preuve du §4 sans aucune boucle sur les triplets.

**L'analyseur de réseaux de Petri.** [`analyze`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L436) explore les marquages accessibles jusqu'à ses limites. Son verdict sur les blocages, reproduit tel quel depuis les lignes 483 à 491 de `analysis.rs`, est l'asymétrie du §5 écrite en code :

```rust
    let deadlock_free = if deadlock_count > 0 {
        Verdict::Fails(deadlocks)
    } else if complete {
        Verdict::Holds(Vec::new())
    } else {
        Verdict::Unknown {
            reason: unknown("deadlock freedom"),
        }
    };
```

Un marquage mort trouvé donne `Fails`, que l'exploration soit terminée ou non : comme le dit le commentaire placé au-dessus de ce code ([ligne 460](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L460)), sa séquence témoin l'atteint depuis le marquage initial et le tir est déterministe. L'absence de marquage mort ne donne `Holds` que si l'exploration est terminée (`complete`), et `Unknown` sinon. Le test [`witness_sequences_are_shortest_and_replayable`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-petri/src/analysis.rs#L809) construit un petit réseau avec un chemin court et un chemin long vers le même marquage mort, affirme que le témoin signalé est le court, `a_short`, et le rejoue avec `fire` pour vérifier qu'il atteint le marquage signalé.

**Les tests fondés sur les propriétés.** IX déclare la bibliothèque `proptest`, un outil Rust de la famille QuickCheck, dans le manifeste de son espace de travail ([`Cargo.toml` ligne 211](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/Cargo.toml#L211)) et dans cinq crates, mais à ce commit aucun fichier Rust ne l'utilise. Dans IX, les tests fondés sur les propriétés relèvent de la théorie, pas de la pratique.

### Exercice pratique

Quelle assertion de `group_law_exhaustive_closure_and_inverse` ne peut jamais échouer, et pourquoi ? Considérez ensuite un produit fautif qui ne diffère de celui d'IX que par une seule entrée : (1, 1) · (2, 1) renvoie (5, 0) au lieu de (11, 0). Lequel des deux tests de D12 ci-dessus le détecterait ?

> *Solution :* « La rotation de g · h est inférieure à 12 » ne peut jamais échouer : `compose` réduit la rotation avec `rem_euclid(12)`, qui renvoie toujours une valeur de 0 à 11, et une assertion qui ne peut pas échouer ne vérifie rien. Le produit fautif passe toutes les assertions de `dihedral.rs` : les assertions d'identité et d'inverse n'utilisent que des couples contenant e, ou un élément et son inverse, et (2, 1) n'est pas l'inverse de (1, 1), puisque chaque réflexion est son propre inverse ; les 576 produits contiennent toujours les 24 éléments ; et les autres tests du fichier utilisent d'autres produits. Pourtant la règle fautive n'est pas associative : avec g₁ = (1, 0), g₂ = (0, 1) et g₃ = (2, 1), (g₁ · g₂) · g₃ = (1, 1) · (2, 1) = (5, 0), alors que g₂ · g₃ = (0 − 2, 0) = (10, 0) et g₁ · (10, 0) = (11, 0). Le test d'action la détecte : π_(1,1) ∘ π_(2,1) envoie p sur 1 − (2 − p) = p − 1, c'est-à-dire π_(11,0), donc seul (11, 0) envoie {0, 4, 7} sur le bon ensemble.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **L'associativité, exhaustivement.** Vérifier (g · h) · f = g · (h · f) avec la fonction `compose` d'IX pour les 13 824 triplets et compter les échecs. Prédiction : aucun, d'après la preuve du §4.
2. **Contrôles négatifs.** Passer le même vérificateur sur la règle fautive de l'exercice du §4 et sur le produit fautif à une entrée de l'exercice du §6. Prédiction : au moins un triplet en échec pour chacun, dont les deux triplets trouvés à la main plus haut. Un vérificateur qui ne signale ici aucun échec est défaillant, et son verdict à l'étape 1 ne voudrait rien dire.
3. **Ce que détectent les tests d'IX.** Réécrire les assertions de `group_law_exhaustive_closure_and_inverse` et de `action_composition_matches_group_composition` comme des vérifications d'une règle de produit quelconque, et les appliquer à la fonction `compose` d'IX et aux deux règles fautives. Prédiction : la fonction `compose` d'IX passe les deux ; le produit fautif à une entrée passe le premier et échoue au second ; la règle de l'exercice du §4 échoue aux deux, au premier dès e · g = g, puisque e · (1, 1) = (0 − 1, 1) = (11, 1).
4. **Rejouer un témoin.** Construire le réseau de `witness_sequences_are_shortest_and_replayable`, lancer `analyze` avec les limites par défaut, et rejouer le témoin signalé avec `fire`. Prédiction : l'absence de blocage est `Fails`, le témoin est `a_short`, et le rejeu atteint le marquage mort signalé.

### Exercice pratique

Pourquoi l'étape 2 doit-elle réussir avant qu'on fasse confiance à l'étape 1 ?

> *Solution :* Un vérificateur qui annonce « aucun échec » peut avoir raison, ou être incapable d'échouer, comme l'assertion « rotation inférieure à 12 » du §6. Le passer sur des règles que l'on sait fausses montre qu'il sait détecter un échec. C'est seulement alors que son silence sur la fonction `compose` d'IX signifie quelque chose : joint à la preuve du §4, il dit que ce code implémente un produit associatif.

---

## 8. Pièges courants

- **Prendre de nombreuses confirmations pour une preuve.** Le polynôme d'Euler a passé quarante cas et a échoué au quarante et unième.
- **Vérifier sur le mauvais nombre de variables.** Un énoncé sur des triplets ne se vérifie pas par une boucle sur des couples, sauf si un argument comme celui du §4 les relie.
- **Écrire des assertions qui ne peuvent pas échouer.** Assurez-vous que chaque assertion échouerait pour une implémentation fausse ; sinon, elle ne teste rien.
- **Compter `Unknown` comme un succès.** « Aucun contre-exemple trouvé dans les limites » n'est pas « aucun contre-exemple ».
- **Faire confiance à un vérificateur qui n'a jamais échoué.** Passez-le d'abord sur une faute connue : un contrôle négatif.
- **Confondre une vérification nécessaire avec une vérification complète.** Des derniers chiffres égaux rendent une identité plausible, pas vraie.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Énoncé universel** | Un énoncé selon lequel une propriété vaut pour tout élément d'un domaine : « pour tout x, P(x) » |
| **Énoncé existentiel** | Un énoncé selon lequel au moins un élément a une propriété : « il existe x tel que P(x) » |
| **Contre-exemple** | Un élément pour lequel un énoncé universel est faux ; un seul suffit à le réfuter |
| **Témoin** | Un élément explicite, accompagné d'une vérification, qui démontre un énoncé existentiel |
| **Preuve par exhaustion** | Une preuve qui vérifie chaque cas d'un domaine fini, ou les cas en nombre fini auxquels se ramène un domaine infini |
| **Vérification nécessaire** | Un test que toute réponse correcte passe : l'échouer réfute, le passer ne démontre rien |
| **Tests aléatoires** | Vérifier une propriété énoncée sur de nombreuses entrées tirées au hasard : ils trouvent des contre-exemples mais ne démontrent rien sur les entrées qu'ils omettent |
| **Contrôle négatif** | Passer un vérificateur sur un cas que l'on sait faux, pour montrer qu'il peut échouer |
| **Associativité** | (g · h) · f = g · (h · f) pour tous g, h, f : un énoncé sur des triplets |
| **Groupe diédral D12** | Les 24 rotations et réflexions d'un dodécagone régulier, utilisées pour les transpositions et les inversions des classes de hauteurs |

---

## Auto-évaluation

**1. Une propriété s'est vérifiée pour le premier million d'entiers positifs. Est-elle démontrée ?**
> Non. C'est un énoncé universel sur un domaine infini, et un million de cas en laissent une infinité non vérifiés ; n² + n + 41 a été premier quarante fois avant d'échouer. Il faut une preuve, éventuellement une preuve qui ramène l'énoncé à un nombre fini de cas.

**2. Pourquoi 13 824 vérifications démontrent-elles qu'un produit de D12 est associatif, alors que 10 000 triplets d'entiers tirés au hasard ne démontrent rien sur une opération définie sur tous les entiers ?**
> D12 a 24 éléments, donc ses 13 824 triplets sont tous les cas : la vérification est une preuve par exhaustion. 10 000 triplets d'entiers tirés au hasard en laissent une infinité non testés, et chacun d'eux pourrait être un contre-exemple.

**3. Une vérification sur les 576 couples de D12 peut-elle établir l'associativité ?**
> Pas à elle seule : l'associativité est un énoncé sur des triplets, et une vérification sur les couples ne l'énonce même pas. Elle le peut avec un argument qui relie les couples aux triplets, comme une action : si π_{g·h} = π_g ∘ π_h pour tout couple et si deux éléments distincts agissent différemment, l'associativité découle de celle de la composition des fonctions. Le test d'action d'IX a cette forme.

**4. L'analyseur de Petri d'IX rend pour l'absence de blocage le verdict `Unknown`. Que pouvez-vous en conclure ?**
> Seulement qu'aucun marquage mort n'a été trouvé dans la partie explorée avant la limite. Rien ne s'ensuit sur le reste, donc ce n'est pas un succès. Si un marquage mort avait été trouvé, le verdict serait `Fails`, avec un témoin rejouable, même après un arrêt prématuré.

**Critères de réussite :** Réfuter un énoncé universel par un contre-exemple, vérifier un témoin, reconnaître quand une vérification finie est une preuve, et expliquer pourquoi les tests aléatoires et les recherches inachevées ne démontrent pas d'énoncés universels, y compris dans les tests d'IX et son analyseur de Petri.

---

## Bases de recherche

- I. Lakatos, *Proofs and Refutations: The Logic of Mathematical Discovery*, Cambridge University Press, 1976 : le rôle des contre-exemples dans le développement des mathématiques
- L. J. Lander et T. R. Parkin, « Counterexample to Euler's conjecture on sums of like powers », *Bulletin of the American Mathematical Society* 72, 1079, 1966
- K. Claessen et J. Hughes, « QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs », *Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP 2000)*, 268–279, doi:10.1145/351240.351266
- Le polynôme d'Euler n² + n + 41 et sa factorisation de 2^32 + 1 sont classiques ; chaque nombre de cette leçon peut se vérifier à la main ou par un calcul direct
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code des §5 et §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
