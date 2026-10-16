---
module_id: psy-008-bursts-are-not-rates
department: psychohistory
course: "Les rafales ne sont pas des taux : les arrivées d'événements dans le journal des déclenchements"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-008
version: "0.1.0"
---

# Les rafales ne sont pas des taux : les arrivées d'événements dans le journal des déclenchements

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un journal d'événements en comptages par jour civil, vous les comparerez à ce que produirait un taux constant, vous mesurerez l'écart par l'indice de dispersion, et vous remplacerez une moyenne trompeuse par des chiffres sur lesquels un plan peut s'appuyer. **Question de projet :** les archives du journal des déclenchements contiennent 594 événements sur 119 jours civils, dont 100 actifs. Une moyenne d'« environ cinq événements par jour » est-elle une description utilisable pour planifier ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) voit dans le doublement du taux de signaux de conscience sur trois cycles le signe qu'une transition est proche (c'est son cinquième signal). Un taux est une moyenne ; ce module demande ce qu'une moyenne dit d'un journal dont les événements arrivent par rafales. [PSY-009](psy-009-concentration-and-heavy-tails.fr.md) mesure la concentration de ce même journal, [PSY-022](psy-022-competing-explanations.fr.md) y compare des modèles de comptage, et [PSY-024](psy-024-the-single-actor.fr.md) cherche qui a envoyé les événements.

## 1. Compter par jour civil, jours vides compris

**Observé.** Jusqu'à son retrait le 2026-07-18, le workflow [`demerzel-driver-triggers.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) écrivait un fichier JSON, un *déclencheur*, pour chaque push sur la branche principale, chaque ticket (*issue*) ouvert ou rouvert, chaque discussion créée et chaque exécution en échec de quatre autres workflows. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) en contient 594, horodatés du 2026-03-20 au 2026-07-16, de trois types seulement : 252 `discussion_created`, 207 `push` et 135 `issue_opened`. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/extract.py) lit les 594 fichiers au commit `4b03838`, refuse un dossier qui diffère de son empreinte épinglée, et écrit une ligne par événement dans [`observed-input.json`](../../../fixtures/psychohistory/psy-008/observed-input.json). Les quelques fichiers déclencheurs [hors de l'archive](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) sont laissés de côté.

Un *jour* est la date UTC de l'horodatage d'un déclencheur. Du premier jour au dernier, on compte **119** jours civils : **100** jours *actifs*, avec au moins un événement, et **19** jours vides. Un taux rapporte des événements à un temps écoulé ; les jours vides restent donc dans la série.

```text
moyenne par jour civil = 594 / 119 = 4.99
moyenne par jour actif = 594 / 100 = 5.94
```

**Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/analyze.py) dans [`results.json`](../../../fixtures/psychohistory/psy-008/results.json) :

| Événements dans la journée | Jours | Événements |
|---|---|---|
| 0 | 19 | 0 |
| 1 à 2 | 76 | 89 |
| 3 à 11 | 13 | 72 |
| 12 ou plus | 11 | 433 |

Le cas le plus fréquent est un jour à exactement 1 événement : 63 jours, soit 52,94 %. Exactement 5 événements se sont produits sur 2 jours, et 4, 5 ou 6 événements sur 4 jours, soit 3,36 % des jours. « Environ cinq par jour » ne décrit presque aucun jour.

### Exercice pratique 1

Calculez les deux moyennes. Un collègue prévoit le volume des 30 prochains jours civils en multipliant par 30 la moyenne par jour actif. Qu'obtient-il, qu'obtient-on avec la moyenne par jour civil, et où est l'erreur ?

> **Réponse :** `594 / 119 = 4.99` et `594 / 100 = 5.94`. Avec la moyenne par jour civil, `30 × 594 / 119 = 149.75` événements ; avec la moyenne par jour actif, `30 × 5.94 = 178.2`, soit `119 / 100 = 1.19` fois le chiffre obtenu par jour civil : la moyenne par jour actif retire du dénominateur les 19 jours vides, mais les 30 prochains jours compteront eux aussi des jours vides.

## 2. La référence de Poisson et l'indice de dispersion

Si les événements arrivent indépendamment les uns des autres à taux constant (un *processus de Poisson*), le comptage d'une journée suit une loi de Poisson, dont la variance est égale à la moyenne. L'*indice de dispersion* D compare les deux :

