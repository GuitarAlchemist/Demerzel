# CYB-003 : Mesurer quantitativement le ratio de variété

**Département :** Cybernétique
**Identifiant du module :** CYB-003
**Produit par :** Cycle du Plan Seldon cybernetics-2026-03-23-003
**Croyance :** T (vérifiée), confiance 0,85
**Date :** 2026-03-23
**Prérequis :** CYB-001 (correspondance MSV), CYB-002 (amortissement actif)

## Question de recherche

Comment Demerzel peut-elle mesurer quantitativement son ratio de variété ? (Question héritée du suivi du cycle 001.)

## Résumé

La loi de la variété requise d'Ashby énonce qu'un régulateur doit posséder au moins autant de variété que les perturbations auxquelles il fait face. Ce cours définit un cadre quantitatif pour mesurer le ratio de variété de Demerzel selon trois dimensions : la variété comportementale (les personas), la variété structurelle (les grammaires) et la variété régulatrice (les politiques, les constitutions, les seuils). La formule centrale est V = log2(N), appliquée dimension par dimension, le ratio de variété R = V_amplificateurs / V_atténuateurs étant suivi dans le temps pour détecter une dérive de la gouvernance vers l'excès de contrainte ou l'insuffisance de régulation.

## La variété selon Ashby : définition formelle

### Qu'est-ce que la variété ?

La variété est le nombre d'états distinguables qu'un système peut présenter. Ashby la définit ainsi dans *An Introduction to Cybernetics* (1956, chapitre 7) :

> La variété d'un ensemble d'éléments est le logarithme (en base 2) du nombre d'éléments distincts.

**Formule :**

```
V = log2(N)
```

où N est le nombre d'états distinguables. La mesure s'exprime en bits, la même unité que l'entropie de Shannon. Un système à 8 états possibles a une variété de 3 bits. Un système à 1024 états possibles a une variété de 10 bits.

### Pourquoi un logarithme ?

L'échelle logarithmique compte, parce que la variété se combine de façon multiplicative et non additive. Si le système A a 4 états et le système B en a 8, le système combiné en a 4 × 8 = 32, et log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. C'est ce qui autorise à additionner les variétés logarithmiques de dimensions indépendantes.

### La loi d'Ashby

```
V(régulateur) >= V(perturbation)
```

« Seule la variété absorbe la variété. » Un système de gouvernance capable de produire moins de réponses distinctes qu'il n'affronte de perturbations distinctes échouera nécessairement à réguler certaines d'entre elles.

## Trois dimensions de la variété dans Demerzel

Dans un cadre de gouvernance, la variété n'est pas un nombre unique. Celle de Demerzel opère selon trois dimensions indépendantes.

### Dimension 1 : la variété comportementale (V_B)

**Ce qu'elle mesure :** l'éventail des comportements d'agent distincts que le système peut produire.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3,81 bits |
| Niveaux d'orientation vers un but | 4 | 2,00 bits |
| Configurations de voix (ton × verbosité × style) | ~27 | 4,75 bits |

**Amplification comportementale totale :** V_B_amp = 3,81 + 2,00 + 4,75 = **10,56 bits**

Autrement dit, Demerzel peut produire environ 2^10,56 = 1 506 configurations comportementales distinguables.

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Contraintes de persona (4 en moyenne par persona) | 56 | 5,81 bits |
| Appariements d'estimateur (fixés à skeptical-auditor) | 1 | 0 bit |

**Atténuation comportementale totale :** V_B_att = 5,81 bits

**Ratio de variété comportementale :** R_B = V_B_amp / V_B_att = 10,56 / 5,81 = **1,82**

Lecture : l'amplification comportementale dépasse l'atténuation d'un facteur 1,82. C'est sain : le système dispose de plus de capacité de réponse que de contraintes.

### Dimension 2 : la variété structurelle (V_S)

