---
module_id: mat-022-symmetry-groups-invariants
department: mathematics
course: Symétrie, groupes et invariants
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-002-counterexamples-and-exhaustive-checks]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Symétrie, groupes et invariants — Compter les classes d'ensembles, et ce qu'un invariant oublie

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Décrire la transposition et l'inversion des classes de hauteurs comme le groupe diédral D12 agissant sur les 4096 sous-ensembles de Z/12, et vérifier les lois de groupe et d'action
- Calculer des orbites et des stabilisateurs, et prédire la taille d'une classe d'ensembles avec le théorème orbite–stabilisateur
- Compter les orbites avec le lemme de Burnside : 352 classes de transposition, 224 classes d'ensembles, et les effectifs pour chaque cardinal
- Distinguer un invariant complet d'un invariant incomplet, et lire la relation Z comme l'échec du vecteur de classes d'intervalles à séparer les orbites
- Traiter les opérations néo-riemanniennes P, L et R comme des involutions sur les 24 accords parfaits, et expliquer pourquoi elles commutent avec la transposition et l'inversion
- Retracer ce que calcule la crate `ix-bracelet` d'IX : quel représentant elle appelle forme primaire, et quels ensembles sa recherche de chemin harmonique peut atteindre

---

## 1. Groupes et actions

Numérotez les classes de hauteurs Do = 0, Do♯ = 1, …, Si = 11, de sorte qu'elles forment Z/12, les entiers modulo 12. La transposition de n est T_n : x ↦ x + n, et l'inversion suivie d'une transposition est T_nI : x ↦ n − x. Ces 24 applications forment un **groupe** : en composer deux en donne une troisième, T_0 est l'identité, et chacune a un inverse, puisque T_n défait T_(−n) et que chaque T_nI se défait elle-même, car n − (n − x) = x. Sur le cadran de l'horloge, T_n est une rotation et T_nI une réflexion, et le groupe est le **groupe diédral** D12 du dodécagone régulier. Lisez les compositions de droite à gauche, comme pour les fonctions : T_mI T_n envoie x sur m − (x + n), c'est donc T_(m−n)I. Le groupe n'est pas commutatif : T_1 T_0I envoie x sur 1 − x, tandis que T_0I T_1 l'envoie sur −(x + 1) = 11 − x.

Un groupe **agit** sur un ensemble lorsque chaque élément g déplace les points de l'ensemble, l'identité ne déplaçant rien et (gh)·x = g·(h·x). D12 agit sur les ensembles de classes de hauteurs point par point : T_n{0, 4, 7} = {n, n + 4, n + 7}. Il permute les 2^12 = 4096 sous-ensembles de Z/12 et ne change jamais leur cardinal.

### Exercice pratique

Calculez T_3I de l'accord de Do majeur {0, 4, 7}, puis appliquez de nouveau T_3I.

> *Solution :* 3 − 0 = 3, 3 − 4 = 11 et 3 − 7 = 8, donc T_3I{0, 4, 7} = {3, 8, 11}, l'accord de Sol♯ mineur. Appliquer de nouveau T_3I donne 3 − 3 = 0, 3 − 8 = 7 et 3 − 11 = 4, l'accord de Do majeur : T_3I est son propre inverse.

---

## 2. Orbites et stabilisateurs

L'**orbite** d'un ensemble X est la collection de ses images g·X, et son **stabilisateur** est l'ensemble des éléments g tels que g·X = X. Les orbites partitionnent les 4096 sous-ensembles. Sous D12, ce sont les **classes d'ensembles** ; sous le sous-groupe C12 des douze transpositions, ce sont les classes de transposition. Le **théorème orbite–stabilisateur** dit que |orbite| · |stabilisateur| = |G|, ici 24. La preuve : g·X = h·X exactement lorsque h⁻¹g appartient au stabilisateur, donc les éléments qui envoient X sur une image donnée forment une classe à gauche du stabilisateur, et toutes les classes à gauche ont sa taille.

