---
module_id: psy-006-transition-matrix-from-counts
department: psychohistory
course: "Estimer une matrice de transition à partir de comptages observés"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "mat-020-markov-chains-hmm"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-006
version: "0.1.0"
---

# Estimer une matrice de transition à partir de comptages observés

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un journal d'étiquettes en une matrice de comptages, vous en estimerez des probabilités de transition, vous bornerez une transition qui n'a jamais été observée, et vous direz ce que le lissage et une matrice uniforme ajoutent aux données. **Question de projet :** le dépôt stocke une matrice de transition de gouvernance uniforme à 4 états, sans aucune observation ; à quoi ressemble une matrice estimée à partir des transitions d'étiquettes dont nous disposons, et que ne peut-elle pas dire ?

[PSY-005](psy-005-persistence-baseline.fr.md) a évalué la prévision « rien ne change » sur ces étiquettes ; le présent module borne la probabilité de changement que cette évaluation laissait ouverte. Les lois stationnaires et les temps d'atteinte viennent de [MAT-020](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-020-markov-chains-hmm.md).

## 1. Compter les transitions, puis diviser

**Observé.** Une tâche quotidienne lance [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), le *feeder* (l'alimenteur) : il ajoute une ligne par *artefact* de gouvernance (une politique, un schéma, une compétence) dans [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), et les lignes d'un même lancement forment une *exécution*. Chaque ligne porte `effectiveness_to`, la valeur de vérité attribuée à une proposition écrite portant sur l'artefact : T (vrai), P (probable), U (inconnu), D (douteux), F (faux) ou C (contradictoire). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/extract.py) fige les cinq fichiers au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-006/observed-input.json) : 1 548 lignes, 88 exécutions, 18 artefacts.

Une *transition* est une paire de lignes consécutives, comme dans PSY-005 : l'étiquette d'un artefact dans une ligne et dans sa ligne suivante. Cela donne 1 548 − 18 = 1 530 paires de lignes ; l'une d'elles part d'une ligne sans étiquette, ce qui en laisse **1 529**. La *matrice de comptages* contient le nombre de paires allant de chaque étiquette (ligne) vers chaque étiquette (colonne) :

```text
de \ vers     T     P     U     D     F     C   paires
T           775     0     0     0     0     0      775
P             0   406     0     0     0     0      406
U             0     0   174     0     1     0      175
D             0     0     0     0     0     0        0
F             0     0     0     0    86     0       86
C             0     0     0     0     0    87       87
```

**Calculé.** Traitons les étiquettes comme une *chaîne de Markov* : l'étiquette suivante ne dépend que de l'étiquette actuelle, par l'intermédiaire d'une matrice fixe de probabilités, la même pour tous les artefacts. L'*estimation par maximum de vraisemblance*, la matrice qui rend les paires observées les plus probables, s'obtient en divisant chaque ligne de comptages par son total (Anderson et Goodman 1957) :

```text
estimation p(a→b) = n_ab / n_a      n_ab = paires de a vers b, n_a = paires partant de a
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/analyze.py) l'écrit dans [`results.json`](../../../fixtures/psychohistory/psy-006/results.json) : 1 sur la diagonale pour T, P, F et C, 174/175 = 0,994286 pour U→U et 1/175 = 0,005714 pour U→F. Prise à la lettre, la matrice dit que quatre étiquettes ne changent jamais et qu'une étiquette inconnue attend en moyenne 175 paires, puis devient toujours fausse. Tout cela repose sur une seule paire.

Une matrice correspond en outre à une seule longueur de pas, et ces paires en mélangent au moins deux. Parmi elles, 1 518 paires relient deux exécutions consécutives du feeder (écarts de 0,001 à 6,453 jours, médiane 0,999). Les 11 autres partent d'une *ligne d'amorçage* (marquée `baseline: true`, horodatée du 2026-05-01) et aboutissent à la première exécution du feeder, 78,5 jours plus tard ; l'unique changement, de U à F, est l'une d'elles. Entre exécutions du feeder, l'estimation est la matrice identité sur cinq étiquettes.

### Exercice pratique 1

À partir de la matrice de comptages, estimez la ligne U. Quelle est l'estimation pour la ligne D ? Que devient la ligne U sur les 1 518 paires entre exécutions du feeder, où elle compte 172 paires et aucune sortie ?

> **Réponse :** `174 / 175 = 0.994286` pour U→U, `1 / 175 = 0.005714` pour U→F, 0 ailleurs. La ligne D vaut `0 / 0`, indéfinie : les données sont muettes, ce qui n'est pas une estimation nulle. Entre exécutions du feeder, la ligne vaut `172 / 172 = 1` pour U→U : la seule estimation hors diagonale de la matrice vient d'une paire de 78,5 jours.

## 2. Borner ce qui n'a jamais été observé

Un comptage nul ne rend pas une probabilité nulle. Si une transition a la probabilité p à chacun de n essais indépendants, elle reste inobservée (le relevé est alors *vierge*) avec la probabilité (1 − p)^n. La *borne supérieure* est le plus grand p qu'un relevé vierge ne rejette pas au seuil de 5 % :

```text
(1 − p)^n = 0.05   →   borne supérieure exacte à 95% = 1 − 0.05^(1/n)
règle de trois : environ 3 / n, car −ln 0.05 = 2.9957
```

La *règle de trois* des statisticiens (*rule of three*) est le raccourci décrit par Hanley et Lippman-Hand (1983). **Calculé** pour la sortie de chaque étiquette, une paire comptant pour un essai :

| Étiquette quittée | Paires sans sortie | Borne exacte | 3/n |
|---|---|---|---|
| T | 775 | 0,386 % | 0,387 % |
| P | 406 | 0,735 % | 0,739 % |
| C | 87 | 3,385 % | 3,448 % |
| F | 86 | 3,423 % | 3,488 % |
| toute étiquette, entre exécutions du feeder | 1 518 | 0,197 % | 0,198 % |

La ligne U compte une sortie sur 175 paires ; sa borne, 2,682 %, est le p pour lequel « au plus une sortie sur 175 paires » a une probabilité de 0,05 (Clopper et Pearson 1934). La ligne D n'a aucun essai, donc aucune borne inférieure à 100 %. La règle de trois dépasse la borne exacte de 1,9 % de cette borne à 86 paires, et de 15,9 % à 10 essais.

Les bornes sont unilatérales ([PSY-004](psy-004-how-large-is-large.fr.md) et [PSY-013](psy-013-four-scores-and-a-trend.fr.md) utilisent l'intervalle bilatéral, 0,025 dans chaque queue) et prises une ligne à la fois ; leur niveau conjoint est inférieur à 95 %. **L'objection la plus forte** porte sur le mot « indépendants ». Une étiquette est une évaluation écrite qui ne change que lorsque son enregistrement est modifié, et une même séance peut couvrir de nombreux artefacts. À un extrême de la dépendance entre artefacts, où les étiquettes d'une exécution changent toutes ensemble ou pas du tout, une exécution est un seul essai : les 86 pas entre exécutions du feeder bornent alors la probabilité de changement à 3,423 % par paire, et non à 0,197 %. Si au contraire l'étiquette de chaque artefact est une seule évaluation, les essais sont les artefacts : la ligne T en a neuf, les lignes F et C une chacune ; 0 artefact sur 9 a quitté T, soit une borne de 28,313 % sur l'ensemble du relevé, et un seul artefact ne donne aucune borne inférieure à 95 %. Cet échantillon ne permet pas de situer la vérité ; l'historique des modifications de `state/evolution/`, où les évaluations sont écrites, montrerait comment les étiquettes sont révisées.

### Exercice pratique 2

Calculez la borne exacte et la règle de trois pour la sortie de F (86 paires, aucune sortie). Un collègue conclut que « F est définitif ». Qu'est-ce que les données étayent ?

> **Réponse :** `1 − 0.05^(1/86) = 0.034234` et `3 / 86 = 0.034884`. Les données étayent « la probabilité de quitter F en une paire est inférieure à 3,423 %, au niveau de confiance de 95 %, si les 86 paires sont des essais indépendants », et non « F est définitif ». Les 86 paires sont un seul artefact lu lors de 87 exécutions consécutives : comptées comme une seule évaluation, elles ne donnent aucune borne inférieure à 95 %.

## 3. Lisser, c'est poser un a priori, et un a priori est une affirmation

Le *lissage de Laplace* (*add-one smoothing*) ajoute un pseudo-comptage de 1 à chaque case avant la division, pour qu'aucune estimation ne soit nulle :

```text
estimation lissée p(a→b) = (n_ab + 1) / (n_a + k)      k = nombre d'étiquettes, ici 6
```

C'est la moyenne des matrices encore plausibles au vu des données lorsque, avant de les voir, on tenait tous les jeux de probabilités d'une ligne pour également plausibles : une *loi a priori uniforme*. **Calculé :**

- Ligne D, aucune paire : chaque destination reçoit 1/6. Sans données, le lissage de Laplace renvoie la ligne uniforme.
- Ligne U parmi les 11 paires issues des lignes d'amorçage (2 restent, 1 passe à F) : le maintien tombe de 2/3 à (2 + 1)/(3 + 6) = 1/3, et 4/9 de la probabilité se répartissent sur quatre destinations jamais observées.
- Ligne T, 775 paires : la sortie reçoit 5/781 = 0,64 %, au-dessus de la borne de 0,386 %.

Pour toute ligne vierge de 5 à 2 000 paires, le lissage de Laplace sur six étiquettes prête à la ligne plus de sorties qu'elle n'en admet au niveau de 95 % ; un pseudo-comptage de 0,5 ne le fait jamais dans cette plage. Ce sont les pseudo-comptages placés sur les cinq sorties, 5 ou 2,5 contre 3 pour la règle, qui en décident, et non les données.

**Observé.** Le dépôt contient une table d'amorçage sur ces six lettres : la machine `belief_hexavalent` de [`state/driver/transition-weights.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L22). Elle maintient T avec un poids de 0,9 et [classe U→F parmi les transitions interdites](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L49). **Calculé sous une hypothèse que le fichier n'énonce pas**, à savoir qu'un pas de la table correspond à une paire : la table attend en moyenne 492,4 changements d'étiquette parmi les 1 518 paires entre exécutions du feeder, où il n'y en a eu aucun. L'unique changement enregistré, U→F, est un saut que la table interdit en un pas (0,0825 en deux, en passant par D ou par C) ; une paire de 78,5 jours ne peut pas montrer combien de pas elle a couverts. Une matrice de comptages presque vide peut donc tout de même écarter un candidat, pour une longueur de pas donnée. Lu comme un a priori, un zéro est l'inverse de l'excès du lissage de Laplace : aucune quantité de données ne peut le relever.

