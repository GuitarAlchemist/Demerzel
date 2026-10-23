---
module_id: psy-023-monitoring-a-plan
department: psychohistory
course: "Surveiller un plan : bandes de tolérance et règles d'alerte"
level: intermediate
prerequisites: ["psy-012-early-warning-false-alarms", "psy-004-how-large-is-large"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-023
version: "0.1.0"
---

# Surveiller un plan : bandes de tolérance et règles d'alerte

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous compterez à quelle fréquence un seul examen d'un plan déclenche une fausse alerte, vous verrez pourquoi un examen chaque semaine la multiplie, vous comparerez une tolérance fixe à la somme cumulée de Page, et vous choisirez un seuil à partir des coûts avant que les données n'arrivent. **Question de projet :** un plan long (25 cours dans chacun de 21 départements) a besoin d'une règle pour dire « nous ne tenons plus le plan » ; à quelle fréquence une règle simple crie-t-elle au loup, et avec quel retard remarque-t-elle un vrai ralentissement ?

Le plan est un chiffre tiré d'un projet de spécification du cursus, pris tel quel et seulement pour fixer l'échelle : le dépôt épinglé ne l'énonce pas. Celui-ci contient [23 fiches de département](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments), dont 21 ont un dossier de cours, et la ligne 57 de son [README](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L57) indique « Streeling University — 23 departments, 21 course tracks » (départements et parcours de cours), sans nombre de cours par parcours. Aucune production hebdomadaire du projet n'a été mesurée : rien ici ne dit donc si le projet tient son plan ou s'en écarte.

[PSY-012](psy-012-early-warning-false-alarms.fr.md) a calibré une alerte pour un seul examen d'un relevé terminé ; ici, l'examen est répété chaque semaine, et c'est ce qui gonfle les fausses alertes. [PSY-010](psy-010-growth-curves-short-series.fr.md) ajuste l'historique de croissance ; ce module suppose qu'un échéancier existe. Tout ce qui suit est **synthétique** : des hypothèses dans [scenarios.json](../../../fixtures/psychohistory/psy-023/scenarios.json), un calcul fait par [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-023/analyze.py), des résultats enregistrés dans [results.json](../../../fixtures/psychohistory/psy-023/results.json).

## 1. Un seul examen du plan

Le plan : 21 × 25 = 525 cours, à raison de 5 par semaine, soit 105 semaines. Supposons que 10 brouillons soient en cours chaque semaine, chacun terminé dans la semaine avec la probabilité 1/2, indépendamment des autres. La production d'une semaine est alors le nombre de pièces tombées sur face parmi 10 pièces équilibrées : moyenne 5, variance 5/2, écart-type 1,5811. Le *déficit* après t semaines est le total prévu moins le total réel. Quand le plan est tenu, il a une moyenne de 0 et un écart-type de `sqrt(5t/2)` : 8,0623 à la semaine 26, 16,2019 à la semaine 105.

Avec des pièces plutôt qu'un bruit normal, chaque probabilité est un décompte exact sur des historiques de lancers équiprobables (2^10 = 1 024 par semaine) ; 20 000 simulations à graine fixée vérifient ensuite chaque valeur exacte, et non l'inverse.

Deux règles peuvent être appliquées à une semaine choisie à l'avance :

- Une *limite hebdomadaire* : alerte quand la production de la semaine est d'au plus 1. Cela se produit dans 1 + 10 = 11 des 1 024 historiques, soit 0,010742. Premières semaines simulées : 215 sur 20 000, soit 0,01075 (erreur type 0,000729 ; intervalle exact à 95 % de 0,009367 à 0,012278, comme dans [PSY-004](psy-004-how-large-is-large.fr.md)).
- Une *bande de prédiction* : alerte quand le déficit dépasse 2 écarts-types, `2 sqrt(5t/2)`.

### Exercice pratique 1

Examinez la bande une seule fois, à la semaine 26. Donnez le total prévu, la largeur de la bande, le plus petit déficit entier qui déclenche l'alerte, et le total réel au-dessous duquel l'alerte se déclenche (ce total compris). Le jeu d'essai compte une probabilité de 0,020247 pour cet examen ; pourquoi n'est-ce pas la queue de la loi normale, 0,02275 ?

> **Réponse :** Total prévu `26 × 5 = 130`. Écart-type `sqrt(26 × 5/2) = sqrt(65) = 8.0623` ; deux écarts-types font 16,1245. Le plus petit déficit entier au-dessus de cette valeur est 17 : l'alerte se déclenche donc à un total de `130 − 17 = 113` ou moins. La production se compte en cours entiers ; le décompte (0,020247) n'est donc pas la queue d'une variable normale continue (0,02275).

## 2. Examiner le plan chaque semaine

Examinée chaque semaine, une limite hebdomadaire donne des examens indépendants, avec des formules explicites. Pour une probabilité d'alerte a par semaine conforme au plan :

```text
P(au moins une alerte en T semaines) = 1 - (1 - a)^T
période opérationnelle moyenne       = 1 / a
```

La *période opérationnelle moyenne* (ARL, *average run length*) est le nombre moyen de semaines jusqu'à la première alerte ; la section 6.3.2.3.1 du manuel NIST/SEMATECH la définit comme « the average number of samples (subgroups) taken before an action signal is given » (le nombre moyen d'échantillons, ou sous-groupes, prélevés avant qu'un signal d'action ne soit émis). Pour la limite 1, a = 11/1024 et l'ARL vaut 93,09 semaines, moins que la durée du plan : la règle se déclenche au moins une fois dans une proportion de 0,678266 des plans tenus. La récurrence du jeu d'essai reproduit exactement la formule ; la simulation donne 13 552 sur 20 000, soit 0,6776 (erreur type 0,003305).

