# CYB-003 : Mesurer quantitativement le ratio de variété

**Département :** Cybernétique
**Identifiant du module :** CYB-003
**Produit par :** cycle du plan Seldon cybernetics-2026-03-23-003
**Croyance :** T (vérifiée), confiance 0.85
**Date :** 2026-03-23
**Prérequis :** CYB-001 (Correspondance VSM), CYB-002 (Amortissement actif)

## Question de recherche

Comment Demerzel peut-elle mesurer quantitativement son ratio de variété ? (Reprise des questions de suivi du cycle 001)

## Résumé

La loi de la variété requise d'Ashby énonce qu'un régulateur doit avoir au moins autant de variété que les perturbations auxquelles il fait face. Ce cours définit un cadre quantitatif pour mesurer le ratio de variété de Demerzel selon trois dimensions : la variété comportementale (personas), la variété structurelle (grammaires) et la variété régulatrice (politiques, constitutions, seuils). La formule clé est V = log2(N), appliquée à chaque dimension, avec le ratio de variété R = V_amplifiers / V_attenuators suivi dans le temps pour détecter une dérive de la gouvernance vers la sur-contrainte ou la sous-régulation.

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
V(regulator) >= V(disturbance)
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

Cela signifie que Demerzel peut produire environ 2^10.56 = 1,506 configurations comportementales distinguables.

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Contraintes de persona (4 en moyenne par persona) | 56 | 5.81 bits |
| Appariements d'estimateur (fixés à skeptical-auditor) | 1 | 0 bits |

**Atténuation comportementale totale :** V_B_att = 5.81 bits

**Ratio de variété comportementale :** R_B = V_B_amp / V_B_att = 10.56 / 5.81 = **1.82**

Interprétation : l'amplification comportementale dépasse l'atténuation d'un facteur 1.82. C'est sain — le système a plus de capacité de réponse que de contrainte.

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

**Ratio de variété structurelle :** R_S = V_S_amp / V_S_att = 17.00 / 1.00 = **17.00**

Interprétation : la variété structurelle est très élevée par rapport à l'atténuation. Cela reflète la nature générative des grammaires — elles sont des amplificateurs de variété par conception. Ce ratio élevé signale toutefois un risque : une contrainte structurelle insuffisante pourrait conduire à une prolifération des grammaires sans contrôle de qualité.

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

**Ratio de variété régulatrice :** R_R = V_R_amp / V_R_att = 6.32 / 11.30 = **0.56**

Interprétation : l'atténuation régulatrice dépasse nettement l'amplification. C'est **voulu** — la gouvernance doit contraindre plus qu'elle n'amplifie. Un ratio régulateur inférieur à 1.0 signifie que le système est prudent, ce qui s'accorde avec les lois d'Asimov (préférer la sécurité à la capacité).

## Le tableau de bord composite de la variété

### Tableau récapitulatif

| Dimension | V_amplifiers | V_attenuators | Ratio R | Évaluation |
|-----------|-------------|---------------|---------|------------|
| Comportementale (V_B) | 10.56 bits | 5.81 bits | 1.82 | Saine — plus de capacité de réponse que de contrainte |
| Structurelle (V_S) | 17.00 bits | 1.00 bit | 17.00 | Prudence — forte générativité, faible contrainte |
| Régulatrice (V_R) | 6.32 bits | 11.30 bits | 0.56 | Voulu — la gouvernance est prudente |

### Plages saines

D'après la loi d'Ashby et les principes du VSM (CYB-001), les ratios de variété sains diffèrent selon la dimension :

| Dimension | Plage saine | Justification |
|-----------|---------------|-----------|
| Comportementale | 1.2 -- 3.0 | Le système a besoin de plus d'options comportementales que de contraintes, mais pas sans limite |
| Structurelle | 2.0 -- 10.0 | Les grammaires doivent être génératives, mais filtrées par des contrôles de qualité |
| Régulatrice | 0.3 -- 0.8 | La gouvernance DOIT être sur-atténuée — c'est le principe de prudence |

### Évaluation actuelle