Aucune transposition ne fixe l'accord de Do majeur, et chaque inversion en fait un accord mineur, donc son stabilisateur est {T_0} et son orbite a 24 membres, les 12 accords majeurs et les 12 accords mineurs. L'accord augmenté {0, 4, 8} est fixé par T_0, T_4 et T_8 et par T_0I, T_4I et T_8I, soit un stabilisateur de 6 et une orbite de 4, les quatre accords augmentés. La septième diminuée {0, 3, 6, 9} a un stabilisateur de 8, les T_n et T_nI avec n = 0, 3, 6 ou 9, et une orbite de 3. Comme un stabilisateur est un sous-groupe, son ordre divise 24, et la taille de chaque classe d'ensembles aussi.

### Exercice pratique

Trouvez le stabilisateur et l'orbite de la gamme par tons {0, 2, 4, 6, 8, 10}.

> *Solution :* T_n envoie les classes de hauteurs paires sur elles-mêmes pour tout n pair, et T_nI aussi, puisque n moins un nombre pair est pair ; pour n impair, l'une et l'autre les envoient sur les impaires. Le stabilisateur a 12 éléments, et l'orbite 24/12 = 2 : les deux gammes par tons.

---

## 3. Compter les orbites avec le lemme de Burnside

Diviser 4096 par 24 ne compte pas les classes d'ensembles ; ce n'est même pas un entier, parce que les ensembles symétriques ont des orbites plus petites. Le **lemme de Burnside** les compte exactement : le nombre d'orbites est le nombre moyen de points fixes, (1/|G|) Σ_g |Fix(g)|. Comptez de deux façons les couples (g, X) tels que g·X = X. Par g, il y en a Σ_g |Fix(g)| ; par X, il y en a Σ_X |Stab(X)| = Σ_X 24/|Orb(X)|, et les membres de chaque orbite contribuent ensemble exactement 24.

**Rotations.** T_n découpe Z/12 en pgcd(n, 12) cycles, et un ensemble est fixé lorsqu'il est une réunion de cycles, donc T_n fixe 2^pgcd(n, 12) ensembles. Pour n = 0, …, 11, cela donne 4096 + 2 + 4 + 8 + 16 + 2 + 64 + 2 + 16 + 8 + 4 + 2 = 4224, et 4224/12 = 352 classes de transposition.

**Réflexions.** T_nI fixe les classes de hauteurs x telles que 2x = n. Pour n pair, il y en a deux, n/2 et n/2 + 6, et les dix autres forment cinq paires échangées, donc 2^7 = 128 ensembles sont fixés ; pour n impair, il n'y en a aucune, six paires et 2^6 = 64 ensembles fixés. Les six réflexions paires et les six impaires fixent 6 × 128 + 6 × 64 = 1152 ensembles, et (4224 + 1152)/24 = 5376/24 = 224 classes d'ensembles.

**Un cardinal à la fois.** Pour les tricordes, seules T_4 et T_8 fixent quelque chose en dehors de l'identité, chacune les quatre accords augmentés : (220 + 4 + 4)/12 = 228/12 = 19 classes de transposition. Une réflexion paire fixe un tricorde formé d'une classe de hauteurs fixe et d'une paire échangée, soit 2 × 5 = 10 tricordes, et une réflexion impaire n'en fixe aucun : (228 + 60)/24 = 288/24 = 12 classes d'ensembles. Cinq des douze sont symétriques, 3-1, 3-6, 3-9, 3-10 et 3-12, et les sept autres se scindent chacune en deux classes de transposition, ce qui redonne 12 + 7 = 19.

| Cardinal | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Classes de transposition (C12) | 1 | 1 | 6 | 19 | 43 | 66 | 80 | 66 | 43 | 19 | 6 | 1 | 1 | 352 |
| Classes d'ensembles (D12) | 1 | 1 | 6 | 12 | 29 | 38 | 50 | 38 | 29 | 12 | 6 | 1 | 1 | 224 |

### Exercice pratique

Comptez les classes de tétracordes avec le lemme de Burnside, d'abord sous la seule transposition, puis sous D12.

> *Solution :* L'identité fixe les C(12, 4) = 495 tétracordes. T_3 et T_9 ont trois cycles de longueur 4 et en fixent 3 chacune ; T_6 a six cycles de longueur 2 et en fixe C(6, 2) = 15 ; les autres rotations n'en fixent aucun. Donc (495 + 3 + 3 + 15)/12 = 516/12 = 43. Une réflexion paire fixe les deux points fixes avec une paire, ou deux de ses cinq paires : 5 + 10 = 15 ; une réflexion impaire fixe deux de ses six paires, encore 15. Donc (516 + 12 × 15)/24 = 696/24 = 29.