```text
probabilité de Poisson   P(k événements) = moyenne^k × exp(−moyenne) / k!
variance d'échantillon   s² = (Σx² − (Σx)² / n) / (n − 1)
indice de dispersion     D  = s² / moyenne
```

Ce module utilise partout la variance d'échantillon, de diviseur n − 1. Un D proche de 1 est ce que donne un taux constant ; un D inférieur à 1 indique des comptages plus réguliers que le hasard (une horloge quotidienne donne 0) ; un D supérieur à 1 est une *surdispersion* : des périodes calmes et des rafales. Sous un processus de Poisson, `(n − 1) × D` suit approximativement une loi du khi-deux à n − 1 degrés de liberté ; D a donc un écart-type d'environ `sqrt(2 / (n − 1))`, ici 0,13 (Cox et Lewis 1966).

**Calculé.** Les comptages quotidiens donnent s² = 198,52 et D = 39,77, soit environ 298 de ces écarts-types au-dessus de 1. La référence est la loi de Poisson de même moyenne que les données observées, 594/119 :

| Type de jour | Probabilité de référence | Attendus sur 119 jours | Observés |
|---|---|---|---|
| aucun événement | 0,68 % | 0,81 | 19 |
| exactement 1 événement | 3,39 % | 4,04 | 63 |
| 4, 5 ou 6 événements | 49,72 % | 59,17 | 4 |
| 12 ou plus (quantile à 99 % de la référence : 11) | 0,54 % | 0,64 | 11 |

Le quantile à 99 % est le plus petit k tel que P(0) + … + P(k) ≥ 0,99. Appelons *jours de rafale* les 11 jours qui le dépassent. Le plus chargé, le 2026-03-22, compte 109 événements ; la référence attribue à un jour au moins aussi chargé une probabilité de 6,32 × 10⁻¹⁰³. Un tel chiffre signifie que la référence décrit mal les données, non qu'un événement presque impossible s'est produit.

**Témoins synthétiques.** Le même code renvoie D = 0,0017 pour 594 événements répartis régulièrement sur 119 jours, et D = 1,23, un écart à 1 compatible avec le hasard, pour un journal généré avec une graine fixée où chaque événement tombe sur un jour tiré uniformément. Les trois journaux ont la même moyenne, 4,99 : la moyenne ne permet pas de les distinguer.

### Exercice pratique 2

Avec n = 119, Σx = 594 et Σx² = 26 390, calculez s² et D, puis dites de combien d'écarts-types D se situe au-dessus de 1.

> **Réponse :** `(Σx)² / n = 352,836 / 119 = 2,965.01`, donc `s² = (26,390 − 2,965.01) / 118 = 23,424.99 / 118 = 198.52` et `D = 198.517 / 4.9916 = 39.77`. Avec `sqrt(2 / 118) = 0.1302`, `(39.77 − 1) / 0.1302 = 297.8` écarts-types : un taux constant n'est pas une hypothèse tenable.

### Exercice pratique 3

Calculez les probabilités P(0) et P(1) de la référence, les nombres attendus de tels jours sur 119, et comparez avec le journal.

> **Réponse :** `exp(−4.9916) = 0.006795` et `119 × 0.006795 = 0.81` jour vide attendu contre 19 observés, 23,5 fois plus. `4.9916 × 0.006795 = 0.03392` et `119 × 0.03392 = 4.04` jours à un seul événement attendus contre 63 observés, 15,6 fois plus. Le journal compte trop de jours vides, de jours à un événement et de jours de rafale, et il lui manque le milieu : les jours qui ressemblent à la moyenne.

## 3. De quoi les jours sont faits

**Calculé à partir des types d'événements.**

*Une horloge.* Sur les 63 jours à un seul événement, 58 contiennent un unique `discussion_created`, horodaté entre 13:51 et 16:09 UTC, dont 56 en semaine. Sur les 85 jours de semaine, 81 comptent au moins un `discussion_created`. C'est compatible avec une tâche planifiée ; un workflow candidat, [`streeling-daily.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/streeling-daily.yml), s'exécute du lundi au vendredi à 13:17 UTC et publie des discussions. Un déclencheur n'enregistre pas quelle discussion il a vue : l'attribution est donc une inférence.

