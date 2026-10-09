---
module_id: mus-008-intervals-inversion-compound
department: music
course: Intervalles, renversements et intervalles composés
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Intervalles, renversements et intervalles composés — Compter au-delà de l'octave

> **Département de musique** | Stade : Nigredo (Débutant) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Nommer un intervalle par son nombre, compté sur les noms de notes, et par sa qualité, mesurée en demi-tons : juste, majeure, mineure, augmentée ou diminuée
- Renverser un intervalle simple, et expliquer pourquoi les nombres d'un intervalle et de son renversement font 9 au total, et leurs demi-tons 12
- Nommer un intervalle composé comme une neuvième majeure ou une onzième juste, donner ses demi-tons, et le ramener à sa forme simple
- Nommer l'intervalle entre deux notes jouées sur le manche à plus d'une octave l'une de l'autre, d'après leurs noms et leurs numéros d'octave
- Repérer où GA calcule correctement les intervalles simples, et où ses intervalles composés mêlent deux numérotations

---

## 1. Nombre et qualité

Un intervalle a deux parties. Son **nombre** compte les noms de notes, extrémités comprises : de do à mi, on passe par do, ré et mi, c'est donc une tierce, quelles que soient les altérations des deux notes. Sa **qualité** vient des demi-tons qu'il couvre.

La référence est la gamme majeure construite sur la note inférieure. Au-dessus de do, elle donne :

| Nombre | Nom | Note au-dessus de do | Demi-tons | Qualité dans la gamme majeure |
|---|---|---|---|---|
| 1 | Unisson | do | 0 | Juste |
| 2 | Seconde | ré | 2 | Majeure |
| 3 | Tierce | mi | 4 | Majeure |
| 4 | Quarte | fa | 5 | Juste |
| 5 | Quinte | sol | 7 | Juste |
| 6 | Sixte | la | 9 | Majeure |
| 7 | Septième | si | 11 | Majeure |
| 8 | Octave | do | 12 | Juste |

L'unisson, la quarte, la quinte et l'octave sont des nombres **justes** ; la seconde, la tierce, la sixte et la septième sont des nombres **imparfaits**. Pour un nombre juste, l'intervalle est juste à la taille de référence, augmenté (A) un demi-ton au-dessus et diminué (d) un demi-ton au-dessous. Pour un nombre imparfait, il est majeur (M) à la taille de référence et mineur (m) un demi-ton au-dessous ; il est augmenté un demi-ton au-dessus du majeur, et diminué un demi-ton au-dessous du mineur. Doublement augmenté et doublement diminué vont un demi-ton plus loin. Il n'y a ni quinte majeure ni tierce juste : chaque nombre n'a que sa propre famille de qualités. Comptés avec toutes les qualités, de doublement diminué à doublement augmenté, l'étendue qu'utilise GA, les huit nombres donnent 44 intervalles simples, 5 pour chaque nombre juste et 6 pour chaque nombre imparfait. Quelques-uns ne sont que théoriques, comme l'unisson diminué, dont la note supérieure sonnerait sous la note inférieure. Les abréviations sont celles de l'anglais, qu'imprime GA : P (perfect) pour juste, M pour majeur, m pour mineur, A pour augmenté et d pour diminué.

Deux intervalles de mêmes demi-tons peuvent porter des noms différents. De do à fa♯ et de do à sol♭, il y a 6 demi-tons : le premier couvre quatre noms et c'est une quarte augmentée, A4 ; le second en couvre cinq et c'est une quinte diminuée, d5. MUS-007 a laissé ouverte une paire de ce genre : de ré♭ à fa et de do♯ à fa, il y a quatre demi-tons. De ré♭ à fa, on couvre trois noms, et quatre demi-tons est la taille de référence d'une tierce : c'est une tierce majeure. De do♯ à fa, on couvre quatre noms, et quatre demi-tons, c'est un de moins qu'une quarte juste : c'est une quarte diminuée.

### Exercice pratique

Nommez les intervalles mi–si♭ et la–do♯.

