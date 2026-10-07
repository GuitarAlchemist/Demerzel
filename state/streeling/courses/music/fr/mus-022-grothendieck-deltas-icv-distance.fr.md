---
module_id: mus-022-grothendieck-deltas-icv-distance
department: music
course: Les deltas de Grothendieck — ce que mesure la distance de contenu intervallique
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Les deltas de Grothendieck — Ce que mesure la distance de contenu intervallique, et ce qui lui échappe

> **Département de musique** | Stade : Citrinitas (Intermédiaire à avancé) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Traiter les vecteurs de classes d'intervalles comme des éléments d'un monoïde commutatif, et construire le groupe dans lequel on peut les soustraire
- Calculer le delta et la distance L1 entre deux ensembles, et borner la distance à partir des seules tailles des ensembles
- Démontrer quels ensembles sont à distance 0, et pourquoi deux ensembles de même taille sont à une distance paire l'un de l'autre
- Dire ce que la distance ne voit pas : la conduite des voix, le majeur et le mineur, les tonalités, les notes qu'un accord contient, et la relation Z
- Retracer ce que GA calcule pour chacun de ces points, et où une heuristique, un commentaire ou un test dit autre chose

---

## 1. Le contenu intervallique comme décompte

Un guitariste demande « un accord proche de celui-ci ». Une réponse possible compare le contenu intervallique. Le vecteur de classes d'intervalles du §2 de MUS-020 compte, pour chaque classe d'intervalles de 1 à 6, les paires de notes de l'ensemble séparées par cette distance. Do majeur a <001110> : une tierce mineure, une tierce majeure et une quinte.

Un vecteur est une liste de six entiers naturels, un élément de N^6, et deux telles listes s'additionnent composante par composante. Avec <000000> pour élément neutre, N^6 est un **monoïde commutatif** : son addition est associative et commutative et possède un élément neutre. Aucun élément autre que <000000> n'y a d'opposé : aucune liste d'entiers naturels ajoutée à <001110> ne donne <000000>.

La somme de deux vecteurs compte des paires ; elle ne combine pas des accords. Ajoutez la note si à do mi sol. Le nouvel ensemble, Cmaj7, garde les trois paires de do majeur et gagne les trois paires que forme si avec do, mi et sol, à 11, 7 et 4 demi-tons : les classes d'intervalles 1, 5 et 4. Donc ICV(Cmaj7) = <001110> + <100110> = <101220>. En général, quand deux ensembles A et B n'ont aucune note commune, ICV(A ∪ B) = ICV(A) + ICV(B) + X(A, B), où X(A, B) compte les paires formées d'une note de chaque ensemble, classe par classe : la fonction d'intervalles de Lewin (1987), repliée sur les classes d'intervalles. La note si, prise seule, a le vecteur <000000> ; tout ce qu'elle ajoute vient de X.

Toute liste n'est pas le vecteur d'un ensemble. Les six décomptes d'un ensemble de n notes ont pour somme n(n − 1)/2, son nombre de paires. Les 4 096 ensembles ont 200 vecteurs distincts : <000000> pour l'ensemble vide et les notes seules, puis 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 et 1 vecteurs pour les tailles 2 à 12. Ce sont les 224 classes d'ensembles du §4 de MUS-020, moins 23 parce que chaque paire en relation Z partage un vecteur, moins 1 parce que l'ensemble vide et une note seule partagent <000000>.

### Exercice pratique

Trouvez le vecteur de C7, do mi sol si♭, à partir de celui de do majeur.

> *Solution :* Si♭ est à 10, 6 et 3 demi-tons au-dessus de do, mi et sol : les classes d'intervalles 2, 6 et 3. Donc X = <011001>, et <001110> + <011001> = <012111>, le vecteur que le §2 de MUS-020 donne pour C7.

---

## 2. Soustraire des décomptes : le groupe de Grothendieck

Pour comparer deux ensembles, on veut une différence : combien de paires de chaque classe le second ensemble a de plus que le premier. N^6 n'a pas d'éléments négatifs, donc on l'agrandit jusqu'au plus petit groupe dans lequel deux quelconques de ses éléments peuvent être soustraits.