*Les week-ends sont vides ou chargés.* Sur les 19 jours vides, 15 sont des samedis ou des dimanches ; c'est aussi le cas des quatre jours les plus chargés, dont les rafales mêlent plusieurs types d'événements :

| Jour | Événements | `push` | `issue_opened` | `discussion_created` |
|---|---|---|---|---|
| 2026-03-22, dimanche | 109 | 32 | 38 | 39 |
| 2026-06-28, dimanche | 72 | 4 | 34 | 34 |
| 2026-03-21, samedi | 60 | 41 | 6 | 13 |
| 2026-06-27, samedi | 45 | 0 | 21 | 24 |

**Observé.** L'enregistrement du projet [`anti-pattern-003-push-triggered-spam`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/patterns/anti-pattern-003-push-triggered-spam.pattern.json) décrit des workflows qui « trigger on every push to master, causing duplicate runs when a session has many commits » (se déclenchent à chaque push sur master et lancent des exécutions en double quand une session compte de nombreux commits). Il date ce motif du 2026-03-21 et du 03-22 (2 occurrences), le détecte par « Workflow runs > 3 in a single day for the same workflow » (plus de trois exécutions d'un même workflow dans une même journée) et signale la correction d'un workflow le 03-22.

**Calculé.** Le journal est compatible avec l'enregistrement sur ces deux jours : 41 et 32 événements `push`. Mais les push comptent pour 77 des 286 événements des quatre jours les plus chargés, soit 26,92 %, moins que leur part dans l'ensemble du journal (207 sur 594, soit 34,85 %).

Chaque fichier archivé correspond à une exécution du producteur, censé s'exécuter une fois par événement. Appliqué à la lettre à ce producteur, le seuil de l'enregistrement est franchi sur 21 jours, dont 18 après le 03-22. Notez la forme de la règle : un seuil sur un comptage quotidien, non sur une moyenne.

### Exercice pratique 4

Classez trois jours : (a) le 2026-03-21, 60 événements dont 41 `push` ; (b) le 2026-06-27, 45 événements, aucun `push` ; (c) le 2026-04-07, un mardi avec un seul `discussion_created` à 13:54 UTC. Lesquels l'enregistrement sur le spam déclenché par les push décrit-il, et lesquels sa règle signalerait-elle ?

> **Réponse :** (a) Décrit et signalé : une rafale de push à une date que l'enregistrement mentionne, et 60 > 3. (b) Signalé, puisque 45 > 3, mais non décrit : aucun push, la rafale se compose de 21 tickets et de 24 discussions. (c) Ni l'un ni l'autre : une seule exécution, à l'heure d'une tâche planifiée en semaine. Trois profils se cachent derrière une même moyenne ; une correction visant les push n'aurait pas touché (b).

## 4. Des fenêtres plus longues ne sauvent pas la moyenne

Une parade naturelle consiste à planifier par semaine et à laisser les rafales se compenser en moyenne. Découpez les 119 jours en 17 blocs de 7 jours à partir du premier jour :

```text
176 38 8 13 7 5 14 6 15 6 6 6 8 63 204 11 8
```

**Calculé.** Un bloc compte en moyenne 34,94 événements, le bloc médian 8 (le quantile à 50 % ; selon la méthode du *rang le plus proche*, le quantile d'ordre p est la k-ième plus petite des n valeurs, avec k = p × n arrondi à l'entier supérieur). Sur les blocs, D vaut 104,41, davantage que sur les jours ; un processus de Poisson donnerait environ 1 quelle que soit la longueur de la fenêtre. Un indice qui croît avec la fenêtre signifie que les jours chargés arrivent par séries : les 11 jours de rafale forment deux *épisodes* (des jours de rafale séparés d'au plus 7 jours comptent pour un seul épisode, un choix d'analyse), trois jours entre le 03-21 et le 03-27 et huit entre le 06-21 et le 07-02, à 86 jours d'intervalle.

Le total d'un bloc a au moins doublé sur 4 des 16 passages d'un bloc au suivant ; une règle de doublement du type de PSY-002 a donc besoin d'une référence qui tienne compte des rafales. La moyenne elle-même est mal connue : son erreur type, `sqrt(variance / n)`, vaudrait 0,20 avec la variance de la référence (la moyenne), et vaut 1,29 avec s² et 2,09 à partir des blocs, `sqrt(s²_blocks / 17) / 7`. Le résultat ne dépend pas non plus de minuit UTC : avec la limite du jour décalée de 6, 12 ou 18 heures, D se situe entre 47,58 et 64,09 et la médiane reste à 1.

