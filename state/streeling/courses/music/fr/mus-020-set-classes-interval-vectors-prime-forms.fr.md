---
module_id: mus-020-set-classes-interval-vectors-prime-forms
department: music
course: Classes d'ensembles, vecteurs d'intervalles, relation Z et formes premières
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-002-beyond-tonality]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Classes d'ensembles, vecteurs d'intervalles, relation Z et formes premières — Deux tassements, un catalogue

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Regrouper des ensembles de classes de hauteurs par transposition seule, puis par transposition et inversion, et déduire de la symétrie d'un ensemble combien d'ensembles compte sa classe
- Calculer un vecteur de classes d'intervalles, montrer que toute une classe d'ensembles le partage, et dire ce que la multiplication par 5 lui fait
- Trouver un ordre normal et une forme première selon la règle de Forte et selon celle de Rahn, et nommer les six classes d'ensembles sur lesquelles elles divergent
- Expliquer pourquoi le plus petit nombre de 12 bits parmi les 24 formes d'un ensemble est sa forme première selon la règle de Rahn
- Compter les classes d'ensembles avec le lemme de Burnside
- Énoncer le théorème du complémentaire et le théorème de l'hexacorde, et s'en servir avec la relation M pour expliquer comment se répartissent les 23 paires en relation Z et comment certaines d'entre elles sont reliées
- Lire un numéro de Forte, et le distinguer d'un ordinal qui lui ressemble seulement
- Retracer ce que GA calcule pour chacun de ces points, et où ses noms, sa documentation et ses tests disent autre chose

---

## 1. Ensembles de classes de hauteurs et leurs symétries

Numérotez les classes de hauteurs de do = 0 à si = 11, comme le fait MUS-002. Un accord, une gamme ou les notes d'une mélodie deviennent alors un **ensemble de classes de hauteurs**, un sous-ensemble des 12 classes de hauteurs. Il y en a 2¹² = 4 096, de l'ensemble vide à l'agrégat complet.

Deux sortes d'opérations déplacent un ensemble sans changer sa forme. La **transposition** Tn ajoute n à chaque classe de hauteurs, modulo 12. L'**inversion suivie d'une transposition**, TnI (In en abrégé), envoie chaque x sur n − x. Ensemble, elles forment 24 opérations. T2 transforme do majeur {0, 4, 7} en ré majeur {2, 6, 9}. I0 le transforme en {0, 8, 5}, fa mineur, et I7 en {7, 3, 0}, do mineur : un miroir qui échange do et sol et change mi en mi♭.

Les ensembles reliés par une transposition forment un **type Tn** ; les ensembles reliés par une transposition ou une inversion forment une **classe d'ensembles**. Les 4 096 ensembles se répartissent en 352 types Tn et 224 classes d'ensembles. Un accord parfait majeur et un accord parfait mineur sont deux types Tn d'une même classe d'ensembles, que le catalogue de Forte (§6) étiquette 3-11.

Le nombre d'ensembles d'une classe dépend de la symétrie de ses membres. Si k des 24 opérations envoient un ensemble sur lui-même, sa classe compte 24 / k ensembles. Seule T0 envoie un accord parfait majeur sur lui-même, donc sa classe compte 24 ensembles : les 12 accords parfaits majeurs et les 12 mineurs. L'accord parfait augmenté do mi sol♯ est envoyé sur lui-même par T0, T4, T8 et trois inversions, donc sa classe compte 24 / 6 = 4 ensembles. La classe de l'accord de septième diminuée compte 3 ensembles, celle de la gamme par tons 2, et celle de l'agrégat 1.

### Exercice pratique

La classe de C7, do mi sol si♭, compte 24 ensembles ; celle de Cmaj7, do mi sol si, seulement 12. Pourquoi ?

> *Solution :* Seule T0 envoie C7 sur lui-même, donc sa classe compte 24 ensembles : les 12 septièmes de dominante et leurs 12 inversions, les septièmes semi-diminuées (I0 transforme {0, 4, 7, 10} en {0, 8, 5, 2}, ré fa la♭ do, Dø7). Cmaj7 est sa propre inversion : I11 échange do et si, et mi et sol. Deux des 24 opérations l'envoient sur lui-même, donc sa classe compte 24 / 2 = 12 ensembles, les septièmes majeures.

