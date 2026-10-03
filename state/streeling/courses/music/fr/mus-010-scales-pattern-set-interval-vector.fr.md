---
module_id: mus-010-scales-pattern-set-interval-vector
department: music
course: Formules de gammes, ensembles et vecteur d'intervalles diatonique
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-008-intervals-inversion-compound, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Formules de gammes, ensembles et vecteur d'intervalles diatonique — Ce que la gamme majeure a de rare

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Construire n'importe quelle gamme sur n'importe quelle tonique à partir de sa formule d'intervalles, et orthographier une gamme de sept notes avec une lettre par degré
- Distinguer la formule d'une gamme, son ensemble de classes de hauteurs et son vecteur de classes d'intervalles, et dire ce que chacun oublie
- Calculer les vecteurs des gammes majeure, pentatonique et par tons, et utiliser le théorème des notes communes pour dire combien de notes partagent deux tonalités
- Reconnaître la propriété de gamme profonde, la propriété de Myhill, la régularité maximale et l'engendrement par quintes, et dire lesquelles ont la gamme majeure, la pentatonique et la gamme par tons
- Retracer comment GA calcule ces propriétés, et où ses résultats dépendent de la transposition ou s'écartent des définitions

---

## 1. Une gamme comme formule d'intervalles

Une gamme énumère des notes dans l'ordre à l'intérieur d'une octave. Sa **formule d'intervalles** donne le nombre de demi-tons de chaque note à la suivante, en finissant par le pas qui ramène à l'octave, si bien que les pas font 12 au total.

| Gamme | Formule | Sur do |
|------|------|------|
| Majeure | 2 2 1 2 2 2 1 | do ré mi fa sol la si |
| Mineure naturelle | 2 1 2 2 1 2 2 | do ré mi♭ fa sol la♭ si♭ |
| Pentatonique majeure | 2 2 3 2 3 | do ré mi sol la |
| Par tons | 2 2 2 2 2 2 | do ré mi fa♯ sol♯ la♯ |

Écrite en tons (T) et demi-tons (½T), la formule majeure est T T ½T T T T ½T. L'article « Major scale » de Wikipédia note qu'« a major scale may be seen as two identical tetrachords separated by a whole tone » (une gamme majeure peut se voir comme deux tétracordes identiques séparés par un ton) : T T ½T, puis T, puis T T ½T.

Pour construire une gamme sur une autre tonique, on applique les mêmes pas à partir de cette tonique. Une gamme de sept notes prend alors une lettre par degré, et chaque altération découle de la lettre (MUS-007). Mi majeur s'écrit mi fa♯ sol♯ la si do♯ ré♯. Fa majeur s'écrit fa sol la si♭ do ré mi : le quatrième degré est un demi-ton au-dessus de la, et il s'écrit si♭, pas la♯, parce que la est déjà le troisième degré.

À la guitare, une formule jouée sur une seule corde est une liste d'écarts entre cases. Sur la corde de la, la formule majeure depuis la corde à vide donne les cases 0 2 4 5 7 9 11 12 : la si do♯ ré mi fa♯ sol♯ la. Les mêmes écarts depuis la case 3 donnent do majeur : cases 3 5 7 8 10 12 14 15.

### Exercice pratique

Construisez si♭ majeur et ré mineur naturel à partir de leurs formules, avec une lettre par degré.

> *Solution :* Si♭ majeur : si♭ do ré mi♭ fa sol la, pas 2 2 1 2 2 2 1. Ré mineur naturel : ré mi fa sol la si♭ do, pas 2 1 2 2 1 2 2. Dans les deux, chaque lettre apparaît une fois.

---

## 2. Formule, ensemble et tonique

Une formule ne dit pas où commencer ; une tonique fixe les notes. L'**ensemble de classes de hauteurs** garde les notes et oublie la tonique, l'ordre et les octaves (MUS-020) : do majeur est {0, 2, 4, 5, 7, 9, 11} avec do = 0.

Deux gammes peuvent partager un ensemble et différer par leur formule. La mineur naturel, la si do ré mi fa sol, contient les notes de do majeur. Sa formule, 2 1 2 2 1 2 2, est la formule majeure lue à partir de son sixième pas : les pas la–si, si–do, puis de do–ré à sol–la. Lire une formule à partir d'un autre pas donne un **mode** ; MUS-006 compte les modes comme des rotations.