> *Solution :* De mi à si♭, on couvre cinq noms, mi fa sol la si, et 6 demi-tons, un de moins qu'une quinte juste : une quinte diminuée, d5. De la à do♯, on couvre trois noms et 4 demi-tons, la taille de référence d'une tierce : une tierce majeure, M3.

---

## 2. Renversement

Pour **renverser** un intervalle, on monte sa note inférieure d'une octave, ou on descend sa note supérieure d'une octave. De do à mi au-dessus, une tierce majeure, devient de mi à do au-dessus, une sixte mineure.

Deux sommes restent fixes. Les nombres font 9 au total, et non 8, parce que la note qui reste en place est comptée dans les deux intervalles : une tierce et une sixte, 3 + 6 = 9. Les demi-tons font 12, une octave : 4 + 8 = 12. La qualité change à l'intérieur de sa famille : majeur devient mineur et mineur devient majeur, augmenté devient diminué et diminué devient augmenté, les qualités doublement altérées s'échangent de la même façon, et juste reste juste. Les nombres justes se renversent l'un dans l'autre, 1 et 8, 4 et 5, et de même les nombres imparfaits, 2 et 7, 3 et 6. Sur les 44 intervalles simples, les deux sommes valent toujours 9 et 12.

| Intervalle | Demi-tons | Renversement | Demi-tons |
|---|---|---|---|
| M3 | 4 | m6 | 8 |
| m2 | 1 | M7 | 11 |
| P4 | 5 | P5 | 7 |
| A4 | 6 | d5 | 6 |

La quarte augmentée et la quinte diminuée sont le renversement l'une de l'autre, et toutes deux couvrent 6 demi-tons, une demi-octave : le **triton**.

### Exercice pratique

Renversez une septième mineure et une seconde augmentée.

> *Solution :* Une septième mineure, 10 demi-tons, se renverse en seconde majeure, 2 demi-tons : 7 + 2 = 9 et 10 + 2 = 12. Une seconde augmentée, 3 demi-tons, se renverse en septième diminuée, 9 demi-tons.

---

## 3. Intervalles composés

Un intervalle dont le nombre dépasse 8 est **composé** : il couvre plus d'une octave de noms. Ajoutez une octave à un intervalle simple : son nombre augmente de 7, et non de 8, pour la même raison qu'au §2 : la note du haut de l'octave est comptée deux fois, comme dernier nom de l'octave et comme premier de l'intervalle au-dessus. Une seconde au-dessus d'une octave est une neuvième, 8 + 2 − 1, et une tierce au-dessus d'une octave une dixième. Les demi-tons augmentent de 12, et la qualité ne change pas. Pour trouver la **forme simple** d'un intervalle composé, retirez 7 au nombre et 12 aux demi-tons.

| Nombre composé | Forme simple | Demi-tons, majeur ou juste |
|---|---|---|
| 9 | 2 | 14 |
| 10 | 3 | 16 |
| 11 | 4 | 17 |
| 12 | 5 | 19 |
| 13 | 6 | 21 |
| 14 | 7 | 23 |
| 15 | 8 | 24 |

La onzième, la douzième et la quinzième sont justes, comme la quarte, la quinte et l'octave dont elles viennent ; les autres sont majeures ou mineures. La quinzième couvre deux octaves, 15 = 8 + 8 − 1, et s'appelle aussi **double octave**.

Les symboles d'accords nomment les notes empilées au-dessus de la septième par des nombres composés : le 9 de C9 est ré, le deuxième degré de do majeur une octave plus haut, et les 11 et 13 de C11 et C13 sont fa et la. Dans un voicing, la note peut sonner à n'importe quelle octave ; le nombre nomme son degré au-dessus de la fondamentale.

### Exercice pratique

Donnez la forme simple d'une dixième majeure et d'une douzième juste, et les demi-tons d'une neuvième mineure.

> *Solution :* Une dixième majeure, 16 demi-tons, se ramène à une tierce majeure, 4 demi-tons ; une douzième juste, 19, à une quinte juste, 7. Une neuvième mineure couvre 13 demi-tons : une seconde mineure, 1, plus une octave.

