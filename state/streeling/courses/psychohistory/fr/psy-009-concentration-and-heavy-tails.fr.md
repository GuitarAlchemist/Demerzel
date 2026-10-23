---
module_id: psy-009-concentration-and-heavy-tails
department: psychohistory
course: "Concentration : quand quatre jours réunissent la moitié des événements"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-009
version: "0.1.0"
---

# Concentration : quand quatre jours réunissent la moitié des événements

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous classerez les jours d'un journal d'événements, vous mesurerez l'inégalité avec laquelle ils se partagent les événements (parts des k jours les plus chargés, courbe de Lorenz, coefficient de Gini), vous comparerez une moyenne à une médiane, et vous confronterez un plan de capacité dimensionné sur la moyenne à un plan dimensionné sur un quantile. **Question de projet :** quelle part de l'activité des déclencheurs se concentre sur les quelques jours les plus chargés, et quel effet cela a-t-il sur un plan de capacité fondé sur la moyenne ?

[PSY-002](psy-002-governance-phase-transitions.fr.md) voit dans un doublement du taux de signaux, un nombre divisé par une fenêtre de temps, le signe d'une transition à venir. Un taux est une moyenne, et ce module mesure quelle part d'une moyenne quelques jours peuvent porter. [PSY-008](psy-008-bursts-are-not-rates.fr.md) confronte les mêmes comptages quotidiens à une référence de Poisson ; [PSY-007](psy-007-power-law-or-not.fr.md) et [PSY-022](psy-022-competing-explanations.fr.md) ajustent des lois de probabilité.

## 1. Classer les jours et cumuler à partir du plus chargé

**Observé.** Jusqu'à son retrait le 2026-07-18, un [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) écrivait un *fichier déclencheur* par événement du dépôt. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) en contient 594, de trois types : des push, des tickets (*issues*) ouverts et des discussions créées. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/extract.py) fige le dossier dans [`observed-input.json`](../../../fixtures/psychohistory/psy-009/observed-input.json). Le jour d'un événement est la date UTC de son horodatage. Le journal s'étend du 2026-03-20 au 2026-07-16 : **119** jours civils, dont **100** avec au moins un événement et **19** sans aucun.

**Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/analyze.py) dans [`results.json`](../../../fixtures/psychohistory/psy-009/results.json), pourcentages arrondis à deux décimales. Triez les jours du plus chargé au plus calme et cumulez à partir du premier : la *part des k premiers* (*top-k share*) est la fraction de l'ensemble des événements qui tombe sur les k jours les plus chargés.

Les quatre jours les plus chargés réunissent 286 des 594 événements, soit 48,15 % : presque la moitié, mais pas la moitié qu'annonce le titre de ce module ; il faut un cinquième jour pour dépasser la moitié. Ces quatre jours forment deux paires de jours voisins, les 21 et 22 mars (169 événements) et les 27 et 28 juin (117), séparées de 97 jours (du 22 mars au 27 juin), chacune à l'intérieur de l'un des deux *épisodes* de PSY-008 (des jours de rafale séparés d'au plus 7 jours). La part dépend de l'heure à laquelle commence un jour : sur les 24 décalages horaires de UTC−11 à UTC+12, elle se situe entre 48,15 % (UTC, la plus basse) et 55,05 %, et atteint ou dépasse la moitié pour 15 d'entre eux.

### Exercice pratique 1

Les dix jours les plus chargés comptent 109, 72, 60, 45, 26, 24, 20, 20, 20 et 19 événements, sur 594. Calculez la part du jour le plus chargé, celle des quatre plus chargés et celle des dix plus chargés, ainsi que le nombre de jours nécessaires pour dépasser la moitié.

> **Réponse :** `109 / 594 = 18.35%`. `109 + 72 + 60 + 45 = 286` et `286 / 594 = 48.15%`. Les dix totalisent 415 : `415 / 594 = 69.87%`. La moitié de 594 est 297 ; quatre jours donnent 286 et cinq donnent `286 + 26 = 312` : il faut donc cinq jours (52,53 %).

## 2. La courbe de Lorenz et le coefficient de Gini

