---
module_id: mus-006-the-scale-universe
department: music
course: Fondements de la théorie musicale
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutes"
produced_by: music
version: "1.0.0"
---

# L'univers des gammes : 4 096 possibilités à partir de 12 notes

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée : 45 minutes

## Objectifs d'apprentissage

Après ce cours, vous serez capable de :

- Représenter n'importe quelle gamme comme un nombre binaire de 12 bits et le convertir en entier décimal
- Expliquer pourquoi il existe exactement 4 096 gammes mathématiquement possibles dans le tempérament égal à 12 demi-tons
- Calculer les modes de n'importe quelle gamme par décalages circulaires (rotations de bits)
- Distinguer le nombre total (4 096) du nombre obtenu sous diverses équivalences (formes premières, classes de Forte)
- Appliquer les critères de Zeitler pour réduire l'univers aux gammes « musicalement réelles »
- Calculer les vecteurs d'intervalles, la luminosité et les propriétés de symétrie à partir de l'entier d'une gamme
- Associer n'importe quel entier de gamme à des positions sur le manche de la guitare
- Relier l'espace des gammes aux relations d'équivalence OPTIC-K utilisées en théorie des ensembles musicaux

---

## 1. L'alphabet chromatique

La musique occidentale utilise douze classes de hauteur par octave. Une **classe de hauteur** est une note indépendamment de l'octave dans laquelle elle apparaît — tous les Do d'un piano appartiennent à la même classe de hauteur.

Les douze classes de hauteur, numérotées de 0 à 11 :

| Classe de hauteur | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|
| Nom de note | C | C#/Db | D | D#/Eb | E | F | F#/Gb | G | G#/Ab | A | A#/Bb | B |

Pensez maintenant à une gamme comme à un **choix** : pour chacune des douze classes de hauteur, soit elle est **dans** la gamme (1), soit elle est **hors** de la gamme (0). Cela nous donne un nombre binaire de 12 bits — douze décisions oui/non indépendantes.

**Combien de choix possibles ?** Deux options pour chacune des douze positions :

$$ 2^{12} = 4096 $$

Il existe exactement 4 096 gammes mathématiquement possibles dans le tempérament égal à 12 demi-tons. Cela inclut la gamme vide (que des zéros), la gamme chromatique (que des uns), toutes les « gammes » d'une seule note, toutes les gammes traditionnelles et chaque collection étrange entre les deux.

C'est l'**univers des gammes**. Sa taille est finie, connaissable et étonnamment petite — un nombre qu'un ordinateur peut énumérer en quelques microsecondes.

---

## 2. Une gamme EST un nombre

Voici le changement de perspective essentiel : **chaque gamme est un entier compris entre 0 et 4095**.

### La correspondance des bits

Attribuez à chaque classe de hauteur une position de bit :

| Bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| Classe de hauteur | C | C# | D | D# | E | F | F# | G | G# | A | A# | B |
| Valeur de position | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

Pour convertir une gamme en entier, marquez chaque note d'un 1 et additionnez les valeurs de position.

### Exemple : la gamme majeure

La **gamme de Do majeur** contient les notes Do, Ré, Mi, Fa, Sol, La, Si — classes de hauteur 0, 2, 4, 5, 7, 9, 11.

