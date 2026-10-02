---
module_id: mus-018-key-finding-roman-numerals-cadences
department: music
course: Identification de la tonalité, chiffres romains et cadences
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-003-functional-harmony]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Identification de la tonalité, chiffres romains et cadences — Ce qu'un décompte d'accords peut trancher, et ce qu'il ne peut pas

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 60 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Énumérer les accords parfaits d'une tonalité majeure et de sa relative mineure, et expliquer pourquoi les accords seuls ne permettent pas de distinguer ces deux tonalités
- Noter une progression contre les 30 tonalités majeures et mineures en comptant ses accords parfaits diatoniques, et départager les ex aequo par la cadence, l'accord d'ouverture et le mode
- Expliquer pourquoi le V majeur d'une tonalité mineure n'appartient pas à son mineur naturel, et ce que cela change à un décompte
- Étiqueter une progression en chiffres romains une fois sa tonalité choisie, dominantes secondaires et accords semi-diminués compris
- Distinguer des tonalités enharmoniques par leur orthographe, et nommer la tonalité relative de chacune des 30 tonalités
- Dire en quoi les algorithmes à profils de tonalité diffèrent du décompte d'accords, et ce que chacun peut et ne peut pas entendre
- Retracer ce que calcule l'identification de tonalité de GA, ce que montre chacun de ses outils, et où ses réponses et sa documentation divergent

---

## 1. Tonalités, accords parfaits diatoniques et paire relative

Une tonalité majeure construit un accord parfait sur chaque degré de sa gamme : I, ii, iii, IV, V, vi et vii°. En do majeur, ce sont C, Dm, Em, F, G, Am et B°. Le **mineur naturel** bâti sur la note la utilise les mêmes sept notes, si bien que ses accords parfaits sont les sept mêmes accords dans un autre ordre : i, ii°, III, iv, v, VI et VII, soit Am, B°, C, Dm, Em, F et G. Une tonalité majeure et la tonalité mineure bâtie sur son sixième degré forment une **paire relative** : elles partagent une armure, chaque note et chaque accord parfait diatonique. Dans l'autre sens, la relative majeure se trouve sur le troisième degré de la tonalité mineure.

L'harmonie en mineur ne reste pas dans le mineur naturel. Pour ramener vers sa tonique, elle hausse le septième degré, sol en sol♯ en la mineur. C'est le **mineur harmonique**. L'accord parfait du cinquième degré devient majeur, mi sol♯ si, et la septième de dominante E7 (mi sol♯ si ré) porte le triton sol♯–ré dont MUS-003 §3 a décrit la résolution. L'accord parfait du septième degré devient vii°, sol♯ si ré. Une tonalité mineure a donc deux dominantes sur son cinquième degré, v venu du mineur naturel et V venu du mineur harmonique, et ses cadences emploient V.

Avec au plus sept dièses ou bémols, il y a 15 tonalités majeures et 15 tonalités mineures, 30 noms en tout. Leurs gammes ne forment que 12 ensembles de notes différents, un par transposition de la gamme diatonique. Neuf de ces ensembles portent deux noms, une tonalité majeure et sa relative mineure. Les trois autres en portent quatre, parce que chacune de leurs tonalités peut s'écrire de deux façons : si et do♭ majeur avec sol♯ et la♭ mineur, fa♯ et sol♭ majeur avec ré♯ et mi♭ mineur, et do♯ et ré♭ majeur avec la♯ et si♭ mineur. Cela fait 9 × 2 + 3 × 4 = 30.

### Exercice pratique

Pourquoi les accords seuls ne peuvent-ils pas séparer do majeur de la mineur dans Am F C G ?

> *Solution :* Les deux tonalités partagent tous leurs accords parfaits diatoniques, donc les quatre accords appartiennent aux deux, comme chaque note. Seule l'accentuation peut trancher : quel accord ouvre et lequel conclut, lequel dure le plus longtemps ou tombe sur les temps forts, et surtout une cadence, G vers C ou E vers Am. Ici, Am ouvre la progression, ce qui penche vers la mineur, mais rien dans la liste des accords ne le prouve.

---

## 2. Compter les accords parfaits diatoniques

Le plus simple des détecteurs de tonalité réduit chaque accord à sa fondamentale et à la qualité de son accord parfait : majeur, mineur ou diminué. Un accord de septième compte comme son accord parfait, si bien que Dm7 vaut Dm et G7 vaut G. Pour chacune des 30 tonalités, il compte combien des accords distincts de la progression figurent parmi les sept accords parfaits de la tonalité, et il garde les tonalités qui ont le décompte le plus élevé.

