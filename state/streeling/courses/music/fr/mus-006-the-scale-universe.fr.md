---
module_id: mus-006-the-scale-universe
department: music
course: "Fondements de la théorie musicale"
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

## Objectifs

Après cette leçon, vous serez capable de :

- Représenter n'importe quelle gamme sous la forme d'un nombre binaire de 12 bits et le convertir en entier décimal
- Expliquer pourquoi il existe exactement 4 096 gammes mathématiquement possibles dans le tempérament égal à 12 sons
- Calculer les modes de n'importe quelle gamme au moyen de décalages circulaires à gauche (rotations de bits)
- Distinguer le décompte total (4 096) des décomptes obtenus sous diverses équivalences (formes premières, classes de Forte)
- Appliquer les critères de Zeitler pour filtrer l'univers et n'en retenir que les gammes « musicalement réelles »
- Calculer vecteurs d'intervalles, brillance et propriétés de symétrie à partir de l'entier d'une gamme
- Reporter n'importe quel entier de gamme sur les positions du manche de guitare
- Relier l'espace des gammes aux relations d'équivalence OPTIC-K employées en théorie des ensembles musicaux

---

## 1. L'alphabet chromatique

La musique occidentale emploie douze classes de hauteurs par octave. Une **classe de hauteurs** est une note indépendamment de l'octave où elle apparaît : tous les do d'un piano appartiennent à la même classe de hauteurs.

Les douze classes de hauteurs, numérotées de 0 à 11 :

| Classe de hauteurs | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|
| Nom de note | do | do♯/ré♭ | ré | ré♯/mi♭ | mi | fa | fa♯/sol♭ | sol | sol♯/la♭ | la | la♯/si♭ | si |

Voyez maintenant une gamme comme un **choix** : pour chacune des douze classes de hauteurs, soit elle est **dans** la gamme (1), soit elle est **hors** de la gamme (0). Cela nous donne un nombre binaire de 12 bits — douze décisions oui/non indépendantes.

**Combien de choix possibles ?** Deux options pour chacune des douze positions :

$$ 2^{12} = 4096 $$

Il existe exactement 4 096 gammes mathématiquement possibles dans le tempérament égal à 12 sons. Cela inclut la gamme vide (que des zéros), la gamme chromatique (que des uns), toutes les « gammes » d'une seule note, toutes les gammes traditionnelles et toutes les collections bizarres qui se trouvent entre les deux.

C'est l'**univers des gammes**. Sa taille est finie, connaissable et étonnamment petite — un nombre qu'un ordinateur énumère en quelques microsecondes.

---

## 2. Une gamme EST un nombre

Voici le recadrage décisif : **toute gamme est un entier compris entre 0 et 4095**.

### L'assignation des bits

On attribue à chaque classe de hauteurs une position binaire :

| Bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| Classe de hauteurs | do | do♯ | ré | ré♯ | mi | fa | fa♯ | sol | sol♯ | la | la♯ | si |
| Valeur de position | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

Pour convertir une gamme en entier, on marque chaque note par un 1 et on additionne les valeurs de position.

### Exemple : la gamme majeure

La **gamme de do majeur** contient les notes do, ré, mi, fa, sol, la, si — classes de hauteurs 0, 2, 4, 5, 7, 9, 11.

