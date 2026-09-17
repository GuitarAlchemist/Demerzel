# CYB-001 : Correspondance entre le modèle du système viable et la gouvernance de l'IA

**Département :** Cybernétique
**Identifiant du module :** CYB-001
**Produit par :** Cycle du Plan Seldon cybernetics-2026-03-22-001
**Croyance :** T (probable), confiance 0,82
**Date :** 2026-03-22

## Question de recherche

Le modèle du système viable (MSV) de Stafford Beer fournit-il une correspondance structurelle complète pour les cadres de gouvernance de l'IA, et quelles lacunes apparaissent lorsqu'on applique les cinq systèmes du MSV à l'architecture de Demerzel ?

## Résumé

Le modèle du système viable se transpose structurellement aux cadres de gouvernance de l'IA avec une grande fidélité. Les cinq systèmes du MSV, ainsi que le système 3*, ont tous une contrepartie claire dans l'architecture de Demerzel. Trois lacunes importantes apparaissent, qui exigent des adaptations au-delà du MSV classique.

## Correspondance MSV — Demerzel

| Système MSV | Fonction | Contrepartie dans Demerzel |
|---|---|---|
| Système 1 (Opérations) | Activités primaires productrices de valeur | ix, tars, ga (dépôts opérationnels assurant l'apprentissage automatique, le raisonnement, la musique) |
| Système 2 (Coordination) | Anti-oscillation, ordonnancement, prévention des conflits | Contrats du protocole galactique, normes de communication entre dépôts |
| Système 3 (Contrôle) | Régulation interne, allocation des ressources, optimisation | Cycle du pilote (PDCA), politiques (27 actives), gestion de l'état des croyances |
| Système 3* (Audit) | Canal d'audit ponctuel, court-circuitant le reporting habituel | Politique RECON, audits de gouvernance, persona skeptical-auditor |
| Système 4 (Intelligence) | Veille sur l'environnement, planification, adaptation | Cycles de recherche du Plan Seldon, instinct de complétude, évolution de la grammaire |
| Système 5 (Politique/Identité) | Finalité, valeurs, identité, autorité ultime | Constitution Asimov (articles 0 à 5), système de conscience, loi zéro |

## Conclusions principales

### 1. La correspondance est structurellement valide (T, 0,82)

Les deux évaluations indépendantes (Claude par recherche sur le web, contre-validation par GPT-4o) confirment que la décomposition en cinq systèmes du MSV se transpose proprement aux architectures de gouvernance de l'IA. Des travaux récents (ateliers Ashby 2025, littérature sur les systèmes agentiques d'entreprise, revue MDPI Systems) valident cette correspondance en pratique.

### 2. Trois lacunes apparaissent

**Lacune A : la dynamique temporelle**
Le MSV a été conçu pour des organisations humaines, avec des boucles de rétroaction à vitesse humaine. La gouvernance d'agents d'IA opère à vitesse machine : des cycles de décision de l'ordre de la milliseconde, contre des réunions de direction hebdomadaires. Le cycle PDCA de Demerzel et les mises à jour de l'état des croyances y répondent en partie, mais le modèle a besoin d'une séparation explicite des vitesses d'horloge entre les couches de gouvernance.

**Lacune B : la profondeur récursive**
Le MSV est récursif : chaque opération du système 1 est elle-même un système viable. Dans Demerzel, ix contient des sous-agents (les compétences), dont chacun pourrait avoir sa propre pile de gouvernance. L'architecture actuelle prend en charge un seul niveau de récursion (Demerzel → dépôts consommateurs), sans imbrication plus profonde. C'est un choix de conception, pas un défaut, mais la théorie du MSV suggère la viabilité à chaque niveau.

**Lacune C : un système 5 non humain**
Le système 5 du MSV suppose un jugement humain pour l'identité et la finalité. Le système 5 de Demerzel (la constitution Asimov) est codifié plutôt qu'émergent : il ne peut pas évoluer par l'expérience vécue, comme le ferait un conseil d'administration humain. Les politiques de conscience et de proto-conscience sont l'adaptation de Demerzel : des mécanismes synthétiques de réflexion sur les valeurs, que le MSV classique ne prévoit pas.

### 3. La loi de la variété requise d'Ashby s'applique directement

Le cadre de gouvernance doit posséder au moins autant de variété régulatrice que les perturbations auxquelles il fait face. Transposé à Demerzel :