### Exercice pratique 3

Appliquez le lissage de Laplace sur six étiquettes à la ligne F (86 paires, toutes F→F) : donnez les probabilités lissées de maintien et de sortie, et comparez la seconde à la borne de l'exercice 2.

> **Réponse :** Maintien : `(86 + 1) / (86 + 6) = 87/92 = 0.945652`. Chaque autre étiquette reçoit `1/92`, donc la sortie reçoit `5/92 = 0.054348`, soit 5,435 %, au-dessus de la borne de 3,423 % : la ligne lissée affirme plus de changement que ses propres 86 paires n'en admettent au niveau de 95 %.

## 4. Ce qu'affirme la matrice uniforme stockée

**Observé.** [`state/markov/transition-matrix.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/transition-matrix.json) comporte quatre états, Healthy, Watch, Warning et Freeze, et 0,25 dans chaque case ; sa note commence par « Uniform prior — no observations yet. » (a priori uniforme, pas encore d'observations). [`predictions.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/predictions.json) contient une liste vide, et le fichier `engine-state.json` que nomme la note ne se trouve pas dans le dossier. La [spécification](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L29) attribue l'un des quatre états à chaque cycle de gouvernance pris dans son ensemble, à partir d'un score de résilience et d'un ratio d'inflation des artefacts (LOLLI/ERGOL) seulement.