Examinée chaque semaine, la bande donne des examens dépendants (le déficit de la semaine 27 est celui de la semaine 26 plus une semaine) : la formule du produit ne s'applique plus, et la probabilité que le déficit franchisse la bande au moins une fois sur un horizon donné n'a pas d'expression explicite simple. La récurrence la calcule exactement, semaine après semaine, à partir des historiques qui n'ont pas encore franchi la bande. Pour la bande à 2 écarts-types, aucun examen isolé ne dépasse 0,028332, et pourtant la bande se déclenche au moins une fois d'ici la semaine 105 dans une proportion de 0,170761 des plans tenus, soit 6,03 fois la probabilité du plus grand examen isolé. La simulation : 3 380 sur 20 000, soit 0,169 (erreur type 0,00265). La somme des probabilités des 105 examens isolés, 2,359684, est une borne supérieure valable, et inutile.

### Exercice pratique 2

Pour la limite hebdomadaire « production d'au plus 1 » : (a) donnez l'ARL et la probabilité d'au moins une alerte d'ici la semaine 52 ; (b) à l'aide de la borne `P(at least one alarm) ≤ T × a`, trouvez la probabilité par semaine qui limiterait à 5 % le risque sur l'ensemble du plan. Une limite hebdomadaire peut-elle y parvenir ?

> **Réponse :** (a) `1024 / 11 = 93.09` semaines ; `1 − (1 − 11/1024)^52 = 0.429713`. (b) `0.05 / 105 = 0.000476` (résoudre exactement `1 − (1 − a)^105 = 0.05` donne 0,000488). La limite la plus stricte, une semaine vide, a une probabilité de `1/1024 = 0.000977`, environ le double de ce qu'il faudrait : aucune limite hebdomadaire n'est assez silencieuse. Même cette limite se déclenche dans une proportion de 0,097502 des plans tenus.

## 3. Une tolérance et la somme cumulée de Page

Deux règles surveillent le déficit cumulé. La *tolérance* se déclenche quand le déficit atteint c cours. La *somme cumulée* de Page (Page, 1954) attribue à chaque semaine un score égal à son déficit moins une *valeur de référence* k, et se déclenche quand la somme des scores dépasse d'au moins l'*intervalle de décision* h sa plus basse valeur antérieure, valeur de départ 0 comprise. L'énoncé du manuel : « If the distance between a plotted point and the lowest previous point is equal to or greater than h, one concludes that the process mean has shifted (increased) » (si la distance entre un point tracé et le point le plus bas qui le précède est supérieure ou égale à h, on conclut que la moyenne du processus s'est déplacée vers le haut). La récurrence ci-dessous est équivalente ; les deux formes concordent dans chaque simulation.

```text
tolérance :       S(t) = S(t-1) + 5 - production(t) ;              alerte quand S(t) >= c
somme cumulée :   C(t) = max(0, C(t-1) + 5 - production(t) - k) ;  alerte quand C(t) >= h
```

Ici, k = 1, la moitié des 2 cours par semaine que fait perdre le ralentissement supposé : à partir de la semaine 53, 6 brouillons en cours, une moyenne de 3 cours, 60 % du plan. Une règle est *calibrée* au plus petit seuil entier dont la probabilité exacte d'alerte en 105 semaines, plan tenu, est d'au plus 5 % : c = 32 (31 donne 0,052439) et h = 8 (7 donne 0,084257). Le *délai* est le nombre de semaines lentes écoulées au moment où l'alerte survient, parmi les plans encore silencieux à la semaine 52 (les simulations se poursuivent au-delà de la semaine 105).

