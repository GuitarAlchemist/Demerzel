---
module_id: psy-009-concentration-and-heavy-tails
department: psychohistory
course: "Concentration : quand quatre journées portent la moitié des événements"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-009
version: "0.1.0"
---

# Concentration : quand quatre journées portent la moitié des événements

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous classerez les journées d'un journal d'événements, vous mesurerez l'inégalité avec laquelle elles se partagent les événements (parts des k premières, courbe de Lorenz, coefficient de Gini), vous comparerez une moyenne à une médiane, et vous éprouverez un plan de capacité dimensionné sur la moyenne face à un plan dimensionné sur un quantile. **Question de projet :** quelle part de l'activité de déclenchement se tient dans les quelques journées les plus chargées, et qu'est-ce que cela fait à un plan de capacité fondé sur une moyenne ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit un doublement du taux de signaux, un effectif divisé par une fenêtre de temps, comme le signe d'une transition prochaine. Un taux est une moyenne, et ce module mesure quelle part d'une moyenne quelques journées peuvent porter. [PSY-008](psy-008-bursts-are-not-rates.fr.md) confronte les mêmes effectifs journaliers à une référence poissonnienne ; [PSY-007](psy-007-power-law-or-not.fr.md) et PSY-022 ajustent des distributions.

## 1. Classer les journées et sommer depuis le haut

**Observé.** Jusqu'à son retrait le 2026-07-18, un [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) écrivait un *fichier de déclenchement* par événement du dépôt. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) en contient 594, de trois types : poussées, tickets ouverts et discussions créées. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/extract.py) fige le dossier dans [`observed-input.json`](../../../fixtures/psychohistory/psy-009/observed-input.json). Le jour d'un événement est la date UTC de son horodatage. Le journal court du 2026-03-20 au 2026-07-16 : **119** jours calendaires, **100** avec au moins un événement et **19** sans aucun.

**Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/analyze.py) dans [`results.json`](../../../fixtures/psychohistory/psy-009/results.json), pourcentages arrondis à deux décimales. Classons les journées de la plus chargée à la plus calme et sommons depuis le haut : une *part des k premières* est la fraction de tous les événements qui tombe sur les k journées les plus chargées.