**Ce qu'il faut utiliser pour planifier** (calculé) : jours vides, 15,97 % ; jours à 2 événements au plus, 79,83 % ; médiane 1, quantile à 90 % égal à 8, quantile à 95 % égal à 24, maximum 109 ; jours de rafale, 11 sur 119, en deux épisodes. PSY-009 dimensionne un plan sur un tel quantile.

**L'objection la plus forte à cette lecture** : pour un total sur un horizon long, le taux moyen est la bonne grandeur quelle que soit la dispersion, puisque total attendu = taux × durée. Cela ne vaut que si les mois à venir ressemblent à ces 17 semaines, et même alors le taux est de 4,99 avec une erreur type voisine de 2,09, parce que 11 jours de rafale portent 433 des 594 événements. **Cet échantillon ne permet pas de distinguer un processus qui produit des rafales à quelques mois d'intervalle d'un processus qui en a produit deux pour des raisons sans lien entre elles.** La prochaine vérification trancherait.

### Exercice pratique 5

Un coéquipier propose « environ 35 événements par semaine, à 20 % près ». Combien des 17 blocs tombent dans cette fourchette ? Énoncez un critère pour accepter une moyenne comme description utile à la planification, et appliquez-le.

> **Réponse :** 20 % autour de 34,94 donnent 27,95 à 41,93 ; un seul bloc sur 17 (38 événements) tombe dans la fourchette, et le bloc médian compte 8 événements. Critère : accepter la moyenne quand les comptages se dispersent autour d'elle comme sous un taux constant, avec un D à moins de deux écarts-types de 1 pour la fenêtre sur laquelle vous planifiez. Pour 17 blocs, `sqrt(2 / 16) = 0.35`, donc D devrait se situer entre 0,29 et 1,71 ; il vaut 104,41. Rejetez la moyenne ; planifiez avec la part des jours vides, la médiane et les épisodes de rafales.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les 594 fichiers déclencheurs archivés (arbre Git `2da37c16496d39c0c9137897c8be2b0c6d6b7978` ; empreinte du manifeste dans `observed-input.json`), l'enregistrement du motif et les deux fichiers de workflow dont les liens figurent plus haut.

**Jeu d'essai.** [`scenarios.json`](../../../fixtures/psychohistory/psy-008/scenarios.json) contient les choix d'analyse ; le [README](../../../fixtures/psychohistory/psy-008/README.md) donne les commandes, les autocontrôles et les témoins.

**Références de méthode.** Cox, D. R., et Lewis, P. A. W. (1966), *The Statistical Analysis of Series of Events*, Methuen (l'indice de dispersion et son test). Barabási, A.-L. (2005), « The origin of bursts and heavy tails in human dynamics », *Nature* 435, 207–211 (les temps entre événements, non analysés ici).

**Limites et ce qui n'a pas été fait.** Un seul dépôt et 119 jours, la durée de service d'un seul workflow producteur ; deux épisodes ne peuvent pas dire à quelle fréquence surviennent les rafales. Un horodatage indique le moment où le producteur a écrit le fichier. Douze fichiers déclencheurs ont été supprimés du dépôt sans avoir été archivés (sept datés du 2026-03-20, cinq du 2026-06-30, aucun sur les quatre jours les plus chargés) ; PSY-009 les compte, et avec eux la moyenne serait de 5,09 et D de 39,40. On n'a pas vérifié si des exécutions qui se chevauchaient en ont perdu d'autres. Aucun modèle de comptage n'a été ajusté (PSY-022), aucune mesure de concentration calculée (PSY-009), aucune cause de rafale établie. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Compter les push, les tickets et les discussions par jour à partir de l'historique des événements de GitHub lui-même, sur une période plus longue, avec la cause de chaque jour de rafale. Si les rafales reviennent avec un espacement et une taille stables, une horloge de semaine complétée par des épisodes devient un plan utilisable ; sinon, le plan honnête est une alerte à seuil, non une prévision.