---

## 2. Vecteurs de classes d'intervalles

Prenez chaque paire de notes d'un ensemble, mesurez l'intervalle qui les sépare en demi-tons, et ramenez-le à une **classe d'intervalles** de 1 à 6 : un intervalle et son renversement, comme une quarte et une quinte, forment une seule classe. Les six décomptes forment le **vecteur de classes d'intervalles** de l'ensemble. Un ensemble de n notes a n(n − 1)/2 paires, et la somme des décomptes vaut ce nombre. Do majeur a une tierce mineure (mi–sol), une tierce majeure (do–mi) et une quinte (do–sol) : <001110>. C7 a <012111>, Cmaj7 <101220>, l'accord de septième diminuée <004002> et la gamme majeure <254361>.

Tous les ensembles d'une classe d'ensembles ont le même vecteur. Une transposition conserve la différence entre deux notes quelconques. Une inversion change une différence d en −d, qui est la même classe d'intervalles. Ainsi do majeur et do mineur partagent <001110>, et C7 et Cø7 partagent <012111>. La réciproque est fausse : deux ensembles peuvent partager un vecteur sans partager une classe (§5).

Multiplier chaque classe de hauteurs par 5, l'opération **M5**, ne fait pas partie des 24 opérations du §1, mais son effet sur le vecteur est simple. Elle multiplie chaque intervalle par 5 : 1 devient 5 ; 2 devient 10, classe d'intervalles 2 ; 3 devient 15, c'est-à-dire 3 ; 4 devient 20, c'est-à-dire 8, classe d'intervalles 4 ; 5 devient 25, c'est-à-dire 1 ; et 6 devient 30, c'est-à-dire 6. M5 échange donc les décomptes des classes d'intervalles 1 et 5 et garde les autres. Le pentacorde chromatique do do♯ ré mi♭ mi, <432100>, devient do fa si♭ mi♭ la♭, <032140> : un empilement de quartes, la gamme pentatonique. M5 envoie 132 des 224 classes d'ensembles dans une autre classe : elle envoie do majeur sur do la♭ si, un membre de la classe notée (014) au §3. M7 est M5 suivie de I0, puisque 7 = −5 mod 12.

### Exercice pratique

Calculez le vecteur de do mi sol la, qui est à la fois C6 et Am7.

> *Solution :* Six paires, par classe d'intervalles : do–mi (4), do–sol (5), do–la (3), mi–sol (3), mi–la (5) et sol–la (2). Une fois la classe 2, deux fois la classe 3, une fois la classe 4 et deux fois la classe 5 : <012120>.

---

## 3. Ordre normal et forme première : deux façons de tasser

Pour nommer une classe d'ensembles, les théoriciens choisissent un membre et l'écrivent dans un ordre standard. L'**ordre normal** d'un ensemble est la rotation de ses notes, rangées par ordre croissant autour de l'octave, dont l'étendue de la première à la dernière note est la plus petite. Quand des rotations sont à égalité, on les compare par leurs intervalles depuis la première note, et l'égalité peut se trancher par l'un ou l'autre bout :

- **Forte (1973)** tasse vers la gauche : le plus petit intervalle de la première note à la deuxième, puis à la troisième, et ainsi de suite.
- **Rahn (1980)** tasse depuis la droite : le plus petit intervalle de la première note à l'avant-dernière, puis à celle d'avant, et ainsi de suite.

La **forme première** compare les ordres normaux de l'ensemble et de son inversion, tous deux transposés pour commencer sur 0, selon la même règle, et garde le plus tassé. Les formes premières s'écrivent entre parenthèses sans virgules, avec T et E pour 10 et 11 : (037) pour les deux accords parfaits.

Les deux règles ne peuvent diverger que si des candidats sont à égalité d'étendue. Prenez 5-20, do do♯ fa fa♯ la♭, {0, 1, 5, 6, 8}. Deux rotations ont une étendue de 8 : 0 1 5 6 8 et, à partir de fa, 0 1 3 7 8. L'inversion en donne deux autres d'étendue 8, 0 1 5 7 8 et 0 2 3 7 8. Depuis la gauche, les deuxièmes intervalles sont 1, 1, 1 et 2 ; parmi les trois premières, les troisièmes intervalles sont 5, 3 et 5, donc la forme première de Forte est (01378). Depuis la droite, les avant-derniers intervalles sont 6, 7, 7 et 7, donc la forme première de Rahn est (01568). Sur les 224 classes d'ensembles, les deux règles divergent pour six :