En binaire (lecture du bit 11 jusqu'au bit 0) :

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
Note:     B  Bb  A  Ab G  Gb F  E  Eb D  Db C
In scale:  1  0  1  0  1  0  1  1  0  1  0  1
```

En décimal :

$$ 1 + 4 + 16 + 32 + 128 + 512 + 2048 = 2741 $$

**Do majeur = 2741.**

Toutes les gammes majeures ont la même **structure intervallique** : quelle que soit la fondamentale, le motif (pas de 2-2-1-2-2-2-1 demi-tons) définit le majeur. L'entier 2741 est la représentation enracinée sur Do. Enracinée sur d'autres notes, le motif subit une rotation.

### Exemple : la gamme pentatonique mineure

La gamme **pentatonique mineure de Do** contient Do, Mib, Fa, Sol, Sib — classes de hauteur 0, 3, 5, 7, 10.

En binaire :

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
In scale:  0  1  0  0  1  0  1  0  1  0  0  1
```

En décimal :

$$ 1 + 8 + 32 + 128 + 1024 = 1193 $$

**Pentatonique mineure de Do = 1193.**

### Pourquoi c'est important

Dès que vous acceptez qu'une gamme est un nombre, tout le reste suit :
- Vous pouvez **énumérer** toutes les gammes (compter de 0 à 4095)
- Vous pouvez **comparer** des gammes (comparaison d'entiers)
- Vous pouvez **transformer** des gammes (opérations sur les bits : décalage, AND, OR, XOR, POPCOUNT)
- Vous pouvez **rechercher** des gammes (selon des vecteurs d'intervalles, des cardinalités, des symétries précises)
- Vous pouvez **stocker** des gammes (12 bits au lieu d'une liste de notes)

Une gamme n'a rien de mystique. C'est un nombre.

### Exercice pratique

Convertissez les trois gammes suivantes en entiers à l'aide de la correspondance des bits :

1. **Do mineur naturel** (Do, Ré, Mib, Fa, Sol, Lab, Sib) — classes de hauteur 0, 2, 3, 5, 7, 8, 10
2. **Pentatonique majeure de Do** (Do, Ré, Mi, Sol, La) — classes de hauteur 0, 2, 4, 7, 9
3. **Gamme par tons de Do** (Do, Ré, Mi, Fa#, Sol#, La#) — classes de hauteur 0, 2, 4, 6, 8, 10

Calculez chacune en additionnant les valeurs de position (puissances de 2). Vérifiez vos réponses ci-dessous.

Réponses :
1. Do mineur naturel = 1 + 4 + 8 + 32 + 128 + 256 + 1024 = **1453**
2. Pentatonique majeure de Do = 1 + 4 + 16 + 128 + 512 = **661**
3. Gamme par tons de Do = 1 + 4 + 16 + 64 + 256 + 1024 = **1365**

---

## 3. Les modes comme rotations

Un **mode** est une gamme commencée à partir d'un autre degré. Do dorien contient les mêmes notes que Sib majeur, mais commence sur Do. Dans la représentation entière, il ne s'agit ni d'une addition ni d'une multiplication — c'est une **rotation**.

### L'opération de décalage circulaire

Pour trouver le mode suivant d'une gamme :
1. Trouvez le bit à 1 le plus bas (la fondamentale)
2. Retirez-le et décalez le reste du motif vers le bas
3. Replacez l'ancienne fondamentale en haut

Plus précisément, la rotation modale est un **décalage circulaire à droite** de la distance, en demi-tons, entre l'ancienne fondamentale et la nouvelle : chaque classe de hauteur p devient (p − n) mod 12, de sorte que la nouvelle fondamentale arrive sur le bit 0. Dans un système à 12 bits, « revenir au début » signifie que les bits qui sortent par le bord droit réapparaissent à gauche. Un décalage circulaire à droite de n équivaut à un décalage circulaire à gauche de 12 − n.

Attention au sens : un décalage circulaire **à gauche** de n ajoute n à chaque classe de hauteur, ce qui **transpose** la gamme vers le haut au lieu de changer son mode. Décaler Do majeur (2741) de 2 vers la gauche donne Ré majeur (2774) ; le décaler de 2 vers la droite donne Ré dorien ramené sur Do, c'est-à-dire Do dorien (1709).

### Exemple : les modes du majeur

Le motif de la gamme majeure a pour intervalles 2-2-1-2-2-2-1 (sept notes). Ses sept modes sont engendrés par rotation vers chacun des sept degrés de la gamme :

| Nom du mode | Degré de départ | Motif d'intervalles |
|-----------|----------------|------------------|
| Ionien (majeur) | 1 | 2-2-1-2-2-2-1 |
| Dorien | 2 | 2-1-2-2-2-1-2 |
| Phrygien | 3 | 1-2-2-2-1-2-2 |
| Lydien | 4 | 2-2-2-1-2-2-1 |
| Mixolydien | 5 | 2-2-1-2-2-1-2 |
| Éolien (mineur naturel) | 6 | 2-1-2-2-1-2-2 |
| Locrien | 7 | 1-2-2-1-2-2-2 |

Ce ne sont **pas sept gammes différentes.** Ce sont sept rotations du même motif sous-jacent. Quand vous jouez Ré dorien sur un piano, vous jouez les touches blanches en partant de Ré.

### Calculer les rotations par des opérations sur les bits

En pseudocode, pour faire tourner un entier de gamme de 12 bits de `n` positions vers la gauche :

```
rotate_left(scale, n):
    shifted = (scale << n) & 0xFFF        # shift left, mask to 12 bits
    wrapped = scale >> (12 - n)           # bits that fell off
    return shifted | wrapped               # combine

mode(scale, n):                           # n = semitones from old root to new root
    return rotate_left(scale, (12 - n) % 12)   # = circular right shift by n
```

Appliqué à la gamme majeure (2741), `mode(2741, n)` pour n = 0, 2, 4, 5, 7, 9, 11 produit la représentation entière de chaque mode sur Do : ionien 2741, dorien 1709, phrygien 1451, lydien 2773, mixolydien 1717, éolien 1453, locrien 1387. (`rotate_left(2741, n)` donnerait plutôt les gammes majeures sur Ré, Mi, Fa...)

### Exercice pratique

Calculez les trois premiers modes de la **gamme mineure harmonique** (Do Ré Mib Fa Sol Lab Si — intervalles 2-1-2-2-1-3-1).

1. Écrivez la représentation binaire sur 12 bits de Do mineur harmonique
2. Déterminez de combien de bits il faut tourner pour obtenir le 2e mode (locrien bécarre 6)
3. Déterminez de combien de bits il faut tourner pour obtenir le 3e mode (ionien #5)

Indice : le nombre de positions de rotation est égal au nombre de demi-tons entre l'ancienne fondamentale et la nouvelle.

Esquisse de réponse :
- Do mineur harmonique = 2477 (binaire : 100110101101)
- Rotation à droite de 2 demi-tons (Ré est 2 demi-tons au-dessus de Do) → 2e mode sur Do : Do Réb Mib Fa Solb La Sib = 1643
- Rotation à droite de 3 demi-tons (Mib est 3 demi-tons au-dessus de Do) → 3e mode sur Do : Do Ré Mi Fa Sol# La Si = 2869

Les sept modes du mineur harmonique sont tous des rotations de l'entier 2477.

---

## 4. Combien sont vraiment uniques ?

Nous sommes partis de **4 096** gammes. Mais beaucoup d'entre elles sont « les mêmes » sous différentes équivalences. Combien de structures sont réellement distinctes ?

### Formes premières — ignorer la rotation

Deux gammes sont **modalement équivalentes** si l'une est une rotation de l'autre. La **forme première** d'une gamme est son représentant canonique — par convention, la rotation de plus petite valeur entière (ou la rotation qui regroupe les notes vers le début).

Sous l'équivalence modale :
- La famille de la gamme majeure à 7 notes a 7 rotations (7 modes) → 1 forme première
- La gamme par tons à 6 notes n'a qu'une seule rotation unique (elle se transforme en elle-même) → 1 forme première
- La gamme chromatique à 12 notes est sa propre forme première

**Compter les formes premières :** sur les 4 096 gammes, exactement **352** sont structurellement uniques par rotation, en comptant toutes les cardinalités, de la gamme vide à la gamme chromatique (les 352 colliers binaires à 12 perles, OEIS A000031).

### Classes de Forte — ignorer la rotation ET l'inversion

Dans les années 1970, Allen Forte a formalisé une équivalence supplémentaire : traiter une gamme et son **inversion** (image miroir) comme la même structure. L'inversion d'une gamme renverse son motif d'intervalles.

- La **gamme majeure** (2-2-1-2-2-2-1) s'inverse en **phrygien** (1-2-2-2-1-2-2) — attendez, c'EST un mode du majeur.
- Mais la plupart des gammes ont des inversions qui ne sont PAS dans la même famille modale.

Sous l'**équivalence T/I** (transposition + inversion), la table de Forte recense **208 classes d'ensembles distinctes** pour les cardinalités 3 à 9. En ajoutant les 16 classes à 0, 1, 2, 10, 11 ou 12 notes, on obtient **224 classes d'ensembles** sur toutes les cardinalités de 0 à 12.

Le **nombre de Forte** (par exemple « 7-35 » pour la gamme diatonique/majeure) est un système de dénomination normalisé où :
- Premier nombre = cardinalité (nombre de notes)
- Second nombre = position ordinale au sein de cette cardinalité (triée selon un ordre canonique)

### Le cas particulier de la gamme par tons

La gamme par tons (Do Ré Mi Fa# Sol# La#) a un motif d'intervalles 2-2-2-2-2-2. Chaque rotation produit une gamme identique — elle n'a **qu'un seul mode**.

Son entier : 1365 (binaire 010101010101).

Faites-la tourner d'un nombre pair de positions : vous retrouvez 1365. Faites-la tourner d'un nombre impair : vous obtenez l'autre gamme par tons (2730, binaire 101010101010).

Il n'existe donc que **deux gammes par tons** dans tout l'univers, et chacune est la transposition de l'autre d'un demi-ton. Sous l'équivalence de Forte, les deux appartiennent à la même classe d'ensembles.

### La hiérarchie des dénombrements

| Équivalence | Nombre | Ce qui est identifié |
|-------------|-------|-----------------|
| Aucune (brut) | 4,096 | Tous les sous-ensembles des 12 classes de hauteur |
| Transposition (T) | 352 formes premières | Rotations d'un même motif |
| Transposition + inversion (T/I) | 224 classes de Forte | Ci-dessus, plus les images miroirs |
| T/I + complémentation | 122 | Ci-dessus, plus les paires gamme + complément |

### Exercice pratique

Convainquez-vous que la gamme par tons est « modalement invariante » :

1. Écrivez la gamme par tons de Do en binaire sur 12 bits : 010101010101
2. Faites une rotation de 2 bits vers la gauche : qu'obtenez-vous ?
3. Faites une rotation de 1 bit vers la gauche : qu'obtenez-vous ?
4. Expliquez pourquoi une gamme à structure intervallique uniforme (des pas tous de même taille) a moins de modes uniques

Réponses :
1. 010101010101 = 1365
2. Rotation de 2 vers la gauche : toujours 010101010101 = 1365 (même gamme)
3. Rotation de 1 vers la gauche : 101010101010 = 2730 (l'autre gamme par tons)
4. Une gamme à N notes a au plus N modes, mais si la gamme possède une symétrie de rotation (elle se transforme en elle-même par une rotation de k demi-tons avec k < 12), elle a moins de modes uniques. La gamme par tons se transforme en elle-même par une rotation de 2 demi-tons, donc ses six modes sont tous la même gamme, et ses rotations d'un nombre quelconque de demi-tons ne produisent que deux gammes distinctes (1365 et 2730).

---

## 5. Qu'est-ce qui fait une « vraie gamme » ?

Sur les 4 096 possibilités mathématiques, la plupart ne sont pas utiles en musique. Une gamme comme `101100000001` (Do, Réb, Mib, Si) est une collection de notes, mais personne ne l'appellerait une gamme au sens pratique. Comment réduire l'univers aux gammes légitimes ?

### Les critères de Zeitler

Le catalogue exhaustif de William Zeitler (allthescales.org) définit une gamme par les critères 1 et 2 ci-dessous ; ce module y ajoute les critères 3 et 4 comme filtres supplémentaires :

1. **La fondamentale est présente** — le bit 0 doit être à 1. Une gamme doit contenir sa propre tonique. Cela élimine 2 048 gammes (la moitié de l'univers).

2. **Aucun écart supérieur à 4 demi-tons** — deux notes consécutives de la gamme ne peuvent être distantes de plus d'une tierce majeure. Un écart de 5 demi-tons ou plus crée un trou audible qui rompt la continuité de la gamme.

3. **Entre 5 et 8 notes** — les gammes hors de cet intervalle sonnent soit trop clairsemées (pour être entendues comme des gammes), soit trop denses (pour être distinguées du chromatisme). C'est une contrainte pragmatique, pas mathématique.

4. **Aucun agrégat de plus de 3 demi-tons consécutifs** — quatre notes chromatiques ou plus à la suite forment un cluster chromatique qui perd son caractère de gamme.

Les critères 1 et 2 réduisent à eux seuls les 4 096 gammes à exactement **1 490**, le compte de Zeitler. L'application des quatre critères tels qu'énoncés ici en laisse **716**. C'est encore bien plus que le répertoire familier des gammes qui portent un nom.

### Pourquoi ces critères sont des lignes directrices, pas des lois

Les critères de Zeitler sont des **heuristiques**, pas des définitions. Les contre-exemples abondent :

- La **gamme chromatique** a 12 demi-tons consécutifs (elle enfreint le critère 4) — c'est clairement une vraie gamme
- Les **« bourdons » d'une seule note** enfreignent le minimum de 5 notes — c'est clairement une vraie structure musicale
- Les **gammes blues** utilisent parfois habilement des écarts de 3 demi-tons (la pentatonique mineure de Do a des écarts de 3 demi-tons de Do à Mib et de Sol à Sib)
- Les **gammes du gagaku**, les gammes microtonales et d'autres systèmes non occidentaux ne rentrent pas du tout dans le 12-TET

Les critères sont **propres à une culture** — ils décrivent des gammes adaptées à la pratique tonale et modale européenne. Ce sont un filtre utile, pas une vérité universelle.

### Exercice pratique

Pour chacune des gammes suivantes, déterminez quels critères de Zeitler elle enfreint (le cas échéant) :

1. **Do majeur** (0, 2, 4, 5, 7, 9, 11)
2. **Do chromatique** (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
3. **Une gamme à écart** (0, 5, 11) — Do, Fa, Si
4. **Une gamme en cluster** (0, 1, 2, 3, 4) — Do, Do#, Ré, Ré#, Mi

Réponses :
1. Do majeur : n'en enfreint aucun — satisfait tous les critères
2. Do chromatique : enfreint le critère 3 (12 notes, au-delà du maximum de 8) et le critère 4 (12 demi-tons consécutifs)
3. Gamme à écart : enfreint le critère 2 (écarts de 5 demi-tons de Do à Fa et de 6 de Fa à Si) et le critère 3 (seulement 3 notes)
4. Gamme en cluster : enfreint le critère 4 (5 demi-tons consécutifs) et le critère 2 (écart de 8 demi-tons de Mi jusqu'au Do suivant) ; ses 5 notes satisfont le critère 3

---

## 6. Les propriétés d'une gamme que l'on peut calculer

Dès qu'une gamme est un entier, toutes ses propriétés musicales deviennent calculables. Vous n'avez pas besoin d'écouter — vous pouvez analyser le nombre.

### Vecteur d'intervalles

Un **vecteur d'intervalles** compte combien de fois chaque classe d'intervalles apparaît dans la gamme. Il existe six classes d'intervalles (de 1 à 6 demi-tons ; le triton est son propre renversement, et les intervalles 7-11 sont les compléments de 1-5).

Pour la **gamme de Do majeur** (Do Ré Mi Fa Sol La Si) :

```
Interval class: 1   2   3   4   5   6
Count:          2   5   4   3   6   1
```

Vecteur d'intervalles : `[2, 5, 4, 3, 6, 1]`

Le vecteur se calcule en examinant toutes les paires de notes de la gamme et en comptant la distance qui les sépare (ramenée à l'intervalle 1-6).

**Pourquoi c'est important :** le vecteur d'intervalles encode le potentiel harmonique. Les gammes riches en tierces et en quintes (classes d'intervalles 3, 4, 5) sonnent consonantes et tonales. Les gammes chargées en classes d'intervalles 1 et 6 sonnent dissonantes et instables.

### Luminosité

La **luminosité** est la somme des classes de hauteur (positions des bits à 1). Des sommes plus élevées signifient que les notes de la gamme sont plus hautes dans le cercle chromatique (plus de dièses), des sommes plus basses signifient plus de bémols.

- Do majeur (0, 2, 4, 5, 7, 9, 11) : somme = 38
- Do lydien (0, 2, 4, 6, 7, 9, 11) : somme = 39 — plus lumineux d'une unité
- Do phrygien (0, 1, 3, 5, 7, 8, 10) : somme = 34 — plus sombre

Le **spectre du locrien au lydien** (des modes du majeur les plus sombres aux plus lumineux) correspond à des valeurs de luminosité strictement croissantes. C'est une propriété calculée — aucune oreille requise.

### Symétrie

Une gamme possède une **symétrie de rotation** si une rotation de k demi-tons produit la même gamme. L'ordre de symétrie de la gamme vous indique combien de transpositions distinctes elle possède.

- **Gamme par tons :** symétrie tous les 2 demi-tons → seulement 2 transpositions distinctes
- **Gamme diminuée (octatonique) :** symétrie tous les 3 demi-tons → seulement 3 transpositions distinctes
- **Gamme augmentée :** symétrie tous les 4 demi-tons → seulement 4 transpositions distinctes
- **Gamme majeure :** aucune symétrie de rotation → les 12 transpositions sont toutes distinctes

### Chiralité

Une gamme est **chirale** si son inversion (image miroir autour de la classe de hauteur 0) n'est PAS identique à l'une de ses propres rotations. La plupart des gammes sont chirales. Les exceptions incluent la gamme majeure (dont l'inversion est le mode phrygien, qui EST une rotation) et les gammes symétriques.

### Relation Z

Deux gammes sont **en relation Z** si elles ont le même vecteur d'intervalles mais ne sont PAS liées par transposition ou inversion. Elles sonnent de façon semblable sur le plan harmonique mais sont structurellement distinctes. Les paires en relation Z sont rares et musicalement fascinantes.

La paire Z la plus célèbre : la relation Z des **tétracordes à tous les intervalles** `{0,1,4,6}` et `{0,1,3,7}`, tous deux de vecteur d'intervalles `[1,1,1,1,1,1]`.

### Exercice pratique

Calculez le vecteur d'intervalles de la **gamme pentatonique mineure de Do** (Do Mib Fa Sol Sib = classes de hauteur 0, 3, 5, 7, 10).

Étape 1 : listez toutes les paires et leurs distances.
Étape 2 : ramenez les distances à des classes d'intervalles (les distances 7-11 deviennent 12 − distance : par ex. 8 demi-tons → classe 4).
Étape 3 : comptez les occurrences de chaque classe.

Réponse :
Paires et distances :
- 0-3 : 3
- 0-5 : 5
- 0-7 : 5 (7 se ramène à 5)
- 0-10 : 2 (10 se ramène à 2)
- 3-5 : 2
- 3-7 : 4
- 3-10 : 5 (7 se ramène à 5)
- 5-7 : 2
- 5-10 : 5
- 7-10 : 3

Nombre d'occurrences par classe d'intervalles :
- Classe 1 : 0
- Classe 2 : 3
- Classe 3 : 2
- Classe 4 : 1
- Classe 5 : 4
- Classe 6 : 0

Vecteur d'intervalles : **[0, 3, 2, 1, 4, 0]**

Remarque : forte présence de la classe 5 (quartes/quintes justes) et absence de la classe 6 (triton) et de la classe 1 (demi-ton) — c'est pourquoi les gammes pentatoniques sonnent stables et « jamais fausses ».

---

## 7. Explorer les gammes sans nom à la guitare

Les manuels de théorie musicale couvrent peut-être **200 gammes nommées** : majeure, mineure, modes, pentatoniques, mineures harmonique et mélodique et leurs modes, diminuée, par tons, blues, gammes bebop, une poignée de gammes « exotiques » (hongroise, byzantine, etc.) et les modes de Messiaen.

Il reste donc **environ 1 300 gammes sans nom** parmi les 1 490 qui satisfont les critères de base de Zeitler (environ 500 parmi les 716 qui passent les quatre). L'immense majorité de l'univers des gammes est un territoire inexploré.

### Comment explorer

1. **Choisissez un nombre** entre 1 et 4095 (ou utilisez un générateur aléatoire)
2. **Décodez les bits** pour trouver quelles classes de hauteur sont dans la gamme
3. **Vérifiez les critères de Zeitler** — cette gamme est-elle « raisonnable » ?
4. **Jouez-la** sur votre instrument et écoutez
5. **Notez le vecteur d'intervalles** et comparez-le aux gammes que vous connaissez

### Formule de correspondance sur le manche

Pour jouer un entier de gamme à la guitare, vous devez associer les classes de hauteur aux positions de frettes sur chaque corde.

Données :
- Entier de gamme S
- Classes de hauteur des cordes à vide en accordage standard : Mi(4), La(9), Ré(2), Sol(7), Si(11), Mi(4)
- Pour chaque corde, calculez quelles frettes (0-12) portent une note de la gamme

**Formule :** pour chaque frette f (de 0 à 12) sur une corde dont la classe de hauteur à vide est p :

```
pitch_class_at_fret = (p + f) mod 12
is_in_scale = (S >> pitch_class_at_fret) & 1
```

Si le résultat vaut 1, marquez cette frette. Répétez pour les six cordes.

### Exemple : une gamme au hasard

Choisissez l'entier de gamme **1749**. Décodez :

```
1749 in binary: 011011010101
Pitch classes (reading bits 0-11): 0, 2, 4, 6, 7, 9, 10
Notes from C:                     C, D, E, F#, G, A, Bb
```

Cette gamme a 7 notes, contient Do (la fondamentale est présente), son plus grand écart est de 2 demi-tons, sans longs clusters — elle satisfait les critères de Zeitler.

Motif d'intervalles : 2-2-2-1-2-1-2 (somme égale à 12).

**C'est le mixolydien #11** (ou lydien dominant, le 4e mode du mineur mélodique) — une gamme qui porte un nom ! Vous venez de la redécouvrir en choisissant un nombre.

Essayez un nombre moins balisé : **2391**. Décodez :

```
2391 in binary: 100101010111
Pitch classes: 0, 1, 2, 4, 6, 8, 11
Notes from C: C, C#, D, E, F#, G#, B
```

Elle satisfait trois critères de Zeitler (fondamentale présente, plus grand écart de 3 demi-tons, 7 notes) mais échoue au critère 4 : Si, Do, Do#, Ré forment quatre demi-tons consécutifs, en passant de Si à Do. Ce n'est pas non plus une gamme couramment nommée. Les critères sont des heuristiques, alors jouez-la quand même à la guitare. Écoutez. Donnez-lui un nom.

### Le protocole d'exploration

1. Générez 5 à 10 nombres de gammes aléatoires qui satisfont les critères de Zeitler
2. Jouez chacune pendant 30 secondes en étant attentif à son caractère émotionnel
3. Notez vos préférées
4. Construisez des mélodies simples en utilisant la couleur intervallique propre à chaque gamme
5. Comparez-les aux gammes nommées ayant des vecteurs d'intervalles semblables

C'est ainsi que l'on découvre de la nouvelle musique. L'univers est là ; la correspondance est mécanique ; le jugement musical vous appartient.

### Exercice pratique

Prenez l'entier de gamme **1709** (Do dorien).

1. Convertissez-le en binaire et identifiez les classes de hauteur
2. Écrivez la gamme en commençant sur Do
3. Calculez le motif d'intervalles (les pas entre notes consécutives)
4. Reportez la gamme sur les deux cordes aiguës d'une guitare en accordage standard (1re corde = Mi, 2e corde = Si) pour les frettes 0-12

Indice : 1709 = 1024 + 512 + 128 + 32 + 8 + 4 + 1 → bits 0, 2, 3, 5, 7, 9, 10.

---

## 8. Lien avec OPTIC-K

La théorie des ensembles musicaux utilise une taxonomie de **relations d'équivalence** pour décrire comment deux collections de notes peuvent être considérées comme « identiques ». Le moyen mnémotechnique OPTIC les rassemble toutes. Le cadre des entiers de gammes rend ces équivalences calculables.

### Les cinq équivalences

| Lettre | Nom | Signification | Opération |
|--------|------|---------|-----------|
| **O** | Octave | Les notes situées dans des octaves différentes sont équivalentes | Ramener à la classe de hauteur (mod 12) |
| **P** | Permutation | L'ordre des notes n'a pas d'importance | Traiter comme un ensemble |
| **T** | Transposition | Même motif commençant sur une fondamentale différente | Rotation modulaire |
| **I** | Inversion | Image miroir autour d'un pivot | Inverser l'ordre des intervalles |
| **C** | Cardinalité | Nombre de classes de hauteur distinctes | POPCOUNT de l'entier |

(OPTIC, sans K, désigne les cinq équivalences définies par Callender, Quinn et Tymoczko, « Generalized Voice-Leading Spaces », *Science* 320, 2008. Le « -K » appartient à l'embedding OPTIC-K de Guitar Alchemist, pas à cet article.)

### Où chaque équivalence se situe dans le cadre

- **Équivalence O :** intégrée au modèle. En ramenant les notes aux classes de hauteur 0-11, l'information d'octave est écartée.
- **Équivalence P :** intégrée au modèle. Un entier de 12 bits est par construction un ensemble (indépendant de l'ordre).
- **Équivalence T :** calculée comme rotation (décalage circulaire) de l'entier.
- **Équivalence I :** calculée comme **inversion de l'ordre des bits** de l'entier de 12 bits. Inverser l'ordre des bits de la gamme S donne sa gamme inversée (puis on effectue une rotation pour replacer la fondamentale sur le bit 0).
- **Équivalence C :** calculée par POPCOUNT — le nombre de bits à 1.

### Les 224 classes de Forte

Sous l'équivalence combinée T et I (la taxonomie standard de Forte), les 4 096 gammes se réduisent à **224 classes distinctes**. Ces classes constituent le fondement de la théorie des ensembles musicaux du XXe siècle.

Chaque classe de Forte a une forme première canonique (le représentant lexicographiquement le plus petit après normalisation). Le livre de Forte de 1973, **« The Structure of Atonal Music »**, recense les 208 classes de 3 à 9 notes avec leurs vecteurs d'intervalles, leurs symétries et leurs relations Z ; les 16 classes restantes (0, 1, 2, 10, 11 et 12 notes) complètent les 224.

### L'espace vectoriel à 216 dimensions de GA

Guitar Alchemist représente les gammes comme des vecteurs de caractéristiques dans un espace à 216 dimensions. Les dimensions encodent :

- La cardinalité (1 dimension)
- Le vecteur d'intervalles (6 dimensions)
- La luminosité (1 dimension)
- Les positions modales (variable)
- Le contenu en accords (variable)
- Des métriques de jouabilité propres à la guitare (variable)
- Les appartenances aux classes d'équivalence OPTIC-K (variable)

Deux gammes proches dans cet espace à 216 dimensions partagent un caractère musical. L'espace est navigable : vous pouvez aller du majeur vers le lydien en marchant dans une direction précise ; vous pouvez trouver la gamme « sans nom » la plus proche d'une gamme nommée ; vous pouvez calculer des distances harmoniques entre des gammes quelconques.

L'entier de gamme est l'**index** dans cet espace vectoriel. À partir de l'entier S, GA calcule de façon déterministe le vecteur de caractéristiques complet à 216 dimensions.

### Ce que l'on y gagne

L'univers des gammes est :
- **Fini** (4 096 gammes)
- **Énumérable** (entiers de 0 à 4095)
- **Transformable** (opérations sur les bits pour les modes, inversions, compléments)
- **Calculable** (chaque propriété se déduit de l'entier)
- **Navigable** (distances et voisinages dans l'espace des caractéristiques)
- **Largement inexploré** (seules ~200 des ~1 500 gammes légitimes ont un nom)

La théorie musicale n'avait pas besoin d'être floue. La théorie des ensembles de classes de hauteur, combinée au calcul moderne, transforme les gammes de folklore en données.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Classe de hauteur** | L'identité d'une note indépendamment de l'octave (Do, Do#, Ré, ... Si) |
| **12-TET** | Tempérament égal à douze demi-tons — le système d'accord occidental standard |
| **Entier de gamme** | Un nombre de 12 bits dont chaque bit indique la présence ou l'absence d'une classe de hauteur |
| **Mode** | Une rotation d'une gamme, qui prend un degré autre que la fondamentale comme nouvelle fondamentale |
| **Forme première** | Le représentant canonique d'une famille de gammes sous une équivalence |
| **Nombre de Forte** | Une étiquette normalisée (par ex. 7-35) pour une classe d'ensembles de classes de hauteur |
| **Vecteur d'intervalles** | Un 6-uplet qui compte les occurrences de chaque classe d'intervalles dans une gamme |
| **Classe d'intervalles** | Un intervalle réduit modulo l'octave et le renversement : n et 12 − n demi-tons forment la même classe (1 et 11 sont tous deux de classe 1, 5 et 7 tous deux de classe 5), ce qui donne les classes 1 à 6 |
| **Luminosité** | La somme des classes de hauteur d'une gamme (indicateur de dièses/bémols) |
| **Symétrie (de rotation)** | Propriété d'une gamme qui se transforme en elle-même par rotation |
| **Chiralité** | L'asymétrie d'une gamme sous l'inversion |
| **Relation Z** | Deux gammes de même vecteur d'intervalles mais non liées par T ou I |
| **Critères de Zeitler** | Heuristiques pour filtrer les gammes mathématiques et ne garder que celles « musicalement réelles » |
| **POPCOUNT** | Le nombre de bits à 1 dans un nombre binaire (= cardinalité de la gamme) |
| **OPTIC-K** | Moyen mnémotechnique des relations d'équivalence en théorie des ensembles musicaux |

---

## Auto-évaluation

**1. Convertissez la gamme de Do dorien (Do Ré Mib Fa Sol La Sib) en son entier de classes de hauteur à l'aide de la convention de correspondance des bits.**
> Classes de hauteur : 0, 2, 3, 5, 7, 9, 10. Entier = 1 + 4 + 8 + 32 + 128 + 512 + 1024 = **1709**.

**2. Calculez le vecteur d'intervalles de la gamme par tons de Do (Do Ré Mi Fa# Sol# La#).**
> Les paires ne donnent que des intervalles de 2, 4 et 6 demi-tons. Décompte : classe 1 = 0, classe 2 = 6, classe 3 = 0, classe 4 = 6, classe 5 = 0, classe 6 = 3. Vecteur d'intervalles : **[0, 6, 0, 6, 0, 3]**.

**3. Quel est le nombre de Forte de la gamme majeure (collection diatonique), et combien de notes a-t-elle ?**
> Nombre de Forte **7-35**. Le premier chiffre (7) indique la cardinalité = 7 notes.

**4. Expliquez pourquoi les sept modes de la gamme majeure ne sont PAS sept gammes différentes sous l'équivalence par transposition.**
> Les sept modes contiennent les mêmes sept classes de hauteur, disposées selon le même motif cyclique d'intervalles (2-2-1-2-2-2-1). Chaque mode est une rotation des autres — ils partagent une même forme première. Commencer le motif sur un autre degré ne change pas la structure sous-jacente de la gamme, seulement le choix de la tonique.

**5. Appliquez le filtrage de Zeitler à la gamme de classes de hauteur {0, 1, 7}. Quels critères satisfait-elle ou enfreint-elle ?**
> Fondamentale présente (bit 0 à 1) : RÉUSSI. Écart maximal de 1 à 7 de 6 demi-tons : ÉCHEC (dépasse 4). Cardinalité = 3 notes : ÉCHEC (sous le minimum de 5). Aucun cluster de 4 demi-tons ou plus : RÉUSSI. Bilan : elle échoue au filtre de Zeitler en tant que gamme « légitime » (c'est un tricorde, pas une gamme).

**Critères de réussite :** convertir n'importe quelle gamme (donnée sous forme de classes de hauteur ou de noms de notes) vers et depuis sa représentation entière, calculer son vecteur d'intervalles à la main, identifier sa cardinalité de Forte, et expliquer quelles équivalences OPTIC-K sont intégrées au modèle entier et lesquelles demandent un calcul supplémentaire.

---

## Bases de recherche

- Le tempérament égal à 12 demi-tons comme standard d'accord occidental est documenté empiriquement dans la pratique de l'accord du piano et de l'orchestre depuis le XIXe siècle
- La théorie des ensembles de classes de hauteur et l'énumération des 4 096 gammes trouvent leur origine dans les travaux combinatoires de Milton Babbitt (années 1950) et ont été formalisées par Allen Forte dans *The Structure of Atonal Music* (1973)
- Les 224 classes d'ensembles sous l'équivalence T/I (toutes cardinalités, de 0 à 12 ; OEIS A000029 les compte comme les 224 bracelets binaires à 12 perles) incluent les 208 classes de 3 à 9 notes recensées dans Forte (1973), qui restent la taxonomie standard
- Les critères de gammes de Zeitler proviennent du projet de catalogage exhaustif de William Zeitler (*All The Scales*, 2011, et le site web qui l'accompagne), et représentent un filtre pratique sur l'univers
- La géométrie des gammes et les relations de voisinage sont explorées dans *A Geometry of Music* (2011) de Dmitri Tymoczko, qui formalise les distances de conduite des voix entre accords et gammes
- La représentation de GA dans un espace de caractéristiques à 216 dimensions est un choix d'implémentation de Guitar Alchemist, qui étend la théorie classique des ensembles de classes de hauteur avec des métadonnées d'exécution et de fonction harmonique
- Les relations d'équivalence OPTIC sont définies dans Clifton Callender, Ian Quinn et Dmitri Tymoczko, « Generalized Voice-Leading Spaces », *Science* 320 (2008) : 346–348 ; *Generalized Musical Intervals and Transformations* (1987) de David Lewin relève de la tradition transformationnelle, distincte
- Sources : Forte (1973) ; Tymoczko (2011) ; Callender, Quinn et Tymoczko (2008) ; Lewin (1987) ; Rahn, *Basic Atonal Theory* (1980) ; catalogue de gammes de Zeitler (2011)
- État de croyance : T(0.85) F(0.03) U(0.08) C(0.04)