La *courbe de Lorenz* montre tous les k à la fois : triez les jours du plus calme au plus chargé et portez la part cumulée des événements en fonction de la part cumulée des jours. Des jours tous égaux donneraient la diagonale. **Calculé :** la moitié la plus calme des jours (60 sur 119) réunit 41 événements, soit 6,90 % ; les 90 % les plus calmes (108 jours) en réunissent 27,10 %.

Le *coefficient de Gini* G résume la courbe en un seul nombre : deux fois l'aire comprise entre la diagonale et la courbe. Avec les n comptages quotidiens triés par ordre croissant et T leur total :

```text
G = somme sur i de (2i - n - 1) * x_i / (n * T)       x_1 <= x_2 <= ... <= x_n
tous les jours égaux    -> G = 0
un jour les réunit tous -> G = (n - 1) / n            118/119 = 0.9916 pour ce journal
```

Le jeu d'essai vérifie ces deux limites. **Calculé :** G = 0,7789 sur les 119 jours civils et 0,7369 sur les seuls 100 jours actifs : ce ne sont pas les jours vides qui le rendent élevé.

Zéro n'est pas le bon étalon pour ce chiffre : le hasard suffit à rendre les jours inégaux. **Synthétique.** [`scenarios.json`](../../../fixtures/psychohistory/psy-009/scenarios.json) définit 2 000 journaux témoins de 594 événements, chaque événement étant placé sur l'un des 119 jours, tiré uniformément au hasard.

| Mesure | Journal observé | 2 000 journaux synthétiques : médiane (du minimum au maximum) |
|---|---|---|
| Événements des quatre jours les plus chargés | 286 | 41 (34 à 52) |
| Jours nécessaires pour dépasser la moitié | 5 | 40 (36 à 44) |
| Coefficient de Gini | 0,7789 | 0,2468 (0,1958 à 0,2995) |

Aucun journal synthétique n'atteint la valeur observée, sur aucune ligne : un placement au hasard donne un coefficient de Gini proche de 0,25, non de 0.

### Exercice pratique 2

Un journal de cinq jours a pour comptages quotidiens 0, 1, 1, 2, 6. Calculez son coefficient de Gini, puis recalculez-le sur ses quatre seuls jours actifs.

> **Réponse :** n = 5 et T = 10 ; les poids `2i − n − 1` valent −4, −2, 0, 2, 4, la somme vaut `0 − 2 + 0 + 4 + 24 = 26`, et `G = 26 / 50 = 0.52`. Sur 1, 1, 2, 6, les poids valent −3, −1, 1, 3 : `−3 − 1 + 2 + 18 = 16` et `G = 16 / 40 = 0.40`. Retirer un jour vide abaisse G alors qu'aucun événement n'a bougé : précisez quels jours ont été comptés.

### Exercice pratique 3

Deux journaux imaginaires comptent chacun 594 événements sur 119 jours. Dans le journal A, les quatre jours les plus chargés réunissent 42 événements et G = 0,25 ; dans le journal B, 89 événements et G = 0,45. Situez chacun par rapport aux journaux synthétiques et par rapport au journal observé.

> **Réponse :** A se situe dans la plage des journaux synthétiques sur les deux mesures (34 à 52 événements ; 0,1958 à 0,2995) : il est compatible avec un placement au hasard. B se situe au-dessus de tous les journaux synthétiques sur les deux mesures, mais loin en dessous du journal observé : `89 / 286 = 31.12%` des événements de ses quatre jours les plus chargés, et 0,45 contre 0,7789. La plage provient d'un lot fini, non d'une borne.

## 3. Moyenne, médiane et une moyenne qui ne se stabilise pas

**Calculé.** La moyenne est de `594 / 119 = 4.99` événements par jour civil. La médiane, valeur centrale des comptages triés (la moyenne des deux valeurs centrales quand leur nombre est pair), vaut 1 : 63 jours comptent exactement un événement, et 100 des 119 jours sont égaux ou inférieurs à la moyenne, qui ne décrit donc pas un jour ordinaire.

Dans un journal concentré, quelques jours portent la moyenne, et elle bouge avec eux. Sans le jour le plus chargé, elle tombe de 4,99 à 4,11 (−17,66 %) ; sans les quatre plus chargés, à 2,68 (−46,34 %). La médiane reste à 1. Dans les journaux synthétiques, le même retrait déplace la moyenne de 2,21 % au plus.

