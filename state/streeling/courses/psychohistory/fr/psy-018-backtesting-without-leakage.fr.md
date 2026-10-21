---
module_id: psy-018-backtesting-without-leakage
department: psychohistory
course: "Tests rétrospectifs sans fuite de données"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-018
version: "0.1.0"
---

# Tests rétrospectifs sans fuite de données

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Un *test rétrospectif* (*backtest*) évalue une méthode de prévision sur des données qui existent déjà, comme si chaque valeur n'était pas encore arrivée. Vous déciderez ce qu'est une prévision dans un relevé irrégulier, vous ferez glisser l'origine le long de ce relevé, vous évaluerez trois méthodes simples et vous reconnaîtrez trois façons dont une valeur ultérieure s'introduit dans une prévision antérieure. **Question de projet :** comment tester une prévision du nombre de citations d'un artefact sans qu'une fuite fasse entrer le futur dans le test ?

[PSY-005](psy-005-persistence-baseline.fr.md) évaluait « rien ne change » sur des étiquettes. Une série numérique ajoute des erreurs qui ont une taille, ainsi que des statistiques à ajuster, par lesquelles entrent les fuites. [PSY-011](psy-011-measurement-change-or-system-change.fr.md) étudie le changement d'instrument mis de côté ici ; [PSY-004](psy-004-how-large-is-large.fr.md) explique pourquoi des observations qui partagent une cause comptent pour moins.

## 1. Ce qu'il y a à prévoir

**Observé.** À chaque *exécution*, le *feeder* (l'alimenteur) [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py) ajoute à [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) une ligne par *artefact* de gouvernance (une politique, une compétence). `citation_count` est censé être [le nombre de fichiers suivis qui mentionnent l'artefact](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) ; les fichiers de leçon comptent eux aussi, d'où les barres obliques espacées ci-dessous. Selon la [ligne 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), `delta_citations` est ce nombre moins celui de la ligne précédente, ou 0 sur une ligne marquée `rebaseline`.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/extract.py) fige ces fichiers au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-018/observed-input.json) : **1 548** lignes, **88** exécutions, **18** artefacts. Les 11 lignes de la première exécution sont des lignes d'amorçage sans nombre de citations ; il reste 1 537 lignes qui portent un nombre, et 1 537 − 18 = 1 519 *paires de lignes consécutives* d'un même artefact.

Le nombre diffère dans **20** paires : 16 se terminent le 2026-09-13 et 4 le 2026-10-03. Jusqu'à la première de ces dates, les nombres étaient [saisis à la main et jamais mis à jour](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) ; dans l'exécution du 2026-09-13T17:52:14Z, un décompte par `git grep` les a remplacés pour 16 artefacts (`policies / alignment-policy.yaml` est passé de 3 à 42), et le feeder a marqué ces lignes `rebaseline: true`. L'*instrument*, la procédure qui produit le nombre, avait changé. Ce module fait repartir chaque série à une ligne de rebaseline : une *série*, c'est un artefact sous un même instrument. On obtient ainsi **34** séries (16 avant une ligne de rebaseline, 16 à partir d'une telle ligne, 2 artefacts jamais remesurés) et 1 519 − 16 = 1 503 paires à l'intérieur d'une série.

À l'intérieur des séries, **4** paires changent, dans 4 artefacts : toutes dans l'exécution du 2026-10-03T15:31:16Z, toutes de +2 (de 42 à 44, de 43 à 45, et de 27 à 29 deux fois). Les 30 autres séries ne varient jamais.

- **Deux ensembles de vingt.** 20 lignes portent un `delta_citations` non nul et 20 lignes diffèrent du nombre de la ligne précédente, mais 4 lignes seulement appartiennent aux deux ensembles : seize deltas non nuls se trouvent sur la première ligne d'un artefact à porter un nombre, où le feeder soustrait 0, et les 16 lignes de rebaseline ont changé alors que leur delta était inscrit à 0. Ce module compte les changements de valeur.
- **Une exécution n'est pas un jour.** Deux exécutions consécutives du feeder sont espacées de 0,001 à 6,453 jours : prévoir « à un pas » veut dire prévoir l'exécution suivante.

### Exercice pratique 1

Une prévision a besoin de deux lignes antérieures de sa série. En partant de 1 548 lignes, établissez le nombre de prévisions qu'offrent les 34 séries. Quelles lignes ont un delta non nul alors que leur nombre n'a pas changé ?

> **Réponse :** `1,548 − 11 = 1,537` lignes qui portent un nombre ; `1,537 − 18 = 1,519` paires ; `1,519 − 16 = 1,503` paires à l'intérieur d'une série ; la première paire de chaque série n'a qu'une ligne antérieure, d'où `1,503 − 34 = 1,469` prévisions. Les `20 − 4 = 16` lignes sont des premières lignes à porter un nombre, 12 le 2026-07-18 et 4 le 2026-07-29 : leur delta est le nombre lui-même.

## 2. Faire glisser l'origine

Une prévision a une *origine*, la dernière ligne qu'elle peut utiliser, et une *cible*, la ligne qu'elle prédit. Un *découpage temporel* place toutes les lignes d'entraînement avant toutes les lignes de test. Une *origine glissante* répète ce découpage : chaque ligne devient tour à tour la cible, prévue à partir des seules lignes qui la précèdent ([Hyndman et Athanasopoulos, section 5.10](https://otexts.com/fpp3/toolbox.html#sec-tscv) ; Tashman 2000). Trois méthodes, pour une série y_1 … y_t connue à l'origine t :

```text
persistance (naïve)   prévision = y_t
moyenne à ce jour     prévision = (y_1 + ... + y_t) / t
dérive                prévision = y_t + (y_t - y_1) / (t - 1)

erreur = observé - prévision       MAE = moyenne de |erreur|
MAE relative = MAE / MAE de la persistance, sur les mêmes prévisions
```

**Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-018/analyze.py) dans [`results.json`](../../../fixtures/psychohistory/psy-018/results.json), arrondi à 6 décimales :