La **construction de Grothendieck** fait cela pour tout monoïde commutatif M. On prend des paires (a, b) d'éléments de M, à lire comme « a − b ». On dit que (a, b) et (c, d) sont équivalentes quand a + d + k = b + c + k pour un certain k de M. Les classes forment un groupe abélien K(M) : (a, b) + (c, d) = (a + c, b + d), l'élément neutre est la classe de (0, 0), et l'opposé de (a, b) est la classe de (b, a). L'application a ↦ (a, 0) envoie M dans K(M), et tout homomorphisme de M vers un groupe se prolonge à K(M) d'une seule façon : c'est le sens de « plus petit ». Quand M est **simplifiable**, c'est-à-dire quand a + k = b + k entraîne a = b, on peut se passer du k et l'application est injective. N^6 est simplifiable, et K(N^6) est Z^6 : la classe de (a, b) est la liste d'entiers a − b.

Le **delta de Grothendieck** d'un ensemble A vers un ensemble B est δ(A, B) = ICV(B) − ICV(A), un élément de Z^6. De do majeur à Cmaj7, il vaut <+1, 0, 0, +1, +1, 0> : un demi-ton de plus, une tierce majeure de plus et une quinte de plus. Trois lois en font une différence, et elles sont vérifiées parce que la soustraction dans un groupe les respecte :
- δ(A, A) = 0 ;
- δ(B, A) = −δ(A, B) ;
- δ(A, B) + δ(B, C) = δ(A, C).

Le delta ne dépend que des deux vecteurs, pas des notes. Aller de do majeur à Fmaj7, fa la do mi, garde do et mi, retire sol et ajoute fa et la, et donne pourtant le même delta qu'aller à Cmaj7, parce que Fmaj7 et Cmaj7 partagent le vecteur <101220>.

La **norme L1** d'un delta additionne les valeurs absolues de ses six composantes, et la **distance** d(A, B) est la norme L1 de δ(A, B). Sur les vecteurs, c'est une métrique. Sur les ensembles, ce n'est qu'une pseudométrique : d(A, B) = 0 n'impose pas A = B (§3).

### Exercice pratique

Donnez les vecteurs d'un accord parfait majeur et d'un accord parfait mineur, et leur distance.

> *Solution :* Les deux valent <001110>. Un accord parfait mineur est une inversion d'un accord parfait majeur, et une inversion conserve chaque classe d'intervalles (§2 de MUS-020). Le delta vaut 0, et la distance aussi. GA donne 1 (§5).

---

## 3. Ce que mesure la distance

Notons T(n) = n(n − 1)/2 le nombre de paires d'un ensemble de n notes. Les six composantes de δ(A, B) ont pour somme T(|B|) − T(|A|).

**Théorème 1 (borne de taille et parité).** d(A, B) ≥ |T(|B|) − T(|A|)|, et d(A, B) − (T(|B|) − T(|A|)) est pair.

*Démonstration.* La somme des valeurs absolues des composantes est au moins la valeur absolue de leur somme. Et pour tout entier x, |x| − x vaut 0 ou 2|x|, un nombre pair, donc la norme et la somme diffèrent d'un nombre pair. ∎

Trois conséquences en découlent :
- Deux ensembles de même taille sont à une distance paire l'un de l'autre, donc deux ensembles de même taille aux vecteurs différents sont à au moins 2 l'un de l'autre.
- Un ensemble de trois notes et un ensemble de quatre notes sont à au moins T(4) − T(3) = 3 l'un de l'autre.
- Une distance d'exactement 1 demande T(|B|) − T(|A|) = ±1, ce qui n'arrive qu'entre un ensemble de deux notes et un ensemble d'au plus une note. Depuis un ensemble de trois notes ou plus, tout ensemble est à distance 0 ou à au moins 2.

**Théorème 2 (une note ajoutée).** Si A a n notes et que x n'en fait pas partie, ajouter x ajoute les n paires entre x et les notes de A et ne change aucune autre paire. Donc δ(A, A ∪ {x}) a des composantes positives ou nulles dont la somme vaut n, et d(A, A ∪ {x}) = n, quelle que soit la note ajoutée.

Ainsi Cmaj7, C7, C6 et Cadd9 sont tous à distance 3 de do majeur, la plus petite distance qu'un ensemble de quatre notes puisse avoir d'un ensemble de trois notes. Sur les 29 classes de tétracordes, 13 sont à distance 3 de do majeur, et quatre d'entre elles ne contiennent aucun accord parfait, ni majeur ni mineur.

