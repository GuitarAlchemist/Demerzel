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

Vous calculerez un nombre de reproduction et son seuil, vous trouverez la taille finale que prédit une courbe épidémique déterministe, vous simulerez le même modèle un événement à la fois, et vous lirez la loi dont une simulation isolée est tirée. **Question de projet :** le département compte parmi ses domaines la « belief state epidemiology » (épidémiologie des états de croyance). Si une croyance se propage parmi 14 agents, dans quelle mesure une simulation s'écarte-t-elle de la courbe épidémique déterministe ?

[PSY-002](psy-002-governance-phase-transitions.fr.md) lit un déplacement des étiquettes de croyance comme le signe d'un changement de régime ; ce module demande ce qu'un modèle de propagation peut prévoir. [PSY-004](psy-004-how-large-is-large.fr.md) étudie 14 agents dont les réponses ont une cause commune, et [PSY-017](psy-017-calibration-with-six-observations.fr.md) la croyance sur la calibration rencontrée à la section 1.

## 1. Le modèle, et ce que signifie ici « infecté »

**Observé.** La [fiche du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) mentionne, comme domaine de recherche 7 sur 10, « Belief state epidemiology — how beliefs spread across agents and repos » (comment les croyances se propagent entre agents et dépôts), et son principe clé parle de « 14 personas across 4 repos ». [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/extract.py) fige ce que le dépôt enregistre sur les croyances au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-015/observed-input.json) : les 8 fichiers de croyances actuels de [`state/beliefs/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs) et 13 fichiers archivés. Aucune proposition n'apparaît chez deux porteurs (0 sur 21), mais ce décompte n'aurait pas pu montrer un partage : les 12 fichiers qui ont un contenu ont un seul évaluateur, le persona de gouvernance Demerzel, et les 9 autres sont des squelettes vides.

Deux fichiers actuels nomment une source extérieure à leur évaluateur : `confidence-calibration` et `remediation-effectiveness` reposent chacun sur un seul élément de preuve, un message `ml-feedback-recommendation` dont [le script qui l'applique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py) recopie la justification et le niveau de confiance dans la croyance de Demerzel. Le schéma de ce message dit « from an ix ML pipeline to Demerzel » (d'une chaîne de traitement ML d'ix vers Demerzel) ; les deux messages ne sont pas dans le dépôt, si bien que l'expéditeur n'est connu que par cette description et par la docstring du script. Chacun de ces deux cas ne compte qu'un maillon, d'un document vers un seul porteur.

Deux types d'enregistrement sont conçus pour contenir les croyances d'un agent : l'[instantané de croyances](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/contracts/belief-snapshot.schema.json) (les croyances d'un agent à un instant donné) et l'[état de connaissance](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/knowledge-state.schema.json) (un enseignant, un apprenant, la croyance de l'apprenant avant et après). Sur les 722 fichiers JSON sous `state/`, bibliothèque de cours exclue, aucun n'a la forme de l'un ou de l'autre (le test reconnaît bien leurs trois fichiers d'exemple) et aucun n'a de clé désignant un enseignant, un apprenant ou l'expéditeur d'un message (`origin_repo`, `origin_agent`). Selon ces tests, aucun fichier n'enregistre un porteur qui transmet une croyance, un second maillon, ni un agent exposé qui ne l'a pas adoptée. Aucun taux ne peut être estimé : tout ce qui suit est donc **synthétique**.

**Analogie.** Dans le modèle SIR de l'épidémiologie, un agent est *susceptible* (S) jusqu'à ce qu'il adopte la croyance, *infecté* (I) tant qu'il la détient et la transmet, et *rétabli* (R) dès qu'il ne la transmet plus. « Infecté » ne veut dire ni erroné ni nuisible : le mot désigne l'état de transmission. Parmi N agents, chaque porteur transmet la croyance à des agents tirés au hasard, au taux β, et cesse de la transmettre au taux γ :

```text
adoption :                  (S, I) -> (S-1, I+1)   au taux beta*S*I/N
arrêt de la transmission :  (S, I) -> (S, I-1)     au taux gamma*I
R0 = beta/gamma
P(l'événement suivant est une adoption) = R0*S / (R0*S + N)
```

Le *nombre de reproduction de base* R0 est le nombre moyen d'agents qu'un porteur convertit dans une grande population où tous les autres sont susceptibles. La dernière ligne est la *chaîne des sauts* (*embedded jump chain*) : elle dit quel événement vient ensuite, sans dire quand. La *taille finale*, c'est-à-dire le nombre d'agents qui ont détenu la croyance à un moment ou à un autre, ne dépend que de cet ordre ; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-015/analyze.py) ne tire donc aucun temps d'attente.

Hypothèses, dans [`scenarios.json`](../../../fixtures/psychohistory/psy-015/scenarios.json) : N = 14 (le nombre du principe clé ; PSY-004 trouve 17 fichiers de personas au commit épinglé) et N = 1 400 ; un seul porteur initial ; R0 égal à 0,8, à 1,2 ou à 3.

### Exercice pratique 1

Avec N = 14, R0 = 3 et un seul porteur initial, quelle est la probabilité que le premier événement soit une adoption ? Que la croyance ne soit jamais transmise ? Recalculez la seconde pour N = 1 400.

> **Réponse :** Avec S = 13, `3×13 / (3×13 + 14) = 39/53 = 0.7358`. Sinon, l'unique porteur s'arrête le premier et la croyance s'éteint avec lui : `14/53 = 0.2642`. Pour N = 1 400 : `1,400 / (3×1,399 + 1,400) = 1,400/5,597 = 0.2501`.

## 2. La courbe déterministe et son seuil

Remplaçons les effectifs par les proportions s, i, r d'une grande population, et les événements aléatoires par leurs taux moyens, en comptant le temps en durées moyennes de portage (1/γ) :

```text
ds/dt = -R0*s*i        di/dt = R0*s*i - i        dr/dt = i
le nombre de porteurs augmente tant que R0*s > 1
taille finale z :   1 - z = s0 * exp(-R0*z)
```

C'est la courbe de *champ moyen* : chaque agent ressent l'effet moyen de tous les autres. À son *seuil*, R0 × s = 1, chaque porteur est remplacé par exactement un autre. L'*équation de la taille finale* donne la proportion z de la population qui détient la croyance à un moment ou à un autre.

**Synthétique.** Pour 14 agents (s0 = 13/14), l'équation donne 3,13 agents à R0 = 0,8, 6,65 à R0 = 1,2 et 13,24 à R0 = 3. À R0 = 3, la courbe intégrée monte jusqu'à 4,55 porteurs simultanés au bout de 1,59 durée moyenne de portage et se termine aux mêmes 13,24 (c'est la vérification sur réponse connue). À R0 = 1,2, elle culmine à 1,07 porteur et se termine pourtant à 6,65.

### Exercice pratique 2

Pour N = 14 et un seul porteur initial, calculez R0 × S/N au départ pour les trois valeurs de R0. Là où ce produit dépasse 1, au bout de combien d'adoptions le nombre de porteurs cesse-t-il d'augmenter ?

> **Réponse :** `0.8 × 13/14 = 0.7429`, `1.2 × 13/14 = 1.1143`, `3 × 13/14 = 2.7857`. À R0 = 0,8, la courbe ne monte jamais. Le nombre de porteurs augmente tant que S dépasse N/R0 : `14/1.2 = 11.67`, donc la croissance s'arrête dès que S vaut 11, après `13 − 11 = 2` adoptions ; `14/3 = 4.67`, donc dès que S vaut 4, après `13 − 4 = 9`.

## 3. Quatorze agents : la loi dont une simulation est tirée

**Synthétique.** Nombre de simulations pour chaque taille finale, sur 10 000 simulations par valeur de R0 ([`results.json`](../../../fixtures/psychohistory/psy-015/results.json), section `cases`) :

```text
taille finale  1     2    3    4    5    6    7    8    9   10   11   12    13    14
R0 = 0.8    5708  1553  818  520  364  273  231  176  133  101   65   41    11     6
R0 = 1.2    4706  1253  751  504  451  371  319  302  324  291  261  244   153    70
R0 = 3      2664   606  267  167  124  114  119  112  175  237  414  809  1464  2728
```

- **À R0 = 3, la loi a deux bosses.** 2 664 simulations ne dépassent jamais le premier porteur et 4 192 se terminent à 13 ou 14. La valeur déterministe 13,24 se trouve dans la bosse haute : 5 001 simulations se terminent à 12, 13 ou 14, à moins de 1,4 agent (un dixième de la population) de cette valeur. La courbe décrit la moitié des simulations.
- **La moyenne tombe dans le creux.** Elle vaut 8,38, et les tailles 5 à 8 sont les quatre issues les plus rares.
- **À R0 = 1,2, une seule bosse, à 1, et un long plateau**, comme à R0 = 0,8 de l'autre côté du seuil. Seules 992 simulations se terminent à 6, 7 ou 8, autour de la valeur déterministe 6,65.

**Vérification calculée.** En sommant sur tous les chemins de la même chaîne, on obtient les probabilités exactes sans aucun nombre aléatoire (des fractions à N = 14, des sommes en virgule flottante à N = 1 400). Dans les six cas, les décomptes simulés restent à moins de 2,65 erreurs types de ces probabilités, et le test rejette des décomptes simulés avec un autre R0.

### Exercice pratique 3

D'après la ligne R0 = 3 : quelle part des simulations se termine avec au plus 2 agents, et quelle part avec au moins 12 ? Quelle part se termine à 8 ou 9, les entiers qui encadrent la moyenne ? « Environ 8 agents » : est-ce une prévision utilisable ?

> **Réponse :** `2,664 + 606 = 3,270` simulations, soit 32,70 %. `809 + 1,464 + 2,728 = 5,001` simulations, soit 50,01 %. `112 + 175 = 287` simulations, soit 2,87 %. Non : les deux extrémités regroupent `3,270 + 5,001 = 8,271` simulations, soit 82,71 %. Pour une issue à deux bosses, donnez les deux bosses et leurs parts, pas la moyenne.

## 4. Cent fois plus d'agents, et l'objection la plus forte

**Synthétique.** Le même modèle avec N = 1 400. « Proche » signifie à moins d'un dixième de la population de la taille finale déterministe ; une « extinction précoce » s'arrête à un dixième de la population ou moins (1 agent sur 14, 140 sur 1 400).

| R0 | Taille finale déterministe | Simulations proches | Extinctions précoces |
|---|---|---|---|
| 0,8 | 4,96 | 9 995 | 9 995 |
| 1,2 | 443,03 | 1 097 | 8 455 |
| 3 | 1 316,74 | 6 634 | 3 366 |

**La taille ne supprime pas l'extinction précoce.** À N = 1 400 et R0 = 3, 3 366 simulations s'éteignent précocement ; la probabilité exacte est de 0,3339. Tant que presque tout le monde est susceptible, chaque porteur convertit indépendamment un nombre aléatoire d'autres agents : la loi de descendance est géométrique, de moyenne R0, parce que la durée de portage est exponentielle. Ce *processus de branchement* s'éteint avec la probabilité 1/R0 quand R0 dépasse 1 : ici 0,3333. Avec une durée de portage fixe, la valeur serait 0,0595 : la part des extinctions précoces repose donc aussi sur cette hypothèse. À R0 = 1,2, le nombre d'extinctions précoces dépend du seuil choisi.

**Ce que la taille apporte, c'est la séparation.** À N = 1 400 et R0 = 3, aucune simulation ne s'est terminée entre 16 et 1 256 agents, et 90 % des 6 634 simulations au-dessus du seuil se sont terminées entre 1 293 et 1 337 : une fois qu'une simulation a décollé, 1 316,74 est une prévision précise. À N = 14, aucun vide ne sépare les bosses.

Le risque d'extinction précoce diminue avec le nombre m de porteurs initiaux : la valeur du processus de branchement est 1/R0 élevé à la puissance m, et les probabilités exactes à N = 1 400 et R0 = 3 sont 0,3339 ; 0,1117 ; 0,0374 et 0,0042 pour m = 1, 2, 3 et 5.

### Exercice pratique 4

Calculez la valeur du processus de branchement pour R0 = 3 et m = 1, 2, 3 et 5, et comparez-la aux probabilités exactes ci-dessus. Quel est le plus petit m qui ramène le risque d'extinction précoce sous 5 % ?

> **Réponse :** `1/3 = 0.3333`, `1/9 = 0.1111`, `1/27 = 0.0370` et `1/243 = 0.0041`, proches des valeurs exactes. Trois porteurs : 0,0374 est inférieur à 0,05, alors que deux laissent 0,1117. La taille seule ne suffit pas ; plusieurs porteurs initiaux, si.

**L'objection la plus forte à cette lecture** est que le modèle SIR appartient peut-être à la mauvaise famille de modèles. Il suppose des porteurs qui convertissent les autres agents un par un. Des personas qui lisent les mêmes fichiers de gouvernance peuvent au contraire acquérir une croyance ensemble, à partir d'une source commune : c'est une diffusion, sans chaîne, sans nombre de reproduction et sans extinction précoce. Ce qui est enregistré penche dans ce sens : les deux états de connaissance d'exemple désignent un seul enseignant, le persona qui dirige le département, et les deux adoptions enregistrées viennent toutes deux d'un document. **Ce jeu d'essai ne permet pas de distinguer la contagion de la diffusion : deux adoptions issues d'un document et aucune chaîne, c'est trop peu pour trancher.** Un registre des transmissions trancherait, avec six éléments par agent et par proposition : qui la détient, ce qu'elle dit, de qui elle vient, quand elle a été adoptée, quand l'agent a cessé de la transmettre, et qui d'autre y a été exposé sans l'adopter. Le schéma des états de connaissance a des clés pour quatre d'entre eux et, par son évaluation d'un apprenant à la fois, pour une partie du sixième ; l'instantané de croyances en a pour trois ; aucun des deux n'enregistre le moment où un porteur s'arrête.

### Exercice pratique 5

Classez chaque énoncé comme observé, synthétique, analogie ou non étayé, en donnant la raison : (a) deux fichiers de croyances actuels reposent sur un message venu d'une autre chaîne de traitement ; (b) avec R0 = 3, dans environ un quart des simulations à 14 agents, la croyance n'est jamais transmise ; (c) un agent qui détient une croyance est infecté ; (d) les croyances se propagent parmi les personas du projet avec un R0 supérieur à 1.

> **Réponse :** (a) Observé, dans les deux fichiers et dans le script qui les écrit ; l'expéditeur est lu dans la description du schéma, non dans les messages. (b) Synthétique : 2 664 simulations sur 10 000 (probabilité exacte 14/53), sous des taux supposés. (c) Analogie : un mot emprunté à l'épidémiologie pour « la détient et la transmet ». (d) Non étayé : aucun fichier lu ici n'enregistre un porteur qui transmet une croyance à un autre agent, si bien que R0 ne peut pas être estimé ; le registre à six éléments le rendrait observable.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** `extract.py` refuse de s'exécuter si l'un de ses 32 fichiers, ou l'un des deux dossiers qu'il liste (722 fichiers JSON sous `state/`, 11 schémas de contrat), diffère de la version épinglée. `results.json` énumère les 42 autocontrôles ; le [README](../../../fixtures/psychohistory/psy-015/README.md) donne les commandes et les témoins.

**Références de méthode.** Kermack, W. O., et McKendrick, A. G. (1927), « A Contribution to the Mathematical Theory of Epidemics », *Proceedings of the Royal Society of London, Series A* 115, 700–721 (modèle déterministe, seuil, taille finale). Bailey, N. T. J. (1975), *The Mathematical Theory of Infectious Diseases and its Applications*, 2e édition, Griffin. Whittle, P. (1955), « The Outcome of a Stochastic Epidemic: A Note on Bailey's Paper », *Biometrika* 42, 116–122 (épidémies mineures et 1/R0).

**Non fait.** Aucun taux n'a été estimé à partir des données du projet : les trois valeurs de R0 sont supposées. Seule la taille finale a été simulée, et seulement sous mélange homogène : pas de réseau, pas d'agents inégaux, pas de seconde adoption. Les tests de forme et de clés portent sur les fichiers JSON sous `state/` ; hormis un fichier de croyances YAML (sans évaluateur ; 10 de ses 49 éléments de preuve citent `GPT-4o`), aucun fichier YAML ou Markdown n'a été lu, ni aucun autre dépôt. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Tenir le registre à six éléments pour une poignée de propositions. Si la plupart des adoptions désignent comme source un document ou un enseignant unique, remplacer ce modèle par un modèle de diffusion. Si elles désignent d'autres agents, estimer R0 à partir des adoptions par porteur et comparer les tailles finales observées à celles de la section 3.
