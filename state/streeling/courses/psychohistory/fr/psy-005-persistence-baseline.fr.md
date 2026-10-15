---
module_id: psy-005-persistence-baseline
department: psychohistory
course: "La persistance d'abord : la référence qu'une prévision de gouvernance doit battre"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-005
version: "0.1.0"
---

# La persistance d'abord : la référence qu'une prévision de gouvernance doit battre

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous déciderez ce qu'on compte comme une prévision dans un journal, vous évaluerez la prévision « rien ne change », vous exprimerez toute autre prévision par un score de compétence (*skill score*) relatif à celle-ci, et vous direz quand ce score ne peut pas être calculé. **Question de projet :** si un modèle prédit, pour chaque artefact de gouvernance, l'étiquette d'efficacité du lendemain, quelle exactitude la prévision « rien ne change » atteint-elle déjà sur la tendance de qualité enregistrée ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) voit dans un changement rapide de l'équilibre entre les étiquettes de valeur de vérité le signe d'un changement de régime à venir. Tout modèle qui prévoit de telles étiquettes doit d'abord être comparé à la prévision la moins coûteuse qui soit ; ce module construit cette comparaison pour des étiquettes catégorielles. [PSY-016](../en/psy-016-brier-score.md) évalue des prévisions probabilistes sur les mêmes paires, [PSY-006](psy-006-transition-matrix-from-counts.fr.md) en tire une matrice de transition, et [PSY-018](../en/psy-018-backtesting-without-leakage.md) teste rétrospectivement des séries numériques.

## 1. Décider ce qu'est une prévision

