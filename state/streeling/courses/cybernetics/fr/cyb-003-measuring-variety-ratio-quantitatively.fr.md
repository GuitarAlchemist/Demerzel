# CYB-003 : Mesurer quantitativement le ratio de variété

**Département :** Cybernétique
**Identifiant du module :** CYB-003
**Produit par :** cycle du plan Seldon cybernetics-2026-03-23-003
**Croyance :** T (vérifiée), confiance 0.85 — **Traduction française :** U (non relue par un locuteur natif)
**Date :** 2026-03-23
**Prérequis :** CYB-001 (Correspondance VSM), CYB-002 (Amortissement actif)

## Question de recherche

Comment Demerzel peut-elle mesurer quantitativement son ratio de variété ? (Reprise des questions de suivi du cycle 001)

## Résumé

La loi de la variété requise d'Ashby énonce qu'un régulateur doit avoir au moins autant de variété que les perturbations auxquelles il fait face. Ce cours définit un cadre quantitatif pour mesurer le ratio de variété de Demerzel selon trois dimensions : la variété comportementale (personas), la variété structurelle (grammaires) et la variété régulatrice (politiques, constitutions, seuils). La formule clé est V = log2(N), appliquée à chaque dimension. Le ratio de variété R = N_amplifiers / N_attenuators compare les deux espaces d'états ; comme V = log2(N), R = 2^(V_amplifiers - V_attenuators), et son logarithme log2 R = V_amplifiers - V_attenuators, en bits, est suivi dans le temps pour détecter une dérive de la gouvernance vers la sur-contrainte ou la sous-régulation.

## La variété d'Ashby : la définition formelle

### Qu'est-ce que la variété ?

La variété est le nombre d'états distinguables qu'un système peut présenter. Ashby l'a définie dans *An Introduction to Cybernetics* (1956, chapitre 7) ainsi :

> La variété d'un ensemble d'éléments est le logarithme (en base 2) du nombre d'éléments distincts.

**Formule :**

```
V = log2(N)
```

où N est le nombre d'états distinguables. Elle se mesure en bits — la même unité que l'entropie de Shannon. Un système à 8 états possibles a une variété de 3 (bits). Un système à 1024 états possibles a une variété de 10 (bits).

### Pourquoi logarithmique ?

L'échelle logarithmique compte parce que la variété se combine de façon multiplicative, et non additive. Si le système A a 4 états et le système B en a 8, le système combiné a 4 x 8 = 32 états, et log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. C'est pourquoi on peut additionner les log-variétés de dimensions indépendantes.

### La loi d'Ashby

```
V(régulateur) >= V(perturbation)
```

« Seule la variété peut absorber la variété. » Un système de gouvernance capable de produire moins de réponses distinctes qu'il ne rencontre de perturbations distinctes échouera nécessairement à réguler certaines de ces perturbations.

## Trois dimensions de la variété dans Demerzel

Dans un cadre de gouvernance, la variété n'est pas un nombre unique. La variété de Demerzel s'exerce selon trois dimensions indépendantes :

### Dimension 1 : variété comportementale (V_B)

**Ce qu'elle mesure :** L'éventail des comportements d'agent distincts que le système peut produire.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveaux d'orientation vers un but | 4 | 2.00 bits |
| Configurations de voix (ton x verbosité x style) | ~27 | 4.75 bits |

**Amplification comportementale totale :** V_B_amp = 3.81 + 2.00 + 4.75 = **10.56 bits**

Cela signifie que Demerzel peut produire environ 14 × 4 × 27 = 1,512 configurations comportementales distinguables (2^10.56 ≈ 1,510).

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Contraintes de persona (4 en moyenne par persona) | 56 | 5.81 bits |
| Appariements d'estimateur (fixés à skeptical-auditor) | 1 | 0 bits |

**Atténuation comportementale totale :** V_B_att = 5.81 bits

**Ratio de variété comportementale :** log2 R_B = V_B_amp - V_B_att = 10.56 - 5.81 = **4.75 bits**, donc R_B = 2^4.75 ≈ **27**