Les quatre journées les plus chargées portent 286 des 594 événements, soit 48,15 % : presque la moitié, non la moitié du titre de ce module ; il faut une cinquième journée pour dépasser la moitié. Ces quatre journées forment deux paires de voisines, les 21 et 22 mars (169 événements) et les 27 et 28 juin (117), à 97 jours de distance (du 22 mars au 27 juin), chacune à l'intérieur de l'un des deux *épisodes* de PSY-008 (des jours de salve séparés d'au plus 7 jours). La part dépend de l'heure à laquelle une journée commence : sur les 24 fuseaux de UTC−11 à UTC+12, elle se situe entre 48,15 % (UTC, la plus basse) et 55,05 %, et atteint ou dépasse la moitié sur 15 d'entre eux.

### Exercice pratique 1

Les dix journées les plus chargées portent 109, 72, 60, 45, 26, 24, 20, 20, 20 et 19 événements, sur 594. Calculez la part de la journée la plus chargée, celle des quatre premières et celle des dix premières, ainsi que le nombre de journées nécessaires pour dépasser la moitié.

> **Réponse :** `109 / 594 = 18.35%`. `109 + 72 + 60 + 45 = 286` et `286 / 594 = 48.15%`. Les dix somment à 415 : `415 / 594 = 69.87%`. La moitié de 594 est 297 ; quatre journées donnent 286 et cinq donnent `286 + 26 = 312`, d'où cinq journées (52,53 %).

## 2. La courbe de Lorenz et le coefficient de Gini

La *courbe de Lorenz* montre tous les k à la fois : on classe les journées de la plus calme à la plus chargée et l'on porte la part cumulée des journées contre la part cumulée des événements. Des journées égales donneraient la diagonale. **Calculé :** la moitié la plus calme des journées (60 sur 119) porte 41 événements, soit 6,90 % ; les 90 % les plus calmes (108 journées) en portent 27,10 %.

Le *coefficient de Gini* G condense la courbe en un seul nombre, le double de l'aire entre la diagonale et la courbe. Avec les n effectifs journaliers classés par ordre croissant et T leur total :

```text
G = somme sur i de (2i - n - 1) * x_i / (n * T)       x_1 <= x_2 <= ... <= x_n
toutes les journées égales       -> G = 0
une journée les porte toutes     -> G = (n - 1) / n   118/119 = 0.9916 pour ce journal
```

Le jeu d'essai vérifie les deux limites. **Calculé :** G = 0,7789 sur les 119 jours calendaires et 0,7369 sur les 100 jours actifs seuls : ce ne sont pas les jours vides qui le rendent élevé.

Zéro est le mauvais étalon pour ce chiffre : le hasard seul rend les journées inégales. **Synthétique.** [`scenarios.json`](../../../fixtures/psychohistory/psy-009/scenarios.json) définit 2 000 journaux de contrôle de 594 événements, chaque événement placé sur l'une des 119 journées tirée uniformément au hasard.

| Mesure | Journal observé | 2 000 journaux synthétiques : médiane (du plus bas au plus haut) |
|---|---|---|
| Événements des quatre journées les plus chargées | 286 | 41 (34 à 52) |
| Journées nécessaires pour dépasser la moitié | 5 | 40 (36 à 44) |
| Coefficient de Gini | 0,7789 | 0,2468 (0,1958 à 0,2995) |

Aucun journal synthétique n'atteint la valeur observée sur aucune ligne : un placement au hasard donne un coefficient de Gini voisin de 0,25, non de 0.

### Exercice pratique 2

Un journal de cinq journées a pour effectifs journaliers 0, 1, 1, 2, 6. Calculez son coefficient de Gini, puis de nouveau sur ses quatre journées actives seules.

> **Réponse :** n = 5 et T = 10 ; les poids `2i − n − 1` valent −4, −2, 0, 2, 4, la somme vaut `0 − 2 + 0 + 4 + 24 = 26`, et `G = 26 / 50 = 0.52`. Sur 1, 1, 2, 6 les poids valent −3, −1, 1, 3 : `−3 − 1 + 2 + 18 = 16` et `G = 16 / 40 = 0.40`. Retirer une journée vide abaisse G alors qu'aucun événement n'a bougé : dites quelles journées ont été comptées.

### Exercice pratique 3

Deux journaux imaginaires portent chacun 594 événements sur 119 journées. Dans le journal A, les quatre journées les plus chargées portent 42 événements et G = 0,25 ; dans le journal B, 89 événements et G = 0,45. Classez chacun face aux journaux synthétiques et face au journal observé.

> **Réponse :** A se situe dans l'étendue synthétique sur les deux mesures (34 à 52 événements ; 0,1958 à 0,2995) : il est compatible avec un placement au hasard. B se situe au-dessus de tous les journaux synthétiques sur les deux, et pourtant très loin en dessous du journal observé : `89 / 286 = 31.12%` de ses événements de tête, et 0,45 contre 0,7789. L'étendue vient d'un lot fini, non d'une borne.

## 3. Moyenne, médiane, et une moyenne qui ne se stabilise pas

**Calculé.** La moyenne vaut `594 / 119 = 4.99` événements par jour calendaire. La médiane, la valeur centrale des effectifs classés (la moyenne des deux valeurs centrales quand leur nombre est pair), vaut 1 : 63 journées portent exactement un événement, et 100 des 119 journées sont à la moyenne ou en dessous, ce qui ne décrit pas une journée ordinaire.

Dans un journal concentré, quelques journées portent la moyenne, et celle-ci se déplace avec elles. Sans la journée la plus chargée, elle tombe de 4,99 à 4,11 (−17,66 %) ; sans les quatre plus chargées, à 2,68 (−46,34 %). La médiane reste à 1. Dans les journaux synthétiques, le même retrait déplace la moyenne de 2,21 % au plus.

La même instabilité apparaît dans le temps : lue à la fin mars (12 journées), avril, mai et juin, puis au dernier jour, la moyenne cumulée valait 17,67, 5,88, 3,97, 5,14 et 4,99 ; la médiane valait 4,5, puis 1 quatre fois.

De façon informelle, des effectifs sont *à queue lourde* lorsque des valeurs très au-dessus de l'ordinaire sont assez fréquentes pour porter une large part du total ; une moyenne d'échantillon dépend alors du fait que l'échantillon en ait attrapé une. Cette description convient à ces effectifs. La définition formelle porte sur la lenteur de décroissance de la queue, et 119 journées ne permettent pas de la tester : deux épisodes peuvent produire de tels chiffres sans aucune queue lourde.

### Exercice pratique 4

Recalculez la moyenne sans la journée la plus chargée, puis sans les quatre plus chargées. Quel nombre rapporteriez-vous pour « une journée ordinaire », et à quoi la moyenne sert-elle encore ?

> **Réponse :** `(594 − 109) / 118 = 485 / 118 = 4.11` et `(594 − 286) / 115 = 308 / 115 = 2.68`. Rapportez la médiane, 1, pour une journée ordinaire ; elle ne bouge dans aucun des deux cas. La moyenne reste le bon nombre pour des totaux : `4.99 × 119` redonne les 594 événements, à l'arrondi près.

## 4. Dimensionner un plan sur la moyenne, puis sur un quantile

**Observé.** Les déclenchements étaient écrits pour un pilote autonome dont le [fichier de compétence](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md) indique qu'il « ran 3 manual cycles in March 2026 and was never scheduled ». Le même fichier fixe deux limites : au plus 50 déclenchements dans la file, et les déclenchements de plus de 72 heures écartés. Les déclenchements archivés n'ont jamais été consommés : rien de ce qui suit n'est donc une mesure.

**Synthétique.** Supposons un consommateur qui traite au plus c événements par jour, les plus anciens d'abord ; le reste attend, et la capacité non employée est perdue. Un événement est *en retard* quand il n'est pas traité dans les 3 jours suivant son jour d'arrivée (la limite de 72 heures à la résolution d'un jour). Le *centile* d'ordre p est la valeur en position `ceil(p × n / 100)` des effectifs classés (rang le plus proche, la règle des quantiles de PSY-008).