Pour Am F C G, do majeur et la mineur comptent tous deux 4 sur 4. Quatre tonalités comptent 3 sur 4. Fa majeur contient F, C et Am, mais son ii est Gm, pas G. Sol majeur contient C, G et Am, mais pas F. Ré mineur contient F, C et Am, et mi mineur contient G, Am et C. Toute autre tonalité compte au plus 1.

Un décompte sur le mineur naturel manque la cadence propre à la tonalité mineure. Dans Am Dm E7 Am, l'accord parfait de E7 est mi majeur, qui n'est pas dans la mineur naturel, où le cinquième degré porte Em. La mineur compte 2 des 3 accords distincts, pas plus que do majeur, fa majeur et ré mineur. Compter aussi le V harmonique donne à la mineur 3 sur 3, seule en tête. Ce correctif a un prix dans les tonalités majeures. Une **dominante secondaire** (MUS-003 §5) emprunte le V de la forme harmonique d'une tonalité mineure : dans C E7 Am F, E7 est le V7/vi de do majeur. Si l'on compte le V harmonique, la mineur obtient les 4 accords et do majeur 3, si bien que le décompte désigne la relative mineure d'une progression qui reste en do majeur. Sans lui, do majeur, la mineur, fa majeur et ré mineur comptent chacune 3. Aucune des deux façons de compter ne traite correctement les deux progressions : le décompte a besoin de l'aide de l'ordre des accords.

### Exercice pratique

Notez Dm G C contre do majeur, la mineur, ré mineur et sol majeur.

> *Solution :* Do majeur compte 3 sur 3 (ii, V, I), et la mineur aussi (iv, VII, III). Ré mineur compte 2 : Dm et C, ses i et VII, mais G est un accord parfait majeur, pas son iv naturel. Sol majeur compte 2 : G et C, ses I et IV, mais son V est ré majeur, pas Dm.

---

## 3. Départager : cadence, accord d'ouverture et mode

Un décompte laisse une tonalité et sa relative mineure à égalité chaque fois que tous les accords sont diatoniques, et il peut aussi laisser d'autres tonalités à égalité. Trois sortes d'indices départagent, par force décroissante.

- **La cadence.** Une progression qui finit sur V–I, ou V7–I, confirme la tonalité de ce I. Dans une tonalité mineure, le V de la cadence est le V majeur du mineur harmonique. Une demi-cadence finit sur V, et une cadence plagale finit sur IV–I. Aucune des deux ne confirme une tonalité de la même façon, et une cadence rompue, V–vi, évite complètement la tonique.
- **L'accord d'ouverture.** Une progression qui s'ouvre sur l'accord de tonique d'une des tonalités à égalité penche vers cette tonalité.
- **La convention.** Quand rien d'autre ne tranche, un détecteur doit choisir, par exemple la tonalité majeure.

Ces règles tranchent les exemples précédents. Am F C G s'ouvre sur Am et va à la mineur, tandis que C G Am F va à do majeur. Dm G C finit sur G–C, V–I de do majeur, donc do majeur vient en premier, bien que la mineur ait le même décompte. Dans Am Dm E7 Am, E7–Am est le V7–i de la mineur, ce qui tranche entre les quatre tonalités qui comptent 2. C D G C montre qu'une cadence peut peser plus que le décompte. Sol majeur et mi mineur contiennent les trois accords distincts et do majeur seulement deux, puisque D est V/V, une dominante secondaire. Pourtant la progression finit sur G–C et elle est en do majeur. Un détecteur qui donne à la cadence le poids de deux accords, comme le fait GA (§7), place do majeur en premier.

Certaines musiques n'ont pas de tonalité majeure ou mineure à trouver. G F C G est en sol mixolydien, le mode de la gamme majeure à septième abaissée, si bien que son accord de F est ♭VII. Son décompte donne à do majeur et à la mineur 3 sur 3 et à sol majeur 2, et sa fin C–G est plagale, donc aucune cadence ne parle pour sol. C B♭ F C est en do majeur avec un ♭VII emprunté à do mineur ; le décompte préfère fa majeur et ré mineur, qui contiennent les trois accords distincts, à do majeur, qui en contient deux. Un vamp dorien, Dm7 Em7 répété, compte 2 sur 2 pour do majeur et la mineur. Un détecteur dont les réponses sont les 30 tonalités majeures et mineures ne peut nommer que la tonalité dont ces progressions utilisent les notes.

### Exercice pratique

D C♯7 F♯m s'ouvre sur D. Dans quelle tonalité est-elle ?

