---
module_id: mus-002-beyond-tonality
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

# Au-delà de la tonalité : la théorie post-tonale pour guitaristes

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Expliquer la dissolution historique de la tonalité classique et l'apparition de l'atonalité
- Traduire des hauteurs en notation entière de classes de hauteurs et calculer formes normale et première
- Construire des vecteurs d'intervalles et identifier les classes d'ensembles par leur numéro de Forte
- Dériver les quatre formes d'une série dodécaphonique et comprendre la matrice 12 × 12
- Analyser la musique atonale libre par la centricité de hauteur, les cellules motiviques et la distribution registrale
- Appliquer la pensée post-tonale au répertoire de guitare moderne, ainsi qu'à votre composition et à votre improvisation
- Reconnaître comment la théorie des ensembles fait le pont avec l'analyse des voicings de jazz

---

## 1. La fin de la pratique classique

Pendant environ 300 ans, de Bach à Brahms, la musique savante occidentale a fonctionné dans un système commun appelé **tonalité de la pratique classique**. Ce système avait une grammaire claire : un centre tonique, une harmonie fonctionnelle (tonique — sous-dominante — dominante) et une organisation mélodique autour des gammes diatoniques. Chaque accord avait un rôle ; chaque note avait une destination.

À la fin du XIXe siècle, les compositeurs ont étiré cette grammaire jusqu'à la rompre. L'opéra *Tristan et Isolde* de Wagner (1859) s'ouvre sur un accord — le fameux « accord de Tristan » (fa, si, ré♯, sol♯) — qui refuse toute résolution traditionnelle. Des heures durant, Wagner diffère la résolution attendue sur la tonique et maintient l'auditeur suspendu dans une ambiguïté chromatique. L'opéra finit par résoudre, mais le message était clair : la fonction tonale pouvait être retardée, affaiblie, puis dissoute.

Debussy, Mahler, Strauss et Scriabine ont poursuivi cette expansion chromatique. Les accords se sont chargés de tant de notes étrangères, d'extensions altérées et de mouvements parallèles que le squelette tonal a disparu. Au début des années 1900, la question devenait inévitable : si les accords n'ont plus à se résoudre, et si les tonalités n'engagent plus à rien, que reste-t-il ?

**L'émancipation de la dissonance selon Schoenberg :**

Arnold Schoenberg a répondu par une affirmation radicale, en 1908 : **la dissonance n'a pas besoin de se résoudre**. Dans la théorie traditionnelle, la consonance était « naturelle » et la dissonance un écart qu'il fallait corriger. Schoenberg soutenait qu'il s'agissait d'une convention historique et non d'une loi acoustique. Dissonance et consonance ne sont pas des contraires : ce sont des points sur un continuum, et les compositeurs devraient être libres d'employer n'importe quelle sonorité comme événement stable.

Cette émancipation de la dissonance a rompu la dernière contrainte de la tonalité. Les *Trois pièces pour piano, op. 11* de Schoenberg (1909) sont souvent citées comme la première œuvre « atonale ». Pas d'armure. Pas de résolution sur une tonique. Des hauteurs organisées par une logique motivique et registrale plutôt que par l'harmonie fonctionnelle.

**Deux voies : atonalité libre et sérialisme :**

Après l'émancipation, les compositeurs ont divergé selon deux voies :

- **L'atonalité libre :** intuitive, motivique, non systématisée. Les hauteurs sont choisies à l'oreille et par logique structurelle. Schoenberg (1908-1920), Berg, le premier Webern, Varèse, Ives. L'oreille du compositeur est la seule autorité.
- **Le sérialisme (technique dodécaphonique) :** une méthode systématique, mise au point par Schoenberg en 1921, pour organiser le matériau atonal. Chaque composition repose sur une série ordonnée des 12 classes de hauteurs, manipulée par des opérations précises. Le système a remplacé la grammaire tonale par une nouvelle.

Les deux voies partagent le même fondement : les 12 classes de hauteurs du tempérament égal sont traitées comme un ensemble démocratique, aucune note n'étant privilégiée. C'est le point de départ de la théorie post-tonale.

---

## 2. La notation entière des classes de hauteurs

La théorie post-tonale a besoin d'une notation qui traite les 12 classes de hauteurs comme équivalentes et abstraites. Les noms de notes traditionnels (do, ré, mi…) sont commodes, mais chargés d'héritage tonal : les orthographes enharmoniques (do♯ contre ré♭) suggèrent des significations tonales différentes, sans pertinence en analyse post-tonale.

La solution : la **notation entière**. On attribue un entier à chaque classe de hauteurs :