La même instabilité apparaît dans le temps : lue fin mars (12 jours), fin avril, fin mai et fin juin, puis le dernier jour, la moyenne cumulée valait successivement 17,67 ; 5,88 ; 3,97 ; 5,14 et 4,99, et la médiane 4,5, puis 1 les quatre fois suivantes.

De façon informelle, des comptages sont dits *à queue lourde* quand des valeurs très supérieures à la valeur habituelle sont assez fréquentes pour porter une grande part du total ; une moyenne d'échantillon dépend alors du fait que l'échantillon en contienne une ou non. Cette description convient à ces comptages. La définition formelle porte sur la lenteur avec laquelle la queue décroît, et 119 jours ne permettent pas de la tester : deux épisodes peuvent produire de tels chiffres sans aucune queue lourde.

### Exercice pratique 4

Recalculez la moyenne sans le jour le plus chargé, puis sans les quatre plus chargés. Quel nombre donneriez-vous pour « un jour ordinaire », et à quoi la moyenne sert-elle encore ?

> **Réponse :** `(594 − 109) / 118 = 485 / 118 = 4.11` et `(594 − 286) / 115 = 308 / 115 = 2.68`. Pour un jour ordinaire, donnez la médiane, 1 ; elle ne bouge dans aucun des deux cas. La moyenne reste le bon nombre pour les totaux : `4.99 × 119` redonne les 594 événements, aux arrondis près.

## 4. Dimensionner un plan sur la moyenne, puis sur un quantile

**Observé.** Les déclencheurs étaient écrits pour un pilote autonome dont le [fichier de compétence](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md) indique qu'il « ran 3 manual cycles in March 2026 and was never scheduled » (il a effectué trois cycles manuels en mars et n'a jamais été planifié). Le même fichier fixe deux limites : au plus 50 déclencheurs dans la file d'attente, et l'abandon des déclencheurs de plus de 72 heures. Les déclencheurs archivés n'ont jamais été consommés : rien de ce qui suit n'est donc une mesure.

