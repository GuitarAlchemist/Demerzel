---
module_id: psy-011-measurement-change-or-system-change
department: psychohistory
course: "Changement de mesure ou changement du système ? Les rebaselines de la tendance de qualité"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-005-persistence-baseline"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-011
version: "0.1.0"
---

# Changement de mesure ou changement du système ? Les rebaselines de la tendance de qualité

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous lirez comment un nombre est produit avant de lire sa série, vous repérerez un changement d'instrument dans un journal, vous rangerez chaque saut dans l'une des classes « début de mesure », « changement d'instrument » ou « même instrument », et vous montrerez ce que fait une règle d'alerte quand les trois sont mélangées. **Question de projet :** la tendance de qualité contient des lignes marquées `rebaseline` et un champ `citation_source` qui apparaît en cours de route ; quels sauts de la série traduisent un changement de l'instrument plutôt que du système ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) voit dans un changement rapide d'un indicateur de gouvernance le signe d'un changement de régime à venir. Cette lecture suppose que l'indicateur a été produit de la même façon avant et après ; ce module met cette hypothèse à l'épreuve sur la colonne des citations du journal que [PSY-005](psy-005-persistence-baseline.fr.md) a présenté. [PSY-012](psy-012-early-warning-false-alarms.fr.md) traite des indicateurs d'alerte précoce.

## 1. Lire l'instrument avant la série

Un *instrument* est toute la procédure qui transforme le monde en un nombre enregistré : qui ou quoi compte, ce qui est compté, et où. Un *changement du système* est un changement de la chose comptée.