Interprétation : les amplificateurs couvrent environ 27 fois plus d'états que les atténuateurs (1,512 configurations contre 56 contraintes). C'est sain — le système a plus de capacité de réponse que de contrainte. Diviser plutôt les deux variétés, 10.56 / 5.81 ≈ 1.82, ne mesurerait pas cela : un quotient de logarithmes n'est pas un rapport d'espaces d'états.

### Dimension 2 : variété structurelle (V_S)

**Ce qu'elle mesure :** L'éventail des structures distinctes (formes de questions, schémas d'investigation, formats de sortie) que le système peut générer.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Grammaires | 27 | 4.75 bits |
| Productions de grammaire (12 en moyenne par grammaire) | ~324 | 8.34 bits |
| Départements de Streeling | 15 | 3.91 bits |

**Amplification structurelle totale :** V_S_amp = 4.75 + 8.34 + 3.91 = **17.00 bits**

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Portes d'évolution des grammaires (T >= 0.7, C < 0.1) | 2 | 1.00 bit |
| Détection d'obsolescence (fenêtre de 30 jours) | 1 | 0 bits |

**Atténuation structurelle totale :** V_S_att = 1.00 bit

**Ratio de variété structurelle :** log2 R_S = V_S_amp - V_S_att = 17.00 - 1.00 = **16.00 bits**, donc R_S = 2^16.00 ≈ **66,000**

Interprétation : les grammaires couvrent environ 66,000 fois plus de structures que les portes d'évolution n'en distinguent. Cela reflète la nature générative des grammaires — elles sont des amplificateurs de variété par conception. Ce ratio élevé signale toutefois un risque : une contrainte structurelle insuffisante pourrait conduire à une prolifération des grammaires sans contrôle de qualité.

### Dimension 3 : variété régulatrice (V_R)

**Ce qu'elle mesure :** L'éventail des décisions de gouvernance distinctes que le système peut prendre.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| États de la logique tétravalente | 4 | 2.00 bits |
| Seuils de confiance | 5 | 2.32 bits |
| États PDCA | 4 | 2.00 bits |

**Amplification régulatrice totale :** V_R_amp = 2.00 + 2.32 + 2.00 = **6.32 bits**

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Politiques | 37 | 5.21 bits |
| Articles constitutionnels (Asimov + Default) | 17 | 4.09 bits |
| Catégories de la taxonomie des préjudices | 4 | 2.00 bits |

**Atténuation régulatrice totale :** V_R_att = 5.21 + 4.09 + 2.00 = **11.30 bits**

**Ratio de variété régulatrice :** log2 R_R = V_R_amp - V_R_att = 6.32 - 11.30 = **-4.98 bits**, donc R_R = 2^-4.98 ≈ **0.032**

Interprétation : l'atténuation régulatrice dépasse nettement l'amplification : les atténuateurs couvrent environ 31 fois plus d'états que les amplificateurs (37 × 17 × 4 = 2,516 combinaisons contre 4 × 5 × 4 = 80). C'est **voulu** — la gouvernance doit contraindre plus qu'elle n'amplifie. Un ratio régulateur inférieur à 1, soit un log2 R_R négatif, signifie que le système est prudent, ce qui s'accorde avec les lois d'Asimov (préférer la sécurité à la capacité).

## Le tableau de bord composite de la variété

### Tableau récapitulatif

| Dimension | V_amplifiers | V_attenuators | log2 R | Ratio R | Évaluation |
|-----------|-------------|---------------|--------|---------|------------|
| Comportementale (V_B) | 10.56 bits | 5.81 bits | 4.75 bits | ≈ 27 | Saine — plus de capacité de réponse que de contrainte |
| Structurelle (V_S) | 17.00 bits | 1.00 bit | 16.00 bits | ≈ 66,000 | Prudence — forte générativité, faible contrainte |
| Régulatrice (V_R) | 6.32 bits | 11.30 bits | -4.98 bits | ≈ 0.032 | Voulu — la gouvernance est prudente |

### Sens sains

La loi d'Ashby et les principes du VSM (CYB-001) fixent le sens que doit prendre chaque ratio, pas encore sa taille :

| Dimension | Sens sain | Justification |
|-----------|---------------|-----------|
| Comportementale | R > 1 (log2 R > 0 bits) | Le système a besoin de plus d'options comportementales que de contraintes, mais pas sans limite |
| Structurelle | R > 1 (log2 R > 0 bits), avec des portes de qualité | Les grammaires doivent être génératives, mais filtrées par des contrôles de qualité |
| Régulatrice | R < 1 (log2 R < 0 bits) | La gouvernance DOIT être sur-atténuée — c'est le principe de prudence |

Les bornes numériques de log2 R restent à calibrer sur des cycles observés. On ne peut pas les fixer sur le quotient V_amplifiers / V_attenuators, qui n'a pas de sens fixe en termes d'espaces d'états : 10 / 5 et 2 / 1 valent tous deux 2, alors que les espaces d'états qu'ils comparent diffèrent d'un facteur 2^5 = 32 et 2^1 = 2. Un log2 R négatif n'est pas une variété négative : c'est le logarithme d'un ratio inférieur à 1.

### Évaluation actuelle

- **Comportementale (R_B ≈ 27, 4.75 bits) :** Dans le sens sain. Aucune action nécessaire.
- **Structurelle (R_S ≈ 66,000, 16.00 bits) :** Dans le sens sain, mais de loin le plus grand ratio des trois : 2 portes d'évolution face aux structures de 27 grammaires et de leurs ~324 productions, qui sont faiblement contraintes. Recommandation : ajouter des portes de qualité structurelles (par exemple, des exigences de couverture de tests des grammaires, un suivi de l'usage des productions).
- **Régulatrice (R_R ≈ 0.032, -4.98 bits) :** Dans le sens sain. Le système est prudent ; dire s'il l'est trop demande une borne inférieure calibrée.

