---
module_id: mus-014-inversions-bass-line
department: music
course: Renversements et ligne de basse
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-013-root-bass-pitch-class-set]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Renversements et ligne de basse — Mêmes notes, autre basse

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Nommer la position d'un accord d'après sa seule basse : état fondamental, premier, deuxième ou troisième renversement
- Écrire le chiffrage de basse chiffrée de chaque position d'une triade et d'un accord de septième, et distinguer le chiffre 6 du C6 du jazz
- Reconnaître les quatre sortes d'accord de quarte et sixte et jouer chacune à la guitare
- Dire où la position ne se lit pas sur les seules notes qui sonnent, et retracer comment GA traite les renversements dans son type `Chord`, ses documents de voicing et son catalogue de modes

---

## 1. Mêmes notes, autre basse

MUS-013 a séparé la fondamentale d'un accord de sa basse. La **position** d'un accord dit laquelle de ses notes est à la basse. L'article « Inversion (music) » de Wikipédia : « A chord's inversion describes the relationship of its lowest notes to the other notes in the chord. » (Le renversement d'un accord décrit le rapport entre ses notes les plus graves et les autres notes de l'accord.) Avec la fondamentale à la basse, l'accord est à l'état fondamental ; avec une autre note, il est renversé. « The inversions are numbered in the order their lowest notes appear in a close root-position chord (from bottom to top) » (les renversements sont numérotés dans l'ordre où leurs notes les plus graves apparaissent dans l'accord serré à l'état fondamental, de bas en haut) : la tierce donne le premier renversement, la quinte le deuxième, et dans un accord de septième, la septième donne le troisième. Un accord de trois notes a deux renversements ; « Chords with four notes (such as seventh chords) work in a similar way, except that they have three inversions » (les accords de quatre notes, comme les accords de septième, fonctionnent de la même façon, sauf qu'ils ont trois renversements). Le même article note que certains textes réservent le terme « inversion » (renversement) à une basse autre que la fondamentale et emploient **position** pour tous les cas ; cette leçon fait de même.

| Position | Basse | Position serrée | Au-dessus de la basse (demi-tons) |
|------|------|------|------|
| État fondamental | do, la fondamentale | do mi sol | tierce majeure (4), quinte juste (7) |
| Premier renversement | mi, la tierce | mi sol do | tierce mineure (3), sixte mineure (8) |
| Deuxième renversement | sol, la quinte | sol do mi | quarte juste (5), sixte majeure (9) |

Les intervalles au-dessus de la basse changent avec la position, et c'est pourquoi chacune sonne différemment : Wikipédia donne au premier renversement « the intervals of a minor third and a minor sixth above the inverted bass of E » (les intervalles de tierce mineure et de sixte mineure au-dessus de la basse renversée, mi). La fondamentale ne change pas. Dans son *Traité de l'harmonie* (1722), Rameau tenait les positions d'un accord pour « functionally equivalent » (équivalentes sur le plan fonctionnel ; « Inversion (music) »).

Seule la basse compte. L'ordre des notes au-dessus d'elle, leurs octaves et leurs redoublements ne changent pas la position. Sur les trois cordes aiguës, les positions serrées de do sont des rotations les unes des autres :

| Forme | Notes, corde 6 d'abord | Basse | Position |
|------|------|------|------|
| xxx553 | do4 mi4 sol4 | do | état fondamental |
| xxx988 | mi4 sol4 do5 | mi | premier renversement |
| xxx010 | sol3 do4 mi4 | sol | deuxième renversement |

Les formes ouvertes x32010, 032010 et 332010 de MUS-013 contiennent les trois mêmes positions sur cinq ou six cordes. Les renversements permettent aussi à une ligne de basse d'avancer par degrés conjoints pendant que les accords changent : C – G/B – Am, joué x32010 – x20003 – x02210, fait descendre la basse par do3, si2, la2, avec G au premier renversement.

### Exercice pratique

Donnez la position de 2x0232 et de x00232.

> *Solution :* 2x0232 fait sonner fa♯2 ré3 la3 ré4 fa♯4. L'accord est ré majeur, et fa♯, sa tierce, est à la basse : premier renversement. x00232 fait sonner la2 ré3 la3 ré4 fa♯4 : la, la quinte, est à la basse, c'est donc le deuxième renversement, D/A.

---

## 2. La basse chiffrée