**Calculé.** C'est à nouveau la ligne D : le lissage de Laplace sans données, avec k = 4. Toutes les lignes étant égales, l'état suivant ne dépend pas de l'état actuel. Depuis Healthy, un Freeze a une probabilité de 0,25 au cycle suivant, de 0,578125 en 3 cycles au plus et de 0,943686 en 10 ; l'attente moyenne avant le premier Freeze est de 4 cycles, et à long terme un quart des cycles sont en Freeze. La formule de la spécification, [`cycles_to_freeze = log(0.5) / log(P(not_freeze))`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L151), donne 2,409 cycles pour P(not_freeze) = 0,75 (le moment où la probabilité d'un Freeze atteint la moitié, et non l'attente moyenne), tandis que son [alerte](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L168), déclenchée « When P(Freeze) > 0.3 » (quand P(Freeze) dépasse 0,3), reste muette.

**Synthétique.** [`scenarios.json`](../../../fixtures/psychohistory/psy-006/scenarios.json) définit une matrice imaginaire « persistante » qui conserve chaque état avec la probabilité 0,97 et répartit le reste à parts égales. Sa loi stationnaire est la même, et pourtant un Freeze en 10 cycles au plus a une probabilité de 0,095618 et l'attente moyenne est de 100 cycles. Les proportions de long terme n'identifient pas une matrice ; la matrice uniforme est le membre sans mémoire de cette famille, une affirmation précise et non une position neutre.