| Classe d'ensembles | Rahn | Forte |
|---|---|---|
| 5-20 | (01568) | (01378) |
| 6-Z29 | (023679) | (013689) |
| 6-31 | (014579) | (013589) |
| 7-Z18 | (0145679) | (0123589) |
| 7-20 | (0125679) | (0124789) |
| 8-26 | (0134578T) | (0124579T) |

Ces six classes comptent 120 des 4 096 ensembles. Tous les autres ensembles reçoivent la même forme première des deux règles.

**Pourquoi un ordinateur peut se passer des règles.** Écrivez un ensemble comme un nombre de 12 bits, dont le bit p vaut 1 quand la classe de hauteurs p est présente : do majeur {0, 4, 7} vaut 1 + 16 + 128 = 145. Comparer deux tels nombres compare d'abord leurs classes de hauteurs les plus hautes, puisque 2^p dépasse la somme de toutes les puissances de 2 inférieures. Parmi les 24 formes d'un ensemble, le plus petit nombre contient 0, car transposer un ensemble vers le bas abaisse chaque bit. Ensuite, il a la plus petite dernière note, c'est-à-dire la plus petite étendue, puis la plus petite avant-dernière note, et ainsi de suite. C'est la règle de Rahn. Pour 5-20, (01568) vaut 1 + 2 + 32 + 64 + 256 = 355, et (01378) vaut 395.

### Exercice pratique

L'ensemble do do♯ mi fa sol la, {0, 1, 4, 5, 7, 9}, appartient à 6-31. Donnez sa forme première selon chaque règle, et le nombre de 12 bits de chacune.

> *Solution :* Quatre formes ont une étendue de 9 : 0 1 4 5 7 9 et, à partir de mi, 0 1 3 5 8 9, puis 0 2 4 5 8 9 et 0 1 4 6 8 9 venant de l'inversion. Depuis la gauche, les deuxièmes intervalles sont 1, 1, 2 et 1, et les troisièmes intervalles des trois restantes sont 4, 3 et 4 : la forme de Forte, (013589), 1 + 2 + 8 + 32 + 256 + 512 = 811. Depuis la droite, les avant-derniers intervalles sont 7, 8, 8 et 8 : la forme de Rahn, (014579), 1 + 2 + 16 + 32 + 128 + 512 = 691. Le plus petit nombre est celui de Rahn.

---

## 4. Compter les classes d'ensembles

Le **lemme de Burnside** compte les classes sans les énumérer : le nombre de classes est la moyenne, sur les opérations, du nombre d'ensembles que chaque opération laisse inchangés.

Prenez les 220 ensembles de trois notes. Parmi les 12 transpositions, T0 laisse les 220 inchangés, T4 et T8 laissent inchangés les 4 accords parfaits augmentés, et les autres n'en laissent aucun : (220 + 4 + 4) / 12 = 19 types Tn. Ajoutez maintenant les 12 inversions. Quand n est pair, TnI est la symétrie du cercle des classes de hauteurs par rapport à un axe qui passe par deux classes de hauteurs, n/2 et n/2 + 6. Elle laisse inchangé un ensemble de trois notes quand l'ensemble contient l'une de ces deux classes et l'une des cinq paires que le miroir échange : 2 × 5 = 10 ensembles. Quand n est impair, l'axe passe entre les classes de hauteurs, chaque note est échangée avec une autre, et aucun ensemble de trois notes n'est laissé inchangé. Donc (228 + 6 × 10) / 24 = 12 classes d'ensembles.

| Notes | Classes d'ensembles | Types Tn |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 6 | 6 |
| 3 | 12 | 19 |
| 4 | 29 | 43 |
| 5 | 38 | 66 |
| 6 | 50 | 80 |
| 7 | 38 | 66 |
| 8 | 29 | 43 |
| 9 | 12 | 19 |
| 10 | 6 | 6 |
| 11 | 1 | 1 |
| 12 | 1 | 1 |
| Total | 224 | 352 |