---

## 4. Sur le manche

Sur une guitare en accordage standard, les cordes à vide sont mi2, la2, ré3, sol3, si3 et mi4, MIDI 40, 45, 50, 55, 59 et 64, et chaque case ajoute un demi-ton, comme le vérifie la [leçon 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de Learn. Les numéros d'octave sont ceux de la notation scientifique, comme dans MUS-007 : le do central est do4 (la tradition française l'appelle do3). Une forme d'accord couvre souvent plus d'une octave. Dans x32033, un accord de do avec neuvième ajoutée, Cadd9, la cinquième corde à la case 3 donne do3, MIDI 48, et la deuxième corde à la case 3 donne ré4, MIDI 62.

Deux soustractions nomment l'intervalle. Les demi-tons sont la différence des numéros MIDI : 62 − 48 = 14. Le nombre compte les noms d'une octave à l'autre : avec les noms numérotés de do = 0 à si = 6, il vaut 7 × (différence des numéros d'octave) + (différence des noms) + 1. De do3 à ré4, cela donne 7 × 1 + 1 + 1 = 9. Une neuvième est majeure à 14 demi-tons, une seconde majeure plus une octave : de do3 à ré4, c'est donc une neuvième majeure, la neuvième ajoutée qui donne son nom à l'accord.

| Forme | Note inférieure | Note supérieure | Demi-tons | Intervalle |
|---|---|---|---|---|
| Cadd9, x32033 | do3, corde 5, case 3 | ré4, corde 2, case 3 | 14 | M9 |
| Cadd9, x32033 | do3, corde 5, case 3 | sol4, corde 1, case 3 | 19 | P12 |
| E, 022100 | mi2, corde 6, à vide | sol♯3, corde 3, case 1 | 16 | M10 |
| Asus4, x02230 | la2, corde 5, à vide | ré4, corde 2, case 3 | 17 | P11 |

La forme ouverte de mi place sa tierce, sol♯3, une dixième au-dessus de la basse, et la quarte suspendue de Asus4, ré4, sonne une onzième au-dessus de sa basse. Ramener chacun de ces intervalles à sa forme simple donne le nom de la note dans l'accord : la tierce, la quarte, et pour Cadd9 la seconde et la quinte.

### Exercice pratique

Dans la forme ouverte de sol 320003, nommez les intervalles du sol grave, corde 6 case 3, à la corde de si à vide et au sol aigu, corde 1 case 3.

> *Solution :* Le sol grave est sol2, MIDI 43. La corde de si à vide est si3, MIDI 59 : 16 demi-tons, et 7 × 1 + (6 − 4) + 1 = 10, une dixième majeure. Le sol aigu est sol4, MIDI 67 : 24 demi-tons, et 7 × 2 + 0 + 1 = 15, une quinzième juste, une double octave.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26) ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA à `8fe33f8`. La [leçon 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) de music-theory-ga, dans Learn, compile une version antérieure de GA, `a826864`, et vérifie ses intervalles simples. Les autres nombres ci-dessous viennent d'une transcription en Python, ligne à ligne, du code GA nommé.

**`Interval.Simple` est correct.** [`Interval.Simple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L28) calcule ses demi-tons comme la [taille de référence](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L85) de son nombre plus l'[altération de sa qualité](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L127), avec une table pour les nombres justes et une pour les nombres imparfaits, comme au §1. [`ToInverse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L43) prend [9 moins le nombre](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L136) et [change le signe de la qualité](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L115), dont les valeurs vont de −3 pour doublement diminué à 3 pour doublement augmenté : majeur et mineur s'échangent, et de même augmenté et diminué. Par transcription, les 44 intervalles simples reçoivent les demi-tons du §1, et chacun se renverse comme au §2, avec des sommes de 9 et 12. La leçon 1 de Learn vérifie [huit intervalles](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L27) nommés par [`GetInterval`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L104) à partir de deux noms de notes, de do–mi à mi–do, et le renversement de [M3 en m6](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L37). `NoteExtensions.cs` et `IntervalQuality.cs` n'ont pas changé depuis `a826864`, pas plus que la table de demi-tons et `ToInverse` de `SimpleIntervalSize` : ces vérifications valent donc encore à `5c3a52a`. `GetInterval` prend des notes sans octave, et rend donc toujours un intervalle simple : de do3 et ré4, il ne voit que do et ré, une seconde majeure. Il [réduit aussi les demi-tons modulo 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L110) et se rabat sur [juste](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L42) ou [majeur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L55) quand l'écart sort de sa table : de do à si♯, une septième augmentée de 12 demi-tons, il rend M7.