La basse chiffrée écrit un accord en chiffres placés à côté de sa basse. L'article « Figured bass » de Wikipédia les place « above or below (or next to) a bass note » (au-dessus ou au-dessous d'une note de basse, ou à côté) : « The numbers indicate the number of scale steps above the given bass-line that a note should be played. » (Les chiffres indiquent à combien de degrés au-dessus de la ligne de basse donnée une note doit être jouée.) Les degrés se comptent par noms de notes, comme pour les numéros d'intervalles (MUS-008) : au-dessus de sol, do est une quarte (sol la si do) et mi une sixte. Les chiffres « do not express notes in upper voices that double, or are unison with, the bass note » (n'expriment pas les notes des voix supérieures qui redoublent la basse ou sont à l'unisson avec elle ; « Inversion (music) »), et ils ignorent d'ordinaire les octaves : un chiffrage nomme une position, pas un voicing.

Chaque position a un chiffrage complet et une abréviation usuelle. Les triades à l'état fondamental « appear without symbols (the 53 is understood) » (apparaissent sans symbole, le 53 étant sous-entendu), et « first-inversion triads are customarily abbreviated as just 6 » (les triades au premier renversement s'abrègent d'ordinaire en un simple 6 ; « Inversion (music) ») :

| Position de la triade | Chiffrage complet | Écrit |
|------|------|------|
| État fondamental | 5/3 | rien |
| Premier renversement | 6/3 | 6 |
| Deuxième renversement | 6/4 | 6/4 |

Pour les accords de septième, « Seventh chord » donne les quatre positions de G7, sol si ré fa, avec V7, V6/5, V4/3 et V4/2 ou V2 :

| Position | Basse | Position serrée | Chiffrage complet | Écrit |
|------|------|------|------|------|
| État fondamental | sol | sol si ré fa | 7/5/3 | 7 |
| Premier renversement | si | si ré fa sol | 6/5/3 | 6/5 |
| Deuxième renversement | ré | ré fa sol si | 6/4/3 | 4/3 |
| Troisième renversement | fa | fa sol si ré | 6/4/2 | 4/2 ou 2 |

