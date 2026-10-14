---
module_id: psy-006-transition-matrix-from-counts
department: psychohistory
course: "Estimer une matrice de transition à partir d'effectifs observés"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "mat-020-markov-chains-hmm"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-006
version: "0.1.0"
---

# Estimer une matrice de transition à partir d'effectifs observés

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un journal d'étiquettes en une matrice d'effectifs, vous en estimerez des probabilités de transition, vous bornerez une transition jamais observée, et vous direz ce que le lissage et une matrice uniforme ajoutent aux données. **Question de projet :** le dépôt conserve une matrice de transition de gouvernance uniforme à 4 états, sans aucune observation ; à quoi ressemble une matrice estimée à partir des transitions d'étiquettes dont nous disposons, et que ne peut-elle pas dire ?

[PSY-005](psy-005-persistence-baseline.fr.md) a évalué la prévision « rien ne change » sur ces étiquettes ; ce module borne la probabilité de changement qu'elle laissait ouverte. Les distributions stationnaires et les temps d'atteinte viennent de [MAT-020](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-020-markov-chains-hmm.md).

## 1. Compter les transitions, puis diviser

**Observé.** Une tâche quotidienne lance [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), le *feeder* (l'alimenteur) : il ajoute une ligne par *artefact* de gouvernance (une politique, un schéma, une compétence) dans [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), et les lignes d'un même lancement forment une *exécution*. Chaque ligne porte un `effectiveness_to`, la valeur de vérité attribuée à une proposition écrite portant sur l'artefact : T (vrai), P (probable), U (inconnu), D (douteux), F (faux) ou C (contradictoire). [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/extract.py) fige les cinq fichiers au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-006/observed-input.json) : 1 548 lignes, 88 exécutions, 18 artefacts.

Une *transition* est une paire de lignes consécutives, comme dans PSY-005 : l'étiquette d'un artefact dans une ligne et dans sa ligne suivante. Cela donne 1 548 − 18 = 1 530 paires de lignes ; l'une d'elles part d'une ligne sans étiquette, ce qui en laisse **1 529**. La *matrice d'effectifs* contient le nombre de paires allant de chaque étiquette (ligne) à chaque étiquette (colonne) :

```text
de \ vers     T     P     U     D     F     C   paires
T           775     0     0     0     0     0      775
P             0   406     0     0     0     0      406
U             0     0   174     0     1     0      175
D             0     0     0     0     0     0        0
F             0     0     0     0    86     0       86
C             0     0     0     0     0    87       87
```

**Calculé.** Traitons les étiquettes comme une *chaîne de Markov* : l'étiquette suivante ne dépend que de l'étiquette actuelle, par une matrice de probabilités fixe, la même pour tous les artefacts. L'*estimation du maximum de vraisemblance*, la matrice qui rend les paires observées les plus probables, est chaque ligne d'effectifs divisée par son total (Anderson et Goodman 1957) :

```text
estimation p(a→b) = n_ab / n_a      n_ab = paires de a vers b, n_a = paires partant de a
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-006/analyze.py) l'écrit dans [`results.json`](../../../fixtures/psychohistory/psy-006/results.json) : 1 sur la diagonale pour T, P, F et C, 174/175 = 0,994286 pour U→U et 1/175 = 0,005714 pour U→F. Lue littéralement, la matrice dit que quatre étiquettes ne changent jamais et qu'une étiquette inconnue attend 175 paires en moyenne, puis devient toujours fausse. Tout cela repose sur une seule paire.

Une matrice appartient en outre à un pas de temps donné, et ces paires en mélangent au moins deux. 1 518 paires relient deux exécutions consécutives du feeder (écarts de 0,001 à 6,453 jours, médiane 0,999). Les 11 autres partent d'une *ligne d'amorçage* (marquée `baseline: true`, horodatée du 2026-05-01) et aboutissent à la première exécution du feeder, 78,5 jours plus tard ; l'unique changement, U vers F, en fait partie. Entre exécutions du feeder, l'estimation est la matrice identité sur cinq étiquettes.

### Exercice pratique 1

À partir de la matrice d'effectifs, estimez la ligne U. Quelle est l'estimation pour la ligne D ? Que devient la ligne U sur les 1 518 paires entre exécutions du feeder, où elle compte 172 paires et aucune sortie ?

> **Réponse :** `174 / 175 = 0.994286` pour U→U, `1 / 175 = 0.005714` pour U→F, 0 ailleurs. La ligne D vaut `0 / 0`, indéfinie : les données se taisent, ce qui n'est pas une estimation de zéro. Entre exécutions du feeder, la ligne vaut `172 / 172 = 1` pour U→U : la seule estimation hors diagonale de la matrice provient d'une paire de 78,5 jours.

## 2. Borner ce qui n'a jamais été observé

Un effectif nul ne rend pas une probabilité nulle. Une transition de probabilité p à chacun de n essais indépendants reste invisible — un relevé *vierge* — avec la probabilité (1 − p)^n. La *borne supérieure* est le plus grand p qu'un relevé vierge ne rejette pas au seuil de 5 % :

```text
(1 − p)^n = 0.05   →   borne supérieure exacte à 95 % = 1 − 0.05^(1/n)
règle de trois : environ 3 / n, car −ln 0.05 = 2.9957
```

La *règle de trois* est le raccourci décrit par Hanley et Lippman-Hand (1983). **Calculé** pour la sortie de chaque étiquette, une paire comptant pour un essai :

| Étiquette quittée | Paires vierges | Borne exacte | 3/n |
|---|---|---|---|
| T | 775 | 0,386 % | 0,387 % |
| P | 406 | 0,735 % | 0,739 % |
| C | 87 | 3,385 % | 3,448 % |
| F | 86 | 3,423 % | 3,488 % |
| toute étiquette, entre exécutions du feeder | 1 518 | 0,197 % | 0,198 % |

La ligne U a une sortie en 175 paires ; sa borne, 2,682 %, est le p auquel « au plus une sortie en 175 paires » a la probabilité 0,05 (Clopper et Pearson 1934). La ligne D n'a aucun essai, donc aucune borne inférieure à 100 %. La règle de trois dépasse la borne exacte de 1,9 % de cette borne à 86 paires et de 15,9 % à 10 essais.

Les bornes sont unilatérales ([PSY-004](psy-004-how-large-is-large.fr.md) et [PSY-013](psy-013-four-scores-and-a-trend.fr.md) emploient l'intervalle bilatéral, 0,025 dans chaque queue) et prises une ligne à la fois ; ensemble, elles tiennent à moins de 95 %. **L'objection la plus forte** porte sur le mot « indépendants ». Une étiquette est une évaluation écrite qui ne change que lorsque son enregistrement est modifié, et une même séance peut couvrir plusieurs artefacts. À un extrême de la dépendance entre artefacts, où les étiquettes d'une exécution changent toutes ensemble ou pas du tout, une exécution vaut un essai : les 86 pas entre exécutions du feeder bornent alors la probabilité de changement à 3,423 % par paire, et non 0,197 %. Si au contraire l'étiquette de chaque artefact est une évaluation, les essais sont les artefacts : la ligne T en compte neuf, les lignes F et C une chacune ; 0 sortie sur 9 pour T, soit une borne de 28,313 % sur tout le relevé, et un seul artefact ne donne aucune borne inférieure à 95 %. Cet échantillon ne permet pas de situer la vérité ; l'historique des modifications de `state/evolution/`, où les évaluations sont écrites, montrerait comment les étiquettes sont révisées.

### Exercice pratique 2

Calculez la borne exacte et la règle de trois pour la sortie de F (86 paires, aucune sortie). Un collègue en conclut que « F est définitif ». Que soutiennent les données ?

> **Réponse :** `1 − 0.05^(1/86) = 0.034234` et `3 / 86 = 0.034884`. Les données soutiennent « la probabilité de quitter F sur une paire est inférieure à 3,423 %, au seuil de 95 %, si les 86 paires sont des essais indépendants », non « F est définitif ». Les 86 paires sont un seul artefact lu sur 87 exécutions consécutives : comptées comme une seule évaluation, elles ne donnent aucune borne inférieure à 95 %.

## 3. Le lissage est un a priori, et un a priori est une affirmation

Le *lissage par ajout de un* ajoute un pseudo-effectif de 1 à chaque case avant de diviser, de sorte qu'aucune estimation ne soit nulle :

```text
p lissée (a→b) = (n_ab + 1) / (n_a + k)      k = nombre d'étiquettes, ici 6
```

C'est la moyenne des matrices encore plausibles après les données lorsque, avant elles, tout jeu de probabilités de ligne était tenu pour également plausible : un *a priori uniforme*. **Calculé :**

- Ligne D, aucune paire : chaque destination reçoit 1/6. Sans données, l'ajout de un rend la ligne uniforme.
- Ligne U parmi les 11 paires de lignes d'amorçage (2 restent, 1 va vers F) : rester tombe de 2/3 à (2 + 1)/(3 + 6) = 1/3, et 4/9 de la probabilité se pose sur quatre destinations jamais observées.
- Ligne T, 775 paires : la sortie reçoit 5/781 = 0,64 %, au-dessus de la borne de 0,386 %.

Pour toute ligne vierge de 5 à 2 000 paires, l'ajout de un sur six étiquettes affirme plus de sorties que la ligne n'en autorise au seuil de 95 % ; un pseudo-effectif de 0,5 ne le fait jamais dans cette plage. Ce sont les pseudo-effectifs portés sur les cinq sorties, 5 ou 2,5 contre le 3 de la règle, qui en décident, non les données.

**Observé.** Le dépôt contient une table d'amorçage sur ces six lettres : la machine `belief_hexavalent` de [`state/driver/transition-weights.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L22). Elle garde T avec un poids de 0,9 et [classe U→F comme interdite](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/transition-weights.json#L49). **Calculé sous une hypothèse que le fichier n'énonce pas**, à savoir qu'un pas de la table vaut une paire : la table attend 492,4 étiquettes changées parmi les 1 518 paires entre exécutions du feeder, où il n'y en a eu aucune. L'unique changement au relevé, U→F, est un saut que la table interdit en un pas (0,0825 en deux, par D ou C) ; une paire de 78,5 jours ne peut pas montrer combien de pas elle a couverts. Une matrice d'effectifs presque vide peut donc tout de même écarter un candidat à un pas de temps énoncé. Lu comme un a priori, un zéro est l'inverse de l'excès de l'ajout de un : aucune quantité de données ne peut le relever.

### Exercice pratique 3

Appliquez l'ajout de un sur six étiquettes à la ligne F (86 paires, toutes F→F) : donnez les probabilités lissées de rester et de sortir, et comparez la seconde à la borne de l'exercice 2.

> **Réponse :** Rester : `(86 + 1) / (86 + 6) = 87/92 = 0.945652`. Chaque autre étiquette reçoit `1/92`, la sortie reçoit donc `5/92 = 0.054348`, soit 5,435 %, au-dessus de la borne de 3,423 % : la ligne lissée affirme plus de changement que ses propres 86 paires n'en autorisent au seuil de 95 %.

## 4. Ce qu'affirme la matrice uniforme stockée

**Observé.** [`state/markov/transition-matrix.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/transition-matrix.json) a quatre états, Healthy, Watch, Warning et Freeze, et 0,25 dans chaque case ; sa note commence par « Uniform prior — no observations yet. » [`predictions.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/markov/predictions.json) contient une liste vide, et le fichier `engine-state.json` que la note nomme n'est pas dans le dossier. La [spécification](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L29) attribue l'un des quatre états à chaque cycle de gouvernance pris dans son ensemble, à partir d'un score de résilience et d'un ratio d'inflation d'artefacts (LOLLI/ERGOL) seuls.

**Calculé.** C'est de nouveau la ligne D : l'ajout de un sans données, avec k = 4. Toutes les lignes étant égales, l'état suivant ne dépend pas de l'état actuel. Depuis Healthy, un Freeze a la probabilité 0,25 au cycle suivant, 0,578125 en 3 cycles et 0,943686 en 10 ; l'attente moyenne du premier Freeze est de 4 cycles, et à long terme un quart des cycles sont gelés. La formule de la spécification, [`cycles_to_freeze = log(0.5) / log(P(not_freeze))`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L151), donne 2,409 cycles pour P(not_freeze) = 0,75 (là où la probabilité d'un Freeze atteint la moitié, non l'attente moyenne), tandis que son [alerte](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/specs/governance-markov-simulation.md#L168), déclenchée « When P(Freeze) > 0.3 », reste muette.

**Synthétique.** [`scenarios.json`](../../../fixtures/psychohistory/psy-006/scenarios.json) définit une matrice « collante » imaginaire qui garde chaque état avec la probabilité 0,97 et répartit le reste uniformément. Sa distribution stationnaire est la même, pourtant un Freeze en 10 cycles a la probabilité 0,095618 et l'attente moyenne est de 100 cycles. Les parts de long terme n'identifient pas une matrice ; l'uniforme est le membre sans mémoire de cette famille, une affirmation précise et non une affirmation neutre.

**Deux espaces d'états.** Les étiquettes décrivent 18 artefacts ; les états de gouvernance décrivent le système entier, un par cycle. Aucune étiquette n'entre dans cette classification, donc les effectifs d'étiquettes ne disent rien de Healthy→Freeze. Un état enregistré par cycle le dirait : 59 transitions hors de Healthy, aucune vers Freeze, ramèneraient la borne sur cette transition à 5 %. Aucun n'est enregistré : le journal de prévisions est vide.

### Exercice pratique 4

En partant de Healthy, calculez la probabilité d'un Freeze en 3 cycles et l'attente moyenne du premier Freeze, sous la matrice stockée puis sous la matrice collante (chaque autre état : 0,01).

> **Réponse :** Stockée : chaque cycle est un Freeze avec la probabilité 0,25, donc `1 − 0.75^3 = 37/64 = 0.578125` et l'attente est de `1 / 0.25 = 4` cycles. Collante : depuis tout autre état, un Freeze a la probabilité 0,01, donc `1 − 0.99^3 = 0.029701` et `1 / 0.01 = 100` cycles.

### Exercice pratique 5

Un coéquipier veut remplir la matrice de gouvernance à partir de la matrice d'étiquettes : « les étiquettes ne changent presque jamais, donc Healthy reste Healthy ». Acceptez ou rejetez, en donnant votre critère. Combien de cycles consécutifs sans Freeze rejetteraient le 0,25 stocké au seuil de 5 % ?

> **Réponse :** Rejeter. Un effectif n'est une preuve que pour l'espace d'états et le pas dans lesquels il a été compté : les étiquettes sont des valeurs de vérité de 18 artefacts, les états de gouvernance classent le système entier une fois par cycle, et la spécification classe un cycle sans aucune étiquette. `0.75^10 = 0.056314` est au-dessus de 0,05 et `0.75^11 = 0.042235` en dessous : 11 cycles consécutifs sans Freeze.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers de tendance de qualité, deux des trois fichiers de `state/markov/`, la spécification et la table d'amorçage dont les liens figurent plus haut. Le [README](../../../fixtures/psychohistory/psy-006/README.md) du jeu d'essai donne les commandes et les vérifications.

**Références de méthode.** Anderson, T. W., et Goodman, L. A. (1957), « Statistical Inference about Markov Chains », *Annals of Mathematical Statistics* 28(1), 89–110, [doi:10.1214/aoms/1177707039](https://doi.org/10.1214/aoms/1177707039). Hanley, J. A., et Lippman-Hand, A. (1983), « If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators », *JAMA* 249(13), 1743–1745, [doi:10.1001/jama.1983.03330370053031](https://doi.org/10.1001/jama.1983.03330370053031). Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404).

**Non fait.** Aucun état de gouvernance n'a été classé, donc rien n'a été testé au sujet de la matrice à 4 états, bien que les entrées du classificateur aient été enregistrées quelques fois : [quatre scores de résilience](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json), que PSY-013 lit, et [un ratio](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json). L'hypothèse de Markov et la constance de la matrice dans le temps n'ont pas été testées : un seul changement ne donne rien sur quoi les tester. L'évaluation de prévisions probabilistes sur ces étiquettes relève de PSY-016. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Comparer les blocs `assessment` à travers l'historique Git de `state/evolution/` pour compter combien de fois chaque valeur de vérité a été réexaminée. Si c'est une poignée de fois, les bornes par paire cèdent la place à des bornes par évaluation bien plus larges, et la matrice identité de la section 1 consigne des fichiers non révisés, non des artefacts stables.