| Règle | Alerte plan tenu, exacte | Simulée ± erreur type [intervalle exact à 95 %] | Délai moyen, exact (simulé ± erreur type) | 90 % des délais ne dépassent pas |
|---|---|---|---|---|
| Tolérance 32, calibrée | 0,045372 | 0,0458 ± 0,001478 [0,042944 ; 0,048789] | 16,5 (16,56 ± 0,04) | 25 |
| Tolérance 40 | 0,012603 | 0,01185 ± 0,000765 [0,010397 ; 0,013448] | 20,44 (20,5 ± 0,04) | 29 |
| Somme cumulée 6 | 0,185318 | 0,18365 ± 0,002738 [0,178305 ; 0,189087] | 5,88 (5,87 ± 0,02) | 10 |
| Somme cumulée 8, calibrée | 0,037333 | 0,03655 ± 0,001327 [0,033992 ; 0,039244] | 7,85 (7,85 ± 0,02) | 12 |
| Somme cumulée 10 | 0,007136 | 0,0064 ± 0,000564 [0,005342 ; 0,007605] | 9,83 (9,82 ± 0,03) | 15 |

Pour chaque règle, un seuil plus silencieux signifie une alerte plus tardive : aucun seuil n'est gratuit. À niveaux de fausses alertes comparables, la somme cumulée signale le ralentissement au bout de 7,85 semaines en moyenne, contre 16,5, soit un rapport de 0,4754 ; son ARL est de 2 623,4 semaines quand le plan est tenu, et de 8,3 après un ralentissement, en partant de zéro. La tolérance est plus lente parce qu'elle capitalise chaque excédent : un plan en avance doit d'abord perdre son avance. Une semaine conforme au plan a un score de −1 dans la somme cumulée ; C redescend donc vers zéro et oublie le passé. Un des 28 intervalles à 95 % simulés manque sa valeur exacte (intervalle de décision 9, à 2,97 erreurs types en dessous), soit environ un sur vingt, comme attendu.

### Exercice pratique 3

Un relevé inventé de 12 semaines : 7, 6, 6, 5, 3, 4, 2, 3, 4, 2, 3, 3 ; le ralentissement a commencé à la semaine 5. Calculez S et C (k = 1) pour chaque semaine. Quelle règle calibrée se déclenche, et quand ?

> **Réponse :** Déficits hebdomadaires : −2, −1, −1, 0, 2, 1, 3, 2, 1, 3, 2, 2. S : −2, −3, −4, −4, −2, −1, 2, 4, 5, 8, 10, 12 ; la tolérance (32) reste silencieuse, à 20 cours du seuil, soit environ `20 / 2 = 10` semaines lentes de plus. Scores : −3, −2, −2, −1, 1, 0, 2, 1, 0, 2, 1, 1, d'où C : 0, 0, 0, 0, 1, 1, 3, 4, 4, 6, 7, 8. La somme cumulée se déclenche à la semaine 12, la 8e semaine lente. La tolérance porte encore l'avance de 4 cours des semaines 1 à 4 ; la somme cumulée l'a oubliée.

## 4. Choisir le seuil à partir des coûts, et le fixer avant de regarder

Un seuil choisi après lecture du relevé n'a pas de taux de fausses alertes connu : c'est le relevé qui l'a choisi.

### Exercice pratique 4

Un collègue qui lit le relevé chaque semaine constate à la semaine 61 un déficit de 25 cours, alors que la bande à 2 écarts-types se déclenche à partir de 25, et conclut : « si le plan était tenu, un déficit aussi grand à la semaine 61 aurait une probabilité de 0,023586 ; le plan n'est plus tenu. » Qualifiez cette affirmation et nommez la règle que vous utiliseriez à la place.

> **Réponse :** Non étayée. La valeur 0,023586 est la probabilité d'un seul examen, à une semaine choisie à l'avance. Ce collègue aurait signalé n'importe quelle semaine où la bande était franchie, et cette procédure se déclenche dans une proportion de 0,170761 des plans tenus en 105 semaines. Fixez une règle avant de regarder, calibrée sur l'ensemble du plan : la tolérance 32 ou la somme cumulée 8, chacune à 5 % au plus.

L'objectif de 5 % est lui-même une convention, pas un coût. Avec des coûts supposés (un ralentissement à partir de la semaine 53 avec la probabilité q = 1/2, chaque semaine lente avant l'alerte coûtant 2 cours, chaque fausse alerte coûtant F cours de vérification) :

```text
coût attendu = (1 - q) × P(fausse alerte) × F + q × délai moyen × 2
```