| Hauteur | Entier |
|-------|---------|
| do     | 0       |
| do♯/ré♭ | 1       |
| ré     | 2       |
| ré♯/mi♭ | 3       |
| mi     | 4       |
| fa     | 5       |
| fa♯/sol♭ | 6       |
| sol     | 7       |
| sol♯/la♭ | 8       |
| la     | 9       |
| la♯/si♭ | 10 (t)  |
| si     | 11 (e)  |

**Équivalence d'octave :** dans l'espace des classes de hauteurs, tous les do sont « le même » : il n'y a pas de do central opposé à un do grave. L'entier 0 représente la classe de tous les do, à toutes les octaves. Un ensemble de hauteurs devient un ensemble d'entiers modulo 12.

**Équivalence enharmonique :** do♯ et ré♭ sont la même classe de hauteurs (1). L'analyse post-tonale abandonne la distinction tonale, faute de contexte tonal pour la justifier.

**Forme normale :**

Étant donné un ensemble de hauteurs, la **forme normale** en est l'ordonnancement le plus compact. Pour la trouver :

1. Ranger les classes de hauteurs par ordre croissant autour du cercle chromatique.
2. Considérer chaque rotation de l'ensemble.
3. Choisir la rotation dont l'étendue, du premier au dernier élément, est la plus petite.
4. En cas d'égalité, choisir celle qui est la plus tassée vers la gauche (plus petit deuxième élément, puis troisième, etc.).

**Exemple :** l'ensemble {mi, sol♯, do} = {4, 8, 0}. Rotations (avec leur étendue du premier au dernier autour du cercle) :
- 0, 4, 8 : étendue = 8
- 4, 8, 0 : étendue = 8 (car 0 vaut « 0 + 12 = 12 », soit 12 − 4 = 8)
- 8, 0, 4 : étendue = 8

Toutes les rotations sont symétriques : c'est un accord augmenté. Par convention, on retient {0, 4, 8}.

**Forme première :**

La **forme première** est la représentation la plus abstraite d'une classe d'ensembles : elle efface à la fois les distinctions de transposition ET d'inversion. Pour la trouver :

1. Calculer la forme normale.
2. Calculer la forme normale de l'inversion (inverser l'ensemble autour de 0 en prenant l'opposé de chaque élément modulo 12, puis normaliser).
3. Retenir celle des deux qui est la plus tassée vers la gauche.
4. Transposer pour que le premier élément soit 0.

Les formes premières s'écrivent entre crochets : [0,3,7] pour l'accord mineur, [0,4,7] pour l'accord majeur.

**Un instant : les accords majeur et mineur sont-ils des classes d'ensembles différentes ?** Oui, mais leurs formes premières sont liées par inversion : [0,3,7] (mineur) s'inverse en [0,4,7] (majeur). Dans la classification de Forte, les deux appartiennent à la classe d'ensembles **3-11**, puisque le système considère comme une seule classe les ensembles équivalents par inversion. En pratique, [0,3,7] est la forme première canonique de la classe 3-11.

### Exercice pratique

Les cordes à vide d'une guitare en accordage standard sont mi, la, ré, sol, si, mi. En entiers de classes de hauteurs :
- mi = 4
- la = 9
- ré = 2
- sol = 7
- si = 11