> *Solution :* Fa♯ mineur. D et F♯m sont tous deux dans ré majeur, la majeur, si mineur et fa♯ mineur, chacune comptant 2 sur 3, tandis que l'accord parfait de C♯7 n'est dans aucune de leurs formes naturelles. C♯7–F♯m est le V7–i de fa♯ mineur, la cadence du mineur harmonique, et elle l'emporte sur l'ouverture en D.

---

## 4. Chiffres romains

Une fois la tonalité choisie, chaque accord reçoit un **chiffre romain** : le degré de sa fondamentale dans la gamme de la tonalité, écrit en majuscules pour un accord parfait majeur, en minuscules pour un mineur, avec ° pour un accord parfait diminué, ø pour une septième semi-diminuée, + pour un accord parfait augmenté, et le chiffre de la septième quand il y en a une. En do majeur, Dm7 G7 Cmaj7 donne ii7 V7 Imaj7. En la mineur, Bø7 E7 Am donne iiø7 V7 i. L'accord parfait de Bø7, si ré fa, est diminué : Bø7 est le même accord que Bm7♭5, une septième mineure à quinte abaissée, et non un accord parfait mineur. E7 est V7, venu du mineur harmonique, et Am est i.

Les chiffres portent la fonction autant que le degré. Dans C E7 Am F G7 C, E7 est **V7/vi**, la dominante de Am, et non un accord « III7 » de do majeur : le chiffre nomme l'accord vers lequel il conduit (MUS-003 §5). Un accord dont la fondamentale est hors de la gamme reçoit une altération : B♭ en do majeur est ♭VII.

Un étiqueteur qui ne lit que le degré de la fondamentale et la qualité de l'accord écrira III pour E7 en do majeur. Cela décrit l'accord, mais en cache la fonction, et il ne faut pas confondre les deux conventions.

### Exercice pratique

Étiquetez C E7 Am F G7 C en do majeur.

> *Solution :* I, V7/vi, vi, IV, V7, I. La progression tonicise vi le temps d'un accord, puis revient par IV et V7 à I.

---

## 5. Tonalités enharmoniques et tonalité relative

Ré♭ majeur et do♯ majeur sonnent de la même façon sur une guitare et contiennent les mêmes classes de hauteurs, mais ce sont des tonalités différentes sur le papier. Ré♭ majeur a cinq bémols ; do♯ majeur a sept dièses, et ses accords s'écrivent C♯, F♯ et G♯. Une grille qui indique D♭ G♭ A♭ D♭ est en ré♭ majeur, et l'orthographe en est la preuve. Un détecteur de tonalité qui transforme chaque accord en classe de hauteurs avant de noter donne aux deux tonalités le même score, et ne peut donc pas utiliser cette preuve.

La relative est elle aussi une affaire d'orthographe. La relative mineure de si majeur est sol♯ mineur, sur le sixième degré de si majeur, et toutes deux ont cinq dièses. La♭ mineur contient les mêmes classes de hauteurs, mais a sept bémols et est la relative mineure de do♭ majeur. Les 12 noms de tonalité des trois ensembles qui portent quatre noms forment six paires enharmoniques de même mode : si et do♭ majeur, fa♯ et sol♭ majeur, do♯ et ré♭ majeur, et sol♯ et la♭, ré♯ et mi♭, la♯ et si♭ mineur.

### Exercice pratique

Nommez les tonalités relatives de fa♯ majeur et de ré♯ mineur.

> *Solution :* Ré♯ mineur et fa♯ majeur, chacune avec six dièses. Mi♭ mineur et sol♭ majeur ont les mêmes notes, mais avec six bémols.

---

## 6. Profils de tonalité : peser les notes au lieu de compter les accords

Le décompte d'accords est une famille de détecteurs de tonalité. Une autre pèse les notes elles-mêmes. Longuet-Higgins et Steedman (1971) trouvaient la tonalité des 48 sujets de fugue du *Clavier bien tempéré* de Bach en éliminant, note après note, les tonalités dont la gamme ne contient pas la note entendue, avec une règle qui favorise la tonalité dont la tonique, ou à défaut la dominante, est la première note quand l'élimination ne tranche pas. Krumhansl et Kessler (1982) ont demandé à des auditeurs à quel point chacune des 12 classes de hauteurs convenait à un contexte tonal. Les réponses ont donné un **profil de tonalité** pour les tonalités majeures et un pour les tonalités mineures, le plus haut pour la tonique et le plus bas pour les notes hors de la gamme. Dans l'**algorithme de Krumhansl–Schmuckler** (Krumhansl, 1990, chap. 4), la durée totale de chaque classe de hauteurs dans un passage est corrélée avec les 24 rotations des deux profils, et la tonalité de plus forte corrélation l'emporte. Temperley (1999) a réexaminé cet algorithme et proposé des révisions. Son livre (Temperley, 2001) traite l'identification de la tonalité par des règles de préférence, aux côtés de la métrique, de l'harmonie et de l'orthographe des hauteurs, et laisse la tonalité changer au cours d'un morceau.