**Observé.** Une [tâche planifiée quotidienne](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) lance [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), que le dépôt appelle le *feeder* (l'alimenteur). Ce script lit un enregistrement d'évolution (un fichier JSON dans `state/evolution/`) par *artefact* de gouvernance (une politique, une constitution, un schéma, une compétence) et ajoute une ligne par artefact dans `state/quality-trend/`. Toutes les lignes d'un même lancement partagent un `timestamp` ; appelons cela une *exécution*. Le champ `effectiveness_to` d'une ligne est la valeur de vérité que l'enregistrement attribue actuellement à une proposition écrite portant sur l'artefact : T (vrai), P (probable), U (inconnu), D (douteux), F (faux) ou C (contradictoire). Son champ `effectiveness_from` est [recopié de la ligne précédente de l'artefact](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L104).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/extract.py) fige ces fichiers au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-005/observed-input.json) : **1 548** lignes, **88** exécutions réparties sur **83** dates UTC, **18** artefacts. La première exécution est d'une autre nature. Ses 11 lignes, horodatées du 2026-05-01, portent la marque `baseline: true` : ce sont des *lignes d'amorçage*, qui consignent un état de départ. Les 87 autres sont des *exécutions du feeder*, du 2026-07-18 au 2026-10-13.

Les deux étiquettes sont présentes dans 1 540 lignes. Sept lignes n'ont pas de champ `effectiveness_from`, faute d'étiquette antérieure à recopier. Une ligne, la première de `contracts / galactic-protocol.md`, n'a ni l'une ni l'autre : le feeder écrit un `effectiveness_to` nul quand l'évaluation d'un enregistrement est du texte libre, et c'est ce que [contenait alors cet enregistrement](https://github.com/GuitarAlchemist/Demerzel/blob/d9ddbaf9203a12b14c31b580070599efb8498031/state/evolution/2026-07-23-galactic-v1.3-ratification.evolution.json) (lu une seule fois au commit `d9ddbaf`, hors du jeu d'essai).

Une prévision a besoin d'un instant d'émission et d'un instant de vérification postérieur. Les données se prêtent à deux lectures :

- **Dans la ligne :** `effectiveness_from` face à `effectiveness_to` au sein d'une même ligne, soit 1 540 paires.
- **Lignes consécutives :** le champ `effectiveness_to` d'un artefact dans une ligne, face à celui de sa ligne suivante. Il y a 1 548 − 18 = 1 530 paires de lignes ; 1 d'entre elles part de la ligne sans étiquette, ce qui en laisse **1 529**.

Cette leçon retient les lignes consécutives : chaque paire relie deux étiquettes enregistrées à deux instants différents. Le décompte fait dans la ligne contient aussi les 11 lignes d'amorçage, dont les deux champs ont été écrits ensemble, sans aucune ligne antérieure : il n'existait aucun moment antérieur où une prévision aurait pu être émise, et les 11 concordent par construction. **Recoupement calculé :** hors des lignes d'amorçage, les deux lectures donnent les mêmes 1 529 paires, et aucune ligne n'a un champ `effectiveness_from` différent du champ `effectiveness_to` de la ligne précédente (0 discordance ; `negative_controls` dans [`results.json`](../../../fixtures/psychohistory/psy-005/results.json) montre qu'une discordance introduite volontairement est bien comptée).

### Exercice pratique 1

En partant de 1 548 lignes et de 18 artefacts, établissez le nombre de prévisions. Retrouvez-le ensuite à partir des 1 540 lignes qui portent les deux étiquettes, et dites pourquoi 1 540 n'est pas, tel quel, le bon décompte.

> **Réponse :** La première ligne de chaque artefact n'a pas de prédécesseur : `1,548 − 18 = 1,530` paires de lignes. L'une d'elles part de la ligne sans étiquette : `1,530 − 1 = 1,529` prévisions. Dans l'autre sens, `1,540 − 11 = 1,529` une fois les lignes d'amorçage retirées. Compter 1 540 ajouterait 11 paires sans aucune exécution antérieure, chacune « correcte » pour la seule raison que ses deux champs ont été écrits ensemble.

## 2. Évaluer la prévision qui ne prédit rien de nouveau

La *prévision par persistance* dit que la prochaine étiquette sera égale à l'étiquette actuelle ; elle ne demande ni modèle ni données d'entraînement. L'*exactitude* est la part des prévisions conformes à ce qui a été observé ensuite. Le *taux de base de changement* est la part des paires dont l'étiquette a changé.

```text
exactitude                   = prévisions correctes / prévisions
taux de base de changement   = paires avec changement / paires
exactitude de la persistance = 1 - taux de base de changement
```

**Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-005/analyze.py) à partir de l'instantané (pourcentages arrondis à deux décimales) :

| Paires | Nombre | Avec changement | Exactitude de la persistance |
|---|---|---|---|
| Toutes les paires exploitables | 1 529 | 1 | 1 528/1 529 = 99,93 % |
| D'une ligne d'amorçage à la première exécution du feeder, 78,5 jours | 11 | 1 | 10/11 = 90,91 % |
| Entre exécutions du feeder séparées de moins d'une demi-journée | 72 | 0 | 100 % |
| Entre exécutions du feeder séparées de 0,565 à 1,372 jour | 1 433 | 0 | 100 % |
| Entre exécutions du feeder séparées de 6,453 jours | 13 | 0 | 100 % |

La réponse à la question de projet est 99,93 % sur tout ce qui a été enregistré, et 100 % sur les 1 433 paires dont les deux lignes sont séparées d'environ un jour. Le taux de base de changement est de 1/1 529 = 0,000654. L'unique changement va de U à F, pour `skills/demerzel-drive + policies/autonomous-loop-policy v1.1.0` ; les étiquettes des dix-sept autres artefacts n'ont jamais changé dans l'historique.

L'unité compte, et la référence aussi. Évaluée par exécution (« aucune étiquette ne change dans cette exécution »), la persistance a raison pour 86 des 87 exécutions cibles, soit 98,85 %. Une autre prévision peu coûteuse, « toujours T » (l'issue la plus fréquente, choisie a posteriori), a raison pour 775 des 1 529 paires, soit 50,69 %. Un modèle doit battre la meilleure des prévisions peu coûteuses, non pas zéro, ni la plus faible d'entre elles.

### Exercice pratique 2

À partir du tableau et du paragraphe ci-dessus, calculez l'exactitude de la persistance et le taux de base de changement (a) sur toutes les paires exploitables et (b) sur toutes les paires entre exécutions du feeder. Calculez ensuite l'exactitude de « toujours T ».

> **Réponse :** (a) `1,528 / 1,529 = 0.999346`, soit 99,93 % ; taux de base `1 / 1,529 = 0.000654`. (b) `72 + 1,433 + 13 = 1,518` paires et aucun changement : exactitude 100 %, taux de base 0. « Toujours T » : `775 / 1,529 = 0.506867`, soit 50,69 %. Ce sont des décomptes sur l'instantané épinglé, pas des prévisions des exécutions futures.

## 3. Mesurer la compétence à partir de la référence

Un *score de compétence* place une exactitude A sur une échelle où une prévision de référence obtient 0 et une prévision sans erreur obtient 1 :

```text
compétence = (A - A_ref) / (1 - A_ref) = 1 - E / E_ref
```

E et E_ref comptent les erreurs de la prévision et celles de la référence sur les mêmes paires. Une compétence négative signifie que la prévision a fait moins bien que la référence.

Ici, la référence est la persistance, avec E_ref = 1. L'échelle progresse donc par pas entiers de 1 : aucune erreur donne 1, une erreur donne 0, deux erreurs donnent −1. Aucune valeur entre 0 et 1 n'est possible.

**Synthétique.** Les modèles ci-dessous n'existent pas. [`scenarios.json`](../../../fixtures/psychohistory/psy-005/scenarios.json) définit chacun d'eux par la façon dont il se serait comporté sur les paires observées :

| Modèle imaginaire | Comportement | Exactitude | Compétence |
|---|---|---|---|
| `echo` | renvoie l'étiquette précédente, quel que soit son fonctionnement interne | 99,93 % | 0 |
| `one_false_alarm` | comme `echo`, plus un changement annoncé qui n'a pas eu lieu | 99,87 % | −1 |
| `one_right_call` | annonce l'unique changement et rien d'autre | 100 % | 1 |
| `cautious_alarm` | annonce l'unique changement et trois autres qui n'ont pas eu lieu | 99,80 % | −2 |

La première ligne du tableau est le cœur de ce module. Un modèle atteint 99,93 % sans rien apprendre d'autre que « recopier la dernière étiquette » ; une exactitude annoncée proche de 99,9 % ne dit donc rien de sa capacité à anticiper un changement. Seule la comparaison avec la persistance le dit, et ici cette comparaison repose sur une seule paire : `one_right_call` obtient le score maximal avec une seule annonce, que cet échantillon ne permet pas de distinguer d'un coup de chance.

### Exercice pratique 3

Un fournisseur annonce que son modèle a eu raison sur 1 527 des 1 529 paires. Donnez son exactitude et sa compétence par rapport à la persistance. Qu'est-ce que cette annonce ne vous dit toujours pas ?

> **Réponse :** Exactitude `1,527 / 1,529 = 0.998692`, soit 99,87 %. Le modèle a commis 2 erreurs là où la persistance en a commis 1 : compétence `= 1 − 2/1 = −1`, moins bien que de recopier la dernière étiquette. L'annonce ne dit pas de quelles erreurs il s'agit : le changement manqué plus une fausse alerte, le changement correctement annoncé plus deux fausses alertes, ou le changement annoncé avec une nouvelle étiquette erronée plus une fausse alerte.

## 4. Non-détections, fausses alertes et l'objection la plus forte

L'exactitude, et un score de compétence construit sur elle, comptent toutes les erreurs de la même façon. Pour des changements rares, il y en a deux sortes : la *non-détection* (un changement que personne n'a annoncé) et la *fausse alerte* (un changement annoncé qui n'a pas eu lieu). Un changement annoncé avec une nouvelle étiquette erronée est lui aussi une erreur. La persistance ne déclenche jamais de fausse alerte et manque tous les changements. Si une non-détection coûte c fois ce que coûte une fausse alerte, comparez `c × misses + false alarms` (c fois le nombre de non-détections, plus le nombre de fausses alertes).

**Analogie (données citées, non issues du projet).** En 1884, les prévisions de tornades de J. P. Finley étaient correctes 96,61 % du temps, sur 2 803 prévisions. Ne jamais prévoir de tornade aurait obtenu 98,18 % ; pourtant Finley a annoncé 28 des 51 tornades, et 72 % de ses alertes étaient fausses ([tableau du JWGFVR](https://jwgfvr.github.io/forecastverification/) ; Murphy 1996). Laquelle des deux prévisions était la meilleure dépend de ce que coûte une tornade manquée.

### Exercice pratique 4

Synthétique. `cautious_alarm` annonce l'unique changement et déclenche trois fausses alertes ; la persistance manque le changement. Pour quel rapport de coûts c `cautious_alarm` est-il la prévision la moins coûteuse, et que coûtent les deux prévisions à c = 10 ?

> **Réponse :** La persistance coûte `c × 1 + 0 = c` ; `cautious_alarm` coûte `c × 0 + 3 = 3`. Les deux sont à égalité à `c = 3` ; au-dessus de 3 l'alerte est moins coûteuse, en dessous de 3 c'est la persistance. À `c = 10`, les coûts sont 10 et 3. L'alerte a l'exactitude la plus faible (99,80 % contre 99,93 %) et une compétence de −2 : le critère est donc le coût de chaque sorte d'erreur, pas l'exactitude. Le modèle est imaginaire : cela ne dit rien d'un prévisionniste réel.

**L'objection la plus forte à la lecture que fait cette leçon** est que son unique changement n'est pas un événement à échéance d'un jour. Il se situe sur le pas de 78,5 jours qui sépare une ligne d'amorçage de la première exécution du feeder, et l'[enregistrement d'évolution](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-03-20-autonomous-driver.evolution.json) de l'artefact date un événement `demoted` du 2026-07-18, le jour de cette exécution. C'est un retrait que quelqu'un a décidé et consigné, non une dérive que l'historique des étiquettes aurait pu révéler. Entre exécutions du feeder, rien n'a changé dans 1 518 paires ; la persistance n'y commet donc aucune erreur et la compétence y est indéfinie (une division par zéro) : un modèle peut égaler le zéro erreur de la persistance ou en commettre davantage, jamais moins. Les étiquettes sont en outre des évaluations écrites que le feeder relit ; une étiquette inchangée peut signifier « personne n'a réévalué » tout autant que « toujours efficace ». **Cet échantillon ne permet de distinguer ni un système stable d'un enregistrement non révisé, ni un modèle compétent de la persistance.** Deux choses trancheraient : l'historique des modifications des enregistrements d'évolution (à quelle fréquence une valeur de vérité est réexaminée, et à quelle fréquence elle change alors), et un historique assez long pour contenir plusieurs changements entre exécutions du feeder.

### Exercice pratique 5

Écartez les 11 paires qui partent d'une ligne d'amorçage. (a) Quelle est l'exactitude de la persistance sur le reste, et quelle compétence un modèle peut-il y montrer ? (b) Supposez, uniquement pour fixer une échelle, que les changements continuent de se produire dans 1 paire sur 1 529, quel que soit le temps écoulé entre les deux lignes, et que chaque exécution compte 18 artefacts. Au bout de combien d'exécutions attend-on 10 changements ?

> **Réponse :** (a) `1,529 − 11 = 1,518` paires, dont aucune n'a changé : exactitude 100 %. E_ref vaut 0, le score de compétence est donc indéfini ; un modèle peut égaler la persistance, sans erreur, ou tomber en dessous. (b) `10 × 1,529 = 15,290` paires, et `15,290 / 18 = 849.4`, donc 850 exécutions, contre 87 exécutions du feeder enregistrées à ce jour. L'hypothèse repose sur un seul changement observé, et ce changement se situe sur une paire de 78,5 jours, non sur une paire quotidienne : 850 est un ordre de grandeur, pas un calendrier.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers de tendance de qualité de [mai](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-05.jsonl), [juillet](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-07.jsonl), [août](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-08.jsonl), [septembre](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-09.jsonl) et [octobre](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl) 2026 (il n'y a pas de fichier pour juin), le script du feeder et l'enregistrement d'évolution dont les liens figurent plus haut. `extract.py` refuse de s'exécuter si l'un de ces fichiers diffère de son blob Git épinglé.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-005/extract.py`, puis `analyze.py` dans le même dossier ; `analyze.py --check` compare une nouvelle exécution aux résultats enregistrés. Le [README](../../../fixtures/psychohistory/psy-005/README.md) énumère chaque fichier, les autocontrôles et les témoins négatifs.

**Références de méthode.** Hyndman, R. J., et Athanasopoulos, G. (2021), *Forecasting: Principles and Practice*, 3e édition, OTexts, [section 5.2](https://otexts.com/fpp3/simple-methods.html) (la prévision naïve, qui est la persistance pour les séries numériques). Jolliffe, I. T., et Stephenson, D. B. (dir.) (2012), *Forecast Verification: A Practitioner's Guide in Atmospheric Science*, 2e édition, Wiley (exactitude et scores de compétence). Murphy, A. H. (1996), « The Finley Affair: A Signal Event in the History of Forecast Verification », *Weather and Forecasting* 11, 3–20. Murphy, A. H. (1993), « What Is a Good Forecast? An Essay on the Nature of Goodness in Weather Forecasting », *Weather and Forecasting* 8, 281–293 (la qualité d'une prévision face à sa valeur pour un utilisateur).

**Non fait.** Aucun modèle de prévision n'a été entraîné ni exécuté ; les quatre modèles sont imaginaires. Aucun intervalle n'a été associé au taux de base (PSY-006 traite des transitions rarement ou jamais observées) et aucune prévision probabiliste n'a été évaluée (PSY-016). L'historique des modifications des enregistrements d'évolution n'a pas été lu. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Compter, dans l'historique Git de `state/evolution/`, combien de fois chaque valeur de vérité a été réexaminée et combien de fois elle a changé. Si les étiquettes ne sont presque jamais réexaminées, la conclusion passe de « cet échantillon ne permet pas de distinguer un modèle compétent de la persistance » à « cette étiquette n'est pas une observable quotidienne », et la question de prévision devrait se reporter sur une grandeur mesurée à chaque exécution.
