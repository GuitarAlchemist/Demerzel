---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Composer les contraintes d’origami avant d’accepter un empilement rigide"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Composer les contraintes d’origami avant d’accepter un empilement rigide

> **Département d’informatique** | Niveau intermédiaire | 40 minutes | Version française provisoire ; validation du contenu et évaluation par un apprenant en attente

## Objectifs et question pour le projet

Vous transformerez les jonctions à plat en classes d’équivalence, conserverez les contraintes orientées entre ces classes, distinguerez les tests locaux de recouvrement d’une contrainte globale d’empilement et lirez un résultat incomplet sans inventer de placement. La question pratique est : **quel résultat un agent peut-il transmettre à un futur adaptateur Blender ou Godot après la vérification d’un état d’origami par IX ?** La représentation visuelle d’un objet à fabriquer exige une interprétation explicite de l’analyse : la réussite d’une vérification peut coexister avec un refus dans un autre modèle.

L’étude de cas porte sur le [module d’épaisseur d’IX](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) et ses [tests d’intégration](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), tous deux figés à la révision `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. Le module lit une épaisseur de matériau exprimée dans les unités des coordonnées du patron de plis. Il examine un état replié à plat donné ; il ne planifie pas le mouvement de pliage et n’exporte pas de scène. Le [jeu de données du cours](../../../fixtures/computer-science/cs-009/README.md) contient de petites démonstrations sur des graphes, clairement séparées des résultats réels des tests Rust.

## 1. Regrouper d’abord les faces en panneaux

Une face est un polygone dans la description de l’état plié. Dans ce modèle, un panneau est un ensemble de faces reliées par des jonctions à plat et devant conserver une même hauteur. La fonction `panels` de l’implémentation réunit leurs ensembles et associe chaque face à la face de plus petit indice de sa composante connexe. Ce représentant est une étiquette algorithmique. Ce n’est pas un identifiant permanent d’objet : renuméroter l’entrée peut le modifier tout en conservant le panneau représenté.

Considérons les faces 0, 1 et 2. Les faces 0 et 1 partagent une jonction à plat. Les relations données placent 2 au-dessus de 0 et 1 au-dessus de 2. Dans le graphe des faces, les arcs allant du bas vers le haut sont `0 → 2 → 1`, sans cycle. Si chaque face reçoit sa propre hauteur, la réponse semble être les niveaux 0, 1 et 2. Elle viole pourtant le modèle : les faces 0 et 1 appartiennent au même panneau rigide et ne peuvent pas avoir des hauteurs différentes.

Après réunion des faces reliées à plat, la correspondance des panneaux est `[0, 0, 2]`. Les deux contraintes deviennent `panneau 0 → panneau 2` et `panneau 2 → panneau 0`. Le cycle apparaît alors. Il s’agit d’une construction par quotient : regrouper d’abord les objets qui doivent se déplacer ensemble, puis appliquer les contraintes d’ordre à ces groupes. Vérifier chaque partie avant de les composer fait manquer l’exigence introduite par leur identité commune.

### Exercice 1 : corriger le graphe trompeur

Utilisez le cas `pierced-flat-joint` du jeu de données. Donnez les représentants des panneaux et les deux arcs entre panneaux. Expliquez pourquoi l’ordre topologique du graphe des faces ne peut pas justifier un placement rigide. Quelle décision d’implémentation supplémentaire faudrait-il prendre si un adaptateur exigeait un identifiant permanent de panneau ?

> **Réponse :** Les représentants sont `[0, 0, 2]` ; les arcs sont `0 → 2` et `2 → 0`. L’ordre des faces autorise deux hauteurs différentes pour un même panneau relié à plat : il résout donc le mauvais système de contraintes. Un identifiant permanent de panneau nécessiterait une correspondance déclarée avec l’identité du matériau ou de la source, conservée malgré les modifications ou permutations. Le représentant de plus petit indice n’offre pas, à lui seul, cette garantie.

## 2. Une réussite locale peut coexister avec un refus global

Le test figé `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` construit quatre bandes. Chacune recouvre la suivante dans un coin différent. Chaque cellule locale de la superposition peut admettre un ordre cohérent ; pourtant, les énoncés réunis disent que la bande 0 est au-dessus de 1, 1 au-dessus de 2, 2 au-dessus de 3 et 3 au-dessus de 0. Les arcs allant du bas vers le haut donnent `0 → 3 → 2 → 1 → 0`. Pour une épaisseur de matériau positive, aucune hauteur unique par bande ne satisfait les quatre inégalités.

Ce problème diffère de celui de [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), dont le vérificateur synthétique détecte un redémarrage de la parité aux frontières de tuiles répétées. Ici, le problème est un cycle traversant différentes régions de recouvrement dans l’implémentation existante d’IX. Une texture, un aperçu d’un croisement local ou la réussite de l’analyse de base de l’origami ne tranche pas la question globale des panneaux parallèles.

Le test vérifie que `analyse(&weave()).unwrap().ok` est vrai. Il vérifie aussi la lecture optionnelle de l’épaisseur pour `t = 0`, un très petit `t` positif et `t = 0.5`. Le graphe reste cyclique, mais `rigid.refused` n’est vrai que pour un `t` positif. À zéro, l’implémentation renvoie toujours `levels`, `height` et `face_levels` comme absents pour cette lecture cyclique. Ne remplacez pas une hauteur rigide absente par zéro au motif que la valeur distincte `ply_height` vaut zéro.

### Exercice 2 : interpréter le cas nul

L’entrelacs a `ply = 2` et un ordre cyclique des panneaux. Que valent `ply_height` et `rigid.refused` pour `t = 0` et `t = 0.5` ? L’un de ces résultats fournit-il une affectation des niveaux des faces rigides ?

> **Réponse :** À zéro, `ply_height = 0` et `rigid.refused = false` ; à 0.5, `ply_height = 1` et le refus est vrai. Dans les deux rapports cycliques, les niveaux rigides, la hauteur rigide et l’affectation des niveaux des faces sont absents. L’absence de refus à épaisseur nulle ne fournit pas le témoin manquant ; le refus à épaisseur positive concerne ce modèle de panneaux parallèles.

## 3. Des contraintes acycliques permettent un calcul de plus long chemin

Lorsque le graphe des panneaux admet un ordre topologique, l’implémentation initialise chaque niveau à zéro. Pour chaque arête orientée allant d’un panneau inférieur `u` à un panneau supérieur `v`, elle met à jour `level[v] = max(level[v], level[u] + 1)`. Le traitement dans l’ordre topologique garantit que le niveau de chaque prédécesseur est disponible. Le niveau maximal, dont la numérotation commence à zéro, augmenté de un donne la longueur de la chaîne en panneaux. La multiplication par l’épaisseur totale `t` donne la hauteur de l’empilement pour un ordre entièrement déterminé.

La valeur `face_levels` rapportée est un témoin produit par cette récurrence. D’autres empilements valides peuvent exister ; les valeurs par face ne constituent pas un étiquetage canonique de tous les empilements admissibles.

Le DAG synthétique du jeu de données comporte les arcs `P → R`, `Q → R` et `R → S`. P et Q peuvent partager le niveau zéro, car l’exemple ne fournit aucune relation imposant leur séparation ; R doit être au-dessus des deux, puis S au-dessus de R. Il s’agit de données de graphe abstraites, pas d’une géométrie FOLD exportée ni d’une affirmation sur le recouvrement spatial. Elles servent à s’exercer à la récurrence avant de lire le test, plus volumineux, de la grue.

### Exercice 3 : calculer la chaîne

Attribuez les niveaux aux quatre panneaux du DAG synthétique, comptez les panneaux de la plus longue chaîne et calculez la hauteur pour `t = 0.2`. Pourquoi rapporter seulement le niveau maximal produirait-il une erreur de décalage de un ? À titre de comparaison, quels sont les deux nombres distingués par le test réel de la grue ?

> **Réponse :** P et Q sont à 0, R à 1 et S à 2. La chaîne comporte trois panneaux ; la hauteur vaut donc `3 × 0.2 = 0.6` dans les unités du patron de plis. L’indice maximal 2 omet un niveau occupé. Le test réel de la grue distingue une superposition locale maximale de 28 épaisseurs de feuille des 36 niveaux de panneaux parallèles nécessaires ; l’occupation locale et une chaîne traversant plusieurs régions répondent à des questions différentes.

## 4. L’ordre manquant fait partie du résultat

L’implémentation compte les paires de faces qui se recouvrent, appartiennent à des panneaux différents et dont l’ordre n’est pas précisé. Dès qu’une telle paire existe, `levels_exact` est faux. Elle rapporte `max(chain, ply)` comme borne inférieure et ne fournit pas `face_levels`. Des contraintes données acycliques ne suffisent pas à certifier qu’un placement proposé respecte une relation que l’entrée n’a jamais spécifiée.

Le test figé `an_unstated_overlap_gives_a_lower_bound` utilise deux feuilles qui se recouvrent sans ordre donné. Il attend une paire indéterminée, deux niveaux comme borne inférieure et aucune affectation des niveaux des faces. L’appelant doit conserver l’indicateur d’exactitude avec le nombre. Si le résumé d’un agent l’omet, une étape ultérieure risque de transformer une borne inférieure en arrangement prétendument complet sans que personne ait pris explicitement cette décision.

### Exercice 4 : conserver l’incertitude dans une transmission

La fiche synthétique d’ordre incomplet a une chaîne de 2, un `ply` de 3, une paire indéterminée et `t = 0.2`. Quelle hauteur numérique l’algorithme peut-il rapporter, et comment faut-il la qualifier ? Un adaptateur de scène peut-il s’en servir pour placer toutes les faces ?

> **Réponse :** Il rapporte `max(2, 3) = 3` niveaux et une borne inférieure de hauteur de 0.6, avec `levels_exact = false` et `face_levels = null`. Il ne peut pas fournir un placement complet. Une transmission doit conserver la qualification de borne inférieure, le nombre de paires dont l’ordre manque, l’identité de la source et l’absence de témoin, sans promettre des coordonnées déduites d’un ordre non observé.

## 5. Faire du résultat une décision vérifiable

Une composition agentique peut transporter ensemble l’analyse de base et la lecture rigide. La [décision de conception figée](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) conserve explicitement la lecture de l’épaisseur à côté du verdict de base. Un refus signifie qu’aucun empilement n’existe sous les hypothèses de panneaux rigides parallèles. Il ne prouve pas qu’un objet matériel soit impossible avec des panneaux inclinés, des plis modifiés ou d’autres méthodes de construction. Inversement, l’absence de refus ne prouve pas la faisabilité de fabrication.

Pour un essai Godot proposé, conservez la révision du FOLD source, la conversion de l’épaisseur totale et des unités, les deux résultats d’analyse, tout témoin de cycle, l’exactitude et la correspondance entre faces et objets. Donnez à l’observateur une tâche précise, par exemple trouver la relation responsable d’un refus. Comparez sa réponse à celle obtenue avec un simple diagramme du graphe pour la même tâche. Il s’agit d’une expérience de transfert proposée ; le cours ne consigne aucun moteur de rendu, export, essai avec un apprenant ou gain de performance. Un nouveau DSL ne justifierait son coût que s’il améliorait la réalisation de cette tâche par rapport à un rapport typé plus simple et au vérificateur existant.

### Exercice 5 : décider quoi transmettre en aval

Un futur agent rapporte : « analyse de base réussie ; refus rigide à épaisseur positive ; faces du cycle `[0,3], [3,2], [2,1], [1,0]` ». Il propose d’étiqueter l’objet « physiquement impossible » et d’omettre le cycle parce que la scène semble plausible. Rédigez une formulation corrigée destinée à l’utilisateur et indiquez les preuves nécessaires à une démonstration en scène.

> **Réponse :** « L’état donné a passé les vérifications de base, mais l’ordre donné contient un cycle qui empêche un empilement de panneaux rigides parallèles à cette épaisseur positive. » Conservez le cycle et les hypothèses. Une démonstration en scène nécessite un import rattaché à la source, une correspondance entre faces et objets, un affichage du cycle vérifiable indépendamment et une tâche d’observation consignée. Une capture d’écran ne suffit pas à établir le résultat du graphe, l’impossibilité physique ou un bénéfice pédagogique.

## Rejouer les tests et comprendre les limites

Exécutez `cargo test -p ix-origami --test thickness` dans IX à la révision figée. Le coordinateur a rejoué les 11 tests d’intégration d’épaisseur le 2026-10-21 : 11 réussis, 0 échec. Le README du jeu de données consigne les blobs de la source et des tests. Les fiches de graphes sont des données pédagogiques dérivées à la main ; aucun analyseur supplémentaire ni runtime consommateur n’est introduit. La réussite de ces tests étaye les cas d’implémentation décrits ; l’exactitude du contenu, la qualité idiomatique des traductions, la réussite des apprenants, l’import de scène et la publication Learn vérifiée sans authentification restent des travaux distincts.