Pour F = 20, l'intervalle de décision le moins coûteux est 7 (7,7 cours) ; pour F = 100, c'est 9 (9,66). L'intervalle calibré, 8, n'est le moins coûteux dans aucun des deux cas.

### Exercice pratique 5

Avec q = 1/2, 2 cours par semaine lente et F = 20, calculez à partir du tableau le coût attendu des intervalles de décision 6 et 8, ainsi que le coût de fausse alerte pour lequel ils sont à égalité.

> **Réponse :** h = 6 : `0.5 × 0.185318 × 20 + 0.5 × 5.88 × 2 = 1.85 + 5.88 = 7.73`. h = 8 : `0.5 × 0.037333 × 20 + 0.5 × 7.85 × 2 = 0.37 + 7.85 = 8.22`. Ils sont à égalité quand `0.5 × F × (0.185318 − 0.037333) = 7.85 − 5.88`, donc `F = 1.97 / 0.0739925 = 26.62` avec les valeurs arrondies du tableau (26,55 avec les valeurs exactes). En dessous de l'égalité, h = 6 est moins coûteux ; au-dessus, c'est h = 8.

**L'objection la plus forte** est que chaque seuil appartient à son modèle de production. PSY-010 a trouvé des modules ajoutés par rafales, et [PSY-008](psy-008-bursts-are-not-rates.fr.md) montre combien un taux moyen induit en erreur quand les arrivées se font par rafales. Gardons la moyenne de 5 par semaine, mais livrée par lots : 40 brouillons en cours une semaine sur quatre, aucun le reste du temps. La variance hebdomadaire devient 155/2, 31 fois celle du régime régulier. La tolérance calibrée 32 se déclenche alors dans une proportion de 0,704574 des plans tenus (simulée : 0,7046 ± 0,003226), et la somme cumulée 8 dans une proportion de 1,000000 à six décimales (20 000 sur 20 000 en simulation, intervalle de 0,999816 à 1). Le réglage de k a lui aussi un revers : pour un ralentissement plus modéré (8 brouillons, 80 % du plan), une semaine lente a un score moyen de 0, et le délai moyen de la somme cumulée, 41,45 semaines, dépasse celui de la tolérance, 32,78 ; parmi les plans encore silencieux à la semaine 52, une proportion de 0,261752 pour la somme cumulée et de 0,076485 pour la tolérance reste sans alerte à la fin du plan. **Ce modèle ne peut pas dire quelle règle convient au projet** : il faudrait pour cela la production hebdomadaire du projet et une décision sur le ralentissement qui mérite d'être détecté.

## Sources, limites et prochaine vérification

**Épinglés au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** la ligne du README et les fiches de département citées plus haut, pour l'échelle ; aucun fichier de données n'a été lu.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py`, puis la même commande avec `--check`, qui compare une nouvelle exécution aux résultats enregistrés. Le [README](../../../fixtures/psychohistory/psy-023/README.md) énumère les 24 autocontrôles, dont un cas calculé à la main et un témoin négatif.

**Références de méthode.** Page, E. S. (1954), « Continuous Inspection Schemes », *Biometrika* 41(1–2), 100–115, doi:10.1093/biomet/41.1-2.100. NIST/SEMATECH *e-Handbook of Statistical Methods*, section [6.3.2.3.1](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3231.htm), la source des deux citations, et section [6.3.2.3](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) sur les cartes de somme cumulée. Brook, D., et Evans, D. A. (1972), « An approach to the probability distribution of cusum run length », *Biometrika* 59(3), 539–549, doi:10.1093/biomet/59.3.539 (l'idée de chaîne de Markov qui sous-tend la récurrence du jeu d'essai). Armitage, P., McPherson, C. K., et Rowe, B. C. (1969), « Repeated Significance Tests on Accumulating Data », *Journal of the Royal Statistical Society, Series A* 132(2), 235–244, doi:10.2307/2343787 (pourquoi des examens répétés gonflent un taux d'erreur).

**Non fait.** Aucune production hebdomadaire du projet n'a été lue. L'article de Page de 1954 n'a pas été ouvert ; sa règle est énoncée telle que la donne le manuel. Seules des règles unilatérales et un ralentissement brutal et permanent ont été étudiés ; ni règles bilatérales, ni dérives progressives, ni estimation de l'ampleur d'un ralentissement. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Dès qu'un échéancier existera, extraire la production hebdomadaire du projet (les ajouts de modules datés de PSY-010 sont un point de départ), estimer sa variance et la part des semaines vides, et recalibrer les deux règles sur cette dispersion. Si la production arrive par rafales, les seuils ci-dessus se déclencheraient dans la plupart des plans tenus.
