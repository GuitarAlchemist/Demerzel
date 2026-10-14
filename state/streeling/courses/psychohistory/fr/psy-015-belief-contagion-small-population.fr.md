---
module_id: psy-015-belief-contagion-small-population
department: psychohistory
course: "Contagion des croyances dans une petite population"
level: intermediate
prerequisites: ["mat-020-markov-chains-hmm", "mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-015
version: "0.1.0"
---

# Contagion des croyances dans une petite population

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous calculerez un nombre de reproduction et son seuil, vous trouverez la taille finale que prédit une courbe épidémique déterministe, vous simulerez le même modèle événement par événement, et vous lirez la distribution dont une trajectoire unique est tirée. **Question de projet :** le département inscrit une « belief state epidemiology ». Si une croyance se répand parmi 14 agents, de combien une trajectoire unique diffère-t-elle de la courbe épidémique déterministe ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit un basculement des étiquettes de croyance comme le signe d'un changement de régime ; ce module demande ce qu'un modèle de propagation peut prévoir. [PSY-004](psy-004-how-large-is-large.fr.md) étudie 14 agents dont les réponses partagent une cause, et PSY-017 la croyance de calibration rencontrée à la section 1.

## 1. Le modèle, et ce que « infecté » signifie ici

**Observé.** L'[enregistrement du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) inscrit, comme septième de dix axes de recherche, « Belief state epidemiology — how beliefs spread across agents and repos », et son principe clé parle de « 14 personas across 4 repos ». [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/extract.py) fige ce que le dépôt consigne au sujet des croyances au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-015/observed-input.json) : les 8 fichiers de croyance actuels de [`state/beliefs/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs) et 13 fichiers archivés. Aucune proposition n'apparaît sous deux détenteurs (0 sur 21), mais ce décompte n'aurait pas pu montrer de partage : les 12 fichiers qui ont du contenu n'ont qu'un évaluateur, la persona de gouvernance Demerzel, et les 9 autres sont des coquilles vides.

Deux fichiers actuels nomment une source extérieure à leur évaluateur : `confidence-calibration` et `remediation-effectiveness` reposent chacun sur un élément de preuve unique, un message `ml-feedback-recommendation` dont [le script qui l'applique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py) recopie la justification et la confiance dans la croyance de Demerzel. Son schéma dit « from an ix ML pipeline to Demerzel » ; les deux messages ne sont pas dans le dépôt, de sorte que l'expéditeur n'est connu que par cette description et par la docstring du script. Chacun est un saut unique, d'un document vers un seul détenteur.

Deux types d'enregistrement sont conçus pour contenir les croyances d'un agent : un [instantané de croyances](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/contracts/belief-snapshot.schema.json) (les croyances d'un agent à un instant donné) et un [état de connaissance](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/knowledge-state.schema.json) (un enseignant, un apprenant, la croyance de l'apprenant avant et après). Sur les 722 fichiers JSON de `state/`, bibliothèque de cours exclue, aucun n'a la forme de l'un ou de l'autre (le test reconnaît bien leurs trois fichiers d'exemple) et aucun n'a de clé nommant un enseignant, un apprenant ou l'expéditeur d'un message (`origin_repo`, `origin_agent`). Sous ces tests, aucun fichier ne consigne un détenteur transmettant une croyance, un deuxième saut, ou un agent exposé sans avoir adopté. Aucun taux ne peut être estimé : tout ce qui suit est donc **synthétique**.

**Analogie.** Dans le modèle SIR de l'épidémiologie, un agent est *susceptible* (S) jusqu'à ce qu'il adopte la croyance, *infecté* (I) tant qu'il la détient et la transmet, et *rétabli* (R) dès qu'il ne la transmet plus. « Infecté » ne veut dire ni faux ni nuisible ; le mot nomme l'état de transmission. Parmi N agents, chaque détenteur transmet la croyance à des agents choisis au hasard au taux β et cesse de transmettre au taux γ :

```text
adoption :              (S, I) -> (S-1, I+1)   au taux beta*S*I/N
arrêt de transmission : (S, I) -> (S, I-1)     au taux gamma*I
R0 = beta/gamma
P(le prochain événement est une adoption) = R0*S / (R0*S + N)
```

Le *nombre de reproduction de base* R0 est le nombre moyen d'agents qu'un détenteur convertit dans une grande population où tous les autres sont susceptibles. La dernière ligne est la *chaîne de sauts incorporée* : elle dit quel événement vient ensuite et ignore quand. La *taille finale*, le nombre d'agents qui ont détenu la croyance à un moment, ne dépend que de cet ordre : [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/analyze.py) ne tire donc aucun temps d'attente.

Hypothèses, dans [`scenarios.json`](../../../fixtures/psychohistory/psy-015/scenarios.json) : N = 14 (l'effectif du principe clé ; PSY-004 trouve 17 fichiers de persona à l'épinglage) et N = 1 400 ; un détenteur initial ; R0 = 0,8, 1,2 et 3.

### Exercice pratique 1

Avec N = 14, R0 = 3 et un détenteur initial, quelle est la probabilité que le premier événement soit une adoption ? Que la croyance ne soit jamais transmise ? Recalculez la seconde pour N = 1 400.

> **Réponse :** Avec S = 13, `3×13 / (3×13 + 14) = 39/53 = 0.7358`. Sinon, le seul détenteur s'arrête d'abord et la croyance s'éteint avec lui : `14/53 = 0.2642`. Pour N = 1 400 : `1,400 / (3×1,399 + 1,400) = 1,400/5,597 = 0.2501`.

## 2. La courbe déterministe et son seuil

Remplaçons les effectifs par des parts s, i, r d'une grande population et les événements aléatoires par leurs taux moyens, le temps étant compté en périodes de détention moyennes (1/γ) :

```text
ds/dt = -R0*s*i        di/dt = R0*s*i - i        dr/dt = i
les détenteurs augmentent tant que R0*s > 1
taille finale z :   1 - z = s0 * exp(-R0*z)
```

C'est la courbe de *champ moyen* : chaque agent ressent la moyenne de tous les autres. À son *seuil*, R0 × s = 1, chaque détenteur est remplacé par exactement un. L'*équation de la taille finale* donne la part z qui détient la croyance à un moment ou l'autre.

**Synthétique.** Pour 14 agents (s0 = 13/14), l'équation donne 3,13 agents à R0 = 0,8, 6,65 à R0 = 1,2 et 13,24 à R0 = 3. À R0 = 3, la courbe intégrée monte à 4,55 détenteurs simultanés après 1,59 période de détention et finit sur les mêmes 13,24 (la vérification à réponse connue). À R0 = 1,2, elle culmine à 1,07 détenteur et finit pourtant à 6,65.

### Exercice pratique 2

Pour N = 14 et un détenteur initial, calculez R0 × S/N au départ pour les trois valeurs de R0. Là où il dépasse 1, après combien d'adoptions les détenteurs cessent-ils d'augmenter ?

> **Réponse :** `0.8 × 13/14 = 0.7429`, `1.2 × 13/14 = 1.1143`, `3 × 13/14 = 2.7857`. À R0 = 0,8, la courbe ne monte jamais. Les détenteurs augmentent tant que S dépasse N/R0 : `14/1.2 = 11.67`, donc la croissance s'arrête dès que S vaut 11, après `13 − 11 = 2` adoptions ; `14/3 = 4.67`, donc dès que S vaut 4, après `13 − 4 = 9`.

## 3. Quatorze agents : la distribution dont vient une trajectoire

**Synthétique.** Nombre de trajectoires par taille finale, sur 10 000 trajectoires pour chaque R0 ([`results.json`](../../../fixtures/psychohistory/psy-015/results.json), section `cases`) :

```text
taille finale  1     2    3    4    5    6    7    8    9   10   11   12    13    14
R0 = 0,8    5708  1553  818  520  364  273  231  176  133  101   65   41    11     6
R0 = 1,2    4706  1253  751  504  451  371  319  302  324  291  261  244   153    70
R0 = 3      2664   606  267  167  124  114  119  112  175  237  414  809  1464  2728
```

- **R0 = 3 a deux bosses.** 2 664 trajectoires ne dépassent jamais le premier détenteur et 4 192 finissent à 13 ou 14. Le 13,24 déterministe se situe dans la bosse haute : 5 001 trajectoires finissent à 12, 13 ou 14, à moins de 1,4 agent (un dixième de la population) de là. La courbe décrit la moitié des trajectoires.
- **La moyenne tombe dans le creux.** Elle vaut 8,38, et les tailles 5 à 8 sont les quatre résultats les plus rares.
- **R0 = 1,2 a une seule bosse, à 1, et un long palier**, comme R0 = 0,8 de l'autre côté du seuil. Seules 992 trajectoires finissent à 6, 7 ou 8, autour du 6,65 déterministe.

**Vérification calculée.** Sommer sur tous les chemins de la même chaîne donne des probabilités exactes sans aucun nombre aléatoire (des fractions à N = 14, des sommes en virgule flottante à N = 1 400). Dans les six cas, les effectifs simulés restent à moins de 2,65 erreurs types de celles-ci, et le test rejette des effectifs simulés avec un autre R0.

### Exercice pratique 3

À partir de la ligne R0 = 3 : quelle part des trajectoires finit avec au plus 2 agents, et avec au moins 12 ? Quelle part finit à 8 ou 9, les entiers qui encadrent la moyenne ? « Environ 8 agents » est-elle une prévision utilisable ?

> **Réponse :** `2,664 + 606 = 3,270` trajectoires, soit 32,70 %. `809 + 1,464 + 2,728 = 5,001` trajectoires, soit 50,01 %. `112 + 175 = 287` trajectoires, soit 2,87 %. Non : les deux extrémités portent `3,270 + 5,001 = 8,271` trajectoires, soit 82,71 %. Pour un résultat à deux bosses, énoncez les deux bosses et leurs parts, non la moyenne.

## 4. Cent fois plus d'agents, et l'objection la plus forte

**Synthétique.** Le même modèle avec N = 1 400. « Près de » signifie à moins d'un dixième de la population de la taille finale déterministe ; une « extinction précoce » finit à un dixième de la population ou en dessous (1 agent sur 14, 140 sur 1 400).

| R0 | Taille finale déterministe | Trajectoires près d'elle | Extinctions précoces |
|---|---|---|---|
| 0,8 | 4,96 | 9 995 | 9 995 |
| 1,2 | 443,03 | 1 097 | 8 455 |
| 3 | 1 316,74 | 6 634 | 3 366 |

**La taille ne supprime pas l'extinction.** À N = 1 400 et R0 = 3, 3 366 trajectoires s'éteignent tôt ; la probabilité exacte vaut 0,3339. Tant que presque tout le monde est susceptible, chaque détenteur convertit indépendamment un nombre aléatoire d'autres agents, de loi géométrique de moyenne R0 parce que la durée de détention est exponentielle. Ce *processus de branchement* s'éteint avec la probabilité 1/R0 quand R0 dépasse 1 : ici 0,3333. Avec une durée de détention fixe, la valeur serait 0,0595 : la part d'extinctions repose donc aussi sur cette hypothèse. À R0 = 1,2, le nombre d'extinctions dépend du seuil de coupure.

**Ce que la taille achète, c'est la séparation.** À N = 1 400 et R0 = 3, aucune trajectoire n'a fini entre 16 et 1 256 agents, et 90 % des 6 634 trajectoires au-dessus de la coupure ont fini entre 1 293 et 1 337 : une fois qu'une trajectoire a décollé, 1 316,74 est une prévision précise. À N = 14, aucun intervalle ne sépare les bosses.

Le risque d'extinction diminue avec le nombre m de détenteurs initiaux : la valeur de branchement est 1/R0 à la puissance m, et les probabilités exactes à N = 1 400 et R0 = 3 valent 0,3339, 0,1117, 0,0374 et 0,0042 pour m = 1, 2, 3 et 5.

### Exercice pratique 4

Calculez la valeur de branchement pour R0 = 3 et m = 1, 2, 3 et 5, et comparez-la aux probabilités exactes ci-dessus. Quel est le plus petit m qui ramène le risque d'extinction précoce sous 5 % ?

> **Réponse :** `1/3 = 0.3333`, `1/9 = 0.1111`, `1/27 = 0.0370` et `1/243 = 0.0041`, proches des valeurs exactes. Trois détenteurs : 0,0374 est sous 0,05, tandis que deux en laissent 0,1117. La taille seule ne suffit pas ; plusieurs détenteurs initiaux, si.

**L'objection la plus forte à cette lecture** est que SIR n'est peut-être pas la bonne famille de modèles. Il lui faut des détenteurs qui convertissent les autres agents un à un. Des personas qui lisent les mêmes fichiers de gouvernance peuvent au contraire acquérir une croyance ensemble, depuis une source commune : une diffusion, sans chaîne, sans nombre de reproduction et sans extinction. Ce qui est consigné penche de ce côté : les deux états de connaissance d'exemple nomment un seul enseignant, la persona dirigeante du département, et les deux adoptions consignées viennent toutes deux d'un document. **Ce jeu d'essai ne permet pas de distinguer la contagion de la diffusion : deux adoptions depuis un document et aucune chaîne sont trop peu pour trancher.** Un relevé de transmission trancherait, avec six éléments par agent et par proposition : qui la détient, ce qu'elle dit, de qui elle est venue, quand elle a été adoptée, quand l'agent a cessé de la transmettre, et qui d'autre y a été exposé sans l'adopter. Le schéma d'état de connaissance a des clés pour quatre d'entre eux et, par son évaluation d'un apprenant à la fois, pour une partie du sixième ; l'instantané de croyances a des clés pour trois ; ni l'un ni l'autre ne consigne le moment où un détenteur s'arrête.

### Exercice pratique 5

Classez chaque énoncé comme observé, synthétique, analogie ou non soutenu, en donnant la raison : (a) deux fichiers de croyance actuels reposent sur un message venu d'une autre chaîne de traitement ; (b) avec R0 = 3, environ un quart des trajectoires parmi 14 agents ne transmettent jamais la croyance ; (c) un agent qui détient une croyance est infecté ; (d) les croyances se répandent parmi les personas du projet avec un R0 supérieur à 1.

> **Réponse :** (a) Observé dans les deux fichiers et dans le script qui les écrit ; l'expéditeur est lu dans la description du schéma, non dans les messages. (b) Synthétique : 2 664 trajectoires sur 10 000 (probabilité exacte 14/53), sous des taux supposés. (c) Analogie : un mot emprunté à l'épidémiologie pour « la détient et la transmet ». (d) Non soutenu : aucun fichier lu ici ne consigne un détenteur transmettant une croyance à un autre agent, de sorte que R0 ne peut pas être estimé ; le relevé à six éléments le rendrait observable.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** `extract.py` refuse de s'exécuter si l'un de ses 32 fichiers, ou l'un des deux dossiers qu'il énumère (722 fichiers JSON sous `state/`, 11 schémas de contrat), diffère de l'épinglage. `results.json` énumère les 42 autovérifications ; le [README](../../../fixtures/psychohistory/psy-015/README.md) donne les commandes et les contrôles.

**Références de méthode.** Kermack, W. O., et McKendrick, A. G. (1927), « A Contribution to the Mathematical Theory of Epidemics », *Proceedings of the Royal Society of London, Series A* 115, 700–721 (modèle déterministe, seuil, taille finale). Bailey, N. T. J. (1975), *The Mathematical Theory of Infectious Diseases and its Applications*, 2e édition, Griffin. Whittle, P. (1955), « The Outcome of a Stochastic Epidemic: A Note on Bailey's Paper », *Biometrika* 42, 116–122 (les flambées mineures et 1/R0).

**Non fait.** Aucun taux n'a été estimé à partir de données du projet : les trois valeurs de R0 sont supposées. Seule la taille finale a été simulée, et seul un mélange uniforme : pas de réseau, pas d'agents inégaux, pas de seconde adoption. Les tests de forme et de clés portent sur les fichiers JSON sous `state/` ; au-delà d'un fichier de croyance YAML (sans évaluateur ; 10 de ses 49 éléments de preuve citent `GPT-4o`), aucun YAML, aucun Markdown et aucun autre dépôt n'ont été lus. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Tenir le relevé à six éléments pour une poignée de propositions. Si la plupart des adoptions nomment un document ou un enseignant unique comme source, remplacer ce modèle par un modèle de diffusion. Si elles nomment d'autres agents, estimer R0 d'après les adoptions par détenteur et comparer les tailles finales observées à la section 3.