La différence avec un décompte d'accords tient au poids. Une méthode à profils entend qu'un accord dure quatre mesures et que la note de tonique revient sans cesse, si bien qu'elle peut séparer une tonalité de sa relative mineure là où un décompte d'accords distincts ne le peut pas. Une liste d'accords sans durées ne lui donne rien à peser, et aucune des deux familles n'entend la ligne de basse, la métrique ou la phrase si on ne les ajoute pas à son entrée. Les deux ne choisissent en outre que parmi les tonalités majeures et mineures, si bien qu'un passage dorien ou mixolydien reçoit la tonalité majeure ou mineure dont il utilise les notes.

### Exercice pratique

C dure quatre mesures, puis Am, F et G une mesure chacun. Pourquoi un profil pondéré par les durées peut-il séparer ici do majeur de la mineur, alors qu'un décompte d'accords distincts ne le peut pas ?

> *Solution :* Les deux tonalités contiennent les quatre accords, donc le décompte est à égalité. Dans les durées, do, mi et sol pèsent bien plus que la, et do pèse le plus. Le profil de do majeur est le plus haut sur do, donc sa corrélation avec le passage bat celle de la mineur, dont le profil est le plus haut sur la.

---

## 7. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26) ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Le service et ses appelants sont inchangés aujourd'hui sur la branche `main` de GA. Les nombres viennent de deux sources. La [leçon 11 de ga-ai](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/ga-ai/11-the-chords-the-key-skill-reads.md) de Learn compile le service de GA et imprime ses réponses, sous l'étiquette `6baf32e`, le dernier commit qui a modifié le service. Les autres nombres viennent d'une transcription Python, ligne à ligne, du service, de l'outil du chatbot et de l'outil à tableau, qui reproduit chaque réponse que Learn imprime pour cette version du service, sur 53 lignes.

**Un service, six appelants.** [`KeyIdentificationService.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L175) note les 30 tonalités du §1 avec le motif majeur et le [motif du mineur naturel](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L40), et compte les [accords distincts](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L182). Les compétences [`KeyIdentificationSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L47) et [`ProgressionCompletionSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ProgressionCompletionSkill.cs#L51) du chatbot, et l'outil MCP [`ga_key_identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L62), l'appellent sur des accords lus dans une phrase. L'outil MCP [`ga_key_from_progression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L177) et les fermetures DSL [`domain.analyzeProgression`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L405) et [`domain.progressionCompletion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L739) l'appellent sur une liste d'accords.

**Le V du mineur : dans l'ordre, pas dans le décompte.** Le motif du mineur naturel place un accord parfait mineur sur le cinquième degré, et une septième de dominante ne compte dans une tonalité mineure que sur le [septième degré](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L207), comme VII7, si bien que ni E ni E7 ne comptent en la mineur. GA a choisi le décompte naturel du §2, avec lequel C E7 Am F met quatre tonalités à égalité et do majeur vient en premier par son accord d'ouverture. La cadence revient dans l'ordre des candidats :

```csharp
            .Where(s => s.Candidate.MatchCount > 0)
            .OrderByDescending(s => s.Candidate.MatchCount + s.Cadence)
            .ThenByDescending(s => s.OpensOnTonic)
            .ThenByDescending(s => s.Candidate.Key.EndsWith("major", StringComparison.OrdinalIgnoreCase))
            .ThenBy(s => s.Candidate.Key)
            .Select(s => s.Candidate)];
```

