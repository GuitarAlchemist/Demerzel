---
module_id: mus-011-modes-modal-families
department: music
course: Modes et familles modales
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-010-scales-pattern-set-interval-vector, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Modes et familles modales — La rotation contre le vecteur d'intervalles partagé

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Construire les modes d'une gamme en faisant tourner sa formule d'intervalles, et nommer les sept modes de la gamme majeure
- Distinguer les modes relatifs, qui gardent les notes et changent de tonique, des modes parallèles, qui gardent la tonique et changent les notes, et jouer les uns et les autres à la guitare
- Compter les modes distincts d'une gamme, y compris les gammes à transpositions limitées
- Expliquer pourquoi deux gammes qui ont le même vecteur de classes d'intervalles ne sont pas forcément des modes l'une de l'autre : images miroirs et relation Z
- Retracer comment GA construit ses familles modales, et lire ce que le laboratoire de Learn a déjà mesuré

---

## 1. Les modes comme rotations

MUS-010 a décrit une gamme par sa formule d'intervalles. Lire la même formule à partir d'un autre pas donne un **mode**. L'article « Mode (music) » de Wikipédia le dit ainsi : « Modern Western modes use the same set of notes as the major scale, in the same order, but starting from one of its seven degrees in turn as a tonic, and so present a different sequence of whole and half steps. » (Les modes occidentaux modernes utilisent les mêmes notes que la gamme majeure, dans le même ordre, mais en prenant tour à tour chacun de ses sept degrés comme tonique, et présentent donc une suite différente de tons et de demi-tons.)

| Mode | Formule d'intervalles | Sur son degré de do majeur |
|------|------|------|
| Ionien | 2 2 1 2 2 2 1 | do ré mi fa sol la si |
| Dorien | 2 1 2 2 2 1 2 | ré mi fa sol la si do |
| Phrygien | 1 2 2 2 1 2 2 | mi fa sol la si do ré |
| Lydien | 2 2 2 1 2 2 1 | fa sol la si do ré mi |
| Mixolydien | 2 2 1 2 2 1 2 | sol la si do ré mi fa |
| Éolien | 2 1 2 2 1 2 2 | la si do ré mi fa sol |
| Locrien | 1 2 2 1 2 2 2 | si do ré mi fa sol la |

Chaque formule est celle de la ligne du dessus, dont le premier pas passe à la fin : une **rotation**. Un mode est fixé par sa formule, pas par ses notes : « transposition preserves mode » (la transposition conserve le mode), donc ré dorien, do dorien et fa♯ dorien sont tous doriens. L'ionien est la gamme majeure, et l'éolien la mineure naturelle.

Toute gamme a des modes au même sens. « Other heptatonic scales also have seven modes each » (les autres gammes heptatoniques ont aussi sept modes chacune), et Wikipédia donne l'exemple de l'harmonie de la mineure mélodique, « based on the seven rotations of the ascending melodic minor scale » (fondée sur les sept rotations de la gamme mineure mélodique ascendante).

### Exercice pratique

Écrivez la formule du quatrième mode de la pentatonique majeure, 2 2 3 2 3, et donnez ses notes sur do.

> *Solution :* Le quatrième mode commence par le quatrième pas de la formule : 2 3 2 2 3. Sur do, les pas 2, 3, 2 et 2 mènent à ré, fa, sol et la, et le dernier pas, 3, ramène à do : do ré fa sol la. C'est la pentatonique majeure do ré mi sol la lue depuis sol, sa quatrième note, et ramenée sur do.

---

## 2. Modes relatifs et modes parallèles

On peut comparer deux modes de deux façons.

**Les modes relatifs gardent les notes.** Ré dorien et sol mixolydien se jouent tous deux sur les touches blanches : ré dorien est do majeur lu depuis ré, sol mixolydien est do majeur lu depuis sol. L'article « Relative key » de Wikipédia dit la même chose d'une tonalité majeure et de sa relative mineure : elles « share all of the same notes but are arranged in a different order of whole steps and half steps » (partagent toutes les mêmes notes, mais rangées dans un ordre différent de tons et de demi-tons).