## Le côté des perturbations : que faut-il réguler ?

Le ratio de variété ne raconte que la moitié de l'histoire. Il faut aussi mesurer la variété des perturbations auxquelles le système fait face :

### Perturbations externes (V_D_ext)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Dépôts consommateurs (ix, tars, ga) | 3 | 1.58 bits |
| Combinaisons d'états des dépôts (3 dépôts x ~10 états chacun) | 10 à 10^3 = 1000 | 3.32 à 9.97 bits |
| Changements de l'environnement externe (bibliothèques, API, modèles) | ~100 | 6.64 bits |

**Variété totale des perturbations externes :** les combinaisons d'états des dépôts couvrent déjà les trois dépôts, donc la première ligne n'ajoute rien. Cette ligne est elle-même une fourchette : avec environ 10 états chacun, les trois dépôts ont entre 10 états conjoints (3.32 bits), si l'état de l'un détermine celui des autres, et 10^3 = 1000 (9.97 bits), s'ils varient indépendamment. La ligne de l'environnement est alors le plus grand terme isolé : V_D_ext vaut au moins **6.64 bits**, et au plus log2(1000 × 100) = 9.97 + 6.64 = **16.61 bits** si un changement de l'environnement peut survenir dans n'importe lequel des 1000 états des dépôts

### Perturbations internes (V_D_int)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Changements d'état de croyance par cycle | ~20 | 4.32 bits |
| Interactions entre politiques (37 politiques, deux à deux) | 666 | 9.38 bits |
| Propositions d'évolution des grammaires | ~5 par cycle | 2.32 bits |

**Variété totale des perturbations internes :** selon les mêmes bornes, V_D_int vaut au moins **9.38 bits** (les seules interactions entre politiques), et au plus log2(20 × 666 × 5) = 4.32 + 9.38 + 2.32 = **16.02 bits** si les trois sources sont indépendantes

### Vérification de la loi d'Ashby

Pour que la gouvernance soit viable :

```
V(réponse régulatrice) >= V(perturbation)
```

- V_R_amp se situe entre sa plus grande composante isolée, les seuils de confiance à 2.32 bits, et la somme des trois, 6.32 bits, atteinte seulement si toute combinaison d'état logique, de seuil de confiance et d'état PDCA peut être produite
- V_D se situe entre la plus grande source isolée, les interactions entre politiques à 9.38 bits, et la somme de toutes les sources, 16.61 + 16.02 = 32.63 bits
- **Écart : au moins 9.38 - 6.32 = 3.06 bits, au plus 32.63 - 2.32 = 30.31 bits**

