---
module_id: mus-005-jazz-harmony
department: music
course: Harmonie jazz pour la guitare
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites:
  - mus-001-what-is-a-chord
  - mus-003-functional-harmony
  - gtr-002-caged-geometry
estimated_duration: "3 hours"
produced_by: music
version: "1.0.0"
---

# Harmonie jazz pour la guitare : du ii-V-I aux Coltrane Changes

> **Département de musique** | Stade : Citrinitas (Intermédiaire à avancé) | Durée : 3 heures

## Objectifs d'apprentissage

À l'issue de ce cours, vous serez capable de :

- Lire et interpréter n'importe quel symbole d'accord jazz, y compris les extensions, les altérations et la notation avec barre oblique
- Identifier les progressions ii-V-I en majeur et en mineur dans le répertoire standard du jazz
- Conduire les voix à travers les changements d'accords avec des voicings en shell, drop-2 et drop-3
- Appliquer la conduite des voix par notes guides pour enchaîner les accords en douceur
- Employer la substitution tritonique, la substitution diminuée et la dominante « backdoor »
- Associer les gammes appropriées aux qualités d'accords grâce à la théorie accord-gamme
- Construire des voicings en quartes et des triades de structure supérieure pour une sonorité jazz moderne
- Analyser et appliquer le cycle de substitution symétrique en tierces majeures de Coltrane

---

## 1. Savoir lire les symboles d'accords jazz

Les symboles d'accords jazz sont un langage de notation compressé. Contrairement à la basse chiffrée classique, ils encodent la qualité, les extensions, les altérations et la note de basse en un seul symbole compact. Les lire couramment est une condition préalable à tout ce qui suit.

### Anatomie d'un symbole d'accord

Tout symbole d'accord jazz comporte jusqu'à quatre composantes :

```
Root  +  Quality  +  Extensions/Alterations  +  Slash Bass
 C        maj           9#11                      /E
```

**Fondamentale :** n'importe quelle lettre de A à G, éventuellement suivie de # ou b.

La **qualité** encode la triade et la septième :

| Symbole | Signification | Tierce | Septième |
|--------|---------|-------|---------|
| (rien) ou `maj` | Accord parfait majeur | Tierce majeure | — |
| `m` ou `min` ou `-` | Accord parfait mineur | Tierce mineure | — |
| `7` | Septième de dominante | Tierce majeure | Septième mineure |
| `maj7` ou `M7` ou triangle | Septième majeure | Tierce majeure | Septième majeure |
| `m7` ou `min7` ou `-7` | Septième mineure | Tierce mineure | Septième mineure |
| `m7b5` ou demi-diminué | Demi-diminué | Tierce mineure | Septième mineure (b5) |
| `dim7` ou `o7` | Septième diminuée | Tierce mineure | Septième diminuée |

Les **extensions** ajoutent des notes supérieures (9, 11, 13). Le nombre le plus élevé implique toutes les notes impaires inférieures :

