---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Mesurer la couverture des voies de travail après un changement de mode"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Mesurer la couverture des voies de travail après un changement de mode

> **Département de science des réseaux** | Niveau intermédiaire | 35 minutes | Brouillon français ; révision et publication en attente

## Objectifs et question du projet

Vous construirez un graphe reliant les agents à des classes de travail à partir d'une politique de voies Demerzel figée à un commit. Vous mesurerez sa couverture, l'effet du retrait d'un agent et les informations que la projection perd sur les rôles et les décisions. **Question du projet :** si le mode de répartition consultatif change ou si une voie devient indisponible, quelles *classes de travail déclarées* conservent un chemin nommé ? Ce calcul peut guider le choix d'une voie ou une question de révision. Il ne prouve ni qu'un agent est en ligne, ni qu'il est autorisé à agir, ni qu'il a terminé une tâche.

[NET-002](../en/net-002-capability-graphs-and-projections.md) relie des *dépôts* à des familles de capacités. Ici, les sommets sont des *agents*, leurs rôles attribués et les classes correspondantes. Les arêtes viennent de la [politique des voies Demerzel au commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json), puis sont filtrées par mode. Le graphe ne contient ni route MCP ni état réel des agents.

## 1. Définir le graphe avant de le mesurer

La politique figée nomme cinq agents : `jules`, `claude`, `gemini`, `codex` et `augment`. Chacun possède un rôle `primary`, des rôles `secondary` et une liste `forbidden` distincte ([définitions des agents](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Chaque rôle nommé renvoie à une `work_class` ([définitions des rôles](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). La politique se décrit comme **consultative et sans exécution** : elle propose une orientation, sans fournir de reçu de travail accompli.

Construisez le graphe orienté à trois couches `agent → rôle attribué → classe de travail`. La première arête n'existe que pour un rôle primaire ou secondaire ; un rôle interdit ne crée jamais de chemin. La seconde suit `work_class`. Pour un mode donné, masquez les chemins dont la classe apparaît dans [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86). Dans la projection à deux couches, une arête agent-classe existe si au moins un chemin attribué subsiste. Plusieurs rôles d'une même classe ne comptent que pour **une** arête agent-classe. Nous comptons des choix d'agents distincts, pas leur capacité ni leurs tâches terminées.

Le dictionnaire complet `work_classes` contient 13 noms, dont des actions interdites. Seules cinq classes figurent dans les attributions primaires ou secondaires : `fix`, `groom`, `navigate`, `net_new_feature` et `review`. Appelons cet ensemble `A`. Définissons la **couverture** `C(m) = |{c in A: degree_m(c) > 0}| / |A|` et le **nombre de classes redondantes** `R(m) = |{c in A: degree_m(c) >= 2}|`. Ce sont des mesures descriptives. Deux agents voisins d'une même classe ne sont pas nécessairement interchangeables pour un rôle précis.

### Exercice pratique 1 : éviter de compter deux fois les rôles

En mode NORMAL, `claude` possède `draft_to_ready_helper`, `test_author` et `review_feedback_applier`, tous de classe `fix`, ainsi que `builder_fixer` de classe `net_new_feature` et `lightweight_groomer` de classe `groom`. Quel est son degré dans la projection agent-classe ? Combien de chemins agent-rôle possède-t-il ? Pourquoi les deux nombres diffèrent-ils ?

> **Réponse :** Son degré projeté est **3** : `fix`, `net_new_feature`, `groom`. Il possède **5** chemins vers des rôles attribués, soit un primaire et quatre secondaires. Les trois rôles `fix` deviennent une seule arête agent-classe. Compter cinq rôles comme cinq agents de remplacement gonflerait artificiellement la redondance.

## 2. Mesurer la coupure produite par un mode

Les attributions primaires et secondaires donnent la projection suivante en mode NORMAL. Un `1` indique qu'au moins un chemin agent-rôle survit au blocage de sa classe :

| Agent | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

Cette matrice contient **9** arêtes agent-classe. Les degrés des classes sont `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1`, `review:3`. Ainsi, `C(NORMAL)=5/5` et `R(NORMAL)=3`. CONSTRAINED bloque `net_new_feature` et `broad_architecture` ; DRAINING bloque aussi `workflow_policy_change`. Parmi ces classes, seule `net_new_feature` possède une attribution : **les deux** modes gardent 8 arêtes et quatre classes couvertes, soit `C=4/5` et `R=3`. HALTED bloque en plus `fix`, `groom` et `navigate`, mais pas `review`. Il reste trois arêtes, toutes vers `review` : `C(HALTED)=1/5`, `R(HALTED)=1`. Ce ratio n'autorise aucune opération dans un système arrêté ; il décrit seulement les déclarations qui survivent à ce filtre.

### Exercice pratique 2 : calculer une coupure, pas une panne

En DRAINING, quelle arête de NORMAL disparaît ? Calculez `C` et `R`. Le résultat prouve-t-il qu'un agent Claude a effectivement cessé de travailler ?

> **Réponse :** Seule `claude → net_new_feature` disparaît : c'est l'unique arête attribuée de cette classe bloquée. Huit des neuf arêtes restent ; quatre classes sur cinq sont couvertes, donc `C=4/5`. `fix`, `groom` et `review` ont encore au moins deux agents voisins, donc `R=3`. C'est une coupure du graphe de politique, pas une observation d'un agent en cours d'exécution ou d'une répartition réelle.

## 3. Tester la fragilité face au retrait d'un agent

Pour le mode `m` et l'agent retiré `w`, définissons `L_m(w)` comme le nombre de classes couvertes avant retrait, mais découvertes ensuite. Supprimez `w` et ses chemins, puis recalculez les degrés. En DRAINING, seul `augment` rejoint `navigate` : son retrait fait passer ce degré de 1 à 0. Ainsi, `L_DRAINING(augment)=1` et la couverture passe de `4/5` à `3/5`. Retirer chacun des quatre autres agents ne fait perdre **aucune classe entière**, car un autre agent voisin subsiste. Cette suppression de sommet teste la sensibilité du graphe ; elle ne prédit aucune probabilité de panne. La politique ne mesure pas la disponibilité et une même classe ne garantit pas le rôle exact requis.

La redondance des classes diffère de celle des rôles. En DRAINING, `review` a trois agents voisins. Pourtant, le rôle primaire `read_only_critic` de `gemini`, le rôle secondaire `architecture_summarizer` de `jules` et les rôles secondaires de révision de `codex` ont des productions différentes. Le graphe maintient un chemin vers la classe générale `review`, sans garantir trois remplaçants pour chaque demande précise. Une réaffectation ou une remontée de décision peut rester nécessaire.

### Exercice pratique 3 : supprimer un sommet

Comparez le retrait de `augment` et celui de `codex` en DRAINING. Quelles classes disparaissent et quelle couverture reste-t-il ? Le graphe suffit-il pour comparer la qualité des notes de révision de remplacement ?

> **Réponse :** Retirer `augment` fait perdre `navigate` ; `fix`, `groom` et `review` restent, donc `C=3/5`. Retirer `codex` ne fait perdre aucune classe : `claude` garde `fix`, tandis que `jules` et `gemini` gardent `review`, donc `C=4/5`. Aucun résultat ne mesure la qualité, les permissions, l'équivalence des rôles, la disponibilité ou l'achèvement d'une tâche.

## 4. Garder la sémantique du sélecteur à côté du graphe

Le [sélecteur consultatif figé](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) lit cette politique. Il vérifie successivement l'agent et le mode inconnus, le rôle interdit, l'appartenance du rôle à la voie et le blocage de sa classe ([ordre de décision](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). Un rôle primaire attribué et non bloqué donne `allow` ; un secondaire donne `recommend`, non `allow`. Un rôle interdit donne `block` **avant** le test d'appartenance. Un rôle absent de la voie donne `warn`. Une classe bloquée donne `block` avec un code de backpressure. Ces valeurs sont des réponses du code, pas des autorisations de modifier l'état. Le code de sortie 0 signifie **évalué** ; la décision se lit dans le JSON. Une erreur d'entrée ou de politique peut donner le code 2.

En DRAINING, le rôle primaire `builder_fixer` de `claude` appartient à `net_new_feature`, bloquée, tandis que son rôle secondaire `test_author` appartient à `fix`, non bloquée. Le code prévoit respectivement `block` et `recommend`. Cela ne transforme pas `test_author` en constructeur de fonctionnalités : la demande et la production attendue doivent correspondre. Pour `codex`, `autonomous_merge_actor` est explicitement interdit, donc sa demande prévoit `block` même si le mode change. Aucune arête du graphe n'autorise une fusion.

### Exercice pratique 4 : distinguer chemins et décisions

En DRAINING, prévoyez les décisions pour `(claude, builder_fixer)`, `(claude, test_author)` et `(codex, autonomous_merge_actor)`. Quelle information la projection agent-classe perd-elle pour la dernière demande ?

> **Réponse :** La première donne `block`, car `net_new_feature` est bloquée ; la deuxième donne `recommend`, car `test_author` est un rôle `fix` *secondaire* non bloqué ; la troisième donne `block`, car `autonomous_merge_actor` figure dans la liste interdite de `codex`. La projection ne contient ni l'appartenance aux rôles interdits ni l'ordre des tests du sélecteur. L'absence d'arête vers une fusion ne signifie ni simple avertissement pour rôle inconnu ni permission d'agir.

## 5. Rendre la mesure réfutable

Les nombres ci-dessus proviennent du **JSON figé** : développement des rôles primaires et secondaires, correspondance avec `work_class`, filtrage par `mode_blocks`, puis déduplication des couples `(agent, classe)`. Un [script de rejeu hors ligne](../../../../../scripts/streeling_net003_replay.py) contrôle désormais séparément l'interprétation du sélecteur. Il compare les identifiants des blobs Git du sélecteur et de la politique présents dans le checkout à ceux du commit figé, puis énumère les 22 couples `(agent, rôle)` attribués dans chacun des quatre modes. `allow` et `recommend` comptent comme chemins attribués non bloqués ; `block` indique un chemin coupé par le mode. Le [reçu du rejeu du 12 octobre 2026](../../../reviews/net-003-selector-replay-2026-10-12.json) consigne **22, 21, 21, 8** chemins de rôle non bloqués pour NORMAL, CONSTRAINED, DRAINING et HALTED, **9, 8, 8, 3** arêtes agent-classe projetées et **5, 4, 4, 1** chemins primaires non bloqués. Tous ces résultats correspondent aux prévisions tirées de la politique et du sélecteur figés.

Le rejeu compare la décision du JSON plutôt que le code de sortie du processus. Ses contrôles distincts ont renvoyé `block` pour le rôle de fusion interdit à `codex`, `warn` pour un rôle inconnu et `escalate` pour un mode inconnu ; aucun ne fait partie des 22 couples attribués. Un écart dans les nombres ou les décisions réfuterait la règle supposée ou révélerait une dérive des sources. Cet accord valide le modèle limité pour la révision figée, sans établir l'ordonnancement réel, la santé des agents ou la qualité de la gouvernance humaine. Pour reproduire le reçu JSON, exécutez `python scripts/streeling_net003_replay.py` à la racine du dépôt Demerzel.

### Exercice pratique 5 : concevoir l'oracle de répétition

Supposons que `(claude, builder_fixer, DRAINING)` rende le code de sortie 0 et une décision JSON `block`. Un collègue compte un chemin actif puisque le processus a réussi. Quelle classification convient ? Donnez un nombre dont l'écart avec les prédictions réfuterait l'extraction du graphe.

> **Réponse :** C'est un **chemin vers un rôle attribué, mais bloqué**. Le code 0 indique que la demande consultative a été évaluée, pas autorisée. La répétition devrait trouver 21 chemins attribués non bloqués en DRAINING et 8 arêtes agent-classe après projection. En trouver 22 ou 9 respectivement avec la politique et le script figés réfuterait l'extraction. Cela ne prouverait pas à lui seul un incident de production.

## Preuves et limites

- La [politique des voies](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) et le [sélecteur](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) sont figés au commit Demerzel `ecdc6c27559bb1a11343cfad33687465893e9891`. Le rejeu local de la section 5 a vérifié les identifiants de leurs blobs Git avant d'utiliser les fichiers du checkout. Il s'agit d'un calcul reproductible et d'une invocation à blanc du sélecteur, pas d'une mesure d'agents actifs.
- Le graphe regroupe des rôles attribués distincts par classe. Il exclut les rôles interdits et ne porte ni l'ordre complet des décisions, ni les entrées, ni l'autorité du sélecteur. `allow` et `recommend` sont des valeurs consultatives ; aucune ne vaut reçu d'achèvement.
- Les retraits d'agents et les coupures de mode sont des expériences de sensibilité sur un graphe statique déclaré. Avant toute affirmation opérationnelle, vérifiez la révision actuelle de la politique, la demande et sa décision réelles, la présence et les permissions de l'agent, ainsi que l'artefact ou le reçu de la tâche. La révision disciplinaire, les essais d'apprenants, la révision de traduction, la synchronisation et compilation dans Learn, et la lecture publique anonyme restent en attente.