Les colonnes sont symétriques, parce que la complémentation apparie les ensembles de n notes avec ceux de 12 − n. Une classe compte un seul type Tn quand une inversion envoie ses membres sur eux-mêmes, et deux sinon, comme 3-11A, les accords parfaits mineurs, et 3-11B, les accords parfaits majeurs. Donc 352 − 224 = 128 classes comptent deux types Tn, et les 96 autres sont symétriques par inversion. Les totaux sont les nombres de bracelets et de colliers binaires à 12 perles (OEIS A000029 et A000031).

### Exercice pratique

Lesquelles des 12 classes de tricordes sont leur propre inversion ? Vérifiez que le compte s'accorde avec les 19 types Tn.

> *Solution :* (012), (024), (027), (036) et (048), les classes de do do♯ ré, do ré mi, do ré sol, do mi♭ sol♭ et do mi sol♯ : inverser l'une d'elles donne une transposition du même ensemble. Les 7 autres classes comptent deux types Tn chacune, donc 5 + 2 × 7 = 19.

---

## 5. Complémentaires et relation Z

Le **complémentaire** d'un ensemble contient les classes de hauteurs qui lui manquent, et son vecteur se déduit de celui de l'ensemble. Fixez une classe d'intervalles k de 1 à 5. L'agrégat contient 12 paires de classe d'intervalles k, et chaque note a deux partenaires à cette distance. Si un ensemble de n notes contient a_k telles paires, ses notes prennent part à 2n paires comptées de leur côté, dont 2a_k à l'intérieur de l'ensemble, si bien que 2n − 2a_k paires passent vers le complémentaire. Le complémentaire garde le reste : 12 − a_k − (2n − 2a_k) = a_k + 12 − 2n. Pour le triton, avec 6 paires en tout et un partenaire par note, le même décompte donne a_6 + 6 − n. C'est le **théorème du complémentaire** : chaque décompte sauf celui du triton varie de 12 − 2n, et celui du triton de 6 − n.

Pour un hexacorde, n = 6, donc un hexacorde et son complémentaire ont le même vecteur. C'est le **théorème de l'hexacorde**, souvent attribué à Babbitt.

Deux classes d'ensembles de même nombre de notes et de même vecteur sont **en relation Z**. Il existe 23 telles paires. L'une se trouve parmi les tétracordes, 4-Z15 (0146) et 4-Z29 (0137), toutes deux <111111>. Trois se trouvent parmi les pentacordes, 15 parmi les hexacordes, 3 parmi les heptacordes et 1 parmi les octocordes. Le théorème du complémentaire explique cette symétrie : les complémentaires de deux ensembles en relation Z partagent aussi un vecteur, si bien que les paires de 4 et 8 notes, et celles de 5 et 7, vont ensemble. Des 50 classes d'hexacordes, 20 contiennent leurs propres complémentaires. Chacune des 30 autres a ses complémentaires dans sa partenaire Z, ce qui rend compte des 15 paires d'hexacordes.

M5 rend compte de certaines paires d'une autre manière. Elle échange les décomptes des classes d'intervalles 1 et 5 (§2), si bien qu'un ensemble dont ces deux décomptes sont égaux garde son vecteur sous M5 : l'image tombe dans la même classe ou dans sa partenaire Z. 4-Z15 en est un exemple : 0 1 4 6 multiplié par 5 donne 0 5 8 6, dont l'ordre normal 5 6 8 0 donne (0137), 4-Z29. Neuf des 23 paires sont reliées ainsi : 4-Z15/4-Z29, 5-Z17/5-Z37, 5-Z18/5-Z38, 6-Z6/6-Z38, 6-Z11/6-Z40, 6-Z19/6-Z44, 7-Z17/7-Z37, 7-Z18/7-Z38 et 8-Z15/8-Z29.

### Exercice pratique

Montrez que 5-Z17 (01348) et 5-Z37 (03458) ont le même vecteur, et que M5 envoie l'une sur l'autre.

> *Solution :* Toutes deux ont <212320>. Multiplier 0 1 3 4 8 par 5 donne 0 5 3 8 4, soit {0, 3, 4, 5, 8}. Sa seule rotation d'étendue 8 commence sur 0, et son inversion donne la même, donc sa forme première est (03458).

---

## 6. Numéros de Forte

