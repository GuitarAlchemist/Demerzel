---
module_id: mus-013-root-bass-pitch-class-set
department: music
course: Fondamentale, basse et ensemble de classes de hauteurs
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-012-chord-formulas-essential-tones-doubling, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Fondamentale, basse et ensemble de classes de hauteurs — Un ensemble, plusieurs noms

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Distinguer la fondamentale d'un accord, sa basse et son ensemble de classes de hauteurs, et dire ce que fixent respectivement un symbole d'accord, une barre oblique et un voicing
- Trouver toutes les fondamentales qui lisent un ensemble comme un accord nommé, et reconnaître les ensembles qui en ont plusieurs : accords de sixte et de septième, sus2 et sus4, triade augmentée, septième diminuée
- Choisir entre les lectures par la basse, l'harmonie et la résolution, et noter ce choix en accord à barre oblique quand la basse n'est pas la fondamentale
- Retracer comment GA donne un seul nom à chaque ensemble de classes de hauteurs sans regarder la basse, et où ce nom perd une note ou une orthographe

---

## 1. Trois choses dans un nom d'accord

Un accord joué à la guitare a trois propriétés, et un nom d'accord les mêle.

- **L'ensemble de classes de hauteurs** est l'ensemble des notes de l'accord, sans les octaves ni les redoublements (MUS-020). La forme x32010 sonne do3 mi3 sol3 do4 mi4, et son ensemble est {do, mi, sol}, ou {0, 4, 7} avec do = 0.
- **La basse** est la note la plus grave qui sonne : do3 dans x32010. Elle appartient au voicing, pas à l'ensemble.
- **La fondamentale** est la note qui donne son nom à l'accord. Pour un accord construit en tierces, l'article « Root (chord) » de Wikipédia donne la méthode : « reorganize the pitches as a stack of thirds and then identify the lowest note in the stack » (réorganiser les hauteurs en un empilement de tierces, puis repérer la note la plus grave de l'empilement). Les notes do, mi et sol forment un empilement de tierces sur do, donc la fondamentale est do, où que do sonne.

La fondamentale n'est pas forcément la basse. Avec la fondamentale à la basse, l'accord est à l'état fondamental ; avec une autre note de l'accord à la basse, il est renversé, au sens d'un renversement d'accord et non d'intervalle comme dans MUS-008. Un **accord à barre oblique** (slash chord) écrit la basse après une barre oblique : C/E est un accord parfait de do majeur avec mi à la basse. L'article « Slash chord » de Wikipédia ajoute que la barre « does not indicate 'or' » (n'indique pas « ou »). Trois voicings de do majeur partagent un même ensemble :

| Forme | Notes, corde 6 d'abord | Ensemble | Basse | Fondamentale | Symbole |
|------|------|------|------|------|------|
| x32010 | do3 mi3 sol3 do4 mi4 | {0, 4, 7} | do | do | C |
| 032010 | mi2 do3 mi3 sol3 do4 mi4 | {0, 4, 7} | mi | do | C/E |
| 332010 | sol2 do3 mi3 sol3 do4 mi4 | {0, 4, 7} | sol | do | C/G |

Un symbole d'accord fixe une fondamentale et un ensemble. Une barre oblique ajoute la basse. Un voicing ajoute des octaves et des redoublements, et peut omettre des notes (MUS-012).

### Exercice pratique

Donnez l'ensemble, la basse, la fondamentale et le symbole de 2x0232.

> *Solution :* 2x0232 sonne fa♯2 ré3 la3 ré4 fa♯4. L'ensemble est {ré, fa♯, la}, ou {2, 6, 9}, et la basse est fa♯. La fondamentale est ré, puisque ré fa♯ la est un empilement de tierces sur ré. Le symbole est D/F♯, l'accord du milieu de la descente G – D/F♯ – Em que l'article « Slash chord » de Wikipédia donne en exemple.

---

## 2. Un ensemble, plusieurs fondamentales

L'empilement de tierces trouve une seule fondamentale pour une triade ou un accord de septième sans trou dans son empilement, sauf si l'empilement referme l'octave : la triade augmentée et la septième diminuée sont des empilements de tierces à partir de n'importe laquelle de leurs notes, comme le montre le troisième point ci-dessous. Certains ensembles se lisent à partir de plusieurs de leurs notes, et chaque lecture est juste. Les notes la, do, mi et sol forment un empilement de tierces sur la : c'est l'accord de septième mineure Am7. C'est aussi un accord parfait de do majeur auquel s'ajoute la, une sixte au-dessus de do : c'est C6. L'article « Sixth chord » de Wikipédia dit de C6 : « Because it is also an A minor seventh chord in first inversion, it is tonally ambiguous. Identifying the root depends on context. » (Comme c'est aussi un accord de la mineur septième au premier renversement, il est tonalement ambigu. Identifier sa fondamentale dépend du contexte.)

| Notes | Ensemble | Lectures |
|------|------|------|
| do mi sol la | {0, 4, 7, 9} | C6, Am7 |
| do mi♭ sol la | {0, 3, 7, 9} | Cm6, Am7♭5 |
| do ré sol | {0, 2, 7} | Csus2, Gsus4 |
| do mi sol♯ | {0, 4, 8} | Caug, Eaug, A♭aug |
| do mi♭ sol♭ la | {0, 3, 6, 9} | Cdim7, E♭dim7, G♭dim7, Adim7 |

Chaque lecture orthographie les notes à sa façon. Comme Eaug, le do de la quatrième ligne est si♯ ; comme A♭aug, le sol♯ est la♭, ce qui donne l'exemple de triade augmentée de Wikipédia, la♭–do–mi (« Augmented triad »).

- **Accords de sixte et de septième.** C6 et Am7 partagent un ensemble, de même que Cm6 et Am7♭5. L'article « Sixth chord » de Wikipédia donne d'autres noms pour do mi♭ sol la : il « might be written as Cm6, F9, F9 (no root), Am7♭5, B7♭9, A♭Maj7♭9, or Balt » (peut s'écrire Cm6, F9, F9 sans fondamentale, Am7♭5, B7♭9, A♭Maj7♭9 ou Balt). L'un d'eux est une erreur : B7♭9 est si ré♯ fa♯ la do, avec fa♯ et sans sol, et ne contient donc pas l'ensemble.
- **Accords suspendus.** Csus2 est do ré sol et Gsus4 est sol do ré : les trois mêmes notes. Pour un accord suspendu, « Root (chord) » dit d'« identify the triad that has been modified and then find its root » (repérer la triade qui a été modifiée, puis trouver sa fondamentale). Les notes do, ré et sol forment une triade de do où ré remplace mi, ou une triade de sol où do remplace si ; l'ensemble ne dit pas laquelle.
- **Accords symétriques.** La triade augmentée divise l'octave en trois tierces majeures, 4 + 4 + 4 = 12 demi-tons, et la septième diminuée en quatre tierces mineures, 3 + 3 + 3 + 3 = 12. Transposer l'une ou l'autre par l'un de ses propres intervalles redonne le même ensemble (MUS-020), si bien que chacune de ses notes le lit comme le même type d'accord. En tant qu'ensembles, il n'existe que quatre triades augmentées et trois accords de septième diminuée ; Wikipédia : « there are only three distinct diminished seventh chords (as opposed to twelve) » (il n'existe que trois accords de septième diminuée distincts, et non douze ; « Diminished seventh chord »).

Pour un accord de septième diminuée, le même article renvoie aux notes écrites : « Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling. » (Comprendre dans quel renversement un accord de septième diminuée est écrit, et donc trouver sa fondamentale, dépend de son orthographe enharmonique.) Un ensemble de classes de hauteurs n'a pas d'orthographe (MUS-007) : {0, 3, 6, 9} est do mi♭ sol♭ si𝄫 comme Cdim7, et la do mi♭ sol♭ comme Adim7.

### Exercice pratique

Quelles notes de mi sol si♭ do♯ peuvent être la fondamentale d'un accord de septième diminuée ? Vers quelle fondamentale pointe l'orthographe mi sol si♭ ré♭ ?

> *Solution :* Toutes les quatre : l'ensemble {1, 4, 7, 10} est un empilement de tierces mineures à partir de n'importe laquelle de ses notes. Orthographié mi sol si♭ ré♭, l'empilement commence sur mi : mi–sol, sol–si♭ et si♭–ré♭ sont des tierces mineures, et ré♭ est une septième diminuée au-dessus de mi, donc l'accord est Edim7. Orthographié avec do♯, l'empilement commence sur do♯ : do♯ mi sol si♭, C♯dim7.

---

## 3. Choisir entre les lectures

L'ensemble donne les candidats. La basse, l'harmonie et la résolution choisissent parmi eux.

- **La basse.** Une grille nomme d'ordinaire la lecture dont la fondamentale est à la basse : les notes la do mi sol avec la à la basse sont Am7, et avec do à la basse, C6. Sur toute autre note de basse, il faut une barre oblique. Am7/C n'est pas faux : il nomme les mêmes notes avec la fondamentale la et la basse do. Celui des deux qu'écrit une grille dit quelle fondamentale l'harmonie utilise.
- **L'harmonie.** Après G7 en do majeur, les notes la do mi sol avec do à la basse forment la tonique, C6. En sol majeur, entre Em et D7, les mêmes notes sont l'accord ii7 : Am7, écrit Am7/C si do est à la basse. Pour do mi♭ sol la, l'article « Sixth chord » de Wikipédia choisit entre Cm6 et F9 par l'« analysis of the movement of the root, in the presence of dominant-functioning harmonies » (analyse du mouvement de la fondamentale, en présence d'harmonies à fonction de dominante).
- **La résolution.** « A common suspension is a fourth above the root resolving to the third of the chord » (une suspension courante est une quarte au-dessus de la fondamentale qui se résout sur la tierce de l'accord ; Wikipédia, « Suspended chord »). L'ensemble ré sol la, quand il se résout sur ré fa♯ la, est Dsus4, et non Gsus2 sur ré. Pour un accord de septième diminuée, « resolution is a better indicator of function than spelling » (la résolution indique mieux la fonction que l'orthographe ; Wikipédia, « Diminished seventh chord ») : l'accord sur la sensible de do, si ré fa la♭, se résout sur la tonique.

Les accords à barre oblique servent aussi les arrangeurs. L'article « Slash chord » de Wikipédia écrit F/D pour un Dm7, afin qu'un débutant puisse jouer une triade de fa sur ré, et B°7/G pour G7♭9. Les deux écrivent un ensemble comme un accord familier sur une basse : F/D est ré fa la do, et B°7/G est sol si ré fa la♭.

### Exercice pratique

Une grille en do majeur se termine par Dm7 – G7 – ?, et le dernier accord est joué x35555. Nommez-le.

> *Solution :* x35555 sonne do3 sol3 do4 mi4 la4 : l'ensemble {do, mi, sol, la} avec do à la basse. Après G7, la cadence arrive sur la tonique do, donc l'accord est C6. Am7/C nomme les mêmes notes, mais avec la fondamentale la.

---

## 4. Formes de guitare à deux noms

Beaucoup de formes courantes contiennent l'un des ensembles du §2 ou une de ses transpositions. Le nom de grille suit la basse et la résolution habituelle ; les autres lectures demandent une barre oblique.

| Forme | Notes, corde 6 d'abord | Nom de grille | Ensemble | Autres lectures |
|------|------|------|------|------|
| x02010 | la2 mi3 sol3 do4 mi4 | Am7 | {la, do, mi, sol} | C6/A |
| x35555 | do3 sol3 do4 mi4 la4 | C6 | {la, do, mi, sol} | Am7/C |
| xx0233 | ré3 la3 ré4 sol4 | Dsus4 | {ré, sol, la} | Gsus2/D |
| x02230 | la2 mi3 la3 ré4 mi4 | Asus4 | {la, ré, mi} | Dsus2/A |
| xx0230 | ré3 la3 ré4 mi4 | Dsus2 | {la, ré, mi} | Asus4/D |
| 022200 | mi2 si2 mi3 la3 si3 mi4 | Esus4 | {mi, la, si} | Asus2/E |
| xx0101 | ré3 sol♯3 si3 fa4 | Ddim7 | {ré, fa, sol♯, si} | Fdim7/D, G♯dim7/D, Bdim7/D |
| 032110 | mi2 do3 mi3 sol♯3 do4 mi4 | Eaug | {mi, sol♯, do} | Caug/E, A♭aug/E |

La colonne des notes nomme chaque case avec des dièses ; ce n'est pas l'orthographe de l'accord. Comme Ddim7, xx0101 s'écrit ré fa la♭ do♭, et comme Eaug, 032110 s'écrit mi sol♯ si♯.

Deux formes, x02230 et xx0230, contiennent le même ensemble {la, ré, mi} : seules la basse et la résolution séparent Asus4 de Dsus2. Chaque forme sus4 se résout d'une case : xx0233 vers D xx0232 (sol4 descend à fa♯4), x02230 vers A x02220 (ré4 vers do♯4), et 022200 vers E 022100 (la3 vers sol♯3). Les deux dernières lignes contiennent des ensembles symétriques que Wikipédia prend en exemple. L'ensemble de xx0101 est celui de G♯dim7, « G♯–B–D–F » (sol♯–si–ré–fa), dont « Diminished seventh chord » dit qu'il est « enharmonically equivalent to three other inverted diminished chords » (enharmoniquement équivalent à trois autres accords diminués renversés) ; l'ensemble de 032110 est celui de A♭+, la♭–do–mi, l'exemple qui ouvre « Augmented triad ».

### Exercice pratique

Nommez 3x0013 comme le ferait une grille, et donnez l'autre lecture de son ensemble.

> *Solution :* 3x0013 sonne sol2 ré3 sol3 do4 sol4 : l'ensemble {sol, do, ré} avec sol à la basse. Une grille le nomme Gsus4, puisque le do descend d'ordinaire sur si et donne G. Le même ensemble est Csus2, écrit sur cette basse Csus2/G.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Cette leçon documente ce code et ne le modifie pas. Elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA, à `ba3b9ac`. Learn, le site de cours de l'écosystème, a un cours music-theory-ga dont les leçons compilent une version antérieure de GA, `a826864` ; les fichiers du reconnaisseur ont changé depuis. Sa leçon 3 [nomme une forme](https://github.com/spareilleux/learn/blob/89dc3e64d392cdc36844b03719880484d823b4d7/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L240) en essayant d'abord la basse, comme le fait une grille, et demande au catalogue de GA les intervalles mesurés depuis la basse. Cette leçon suit le reconnaisseur d'accords de GA, qui choisit lui-même la fondamentale.

**GA nomme un ensemble de classes de hauteurs sans sa basse.** [`CanonicalChordRecognizer.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L26-L39) prend un ensemble et une basse facultative. Son commentaire dit que [« Everything except the slash suffix is a function of the pitch-class set alone »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L30-L31) (tout, sauf le suffixe à barre oblique, ne dépend que de l'ensemble de classes de hauteurs), et la méthode garde [une réponse par ensemble](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L34). Pour trois classes de hauteurs ou plus :
- chaque note de l'ensemble est essayée comme fondamentale contre chaque motif du catalogue, et un motif peut [manquer un intervalle et en ajouter un](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L153-L166) ;
- les candidats sont [classés](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L178-L183) par distance (intervalles manquants plus intervalles en trop), puis selon qu'il ne manque rien, puis par la priorité du motif (le plus petit nombre d'abord), puis par un [score de fréquence de la fondamentale](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L362-L377) : do vaut 0, sol et fa 1, ré et si♭ 2, la et mi♭ 3, et ainsi de suite ;
- [« the bass note must NOT influence which pattern wins »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L171-L173) (la basse ne doit PAS influer sur le motif qui l'emporte) ;
- une basse différente de la fondamentale est ajoutée ensuite comme [suffixe à barre oblique](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L35-L38).

Un test passe [les 4096 ensembles avec chacune des 12 basses](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Chords/CanonicalChordRecognizerCacheTests.cs#L24-L46) et vérifie que la basse ne change que le suffixe. L'analyseur de voicings de GA passe la [note la plus grave du voicing comme basse](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L12-L17) et garde [le nom avec son suffixe](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L72-L80) comme nom d'accord du voicing.

**L'ensemble la do mi sol est toujours Am7.** Minor-7 a la [priorité 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L63) et major-6 la [priorité 10](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L55). Les deux lectures sont exactes, donc Am7 l'emporte quelle que soit la basse, et la forme de C6 x35555 est nommée `Am7/C`. La liste d'exclusions du test d'aller-retour le dit : [« major-6 [0,4,7,9] ≡ minor-7 at root 9 (priority 5 beats 10) »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L39) (major-6 équivaut à minor-7 sur la fondamentale 9, la priorité 5 bat 10). Son corpus de référence attend [Am7 pour x02010](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L424-L426). Le reconnaisseur ne peut pas donner le C6 de la cadence du §3.

**Les égalités vont à la fondamentale la plus fréquente.** sus2 et sus4 ont tous deux la [priorité 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L51-L52), donc entre deux lectures d'un ensemble sus, c'est le score de fréquence de la fondamentale qui décide. Sol vaut 1 et ré 2, donc le Dsus4 xx0233 est nommé `Gsus2/D`. Le corpus de référence [attend Gsus2](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L451-L456), et son commentaire explique ce choix par sus4 sur ré « (prio 8) » contre sus2 sur sol « (prio 7) ». Le catalogue leur donne 8 à tous deux : c'est le score de la fondamentale qui départage, pas la priorité. Le même commentaire dit que le « Dsus4 » du guitariste est « recovered » (retrouvé) sous la forme `Gsus2/D` ; c'est l'autre lecture du tableau du §4, pas le nom de grille. Csus4 et Dsus2 [sortent comme sur la grille](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L443-L449), parce que do a un score plus bas que fa, et ré plus bas que la. La septième diminuée a la [priorité 7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L66) sur chacune de ses quatre fondamentales, et la triade augmentée la [priorité 3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L50) sur chacune de ses trois, donc le score de la fondamentale suffit à les nommer.

**Les noms s'écrivent avec des bémols.** Les fondamentales et les suffixes viennent d'une même [liste de douze noms](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L379-L383), C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B, qui construit aussi les [suffixes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L51-L52). Un accord de fa♯ mineur est `Gbm`, et le D/F♯ de la descente est `D/Gb`. Le reconnaisseur travaille sur des classes de hauteurs, qui ne portent pas d'orthographe (MUS-007) ; l'indice que Wikipédia donne pour la fondamentale d'une septième diminuée lui est donc inaccessible.

**Un nom cache la neuvième.** Le catalogue liste deux fois l'ensemble do ré mi sol la : comme [major-6-add-9, priorité 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L57), et comme [6-9, priorité 54](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L111). Ses remarques appellent ces deux noms des [synonymes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L166-L168). Le constructeur de suffixes a un cas pour [« 6-9 »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L281) mais aucun pour major-6-add-9. Ce motif reçoit sa [qualité, son extension et ses altérations](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L293) à la suite : rien pour majeur, « 6 » pour la sixte, et rien pour « add9 », une [altération qui ne s'affiche pas](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L307). Lu, pas exécuté : do ré mi sol la a cinq lectures exactes, major-6-add-9 sur do, 9-sus4 sur ré, dominant-11 sur ré, 6-9 sur do et quartal-5 sur mi. La première a le plus petit nombre de priorité, donc le reconnaisseur nomme l'ensemble `C6`. Minor-6-add-9 transforme de même do ré mi♭ sol la en `Cm6`. Comme la do mi sol est Am7, un `C6` du reconnaisseur n'est jamais le C6 du §2 : il contient une neuvième. Le test d'aller-retour vérifie le nom du motif, la distance, la fondamentale et l'indicateur d'exactitude, [mais pas le nom qui s'affiche](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L134-L142), si bien qu'il passe.

**L'exemple symétrique du test n'est pas symétrique.** La liste d'exclusions dit que [« dominant-7-sharp-5 [0,4,8,10] is T4-symmetric — multiple roots, same set »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L43) (dominant-7-sharp-5 est symétrique par T4 : plusieurs fondamentales, même ensemble). Transposé de 4 demi-tons, do mi sol♯ si♭ devient mi sol♯ do ré, un autre ensemble. Ses seules lectures exactes sont sur do, sous deux noms pour les mêmes intervalles, [augmented-7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L68) et [dominant-7-sharp-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L95). L'aller-retour rend augmented-7, priorité 8 avant 30, et l'exclusion tient pour cette raison. Les accords de quatre notes du catalogue contiennent bien deux ensembles symétriques : la septième diminuée du §2, et [dominant-7-b5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L94), do mi sol♭ si♭, qu'une transposition d'un triton envoie sur lui-même : C7♭5 est aussi G♭7♭5.

**Les ensembles sans correspondance reçoivent un nom de Forte et pas de fondamentale.** Un ensemble dont aucun motif ne s'approche à un intervalle manquant et un intervalle en trop près est nommé par son [numéro de Forte](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L320-L356), sans fondamentale, et [seule une correspondance avec un motif](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L43-L44) peut porter un suffixe à barre oblique. Pour un tel ensemble, l'analyseur de voicings de GA [enregistre la basse comme fondamentale du voicing](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L84), écrite par [`PitchClass.ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L83-L88) sous forme de nombre, avec T pour 10 et E pour 11, là où un ensemble reconnu enregistre un nom de note. Le nom de l'accord n'en est pas affecté. MUS-020 traite du catalogue de Forte.

Corriger quoi que ce soit ici revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

D'après le classement de GA, que renvoie `Identify` pour do ré sol avec sol à la basse, et pour mi sol♯ do avec mi à la basse ?

> *Solution :* Pour do ré sol, Csus2 et Gsus4 sont tous deux exacts à la priorité 8, et do vaut 0 contre 1 pour sol, donc la fondamentale est do. Sol n'est pas la fondamentale, donc le nom est `Csus2/G`. Pour mi sol♯ do, Caug, Eaug et Abaug sont exacts à la priorité 3 ; do vaut 0, mi et la♭ 4, donc le nom est `Caug/E`.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA. L'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien dans cette section n'est une mesure :
- les prédictions viennent des §2 à §5 et sont écrites avant toute exécution ;
- les noms et les décomptes viennent d'une transcription Python, ligne par ligne, du reconnaisseur et de son catalogue de motifs ;
- une version ultérieure de cette leçon rapportera les résultats.

Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **La basse ne change que le suffixe.** Pour les huit formes du §4 et quatre autres, appeler `Identify` avec l'ensemble seul, puis avec la basse de la forme. Prédiction :

   | Forme | Sans la basse | Avec la basse |
   |------|------|------|
   | x02010 | Am7 | Am7 |
   | x35555 | Am7 | Am7/C |
   | xx0233 | Gsus2 | Gsus2/D |
   | x02230 | Dsus2 | Dsus2/A |
   | xx0230 | Dsus2 | Dsus2 |
   | 022200 | Asus2 | Asus2/E |
   | xx0101 | Fdim7 | Fdim7/D |
   | 032110 | Caug | Caug/E |
   | 3x0013 | Csus2 | Csus2/G |
   | x03221 | Faug | Faug/A |
   | 244222 | Gbm | Gbm |
   | 2x0232 | D | D/Gb |

2. **Le recensement.** Pour chacun des 4096 ensembles, appeler `Identify` et relever `MatchDistance`. Pour chaque ensemble de trois classes de hauteurs ou plus, compter les fondamentales auxquelles un motif du catalogue correspond exactement. Prédiction :
   - sur les 4017 ensembles de trois classes de hauteurs ou plus, 484 correspondent exactement, 1644 à distance 1 et 648 à distance 2, et 1241 se rabattent sur un nom de Forte ;
   - les seuls ensembles de quatre notes qui se rabattent sont les six transpositions de do ré♭ sol♭ sol ;
   - 124 ensembles ont des lectures exactes sur deux fondamentales ou plus. À transposition près, ils sont 15 : l'ensemble sus2, l'ensemble 7sus4, l'ensemble 7sus2, m7♭5, m7, 7♭5, la triade augmentée, la septième diminuée, 7♭9♯9, l'ensemble 6/9, m11, 7♭9♯11, et les gammes augmentée, par tons et octotonique.
3. **Les accords de sixte.** Compter les ensembles dont le nom finit par `6` mais pas par `m6`, et ceux dont le nom finit par `m6`, et vérifier pour chacun la neuvième au-dessus de sa fondamentale ; compter les noms qui finissent par `6/9`. Prédiction : 48 et 60 ensembles, tous avec leur neuvième, et aucun ensemble nommé 6/9 ou m6/9. L'ensemble la do mi sol est nommé Am7, et do mi♭ sol la, Am7b5.
4. **L'exemple symétrique.** Identifier do mi sol♯ si♭ et sa transposition de 4 demi-tons, puis do mi sol♭ si♭ et sa transposition de 6. Prédiction : `Caug7` et `Eaug7`, deux ensembles différents ; `C7b5` les deux fois, un seul ensemble.

### Exercice pratique

L'étape 2 prédit 124 ensembles ayant des lectures exactes sur deux fondamentales ou plus, issus de 15 ensembles à transposition près. Pourquoi la triade augmentée et la septième diminuée ne comptent-elles que pour 4 et 3 ensembles, quand la do mi sol et ses transpositions comptent pour 12 ?

> *Solution :* Un ensemble qui s'envoie sur lui-même par une transposition a moins de transpositions distinctes. La triade augmentée s'envoie sur elle-même par 4 demi-tons, elle a donc 12 / 3 = 4 transpositions ; la septième diminuée s'envoie sur elle-même par 3 demi-tons, elle en a donc 12 / 4 = 3. L'ensemble la do mi sol ne s'envoie sur lui-même par aucune transposition sauf T0, il en a donc 12.

---

## 7. Pièges courants

- **Prendre la basse pour la fondamentale.** C/E a pour fondamentale do ; la basse est une propriété du voicing.
- **Lire la barre oblique comme « ou ».** C/E signifie un accord de do sur mi.
- **Déclarer une lecture fausse.** C6 et Am7/C sont les mêmes notes ; l'harmonie décide quelle fondamentale nommer.
- **Nommer une septième diminuée d'après son ensemble.** Chacune de ses notes peut être la fondamentale ; l'orthographe et la résolution décident.
- **Se fier au `C6` de GA.** Venant du reconnaisseur, il contient une neuvième : c'est un accord 6/9.
- **Prendre le nom à barre oblique de GA pour le nom de grille.** `Gsus2/D` est l'autre lecture de Dsus4, choisie par le score de fréquence de la fondamentale de GA.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Ensemble de classes de hauteurs** | Les notes d'un accord sans les octaves ni les redoublements, comme {0, 4, 7} |
| **Basse** | La note la plus grave qui sonne ; une propriété du voicing |
| **Fondamentale** | La note qui donne son nom à un accord ; pour un accord en tierces, la note la plus grave de l'empilement de tierces |
| **Renversement** | Un voicing d'un accord avec à la basse une note de l'accord autre que la fondamentale |
| **Accord à barre oblique** | Un symbole d'accord suivi de sa basse, comme C/E |
| **Lecture** | Une fondamentale et un type d'accord qui donnent ensemble exactement un ensemble : C6 et Am7 sont deux lectures de la do mi sol |
| **Accord symétrique** | Un accord dont l'ensemble s'envoie sur lui-même par une transposition autre que T0, comme la triade augmentée et la septième diminuée |
| **Fréquence de la fondamentale** | Le départage de GA entre des lectures également bonnes : do d'abord, puis sol et fa, puis ré et si♭, et ainsi de suite |

---

## Auto-évaluation

**1. Donnez l'ensemble, la basse et les deux lectures de 8x798x, et le nom qu'écrirait une grille après G7 en do majeur.**
> 8x798x sonne do3 la3 mi4 sol4 : l'ensemble {do, mi, sol, la}, avec do à la basse. Les lectures sont C6 et Am7, écrites sur cette basse C6 et Am7/C. Après G7 en do majeur, la grille écrit C6.

**2. Pourquoi n'importe quelle note d'un accord de septième diminuée peut-elle être sa fondamentale, et qu'est-ce qui indique la fondamentale dans la musique écrite ?**
> Ses quatre notes divisent l'octave en quatre tierces mineures, si bien que l'ensemble est le même empilement de tierces mineures à partir de chacune d'elles. L'orthographe indique la fondamentale, là où commence l'empilement de tierces écrit, et la résolution indique la fonction.

**3. Pourquoi GA nomme-t-il l'Asus4 x02230 `Dsus2/A` ?**
> Son ensemble {la, ré, mi} est exactement Asus4 et exactement Dsus2. Les deux motifs ont la priorité 8, et le score de fréquence de la fondamentale préfère ré (2) à la (3). La basse, la, n'est pas cette fondamentale, donc GA ajoute `/A`.

**4. Dans GA à `5c3a52a`, que contient un `C6` du reconnaisseur, et pourquoi ?**
> Do, ré, mi, sol et la, neuvième comprise. GA nomme l'ensemble 6/9 par son motif major-6-add-9, dont le « add9 » ne s'affiche pas. Le C6 simple, la do mi sol, est toujours Am7.

**Critères de réussite :** Distinguer la fondamentale, la basse et l'ensemble dans n'importe quel voicing. Énumérer les lectures d'un ensemble, symétriques comprises. Choisir une lecture par la basse, l'harmonie et la résolution, et l'écrire en accord à barre oblique au besoin. Dire comment GA nomme un ensemble, et où son nom diffère de celui d'une grille.

---

## Bases de recherche

- Wikipédia, « Root (chord) » : la méthode de l'empilement de tierces et la fondamentale d'un accord suspendu.
- Wikipédia, « Slash chord » : la barre oblique, qui « does not indicate 'or' », la descente, et les accords à barre oblique des arrangeurs.
- Wikipédia, « Sixth chord » : C6 comme Am7 au premier renversement, et les noms de do mi♭ sol la.
- Wikipédia, « Suspended chord » : la quarte qui se résout sur la tierce.
- Wikipédia, « Diminished seventh chord » : les trois accords distincts, la fondamentale par l'orthographe, et la résolution plutôt que l'orthographe.
- Wikipédia, « Augmented triad » : A♭+ orthographié la♭–do–mi.
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne.
- Learn, leçon 3 de music-theory-ga au commit `89dc3e64d392cdc36844b03719880484d823b4d7` : comment son laboratoire nomme une forme.
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre.
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue.
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
