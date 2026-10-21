---
module_id: cyb-003-measuring-variety-ratio-quantitatively
department: cybernetics
course: Mesurer la variété requise sans inventer une capacité
level: intermediate
prerequisites: [cyb-001-vsm-ai-governance-mapping, cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: cybernetics-2026-10-21-003
version: "0.2.0"
---

# Mesurer la variété requise sans inventer une capacité

> **Département de cybernétique** | Niveau : intermédiaire | Durée : 35 minutes | Statut : relectures thématique, apprenant et linguistique en attente

## Objectifs

Après ce cours, vous pourrez :

- distinguer les étiquettes possibles d'un schéma, les états observés dans un échantillon et les réponses régulatrices efficaces ;
- calculer la variété maximale d'un alphabet fini et l'entropie empirique d'un échantillon sans les confondre avec la qualité de la gouvernance ;
- expliquer pourquoi les nombres de politiques, de personas et de productions grammaticales ne forment pas un « ratio de variété » pertinent ;
- concevoir pour Demerzel une expérience appariant perturbation, réponse et issue.

## Le problème du projet

La première version de CYB-003 annonçait des ratios comportementaux et régulateurs « sains » ainsi qu'un « déficit régulateur de 3 bits ». Elle additionnait des logarithmes de nombres de fichiers, de seuils et d'interactions supposées entre politiques. Ces nombres ne représentaient ni des perturbations distinguables ni des réponses efficaces dans une tâche définie. Les plages dites saines n'avaient pas de fondement mesuré. **Ces conclusions sont retirées.** Les calculs ci-dessous utilisent des données du projet, sans prétendre mesurer sa capacité opérationnelle.

L'exemple est figé à la révision Demerzel [66083fc](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f). Consultez le [schéma de production des cours](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) et les [huit enregistrements](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions). Le [script de rejeu](../../../fixtures/cybernetics/cyb-003/README.md) vérifie les nombres dans un checkout contenant cette révision. Cet instantané historique ne décrit pas l'état actuel du pipeline.

## 1. Définir l'ensemble avant de compter

La variété d'Ashby porte sur les états distinguables d'un **ensemble défini**. Si ses N états sont possibles, sa variété maximale vaut log2(N) bits. Le choix de l'ensemble et les distinctions observables comptent. Un schéma énumère des *symboles permis* ; il ne dit pas à quelle fréquence ils surviennent, si toutes leurs combinaisons sont possibles, ni si un contrôleur sait traiter une perturbation. Le [texte original d'Ashby](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf) distingue états possibles, états observés et régulation.

À la révision figée, le schéma autorise cinq valeurs de status : in_progress, review_pending, published, rejected et failed. Il autorise également trois valeurs de review.verdict : approved, revise et reject. Ce verdict est facultatif dans le schéma et absent des huit enregistrements examinés. Sept enregistrements ont le statut in_progress ; un seul, review_pending.

| Question | Réponse tirée de la source figée | Ce que cela ne démontre **pas** |
|---|---:|---|
| Combien d'étiquettes de statut sont configurées ? | 5 | Cinq comportements exercés |
| Combien d'étiquettes de statut apparaissent dans l'échantillon ? | 2 | Toute la plage de fonctionnement |
| Combien d'enregistrements sont examinés ? | 8 | Une série temporelle représentative |
| Combien portent un verdict de revue ? | 0 | La capacité ou la qualité des relecteurs |

### Exercice pratique 1

Calculez la variété maximale de l'alphabet des statuts configurés, puis celle des deux statuts observés. Peut-on appeler l'un ou l'autre nombre la capacité régulatrice de Demerzel ?

> **Réponse :** log2(5) ≈ 2,322 bits pour l'alphabet configuré ; log2(2) = 1 bit pour les deux étiquettes observées. Aucun ne mesure la capacité régulatrice : ils comptent des étiquettes, pas des réponses distinctes et efficaces à des perturbations définies.

## 2. Une distribution échantillonnée répond à une autre question