**Synthétique.** Supposons un consommateur qui traite au plus c événements par jour, les plus anciens d'abord ; les autres attendent, et la capacité inutilisée est perdue. Un événement est *en retard* s'il n'est pas traité dans les 3 jours qui suivent son jour d'arrivée (la limite de 72 heures, à la résolution d'un jour). Le p-ième *centile* est la valeur située au rang `ceil(p × n / 100)` des comptages triés (rang le plus proche, la règle des quantiles de PSY-008).

| Plan | c par jour | Événements en retard | Attente la plus longue |
|---|---|---|---|
| Moyenne, arrondie à l'entier supérieur | 5 | 489 | 33 jours |
| 90e centile | 8 | 393 | 20 jours |
| 95e centile | 24 | 49 | 6 jours |
| Plus petit c suffisant | 34 | 0 | 3 jours |
| 99e centile | 72 | 0 | 1 jour |

Le plan fondé sur la moyenne offre `5 × 119 = 595` créneaux pour 594 événements et semble suffisant. Il en traite 440 et en laisse 154 en attente à la fin, parce que la capacité restée inutilisée pendant les semaines calmes ne peut pas être reportée sur une semaine chargée ; son arriéré culmine à 205 événements, plus de quatre fois la limite de 50 que la conception fixe à la file d'attente.

Une partie de cet échec tient à un plan sans marge, non à la concentration : dans 1 919 des 2 000 journaux synthétiques, une capacité de 5 laisse aussi des événements en retard (81 dans le journal médian). Mais dans ces journaux, la plus petite capacité suffisante est de 5 à 7 par jour, et le 95e centile (8 à 11) ne laisse jamais d'événement en retard. La concentration change le prix du remède : 34 par jour, 6,81 fois la moyenne.

Chaque plan du tableau est dimensionné a posteriori, sur les 119 jours mêmes auxquels on l'applique, et un centile élevé ne se stabilise pas mieux que la moyenne : lu fin mai, le 95e centile valait 8, non 24, et une capacité de 8 à partir du 1er juin laisse 199 événements en retard sur les 46 jours restants. Tant que moins de 100 jours ont été lus, le 99e centile est le jour le plus chargé observé jusque-là.

### Exercice pratique 5

Votre critère est celui de la conception : aucun événement en retard. Quel plan fondé sur un centile, dans le tableau, le satisfait ? Calculez la capacité qu'offre le plus petit plan suffisant sur l'ensemble du journal, et la part qui en est utilisée.

> **Réponse :** A posteriori, seul le 99e centile ; le 95e laisse 49 événements en retard et une attente maximale de 6 jours. La plus petite capacité suffisante est de 34 par jour : `34 × 119 = 4,046` créneaux, dont `594 / 4,046 = 14.68%` sont utilisés et `100 − 14.68 = 85.32%` restent inutilisés. Décidez selon la tolérance et le coût de la capacité inutilisée, non selon la moyenne. La règle est supposée et les capacités sont fixées après coup : on décrit un profil d'arrivées, non un consommateur, et ce n'est pas une recette pour les 119 prochains jours.

**L'objection la plus forte à la lecture que fait cette leçon** est qu'un fichier déclencheur n'est pas une unité de travail. Le même fichier de compétence fusionne les déclencheurs qui partagent le type, le dépôt et la référence Git, et les 594 partagent un même dépôt et une même référence : un pilote qui se réveillerait une fois par jour (une cadence supposée) aurait reçu 132 déclencheurs fusionnés, au plus 3 par jour, avec un coefficient de Gini de 0,3287. Selon cette lecture, la concentration décrit la fréquence à laquelle le producteur s'est activé, non la quantité de travail arrivée. En second lieu, la part des quatre premiers jours repose sur deux épisodes : **cet échantillon ne permet pas de distinguer un processus qui produit un épisode à quelques mois d'intervalle de deux incidents sans lien entre eux.** Un relevé du travail effectué pour chaque déclencheur trancherait le premier point ; un flux d'événements plus long, le second.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les 594 fichiers déclencheurs, le workflow et le fichier de compétence dont les liens figurent plus haut. `extract.py` refuse de s'exécuter si le dossier ou un fichier de conception diffère de sa version épinglée.

**Jeu d'essai.** Le [README](../../../fixtures/psychohistory/psy-009/README.md) donne les commandes, les cas calculés à la main, les 41 autocontrôles et les témoins négatifs.

**Lu hors du jeu d'essai.** `git log --diff-filter=D`, au commit épinglé, liste 12 fichiers déclencheurs supprimés sans avoir été archivés : sept datés du 2026-03-20, dont cinq retirés de `processing/` par le commit du [cycle 002 du pilote](https://github.com/GuitarAlchemist/Demerzel/commit/2b752a763e490aa090cf32ee992cb923a6d1bc24), et cinq datés du 2026-06-30, supprimés par le commit [`a2c1ef0`](https://github.com/GuitarAlchemist/Demerzel/commit/a2c1ef01d2470ca737b89e005eddc8aa78fa7583). L'un des douze est un déclencheur `self_initiated`, non un événement du dépôt. Aucun ne tombe sur l'un des quatre jours les plus chargés, qui, avec les douze comptés, réuniraient `286 / (594 + 12) = 47.19%`.

**Références de méthode.** Lorenz, M. O. (1905), « Methods of Measuring the Concentration of Wealth », *Publications of the American Statistical Association* 9(70), 209–219, doi:10.2307/2276207. Ceriani, L., et Verme, P. (2012), « The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini », *The Journal of Economic Inequality* 10(3), 421–443, doi:10.1007/s10888-011-9188-x. Hyndman, R. J., et Fan, Y. (1996), « Sample Quantiles in Statistical Packages », *The American Statistician* 50(4), 361–365.

**Non fait.** Aucune loi de probabilité n'a été ajustée et aucune loi de queue n'a été testée. La règle de capacité est supposée et n'utilise que les comptages d'arrivées : ni temps de traitement, ni priorité, ni dédoublonnage. Les plans sont dimensionnés a posteriori : quatre lectures antérieures ne testent pas une règle de dimensionnement. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Appliquer les mêmes mesures à un flux d'événements du projet qui continue de croître, comme les commits par jour. Si son coefficient de Gini est proche de celui d'un placement au hasard pour son propre total et son propre nombre de jours, la concentration trouvée ici appartient au producteur retiré, non au projet.