**Les modes parallèles gardent la tonique.** Do dorien et do mixolydien commencent tous deux sur do, mais leurs notes diffèrent. L'article « Parallel key » de Wikipédia appelle tonalités parallèles (en français, homonymes) une gamme majeure et une gamme mineure qui ont « the same starting note (tonic) » (la même note de départ, la tonique). Les sept modes parallèles sur do empruntent les notes de sept gammes majeures différentes :

| Mode sur do | Notes | Notes de | Abaissés par rapport au lydien |
|------|------|------|------|
| do lydien | do ré mi fa♯ sol la si | sol majeur | aucun |
| do ionien | do ré mi fa sol la si | do majeur | 4 |
| do mixolydien | do ré mi fa sol la si♭ | fa majeur | 4, 7 |
| do dorien | do ré mi♭ fa sol la si♭ | si♭ majeur | 4, 7, 3 |
| do éolien | do ré mi♭ fa sol la♭ si♭ | mi♭ majeur | 4, 7, 3, 6 |
| do phrygien | do ré♭ mi♭ fa sol la♭ si♭ | la♭ majeur | 4, 7, 3, 6, 2 |
| do locrien | do ré♭ mi♭ fa sol♭ la♭ si♭ | ré♭ majeur | 4, 7, 3, 6, 2, 5 |

Lues dans cet ordre, les tonalités d'origine descendent le cycle des quintes, d'un dièse à cinq bémols. L'article « Mode (music) » de Wikipédia décrit la même suite : « each mode has one more lowered interval relative to the tonic than the mode preceding it » (chaque mode a un intervalle abaissé de plus, par rapport à la tonique, que le mode qui le précède).

**À la guitare.** En première position, avec l'accord standard, les notes de do majeur se trouvent sur les cases 0 à 3. Ré dorien part de la corde de ré à vide et monte jusqu'au ré de la deuxième corde, case 3 : ré mi fa sol la si do ré. Sol mixolydien part de la sixième corde, case 3, et monte jusqu'à la corde de sol à vide : sol la si do ré mi fa sol. Les deux viennent de la même forme de do majeur en première position, sur les cases 0 à 3 : ce sont des modes relatifs, le même ensemble lu depuis deux toniques. Ce qui les fait sonner différemment, c'est la note sur laquelle on commence et on finit, et les accords qu'on joue dessous.

### Exercice pratique

Quelle gamme majeure contient les notes de mi phrygien, et laquelle contient les notes de do phrygien ?

> *Solution :* Mi phrygien est do majeur lu depuis mi, son troisième degré. Do phrygien commence sur do avec la même formule, 1 2 2 2 1 2 2 : do ré♭ mi♭ fa sol la♭ si♭, les notes de la♭ majeur, dont le troisième degré est do.

---

## 3. Combien de modes ?

Une gamme de n notes a n rotations, mais deux rotations peuvent donner la même formule. Wikipédia : « The number of possible modes for any intervallic set is dictated by the pattern of intervals in the scale. » (Le nombre de modes possibles d'un ensemble d'intervalles est dicté par la formule d'intervalles de la gamme.) La gamme diminuée « has only two distinct modes » (n'a que deux modes distincts), et l'article poursuit : « The chromatic and whole-tone scales, each containing only steps of uniform size, have only a single mode each, as any rotation of the sequence results in the same sequence. » (Les gammes chromatique et par tons, qui ne contiennent chacune que des pas d'une seule taille, n'ont chacune qu'un seul mode, puisque toute rotation de la suite redonne la même suite.)