| Plan | c par jour | Événements en retard | Attente la plus longue |
|---|---|---|---|
| Moyenne, arrondie vers le haut | 5 | 489 | 33 jours |
| 90e centile | 8 | 393 | 20 jours |
| 95e centile | 24 | 49 | 6 jours |
| Plus petit c suffisant | 34 | 0 | 3 jours |
| 99e centile | 72 | 0 | 1 jour |

Le plan fondé sur la moyenne offre `5 × 119 = 595` créneaux pour 594 événements et paraît suffisant. Il en traite 440 et en laisse 154 en attente à la fin, parce qu'une capacité laissée oisive pendant les semaines calmes ne peut pas être reportée sur une semaine chargée ; son arriéré culmine à 205 événements, plus de quatre fois la limite de file de 50 prévue par la conception.

Une part de cet échec revient à un plan sans marge, non à la concentration : dans 1 919 des 2 000 journaux synthétiques, une capacité de 5 laisse elle aussi des événements en retard (81 dans le journal médian). Mais là, la plus petite capacité suffisante est de 5 à 7 par jour, et le 95e centile (de 8 à 11) ne laisse jamais un événement en retard. La concentration change le prix du remède : 34 par jour, soit 6,81 fois la moyenne.

Chaque plan du tableau est dimensionné après coup, sur les 119 journées où il est exécuté, et un centile élevé ne se stabilise pas mieux que la moyenne : lu à la fin mai, le 95e valait 8 et non 24, et une capacité de 8 à partir du 1er juin laisse 199 événements en retard sur les 46 journées restantes. Avec moins de 100 journées lues, le 99e centile est la journée la plus chargée à ce jour.

### Exercice pratique 5

