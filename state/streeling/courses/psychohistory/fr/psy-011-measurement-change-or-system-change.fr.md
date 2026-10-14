---
module_id: psy-011-measurement-change-or-system-change
department: psychohistory
course: "Changement de mesure ou changement de système ? Les rebaselines dans la tendance de qualité"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-005-persistence-baseline"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-011
version: "0.1.0"
---

# Changement de mesure ou changement de système ? Les rebaselines dans la tendance de qualité

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous lirez comment un nombre est produit avant de lire sa série, vous trouverez un changement d'instrument dans un journal, vous rangerez chaque saut dans « début de mesure », « changement d'instrument » ou « même instrument », et vous montrerez ce qu'une règle d'alerte fait quand les trois sont mêlés. **Question de projet :** la tendance de qualité comporte des lignes marquées `rebaseline` et un champ `citation_source` qui apparaît en cours de route ; lesquels des sauts de la série sont l'instrument qui change plutôt que le système ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit un changement rapide d'un indicateur de gouvernance comme le signe d'un basculement de régime qui approche. Cette lecture suppose que l'indicateur était produit de la même façon avant et après ; ce module met l'hypothèse à l'épreuve sur la colonne des citations du journal présenté par [PSY-005](psy-005-persistence-baseline.fr.md). [PSY-012](psy-012-early-warning-false-alarms.fr.md) traite des indicateurs d'alerte précoce.

## 1. Lire l'instrument avant la série

Un *instrument* est toute la procédure qui transforme le monde en un nombre consigné : qui ou quoi compte, ce qui est compté, et où. Un *changement de système* est un changement de la chose comptée.

