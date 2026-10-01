# CYB-001 : Correspondance entre le modèle du système viable et la gouvernance de l'IA

**Département :** Cybernétique
**Identifiant du module :** CYB-001
**Produit par :** Cycle du Plan Seldon cybernetics-2026-03-22-001
**Croyance :** T, confiance 0.82 — **Traduction française :** U (non relue par un locuteur natif)
**Date :** 2026-03-22

## Question de recherche

Le modèle du système viable (VSM) de Stafford Beer fournit-il une correspondance structurelle complète pour les cadres de gouvernance de l'IA, et quelles lacunes apparaissent lorsqu'on applique les cinq systèmes du VSM à l'architecture de Demerzel ?

## Résumé

Le modèle du système viable correspond structurellement aux cadres de gouvernance de l'IA avec une grande fidélité. Les cinq systèmes du VSM, ainsi que le Système 3*, ont des équivalents clairs dans l'architecture de Demerzel. Quatre lacunes importantes apparaissent (trois dans la section 2, le canal algédonique manquant dans la section 4), qui exigent une adaptation au-delà du VSM classique. Le canal algédonique a été mis en œuvre le jour même, dans `policies/algedonic-channel-policy.yaml` (section 4).

## Correspondance VSM-Demerzel

| Système du VSM | Fonction | Équivalent dans Demerzel |
|---|---|---|
| Système 1 (Opérations) | Activités primaires produisant de la valeur | ix, tars, ga (dépôts opérationnels réalisant le ML, le raisonnement, la musique) |
| Système 2 (Coordination) | Anti-oscillation, planification, prévention des conflits | Contrats du Galactic Protocol, standards de communication entre dépôts |
| Système 3 (Contrôle) | Régulation interne, allocation des ressources, optimisation | Cycle du driver (PDCA), politiques (27 actives), gestion de l'état des croyances |
| Système 3* (Audit) | Canal d'audit sporadique, contournant le reporting normal | Politique RECON, audits de gouvernance, persona skeptical-auditor |
| Système 4 (Intelligence) | Veille de l'environnement, planification de l'avenir, adaptation | Cycles de recherche du Plan Seldon, instinct de complétude, évolution des grammaires |
| Système 5 (Politique/Identité) | Finalité, valeurs, identité, autorité ultime | Constitution d'Asimov (Articles 0-5), système de conscience, Loi Zéro |

## Principales conclusions

### 1. La correspondance est structurellement valide (T, 0.82)

Les deux évaluations indépendantes (Claude par recherche sur le web, validation croisée par GPT-4o) confirment que la décomposition en cinq systèmes du VSM correspond proprement aux architectures de gouvernance de l'IA. Des travaux récents (Ashby Workshops 2025, littérature sur les systèmes agentiques d'entreprise, revue MDPI Systems) valident cette correspondance en pratique.

### 2. Trois lacunes apparaissent

**Lacune A : dynamique temporelle**
Le VSM a été conçu pour des organisations humaines dotées de boucles de rétroaction à vitesse humaine. La gouvernance des agents d'IA opère à la vitesse de la machine — des cycles de décision à la milliseconde contre des réunions de direction hebdomadaires. Le cycle PDCA de Demerzel et les mises à jour de l'état des croyances répondent en partie à ce problème, mais le modèle a besoin d'une séparation explicite des vitesses d'horloge entre les couches de gouvernance.

**Lacune B : profondeur récursive**
Le VSM est récursif — chaque opération du Système 1 est elle-même un système viable. Dans Demerzel, ix contient des sous-agents (skills), dont chacun pourrait avoir sa propre pile de gouvernance. L'architecture actuelle prend en charge un niveau de récursion (Demerzel → dépôts consommateurs) mais pas d'imbrication plus profonde. C'est un choix de conception, pas un défaut — mais la théorie du VSM suggère la viabilité à chaque niveau.

**Lacune C : S5 non humain**
Le Système 5 du VSM suppose un jugement humain pour l'identité et la finalité. Le S5 de Demerzel (la Constitution d'Asimov) est codifié plutôt qu'émergent — il ne peut pas évoluer par l'expérience vécue comme le fait un conseil d'administration humain. Les politiques de conscience et de proto-conscience sont l'adaptation de Demerzel : des mécanismes synthétiques de réflexion sur les valeurs dont le VSM classique ne rend pas compte.

### 3. La loi de la variété requise d'Ashby s'applique directement

La loi d'Ashby s'énonce sur les issues : là où chaque perturbation reçoit une réponse et où aucune réponse ne mène deux perturbations à la même issue, garder chaque issue acceptable exige au moins autant de variété régulatrice que les perturbations en portent, moins la variété des issues que la gouvernance peut accepter. En termes de Demerzel :