« Figured bass » confirme la dernière ligne : un 2 seul ou un 4/2 vaut 6/4/2. En analyse, le chiffrage suit un chiffre romain : « the term I6 refers to a tonic triad in first inversion » (le terme I6 désigne une triade de tonique au premier renversement ; « Inversion (music) »). Il peut aussi suivre une note de basse : une triade de do majeur sur sol « would be written G64 » (s'écrirait G64), et sur mi « E63 or E6 (this is different from the jazz notation, where a C6 means the added sixth chord C–E–G–A, i.e., a C major with an added 6th degree) » (E63 ou E6, ce qui diffère de la notation jazz, où C6 désigne l'accord de sixte ajoutée do–mi–sol–la, c'est-à-dire un do majeur avec un sixième degré ajouté ; « Figured bass »). Cités en texte brut, les chiffres superposés se suivent : G64 est sol avec 6/4, E63 est mi avec 6/3, et 53 est 5/3. Le C6 d'une grille est un accord de quatre notes avec do à la basse ; le chiffrage E6 est une triade de do avec mi à la basse.

### Exercice pratique

Écrivez le chiffrage de chaque accord sur sa basse : D/A, Am/C, G7/D, G7/F.

> *Solution :* D/A : au-dessus de la, ré est une quarte et fa♯ une sixte, donc 6/4 : la triade a sa quinte à la basse. Am/C : au-dessus de do, mi est une tierce et la une sixte, donc 6. G7/D : au-dessus de ré, fa est une tierce, sol une quarte et si une sixte, donc 6/4/3, écrit 4/3. G7/F : au-dessus de fa, sol est une seconde, si une quarte et ré une sixte, donc 6/4/2, écrit 4/2 ou 2.

---

## 3. L'accord de quarte et sixte

Parmi les positions d'une triade, seul le deuxième renversement place une quarte au-dessus de la basse. L'article « Six-four chord » de Wikipédia : « the bass note and the root of the chord are a fourth apart (or a corresponding compound interval) which traditionally qualifies as a dissonance. There is therefore a tendency for movement and resolution. » (la basse et la fondamentale de l'accord sont à distance de quarte, ou de l'intervalle composé correspondant, ce qui compte traditionnellement comme une dissonance. D'où une tendance au mouvement et à la résolution.) Le voicing au-dessus de la basse est libre : « Note that any voicing above the bass is allowed. » (Notez que tout voicing au-dessus de la basse est permis.) Un accord de quarte et sixte est rarement un point de repos, et le même article classe ses emplois : « There are four types of second-inversion chords: cadential, passing, auxiliary, and bass arpeggiation. » (Il existe quatre types d'accords au deuxième renversement : de cadence, de passage, de broderie et d'arpège de basse.)

| Type | En do majeur | Formes | Ce qui bouge |
|------|------|------|------|
| De cadence | C/G – G – C, I6/4 – V – I | 332010 – 320003 – x32010 | Sur sol2, do3 descend à si2 et mi3 à ré3 : la quarte et la sixte descendent sur la tierce et la quinte |
| De passage | C – G/D – C/E, I – V6/4 – I6 | x32010 – xx0003 – xx2010 | La basse avance par degrés do3, ré3, mi3 ; le sol3 à vide est tenu |
| De broderie (pédale, auxiliaire) | C – F/C – C, I – IV6/4 – I | x32010 – x33211 – x32010 | Sur do3, mi3 monte à fa3 et sol3 à la3, puis les deux redescendent |
| Arpège de basse | C – C/E – C/G | x32010 – 032010 – 332010 | La basse joue do3, mi2, sol2 sous un seul accord |

- **De cadence.** « Six-four chord » en donne deux lectures. L'une, celle de la plupart des anciens manuels d'harmonie, voit dans l'accord une tonique au deuxième renversement, I6/4 – V – I. L'autre, que préfèrent plusieurs manuels modernes, entend la dominante avec « a double appoggiatura on the V that resolves down by step » (une double appoggiature sur le V qui se résout en descendant par degré conjoint), notée V6/4 – 5/3 : la basse sol est déjà la dominante, et do et mi sont des dissonances qui se résolvent sur si et ré.
- **De passage.** Dans un accord de quarte et sixte de passage, « the bass passes between two tones a third apart » (la basse passe entre deux notes à distance de tierce), et l'accord, placé entre deux accords plus stables, tombe « on the weaker beat between these two chords » (sur le temps le plus faible, entre ces deux accords).
- **De broderie.** Le IV6/4 harmonise une note de broderie : « the third and fifth rise a step each and then fall back » (la tierce et la quinte montent chacune d'un degré, puis redescendent).
- **Arpège de basse.** La basse parcourt la fondamentale, la tierce et la quinte d'un même accord ; la quinte à la basse fait un accord de quarte et sixte, mais rien n'a besoin de se résoudre.

### Exercice pratique

Une progression en do majeur enchaîne Am – C/G – G7 – C. Quelle sorte d'accord de quarte et sixte est C/G, et comment peut-on le lire ?

> *Solution :* C'est un accord de quarte et sixte de cadence : il tombe avant la dominante d'une cadence. Une lecture l'appelle I6/4, la tonique au deuxième renversement. L'autre entend la dominante déjà à la basse, sol, avec do et mi en double appoggiature qui descend sur si et ré : V6/4 – 5/3, G7 ajoutant sa septième, fa, à la résolution.

---

## 4. Quand les notes ne décident pas

Une position se mesure depuis une fondamentale, et les notes qui sonnent ne fixent pas toujours la fondamentale.

- **Deux lectures, deux positions.** MUS-013 a montré que do mi sol la est à la fois C6 et Am7. Sur do, c'est C6 à l'état fondamental, ou Am7/C au premier renversement. La basse chiffrée ne nomme aucune fondamentale et écrit le même chiffrage pour les deux : au-dessus de do, mi est une tierce, sol une quinte et la une sixte, donc 6/5, le chiffrage d'un accord de septième au premier renversement.
- **L'orthographe décide du chiffrage.** Les chiffres comptent des noms de notes, et un accord symétrique peut s'orthographier à partir de n'importe laquelle de ses notes. Mi sol♯ do sur mi est la triade augmentée Caug au premier renversement : de mi à do, il y a une sixte, donc le chiffrage est 6. Orthographié mi sol♯ si♯, c'est Eaug à l'état fondamental : de mi à si♯, il y a une quinte, donc le chiffrage est 5/3. Les deux font 8 demi-tons.
- **La septième diminuée.** Dans chaque position de si ré fa la♭, les notes au-dessus de la basse se trouvent 3, 6 et 9 demi-tons plus haut, si bien que le son ne montre pas la position. Les noms de notes, eux, la montrent : si ré fa la♭ donne 7/5/3, ré fa la♭ si 6/5/3, fa la♭ si ré 6/4/3, et la♭ si ré fa 6/4/2. Comme MUS-013 l'a cité d'après « Diminished seventh chord » : « Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling. » (Comprendre dans quel renversement un accord de septième diminuée est écrit, et donc trouver sa fondamentale, dépend de son orthographe enharmonique.)

### Exercice pratique

Donnez le chiffrage et la position de la♭ si ré fa sur la♭, et du même son orthographié sol♯ si ré fa sur sol♯.

> *Solution :* Au-dessus de la♭, si est une seconde (la si), ré une quarte et fa une sixte : 6/4/2, le troisième renversement de B°7, si ré fa la♭. Au-dessus de sol♯, si est une tierce, ré une quinte et fa une septième (de sol à fa) : 7/5/3, G♯°7 à l'état fondamental.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Cette leçon documente ce code et ne le modifie pas. Elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA, à `e610b77`, sauf deux : dans `Modes.yaml`, les lignes citées sont inchangées, et dans `ModesSkill.cs`, le code cité est inchangé mais à d'autres numéros de ligne. Cette leçon suit les renversements à travers trois endroits de GA.

**`Chord` compte par rotation.** [`Bass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L260-L263) vaut `Notes[0]`, documentée comme la « lowest note in the voicing » (note la plus grave du voicing). [`GetInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L281-L298) renvoie 0 quand la basse est la fondamentale ; sinon, elle cherche la fondamentale dans la liste des notes et renvoie le nombre de notes qui vont de la fondamentale à la fin de la liste. [`ToInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L300-L320) fait tourner la liste. Un accord construit à partir d'un symbole range ses notes dans l'[ordre de sa formule](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L43), do mi sol pour C, si bien que les rotations mi sol do et sol do mi comptent 1 et 2. Les tests [`Inversions_ShouldWorkCorrectly`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Harmony/ChordTests.cs#L123-L143) et [`ToInversion_PreservesFormulaAndSymbol`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L134-L154) le vérifient pour C, Cm, Cmaj7, C9 et C13.

Learn, le site de cours de l'écosystème, a un cours music-theory-ga dont le laboratoire compile une version antérieure de GA, `a826864`. Sa [leçon 3](https://github.com/spareilleux/learn/blob/aaf6d3e52490d159ab962c75928e88c0dae28c28/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L174-L195) a constaté que `ToInversion` analysait à nouveau les notes après rotation et perdait la tierce d'un premier renversement, en affichant la qualité `Other` pour C/E. À `5c3a52a`, `ToInversion` passe par un [constructeur privé](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L64-L71) qui copie la fondamentale, la formule, le symbole et l'ensemble, et ne remplace que les notes. Deux faits comptent pour les renversements :
- **Le symbole n'a pas de barre oblique.** Le premier renversement de C a la basse mi et s'affiche `C`, puisque le constructeur copie le symbole : [`ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L367) renvoie le symbole, et le test [vérifie qu'il est inchangé](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L149).
- **L'égalité ignore la basse.** [`Equals`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L277) et [`GetHashCode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L365) ne comparent que l'ensemble et la fondamentale, si bien que C est égal à ses renversements, comme l'aurait voulu Rameau.

**Les notes dans un autre ordre sont mal comptées.** Le [constructeur à partir de notes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L48-L62) garde les notes dans l'ordre donné. Lu, pas exécuté, avec la fondamentale do :

| Notes | Basse | Position | `GetInversion` |
|------|------|------|------|
| mi sol do | mi, la tierce | premier renversement | 1 |
| mi do sol | mi, la tierce | premier renversement | 2 |
| sol do mi | sol, la quinte | deuxième renversement | 2 |
| sol mi do | sol, la quinte | deuxième renversement | 1 |

`GetInversion` ne regarde que l'endroit où la fondamentale apparaît pour la première fois dans la liste, et compte les notes de là jusqu'à la fin. En position serrée, sans redoublement, ce compte donne le renversement ; d'autres ordres et des redoublements peuvent fausser ce compte : mi sol do mi, avec mi redoublé en haut, compte 2. Un accord à l'état fondamental compte 0 dans n'importe quel ordre, puisque la basse est la fondamentale. `ToInversion` hérite de l'erreur : à partir de mi do sol, `ToInversion(1)` renvoie sol mi do, avec la quinte à la basse, et `GetInversion` dit alors 1. Le [test de ce constructeur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L156-L162) passe mi sol do, un ordre qui compte juste, et vérifie la qualité et la formule, pas le renversement. La leçon 3 de Learn juge `GetInversion` correcte ; elle l'est, pour les rotations que cette leçon teste.

**Le document de voicing compte des demi-tons.** GA décrit un voicing par un document pour sa recherche. [`VoicingDocumentFactory`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L22-L28) prend la note la plus grave comme basse et, comme fondamentale, celle du reconnaisseur d'accords de MUS-013, via [`TryGetRootPitchClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L19-L29). [`CalculateInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L88-L96) convertit ensuite les demi-tons qui mènent de la fondamentale à la basse, en montant : 0 donne l'état fondamental ; 3 ou 4 donnent 1 ; 6 ou 7 donnent 2 ; 10 ou 11 donnent 3 ; toute autre distance donne −1. Lu, pas exécuté, avec les noms du reconnaisseur transcrits depuis son code ; comme dans MUS-013, la colonne des notes nomme chaque case avec des dièses :

| Forme | Nom de grille | Notes, corde 6 d'abord | Nom du reconnaisseur | Basse au-dessus de la fondamentale de GA | Renversement |
|------|------|------|------|------|------|
| 032010 | C/E | mi2 do3 mi3 sol3 do4 mi4 | `C/E` | 4 | 1 |
| 332010 | C/G | sol2 do3 mi3 sol3 do4 mi4 | `C/G` | 7 | 2 |
| 1x0003 | G7/F | fa2 ré3 sol3 si3 sol4 | `G7/F` | 10 | 3 |
| x35555 | C6 | do3 sol3 do4 mi4 la4 | `Am7/C` | 3 | 1 |
| xx0233 | Dsus4 | ré3 la3 ré4 sol4 | `Gsus2/D` | 7 | 2 |
| 032110 | Eaug | mi2 do3 mi3 sol♯3 do4 mi4 | `Caug/E` | 4 | 1 |
| 4x2110 | A♭aug | sol♯2 mi3 sol♯3 do4 mi4 | `Caug/Ab` | 8 | −1 |
| xx0101 | Ddim7 | ré3 sol♯3 si3 fa4 | `Fdim7/D` | 9 | −1 |

- **Le nombre suit la fondamentale de GA.** Le C6 et le Dsus4 des grilles sont à l'état fondamental ; GA les lit comme Am7 et Gsus2, et donne donc 1 et 2. Eaug, A♭aug et Ddim7 sont aussi à l'état fondamental sur une grille, mais GA les mesure depuis do, do et fa.
- **Le document laisse tomber la barre oblique.** Son `ChordName` [préfère le nom canonique du reconnaisseur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L43-L46), que le nom avec barre oblique [ne fait que prolonger](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L417-L419) : le document de 032010 s'appelle `C`, et celui de 4x2110 `Caug`.
- **Deux distances des triades et des accords de septième manquent.** Une triade augmentée avec sa quinte à la basse a cette basse à 8 demi-tons au-dessus de la fondamentale, et une septième diminuée avec sa septième à la basse l'a à 9 : toutes deux reçoivent −1, là où les lectures choisies par GA en font un deuxième et un troisième renversement. De même pour toute basse à 1, 2 ou 5 demi-tons au-dessus de la fondamentale.
- **Les consommateurs le lisent tel quel.** Quand le service de recherche de GA indexe des documents, il [copie chaque renversement](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/EnhancedVoicingSearchService.cs#L120) dans l'entrée, et [`VoicingFilterEngine`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/VoicingFilterEngine.cs#L105) ne garde une entrée que si son renversement est égal à celui du filtre, si bien qu'une recherche de deuxièmes renversements écarte 4x2110. [`AutoTaggingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Enrichment/AutoTaggingService.cs#L164-L168) n'ajoute une étiquette `Inversion:n` que si n est supérieur à 0, si bien qu'un −1 ne reçoit pas d'étiquette, comme un état fondamental.
- **Les tests s'arrêtent à C/E.** Le test de la fabrique [attend 1 pour C/E et 0 pour quatre formes à l'état fondamental](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/VoicingDocumentFactoryTests.cs#L21-L25). Un test de recherche filtre sur 2, avec un [document de fixture](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/SemanticSearchTestFixture.cs#L243-L246) dont le renversement est fixé à la main. Un test d'indexation [passe 100 voicings générés à l'indexeur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/VoicingIndexingServiceTests.cs#L18-L34), qui construit des documents par la fabrique, mais il ne vérifie aucun renversement. Aucun test ne vérifie ce que `CalculateInversion` donne pour un deuxième ou un troisième renversement, ni pour une distance qu'elle convertit en −1.

**Les renversements de triades du catalogue sont mal étiquetés.** Le fichier `Modes.yaml` de GA liste les triades comme des [familles modales](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L424-L492), chacune avec des entrées nommées comme des renversements, toutes avec do à la basse :

| Entrée | Notes | Alias | Ce que sont les notes | Chiffrage |
|------|------|------|------|------|
| [Minor Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L432-L436) | do mi♭ la♭ | Minor 6/4 | la♭ majeur, premier renversement | 6 |
| [Minor Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L437-L441) | do fa la | Minor 6/4 | fa majeur, deuxième renversement | 6/4 |
| [Major Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L442-L446) | do fa la♭ | Major 6/4 | fa mineur, deuxième renversement | 6/4 |
| [Major Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L447-L451) | do mi la | Major 6/4 | la mineur, premier renversement | 6 |
| [Diminished Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L465-L469) | do mi la | Diminished 6/4 | la mineur, premier renversement | 6 |
| [Diminished Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L470-L474) | do fa♯ si♭ | Diminished 6/4 | pas de triade : classe d'ensembles 3-8 | — |
| [Augmented Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L483-L487) | do fa la | Augmented 6/4 | fa majeur, deuxième renversement | 6/4 |
| [Augmented Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L488-L492) | do mi♭ fa♯ | Augmented 6/4 | do diminué, état fondamental, écrit do mi♭ sol♭ | 5/3 |

Aucune entrée ne nomme ses notes. La famille majeure contient les quatre bons ensembles, les renversements de la♭ et fa majeurs et de la et fa mineurs sur do, sous des noms intervertis. Les deux autres familles contiennent d'autres triades, et un ensemble qui n'est pas une triade. Chaque alias dit 6/4, mais seules trois des huit entrées sont des accords de quarte et sixte. Sur do, les renversements de la triade diminuée sont do mi♭ la et do fa♯ la, et la triade augmentée est do mi sol♯ dans toutes les positions, réorthographiée (§4). Le chiffrage de la dernière ligne suppose lui aussi la réorthographie : tel qu'il est écrit, fa♯ est une quarte au-dessus de do. Le vecteur d'intervalles de la famille augmentée, [<0 1 0 0 2 0>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L476), n'est pas non plus celui de la triade augmentée, <0 0 0 3 0 0>.

`AtonalModalFamilies.yaml` [importe ces noms par ensemble](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L9-L10). La famille de la triade majeure reçoit [les quatre noms](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L185-L204). Les vrais renversements de la triade diminuée, {0, 3, 9} et {0, 6, 9}, [n'en reçoivent aucun](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L220-L229). {0, 6, 10} [porte « Diminished Triad Second Inversion »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L290-L294), ce qui donne aussi à sa famille [le nom « Diminished Triad Family »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L256-L259), le nom de [la vraie](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L206-L207). Le fichier numérote aussi ces deux familles [3-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L258) et [3-3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L208), là où la liste de Forte donne 3-8 et 3-10. Quand le `ModesSkill` de GA trouve un vecteur d'intervalles dans une question, il [répond à partir de ce fichier](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L560-L568) [avant toute autre chose](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L156-L164), et [liste chaque mode de la famille](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L628-L656) sous ce nom avec ses classes de hauteurs, avec une confiance de 1.0.

Corriger quoi que ce soit ici revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

Dans GA à `5c3a52a`, quels sont la basse, le numéro de renversement et le nom affiché du troisième renversement de `Chord.FromSymbol("G7")` ? Quel renversement le document de voicing donne-t-il à G7/F, 1x0003 ?

> *Solution :* Les notes sol si ré fa tournent en fa sol si ré : basse fa, `GetInversion` 3, et l'accord s'affiche `G7`, puisque le symbole est conservé. Pour 1x0003, le reconnaisseur donne `G7/F` ; fa est à 10 demi-tons au-dessus de sol, donc `CalculateInversion` donne 3. Les deux disent troisième renversement, et aucun des deux noms ne montre la basse : le document s'appelle `G7`, lui aussi.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA. L'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien dans cette section n'est une mesure :
- les prédictions viennent du §5 et sont écrites avant toute exécution ;
- elles viennent d'une transcription Python, ligne par ligne, de `Chord`, de `CalculateInversion` et du reconnaisseur d'accords, et de la lecture des deux fichiers de catalogue de GA ;
- une version ultérieure de cette leçon rapportera les résultats.

Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Rotations à partir de symboles.** Pour C, Cmaj7, G7 et C6 construits avec `Chord.FromSymbol`, appeler `ToInversion(k)` pour chaque k, et relever `Bass`, `GetInversion`, `Symbol` et `Equals` avec l'original. Prédiction : la basse est la note de rang k, en comptant depuis 0, dans do mi sol, do mi sol si, sol si ré fa et do mi sol la ; `GetInversion` renvoie k ; le symbole ne change pas ; `Equals` est vrai.
2. **Ordres.** Construire `new Chord(AccidentedNoteCollection.Parse(...), C)` à partir de mi sol do, mi do sol, sol do mi et sol mi do, et appeler `GetInversion` ; puis appeler `ToInversion(1)` sur l'accord mi do sol. Prédiction : 1, 2, 2 et 1 ; puis les notes sol mi do, avec `GetInversion` 1.
3. **Documents de voicing.** Pour les huit formes du tableau du §5, construire le document de voicing comme le fait `VoicingDocumentFactoryTests`, chaque diagramme écrit corde 1 d'abord (032010 devient `0-1-0-2-3-0`), et relever `RootPitchClass`, `MidiBassNote` et `Inversion`. Prédiction, dans l'ordre du tableau : les fondamentales 0, 0, 7, 9, 7, 0, 0 et 5 ; les basses 40, 43, 41, 48, 50, 40, 44 et 50 ; les renversements 1, 2, 3, 1, 2, 1, −1 et −1.
4. **Le catalogue.** Charger la configuration des modes de GA et ses familles modales atonales, et, pour chaque mode dont le nom contient « Inversion », identifier la triade que forment ses notes sur do. Prédiction : le tableau du §5, aucune entrée ne nommant ses notes ; dans le fichier atonal, {0, 3, 9} et {0, 6, 9} n'ont pas de nom tonal.

### Exercice pratique

L'étape 3 prédit −1 pour 4x2110. Comment une grille le nomme-t-elle, quelle position la lecture de GA lui donne-t-elle, et quelle distance `CalculateInversion` manque-t-elle ?

> *Solution :* Une grille nomme d'ordinaire la lecture dont la fondamentale est à la basse : A♭aug, à l'état fondamental. Le reconnaisseur prend do pour fondamentale, `Caug/Ab` ; pour do, la basse est la quinte augmentée sol♯, si bien que la forme est un deuxième renversement, avec la basse à 8 demi-tons au-dessus de do. `CalculateInversion` ne reconnaît une quinte à la basse qu'à 6 ou 7 demi-tons, la quinte diminuée et la quinte juste.

---

## 7. Pièges courants

- **Lire la position sur la note du dessus ou sur la forme.** Seule la basse compte : xxx988 et 032010 sont tous deux des premiers renversements.
- **Lire le C6 du jazz comme le chiffrage 6.** C6 ajoute la à une triade de do sur do ; le chiffrage E6 est une triade de do sur mi.
- **Traiter un accord de quarte et sixte comme un accord de repos.** La quarte au-dessus de la basse est une dissonance ; l'accord passe, brode, arpège ou se résout sur une dominante.
- **Donner une position sans fondamentale.** Sur do, do mi sol la est à l'état fondamental comme C6 et au premier renversement comme Am7/C.
- **Lire une position en demi-tons.** La septième diminuée a 3, 6 et 9 demi-tons au-dessus de sa basse dans toutes ses positions ; seule l'orthographe les distingue.
- **Se fier aux noms de GA pour les renversements de triades.** Aucune des huit entrées de `Modes.yaml` ne nomme ses notes.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Position** | La note de l'accord qui est à la basse : état fondamental, ou un renversement |
| **État fondamental** | La fondamentale à la basse |
| **Premier, deuxième, troisième renversement** | La tierce, la quinte ou la septième à la basse |
| **Basse chiffrée** | Des chiffres à côté d'une note de basse pour les intervalles au-dessus d'elle, comptés par noms de notes |
| **Chiffrage** | Ces chiffres, d'ordinaire abrégés : 6, 6/4, 7, 6/5, 4/3, 4/2 |
| **Accord de quarte et sixte** | Une triade au deuxième renversement, avec une quarte et une sixte au-dessus de la basse |
| **Quarte et sixte de cadence** | I6/4 avant V, ou la dominante avec une double appoggiature, V6/4 – 5/3 |
| **Quarte et sixte de passage, de broderie, d'arpège** | Un accord de quarte et sixte sur une basse qui passe par degrés entre deux notes à distance de tierce ; sur une basse tenue, avec deux voix qui montent d'un degré et reviennent ; sous une basse qui parcourt un seul accord |

---

## Auto-évaluation

**1. Donnez la position et le chiffrage de Em/G, 3x2000, et de Am/E, 002210.**
> 3x2000 fait sonner sol2 mi3 sol3 si3 mi4 : sol, la tierce de mi mineur, est à la basse, donc premier renversement, chiffrage 6 (si est une tierce et mi une sixte au-dessus de sol). 002210 fait sonner mi2 la2 mi3 la3 do4 mi4 : mi, la quinte de la mineur, est à la basse, donc deuxième renversement, chiffrage 6/4 (la est une quarte et do une sixte au-dessus de mi).

**2. Sur do, pourquoi do mi sol la est-il à l'état fondamental comme C6 et au premier renversement comme Am7/C, et quel chiffrage écrit la basse chiffrée ?**
> Une position se mesure depuis la fondamentale, et les deux lectures ont des fondamentales différentes, do et la. La basse chiffrée ne nomme aucune fondamentale : au-dessus de do, mi est une tierce, sol une quinte et la une sixte, donc elle écrit 6/5 pour les deux.

**3. Dans C – F/C – C, quelle sorte d'accord de quarte et sixte est F/C, et qu'est-ce qui bouge ?**
> Un accord de quarte et sixte de broderie (pédale ou auxiliaire), IV6/4. Sur le do tenu, mi et sol montent d'un degré vers fa et la, puis redescendent.

**4. Quel renversement le document de voicing de GA donne-t-il à Ddim7, xx0101, et pourquoi ?**
> −1. Le reconnaisseur nomme la forme `Fdim7/D`, donc la fondamentale est fa, et ré se trouve à 9 demi-tons au-dessus de fa, une distance que `CalculateInversion` ne convertit pas.

**Critères de réussite :** Nommer la position de n'importe quel voicing d'après sa basse. Écrire les chiffrages des triades et des accords de septième dans toutes les positions, et les distinguer des symboles d'accords. Nommer les quatre sortes d'accord de quarte et sixte et jouer chacune. Dire où le son seul ne fixe pas la position, et où le `Chord`, les documents de voicing et le catalogue de GA se trompent.

---

## Bases de recherche

- Wikipédia, « Inversion (music) » : la définition et la numérotation des renversements, les intervalles du premier renversement, les chiffrages 53 et 6, I6, « position », et Rameau.
- Wikipédia, « Figured bass » : les degrés au-dessus de la basse, 2 pour 6/4/2, G64 et E6 face au C6 du jazz.
- Wikipédia, « Six-four chord » : la quarte comme dissonance, le voicing libre au-dessus de la basse, et les quatre types.
- Wikipédia, « Seventh chord » : les quatre positions de G7 en notation de basse chiffrée.
- Wikipédia, « Diminished seventh chord » : la position connue par la seule orthographe, comme cité dans MUS-013.
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne.
- Learn, leçon 3 de music-theory-ga au commit `aaf6d3e52490d159ab962c75928e88c0dae28c28` : son contrôle des renversements sur GA `a826864`.
- Cité par le plan de cursus de Streeling et non consulté pour cette version : Aldwell et Schachter, *Harmony and Voice Leading*, chapitres 5 et 9.
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre.
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue.
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