- **Comportementale (1.82) :** Dans la plage saine. Aucune action nécessaire.
- **Structurelle (17.00) :** Au-dessus de la plage saine. Les 27 grammaires et leurs ~324 productions sont faiblement contraintes. Recommandation : ajouter des portes de qualité structurelles (par exemple, des exigences de couverture de tests des grammaires, un suivi de l'usage des productions).
- **Régulatrice (0.56) :** Dans la plage saine. Le système est prudent, mais pas paralysé.

## Le côté des perturbations : que faut-il réguler ?

Le ratio de variété ne raconte que la moitié de l'histoire. Il faut aussi mesurer la variété des perturbations auxquelles le système fait face :

### Perturbations externes (V_D_ext)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Dépôts consommateurs (ix, tars, ga) | 3 | 1.58 bits |
| Combinaisons d'états des dépôts (3 dépôts x ~10 états chacun) | 10^3 = 1000 | 9.97 bits |
| Changements de l'environnement externe (bibliothèques, API, modèles) | ~100 | 6.64 bits |

**Variété totale des perturbations externes :** V_D_ext = **9.97 bits** (dominée par les combinaisons d'états des dépôts)

### Perturbations internes (V_D_int)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Changements d'état de croyance par cycle | ~20 | 4.32 bits |
| Interactions entre politiques (37 politiques, deux à deux) | 666 | 9.38 bits |
| Propositions d'évolution des grammaires | ~5 par cycle | 2.32 bits |

**Variété totale des perturbations internes :** V_D_int = **9.38 bits** (dominée par les interactions entre politiques)

### Vérification de la loi d'Ashby

Pour que la gouvernance soit viable :

```
V(regulatory response) >= V(disturbance)
```

- V_R_amp = 6.32 bits
- V_D = max(V_D_ext, V_D_int) = 9.97 bits
- **Écart : 9.97 - 6.32 = 3.65 bits**

Cela signifie que le système régulateur fait face à environ 2^3.65 ≈ 12.6x plus de variété de perturbations qu'il ne peut produire de variété de réponses. L'écart est absorbé par :

1. **L'escalade vers des humains** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **La primauté constitutionnelle** — les lois d'Asimov ramènent les décisions complexes à un choix binaire (sûr/dangereux), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente gérables

Ce sont des mécanismes légitimes d'absorption de la variété, mais l'écart de 3.65 bits suggère que Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que la capacité de régulation.

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
  "variety_ratios": {
    "behavioral": 1.82,
    "structural": 17.00,
    "regulatory": 0.56,
    "timestamp": "2026-03-23T00:00:00Z"
  }
}
```

### Métrique 3 : détection des tendances

Suivez les ratios sur des cycles consécutifs. Alertez quand :
- Un ratio franchit la limite de sa plage saine
- Le ratio régulateur passe sous 0.3 (risque de paralysie du système)
- Le ratio structurel dépasse 20.0 (risque de prolifération des grammaires)
- Le ratio comportemental passe sous 1.0 (système insuffisamment réactif)

### Métrique 4 : taux de croissance des perturbations

Suivez V_disturbance dans le temps. Si la variété des perturbations croît plus vite que la variété des réponses, la loi d'Ashby finira par être violée. C'est l'équivalent, en gouvernance, de la dette technique.

## Validation croisée avec GPT-4o

La validation croisée avec GPT-4o a confirmé :

1. **V = log2(N) est la bonne formule** pour la variété d'Ashby. Les deux modèles sont d'accord.
2. **Le modèle additif (somme des log-variétés) est valide** pour des dimensions indépendantes, mais trop simpliste quand les composants interagissent. La séparation en dimensions (comportementale, structurelle, régulatrice) y répond en traitant chaque dimension indépendamment.
3. **GPT-4o a calculé un ratio composite naïf de -2.8**, en traitant amplificateurs et atténuateurs comme une seule somme additive. C'est incorrect — une variété négative n'a pas de sens (on ne peut pas avoir moins de zéro état distinguable). Le modèle par dimensions évite cette erreur.
4. **Les deux modèles s'accordent sur le fait que R_regulatory < 1.0 est attendu** pour un système de gouvernance. La gouvernance est intrinsèquement atténuatrice.
5. **L'écart régulateur de 3.65 bits** est un résultat nouveau, absent de l'analyse de GPT-4o. Il découle du calcul séparé de la variété des perturbations, que GPT-4o n'a pas effectué.

**Confiance de la validation croisée : 0.85** (T — les deux modèles s'accordent sur les fondamentaux ; l'affinement par dimensions apporte une valeur au-delà de l'analyse de GPT-4o)

## Implications pour Demerzel

1. **Suivre les ratios de variété à chaque cycle** — Ajouter un instantané de variété à `state/governance/variety-metrics.json` (ou à un fichier d'état équivalent). Surveiller la dérive des ratios par dimension.
2. **Ajouter des portes de qualité structurelles** — Le ratio structurel (17.00) est au-dessus de la plage saine. Introduire des exigences de couverture de tests des grammaires et un suivi de l'usage des productions pour augmenter l'atténuation sans réduire la générativité.
3. **Surveiller l'écart régulateur de 3.65 bits** — La complexité des interactions entre politiques (666 combinaisons deux à deux à partir de 37 politiques) est la principale source de perturbation interne. À mesure que les politiques augmentent, le nombre de paires croît de façon quadratique, mais sa variété log2(n(n-1)/2) ne croît que de façon logarithmique, d'environ 2 bits chaque fois que le nombre de politiques double ; elle dépasse le terme des états des dépôts (9.97 bits) à partir de 46 politiques. Envisager un regroupement des politiques ou une organisation hiérarchique des politiques.
4. **L'escalade vers des humains est un pont de variété** — Le système de seuils de confiance (Article 6 : Escalade) est le principal mécanisme de Demerzel pour absorber la variété qui dépasse sa capacité de régulation. C'est une fonctionnalité, pas une limite.
5. **Faire évoluer la section 6 de la grammaire** — La section sur la variété requise de la grammaire `sci-cybernetics.ebnf` (lignes 78-82) devrait être enrichie de productions de mesure quantitative.

## Lien avec CYB-001 et CYB-002

- **CYB-001** a établi que la loi d'Ashby s'applique à Demerzel et a listé qualitativement les amplificateurs et atténuateurs de variété. CYB-003 rend cela quantitatif.
- **La recommandation 5 de CYB-001** (« Surveiller le ratio de variété ») est désormais opérationnalisée avec des formules précises, des plages saines et un protocole de mesure.
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

1. L'écart régulateur de 3.65 bits peut-il être comblé par un regroupement hiérarchique des politiques (en réduisant les interactions deux à deux de O(n^2) à O(n log n)) ?
2. Comment suivre l'usage des productions de grammaire pour détecter les productions mortes et éclairer l'atténuation structurelle ?
3. Quelle est la relation, du point de vue de la théorie de l'information, entre la logique tétravalente de Demerzel (T/F/U/C) et l'entropie de Shannon — U (Unknown) porte-t-il plus de bits que T (True) ?

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Prérequis : `state/streeling/courses/cybernetics/en/CYB-002-active-dampening-cross-repo-oscillation.md`
- Grammaire : `grammars/sci-cybernetics.ebnf` (section 6, variété requise)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