Transposer une gamme ajoute le même nombre à chaque classe de hauteurs. Cela garde la formule et change l'ensemble : les douze gammes majeures sont douze ensembles différents. Une gamme qui s'envoie sur elle-même par une transposition en a moins : il n'existe que deux gammes par tons, {0, 2, 4, 6, 8, 10} et {1, 3, 5, 7, 9, 11} (MUS-006, MAT-022).

La suite de cette leçon étudie des propriétés de l'ensemble, que la tonique ne change pas : son vecteur d'intervalles, les tailles que prennent ses intervalles, et la régularité avec laquelle il se répartit sur l'octave.

### Exercice pratique

Quelle gamme majeure contient les notes de mi mineur naturel, et à partir de quel degré de cette gamme commence mi mineur ?

> *Solution :* Mi mineur naturel s'écrit mi fa♯ sol la si do ré, les notes de sol majeur. Mi est le sixième degré de sol majeur, et la formule de mi mineur, 2 1 2 2 1 2 2, est celle de sol majeur lue à partir de ce degré.

---

## 3. Le vecteur d'intervalles d'une gamme

Le **vecteur de classes d'intervalles** compte, pour chaque paire de notes d'un ensemble, la classe d'intervalle qui les sépare, de 1 (un demi-ton ou une septième majeure) à 6 (un triton) (MUS-020). Un ensemble de n notes a n(n − 1)/2 paires : 21 pour sept notes, 15 pour six, 10 pour cinq.

Pour la gamme majeure, comptez chaque classe sur do ré mi fa sol la si :
- **Classe 1**, demi-tons : mi–fa et si–do. **2.**
- **Classe 2**, tons : do–ré, ré–mi, fa–sol, sol–la et la–si. **5.**
- **Classe 3**, tierces mineures : ré–fa, mi–sol, la–do et si–ré. **4.**
- **Classe 4**, tierces majeures : do–mi, fa–la et sol–si. **3.**
- **Classe 5**, quintes justes : fa–do, do–sol, sol–ré, ré–la, la–mi et mi–si. **6.**
- **Classe 6**, le triton : si–fa. **1.**

Le total est 21, et le vecteur est <2 5 4 3 6 1>.

| Gamme | Notes | Paires | Vecteur |
|------|------|------|------|
| Majeure | do ré mi fa sol la si | 21 | <2 5 4 3 6 1> |
| Mineure harmonique | la si do ré mi fa sol♯ | 21 | <3 3 5 4 4 2> |
| Pentatonique majeure | do ré mi sol la | 10 | <0 3 2 1 4 0> |
| Par tons | do ré mi fa♯ sol♯ la♯ | 15 | <0 6 0 6 0 3> |

La pentatonique n'a ni demi-ton ni triton ; MUS-006 calcule le même vecteur pour la pentatonique mineure. Dans la gamme par tons, chaque note a un ton de chaque côté et une tierce majeure de chaque côté, ce qui fait six paires de classe 2 et six de classe 4. Ses trois tritons sont do–fa♯, ré–sol♯ et mi–la♯, et elle n'a aucune classe d'intervalle impaire.

### Exercice pratique

Calculez le vecteur de la gamme de six notes do ré mi fa sol la.

> *Solution :* Quinze paires. Classe 1 : mi–fa. Classe 2 : do–ré, ré–mi, fa–sol et sol–la. Classe 3 : ré–fa, mi–sol et la–do. Classe 4 : do–mi et fa–la. Classe 5 : do–fa, do–sol, ré–sol, ré–la et mi–la. Aucun triton, puisque si manque. Le vecteur est <1 4 3 2 5 0>, et ses composantes font 15 au total.

---

## 4. Gammes profondes et notes communes

Les six composantes de <2 5 4 3 6 1> sont six nombres différents. L'article « Common tone (scale) » de Wikipédia appelle cela la **propriété de gamme profonde** (deep scale property) : « containing each interval class a unique number of times » (contenir chaque classe d'intervalle un nombre de fois qui n'appartient qu'à elle). Le vecteur de la pentatonique répète 0, celui de la mineure harmonique répète 3 et 4, et celui de la gamme par tons répète 0 et 6 : aucune de ces gammes n'est profonde.