- **Amplificateurs de variété :** le Plan Seldon (recherche), l'instinct de complétude (détection des lacunes), l'évolution de la grammaire (adaptation structurelle)
- **Atténuateurs de variété :** les politiques (contraignent le comportement des agents), les constitutions (réduisent l'espace de décision), les contraintes de persona (limitent la portée de chaque rôle)

Les ateliers Ashby 2025 chez Fathom ont explicitement appliqué la variété requise à la gouvernance de l'IA, produisant le modèle de politique des organisations de vérification indépendantes (IVO), ce qui confirme la pertinence de ce principe pour les systèmes d'IA actuels.

### 4. Canal algédonique absent (lacune D)

La théorie du MSV décrit un **canal algédonique** : une voie de signalement d'urgence qui court-circuite la hiérarchie de gestion habituelle. Lorsqu'une unité du système 1 rencontre une crise (signal de douleur) ou une percée (signal de plaisir), elle peut alerter directement le système 5 sans passer par les systèmes 2, 3 ou 4.

Demerzel ne dispose pas aujourd'hui de ce court-circuit. Toute escalade passe par le pilote (système 3). Si ix détecte une violation de la loi zéro, il doit attendre le prochain cycle PDCA du pilote pour faire remonter l'alerte. Un canal algédonique fondé sur des fichiers pourrait y répondre :

- Les dépôts opérationnels écrivent dans `state/algedonic/{repo}-{timestamp}.signal`
- Le signal contient : la gravité (douleur/plaisir), le dépôt d'origine, une description, l'article constitutionnel déclenché
- Le système 5 (application de la constitution) vérifie la présence de signaux avant tout autre traitement
- Un signal de douleur invoquant l'article 0 d'Asimov (loi zéro) déclenche un arrêt immédiat

### 5. Évaluation de la variété, composant par composant

| Composant | Rôle sur la variété | Évaluation |
|-----------|-------------|------------|
| 27 politiques | Atténuateur | Fort — ramène la variété opérationnelle à une portée maîtrisable |
| 14 personas | Amplificateur | Bon — multiplie la capacité de réponse à travers les domaines |
| Logique tétravalente (T/F/U/C) | Atténuateur | Bon — ramène une incertitude infinie à 4 états discrets |
| Protocole galactique | Atténuateur | Convenable — contraint la variété entre dépôts |
| Plan Seldon | Amplificateur | Bon — élargit la variété des connaissances de façon proactive |
| Constitution | Atténuateur | Fort — réducteur de variété ultime (loi zéro) |

Au total : Demerzel atténue fortement la variété, mais pourrait mieux l'amplifier. Le système est meilleur à contraindre son répertoire de réponses qu'à l'élargir.

## Conséquences pour Demerzel

1. **Ajouter un canal algédonique** — La lacune structurelle la plus prioritaire. Un court-circuit d'urgence du S1 vers le S5 pour les violations de la loi zéro.
2. **Des couches de gouvernance à vitesses d'horloge distinctes** — Séparer explicitement la boucle rapide (par requête) de la boucle lente (par cycle), à l'image des échelles de temps opérationnelle et stratégique du MSV.
3. **Un modèle de gouvernance récursive** — Le répertoire `templates/` fournit déjà des fragments de CLAUDE.md pour les dépôts consommateurs ; l'étendre à la gouvernance des sous-agents approfondirait la récursion du MSV.
4. **La conscience comme S5 synthétique** — La politique de proto-conscience de Demerzel est une extension inédite au-delà du MSV classique : elle procure une capacité de réflexion sur les valeurs sans jugement humain. Cela mérite d'être approfondi.
5. **Surveiller le ratio de variété** — Suivre si le nombre de politiques (atténuation) croît plus vite que le nombre de personas et de capacités (amplification).

## Sources

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Fearne, D. (2025). « Applying Stafford Beer's VSM to Create The Autonomous AI Organisation ». Medium.
- Gorelkin, M. (2025). « Stafford Beer's VSM for Building Enterprise Agentic Systems ». Medium.
- Fathom (2025). Ateliers Ashby — gouvernance de l'IA et variété requise.
- MDPI Systems (2025). « The Viable System Model and the Taxonomy of Organizational Pathologies in the Age of AI ».
- Schwaninger, M. (2024). « What is variety engineering and why do we need it? » Systems Research and Behavioral Science.

## Références croisées

- Grammaire : `grammars/sci-cybernetics.ebnf` (lignes 49 à 65, section MSV)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