| Méthode | Erreur absolue totale (1 469 prévisions) | MAE, une série qui varie (30 prévisions) | MAE relative |
|---|---|---|---|
| persistance | 8 | 0,066667 | 1 |
| dérive | 11,177980 | 0,093150 | 1,397247 |
| moyenne à ce jour | 72,156930 | 0,601308 | 9,019616 |

La persistance se trompe de 2 à chacun des quatre sauts. Les deux autres méthodes commettent les mêmes erreurs et continuent d'en payer le prix : la moyenne à ce jour reste en retard sur le nouveau niveau pendant dix lignes de plus, et la dérive extrapole une hausse survenue une seule fois. Toutes ces erreurs se trouvent parmi les 480 prévisions qui portent sur des décomptes par `git grep` ; les 819 qui portent sur des nombres saisis à la main et les 170 qui portent sur les deux artefacts jamais remesurés relisent un nombre que personne n'a mis à jour. Là, toutes les méthodes sont exactes, et la MAE relative des 30 séries plates vaut 0/0.

Une *erreur mise à l'échelle* (*scaled error*, Hyndman et Koehler 2006) divise chaque erreur par la MAE de la prévision naïve sur les lignes d'entraînement :

```text
échelle à l'origine t   = (|y_2 - y_1| + ... + |y_t - y_(t-1)|) / (t - 1)
erreur mise à l'échelle = |erreur| / échelle
```

Ici, l'échelle reste à 0 tant qu'une série n'a pas changé : 40 seulement des 1 469 prévisions ont une échelle positive, aucune dans une série plate, et les quatre erreurs de la persistance tombent sur des origines où l'échelle vaut encore 0. Sur ces 40, la persistance obtient 0 et la dérive 1 : dès lors que chaque série repart à sa ligne de rebaseline, le score n'existe que là où il ne reste plus rien à mesurer.

### Exercice pratique 2

`policies / alignment-policy.yaml` affiche 42 pendant 21 lignes, puis 44 pendant 11 lignes. Calculez les trois prévisions de la ligne 23 (origine : ligne 22) et leurs erreurs, puis la MAE de la persistance sur les 30 prévisions de cette série.

> **Réponse :** Persistance : 44, erreur 0. Moyenne à ce jour : `(21 × 42 + 44) / 22 = 42.090909`, erreur 1,909091. Dérive : `44 + (44 − 42) / 21 = 44.095238`, erreur −0,095238. La persistance se trompe une seule fois, de 2, à la ligne 22 : MAE `2 / 30 = 0.066667`.

### Exercice pratique 3

Même série. Donnez l'échelle aux origines 21 et 22, puis l'erreur mise à l'échelle de chaque méthode pour la ligne 23. Quelle est l'erreur mise à l'échelle des prévisions de la ligne 22 ?

> **Réponse :** À l'origine 21, toutes les lignes affichent 42 : échelle 0. À l'origine 22, un changement de 2 en 21 paires : `2 / 21 = 0.095238`. Ligne 23 : persistance 0, moyenne à ce jour `(42 / 22) / (2 / 21) = 20.045455`, dérive `(2 / 21) / (2 / 21) = 1`. À la ligne 22, celle du saut, toutes les méthodes se trompent de 2 pour une échelle de 0 : l'erreur mise à l'échelle est indéfinie.