En traitant les cordes à vide comme un ensemble (en ignorant le doublement à l'octave du mi) : {2, 4, 7, 9, 11}.

Votre tâche :
1. Ranger ces éléments par ordre croissant.
2. Déterminer la forme normale.
3. Calculer la forme première.

**Corrigé détaillé :**
- Ordre croissant : {2, 4, 7, 9, 11}
- Rotations et étendues :
  - (2, 4, 7, 9, 11) : étendue = 11 − 2 = 9
  - (4, 7, 9, 11, 2+12=14) : étendue = 14 − 4 = 10
  - (7, 9, 11, 14, 16) : étendue = 9
  - (9, 11, 14, 16, 19) : étendue = 10
  - (11, 14, 16, 19, 21) : étendue = 10
- Rotations à égalité : (2,4,7,9,11) et (7,9,11,2,4). On compare les deuxièmes éléments : 4 contre 9. On retient 4. Forme normale : {2, 4, 7, 9, 11}.
- Transposition pour commencer à 0 : retrancher 2 à chaque élément → {0, 2, 5, 7, 9}.
- Vérification de l'inversion : inverser {0,2,5,7,9} → {0,−2,−5,−7,−9} modulo 12 = {0, 10, 7, 5, 3}. Réordonner : {0, 3, 5, 7, 10}. Est-ce plus tassé vers la gauche que {0,2,5,7,9} ? Comparons les deuxièmes éléments, 2 contre 3 : {0,2,5,7,9} l'emporte (2 < 3).
- **Forme première : [0,2,5,7,9]** — c'est la classe d'ensembles 5-35, le **sous-ensemble pentatonique/diatonique** (la gamme pentatonique anhémitonique). Les cordes à vide de la guitare forment une classe d'ensembles pentatonique.

---

## 3. Vecteurs d'intervalles et classes d'ensembles

Au-delà du contenu en hauteurs, l'analyse post-tonale s'intéresse au **contenu intervallique** : quels intervalles sont présents dans un ensemble, et combien de chaque. C'est ce que capte le **vecteur d'intervalles**.

**Classe d'intervalles (ci) :**

En théorie post-tonale, les intervalles sont classés de 0 à 6 (il n'existe que 7 classes d'intervalles, celles-ci étant symétriques autour du triton) :

| ci | Demi-tons | Exemple |
|----|-----------|---------|
| 0  | unisson/octave | do-do |
| 1  | seconde mineure / septième majeure | do-ré♭ / do-si |
| 2  | seconde majeure / septième mineure | do-ré / do-si♭ |
| 3  | tierce mineure / sixte majeure | do-mi♭ / do-la |
| 4  | tierce majeure / sixte mineure | do-mi / do-la♭ |
| 5  | quarte juste / quinte juste | do-fa / do-sol |
| 6  | triton | do-fa♯ |

Une seconde mineure (1 demi-ton) et une septième majeure (11 demi-tons) appartiennent à la même classe d'intervalles, parce qu'elles sont l'inversion l'une de l'autre.

**Construire le vecteur d'intervalles :**

Le vecteur d'intervalles est une liste de 6 éléments comptant les occurrences de chaque classe d'intervalles (ci1 à ci6) entre toutes les paires de notes d'un ensemble.

**Exemple — l'accord parfait de do majeur {0, 4, 7} :**
- Paires : (0,4), (0,7), (4,7)
- Intervalles : 4−0=4 (ci4), 7−0=7 (ci5), 7−4=3 (ci3)
- Décompte : ci1=0, ci2=0, ci3=1, ci4=1, ci5=1, ci6=0
- **Vecteur d'intervalles : [001110]**

Remarquez que l'accord majeur et l'accord mineur partagent le même vecteur [001110], parce qu'ils sont liés par inversion. C'est pourquoi ils appartiennent à la même classe d'ensembles : **3-11**.

**Numéros de Forte :**

Allen Forte (1973) a catalogué toutes les classes d'ensembles de 3 à 9 notes et a attribué un numéro à chacune. Le format est **cardinalité-rang** :

- **3-11 :** la 11e classe d'ensembles de cardinalité 3 — l'accord parfait majeur/mineur.
- **3-12 :** l'accord augmenté [0,4,8], vecteur d'intervalles [000300].
- **4-20 :** l'accord de septième majeure [0,1,5,8], vecteur d'intervalles [101220].
- **3-1 :** le trichorde chromatique [0,1,2], vecteur d'intervalles [210000].
- **6-Z28 / 6-Z49 :** hexacordes en relation Z (voir ci-dessous).

Les rangs reflètent un ordre choisi par Forte d'après le contenu intervallique, allant grossièrement du plus compact (rangs les plus bas) au plus dispersé.

**Relations Z :**

Certaines classes d'ensembles distinctes partagent le même vecteur d'intervalles, alors que leurs contenus en hauteurs diffèrent et qu'elles ne sont liées ni par transposition ni par inversion. On les dit **en relation Z**, et Forte les a marquées du préfixe Z. L'exemple le plus célèbre : les classes 4-Z15 et 4-Z29 ont toutes deux le vecteur [111111] (le « tétracorde tous-intervalles »), tout en étant réellement différentes. Les relations Z ont fasciné Elliott Carter et Milton Babbitt, parce qu'elles révèlent une symétrie profonde dans l'espace des intervalles.

### Exercice pratique

Calculez le vecteur d'intervalles de **Misus4** à la guitare. Misus4 se compose de mi, la, si, soit les classes de hauteurs {4, 9, 11}.

**Corrigé détaillé :**
- Paires et intervalles :
  - (4, 9) : 9 − 4 = 5 → ci5
  - (4, 11) : 11 − 4 = 7 → ci5 (car ci = min(7, 12−7) = 5)
  - (9, 11) : 11 − 9 = 2 → ci2
- Décompte : ci1=0, ci2=1, ci3=0, ci4=0, ci5=2, ci6=0
- **Vecteur d'intervalles : [010020]**

Cette classe d'ensembles contient une seconde majeure et deux quartes/quintes justes. Sa forme première est [0,2,7], classe d'ensembles **3-9**. C'est le trichorde quartal, une sonorité centrale dans les voicings de jazz (l'accompagnement de la main gauche de McCoy Tyner, par exemple) et dans l'écriture orchestrale du XXe siècle (Copland, Hindemith).