[`CadenceWeight`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L233) ajoute 2 quand les deux derniers accords sont le V de la tonalité, en accord parfait majeur ou en septième de dominante, puis son accord de tonique. Viennent ensuite l'accord d'ouverture et la tonalité majeure, comme au §3, et en dernier le nom de la tonalité. Am Dm E7 Am place donc la mineur en premier, à 2 sur 3. La remarque du service sur C E7 Am F G7 C dit que la mineur [correspond à plus d'accords](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L165). C'était vrai du décompte harmonique, pas de ce code : do majeur et la mineur comptent tous deux 4 sur 5, et la cadence G7–C place do majeur en premier, comme l'exige [le test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L104).

**Deux décomptes pour une progression.** [`IsChordDiatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L251) [accepte bien le V harmonique](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L265) dans une tonalité mineure, et l'indice de confiance de l'outil à tableau compte chaque accord de la liste, répétitions comprises, [avec lui](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L187). Le chatbot affiche plutôt le décompte de `Identify`, sous la forme [« N/M chords diatonic »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L105). Pour Am Dm E7 Am, l'outil à tableau donne la mineur à 4/4 (100%), comme le [test de la fermeture](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L97) l'affirme pour son indice de confiance, tandis que `Identify` compte 2 sur 3. L'outil à tableau garde l'ordre de `Identify` mais [calcule son propre score](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GuitaristProblemTools.cs#L204), si bien que sa première tonalité peut afficher la confiance la plus basse. Pour C E7 Am F G7 C, sa meilleure hypothèse est do majeur à 5/6 (83%), suivie de la mineur à 6/6 (100%). Pour C D G C, c'est do majeur à 3/4 (75%), suivi de sol majeur et mi mineur à 4/4 (100%).

**Ce que lit le chatbot.** Les accords d'une phrase sont lus par [une expression régulière](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L325) dont le `\b` final fait tomber un dièse placé devant une espace. Dans « What key is F# B C# F# in? », F♯ est lu F et C♯ est lu C. Les signes ♭ et ♯ ne sont pas lus, C° est lu comme un accord de do majeur, et CM7, CΔ7 et Cø7 sont ignorés. Les accords répétés sont [supprimés](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L299) avant que `Identify` ne les voie. « What key is C D G C in? » est lu C D G, dont les deux derniers accords sont le V–I de sol majeur, et la réponse est [sol majeur](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L92). L'analyseur d'accords change min en m, puis garde l'accord parfait en supprimant [tout à partir du premier chiffre](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L319), avec un maj, aug, sus ou add placé juste avant. Bm7♭5, écrit Bm7b5, devient Bm, un accord parfait mineur, si bien qu'un iiø7 ne correspond jamais à ii°. AM7 devient un accord de la mineur, et un [test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L149) affirme qu'AM7, lu comme un accord mineur, est diatonique à do majeur. Dans les symboles d'accords usuels, CM7 est Cmaj7, une septième majeure. Learn a posé les six progressions de manuel de sa leçon dans les 15 tonalités de leur mode, soit 90 questions. Sur [cette version](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L84), 50 placent la tonalité du manuel en premier, 13 l'ont à égalité en tête sans la placer en premier, 11 la laissent hors du groupe de tête, et 16 perdent ou lisent mal un accord.

**Le groupe de tête que voit le modèle.** L'outil remet au modèle les tonalités à égalité en tête, puis jusqu'à trois de plus, prises dans la liste ordonnée :

```csharp
        var topScore = candidates[0].MatchCount;
        var topTied  = candidates
            .Where(c => c.MatchCount == topScore)
            .Select(ToCandidate)
            .ToArray();
        var partial  = candidates
            .Skip(topTied.Length)
            .Take(MaxPartialCandidates)
            .Select(ToCandidate)
            .ToArray();
```

Le groupe de tête est découpé selon le décompte de la première tonalité, tandis que l'ordre utilise le décompte plus la cadence, si bien que les deux divergent chaque fois que la cadence fait monter une tonalité de décompte plus faible. Pour C♯m7b5 F♯7 Bm, iiø7 V7 i de si mineur, si mineur vient en premier à 1 sur 3 grâce à sa cadence. Le groupe de tête est alors formé des [six tonalités à 1 sur 3](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L103), et sol♯ mineur, à 2 sur 3, figure parmi les correspondances partielles. Cinq autres tonalités comptent 2 sur 3, la majeur, si majeur, do♭ majeur, la♭ mineur et fa♯ mineur, et n'apparaissent dans aucune des deux listes. Pour Bm7b5 E7 Am, le ii–V–i mineur du [corpus de GA lui-même](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/Progressions/README.md#L37), le groupe de tête compte six tonalités à 1 sur 3. Les correspondances partielles en répètent trois, do majeur, ré majeur et fa majeur, et les quatre tonalités à 2 sur 3, la majeur, mi mineur, fa♯ mineur et sol majeur, sont laissées de côté. Le prompt de la compétence appelle le groupe de tête [« all tied at the highest score »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/KeyIdentificationSkill.cs#L102), ce qu'il n'est pas ici. Le test du corpus utilise une deuxième définition, le [décompte le plus élevé](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Corpus/ProgressionCorpusMatrixTests.cs#L440) parmi toutes les tonalités, qui laisse la mineur hors du groupe de tête pour Bm7b5 E7 Am.

**Tonalités enharmoniques et tonalités relatives.** Les fondamentales des accords deviennent des [classes de hauteurs](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L106) avant la notation, si bien que les jumelles enharmoniques du §5 reçoivent toujours le même score, et c'est le [nom de la tonalité](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L227) qui les départage. D♭ G♭ A♭ D♭ place [do♯ majeur en premier](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L88), et les 13 questions de la grille de Learn qui mettent la tonalité du manuel à égalité en tête sans la placer en premier sont toutes de telles égalités. La relative de chaque tonalité est la [première tonalité de l'autre mode](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Tonal/KeyIdentificationService.cs#L98) qui a les mêmes classes de hauteurs, si bien que [6 des 30](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L107) sont écrites à partir de la jumelle : la relative de si majeur est donnée comme la♭ mineur, et celle de sol♯ mineur comme do♭ majeur.

**Chiffres romains.** [`romanFor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L355) prend le degré d'après la position de la fondamentale dans la gamme majeure ou mineure naturelle, et la casse et le signe d'après l'accord. Am Dm E7 Am est étiqueté [i iv V i](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L99), et C Bdim Bm7b5 Caug en do majeur [I vii° viiø I+](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Apps/GaMcpServer.Tests/GuitaristProblemToolsTests.cs#L110). Une fondamentale hors de la gamme reçoit [un point d'interrogation](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L374), si bien que B♭ en do majeur donne « ? », et non ♭VII. Il n'y a pas de notation de dominante secondaire : E7 en do majeur est étiqueté par son degré, comme l'accord III du §4.

