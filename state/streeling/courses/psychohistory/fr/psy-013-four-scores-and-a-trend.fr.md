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

Vous placerez un intervalle exact sur un score de onze essais, vous testerez un saut entre deux scores, vous tiendrez compte de la multiplicité des tests portant sur les quatre mêmes nombres, et vous direz ce que mesure un jeu de test réutilisé. **Question de projet :** l'historique de résilience affiche 0,00 ; 0,64 ; 0,73 ; 0,82 sur quatre cycles ; lesquels de ces sauts se distinguent du hasard, et que mesure un jeu d'injections répété ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit ce score comme un indicateur de régime et sa variation comme une vitesse. Ce module demande quelle variation onze essais peuvent montrer. [PSY-004](psy-004-how-large-is-large.fr.md) construit l'intervalle exact utilisé ici, [PSY-011](psy-011-measurement-change-or-system-change.fr.md) traite des changements d'instrument, et [PSY-023](psy-023-monitoring-a-plan.fr.md) conçoit des règles d'alerte.

## 1. Lire les enregistrements avant de calculer

**Observé** au commit `4b03838`. Le projet définit le score de résilience par `R = injections_caught / injections_total` ([glossaire](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/CONTEXT.md#L48), [politique de la métrique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/resilience-metric-policy.yaml)). Une *injection* est un défaut introduit volontairement. Le [rapport du test de chaos](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/chaos-test-report.md) en énumère onze, réparties dans trois fichiers : par exemple une liaison que rien ne lit dans [`chaos-test.ixql`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/chaos-test.ixql), une politique dont la description est délibérément dépourvue de sens, un schéma que rien ne référence. Chacune relève de l'un des sept *niveaux* (de L0, un fichier entier, à L4, une seule expression, puis politique et schéma) et a un détecteur attendu.

[`history.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience/history.json) contient quatre enregistrements, de `chaos-001` à `chaos-004`, horodatés en l'espace de 20 heures les 2026-03-22 et 2026-03-23 ; le commit épinglé date de 204 jours plus tard. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/extract.py) en prend un instantané dans [`observed-input.json`](../../../fixtures/psychohistory/psy-013/observed-input.json), et [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-013/analyze.py) confirme que les onze noms d'injection sont identiques dans les quatre enregistrements : le jeu est réutilisé, et non tiré à nouveau. Le README énonce l'affirmation examinée ici : « Trend: 0.0 → 0.64 → 0.73 → 0.82 across 4 chaos cycles » (« tendance : 0,0 → 0,64 → 0,73 → 0,82 sur quatre cycles de chaos », [ligne 132](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/README.md#L132)).

| Cycle | Interceptées (valeur enregistrée) | Statuts des 11 injections |
|---|---|---|
| chaos-001 | 0 | 11 missed |
| chaos-002 | 7 | 6 automated, 2 spec-only, 2 manual, 1 delayed-14d |
| chaos-003 | 8 | 6 automated, 2 policy-enforceable, 2 spec-only, 1 delayed-14d |
| chaos-004 | 9 | 6 automated, 3 policy-enforceable, 2 spec-only |

Trois faits passent avant toute statistique :

- **Ce que signifie « interceptée ».** Le [rapport de `chaos-003`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/docs/reports/shake-metafix-cycle-001.md) compte une injection comme interceptée quand son statut est `automated` ou `policy-enforceable`, et décrit le second statut comme des règles exécutables par un humain, « NOT yet automated tooling » (pas encore un outillage automatisé).
- **Le compte du cycle 2 ne tombe pas juste.** Cette règle donne 6, les scores par niveau de l'enregistrement impliquent 5, et c'est 7 qui est enregistré.
- **Le point de départ dépend de l'évaluateur.** Le rapport du test de chaos, daté du même jour que `chaos-001`, note les onze mêmes injections 5/11 « immediate » (immédiat) et 9/11 « including spec-level » (en comptant le niveau spécification). L'historique enregistre 0.

Les trois autres fichiers du dossier, `2026-03-23-red-team-cycle-00N.json`, forment une autre série (14 scénarios d'attaque notés PASS, PARTIAL ou FAIL), et non le détail de ces cycles.

### Exercice pratique 1

Appliquez la règle « interceptée = automated ou policy-enforceable » aux quatre lignes du tableau. Où contredit-elle le nombre enregistré ? Notez ensuite le cycle 2 à partir de ses scores par niveau : 1,0 pour L2 (trois injections) et pour L3 (une), 0,5 pour L4 (deux), 0 ailleurs.

> **Réponse :** La règle donne 0, 6, 8, 9 contre 0, 7, 8, 9 enregistrés : seul le cycle 2 diverge. Scores par niveau : `3 × 1 + 1 × 1 + 2 × 0.5 = 5`. Pour un même cycle, les enregistrements admettent donc 7, 6 ou 5, et aucun ensemble de statuts ne reproduit les quatre nombres enregistrés (`status_rules` dans [`results.json`](../../../fixtures/psychohistory/psy-013/results.json)). Les sections suivantes retiennent 7 et disent ce qui change avec 6 ou 5.

## 2. Placer un intervalle sur chaque score

On traite ici un cycle comme 11 essais indépendants partageant un même taux de détection p, comme si les injections étaient un échantillon aléatoire des défauts qui comptent (une hypothèse que la section 4 remet en question). L'*intervalle exact (de Clopper–Pearson) à 95 %* est l'ensemble des taux que le nombre observé ne rejette pas : sa borne inférieure est le p pour lequel « au moins autant » a une probabilité de 0,025, sa borne supérieure le p pour lequel « au plus autant » a une probabilité de 0,025.

**Calculé** (bornes arrondies à trois décimales) :

| Cycle (interceptées) | Intervalle à 95 % | Bandes de la politique touchées |
|---|---|---|
| chaos-001 (0/11) | 0–0,285 | critical |
| chaos-002 (7/11) | 0,308–0,891 | critical, warning, watch |
| chaos-003 (8/11) | 0,390–0,940 | les quatre |
| chaos-004 (9/11) | 0,482–0,977 | les quatre |

La politique de la métrique coupe R aux seuils 0,5 ; 0,7 et 0,9 en quatre bandes : critical, warning, watch et healthy (critique, alerte, vigilance, sain). Le dernier score, 0,82, se lit « watch » (« proactif » dans PSY-002), mais son intervalle a une largeur de 0,49 et touche toutes les bandes. Le premier intervalle ne chevauche aucun des autres ; les trois derniers se chevauchent entre eux.

### Exercice pratique 2

Pour 0 sur n, la borne supérieure a une expression explicite, `1 − 0.025^(1/n)` ; pour n sur n, la borne inférieure vaut `0.025^(1/n)`. Ces expressions sont celles de l'intervalle bilatéral ; une borne unilatérale à 95 %, comme dans [PSY-006](psy-006-transition-matrix-from-counts.fr.md), utilise 0,05. (a) Calculez les deux pour n = 11. (b) Un nouveau jeu est intercepté en entier. Quelle taille doit-il avoir pour que la borne inférieure atteigne le seuil « healthy », 0,9 ?

> **Réponse :** (a) `0.025^(1/11) = 0.715` : 0 sur 11 donne une borne supérieure de `1 − 0.715 = 0.285`, et 11 sur 11 une borne inférieure de 0,715, encore dans « watch ». (b) La borne atteint 0,9 quand `0.9^n ≤ 0.025`. `0.9^35 = 0.02503` est trop grand et `0.9^36 = 0.02253` est assez petit : 36 injections, toutes interceptées.

## 3. Tester chaque saut, puis compter les tests

**Calculé.** Le *test exact de Fisher* compare deux nombres comme deux échantillons indépendants. On fixe les marges : 11 essais par cycle, et le total des interceptions dans les deux. Si les cycles partagent un même taux, toutes les façons de répartir ces interceptions entre les 22 essais sont équiprobables. La *valeur p* utilisée ici est bilatérale : la probabilité totale de tous les tableaux qui ne sont pas plus probables que le tableau observé. La valeur unilatérale (le cycle ultérieur est supérieur) vaut moitié moins pour le premier saut.

| Cycles comparés (nombres) | Valeur p bilatérale |
|---|---|
| 1 à 2 (0/11, 7/11) | 0,0039 |
| 2 à 3 (7/11, 8/11) | 1 |
| 3 à 4 (8/11, 9/11) | 1 |
| 1 à 4 (0/11, 9/11) | 0,0002 |

**Quatre tests sur quatre nombres.** Quatre tests indépendants au seuil de 5 % donnent au moins un faux positif (une valeur p inférieure à 0,05 alors que rien ne diffère) dans 18,5 % des cas (`1 − 0.95^4`). La *correction de Bonferroni* compare chaque valeur p à `0.05 / 4 = 0.0125` et reste valable quelle que soit la dépendance entre les tests. Ici, les tests partagent des nombres, et un test exact sur 11 essais est conservateur : sur toutes les façons de répartir les 24 interceptions enregistrées entre les 44 essais, un test pris isolément passe sous 0,05 dans 1,78 % des répartitions, et au moins un des quatre dans 6,2 %. La correction ne change aucun verdict du tableau, mais elle tranche deux autres lectures :

- **Le plan est apparié.** Ce sont les mêmes injections qui sont notées à nouveau ; le test adapté est donc le *test exact des signes* (le test de McNemar sous sa forme exacte) : si rien n'a changé, une injection dont le résultat diffère a autant de chances d'avoir bougé dans un sens que dans l'autre. Du cycle 1 au cycle 2, sept gains et aucune perte donnent une valeur p bilatérale de `2 × (1/2)^7 = 0.0156`, au-dessus de 0,0125 (six gains selon les statuts : 0,031).
- **Le nombre du cycle 2.** Avec 6 au lieu de 7, la valeur p de Fisher vaut 0,0124 ; avec 5, elle vaut 0,035.

**Un saut ou trois ?** Pour les trois derniers cycles, un test exact de l'hypothèse « un taux commun » (Freeman–Halton) donne p = 0,88, et un test exact unilatéral de tendance (Cochran–Armitage, scores 0, 1, 2) p = 0,24. Trois cycles indépendants de 11 essais à leur taux groupé, 8/11, sont strictement croissants dans 8,5 % des cas. La politique qualifie un cycle d'« improving » (en amélioration) quand son R dépasse la moyenne des deux précédents ; sur de tels cycles, cette règle dit « improving » 45 % du temps, et deux fois de suite 18 %.

Avec les nombres enregistrés et le test de Fisher, le premier saut est le seul qui se distingue du hasard (avec le test apparié, il passe avec trois comparaisons et échoue avec quatre) ; les deux sauts suivants ne s'en distinguent pas, quelle que soit la lecture retenue ci-dessus.

### Exercice pratique 3

Calculez à la main la valeur p unilatérale de Fisher du cycle 1 au cycle 2, puis la valeur bilatérale.

> **Réponse :** Avec 7 interceptions sur 22 essais et aucune au cycle 1, les 11 essais du cycle 1 proviennent tous des 15 échecs : `C(15,11) / C(22,11) = 1,365 / 705,432 = 0.0019`. Le tableau symétrique (7 puis 0) est tout aussi probable et aucun autre tableau n'est aussi improbable ; la valeur bilatérale en est donc le double : 0,0039.

### Exercice pratique 4

Du cycle 2 au cycle 3, les statuts montrent deux injections passées de manquée à interceptée, aucune dans l'autre sens. Donnez la valeur p bilatérale du test des signes. Décidez ensuite si la valeur p appariée du premier saut résiste à une correction de Bonferroni pour trois tests (les sauts consécutifs) et pour quatre (en ajoutant le premier cycle contre le dernier).

> **Réponse :** `2 × (1/2)^2 = 0.5` : aucun indice de changement. Premier saut : `2 × (1/2)^7 = 1/64 = 0.0156`. Avec trois tests, le seuil est `0.05 / 3 = 0.0167` et le saut passe ; avec quatre, il est de 0,0125 et le saut échoue. Le verdict dépend du nombre de comparaisons que vous reconnaissez avoir faites.

## 4. Ce que mesure un jeu d'injections réutilisé

**Observé.** Chaque enregistrement ultérieur dit ce qui a été construit avant sa notation. `chaos-002` : trois détections implémentées dans un analyseur syntaxique, après quoi six injections désignent une même fonction, `analyzeLolli()`, comme leur détecteur. `chaos-003` : deux correctifs au niveau des politiques, et les deux injections de politique changent de statut. `chaos-004` : deux correctifs au niveau des schémas, dont un fichier de test « including injection #10 regression test », et c'est l'injection 10, le schéma que rien ne référence, qui change. Aucune injection ne repasse d'interceptée à manquée.

À partir du cycle 2, R compte donc, sur ce jeu, combien des onze défauts connus disposent désormais d'un détecteur ou d'une règle écrite : une mesure valable de l'avancement d'une liste de réparations, mais pas le taux de détection des défauts que personne n'a encore introduits, alors que c'est ce que suggère le nom de « résilience ». **Analogie :** un modèle ajusté sur son propre jeu de test garde un score croissant qui n'estime plus la performance sur des données nouvelles (Dwork et al. 2015).

**Synthétique** (aucun jeu de ce type n'existe). Un *jeu mis de côté* (*held-out set*), écrit par quelqu'un qui n'a pas lu les correctifs et noté une seule fois avant toute réparation, estimerait ce taux. Avec 11 injections mises de côté, un test de Fisher bilatéral contre 9/11 ne passe sous 0,05 qu'à 3 interceptions ou moins (p = 0,030 ; 4 interceptions donnent 0,080).

**L'objection la plus forte à cette leçon** est que son modèle de hasard ne correspond ni au jeu ni à la notation. Les injections n'ont pas été tirées au sort ; un statut indique si un détecteur existe, non le résultat d'une exécution bruitée ; et les injections bougent ensemble : les scores par niveau valent 0 ou 1 dans tous les cycles sauf un. En prenant les 7 niveaux pour unités (0, 2, 4, 5 entièrement notés), le premier saut a p = 0,46 et le premier cycle contre le dernier 0,021, au-dessus de 0,0125. Le point de départ bouge aussi : avec les 5/11 du rapport au lieu de 0, le cycle 2 donne p = 0,67 et le cycle 4 donne 0,18. **Ces enregistrements ne permettent pas de distinguer entre un bond de la détection et un changement de ce qui a été compté comme intercepté.** La prochaine vérification, ci-dessous, trancherait.

### Exercice pratique 5

Synthétique. Un cinquième cycle enregistre 11 sur 11 sur le même jeu, et la ligne d'état affiche R = 1,00, « healthy ». Un collègue écrit ensuite 11 nouvelles injections sans lire les correctifs ; 4 sont interceptées. (a) Qu'établit ce 1,00 ? (b) 4/11 diffère-t-il du dernier 9/11 enregistré ? Énoncez votre critère.

> **Réponse :** (a) Que les onze défauts connus ont tous désormais un détecteur ou une règle, et non le sort de défauts nouveaux ; même lu comme un échantillon neuf, 11 sur 11 laisse possibles des taux descendant jusqu'à 0,715. (b) Critère : une valeur p de Fisher bilatérale inférieure à 0,05. 4/11 contre 9/11 donne 0,080 : les deux ne se distinguent pas ; 3/11 donnerait 0,030.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les quatre fichiers de [`state/resilience/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/resilience), les deux rapports, la politique de la métrique, le glossaire, la ligne du README et les trois fichiers d'injections. `extract.py` refuse de s'exécuter si l'un d'eux diffère de son blob épinglé ou si le dossier gagne un fichier.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py`, puis `analyze.py` dans le même dossier. Le [README](../../../fixtures/psychohistory/psy-013/README.md) énumère les autocontrôles et les témoins négatifs, [`scenarios.json`](../../../fixtures/psychohistory/psy-013/scenarios.json) les choix d'analyse.

**Références de méthode.** Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413. Dunn, O. J. (1961), « Multiple Comparisons Among Means », *Journal of the American Statistical Association* 56, 52–64 (la correction de Bonferroni). Agresti, A. (2013), *Categorical Data Analysis*, 3e édition, Wiley (tests exacts, test de McNemar). Dwork, C., et cinq coauteurs (2015), « The Reusable Holdout: Preserving Validity in Adaptive Data Analysis », *Science* 349, 636–638.

**Non fait.** Aucune injection n'a été rejouée, et l'analyseur syntaxique que citent les enregistrements ([`Parser.fs`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/tools/ixql-parser/IxqlParser/Parser.fs), dans ce dépôt) n'a été ni compilé ni exécuté : le jeu d'essai se contente de lire les enregistrements. Aucun jeu mis de côté n'existe. Les quatre comparaisons ont été choisies une fois les quatre scores connus. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Écrire la règle de notation, l'appliquer aux onze verdicts du premier rapport et à chaque cycle, puis noter une seule fois un jeu mis de côté. Si la règle place le point de départ près de 5/11, la conclusion passe de « un grand saut, puis un plateau » à « aucun saut distinguable ». Par ailleurs, compiler l'analyseur syntaxique et appliquer `analyzeLolli` à `pipelines/chaos-test.ixql` : les enregistrements lui attribuent six injections.
