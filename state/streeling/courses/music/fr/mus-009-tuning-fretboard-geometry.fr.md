---
module_id: mus-009-tuning-fretboard-geometry
department: music
course: Accordage et géométrie du manche
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity, mat-004-vectors-matrices-norms, phy-001-science-of-guitar-sound]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Accordage et géométrie du manche — Une hauteur, plusieurs emplacements

> **Département de musique** | Stade : Nigredo (Débutant) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Écrire un accordage comme un vecteur de six hauteurs et donner la hauteur de n'importe quelle corde à n'importe quelle case
- Trouver tous les emplacements où se joue une hauteur donnée, et compter les emplacements de chaque hauteur du manche
- Décrire ce qu'un accordage alternatif change et ce qu'il laisse intact, comme la différence de deux vecteurs d'accordage
- Déduire l'emplacement des frettes du demi-ton tempéré, et calculer la position des frettes pour n'importe quel diapason
- Repérer ce que GA calcule pour les accordages, les positions et les distances entre frettes, et où son catalogue et ses tests s'écartent de la théorie

---

## 1. L'accordage comme vecteur

Les guitaristes numérotent les cordes depuis l'aigu : la corde 1 est la plus fine, celle qui sonne le plus haut, la corde 6 la plus grosse. En accordage standard, elles sonnent, de la corde 1 à la corde 6, mi4, si3, sol3, ré3, la2 et mi2, MIDI 64, 59, 55, 50, 45 et 40. Les numéros d'octave sont ceux de la notation scientifique, comme dans MUS-007 : le do central est do4, MIDI 60 (la tradition française l'appelle do3).

Dans le langage de MAT-004, l'accordage est un vecteur avec une composante par corde, t = (t₁, …, t₆) = (64, 59, 55, 50, 45, 40). Chaque case ajoute un demi-ton, si bien que la corde s à la case f donne t_s + f. Une forme d'accord est un vecteur de cases, une par corde. Les guitaristes l'écrivent à partir de la corde 6 : dans la forme ouverte de mi 022100, les cordes 6 à 1 sont aux cases 0, 2, 2, 1, 0 et 0. Rangée corde 1 en premier, comme t, la forme vaut (0, 0, 1, 2, 2, 0), et les hauteurs qu'elle fait sonner sont la somme des deux vecteurs : (64, 59, 56, 52, 47, 40). Lu depuis la corde 6, cela donne 40, 47, 52, 56, 59 et 64, soit mi2, si2, mi3, sol♯3, si3 et mi4.

Les différences entre composantes voisines sont les intervalles entre les cordes. En montant depuis la corde 6, elles valent 5, 5, 5, 4 et 5 demi-tons : des quartes justes, sauf la tierce majeure de la corde 3 à la corde 2. Ainsi la case 5 d'une corde donne la corde à vide suivante vers l'aigu, sauf sur la corde 3, où c'est la case 4.

### Exercice pratique

Dans la forme barrée de fa 133211, écrite à partir de la corde 6, quelles hauteurs donnent les cordes 6 et 3 ?

> *Solution :* La corde 6 est à la case 1 : 40 + 1 = 41, fa2. La corde 3 est à la case 2 : 55 + 2 = 57, la3, la tierce majeure de l'accord.

---

## 2. Une hauteur, plusieurs emplacements

Une hauteur p se joue sur la corde s quand la case qu'il lui faut, p − t_s, est comprise entre 0 et le nombre de cases. La guitare par défaut de GA a 24 cases. Sur elle, la4, MIDI 69, a cinq emplacements : corde 1 à la case 5, corde 2 à la case 10, corde 3 à la case 14, corde 4 à la case 19 et corde 5 à la case 24. La corde 6 demanderait la case 29. Sur une guitare à 22 cases, la corde 5 disparaît et la4 a quatre emplacements.

Le même décompte vaut pour chaque hauteur. Une guitare à 24 cases en accordage standard va de mi2, MIDI 40, à mi6, MIDI 64 + 24 = 88 : 49 hauteurs. Parmi elles, 10 ont un emplacement, 9 en ont deux, 10 en ont trois, 9 en ont quatre et 10 en ont cinq. Une seule hauteur se joue sur les six cordes : mi4, la première corde à vide, que la corde 6 atteint à la case 24. Les hauteurs à un seul emplacement sont les cinq plus graves, de mi2 à sol♯2, que seule la corde 6 possède, et les cinq plus aiguës, de do6 à mi6, que seule la corde 1 atteint.

Une hauteur n'est pas une classe de hauteurs. La classe de hauteurs la, à n'importe quelle octave, a 13 emplacements sur le même manche : la2 en a 2, la3 en a 4, la4 en a 5 et la5 en a 2. Une grille de doigtés qui marque « tous les la » en montre 13 ; un guitariste à qui l'on demande la4 a besoin des 5.

### Exercice pratique

Combien d'emplacements a mi4 sur une guitare à 22 cases, et à quelles cases ?

> *Solution :* Cinq : corde 1 à vide, corde 2 à la case 5, corde 3 à la case 9, corde 4 à la case 14 et corde 5 à la case 19. La corde 6 demanderait la case 24, qu'une guitare à 22 cases n'a pas.

---

## 3. Changer d'accordage

Un accordage alternatif est un nouveau vecteur t′, et la différence Δ = t′ − t dit, corde par corde, de combien de demi-tons chaque corde a été tournée. En drop D, écrit ré2 la2 ré3 sol3 si3 mi4 à partir de la corde 6, seule la corde 6 change, de mi2 à ré2 : Δ = (0, 0, 0, 0, 0, −2), rangé corde 1 en premier comme t. DADGAD, ré2 la2 ré3 sol3 la3 ré4, donne Δ = (−2, −2, 0, 0, 0, −2), et l'open G, ré2 sol2 ré3 sol3 si3 ré4, donne Δ = (−2, 0, 0, 0, −2, −2).

Ce qui change se limite aux cordes où Δ n'est pas nul. Chaque note d'une telle corde se déplace : pour garder une hauteur, sa case devient f − Δ_s. En drop D, mi2 demande la corde 6 à la case 2, et la guitare descend maintenant jusqu'à ré2, MIDI 38. Une forme gardée avec les mêmes cases donne t′ plus les cases : la forme ouverte de mi 022100 a désormais ré2 à la basse. L'intervalle de la corde 6 à la corde 5 devient 7 demi-tons, une quinte, si bien que les cordes 6, 5 et 4 à une même case donnent une fondamentale, une quinte et une octave : à vide, elles sonnent ré2, la2 et ré3.

Ce qui reste, c'est tout le reste. Les autres cordes, la règle t_s + f et les frettes elles-mêmes sont inchangées, de même que le nombre d'emplacements de toute hauteur que les cordes changées n'atteignent dans aucun des deux accordages : en drop D, la4 garde ses cinq emplacements.

Les normes de MAT-004 mesurent un réaccordage. La norme 1, ‖Δ‖₁, additionne les demi-tons tournés : 2 pour le drop D, 6 pour DADGAD et l'open G. La norme ∞, ‖Δ‖∞, est le plus grand tour sur une seule corde : 2 pour les trois. C'est elle qui compte pour la corde : d'après la formule de PHY-001, à longueur fixe, la tension d'une corde suit le carré de sa fréquence, si bien que baisser une corde de k demi-tons multiplie sa tension par 2^(−2k/12). Deux demi-tons plus bas, il lui reste environ 0,79 de sa tension.

### Exercice pratique

L'open D s'écrit ré2 la2 ré3 fa♯3 la3 ré4, à partir de la corde 6. Donnez son Δ, ses deux normes, et les cordes qui gardent leur hauteur.

> *Solution :* t′ = (62, 57, 54, 50, 45, 38), donc Δ = (−2, −2, −1, 0, 0, −2) : ‖Δ‖₁ = 7 et ‖Δ‖∞ = 2. Les cordes 4 et 5 gardent leur hauteur.

---

## 4. Où vont les frettes

À tension égale et pour la même corde, la fréquence d'une corde vibrante est inversement proportionnelle à sa longueur, comme le montre PHY-001. Un demi-ton multiplie la fréquence par 2^(1/12), donc la corde doit être 2^(−1/12) fois aussi longue. Appelons L le **diapason**, la longueur vibrante de la corde à vide, du sillet de tête au sillet du chevalet. À la case n, la corde vibre encore sur L · 2^(−n/12), si bien que la frette se trouve à une distance du sillet de

d(n) = L · (1 − 2^(−n/12)).

La frette 12 partage la corde en deux : d(12) = L/2. La frette 24 en laisse un quart : d(24) = 3L/4. Sur un diapason de 648 mm, les frettes 1, 5, 7, 12 et 24 sont à 36,4, 162,5, 215,5, 324 et 486 mm du sillet. Les frettes ne sont pas également espacées. Chaque intervalle vaut 2^(−1/12), environ 0,944, fois le précédent, si bien que l'intervalle de la frette 12 à la frette 13, 18,2 mm, est la moitié du premier. Autrement dit, l'intervalle qui suit chaque frette vaut 1/17,817 de la longueur qui vibre encore de cette frette au sillet du chevalet, puisque 1/(1 − 2^(−1/12)) vaut environ 17,817.

Le diapason change les distances, pas les proportions : sur tout diapason, la frette 12 est au milieu de la corde, à 314 mm sur un diapason de 628 mm et à 432 mm sur une basse de 864 mm. Certaines frettes tombent près de fractions simples de la corde. Sur un diapason de 648 mm, la frette 7 est à 0,5 mm en deçà du tiers, 216 mm, et la frette 5 à 0,5 mm au-delà du quart, 162 mm. Le tiers et le quart de la corde sont les points où l'on joue les troisième et quatrième harmoniques, comme PHY-001 joue le deuxième à la frette 12.

### Exercice pratique

Sur un diapason de 628 mm, où est la frette 12, et à quelle distance du sillet est la première frette ?

> *Solution :* La frette 12 est à 628/2 = 314 mm. La première frette est à 628 · (1 − 2^(−1/12)), environ 35,2 mm.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26) ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA à `8fe33f8`. Learn, le site de cours de l'écosystème, propose un cours music-theory-ga dont les leçons [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) et [8](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx) compilent une version antérieure de GA, `a826864`. Les autres nombres ci-dessous viennent d'une transcription en Python, ligne à ligne, du code GA nommé.