**Le théorème des notes communes.** Transposez un ensemble de n demi-tons. Une note b de l'ensemble transposé vaut a + n pour une note a de l'ensemble, et b appartient aussi à l'ensemble de départ exactement quand l'ensemble contient l'intervalle qui monte de n demi-tons depuis a. Le nombre de notes communes est donc le nombre de telles paires :
- pour n de 1 à 5, chaque paire est un intervalle de classe n, et le nombre est la composante du vecteur pour la classe n ;
- pour n de 7 à 11, chaque paire est un intervalle de classe 12 − n ;
- pour le triton, n = 6, chaque triton compte depuis ses deux extrémités, puisque a + 6 + 6 = a : si monte à fa et fa monte à si. Le nombre est le double de la composante du vecteur.

Wikipédia énonce le théorème pour la gamme diatonique : « However many times an interval class occurs in a diatonic scale is the number of tones common both to the original scale and a scale transposed by that particular interval class. » (Le nombre de fois qu'une classe d'intervalle apparaît dans une gamme diatonique est le nombre de notes communes à la gamme de départ et à la gamme transposée de cette classe d'intervalle.) Pour do majeur :

| Transposition (demi-tons) | Tonalités | Notes communes |
|------|------|------|
| 0 | do | 7 |
| 1 ou 11 | ré♭, si | 2 |
| 2 ou 10 | ré, si♭ | 5 |
| 3 ou 9 | mi♭, la | 4 |
| 4 ou 8 | mi, la♭ | 3 |
| 5 ou 7 | fa, sol | 6 |
| 6 | fa♯ | 2 : si, et fa, écrit mi♯ en fa♯ majeur |

Les deux voisines de do sur le cycle des quintes, fa et sol, gardent six notes : passer de do majeur à sol majeur ne change que fa en fa♯, un doigt déplacé d'une case. Wikipédia : « Six of seven possible common tones are shared by closely related keys » (les tonalités voisines partagent six des sept notes communes possibles). Comme la gamme est profonde, les transpositions de 1 à 5 demi-tons gardent cinq nombres de notes différents, les mêmes vers le haut ou vers le bas.

La ligne du triton demande de la prudence. Wikipédia donne au triton 1 note commune, « as there is only one tritone in a diatonic scale » (puisqu'il n'y a qu'un triton dans une gamme diatonique), et son tableau place si pour fa♯ majeur et fa pour sol♭ majeur sur deux lignes séparées. Comptées en classes de hauteurs, do majeur et fa♯ majeur partagent à la fois si et fa ; fa♯ majeur écrit fa mi♯. Chaque triton compte depuis ses deux extrémités. Cela fait deux notes, autant qu'une transposition d'un demi-ton ; le 1 de Wikipédia ne vaut que pour les notes écrites de la même façon. Le nombre doublé du triton peut répéter un autre nombre : la propriété de gamme profonde ne garantit des nombres différents que pour les classes d'intervalles 1 à 5.

La gamme par tons montre le cas opposé : « every even transposition of the whole tone scale is identical with the original and every odd transposition has no common tones whatsoever » (toute transposition paire de la gamme par tons est identique à l'originale, et toute transposition impaire n'a aucune note commune) (Wikipédia, « Common tone (scale) »).

**Quels ensembles sont profonds ?** Six nombres entiers différents font au moins 0 + 1 + 2 + 3 + 4 + 5 = 15, donc un ensemble profond a au moins 15 paires, et par conséquent au moins six notes. Un décompte sur les 4096 ensembles de classes de hauteurs trouve 48 ensembles profonds, douze transpositions dans chacune de quatre classes d'ensembles :

| Classe de Forte | Exemple | Vecteur | Une chaîne de |
|------|------|------|------|
| 6-1 | do do♯ ré mi♭ mi fa | <5 4 3 2 1 0> | demi-tons |
| 6-32 | do ré mi fa sol la | <1 4 3 2 5 0> | quintes, de fa à mi |
| 7-1 | do do♯ ré mi♭ mi fa fa♯ | <6 5 4 3 2 1> | demi-tons |
| 7-35 | do ré mi fa sol la si | <2 5 4 3 6 1> | quintes, de fa à si |

Parmi les ensembles de sept notes, seuls la gamme diatonique et le segment chromatique de sept notes sont donc profonds. L'article « Common tone (scale) » de Wikipédia énonce la règle ainsi : « In twelve-tone equal temperament, all scales with the deep scale property can be generated with any interval coprime with twelve » (dans le tempérament égal à douze sons, toutes les gammes qui ont la propriété de gamme profonde peuvent être engendrées par n'importe quel intervalle premier avec douze). Lue avec le tableau, chaque gamme profonde est une chaîne d'un seul de ces intervalles, pas de chacun d'eux : le demi-ton ou la quinte, les deux seuls au renversement près. Multiplier chaque classe de hauteurs par 5, l'opération que MUS-020 appelle M5, échange les nombres des classes 1 et 5 : elle envoie chaque ligne chromatique du tableau sur la ligne de quintes de même taille.

### Exercice pratique

Combien de notes do majeur et mi♭ majeur partagent-ils, et lesquelles ?

> *Solution :* Mi♭ est 3 demi-tons au-dessus de do, et la gamme majeure a quatre intervalles de classe 3, donc elles partagent quatre notes : do, ré, fa et sol. Mi♭ majeur remplace mi, la et si par mi♭, la♭ et si♭.

---

## 5. Deux tailles par pas, et répartition régulière

Un **intervalle générique** « is the number of scale steps between notes of a collection or scale » (est le nombre de pas de la gamme entre deux notes d'une collection ou d'une gamme) ; un **intervalle spécifique** est le nombre de demi-tons (Wikipédia, « Generic and specific intervals »). Dans la gamme majeure, une tierce, deux pas, est une tierce mineure ou une tierce majeure : 3 ou 4 demi-tons.

| Intervalle générique (pas) | 1 | 2 | 3 | 4 | 5 | 6 |
|------|------|------|------|------|------|------|
| Majeure | 1, 2 | 3, 4 | 5, 6 | 6, 7 | 8, 9 | 10, 11 |
| Pentatonique majeure | 2, 3 | 4, 5 | 7, 8 | 9, 10 | | |
| Par tons | 2 | 4 | 6 | 8 | 10 | |

- La **propriété de Myhill** consiste à avoir « exactly two specific intervals for every generic interval » (exactement deux intervalles spécifiques pour chaque intervalle générique) (Wikipédia, « Generic and specific intervals »). Les gammes majeure et pentatonique l'ont ; la gamme par tons, avec une seule taille par pas, ne l'a pas.
- La **régularité maximale** (maximal evenness, Clough et Douthett, 1991) est une autre condition : chaque intervalle générique prend une seule taille ou deux tailles consécutives, de sorte que les notes soient « spread out as much as possible » (réparties autant que possible) (Wikipédia, « Maximal evenness »). Les gammes majeure, pentatonique et par tons sont maximalement régulières ; la mineure harmonique ne l'est pas, puisque ses secondes font 1, 2 et 3 demi-tons. Aucune des deux propriétés n'entraîne l'autre. La gamme par tons est maximalement régulière sans avoir la propriété de Myhill, et le segment chromatique de sept notes de do à fa♯ du §4 a la propriété de Myhill sans être maximalement régulier : ses secondes font 1 ou 6 demi-tons, deux tailles mais non consécutives.
- Une **collection engendrée** est « formed by repeatedly adding a constant interval in integer notation, the generator » (formée en ajoutant de façon répétée un intervalle constant en notation entière, le générateur) (Wikipédia, « Generated collection »). La gamme majeure est une chaîne de sept notes reliées par six quintes : « F-C-G-D-A-E-B » (fa-do-sol-ré-la-mi-si). Une chaîne est **bien formée** quand le générateur couvre toujours le même nombre de pas : dans la gamme majeure, chaque quinte de la chaîne couvre 4 pas. « The major and minor pentatonic scales are also well formed. » (Les gammes pentatoniques majeure et mineure sont aussi bien formées.) Les six notes fa do sol ré la mi donnent do ré mi fa sol la, dont les pas sont 2 2 1 2 2 3 : une quinte couvre 4 pas de do à sol mais 3 de fa à do, donc cette chaîne est engendrée et n'est pas bien formée. L'article « Maximal evenness » de Wikipédia lie la bonne formation à la propriété de Myhill, « a scale with Myhill's property is said to be a well-formed scale » (une gamme qui a la propriété de Myhill est dite bien formée), et dit que la gamme par tons « is not well-formed since each generic interval comes in only one size » (n'est pas bien formée puisque chaque intervalle générique n'a qu'une taille). Son article « Generated collection » appelle la même gamme une « degenerate well-formed collection » (collection bien formée dégénérée), dans laquelle chaque pas est le générateur. Pour les ensembles de deux notes ou plus, les chaînes dégénérées mises à part, bonne formation et propriété de Myhill veulent dire la même chose.