**Observé, dans le code épinglé.** Une [tâche quotidienne](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) lance le *feeder* (l'alimenteur), [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), qui ajoute une ligne par *artefact* de gouvernance (une politique, un schéma, une compétence) dans `state/quality-trend/` ; un lancement est une *exécution*. Le `citation_count` d'une ligne est [recopié de l'enregistrement d'évolution de l'artefact](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L75-L76), un fichier JSON de `state/evolution/`. Depuis septembre 2026, un second script, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), calcule ce nombre comme les ["tracked files that mention any of the artifact's citation paths (`git grep -lF`)"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) et [marque l'enregistrement](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L104-L107) d'un `citation_source: "git-grep-v1"`. Avant cela, dit sa docstring, chaque métrique ["was typed by hand"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) et « nothing updated it afterwards ».

Le feeder réagit à la marque aux [lignes 90 à 92](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L90-L92) et à la [ligne 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), où `prev` est la ligne précédente de l'artefact :

```text
prev = previous.get(artifact, {})
source = metrics.get("citation_source")
rebaseline = bool(prev) and prev.get("citation_source") != source
"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),
```

Trois conséquences :

1. Un *rebaseline* (une remise à la base) est déclaré lorsqu'une ligne précédente existe et que son étiquette de source diffère de l'étiquette actuelle ; une clé absente se lit comme nulle.
2. Le changement consigné, `delta_citations`, vaut alors 0, tandis que [`citation_count` est écrit tel qu'il a été lu](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L96) : le saut reste dans `citation_count`.
3. Sans ligne précédente, ou avec une ligne sans effectif, le feeder soustrait 0 : le « changement » est l'effectif tout entier.

La docstring du feeder donne l'intention : ["the jump is a change of measurement, not a change in citations"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L14-L18).

**Calculé.** [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/analyze.py) réimplémente cette règle sur l'instantané que prend [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/extract.py). Il reproduit `delta_citations` dans les 1 537 lignes qui ont un effectif et les 576 marques consignées, avec 0 écart.

### Exercice pratique 1

Lignes **synthétiques** tirées de [`scenarios.json`](../../../fixtures/psychohistory/psy-011/scenarios.json). Donnez la marque et le `delta_citations` que la règle écrit : (a) la première ligne d'un artefact, effectif 9 ; (b) ligne précédente à 12 sans source, maintenant 27 depuis `git-grep-v1` ; (c) ligne précédente à 6 et maintenant 19, les deux en `git-grep-v1`, après que quelqu'un a ajouté un chemin aux `citation_paths` de l'enregistrement. Lequel des cas est un changement d'instrument que la règle ne peut pas voir ?

> **Réponse :** (a) Aucune ligne précédente : pas de marque, delta 9, un début de mesure consigné comme une hausse. (b) Marque, delta 0 ; le pas de 15 ne survit que dans `citation_count`. (c) Pas de marque, delta 13, le cas que la règle ne peut pas voir : la liste des chemins fait partie de l'instrument, mais l'étiquette n'a pas changé, de sorte que la modification est consignée comme 13 nouvelles citations.

## 2. Localiser le changement dans le relevé

**Observé** dans [`observed-input.json`](../../../fixtures/psychohistory/psy-011/observed-input.json) : 1 548 lignes en 88 exécutions pour 18 artefacts. La première exécution, horodatée du 2026-05-01, porte 11 *lignes d'amorçage* sans effectif ; 87 exécutions du feeder suivent. La clé `citation_source` est absente des 56 premières exécutions (972 lignes) et présente dans les 32 dernières. Elle apparaît pour la première fois au 2026-09-13T17:52:14Z, où 16 lignes portent `git-grep-v1` et `rebaseline: true`. Les 2 autres lignes ont une source nulle et aucune marque : leurs artefacts ont une liste `citation_paths` vide, ce qui [désigne un artefact extérieur au dépôt](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23), et conservent leurs 55 et 0 saisis à la main. Aucune autre ligne n'est marquée.

**Calculé.** Chacun des 16 artefacts portait une valeur saisie à la main dans toutes ses lignes antérieures. Cette exécution l'a remplacée :

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

Les pas vont de −7 à +60 et le rapport de la nouvelle à l'ancienne valeur de 0 à 27 (indéfini pour une ancienne valeur de 0) : aucun facteur de conversion unique ne relie les deux instruments.

### Exercice pratique 2

À partir du tableau, calculez la somme des 16 effectifs avant et après, et le pas. Ajoutez les deux artefacts non marqués pour obtenir le total sur les 18 et son rapport. Combien d'effectifs ont baissé ? À combien se montait la somme des `delta_citations` dans cette exécution ?

> **Réponse :** Avant `61`, après `351`, pas `351 − 61 = 290`. Sur les 18 artefacts : `61 + 55 + 0 = 116` avant et `351 + 55 + 0 = 406` après, soit un rapport de `406 / 116 = 3.5`. Deux effectifs ont baissé (de 8 à 1 et de 1 à 0). Les lignes marquées ont un delta de 0 et les deux autres n'ont pas bougé : la somme des `delta_citations` vaut donc 0 dans l'exécution où le total a crû de 290.

## 3. Ranger chaque saut

« Lignes dont le `delta_citations` est non nul » et « lignes dont l'effectif diffère de celui de la ligne précédente » sonnent comme un seul ensemble. Chacun compte 20 lignes ; 4 seulement sont dans les deux. Classer chaque ligne face à la ligne précédente de l'artefact montre pourquoi (**calculé**, [`results.json`](../../../fixtures/psychohistory/psy-011/results.json)) :

| Classe de ligne | Lignes | Effectif changé | Delta non nul |
|---|---|---|---|
| Premier effectif : aucun effectif antérieur auquel se comparer | 18 | indéfini | 16 |
| Changement d'instrument : la ligne précédente a une autre source | 16 | 16 | 0 |
| Même instrument : la ligne précédente a la même source | 1 503 | 4 | 4 |

Les 16 deltas non nuls de la première classe sont des niveaux, non des changements : 10 suivent une ligne d'amorçage, 6 sont la première ligne d'un artefact, et leur somme vaut 116. Restent 4 lignes, toutes dans l'exécution du 2026-10-03T15:31:16Z, chacune d'un pas de +2.

Sur les 1 503 paires de lignes consécutives d'un même artefact à instrument constant, 1 007 n'ont de source dans aucune des deux lignes (la période de saisie à la main et les deux artefacts extérieurs) et comptent 0 changement. Un nombre que personne ne retape ne peut pas bouger : ce zéro dit donc que l'instrument était muet, non que le système était immobile. Sous `git-grep-v1` : 496 paires, et les 4 changements.

Le même partage s'applique à la somme sur les artefacts, passée de 106 à la première exécution du feeder à 414 à la dernière : `308 = 10 + 290 + 8`, c'est-à-dire les premiers effectifs d'artefacts ajoutés plus tard, le changement d'instrument, et les pas à instrument constant. Seul le dernier est *comparable à l'identique* : même instrument, même ensemble d'artefacts.

### Exercice pratique 3

En partant de 1 548 lignes et 18 artefacts, déduisez le nombre de paires à instrument constant et la part de celles qui ont changé. Donnez ensuite la part de la croissance du total qui a été mesurée à l'identique.

> **Réponse :** `1,548 − 18 = 1,530` paires de lignes. Retirez les 11 qui partent d'une ligne d'amorçage et les 16 qui traversent le changement de source : `1,530 − 11 − 16 = 1,503`. Changées : `4 / 1,503 = 0.27%`. Croissance : `8 / 308 = 2.60%` ; le reste est un nouvel instrument (290) ou de nouveaux artefacts (10).

## 4. Fixer la mesure avant de lire un basculement

Le premier signal de PSY-002 est un taux de variation « exceeding 2 standard deviations from its running mean », énoncé pour son indice de cristallisation, non pour les citations. Comme **choix d'analyse** consigné dans `scenarios.json`, appliquons une règle de cette forme au pas d'une exécution à la suivante de l'effectif de citations sommé sur les artefacts : marquer un pas qui s'écarte de la moyenne de tous les pas antérieurs (au moins 3) de plus de 2 de leurs écarts-types de population. Les exécutions du feeder sont espacées de 122 secondes à 6,45 jours ; la même règle sur les pas par jour marque les mêmes exécutions. **Calculé** sur trois versions de la série :

| Série | Pas marqués | Le +8 du 2026-10-03 |
|---|---|---|
| `citation_count` sommé | +2 et +8 le 2026-07-29, +290 le 2026-09-13 | non marqué |
| `delta_citations` sommé | +2 et +8 le 2026-07-29 | marqué |
| Pas à instrument constant seuls | aucun antérieur | marqué |

Sur la somme brute, la règle lève trois alertes et aucune n'est un changement à l'identique : deux sont des artefacts qui entrent dans la somme, une est le nouvel instrument. Celle-ci gonfle aussi l'écart-type glissant, de sorte que le seul pas comparable à l'identique passe inaperçu. En gardant tous les pas antérieurs, un changement d'instrument coûte deux fois : une fausse alerte au moment où il survient, et un aveuglement ensuite. Prudence sur la dernière ligne : après un historique tout à zéro, n'importe quel pas non nul est marqué.

### Exercice pratique 4

À l'exécution du 2026-10-03, les 75 pas antérieurs ont une moyenne de 4 et un écart-type de 33,2602 dans la somme brute, et une moyenne de 0,1333 et un écart-type de 0,9428 dans le `delta_citations` sommé. Pour chaque série, calculez le bord supérieur de la bande (moyenne plus 2 écarts-types) et le plus petit pas entier qui serait marqué.

> **Réponse :** Somme brute : `4 + 2 × 33.2602 = 70.5204`, donc +8 est à l'intérieur de la bande et le plus petit pas marqué est 71. Deltas sommés : `0.1333 + 2 × 0.9428 = 2.0189`, donc +8 est marqué et le plus petit pas marqué est 3. Un seul changement d'instrument a déplacé le seuil de détection de 3 à 71.

**L'objection la plus forte à cette lecture** est que « même instrument » repose sur une étiquette, et l'exercice 1(c) montre un changement d'instrument qui conserve son étiquette : les quatre pas restants pourraient être un tel changement. Le jeu d'essai répond : les quatre enregistrements d'évolution partagent un même instant `last_cited`, 2026-10-02T20:05:16Z, situé entre l'exécution précédente et celle du pas, et deux des quatre artefacts mesurent le même chemin : quatre lignes, au plus trois effectifs indépendants. Lu en dehors du jeu d'essai, dans l'historique Git jusqu'à l'épinglage : le script producteur n'a qu'un seul commit, et entre les deux exécutions seul le commit de la tâche quotidienne elle-même a touché `state/evolution/`, donc personne n'a modifié le code ni une liste de chemins ; le commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642), fait à ce même instant, a ajouté les traductions française et espagnole de 13 modules de cours ; et pour chaque chemin de citation des quatre artefacts, exactement deux fichiers ajoutés entre les deux exécutions le citent à l'épinglage, les deux traductions d'une même leçon. C'est compatible avec un changement de la chose comptée, et un petit : trois leçons ont été traduites.

### Exercice pratique 5

Un tableau de bord rapporte « les citations ont été multipliées par environ 3,9 depuis juillet (de 106 à 414) » comme preuve d'un basculement de régime. Acceptez ou rejetez, énoncez votre critère, et nommez deux relevés qui rendraient lisible un basculement futur.

> **Réponse :** Rejeter. Critère : deux effectifs ne peuvent être comparés que si le même instrument a produit les deux, pour le même ensemble d'artefacts. Sur les 308, 290 viennent d'un nouvel instrument et 10 d'artefacts ajoutés à la somme ; 8 satisfont le critère, tous dans une seule exécution. Deux relevés utiles : une étiquette de source qui change dès que le script, sa liste d'exclusions ou une liste `citation_paths` change ; et, à chaque changement, les deux instruments exécutés côte à côte pendant plusieurs exécutions, pour que le recouvrement mesure la différence.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers JSONL de [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), les deux scripts dont les liens figurent plus haut et les 18 enregistrements `*.evolution.json` de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution). Le [README](../../../fixtures/psychohistory/psy-011/README.md) du jeu d'essai donne les commandes, les autovérifications et les contrôles négatifs.

**Références de méthode.** Shadish, W. R., Cook, T. D., et Campbell, D. T. (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin (l'*instrumentation* comme menace pour la validité).

**Non fait.** L'effectif `git grep` n'a pas été recalculé pour les exécutions antérieures au 2026-09-13 : rien ici ne dit donc si les citations ont bougé alors. Les versions antérieures du feeder n'ont pas été lues. Les affirmations tirées de l'historique Git reposent sur des commandes énumérées dans la note de relecture, non sur le jeu d'essai. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Recalculer l'effectif `git-grep-v1` au commit de chacune des exécutions antérieures. Un seul instrument sous les 87 exécutions du feeder montrerait si quelque chose a bougé avant septembre ; si c'est le cas, la conclusion passe de « presque rien n'a bougé » à « le mouvement n'a pas été mesuré ».

**Empreinte propre.** Ce module écrit les noms d'artefacts comme des étiquettes aux barres obliques espacées, de sorte qu'aucun de ses fichiers ne contient le chemin de citation d'un artefact : exécutée sur eux avec chacun des chemins, la recherche littérale de la section 1 (`git grep -lF`) ne trouve rien. PSY-020 reprend la question générale.