Forte (1973) a donné à chaque classe de 3 à 9 notes, 208 en tout, un nom de la forme cardinalité-indice : 3-11 est la onzième classe de tricordes. Un Z devant l'indice marque une classe en relation Z. Deux conventions rendent le catalogue plus commode. Sauf pour les hexacordes en relation Z, dont les complémentaires se trouvent dans la partenaire Z, une classe de n notes et la classe de ses complémentaires portent le même indice : 4-Z15 et 8-Z15, ou 5-35, la gamme pentatonique, et 7-35, la collection diatonique que forme son complémentaire. Et dans chaque paire d'hexacordes en relation Z, l'un porte un indice de 3 à 29 et l'autre un indice de 36 à 50.

Les étiquettes sont celles de Forte ; les formes imprimées à côté dépendent du tassement. Une table qui suit Rahn imprime (01568) à côté de 5-20, une table qui suit Forte imprime (01378). Un ordinal qui compte selon un autre ordre n'est pas un numéro de Forte, même quand il a la même forme (§7).

### Exercice pratique

Les touches noires d'un piano, do♯ ré♯ fa♯ sol♯ la♯, forment une gamme pentatonique. Nommez sa classe et la classe des touches blanches.

> *Solution :* 5-35, (02479), et 7-35, (013568T), pour les sept touches blanches, son complémentaire. L'indice est le même, comme pour toute paire de classes complémentaires sauf les hexacordes en relation Z.

---

## 7. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26) ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA à `6d5ff22`. La [leçon 4 de music-theory-ga](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/04-set-classes.mdx) de Learn compile une version antérieure de GA, `a826864`, et vérifie ses classes d'ensembles par rapport aux définitions des manuels. Les autres nombres ci-dessous viennent d'une transcription en Python, ligne à ligne, du code de GA nommé.

**Les formes premières sont celles de Rahn, par le nombre.** [`PitchClassSetId.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L137) garde le plus petit identifiant parmi les 24 formes, et [`PitchClassSet.PrimeForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L161) et [`SetClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L53) reposent sur lui. D'après le §3, c'est la règle de Rahn, et le programme de Learn, compilé à `a826864`, l'a trouvée pour [4 096 ensembles sur 4 096](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L45). Le propre test de GA compare la forme première à ce qu'il appelle un [oracle indépendant](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L32), qui prend lui aussi le plus petit des 24 identifiants. Il fige la définition au lieu de la confronter à une règle de tassement, et aucun de ses [trois points d'ancrage](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L89) n'appartient aux six classes du §3.

**La forme normale n'est pas celle des manuels.** [`ToNormalForm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L420) garde la rotation dont les écarts entre notes successives, autour du cercle, sont les plus réguliers : la plus petite différence entre le plus grand et le plus petit écart, puis la suite d'écarts la plus petite dans l'ordre lexicographique. Ses remarques le disent, [« This is not the textbook normal form »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L415), et le code nomme cette différence d'écarts [« span »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L671). La table que lit `ToNormalForm` est construite par [cette boucle](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L631) :

```csharp
                var rotation = Rotr12(set, member);
                Gaps(rotation, count, gaps);
                var span = Span(gaps[..count]);
                if (span > bestSpan || (span == bestSpan && !MoreCompact(gaps[..count], bestGaps[..count])))
                {
                    continue;
                }
```

Sur les 4 095 ensembles non vides, sa réponse diffère sur 1 998 de l'ordre normal de la règle de Rahn transposé à 0. L'exemple de la méthode décrit pourtant encore la règle des manuels : pour sol si ré, il dit que le résultat 0 3 8 est le plus compact, avec une étendue [de 0 à 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L402), alors que 0 4 7, à partir de sol, s'étend sur 7. La forme première n'utilise pas cette méthode, mais la [recherche de la tonalité la plus proche](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L559) de GA l'utilise : elle attend une tonalité mineure quand la forme normale contient la classe de hauteurs 3. Tout accord parfait majeur reçoit 0 3 8, si bien que pour do mi sol, que contiennent trois tonalités majeures et trois tonalités mineures, la recherche choisit une tonalité mineure.