| Gamme | Profonde | Propriété de Myhill | Maximalement régulière | Engendrée |
|------|------|------|------|------|
| Majeure | oui | oui | oui | oui, sept notes en quintes |
| Pentatonique majeure | non | oui | oui | oui, cinq notes en quintes |
| Par tons | non | non | oui | dégénérée, par tons |
| Mineure harmonique | non | non | non | non |
| do ré mi fa sol la | oui | non | non | oui, six notes en quintes |

De ces cinq gammes, seule la gamme majeure a les quatre propriétés. La **propriété de Rothenberg** (Rothenberg propriety) ajoute un test : un intervalle qui couvre plus de pas ne devrait jamais être plus petit qu'un intervalle qui en couvre moins. La gamme majeure le passe, mais le triton est à la fois une quarte, fa–si, et une quinte, si–fa, si bien que l'article « Rothenberg propriety » de Wikipédia la dit propre mais « not strictly proper because the three step intervals and the four step intervals share an interval size (the tritone) » (pas strictement propre, parce que les intervalles de trois pas et ceux de quatre pas partagent une taille, le triton) ; « the major pentatonic scale is strictly proper » (la pentatonique majeure est strictement propre).

Ce sont des faits de structure. Ils ne prouvent pas que la gamme majeure sonne équilibrée ; ils montrent ce qu'elle a de rare parmi les 4096 ensembles.