- **Amplificateurs de variété :** Plan Seldon (recherche), instinct de complétude (détection des lacunes), évolution des grammaires (adaptation structurelle)
- **Atténuateurs de variété :** politiques (contraignent le comportement des agents), constitutions (réduisent l'espace de décision), contraintes de persona (limitent le périmètre de chaque rôle)

Les Ashby Workshops 2025 chez Fathom ont explicitement appliqué la variété requise à la gouvernance de l'IA, produisant le modèle de politique des Independent Verification Organizations (IVO) — ce qui confirme la pertinence de ce principe pour les systèmes d'IA modernes.

### 4. Canal algédonique manquant (lacune D)

La théorie du VSM décrit un **canal algédonique** — un chemin de signal d'urgence qui contourne la hiérarchie de direction normale. Lorsqu'une unité du Système 1 rencontre une crise (signal de douleur) ou une percée (signal de plaisir), elle peut signaler directement au Système 5 sans passer par les Systèmes 2, 3 ou 4.

Lorsque ce module a été rédigé, Demerzel ne disposait pas de ce contournement. Toute escalade passait par le driver (Système 3) : si ix détectait une violation de la Loi Zéro, il devait attendre le prochain cycle PDCA du driver pour faire remonter l'alerte. Le module proposait un canal algédonique fondé sur des fichiers :

- Les dépôts opérationnels écrivent dans `state/algedonic/{repo}-{timestamp}.signal`
- Le signal contient : la gravité (douleur/plaisir), le dépôt source, une description, l'article constitutionnel déclenché
- Le Système 5 (application de la constitution) vérifie la présence de signaux avant tout autre traitement
- Les signaux de douleur invoquant l'Article 0 d'Asimov (Loi Zéro) déclenchent un arrêt immédiat

**Mis en œuvre le jour même.** `policies/algedonic-channel-policy.yaml` (en vigueur le 2026-03-22) définit le canal, et sa conception diffère de cette proposition. Le chemin va directement de S1 à S5, et S2, S3 et S4 ne peuvent ni supprimer, ni filtrer, ni retarder une alerte. Chaque alerte avertit un humain, qui doit en accuser réception, et elle est validée par rapport à la constitution d'Asimov (S5). Les alertes sont stockées sous `state/algedonic/{date}-{signal_id}.alert.json`, et non dans des fichiers `.signal`, et l'arrêt automatique dépend de la gravité : seule une alerte `critical` provoque l'arrêt. Lisez la liste ci-dessus comme la proposition qui a mené à la politique, non comme un canal encore à construire.

### 5. Évaluation de la variété par composant

| Composant | Rôle de variété | Évaluation |
|-----------|-------------|------------|
| 27 politiques | Atténuateur | Fort — réduit la variété opérationnelle à un périmètre gérable |
| 14 personas | Amplificateur | Bon — multiplie la capacité de réponse à travers les domaines |
| Logique hexavalente (T/P/U/D/F/C) | Atténuateur | Bon — réduit l'incertitude infinie à 6 états discrets |
| Galactic Protocol | Atténuateur | Adéquat — contraint la variété entre dépôts |
| Plan Seldon | Amplificateur | Bon — étend la variété des connaissances de manière proactive |
| Constitution | Atténuateur | Fort — réducteur de variété ultime (Loi Zéro) |

Les évaluations du tableau sont qualitatives et n'ont pas été mesurées, tout comme le bilan du module, selon lequel Demerzel est meilleur pour contraindre que pour étendre son répertoire de réponses. Les décomptes des deux premières lignes, 27 politiques et 14 personas, sont un inventaire, pas une variété : ajouter une politique ou une persona en double change un décompte sans changer les réponses que la gouvernance peut donner ni les perturbations qu'elle affronte. Seuls les relevés par cycle de la recommandation 5 peuvent dire si l'atténuation l'emporte sur l'amplification.

## Implications pour Demerzel

1. **Ajouter un canal algédonique** — Lacune structurelle la plus prioritaire. Contournement d'urgence de S1 vers S5 pour les violations de la Loi Zéro. Mis en œuvre : `policies/algedonic-channel-policy.yaml`.
2. **Couches de gouvernance à vitesses d'horloge** — Séparation explicite de la gouvernance en boucle rapide (par requête) et en boucle lente (par cycle), correspondant aux échelles de temps opérationnelle et stratégique du VSM.
3. **Modèle de gouvernance récursive** — Le répertoire templates/ fournit déjà des extraits de CLAUDE.md pour les dépôts consommateurs ; l'étendre à la gouvernance des sous-agents approfondirait la récursion du VSM.
4. **La conscience comme S5 synthétique** — La politique de proto-conscience de Demerzel est une extension inédite au-delà du VSM classique, qui fournit une capacité de réflexion sur les valeurs sans jugement humain. Cela mérite des recherches plus poussées.
5. **Mesurer la variété sur les issues** — Le rapport du nombre de politiques au nombre de personas est un bilan d'inventaire, pas un ratio de variété : une politique ou une persona en double le modifie sans changer les réponses que la gouvernance peut donner ni les perturbations qu'elle affronte. Mesurer plutôt chaque cycle : consigner chaque perturbation rencontrée, la réponse donnée (aucune, s'il n'y en a pas) et son issue sur les variables essentielles, puis compter les perturbations, les réponses et les issues distinctes.

## Sources

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Fearne, D. (2025). "Applying Stafford Beer's VSM to Create The Autonomous AI Organisation." Medium.
- Gorelkin, M. (2025). "Stafford Beer's VSM for Building Enterprise Agentic Systems." Medium.
- Fathom (2025). Ashby Workshops — gouvernance de l'IA et variété requise.
- MDPI Systems (2025). "The Viable System Model and the Taxonomy of Organizational Pathologies in the Age of AI."
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.

## Références croisées

- Grammaire : `grammars/sci-cybernetics.ebnf` (lignes 49-65, section VSM)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
- Politique : `policies/algedonic-channel-policy.yaml` (le canal algédonique, section 4)
