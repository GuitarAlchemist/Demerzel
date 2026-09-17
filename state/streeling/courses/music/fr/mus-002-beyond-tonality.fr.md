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

# Au-delà de la tonalité : théorie post-tonale pour guitaristes

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée : 45 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Expliquer la dissolution historique de la tonalité de la pratique commune et l'émergence de l'atonalité
- Traduire des hauteurs en notation entière de classes de hauteur et calculer formes normales et formes premières
- Construire des vecteurs d'intervalles et identifier des classes d'ensembles à l'aide des nombres de Forte
- Dériver les quatre formes d'une série dodécaphonique et comprendre la matrice 12x12
- Analyser la musique atonale libre à travers la centralité de hauteur, les cellules motiviques et la distribution des registres
- Appliquer la pensée post-tonale au répertoire moderne de la guitare et à vos propres compositions/improvisations
- Reconnaître comment la théorie des ensembles offre un pont de retour vers l'analyse des voicings jazz

---

## 1. La fin de la pratique commune

Pendant environ 300 ans — de Bach à Brahms — la musique savante occidentale a fonctionné au sein d'un système partagé appelé **tonalité de la pratique commune**. Ce système avait une grammaire claire : un centre tonal, une harmonie fonctionnelle (tonique-sous-dominante-dominante) et une organisation mélodique autour des gammes diatoniques. Chaque accord avait un rôle ; chaque note avait une destination.