**Théorème 3 (distance nulle).** d(A, B) = 0 exactement quand A et B ont le même vecteur. Comme T(0) = T(1) = 0 et que T croît à partir de n = 1, deux ensembles de tailles différentes ne partagent un vecteur que si l'un est vide et l'autre une note seule. Deux ensembles de même taille partagent un vecteur exactement quand ils sont dans la même classe d'ensembles ou dans deux classes en relation Z (§5 de MUS-020). Ainsi chaque transposition et chaque inversion d'un ensemble est à distance 0 de lui, et il en va de même de chaque ensemble de sa classe partenaire en relation Z.

La distance compte combien de paires de chaque classe d'intervalles apparaissent ou disparaissent, et rien d'autre. Le théorème 2 dit ce que coûte une note ajoutée ; le théorème 3 dit ce qui ne coûte rien.

### Exercice pratique

Quelles distances séparent deux classes de tricordes distinctes ?

> *Solution :* Deux tricordes ont chacun 3 paires, donc d'après le théorème 1 leur distance est paire, et elle n'est pas 0, car aucune paire de classes de tricordes n'est en relation Z. Les valeurs atteintes sont 2, 4 et 6 : (037) est à 2 de (025), à 4 de (048) et à 6 de (012).

---

## 4. Ce qu'elle ne voit pas

Chaque limite ci-dessous découle du §3 : la distance est une fonction de deux vecteurs, donc une opération qui conserve le vecteur lui est invisible.

**La conduite des voix.** Déplacez une note de do mi sol d'un demi-ton, vers le haut ou vers le bas. Les six résultats sont mi sol si (mi mineur) et do mi♭ sol (do mineur) à distance 0, et do♯ mi sol (do♯ diminué), do fa sol (Csus4), do mi fa♯ et do mi sol♯ (do augmenté) à distance 4. Les trois classes de tricordes les plus proches de do majeur par le contenu intervallique, à distance 2, sont (014), (015) et (025), et aucune n'est à un demi-ton : leurs représentants les plus proches, comme mi♭ mi sol, do mi fa et ré mi sol, demandent trois, deux et deux demi-tons de mouvement, en additionnant le déplacement de chaque voix. Une distance sur les vecteurs ne peut pas classer les accords selon le chemin que parcourt la main. Le §6 de MAT-022 montre que la recherche de chemin d'IX échoue pour cette raison à relier l'accord parfait augmenté et do majeur, et la recherche de GA échoue de la même façon (§5).

**Le majeur et le mineur, les tonalités et les modes.** Do majeur et do mineur sont à distance 0, puisqu'une inversion conserve le vecteur. Il en va de même des douze gammes majeures, do majeur et fa♯ majeur compris : une transposition conserve le vecteur, donc une distance sur les vecteurs ne peut pas compter les altérations. Un mode d'une gamme est le même ensemble de classes de hauteurs, et do mineur naturel contient les notes de mi♭ majeur, donc tous deux sont à distance 0 de chaque gamme majeure.

**Les notes qu'un accord contient.** 4-Z15, do do♯ mi fa♯, et 4-Z29, do do♯ mi♭ sol, sont tous deux à distance 3 de do majeur, avec le même delta <+1, +1, 0, 0, 0, +1>. 4-Z29 contient un accord parfait mineur, do mi♭ sol ; 4-Z15 ne contient aucun accord parfait, ni majeur ni mineur. Être à distance 3 de do majeur ne veut pas dire « do majeur plus une note » : trois autres classes de tétracordes sont à distance 3 sans accord parfait, ni majeur ni mineur, comme 4-Z15 (§3).

**La relation Z.** Ces deux ensembles partagent le vecteur <111111> et sont à distance 0 l'un de l'autre, bien qu'aucune transposition ni inversion n'envoie l'un sur l'autre.

### Exercice pratique

Un utilisateur demande « un accord de quatre notes proche de do majeur » et reçoit les classes de tétracordes à distance 3, la distance la plus faible possible pour un ensemble de quatre notes. Quelles sont les quatre qui ne contiennent aucun accord parfait, ni majeur ni mineur ?

> *Solution :* (0125), (0135), (0145) et (0146), qui est 4-Z15. Les 9 autres en contiennent un. La distance classe les 13 à égalité.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), la branche `main` de GA le 2026-10-06 ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Le cours ga-ai de Learn a exécuté une partie du même code, compilé à partir de deux commits antérieurs de GA ; ses sorties sont citées là où elles s'appliquent, chacune avec le commit compilé et le code qui y est le même qu'au commit `40d3374`. Les autres nombres viennent d'une transcription en Python, ligne à ligne, du code de GA en question.