---

## 4. Invariants et formes normales

Un **invariant** est une fonction qui prend la même valeur sur tous les membres d'une orbite. Le cardinal en est un. Le vecteur de classes d'intervalles en est un autre : T_n préserve chaque différence entre deux classes de hauteurs, T_nI la change de signe, et la classe d'intervalle min(d, 12 − d) ignore le signe. Un invariant est **complet** lorsqu'il sépare aussi les orbites, de sorte que des valeurs égales impliquent la même orbite. Le vecteur de classes d'intervalles n'est pas complet : {0, 1, 4, 6} et {0, 1, 3, 7} ont tous deux un intervalle de chaque classe, le vecteur ⟨111111⟩, et pourtant ils appartiennent à des orbites différentes, 4-Z15 et 4-Z29. C'est la **relation Z**. Une vérification exhaustive des 224 classes, à la manière de MAT-002, trouve 23 paires de ce genre, 46 classes en tout : 1 paire de tétracordes, 3 de pentacordes, 15 d'hexacordes, 3 d'heptacordes et 1 d'octacordes.

Une **forme normale** est un invariant complet d'un genre particulier : une règle qui choisit un membre de chaque orbite, le même quel que soit le membre dont elle part. La forme primaire d'une classe d'ensembles est une telle règle, et les deux règles publiées départagent les ex æquo différemment : celles de Forte et de Rahn donnent des formes primaires différentes pour 6 des 224 classes, 5-20, 6-Z29, 6-31, 7-Z18, 7-20 et 8-26. Toute règle qui renvoie le plus petit membre de l'orbite dans un ordre total fixé est aussi une forme normale, mais elle n'affiche pas forcément ce qu'affiche une table publiée. Les modules de la transformée de Fourier discrète d'un ensemble de classes de hauteurs sont d'autres invariants, et ils ne séparent pas non plus les classes en relation Z : les deux membres de chacune des 23 paires ont les mêmes.

### Exercice pratique

Montrez que {0, 1, 4, 6} et {0, 1, 3, 7} ont le même vecteur de classes d'intervalles, et trouvez un invariant qui les sépare.

> *Solution :* Les six différences dans {0, 1, 4, 6} sont 1, 4, 6, 3, 5 et 2, et dans {0, 1, 3, 7} ce sont 1, 3, 7, 2, 6 et 4, où 7 est la classe d'intervalle 5 : une de chaque classe dans les deux cas. En faisant le tour du cercle, les pas entre notes successives sont 1, 3, 2, 6 pour le premier ensemble et 1, 2, 4, 5 pour le second. T_n conserve ce cycle de pas et T_nI l'inverse, donc le multi-ensemble des pas est un invariant, et {1, 2, 3, 6} ≠ {1, 2, 4, 5}.

---

## 5. Transformations néo-riemanniennes

Trois opérations agissent sur les 24 accords majeurs et mineurs. **P** (parallèle) garde la fondamentale et la quinte et déplace la tierce d'un demi-ton : Do majeur ↔ Do mineur. **L** (échange de sensible, *leading-tone exchange*) garde la tierce et la quinte d'un accord majeur et abaisse sa fondamentale d'un demi-ton : Do majeur {0, 4, 7} ↔ Mi mineur {4, 7, 11}. **R** (relatif) garde la fondamentale et la tierce d'un accord majeur et élève sa quinte d'un ton : Do majeur ↔ La mineur {9, 0, 4}. Chacune garde deux notes de l'accord et réfléchit la troisième autour d'elles, donc chacune est une inversion choisie par l'accord lui-même, et chacune est une **involution** : appliquée deux fois, elle ramène l'accord de départ.