Les gammes par tons et diminuée sont deux des **modes à transpositions limitées** de Messiaen : des gammes qui « may be transposed to all twelve notes of the chromatic scale, but at least two of these transpositions must result in the same pitch classes » (peuvent être transposées sur les douze notes de la gamme chromatique, mais au moins deux de ces transpositions doivent donner les mêmes classes de hauteurs ; Wikipédia, « Modes of limited transposition »). La gamme par tons « has two transpositions and one mode » (a deux transpositions et un mode) ; la gamme octatonique, ou gamme diminuée, « has three transpositions, like the diminished 7th chord, and two modes » (a trois transpositions, comme l'accord de septième diminuée, et deux modes). La gamme augmentée du tableau ci-dessous répond à la même définition, mais Messiaen ne l'a pas retenue : le même article y voit une forme tronquée du troisième mode de Messiaen.

Les deux nombres sont liés. Un mode sur do est une transposition de la gamme, choisie pour contenir do, lue depuis do. Une gamme de n notes qui a t transpositions différentes place n × t notes sur les 12 classes de hauteurs, autant sur chacune, donc n × t / 12 de ses transpositions contiennent do :

| Gamme | Notes n | Transpositions t | Modes n × t / 12 |
|------|------|------|------|
| Majeure | 7 | 12 | 7 |
| Mineure harmonique | 7 | 12 | 7 |
| Pentatonique majeure | 5 | 12 | 5 |
| Par tons | 6 | 2 | 1 |
| Augmentée, do mi♭ mi sol sol♯ si | 6 | 4 | 2 |
| Octatonique | 8 | 3 | 2 |
| Chromatique | 12 | 1 | 1 |

MUS-006 compte les mêmes rotations, et la leçon 12 du cours music-theory-ga de Learn étudie ces gammes dans GA.

### Exercice pratique

La formule de la gamme augmentée est 3 1 3 1 3 1. Combien a-t-elle de modes distincts, et quelles sont leurs formules ?

> *Solution :* Deux : 3 1 3 1 3 1 et 1 3 1 3 1 3. Toute rotation de deux pas redonne la même formule. Elle a quatre transpositions, et 6 × 4 / 12 = 2.

---

## 4. Même vecteur, famille différente

Les rotations gardent l'ensemble d'une gamme, à une transposition près, donc les modes d'une gamme partagent tous son vecteur de classes d'intervalles (MUS-010, MUS-020). La réciproque est fausse : deux gammes peuvent partager un vecteur sans être des modes l'une de l'autre.

**Les images miroirs.** Do mineur harmonique, do ré mi♭ fa sol la♭ si, a la formule 2 1 2 2 1 3 1. Do majeur harmonique, do ré mi fa sol la♭ si, a la formule 2 2 1 2 1 3 1. L'article « Harmonic major scale » de Wikipédia la décrit comme une gamme majeure à sixte abaissée, et ajoute : « Its upper tetrachord is the same as that of the harmonic minor scale. » (Son tétracorde supérieur est le même que celui de la gamme mineure harmonique.) Les deux ont le vecteur <3 3 5 4 4 2>. Les sept rotations de la formule de la mineure harmonique sont :

2 1 2 2 1 3 1, 1 2 2 1 3 1 2, 2 2 1 3 1 2 1, 2 1 3 1 2 1 2, 1 3 1 2 1 2 2, 3 1 2 1 2 2 1, 1 2 1 2 2 1 3

Aucune n'est 2 2 1 2 1 3 1, donc la majeure harmonique n'est pas un mode de la mineure harmonique. C'en est l'**image miroir** : jouez les pas de la mineure harmonique en descendant depuis sol, 2 1 2 2 1 3 1, et vous obtenez sol fa mi ré do si la♭, les notes de do majeur harmonique ; sol est la note de départ qui tombe sur do plutôt que sur une transposition. Une image miroir a les mêmes intervalles dans l'ordre inverse, donc le même vecteur (MUS-020 l'appelle une inversion). La gamme majeure, la mineure mélodique, la pentatonique et les gammes par tons, augmentée, octatonique et chromatique du §3 sont leurs propres images miroirs ; la mineure harmonique, la majeure harmonique et la gamme blues ne le sont pas.

**La relation Z.** Certains ensembles partagent un vecteur sans être une transposition ni une image miroir l'un de l'autre. L'article « Interval vector » de Wikipédia en donne un exemple, le plus petit qui soit : « the two sets 4-z15A {0,1,4,6} and 4-z29A {0,1,3,7} have the same interval vector ⟨111111⟩ but one can not transpose and/or invert the one set onto the other. » (Les deux ensembles 4-z15A {0,1,4,6} et 4-z29A {0,1,3,7} ont le même vecteur d'intervalles ⟨111111⟩, mais on ne peut ni transposer ni renverser l'un sur l'autre.) Sur do, ce sont do do♯ mi fa♯ et do do♯ mi♭ sol.