Votre critère est celui de la conception : aucun événement en retard. Quel plan en centile du tableau le satisfait ? Calculez la capacité qu'offre le plus petit plan suffisant sur l'ensemble du journal, et la part qui en est employée.

> **Réponse :** Après coup, le 99e centile seulement ; le 95e laisse 49 événements en retard et une attente la plus longue de 6 jours. La plus petite capacité suffisante est de 34 par jour : `34 × 119 = 4,046` créneaux, dont `594 / 4,046 = 14.68%` sont employés et `100 − 14.68 = 85.32%` restent oisifs. Tranchez selon la tolérance et le coût de la capacité oisive, non selon la moyenne. La règle est supposée et les dimensionnements sont lus après coup : un profil d'arrivées, non un consommateur, et aucune recette pour les 119 journées suivantes.

**L'objection la plus forte à la lecture de cette leçon** est qu'un fichier de déclenchement n'est pas une unité de travail. Le même fichier de compétence fusionne les déclenchements qui partagent le type, le dépôt et la référence, et les 594 partagent un seul dépôt et une seule référence : un pilote s'éveillant une fois par jour (une cadence supposée) aurait reçu 132 déclenchements fusionnés, au plus 3 par jour, avec un coefficient de Gini de 0,3287. Sous cette lecture, la concentration décrit la fréquence à laquelle le producteur a tiré, non la quantité de travail arrivée. Ensuite, la part des quatre premières repose sur deux épisodes : **cet échantillon ne permet pas de distinguer un processus à un épisode tous les quelques mois de deux incidents sans rapport.** Un relevé du travail accompli par déclenchement trancherait le premier point ; un flux d'événements plus long, le second.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les 594 fichiers de déclenchement, le workflow et le fichier de compétence dont les liens figurent plus haut. `extract.py` refuse de s'exécuter lorsque le dossier ou un fichier de conception diffère de son épinglage.

**Jeu d'essai.** Le [README](../../../fixtures/psychohistory/psy-009/README.md) donne les commandes, les cas traités à la main, les 41 autovérifications et les contrôles négatifs.

**Lu en dehors du jeu d'essai.** `git log --diff-filter=D` à l'épinglage énumère 12 fichiers de déclenchement supprimés sans avoir été archivés : sept datés du 2026-03-20, dont cinq retirés de `processing/` par le commit du [cycle de pilotage 002](https://github.com/GuitarAlchemist/Demerzel/commit/2b752a763e490aa090cf32ee992cb923a6d1bc24), et cinq datés du 2026-06-30, abandonnés par le commit [`a2c1ef0`](https://github.com/GuitarAlchemist/Demerzel/commit/a2c1ef01d2470ca737b89e005eddc8aa78fa7583). L'un des douze est un déclenchement `self_initiated`, non un événement du dépôt. Aucun ne tombe sur l'une des quatre journées les plus chargées, qui, les douze comptés, porteraient `286 / (594 + 12) = 47.19%`.

**Références de méthode.** Lorenz, M. O. (1905), « Methods of Measuring the Concentration of Wealth », *Publications of the American Statistical Association* 9(70), 209–219, doi:10.2307/2276207. Ceriani, L., et Verme, P. (2012), « The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini », *The Journal of Economic Inequality* 10(3), 421–443, doi:10.1007/s10888-011-9188-x. Hyndman, R. J., et Fan, Y. (1996), « Sample Quantiles in Statistical Packages », *The American Statistician* 50(4), 361–365.

**Non fait.** Aucune distribution n'a été ajustée et aucune loi de queue testée. La règle de capacité est supposée et n'emploie que les effectifs d'arrivée : ni temps de traitement, ni priorité, ni déduplication. Les plans sont dimensionnés après coup : quatre lectures antérieures ne mettent pas à l'épreuve une règle de dimensionnement. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Appliquer les mêmes mesures à un flux d'événements du projet encore en croissance, par exemple les commits par jour. Si son coefficient de Gini est proche de celui d'un placement au hasard pour son propre total et son propre nombre de journées, la concentration trouvée ici appartient au producteur retiré, non au projet.
