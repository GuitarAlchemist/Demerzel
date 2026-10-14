---
module_id: psy-013-four-scores-and-a-trend
department: psychohistory
course: "Quatre scores et une tendance : lire l'historique de résilience"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-013
version: "0.1.0"
---

# Quatre scores et une tendance : lire l'historique de résilience

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous associerez un intervalle exact à un score établi sur onze essais, vous éprouverez un pas entre deux scores, vous tiendrez compte de plusieurs tests portant sur les mêmes quatre nombres, et vous direz ce que mesure un jeu d'essai réutilisé. **Question de projet :** l'historique de résilience affiche 0,00, 0,64, 0,73 et 0,82 sur quatre cycles ; lequel de ces pas se distingue du hasard, et que mesure un jeu d'injections répété ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit ce score comme un indicateur de régime et sa variation comme une vitesse. Ce module demande quelle quantité de changement onze essais permettent de montrer. [PSY-004](psy-004-how-large-is-large.fr.md) construit l'intervalle exact employé ici, [PSY-011](psy-011-measurement-change-or-system-change.fr.md) traite des changements d'instrument, et PSY-023 conçoit des règles d'alerte.

## 1. Lire le relevé avant de calculer

**Observé** au commit `4b03838`. Le projet définit le score de résilience comme `R = injections_caught / injections_total` ([glossaire](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/CONTEXT.md#L48), [politique de métrique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/resilience-metric-policy.yaml)). Une *injection* est un défaut planté à dessein. Le [rapport de test de chaos](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/chaos-test-report.md) en énumère onze dans trois fichiers, par exemple une liaison que rien ne lit dans [`chaos-test.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/chaos-test.ixql), une politique dont la description est délibérément vide de sens, un schéma que rien ne référence. Chacune relève de l'un de sept *niveaux* (L0, un fichier entier, à L4, une seule expression, puis politique et schéma) et d'un détecteur attendu.

[`history.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json) contient quatre enregistrements, de `chaos-001` à `chaos-004`, horodatés à moins de 20 heures d'intervalle les 2026-03-22 et 2026-03-23 ; le commit épinglé est daté de 204 jours plus tard. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/extract.py) le fige dans [`observed-input.json`](../../../fixtures/psychohistory/psy-013/observed-input.json), et [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/analyze.py) confirme que les onze noms d'injection sont identiques dans les quatre enregistrements : le jeu est réutilisé, non retiré au sort. Le README énonce l'affirmation examinée ici : « Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles » ([ligne 132](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L132)).

| Cycle | Détectées (consigné) | Étiquettes de statut des 11 injections |
|---|---|---|
| chaos-001 | 0 | 11 manquées |
| chaos-002 | 7 | 6 automated, 2 spec-only, 2 manual, 1 delayed-14d |
| chaos-003 | 8 | 6 automated, 2 policy-enforceable, 2 spec-only, 1 delayed-14d |
| chaos-004 | 9 | 6 automated, 3 policy-enforceable, 2 spec-only |

Trois faits viennent avant toute statistique :

- **Ce que « détectée » signifie.** Le [rapport de `chaos-003`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/shake-metafix-cycle-001.md) marque une injection comme détectée quand son statut est `automated` ou `policy-enforceable`, et qualifie le second de règles exécutables par un humain, « NOT yet automated tooling ».
- **Le cycle 2 ne tombe pas juste.** Cette règle donne 6, les scores de niveau de l'enregistrement impliquent 5, et c'est 7 qui est consigné.
- **La référence dépend de l'évaluateur.** Le rapport de test de chaos, daté du même jour que `chaos-001`, note les mêmes onze injections 5/11 « immediate » et 9/11 « including spec-level ». L'historique consigne 0.

Les trois autres fichiers du dossier, `2026-03-23-red-team-cycle-00N.json`, forment une autre série (14 scénarios d'attaque notés PASS, PARTIAL ou FAIL), non le détail de ces cycles.

### Exercice pratique 1

Appliquez la règle « détectée = automated ou policy-enforceable » aux quatre lignes du tableau. Où diverge-t-elle de l'effectif consigné ? Notez ensuite le cycle 2 d'après ses scores de niveau : 1,0 pour L2 (trois injections) et pour L3 (une), 0,5 pour L4 (deux), 0 ailleurs.

> **Réponse :** La règle donne 0, 6, 8, 9 contre les 0, 7, 8, 9 consignés : seul le cycle 2 diverge. Scores de niveau : `3 × 1 + 1 × 1 + 2 × 0.5 = 5`. L'enregistrement soutient 7, 6 ou 5 pour un même cycle, et aucun jeu d'étiquettes de statut ne reproduit les quatre effectifs consignés (`status_rules` dans [`results.json`](../../../fixtures/psychohistory/psy-013/results.json)). Les sections ci-dessous emploient 7 et disent ce que change 6 ou 5.

## 2. Associer un intervalle à chaque score

Traitons un cycle comme 11 essais indépendants de même taux de détection p, comme si les injections étaient un échantillon au hasard des défauts qui comptent (une hypothèse que la section 4 met en cause). L'*intervalle exact à 95 % (de Clopper–Pearson)* est l'ensemble des taux que l'effectif ne rejette pas : sa borne inférieure est le p auquel « ce nombre ou davantage » a la probabilité 0,025, sa borne supérieure le p auquel « ce nombre ou moins » a la probabilité 0,025.

**Calculé** (bornes arrondies à trois décimales) :

| Cycle (détectées) | Intervalle à 95 % | Bandes de la politique touchées |
|---|---|---|
| chaos-001 (0/11) | 0–0,285 | critical |
| chaos-002 (7/11) | 0,308–0,891 | critical, warning, watch |
| chaos-003 (8/11) | 0,390–0,940 | les quatre |
| chaos-004 (9/11) | 0,482–0,977 | les quatre |

La politique de métrique découpe R à 0,5, 0,7 et 0,9 en critical, warning, watch et healthy. Le dernier score, 0,82, se lit « watch » (« proactive » dans PSY-002), mais son intervalle est large de 0,49 et touche toutes les bandes. Le premier intervalle ne recouvre aucun des autres ; les trois derniers se recouvrent entre eux.

### Exercice pratique 2

Pour 0 détectée sur n, la borne supérieure a une forme fermée, `1 − 0.025^(1/n)` ; pour n sur n, la borne inférieure vaut `0.025^(1/n)`. Ces formes appartiennent à l'intervalle bilatéral ; une borne unilatérale à 95 %, comme dans [PSY-006](psy-006-transition-matrix-from-counts.fr.md), emploie 0,05. (a) Calculez les deux pour n = 11. (b) Un jeu neuf est détecté en entier. Quelle taille doit-il avoir pour que la borne inférieure atteigne la coupure « healthy », 0,9 ?

> **Réponse :** (a) `0.025^(1/11) = 0.715` : 0 sur 11 donne une borne supérieure de `1 − 0.715 = 0.285`, et 11 sur 11 une borne inférieure de 0,715, encore dans « watch ». (b) La borne atteint 0,9 quand `0.9^n ≤ 0.025`. `0.9^35 = 0.02503` est trop grand et `0.9^36 = 0.02253` est assez petit : 36 injections, toutes détectées.

## 3. Éprouver chaque pas, puis compter les tests

**Calculé.** Le *test exact de Fisher* compare deux effectifs comme deux échantillons indépendants. Fixons les marges : 11 essais par cycle, et le total détecté dans les deux. Si les cycles partagent un seul taux, toutes les façons de placer ces détections parmi les 22 essais sont également probables. La *valeur p* employée ici est bilatérale : la probabilité totale de tous les tableaux non plus probables que celui observé. La valeur unilatérale (le cycle postérieur est le plus élevé) vaut la moitié pour le premier pas.

| Cycles comparés (effectifs) | p bilatéral |
|---|---|
| 1 contre 2 (0/11, 7/11) | 0,0039 |
| 2 contre 3 (7/11, 8/11) | 1 |
| 3 contre 4 (8/11, 9/11) | 1 |
| 1 contre 4 (0/11, 9/11) | 0,0002 |

**Quatre tests sur quatre nombres.** Quatre tests indépendants au seuil de 5 % donnent au moins un faux positif (un p inférieur à 0,05 alors que rien ne diffère) dans 18,5 % des cas (`1 − 0.95^4`). La *correction de Bonferroni* compare chaque p à `0.05 / 4 = 0.0125` et tient quelle que soit la dépendance entre les tests. Ici, les tests partagent des effectifs, et un test exact sur 11 essais est conservateur : sur toutes les façons de placer les 24 détections consignées parmi les 44 essais, un test seul tombe sous 0,05 dans 1,78 % des dispositions et au moins l'un des quatre dans 6,2 %. La correction ne change aucun verdict du tableau, mais elle tranche deux autres lectures :

- **Le plan est apparié.** Les mêmes injections sont réévaluées : le test adapté est donc le *test des signes exact* (le test de McNemar sous forme exacte) : si rien n'a changé, une injection dont le résultat diffère a autant de chances d'avoir bougé dans un sens que dans l'autre. Du cycle 1 au cycle 2, sept gains et aucune perte donnent un p bilatéral de `2 × (1/2)^7 = 0.0156`, au-dessus de 0,0125 (six gains, selon les étiquettes de statut : 0,031).
- **L'effectif du cycle 2.** Avec 6 au lieu de 7, le p de Fisher vaut 0,0124 ; avec 5, il vaut 0,035.

**Un pas ou trois ?** Pour les trois derniers cycles, un test exact de « un seul taux commun » (Freeman–Halton) donne p = 0,88 et un test exact de tendance unilatéral (Cochran–Armitage, scores 0, 1, 2) donne p = 0,24. Trois cycles indépendants de 11 essais à leur taux groupé, 8/11, croissent strictement dans 8,5 % des cas. La politique étiquette un cycle « improving » quand son R dépasse la moyenne des deux précédents ; sur de tels cycles, cette règle dit « improving » dans 45 % des cas, et deux fois de suite dans 18 %.

Sur les effectifs consignés et avec le test de Fisher, le premier pas est le seul qui se distingue du hasard (au test apparié, il passe avec trois comparaisons et échoue avec quatre) ; les deux pas suivants ne s'en distinguent pas, sous aucune des lectures ci-dessus.

### Exercice pratique 3

Calculez à la main la valeur p unilatérale de Fisher du cycle 1 au cycle 2, puis la valeur bilatérale.

> **Réponse :** Avec 7 détections parmi 22 essais et aucune dans le cycle 1, les 11 essais du cycle 1 proviennent tous des 15 manquées : `C(15,11) / C(22,11) = 1,365 / 705,432 = 0.0019`. Le tableau miroir (7 puis 0) est également probable et aucun autre tableau n'est aussi improbable : la valeur bilatérale vaut donc le double, soit 0,0039.

### Exercice pratique 4

Du cycle 2 au cycle 3, les étiquettes de statut montrent deux injections passant de manquée à détectée, aucune dans l'autre sens. Donnez la valeur p bilatérale du test des signes. Décidez ensuite si la valeur p appariée du premier pas survit à une correction de Bonferroni pour trois tests (les pas consécutifs) et pour quatre (en ajoutant le premier contre le dernier).

> **Réponse :** `2 × (1/2)^2 = 0.5` : aucune preuve de changement. Premier pas : `2 × (1/2)^7 = 1/64 = 0.0156`. Avec trois tests, le seuil est `0.05 / 3 = 0.0167` et le pas passe ; avec quatre, il est de 0,0125 et le pas échoue. Le verdict dépend du nombre de comparaisons que vous reconnaissez avoir faites.

## 4. Ce que mesure un jeu d'injections réutilisé

**Observé.** Chaque enregistrement postérieur dit ce qui a été construit avant qu'il ne soit noté. `chaos-002` : trois détections implémentées dans un analyseur syntaxique, après quoi six injections nomment une seule fonction, `analyzeLolli()`, comme détecteur. `chaos-003` : deux correctifs au niveau de la politique, et les deux injections de politique changent de statut. `chaos-004` : deux correctifs au niveau du schéma, dont un fichier de test « including injection #10 regression test », et l'injection 10, le schéma non référencé, est celle qui change. Aucune injection ne repasse de détectée à manquée.

À partir du cycle 2, R sur ce jeu compte donc combien des onze défauts connus ont désormais un détecteur ou une règle écrite : une mesure d'avancement solide pour une liste de réparations, mais non le taux de détection sur des défauts que personne n'a encore plantés, ce que le nom de « résilience » suggère. **Analogie :** un modèle réglé contre son propre jeu d'essai conserve un score qui monte et qui n'estime plus sa performance sur des données nouvelles (Dwork et al. 2015).

**Synthétique** (aucun tel jeu n'existe). Un *jeu réservé*, écrit par quelqu'un qui n'a pas lu les correctifs et noté une seule fois avant toute réparation, estimerait ce taux. Avec 11 injections réservées, un test bilatéral de Fisher contre 9/11 ne tombe sous 0,05 qu'à 3 détectées ou moins (p = 0,030 ; 4 détectées donnent 0,080).

**L'objection la plus forte à cette leçon** est que son modèle de hasard ne convient ni au jeu ni à la notation. Les injections n'ont pas été échantillonnées ; un statut consigne l'existence d'un détecteur, non une exécution bruitée ; et les injections bougent ensemble : les scores de niveau valent 0 ou 1 dans tous les cycles sauf un. Avec les 7 niveaux pour unités (0, 2, 4, 5 pleinement notés), le premier pas a p = 0,46 et le premier contre le dernier 0,021, au-dessus de 0,0125. La référence bouge aussi : avec le 5/11 du rapport au lieu de 0, le cycle 2 donne p = 0,67 et le cycle 4 donne 0,18. **Ce relevé ne permet pas de distinguer un bond de la détection d'un changement de ce qui était compté comme détecté.** La prochaine vérification ci-dessous trancherait.

### Exercice pratique 5

Synthétique. Un cinquième cycle consigne 11 détectées sur 11 sur le même jeu, et la ligne de statut affiche R = 1,00, « healthy ». Un collègue écrit ensuite 11 nouvelles injections sans lire les correctifs ; 4 sont détectées. (a) Qu'établit le 1,00 ? (b) Le 4/11 diffère-t-il du dernier 9/11 consigné ? Énoncez votre critère.

> **Réponse :** (a) Que les onze défauts connus ont désormais tous un détecteur ou une règle, non ce qu'il advient de défauts nouveaux ; même lu comme un échantillon neuf, 11 sur 11 laisse des taux jusqu'à 0,715. (b) Critère : un p bilatéral de Fisher inférieur à 0,05. 4/11 contre 9/11 donne 0,080 : les deux ne se distinguent donc pas ; 3/11 donnerait 0,030.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les quatre fichiers de [`state/resilience/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience), les deux rapports, la politique de métrique, le glossaire, la ligne du README et les trois fichiers d'injection. `extract.py` refuse de s'exécuter si l'un d'eux diffère de son blob épinglé ou si le dossier gagne un fichier.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py`, puis `analyze.py` dans le même dossier. Le [README](../../../fixtures/psychohistory/psy-013/README.md) énumère les autovérifications et les contrôles négatifs, [`scenarios.json`](../../../fixtures/psychohistory/psy-013/scenarios.json) les choix d'analyse.

**Références de méthode.** Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413. Dunn, O. J. (1961), « Multiple Comparisons Among Means », *Journal of the American Statistical Association* 56, 52–64 (la correction de Bonferroni). Agresti, A. (2013), *Categorical Data Analysis*, 3e édition, Wiley (les tests exacts, le test de McNemar). Dwork, C., et cinq coauteurs (2015), « The Reusable Holdout: Preserving Validity in Adaptive Data Analysis », *Science* 349, 636–638.

**Non fait.** Aucune injection n'a été rejouée, et l'analyseur syntaxique que les enregistrements nomment ([`Parser.fs`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/tools/ixql-parser/IxqlParser/Parser.fs), dans ce dépôt) n'a été ni compilé ni exécuté : le jeu d'essai ne lit que les enregistrements. Aucun jeu réservé n'existe. Les quatre comparaisons ont été choisies après que les quatre scores étaient connus. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Écrire la règle de notation, l'appliquer aux onze verdicts du premier rapport puis à chaque cycle, et noter une seule fois un jeu réservé. Si la règle place la référence près de 5/11, la conclusion passe de « un grand pas, puis un plateau » à « aucun pas distinguable ». Séparément, compiler l'analyseur syntaxique et appliquer `analyzeLolli` à `pipelines/chaos-test.ixql` : les enregistrements lui créditent six injections.
