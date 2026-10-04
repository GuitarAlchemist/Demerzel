---
module_id: mus-019-transposition-capo-cross-instrument
department: music
course: Transposition, capodastre et équivalence entre instruments
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-009-tuning-fretboard-geometry, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Transposition, capodastre et équivalence entre instruments — Trois sortes d'identité

> **Département de musique** | Stade : Albedo (Intermédiaire) | Durée estimée : 45 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Transposer une hauteur, un accord, une progression ou une tonalité de n demi-tons, et écrire le résultat dans sa nouvelle tonalité
- Trouver la tonalité entendue avec un capodastre et ses formes d'accords, et les formes et la case du capodastre pour une tonalité entendue
- Dire ce que devient une forme d'accord sur un autre instrument ou sur un autre groupe de cordes
- Écrire la tonalité de la partie d'un instrument en si♭, en mi♭ ou en fa pour une tonalité réelle, et garder distincts le son réel et la hauteur écrite
- Retracer ce que GA calcule pour la transposition et le capodastre, où ses noms ou sa lecture d'une question se trompent, et ce qui lui manque

---

## 1. Transposition

L'article « Transposition (music) » de Wikipédia : « transposition refers to the process or operation of moving a collection of notes (pitches or pitch classes) up or down in pitch by a constant interval. » (la transposition désigne le procédé ou l'opération qui déplace un ensemble de notes, hauteurs ou classes de hauteurs, vers le haut ou vers le bas d'un intervalle constant.) Pour des hauteurs, l'intervalle est un nombre de demi-tons : la4, MIDI 69, monté d'une tierce majeure, 4 demi-tons, donne MIDI 73, do♯5. Les numéros d'octave sont ceux de la notation scientifique, comme dans MUS-007 : le do central est do4, MIDI 60 (la tradition française l'appelle do3). Pour des classes de hauteurs, la somme se prend modulo 12 : 9 + 4 = 13 ≡ 1. MUS-020 a noté cette opération Tn : Tn ajoute n à chaque classe de hauteurs, modulo 12.

Une transposition garde chaque intervalle, donc elle garde la qualité de chaque accord et sa place dans la tonalité. T3 envoie la triade de do majeur {0, 4, 7} sur {3, 7, 10}, mi♭ majeur, et envoie la progression C – Am – F – G, I – vi – IV – V en do majeur, sur E♭ – Cm – A♭ – B♭, I – vi – IV – V en mi♭ majeur. Chaque accord de la nouvelle progression est l'image par T3 de l'ancien.

Seul un décalage d'un nombre fixe de demi-tons est un Tn. Wikipédia distingue deux sortes de décalage :
- **Transposition chromatique.** Dans celle-ci, « every pitch in a collection of notes is shifted by the same number of semitones. For instance, transposing the pitches C4–E4–G4 upward by four semitones, one obtains the pitches E4–G♯4–B4. » (chaque hauteur d'un ensemble de notes est décalée du même nombre de demi-tons. Par exemple, en transposant les hauteurs do4–mi4–sol4 de quatre demi-tons vers le haut, on obtient mi4–sol♯4–si4.)
- **Transposition diatonique.** Chaque hauteur se déplace du même nombre de degrés d'une gamme : « transposing the pitches C4–E4–G4 up two steps in the familiar C major scale gives the pitches E4–G4–B4 » (transposer les hauteurs do4–mi4–sol4 de deux degrés dans la gamme familière de do majeur donne mi4–sol4–si4). La triade majeure est devenue mi mineur. Les degrés d'une gamme n'ont pas tous la même taille, donc ce n'est pas un Tn.

Transposer un morceau dans une autre tonalité est une transposition chromatique.

**Les demi-tons ne fixent pas le nom des notes.** Comme l'a montré MUS-007, une même classe de hauteurs a plusieurs noms. Une transposition de n demi-tons s'écrit en nommant son intervalle, par un nombre et une qualité, et en déplaçant la tonique de cet intervalle. Trois demi-tons au-dessus de do, c'est une tierce mineure, do ré mi, vers mi♭ ; ou une seconde augmentée, do ré, vers ré♯. Mi♭ majeur a trois bémols ; ré♯ majeur demanderait neuf dièses, en comptant chaque 𝄪 pour deux. Quand seuls les demi-tons sont donnés, la tonalité qui a le moins d'altérations est le nom habituel.

La ligne des quintes de MUS-007 fait le compte. Chaque quinte juste ascendante ajoute un dièse à l'armure ou retire un bémol, donc un intervalle vaut un nombre fixe de quintes :

| Intervalle ascendant | quinte juste | seconde majeure | sixte majeure | tierce majeure | quarte juste | septième mineure | tierce mineure | sixte mineure |
|------|------|------|------|------|------|------|------|------|
| Quintes | +1 | +2 | +3 | +4 | −1 | −2 | −3 | −4 |

Transposer do majeur d'une tierce mineure vers le haut déplace son armure de −3 places : elle passe d'aucune altération à trois bémols, mi♭ majeur. Sol majeur, un dièse, monté d'une seconde majeure, reçoit trois dièses, la majeur.

### Exercice pratique

Transposez G – Em – C – D7 de trois demi-tons vers le haut. Nommez la tonalité et écrivez les accords.

> *Solution :* Trois demi-tons vers le haut, c'est une tierce mineure, −3 quintes. Sol majeur a un dièse ; un dièse et trois bémols laissent deux bémols : si♭ majeur. Les accords sont B♭ – Gm – E♭ – F7. Écrite en la♯ majeur, la tonalité demanderait dix dièses.

---

## 2. Le capodastre

L'article « Capo (musical device) » de Wikipédia définit le capodastre comme « a device a musician uses on the neck of a stringed (typically fretted) instrument to transpose and shorten the playable length of the strings—hence raising the pitch » (un dispositif qu'un musicien place sur le manche d'un instrument à cordes, en général à frettes, pour transposer et raccourcir la longueur jouable des cordes, et donc élever la hauteur). Les musiciens s'en servent « so they can play in a different key using the same fingerings as playing open (i.e., without a capo). In effect, a capo uses a fret of an instrument to create a new nut at a higher note than the instrument's actual nut. » (pour jouer dans une autre tonalité avec les mêmes doigtés qu'à vide, c'est-à-dire sans capodastre. En pratique, un capodastre se sert d'une frette de l'instrument pour créer un nouveau sillet, sur une note plus haute que le vrai sillet de l'instrument.)

Dans le langage de MUS-009, l'accordage est un vecteur t, et une corde s à la case f sonne t_s + f. Un capodastre à la case c fait sonner chaque corde à vide c demi-tons plus haut. Le nouvel accordage est t + (c, c, c, c, c, c), et la différence Δ vaut c sur chaque corde. Une forme jouée avec les cases f comptées depuis le capodastre sonne t + c + f : chaque note qu'elle joue monte de c demi-tons. Le capodastre, c'est T_c appliqué à tout ce que joue le guitariste. Wikipédia : « Playing with a capo creates the same musical effect as retuning all strings up the same number of steps. However, using a capo only affects the open note of each string. » (jouer avec un capodastre produit le même effet musical que réaccorder toutes les cordes vers le haut d'un même écart. Cependant, le capodastre n'agit que sur la note à vide de chaque corde.) Les notes frettées ne changent pas : avec le capodastre en case 3, la case 7 de la corde 6 sonne toujours si2.

**Deux noms pour un accord.** Un accord peut se nommer par la forme que font les doigts ou par ce qu'il fait entendre. Wikipédia : « a D-shaped chord can be referred to as "D" (based on the shape relative to the capo), or E (based on the absolute audible chord produced). Neither method strongly prevails over the other. » (un accord en forme de ré peut s'appeler D, d'après la forme par rapport au capodastre, ou E, d'après l'accord réellement entendu. Aucune des deux méthodes ne l'emporte nettement sur l'autre.) C'est pourquoi les guitaristes disent « forme d'accord » quand ils parlent du doigté. Avec le capodastre à la case c :

- son entendu = forme + c ;
- forme = son entendu − c.

La question de cette leçon est celle d'un guitariste : avec un capodastre en troisième case et des formes de do, dans quelle tonalité le public entend-il le morceau, et que lit un trompettiste en si♭ pour le même morceau ? Avec le capodastre en case 3, la forme de do x32010 se joue en x65343, en comptant depuis le sillet. Elle fait entendre mi♭3 sol3 si♭3 mi♭4 sol4 : mi♭ majeur, trois demi-tons au-dessus de do. La progression C – Am – F – G, jouée en formes, sonne E♭ – Cm – A♭ – B♭. Les noms entendus s'écrivent dans la tonalité entendue, par la règle du §1 : do monté d'une tierce mineure donne mi♭, pas ré♯.

**Choisir la case du capodastre.** Pour sonner dans une tonalité K avec des formes ouvertes, prenez une tonalité S qui a des accords ouverts faciles, do, la, sol, mi ou ré, et placez le capodastre à la case K − S, modulo 12. Pour mi♭ majeur :

| Formes | ré | do | la | sol | mi |
|------|------|------|------|------|------|
| Case du capodastre | 1 | 3 | 6 | 8 | 11 |

Wikipédia donne deux de ces choix. Dans « Guitar », pour un morceau en si majeur, un guitariste peut « put a capo on the second fret of the instrument, and then play the song as if it were in the key of A Major » (placer un capodastre sur la deuxième case de l'instrument, puis jouer le morceau comme s'il était en la majeur). Dans « Capo (musical device) », deux guitaristes jouent I IV V en mi : « the first guitarist plays E A B7 while the second plays the same progression capoed at the fourth fret using C F G7 chord-shapes » (le premier guitariste joue E A B7, tandis que le second joue la même progression avec un capodastre en quatrième case, en formes C F G7). La seconde guitare fait entendre les mêmes accords dans d'autres voicings.

La tonalité entendue prend le nom qui a le moins d'altérations. Des formes de sol avec un capodastre en case 4 sonnent si majeur, cinq dièses, plutôt que do♭ majeur, sept bémols. Des formes de ré en case 4 sonnent fa♯ majeur ou sol♭ majeur, six altérations dans les deux cas : égalité, et les deux noms sont en usage.

**Le capodastre partiel.** Un capodastre partiel ne couvre que certaines cordes. L'exemple de Wikipédia couvre « the top five strings of a guitar » (les cinq cordes aiguës d'une guitare) et laisse libre le mi grave : « When played at the second fret, this appears to create a drop D tuning (in which the bass E string is detuned to a D) raised one full tone in pitch. » (placé en deuxième case, il semble créer un accordage en drop D, où la corde grave de mi est descendue en ré, monté d'un ton entier.) Énumérée corde 1 d'abord, Δ = (2, 2, 2, 2, 2, 0), c'est-à-dire un capodastre d'un ton, (2, 2, 2, 2, 2, 2), plus le (0, 0, 0, 0, 0, −2) du drop D. Les cordes à vide sonnent mi2 si2 mi3 la3 do♯4 fa♯4 depuis la corde 6 : le drop D, ré2 la2 ré3 sol3 si3 mi4, deux demi-tons plus haut.

### Exercice pratique

Avec un capodastre en case 2, un guitariste joue des formes G – C – D – Em. Quelle tonalité le public entend-il ? Pour un morceau en la♭ majeur, où va le capodastre pour des formes de sol, et pour des formes de mi ?

> *Solution :* La majeur, deux demi-tons au-dessus de sol : les accords sonnent A – D – E – F♯m. Pour la♭ majeur : formes de sol en case 1, puisque 7 + 1 = 8, et formes de mi en case 4, puisque 4 + 4 = 8.

---

## 3. Même forme, autre instrument

Un capodastre change chaque corde de la même quantité, donc une forme garde la qualité de son accord et se déplace d'un seul Tn. Un autre instrument se compare à la guitare de la même façon, corde par corde, par la différence des deux accordages. Le cours music-theory-ga de Learn étudie ces comparaisons dans sa [leçon 8](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L99-L161). L'article « Ukulele » de Wikipédia donne les accordages :
- **Sol grave.** L'accordage linéaire C6, « or "low G" tuning, which has the G in sequence an octave lower: G3–C4–E4–A4, which is equivalent to playing the top four strings (DGBE) of a guitar with a capo on the fifth fret. » (ou accordage en sol grave, où le sol suit l'ordre, une octave plus bas : sol3–do4–mi4–la4, ce qui équivaut à jouer les quatre cordes aiguës, ré sol si mi, d'une guitare avec un capodastre en cinquième case.)
- **Sol aigu.** L'accordage C6 courant, sol4–do4–mi4–la4 : « The G string is tuned an octave higher than might be expected, so this is often called "high G" tuning. This is known as a "reentrant tuning" » (la corde de sol est accordée une octave plus haut qu'on ne s'y attendrait, d'où le nom courant d'accordage en sol aigu. On parle d'accordage rentrant.)
- **Baryton.** « The baritone ukulele usually uses linear G6 tuning: D3–G3–B3–E4, the same as the highest four strings of a standard 6-string guitar. » (le ukulélé baryton utilise en général l'accordage linéaire G6 : ré3–sol3–si3–mi4, le même que les quatre cordes les plus aiguës d'une guitare standard à 6 cordes.)