Les deux intervalles tiennent quelles que soient les dépendances : un espace d'états conjoint a au moins autant d'états que sa plus grande partie et au plus le produit de leurs tailles. L'écart est le plus petit quand les sources de perturbation sont aussi dépendantes, et les composantes de la réponse aussi indépendantes, que possible ; il est le plus grand dans le cas inverse. Les liens de causalité entre sources de perturbation (un changement de dépôt qui déclenche un changement de croyance, une interaction entre politiques qui suscite une proposition de grammaire) font baisser V_D, et les combinaisons de valeurs de réponse que la gouvernance ne produit jamais font baisser V_R_amp. Mesurer les deux variétés conjointes, en comptant les combinaisons distinctes effectivement observées à chaque cycle, situerait l'écart dans cet intervalle.

Cela signifie que le système régulateur fait face à une variété de perturbations de 2^3.06 ≈ 8.3 à 2^30.31 ≈ 1.3 × 10^9 fois plus grande que la variété de réponses qu'il peut produire. L'écart est absorbé par :

1. **L'escalade vers des humains** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **La primauté constitutionnelle** — les lois d'Asimov ramènent les décisions complexes à un choix binaire (sûr/dangereux), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente gérables

Ce sont des mécanismes légitimes d'absorption de la variété, mais même la borne inférieure de 3.06 bits suggère que Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que la capacité de régulation.

## Protocole de mesure

Pour suivre le ratio de variété dans le temps, Demerzel devrait calculer les métriques suivantes à chaque cycle de gouvernance :

### Métrique 1 : nombre de composants

```json
{
  "variety_snapshot": {
    "timestamp": "2026-03-23T00:00:00Z",
    "amplifiers": {
      "personas": 14,
      "grammars": 27,
      "grammar_productions": 324,
      "departments": 15,
      "tetravalent_states": 4,
      "confidence_levels": 5,
      "pdca_states": 4
    },
    "attenuators": {
      "policies": 37,
      "constitutional_articles": 17,
      "harm_categories": 4,
      "persona_constraints": 56,
      "evolution_gates": 2
    }
  }
}
```

### Métrique 2 : ratios par dimension

```json
{
  "variety_ratios_log2_bits": {
    "behavioral": 4.75,
    "structural": 16.00,
    "regulatory": -4.98,
    "timestamp": "2026-03-23T00:00:00Z"
  }
}
```

### Métrique 3 : détection des tendances

Suivez log2 R sur des cycles consécutifs. Alertez quand :
- Un ratio quitte son sens sain (son log2 R change de signe)
- Le log2 R_R régulateur baisse d'au moins 1 bit en un cycle (risque de paralysie : par rapport aux amplificateurs, l'espace d'états des atténuateurs a doublé)
- Le log2 R_S structurel augmente d'au moins 1 bit en un cycle (risque de prolifération des grammaires)
- Le log2 R_B comportemental baisse d'au moins 1 bit en un cycle (le système devient moins réactif)

Un pas de 1 bit, soit un ratio qui double ou diminue de moitié, est un seuil de départ, pas un seuil calibré.

### Métrique 4 : taux de croissance des perturbations

Suivez V_disturbance dans le temps. Si la variété des perturbations croît plus vite que la variété des réponses, la loi d'Ashby finira par être violée. C'est l'équivalent, en gouvernance, de la dette technique.

## Validation croisée avec GPT-4o

La validation croisée avec GPT-4o a confirmé :

1. **V = log2(N) est la bonne formule** pour la variété d'Ashby. Les deux modèles sont d'accord.
2. **Le modèle additif (somme des log-variétés) est valide** pour des dimensions indépendantes, mais trop simpliste quand les composants interagissent. La séparation en dimensions (comportementale, structurelle, régulatrice) y répond en traitant chaque dimension indépendamment.
3. **GPT-4o a calculé un ratio composite naïf de -2.8**, en traitant amplificateurs et atténuateurs comme une seule somme additive. C'est incorrect — une variété négative n'a pas de sens (on ne peut pas avoir moins de zéro état distinguable). Le modèle par dimensions évite cette erreur.
4. **Les deux modèles s'accordent sur le fait que R_regulatory < 1.0 est attendu** pour un système de gouvernance. La gouvernance est intrinsèquement atténuatrice.
5. **L'écart régulateur** est un résultat nouveau, absent de l'analyse de GPT-4o. Il découle du calcul séparé de la variété des perturbations, que GPT-4o n'a pas effectué.