### Exercice pratique

La mineure harmonique de la a-t-elle la propriété de Myhill ? Est-elle maximalement régulière ?

> *Solution :* Ni l'un ni l'autre. Ses secondes la–si, 2 demi-tons, si–do, 1, et fa–sol♯, 3 : un même intervalle générique en trois tailles. L'article « Maximal evenness » de Wikipédia donne cet exemple.

---

## 6. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). Cette leçon documente ce code et ne le modifie pas. Elle n'a exécuté ni GA ni ses tests : les décomptes ci-dessous viennent d'une transcription Python, ligne par ligne, des méthodes citées. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA, à `0843879`. Le cours music-theory-ga de Learn compile une version antérieure de GA, `a826864`, qui a `IsDeepScale` mais pas `ScaleStructuralProperties`. Sa leçon 4 [cite déjà `IsDeepScale`](https://github.com/spareilleux/learn/blob/0c918c8206dc9dda0241d097e6b0c65e897c92ec/src/content/docs/music-theory-ga/04-set-classes.mdx#L77-L81) et la définition d'une gamme profonde donnée par Wikipédia ; cette section va plus loin, jusqu'aux notes communes et aux autres propriétés.

**Une gamme se construit à partir de notes.** [`Scale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L37-L45) prend une liste de notes et [calcule leur ensemble de classes de hauteurs et leur vecteur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L42-L43). Ses gammes nommées sont écrites en toutes lettres : [`Major`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L53) vaut « C D E F G A B », [`MajorPentatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L57) « C D E G A », [`WholeTone`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L60) « C D E F# G# A# » et [`Minor.Natural`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L125) « A B C D E F G », en noms de notes anglais. Un test vérifie que [le vecteur de la gamme majeure est <2 5 4 3 6 1>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L19-L21), et un autre que [la mineur et do majeur partagent un ensemble](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L24-L27), comme au §2. La gamme expose aussi [six propriétés structurelles](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L85-L90), et le serveur MCP de GA les affiche pour un identifiant de gamme à 12 bits dans son [outil `GaScaleProperties`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L168-L194).

**`IsDeepScale` est juste, et aucun code n'y fait référence.** [`IsDeepScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L99) vérifie que les six valeurs du vecteur sont distinctes, et le vecteur contient toujours six valeurs, [zéros compris](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L45-L72), si bien que les deux zéros de la pentatonique comptent comme une répétition. Transcrite sur les 4096 ensembles, elle est vraie pour exactement les 48 ensembles du §4. Sa documentation [renvoie au théorème des notes communes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L89-L98). Aucun autre fichier de code de GA ne la nomme, et aucun test ne la vérifie.

**La propriété de Myhill et la propriété de Rothenberg suivent les définitions.** [`HasMyhillProperty`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L40-L68) rassemble les tailles de chaque intervalle générique et en exige exactement deux ; transcrite, elle vaut vrai pour les gammes majeure et pentatonique et faux pour la gamme par tons. [`GetRothenbergPropriety`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L76-L123) compare la plus grande taille de chaque intervalle générique à la plus petite taille de chaque intervalle plus grand ; transcrite, elle renvoie `Proper` pour la gamme majeure et `StrictlyProper` pour la pentatonique, comme Wikipédia. Le test de Myhill s'appelle [`Dorian_HasMyhillProperty_ReturnsTrue`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/ScaleStructuralPropertiesTests.cs#L10-L16) et construit `Scale.Major` ; son commentaire dit « Major / Dorian (1709) », mais 1709 est l'identifiant de do dorien, un autre ensemble que le 2741 de do majeur. Les cinq tests du fichier construisent tous `Scale.Major`, si bien qu'aucun ne vérifie une gamme pour laquelle `HasMyhillProperty` ou `IsWellFormed` est faux.