Comme chacune est définie par les intervalles propres de l'accord, et que T_n et T_nI transportent les intervalles, P, L et R commutent avec chaque transposition et chaque inversion : transposer puis appliquer P donne le même accord qu'appliquer P puis transposer. Les trois engendrent un groupe d'ordre 24 qui agit sur les mêmes 24 accords, le dual du groupe T/I au sens de Lewin. Alterner P et L à partir de Do majeur visite six accords, Do majeur, Do mineur, La♭ majeur, La♭ mineur, Mi majeur et Mi mineur : c'est le cycle hexatonique, dont les notes {0, 3, 4, 7, 8, 11} forment la collection hexatonique. Alterner P et R en visite huit, le cycle octatonique qui passe par Do, Mi♭, Fa♯ et La. Alterner R et L les visite tous les 24.

### Exercice pratique

En partant de Do majeur, appliquez L, puis P, puis R. Où arrivez-vous, et que partagent les deux accords ?

> *Solution :* L donne Mi mineur {4, 7, 11} ; P donne Mi majeur {4, 8, 11} ; R garde Mi et Sol♯ et monte Si d'un ton jusqu'à Do♯, ce qui donne Do♯ mineur {1, 4, 8}. Do majeur et Do♯ mineur partagent leur tierce, Mi : c'est le glissement S (*slide*). Appliquer R, puis P, puis L donne aussi Do♯ mineur, puisque S est une involution.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python de `dihedral.rs`, `action.rs`, `orbit.rs`, `prime_form.rs`, `forte.rs`, `neo_riemannian.rs` et `grothendieck.rs` dans `crates/ix-bracelet`, et du gestionnaire `ix_grothendieck_path`. Ces nombres sont des prédictions, et le §7 propose de les vérifier.