**Deux espaces d'états.** Les étiquettes décrivent 18 artefacts ; les états de gouvernance décrivent le système entier, un par cycle. Aucune étiquette n'entre dans cette classification, si bien que les comptages d'étiquettes ne disent rien de Healthy→Freeze. Un état enregistré à chaque cycle le dirait : 59 transitions depuis Healthy, aucune vers Freeze, ramèneraient la borne sur cette transition à 5 %. Aucun n'est enregistré : le journal des prédictions est vide.

### Exercice pratique 4

En partant de Healthy, calculez la probabilité d'un Freeze en 3 cycles au plus et l'attente moyenne avant le premier Freeze, sous la matrice stockée et sous la matrice persistante (chaque autre état : 0,01).

> **Réponse :** Matrice stockée : chaque cycle est un Freeze avec la probabilité 0,25, donc `1 − 0.75^3 = 37/64 = 0.578125`, et l'attente vaut `1 / 0.25 = 4` cycles. Matrice persistante : depuis tout autre état, un Freeze a la probabilité 0,01, donc `1 − 0.99^3 = 0.029701` et `1 / 0.01 = 100` cycles.

### Exercice pratique 5

Un coéquipier veut remplir la matrice de gouvernance à partir de la matrice des étiquettes : « les étiquettes ne changent presque jamais, donc Healthy reste Healthy ». Acceptez ou rejetez, en énonçant votre critère. Combien de cycles consécutifs sans Freeze rejetteraient la valeur stockée de 0,25 au seuil de 5 % ?

> **Réponse :** À rejeter. Un comptage ne vaut preuve que pour l'espace d'états et le pas dans lesquels il a été fait : les étiquettes sont des valeurs de vérité de 18 artefacts, les états de gouvernance classent le système entier une fois par cycle, et la spécification classe un cycle sans aucune étiquette. `0.75^10 = 0.056314` est au-dessus de 0,05 et `0.75^11 = 0.042235` en dessous : 11 cycles consécutifs sans Freeze.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers de tendance de qualité, deux des trois fichiers de `state/markov/`, la spécification et la table d'amorçage dont les liens figurent plus haut. Le [README](../../../fixtures/psychohistory/psy-006/README.md) du jeu d'essai donne les commandes et les contrôles.

**Références de méthode.** Anderson, T. W., et Goodman, L. A. (1957), « Statistical Inference about Markov Chains », *Annals of Mathematical Statistics* 28(1), 89–110, [doi:10.1214/aoms/1177707039](https://doi.org/10.1214/aoms/1177707039). Hanley, J. A., et Lippman-Hand, A. (1983), « If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators », *JAMA* 249(13), 1743–1745, [doi:10.1001/jama.1983.03330370053031](https://doi.org/10.1001/jama.1983.03330370053031). Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).

**Non fait.** Aucun état de gouvernance n'a été classé, si bien que rien n'a été testé de la matrice à 4 états, bien que les entrées du classificateur aient été enregistrées quelques fois : [quatre scores de résilience](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json), que lit PSY-013, et [un ratio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json). L'hypothèse de Markov et la constance de la matrice dans le temps n'ont pas été testées : un seul changement ne donne rien sur quoi les tester. L'évaluation de prévisions probabilistes sur ces étiquettes relève de [PSY-016](../en/psy-016-brier-score.md). Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Comparer les blocs `assessment` au fil de l'historique Git de `state/evolution/` pour compter combien de fois chaque valeur de vérité a été réexaminée. Si ce n'est qu'une poignée de fois, les bornes par paire cèdent la place à des bornes par évaluation bien plus larges, et la matrice identité de la section 1 enregistre des fichiers non révisés, et non des artefacts stables.