**Ce qu'elle mesure :** l'éventail des structures distinctes (formes de questions, motifs d'investigation, formats de sortie) que le système peut engendrer.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Grammaires | 27 | 4,75 bits |
| Productions grammaticales (12 en moyenne par grammaire) | ~324 | 8,34 bits |
| Départements de Streeling | 15 | 3,91 bits |

**Amplification structurelle totale :** V_S_amp = 4,75 + 8,34 + 3,91 = **17,00 bits**

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Seuils d'évolution des grammaires (T >= 0,7 ; C < 0,1) | 2 | 1,00 bit |
| Détection de péremption (fenêtre de 30 jours) | 1 | 0 bit |

**Atténuation structurelle totale :** V_S_att = 1,00 bit

**Ratio de variété structurelle :** R_S = V_S_amp / V_S_att = 17,00 / 1,00 = **17,00**

Lecture : la variété structurelle est très élevée au regard de l'atténuation. Cela reflète la nature générative des grammaires, amplificatrices de variété par construction. Mais ce ratio élevé signale aussi un risque : une contrainte structurelle insuffisante peut mener à une prolifération de grammaires sans contrôle de qualité.

### Dimension 3 : la variété régulatrice (V_R)

**Ce qu'elle mesure :** l'éventail des décisions de gouvernance distinctes que le système peut prendre.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| États de la logique tétravalente | 4 | 2,00 bits |
| Seuils de confiance | 5 | 2,32 bits |
| États PDCA | 4 | 2,00 bits |

**Amplification régulatrice totale :** V_R_amp = 2,00 + 2,32 + 2,00 = **6,32 bits**

**Atténuateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Politiques | 37 | 5,21 bits |
| Articles constitutionnels (Asimov et Défaut) | 17 | 4,09 bits |
| Catégories de la taxonomie des préjudices | 4 | 2,00 bits |

**Atténuation régulatrice totale :** V_R_att = 5,21 + 4,09 + 2,00 = **11,30 bits**

**Ratio de variété régulatrice :** R_R = V_R_amp / V_R_att = 6,32 / 11,30 = **0,56**

Lecture : l'atténuation régulatrice dépasse nettement l'amplification. C'est **voulu** : la gouvernance doit contraindre plus qu'elle n'amplifie. Un ratio régulateur inférieur à 1,0 signifie que le système est conservateur, ce qui s'accorde avec les lois d'Asimov (préférer la sûreté à la capacité).

## Le tableau de bord composite de la variété

### Synthèse

| Dimension | V_amplificateurs | V_atténuateurs | Ratio R | Évaluation |
|-----------|-------------|---------------|---------|------------|
| Comportementale (V_B) | 10,56 bits | 5,81 bits | 1,82 | Sain — plus de capacité de réponse que de contraintes |
| Structurelle (V_S) | 17,00 bits | 1,00 bit | 17,00 | Vigilance — forte générativité, faible contrainte |
| Régulatrice (V_R) | 6,32 bits | 11,30 bits | 0,56 | Voulu — la gouvernance est conservatrice |

### Plages saines

D'après la loi d'Ashby et les principes du MSV (CYB-001), les plages saines diffèrent selon la dimension :

| Dimension | Plage saine | Justification |
|-----------|---------------|-----------|
| Comportementale | 1,2 à 3,0 | Le système a besoin de plus d'options comportementales que de contraintes, sans être illimité |
| Structurelle | 2,0 à 10,0 | Les grammaires doivent être génératives, mais encadrées par des contrôles de qualité |
| Régulatrice | 0,3 à 0,8 | La gouvernance DOIT être sur-atténuée : c'est le principe de prudence |

### Évaluation actuelle

- **Comportementale (1,82) :** dans la plage saine. Aucune action nécessaire.
- **Structurelle (17,00) :** au-dessus de la plage saine. Les 27 grammaires et leurs ~324 productions sont faiblement contraintes. Recommandation : ajouter des contrôles de qualité structurels (exigences de couverture de test des grammaires, suivi de l'usage des productions).
- **Régulatrice (0,56) :** dans la plage saine. Le système est conservateur sans être paralysé.

## Le côté perturbation : que faut-il réguler ?

Le ratio de variété ne dit que la moitié de l'histoire. Il faut aussi mesurer la variété des perturbations auxquelles le système fait face.

### Perturbations externes (V_D_ext)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Dépôts consommateurs (ix, tars, ga) | 3 | 1,58 bit |
| Combinaisons d'états des dépôts (3 dépôts × ~10 états chacun) | 30 | 4,91 bits |
| Changements de l'environnement externe (bibliothèques, API, modèles) | ~100 | 6,64 bits |

**Variété totale des perturbations externes :** V_D_ext = **6,64 bits** (dominée par les changements d'environnement)

### Perturbations internes (V_D_int)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Changements d'état des croyances par cycle | ~20 | 4,32 bits |
| Interactions entre politiques (37 politiques, deux à deux) | 666 | 9,38 bits |
| Propositions d'évolution des grammaires | ~5 par cycle | 2,32 bits |

**Variété totale des perturbations internes :** V_D_int = **9,38 bits** (dominée par les interactions entre politiques)

### Vérification de la loi d'Ashby

Pour que la gouvernance soit viable :

```
V(réponse régulatrice) >= V(perturbation)
```

- V_R_amp = 6,32 bits
- V_D = max(V_D_ext, V_D_int) = 9,38 bits
- **Écart : 9,38 − 6,32 = 3,06 bits**

Le système régulateur affronte donc environ 2^3,06 = 8 fois plus de variété de perturbations qu'il ne peut produire de variété de réponses. Cet écart est absorbé par trois voies :

1. **L'escalade vers l'humain** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **Le passage outre constitutionnel** — les lois d'Asimov ramènent des décisions complexes à un choix binaire (sûr / non sûr), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente maîtrisables

Ce sont des mécanismes d'absorption de variété légitimes, mais l'écart de 3 bits suggère que Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que sa capacité régulatrice.

## Protocole de mesure

Pour suivre le ratio de variété dans le temps, Demerzel devrait calculer les indicateurs suivants à chaque cycle de gouvernance.

### Indicateur 1 : décompte des composants

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

### Indicateur 2 : ratios par dimension

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

### Indicateur 3 : détection de tendance

Suivre les ratios sur des cycles consécutifs. Alerter lorsque :
- un ratio franchit la borne de sa plage saine ;
- le ratio régulateur descend sous 0,3 (risque de paralysie du système) ;
- le ratio structurel dépasse 20,0 (risque de prolifération des grammaires) ;
- le ratio comportemental descend sous 1,0 (système sous-réactif).

### Indicateur 4 : taux de croissance des perturbations

Suivre V_perturbation dans le temps. Si la variété des perturbations croît plus vite que celle des réponses, la loi d'Ashby finira par être violée. C'est l'équivalent, en gouvernance, de la dette technique.

## Contre-validation par GPT-4o

La contre-validation avec GPT-4o a confirmé cinq points :

1. **V = log2(N) est bien la formule correcte** pour la variété d'Ashby. Les deux modèles sont d'accord.
2. **Le modèle additif (sommer les variétés logarithmiques) est valide** pour des dimensions indépendantes, mais trop simpliste dès que les composants interagissent. La séparation en dimensions (comportementale, structurelle, régulatrice) y répond en traitant chacune indépendamment.
3. **GPT-4o a calculé un ratio composite naïf de −2,8**, en traitant amplificateurs et atténuateurs comme une somme additive unique. C'est incorrect : une variété négative n'a pas de sens, puisqu'on ne peut pas avoir moins de zéro état distinguable. Le modèle dimensionnel évite cette erreur.
4. **Les deux modèles s'accordent sur le fait qu'un R_régulateur < 1,0 est attendu** pour un système de gouvernance. La gouvernance atténue par nature.
5. **L'écart régulateur de 3 bits** est un résultat inédit, absent de l'analyse de GPT-4o. Il n'apparaît qu'en calculant séparément la variété des perturbations, ce que GPT-4o n'a pas fait.

**Confiance de la contre-validation : 0,85** (T — les deux modèles s'accordent sur les fondamentaux ; l'affinage par dimension apporte plus que l'analyse de GPT-4o.)

## Conséquences pour Demerzel

1. **Suivre les ratios de variété à chaque cycle** — Ajouter un instantané de variété dans `state/governance/variety-metrics.json` (ou le fichier d'état équivalent) et surveiller la dérive des ratios par dimension.
2. **Ajouter des contrôles de qualité structurels** — Le ratio structurel (17,00) dépasse la plage saine. Introduire des exigences de couverture de test des grammaires et un suivi de l'usage des productions, pour augmenter l'atténuation sans réduire la générativité.
3. **Surveiller l'écart régulateur de 3 bits** — La complexité des interactions entre politiques (666 combinaisons deux à deux pour 37 politiques) est la première source de perturbation interne. À mesure que les politiques se multiplient, cet écart se creusera de façon quadratique. Envisager un regroupement ou une organisation hiérarchique des politiques.
4. **L'escalade vers l'humain est un pont de variété** — Le système de seuils de confiance (article 6 : escalade) est le mécanisme principal par lequel Demerzel absorbe la variété qui dépasse sa capacité régulatrice. C'est une fonctionnalité, pas une limite.
5. **Faire évoluer la section 6 de la grammaire** — La section sur la variété requise de `sci-cybernetics.ebnf` (lignes 78 à 82) devrait être étendue par des productions de mesure quantitative.

## Lien avec CYB-001 et CYB-002

- **CYB-001** a établi que la loi d'Ashby s'applique à Demerzel et a listé qualitativement les amplificateurs et atténuateurs de variété. CYB-003 rend cela quantitatif.
- **La recommandation 5 de CYB-001** (« surveiller le ratio de variété ») est désormais opérationnelle : formules précises, plages saines et protocole de mesure.
- **CYB-002** traitait de l'amortissement du système 2. Les bandes mortes et l'hystérésis y sont elles-mêmes des atténuateurs de variété : elles réduisent la variété des signaux circulant dans les canaux de coordination. Une fois mises en œuvre, elles devront entrer dans l'indicateur d'atténuation structurelle de CYB-003.

## Sources

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Chapitre 7 : Quantity of Variety ; chapitre 11 : Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Chapitre 6 : Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). « A Mathematical Theory of Communication ». Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). « What is variety engineering and why do we need it? » Systems Research and Behavioral Science.
- Fathom (2025). Ateliers Ashby — gouvernance de l'IA et variété requise, modèle des organisations de vérification indépendantes (IVO).

## Questions de suivi pour le cycle 004

1. L'écart régulateur de 3 bits peut-il être comblé par un regroupement hiérarchique des politiques, qui ramènerait les interactions deux à deux de O(n²) à O(n log n) ?
2. Comment suivre l'usage des productions grammaticales, afin de détecter les productions mortes et d'éclairer l'atténuation structurelle ?
3. Quelle est la relation, du point de vue de la théorie de l'information, entre la logique tétravalente de Demerzel (T/F/U/C) et l'entropie de Shannon : l'état U (inconnu) porte-t-il plus de bits que l'état T (vrai) ?

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md`
- Prérequis : `state/streeling/courses/cybernetics/en/cyb-002-active-dampening-cross-repo-oscillation.md`
- Grammaire : `grammars/sci-cybernetics.ebnf` (section 6, variété requise)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