**Le groupe et l'action.** La crate présente [D12 par générateurs et relations](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L1), compose les éléments selon la [règle pour r^i s^j](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/dihedral.rs#L67), et [réfléchit avant de tourner](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L41), de sorte qu'un élément avec réflexion envoie x sur n − x, le T_nI du §1. La loi d'action est, selon les mots du trait, [« verified in tests, not by this trait »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/action.rs#L10) ; la transcription la vérifie pour les 576 couples d'éléments, sur quatre ensembles. [`orbit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L13) énumère les 24 images d'un ensemble, et ses tests fixent l'orbite de l'[accord augmenté](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L118) à 4 et celle de la [septième diminuée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L125) à 3, comme le dérive le §2. `all_prime_forms` trouve ses 224 classes en réduisant [chaque masque](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L43) à son représentant, et son commentaire nomme le [total de Burnside/Pólya](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/orbit.rs#L36) que calcule le §3.

**Ce qu'IX appelle forme primaire n'est ni celle de Forte ni celle de Rahn.** La fonction derrière chaque représentant est :

```rust
/// Minimum (under [`lex_less`]) over all 24 dihedral images of `x`.
pub fn bracelet_prime_form(x: PcSet) -> PcSet {
    let mut best = x;
    for reflected in [false, true] {
        for rotation in 0u8..12 {
            let g = DihedralElement {
                rotation,
                reflected,
            };
            let cand = g.apply(x);
            if lex_less(cand.raw(), best.raw()) {
                best = cand;
            }
        }
    }
    best
}
```

- **L'ordre est lexicographique sur les listes triées.** `lex_less` implémente l'[ordre lexicographique sur les listes triées de classes de hauteurs](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L12), donc le représentant est le membre de l'orbite dont la liste triée est la plus petite, pas la forme normale la plus compacte du §4. Le commentaire du module dit que cela correspond à la [convention de Forte pour les classes d'ensembles](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/prime_form.rs#L5). C'est vrai des classes, pas de leur graphie : le représentant est la forme primaire de Forte pour 189 classes et celle de Rahn pour 183. Pour 4-10, il renvoie [0, 1, 3, 10], là où les deux règles publiées donnent (0235).
- **Les numéros de Forte sont justes.** [`forte_number`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L360) cherche [ce représentant](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L363) dans une table de 224 masques, et chaque masque porte le numéro que la liste publiée donne à son orbite. L'en-tête de la table dit que les masques [coïncident exactement avec les orbites canoniques de Forte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L19), ce qui est vrai des orbites. Le test d'invariance vérifie [huit ensembles témoins](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/forte.rs#L427) sous les 24 éléments.
- **La graphie atteint les utilisateurs.** La fonction DuckDB `ix_prime_form` renvoie ce représentant sous le nom de [« bracelet prime form »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/bracelet.rs#L9), donc une requête qui compare sa sortie à une table publiée diverge sur 35 classes avec une table dans la graphie de Forte et sur 41 avec une table dans celle de Rahn.

**Les opérateurs néo-riemanniens.** [`p`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L36), [`l`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L48) et [`r`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L59) implémentent le §5 sur les 24 accords parfaits, et un [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L134) vérifie que les trois sont des involutions. La transcription ajoute qu'ils engendrent un groupe d'ordre 24 et commutent avec T_1 et avec T_0I. Le commentaire du glissement dit [« L ∘ P ∘ R applied left-to-right »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L67), alors que le code [`l(p(r(x)?)?)`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/neo_riemannian.rs#L70) applique R en premier. Comme S est une involution, les deux ordres donnent le même accord.

**Le chemin harmonique ne peut pas atteindre l'accord augmenté.** `find_shortest_path` exécute l'A* d'IX sur les ensembles d'un même cardinal, et un pas mène à tout autre ensemble dont le [vecteur de classes d'intervalles](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L129) se trouve à une distance L1 d'au plus [2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L259) :

```rust
    fn successors(&self) -> Vec<(PcSet, Self, f64)> {
        let card = self.current.cardinality();
        find_nearby(self.current, FIND_NEARBY_RADIUS_PER_STEP)
            .into_iter()
            .filter(|(s, _, _)| s.cardinality() == card && *s != self.current)
            .map(|(s, _, _)| {
                (
                    s,
                    PathNode {
                        current: s,
                        target: self.target,
                    },
                    1.0,
                )
            })
            .collect()
    }
```

- **Certaines classes forment des îles.** Deux tierces majeures parmi trois notes forcent le troisième intervalle à être lui aussi une tierce majeure, donc aucun tricorde n'a exactement deux intervalles de classe 4. Le vecteur ⟨000300⟩ de l'accord augmenté se trouve donc à une distance L1 de 4 ou plus de celui de tout autre tricorde, et les quatre accords augmentés forment une composante à eux seuls. Les 12 accords diminués en forment une autre, et parmi les tétracordes, les trois septièmes diminuées aussi. Les tricordes se répartissent en composantes de 4, 12, 36 et 168 ensembles, les tétracordes en composantes de 3, 30 et 462.
- **« Introuvable » a deux sens.** [`find_shortest_path`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L275) renvoie un chemin vide lorsque l'[A* n'en trouve aucun](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L169), et aussi lorsque le plus court est plus long que `max_steps`. `ix_grothendieck_path` fixe `max_steps` par défaut à [5](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7066) et rapporte les deux cas comme [`"found": false`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L7075). De {0, 4, 8} à {0, 4, 7}, il ne rapporte aucun chemin, alors que déplacer une voix d'un demi-ton les relie ; la distance est construite sur un invariant, et ne peut pas voir ce que cet invariant oublie.
- **L'heuristique est juste ; son commentaire hésite.** L'heuristique est [la moitié de la distance L1 à la cible](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L289). Elle est cohérente, ce dont l'A* d'IX a besoin parce que [les états fermés ne sont jamais rouverts](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-search/src/astar.rs#L75), donc les chemins qu'il renvoie sont les plus courts ; chaque tricorde de la composante de Do majeur est à 3 pas au plus de Do majeur. Le commentaire de documentation arrive à cette conclusion après une correction laissée en place, [« wait, actually »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-bracelet/src/grothendieck.rs#L267).
- **Autres lacunes.** Rien ne renvoie un stabilisateur ni ne compte les orbites par le lemme de Burnside ; il n'existe pas de forme primaire dans la graphie de Forte ou de Rahn ; P, L et R ne sont définis que sur les accords parfaits ; et la recherche de chemin mesure la distance entre vecteurs de classes d'intervalles, pas la conduite des voix.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Montrez que l'heuristique h = L1/2 est cohérente pour des pas de coût 1 dont les vecteurs de classes d'intervalles diffèrent d'au plus 2 en distance L1.

> *Solution :* Pour un pas de u à v et une cible t, l'inégalité triangulaire donne L1(u, t) ≤ L1(u, v) + L1(v, t) ≤ 2 + L1(v, t). En divisant par 2, h(u) ≤ 1 + h(v) : l'estimation ne baisse jamais de plus que le coût du pas, ce qui est la cohérence, et h(t) = 0 à la cible.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Burnside contre énumération.** Appliquer `necklace_prime_form` et `bracelet_prime_form` aux 4096 masques et compter les résultats distincts pour chaque cardinal. Prédiction : 352 et 224 en tout, répartis comme dans la table du §3.
2. **Stabilisateurs.** Pour chaque masque, compter les éléments qui le fixent et les membres de `orbit_unique`. Prédiction : le produit vaut 24 pour chaque masque ; les rotations fixent 4224 ensembles en tout et les réflexions 1152.
3. **Graphies.** Comparer `bracelet_prime_form` de chaque classe avec les formes primaires de Forte et de Rahn. Prédiction : 35 et 41 différences, avec [0, 1, 3, 10] pour 4-10.
4. **Cycles néo-riemanniens.** Appliquer `p`, `l`, `r`, `s`, `n` et `h` deux fois à chacun des 24 accords, puis alterner P et L, P et R, et R et L à partir de Do majeur. Prédiction : six involutions, et des cycles de 6, 8 et 24 accords.
5. **Chemins.** Appeler `find_shortest_path` de {0, 4, 8} à {0, 4, 7} avec `max_steps` à 10, et de {0, 4, 7} à {0, 1, 2} avec 3, puis 2. Prédiction : un chemin vide ; un chemin de quatre ensembles ; un chemin vide.

### Exercice pratique

À l'étape 5, comment un appelant peut-il savoir si un chemin vide signifie qu'aucun chemin n'existe ou que la limite était trop petite ?

> *Solution :* Un plus court chemin ne visite jamais deux fois le même ensemble, donc il a moins de pas qu'il n'y a d'ensembles de ce cardinal. Avec `max_steps` à C(12, k) − 1, soit 219 pour les tricordes, un chemin vide signifie qu'aucun chemin n'existe. Moins coûteux encore : comparer les composantes du graphe des classes d'intervalles, qui ne dépendent que des vecteurs.

---

## 8. Pièges courants

- **Composer dans le mauvais ordre.** T_mI T_n est T_(m−n)I, pas T_(m+n)I ; le groupe n'est pas commutatif, donc précisez quelle application agit en premier.
- **Diviser par l'ordre du groupe pour compter les classes.** Les ensembles symétriques ont des orbites plus petites ; utilisez le lemme de Burnside, ou comptez directement les orbites.
- **Prendre un invariant pour un invariant complet.** Des vecteurs de classes d'intervalles égaux ne rendent pas deux ensembles équivalents par transposition et inversion : c'est la relation Z.
- **Mélanger les conventions de forme primaire.** Les règles de Forte et de Rahn diffèrent sur six classes, et un représentant lexicographique diffère des deux sur des dizaines ; nommez la règle avant de comparer des tables.
- **Confondre une classe avec son représentant.** Deux outils peuvent s'accorder sur chaque classe et afficher pourtant des formes primaires différentes.
- **Lire « aucun chemin » comme « sans rapport ».** Une distance construite sur un invariant ne peut pas voir ce que l'invariant oublie, comme la conduite des voix.
- **Laisser implicite l'ordre d'un produit néo-riemannien.** De gauche à droite et de droite à gauche ne concordent que lorsque le produit est une involution, comme pour S.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Groupe** | Un ensemble muni d'une composition associative, d'un élément neutre et d'un inverse pour chaque élément |
| **Groupe diédral D12** | Les 24 symétries du dodécagone régulier : les transpositions T_n et les inversions T_nI |
| **Action de groupe** | Une règle g·x sous laquelle l'identité ne déplace rien et (gh)·x = g·(h·x) |
| **Orbite** | Les images g·X de X ; pour D12 sur les ensembles de classes de hauteurs, une classe d'ensembles |
| **Stabilisateur** | Les éléments g tels que g·X = X |
| **Théorème orbite–stabilisateur** | La taille d'une orbite multipliée par celle du stabilisateur est égale à l'ordre du groupe |
| **Lemme de Burnside** | Le nombre d'orbites est égal au nombre moyen de points fixes |
| **Invariant** | Une fonction constante sur les orbites ; complet lorsqu'il les sépare aussi |
| **Relation Z** | Deux classes d'ensembles qui partagent un vecteur de classes d'intervalles |
| **Forme primaire** | Un membre canonique d'une classe d'ensembles, choisi par une règle de départage énoncée |
| **P, L, R néo-riemanniens** | Les inversions d'un accord parfait qui gardent deux de ses notes |
| **Involution** | Une application qui est son propre inverse |

---

## Auto-évaluation

**1. Une table publiée donne 4-10 comme (0235), et IX affiche [0, 1, 3, 10]. L'un des deux a-t-il tort ?**
> Aucun. T_10 envoie {0, 2, 3, 5} sur {10, 0, 1, 3}, donc les deux sont dans la même orbite, et `forte_number` donne 4-10 pour les deux. Ils ne diffèrent que par la règle qui choisit le représentant : les règles publiées prennent la forme la plus compacte, IX la liste triée lexicographiquement la plus petite.

**2. Sans rien énumérer, pourquoi une classe d'ensembles ne peut-elle pas avoir 5 ou 7 membres ?**
> Par le théorème orbite–stabilisateur, la taille d'une orbite est 24 divisé par l'ordre de son stabilisateur, qui est un sous-groupe de D12. Les tailles possibles sont les diviseurs de 24 : 1, 2, 3, 4, 6, 8, 12 et 24.

**3. `ix_grothendieck_path` renvoie `"found": false` de l'accord augmenté à Do majeur. Qu'est-ce que cela vous apprend ?**
> Que dans le graphe d'IX, où des ensembles sont reliés lorsque leurs vecteurs de classes d'intervalles sont à une distance L1 d'au plus 2, les quatre accords augmentés forment une composante à eux seuls, puisqu'aucun tricorde n'a exactement deux intervalles de classe 4. Cela ne dit rien de la conduite des voix, où un demi-ton les relie. En général, l'indicateur peut aussi signifier que le chemin dépasse `max_steps` ; ici, c'est impossible, puisque la composante a quatre ensembles.

**4. Pourquoi P, L et R commutent-elles avec chaque T_n et chaque T_nI ?**
> Chacune garde deux notes de l'accord et réfléchit la troisième autour d'elles, une règle énoncée dans les intervalles propres de l'accord. T_n et T_nI transportent ces intervalles, donc appliquer P après une transposition ou une inversion donne l'image du résultat de P.

**Critères de réussite :** Décrire la transposition et l'inversion comme le groupe D12 agissant sur les ensembles de classes de hauteurs ; calculer des orbites et des stabilisateurs ; compter les classes avec le lemme de Burnside, en tout et par cardinal ; distinguer un invariant complet d'un invariant incomplet et expliquer la relation Z ; manipuler P, L et R et leurs cycles ; et retracer quel représentant IX appelle forme primaire et quels ensembles sa recherche de chemin peut atteindre.

---

## Bases de recherche

- W. Burnside, *Theory of Groups of Finite Order*, Cambridge University Press, 1897 : le lemme de dénombrement des orbites, aussi attribué à Cauchy et à Frobenius
- G. Pólya, « Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen », *Acta Mathematica* 68, 1937 : le dénombrement sous symétrie
- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973 : les classes d'ensembles et leur numérotation
- J. Rahn, *Basic Atonal Theory*, Longman, 1980 : la règle de forme primaire qu'emploient la plupart des tables actuelles
- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987 : les groupes de transformations et l'inversion contextuelle
- R. Cohn, « Maximally smooth cycles, hexatonic systems, and the analysis of late-Romantic triadic progressions », *Music Analysis* 15, 1996 : les cycles hexatoniques
- R. Cohn, « Neo-Riemannian operations, parsimonious trichords, and their Tonnetz representations », *Journal of Music Theory* 41, 1997 : P, L, R et leurs cycles
- A. S. Crans, T. M. Fiore et R. Satyendra, « Musical actions of dihedral groups », *American Mathematical Monthly* 116, 2009 : le groupe PLR comme dual du groupe T/I
- D. Tymoczko, *A Geometry of Music*, Oxford University Press, 2011 : la distance de conduite des voix
- E. Amiot, *Music Through Fourier Space*, Springer, 2016 : les modules de Fourier comme invariants
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