**Observé, dans le code épinglé.** Une [tâche quotidienne](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) lance le *feeder* (l'alimenteur), [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), qui ajoute à `state/quality-trend/` une ligne par *artefact* de gouvernance (une politique, un schéma, une compétence) ; un lancement est une *exécution*. Le `citation_count` d'une ligne est [recopié de l'enregistrement d'évolution de l'artefact](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L75-L76), un fichier JSON de `state/evolution/`. Depuis septembre 2026, un second script, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), calcule ce nombre comme les [« tracked files that mention any of the artifact's citation paths (`git grep -lF`) »](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) (les fichiers suivis qui mentionnent l'un des chemins de citation de l'artefact) et [estampille l'enregistrement](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L104-L107) avec `citation_source: "git-grep-v1"`. Auparavant, dit sa docstring, chaque métrique [« was typed by hand »](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) (était saisie à la main) et « nothing updated it afterwards » (rien ne la mettait à jour ensuite).

Le feeder réagit à cette estampille aux [lignes 90 à 92](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L90-L92) et à la [ligne 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), où `prev` est la ligne précédente de l'artefact :

```text
prev = previous.get(artifact, {})
source = metrics.get("citation_source")
rebaseline = bool(prev) and prev.get("citation_source") != source
"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),
```

Il en découle trois choses :

1. Une *rebaseline* (redéfinition de la valeur de référence) est déclarée quand une ligne précédente existe et que son étiquette de source diffère de l'étiquette actuelle ; une clé absente se lit comme nulle.
2. La variation enregistrée, `delta_citations`, vaut alors 0, tandis que [`citation_count` est écrit tel qu'il a été lu](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L96) : le saut reste dans `citation_count`.
3. Sans ligne précédente, ou avec une ligne précédente sans nombre de citations, le feeder soustrait 0 : la « variation » est le nombre de citations tout entier.

La docstring du feeder en donne l'intention : [« the jump is a change of measurement, not a change in citations »](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L14-L18) (le saut est un changement de mesure, non un changement des citations).

**Calculé.** [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/analyze.py) réimplémente cette règle sur l'instantané que prend [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/extract.py). Il reproduit `delta_citations` dans les 1 537 lignes qui portent un nombre de citations et les 576 valeurs de marque enregistrées, avec 0 discordance.

### Exercice pratique 1

Lignes **synthétiques** tirées de [`scenarios.json`](../../../fixtures/psychohistory/psy-011/scenarios.json). Donnez la marque et le `delta_citations` qu'écrit la règle : (a) la première ligne d'un artefact, nombre de citations 9 ; (b) une ligne précédente à 12 sans source, puis 27 avec `git-grep-v1` ; (c) une ligne précédente à 6, puis 19, toutes deux en `git-grep-v1`, après que quelqu'un a ajouté un chemin aux `citation_paths` de l'enregistrement. Quel cas est un changement d'instrument que la règle ne peut pas voir ?

> **Réponse :** (a) Pas de ligne précédente : pas de marque, delta 9, un début de mesure enregistré comme une hausse. (b) Marque, delta 0 ; le saut de 15 ne survit que dans `citation_count`. (c) Pas de marque, delta 13 : c'est le cas que la règle ne peut pas voir. La liste des chemins fait partie de l'instrument, mais l'étiquette n'a pas changé, si bien que la modification est enregistrée comme 13 nouvelles citations.

## 2. Situer le changement dans le relevé

**Observé** dans [`observed-input.json`](../../../fixtures/psychohistory/psy-011/observed-input.json) : 1 548 lignes en 88 exécutions pour 18 artefacts. La première exécution, horodatée du 2026-05-01, contient 11 *lignes d'amorçage* sans nombre de citations ; suivent 87 exécutions du feeder. La clé `citation_source` est absente des 56 premières exécutions (972 lignes) et présente dans les 32 dernières. Elle apparaît pour la première fois le 2026-09-13T17:52:14Z, où 16 lignes portent `git-grep-v1` et `rebaseline: true`. Les 2 autres lignes ont une source nulle et pas de marque : leurs artefacts ont une liste `citation_paths` vide, ce qui [signale un artefact extérieur au dépôt](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23), et gardent leurs valeurs saisies à la main, 55 et 0. Aucune autre ligne n'est marquée.

**Calculé.** Chacun des 16 artefacts avait la même valeur saisie à la main dans toutes ses lignes antérieures. Cette exécution l'a remplacée :

| Artefact (barres obliques espacées) | Saisi à la main | `git grep` |
|---|---|---|
| `constitutions / asimov.constitution.md` | 5 | 65 |
| `contracts / galactic-protocol.md` | 2 | 43 |
| `policies / alignment-policy.yaml` | 3 | 42 |
| `constitutions / default.constitution.md` | 11 | 47 |
| `skills / demerzel-drive + policies / autonomous-loop-policy v1.1.0` | 1 | 27 |
| `logic / tetravalent-state.schema.json` | 4 | 23 |
| `logic / governance-evolution.schema.json` | 2 | 17 |
| `policies / autonomous-loop-policy.yaml` | 12 | 27 |
| `afk-graduated-self-merge` | 1 | 14 |
| `schemas / loop-state.schema.json` | 3 | 15 |
| `logic / kaizen-pdca-state.schema.json` | 3 | 13 |
| `scripts / afk_backends /` | 0 | 6 |
| `ml-feedback-loop` | 1 | 6 |
| `meta / compounding-cycle` | 4 | 5 |
| `docs / governance / the-sentinel-spec.md` | 1 | 0 |
| `docs / governance / harness-engineering-direction.md` | 8 | 1 |

Les sauts vont de −7 à +60, et le rapport de la nouvelle valeur à l'ancienne de 0 à 27 (indéfini pour une ancienne valeur de 0) : aucun facteur de conversion unique ne relie les deux instruments.

### Exercice pratique 2

À partir du tableau, calculez la somme des 16 nombres avant et après, et le saut. Ajoutez les deux artefacts non marqués pour obtenir le total sur les 18 et son rapport. Combien de nombres ont baissé ? Quelle était la somme des `delta_citations` dans cette exécution ?

> **Réponse :** Avant `61`, après `351`, saut `351 − 61 = 290`. Sur les 18 artefacts : `61 + 55 + 0 = 116` avant et `351 + 55 + 0 = 406` après, soit un rapport de `406 / 116 = 3.5`. Deux nombres ont baissé (de 8 à 1 et de 1 à 0). Les lignes marquées ont un delta de 0 et les deux autres n'ont pas bougé : la somme des `delta_citations` vaut donc 0 dans l'exécution où le total a augmenté de 290.

## 3. Classer chaque saut

« Lignes dont le `delta_citations` est non nul » et « lignes dont le nombre de citations diffère de celui de la ligne précédente » ont l'air de désigner un même ensemble. Chacun contient 20 lignes ; 4 seulement sont dans les deux. Classer chaque ligne par rapport à la ligne précédente de l'artefact montre pourquoi (**calculé**, [`results.json`](../../../fixtures/psychohistory/psy-011/results.json)) :

| Classe de ligne | Lignes | Nombre modifié | Delta non nul |
|---|---|---|---|
| Premier nombre : aucun nombre antérieur auquel le comparer | 18 | indéfini | 16 |
| Changement d'instrument : la ligne précédente a une autre source | 16 | 16 | 0 |
| Même instrument : la ligne précédente a la même source | 1 503 | 4 | 4 |

Les 16 deltas non nuls de la première classe sont des niveaux, non des variations : 10 suivent une ligne d'amorçage, 6 sont la première ligne d'un artefact, et leur somme vaut 116. Restent 4 lignes, toutes dans l'exécution du 2026-10-03T15:31:16Z, chacune avec une variation de +2.

Sur les 1 503 paires de lignes consécutives d'un même artefact relevées avec le même instrument, 1 007 n'ont de source dans aucune des deux lignes (la période de saisie à la main et les deux artefacts extérieurs) et comptent 0 changement. Un nombre que personne ne ressaisit ne peut pas bouger : ce zéro dit que l'instrument était muet, non que le système était immobile. Sous `git-grep-v1` : 496 paires, et les 4 changements.

La même décomposition s'applique à la somme sur les artefacts, passée de 106 à la première exécution du feeder à 414 à la dernière : `308 = 10 + 290 + 8`, c'est-à-dire les premiers nombres d'artefacts ajoutés plus tard, le changement d'instrument, et les variations à instrument constant. Seule la dernière part est *à données comparables* : même instrument, même ensemble d'artefacts.

### Exercice pratique 3

En partant de 1 548 lignes et de 18 artefacts, établissez le nombre de paires à instrument constant et la part de celles qui ont changé. Donnez ensuite la part de la croissance du total mesurée à données comparables.

> **Réponse :** `1,548 − 18 = 1,530` paires de lignes. Retirez les 11 qui partent d'une ligne d'amorçage et les 16 qui franchissent le changement de source : `1,530 − 11 − 16 = 1,503`. Ont changé : `4 / 1,503 = 0.27%`. Croissance : `8 / 308 = 2.60%` ; le reste vient d'un nouvel instrument (290) ou de nouveaux artefacts (10).

## 4. Garder la mesure fixe avant de lire un basculement

Le premier signal de PSY-002 est un taux de variation « exceeding 2 standard deviations from its running mean » (qui s'écarte de plus de deux écarts-types de sa moyenne glissante), énoncé pour son indice de cristallisation, non pour les citations. Par un **choix d'analyse** consigné dans `scenarios.json`, appliquez une règle de cette forme à la variation, d'une exécution à la suivante, du nombre de citations sommé sur les artefacts : signalez une variation qui s'écarte de la moyenne de toutes les variations antérieures (au moins 3) de plus de 2 fois leur écart-type de population. Les exécutions du feeder sont espacées de 122 secondes à 6,45 jours ; la même règle appliquée aux variations par jour signale les mêmes exécutions. **Calculé** sur trois versions de la série :

| Série | Variations signalées | Le +8 du 2026-10-03 |
|---|---|---|
| Somme des `citation_count` | +2 et +8 le 2026-07-29, +290 le 2026-09-13 | non signalé |
| Somme des `delta_citations` | +2 et +8 le 2026-07-29 | signalé |
| Variations à instrument constant seulement | aucune auparavant | signalé |

Sur la somme brute, la règle déclenche trois alertes, et aucune n'est un changement à données comparables : deux viennent d'artefacts qui entrent dans la somme, une du nouvel instrument. Cette dernière gonfle aussi l'écart-type courant, si bien que la seule variation à données comparables passe inaperçue. Tant qu'on garde toutes les variations antérieures, un changement d'instrument coûte deux fois : une fausse alerte au moment où il survient, et l'aveuglement ensuite. Prudence pour la dernière ligne : après un historique entièrement nul, toute variation non nulle est signalée.

### Exercice pratique 4

À l'exécution du 2026-10-03, les 75 variations antérieures ont une moyenne de 4 et un écart-type de 33,2602 dans la somme brute, et une moyenne de 0,1333 et un écart-type de 0,9428 dans la somme des `delta_citations`. Pour chaque série, calculez le bord supérieur de la bande (moyenne plus 2 écarts-types) et la plus petite variation entière qui serait signalée.

> **Réponse :** Somme brute : `4 + 2 × 33.2602 = 70.5204`, donc +8 reste dans la bande et la plus petite variation signalée est 71. Somme des deltas : `0.1333 + 2 × 0.9428 = 2.0189`, donc +8 est signalé et la plus petite variation signalée est 3. Un seul changement d'instrument a fait passer le seuil de détection de 3 à 71.

**L'objection la plus forte à cette lecture** est que « même instrument » repose sur une étiquette, et l'exercice 1(c) montre un changement d'instrument qui garde son étiquette : les quatre variations restantes pourraient être un tel changement. Le jeu d'essai dit ceci : les quatre enregistrements d'évolution partagent un même instant `last_cited`, 2026-10-02T20:05:16Z, situé entre l'exécution précédente et celle de la variation, et deux des quatre artefacts mesurent le même chemin : quatre lignes, au plus trois nombres indépendants. Hors du jeu d'essai, dans l'historique Git jusqu'au commit épinglé : le script producteur n'a qu'un seul commit, et entre les deux exécutions seul le commit de la tâche quotidienne elle-même a touché `state/evolution/`, si bien que personne n'a modifié le code ni une liste de chemins ; le commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642), fait à ce même instant, a ajouté les traductions française et espagnole de 13 modules de cours ; et chaque chemin de citation des quatre artefacts est cité, au commit épinglé, par exactement deux fichiers ajoutés entre les deux exécutions, les deux traductions d'une même leçon. C'est compatible avec un changement de la chose comptée, et un changement modeste : trois des 13 modules traduits citent ces chemins.

### Exercice pratique 5

Un tableau de bord présente « citations multipliées par environ 3,9 depuis juillet (de 106 à 414) » comme l'indice d'un changement de régime. Acceptez ou rejetez, énoncez votre critère, et nommez deux enregistrements qui rendraient lisible un futur changement de régime.

> **Réponse :** Rejeter. Critère : deux nombres ne peuvent être comparés que si le même instrument les a produits tous deux, pour le même ensemble d'artefacts. Sur les 308, 290 viennent d'un nouvel instrument et 10 d'artefacts ajoutés à la somme ; 8 satisfont au critère, tous dans une même exécution. Deux enregistrements utiles : une étiquette de source qui change chaque fois que changent le script, sa liste d'exclusion ou une liste `citation_paths` ; et, à chaque changement, les deux instruments exécutés côte à côte pendant plusieurs exécutions, pour que le recouvrement mesure l'écart.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers JSONL de [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), les deux scripts dont les liens figurent plus haut et les 18 enregistrements `*.evolution.json` de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution). Le [README](../../../fixtures/psychohistory/psy-011/README.md) du jeu d'essai donne les commandes, les autocontrôles et les témoins négatifs.

**Références de méthode.** Shadish, W. R., Cook, T. D., et Campbell, D. T. (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin (l'*instrumentation* comme menace pour la validité).

**Non fait.** Le décompte par `git grep` n'a pas été recalculé pour les exécutions antérieures au 2026-09-13 : rien ici ne dit donc si les citations ont bougé à cette époque. Les versions antérieures du feeder n'ont pas été lues. Les affirmations tirées de l'historique Git reposent sur des commandes énumérées dans le dossier de relecture, non sur le jeu d'essai. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Recalculer le décompte `git-grep-v1` au commit de chaque exécution antérieure. Un seul instrument sous les 87 exécutions du feeder montrerait si quelque chose a bougé avant septembre ; si c'est le cas, la conclusion passe de « presque rien n'a bougé » à « le mouvement n'a pas été mesuré ».

**Empreinte propre.** Ce module écrit les noms d'artefacts sous forme d'étiquettes aux barres obliques espacées, si bien qu'aucun de ses fichiers ne contient le chemin de citation d'un artefact : lancée sur eux avec chaque chemin, la recherche littérale de la section 1 (`git grep -lF`) ne trouve rien. [PSY-020](../en/psy-020-goodhart-and-reflexivity.md) reprend la question générale.