**`IsWellFormed` teste l'engendrement, pas la bonne formation.** Le résumé de la méthode définit une gamme bien formée comme une gamme [« generated by repeatedly stacking a single generator interval mod 12 »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L151-L154) (engendrée en empilant de façon répétée un seul intervalle générateur modulo 12), et la [méthode](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L163-L187) accepte toute chaîne d'un seul intervalle. C'est la collection engendrée du §5. Transcrite sur les 4096 ensembles, 89 ensembles passent `IsWellFormed` sans avoir la propriété de Myhill :
- 13 ensembles d'au plus une note : l'ensemble vide et les 12 notes seules ;
- 16 divisions égales de l'octave : le triton, la triade augmentée, la septième diminuée, la gamme par tons et le total chromatique, que Wikipédia appelle dégénérées ;
- 60 chaînes de quintes de 4, 6, 8, 9 ou 10 notes, comme do ré sol la et le do ré mi fa sol la du §5, qui ont chacune un intervalle générique en trois tailles.

Aucun ensemble n'a la propriété de Myhill en échouant à `IsWellFormed`. Pour la gamme majeure, la méthode renvoie le générateur 5, le premier qui fonctionne dans l'ordre de 1 à 11 : la chaîne de quartes si mi la ré sol do fa, qui est la chaîne de quintes du §5 lue à l'envers.

**Le score de régularité dépend de la transposition.** [`GetMaximalEvennessDiscrepancy`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L129-L149) prend les classes de hauteurs d'un ensemble de n notes dans l'ordre croissant depuis do, les compare aux points 0, 12 / n, 2 × 12 / n et ainsi de suite, et renvoie la moyenne quadratique des écarts. Son résumé cite Clough et Douthett et promet [« 0.0 for perfectly even sets like Whole Tone or Augmented »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L125-L128) (0.0 pour les ensembles parfaitement réguliers comme la gamme par tons ou augmentée). Transcrit, arrondi à quatre décimales :
- la gamme par tons obtient 0,0000 sur do et 1,0000 sur do♯, et la triade augmentée 0,0000 sur do et 1,0000 sur do♯ ;
- le [`Scale.Augmented`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L61) de GA, do ré♯ mi sol sol♯ si, est la gamme augmentée de six notes, pas la triade, et obtient 0,7071 ;
- les douze gammes majeures obtiennent de 0,2857, si♭ majeur, à 1,1780, fa♯ majeur ; do majeur obtient 0,4041.

Pour Clough et Douthett, la régularité maximale est une propriété par oui ou non, et les douze gammes majeures l'ont toutes. D'après le score de GA, 472 ensembles de sept notes qui ne sont pas maximalement réguliers sortent plus réguliers que fa♯ majeur. La description de l'outil propose elle-même [« 1709 for Dorian or 2741 for Major »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L174) (1709 pour le dorien ou 2741 pour le majeur) : les deux identifiants contiennent les notes de si♭ majeur et de do majeur, une même gamme dans deux transpositions, et obtiennent 0,2857 et 0,4041. Aucun test ne vérifie le score.

Corriger quoi que ce soit ici revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

Que renvoient `IsWellFormed` et `HasMyhillProperty` de GA pour do ré sol la, et pourquoi ne sont-elles pas d'accord ?