En binaire (lu du bit 11 jusqu'au bit 0) :

```
Bit :      11 10  9  8  7  6  5  4  3  2  1  0
Note :      si si♭ la la♭ sol sol♭ fa mi mi♭ ré ré♭ do
Dans la gamme : 1  0  1  0  1  0  1  1  0  1  0  1
```

En décimal :

$$ 1 + 4 + 16 + 32 + 128 + 512 + 2048 = 2741 $$

**do majeur = 2741.**

Toute gamme majeure a la même **structure intervallique** ; quelle que soit la fondamentale, c'est le motif (pas de 2-2-1-2-2-2-1 demi-tons) qui définit le mode majeur. L'entier 2741 en est la représentation enracinée sur do. Enraciné sur d'autres notes, le motif tourne.

### Exemple : la gamme pentatonique mineure

La gamme **pentatonique mineure de do** contient do, mi♭, fa, sol, si♭ — classes de hauteurs 0, 3, 5, 7, 10.

En binaire :

```
Bit :      11 10  9  8  7  6  5  4  3  2  1  0
Dans la gamme : 0  1  0  0  1  0  1  0  1  0  0  1
```

En décimal :

$$ 1 + 8 + 32 + 128 + 1024 = 1193 $$

**pentatonique mineure de do = 1193.**

### Pourquoi c'est important

Une fois admis qu'une gamme est un nombre, tout en découle :
- Vous pouvez **énumérer** toutes les gammes (compter de 0 à 4095)
- Vous pouvez **comparer** des gammes (comparaison d'entiers)
- Vous pouvez **transformer** des gammes (opérations sur les bits : décalage, ET, OU, OU exclusif, POPCOUNT)
- Vous pouvez **rechercher** des gammes (par vecteur d'intervalles, cardinalité ou symétrie précis)
- Vous pouvez **stocker** des gammes (12 bits au lieu d'une liste de notes)

Une gamme n'est pas une chose mystique. C'est un nombre.

### Exercice pratique

Convertissez les trois gammes suivantes en entiers à l'aide de l'assignation des bits :

1. **do mineur naturel** (do, ré, mi♭, fa, sol, la♭, si♭) — classes de hauteurs 0, 2, 3, 5, 7, 8, 10
2. **do pentatonique majeur** (do, ré, mi, sol, la) — classes de hauteurs 0, 2, 4, 7, 9
3. **do par tons** (do, ré, mi, fa♯, sol♯, la♯) — classes de hauteurs 0, 2, 4, 6, 8, 10

Calculez chacune en additionnant les valeurs de position (puissances de 2). Vérifiez vos réponses ci-dessous.

Réponses :
1. do mineur naturel = 1 + 4 + 8 + 32 + 128 + 256 + 1024 = **1453**
2. do pentatonique majeur = 1 + 4 + 16 + 128 + 512 = **661**
3. do par tons = 1 + 4 + 16 + 64 + 256 + 1024 = **1365**

---

## 3. Les modes comme rotations

Un **mode** est une gamme commencée sur un autre degré. Do dorien contient les mêmes notes que si♭ majeur, mais commence sur do. Dans la représentation entière, ce n'est ni une addition ni une multiplication : c'est une **rotation**.

### L'opération de décalage circulaire

Pour trouver le mode suivant d'une gamme :
1. Repérer le bit à 1 le plus bas (la fondamentale)
2. Le retirer et décaler le motif restant vers le bas
3. Reporter l'ancienne fondamentale au sommet

Plus précisément, la rotation modale est un **décalage circulaire à gauche** de la distance qui sépare la fondamentale de la note suivante de la gamme. Dans un système à 12 bits, « reporter » signifie que les bits qui sortent par la gauche réapparaissent à droite.

### Exemple : les modes de la gamme majeure

Le motif de la gamme majeure a pour intervalles 2-2-1-2-2-2-1 (sept notes). Ses sept modes sont engendrés par rotation sur chacun des sept degrés :

| Nom du mode | Degré de départ | Motif d'intervalles |
|-----------|----------------|------------------|
| Ionien (majeur) | 1 | 2-2-1-2-2-2-1 |
| Dorien | 2 | 2-1-2-2-2-1-2 |
| Phrygien | 3 | 1-2-2-2-1-2-2 |
| Lydien | 4 | 2-2-2-1-2-2-1 |
| Mixolydien | 5 | 2-2-1-2-2-1-2 |
| Éolien (mineur naturel) | 6 | 2-1-2-2-1-2-2 |
| Locrien | 7 | 1-2-2-1-2-2-2 |

Ce ne sont **pas sept gammes différentes.** Ce sont sept rotations du même motif sous-jacent. Quand vous jouez do dorien au piano, vous jouez les touches blanches en partant de ré.

### Calculer les rotations comme opérations binaires

En pseudocode, pour faire tourner de `n` positions vers la gauche un entier de gamme sur 12 bits :

```
rotation_gauche(gamme, n):
    decale = (gamme << n) & 0xFFF        # décalage à gauche, masqué sur 12 bits
    reporte = gamme >> (12 - n)          # bits qui sont sortis
    return decale | reporte              # combinaison
```

Appliquée à la gamme majeure (2741), une rotation du bon nombre de positions produit la représentation entière de chaque mode.

### Exercice pratique

Calculez les trois premiers modes de la **gamme mineure harmonique** (do ré mi♭ fa sol la♭ si — intervalles 2-1-2-2-1-3-1).

1. Écrivez la représentation binaire sur 12 bits de do mineur harmonique
2. Déterminez de combien de bits il faut tourner pour obtenir le 2e mode (locrien 6e naturelle)
3. Déterminez de combien de bits il faut tourner pour obtenir le 3e mode (ionien ♯5)

Indice : la valeur de rotation est égale au nombre de demi-tons entre l'ancienne et la nouvelle fondamentale.

Ébauche de réponse :
- do mineur harmonique = 2477 (binaire : 100110101101)
- Tourner à gauche de 2 demi-tons (ré est 2 demi-tons au-dessus de do) → 2e mode
- Tourner à gauche de 3 demi-tons (mi♭ est 3 demi-tons au-dessus de do) → 3e mode

Les sept modes de la mineure harmonique sont tous des rotations de l'entier 2477.

---

## 4. Combien sont réellement uniques ?

Nous sommes partis de **4 096** gammes. Mais beaucoup d'entre elles sont « les mêmes » sous diverses équivalences. Combien de structures sont réellement distinctes ?

### Formes premières — en ignorant la rotation

Deux gammes sont **modalement équivalentes** si l'une est une rotation de l'autre. La **forme première** d'une gamme en est le représentant canonique — par convention, la rotation de plus petite valeur entière (ou celle qui tasse les notes vers le début).

Sous l'équivalence modale :
- La famille de la gamme majeure à 7 notes a 7 rotations (7 modes) → 1 forme première
- La gamme par tons à 6 notes n'a qu'une seule rotation unique (elle se transforme en elle-même) → 1 forme première
- La gamme chromatique à 12 notes est sa propre forme première

**Décompte des formes premières :** sur les 4 096 gammes, environ **352** sont structurellement uniques par rotation. Le décompte exact dépend des conventions (faut-il inclure la gamme vide, les gammes d'une seule note, etc.).

### Classes de Forte — en ignorant la rotation ET l'inversion

Dans les années 1970, Allen Forte a formalisé une équivalence supplémentaire : traiter une gamme et son **inversion** (image en miroir) comme une même structure. L'inversion d'une gamme renverse son motif d'intervalles.

- La **gamme majeure** (2-2-1-2-2-2-1) s'inverse en **phrygien** (1-2-2-2-1-2-2) — or c'est justement un mode du majeur.
- Mais la plupart des gammes ont des inversions qui ne font PAS partie de la même famille modale.

Sous l'**équivalence T/I** (transposition + inversion), Forte a identifié **224 classes d'ensembles distinctes** pour les cardinalités de 3 à 9. En incluant toutes les cardinalités de 0 à 12, le décompte total est un peu supérieur.

Le **numéro de Forte** (par exemple « 7-35 » pour la gamme diatonique/majeure) est un système de nommage normalisé où :
- Le premier nombre est la cardinalité (le nombre de notes)
- Le second est le rang au sein de cette cardinalité (selon un ordre canonique)

### Le cas particulier de la gamme par tons

La gamme par tons (do ré mi fa♯ sol♯ la♯) a un motif d'intervalles 2-2-2-2-2-2. Chaque rotation produit une gamme identique : elle n'a **qu'un seul mode**.

Son entier : 1365 (binaire 010101010101).

Tournez-la d'un nombre pair de positions : vous retombez sur 1365. Tournez-la d'un nombre impair : vous obtenez l'autre gamme par tons (2730, binaire 101010101010).

Il n'existe donc que **deux gammes par tons** dans l'univers entier, et elles sont transposées l'une de l'autre d'un demi-ton. Sous l'équivalence de Forte, les deux appartiennent à la même classe d'ensembles.

### La hiérarchie des décomptes

| Équivalence | Décompte | Ce qui est identifié |
|-------------|-------|-----------------|
| Aucune (brut) | 4 096 | Tous les sous-ensembles des 12 classes de hauteurs |
| Transposition (T) | ~352 formes premières | Rotations d'un même motif |
| Transposition + inversion (T/I) | 224 classes de Forte | Ci-dessus, plus les images en miroir |
| T/I + complémentation | ~158 | Ci-dessus, plus les paires gamme+complément |

### Exercice pratique

Convainquez-vous que la gamme par tons est « modalement invariante » :

1. Écrivez do par tons en binaire sur 12 bits : 010101010101
2. Tournez à gauche de 2 bits : qu'obtenez-vous ?
3. Tournez à gauche de 1 bit : qu'obtenez-vous ?
4. Expliquez pourquoi une gamme à structure intervallique uniforme (tous les pas de même taille) a moins de modes uniques

Réponses :
1. 010101010101 = 1365
2. Rotation à gauche de 2 : toujours 010101010101 = 1365 (la même gamme)
3. Rotation à gauche de 1 : 101010101010 = 2730 (l'autre gamme par tons)
4. Une gamme à N notes a au plus N modes, mais si elle possède une symétrie de rotation (elle se transforme en elle-même par rotation de k demi-tons avec k < 12), elle en a moins. La gamme par tons a une période de symétrie de rotation de 12/6 = 2, si bien que toutes les rotations produisent l'un de deux états.

---

## 5. Qu'est-ce qui fait une « vraie gamme » ?

Sur les 4 096 possibilités mathématiques, la plupart ne sont pas utiles en musique. Une gamme comme `101100000001` (do, ré♭, mi♭, si) est une collection de notes, mais personne ne l'appellerait une gamme au sens pratique. Comment filtrer l'univers pour n'en garder que les gammes légitimes ?

### Les critères de Zeitler

William Zeitler, dans son travail de catalogage exhaustif, a proposé quatre critères pour qu'une gamme soit « réelle » :

1. **La fondamentale est présente** — le bit 0 doit être à 1. Une gamme doit contenir sa propre tonique. Cela élimine 2 048 gammes (la moitié de l'univers).

2. **Aucun écart supérieur à 4 demi-tons** — deux notes consécutives de la gamme ne peuvent pas être séparées par plus d'une tierce majeure. Un écart de 5 demi-tons ou plus crée un trou audible qui rompt la continuité scalaire.

3. **Entre 5 et 8 notes** — les gammes hors de cette plage sonnent soit trop clairsemées (pour être entendues comme des gammes), soit trop denses (pour se distinguer du chromatisme). Il s'agit d'une contrainte pragmatique, non mathématique.

4. **Aucun amas de plus de 3 demi-tons consécutifs** — quatre notes chromatiques d'affilée ou plus créent un amas chromatique qui perd son caractère scalaire.

L'application des quatre critères ramène les 4 096 gammes à environ **1 490 gammes « légitimes »**. C'est encore bien plus que le répertoire familier des gammes nommées.

### Pourquoi ces critères sont des lignes directrices, non des lois

Les critères de Zeitler sont des **heuristiques**, pas des définitions. Les contre-exemples abondent :

- La **gamme chromatique** a 12 demi-tons consécutifs (elle viole le critère 4) — c'est manifestement une vraie gamme
- Les **bourdons** d'une seule note violent le minimum de 5 notes — c'est manifestement une structure musicale réelle
- Les **gammes de blues** exploitent parfois habilement des écarts de 3 demi-tons (la pentatonique mineure présente un écart de si♭ à do)
- Les **gammes du gagaku**, les gammes microtonales et d'autres systèmes non occidentaux n'entrent pas du tout dans le tempérament égal à 12 sons

Ces critères sont **propres à une culture** : ils décrivent des gammes qui conviennent à la pratique tonale et modale européenne. C'est un filtre utile, pas une vérité universelle.

### Exercice pratique

Pour chacune des gammes suivantes, déterminez quels critères de Zeitler elle viole, le cas échéant :

1. **do majeur** (0, 2, 4, 5, 7, 9, 11)
2. **do chromatique** (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
3. **une gamme à trou** (0, 5, 11) — do, fa, si
4. **une gamme en amas** (0, 1, 2, 3, 4) — do, do♯, ré, ré♯, mi

Réponses :
1. do majeur : n'en viole aucun — elle satisfait tous les critères
2. do chromatique : viole le critère 3 (12 notes, au-delà du maximum de 8) et le critère 4 (12 demi-tons consécutifs)
3. Gamme à trou : viole le critère 2 (l'écart de fa à si fait 6 demi-tons) et le critère 3 (3 notes seulement)
4. Gamme en amas : viole le critère 4 (5 demi-tons consécutifs) et le critère 3 (5 notes seulement, à la limite)

---

## 6. Les propriétés de gamme que vous pouvez calculer

Dès lors qu'une gamme est un entier, toutes ses propriétés musicales deviennent calculables. Pas besoin d'écouter : vous pouvez analyser le nombre.

### Vecteur d'intervalles

Un **vecteur d'intervalles** compte combien de fois chaque classe d'intervalles apparaît dans la gamme. Il existe six classes d'intervalles (de 1 à 6 demi-tons ; le triton est son propre inverse, et les intervalles de 7 à 11 sont les compléments de ceux de 1 à 5).

Pour la **gamme de do majeur** (do ré mi fa sol la si) :

```
Classe d'intervalles : 1   2   3   4   5   6
Décompte :             2   5   4   3   6   1
```

Vecteur d'intervalles : `[2, 5, 4, 3, 6, 1]`

Le vecteur se calcule en examinant toutes les paires de notes de la gamme et en comptant la distance qui les sépare (ramenée à la plage 1-6).

**Pourquoi c'est important :** le vecteur d'intervalles encode le potentiel harmonique. Les gammes riches en tierces et en quintes (classes d'intervalles 3, 4, 5) sonnent consonantes et tonales. Les gammes chargées en classes 1 et 6 sonnent dissonantes et instables.

### Brillance

La **brillance** est la somme des classes de hauteurs (les positions binaires à 1). Une somme élevée signifie que les notes de la gamme sont plus hautes sur le cercle chromatique (plus de dièses) ; une somme basse signifie davantage de bémols.

- do majeur (0, 2, 4, 5, 7, 9, 11) : somme = 38
- do lydien (0, 2, 4, 6, 7, 9, 11) : somme = 39 — plus brillant d'une unité
- do phrygien (0, 1, 3, 5, 7, 8, 10) : somme = 34 — plus sombre

Le **spectre locrien-lydien** (du plus sombre au plus brillant des modes du majeur) correspond à des valeurs de brillance croissantes de façon monotone. C'est une propriété calculée — nul besoin d'oreille.

### Symétrie

Une gamme possède une **symétrie de rotation** si une rotation de k demi-tons produit la même gamme. L'ordre de symétrie d'une gamme vous dit combien de transpositions distinctes elle admet.

- **Gamme par tons :** symétrie tous les 2 demi-tons → seulement 2 transpositions distinctes
- **Gamme diminuée (octatonique) :** symétrie tous les 3 demi-tons → seulement 3 transpositions distinctes
- **Gamme augmentée :** symétrie tous les 4 demi-tons → seulement 4 transpositions distinctes
- **Gamme majeure :** aucune symétrie de rotation → les 12 transpositions sont distinctes

### Chiralité

Une gamme est **chirale** si son inversion (image en miroir autour de la classe de hauteurs 0) n'est identique à AUCUNE de ses rotations. La plupart des gammes sont chirales. Font exception la gamme majeure (dont l'inversion est le mode phrygien, qui EST une rotation) et les gammes symétriques.

### Relation Z

Deux gammes sont **en relation Z** si elles ont le même vecteur d'intervalles sans être liées par transposition ni par inversion. Elles sonnent harmoniquement de façon proche mais sont structurellement distinctes. Les paires en relation Z sont rares et musicalement fascinantes.

La paire Z la plus célèbre : la relation Z du **tétracorde tous-intervalles** entre `{0,1,4,6}` et `{0,1,3,7}`, tous deux de vecteur d'intervalles `[1,1,1,1,1,1]`.

### Exercice pratique

Calculez le vecteur d'intervalles de la **gamme pentatonique mineure de do** (do mi♭ fa sol si♭ = classes de hauteurs 0, 3, 5, 7, 10).

Étape 1 : lister toutes les paires et leurs distances.
Étape 2 : ramener les distances à des classes d'intervalles (les distances de 7 à 11 deviennent 12 − distance : par exemple, 8 demi-tons → classe 4).
Étape 3 : compter les occurrences de chaque classe.

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

Décompte des classes d'intervalles :
- Classe 1 : 0
- Classe 2 : 3
- Classe 3 : 2
- Classe 4 : 1
- Classe 5 : 4
- Classe 6 : 0

Vecteur d'intervalles : **[0, 3, 2, 1, 4, 0]**

Remarque : forte présence de la classe 5 (quartes et quintes justes), absence de la classe 6 (triton) et de la classe 1 (demi-ton) — voilà pourquoi les gammes pentatoniques sonnent stables et « jamais fausses ».

---

## 7. Explorer les gammes sans nom à la guitare

Les manuels de théorie musicale couvrent peut-être **200 gammes nommées** : majeure, mineure, modes, pentatoniques, mineures harmonique et mélodique et leurs modes, diminuée, par tons, blues, gammes bebop, une poignée de gammes « exotiques » (hongroise, byzantine, etc.) et les modes de Messiaen.

Il reste donc **environ 3 800 gammes sans nom** qui satisfont aux critères de base de Zeitler. La très grande majorité de l'univers des gammes est un territoire inexploré.

### Comment explorer

1. **Choisir un nombre** entre 1 et 4095 (ou utiliser un générateur aléatoire)
2. **Décoder les bits** pour trouver quelles classes de hauteurs sont dans la gamme
3. **Vérifier les critères de Zeitler** — cette gamme est-elle « raisonnable » ?
4. **La jouer** sur votre instrument et écouter
5. **Noter le vecteur d'intervalles** et le comparer à celui de gammes que vous connaissez

### Formule de report sur le manche

Pour jouer un entier de gamme à la guitare, il faut reporter les classes de hauteurs sur les positions de frettes de chaque corde.

Étant donné :
- L'entier de gamme S
- Les classes de hauteurs des cordes à vide en accordage standard : mi(4), la(9), ré(2), sol(7), si(11), mi(4)
- Pour chaque corde, calculer quelles frettes (0-12) contiennent une note de la gamme

**Formule :** pour chaque frette f (de 0 à 12) sur une corde dont la classe de hauteurs à vide est p :

```
classe_de_hauteurs_a_la_frette = (p + f) mod 12
est_dans_la_gamme = (S >> classe_de_hauteurs_a_la_frette) & 1
```

Si le résultat vaut 1, marquez cette frette. Répétez pour les six cordes.

### Exemple : une gamme au hasard

Choisissons l'entier de gamme **1749**. Décodage :

```
1749 en binaire : 011011010101
Classes de hauteurs (bits 0 à 11) : 0, 2, 4, 6, 7, 9, 10
Notes à partir de do :              do, ré, mi, fa♯, sol, la, si♭
```

Cette gamme a 7 notes, contient do (la fondamentale est présente), son écart maximal est de 2 demi-tons, elle n'a pas d'amas long — elle satisfait aux critères de Zeitler.

Motif d'intervalles : 2-2-2-1-2-1-2 (somme égale à 12).

**C'est le mixolydien ♯11** (ou lydien dominant, le 4e mode de la mineure mélodique) — une gamme nommée ! Vous venez de la redécouvrir en choisissant un nombre.

Essayez un nombre moins balisé : **2391**. Décodage :

```
2391 en binaire : 100101010111
Classes de hauteurs : 0, 1, 2, 4, 6, 8, 11
Notes à partir de do : do, do♯, ré, mi, fa♯, sol♯, si
```

Celle-ci satisfait à Zeitler (fondamentale présente, écarts réduits, 7 notes, amas courts) mais ne correspond à aucune gamme couramment nommée. Jouez-la à la guitare. Écoutez. Donnez-lui un nom.

### Le protocole d'exploration

1. Générer 5 à 10 nombres de gamme aléatoires qui satisfont aux critères de Zeitler
2. Jouer chacun pendant 30 secondes en écoutant son caractère émotionnel
3. Noter vos préférés
4. Construire des mélodies simples exploitant la saveur intervallique propre à chaque gamme
5. Comparer aux gammes nommées de vecteurs d'intervalles voisins

C'est ainsi que se découvre une musique nouvelle. L'univers est là ; le report est mécanique ; le jugement musical vous appartient.

### Exercice pratique

Prenez l'entier de gamme **1709** (à la sonorité hongroise).

1. Convertissez-le en binaire et identifiez les classes de hauteurs
2. Écrivez la gamme en partant de do
3. Calculez le motif d'intervalles (les pas entre notes consécutives)
4. Reportez la gamme sur les deux cordes aiguës d'une guitare en accordage standard (1re corde = mi, 2e corde = si) pour les frettes 0 à 12

Indice : 1709 = 1024 + 512 + 128 + 32 + 8 + 4 + 1 → bits 0, 2, 3, 5, 7, 9, 10.

---

## 8. Lien avec OPTIC-K

La théorie des ensembles musicaux emploie une taxonomie de **relations d'équivalence** pour décrire en quel sens deux collections de notes peuvent être tenues pour « les mêmes ». Le moyen mnémotechnique OPTIC-K les rassemble toutes. Le cadre de l'entier de gamme rend ces équivalences calculables.

### Les six équivalences

| Lettre | Nom | Signification | Opération |
|--------|------|---------|-----------|
| **O** | Octave | Les notes d'octaves différentes sont équivalentes | Réduction en classe de hauteurs (mod 12) |
| **P** | Permutation | L'ordre des notes est indifférent | Traitement comme ensemble |
| **T** | Transposition | Même motif à partir d'une autre fondamentale | Rotation modulaire |
| **I** | Inversion | Image en miroir autour d'un pivot | Renversement de l'ordre des intervalles |
| **C** | Cardinalité | Nombre de classes de hauteurs distinctes | POPCOUNT de l'entier |
| **K** | (Forme alternative) | — | Calculée à partir d'un K-net ou d'une structure analogue |

(Le « K » d'OPTIC-K renvoie, selon les sources, soit à l'équivalence de cardinalité, soit à une structure particulière de Kuusisto/Lewin.)

### Où vit chaque équivalence dans le cadre

- **Équivalence O :** intégrée au modèle. En réduisant les notes à des classes de hauteurs de 0 à 11, l'information d'octave est écartée.
- **Équivalence P :** intégrée au modèle. Un entier de 12 bits est un ensemble (indépendant de l'ordre) par construction.
- **Équivalence T :** calculée comme rotation (décalage circulaire) de l'entier.
- **Équivalence I :** calculée comme **renversement des bits** de l'entier de 12 bits. Renverser les bits d'une gamme S donne sa gamme inversée (il reste à tourner pour ramener la fondamentale au bit 0).
- **Équivalence C :** calculée par POPCOUNT — le nombre de bits à 1.

### Les 224 classes de Forte

Sous l'équivalence combinée T et I (la taxonomie de Forte standard), les 4 096 gammes se réduisent à **224 classes distinctes**. Ces classes constituent le fondement de la théorie des ensembles musicaux du XXe siècle.

Chaque classe de Forte a une forme première canonique (le plus petit représentant dans l'ordre lexicographique après normalisation). L'ouvrage de Forte paru en 1973, **« The Structure of Atonal Music »**, répertorie les 224 classes avec leurs vecteurs d'intervalles, leurs symétries et leurs relations Z.

### L'espace vectoriel à 216 dimensions de GA

Guitar Alchemist représente les gammes comme des vecteurs de caractéristiques dans un espace à 216 dimensions. Ces dimensions encodent :

- La cardinalité (1 dimension)
- Le vecteur d'intervalles (6 dimensions)
- La brillance (1 dimension)
- Les positions modales (nombre variable)
- Le contenu en accords (nombre variable)
- Les mesures de jouabilité propres à la guitare (nombre variable)
- Les appartenances aux classes d'équivalence OPTIC-K (nombre variable)

Deux gammes proches dans cet espace à 216 dimensions partagent un même caractère musical. L'espace est navigable : vous pouvez aller du majeur vers le lydien en marchant dans une direction précise ; vous pouvez trouver la gamme « sans nom » la plus proche d'une gamme nommée ; vous pouvez calculer les distances harmoniques entre gammes quelconques.

L'entier de gamme est l'**index** de cet espace vectoriel. Étant donné l'entier S, GA calcule de manière déterministe le vecteur de caractéristiques complet à 216 dimensions.

### Le bénéfice

L'univers des gammes est :
- **Fini** (4 096 gammes)
- **Énumérable** (les entiers de 0 à 4095)
- **Transformable** (opérations binaires pour les modes, les inversions, les compléments)
- **Calculable** (toute propriété se déduit de l'entier)
- **Navigable** (distances et voisinages dans l'espace de caractéristiques)
- **Largement inexploré** (seules ~200 des ~1 500 gammes légitimes portent un nom)

La théorie musicale n'avait pas à rester floue. La théorie des ensembles de classes de hauteurs, alliée au calcul moderne, fait passer les gammes du folklore aux données.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Classe de hauteurs** | L'identité d'une note indépendamment de l'octave (do, do♯, ré, … si) |
| **Tempérament égal à 12 sons** | Le tempérament égal à douze degrés — le système d'accord occidental standard |
| **Entier de gamme** | Un nombre de 12 bits où chaque bit indique la présence ou l'absence d'une classe de hauteurs |
| **Mode** | Une rotation d'une gamme, un degré autre que la fondamentale devenant la nouvelle fondamentale |
| **Forme première** | Le représentant canonique d'une famille de gammes sous une équivalence |
| **Numéro de Forte** | Une étiquette normalisée (par exemple 7-35) pour une classe d'ensembles de classes de hauteurs |
| **Vecteur d'intervalles** | Un sextuplet comptant les occurrences de chaque classe d'intervalles dans une gamme |
| **Classe d'intervalles** | Un intervalle réduit modulo l'octave ET l'inversion : les intervalles de 1 à 6 et leurs compléments de 11 à 6 se ramènent aux classes 1 à 6 |
| **Brillance** | La somme des classes de hauteurs d'une gamme (indicateur du caractère dièse/bémol) |
| **Symétrie (de rotation)** | La propriété d'une gamme de se transformer en elle-même par rotation |
| **Chiralité** | L'asymétrie d'une gamme sous l'inversion |
| **Relation Z** | Deux gammes de même vecteur d'intervalles non liées par T ni par I |
| **Critères de Zeitler** | Heuristiques filtrant les gammes mathématiques pour n'en retenir que les « musicalement réelles » |
| **POPCOUNT** | Le nombre de bits à 1 d'un nombre binaire (= la cardinalité de la gamme) |
| **OPTIC-K** | Moyen mnémotechnique désignant les relations d'équivalence en théorie des ensembles musicaux |

---

## Auto-évaluation

**1. Convertissez la gamme de do dorien (do ré mi♭ fa sol la si♭) en son entier de classes de hauteurs selon la convention d'assignation des bits.**
> Classes de hauteurs : 0, 2, 3, 5, 7, 9, 10. Entier = 1 + 4 + 8 + 32 + 128 + 512 + 1024 = **1709**.

**2. Calculez le vecteur d'intervalles de la gamme par tons de do (do ré mi fa♯ sol♯ la♯).**
> Les paires ne donnent que des intervalles de 2, 4 et 6 demi-tons. Décomptes : classe 1 = 0, classe 2 = 6, classe 3 = 0, classe 4 = 6, classe 5 = 0, classe 6 = 3. Vecteur d'intervalles : **[0, 6, 0, 6, 0, 3]**.

**3. Quel est le numéro de Forte de la gamme majeure (collection diatonique), et combien de notes comporte-t-elle ?**
> Numéro de Forte **7-35**. Le premier chiffre (7) indique une cardinalité de 7 notes.

**4. Expliquez pourquoi les sept modes de la gamme majeure ne sont PAS sept gammes différentes sous l'équivalence de transposition.**
> Les sept modes contiennent les mêmes sept classes de hauteurs disposées selon le même motif cyclique d'intervalles (2-2-1-2-2-2-1). Chaque mode est une rotation des autres : ils partagent une seule forme première. Commencer le motif sur un autre degré ne change pas la structure sous-jacente de la gamme, seulement le choix de la tonique.

**5. Appliquez le filtrage de Zeitler à la gamme de classes de hauteurs {0, 1, 7}. Quels critères satisfait-elle ou viole-t-elle ?**
> Fondamentale présente (bit 0 à 1) : SATISFAIT. Écart maximal de 1 à 7 : 6 demi-tons : ÉCHEC (au-delà de 4). Cardinalité = 3 notes : ÉCHEC (sous le minimum de 5). Aucun amas de 4 demi-tons ou plus : SATISFAIT. Bilan : elle échoue au test de Zeitler en tant que gamme « légitime » (c'est un trichorde, pas une gamme).

**Critères de réussite :** convertir n'importe quelle gamme (donnée en classes de hauteurs ou en noms de notes) vers et depuis sa représentation entière, calculer son vecteur d'intervalles à la main, identifier sa cardinalité de Forte, et expliquer quelles équivalences OPTIC-K sont intégrées au modèle entier et lesquelles exigent un calcul supplémentaire.

---

## Bases de la recherche

- Le tempérament égal à 12 sons comme standard d'accord occidental est empiriquement documenté dans l'accord des pianos et la pratique orchestrale depuis le XIXe siècle
- La théorie des ensembles de classes de hauteurs et l'énumération des 4 096 gammes prennent leur origine dans les travaux combinatoires de Milton Babbitt (années 1950) et ont été formalisées par Allen Forte dans *The Structure of Atonal Music* (1973)
- Les 224 classes d'ensembles sous l'équivalence T/I sont énumérées et répertoriées dans Forte (1973) et demeurent la taxonomie de référence
- Les critères de gamme de Zeitler proviennent du projet de catalogage exhaustif de William Zeitler (*All The Scales*, 2011, et le site compagnon), et constituent un filtre pratique sur l'univers
- La géométrie des gammes et les relations de voisinage sont explorées dans *A Geometry of Music* de Dmitri Tymoczko (2011), qui formalise les distances de conduite des voix entre accords et gammes
- La représentation dans un espace de caractéristiques à 216 dimensions est un choix d'implémentation de Guitar Alchemist, qui étend la théorie classique des ensembles de classes de hauteurs par des métadonnées de performance et de fonction harmonique
- Les relations d'équivalence OPTIC-K remontent à *Generalized Musical Intervals and Transformations* de David Lewin (1987) et à sa systématisation ultérieure dans l'enseignement de la théorie musicale
- Sources : Forte (1973) ; Tymoczko (2011) ; Lewin (1987) ; Rahn, *Basic Atonal Theory* (1980) ; catalogue de gammes de Zeitler (2011)
- État de croyance : T(0.85) F(0.03) U(0.08) C(0.04)