Il reste une lacune dans la lecture des noms. [`Interval.Simple.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L77) accepte n'importe quelle lettre de qualité devant n'importe quel nombre, si bien que « M5 » est lu comme une quinte majeure, que le §1 exclut. Interrogé sur ses demi-tons, cet intervalle lève une `InvalidOperationException` depuis la [table des altérations des intervalles justes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L142).

**Les intervalles composés mêlent deux numérotations.** [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L15) contient les nombres 9 à 16 et les nomme Ninth à Fifteenth, puis [DoubleOctave](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L188) pour 16. Ses parties ne s'accordent pas sur le sens d'un nombre :

- Sa [table de demi-tons](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) donne 9 → 12, 10 → 14, 11 → 16, 12 → 17, 13 → 19, 14 → 21, 15 → 23 et 16 → 24. C'est la table du §3 décalée d'un nombre vers le haut : chaque nombre reçoit les demi-tons du nombre au-dessous, 12, une octave, pour une neuvième, et 24, une double octave, pour 16.
- [`ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L47) retire 8, dans la même numérotation décalée : une neuvième se ramène à 1, un unisson, et non à une seconde.
- [`SimpleIntervalSize.ToCompound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L125) ajoute 7, comme le §3. Un aller-retour par `ToCompound` puis `ToSimple` rend donc le nombre au-dessous du départ, d'une seconde, par 9, à 1, jusqu'à une octave, par 15, à 7. Le `ToCompound` d'un unisson vaudrait 8, hors limites, et lève une `ArgumentOutOfRangeException`.
- Sa [consonance](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L129) déclare justes 11, 12 et 16 : 11 et 12 comme au §3, puis 16 là où le §3 a 15.
- Son résumé dit des nombres qu'ils sont [« Between 9 and 16 semitones »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L4) et donne l'exemple [« 9 = Octave + Second (9 semitones) »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L12). Neuf compte des noms de notes ; une neuvième mineure ou majeure couvre 13 ou 14 demi-tons.

[`Interval.Compound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L31) ajoute l'altération de sa qualité à cette table. Par transcription, sa M9 couvre donc 12 demi-tons, m9 11, M10 14, P11 16, P12 17 et M13 19 : un demi-ton de moins pour la onzième, deux pour les autres. De ses 11 intervalles nommés, de m9 à [P15](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L132), seul P15 est correct, à 24 demi-tons, parce qu'il est construit sur la taille 16, et il s'affiche donc « P16 ». Lire « P15 » donne la taille 15, que la consonance déclare imparfaite, et cet intervalle lève une `InvalidOperationException` quand on lui demande ses demi-tons. Construit par `ToCompound` à partir des 44 intervalles simples du §1, aucun intervalle composé ne reçoit les demi-tons des manuels : 38 ont un ou deux demi-tons de moins, les 5 unissons lèvent une exception dans `ToCompound`, et le composé de P8 en lève une quand on lui demande ses demi-tons. Les bonnes valeurs sont aussi dans GA : son type [`Semitones`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Semitones.cs#L36) définit MajorNinth à 14, PerfectEleventh à 17 et MajorThirteenth à 21.