> *Solution :* `IsWellFormed` renvoie vrai avec le générateur 5 : depuis la, ajouter 5 demi-tons trois fois donne la ré sol do. `HasMyhillProperty` renvoie faux : les secondes do–ré, ré–sol, sol–la et la–do font 2, 5, 2 et 3 demi-tons, trois tailles. L'ensemble est une chaîne d'un seul intervalle, ce qui est tout ce que vérifie `IsWellFormed`, mais la quarte couvre deux pas de la à ré et un de ré à sol, donc la chaîne n'est pas bien formée.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA. L'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`, puisque `ScaleStructuralProperties` n'existe pas à `a826864`. Rien dans cette section n'est une mesure :
- les prédictions viennent des §3 à §6 et sont écrites avant toute exécution ;
- les décomptes et les scores viennent de la transcription Python du §6 ;
- une version ultérieure de cette leçon rapportera les résultats.

Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Trois vecteurs.** Afficher `IntervalClassVector` et `IsDeepScale` pour `Scale.Major`, `Scale.MajorPentatonic` et `Scale.WholeTone`. Prédiction : <2 5 4 3 6 1> et vrai, <0 3 2 1 4 0> et faux, <0 6 0 6 0 3> et faux.
2. **Le recensement des gammes profondes.** Pour chaque ensemble de classes de hauteurs, lire `IsDeepScale`, et pour chaque ensemble profond, `IsWellFormed` et son générateur. Prédiction : 48 ensembles profonds, 24 de six notes dans les classes 6-1 et 6-32 et 24 de sept notes dans les classes 7-1 et 7-35 ; tous passent `IsWellFormed`, avec le générateur 1 pour les classes chromatiques et 5 pour les autres.
3. **Le théorème des notes communes.** Pour chaque ensemble non vide et chaque n de 1 à 11, compter les classes de hauteurs communes à l'ensemble et à sa transposition de n, et comparer au vecteur, doublé pour n = 6. Prédiction : aucune exception sur les 4095 ensembles ; pour do majeur, les nombres pour n = 1 à 11 sont 2 5 4 3 6 2 6 3 4 5 2.
4. **Le score de régularité.** Appeler `GetMaximalEvennessDiscrepancy` sur les douze gammes majeures et les deux gammes par tons. Prédiction, à quatre décimales :

   | Gamme majeure | Score | Gamme majeure | Score |
   |------|------|------|------|
   | do | 0,4041 | fa♯ | 1,1780 |
   | do♯ | 0,5151 | sol | 0,5151 |
   | ré | 0,6389 | la♭ | 0,4041 |
   | mi♭ | 0,3194 | la | 0,7693 |
   | mi | 0,9035 | si♭ | 0,2857 |
   | fa | 0,3194 | si | 1,0400 |

   Les gammes par tons obtiennent 0,0000 sur do et 1,0000 sur do♯, et 472 ensembles de sept notes qui ne sont pas maximalement réguliers obtiennent moins de 1,1780.
5. **Engendrée ou bien formée.** Sur les 4096 ensembles, ensemble vide compris, compter les ensembles pour lesquels `IsWellFormed` est vrai et `HasMyhillProperty` faux, puis l'inverse. Prédiction : 89 et 0.

### Exercice pratique

L'étape 4 prédit exactement 1,0000 pour la gamme par tons sur do♯. Pourquoi ?

> *Solution :* Ses notes dans l'ordre croissant sont 1, 3, 5, 7, 9 et 11, et les points auxquels on les compare sont 0, 2, 4, 6, 8 et 10. Chaque note est à un demi-ton de son point, donc chaque écart au carré vaut 1, et la moyenne quadratique de six 1 vaut 1.

---

## 8. Pièges courants

- **Prendre la formule pour l'ensemble.** La mineur naturel et do majeur partagent un ensemble, pas une formule.
- **Écrire avec la mauvaise lettre.** Fa majeur a si♭, pas la♯ : une lettre par degré.
- **Prendre profonde pour régulière.** La gamme par tons est parfaitement régulière et n'est pas profonde ; l'ensemble profond do ré mi fa sol la n'est pas maximalement régulier.
- **Compter le triton une seule fois.** En classes de hauteurs, une transposition d'un triton garde deux fois plus de notes que l'ensemble n'a de tritons : do majeur et fa♯ majeur partagent si et fa.
- **Lire l'`IsWellFormed` de GA comme la bonne formation de Carey et Clampitt.** Il vérifie seulement qu'un ensemble est une chaîne d'un seul intervalle.
- **Comparer les scores de régularité de GA d'une transposition à l'autre.** Le score se mesure depuis do : si♭ majeur et fa♯ majeur sont aussi réguliers l'un que l'autre et obtiennent 0,2857 et 1,1780.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Formule d'intervalles** | Les demi-tons de chaque note d'une gamme à la suivante, jusqu'à l'octave, comme 2 2 1 2 2 2 1 |
| **Ensemble de classes de hauteurs** | Les notes d'une gamme sans tonique, ordre ni octave, comme {0, 2, 4, 5, 7, 9, 11} |
| **Vecteur de classes d'intervalles** | Le nombre de paires de notes dans chaque classe d'intervalle de 1 à 6, comme <2 5 4 3 6 1> |
| **Gamme profonde** | Un ensemble dont le vecteur contient six nombres différents : en douze sons, les classes 6-1, 6-32, 7-1 et 7-35 |
| **Théorème des notes communes** | Une transposition de n demi-tons garde autant de notes que le vecteur en compte pour la classe d'intervalle de n, le double pour le triton |
| **Intervalle générique** | Le nombre de pas de la gamme entre deux notes |
| **Propriété de Myhill** | Chaque intervalle générique prend exactement deux tailles |
| **Maximalement régulière** | Chaque intervalle générique prend une seule taille ou deux tailles consécutives |
| **Collection engendrée** | Un ensemble formé en empilant un seul intervalle, comme la chaîne de quintes fa do sol ré la mi si |
| **Bien formée** | Engendrée, avec un générateur qui couvre toujours le même nombre de pas ; pour les chaînes de deux notes ou plus qui ne sont pas dégénérées, équivaut à la propriété de Myhill |

---

## Auto-évaluation

**1. Construisez mi♭ majeur à partir de sa formule et donnez son ensemble de classes de hauteurs.**
> Elle s'écrit mi♭ fa sol la♭ si♭ do ré, avec les pas 2 2 1 2 2 2 1. Avec do = 0, son ensemble est {0, 2, 3, 5, 7, 8, 10}.

**2. Pourquoi une modulation de do majeur à sol majeur change-t-elle une note, alors que do majeur et fa♯ majeur en partagent encore deux ?**
> Sol est une transposition de 7 demi-tons, classe d'intervalle 5, et la gamme majeure contient six intervalles de classe 5, donc six notes restent et une change, fa en fa♯. Fa♯ est une transposition d'un triton ; la gamme a un triton, si–fa, qui compte depuis ses deux extrémités, donc si et fa restent. Écrit en fa♯ majeur, fa devient mi♯.

**3. La pentatonique majeure est-elle profonde ? A-t-elle la propriété de Myhill ? Est-elle maximalement régulière ?**
> Elle n'est pas profonde : son vecteur <0 3 2 1 4 0> contient deux fois 0. Elle a la propriété de Myhill, puisque chaque intervalle générique prend deux tailles : 2 ou 3, 4 ou 5, 7 ou 8, 9 ou 10. Elle est maximalement régulière, puisque chaque paire de tailles est consécutive.

**4. Dans GA à `5c3a52a`, que renvoie `GetMaximalEvennessDiscrepancy` pour do majeur et pour si♭ majeur, et que montre la différence ?**
> 0,4041 et 0,2857, à quatre décimales. Les deux gammes ont la même formule et sont aussi régulières l'une que l'autre ; le score diffère parce qu'il mesure chaque ensemble depuis do.

**Critères de réussite :** Construire et orthographier une gamme à partir de sa formule sur n'importe quelle tonique. Calculer le vecteur d'une gamme et s'en servir pour compter les notes communes, triton compris. Dire lesquelles des propriétés profonde, de Myhill, maximalement régulière et engendrée une gamme possède. Dire ce que GA calcule pour chacune, et où son résultat dépend de la transposition ou s'écarte de la définition.

---

## Bases de recherche

- Wikipédia, « Major scale » : les deux tétracordes, et la régularité maximale.
- Wikipédia, « Interval vector » : la définition, et la propriété de gamme profonde de la gamme majeure et de ses modes.
- Wikipédia, « Common tone (scale) » : le théorème des notes communes et son tableau, les tonalités voisines, la propriété de gamme profonde, l'engendrement par un intervalle premier avec douze, et les transpositions de la gamme par tons ; d'après Johnson, *Foundations of Diatonic Theory*, 2003, et Gamer, 1967.
- Wikipédia, « Generic and specific intervals » : intervalles génériques et spécifiques, et propriété de Myhill.
- Wikipédia, « Maximal evenness » : la définition de Clough et Douthett, la mineure harmonique, la gamme par tons, et la propriété de Myhill comme bonne formation.
- Wikipédia, « Generated collection » : la chaîne de quintes, les collections bien formées et dégénérées, d'après Carey et Clampitt, 1989.
- Wikipédia, « Rothenberg propriety » : la gamme majeure propre mais pas strictement, la pentatonique strictement propre.
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §6 renvoie à sa ligne.
- Learn, leçon 4 de music-theory-ga au commit `0c918c8206dc9dda0241d097e6b0c65e897c92ec` : son exposé d'`IsDeepScale`.
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre.
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue.
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