**Le delta.** [`GrothendieckDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L8-L11) est « a signed delta in the Grothendieck group », avec une addition et un opposé qui respectent les lois de groupe ([lignes 139-167](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L139-L167)). [`FromIcVs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L113) soustrait les deux vecteurs composante par composante, puis :

```csharp
        // Heuristic: When two distinct sets share the same ICV (e.g., diatonic modes/keys),
        // L1 difference is zero. To preserve musical differentiation expected by callers/tests,
        // emit a minimal non-zero delta focused on ic1. This keeps related keys close but not identical.
        if (delta.L1Norm == 0)
        {
            delta = delta with { Ic1 = 1 };
        }
```

Le commentaire parle de « two distinct sets », mais la méthode ne voit que deux vecteurs, donc elle donne aussi <+1, 0, 0, 0, 0, 0> pour un ensemble comparé à lui-même : pour les 200 vecteurs, d'après la transcription. L'application enfreint donc les trois lois du §2. δ(A, A) n'est pas 0. De do mineur à do majeur, elle redonne <+1, 0, 0, 0, 0, 0>, et non l'opposé du delta aller. Et do majeur → do mineur → do majeur donne au total <+2, 0, 0, 0, 0, 0>. Entre deux vecteurs différents, la transcription la trouve égale au vrai delta. Le +1 tombe sur la classe d'intervalles 1, où aucune paire de notes n'a changé, et [`Explain`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L172) le lit comme « +1 ic1 (semitone) » et, puisqu'[un gain en ic1 ou en ic2](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckDelta.cs#L229-L232) est testé en premier, comme « more chromatic color ». L'issue [#776](https://github.com/GuitarAlchemist/ga/issues/776) de GA signale l'heuristique et demande que `ComputeDelta(v, v).L1Norm` vaille 0. La [leçon 14 du cours ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/14-what-the-substitution-skill-answers.md) de Learn a affiché `ComputeDelta(...).L1Norm = 1` pour C contre C, contre Am et contre F♯, et pour G7 contre D♭7 ([sortie](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l14.txt#L64-L67)), en compilant GA au commit `a826864`, où `GrothendieckDelta.cs` est le même qu'au commit `40d3374`.

GA a un second delta. [`IcvDelta`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.DSL/Generators/OptickGrothendieck.fs#L77-L93), dans le fichier `OptickGrothendieck.fs` du DSL, représente des « elements of the Grothendieck group Z^6 » et soustrait sans heuristique, donc les deux deltas de GA divergent exactement sur les vecteurs égaux. Son test, [`Grothendieck_IcvDelta_IsAbelianGroupAndCancellative`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L143-L155), vérifie l'élément neutre et l'opposé sur un seul delta ; il ne vérifie ni la commutativité, ni l'associativité, ni la simplifiabilité, et il ne touche pas à `GrothendieckDelta`.

**Les gammes des tests.** Les tests de GA écrivent les ensembles comme des chaînes de chiffres, lues caractère par caractère ([`PitchClassSet.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L728-L748)), par [`PitchClass.TryParseSetNotation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L275-L294), qui lit A et B comme 10 et 11 et passe tout le reste à [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L244-L267) : les chiffres, T pour 10, E pour 11, et les noms de notes, que ces chaînes n'utilisent pas. [`ShouldComputeDelta_FromCMajorToGMajor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L73-L90) lit sol majeur comme [« 02479E1 »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L77), avec le commentaire « G A B C D E F# », et `OptickGrothendieckTests` [le répète](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/OptickGrothendieckTests.cs#L27). Les chiffres donnent do do♯ ré mi sol la si : un 1 là où sol majeur demande un 6. Cet ensemble a le vecteur <354351>, et non le vecteur diatonique <254361>, et son vrai delta depuis do majeur est <+1, 0, 0, 0, −1, 0>, à distance 2. Le « do mineur » de [`ShouldComputeDelta_FromCMajorToCMinor`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L62-L70), « 0235789 », est do ré mi♭ fa sol la♭ la, de vecteur <344352>, à distance 4 ; do mineur naturel s'écrirait « 023578T ». D'après la transcription :
- `FromCMajorToCMinor` affirme une L1 supérieure à 0 et une explication qui contient « ic », et [`ShouldComputeDelta_WithExplanation`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L93-L108), sur le même « 02479E1 » que `FromCMajorToGMajor`, affirme que l'explication contient « ic1 ». Les deux passent avec le vrai delta. Avec do mineur naturel dans le premier test, le mode que désigne son commentaire (« Moves between modes »), et le vrai sol majeur dans le second, les deux vrais deltas seraient 0, et les deux tests ne passeraient que grâce à l'heuristique : sans elle, `Explain` renverrait « No change ». #776 lit le premier test comme une comparaison de do majeur avec do mineur naturel, qui partagent un vecteur, et conclut qu'il passe « only because of the rule above ». Au commit `40d3374`, comme au commit que cite #776, l'ensemble du test n'est pas do mineur naturel, et le test passe avec le vrai delta de 4.
- `FromCMajorToGMajor` affirme une L1 inférieure à 5 : 2 pour l'ensemble qu'il utilise ; 1, par l'heuristique, pour le vrai sol majeur.
- [`ShouldFindShortestPath_BetweenRelatedKeys`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L267-L279) ne vérifie que les deux extrémités du chemin, qui compte une étape, que la cible soit « 02479E1 » ou le vrai sol majeur.
- Le test d'`IcvDelta` ci-dessus porte sur le même « sol majeur » : seul le chiffre erroné rend son delta non nul.

**Voisinages et chemins.** Le coût est la norme L1 multipliée par 0,6 ([lignes 39-42](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L39-L42)), ce que [`ShouldComputeHarmonicCost_AsL1Norm`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/Grothendieck/GrothendieckServiceTests.cs#L115) vérifie avec 5,4 pour une norme de 9. [`FindNearby`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L45) parcourt les 4 096 ensembles, [place la source en premier, au coût 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L58-L62), [écarte la source par valeur](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L72-L77) et garde chaque ensemble dont le delta heuristique reste dans le rayon, trié par coût. Tout autre ensemble ayant le vecteur de la source est renvoyé à la distance 1, jamais 0. D'après la transcription, depuis do majeur (l'accord parfait), le rayon 0 ne renvoie que do majeur ; le rayon 1 renvoie do majeur et les 23 autres accords parfaits majeurs et mineurs, et rien d'autre ; le rayon 2 ajoute 108 dyades et tricordes à vraie distance 2, soit 132 ensembles en tout. Depuis la gamme de do majeur, le rayon 1 renvoie ses 12 transpositions, elle-même comprise, et le rayon 2 renvoie 36 ensembles.

[`FindShortestPath`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L118) effectue un parcours en largeur à l'aide de `FindNearby(current, 2)`, parmi les ensembles de la taille courante ([lignes 148-151](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L148-L151)). Son commentaire dit que le rayon 2 [« connects closely related diatonic collections (e.g., C major → G major) »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/Grothendieck/GrothendieckService.cs#L146-L147), qui « typically differ by one accidental yet may exceed radius=1 ». D'après le §4, deux gammes majeures quelconques sont à distance 0, et à 1 par l'heuristique : la métrique ne voit pas l'altération, et chaque tonalité est à une étape de toutes les autres. La transcription va de la gamme de do majeur à celle de fa♯ majeur en une étape, comme de do majeur à sol majeur ; de l'accord de do majeur à do mineur et à fa♯ majeur, en une étape chaque fois ; et ne trouve aucun chemin de do majeur à do mi sol♯, puisqu'aucune autre classe de tricordes n'est à 2 ou moins de (048). Le §6 de MAT-022 trouve la même lacune dans IX, et l'issue [#802](https://github.com/GuitarAlchemist/ga/issues/802) de GA la signale, avec les chemins d'une étape entre accords parfaits, dans le `IcvShortestPathSkill` du chatbot.

**Les deux skills du chatbot.** La [leçon 23 du cours ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/23-harmonic-distance-and-path.md) de Learn a appelé [`GrothendieckDeltaSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L97-L131) directement, en compilant la branche `main` de GA au commit `f4f5b4a`, où le skill, le delta et le service sont les mêmes qu'au commit `40d3374`. Cinq des dix [prompts d'exemple](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L46-L58) du skill nomment deux accords d'une même classe d'ensembles. Le skill décline l'un d'eux, « how different are C major and F major harmonically », parce que « major » s'intercale entre le premier accord et « and », comme le note la leçon 23. Il répond aux quatre autres : C vers G, Am et Em, Cmaj7 et Fmaj7, C vers F. Pour chacun, dans les deux sens, l'exécution a affiché le delta [+1, 0, 0, 0, 0, 0], L1 1, coût 0,60, puis « +1 ic1 (semitone) » et « more chromatic color » ([sortie, lignes 58-63](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L58-L63) et [66-67](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l23-main.txt#L66-L67)). Le skill [explique](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/GrothendieckDeltaSkill.cs#L123-L128) ensuite que chaque composante « says how many more occurrences of that interval-class the target has than the source » : sol majeur aurait un demi-ton de plus que do majeur, alors qu'aucun des deux n'en a. #802 le signale, ainsi que la flèche mal encodée qu'`Explain` affiche entre les deux parties. La [leçon 22 du cours ga-ai](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/src/content/docs/ga-ai/22-similar-chords.md) de Learn a exécuté [`IcvNeighborsSkill`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L120-L140), qui recalcule le vrai delta à cause de l'heuristique ([son commentaire](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L122-L129)) ; elle a compilé le même commit `f4f5b4a`, où ce skill est lui aussi le même qu'au commit `40d3374`. D'après le théorème 1, tout ensemble à distance 1 ou 2 d'un accord de trois notes est à 2, donc le skill garde les huit premiers dans l'ordre de `FindNearby`, qui est l'ordre des masques de bits des ensembles. Pour C : {0,3}, {0,4}, {1,4}, {0,1,4}, {0,3,4}, {0,5}, {1,5} et {0,1,5}, soit cinq classes d'ensembles, le tout annoncé comme le [« top 8 by harmonic cost »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L146) ([sortie](https://github.com/spareilleux/learn/blob/1190ee33650a5637414e73a455b69f3914f44fd6/code/ga-ai/expected/l22-main.txt#L90-L98)). L'issue [#798](https://github.com/GuitarAlchemist/ga/issues/798) de GA le signale. Le filtre du skill [écarte la distance 0](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Agents/Skills/IcvNeighborsSkill.cs#L136) comme « exact ICV-identical (same set class) », ce qui écarterait aussi une partenaire Z ; aucun des accords que construit le skill n'en a.

**L'outil MCP.** Le [`GaIcvNeighbors`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L325) de GaMcpServer calcule correctement la distance. Il [recalcule la vraie L1](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L337-L348), et son commentaire nomme l'heuristique ; il écarte la classe d'ensembles de l'accord lui-même et liste chaque classe une seule fois. D'après la transcription, `GaIcvNeighbors("C", 2)` liste (03), (04), (014), (05), (015) et (025), toutes à Δ=2. [Ses deux tests](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L72-L94) vérifient que la réponse à la distance 1 pour C ne nomme pas Forte 3-11, et qu'à la distance 2 chaque ligne est à Δ=2, qu'aucune ligne ne se répète ni ne nomme Forte 3-11, et que Forte 3-7 apparaît. Avec la distance par défaut, 1, il ne liste rien pour C. D'après le théorème 1, pour un ensemble de trois notes ou plus, la distance 1 ne peut ajouter qu'une partenaire Z, à distance 0, comme le dit la [description](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L327-L328) de l'outil : « distance 0 is a Z-related set ».

Les issues #776, #798 et #802 de GA couvrent l'heuristique et les deux skills. Au moment où cette leçon est écrite, aucune issue de GA ne couvre les gammes des tests, le commentaire sur les chemins ni le test d'`IcvDelta`. Les corriger revient aux responsables de GA ; cette leçon ne fait que les décrire.

### Exercice pratique

Si `_gMajorScale` dans `OptickGrothendieckTests` était la vraie gamme de sol majeur, « 024679E », que vérifierait `Grothendieck_IcvDelta_IsAbelianGroupAndCancellative` ?

> *Solution :* Seulement l'élément neutre. La vraie gamme de sol majeur est une transposition de celle de do majeur, donc `IcvDelta.Between` renverrait <0, 0, 0, 0, 0, 0>, et les deux assertions vérifieraient 0 + 0 = 0 et 0 + (−0) = 0. Elles n'exerceraient plus l'addition ni la négation sur un delta non nul. Avec « 02479E1 », elles vérifient d + 0 = d et d + (−d) = 0 pour d = <+1, 0, 0, 0, −1, 0>.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `40d3374`, et les fichiers de GA qu'il récupère incluraient aussi `GA.Business.DSL` et `GaMcpServer`. Rien n'y est une mesure. Les prédictions viennent du §3 et de la transcription du §5, et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en marche ni un modèle de langage. Les skills du chatbot sont laissés de côté, puisque les leçons 22 et 23 du cours ga-ai de Learn les ont déjà exécutés.

1. **Les deltas.** Appeler `GrothendieckService.ComputeDelta` et `IcvDelta.Between` sur les vecteurs de do majeur et do mineur (« 047 », « 037 »), de do majeur et ré majeur (« 047 », « 269 »), de 4-Z15 et 4-Z29 (« 0146 », « 0137 »), de la gamme de do majeur et de la vraie gamme de sol majeur (« 024579E », « 024679E »), et de la gamme de do majeur et de « 02479E1 ». Prédiction : pour les quatre premières paires, `IcvDelta` est nul et `ComputeDelta` vaut <+1, 0, 0, 0, 0, 0> ; pour la dernière, les deux donnent +1 sur la classe d'intervalles 1 et −1 sur la classe d'intervalles 5.
2. **Les lois.** Sur les 200 vecteurs distincts des 4 096 ensembles, tester les trois lois du §2 sur `ComputeDelta` et sur `IcvDelta`. Prédiction : `IcvDelta` respecte chaque loi sur chaque paire et chaque triplet. `ComputeDelta(v, v)` vaut <+1, 0, 0, 0, 0, 0> pour les 200 vecteurs ; l'antisymétrie n'échoue que sur les 200 paires égales ; l'additivité échoue sur les 119 600 triplets dont les trois vecteurs ne sont pas tous différents, et seulement là.
3. **Les voisinages.** Compter ce que `FindNearby` renvoie depuis do majeur (« 047 ») aux rayons 0, 1 et 2, et depuis la gamme de do majeur aux rayons 1 et 2. Prédiction : 1, 24 et 132 ; 12 et 36.
4. **Les chemins.** Appeler `FindShortestPath` de la gamme de do majeur à fa♯ majeur (« 13568TE ») et au vrai sol majeur, et de l'accord de do majeur (« 047 ») à celui de do mineur (« 037 ») et à do mi sol♯ (« 048 »). Prédiction : deux ensembles chacun pour les trois premiers ; un chemin vide pour le dernier.
5. **Les gammes des tests.** Afficher les éléments et les vecteurs de « 02479E1 » et « 0235789 ». Prédiction : {0, 1, 2, 4, 7, 9, 11} avec <354351>, et {0, 2, 3, 5, 7, 8, 9} avec <344352>.
6. **L'outil MCP.** Appeler `GaClosureBootstrap.init()`, comme le font les tests de GA, puis `GaIcvNeighbors("C", 1)` et `GaIcvNeighbors("C", 2)`. Prédiction : le message « No other set class within distance 1 of C », puis six classes à Δ=2, dont Forte 3-7.

### Exercice pratique

D'où vient le 119 600 de l'étape 2 ?

> *Solution :* L'heuristique ne se déclenche que sur des vecteurs égaux. Quand a, b et c sont tous différents, chaque terme est une vraie différence et la loi est vérifiée. Quand a = b ≠ c, le membre de gauche porte le +1 du premier terme ; quand b = c ≠ a, celui du second. Quand a = c ≠ b, le membre de gauche vaut 0 et celui de droite <+1, 0, 0, 0, 0, 0>. Quand a = b = c, le membre de gauche vaut <+2, 0, 0, 0, 0, 0> et celui de droite <+1, 0, 0, 0, 0, 0>. La loi échoue donc exactement sur les 200³ − 200 × 199 × 198 = 8 000 000 − 7 880 400 = 119 600 triplets qui ne sont pas tous différents.

---

## 7. Pièges courants

- **Lire la distance 0 comme « le même accord ».** Elle signifie le même vecteur : une transposition, une inversion ou une partenaire Z.
- **Lire une petite distance comme un petit mouvement.** Déplacer une note de do majeur d'un demi-ton donne la distance 0 ou 4 ; les classes de tricordes à distance 2 demandent deux ou trois demi-tons de mouvement.
- **Attendre de la distance qu'elle compte les altérations.** Chaque tonalité majeure est à distance 0 de toutes les autres.
- **Lire un delta comme une recette.** Un delta dit combien de paires de chaque classe apparaissent ou disparaissent, pas quelles notes changent : de do majeur à Cmaj7 et de do majeur à Fmaj7, le delta est le même.
- **Rapiécer un zéro.** Remplacer un delta nul par un delta « minimal non-zero » enfreint δ(A, A) = 0, l'antisymétrie et l'additivité, et signale un changement dans une classe d'intervalles où aucune paire n'a changé.
- **Se fier au commentaire d'un test.** Un test vérifie l'ensemble que construit son code, pas celui que nomme son commentaire : « 02479E1 » n'est pas sol majeur.
- **Comparer des ensembles de tailles différentes.** La borne de taille vaut quelles que soient les notes : un accord de trois notes et un accord de quatre notes ne sont jamais à moins de 3.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Monoïde commutatif** | Un ensemble muni d'une addition associative et commutative et d'un élément neutre, comme N^6 avec l'addition composante par composante |
| **Simplifiable** | Se dit d'un monoïde où a + k = b + k entraîne a = b |
| **Groupe de Grothendieck** | K(M), les classes de paires (a, b) lues comme a − b : tout homomorphisme de M vers un groupe s'y prolonge d'une seule façon ; K(N^6) = Z^6 |
| **Delta de Grothendieck** | δ(A, B) = ICV(B) − ICV(A), un élément de Z^6 |
| **Norme L1** | La somme des valeurs absolues des six composantes d'un delta |
| **Distance de contenu intervallique** | d(A, B), la norme L1 de δ(A, B) : une métrique sur les vecteurs, une pseudométrique sur les ensembles |
| **Borne de taille** | La distance est au moins l'écart absolu entre les nombres de paires des deux ensembles, T(n) = n(n − 1)/2, et a la même parité |

---

## Auto-évaluation

**1. Quel est le delta de do majeur à C7, et quelle est la distance ?**
> <0, +1, +1, 0, 0, +1>, à distance 3. C7 ajoute si♭ à do majeur, et d'après le théorème 2 une note ajoutée à un ensemble de trois notes coûte toujours 3.

**2. Pourquoi aucun accord de quatre notes ne peut-il être à distance 1 ou 2 d'un accord de trois notes ?**
> Les composantes du delta ont pour somme T(4) − T(3) = 3, donc sa norme L1 vaut au moins 3 (théorème 1).

**3. `FindNearby` de GA renvoie 24 ensembles dans un rayon de 1 autour de l'accord de do majeur. Lesquels, et quelle est leur vraie distance à do majeur ?**
> Do majeur lui-même et les 23 autres accords parfaits majeurs et mineurs. Tous partagent le vecteur <001110>, donc leur vraie distance est 0 ; l'heuristique place les 23 à 1.

**4. `GaIcvNeighbors` avec la distance 1 peut-il lister quoi que ce soit pour un accord de septième de dominante ?**
> Seulement une partenaire Z, à distance 0 : une distance d'exactement 1 n'apparaît qu'entre un ensemble de deux notes et un ensemble d'au plus une note. La classe de l'accord de septième de dominante, 4-27, n'a pas de partenaire Z, donc l'outil ne liste rien.

**Critères de réussite :** Construire K(M) et expliquer pourquoi K(N^6) = Z^6 ; calculer des deltas et des distances ; démontrer la borne de taille, la règle de la note ajoutée et le théorème de la distance nulle ; nommer ce que la distance ne voit pas ; et dire où l'heuristique, les commentaires et les tests de GA s'écartent des mathématiques.

---

## Bases de recherche

- D. Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press, 1987 : la fonction d'intervalles de deux ensembles
- S. Lang, *Algebra*, troisième édition révisée, Springer, 2002 : le groupe de Grothendieck d'un monoïde commutatif
- MUS-020 de Streeling pour les vecteurs de classes d'intervalles et la relation Z, et MAT-022 pour les groupes, les invariants et la recherche de chemin d'IX
- Code source de GA au commit `40d337479af36d987df3f06c8c638ffd35f13458`, et issues #776, #798 et #802 de GA : chaque fait de code du §5 renvoie à sa ligne
- Le cours ga-ai de Learn, leçons 14, 22 et 23, au commit `1190ee33650a5637414e73a455b69f3914f44fd6` de Learn : les sorties d'exécution citées au §5
- Vérifications en Python sur les 4 096 ensembles : tous les autres nombres des §§1–5 en proviennent, ou proviennent de la transcription du code de GA
- Expérience : proposée au §6, non exécutée ; cette leçon ne rapporte aucune nouvelle mesure de GA
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
