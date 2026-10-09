---
module_id: mus-007-pitch-spelling-enharmonic-identity
department: music
course: Hauteur, orthographe et identité enharmonique
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-001-what-is-a-chord]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Hauteur, orthographe et identité enharmonique — Un son, plusieurs noms

> **Département de musique** | Stade : Nigredo (Débutant) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Distinguer une hauteur, une classe de hauteurs et un nom de note, et donner l'octave et le numéro MIDI d'une hauteur écrite, comme do♭4 ou si♯3
- Énumérer les 35 noms de notes portant au plus une double altération, les placer sur la ligne des quintes, et expliquer pourquoi sol♯/la♭ est la seule classe de hauteurs qui n'en a que deux
- Écrire les sept notes de n'importe laquelle des 30 tonalités majeures et mineures avec un nom par degré, et expliquer pourquoi les dièses et les bémols de deux tonalités enharmoniques font 12 au total
- Écrire les accords parfaits de ré♭ majeur et de do♯ majeur, qu'un guitariste joue sur les mêmes cases
- Repérer où GA garde l'orthographe d'une note, et où il réduit une note à sa classe de hauteurs puis la renomme d'après une liste

---

## 1. Hauteur, classe de hauteurs et nom de note

Une note se décrit à trois niveaux, et chacun oublie quelque chose que le précédent garde.