## 3. Trois façons dont le futur s'introduit

Un test rétrospectif **présente une fuite** quand une prévision utilise une donnée qui n'était pas encore enregistrée à son origine : la cible, une ligne ultérieure ou un nombre qui en est dérivé (une moyenne, une échelle, un paramètre ajusté), y compris des lignes ultérieures placées parmi les lignes d'entraînement par un découpage aléatoire (d'après Kaufman et al. 2012). Une seule question permet de tester n'importe quel nombre d'une chaîne de traitement : *aurait-il pu être noté à l'origine ?* Une erreur voisine ne change aucune prévision mais biaise le score : choisir les cibles à l'aide d'une information ultérieure, une *sélection a posteriori*. Choisir une méthode sur les lignes de test relève de la réutilisation du jeu de test étudiée dans [PSY-013](psy-013-four-scores-and-a-trend.fr.md).

La persistance n'ajuste rien : deux des trois fuites ne peuvent donc pas l'atteindre ; elles atteignent toute méthode qui ajuste une statistique. La plus simple est un *niveau* : la moyenne des lignes d'entraînement, prise comme prévision de chaque ligne de test. **Calculé :** prenez une série qui varie (32 lignes ; les quatre donnent des nombres identiques) et testez sur son dernier quart, un choix consigné dans [`scenarios.json`](../../../fixtures/psychohistory/psy-018/scenarios.json).

| Test du niveau ajusté | MAE sur les 8 lignes de test | Variation |
|---|---|---|
| Découpage temporel : niveau calculé sur les lignes 1 à 24 | 1,75 | référence |
| Fuite 1 : niveau calculé sur les 32 lignes, lignes de test comprises | 1,3125 | −25 % |
| Fuite 3 : 8 lignes de test tirées au hasard, niveau calculé sur les 24 autres, dont des lignes ultérieures | 0,931452 | −46,77 % |

Le troisième chiffre est la moyenne exacte sur les 10 518 300 façons de tirer les lignes de test ; 165 seulement donnent une erreur aussi grande que celle du découpage temporel.

La **fuite 2** est une variable explicative qui encode la cible : prévoir « nombre précédent + `delta_citations` de la ligne cible ». Sous l'origine glissante, elle ne commet aucune erreur sur 1 469 prévisions, là où la persistance se trompe quatre fois : −100 %.

Les fuites 1 et 3 ne flattent pas toujours le score. Sur les 30 points de coupure qui laissent au moins deux lignes d'entraînement, la fuite 1 abaisse l'erreur dans 21 cas (de 34,38 % au plus), est sans effet dans 1 cas et l'augmente dans 8 (de 25 % au plus) ; la fuite 3 l'abaisse dans 23 cas et l'augmente dans 7. Sous l'origine glissante, la moyenne de toute la série obtient 0,916667, contre 0,601308 pour la moyenne à ce jour, soit une erreur supérieure de 52,45 %, parce que la moyenne honnête est exacte tant que la série est plate. Une fuite fausse le score, dans un sens qui dépend de l'endroit où le changement tombe parmi les lignes de test.

### Exercice pratique 4

À l'aide de la question « aurait-il pu être noté à l'origine ? », classez chaque cas comme une fuite, une sélection a posteriori ou ni l'un ni l'autre : (a) une échelle calculée sur toute la série ; (b) un test portant sur « les artefacts qui varient » seulement ; (c) le `delta_citations` de la ligne d'origine. Calculez ensuite la prévision de la fuite 2 pour `constitutions / asimov.constitution.md` à sa ligne de rebaseline : nombre précédent 5, `delta_citations` 0, valeur observée 65.

> **Réponse :** (a) Fuite : l'échelle contient des lignes ultérieures ; elle rendrait définie chaque erreur mise à l'échelle d'une série qui varie (persistance 1,033333). (b) Sélection a posteriori : aucune prévision ne change, mais on ne sait quels artefacts varient qu'à la fin du relevé ; les 1 469 prévisions regroupées évitent ce choix. (c) Ni l'un ni l'autre : ce delta était enregistré à l'origine. Prévision `5 + 0 = 5`, erreur 60. La variable entachée de fuite échoue là où le feeder a écrit 0 : sur l'ensemble des 1 519 paires, elle manque les 16 lignes de rebaseline, pour une erreur absolue totale de 306.

## 4. Ce que ce test rétrospectif peut montrer

**Quatre séries, un seul événement.** Les quatre changements partagent une exécution et une taille ; les quatre séries partagent un même profil d'erreurs, si bien que les rapports de la section 2 se répètent par construction. Sur 85 exécutions cibles, une seule contient toutes les erreurs de la persistance. Lu hors du jeu d'essai, l'historique est compatible avec une cause unique : entre les deux exécutions, le commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642) a ajouté 26 leçons traduites, dont six contiennent en toutes lettres les chemins de ces artefacts, deux par artefact. Prévoir ce nombre, c'est prévoir ce qui s'écrit dans le dépôt, leçons comprises. « La persistance a battu la dérive sur 4 séries sur 4 » ressemble à quatre tirages à pile ou face (une analogie), une probabilité de 1/16 ; avec un seul événement, c'est un seul tirage, 1/2.

**L'objection la plus forte à cette leçon** est que son propre test dépend d'une valeur ultérieure. Le marqueur `rebaseline` se trouve dans la ligne cible : à l'origine du 2026-09-13T15:24:53Z, personne ne pouvait savoir que l'exécution suivante, 0,102 jour plus tard, changerait d'instrument. Faire repartir la série à cet endroit est une sélection a posteriori : cela retire 16 cibles à l'aide d'une information ultérieure. Sans ce redémarrage, l'erreur absolue totale de la persistance vaut 314 au lieu de 8, dont 306 (97,45 %) sur les lignes de rebaseline. Les deux chiffres répondent à des questions différentes, « que dira le fichier ? » et « que lira cet instrument ? » ; un rapport doit dire à laquelle il répond.

**Cet échantillon ne permet pas de distinguer** un processus par paliers d'une tendance lente, ni de classer les méthodes au-delà d'un pas : à instrument fixe, il contient un seul événement en 31 pas d'une exécution à la suivante. Il montre quelque chose de plus étroit : la manière de tenir les comptes d'un test a fait varier une erreur annoncée, de −100 % à +52,45 % par les trois fuites, et de 8 à 314 par le choix des cibles. Seul un relevé plus long permettrait d'en établir davantage.

### Exercice pratique 5

(a) Pourquoi 1/16 n'est-il pas la bonne probabilité pour « 4 sur 4 » ? (b) Supposez, uniquement pour fixer une échelle, que les exécutions avec changement continuent d'arriver une fois tous les 31 pas d'une exécution à la suivante. Au bout de combien d'exécutions en attend-on 10, contre les 32 enregistrées depuis la rebaseline ?

> **Réponse :** (a) `(1/2)^4 = 1/16` exige quatre comparaisons indépendantes ; les quatre sauts partagent une exécution et une taille : un seul événement, probabilité `1/2`. (b) `10 × 31 = 310` pas, donc 311 exécutions, environ dix fois les 32 enregistrées. Le taux repose sur une seule exécution avec changement : un ordre de grandeur, pas un calendrier.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers JSONL de `state/quality-trend/` et les deux scripts dont les liens figurent plus haut.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-018/extract.py`, puis `analyze.py`, puis `analyze.py --check` ; le [README](../../../fixtures/psychohistory/psy-018/README.md) énumère les 35 autocontrôles, les formes closes et les témoins négatifs.

**Références de méthode.** Hyndman, R. J., et Koehler, A. B. (2006), « Another look at measures of forecast accuracy », *International Journal of Forecasting* 22(4), 679–688. Tashman, L. J. (2000), « Out-of-sample tests of forecasting accuracy: an analysis and review », *International Journal of Forecasting* 16(4), 437–450. Kaufman, S., Rosset, S., Perlich, C., et Stitelman, O. (2012), « Leakage in data mining: Formulation, detection, and avoidance », *ACM Transactions on Knowledge Discovery from Data* 6(4), 1–21. Hyndman, R. J., et Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, 3e édition, OTexts, sections 5.2, [5.8](https://otexts.com/fpp3/toolbox.html#sec-accuracy) et 5.10.

**Non fait.** Aucun modèle n'a été ajusté au-delà des trois méthodes de référence. Le temps irrégulier qui sépare une origine de sa cible (de 0,001 à 6,453 jours) n'a pas été modélisé. L'historique a été lu à la main, hors du jeu d'essai. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Relancer le jeu d'essai quand le relevé contiendra, sous un même instrument, plusieurs exécutions avec changement aux causes distinctes : une méthode qui battrait alors la persistance transformerait « impossible de classer » en un classement assorti d'une incertitude déclarée.