**Confiance de la validation croisée : 0.85** (T — les deux modèles s'accordent sur les fondamentaux ; l'affinement par dimensions apporte une valeur au-delà de l'analyse de GPT-4o)

## Implications pour Demerzel

1. **Suivre les ratios de variété à chaque cycle** — Ajouter un instantané de variété à `state/governance/variety-metrics.json` (ou à un fichier d'état équivalent). Surveiller la dérive des ratios par dimension.
2. **Ajouter des portes de qualité structurelles** — Le ratio structurel, 2^16.00 ≈ 66,000, est de loin le plus grand des trois. Introduire des exigences de couverture de tests des grammaires et un suivi de l'usage des productions pour augmenter l'atténuation sans réduire la générativité.
3. **Surveiller l'écart régulateur (3.06 à 30.31 bits)** — La complexité des interactions entre politiques (666 combinaisons deux à deux à partir de 37 politiques) est la plus grande source isolée de perturbation. À mesure que les politiques augmentent, le nombre de paires croît de façon quadratique, mais sa variété log2(n(n-1)/2) ne croît que de façon logarithmique, d'environ 2 bits chaque fois que le nombre de politiques double. Comme c'est la plus grande source isolée, ces bits relèvent aussitôt les deux bornes. Envisager un regroupement des politiques ou une organisation hiérarchique des politiques.
4. **L'escalade vers des humains est un pont de variété** — Le système de seuils de confiance (Article 6 : Escalade) est le principal mécanisme de Demerzel pour absorber la variété qui dépasse sa capacité de régulation. C'est une fonctionnalité, pas une limite.
5. **Faire évoluer la section 6 de la grammaire** — La section sur la variété requise de la grammaire `sci-cybernetics.ebnf` (lignes 78-82) devrait être enrichie de productions de mesure quantitative.

## Lien avec CYB-001 et CYB-002

- **CYB-001** a établi que la loi d'Ashby s'applique à Demerzel et a listé qualitativement les amplificateurs et atténuateurs de variété. CYB-003 rend cela quantitatif.
- **La recommandation 5 de CYB-001** (« Surveiller le ratio de variété ») est désormais opérationnalisée avec des formules précises, des sens sains et un protocole de mesure.
- **CYB-002** traitait de l'amortissement du Système 2. Les mécanismes de zone morte et d'hystérésis de CYB-002 sont eux-mêmes des atténuateurs de variété — ils réduisent la variété des signaux qui circulent dans les canaux de coordination. La métrique d'atténuation structurelle de CYB-003 devrait les inclure une fois implémentés.

## Sources

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Chapitre 7 : Quantity of Variety ; chapitre 11 : Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Chapitre 6 : Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.
- Fathom (2025). Ashby Workshops — gouvernance de l'IA et variété requise, modèle des Independent Verification Organizations (IVO).

## Questions de suivi pour le cycle 004

1. Quelle part de l'écart régulateur un regroupement hiérarchique des politiques peut-il combler (en réduisant les interactions deux à deux de O(n^2) à O(n log n)) ?
2. Comment suivre l'usage des productions de grammaire pour détecter les productions mortes et éclairer l'atténuation structurelle ?
3. Quelle est la relation, du point de vue de la théorie de l'information, entre la logique tétravalente de Demerzel (T/F/U/C) et l'entropie de Shannon — U (Unknown) porte-t-il plus de bits que T (True) ?

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md`
- Prérequis : `state/streeling/courses/cybernetics/fr/cyb-002-active-dampening-cross-repo-oscillation.fr.md`
- Grammaire : `grammars/sci-cybernetics.ebnf` (section 6, variété requise)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