**Compter les ensembles d'un vecteur.** Prenez tous les ensembles qui contiennent do et ont un vecteur donné. Ils comprennent les modes sur do de toutes les gammes qui ont ce vecteur :
- le vecteur de la gamme majeure : les sept modes sur do du §2, puisque la gamme majeure est sa propre image miroir et n'a pas de partenaire Z ;
- le vecteur de la mineure harmonique : 14 ensembles, les sept modes sur do de la mineure harmonique et les sept de la majeure harmonique ;
- le vecteur de la gamme blues : 24 ensembles, six modes de la gamme blues, six de son image miroir, et douze ensembles d'une classe en relation Z avec elle.

Le décompte du §3 s'étend à une classe entière. Si une classe de n notes compte f ensembles différents parmi ses transpositions et leurs images miroirs, n × f / 12 d'entre eux contiennent do. Pour la classe de la mineure harmonique, f = 24 et 7 × 24 / 12 = 14.

### Exercice pratique

Do mineur harmonique et do majeur harmonique sont-ils des modes l'un de l'autre ?

> *Solution :* Non. La formule de la majeure harmonique, 2 2 1 2 1 3 1, ne figure pas parmi les sept rotations de la formule de la mineure harmonique. Les deux gammes sont des images miroirs l'une de l'autre : elles partagent le vecteur <3 3 5 4 4 2>, mais aucune rotation ne mène de l'une à l'autre.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Cette leçon documente ce code et ne le modifie pas. Elle n'a exécuté ni GA ni ses tests : les décomptes ci-dessous viennent d'une réimplémentation en Python des méthodes citées. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA, à `0843879`.

Le cours music-theory-ga de Learn compile une version antérieure de GA, `a826864`, et ses leçons ont déjà mesuré les familles modales de GA. `ModalFamily.cs` est le même fichier aux deux commits, et les lignes des membres de `PitchClassSet` utilisés plus bas aussi. Le code qu'ils appellent a bien changé entre-temps : des caches et des tables de correspondance ont été ajoutés, le vecteur à douze notes <12 12 12 12 12 6> a reçu un décodage particulier, et du code de lecture de texte, de formes normales et de tonalités a changé, que la construction des familles n'utilise pas. La réimplémentation retrouve aussi tous les décomptes mesurés par Learn. Ces mesures décrivent donc toujours le code de GA. Cette section les résume, y renvoie et ajoute un recensement de toutes les familles.