L'entropie de Shannon d'une distribution échantillonnée vaut H = -Σ p(x) log2 p(x). Dans les huit enregistrements figés, les fréquences des statuts sont 7/8 et 1/8 ; H ≈ 0,544 bit par statut échantillonné. C'est une statistique descriptive de ce petit échantillon choisi d'enregistrements de production, pas une prévision du comportement futur des agents. La formule vient de [l'article original de Shannon](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).

L'alphabet configuré, l'alphabet observé et l'entropie empirique mesurent des choses différentes. N'additionnez pas la variété de « cinq statuts » à celle de « trois verdicts » : le verdict peut manquer, les phases restreignent les combinaisons plausibles et leur indépendance n'est pas établie. Le calcul log2(5 × 3) ≈ 3,907 décrit seulement un ensemble hypothétique de **15 paires d'étiquettes sans valeur manquante**. Si l'absence de verdict devient un quatrième symbole, le produit cartésien sans contrainte contient 20 paires. Aucun des deux nombres n'établit quelles paires sont accessibles ou utiles.

### Exercice pratique 2

Recalculez l'entropie empirique à partir du tableau, puis expliquez pourquoi log2(8) = 3 bits ne répond pas à la question.

> **Réponse :** -(7/8)log2(7/8) -(1/8)log2(1/8) ≈ 0,544 bit. Huit est le nombre d'enregistrements, et non celui des statuts distincts. log2(8) mesurerait la possibilité d'identifier un enregistrement parmi huit si son identité était la variable choisie : c'est une autre question.

### Exercice pratique 3

Un tableau de bord multiplie cinq statuts par trois verdicts, appelle le résultat « 15 réponses du régulateur » et présente 3,907 bits comme preuve d'une gouvernance adéquate. Repérez deux étapes injustifiées.

> **Réponse :** Il suppose que toutes les combinaisons statut/verdict sont valides et accessibles, alors que le verdict est facultatif et que les phases imposent des contraintes. Il remplace aussi les réponses réellement éprouvées face aux perturbations par des symboles de schéma : aucune perturbation, action choisie ou issue n'a été mesurée.

## 3. Mesurer une véritable tâche de régulation

Pour éprouver la variété requise, il faut définir la **perturbation** (ce qui échoue), la **réponse** (ce que fait le contrôleur) et une **issue essentielle** (ce qui doit rester dans les limites). Pour la production de cours, un essai proposé présenterait trois échecs distincts : une fixture absente, une source de preuve illisible et une réponse d'exercice incompatible avec sa fixture. Le système pourrait réparer la fixture, demander l'accès ou corriger la réponse, puis émettre un reçu. Il s'agit de **cas d'essai proposés**, non d'observations du comportement actuel de Demerzel.

Avant l'essai, consignez la fixture d'entrée, la distinction attendue, l'action permise, le délai et la règle de réussite. Exécutez chaque cas et conservez la décision et son issue. Répondre simplement « réessayer » aux trois cas révèle une distinction manquante, même si le contrôleur possède de nombreux fichiers de politiques. Inversement, trois étiquettes différentes ne servent à rien si elles produisent le même artefact incorrect. Comptez les *distinctions efficaces pour cette tâche*, et non les noms présents dans le dépôt.

| Perturbation proposée | Indice distinctif | Réponse possible | Issue vérifiable |
|---|---|---|---|
| Fixture absente | Le chemin déclaré n'existe pas | Réparer ou bloquer en nommant le chemin manquant | Le reçu nomme la fixture absente ; aucun résultat inventé |
| Source illisible | La tentative de lecture échoue | Demander l'accès ou utiliser une source explicitement permise | Le reçu nomme la lecture échouée et sa portée |
| Réponse incohérente | Le calcul reproduit donne un résultat différent | Corriger la réponse, puis rejouer l'exercice | La nouvelle réponse concorde avec la fixture fixée |

Ce tableau est un protocole expérimental. Il ne permet pas d'établir un ratio réponses/perturbations sans essais appariés et issues observées. Même ensuite, un simple ratio d'entropies ignorerait quelle réponse convient à quelle perturbation. Présentez la matrice de confusion et la réussite de la tâche avec toute mesure d'information.

**Une borne conditionnelle d'Ashby.** La grammaire révisée du projet énonce une borne sur les *issues*, non sur le nombre de fichiers de politiques. Dans un cycle où chaque perturbation reçoit une réponse et où une même réponse ne mène jamais deux perturbations différentes à la même issue, le plus grand groupe associé à une réponse contient au moins N_D/N_R perturbations aux issues distinctes. Donc N_O ≥ N_D/N_R, ou V_O ≥ V_D - V_R pour des nombres positifs. Si une seule réponse amène plusieurs perturbations à la même issue acceptable, cette déduction ne s'applique pas : quatre perturbations peuvent partager une réponse et une issue. Aucun des deux cas ne prouve que les issues observées sont acceptables. Enregistrez chaque perturbation, réponse et issue essentielle avant d'appliquer la borne ; la fixture portant sur les étiquettes du schéma ne contient aucune de ces observations.

### Exercice pratique 4

Un agent rencontre une source illisible, mais écrit « revue approuvée » après l'avoir ignorée sans le signaler. Quels champs le reçu de rejeu doit-il exposer ? La régulation a-t-elle réussi ?

> **Réponse :** Il faut enregistrer la source et sa révision, la tentative de lecture, l'erreur, une éventuelle source de repli autorisée, l'action choisie et l'issue finale. Sans cette preuve, l'approbation n'est pas étayée ; l'issue sûre est un blocage ou une revue en attente, pas une réussite.

### Exercice pratique 5

Proposez un moyen de réfuter l'affirmation « ajouter une quatrième politique de gouvernance a amélioré la régulation de la revue des cours ».

> **Réponse :** Gardez les fixtures de perturbation et la règle de réussite identiques ; comparez les décisions de revue et les issues vérifiées indépendamment avant et après l'ajout. Si la politique ne réduit pas les approbations non étayées ou les cas non résolus, ou si elle les augmente, cet essai n'appuie pas l'affirmation. Mesurez aussi le temps de préparation et de revue : un texte supplémentaire peut coûter plus cher sans améliorer les décisions.

## 4. Quoi rapporter ensuite

Un tableau de bord utile présenterait séparément l'alphabet des états configurés, les fréquences des états observés, les verdicts manquants et les issues d'essais appariés. Il indiquerait la révision du dépôt et la méthode de sélection de l'échantillon. Il n'affirmerait pas de plage « saine » pour un ratio qui n'a pas été validé au regard des issues de gouvernance ou des utilisateurs. Pour éprouver une amélioration récurrente, répétez la même série de perturbations entre révisions et suivez les réussites vérifiées indépendamment, les cas non résolus et l'effort de bout en bout. Une boucle plus courte n'est meilleure que si elle produit davantage de décisions justes sans reporter le travail dans une file de revue invisible.

Ce constat rejoint aussi [la boucle audio agentique contrôlée de CS-004](../../../fixtures/computer-science/cs-004/recursive-improvement-evidence.json) : les échecs de lecture d'une source et un comparateur insensible ont conduit à expliciter le harness et l'évaluation. Ces quelques cycles observés montrent un apprentissage local, pas un progrès exponentiel.

## Sources et limites

- [Schéma de production des cours de Demerzel](https://github.com/GuitarAlchemist/Demerzel/blob/66083fc684b57a12ef307c19c3819d91c551295f/schemas/course-production.schema.json) et [enregistrements figés](https://github.com/GuitarAlchemist/Demerzel/tree/66083fc684b57a12ef307c19c3819d91c551295f/state/streeling/course-productions) ; les nombres sont vérifiés par la [fixture de rejeu locale](../../../fixtures/cybernetics/cyb-003/README.md).
- W. Ross Ashby, [*An Introduction to Cybernetics*](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf), chapitres 7 et 11 ; C. E. Shannon, [*A Mathematical Theory of Communication*](https://reach.ieee.org/primary-sources/a-mathematical-theory-of-communication/).
- Ces huit enregistrements forment un échantillon historique choisi. Nous n'avions ni journal appariant perturbations, réponses et issues, ni essai par un apprenant. Les relectures thématique et linguistique restent en attente.
