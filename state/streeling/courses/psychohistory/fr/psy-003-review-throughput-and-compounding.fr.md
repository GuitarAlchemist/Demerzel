---
module_id: psy-003-review-throughput-and-compounding
department: psychohistory
course: "Mesurer l'amélioration récursive, de la revue à la publication"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-002-governance-phase-transitions"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: psychohistory-2026-10-12-003
version: "0.1.0"
---

# Mesurer l'amélioration récursive, de la revue à la publication

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous distinguerez le travail mesuré d'une hypothèse de débit, vous calculerez deux files d'attente sur quatre cycles hebdomadaires, et vous définirez un critère de réfutation pour une amélioration récursive proposée. **Question de projet :** si les agents de Streeling rédigent des cours plus vite, le projet atteindra-t-il réellement plus vite 25 cours utiles, revus et publics dans chacun de 21 départements ? La réponse dépend de chaque étape du chemin, y compris des verdicts humains et de la vérification publique. Des brouillons plus nombreux ne suffisent pas, à eux seuls, à l'établir.

[PSY-001 au commit `4b03838` de Demerzel](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) introduit une analogie, la « capitalisation fractale ». [PSY-002 au même commit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit le changement de gouvernance comme une transition de phase, mais présente ses frontières de régime comme choisies et non mesurées, et avertit qu'un ratio de variété qui franchit 1,0 n'est pas en soi une transition de phase. Nous rendons ici cette même discipline opérationnelle : une boucle d'amélioration répétée est une *explication candidate* d'un débit croissant, non la preuve d'un progrès exponentiel. Ni l'étiquette de loi de puissance ni une analogie avec un théorème de conservation de la physique n'établissent un rythme de livraison mesuré.

## 1. Partir d'une limite observée

L'[instantané épinglé des candidats à la revue](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) indique **21** dossiers de cours, un objectif provisoire de **525** cours du tronc commun, **113** codes distincts du tronc commun, **114** modules anglais rédigés, parce qu'un cours optionnel se situe au-delà des 25 premiers codes de son département, **neuf** sources présentes dans les six langues actives et comptant au moins cinq paires exercice-réponse détectables, et **quatre** dossiers de relecture intégrés au dépôt. À cette révision source, l'outil de suivi d'avancement a enregistré **zéro drapeau de revue de production approuvé**. Ce sont des observations sur les sources et sur le tri, non un décompte d'apprentissages humains ou de pages publiées. Le [générateur](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_review_candidates.py) épingle chaque fichier source listé à un blob Git et indique explicitement qu'un fichier, un signal de réponse ou un dossier n'est pas une revue authentifiée.

Sur la base provisoire des 21 dossiers, il reste `525 − 113 = 412` codes du tronc commun. Ce calcul ne signifie pas que 113 cours sont prêts à être enseignés : l'exactitude du contenu, la qualité vérifiable des exercices, le sens des traductions, le résultat réel pour l'apprenant, l'intégration, le déploiement et la vérification publique anonyme sont des portes distinctes. Il n'explique pas non plus pourquoi le dépôt compte 23 fiches de département ; le [ticket #1209](https://github.com/GuitarAlchemist/Demerzel/issues/1209) suit la question du périmètre, dossiers ou fiches. Utilisez le dénominateur déclaré pour une évaluation, et réexaminez-le si l'institution change sa définition d'un département.

### Exercice pratique 1

Calculez les codes du tronc commun restants à partir des décomptes épinglés des sources. Pourquoi l'inventaire peut-il afficher à juste titre 114 modules anglais, mais seulement 113 codes du tronc commun ? Pourquoi zéro drapeau de revue de production approuvé ne signifie-t-il pas zéro contenu rédigé ?

> **Réponse :** `21 × 25 = 525` ; il reste `525 − 113 = 412` codes du tronc commun. Le décompte des modules rédigés inclut un cours optionnel dont le code sort de la séquence 001–025 de son département ; il n'augmente donc pas l'objectif du tronc commun. Les drapeaux de revue suivent une étape ultérieure du pipeline ; 114 fichiers sources anglais peuvent exister sans qu'aucun ne porte de drapeau de revue de production approuvé enregistré. Même un drapeau positif demanderait qu'un humain vérifie l'attestation avant toute affirmation publique sur la qualité.

## 2. Modéliser les files avant de promettre un débit

Les [données d'entrée des scénarios](../../../fixtures/psychohistory/psy-003/scenarios.json), le [simulateur](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py) et le [résultat enregistré](../../../fixtures/psychohistory/psy-003/results.json) forment un **jeu d'essai pédagogique synthétique de quatre semaines**. Exécutez `python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check` à la racine de Demerzel pour le reproduire ; le [README du jeu d'essai](../../../fixtures/psychohistory/psy-003/README.md) énumère ses autocontrôles. Il suppose **12 nouveaux éléments prêts pour la revue par semaine**, à partir de files de revue et de publication vides. Cette hypothèse est volontairement distincte des neuf *candidats au tri* observés plus haut : être candidat ne rend pas un cours prêt pour la revue.

Chaque semaine, ajoutez les nouveaux éléments prêts à la file de revue ; acceptez au plus autant d'éléments que le permet la capacité de revue, et pas plus qu'il n'y en a de disponibles ; faites passer les éléments acceptés dans la file de publication ; publiez au plus autant d'éléments que le permet la capacité de publication, et pas plus qu'il n'y a d'éléments acceptés disponibles. Le modèle suppose que chaque revue terminée renvoie `approved` et que chaque cours approuvé est déployable. En réalité, un relecteur peut demander des modifications, une revue de langue peut rester en attente, une génération du site peut échouer, et une vérification publique peut ne pas concorder. Les « acceptés » et les « publiés » du modèle sont donc des **bornes supérieures optimistes**, non des mesures actuelles de Streeling.

```text
reviewed_t  = min(waiting_review_t + new_ready_t, review_capacity_t)
waiting_review_(t+1) = waiting_review_t + new_ready_t - reviewed_t
published_t = min(waiting_publication_t + reviewed_t, publication_capacity_t)
waiting_publication_(t+1) = waiting_publication_t + reviewed_t - published_t
```

Les contrôles de conservation sont utiles : sur les quatre semaines, le total des nouveaux éléments prêts est égal aux éléments acceptés plus la file de revue finale ; le total des éléments acceptés est égal aux éléments publiés plus la file de publication finale. Si un tableau de bord enfreint l'une ou l'autre de ces identités sans décompte explicite des rejets ou des retraits, la comptabilité des étapes est fausse. Le modèle ne représente **pas** les demandes de modification, la reprise ni les différentes sortes de revue. Il leur faudrait leurs propres états avant que l'outil puisse estimer le débit réel.

### Exercice pratique 2

Dans le scénario `flat`, les capacités hebdomadaires d'acceptation en revue et de publication valent toutes deux quatre. Avec 12 nouveaux éléments prêts chaque semaine et des files initialement vides, calculez la file de revue à l'issue de chacune des quatre semaines, le total des éléments acceptés, le total des éléments publiés et la file de publication finale.

> **Réponse :** La file de revue s'allonge de huit éléments par semaine : `8, 16, 24, 32`. Chaque semaine, quatre éléments sont acceptés, dans l'hypothèse optimiste, et quatre sont publiés, soit 16 acceptés et 16 publiés au total. La file de publication finale est vide. Ce n'est pas une performance observée ; le rythme d'arrivée synthétique dépasse la capacité de revue fixe.

## 3. Une étape intermédiaire plus rapide peut déplacer le goulot d'étranglement

Le second scénario fixe les capacités d'acceptation en revue à `4, 8, 16, 32`, tandis que la capacité de publication reste de quatre par semaine. Ce doublement est une **hypothèse sur la capacité humaine et opérationnelle disponible**, non un bénéfice gratuit de l'ajout d'agents. Les nombres effectifs d'éléments acceptés sont `4, 8, 16, 20` : la quatrième semaine, une fois les nouvelles arrivées comptées, seuls 20 éléments sont disponibles, si bien qu'une capacité de 32 reste en partie inutilisée. Au bout de quatre semaines, les 48 nouveaux éléments prêts hypothétiques sont tous acceptés et la file de revue est vide. Seuls 16 sont publiés ; **32 attendent la publication**. Si l'étape de publication réelle exige une approbation du déploiement, une génération du site et une vérification publique, davantage d'automatisation de la revue ne peut à elle seule résorber cette file.

C'est là ce qui compte dans une amélioration récursive, plutôt qu'une promesse sur sa forme. Un meilleur vérificateur de terminologie ou un meilleur dossier pour les relecteurs pourrait réduire le temps de ces derniers. Encore faut-il mesurer s'il augmente le nombre de verdicts d'acceptation de qualité égale, s'il reporte le retard sur la revue de langue ou sur le déploiement, et si les pages publiées sont réellement correctes. Un outil qui fait paraître rapide l'étape du milieu tout en multipliant les corrections en aval n'a pas capitalisé de production utile. Le [projet d'attestation de revue](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json) distinguerait les verdicts de fond, de langue et d'apprenant par blob source exact, mais il reste dans une pull request à l'état de brouillon, en attente d'une revue humaine du schéma.

### Exercice pratique 3

Prenez le scénario `growing_review_fixed_publication`. Donnez les nombres effectifs d'éléments acceptés par semaine, les totaux finaux d'éléments acceptés et publiés, et les deux files finales. Pourquoi la capacité de 32 de la quatrième semaine n'est-elle pas entièrement utilisée ?

> **Réponse :** Les nombres effectifs d'éléments acceptés sont `4, 8, 16, 20`. Les totaux sont de 48 acceptés et 16 publiés. La file de revue est vide et la file de publication contient 32 éléments. La quatrième semaine, huit éléments attendaient et 12 nouveaux sont arrivés : seuls 20 pouvaient donc être acceptés, et la capacité restante de 12 n'avait rien à traiter. Le scénario ne prouve pas que de vraies personnes pourraient ou voudraient approuver à ces rythmes.

## 4. Tester une amélioration récursive sur tout le chemin

Pour tester un changement réel, consignez une fenêtre de référence et l'intervention : quel outil ou quelle pratique a changé, qui l'a utilisé, quels cours et quels blobs sources exacts sont entrés dans chaque file, quand ils y sont entrés et quand ils en sont sortis, et pourquoi des éléments ont été rejetés ou renvoyés. Suivez au moins quatre productions hebdomadaires distinctes : les nouveaux brouillons comptant cinq exercices avec réponse, les verdicts **humains** de fond ou de langue rendus, les fusions ou déploiements acceptés, et les pages publiques vérifiées anonymement à la révision source prévue. Suivez aussi le taux de reprise et le temps des relecteurs. Gardez le dénominateur fixe, ou signalez un changement de périmètre. Comparez des cohortes de complexité de cours et d'exigences linguistiques semblables ; sinon, une cohorte facile peut produire une fausse amélioration.

Une règle de **contre-pression sémantique** (*semantic backpressure*), à l'état de proposition, peut orienter l'effort limité des agents vers la réparation des éléments de preuve quand une étape en aval est surchargée. Par exemple, une longue file de revue peut justifier d'améliorer les dossiers pour les relecteurs, la parité des traductions ou la clarté des réponses. Une longue file de publication peut justifier de contrôler le déploiement, le verrouillage de la source et la vérification publique. C'est une hypothèse d'allocation, non un ordonnanceur implémenté dans Streeling ni une raison d'abandonner les 412 cours du tronc commun restants. Si la règle allonge l'attente sans augmenter le nombre de cours acceptés, publics et utilisables par les apprenants, rejetez-la ou révisez-la. Un modèle plus rapide ne peut pas franchir une porte humaine en s'approuvant lui-même.

Définissez un critère de réfutation *avant* l'intervention. Un essai pilote raisonnable pourrait exiger une hausse durable du nombre hebdomadaire de cours dotés de verdicts humains authentifiés **et** d'une vérification publique, sans hausse du taux de correction ni des échecs d'apprenants non résolus. Si seuls les brouillons rédigés augmentent, ou seule la confiance d'un modèle, l'intervention n'a pas démontré de progrès de bout en bout. Si les pages publiées augmentent pendant que les éléments de preuve ou la qualité diminuent, le gain apparent n'est pas l'objectif. Quatre semaines du tableau synthétique ne peuvent pas tenir lieu d'un tel essai pilote.

### Exercice pratique 4

Une équipe rapporte que son nouveau flux de travail d'agents a fait passer les brouillons de 12 à 24 par semaine, tandis que les approbations humaines vérifiées restent à quatre et les vérifications publiques à quatre. Nommez un indicateur avancé qui s'est amélioré, un indicateur de résultat qui ne l'a pas fait, et un critère de réfutation pour l'affirmation selon laquelle ce flux de travail a accéléré la livraison.

> **Réponse :** La création de brouillons est passée de 12 à 24 par semaine. Les vérifications publiques confirmées, un résultat plus proche de l'objectif visé, sont restées à quatre ; les approbations humaines sont elles aussi restées à quatre. Un critère de réfutation déclaré d'avance : après le changement, des cohortes comparables ne montrent aucune hausse durable des approbations authentifiées et des vérifications publiques correctes, ou bien les reprises ou les échecs d'apprenants augmentent. Une file de brouillons plus longue ne démontre pas à elle seule une accélération de la livraison.

### Exercice pratique 5

Le scénario synthétique à revue croissante se termine avec 32 éléments en attente de publication. Un agent propose de doubler encore la rédaction de cours et d'appeler le résultat « progrès exponentiel de Streeling ». Quel travail l'équipe doit-elle examiner en premier, quelle identité de source faut-il préserver, et qu'est-ce qui compterait comme une amélioration réelle ?

> **Réponse :** Examiner pourquoi des éléments acceptés attendent : les entrées de la génération du site, les portes de construction et de mise en production, la capacité de déploiement et la vérification publique anonyme. Préserver, pour chaque cours accepté, le commit et le blob Git source exacts jusqu'à la page générée et à la vérification publique ; ne pas laisser une modification ultérieure hériter d'un ancien verdict. Une amélioration réelle augmenterait le rythme des cours correctement revus et vérifiés publiquement, sans masquer de problèmes de qualité ou de reprise. Poursuivre une rédaction de cours indépendante peut rester utile, mais doubler les brouillons ne règle pas cette file de publication.

## Sources, limites et prochaine vérification

La référence observée repose sur l'[instantané des candidats à la revue, lié à un commit](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/state/streeling/reviews/review-candidates-793e92b.json) et sur l'[outil de suivi d'avancement à cette révision source](https://github.com/GuitarAlchemist/Demerzel/blob/3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b/scripts/streeling_course_progress.py). Les résultats chiffrés sur quatre semaines sont calculés par le [script du jeu d'essai](../../../../../scripts/streeling_fixtures/psychohistory/psy-003/analyze.py), non mesurés sur une intervention. Le modèle suppose des revues et une publication immédiates et réussies, et ignore la reprise et la difficulté variable des cours. Aucune expérience opérationnelle de quatre semaines, aucune revue humaine de cette leçon ni de ses traductions française et espagnole, aucun essai d'apprenant et aucune vérification publique n'ont été réalisés. La prochaine vérification est un essai pilote réel et borné, avec des attestations liées à la source exacte, des cohortes de cours comparables et un décompte explicite des vérifications publiques.