**Les modes tonals de GA sont des rotations.** [`MajorScaleMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/Diatonic/MajorScaleMode.cs#L16) passe `Scale.Major` à sa classe de base, qui la garde comme [`ParentScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L27-L34) et construit les notes de chaque mode en [faisant tourner les notes de la gamme parente](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L127-L135). Ce sont les modes relatifs du §2 : un test vérifie que [les sept modes commencent sur do, ré, mi, fa, sol, la et si](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L21-L40). Un autre test, [`AllModes_ShareParentScaleIntervalClassVector`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L62-L71), affirme que « every rotation of the diatonic scale has the same interval-class vector » (chaque rotation de la gamme diatonique a le même vecteur de classes d'intervalles), mais il lit `mode.ParentScale.IntervalClassVector`, qui est le vecteur de `Scale.Major` pour les sept modes, et le compare à la constante `IntervalClassVector.Major` : la même vérification, sept fois. Lire les notes propres des modes rendrait seulement la vérification triviale, puisque des modes relatifs partagent un seul ensemble. L'affirmation a un contenu pour les modes ramenés sur do, comme dans le tableau du §2 : sept ensembles différents qui ont un seul vecteur ; ce test ne les construit pas.

**Les familles modales de GA regroupent les ensembles par vecteur.** Une [`ModalFamily`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L9-L13) est un [« Group of pitch class sets representing a scale that share the same interval vector »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L10) (groupe d'ensembles de classes de hauteurs représentant une gamme, qui partagent le même vecteur d'intervalles). GA [construit les familles](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114-L129) à partir de tous les ensembles qui contiennent 0, regroupés par nombre de notes puis par vecteur : le décompte du §4. Ses membres sont donc des modes parallèles sur do, et la famille majeure est formée des sept ensembles du tableau du §2. GA range ses ensembles [par identifiant croissant](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L19-L20), l'identifiant d'un ensemble étant son nombre à 12 bits (MUS-020), et le [regroupement](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L119-L120) garde cet ordre. Ainsi, le premier membre et le [`PrimeMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L51) de la famille majeure sont do locrien, identifiant 1387. [`ModeIndex`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L106-L117) est la place d'un ensemble dans cette liste, et `FamilySize` la longueur de la liste ; `ModeIndex` vaut 5 pour do ionien et 6 pour do lydien, ce n'est pas un degré. La leçon 13 de Learn montre qu'il vaut −1 pour un ensemble sans do ([leçon 13](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/13-extended-and-altered-chords.mdx#L355)).

**Ce que Learn a mesuré.** Avec GA compilé à `a826864` :
- la famille de la mineure harmonique a 14 membres dans GA, et la famille blues 24 ([leçon 2](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/02-scales-and-modes.mdx#L236-L256)), les décomptes du §4 ;
- la famille de l'accord parfait majeur a 6 membres, celle de la septième de dominante 8 et celle du tétracorde à tous les intervalles 16 ([leçon 4](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/04-set-classes.mdx#L184-L196)) ;
- `UnifiedModeService.RankByBrightness` classe 14 gammes pour la famille de la mineure harmonique ([leçon 11](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/11-modes-in-depth.mdx#L211-L229)) ;
- `IsMonomodal`, dont le commentaire de documentation donne en exemples « Whole Tone, Diminished » (par tons, diminuée), est faux pour la gamme octatonique, la gamme diminuée, puisque sa famille a deux membres, et vrai pour l'accord de septième diminuée ([leçon 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L254)).

Le catalogue de GA généré à partir de ces familles, `AtonalModalFamilies.yaml`, range le vecteur <3 3 5 4 4 2> sous le nom [« Harmonic Major Family »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L6446-L6452) (famille majeure harmonique), avec un `DistinctModeCount` de 14, c'est-à-dire, d'après le §4, les modes sur do de deux gammes, et deux sous-familles tonales, la majeure harmonique et la mineure harmonique. La leçon 12 de Learn lit le champ `IsSymmetric` du fichier ([leçon 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L260)).

**Toutes les familles, par transcription.** Sur les 200 familles de GA, la transcription trouve :

| Type de famille | Familles | Ensembles |
|------|------|------|
| Seulement des rotations du premier membre | 75 | 398 |
| Aussi des images miroirs, sans partenaire Z | 102 | 1218 |
| Une classe en relation Z | 23 | 432 |

Ainsi, 125 des 200 familles, qui contiennent 1650 des 2048 ensembles contenant do, ne sont pas des familles de modes. Le commentaire de documentation d'[`IsMultimodal`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L181-L184) parle d'« a family with multiple distinct rotations (e.g. Diatonic, Harmonic Minor) » (une famille à plusieurs rotations distinctes, par exemple diatonique, mineure harmonique), mais sept des quatorze membres de la famille de la mineure harmonique ne sont pas ses rotations. [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L196-L211) cherche un membre qui ne figure pas parmi les 24 transpositions et inversions du premier membre, donc il signale les 23 familles Z et accepte les 102 familles à images miroirs.

**Ce que vérifient les tests.** Des tests compilés vérifient que l'ensemble propre d'une gamme se trouve dans sa famille ([`ScaleModalMetadataTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ScaleModalMetadataTests.cs#L8-L32)), qu'`IsZRelated` concorde avec les marques Z du catalogue de Forte jusqu'à six notes ([`CanonicalForteCatalogTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L81-L90)), et que la famille majeure a sept membres, via `UnifiedModeService.EnumerateRotations` ([`UnifiedModeEdgeCaseTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Unified/UnifiedModeEdgeCaseTests.cs#L227-L240)). Aucun ne dresse la liste des ensembles qu'une famille devrait contenir. Le test qui le faisait est retiré de son projet, avec deux autres ([`ModalFamilyScaleModeFactoryTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L50), [`ModalFamilyTests` et `ModalFamilyScaleModeTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L69-L70)). Ce test, `ModalFamilyTests`, [attend sept membres](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L90-L92), puis [cherche](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L103-L109) les sept modes relatifs qu'il énumère, [de C D E F G A B à B C D E F G A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L59-L69), en noms de notes anglais. En tant qu'ensembles, ils n'en font qu'un, celui de do majeur, donc le test ne cherche jamais do dorien ni les autres membres du tableau du §2.

Corriger quoi que ce soit ici revient aux responsables de GA ; cette leçon se contente de le décrire.

### Exercice pratique

Le `FamilySize` de GA pour do mineur harmonique vaut 14. Combien de ces 14 ensembles sont des modes de la gamme mineure harmonique, et que sont les autres ?

> *Solution :* Sept : les transpositions de la mineure harmonique qui contiennent do, lues depuis do. Les sept autres sont les modes sur do de la majeure harmonique, son image miroir, qui partage le vecteur <3 3 5 4 4 2>.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA à `a826864`. L'épinglage de GA dans le laboratoire n'a pas besoin de changer : comme l'explique le §5, le code qui construit les familles est le même à `5c3a52a`, aux caches et à un cas particulier de décodage près. Rien dans cette section n'est une mesure :
- les prédictions viennent des §3 à §5 et sont écrites avant toute exécution ;
- les décomptes et les identifiants, y compris les décomptes par nombre de notes de l'étape 1, viennent de la réimplémentation en Python du §5 ;
- une version ultérieure de cette leçon rapportera les résultats.

Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Le recensement.** Compter les `ModalFamily.Items` et leurs membres par nombre de notes. Prédiction : 200 familles qui contiennent 2048 ensembles ; par nombre de notes de 1 à 12, 1, 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 et 1 familles.
2. **Rotations ou non.** Pour chaque famille, tester chaque membre contre les douze transpositions du premier membre, puis contre ses images miroirs. Prédiction : 75 familles de rotations seulement, 102 avec des images miroirs et sans partenaire Z, 23 avec une classe en relation Z ; 1650 des 2048 ensembles se trouvent dans les 125 familles mixtes.
3. **`IsZRelated`.** Le lire pour chaque ensemble qui contient do. Prédiction : vrai pour les 432 ensembles des 23 familles Z, faux pour les 1616 autres.
4. **Les témoins.** Afficher la famille majeure et la famille de la mineure harmonique. Prédiction : la famille majeure contient les identifiants 1387, 1451, 1453, 1709, 1717, 2741 et 2773, avec `PrimeMode` 1387, do locrien ; la famille de la mineure harmonique contient 14 ensembles, sept transpositions de do mineur harmonique et sept de do majeur harmonique.

### Exercice pratique

L'étape 1 prédit 35 familles de sept notes et 35 de cinq. Pourquoi les deux nombres sont-ils égaux ?

> *Solution :* Une famille de n notes est un vecteur partagé par des ensembles de n notes. Le passage au complémentaire met en correspondance un à un les ensembles de 7 notes et ceux de 5, et deux ensembles de 7 notes partagent un vecteur exactement quand leurs complémentaires en partagent un (le théorème du complémentaire de MUS-020). Les deux cardinalités ont donc le même nombre de vecteurs, et le même nombre de familles.

---

## 7. Pièges courants

- **Confondre modes relatifs et modes parallèles.** Ré dorien a les notes de do majeur ; do dorien a les notes de si♭ majeur.
- **Compter les modes d'une gamme symétrique d'après ses notes.** La gamme octatonique a huit notes et deux modes.
- **Prendre un vecteur partagé pour une famille partagée.** La majeure harmonique a le vecteur de la mineure harmonique et n'est pas l'un de ses modes.
- **Prendre une image miroir pour une rotation.** Une image miroir renverse la formule ; une rotation ne fait que déplacer son début.
- **Lire la `ModalFamily` de GA comme les modes d'une seule gamme.** Elle contient tous les ensembles contenant do qui ont le vecteur, images miroirs et partenaires Z compris.
- **Lire le `ModeIndex` de GA comme un degré.** C'est une place dans une liste triée par identifiant : do locrien vaut 0, do ionien 5.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Mode** | La formule d'intervalles d'une gamme lue depuis un autre de ses pas : une rotation |
| **Modes relatifs** | Des modes qui partagent les mêmes notes et diffèrent par la tonique, comme ré dorien et sol mixolydien |
| **Modes parallèles** | Des modes qui partagent la même tonique et diffèrent par les notes, comme do dorien et do mixolydien |
| **Mode à transpositions limitées** | Une gamme qui a moins de douze transpositions différentes, et donc moins de modes que de notes |
| **Image miroir** | Une gamme qui a les mêmes pas dans l'ordre inverse ; elle partage le vecteur, et n'est un mode que si la gamme est sa propre image miroir |
| **Relation Z** | Deux ensembles qui ont le même vecteur sans être ni des transpositions ni des images miroirs l'un de l'autre |
| **Famille modale** | Les modes d'une gamme : ses rotations |
| **La `ModalFamily` de GA** | Tous les ensembles contenant do qui ont un vecteur donné : les modes de plusieurs gammes quand des images miroirs ou des partenaires Z le partagent |

---

## Auto-évaluation

**1. Écrivez la formule du mode lydien et donnez les notes de fa lydien et de do lydien.**
> 2 2 2 1 2 2 1. Fa lydien s'écrit fa sol la si do ré mi, les notes de do majeur. Do lydien s'écrit do ré mi fa♯ sol la si, les notes de sol majeur.

**2. Jouez ré dorien et sol mixolydien en première position. Pourquoi tiennent-ils tous deux dans la même forme ?**
> Les deux sont do majeur lu depuis une autre tonique : ce sont des modes relatifs, avec le même ensemble. Seules changent la note de départ et les accords joués dessous.

**3. Combien de modes distincts ont la gamme par tons et la gamme octatonique, et pourquoi ?**
> Un et deux. La formule par tons répète un seul pas, donc chaque rotation la redonne ; la formule octatonique alterne deux pas, donc elle a deux rotations distinctes. Avec n notes et t transpositions, n × t / 12 donne 6 × 2 / 12 = 1 et 8 × 3 / 12 = 2.

**4. Dans GA à `5c3a52a`, pourquoi la famille modale de do mineur harmonique a-t-elle 14 membres, et de quel type de famille du §5 s'agit-il ?**
> GA regroupe par vecteur tous les ensembles qui contiennent do, et la majeure harmonique, image miroir de la mineure harmonique, a le même vecteur. La famille contient les sept modes sur do de chacune des deux gammes : c'est l'une des 102 familles à images miroirs sans partenaire Z.

**Critères de réussite :** Construire et nommer les modes d'une gamme à partir de sa formule. Distinguer modes relatifs et modes parallèles, et jouer les uns et les autres. Compter les modes d'une gamme, gammes symétriques comprises. Expliquer pourquoi un vecteur partagé ne fait pas de deux gammes des modes l'une de l'autre. Dire ce que contient la `ModalFamily` de GA, et en quoi elle diffère d'une famille de modes.

---

## Bases de recherche

- Wikipédia, « Mode (music) » : les modes diatoniques modernes, la transposition et le mode, la suite le long du cycle des quintes, les sept modes des autres gammes de sept notes, et le nombre de modes distincts.
- Wikipédia, « Modes of limited transposition » : la définition de Messiaen, les transpositions et les modes des gammes par tons et octatonique, et la gamme augmentée vue comme une troncature du troisième mode de Messiaen.
- Wikipédia, « Relative key » et « Parallel key » : les deux relations, pour les tonalités majeures et mineures.
- Wikipédia, « Harmonic major scale » : la sixte abaissée, et le tétracorde supérieur commun avec la mineure harmonique.
- Wikipédia, « Interval vector » : la relation Z et les ensembles 4-z15A et 4-z29A.
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne.
- Learn, leçons 2, 4, 11, 12 et 13 de music-theory-ga au commit `9e03205191de8602d1833e171aecff832ea9cb14` : leurs mesures des familles modales de GA à `a826864`.
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre.
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue.
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