**Ce que dit la documentation.** Les instructions de la compétence donnent un [exemple à candidat unique](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L60), Dm G C en do majeur à 3/3, mais l'outil renvoie do majeur et la mineur [à égalité](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/ga-ai/expected/l11.txt#L9), comme le sont toujours des tonalités relatives. Les instructions attendent [« almost always 2 »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L64) tonalités à égalité, et la documentation de l'outil [« often 1 element »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L131) ; les ensembles enharmoniques en donnent quatre, et les exemples ci-dessus six. Les instructions renvoient aussi au service à [un chemin](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/key-identification/SKILL.md#L88) où il ne se trouve plus. Un commentaire de test dit que [si mineur n'a pas A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L86) comme accord parfait majeur. En réalité, A est le VII de si mineur naturel, et la relative de mi majeur est do♯ mineur ; l'assertion elle-même tient.

Les issues [#771](https://github.com/GuitarAlchemist/ga/issues/771) et [#772](https://github.com/GuitarAlchemist/ga/issues/772) de GA, toutes deux ouvertes, signalent la façon dont le chatbot lit les accords et regroupe le groupe de tête, les égalités enharmoniques, les tonalités relatives et l'exemple à candidat unique. Corriger tout cela revient aux responsables de GA ; cette leçon ne fait que le décrire.

### Exercice pratique

`ga_key_identify` répond sol majeur pour « What key is C D G C in? », tandis que `ga_key_from_progression`, avec ["C", "D", "G", "C"], répond do majeur. Expliquez les deux réponses.

> *Solution :* L'outil du chatbot lit C D G, parce qu'il supprime le C répété. Ses deux derniers accords, D et G, sont le V–I de sol majeur, si bien que sol majeur reçoit le poids de cadence en plus de son décompte de 3. L'outil à tableau garde la liste telle quelle, si bien que la fin est G–C, V–I de do majeur. Le décompte de 2 de do majeur plus le poids de cadence de 2 bat alors les 3 de sol majeur. Do majeur est la réponse du manuel : D est V/V. L'outil à tableau la place pourtant en premier avec la confiance la plus basse, 3/4 (75%), contre le 4/4 (100%) de sol majeur.

---

## 8. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire ga-ai de Learn, qui compile le service de GA. Rien n'y est une mesure. Les prédictions viennent de la transcription du §7 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape s'exécute dans le processus même du laboratoire et appelle directement les fonctions, jamais un serveur MCP en marche ni un modèle de langage.

1. **Identify sur un corpus fixe.** Appeler `Identify` sur Am F C G, C G Am F, C E7 Am F G7 C, Am Dm E7 Am, D C♯7 F♯m, C D G C, Dm7 G7, G F C G, C B♭ F C (écrit C Bb F C) et Dm7 Em7 Dm7 Em7. Prédiction, première tonalité et son décompte : la mineur 4/4, do majeur 4/4, do majeur 4/5, la mineur 2/3, fa♯ mineur 2/3, do majeur 2/3, do majeur 2/2, do majeur 3/3, fa majeur 3/3 et do majeur 2/2.
2. **L'outil du chatbot sur les mêmes progressions.** Demander à `KeyIdentificationMcpTools.IdentifyKey` « What key is … in? » pour chacune. Prédiction : C D G C est lu C D G et reçoit la réponse sol majeur, avec mi mineur à égalité ; Am Dm E7 Am est lu Am Dm E7, avec la mineur, do majeur, fa majeur et ré mineur à égalité à 2/3, la mineur en premier.
3. **L'outil à tableau.** Appeler `GaKeyFromProgression` sur C E7 Am F G7 C et C D G C. Prédiction : do majeur à 5/6 (83%) devant la mineur à 6/6 (100%), et do majeur à 3/4 (75%) devant sol majeur et mi mineur à 4/4 (100%).
4. **Deux définitions du groupe de tête.** Pour Bm7b5 E7 Am, calculer le groupe de tête de l'outil et ses correspondances partielles, et le groupe de tête du test du corpus. Prédiction : six tonalités à 1/3 avec la mineur en premier ; correspondances partielles do majeur, ré majeur et fa majeur, déjà dans le groupe de tête ; le groupe de tête du corpus la majeur, mi mineur, fa♯ mineur et sol majeur, sans la mineur.
5. **Le V harmonique compté.** Dans une copie du service à l'intérieur du laboratoire, jamais dans GA lui-même, compter un accord parfait majeur ou une septième de dominante sur le cinquième degré d'une tonalité mineure. Prédiction : Am Dm E7 Am donne la mineur 3/3, seule ; C E7 Am F donne la mineur 4/4 devant do majeur 3/4 ; C E7 Am F G7 C place encore do majeur en premier, à 4/5 plus la cadence, devant la mineur à 5/5.
6. **Orthographe enharmonique.** Appeler `Identify` sur D♭ G♭ A♭ D♭ et sur C♯ F♯ G♯ C♯, tous deux sous forme de listes. Prédiction : la même réponse pour les deux, do♯ majeur en premier, puis ré♭ majeur.

### Exercice pratique

L'étape 5 change le décompte. Quel résultat montrerait que le changement vaut la peine, et lequel montrerait qu'il ne la vaut pas ?

> *Solution :* Il vaut la peine si des cadences en mineur comme Am Dm E7 Am sont trouvées sans l'aide de l'ordre, tandis que les progressions en majeur avec une dominante secondaire gardent leur tonalité. C E7 Am F montre qu'il ne la vaut pas : la relative mineure gagne, puisqu'aucune cadence finale ne vient corriger le décompte. Un test équitable demande un corpus qui contienne les deux sortes, avec les tonalités notées avant l'exécution.

---

## 9. Pièges courants

- **Prendre une égalité pour une réponse.** Une tonalité et sa relative mineure sont toujours à égalité sur leurs accords ; c'est l'accentuation qui les départage.
- **Compter le V harmonique partout.** Cela trouve les cadences en mineur, et attire les dominantes secondaires des tonalités majeures vers la relative mineure.
- **Lire une liste d'accords sans son ordre ni ses répétitions.** La cadence est dans l'ordre, et une tonique répétée est une accentuation.
- **Réduire les accords à des classes de hauteurs avant de choisir entre tonalités enharmoniques.** L'orthographe est la preuve.
- **Lire « N/M chords diatonic » comme une confiance.** Deux des outils de GA calculent des N différents pour les mêmes accords, et la première tonalité peut afficher le plus bas.
- **Nommer un mode avec un détecteur de tonalités majeures et mineures.** Les vamps doriens et mixolydiens ressortent comme la tonalité dont ils utilisent les notes.
- **Se fier à un groupe de tête sans demander comment il a été découpé.** Découpés selon le décompte de la première tonalité ou selon le décompte le plus élevé de toutes les tonalités, les mêmes candidats donnent des listes différentes, et aucun des deux découpages ne suit l'ordre par décompte plus cadence.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Accord parfait diatonique** | Un accord parfait construit avec les notes de la gamme d'une tonalité, sur l'un de ses sept degrés |
| **Paire relative** | Une tonalité majeure et la tonalité mineure bâtie sur son sixième degré, avec la même armure et les mêmes accords parfaits |
| **Mineur naturel** | La gamme mineure formée des notes de l'armure ; son accord parfait du cinquième degré est mineur |
| **Mineur harmonique** | La gamme mineure au septième degré haussé, qui rend majeur l'accord parfait du cinquième degré |
| **Cadence parfaite** | V ou V7 vers I (ou i), la fin qui confirme une tonalité |
| **Dominante secondaire** | Le V ou V7 d'un accord autre que I, noté V7/vi pour la septième de dominante de vi |
| **Chiffre romain** | Le degré d'un accord dans la tonalité, avec une casse et des signes pour sa qualité |
| **Tonalités enharmoniques** | Des tonalités de même mode dont les toniques sont une même hauteur écrite de deux façons, comme ré♭ majeur et do♯ majeur |
| **Profil de tonalité** | Le poids de chacune des 12 classes de hauteurs dans un contexte de tonalité majeure ou mineure |
| **Algorithme de Krumhansl–Schmuckler** | Corréler les durées d'un passage par classe de hauteurs avec les 24 rotations des profils de tonalité |

---

## Auto-évaluation

**1. Quelles tonalités sont à égalité pour Em C G D, et laquelle l'ouverture désigne-t-elle ?**
> Sol majeur et mi mineur comptent 4 sur 4. La progression s'ouvre sur Em, l'accord de tonique de mi mineur, si bien qu'un détecteur qui pèse l'accord d'ouverture choisit mi mineur, comme l'exige le [test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/KeyIdentificationServiceTests.cs#L122) de GA.

**2. Pourquoi un décompte sur le mineur naturel laisse-t-il Am Dm E7 Am à 2 sur 3 pour la mineur ?**
> L'accord parfait de E7 est mi majeur, le V du mineur harmonique. Le cinquième degré du mineur naturel porte Em, si bien que E7 n'est pas compté.

**3. Une grille indique D♭ G♭ A♭ D♭, et un détecteur de tonalité répond do♯ majeur. Qu'est-ce qui a mal tourné ?**
> Le détecteur a transformé les accords en classes de hauteurs, que ré♭ majeur et do♯ majeur partagent, puis a choisi par le nom. L'orthographe, avec cinq bémols plutôt que sept dièses, dit ré♭ majeur.

**4. Pour C♯m7b5 F♯7 Bm, `ga_key_identify` renvoie six tonalités comme candidates de tête, [« tied at the highest match count »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/KeyIdentificationMcpTools.cs#L140), à 1 sur 3. Dans quelle tonalité est-elle, et que manque-t-il ?**
> Si mineur : iiø7 V7 i. Le groupe de tête est découpé selon le décompte de la première tonalité, tandis que l'ordre ajoute la cadence. Les tonalités qui comptent 2 sur 3 manquent au groupe de tête : sol♯ mineur figure parmi les correspondances partielles, et cinq autres n'apparaissent nulle part.

**Critères de réussite :** Nommer les accords parfaits d'une tonalité et de sa relative ; noter une progression en comptant ses accords parfaits diatoniques et départager par la cadence et l'accord d'ouverture ; expliquer l'angle mort du décompte en mineur naturel et le prix du V harmonique compté ; étiqueter une progression en chiffres romains, dominantes secondaires comprises ; distinguer tonalités enharmoniques et tonalités relatives par l'orthographe ; et dire quel outil de GA affiche quel décompte.

---

## Bases de recherche

- M. Gotham, K. Gullings, C. Hamm, B. Hughes, B. Jarvis, M. Lavengood et J. Peterson, *Open Music Theory*, version 2, VIVA Open Publishing, 2021 (CC BY-SA 4.0) : les accords parfaits diatoniques, les mineurs naturel et harmonique, et les chiffres romains
- S. Kostka, D. Payne et B. Almén, *Tonal Harmony*, 7e édition, McGraw-Hill, 2013 : chiffres romains, cadences et dominantes secondaires
- H. C. Longuet-Higgins et M. J. Steedman, « On interpreting Bach », *Machine Intelligence* 6, 1971, p. 221–241 : l'identification de la tonalité par élimination des tonalités, note après note
- C. L. Krumhansl et E. J. Kessler, « Tracing the dynamic changes in perceived tonal organization in a spatial representation of musical keys », *Psychological Review* 89(4), 1982, p. 334–368 : les profils de tonalité obtenus par sons-sondes
- C. L. Krumhansl, *Cognitive Foundations of Musical Pitch*, Oxford University Press, 1990, chapitre 4, « A key-finding algorithm based on tonal hierarchies » : l'algorithme de Krumhansl–Schmuckler
- D. Temperley, « What's key for key? The Krumhansl-Schmuckler key-finding algorithm reconsidered », *Music Perception* 17(1), 1999, p. 65–100
- D. Temperley, *The Cognition of Basic Musical Structures*, MIT Press, 2001 : l'identification de la tonalité par règles de préférence
- Wikipedia, « Chord names and symbols (popular music) » : CM7, CΔ7 et Cmaj7 comme noms de la septième majeure
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §7 renvoie à sa ligne ; issues #771 et #772 de GA
- Learn, leçon 11 de ga-ai et sa sortie attendue au commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3` : les réponses compilées du service de GA citées au §7
- Expérience : proposée au §8, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