À la fin du XIXe siècle, les compositeurs ont commencé à étirer cette grammaire jusqu'à ce qu'elle cède. L'opéra de Wagner *Tristan und Isolde* (1859) s'ouvre sur un accord — le célèbre « accord de Tristan » (Fa-Si-Ré#-Sol#) — qui refuse de se résoudre de quelque manière traditionnelle que ce soit. Pendant plusieurs heures de musique, Wagner diffère la résolution attendue sur la tonique, maintenant l'auditeur en suspens dans une ambiguïté chromatique. L'opéra se termine par une résolution, mais le message était clair : la fonction tonale pouvait être retardée, affaiblie et finalement dissoute.

Debussy, Mahler, Strauss et Scriabine ont poursuivi cette expansion chromatique. Les accords sont devenus si chargés de notes étrangères, d'extensions altérées et de mouvements parallèles que le squelette tonal sous-jacent a disparu. Au début des années 1900, la question est devenue inévitable : si les accords n'ont plus besoin de se résoudre, et si les tonalités ne sont plus contraignantes, que reste-t-il ?

**L'émancipation de la dissonance selon Schoenberg :**

Arnold Schoenberg a répondu à la question dans sa musique dès 1908, puis a nommé ce principe « émancipation de la dissonance » (essai « Opinion or Insight? », 1926, repris dans *Style and Idea*) : **la dissonance n'a pas besoin de se résoudre**. Dans la théorie traditionnelle, la consonance était « naturelle » et la dissonance un écart qui devait être corrigé. Schoenberg soutenait qu'il s'agissait d'une convention historique, pas d'une loi acoustique. Dissonance et consonance ne sont pas des opposés — ce sont des points sur un continuum, et les compositeurs devraient être libres d'utiliser n'importe quelle sonorité comme un événement stable.

Cette émancipation de la dissonance a brisé la dernière contrainte de la tonalité. Les *Trois pièces pour piano, op. 11* (1909) de Schoenberg sont souvent citées comme la première œuvre « atonale ». Pas d'armure. Pas de résolution sur une tonique. Des hauteurs organisées par une logique motivique et registrale plutôt que par l'harmonie fonctionnelle.

**Deux voies : atonalité libre ou sérialisme :**

Après l'émancipation, les compositeurs ont suivi deux voies divergentes :

- **Atonalité libre :** intuitive, motivique, non systématisée. Des hauteurs choisies à l'oreille et selon une logique structurelle. Schoenberg (1908-1920), Berg, le premier Webern, Varese, Ives. L'oreille du compositeur est la seule autorité.
- **Sérialisme (technique dodécaphonique) :** une méthode systématique que Schoenberg a développée en 1921 pour organiser le matériau de hauteurs atonal. Chaque composition repose sur une série ordonnée des 12 classes de hauteur, manipulée par des opérations précises. Le système a remplacé la grammaire tonale par une nouvelle grammaire.

Les deux voies partagent le même fondement : les 12 classes de hauteur du tempérament égal sont traitées comme un ensemble démocratique, sans qu'aucune note ne soit privilégiée par rapport aux autres. C'est le point de départ de la théorie post-tonale.

---

## 2. Notation entière des classes de hauteur

La théorie post-tonale a besoin d'une notation qui traite les 12 classes de hauteur comme équivalentes et abstraites. Les noms de notes traditionnels (Do, Ré, Mi...) sont pratiques mais chargés d'un bagage tonal — les orthographes enharmoniques (Do# ou Réb) suggèrent des significations tonales différentes, sans pertinence en analyse post-tonale.

La solution : la **notation entière**. Attribuez un entier à chaque classe de hauteur :

| Hauteur | Entier |
|-------|---------|
| Do    | 0       |
| Do#/Réb | 1     |
| Ré    | 2       |
| Ré#/Mib | 3     |
| Mi    | 4       |
| Fa    | 5       |
| Fa#/Solb | 6    |
| Sol   | 7       |
| Sol#/Lab | 8    |
| La    | 9       |
| La#/Sib | 10 (t) |
| Si    | 11 (e)  |

**Équivalence d'octave :** dans l'espace des classes de hauteur, tous les Do sont « les mêmes » — il n'y a pas de Do central ou de Do grave. L'entier 0 représente la classe de tous les Do à toutes les octaves. Un ensemble de hauteurs devient un ensemble d'entiers modulo 12.

**Équivalence enharmonique :** Do# et Réb sont la même classe de hauteur (1). L'analyse post-tonale écarte la distinction tonale, car aucun contexte de tonalité ne la justifie.

**Forme normale :**

Étant donné un ensemble de hauteurs, la **forme normale** est l'ordonnancement le plus compact de l'ensemble. Pour la trouver :

1. Rangez les classes de hauteur par ordre croissant autour du cercle chromatique.
2. Considérez chaque rotation de l'ensemble.
3. Choisissez la rotation dont l'étendue entre le premier et le dernier élément est la plus petite.
4. En cas d'égalité entre plusieurs rotations, comparez leurs **intervalles mesurés depuis le premier élément** (transposez chaque rotation pour qu'elle commence sur 0), et non les numéros de classes de hauteur eux-mêmes. La règle de Forte choisit la rotation la plus tassée vers la gauche : plus petit intervalle du premier au deuxième élément, puis du premier au troisième, etc. La règle de Rahn, utilisée par la plupart des tables actuelles (par exemple Open Music Theory), compare depuis la droite : plus petit intervalle du premier à l'avant-dernier élément, puis du premier à celui qui le précède, etc. Les deux règles concordent pour tous les ensembles de ce module ; elles ne donnent des formes premières différentes que pour 6 des 224 classes d'ensembles (par exemple 5-20 : Rahn (01568), Forte (01378)).

**Exemple :** l'ensemble {Mi, Sol#, Do} = {4, 8, 0}. Rotations (en intervalles du premier au dernier élément autour du cercle) :
- 0, 4, 8 : étendue = 8
- 4, 8, 0 : étendue = 8 (mais 0 signifie « 0 + 12 = 12 », donc étendue = 12 - 4 = 8)
- 8, 0, 4 : étendue = 8

Toutes les rotations sont symétriques (c'est un accord parfait augmenté). Par convention, on choisit {0, 4, 8}.

**Forme première :**

La **forme première** est la représentation la plus abstraite d'une classe d'ensembles — elle efface les distinctions de transposition ET d'inversion. Pour trouver la forme première :

1. Calculez la forme normale et transposez-la pour que le premier élément soit 0.
2. Calculez la forme normale de l'inversion (inversez l'ensemble autour de 0 en prenant l'opposé de chaque élément mod 12, puis normalisez) et transposez-la pour que le premier élément soit 0.
3. Choisissez la plus tassée des deux, avec la même règle de départage que pour la forme normale.

Les ensembles de classes de hauteur en forme normale s'écrivent entre crochets, par exemple [0,4,7] ; les formes premières, qui nomment toute une classe d'ensembles, s'écrivent entre parenthèses sans virgules : (037) est la forme première à la fois de l'accord parfait majeur et de l'accord parfait mineur.

**Un instant — les accords parfaits majeur et mineur sont-ils des classes d'ensembles différentes ?** Sous la seule transposition, oui : aucune transposition ne change Do majeur [0,4,7] en accord mineur. Mais les classes d'ensembles de la théorie post-tonale (celles de Forte) sont définies à transposition **et** inversion près, et inverser Do majeur [0,4,7] autour de 0 donne Fa mineur [5,8,0]. Les accords parfaits majeur et mineur appartiennent donc à la **même classe d'ensembles, 3-11**, avec l'unique forme première (037). Les catalogues qui séparent les formes liées par inversion (les « types Tn », à transposition seule) étiquettent la forme mineure [0,3,7] 3-11A et la forme majeure [0,4,7] 3-11B.

### Exercice pratique

Les cordes à vide d'une guitare (accordage standard) sont Mi-La-Ré-Sol-Si-Mi. Conversion en entiers de classes de hauteur :
- Mi = 4
- La = 9
- Ré = 2
- Sol = 7
- Si = 11

En traitant les cordes à vide comme un ensemble (en ignorant le doublement du Mi à l'octave) : {2, 4, 7, 9, 11}.

Votre tâche :
1. Rangez-les par ordre croissant.
2. Déterminez la forme normale.
3. Calculez la forme première.

**Corrigé détaillé :**
- Ordre croissant : {2, 4, 7, 9, 11}
- Rotations et étendues :
  - (2, 4, 7, 9, 11) : étendue = 11 - 2 = 9
  - (4, 7, 9, 11, 2+12=14) : étendue = 14 - 4 = 10
  - (7, 9, 11, 14, 16) : étendue = 9
  - (9, 11, 14, 16, 19) : étendue = 10
  - (11, 14, 16, 19, 21) : étendue = 10
- Rotations à égalité : (2,4,7,9,11) et (7,9,11,2,4). Comparez leurs intervalles depuis le premier élément, pas les classes de hauteur : (2,4,7,9,11) → 0, 2, 5, 7, 9 et (7,9,11,14,16) → 0, 2, 4, 7, 9. Depuis la gauche, les deuxièmes éléments sont à égalité (2 contre 2) et les troisièmes départagent (4 < 5) ; depuis la droite, les avant-derniers éléments sont à égalité (7 contre 7) et ceux qui les précèdent départagent (4 < 5). Les deux règles choisissent (7,9,11,2,4). Forme normale : [7, 9, 11, 2, 4] (Sol, La, Si, Ré, Mi).
- Transposez pour commencer sur 0 : soustrayez 7 à chaque élément → [0, 2, 4, 7, 9].
- Vérifiez l'inversion : inversez {2,4,7,9,11} → {10, 8, 5, 3, 1}. Ordre croissant : {1, 3, 5, 8, 10}. Ses rotations à égalité (étendue 9) sont (1,3,5,8,10) → 0, 2, 4, 7, 9 et (8,10,1,3,5) → 0, 2, 5, 7, 9 ; la plus tassée donne de nouveau [0, 2, 4, 7, 9], identique à l'original : cette classe d'ensembles est symétrique par inversion.
- **Forme première : (02479)** — c'est la classe d'ensembles 5-35, le **sous-ensemble pentatonique/diatonique** (la gamme pentatonique anhémitonique). Les cordes à vide de la guitare forment une classe d'ensembles pentatonique : pentatonique majeure de Sol, Sol La Si Ré Mi.

---

## 3. Vecteurs d'intervalles et classes d'ensembles

Au-delà du contenu en hauteurs, l'analyse post-tonale s'intéresse au **contenu intervallique** — quels intervalles sont présents dans un ensemble, et combien de chacun. C'est ce que capture le **vecteur d'intervalles**.

**Classe d'intervalles (ic) :**

En théorie post-tonale, les intervalles sont classés de 0 à 6 (il n'y a que 7 classes d'intervalles, car les classes d'intervalles sont symétriques autour du triton) :

| ic | Demi-tons | Exemple |
|----|-----------|---------|
| 0  | unisson/octave | Do-Do |
| 1  | seconde mineure / septième majeure | Do-Réb / Do-Si |
| 2  | seconde majeure / septième mineure | Do-Ré / Do-Sib |
| 3  | tierce mineure / sixte majeure | Do-Mib / Do-La |
| 4  | tierce majeure / sixte mineure | Do-Mi / Do-Lab |
| 5  | quarte juste / quinte juste | Do-Fa / Do-Sol |
| 6  | triton | Do-Fa# |

Une seconde mineure (1 demi-ton) et une septième majeure (11 demi-tons) sont la même classe d'intervalles, car ce sont des renversements l'une de l'autre.

**Construire le vecteur d'intervalles :**

Le vecteur d'intervalles est une liste de 6 éléments qui compte combien de fois chaque classe d'intervalles (ic1 à ic6) apparaît entre toutes les paires de notes d'un ensemble.

**Exemple — accord parfait de Do majeur {0, 4, 7} :**
- Paires : (0,4), (0,7), (4,7)
- Intervalles : 4-0=4 (ic4), 7-0=7 (ic5), 7-4=3 (ic3)
- Décompte : ic1=0, ic2=0, ic3=1, ic4=1, ic5=1, ic6=0
- **Vecteur d'intervalles : [001110]**

Remarquez : l'accord parfait majeur et l'accord parfait mineur partagent le même vecteur d'intervalles [001110], car ils sont liés par inversion, et l'inversion préserve les classes d'intervalles. C'est aussi parce qu'ils sont liés par inversion qu'ils appartiennent à la même classe d'ensembles, **3-11**. La réciproque est fausse : deux ensembles de même vecteur d'intervalles n'appartiennent pas forcément à la même classe d'ensembles (voir les relations Z ci-dessous).

**Nombres de Forte :**

Allen Forte (1973) a catalogué toutes les classes d'ensembles possibles de 3 à 9 notes et a attribué un numéro à chacune. Le format est **cardinalité-ordinal** :

- **3-11 :** la 11e classe d'ensembles de cardinalité 3 — l'accord parfait majeur/mineur.
- **3-12 :** l'accord parfait augmenté (048), vecteur d'intervalles [000300].
- **4-20 :** l'accord de septième majeure (0158), vecteur d'intervalles [101220].
- **3-1 :** le tricorde chromatique (012), vecteur d'intervalles [210000].
- **6-Z28 / 6-Z49 :** hexacordes en relation Z (voir ci-dessous).

Les ordinaux reflètent un ordre que Forte a choisi en fonction du contenu intervallique, en gros du plus compact (ordinaux les plus bas) au plus dispersé.

**Relations Z :**

Certaines classes d'ensembles distinctes partagent le même vecteur d'intervalles alors qu'elles ont des contenus en hauteurs différents et ne sont liées ni par transposition ni par inversion. On les appelle des ensembles **en relation Z**. Forte les a marqués d'un préfixe Z. L'exemple le plus célèbre : les classes d'ensembles 4-Z15 et 4-Z29 ont toutes deux le vecteur d'intervalles [111111] (le « tétracorde à tous les intervalles »), mais ce sont réellement des ensembles différents. Les relations Z ont fasciné Elliott Carter et Milton Babbitt, car elles représentent une symétrie profonde de l'espace des intervalles.

### Exercice pratique

Calculez le vecteur d'intervalles de **Esus4** à la guitare. Esus4 se compose de Mi, La, Si — classes de hauteur {4, 9, 11}.

**Corrigé détaillé :**
- Paires et intervalles :
  - (4, 9) : 9 - 4 = 5 → ic5
  - (4, 11) : 11 - 4 = 7 → ic5 (car ic = min(7, 12-7) = 5)
  - (9, 11) : 11 - 9 = 2 → ic2
- Décompte : ic1=0, ic2=1, ic3=0, ic4=0, ic5=2, ic6=0
- **Vecteur d'intervalles : [010020]**

Cette classe d'ensembles contient un intervalle de seconde majeure et deux intervalles de quarte/quinte juste. Sa forme première est (027), classe d'ensembles **3-9**. C'est le tricorde en quartes — une sonorité centrale dans les voicings jazz (par exemple l'accompagnement main gauche de McCoy Tyner) et dans l'écriture orchestrale du XXe siècle (Copland, Hindemith).

---

## 4. Séries dodécaphoniques et opérations sérielles

La méthode dodécaphonique de Schoenberg (1921) organisait le matériau de hauteurs atonal au moyen d'une **série ordonnée** — une séquence précise contenant les 12 classes de hauteur, chacune apparaissant exactement une fois. La série sert de code génétique à la composition ; chaque mélodie, harmonie et contrepoint en dérive.

**Les quatre formes de la série :**

Étant donné une **série originale (P0)** — l'ordre de départ —, trois transformations engendrent trois formes apparentées :

1. **Originale (P) :** la série de départ.
2. **Rétrograde (R) :** la série jouée à l'envers (la dernière note en premier).
3. **Inversion (I) :** chaque intervalle de la série originale change de direction. Si P monte d'une tierce mineure, I descend d'une tierce mineure.
4. **Rétrograde de l'inversion (RI) :** l'inversion jouée à l'envers.

Chaque forme peut être **transposée** pour commencer sur n'importe laquelle des 12 classes de hauteur, ce qui donne **48 formes de série au total** (4 opérations × 12 transpositions).

**Exemple — une série simple :**

Soit P0 = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10] (une série fabriquée).

- **R0 :** P0 à l'envers → [10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 1, 0]
- **I0 :** inversion autour de 0. Pour chaque élément x de P0, calculez (0 - x) mod 12 :
  - P0 : [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10]
  - I0 : [0, 11, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
- **RI0 :** I0 à l'envers → [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 11, 0]

**Transposition :** pour créer P3 (forme originale commençant sur la classe de hauteur 3), ajoutez 3 à chaque élément de P0 (mod 12) : [3, 4, 6, 5, 8, 7, 10, 9, 0, 11, 2, 1].

**La matrice 12x12 :**

Une matrice dodécaphonique est une façon compacte d'afficher les 48 formes de la série :

- Les **lignes** (de gauche à droite) sont les 12 transpositions de P, étiquetées P0 à P11 d'après leur niveau de transposition par rapport à P0 (leur première classe de hauteur quand P0 commence sur 0).
- Les **lignes lues de droite à gauche** sont les rétrogrades (R0 à R11).
- Les **colonnes** (de haut en bas) sont les 12 transpositions de I, étiquetées d'après leur première classe de hauteur.
- Les **colonnes lues de bas en haut** sont les rétrogrades des inversions.

Pour construire la matrice :
1. Écrivez P0 sur la ligne du haut.
2. Écrivez I0 dans la colonne de gauche (l'inversion de P0, commençant sur la même première note).
3. Chaque ligne suivante est P0 transposée de sorte que sa première note corresponde à la colonne la plus à gauche.

**Combinatorialité :**

Certaines séries possèdent une propriété particulière appelée **combinatorialité** : si vous divisez la série en deux hexacordes (les 6 premières notes, les 6 dernières), une transposition particulière de I produit des hexacordes qui, avec ceux de P, forment deux agrégats complets (les 12 classes de hauteur dans chaque moitié). Schoenberg a largement exploité la combinatorialité, car elle permet d'énoncer simultanément P et I sans répétition de classes de hauteur — une sorte de contrepoint dodécaphonique qui préserve l'idéal atonal d'absence de privilège.

### Exercice pratique

Soit **P0 = [7, 10, 8, 0, 5, 2, 4, 9, 11, 1, 3, 6]** (le début du *Concerto, op. 24* de Webern, réordonné pour cet exercice) :

1. Dérivez **R0** en inversant l'ordre de P0.
2. Dérivez **I0** en calculant (7 - x + 7) mod 12 pour chaque élément — autrement dit, inversez autour de la première note. Méthode plus simple : calculez (2 × 7 - x) mod 12 pour chaque x de P0, ce qui reflète chaque note autour de la classe de hauteur 7.
3. Dérivez **RI0** en inversant l'ordre de I0.

**Corrigé détaillé :**

- **R0 :** [6, 3, 1, 11, 9, 4, 2, 5, 0, 8, 10, 7]

- **I0** (inversion autour de 7, formule (14 - x) mod 12) :
  - 7 → (14-7) mod 12 = 7
  - 10 → (14-10) mod 12 = 4
  - 8 → (14-8) mod 12 = 6
  - 0 → (14-0) mod 12 = 2
  - 5 → (14-5) mod 12 = 9
  - 2 → (14-2) mod 12 = 0
  - 4 → (14-4) mod 12 = 10
  - 9 → (14-9) mod 12 = 5
  - 11 → (14-11) mod 12 = 3
  - 1 → (14-1) mod 12 = 1
  - 3 → (14-3) mod 12 = 11
  - 6 → (14-6) mod 12 = 8
  - **I0 : [7, 4, 6, 2, 9, 0, 10, 5, 3, 1, 11, 8]**

- **RI0 :** I0 à l'envers → [8, 11, 1, 3, 5, 10, 0, 9, 2, 6, 4, 7]

Vérifiez que chaque série contient chaque classe de hauteur de 0 à 11 exactement une fois.

---

## 5. L'atonalité libre

Toute musique atonale n'est pas sérielle. L'**atonalité libre** — la musique de Schoenberg (1908-1920), du premier Berg, du premier Webern et de nombreux compositeurs ultérieurs — organise les hauteurs sans les contraintes systématiques des séries dodécaphoniques. Elle s'appuie plutôt sur des principes intuitifs :

**Centralité de hauteur (sans tonalité) :**

Même sans tonique, certaines hauteurs peuvent acquérir une importance structurelle par :
- **La répétition :** une hauteur qui revient tout au long d'une pièce devient un point de référence.
- **Le registre :** une hauteur placée systématiquement dans un registre extrême (très aigu ou très grave) prend du relief.
- **Le rythme :** une hauteur placée sur les temps forts ou sur des durées longues se détache.
- **Le timbre :** une hauteur systématiquement confiée à un instrument caractéristique devient mémorable.

C'est la **centralité de hauteur** : l'émergence de hauteurs focales sans l'appareil fonctionnel de la tonalité. La hauteur est centrale non parce qu'elle est « la tonique », mais parce que le compositeur l'a structurellement mise en valeur.

**Cellules motiviques :**

La musique atonale libre repose généralement sur de petits ensembles de classes de hauteur — des **cellules motiviques** — qui constituent son ADN structurel. Une cellule est une classe d'ensembles de 3 à 5 notes qui apparaît tout au long d'une pièce sous diverses transpositions, inversions et dispositions. Les *Cinq pièces pour orchestre, op. 10* de Webern n'utilisent qu'une poignée de classes d'ensembles sur toute leur durée ; l'économie de moyens est stupéfiante.

La cellule fonctionne comme un leitmotiv wagnérien, mais au niveau des classes de hauteur plutôt qu'au niveau mélodique. L'auditeur perçoit une cohérence sans pouvoir expliquer pourquoi.

**Progressions de classes d'ensembles :**

Une succession de classes d'ensembles au fil d'une pièce peut créer un mouvement structurel à grande échelle. Par exemple, une pièce peut commencer par de petites classes d'ensembles chromatiques (3-1, (012)) et s'élargir progressivement vers des classes plus grandes et plus diatoniques (5-35, (02479)). Ou l'inverse : un voyage de la consonance à la dissonance, ou de la tension à la détente, sans recourir à la cadence tonale.

**Distribution des registres :**

Dans la musique atonale, le registre porte souvent une signification structurelle. Webern était célèbre pour répartir les notes d'un même accord ou d'une même ligne mélodique entre des registres extrêmes, et pour faire passer une ligne d'un instrument à l'autre — ce second procédé s'appelle **Klangfarbenmelodie** (mélodie de timbres, terme de Schoenberg à la dernière page de son *Harmonielehre*, 1911). Résultat : l'auditeur perçoit la pièce autant à travers l'espace et le timbre qu'à travers la hauteur. L'analyse post-tonale doit tenir compte de l'endroit où les notes sont placées, et pas seulement des classes de hauteur qui apparaissent.

**Les échos tonaux de Berg :**

Alban Berg occupe un fascinant terrain intermédiaire. Ses œuvres (par exemple le *Concerto pour violon*) utilisent des séries dodécaphoniques qui contiennent des sous-ensembles tonals — accords parfaits, septièmes de dominante, fragments diatoniques. Il en résulte une musique atonale qui évoque sans cesse la mémoire tonale sans jamais s'engager dans une tonalité. La musique de Berg enseigne qu'« atonal » ne veut pas dire « anti-tonal » — cela peut vouloir dire « tonal par fragments, mais pas dans sa grammaire ».

---

## 6. Applications à la guitare et répertoire

Les techniques post-tonales ne sont pas des exercices abstraits — elles occupent une place importante dans le répertoire moderne de la guitare et dans la pratique de l'improvisation.

**Henze — *Royal Winter Music* (1976) :**

Les deux sonates de Hans Werner Henze sur des personnages de Shakespeare comptent parmi les œuvres atonales les plus importantes du répertoire de la guitare. *Royal Winter Music I* comporte six mouvements (Gloucester, Romeo and Juliet, Ariel, Ophelia, Touchstone, Oberon). Chaque personnage est dépeint par un vocabulaire de classes de hauteur propre — un petit ensemble de cellules motiviques développées tout au long du mouvement. La sonate est atonale mais gestuelle : on y reconnaît des portraits de personnages, même sans centre tonal.

**Britten — *Nocturnal after John Dowland, op. 70* (1963) :**

Le chef-d'œuvre de Britten pour guitare seule reprend un thème du compositeur de la Renaissance John Dowland et le soumet à huit variations qui s'éloignent de plus en plus de la tonalité. Les premières variations semblent instables mais reconnaissables ; les variations centrales se dissolvent en textures atonales libres ; la dernière variation (une passacaille) revient à la clarté tonale. La pièce est un voyage à travers les techniques post-tonales qui se résout dans l'harmonie de la pratique commune — une réconciliation plutôt qu'un rejet.

**Construire une étude atonale — méthode pratique :**

Voici une démarche pour composer une courte étude atonale pour guitare à partir d'une cellule de tricorde :

1. **Choisissez une cellule de tricorde.** Exemple : la classe d'ensembles 3-3 (014) — un cluster chromatique plus une tierce. En hauteurs : Do, Do#, Mi.
2. **Associez-la aux positions CAGED.** Trouvez des transpositions de [0,1,4] qui tombent naturellement sous chacune des cinq formes CAGED. En position V (5e case) : La, Sib, Do#. En position III : Sol, Lab, Si. Et ainsi de suite.
3. **Composez des phrases qui parcourent les positions.** Chaque phrase énonce la cellule dans une position, puis passe à la suivante. L'identité de la cellule est préservée tandis que l'emplacement sur le manche se déplace.
4. **Variez le registre, les nuances, l'articulation.** Appliquez la distribution des registres de l'atonalité libre : jouez certaines cellules resserrées, d'autres étalées sur deux octaves.
5. **Utilisez l'inversion et le rétrograde.** Énoncez [0,1,4], puis son inversion [0,3,4], puis son rétrograde, puis le rétrograde de l'inversion. Un développement motivique par les opérations sérielles.

Cette méthode produit une musique atonale, cohérente et spécifiquement guitaristique — la géométrie du manche façonne la forme musicale.

**Applications à l'improvisation :**

Les guitaristes de jazz (par exemple Ben Monder, Kurt Rosenwinkel, Mary Halvorson) utilisent fréquemment des techniques atonales dans leurs improvisations : cellules de tricordes, vecteurs d'intervalles comme guides de sonorité, voicings en quartes et chromatiques. Comprendre la théorie des ensembles permet à l'improvisateur de circuler consciemment entre langages tonal et post-tonal, en les traitant comme un spectre unifié plutôt que comme des systèmes opposés.

---

## 7. Le chemin du retour

La théorie post-tonale n'est pas un rejet de la théorie tonale — c'en est une généralisation. Les outils développés pour l'analyse atonale éclairent la musique tonale sous un jour nouveau, et ils jettent un pont entre des traditions qui pourraient autrement sembler incompatibles.

**La théorie des ensembles comme outil d'analyse des voicings jazz :**

L'harmonie jazz est réputée complexe : extensions, altérations, polyaccords, triades de structure supérieure. L'analyse tonale traditionnelle peine à décrire un accord comme **G7alt(b9,#9,b13)**. L'analyse par classes d'ensembles, elle, le réduit à un ensemble de classes de hauteur et identifie directement sa classe d'ensembles. L'accord ci-dessus a pour classes de hauteur {7, 11, 5, 8, 10, 3} ; sa forme première est un hexacorde précis dont le vecteur d'intervalles caractérise la sonorité.

Cela donne aux théoriciens du jazz un langage qui transcende les conventions des symboles d'accords. Deux accords aux symboles différents peuvent appartenir à la même classe d'ensembles et donc partager le même contenu intervallique. Deux accords aux symboles semblables peuvent appartenir à des classes d'ensembles différentes. La théorie des ensembles révèle la sonorité réelle sous la notation.

**Les vecteurs d'intervalles comme mesures de sonorité :**

Le vecteur d'intervalles quantifie la « couleur » d'un accord. Un accord riche en ic3 et ic4 (tierces) sonne tertien. Un accord dominé par les ic5 sonne en quartes. Un accord riche en ic2 et ic6 sonne dense et dissonant. En lisant le vecteur d'intervalles d'un accord, vous pouvez prédire son caractère sonore sans même l'entendre.

C'est immédiatement utile aux guitaristes : pour choisir un voicing d'un accord ambigu, vous pouvez sélectionner le voicing dont le vecteur d'intervalles correspond à la sonorité voulue — ouverte et en quartes, dense et chromatique, ou quelque part entre les deux.

**OPTIC/K et équivalence des classes de hauteur :**

En théorie musicale géométrique (Callender, Quinn et Tymoczko, *Science*, 2008), les équivalences de conduite des voix sont décrites par les relations **OPTIC** :
- Équivalence d'**O**ctave : deux hauteurs à l'octave l'une de l'autre sont identiques.
- **P**ermutation : réordonner à l'intérieur d'une octave ne change pas l'identité.
- **T**ransposition : deux accords liés par un même intervalle sont équivalents.
- **I**nversion : des accords en miroir sont équivalents.
- **C**ardinalité : les doublures ne comptent pas.

Ce sont exactement les principes de la théorie des ensembles de classes de hauteur, exprimés un peu différemment. OPTIC rend explicite le fait que la théorie des ensembles n'a rien d'exotique — c'est la formalisation de la façon dont les musiciens ont toujours entendu les équivalences (un accord de Do majeur est « le même », qu'il soit disposé Do-Mi-Sol, Sol-Do-Mi ou Do-Mi-Sol-Do).

La relation **K** ajoute une couche supplémentaire (l'équivalence à l'appartenance à une classe d'ensembles près). Ensemble, OPTIC et K fournissent un cadre mathématique qui unifie l'analyse tonale de la conduite des voix et la théorie post-tonale des ensembles. Les deux traditions ne s'opposent pas — ce sont deux dialectes d'une même langue sous-jacente.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Tonalité de la pratique commune** | Le système harmonique de la musique savante occidentale d'environ 1600 à 1900, fondé sur l'harmonie fonctionnelle et les centres tonals |
| **Émancipation de la dissonance** | L'affirmation de Schoenberg, en 1908, selon laquelle les sonorités dissonantes n'ont pas besoin de se résoudre sur une consonance |
| **Atonalité** | Musique organisée sans centre tonal ni tonalité |
| **Atonalité libre** | Musique atonale organisée intuitivement par des cellules motiviques, la distribution des registres et la centralité de hauteur |
| **Sérialisme (dodécaphonique)** | Organisation systématique de la musique atonale fondée sur une série ordonnée des 12 classes de hauteur |
| **Classe de hauteur** | Une classe d'équivalence de hauteurs liées par l'octave (par exemple, tous les Do appartiennent à la classe de hauteur 0) |
| **Notation entière** | Représentation des classes de hauteur par les entiers 0-11 |
| **Forme normale** | L'ordonnancement le plus compact d'un ensemble de classes de hauteur |
| **Forme première** | Le représentant canonique d'une classe d'ensembles, équivalence par inversion comprise, transposé pour commencer sur 0 |
| **Classe d'intervalles (ic)** | Une classe d'équivalence d'intervalles (0-6) qui regroupe les intervalles liés par renversement |
| **Vecteur d'intervalles** | Une liste de 6 éléments qui compte les occurrences de chaque classe d'intervalles dans un ensemble |
| **Classe d'ensembles** | Un groupe d'ensembles de classes de hauteur liés par transposition et inversion, étiqueté par un nombre de Forte |
| **Nombre de Forte** | L'étiquette de catalogue d'Allen Forte pour une classe d'ensembles, au format cardinalité-ordinal (par exemple 3-11) |
| **Relation Z** | La relation entre des classes d'ensembles distinctes qui partagent le même vecteur d'intervalles |
| **Originale/Rétrograde/Inversion/Rétrograde de l'inversion (P/R/I/RI)** | Les quatre opérations sérielles appliquées à une série dodécaphonique |
| **Combinatorialité** | Propriété de certaines séries dont les hexacordes se combinent avec des formes transposées pour produire des agrégats |
| **Centralité de hauteur** | Mise en valeur structurelle de certaines hauteurs dans la musique atonale, sans fonction tonale |
| **Cellule motivique** | Un petit ensemble de classes de hauteur utilisé comme ADN structurel tout au long d'une composition atonale |

---

## Auto-évaluation

**1. Qu'entendait Schoenberg par « l'émancipation de la dissonance », et pourquoi fut-ce un tournant historique ?**
> Schoenberg a soutenu — dans sa musique dès 1908, puis explicitement dans son essai « Opinion or Insight? » de 1926 — que les sonorités dissonantes n'ont pas besoin de se résoudre sur des consonances — que la distinction entre consonance et dissonance est une convention historique, pas une loi acoustique. Ce fut un tournant, car cela levait la dernière contrainte de la tonalité de la pratique commune (l'obligation de résoudre la tension), ouvrant la voie à une composition atonale où n'importe quelle sonorité pouvait constituer un événement structurel stable.

**2. Calculez la forme première de l'ensemble {Ré, Fa, La, Do} (un accord de Ré mineur septième). Montrez la forme normale et une vérification par inversion.**
> Classes de hauteur : {2, 5, 9, 0} → ordre croissant {0, 2, 5, 9}. Rotations et étendues :
> - (0, 2, 5, 9) : étendue = 9
> - (2, 5, 9, 0+12=12) : étendue = 10
> - (5, 9, 12, 14) : étendue = 9
> - (9, 12, 14, 17) : étendue = 8 — la plus petite !
> Forme normale : [9, 0, 2, 5]. Transposez pour commencer sur 0 : soustrayez 9 → [0, 3, 5, 8]. Inversion : inversez {0, 2, 5, 9} → {0, 10, 7, 3}, ordre croissant {0, 3, 7, 10}. Normalisez-la aussi (ne vous contentez pas de la réordonner) : la rotation (7, 10, 12, 15) a la plus petite étendue (8), donc sa forme normale est [7, 10, 0, 3], transposée pour commencer sur 0 → [0, 3, 5, 8]. L'inversion donne le même résultat : cette classe d'ensembles est symétrique par inversion.
> **Forme première : (0358)** — classe d'ensembles 4-26, la sonorité de septième mineure / accord parfait mineur plus 7.

**3. Soit P0 = [0, 1, 4, 9, 5, 11, 2, 7, 6, 10, 3, 8] ; dérivez I0 (inversion commençant sur 0). Indiquez la formule utilisée.**
> Formule : I0[k] = (0 - P0[k]) mod 12 = (-P0[k]) mod 12.
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

**4. Qu'est-ce qu'une relation Z, et pourquoi est-elle importante en théorie post-tonale ?**
> Une relation Z est la propriété partagée par deux classes d'ensembles distinctes qui ont des vecteurs d'intervalles identiques mais ne sont liées ni par transposition ni par inversion. Elle est importante, car elle révèle que le contenu intervallique (quels intervalles sont présents) ne détermine pas de façon unique l'identité de la classe d'ensembles (quelles configurations de hauteurs produisent ces intervalles). Les ensembles en relation Z ont des sonorités très proches mais sont structurellement distincts, une symétrie profonde exploitée par des compositeurs comme Elliott Carter et Milton Babbitt.

**5. En quoi l'analyse par la théorie des ensembles jette-t-elle un pont entre la musique post-tonale et l'harmonie jazz ?**
> La théorie des ensembles abstrait les accords en ensembles de classes de hauteur et en classes d'ensembles, en passant outre les conventions des symboles d'accords. Un accord jazz complexe de dominante altérée peut être identifié par sa classe d'ensembles et caractérisé par son vecteur d'intervalles, ce qui révèle sa sonorité sous-jacente d'une manière que les symboles d'accords masquent. Cela permet aux analystes du jazz de comparer des voicings de qualités d'accords apparemment différentes, de reconnaître des sonorités communes et de comprendre les langages atonal et jazz comme des dialectes d'un même cadre de classes de hauteur plutôt que comme des systèmes opposés.

**Critères de réussite :** calculer la forme première d'un accord donné de 4 ou 5 notes, dériver I0 et R0 à partir d'un P0 donné, et expliquer la fonction structurelle d'une cellule motivique dans un contexte d'atonalité libre.

---

## Bases de recherche

- Théorie des ensembles de classes de hauteur formalisée par Allen Forte dans *The Structure of Atonal Music* (1973) ; les nombres de Forte restent le système de catalogage standard
- *Introduction to Post-Tonal Theory* de Joseph N. Straus (4e éd., 2016) est le manuel pédagogique de référence et la source des algorithmes de forme normale et de forme première
- *Serial Composition and Atonality* de George Perle (6e éd., 1991) fournit un ancrage historique et analytique à la technique dodécaphonique
- La théorie néo-riemannienne et les relations OPTIC étendent la théorie des ensembles vers l'analyse de la conduite des voix (Cohn, 2012 ; Tymoczko, *A Geometry of Music*, 2011)
- Références du répertoire de guitare : Henze *Royal Winter Music I & II* ; Britten *Nocturnal Op. 70* ; Takemitsu *All in Twilight* ; Ginastera *Sonata Op. 47*
- Les propres écrits de Schoenberg (*Style and Idea*, 1950) documentent l'émancipation de la dissonance dans ses propres mots
- Sources : Forte 1973, Straus 2016, Perle 1991, Tymoczko 2011, Cohn 2012, Schoenberg 1950
- État de croyance : T(0.85) F(0.03) U(0.08) C(0.04)