**Les accordages et les positions suivent les §1 et §2.** [`Tuning.Default`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L23) lit « E2 A2 D3 G3 B3 E4 » et range la corde 1 en premier. Pour savoir quelle extrémité d'un accordage écrit est la corde 1, il [compte les pas montants et descendants](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L121) entre cordes voisines, de sorte qu'un accordage rentrant, dont les cordes, en comptant depuis la corde 1, ne sont pas rangées par hauteur décroissante, soit lu dans le sens où il est écrit. La leçon 8 de Learn a relevé le [banjo à 5 cordes](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l8.txt#L29) comme une différence : GA `a826864` prenait le bourdon, la corde courte en sol4 que les joueurs numérotent 5, pour la corde 1. Le commit `4e23984` a changé la règle, et les tests de GA attendent désormais [ré4 comme corde 1](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/TuningTests.cs#L47). [`Fretboard.GetNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L48) ajoute la case à la [note MIDI de la corde à vide](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L62), comme au §1, puis [ne rend que la note](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L67), sans son octave : la corde 1 et la corde 6, à vide, donnent toutes deux mi. Il prend un indice de corde à partir de 0, et l'indice 0 est la corde 1, le mi aigu, comme le disent les [tests](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/FretboardTests.cs#L11) de GA. Son propre commentaire dit l'inverse : [« 0 = lowest string »](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L45). Le manche par défaut a [24 cases](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L109).

[`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) prend une note sans octave et [compare des classes de hauteurs](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L82). Il répond à la question du §2 sur les classes de hauteurs, pas à celle sur les hauteurs : pour la sur le manche par défaut, il rend 13 positions, par transcription. Chacune [porte sa note MIDI](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L87), et garder celles qui valent 69 laisse les cinq emplacements de la4. Dans la leçon 1 de Learn, GA `a826864` comparait encore des notes entières et ne trouvait [aucune position](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L61) pour `Note.Sharp.C`, qui n'est jamais égal à la note chromatique que rend `GetNote` ; le commit `3a7c242` est passé aux classes de hauteurs. Un manche en drop D se construit à partir de ses hauteurs, comme le fait la leçon 1 de Learn pour son [exercice en drop D](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L78).

**Les distances entre frettes suivent le §4.** [`CalculateFretPositionMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L35) calcule [L · (1 − 2^(−n/12))](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L42), avec un [diapason par défaut](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L334) de [648 mm](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L331). Par transcription, il donne les distances du §4, 324 mm à la frette 12 et 486 à la frette 24. Deux limites l'entourent :

- [`CalculateStringSpacingMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L78) élargit le manche en ligne droite de 43 mm au sillet à 52 mm au chevalet, puis [divise par 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L87), le nombre d'écarts entre six cordes, quel que soit l'instrument : 8,6 mm au sillet, 9,5 à la frette 12.
- L'analyseur de voicings mesure l'étendue d'un voicing avec [`CalculateFretDistanceMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs#L103) sans lui passer de diapason, si bien que toute étendue est mesurée à 648 mm.

Le fichier de test du calculateur est [retiré de la compilation](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L47), et aucun test compilé n'appelle directement ses méthodes de distance : les tests de l'analyseur de voicings atteignent `CalculateFretDistanceMm` par `CalculatePlayability` et vérifient la difficulté et la forme d'accord qu'il rend. Le fichier ne compilerait d'ailleurs pas en l'état : il appelle [`CalculateStringSpacingMM`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L169), un nom que la classe n'a pas. Il écrit aussi à la main la note MIDI de chacune de ses 41 positions, et d'après t_s + f, 8 d'entre elles sont fausses. Dans son accord de mi ouvert, la corde 3 à la case 1 est [écrite 55](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L62), sol3, alors qu'elle sonne sol♯3, 56. L'analyse de jouabilité ne lit que les cordes et les cases, si bien que ces nombres ne changeraient aucun résultat.

**Le catalogue d'accordages contient deux erreurs d'octave.** Depuis le commit `49bd286`, GA lit l'intégralité de [`Instruments.yaml`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/InstrumentsConfig.fs#L34), et `InstrumentTool.GetTuning`, un outil du serveur MCP de GA, par lequel des assistants d'IA appellent GA, [rend la ligne d'un accordage](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/InstrumentTool.cs#L27) telle qu'elle est écrite. Des 11 accordages à six cordes qu'il range sous `Guitar`, 9 ont un ‖Δ‖∞ de 2 ou moins par rapport au standard. Les deux autres placent la corde 2 une octave trop bas :

- [`OpenCMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L536) vaut « C2 G2 C3 G3 C3 E4 ». L'open C, do2 sol2 do3 sol3 do4 mi4, donne Δ = (0, 1, 0, −2, −2, −4), avec ‖Δ‖∞ = 4 : il monte la corde 2 d'un demi-ton, de si3 à do4. La ligne du catalogue donne Δ = (0, −11, 0, −2, −2, −4) : son C3 baisserait la corde 2 de 11 demi-tons, à 2^(−22/12), environ 0,28 de sa tension.
- [`OpenAMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L560) vaut « E2 A2 E3 A3 C#3 E4 », dont le C♯3 baisse la corde 2 de 10 demi-tons.

Un code qui compare les accordages par classes de hauteurs ne peut pas voir une telle erreur. La compétence d'accordages alternatifs de GA, pour ses neuf accordages à elle, [réduit chaque différence modulo 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L257) et [la ramène](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L258) entre −5 et +6 : de si à do, elle indiquerait +1, avec ou sans l'erreur d'octave.

Corriger tout cela revient aux responsables de GA ; cette leçon se contente de le décrire.

### Exercice pratique

Le catalogue de GA écrit l'open A mi2 la2 mi3 la3 do♯3 mi4. L'open A monte les cordes 4, 3 et 2 d'un ton par rapport au standard. Donnez Δ pour les deux, et dites quelle composante trahit l'erreur.

> *Solution :* L'open A est mi2 la2 mi3 la3 do♯4 mi4 : Δ = (0, 2, 2, 2, 0, 0), avec ‖Δ‖∞ = 2. La ligne du catalogue donne Δ = (0, −10, 2, 2, 0, 0), avec ‖Δ‖∞ = 10. La deuxième composante, la corde 2 baissée de 10 demi-tons, trahit l'erreur.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `5c3a52a`. Rien n'y est une mesure. Les prédictions viennent des §2 à §5 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types de GA dans le processus du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Les emplacements de chaque hauteur.** Sur le manche par défaut, pour chaque note MIDI de 40 à 88, gardez les positions que `GetPositionsForNote` rend pour sa classe de hauteurs et qui portent cette note MIDI. Prédiction : 10 hauteurs ont un emplacement, 9 deux, 10 trois, 9 quatre, 10 cinq, et mi4 seule six.
2. **La4 dans deux accordages.** Demandez la sur le manche par défaut et sur un manche en drop D à 24 cases. Prédiction : 13 positions sur chacun, et les mêmes 5 avec la note MIDI 69.
3. **L'indice de corde et l'octave.** Appelez `GetNote(0, 0)` et `GetNote(5, 0)`, puis gardez les positions à vide que `GetPositionsForNote` rend pour mi. Prédiction : mi les deux fois, sans octave ; les positions sont la corde 1 avec la note MIDI 64 et la corde 6 avec 40, donc l'indice 0 est la corde aiguë.
4. **Les distances entre frettes.** Comparez `CalculateFretPositionMm(n)` avec L · (1 − 2^(−n/12)) pour n de 0 à 24 à 648 mm. Prédiction : égaux aux arrondis près, avec 324 à la frette 12 et 486 à la frette 24.
5. **Le catalogue.** Lisez les accordages à six cordes rangés sous `Guitar` dans `Instruments.yaml` par `InstrumentsConfig`, analysez chacun et calculez son Δ par rapport au standard. Prédiction : 11 accordages ; 9 avec un ‖Δ‖∞ de 2 ou moins, `OpenCMajor` avec 11 et `OpenAMajor` avec 10.

### Exercice pratique

L'étape 5 signale les accordages par ‖Δ‖∞. Pourquoi pas par ‖Δ‖₁ ?

> *Solution :* ‖Δ‖₁ additionne les tours des six cordes, si bien que beaucoup de petits tours ordinaires s'accumulent. Accorder toutes les cordes un ton plus bas, ré2 sol2 do3 fa3 la3 ré4, donne ‖Δ‖₁ = 12, proche des 14 de la ligne d'open A du catalogue. ‖Δ‖∞ les sépare, 2 contre 10 : elle regarde le plus grand tour sur une seule corde, celui qu'une erreur d'octave rend grand et dont dépend la tension d'une corde.

---

## 7. Pièges courants

- **Numéroter les cordes depuis le grave.** La corde 1 est la plus fine, celle qui sonne le plus haut.
- **Compter les emplacements d'une classe de hauteurs.** Sur une guitare à 24 cases, la a 13 emplacements ; la4 en a 5.
- **Déplacer toutes les formes pour un nouvel accordage.** Seules les cordes où Δ n'est pas nul changent.
- **Espacer les frettes régulièrement.** Chaque intervalle vaut environ 0,944 fois le précédent ; la frette 12 est au milieu de la corde.
- **Changer les proportions avec le diapason.** Un diapason plus long déplace chaque frette, mais la frette 12 reste au milieu.
- **Lire un accordage comme des classes de hauteurs.** Une erreur d'octave sur une corde est invisible modulo 12.
- **Se fier au commentaire de `GetNote`.** Dans GA, l'indice de corde 0 est le mi aigu, pas la corde la plus grave.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Numéro de corde** | Le rang d'une corde compté depuis l'aigu : la corde 1 est la plus fine |
| **Vecteur d'accordage** | Les numéros MIDI des cordes à vide, t = (t₁, …, t₆) ; la corde s à la case f donne t_s + f |
| **Emplacement** | Une corde et une case qui jouent une hauteur donnée ; une classe de hauteurs a les emplacements de toutes ses octaves |
| **Vecteur de réaccordage** | Δ = t′ − t, les demi-tons dont chaque corde est tournée ; ‖Δ‖₁ les additionne, ‖Δ‖∞ prend le plus grand |
| **Diapason** | La longueur vibrante d'une corde à vide, du sillet de tête au sillet du chevalet |
| **Position d'une frette** | La distance de la frette n au sillet, d(n) = L · (1 − 2^(−n/12)) |
| **Accordage rentrant** | Un accordage dont les cordes, en comptant depuis la corde 1, ne sont pas rangées par hauteur décroissante : une corde sonne plus haut que celle qui la précède |

---

## Auto-évaluation

**1. Où est la frette 12 sur un diapason de 648 mm ?**
> À 324 mm du sillet : d(12) = 648 · (1 − 1/2).

**2. Sur une guitare à 24 cases en accordage standard, où peut-on jouer la4 ?**
> À cinq emplacements : corde 1 à la case 5, corde 2 à la case 10, corde 3 à la case 14, corde 4 à la case 19 et corde 5 à la case 24.

**3. Donnez le vecteur de réaccordage du drop D et ses deux normes.**
> Δ = (0, 0, 0, 0, 0, −2), corde 1 en premier : ‖Δ‖₁ = 2 et ‖Δ‖∞ = 2.

**4. Par transcription, [`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) de GA rend 13 positions pour la sur son manche par défaut. Pourquoi plus de cinq ?**
> Il compare des classes de hauteurs, donc il rend tous les la de la2 à la5 : 2, 4, 5 et 2 emplacements. Seuls les 5 dont la note MIDI vaut 69 jouent la4.

**Critères de réussite :** Donner la hauteur de toute corde et de toute case à partir du vecteur d'accordage ; trouver et compter les emplacements d'une hauteur ; décrire un réaccordage par son Δ et ses normes ; calculer la position des frettes pour tout diapason ; et distinguer les positions par classe de hauteurs de GA des emplacements de hauteurs du §2.

---

## Bases de recherche

- T. D. Rossing, F. R. Moore et P. A. Wheeler, *The Science of Sound*, 3e éd., Addison-Wesley, 2002 : les cordes vibrantes et les instruments à cordes
- N. H. Fletcher et T. D. Rossing, *The Physics of Musical Instruments*, 2e éd., Springer, 1998 : la guitare
- Code source de GA au commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26` : chaque fait de code du §5 renvoie à sa ligne
- Learn, leçons 1 et 8 de music-theory-ga et leur sortie attendue au commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3` : les vérifications compilées de GA `a826864` citées au §5
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