---

## 4. Séries dodécaphoniques et opérations sérielles

La méthode dodécaphonique de Schoenberg (1921) organise le matériau atonal au moyen d'une **série ordonnée** : une suite précise contenant les 12 classes de hauteurs, chacune apparaissant exactement une fois. La série est le code génétique de l'œuvre ; toute mélodie, toute harmonie et tout contrepoint en dérivent.

**Les quatre formes de la série :**

À partir d'une **série originale (P0)**, l'ordre de départ, trois transformations engendrent trois formes apparentées :

1. **Originale (P) :** la série de départ.
2. **Rétrograde (R) :** la série jouée à l'envers (dernière note en premier).
3. **Inversion (I) :** chaque intervalle de la série d'origine change de direction. Si P monte d'une tierce mineure, I descend d'une tierce mineure.
4. **Rétrograde de l'inversion (RI) :** l'inversion jouée à l'envers.

Chaque forme peut être **transposée** sur n'importe laquelle des 12 classes de hauteurs, ce qui donne **48 formes au total** (4 opérations × 12 transpositions).

**Exemple — une série simple :**

Soit P0 = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10] (série inventée pour l'exemple).

- **R0 :** inverser l'ordre de P0 → [10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 1, 0]
- **I0 :** inversion autour de 0. Pour chaque élément x de P0, calculer (0 − x) modulo 12 :
  - P0 : [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10]
  - I0 : [0, 11, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
- **RI0 :** inverser l'ordre de I0 → [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 11, 0]

**Transposition :** pour créer P3 (forme originale commençant sur la classe de hauteurs 3), ajouter 3 à chaque élément de P0 (modulo 12) : [3, 4, 6, 5, 8, 7, 10, 9, 0, 11, 2, 1].

**La matrice 12 × 12 :**

La matrice dodécaphonique affiche de façon compacte les 48 formes de la série :

- **Les lignes** (de gauche à droite) sont les 12 transpositions de P, notées P0 à P11 d'après leur première classe de hauteurs.
- **Les lignes lues de droite à gauche** sont les rétrogrades (R0 à R11).
- **Les colonnes** (de haut en bas) sont les 12 transpositions de I, notées d'après leur première classe de hauteurs.
- **Les colonnes lues de bas en haut** sont les rétrogrades de l'inversion.

Pour construire la matrice :
1. Écrire P0 sur la ligne du haut.
2. Écrire I0 dans la colonne de gauche (l'inversion de P0, commençant sur la même première note).
3. Chaque ligne suivante est P0 transposée pour que sa première note corresponde à celle de la colonne de gauche.

**Combinatorialité :**

Certaines séries ont une propriété particulière, la **combinatorialité** : en scindant la série en deux hexacordes (les 6 premières notes et les 6 dernières), une transposition donnée de I produit des hexacordes qui, joints à ceux de P, forment deux agrégats complets (les 12 classes de hauteurs dans chaque moitié). Schoenberg a largement exploité la combinatorialité, parce qu'elle permet d'énoncer P et I simultanément sans répétition de classe de hauteurs : une sorte de contrepoint dodécaphonique qui préserve l'idéal atonal de non-privilège.

### Exercice pratique

Soit **P0 = [7, 10, 8, 0, 5, 2, 4, 9, 11, 1, 3, 6]** (l'ouverture du *Concerto op. 24* de Webern, réordonnée pour l'exercice) :

1. Dérivez **R0** en inversant l'ordre de P0.
2. Dérivez **I0** en calculant (7 − x + 7) modulo 12 pour chaque élément, c'est-à-dire en inversant autour de la première note. Méthode plus simple : calculer (2 × 7 − x) modulo 12 pour chaque x de P0, ce qui reflète chaque note autour de la classe de hauteurs 7.
3. Dérivez **RI0** en inversant l'ordre de I0.

**Corrigé détaillé :**

- **R0 :** [6, 3, 1, 11, 9, 4, 2, 5, 0, 8, 10, 7]

- **I0** (inversion autour de 7, formule (14 − x) modulo 12) :
  - 7 → (14−7) mod 12 = 7
  - 10 → (14−10) mod 12 = 4
  - 8 → (14−8) mod 12 = 6
  - 0 → (14−0) mod 12 = 2
  - 5 → (14−5) mod 12 = 9
  - 2 → (14−2) mod 12 = 0
  - 4 → (14−4) mod 12 = 10
  - 9 → (14−9) mod 12 = 5
  - 11 → (14−11) mod 12 = 3
  - 1 → (14−1) mod 12 = 1
  - 3 → (14−3) mod 12 = 11
  - 6 → (14−6) mod 12 = 8
  - **I0 : [7, 4, 6, 2, 9, 0, 10, 5, 3, 1, 11, 8]**

- **RI0 :** inverser l'ordre de I0 → [8, 11, 1, 3, 5, 10, 0, 9, 2, 6, 4, 7]

Vérifiez que chaque série contient une fois et une seule chaque classe de hauteurs de 0 à 11.

---

## 5. L'atonalité libre

Toute musique atonale n'est pas sérielle. L'**atonalité libre** — la musique de Schoenberg (1908-1920), du premier Berg, du premier Webern et de nombreux compositeurs ultérieurs — organise les hauteurs sans les contraintes systématiques des séries dodécaphoniques. Elle s'appuie plutôt sur des principes intuitifs.

**Centricité de hauteur (sans tonalité) :**

Même sans tonique, certaines hauteurs peuvent acquérir une importance structurelle par :
- **La répétition :** une hauteur qui revient tout au long d'une pièce devient un point de référence.
- **Le registre :** une hauteur placée systématiquement dans un registre extrême (très aigu ou très grave) gagne en relief.
- **Le rythme :** une hauteur placée sur des temps forts ou sur de longues durées ressort.
- **Le timbre :** une hauteur constamment confiée à un instrument caractéristique devient mémorable.

C'est la **centricité de hauteur** : l'émergence de hauteurs focales sans l'appareil fonctionnel de la tonalité. La hauteur est centrale non parce qu'elle serait « la tonique », mais parce que le compositeur l'a structurellement mise en avant.

**Cellules motiviques :**

La musique atonale libre repose le plus souvent sur de petits ensembles de classes de hauteurs — les **cellules motiviques** — qui constituent son ADN structurel. Une cellule est une classe d'ensembles de 3 à 5 notes, qui revient au long de la pièce sous diverses transpositions, inversions et dispositions. Les *Cinq pièces pour orchestre, op. 10* de Webern n'emploient qu'une poignée de classes d'ensembles sur toute leur durée : l'économie en est stupéfiante.

La cellule fonctionne comme un leitmotiv wagnérien, mais au niveau des classes de hauteurs plutôt qu'à celui de la mélodie. L'auditeur perçoit une cohérence sans pouvoir l'expliquer.

**Progressions de classes d'ensembles :**

Une suite de classes d'ensembles à l'échelle d'une pièce peut créer un mouvement structurel de grande ampleur. Une pièce peut par exemple commencer par de petites classes chromatiques (3-1 [0,1,2]) et s'élargir progressivement vers des classes plus vastes et plus diatoniques (5-35 [0,2,4,7,9]). Ou l'inverse : un trajet de la consonance vers la dissonance, ou de la tension vers la détente, sans recourir à la cadence tonale.

**Distribution registrale :**

En musique atonale, le registre porte souvent du sens structurel. Webern était réputé pour distribuer les notes d'un même accord ou d'une même ligne mélodique sur des registres extrêmes, un phénomène appelé **Klangfarbenmelodie** (mélodie de timbres). Résultat : l'auditeur perçoit la pièce autant par l'espace et le timbre que par les hauteurs. L'analyse post-tonale doit donc considérer où les notes sont placées, et pas seulement quelles classes de hauteurs apparaissent.

**Les échos tonals de Berg :**

Alban Berg occupe une position intermédiaire passionnante. Ses œuvres (le *Concerto pour violon*, par exemple) emploient des séries dodécaphoniques qui contiennent des sous-ensembles tonals : accords parfaits, septièmes de dominante, fragments diatoniques. Il en résulte une musique atonale qui évoque sans cesse la mémoire tonale sans jamais s'engager dans une tonalité. La musique de Berg enseigne qu'« atonal » ne signifie pas « antitonal » : cela peut vouloir dire « tonal par fragments, mais pas par grammaire ».

---

## 6. Applications à la guitare et répertoire

Les techniques post-tonales ne sont pas des exercices abstraits : elles sont largement présentes dans le répertoire de guitare moderne et dans la pratique de l'improvisation.

**Henze — *Royal Winter Music* (1976) :**

Les deux sonates de Hans Werner Henze sur des personnages de Shakespeare comptent parmi les œuvres atonales majeures du répertoire de guitare. *Royal Winter Music I* comporte six mouvements (Gloucester, Roméo et Juliette, Ariel, Ophélie, Touchstone, Obéron). Chaque personnage est dépeint par un vocabulaire de classes de hauteurs qui lui est propre : un petit ensemble de cellules motiviques développées tout au long du mouvement. La sonate est atonale mais gestuelle, et reste reconnaissable comme galerie de portraits, même sans centre tonal.

**Britten — *Nocturnal after John Dowland, op. 70* (1963) :**

Ce chef-d'œuvre pour guitare seule prend un thème du compositeur de la Renaissance John Dowland et le soumet à huit variations de plus en plus éloignées de la tonalité. Les premières paraissent instables mais reconnaissables ; celles du milieu se dissolvent en textures atonales libres ; la dernière, une passacaille, retrouve la clarté tonale. L'œuvre est un parcours à travers les techniques post-tonales qui se résout dans l'harmonie classique : une réconciliation plutôt qu'un rejet.

**Composer une étude atonale — méthode pratique :**

Voici un procédé pour composer une courte étude atonale pour guitare à partir d'une cellule de trois notes :

1. **Choisir une cellule trichordale.** Exemple : la classe d'ensembles 3-3 [0,1,4], un agrégat chromatique plus une tierce. En hauteurs : do, do♯, mi.
2. **La reporter sur les positions CAGED.** Trouver les transpositions de [0,1,4] qui tombent naturellement sous chacune des cinq formes CAGED. En position V (5e case) : la, si♭, do♯. En position III : sol, la♭, si. Et ainsi de suite.
3. **Composer des phrases qui parcourent les positions.** Chaque phrase énonce la cellule dans une position, puis glisse vers la suivante. L'identité de la cellule est préservée tandis que sa localisation sur le manche se déplace.
4. **Varier le registre, la nuance, l'articulation.** Appliquer la distribution registrale de l'atonalité libre : jouer certaines cellules resserrées, d'autres étalées sur deux octaves.
5. **Employer l'inversion et le rétrograde.** Énoncer [0,1,4], puis son inversion [0,3,4], puis son rétrograde, puis le rétrograde de l'inversion. Le développement motivique se fait par opérations sérielles.

Cette méthode produit une musique atonale, cohérente et spécifiquement guitaristique : la géométrie du manche façonne la forme musicale.

**Applications à l'improvisation :**

Les guitaristes de jazz — Ben Monder, Kurt Rosenwinkel, Mary Halvorson — emploient fréquemment des techniques atonales dans leurs improvisations : cellules trichordales, vecteurs d'intervalles comme guides de sonorité, voicings quartals et chromatiques. Comprendre la théorie des ensembles permet à l'improvisateur de circuler consciemment entre langages tonal et post-tonal, en les traitant comme un spectre unifié plutôt que comme des systèmes opposés.

---

## 7. Le pont de retour

La théorie post-tonale n'est pas un rejet de la théorie tonale : c'en est une généralisation. Les outils forgés pour l'analyse atonale éclairent la musique tonale sous un jour neuf, et jettent un pont entre des traditions qui pourraient sembler incompatibles.

**La théorie des ensembles comme outil d'analyse des voicings de jazz :**

L'harmonie jazz est notoirement complexe : extensions, altérations, polyaccords, triades supérieures. L'analyse tonale traditionnelle peine à décrire un accord comme **Sol7alt(♭9,♯9,♭13)**. L'analyse par classes d'ensembles, elle, le réduit à un ensemble de classes de hauteurs et en identifie directement la classe. L'accord ci-dessus a pour classes de hauteurs {7, 11, 5, 9, 10, 3} ; sa forme première est un hexacorde précis, dont le vecteur d'intervalles caractérise la sonorité.

Les théoriciens du jazz disposent ainsi d'un langage qui traverse les conventions de chiffrage. Deux accords aux chiffrages différents peuvent appartenir à la même classe d'ensembles, et donc partager le même contenu intervallique. Deux accords aux chiffrages voisins peuvent appartenir à des classes différentes. La théorie des ensembles révèle la sonorité réelle sous la notation.

**Les vecteurs d'intervalles comme mesures de sonorité :**

Le vecteur d'intervalles quantifie la « couleur » d'un accord. Un accord riche en ci3 et ci4 (des tierces) sonne tertien. Un accord dominé par les ci5 sonne quartal. Un accord chargé de ci2 et de ci6 sonne dense et dissonant. En lisant le vecteur d'intervalles d'un accord, on peut prédire son caractère sonore sans même l'entendre.

C'est immédiatement utile au guitariste : pour choisir le voicing d'un accord ambigu, on peut retenir celui dont le vecteur d'intervalles correspond à la sonorité voulue — ouverte et quartale, dense et chromatique, ou entre les deux.

**OPTIC/K et l'équivalence des classes de hauteurs :**

Dans la théorie néo-riemannienne et transformationnelle, les équivalences de conduite des voix sont décrites par les relations **OPTIC** :
- **O**ctave : deux hauteurs distantes d'une octave sont identiques.
- **P**ermutation : réordonner à l'intérieur d'une octave ne change pas l'identité.
- **T**ransposition : deux accords séparés par un même intervalle sont équivalents.
- **I**nversion : deux accords en miroir sont équivalents.
- **C**ardinalité : les doublures ne comptent pas.

Ce sont exactement les principes de la théorie des ensembles de classes de hauteurs, formulés autrement. OPTIC rend explicite que cette théorie n'a rien d'exotique : elle formalise la façon dont les musiciens ont toujours entendu les équivalences (un accord de do majeur est « le même » qu'il soit disposé do-mi-sol, sol-do-mi ou do-mi-sol-do).

La relation **K** ajoute une couche supplémentaire, l'équivalence jusqu'à l'appartenance à une classe d'ensembles. Ensemble, OPTIC et K forment un cadre mathématique qui unifie l'analyse tonale de la conduite des voix et la théorie post-tonale des ensembles. Les deux traditions ne s'opposent pas : ce sont deux dialectes d'une même langue.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Tonalité de la pratique classique** | Le système harmonique de la musique savante occidentale, d'environ 1600 à 1900, fondé sur l'harmonie fonctionnelle et les centres tonals |
| **Émancipation de la dissonance** | L'affirmation de Schoenberg, en 1908, selon laquelle les sonorités dissonantes n'ont pas à se résoudre sur une consonance |
| **Atonalité** | Musique organisée sans centre tonal ni tonalité |
| **Atonalité libre** | Musique atonale organisée intuitivement par cellules motiviques, distribution registrale et centricité de hauteur |
| **Sérialisme (dodécaphonisme)** | Organisation systématique de la musique atonale à partir d'une série ordonnée de 12 classes de hauteurs |
| **Classe de hauteurs** | Classe d'équivalence des hauteurs liées par l'octave (tous les do appartiennent à la classe 0) |
| **Notation entière** | Représentation des classes de hauteurs par les entiers de 0 à 11 |
| **Forme normale** | L'ordonnancement le plus compact d'un ensemble de classes de hauteurs |
| **Forme première** | Le représentant canonique d'une classe d'ensembles, équivalence par inversion comprise, transposé pour commencer à 0 |
| **Classe d'intervalles (ci)** | Classe d'équivalence des intervalles (0 à 6) regroupant ceux qui sont liés par inversion |
| **Vecteur d'intervalles** | Liste de 6 éléments comptant les occurrences de chaque classe d'intervalles dans un ensemble |
| **Classe d'ensembles** | Groupe d'ensembles de classes de hauteurs liés par transposition et inversion, désigné par un numéro de Forte |
| **Numéro de Forte** | L'étiquette du catalogue d'Allen Forte pour une classe d'ensembles, au format cardinalité-rang (par exemple 3-11) |
| **Relation Z** | Relation entre des classes d'ensembles distinctes qui partagent le même vecteur d'intervalles |
| **Originale/Rétrograde/Inversion/Rétrograde de l'inversion (P/R/I/RI)** | Les quatre opérations sérielles appliquées à une série dodécaphonique |
| **Combinatorialité** | Propriété de certaines séries dont les hexacordes, combinés à des formes transposées, produisent des agrégats |
| **Centricité de hauteur** | Mise en relief structurelle de certaines hauteurs en musique atonale, sans fonction tonale |
| **Cellule motivique** | Petit ensemble de classes de hauteurs servant d'ADN structurel à une composition atonale |

---

## Auto-évaluation

**1. Qu'entendait Schoenberg par « émancipation de la dissonance », et pourquoi fut-ce un tournant historique ?**
> Schoenberg a affirmé en 1908 que les sonorités dissonantes n'ont pas besoin de se résoudre sur des consonances, et que la distinction entre consonance et dissonance est une convention historique, non une loi acoustique. Ce fut un tournant parce que cela levait la dernière contrainte de la tonalité classique — l'obligation de résoudre la tension — et ouvrait la voie à une composition atonale où toute sonorité pouvait tenir lieu d'événement structurel stable.

**2. Calculez la forme première de l'ensemble {ré, fa, la, do} (un accord de ré mineur septième). Montrez la forme normale et une vérification d'inversion.**
> Classes de hauteurs : {2, 5, 9, 0} → ordre croissant {0, 2, 5, 9}. Rotations et étendues :
> - (0, 2, 5, 9) : étendue = 9
> - (2, 5, 9, 0+12=12) : étendue = 10
> - (5, 9, 12, 14) : étendue = 9
> - (9, 12, 14, 17) : étendue = 8 — la plus petite !
> Forme normale : {9, 0, 2, 5}. Transposition pour commencer à 0 : retrancher 9 → {0, 3, 5, 8}. Inversion : {0, −3, −5, −8} modulo 12 = {0, 9, 7, 4} → réordonner {0, 4, 7, 9}. Comparaison de {0,3,5,8} et {0,4,7,9} : le deuxième élément 3 < 4, donc {0,3,5,8} est plus tassé vers la gauche.
> **Forme première : [0,3,5,8]** — classe d'ensembles 4-26, la sonorité de septième mineure (accord mineur plus septième).

**3. Soit P0 = [0, 1, 4, 9, 5, 11, 2, 7, 6, 10, 3, 8]. Dérivez I0 (inversion commençant sur 0). Indiquez la formule employée.**
> Formule : I0[k] = (0 − P0[k]) modulo 12 = (−P0[k]) modulo 12.
> - 0 → 0
> - 1 → 11
> - 4 → 8
> - 9 → 3
> - 5 → 7
> - 11 → 1
> - 2 → 10
> - 7 → 5
> - 6 → 6
> - 10 → 2
> - 3 → 9
> - 8 → 4
> **I0 : [0, 11, 8, 3, 7, 1, 10, 5, 6, 2, 9, 4]**

**4. Qu'est-ce qu'une relation Z, et pourquoi importe-t-elle en théorie post-tonale ?**
> Une relation Z est la propriété que partagent deux classes d'ensembles distinctes ayant des vecteurs d'intervalles identiques, sans être liées par transposition ni par inversion. Elle importe parce qu'elle révèle que le contenu intervallique — quels intervalles sont présents — ne détermine pas à lui seul l'identité de la classe d'ensembles, c'est-à-dire quelles configurations de hauteurs produisent ces intervalles. Les ensembles en relation Z sonnent de façon très proche mais sont structurellement distincts : une symétrie profonde, exploitée par des compositeurs comme Elliott Carter et Milton Babbitt.

**5. En quoi l'analyse par la théorie des ensembles fait-elle le pont entre musique post-tonale et harmonie jazz ?**
> La théorie des ensembles abstrait les accords en ensembles et en classes de classes de hauteurs, en s'affranchissant des conventions de chiffrage. Un accord de dominante altérée complexe peut être identifié par sa classe d'ensembles et caractérisé par son vecteur d'intervalles, ce qui met au jour sa sonorité sous-jacente là où le chiffrage la masque. Les analystes du jazz peuvent ainsi comparer des voicings de qualités apparemment différentes, repérer des sonorités communes et comprendre langages atonal et jazz comme deux dialectes d'un même cadre de classes de hauteurs, et non comme des systèmes opposés.

**Critères de réussite :** calculer la forme première d'un accord donné de 4 à 5 notes, dériver I0 et R0 à partir d'une P0 donnée, et expliquer la fonction structurelle d'une cellule motivique dans un contexte atonal libre.

---

## Bases de la recherche

- La théorie des ensembles de classes de hauteurs a été formalisée par Allen Forte dans *The Structure of Atonal Music* (1973) ; les numéros de Forte restent le système de catalogage de référence
- *Introduction to Post-Tonal Theory* de Joseph N. Straus (4e éd., 2016) est le manuel pédagogique de référence et la source des algorithmes de forme normale et de forme première
- *Serial Composition and Atonality* de George Perle (6e éd., 1991) fournit les assises historiques et analytiques de la technique dodécaphonique
- La théorie néo-riemannienne et les relations OPTIC prolongent la théorie des ensembles vers l'analyse de la conduite des voix (Cohn, 2012 ; Tymoczko, *A Geometry of Music*, 2011)
- Répertoire de guitare cité : Henze, *Royal Winter Music I & II* ; Britten, *Nocturnal op. 70* ; Takemitsu, *All in Twilight* ; Ginastera, *Sonate op. 47*
- Les écrits de Schoenberg lui-même (*Style and Idea*, 1950) documentent l'émancipation de la dissonance dans ses propres mots
- Sources : Forte 1973, Straus 2016, Perle 1991, Tymoczko 2011, Cohn 2012, Schoenberg 1950
- État de croyance : T(0.85) F(0.03) U(0.08) C(0.04)