- `Cmaj9` = C E G B D (implique la présence de la 7e)
- `Cmaj13` = C E G B D (F#) A (implique la 9 et la 7 ; la 11 est généralement #11 dans un contexte majeur)

Les **altérations** modifient des notes précises :

- `#11` — 11e augmentée (évite le frottement avec la tierce majeure)
- `b9`, `#9` — 9e abaissée ou augmentée
- `b13` — 13e abaissée (enharmonique de #5)
- `alt` — abréviation d'une dominante avec b9, #9, #11/b5, b13/#5

### L'ambiguïté C7 / Cmaj7

Cela piège tous les débutants :

- **C7** = C E G **Bb** (septième de dominante — le « 7 » par défaut est un intervalle de septième mineure)
- **Cmaj7** = C E G **B** (septième majeure — le qualificatif « maj » élève la septième)

Le « 7 » seul signifie toujours dominante. Il faut écrire « maj7 » pour obtenir une septième majeure. Cette convention est un vestige historique du blues et du jazz des débuts, où les septièmes de dominante étaient le son par défaut.

### Accords avec barre oblique

`C/E` signifie « accord de Do majeur avec E à la basse ». La note après la barre oblique est la note de basse, pas nécessairement une note de l'accord. Usages courants :

- Renversements : `C/E` (premier renversement), `C/G` (deuxième renversement)
- Polyaccords implicites : `Db/C` = triade de Db sur une basse de C (crée une sonorité de Cmaj7#11)
- Pédales : `Dm7/G` = crée une sonorité de G11 sans énoncer G comme fondamentale

### Exercice pratique

Lisez les symboles d'accords suivants et épelez leurs notes. N'utilisez pas votre instrument — travaillez uniquement à partir du symbole :

1. `Fmaj9#11`
2. `Bb7alt`
3. `Ebm11`
4. `Ab13`
5. `Dm7b5`
6. `G7#9/Db` (quelle substitution cela implique-t-il ?)

Réponses :
1. F A C E G B (Fa majeur avec 7e majeure, 9e, #11e)
2. Bb D Ab B/Cb Eb/D# Gb (dominante avec toutes les extensions supérieures altérées)
3. Eb Gb Bb Db F Ab (septième mineure avec 11e)
4. Ab C Eb Gb Bb Db F (septième de dominante avec 9e, 11e implicite, 13e)
5. D F Ab C (triade mineure avec quinte diminuée et septième mineure)
6. G B D F A#/Bb sur une basse de Db — la basse de Db implique la substitution tritonique de G7

---

## 2. L'univers du ii-V-I

La progression ii-V-I est le centre de gravité de l'harmonie jazz. La comprendre, c'est comme comprendre les phrases d'une langue — une fois qu'on les entend, on les entend partout.

### ii-V-I majeur

En Do majeur :

```
  Dm7    →    G7    →    Cmaj7
  ii7         V7         Imaj7
```

Pourquoi cela fonctionne-t-il ? Chaque accord se résout sur le suivant par le mouvement de fondamentale le plus fort de la musique tonale — les quintes descendantes (D→G→C). La conduite des voix est tout aussi puissante : la tierce de Dm7 (F) descend vers la tierce de G7 (B n'est pas F, mais la 7e de Dm7, C, devient la relation de 7e). Plus précisément :

- La **7e du ii** (C) descend d'un degré vers la **tierce du V** (B)
- La **tierce du V** (B) monte d'un degré vers la **fondamentale du I** (C)
- La **7e du V** (F) descend d'un degré vers la **tierce du I** (E)

Cette attraction chromatique conjointe crée un sentiment de résolution irrésistible.

### ii-V-i mineur

En Do mineur :

```
  Dm7b5  →    G7alt   →    Cm(maj7) or Cm7
  ii-half      V7alt        i
```

Le ii demi-diminué apporte la couleur du mode mineur. La dominante altérée (G7alt) contient à la fois la b9 (Ab) et la b13 (Eb), qui sont la b6 et la b3 de Do mineur — précisément les notes qui définissent la tonalité mineure.

### Chaînes de ii-V étendues

Les morceaux de jazz enchaînent souvent des ii-V à travers plusieurs tonalités sans résoudre :

```
  Em7  A7  |  Dm7  G7  |  Cmaj7
  ii   V      ii   V      I
  (of D)      (of C)      (arrived)
```

Le turnaround — les dernières mesures d'une forme qui ramènent au début — est la chaîne étendue la plus courante :

```
  Cmaj7  Am7  |  Dm7  G7  ||  (back to Cmaj7)
  I      vi      ii   V        I
```

### Exercice pratique

Voici la grille d'accords de **« All The Things You Are »** (Kern/Hammerstein). Entourez chaque ii-V-I (majeur ou mineur). Indiquez si chacun se résout ou reste en suspens :

```
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dm7    | G7     | Cmaj7  |
Cm7   | Fm7    | Bb7    | Ebmaj7 |
Abmaj7| Am7    | D7     | Gmaj7  |
Am7   | D7     | Gmaj7  |        |
F#m7  | B7     | Emaj7  | C7alt  |
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dbm7   | Cm7    | Bdim7  |
Bbm7  | Eb7    | Abmaj7 |        |
```

Vous devriez trouver au moins six progressions ii-V-I dans trois tonalités différentes, ainsi que plusieurs ii-V qui se résolvent de façon rompue ou s'enchaînent vers la zone tonale suivante.

---

## 3. Voicings de guitare jazz

Les pianistes peuvent disposer les accords avec dix doigts sur cinq octaves. Les guitaristes ont six cordes et quatre doigts sur le manche. Cette contrainte est en réalité un cadeau — elle impose des voicings économes qui percent à travers l'ensemble et se prêtent magnifiquement à la conduite des voix.

### Voicings en shell (fondamentale + tierce + septième)

La fondamentale, la tierce et la septième sont les **notes essentielles** qui définissent la qualité et la fonction d'un accord. La quinte est presque toujours omise (elle n'apporte aucune information harmonique, sauf si elle est altérée).

**Fondamentale sur la 6e corde :**

```
Dm7:        G7:         Cmaj7:
e ----      e ----      e ----
B ----      B ----      B ----
G ----      G ----      G ----
D ----      D ----      D ----
A --5--     A ----      A --3--
E --x--     E --3--     E --x--
   1 b3 b7     1 3 b7      1 3 7
```

(Les positions réelles des cases dépendent de l'emplacement de la fondamentale ; le principe est fondamentale-tierce-septième sur des cordes adjacentes.)

**Fondamentale sur la 5e corde :**

Les shells avec la fondamentale sur la 5e corde gardent le voicing dans un registre médium confortable. La tierce et la septième tombent sur les cordes 4 et 3, ce qui laisse les cordes aiguës libres pour la mélodie ou les extensions.

### Voicings drop-2

Prenez un accord de quatre notes en position serrée et « faites tomber » la deuxième note la plus haute d'une octave. Cela répartit le voicing sur quatre cordes adjacentes — parfait pour la guitare.

**Cmaj7 en position serrée :** G-B-C-E (du grave à l'aigu, deuxième renversement). Abaissez d'une octave la deuxième note depuis le haut (C) pour obtenir C-G-B-E, avec la fondamentale à la basse.

**Cmaj7 en drop-2 (jeu de cordes 5-4-3-2) :**

```
e ----
B --5-- (E, the 3rd)
G --4-- (B, the 7th)
D --5-- (G, the 5th)
A --3-- (C, the root — dropped from close position)
E ----
```

Les voicings drop-2 existent sur quatre jeux de cordes :

| Jeu de cordes | Registre | Idéal pour |
|-----------|-------|----------|
| 6-5-4-3 | Grave | Accompagnement en duo ou avec une walking bass |
| 5-4-3-2 | Médium | Registre d'accompagnement standard |
| 4-3-2-1 | Aigu | Accompagnement mélodique, chord melody |

Chaque qualité d'accord (maj7, m7, 7, m7b5) a quatre renversements par jeu de cordes, ce qui vous donne 48 voicings drop-2 à intérioriser (4 qualités x 4 renversements x 3 jeux de cordes).

### Voicings drop-3

Faites tomber d'une octave la troisième note la plus haute d'un voicing serré. Cela crée un écartement plus large, avec un espace entre la note de basse et l'agrégat supérieur. Les voicings drop-3 couvrent cinq cordes (en sautant une corde au milieu).

**Jeux de cordes pour le drop-3 :** 6-4-3-2 et 5-3-2-1.

Les voicings drop-3 sont plus sombres et plus orchestraux. Joe Pass les utilisait abondamment en chord melody.

### Voicings à la Freddie Green

L'approche de la guitare rythmique de Count Basie : quatre noires par mesure, un voicing par temps, presque toujours sur les cordes 6-4-3 (ou 5-4-3). Seulement trois notes — fondamentale (ou note de basse du shell), tierce, septième. Grattées avec une attaque rapide et percussive qui s'éteint aussitôt. La guitare devient un tambour à hauteur déterminée.

### Technique d'octaves de Wes Montgomery / George Benson

Ce n'est pas une technique de voicing au sens harmonique, mais un vocabulaire essentiel de la guitare jazz. Des lignes à une note doublées à l'octave (cordes 6+4, 5+3 ou 4+2), la corde intermédiaire étant étouffée par le doigt de la main gauche. Cela crée un son épais, proche de celui d'un cuivre.

### Exercice pratique

Conduisez les voix du ii-V-I suivant en Do majeur avec des voicings drop-2 sur le jeu de cordes 5-4-3-2. Votre objectif : un mouvement minimal des doigts entre les accords. Notez les positions des cases pour chaque accord :

```
Dm7  →  G7  →  Cmaj7
```

Règle : la septième d'un accord doit se résoudre par degré conjoint vers la tierce (ou une note proche) de l'accord suivant. Trouvez deux renversements différents qui réalisent cet enchaînement fluide.

---

## 4. Notes guides et conduite des voix

### Le principe des notes guides

La **tierce** et la **septième** de chaque accord sont appelées **notes guides** parce qu'elles :

1. **Définissent la qualité :** la tierce indique majeur ou mineur. La septième indique dominante, majeur ou mineur.
2. **Créent le mouvement :** lorsque les accords changent, les notes guides bougent d'un demi-ton ou d'un ton — les intervalles les plus petits et les plus doux possibles.

Le miracle central de la conduite des voix dans le ii-V-I :

```
Chord:    Dm7    G7     Cmaj7
3rd:       F  →   B  →   E
7th:       C  →   F  →   B
```

Remarquez :
- La **7e de Dm7 (C)** descend d'un demi-ton pour devenir la **tierce de G7 (B)**
- La **tierce de Dm7 (F)** reste en place pour devenir la **7e de G7 (F)**
- La **7e de G7 (F)** descend d'un demi-ton pour devenir la **tierce de Cmaj7 (E)**
- La **tierce de G7 (B)** reste en place pour devenir la **7e de Cmaj7 (B)**

Les notes guides **échangent leurs rôles** : la tierce d'un accord devient la septième du suivant, et inversement. Cela crée un contrepoint à deux voix qui descend chromatiquement : C-B, F-E.

### L'accompagnement à deux notes de Barry Harris

Barry Harris enseignait qu'on peut accompagner tout un morceau avec **seulement la tierce et la septième** de chaque accord — deux notes sur les cordes du milieu. Cela réduit l'harmonie à son essence et entraîne votre oreille à entendre la fonction sans la béquille des voicings complets.

### Construire une ligne de notes guides

Une ligne de notes guides est une ligne mélodique unique qui trace le chemin le plus fluide à travers une progression d'accords en suivant la tierce ou la septième de chaque accord. Quand l'une se résout vers le bas, suivez-la. Quand l'une reste en place, tenez-la.

Pour un arrangement de guitare seule, la ligne de notes guides devient la voix intérieure autour de laquelle vous construisez des voicings plus complets au-dessus et en dessous.

### Exercice pratique

Écrivez une ligne de notes guides (uniquement des tierces et des septièmes, en choisissant celles qui bougent le plus en douceur) sur la section A des **Rhythm Changes** en Sib :

```
Bbmaj7 | G7    | Cm7   | F7    |
Dm7    | G7    | Cm7   | F7    |
```

Commencez sur la tierce de Bbmaj7 (D). À chaque changement d'accord, allez vers la note guide la plus proche (tierce ou septième) du nouvel accord. Votre ligne doit bouger au plus d'un demi-ton ou d'un ton. Écrivez la ligne de huit notes obtenue.

---

## 5. Techniques de substitution

La substitution est l'art de remplacer un accord par un autre qui remplit une fonction harmonique semblable mais crée une couleur différente. Le jazz est construit sur des couches de substitutions appliquées à des progressions sous-jacentes simples.

### La substitution tritonique en profondeur

La substitution tritonique remplace un accord de septième de dominante par un autre accord de septième de dominante dont la fondamentale est à un triton (b5) de distance.

**G7 → Db7** (tous deux se résolvent sur C)

Pourquoi cela fonctionne-t-il ? Les **notes guides sont partagées :**

```
G7:   B (3rd)  F (7th)
Db7:  F (3rd)  Cb/B (7th)
```

La tierce et la septième échangent simplement leurs rôles. La résolution vers Cmaj7 fonctionne à l'identique, car F→E et B→C (ou Cb→C) dans les deux cas. Ce qui change, c'est le mouvement de basse : au lieu de G→C (quinte descendante), on obtient Db→C (descente chromatique) — un son plus lisse et plus moderne.

**Application au ii-V-I :**

```
Original:    Dm7  | G7    | Cmaj7
Tritone sub: Dm7  | Db7   | Cmaj7
With ii:     Abm7 | Db7   | Cmaj7  (Abm7 is the related ii of Db7)
```

### Substitution diminuée

Un accord de septième diminuée peut se substituer à un accord de septième de dominante situé un demi-ton sous l'une quelconque de ses quatre notes (parce que le dim7 est symétrique — chaque note est à une tierce mineure de la suivante).

**Bdim7 peut se substituer à :** G7, Bb7, Db7 ou E7 (accords de dominante dont la fondamentale est un demi-ton au-dessous de chaque note de l'accord diminué : Ab, B, D, F). Bdim7 est le 7b9 de chacun de ces accords, sans sa fondamentale.

### Accords diminués de passage

Un accord diminué peut relier deux accords diatoniques dont les fondamentales sont à un ton l'une de l'autre :

```
Cmaj7 | C#dim7 | Dm7
I       #Idim7   ii
```

La ligne de basse (C-C#-D) crée une montée chromatique. Le C#dim7 agit comme un A7b9 sans fondamentale (A-C#-E-G-Bb → sans A : C#-E-G-Bb).

### Dominante backdoor (bVII7 → I)

Au lieu de la résolution standard V7→I, le jazz utilise **bVII7→I** :

```
Standard: G7  → Cmaj7  (V → I)
Backdoor: Bb7 → Cmaj7  (bVII → I)
```

Le bVII7 aborde la tonique depuis un ton en dessous. La résolution fonctionne parce que Bb7 contient D et Ab, qui se résolvent sur C et G (ou E) par degré conjoint. Le son est chaleureux, inattendu, et évite l'attraction évidente de la dominante.

Le **ii apparenté** de la dominante backdoor : Fm7 → Bb7 → Cmaj7.

### Exercice pratique

Réharmonisez le pont des **Rhythm Changes** à l'aide des techniques de substitution. Le pont d'origine est :

```
D7  | D7  | G7  | G7  |
C7  | C7  | F7  | F7  |
```

Appliquez ces substitutions :
1. Ajoutez un ii apparenté avant chaque dominante
2. Appliquez des substitutions tritoniques à une dominante sur deux
3. Essayez un accord diminué de passage entre D7 et G7

Écrivez votre pont réharmonisé de 8 mesures. Il n'y a pas de réponse unique — l'objectif est de créer une conduite des voix fluide tout en ajoutant de la couleur harmonique.

---

## 6. La théorie accord-gamme

La théorie accord-gamme attribue une gamme à chaque accord, ce qui fournit un réservoir de notes mélodiques consonantes avec cette harmonie. C'est la pédagogie jazz standard de l'improvisation, même si elle a des limites importantes.

### Les attributions de base

| Qualité d'accord | Gamme | Origine | Notes à éviter |
|--------------|-------|--------|-------------|
| **Imaj7** | Ionien (majeur) | Gamme majeure | 4 (F en Do) |
| **Imaj7#11** | Lydien | Gamme majeure depuis le 4e degré | Aucune |
| **ii-7** | Dorien | Gamme majeure depuis le 2e degré | Aucune (la 6te naturelle ajoute de la couleur) |
| **V7** (qui se résout) | Mixolydien | Gamme majeure depuis le 5e degré | 4 (mais utilisable comme note de passage) |
| **V7#11** | Lydien dominant | Mineur mélodique depuis le 4e degré | Aucune |
| **V7alt** | Altéré | Mineur mélodique depuis le 7e degré | Aucune |
| **ii-7b5** | Locrien | Gamme majeure depuis le 7e degré | b2 (b9) — ou utiliser le locrien #2 (9e naturelle) |
| **i-7** | Dorien | — | — |
| **bVII7** (backdoor) | Lydien dominant | — | — |
| **dim7** | Diminuée (demi-ton/ton) | Symétrique | — |

### La gamme mère mineure mélodique

La gamme **mineure mélodique** (forme ascendante : 1 2 b3 4 5 6 7) est le couteau suisse du jazzman. Ses modes engendrent les gammes de la plupart des situations de dominantes altérées et étendues :

| Mode | Degré | Nom | Utilisé pour |
|------|--------|------|----------|
| 1er | Fondamentale | Mineur mélodique | Accords mineurs à septième majeure |
| 2e | 2e degré | Dorien b2 (phrygien #6) | Accords sus(b9) |
| 3e | 3e degré | Lydien augmenté | Accords maj7#5 |
| 4e | 4e degré | Lydien dominant | Accords 7#11, substitutions tritoniques |
| 5e | 5e degré | Mixolydien b6 | V7 se résolvant vers le mineur |
| 6e | 6e degré | Locrien #2 (éolien b5) | Accords demi-diminués |
| 7e | 7e degré | Altéré (super-locrien) | Accords V7alt |

### Les notes à éviter — ce qu'elles sont et ne sont pas

Une **note à éviter** est un degré de la gamme qui crée une neuvième mineure (intervalle de b9) contre une note de l'accord lorsqu'elle est tenue. Cela ne veut pas dire « ne jamais jouer cette note » — cela veut dire ne pas s'y poser ni la mettre en valeur. Comme note de passage ou approche chromatique, toute note est permise.

Exemple : sur Cmaj7, la note F (4e degré) crée un demi-ton (neuvième mineure) contre E (la tierce). Tenir F contre E produit une dissonance. Mais F comme note de passage entre E et G est parfaitement naturel.

### Les limites de la théorie accord-gamme

La théorie accord-gamme est une carte, pas le territoire :

- Elle fonctionne le mieux pour une harmonie lente, où chaque accord dure assez longtemps pour installer une gamme
- Sur des ii-V-I rapides, les musiciens expérimentés pensent en termes de **conduite des voix** et de **notes cibles**, pas de gammes
- Les plus grands improvisateurs de jazz (Parker, Coltrane, Shorter) dépassent la pensée par gammes grâce à l'**approche chromatique**, aux **enclosures** et au **développement motivique**
- La théorie accord-gamme ne dit rien du rythme, du phrasé ou de la narration — les éléments qui rendent réellement un solo captivant

### Exercice pratique

Pour chaque accord de la progression suivante, nommez la gamme associée et épelez ses notes. Identifiez les éventuelles notes à éviter :

```
Cmaj7 | Dm7 | G7alt | Cm(maj7) |
```

Jouez ensuite la progression à la guitare en improvisant une mélodie simple qui n'utilise que les notes de l'accord et une ou deux notes de la gamme par accord. Remarquez comment les notes guides (tierces et septièmes) créent les liaisons mélodiques les plus fortes.

---

## 7. Harmonie en quartes et structures supérieures

### Voicings en quartes

L'harmonie traditionnelle empile des **tierces**. L'harmonie en quartes empile des **quartes**. Le son est ouvert, ambigu et moderne — il évite la forte attraction majeur/mineur de l'harmonie en tierces.

**L'approche de McCoy Tyner :** sur un vamp en Ré dorien, empilez des quartes justes à partir de différents degrés de la gamme :

```
From D: D - G - C - F     (stacked 4ths)
From E: E - A - D - G     (stacked 4ths)
From G: G - C - F - Bb    (stacked 4ths — includes b6, outside Dorian)
```

Ces voicings peuvent être déplacés à l'intérieur du mode, créant un paysage harmonique chatoyant et non fonctionnel. Les voicings individuels ne se « résolvent » pas — ils flottent.

### Le voicing « So What »

Issu de l'enregistrement historique de Miles Davis (1959). Le voicing pour Ré dorien :

```
E - A - D - G - B
```

Il s'agit de trois quartes empilées (E-A-D-G) surmontées d'une tierce majeure (G-B). Il définit le son du jazz modal. Transposé un demi-ton plus haut pour le pont (Mib dorien) : F-Bb-Eb-Ab-C.

À la guitare, le voicing So What se joue généralement ainsi :

```
e --7-- (B)
B --8-- (G)
G --7-- (D)
D --7-- (A)
A --7-- (E)
E ----
```

### Triades de structure supérieure

Une triade de structure supérieure est une simple triade majeure ou mineure superposée à un accord de septième de dominante, qui crée des extensions et des altérations riches sans symboles d'accords complexes.

Sur **C7**, différentes triades de structure supérieure produisent :

| Triade supérieure | Notes (sur C-E-Bb) | Extensions créées |
|-------------|---------------------|-------------------|
| D majeur | D F# A | 9, #11, 13 — le son lydien dominant |
| Eb majeur | Eb G Bb | #9, 5, b7 — les extensions de l'« accord Hendrix » |
| Ab majeur | Ab C Eb | b13, fondamentale, #9 — le son altéré |
| F# majeur | F# A# C# | #11, b7(enh), b9 — altéré extrême |
| Bb majeur | Bb D F | b7, 9, 11 — le son sus/11 |

La beauté des structures supérieures, c'est que vous jouez une **triade simple** — quelque chose que vos mains connaissent déjà — pendant que le bassiste fournit la fondamentale et la septième. La combinaison produit une harmonie sophistiquée à partir d'ingrédients simples.

### Exercice pratique

Construisez des voicings en quartes à partir de chaque degré de Ré dorien (D E F G A B C) sur le jeu de cordes 4-3-2-1. Empilez trois quartes justes à partir de chaque note de départ. Écrivez les quatre notes de chaque voicing et identifiez la qualité d'accord obtenue (certains seront des accords en tierces familiers déguisés).

Ensuite : sur un vamp de C7, jouez des formes de triades de D majeur, Ab majeur et Eb majeur dans le registre aigu pendant qu'une note de basse C est tenue. Écoutez comment chaque structure supérieure change la couleur de l'accord de dominante.

---

## 8. Coltrane Changes

### La division symétrique en tierces majeures

En 1959, John Coltrane a introduit un système de substitution qui divise l'octave en trois parties égales (tierces majeures) : **B - G - Eb** (ou, de manière équivalente, trois notes quelconques à une tierce majeure d'écart). Cela crée trois centres tonaux équidistants les uns des autres.

Le cycle : en partant de n'importe quelle tonalité, descendez trois fois d'une tierce majeure, et vous revenez à votre point de départ :

```
C → Ab → E → C  (descending major thirds)
or equivalently:
C → E → Ab → C  (ascending major thirds)
```

### Analyse de Giant Steps

**« Giant Steps »** (Coltrane, 1960) en est l'application de référence. Toute la composition parcourt en cycle trois centres tonaux à une tierce majeure d'écart :

```
Bmaj7 D7 | Gmaj7 Bb7 | Ebmaj7 | Am7 D7  |
Gmaj7 Bb7| Ebmaj7 F#7| Bmaj7  | Fm7 Bb7 |
Ebmaj7   | Am7 D7    | Gmaj7  | C#m7 F#7|
Bmaj7    | Fm7 Bb7   | Ebmaj7 | C#m7 F#7|
```

Les trois centres tonaux sont **B, G et Eb** — chacun à une tierce majeure du précédent. Chaque arrivée dans une nouvelle tonalité est précédée de son V7 (et parfois de ii-V).

Le rythme harmonique est fulgurant : deux accords par mesure à un tempo rapide, avec des centres tonaux qui changent tous les un ou deux temps. C'est pourquoi « Giant Steps » était considéré comme presque injouable lors de son premier enregistrement — les accompagnateurs devaient traverser trois tonalités dans l'espace où une seule suffit normalement.

### Countdown, un Tune Up réharmonisé

**« Countdown »** montre comment les Coltrane Changes fonctionnent comme technique de réharmonisation. Le morceau d'origine est « Tune Up » de Miles Davis :

```
Tune Up:   Em7  | A7   | Dmaj7 | Dmaj7 |
Countdown: Em7  | F7 Bbmaj7 | Db7 Gbmaj7 | A7 Dmaj7 |
```

Coltrane remplace le simple ii-V-I par une chaîne de V-I descendant par tierces majeures :

- Depuis la cible (Dmaj7), il remonte le cycle des tierces majeures : Dmaj7 ← Gbmaj7 ← Bbmaj7
- Chaque centre tonal est précédé de son V7 : A7→D, Db7→Gb, F7→Bb
- Le résultat : trois résolutions ii-V-I comprimées en quatre mesures

### La géométrie

Le cycle de Coltrane est un **triangle inscrit dans le cycle des quintes** — trois points équidistants sur le cadran des douze sons. Là où l'harmonie jazz traditionnelle tourne autour du cycle par quintes (pas adjacents), Coltrane le traverse par bonds de tierces majeures (tous les quatre pas).

```
       C
   F       G
 Bb           D
Eb             A
 Ab           E
   Db      B
       F#

Triangle 1: C - E - Ab
Triangle 2: D - F# - Bb
Triangle 3: Eb - G - B  ← Giant Steps triangle
Triangle 4: F - A - Db
```

Il n'existe que quatre triangles de tierces majeures distincts. Ensemble, ils divisent les douze sons en quatre groupes de trois.

### Appliquer les Coltrane Changes à n'importe quel ii-V-I

Pour réharmoniser un ii-V-I avec le cycle de Coltrane :

1. Identifiez la tonalité cible (l'accord de I)
2. Trouvez les deux autres tonalités à une tierce majeure d'écart
3. Insérez un V7→I pour chaque centre tonal, en partant du plus éloigné et en revenant vers la cible

**Exemple — réharmoniser Dm7-G7-Cmaj7 :**

```
Original:  Dm7     | G7      | Cmaj7   |
Coltrane:  Dm7 Eb7 | Abmaj7 B7 | Emaj7 G7 | Cmaj7 |
```

Ou, plus compact :

```
Dm7 | Eb7 Abmaj7 | B7 Emaj7 | Cmaj7 |
```

### Exercice pratique

1. Écrivez les trois centres tonaux en tierces majeures pour un ii-V-I en **Fa majeur** (cible : Fmaj7).
2. Réharmonisez `Gm7 | C7 | Fmaj7` avec le cycle de Coltrane, en insérant des paires V7→I pour chaque centre tonal.
3. Jouez lentement votre réharmonisation à la guitare avec des voicings en shell. Concentrez-vous sur le mouvement de la basse — il doit suivre un motif de tierces majeures descendantes reliées par des demi-tons ascendants (les fondamentales des V7).

---

## Tableau de référence des standards

Les standards de jazz suivants servent de matériau d'étude tout au long de ce cours :

| Standard | Compositeur | Notions clés | Pourquoi l'étudier |
|----------|----------|-------------|--------------|
| **Autumn Leaves** | Kosma/Mercer | ii-V-I en majeur et en relatif mineur | Le premier morceau de jazz idéal — deux ii-V-I dans des tonalités relatives |
| **All The Things You Are** | Kern/Hammerstein | ii-V-I enchaînés à travers quatre centres tonaux | Le standard le plus riche harmoniquement du répertoire |
| **Rhythm Changes** | Gershwin (I Got Rhythm) | Turnarounds, dominantes du pont, terrain de jeu de la substitution | La forme de jazz la plus courante après le blues |
| **Stella by Starlight** | Young | Chaînes de ii-V, mélange modal, résolution rompue | Met à l'épreuve votre capacité à suivre des centres tonaux qui changent vite |
| **Giant Steps** | Coltrane | Division symétrique en tierces majeures, Coltrane Changes | Le parcours d'obstacles harmonique ultime |
| **So What** | Davis | Jazz modal, voicings en quartes, vamp dorien | La naissance du jazz modal — deux accords, des possibilités infinies |

Ces morceaux forment un vocabulaire de base. Un guitariste de jazz capable de conduire les voix, d'accompagner et d'improviser sur ces six morceaux a couvert l'essentiel du paysage harmonique de la tradition.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **ii-V-I** | La progression d'accords fondamentale du jazz : septième sur la sus-tonique, septième de dominante, tonique — construite sur un mouvement de fondamentales en quintes descendantes |
| **Voicing en shell** | Un voicing minimal ne contenant que la fondamentale, la tierce et la septième d'un accord |
| **Voicing drop-2** | Un voicing en position serrée réarrangé en abaissant d'une octave la deuxième note la plus haute |
| **Notes guides** | La tierce et la septième d'un accord — les notes qui définissent sa qualité et guident la conduite des voix |
| **Substitution tritonique** | Remplacement d'une septième de dominante par une autre septième de dominante dont la fondamentale est à un triton (notes guides partagées) |
| **Dominante backdoor** | Résolution vers la tonique depuis bVII7 au lieu de V7 |
| **Théorie accord-gamme** | La pratique qui consiste à attribuer une gamme parente à chaque qualité d'accord pour l'improvisation |
| **Note à éviter** | Un degré de la gamme qui crée une neuvième mineure contre une note de l'accord lorsqu'il est tenu |
| **Mineur mélodique** | La « gamme mère » mineure du jazz (1 2 b3 4 5 6 7) dont les modes engendrent les gammes de dominantes altérées et étendues |
| **Voicing en quartes** | Un accord construit en empilant des quartes justes plutôt que des tierces |
| **Triade de structure supérieure** | Une triade majeure ou mineure superposée à une septième de dominante pour créer des extensions |
| **Coltrane Changes** | Une technique de réharmonisation qui divise l'octave en trois centres tonaux à une tierce majeure d'écart |
| **Conduite des voix** | L'art d'enchaîner les accords avec un mouvement mélodique minimal dans chaque voix |
| **Extensions** | Notes de l'accord au-delà de la septième : 9e, 11e, 13e |
| **Altérations** | Extensions élevées ou abaissées chromatiquement : b9, #9, #11, b13 |

---

## Auto-évaluation

**1. Épelez les notes d'un accord Dm7b5 et nommez la gamme qui lui est le plus souvent associée.**
> D F Ab C. La gamme est le locrien (D Eb F G Ab Bb C) ou le locrien #2 (D E F G Ab Bb C, le 6e mode du mineur mélodique).

**2. Dans un ii-V-I en Sib majeur, quels sont les trois accords ? Montrez comment les notes guides de l'accord de ii s'enchaînent avec celles de l'accord de V.**
> Cm7 - F7 - Bbmaj7. La 7e de Cm7 (Bb) descend vers la tierce de F7 (A). La tierce de Cm7 (Eb) devient la 7e de F7 (Eb). Les notes guides échangent leurs rôles.

**3. Quelle est la substitution tritonique de G7, et pourquoi fonctionne-t-elle ?**
> Db7. Elle fonctionne parce que G7 et Db7 partagent les mêmes notes guides : B/Cb et F, avec leurs rôles de tierce et de septième inversés. Tous deux se résolvent vers Cmaj7 avec le même mouvement de conduite des voix.

**4. Nommez les trois centres tonaux de Giant Steps et la relation géométrique qui les unit.**
> B, G et Eb. Ils sont équidistants sur le cercle chromatique, chacun à une tierce majeure d'écart, et forment un triangle équilatéral sur le cycle des quintes.

**5. Construisez un voicing en quartes à partir de A avec des quartes justes empilées (quatre notes). À quel accord familier ce voicing ressemble-t-il ?**
> A - D - G - C. C'est un Am7(11) ou, de manière équivalente, un voicing C/A. L'empilement de quartes contient les notes de Am7 (A C G) plus D (la 11e), mais sans l'ordre en tierces.

**Critères de réussite :** identifier toutes les progressions ii-V-I d'une grille inconnue, y conduire les voix avec au moins deux types de voicings, appliquer une technique de substitution et expliquer la logique de conduite des voix de chaque enchaînement d'accords.

---

## Fondements de recherche

- Le ii-V-I comme progression fondatrice du jazz est documenté dans tous les grands ouvrages de pédagogie du jazz et constitue la progression statistiquement la plus courante du Great American Songbook
- La théorie accord-gamme provient principalement de la tradition pédagogique Berklee/NEC formalisée par George Russell (Lydian Chromatic Concept, 1953) et systématisée par Jamey Aebersold, Jerry Coker et Mark Levine
- L'analyse des Coltrane Changes s'appuie sur la biographie de Lewis Porter et sur la thèse de Demsey (1991) consacrée à l'harmonie symétrique de Coltrane
- La conduite des voix par notes guides et la pédagogie harmonique de Barry Harris représentent la tradition orale de l'harmonie bebop
- Les systèmes de voicings drop-2 et drop-3 ont été codifiés par Ted Greene, Mick Goodrick et le département de guitare de Berklee
- Sources : Levine, *The Jazz Theory Book* (1995) ; Goodrick, *The Advancing Guitarist* et *Almanac of Guitar Voice Leading* (1987/2011) ; série Aebersold Play-Along ; Porter, *John Coltrane: His Life and Music* (1998)
- État de croyance : T(0.80) F(0.05) U(0.10) C(0.05)