Une **hauteur** est un son de hauteur définie. Le MIDI numérote les hauteurs par demi-ton : en notation scientifique, le do central est do4 (la tradition française l'appelle do3), il vaut 60, et do♯4 vaut 61. Une **classe de hauteurs** oublie l'octave : tout do est la classe de hauteurs 0, numérotées de do = 0 à si = 11, comme le fait MUS-002. Un **nom de note** associe l'un des sept noms do, ré, mi, fa, sol, la, si (C à B en notation anglo-saxonne) à une altération : aucune (♮), ♯ ou ♭ pour le déplacer d'un demi-ton vers le haut ou vers le bas, 𝄪 ou 𝄫 pour le déplacer de deux.

Sur un instrument à tempérament égal, deux noms pour la même hauteur, comme do♯ et ré♭, sont **enharmoniques** : c'est la même touche sur un piano et la même case sur une guitare. Le nom n'est pas une propriété du son. Il indique quel nom, et donc quel degré d'une gamme, la note occupe.

Le numéro d'octave appartient au nom, pas au son. La notation scientifique commence chaque octave à do, donc le do♭ écrit dans l'octave 4 est do♭4, et il sonne comme si3, MIDI 59 ; si♯3 sonne comme do4, MIDI 60. En général, MIDI = 12 × (octave + 1) + la classe de hauteurs du nom + la valeur de l'altération, de −2 pour 𝄫 à +2 pour 𝄪 : do♯4 et ré♭4 valent tous deux 61, mi♯4 vaut 65 et fa♭4 vaut 64.

### Exercice pratique

Donnez le numéro MIDI de si♯4 et de do♭5, et la note naturelle que chacun fait entendre.

> *Solution :* si♯4 vaut 12 × 5 + 11 + 1 = 72, le son de do5. Do♭5 vaut 12 × 6 + 0 − 1 = 71, le son de si4. Les deux noms franchissent la limite entre si et do, donc chacun porte le numéro d'octave de son nom, pas celui de son son.

---

## 2. Les 35 noms et la ligne des quintes

Sept noms et cinq altérations, 𝄫, ♭, ♮, ♯ et 𝄪, donnent 35 noms de notes. Ils couvrent inégalement les 12 classes de hauteurs :

| Classe de hauteurs | Noms |
|---|---|
| 0 | ré𝄫, do, si♯ |
| 1 | ré♭, do♯, si𝄪 |
| 2 | mi𝄫, ré, do𝄪 |
| 3 | fa𝄫, mi♭, ré♯ |
| 4 | fa♭, mi, ré𝄪 |
| 5 | sol𝄫, fa, mi♯ |
| 6 | sol♭, fa♯, mi𝄪 |
| 7 | la𝄫, sol, fa𝄪 |
| 8 | la♭, sol♯ |
| 9 | si𝄫, la, sol𝄪 |
| 10 | do𝄫, si♭, la♯ |
| 11 | do♭, si, la𝄪 |

Onze classes de hauteurs ont trois noms. La classe 8 n'en a que deux : seuls sol et la sont à deux demi-tons d'elle ou moins, et les noms suivants, fa et si, sont à trois demi-tons, un de plus que ce qu'une double altération peut atteindre.

La **ligne des quintes** explique ce décompte. Écrivez les noms à une quinte juste d'écart : … si♭ fa do sol ré la mi si fa♯ do♯ sol♯ … Contrairement au cycle des quintes, la ligne ne se referme jamais : après si vient fa♯, pas fa. Numérotez les places à partir de do = 0, de sorte que sol soit 1, fa −1 et fa♯ 6. Toutes les sept places ajoutent un dièse, et la classe de hauteurs d'un nom vaut 7 fois sa place, modulo 12, c'est-à-dire le reste de la division par 12 : sol♯, à la place 8, donne 56, soit 8. Les 35 noms occupent les 35 places consécutives de fa𝄫 à si𝄪. Douze quintes font sept octaves, donc deux noms distants de douze places ont la même classe de hauteurs : do à 0, si♯ à 12, ré𝄫 à −12. Un segment de 35 places, 2 × 12 + 11, contient trois noms pour 11 classes de hauteurs et deux pour la dernière, la♭ et sol♯.

### Exercice pratique

Nommez toutes les orthographes de la classe de hauteurs 6, et donnez la place de chacune sur la ligne des quintes.

> *Solution :* sol♭ à −6, fa♯ à 6 et mi𝄪 à 18. Chacune est à douze places de la suivante, et 7 × −6 = −42, 7 × 6 = 42 et 7 × 18 = 126 valent tous 6 modulo 12 : par exemple, −42 + 48 = 6.

---

## 3. Écrire une tonalité : un nom par degré

Une gamme majeure ou mineure naturelle utilise chacun des sept noms exactement une fois ; le mineur naturel est la gamme mineure sans degré haussé, comme sur les touches blanches de la à la. Une **armure** indique les noms qui portent une altération : les dièses s'ajoutent dans l'ordre fa do sol ré la mi si, les bémols dans l'ordre si mi la ré sol do fa. Avec 0 à 7 dièses ou bémols, il y a 15 tonalités majeures, de do♭ à do♯, et 15 tonalités mineures, de la♭ mineur à la♯ mineur. Une tonalité majeure et une tonalité mineure de même armure sont **relatives** : si♭ majeur et sol mineur ont toutes deux deux bémols.

Écrire une tonalité devient alors mécanique : partez de la tonique, prenez les six noms suivants, et ajoutez l'altération de l'armure là où elle s'applique. Fa♯ majeur a six dièses, fa do sol ré la mi, et s'écrit fa♯ sol♯ la♯ si do♯ ré♯ mi♯. Son septième degré sonne comme fa, mais le nom fa est déjà celui de la tonique et le nom mi manquerait, donc le degré est mi♯. Do♭ majeur, avec sept bémols, s'écrit do♭ ré♭ mi♭ fa♭ sol♭ la♭ si♭.

Sur les 30 tonalités, les 210 notes écrites utilisent 21 noms : les 7 naturels, les 7 dièses et les 7 bémols. Aucune armure n'exige de double altération. Dans l'écriture des tonalités, mi♯, si♯, do♭ et fa♭ n'apparaissent que dans les 8 tonalités à six ou sept altérations : fa♯ et do♯ majeur, ré♯ et la♯ mineur, sol♭ et do♭ majeur, et mi♭ et la♭ mineur.

Trois paires de tonalités majeures ont les mêmes classes de hauteurs : si et do♭, fa♯ et sol♭, do♯ et ré♭. De même pour trois paires de tonalités mineures : sol♯ et la♭, ré♯ et mi♭, la♯ et si♭. Dans chaque paire, les dièses et les bémols font 12 au total : si majeur a 5 dièses et do♭ majeur 7 bémols. Les deux toniques sont à douze places l'une de l'autre sur la ligne des quintes (§2), et chaque place vers la droite ajoute un dièse à l'armure ou retire un bémol.

La sensible d'une tonalité mineure peut sortir de l'armure. Le mineur harmonique hausse le septième degré d'un demi-ton sans changer son nom, donc la sensible de fa♯ mineur est mi♯ et celle de do♯ mineur si♯, et celle de sol♯ mineur est fa𝄪, celle de ré♯ mineur do𝄪 et celle de la♯ mineur sol𝄪.

### Exercice pratique

Dans quelles tonalités majeures mi♯ est-il un degré de la gamme ?

> *Solution :* fa♯ majeur (fa♯ sol♯ la♯ si do♯ ré♯ mi♯) et do♯ majeur (do♯ ré♯ mi♯ fa♯ sol♯ la♯ si♯). Mi♯ est le sixième dièse de l'ordre fa do sol ré la mi si, donc seules les armures à six ou sept dièses le contiennent.

---

## 4. Mêmes cases, deux orthographes

Un guitariste qui lit une grille en ré♭ majeur puis une autre en do♯ majeur joue les mêmes cases : les deux tonalités ont les sept mêmes classes de hauteurs. Chaque note change de nom :

| Degré | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| ré♭ majeur | ré♭ | mi♭ | fa | sol♭ | la♭ | si♭ | do |
| do♯ majeur | do♯ | ré♯ | mi♯ | fa♯ | sol♯ | la♯ | si♯ |

Chaque nom de la deuxième ligne est le nom situé juste en dessous de celui de la première. Ré♭ majeur demande 5 bémols et do♯ majeur 7 dièses.

Les accords suivent la même règle. Un accord parfait empile deux tierces, et une tierce couvre trois noms, donc un accord parfait prend un nom sur deux : la fondamentale, le nom deux crans au-dessus et le nom quatre crans au-dessus. L'accord de tonique de ré♭ majeur est ré♭ fa la♭ ; celui de do♯ majeur est do♯ mi♯ sol♯, pas do♯ fa sol♯, qui ferait passer la tierce pour une quarte. Compter les demi-tons, comme dans MUS-001, trouve les cases ; c'est la suite des noms qui fixe l'orthographe. Les sept accords construits sur les degrés d'une tonalité sont ses accords **diatoniques**, numérotés en chiffres romains : en majuscules pour un accord majeur, en minuscules pour un accord mineur, et avec ° pour un accord diminué, que GA écrit dim :

| Degré | I | ii | iii | IV | V | vi | vii° |
|---|---|---|---|---|---|---|---|
| ré♭ majeur | ré♭ fa la♭ | mi♭ sol♭ si♭ | fa la♭ do | sol♭ si♭ ré♭ | la♭ do mi♭ | si♭ ré♭ fa | do mi♭ sol♭ |
| do♯ majeur | do♯ mi♯ sol♯ | ré♯ fa♯ la♯ | mi♯ sol♯ si♯ | fa♯ la♯ do♯ | sol♯ si♯ ré♯ | la♯ do♯ mi♯ | si♯ ré♯ fa♯ |

Le numéro d'un intervalle vient de ses noms, comme le montre la [leçon 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de Learn : de ré♭ à fa, on parcourt trois noms, une tierce ; de do♯ à fa, quatre, une quarte, bien que les deux couvrent quatre demi-tons. Les qualités d'intervalles sont laissées à un module ultérieur, MUS-008.

### Exercice pratique

Une grille en ré♭ majeur se lit D♭ – B♭m – G♭ – A♭ – Fm – E♭m – A♭ – D♭. Réécrivez-la en do♯ majeur, sur les mêmes cases.

> *Solution :* La grille est I – vi – IV – V – iii – ii – V – I. En do♯ majeur, elle se lit C♯ – A♯m – F♯ – G♯ – E♯m – D♯m – G♯ – C♯. Chaque fondamentale passe au nom situé juste en dessous, donc Fm devient E♯m : fa n'est pas un degré de do♯ majeur, dont le troisième degré est mi♯.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26) ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA à `8fe33f8`. Les leçons [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) et [5](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/05-keys-and-the-circle-of-fifths.mdx) de music-theory-ga, dans Learn, compilent une version antérieure de GA, `a826864`, et vérifient ses noms de notes et l'orthographe de ses tonalités. Les autres nombres ci-dessous viennent d'une transcription en Python, ligne à ligne, du code GA nommé.

**Les notes gardent leur orthographe.** L'union [`Note`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L17) de GA comprend des notes de tonalité, qui contiennent un nom et une altération, et un cas [`Note.Chromatic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L82) qui ne garde que la classe de hauteurs. En tant que notes de tonalité, do♯ et ré♭ sont des valeurs différentes : des notes enharmoniques [« share a pitch class but are not equal »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L27). [`Note.Accidented.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L330) lit les 35 noms du §2, écrits avec ♯, ♭, 𝄪 et 𝄫 ou avec #, b, ## et bb, mais son analyseur d'altérations [ne prévoit pas ♯♯](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Accidental.cs#L147) ni ♭♭, que `Note.Sharp` et `Note.Flat` acceptent par leurs propres [motifs d'altération](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/SharpAccidental.cs#L64). La leçon 1 de Learn vérifie [huit orthographes](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L16), de do♯ à fa𝄪, par rapport à leurs classes de hauteurs. Les enregistrements `Pitch` suivent le §1 : comptés depuis le do qui commence l'octave, [« Cb4 is -1 (B3) and B#3 is 12 (C4) »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Pitch.cs#L46).

**Les tonalités s'écrivent avec un nom par degré.** [`Key.GetNotes`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Key.cs#L82) prend la tonique, puis les six noms suivants, chacun diésé ou bémolisé quand l'[armure](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/KeySignature.cs#L76) le nomme, les dièses étant ajoutés depuis fa par quintes et les bémols depuis si par quartes. C'est la règle du §3. Les tests de GA vérifient l'orthographe des 15 tonalités majeures, jusqu'à [do♯ majeur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MajorKeyTests.cs#L22), et des 15 tonalités mineures, jusqu'à [la♯ mineur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MinorKeyTests.cs#L22). La leçon 5 de Learn a trouvé l'orthographe des manuels pour les [15 armures](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L3) et pour [huit tonalités](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L21), et ni `GetNotes` ni `KeySignature` n'a changé depuis `a826864`.

**Les notes des accords à partir des noms.** [`ChordSpelling.Spell`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordSpelling.cs#L52) avance d'abord le nom de la fondamentale du nombre de crans que fixe l'accord, puis ajoute l'altération qui atteint la classe de hauteurs visée, comme au §4. Ses tests vérifient par exemple que la [tierce mineure de si♭ est ré♭](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/ChordSpellingTests.cs#L30), pas do♯. L'outil MCP d'accords [l'appelle](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordMcpTools.cs#L62), tout comme la [compétence d'accords](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ChordInfoSkill.cs#L291) du chatbot. Par transcription, à partir de la fondamentale écrite de chaque accord, il écrit les 210 accords parfaits diatoniques des 30 tonalités avec les noms des manuels, E♯m en do♯ majeur compris.

**Où une classe de hauteurs est renommée d'après une liste.** D'autres parties de GA réduisent une note à sa classe de hauteurs et la renomment d'après une liste de 12 noms, une liste avec des dièses et une avec des bémols. Aucune des deux ne contient mi♯, si♯, do♭, fa♭ ni une double altération.

- [`EnharmonicNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L11) garde une [liste en dièses](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L120) et une [liste en bémols](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L141). Sa méthode `GetEnharmonicEquivalents`, documentée comme [« Gets all enharmonic equivalents for a chord »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L48), renvoie au plus deux noms par classe de hauteurs, 17 des 35. Sa méthode [`DetermineContextFromKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L225) prend la tonique de la tonalité comme une classe de hauteurs et ne lit jamais son paramètre `isMajor`. Une tonique 0 ou 9 compte comme naturelle, donc la majeur et do mineur aussi ; 1, 6 et 11 sont testés comme tonalités à dièses avant de l'être comme tonalités à bémols, donc ré♭, sol♭ et do♭ majeur passent pour des tonalités à dièses, tout comme sol et ré mineur, toniques 7 et 2 ; et 8, 3 et 10 comptent comme tonalités à bémols, donc sol♯, ré♯ et la♯ mineur aussi. Comparée à l'armure, elle se trompe pour ces 10 des 30 tonalités. Aucun code ne l'appelle, et aucun test de GA ne nomme le service.
- [`KeyAwareChordNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L295) tire le côté de l'armure, ce qui est juste, puis [nomme une fondamentale](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L302) d'après ces listes par `EnharmonicNamingService.AnalyzeEnharmonicChoices`. Par transcription, la classe de hauteurs 5 en do♯ majeur devient « F », et la classe 11 en sol♭ majeur « B ». Sur les 210 degrés des 30 tonalités, 12 sortent mal écrits, tous dans les 8 tonalités du §3 qui utilisent mi♯, si♯, do♭ ou fa♭.

**Les closures F#.** La couche F# de GA choisit entre ses deux listes d'après l'altération de la fondamentale elle-même : la [liste en bémols](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L31) quand la fondamentale porte un bémol ou est fa, la liste en dièses sinon. [`domain.diatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L274) applique ce choix à la tonique de la tonalité. Par transcription :

| Tonalité | Accords renvoyés | Mal écrits |
|---|---|---|
| do♯ majeur | C#, D#m, Fm, F#, G#, A#m, Cdim | Fm pour E♯m, Cdim pour B♯° |
| sol♭ majeur | Gb, Abm, Bbm, B, Db, Ebm, Fdim | B pour C♭ |
| ré mineur | Dm, Edim, F, Gm, Am, A#, C | A# pour B♭ |
| do mineur | Cm, Ddim, D#, Fm, Gm, G#, A# | D#, G#, A# pour E♭, A♭, B♭ |

Sur les 30 tonalités, 18 des 210 accords sont mal écrits, dans 11 tonalités : les 8 du §3, et ré, sol et do mineur, dont la tonique ne porte pas de bémol. [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) fait le même choix et, par transcription, répond « A# major » pour sol mineur, « D# major » pour do mineur et « B major » pour la♭ mineur. [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L248) garde le côté de l'ancienne fondamentale : sol monté de trois demi-tons devient « A# ». Un nombre de demi-tons ne fixe pas le nom, mais la♯ majeur demanderait dix dièses, en comptant chaque 𝄪 pour deux, alors que si♭ majeur a deux bémols.

Ces closures répondent aux outils MCP [`GaDiatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L179) et [`GaRelativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L188) de GA, et à la compétence [`DiatonicChordsSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L22) du chatbot. La description de la compétence dit qu'elle utilise la closure pour que l'orthographe enharmonique soit juste : [« spelling is correct in less-common keys (Gb major, F# minor) »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L32). Fa♯ mineur est juste. Sol♭ majeur fait partie des 11 tonalités, et les [instructions](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/diatonic-chords/SKILL.md#L26) de la compétence donnent « Gb major returns Cm, not B#m », alors que sol♭ majeur ne contient ni do ni si♯ : son quatrième degré est do♭, que la closure nomme « B ». L'orthographe correcte existe déjà dans GA, dans `Key.Notes` et `ChordSpelling.Spell` ; les closures n'appellent ni l'un ni l'autre.

**Un nom se lit selon une convention.** En notation des ensembles, T et E valent 10 et 11. [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L258) lit T et E de cette façon avant d'essayer les noms de notes, donc « E » est la classe de hauteurs 11, pas la note mi, 4. Ses [remarques](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L232) citent les deux lectures, et [un test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/PitchClassTests.cs#L130) fixe « E » à 11. La méthode `TryGetRootPitchClass` de GA lit plutôt une fondamentale reconnue avec `Note.Accidented.TryParse`, et sa [remarque](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L17) dit encore que cette méthode lit « A » comme 10, ce que seule `TryParseSetNotation` fait désormais ; `TryParse` lit « A » comme la note la, 9.

Corriger quoi que ce soit de tout cela revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

Par transcription, `domain.diatonicChords` renvoie pour do♭ majeur B, Dbm, Ebm, E, Gb, Abm, Bbdim. Corrigez l'orthographe, et dites pourquoi même la tonique change.

> *Solution :* C♭, D♭m, E♭m, F♭, G♭, A♭m, B♭°. La closure lit « Cb » comme la classe de hauteurs 11, puis nomme 11 d'après sa liste en bémols, où 11 est « B » : le nom do est perdu avant qu'aucun nom ne soit choisi. Fa♭, classe de hauteurs 4, devient « E » de la même façon.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien n'y est une mesure. Les prédictions viennent de la transcription du §5 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types ou les closures de GA dans le processus du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Les 35 noms.** Analysez les 35 noms du §2 avec `Note.Accidented.TryParse` et tabulez leurs classes de hauteurs. Prédiction : les 35 sont lus ; 11 classes de hauteurs reçoivent trois noms et la classe 8 deux.
2. **Les 30 tonalités.** Écrivez les 30 tonalités avec `Key.Notes`. Prédiction : 7 noms distincts dans chaque tonalité, 21 noms distincts sur les 210 notes, et l'orthographe des manuels partout.
3. **Les octaves.** Calculez avec `Pitch` les numéros MIDI de do♭4, si♯3, mi♯4 et fa♭4. Prédiction : 59, 60, 65 et 64.
4. **La closure diatonique.** Appelez `domain.diatonicChords` pour les 30 tonalités et comparez la fondamentale de chaque accord à `Key.Notes`. Prédiction : 18 des 210 accords diffèrent, dans 11 tonalités.
5. **La closure des tons relatifs.** Appelez `domain.relativeKey` pour les 30 tonalités. Prédiction : 3 réponses diffèrent, pour sol mineur, do mineur et la♭ mineur.
6. **Le service de nommage.** Pour chacune des 210 notes, appelez `EnharmonicNamingService.AnalyzeEnharmonicChoices` avec le contexte de l'armure de la tonalité ; puis appelez `DetermineContextFromKey` avec la tonique de chaque tonalité. Prédiction : 12 noms diffèrent, dans 8 tonalités, et 10 des 30 contextes contredisent l'armure.
7. **Les notes des accords.** Appelez par réflexion `ChordSpelling.Spell`, qui est interne à GA.Business.ML, sur les 210 accords parfaits diatoniques. Prédiction : les 210 concordent avec `Key.Notes`.

### Exercice pratique

L'étape 4 prédit 18 différences. Que devrait faire la closure pour que la prédiction tombe à 0, et quel genre d'entrée ne pourrait toujours pas être écrit ?

> *Solution :* Elle devrait écrire à partir des noms, comme `Key.Notes` et `ChordSpelling.Spell`, au lieu de nommer des classes de hauteurs d'après une liste. Avec une tonique écrite, rien n'est ambigu : « Db » et « C# » désignent des tonalités différentes. Une tonique donnée seulement comme classe de hauteurs, comme 1, ne peut pas dire si la tonalité est ré♭ ou do♯ majeur.

---

## 7. Pièges courants

- **Dire que do♯ et ré♭ sont la même note.** Ils partagent une classe de hauteurs, une touche de piano et une case, pas un nom ni un degré de gamme.
- **Écrire fa en fa♯ majeur.** Chaque nom apparaît une fois dans une tonalité, donc le septième degré est mi♯.
- **Écrire un accord à partir des demi-tons.** Un accord parfait prend un nom sur deux : E♯m, et non Fm, est l'accord iii de do♯ majeur.
- **Lire l'octave d'après le son.** Si♯3 sonne comme do4, mais son numéro d'octave suit le nom si.
- **Oublier la sensible d'une tonalité mineure à dièses.** Le septième degré haussé de sol♯ mineur est fa𝄪.
- **Nommer les notes d'après une liste de 12.** Une liste en dièses et une liste en bémols contiennent 17 des 35 noms, et aucun des quatre dont 8 tonalités ont besoin.
- **Prendre la tonique d'une tonalité pour une classe de hauteurs.** La classe de hauteurs 1 est la tonique de ré♭ majeur, avec 5 bémols, et de do♯ majeur, avec 7 dièses.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Hauteur** | Un son de hauteur définie, comme do4, MIDI 60 |
| **Classe de hauteurs** | Une hauteur sans son octave, numérotée de do = 0 à si = 11 |
| **Nom de note** | Un nom de do à si avec une altération : 𝄫, ♭, ♮, ♯ ou 𝄪 |
| **Enharmonique** | Se dit de deux noms, ou de deux tonalités, qui ont les mêmes classes de hauteurs, comme do♯ et ré♭ |
| **Ligne des quintes** | Les noms de notes à une quinte juste d'écart, sur une ligne qui ne se referme jamais : … fa do sol ré la mi si fa♯ do♯ … |
| **Armure** | Les noms qui portent un dièse (ajoutés depuis fa, par quintes) ou un bémol (ajoutés depuis si, par quartes) dans une tonalité |
| **Sensible** | Le septième degré, un demi-ton sous la tonique ; dans une tonalité mineure, le septième degré haussé du mineur harmonique |

---

## Auto-évaluation

**1. Combien de noms portant au plus une double altération la classe de hauteurs 6 a-t-elle ? Nommez-les.**
> Trois : sol♭, fa♯ et mi𝄪. Ils se trouvent à douze places d'écart sur la ligne des quintes.

**2. Quel est le numéro MIDI de do♭4, et quelle note naturelle fait-il entendre ?**
> 59, le son de si3. Le numéro d'octave suit le nom do, donc do♭4 se trouve un demi-ton sous do4.

**3. Écrivez la gamme mineure naturelle de la♭ mineur.**
> La♭ si♭ do♭ ré♭ mi♭ fa♭ sol♭ : sept bémols, un nom par degré.

**4. La closure [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) de GA répond « A# major » pour sol mineur. Quel est le relatif majeur, et pourquoi la closure l'écrit-elle mal ?**
> Si♭ majeur. La closure nomme la tonique relative, la classe de hauteurs 10, d'après sa liste en dièses, parce que la tonique sol ne porte pas de bémol et n'est pas fa.

**Critères de réussite :** Distinguer une hauteur, une classe de hauteurs et un nom de note ; donner l'octave et le numéro MIDI d'une hauteur écrite ; énumérer les noms d'une classe de hauteurs à partir de la ligne des quintes ; écrire n'importe laquelle des 30 tonalités, et les accords parfaits de deux tonalités enharmoniques, avec un nom par degré ; et distinguer l'orthographe de GA fondée sur les noms de ses listes de classes de hauteurs.

---

## Bases de recherche

- D. Temperley, « The Line of Fifths », *Music Analysis* 19(3), 2000, 289–319 : les hauteurs écrites placées sur une ligne des quintes plutôt que sur un cycle
- E. Gould, *Behind Bars*, Faber Music, 2011 : les altérations et la notation des hauteurs
- E. Aldwell, C. Schachter et A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019 : les gammes, les armures et l'orthographe des accords parfaits
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne
- Learn, leçons 1 et 5 de music-theory-ga et leur sortie attendue au commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3` : les vérifications compilées des noms de notes et de l'orthographe des tonalités de GA citées au §5
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