**La relation Z et la relation M.** [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L199) cherche dans la [famille modale](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114) de l'ensemble, les ensembles contenant 0 qui partagent son vecteur, un membre qui ne figure pas parmi les 24 formes du premier membre de la famille. Sa transcription concorde avec le vecteur sur les 4 096 ensembles, et [un test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82) la confronte au Z de chaque étiquette stockée. [`SetClass.MRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L80) applique M5 à une classe, et 92 des 224 classes sont leur propre image par M5.

**Deux catalogues.** [`CanonicalForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L25) stocke les étiquettes de Forte de 1 à 6 notes et déduit celles de 7 à 11 notes [du complémentaire](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L227). Ses remarques disent que [« the stored prime forms are Rahn's »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/CanonicalForteCatalog.cs#L16) et nomment les six classes du §3. [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) numérote les classes de chaque taille par l'identifiant de leur vecteur, puis par celui de leur forme première :

```csharp
            var ordered = group
                .OrderBy(sc => sc.IntervalClassVector.Id)
                .ThenBy(sc => sc.PrimeForm.Id.Value)
                .ToList();

            for (var i = 0; i < ordered.Count; i++)
            {
                var setClass = ordered[i];
                var forte = new ForteNumber(cardinality, i + 1);
                result[setClass.PrimeForm.Id] = forte;
            }
```

Son résumé appelle le résultat un [« Forte-style catalog »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L6), et ses remarques qualifient de [« minor »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L18) les différences avec la numérotation de Forte. Des 208 classes de la table de Forte, il donne le même indice que Forte à 3 : 5-Z18, 6-21 et 8-Z15. L'accord parfait majeur y devient 3-2, et la collection diatonique 7-1. [`ForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ForteCatalog.cs#L11) dit que cet ordinal « diverges for most set classes » et ne doit pas être montré aux utilisateurs. L'issue [#544](https://github.com/GuitarAlchemist/ga/issues/544) de GA, désormais fermée, a trouvé {4, 5, 10, 11} étiqueté 4-21 au lieu de 4-9, et le reconnaisseur d'accords la cite là où il [nomme un accord d'après le catalogue de Forte](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L327). [`SetClassLabelFormatter`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/SetClassLabelFormatter.cs#L32) propose toujours l'ordinal comme notation « Rahn », alors que le nom de Rahn désigne une règle de tassement, pas une numérotation.

**Ce que vérifient les tests du catalogue.** Les [tests du catalogue](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L7) le prouvent « against GA's own atonal engine » avec quatre contraintes : chaque forme stockée est une classe d'ensembles de GA, les décomptes par taille concordent, les étiquettes correspondent une à une aux classes de GA, et les marqueurs Z s'accordent avec `IsZRelated`. Trois tests les imposent : [les décomptes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L32), [la correspondance une à une](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L47), qui couvre aussi l'appartenance, et [les marqueurs Z](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L82). Un quatrième vérifie [l'aller-retour](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L145) de la forme à l'étiquette et retour. Ils montrent que la table s'accorde avec GA et avec elle-même, pas qu'elle est celle de Forte : échanger les formes de deux étiquettes stockées de même taille et de même statut Z, comme 5-1 et 5-2, les laisserait toutes vraies. Les autres tests du fichier nomment neuf étiquettes, et aucune de 5-1, 5-2, 7-1 ou 7-2 n'en fait partie (§8, étape 5).

**L'identifiant du vecteur.** [`IntervalClassVectorId`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L17) range les six décomptes comme des chiffres en base 12. Les décomptes de 12 de l'agrégat ne tiennent pas dans un chiffre, et son identifiant est désormais [décodé comme un cas particulier](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L49). La leçon 4 de Learn, compilée à `a826864`, montre encore l'ancienne réponse, [<1 1 1 1 0 6>](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l4.txt#L18).

**Ce que lit le chatbot.** La compétence [`IntervalClassVectorSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L31) du chatbot construit un accord à partir de sa propre table de qualités. Elle met la qualité en minuscules [avant de comparer](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L199), si bien que « CM7 » devient « m7 » et reçoit le vecteur d'une septième mineure, <012120>, au lieu de celui de la septième majeure, <101220>, alors que [sa table contient « M7 »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L206). Une qualité absente de la table, comme C7♯9, C13 ou Cadd9, retombe sur [l'accord parfait majeur](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L216), et la réponse porte quand même [une confiance de 1,0](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L226). Son [motif d'accord](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/IntervalClassVectorSkill.cs#L66) prend aussi l'article de « ICV of a major scale » pour l'accord A.

Corriger quoi que ce soit de tout cela revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

La méthode `ToNormalForm` de GA renvoie 0 3 8 pour sol si ré. Que donne l'ordre normal des manuels, et pourquoi la forme première de GA reste-t-elle juste ?

> *Solution :* Les rotations sont sol si ré (0 4 7, étendue 7), si ré sol (0 3 8, étendue 8) et ré sol si (0 5 9, étendue 9). Les règles de Forte et de Rahn gardent toutes deux sol si ré, 0 4 7, puisque son étendue est la seule plus petite. La forme première de GA n'appelle jamais `ToNormalForm` : elle prend le plus petit identifiant des 24 formes, ce qui donne (037).

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien n'y est une mesure. Les prédictions viennent de la transcription du §7 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en marche ni un modèle de langage.

1. **Formes premières.** Pour les 4 096 ensembles, comparer `PitchClassSet.PrimeForm` aux règles de Rahn et de Forte. Prédiction : celle de Rahn sur les 4 096 ensembles ; celle de Forte sur tous sauf les 120 ensembles des six classes du §3.
2. **Formes normales.** Comparer `ToNormalForm` à l'ordre normal de Rahn transposé à 0. Prédiction : 1 998 différences parmi les 4 095 ensembles non vides, dont sol si ré, donné comme 0 3 8.
3. **Complémentaires et Z.** Sur les 224 classes, compter celles pour lesquelles `IsZRelated` est vrai, et comparer chaque classe d'hexacordes à la classe de son complémentaire. Prédiction : 46 ; le complémentaire tombe dans la même classe pour 20 classes d'hexacordes et dans la partenaire Z pour les 30 autres ; et le théorème du complémentaire du §5 vaut pour les 4 096 ensembles.
4. **La relation M.** Appliquer `SetClass.MRelated` à chaque classe. Prédiction : 92 classes sont leur propre image, et 9 des 23 paires Z sont l'image l'une de l'autre.
5. **Les tests du catalogue après un échange.** Dans une copie de `CanonicalForteCatalog` interne au laboratoire, jamais dans GA lui-même, échanger les formes de 5-1 et 5-2 et lancer les quatre mêmes tests sur la copie. Prédiction : tous les quatre passent.
6. **Deux numérotations.** Comparer `ProgrammaticForteCatalog` à `CanonicalForteCatalog`, sans tenir compte du Z. Prédiction : le même indice pour 7 des 224 classes : les quatre classes de 0, 1, 11 et 12 notes, et 5-Z18, 6-21 et 8-Z15.
7. **Les vecteurs du chatbot.** Appeler `IntervalClassVectorSkill.ExecuteAsync` avec « ICV of CM7 », « ICV of C7#9 » et « ICV of a major scale ». Prédiction : <012120> ; <001110> avec une confiance de 1,0 ; et de nouveau <001110>.

### Exercice pratique

L'étape 5 prédit que les quatre tests passent encore après l'échange. Quel genre de test échouerait ?

> *Solution :* Un test qui compare chaque forme stockée à une copie de la table de Forte établie indépendamment du fichier de GA, saisie à partir d'une autre source. L'appartenance, les décomptes, une correspondance une à une, les marqueurs Z et un aller-retour ne peuvent pas distinguer deux étiquettes de même taille et de même statut Z.

---

## 9. Pièges courants

- **Appeler les accords parfaits majeur et mineur deux classes d'ensembles.** Ce sont deux types Tn d'une même classe, 3-11.
- **Lire une forme première sans sa règle.** Six classes ont deux formes premières ; vérifiez si une table tasse vers la gauche ou depuis la droite.
- **Prendre un vecteur partagé pour une classe partagée.** 23 paires de classes partagent leur vecteur.
- **Supposer que M5 garde la classe d'un ensemble ou son vecteur.** Elle envoie do majeur sur (014) ; elle ne garde le vecteur que si les décomptes des classes d'intervalles 1 et 5 sont égaux.
- **Prendre un ordinal pour un numéro de Forte.** Une étiquette de la forme n-k n'est celle de Forte que si elle vient de la table de Forte.
- **Se fier au nom d'une méthode.** La « forme normale » ou le « span » d'une bibliothèque peut ne pas être celui des manuels ; lisez la définition.
- **Lire un test de cohérence comme un test d'exactitude.** Une table peut s'accorder partout avec elle-même et porter quand même une étiquette fausse.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Ensemble de classes de hauteurs** | Un sous-ensemble des 12 classes de hauteurs, numérotées de do = 0 à si = 11 |
| **Type Tn** | Les ensembles reliés entre eux par transposition |
| **Classe d'ensembles** | Les ensembles reliés entre eux par transposition ou par inversion suivie d'une transposition |
| **Vecteur de classes d'intervalles** | Les décomptes des six classes d'intervalles parmi toutes les paires de notes d'un ensemble |
| **Ordre normal** | La rotation d'un ensemble dont l'étendue est la plus petite, les égalités tranchées par la règle de Forte ou celle de Rahn |
| **Forme première** | Le plus tassé des ordres normaux d'un ensemble et de son inversion, transposé pour commencer sur 0 |
| **Complémentaire** | Les classes de hauteurs qu'un ensemble ne contient pas |
| **Relation Z** | La relation entre deux classes d'ensembles de même taille et de même vecteur de classes d'intervalles |
| **M5** | La multiplication de chaque classe de hauteurs par 5, qui échange les décomptes des classes d'intervalles 1 et 5 |
| **Numéro de Forte** | L'étiquette cardinalité-indice de Forte, avec un Z pour une classe en relation Z |

---

## Auto-évaluation

**1. Combien d'ensembles compte la classe de l'accord de septième diminuée, et pourquoi ?**
> 3. Do mi♭ sol♭ la est envoyé sur lui-même par T0, T3, T6, T9 et quatre inversions, 8 des 24 opérations, donc sa classe compte 24 / 8 = 3 ensembles : les trois accords de septième diminuée.

**2. Un ensemble de cinq notes a le vecteur <212320>. Quel est le vecteur de son complémentaire ?**
> <434541>. Avec n = 5, le théorème du complémentaire ajoute 12 − 2n = 2 aux cinq premiers décomptes et 6 − n = 1 à celui du triton.

**3. Quelle forme première une table qui suit Forte imprime-t-elle pour 6-Z29, et laquelle imprime une table qui suit Rahn ?**
> Celle de Forte, (013689), et celle de Rahn, (023679). 6-Z29 est l'une des six classes sur lesquelles les règles divergent.

**4. Le [`ProgrammaticForteCatalog`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ProgrammaticForteCatalog.cs#L110) de GA étiquette l'accord parfait majeur 3-2. Est-ce son numéro de Forte ?**
> Non. L'accord parfait majeur est 3-11 dans le catalogue de Forte, et 3-2 y est (013). L'ordinal programmatique suit l'identifiant du vecteur, et il ne donne le même indice que Forte qu'à 3 des 208 classes de sa table.

**Critères de réussite :** Regrouper des ensembles en types Tn et en classes d'ensembles et déduire la taille d'une classe de sa symétrie ; calculer un vecteur de classes d'intervalles et celui du complémentaire ; trouver la forme première selon les deux règles et nommer les six classes où elles diffèrent ; compter des classes avec le lemme de Burnside ; expliquer la relation Z par le théorème du complémentaire et par M5 ; et distinguer un numéro de Forte d'un ordinal.

---

## Bases de recherche

- A. Forte, *The Structure of Atonal Music*, Yale University Press, 1973 : le catalogue des classes d'ensembles, l'ordre normal tassé vers la gauche, les numéros de Forte et la relation Z
- J. Rahn, *Basic Atonal Theory*, Longman, 1980 : l'ordre normal tassé depuis la droite
- J. N. Straus, *Introduction to Post-Tonal Theory*, 4e édition, W. W. Norton, 2016 : ordre normal, forme première, vecteurs de classes d'intervalles, complémentaires et relation Z
- OEIS A000029 et A000031 : les nombres de bracelets et de colliers binaires, 224 et 352 pour 12 perles
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §7 renvoie à sa ligne ; issue #544 de GA
- Learn, leçon 4 de music-theory-ga et sa sortie attendue au commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3` : la vérification compilée des formes premières de GA citée au §7
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