**Qui lit ces valeurs.** [`ScaleModeCompoundInterval.ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/ScaleModeCompoundInterval.cs#L15) est le seul appelant de `ToSimple`, et aucun code de GA ne l'appelle. `ScaleMode` construit un [intervalle composé](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L207) pour chaque nombre pair d'un mode, 2, 4 et 6, dans sa propriété `SimpleAndCompoundIntervals`, qu'aucun code de GA ne nomme. La [synchronisation des intervalles](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GA.Data.MongoDB/Services/DocumentServices/IntervalSyncService.cs#L34) de GA vers MongoDB enregistre chaque taille composée avec les demi-tons de la table, 12 pour 9. Les tests de GA lisent des noms composés, comme « b9 » en [m9](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/IntervalTests.cs#L181), vérifient que « 13 » n'est [pas lu comme une tierce](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Primitives/IntervalParsingTests.cs#L53), et vérifient que le `ToCompound` d'une quarte vaut [11](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Core.Tests/Collections/ValueObjectMemoizationTests.cs#L175). Aucun test ne demande ses demi-tons à un intervalle composé, et aucun n'appelle `ToSimple`.

Corriger tout cela revient aux responsables de GA ; cette leçon se contente de le décrire.

### Exercice pratique

Par transcription, `Interval.Compound.P11` de GA couvre 16 demi-tons. Quel intervalle du §4 couvre 16 demi-tons, et que devrait couvrir P11 ?

> *Solution :* La dixième majeure de mi2 à sol♯3. Une onzième juste couvre 17 demi-tons : une quarte juste, 5, plus une octave. GA lit la taille 11 dans une table décalée d'un nombre vers le haut, où 16 appartient à la dixième.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien n'y est une mesure. Les prédictions viennent de la transcription du §5 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types de GA dans le processus du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Intervalles simples.** Construisez les 44 intervalles simples du §1 et lisez leurs demi-tons. Prédiction : les 44 concordent avec le §1.
2. **Renversement.** Renversez chacun d'eux avec `ToInverse`. Prédiction : dans les 44 cas, les nombres font 9 et les demi-tons 12.
3. **Aller-retour.** Pour chacune des 8 tailles simples, appelez `ToCompound`, puis `ToSimple`. Prédiction : l'unisson lève une `ArgumentOutOfRangeException`, et les 7 autres reviennent un nombre plus bas, l'octave en septième.
4. **Intervalles composés nommés.** Lisez les demi-tons des 11 intervalles composés nommés, de m9 à P15. Prédiction : 10 diffèrent du §3 ; seul P15, affiché « P16 », a ses 24.
5. **Composés à partir des simples.** Appelez `ToCompound` sur les 44 intervalles simples et comparez les demi-tons de chaque résultat avec ceux de l'intervalle simple plus 12. Prédiction : aucun ne concorde ; 38 ont un ou deux demi-tons de moins, 5 lèvent une exception dans `ToCompound`, et le composé de P8 en lève une quand on lui demande ses demi-tons.
6. **Lecture.** Lisez « P15 », « 15 » et « M5 » avec `Interval.Diatonic.Parse`, qui essaie d'abord un intervalle simple, puis un intervalle composé. Prédiction : les trois sont lus ; « 15 » donne M15, 23 demi-tons, et les deux autres lèvent une `InvalidOperationException` quand on leur demande leurs demi-tons.

### Exercice pratique

L'étape 3 prédit qu'un aller-retour depuis une tierce rend une seconde. Quel changement de `ToSimple` ferait revenir les 7 allers-retours à leur départ, et quelles autres parties de `CompoundIntervalSize` contredirait-il alors ?

> *Solution :* `ToSimple` retirerait 7, l'inverse de `ToCompound`. Le reste du type suivrait encore la numérotation décalée. La table de demi-tons devrait descendre d'un nombre, à 9 → 14 jusqu'à 15 → 24, et les tailles justes devraient devenir 11, 12 et 15. La taille 16, que `ToSimple` enverrait désormais à 9, hors de l'étendue simple, devrait disparaître, et `DoubleOctave` ainsi que le `P15` construit dessus passer à 15.

---

## 7. Pièges courants

- **Compter les demi-tons pour le nombre.** De do à mi, il y a quatre demi-tons, mais trois noms : c'est une tierce.
- **Nommer un intervalle d'après ses seuls demi-tons.** Do–fa♯ et do–sol♭ couvrent tous deux 6 demi-tons ; le premier est A4, le second d5.
- **Quintes majeures et tierces justes.** Les 1, 4, 5 et 8 sont justes, augmentés ou diminués ; les 2, 3, 6 et 7 sont majeurs, mineurs, augmentés ou diminués.
- **Des renversements qui font 8.** Les nombres d'un intervalle et de son renversement font 9.
- **Ajouter 8 pour une octave.** Une seconde plus une octave est une neuvième, et deux octaves font une quinzième.
- **Oublier l'octave d'un intervalle composé.** Dans Cadd9, ré4 est à 14 demi-tons au-dessus de do3, pas à 2.
- **Lire une taille composée dans la table de GA.** À `5c3a52a`, `CompoundIntervalSize` compte 12 demi-tons pour une neuvième, là où `Semitones.MajorNinth` en compte 14.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Nombre d'un intervalle** | Le nombre de noms de notes que couvre un intervalle, extrémités comprises : de do à mi, c'est une tierce |
| **Qualité** | Juste, majeure, mineure, augmentée ou diminuée, fixée par les demi-tons par rapport à la gamme majeure de la note inférieure |
| **Nombre juste** | L'unisson, la quarte, la quinte et l'octave, et leurs composés : justes, augmentés ou diminués |
| **Nombre imparfait** | La seconde, la tierce, la sixte et la septième, et leurs composés : majeurs, mineurs, augmentés ou diminués |
| **Renversement** | L'intervalle obtenu quand la note inférieure monte d'une octave ; les nombres font 9 et les demi-tons 12 |
| **Intervalle composé** | Un intervalle dont le nombre dépasse 8 : 7 de plus en nombre et 12 de plus en demi-tons que sa forme simple |
| **Triton** | Un intervalle de 6 demi-tons : la quarte augmentée ou la quinte diminuée |

---

## Auto-évaluation

**1. Donnez le renversement d'une tierce majeure, avec les deux sommes.**
> Une sixte mineure : 3 + 6 = 9, et 4 + 8 = 12 demi-tons.

**2. Quelle est la forme simple d'une dixième majeure ?**
> Une tierce majeure : 10 − 7 = 3, et 16 − 12 = 4 demi-tons.

**3. Sur une guitare en accordage standard, combien de demi-tons séparent la cinquième corde à vide de la deuxième corde à la case 3, et quel est l'intervalle ?**
> La2 vaut MIDI 45 et ré4 62 : 17 demi-tons, une onzième juste, la quarte de Asus4 au-dessus de sa basse.

**4. Par transcription, [`Interval.Compound.M9`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L123) de GA couvre 12 demi-tons. Que devrait-il couvrir, et d'où vient 12 ?**
> 14 : une seconde majeure, 2, plus une octave. La table de [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) donne à chaque nombre les demi-tons du nombre au-dessous, et 12 est celui de l'octave.

**Critères de réussite :** Nommer tout intervalle simple ou composé d'après ses noms de notes et ses demi-tons ; renverser un intervalle simple, avec des sommes de 9 et 12 ; ramener un intervalle composé à sa forme simple ; nommer l'intervalle entre deux notes jouées sur le manche d'après leurs numéros d'octave ; et distinguer les intervalles simples corrects de GA de sa table composée décalée.

---

## Bases de recherche

- E. Aldwell, C. Schachter et A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019 : les intervalles, leurs qualités, le renversement et les intervalles composés
- W. Piston, *Harmony*, révisé par M. DeVoto, W. W. Norton, 1987 : les gammes et les intervalles
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne
- Learn, leçon 1 de music-theory-ga et sa sortie attendue au commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3` : les vérifications compilées des intervalles simples de GA citées au §5
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