| Instrument | Cordes 4 à 1 | Moins les cordes 4 à 1 de la guitare | La forme de sol de la guitare sur les cordes 4 à 1, 0003 |
|------|------|------|------|
| Guitare | ré3 sol3 si3 mi4 | 0, 0, 0, 0 | ré3 sol3 si3 sol4 : sol majeur |
| Ukulélé, sol grave | sol3 do4 mi4 la4 | 5, 5, 5, 5 | sol3 do4 mi4 do5 : do majeur, sol à la basse |
| Ukulélé, sol aigu | sol4 do4 mi4 la4 | 17, 5, 5, 5 | sol4 do4 mi4 do5 : do majeur, do à la basse |
| Ukulélé baryton | ré3 sol3 si3 mi4 | 0, 0, 0, 0 | ré3 sol3 si3 sol4 : sol majeur |

- **Le ukulélé en sol grave.** Chaque différence vaut 5, donc le ukulélé est formé des quatre cordes aiguës de la guitare avec un capodastre en case 5. Chaque forme fait entendre T5 de son accord de guitare : la forme de sol de la guitare est l'accord de do du ukulélé, et la forme de ré de la guitare, 0232, est son sol.
- **Le ukulélé en sol aigu.** La différence sur la corde 4 vaut 17, une octave et une quarte. Modulo 12, cela fait toujours 5, donc les classes de hauteurs et les noms d'accords sont ceux du sol grave. La basse, non : le même accord de do a sa quinte à la basse en sol grave et sa fondamentale en sol aigu, un deuxième renversement face à un état fondamental, dans les termes de MUS-014.
- **Le ukulélé baryton.** La différence vaut 0, donc chaque forme garde son nom de guitare.
- **La basse électrique.** L'article « Bass guitar » de Wikipédia dit qu'elle est accordée sur des « pitches one octave lower than the four lowest-pitched strings of a guitar, typically E, A, D, and G » (hauteurs une octave plus bas que les quatre cordes les plus graves d'une guitare, en général mi, la, ré et sol) : mi1 la1 ré2 sol2 contre mi2 la2 ré3 sol3, une différence de −12 sur chaque corde. C'est T0 sur les classes de hauteurs, donc une case sur la corde 4 de la basse donne la note que donne la même case sur la corde 6 de la guitare, une octave plus bas.

**La même forme sur d'autres cordes d'une guitare.** Déplacer une forme vers un autre groupe de cordes ne garde son son que si les cordes gardent leurs intervalles. Comme l'a montré MUS-009, les cordes de la guitare sont à une quarte l'une de l'autre, sauf les cordes 3 et 2, à une tierce majeure. La forme fondamentale-quinte-octave x355xx fait entendre do3 sol3 do4. Un groupe de cordes plus haut, xx355x fait entendre fa3 do4 mi4 : l'octave est devenue une septième majeure, et la forme doit devenir xx356x pour donner fa3 do4 fa4.

### Exercice pratique

La forme 2210, sur les cordes 4 à 1, est le haut de l'accord de la mineur de la guitare. Que fait-elle entendre sur la guitare, sur un ukulélé en sol grave et sur un ukulélé en sol aigu, et quelle note est à la basse ?

> *Solution :* Sur la guitare, mi3 la3 do4 mi4 : la mineur avec mi, sa quinte, à la basse. Sur un ukulélé en sol grave, la3 ré4 fa4 la4 : ré mineur, cinq demi-tons plus haut, avec la, sa quinte, à la basse. Sur un ukulélé en sol aigu, la4 ré4 fa4 la4 : ré mineur avec ré4 comme note la plus grave, sa fondamentale.

---

## 4. Instruments transpositeurs

L'article « Transposing instrument » de Wikipédia : « A transposing instrument is a musical instrument for which music notation is not written at concert pitch (concert pitch is the pitch on a non-transposing instrument such as the piano). » (un instrument transpositeur est un instrument dont la musique n'est pas écrite en son réel, le son réel étant la hauteur d'un instrument non transpositeur comme le piano.) Un instrument est nommé d'après ce que fait entendre son do écrit : « Playing a written C on clarinet or soprano saxophone produces a concert B♭ (i.e. B♭ at concert pitch), so these are referred to as B♭ instruments. » (jouer un do écrit sur une clarinette ou un saxophone soprano produit un si♭ réel, c'est-à-dire un si♭ en son réel ; on les appelle donc instruments en si♭.) L'instrument ne change rien : « The instruments do not transpose the music; rather, their music is written at a transposed pitch. Where chords are indicated for improvisation they are also written in the appropriate transposed form. » (les instruments ne transposent pas la musique ; c'est plutôt leur musique qui est écrite à une hauteur transposée. Quand des accords sont indiqués pour l'improvisation, ils sont aussi écrits sous la forme transposée qui convient.)

| Instrument | Un do écrit sonne | Son réel par rapport à l'écrit | Pour écrire une tonalité réelle, la monter d'une | Mi♭ majeur réel s'écrit en |
|------|------|------|------|------|
| Trompette en si♭, clarinette en si♭ | si♭ | un ton plus bas | seconde majeure (+2 quintes) | fa majeur |
| Saxophone alto en mi♭ | mi♭ | une sixte majeure plus bas | sixte majeure (+3 quintes) | do majeur |
| Cor en fa | fa | une quinte juste plus bas | quinte juste (+1 quinte) | si♭ majeur |
| Guitare, basse électrique | do, une octave plus bas | une octave plus bas | octave | mi♭ majeur |

Les intervalles du son réel sont ceux de Wikipédia. « Trumpet » : « The most common type of trumpet is a transposing instrument in B♭, with pitches sounding a whole step lower than written. » (le type de trompette le plus courant est un instrument transpositeur en si♭, dont les hauteurs sonnent un ton plus bas que l'écrit.) « Alto saxophone » : « The alto saxophone is a transposing instrument, with pitches sounding a major sixth lower than written. » (le saxophone alto est un instrument transpositeur, dont les hauteurs sonnent une sixte majeure plus bas que l'écrit.) « Transposing instrument » donne le cor « sounding a perfect fifth below written pitch in treble clef » (sonnant une quinte juste sous la hauteur écrite en clé de sol) et note que « Double bass, bass guitar, guitar, and contrabassoon sound an octave lower than written. » (la contrebasse, la basse électrique, la guitare et le contrebasson sonnent une octave plus bas que l'écrit.) La guitare est elle-même un instrument transpositeur, à l'octave.

Voici maintenant la seconde moitié de la question. Le morceau sonne en mi♭ majeur : capodastre en case 3, formes de do. Sa grille en son réel se lit E♭ – Cm – A♭ – B♭. Chaque partie monte de l'intervalle de son instrument, et la table des quintes du §1 donne l'armure : mi♭ majeur a trois bémols, donc +2 quintes laissent un bémol, fa majeur.

| Partie | Tonalité écrite | Grille |
|------|------|------|
| Son réel | mi♭ majeur | E♭ – Cm – A♭ – B♭ |
| Trompette en si♭ | fa majeur | F – Dm – B♭ – C |
| Saxophone alto en mi♭ | do majeur | C – Am – F – G |
| Cor en fa | si♭ majeur | B♭ – Gm – E♭ – F |
| Guitare, capodastre en case 3, en formes | do majeur | C – Am – F – G |

Le saxophoniste alto et le guitariste lisent les mêmes noms d'accords. La partie du saxophone est écrite une sixte majeure au-dessus du son, les formes du guitariste une tierce mineure au-dessous, et 9 ≡ −3 modulo 12 : les deux noms tombent sur les mêmes classes de hauteurs, à des octaves différentes.

On peut maintenant distinguer les trois sortes d'identité :

| Relation | Ce qui reste pareil | Ce qui change | Exemple |
|------|------|------|------|
| Transposition Tn | Les intervalles, les qualités d'accords, les degrés de la tonalité | Chaque classe de hauteurs, décalée de n, et les noms de notes | C – Am – F – G et E♭ – Cm – A♭ – B♭ |
| Même forme | Le doigté | Le son, selon la différence des accordages : un Tn seulement quand elle est la même sur chaque corde | La forme de sol : sol sur une guitare, do sur un ukulélé |
| Même note écrite | La notation | Le son, selon la transposition de l'instrument | Un do écrit : si♭ sur une trompette, mi♭ sur un saxophone alto |

### Exercice pratique

Un morceau est en si♭ majeur réel. Dans quelles tonalités le lisent une trompette en si♭, un saxophone alto en mi♭ et un cor en fa ? Que fait entendre un ré écrit sur la trompette ?

> *Solution :* Si♭ majeur a deux bémols. La partie de la trompette se déplace de +2 quintes : do majeur. Celle du saxophone alto se déplace de +3 : un dièse, sol majeur. Celle du cor se déplace de +1 : un bémol, fa majeur. Un ré écrit sonne un ton plus bas sur la trompette : do.

---

## 5. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e610b77`](https://github.com/GuitarAlchemist/ga/tree/e610b7714b9d6a1fe625b17fe6ca004380ca6752). Cette leçon documente ce code et ne le modifie pas. Elle n'a exécuté ni GA ni ses tests. Les fichiers qu'elle cite sont inchangés sur la branche `main` de GA, à `7595983`. Quand un résultat demande un calcul, il vient d'une transcription Python, ligne par ligne, du code nommé : lu, non exécuté.

**Les ensembles de classes de hauteurs se transposent par rotation.** Le `PitchClassSetId` de GA écrit un ensemble comme un nombre de 12 bits, avec le bit p activé pour la classe de hauteurs p, comme dans MUS-020. [`Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L82-L88) réduit n modulo 12 et fait tourner les bits de n places vers le haut, les bits du haut revenant en bas. Do majeur, 145, devient 1160 par T3 : {3, 7, 10}, mi♭ majeur. C'est exactement Tn. [`Rotate`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L90) appelle `Transpose`, avec le commentaire « Rotation of PC set is transposition » (la rotation d'un ensemble de classes de hauteurs est une transposition). Les deux fichiers de test qui appellent `PitchClassSetId.Transpose` s'en servent pour vérifier un autre code : qu'une [forme première ne change](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/GA.Domain.Core.Tests/Theory/Atonal/TranspositionClassTests.cs#L69-L82) sous aucune des 12 transpositions, et, par un [oracle construit dessus](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L16-L30), que les formes premières sont bien calculées. Un deuxième Tn, [`HarmonicTransformationService.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Services/HarmonicTransformationService.fs#L15-L16), ajoute n à chaque classe de hauteurs d'un ensemble, modulo 12. Aucun code hors des tests ne l'appelle, et [son test](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.DSL.Tests/HarmonicTransformationTests.cs#L11-L22) vérifie la valeur : {0, 4, 7} monté de 2 donne {2, 6, 9}.

**Symboles d'accords : la fondamentale bouge, son orthographe et la basse ne suivent pas.** [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L227-L252) analyse un symbole d'accord et ajoute n à la classe de hauteurs de sa fondamentale. Il nomme la nouvelle fondamentale d'après une liste de dièses ou une liste de bémols, choisie par l'ancienne fondamentale : par [`preferFlat`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L29-L37), des bémols pour une fondamentale bémolisée ou pour fa, des dièses sinon, comme l'a trouvé MUS-007. Puis il [remplace la fondamentale et rien d'autre](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L250). Un accord à basse indiquée garde sa [basse](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Types/ChordAst.fs#L29), que le moteur de rendu [réécrit après la barre oblique](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Generators/ChordRenderer.fs#L35-L38) : C/E monté de deux demi-tons devient `D/E`, et non D/F♯, et G/B monté de trois devient `A#/B`, et non B♭/D.

L'outil en ligne de commande de GA transpose une progression avec `ga progression`, qui appelle la closure [accord par accord](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Apps/GaCli/Program.fs#L239-L245). Lu, non exécuté, pour C Am F G :

| `--by` | GA affiche après la flèche | Écrit dans la tonalité |
|------|------|------|
| 1 | C# A#m Gb G# | D♭ B♭m G♭ A♭ |
| 3 | D# Cm Ab A# | E♭ Cm A♭ B♭ |
| 8 | G# Fm Db D# | A♭ Fm D♭ E♭ |
| 10 | A# Gm Eb F | B♭ Gm E♭ F |

Les sept autres décalages, de 1 à 11, donnent une orthographe de leur tonalité. Les classes de hauteurs sont justes à chaque ligne : chaque accord est l'image par Tn de celui dont il vient. Les noms échouent en ré♭, mi♭, la♭ et si♭ majeur, parce que chaque accord prend le côté de son ancienne fondamentale : à `--by 1`, C# et G# côtoient Gb dans une même tonalité.

Le seul test qui transpose un accord par la closure, [`EvalClosure_TransposeWithIntCoercion_Succeeds`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/DslEvalMcpToolsTests.cs#L188-L205), demande C monté de trois demi-tons. Il vérifie qu'un résultat revient, pas ce qu'il vaut ; par transcription, c'est `D#`. Le `TransposeSkill` du chatbot fait appeler [la même closure](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/TransposeSkill.cs#L22) par un modèle de langage.

Le modèle du domaine de GA contient une troisième transposition, [`ChordProgression.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L189-L199). Elle déplace la fondamentale de chaque accord, mais construit le nouvel accord avec [son ancien symbole](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L42), si bien qu'un C Am F G transposé [s'affiche](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L201) toujours `C | Am | F | G`. Rien ne l'appelle, et aucun test ne la couvre.

**Le skill du capodastre : une arithmétique juste, des dièses par défaut, un lecteur étroit.** Le chatbot répond aux questions de capodastre avec [`CapoSkill`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L6-L25) : « Zero LLM calls — pure pitch-class arithmetic. Confidence = 1.0. » (zéro appel à un LLM, de l'arithmétique pure sur les classes de hauteurs ; confiance = 1,0.) Son arithmétique est celle du §2, [son = forme + n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L144) et [forme = son − n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L116), modulo 12. Il [nomme le résultat](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L178-L184) d'après une liste de dièses, « Default: sharps (guitarist convention) » (par défaut : dièses, convention des guitaristes), et ne [prend des bémols](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L186-L191) que si la tonalité ou la forme de la question a un bémol, ou si une question sur une forme contient le mot « flat » (bémol). Son propre résumé promet [« Eb (C + 3st) »](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L13) pour une forme de do avec un capodastre en case 3 ; par transcription, cette question reçoit `D#`.

Le skill lit une question avec [deux expressions régulières](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L52-L64), [celle des formes d'abord](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L88-L106). Par transcription, sur les [dix exemples de requêtes](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L33-L45) du skill lui-même :
- **Sept** reçoivent la réponse du §2.
- **« I play a C shape with capo 3 — what does it sound like »** (je joue une forme de do avec un capodastre en case 3 : qu'est-ce que ça donne ?) reçoit la bonne classe de hauteurs, nommée `D#`.
- **« What's the sounding key if I play in G with capo on 5 »** (quelle est la tonalité entendue si je joue en sol avec un capodastre en case 5 ?) est lue comme un morceau qui sonne en sol. Le skill répond « play a D shape » (jouez une forme de ré) ; la question demande do, sol + 5.
- **« What chord shape for B major with capo 4 »** (quelle forme d'accord pour si majeur avec un capodastre en case 4 ?) ne correspond à aucune des deux expressions, donc le skill la refuse. La réponse est une forme de sol.

La propre question de cette leçon, posée en anglais, « With a capo at the 3rd fret, playing C shapes, what key does the audience hear? », est refusée elle aussi : les deux expressions veulent « capo », puis au plus « on », « at » ou « fret », puis un nombre, comme dans « capo 3 » ou « capo at 3 », et celle des formes veut le mot « shape », pas « shapes ». Les tests du skill, dans [`SkillDeclineTests`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/SkillDeclineTests.cs#L17-L33), vérifient qu'un message sans rapport est refusé et que capo 25 reçoit une erreur plutôt qu'un refus. La transcription s'accorde avec les deux, et aucun test ne vérifie une réponse. Le corpus d'évaluation du chatbot [saute sa seule requête de capodastre](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Apps/GaChatbot.Api.Tests/Corpus/prompts.yaml#L534-L537), « Transpose this progression to capo 3 » (transpose cette progression avec un capodastre en case 3), tant qu'un outil de progression n'existe pas. Le backlog de GA [indique cet outil comme non fait](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/BACKLOG.md#L196).

**Voicings, autres instruments, et ce qui manque.**
- **Documents de voicing.** La fabrique de documents de voicing de GA prend un [argument `capo`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L16). Elle ne s'en sert que dans l'[identifiant](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L29) du document, et aucun appelant n'en passe un.
- **Le catalogue d'instruments.** Il écrit la basse électrique [E1 A1 D2 G2](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L157) et l'accordage en do du ukulélé [G4 C4 E4 A4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1113), tous deux comme au §3. La leçon 8 de Learn a compilé un GA plus ancien, `a826864`, et [a lu ce catalogue](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L186-L225). Elle y a trouvé la ligne du ukulélé précédée d'un `C6` égaré, qui a disparu à `e610b77`. Elle a aussi trouvé deux lignes de ukulélé baryton, qui sont inchangées : [D4 G3 B4 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1120) et [D4 G3 B3 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1434), là où le §3 a ré3 sol3 si3 mi4. Les deux ont les classes de hauteurs de la guitare, donc un code qui compare des classes de hauteurs ne peut pas voir la différence.
- **Instruments transpositeurs.** Ils sont absents. À `e610b77`, rien dans le dépôt de GA ne dit « transposing instrument » ni « written pitch », et « concert pitch » n'apparaît qu'une fois, dans la [tessiture d'un accordage de guitare à 8 cordes](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/SpecializedTunings.yaml#L243). Dans les fichiers C#, F#, TypeScript, JavaScript, Python et YAML de GA, les mots « saxophone » et « clarinet » n'apparaissent qu'une fois, dans une ligne qui range un instrument dont le nom les contient, ou contient « flute », dans la [famille « Wind »](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/GA.Data.MongoDB/Services/InstrumentService.cs#L120). Le §4 est enseigné comme théorie.

Corriger tout cela revient aux responsables de GA ; cette leçon se contente de le décrire.

### Exercice pratique

Par transcription, que répond `CapoSkill` à « I play an F shape with capo 1, what does it sound like » (forme de fa, capodastre en case 1) et à « I play a D shape with capo 1, what does it sound like » (forme de ré, capodastre en case 1) ? Les noms sont-ils justes ?

> *Solution :* « F# » et « D# ». Le premier convient : fa♯ majeur et sol♭ majeur ont tous deux six altérations. Le second, non : la tonalité est mi♭ majeur, trois bémols, alors que ré♯ majeur demanderait neuf dièses. Aucune des deux questions ne contient de bémol, donc le skill utilise sa liste de dièses les deux fois.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA. L'épinglage de GA dans le laboratoire passerait d'abord à `e610b77`. Rien dans cette section n'est une mesure :
- les prédictions viennent du §5 et sont écrites avant toute exécution ;
- elles viennent d'une transcription Python, ligne par ligne, de `PitchClassSetId.Transpose`, de `domain.transposeChord` avec l'analyseur et le moteur de rendu d'accords, et de `CapoSkill` ;
- une version ultérieure de cette leçon rapportera les résultats.

Chaque étape appelle le code de GA dans le processus même du laboratoire, jamais un serveur MCP en cours d'exécution ni un modèle de langage.

1. **Chaque ensemble, chaque n.** Pour chaque `PitchClassSetId` de 0 à 4095 et chaque n de 0 à 11, comparer `Transpose(n)` avec l'ensemble des classes de hauteurs p + n modulo 12, et vérifier que `Transpose(12 − n)` ramène l'ensemble. Prédiction : les 49 152 paires passent les deux vérifications ; 145 donne 1160 pour n = 3.
2. **Une progression, chaque n.** Par le registre de closures de GA, invoquer `domain.transposeChord` sur C, Am, F et G pour chaque n de 1 à 11, et sur C/E avec n = 2 et G/B avec n = 3. Analyser chaque accord transposé de la progression avec `Chord.FromSymbol` et comparer ses classes de hauteurs avec celles de l'original décalées de n. Prédiction : les noms du tableau du §5, avec ré♭, mi♭, la♭ et si♭ majeur mal orthographiés et les sept autres décalages justes ; chaque ensemble de classes de hauteurs une image par Tn ; `D/E` et `A#/B`.
3. **Le skill du capodastre.** Appeler `CapoSkill.ExecuteAsync` sur ses dix exemples de requêtes et sur la question de cette leçon, et relever `Declined` et la première ligne de `Result`. Prédiction : comme au §5. Sept réponses s'accordent avec le §2, la forme de do avec un capodastre en case 3 sonne `D#`, « play in G with capo on 5 » reçoit une forme de ré, et la requête sur si majeur et la question de cette leçon sont refusées.

### Exercice pratique

L'étape 2 prédit `Ab` pour F monté de trois demi-tons et `D#` pour C. Pourquoi F reçoit-il un bémol et C un dièse, et que devraient être les deux ?

> *Solution :* `preferFlat` donne la liste de bémols à une fondamentale bémolisée et à fa, la seule fondamentale naturelle dont la tonalité majeure a un bémol, si♭ ; C reçoit la liste de dièses. Les deux accords arrivent en mi♭ majeur, où ils devraient être A♭ et E♭ : c'est la nouvelle tonalité qui devrait choisir le côté, pas l'ancienne fondamentale.

---

## 7. Pièges courants

- **Écrire une transposition d'après ses seuls demi-tons.** Trois demi-tons au-dessus de do, dans un changement de tonalité, c'est mi♭, une tierce mineure, pas ré♯.
- **Prendre un décalage diatonique pour une transposition.** Do mi sol monté de deux degrés de do majeur donne mi sol si, une triade mineure : pas un Tn.
- **Nommer un accord sans dire quel nom.** Avec un capodastre en case 2, un « ré » peut être la forme ou le son : dites « forme de ré » ou « sonne mi ».
- **Déplacer les notes frettées avec le capodastre.** Le capodastre n'élève que les cordes à vide ; la case 7 de la corde 6 est si2 avec ou sans capodastre sur une case inférieure.
- **S'attendre à ce qu'une forme garde son accord sur chaque instrument.** Sur un ukulélé en sol grave, elle sonne une quarte plus haut ; sur une même guitare, une forme qui passe d'un côté à l'autre des cordes 3 et 2 change.
- **Lire la partie d'un instrument transpositeur en son réel.** Un do écrit sur une trompette en si♭ sonne si♭.
- **Se fier aux noms de GA pour un accord transposé.** `domain.transposeChord` nomme la nouvelle fondamentale avec des dièses sauf si l'ancienne est bémolisée ou est fa, et `CapoSkill` sauf si la tonalité ou la forme demandée a un bémol ; `domain.transposeChord` laisse aussi la basse d'un accord à basse indiquée où elle était.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Transposition, Tn** | Ajouter n demi-tons à chaque hauteur, ou n modulo 12 à chaque classe de hauteurs |
| **Transposition chromatique et diatonique** | Un décalage d'un nombre fixe de demi-tons, ou d'un nombre fixe de degrés d'une gamme |
| **Capodastre** | Une pince posée en travers des cordes à une case, un nouveau sillet : chaque corde à vide monte du même nombre de demi-tons |
| **Forme d'accord** | Un accord nommé d'après son doigté par rapport au capodastre, et non d'après ce qu'il fait entendre |
| **Son réel** | La hauteur qui sonne, qu'un instrument non transpositeur comme le piano écrit telle quelle |
| **Instrument transpositeur** | Un instrument dont la partie est écrite à une autre hauteur que celle qui sonne : la trompette en si♭, le saxophone alto en mi♭, le cor en fa, et la guitare et la basse électrique à l'octave |
| **Accordage rentrant** | Un accordage dont les cordes ne sont pas dans l'ordre des hauteurs, comme le sol aigu du ukulélé |

---

## Auto-évaluation

**1. Un guitariste joue des formes G – Em – C – D avec un capodastre en case 3. Qu'entend le public, et dans quelle tonalité ?**
> B♭ – Gm – E♭ – F, en si♭ majeur. Chaque accord monte d'une tierce mineure, et si♭ majeur a deux bémols là où la♯ majeur demanderait dix dièses.

**2. Un morceau sonne en la majeur. Donnez deux positions de capodastre avec des formes ouvertes.**
> Formes de sol en case 2, puisque 7 + 2 = 9, ou formes de mi en case 5, puisque 4 + 5 = 9. Des formes de ré en case 7 et de do en case 9 conviennent aussi.

**3. Le morceau de la question 2 a une trompette en si♭ et un saxophone alto en mi♭. Dans quelles tonalités lisent-ils ?**
> La majeur a trois dièses. La partie de la trompette se déplace de +2 quintes, vers cinq dièses : si majeur. Celle du saxophone alto se déplace de +3, vers six dièses : fa♯ majeur.

**4. Par transcription, que renvoie `domain.transposeChord` de GA pour C/E monté de deux demi-tons, et que devrait-il renvoyer ?**
> `D/E` : seule la fondamentale bouge. Il devrait renvoyer D/F♯.

**5. Pourquoi une forme de guitare sonne-t-elle une quarte plus haut sur un ukulélé en sol grave, et pareil sur un ukulélé baryton ?**
> Les cordes du ukulélé en sol grave, sol3 do4 mi4 la4, sont les quatre cordes aiguës de la guitare, ré3 sol3 si3 mi4, montées de cinq demi-tons chacune : la même différence sur chaque corde, comme un capodastre en case 5. Les cordes du baryton sont exactement ces quatre cordes, une différence de 0.

**Critères de réussite :** Transposer une hauteur, un accord, une progression ou une tonalité, et écrire le résultat dans sa tonalité. Passer du capodastre et des formes à la tonalité entendue, et inversement. Dire ce que devient une forme sur un autre instrument ou sur un autre groupe de cordes. Écrire la tonalité d'une partie en si♭, en mi♭ ou en fa pour une tonalité réelle. Dire où les réponses de GA sur la transposition et le capodastre sont justes, et où leurs noms ou leur lecture d'une question échouent.

---

## Bases de recherche

- Wikipédia, « Transposition (music) » : la définition, Tn sur les classes de hauteurs, la transposition des hauteurs et des classes de hauteurs, et la transposition chromatique face à la diatonique.
- Wikipédia, « Capo (musical device) » : le nouveau sillet, le même effet que réaccorder chaque corde, le nom de la forme face au nom entendu, l'exemple E A B7 et C F G7, et le capodastre partiel.
- Wikipédia, « Guitar » : le capodastre en deuxième case pour si majeur avec des formes de la.
- Wikipédia, « Ukulele » : les accordages C6 en sol aigu et en sol grave, le sol grave comme les quatre cordes aiguës d'une guitare avec un capodastre en cinquième case, et le ré3–sol3–si3–mi4 du baryton.
- Wikipédia, « Bass guitar » : accordée une octave sous les quatre cordes les plus graves de la guitare.
- Wikipédia, « Transposing instrument » : la définition, les instruments en si♭, les symboles d'accords transposés, le cor en fa, et la guitare et la basse électrique à l'octave.
- Wikipédia, « Trumpet » et « Alto saxophone » : un ton et une sixte majeure sous l'écrit.
- Code source de GA au commit `e610b7714b9d6a1fe625b17fe6ca004380ca6752` : chaque fait de code du §5 renvoie à sa ligne.
- Learn, leçon 8 de music-theory-ga au commit `a0c78d95a4719fdc0df85052fe171c78cf204e2b` : les comparaisons du ukulélé et de la basse, et sa lecture du catalogue de GA à `a826864`.
- Cité par le plan de cursus de Streeling et non consulté pour cette version : Adler, *The Study of Orchestration* (4e éd.), le chapitre sur les instruments transpositeurs.
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure qui lui soit propre.
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue.
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
