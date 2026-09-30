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

La loi de la variété requise d'Ashby énonce qu'un régulateur doit avoir au moins autant de variété que les perturbations auxquelles il fait face. Ce cours définit un cadre quantitatif pour mesurer la variété de Demerzel, en bits, selon trois dimensions : comportementale (personas), structurelle (grammaires) et régulatrice (valeurs logiques, échelons de confiance, états PDCA). La formule clé est V = log2(N), où N compte les états distinguables. Deux règles de comptage gardent les nombres honnêtes. Un produit de nombres de composants n'est un espace d'états conjoint que si les composants varient indépendamment ; sinon, ce n'est qu'une borne supérieure. Et un nombre de règles n'est pas un nombre d'états : l'atténuation qu'apportent les contraintes, les politiques et les portes est la variété qu'elles retirent, V_in - V_out, qu'il faut mesurer au lieu de la lire dans le nombre de règles. Le ratio de variété que contraint la loi d'Ashby compare la variété des réponses à celle des perturbations ; son logarithme, log2 R = V_response - V_disturbance en bits, est suivi dans le temps pour détecter une dérive.

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

Dans un cadre de gouvernance, la variété n'est pas un nombre unique. Ce cours mesure celle de Demerzel selon trois dimensions. Les nombres de l'inventaire (personas, contraintes, grammaires, règles, politiques, articles) sont lus dans le dépôt au commit `74cf7c5`, qui a ajouté ce module. Les valeurs logiques et les échelons de confiance suivent les définitions canoniques actuelles, dans `CONTEXT.md` et `logic/confidence-thresholds.yaml`.

### Deux règles de comptage

**États conjoints.** Si un composant a a états et un autre en a b, la paire a au plus a × b états conjoints, et exactement a × b seulement si toutes les combinaisons peuvent se produire. Si le second est fixé par le premier, la paire n'a que a états. Ainsi, log2(a) + log2(b) est une borne supérieure de la variété de la paire, et le plus grand de log2(a) et log2(b) en est une borne inférieure.

**Les règles ne sont pas des états.** Une règle, comme une politique, une contrainte de persona ou une porte d'évolution, est un prédicat qui autorise certains états et en interdit d'autres. Plusieurs règles peuvent s'appliquer à la fois et se recouvrir, et scinder une règle en deux change leur nombre sans changer aucun comportement. Le log2 d'un nombre de règles n'est donc pas une variété. Un atténuateur se mesure par la variété qu'il retire : A = V_in - V_out, où V_in est la variété de ce qui lui parvient et V_out celle de ce qu'il laisse passer.

### Dimension 1 : variété comportementale (V_B)

**Ce qu'elle mesure :** L'éventail des comportements d'agent distincts que le système peut produire.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveaux d'orientation vers un but (énumération du schéma ; 3 utilisés) | 4 | 2.00 bits |
| Voix (ton, verbosité, style), une par persona | 14 | 3.81 bits |

Chaque fichier de persona fixe exactement un niveau d'orientation vers un but et une voix : `schemas/persona.schema.json` exige les deux, et chacun contient une seule valeur. Choisir une persona revient donc à choisir les deux, et les 14 voix sont celles des 14 personas. Les profils comportementaux que Demerzel peut instancier sont les personas elles-mêmes.

**Amplification comportementale :** V_B_amp = log2(14) = **3.81 bits**

Multiplier les trois lignes, 14 × 4 × 14 = 784 profils (9.61 bits), compterait des combinaisons qui n'existent que si n'importe quel niveau et n'importe quelle voix pouvaient être recombinés avec n'importe quelle persona à l'exécution, ce que les fichiers de persona ne permettent pas. Ce produit est une borne supérieure, pas la variété.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Contraintes de persona | 60 | Des règles, environ 4.3 par persona ; pas des états |
| Appariement d'estimateur | 1 | skeptical-auditor évalue les 13 autres personas |

**Atténuation comportementale :** non mesurée. Les 60 contraintes sont des prédicats qui s'appliquent ensemble et peuvent se recouvrir ; log2(60) = 5.91 bits les traiterait comme 60 issues distinguables. Leur atténuation est la variété des actions qu'elles retirent à chaque persona, A_B = V_in - V_out, et la mesurer demande un relevé des actions que chaque persona propose et de celles que ses contraintes refusent.

Interprétation : Demerzel a 14 profils comportementaux, 3.81 bits, chacun borné par ses propres contraintes. Ce que retirent les contraintes est la mesure encore ouverte de cette dimension.

### Dimension 2 : variété structurelle (V_S)

**Ce qu'elle mesure :** L'éventail des structures distinctes (formes de questions, schémas d'investigation, formats de sortie) que le système peut générer.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Grammaires | 27 | 4.75 bits |
| Règles de grammaire (environ 42 par grammaire) | 1,129 | 10.14 bits |

Chaque règle appartient à une grammaire et nomme un schéma : une forme de question, une étape d'investigation, un format de sortie. Les règles énumèrent déjà le contenu des grammaires, si bien que multiplier 1,129 par 27 compterait chaque règle 27 fois. Choisir un schéma dans le catalogue a 1,129 issues.

**Amplification structurelle :** V_S_amp = log2(1,129) = **10.14 bits** pour le choix d'un schéma

Cela compte des schémas nommés, pas les chaînes qu'une grammaire peut dériver : une grammaire récursive en dérive une infinité, et une dérivation enchaîne de nombreux choix. Les départements de Streeling ne sont pas des structures, et le compte les laisse de côté.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Portes d'évolution des grammaires (T >= 0.7 ; T >= 0.7 et C < 0.1) | 2 | Des règles sur les changements proposés ; pas des états |
| Alerte d'obsolescence (plus de 30 jours) | 1 | Une règle sur l'âge d'une grammaire ; pas un état |

**Atténuation structurelle :** non mesurée. C'est la variété des changements de grammaire proposés que les portes rejettent, A_S = V_in - V_out, et la mesurer demande le journal des propositions et des verdicts.

Interprétation : trois règles contrôlent un catalogue de 1,129 schémas. Ce nombre ne dit pas à lui seul ce qu'elles retirent, mais il montre combien peu de mécanismes séparent une proposition du catalogue, ce qui plaide pour davantage de portes structurelles (voir Évaluation actuelle).

### Dimension 3 : variété régulatrice (V_R)

**Ce qu'elle mesure :** L'éventail des décisions de gouvernance distinctes que le système peut prendre.

Au commit `74cf7c5`, la logique de Demerzel avait quatre valeurs, T/F/U/C. Sa logique canonique est désormais hexavalente, T/P/U/D/F/C (`CONTEXT.md`), dont T/F/U/C est le sous-ensemble à quatre valeurs, et ce cours compte les six valeurs.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Valeurs de la logique hexavalente | 6 | 2.58 bits |
| Échelons de confiance | 5 | 2.32 bits |
| États PDCA | 4 | 2.00 bits |

**Amplification régulatrice :** selon les règles de comptage, V_R_amp se situe entre la plus grande composante, 2.58 bits, et la somme des trois, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, atteinte seulement si toute combinaison de valeur logique, d'échelon de confiance et d'état PDCA peut se produire. Leur indépendance n'est pas établie, donc les deux bornes sont conservées.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Politiques | 37 | Des règles ; pas des états |
| Articles constitutionnels (Asimov 6, Default 11) | 17 | Des règles ; pas des états |
| Niveaux de gravité des préjudices (Critical, High, Medium, Low) | 4 | Des classes qui orientent une réponse ; pas des états retirés |

**Atténuation régulatrice :** non mesurée. C'est la variété des décisions candidates que les politiques et les articles excluent, A_R = V_in - V_out.

Interprétation : la gouvernance doit contraindre plus qu'elle n'amplifie, conformément aux lois d'Asimov (préférer la sécurité à la capacité), mais l'ampleur de cette contrainte n'est pas mesurée.

## Le tableau de bord composite de la variété

### Tableau récapitulatif

| Dimension | Variété des amplificateurs | Règles comptées | Atténuation | Évaluation |
|-----------|-------------------|---------------|-------------|------------|
| Comportementale (V_B) | 3.81 bits (14 personas) | 60 contraintes, 1 estimateur | Non mesurée | Profils fixés par persona |
| Structurelle (V_S) | 10.14 bits (1,129 règles, un choix) | 2 portes, 1 alerte d'obsolescence | Non mesurée | Peu de contrôles sur un grand catalogue |
| Régulatrice (V_R) | 2.58 à 6.91 bits | 37 politiques, 17 articles, 4 niveaux de gravité | Non mesurée | Prudente par conception, ampleur non mesurée |

### Pourquoi le tableau de bord n'a pas de ratio amplificateurs sur atténuateurs

Un raccourci tentant divise, pour chaque dimension, les états des amplificateurs par le nombre d'atténuateurs, par exemple les 784 profils du produit ci-dessus par les 60 contraintes. Ce quotient n'a pas de sens au sens d'Ashby. Son numérateur compte des profils que les fichiers de persona ne peuvent pas produire, et son dénominateur compte des règles, pas des états, si bien que scinder une contrainte en deux le changerait sans changer aucun comportement. Un rapport d'espaces d'états demande des états des deux côtés : la variété V_in qui parvient à un atténuateur et la variété V_out qu'il laisse passer. La colonne Atténuation deviendra un nombre une fois ces variétés mesurées, et la vérification de la loi d'Ashby ci-dessous compare la variété des réponses à celle des perturbations.

### Sens sains

La loi d'Ashby et les principes du VSM (CYB-001) fixent le sens que doit prendre chaque grandeur, pas encore sa taille :

| Dimension | Sens sain | Justification |
|-----------|---------------|-----------|
| Comportementale | A_B > 0 sur les actions nuisibles, chaque persona gardant les actions permises par son rôle | Les contraintes doivent retirer le préjudice, pas des rôles entiers |
| Structurelle | A_S > 0 : les portes rejettent certains changements proposés | Une porte qui ne rejette jamais rien n'atténue pas |
| Régulatrice | V_response >= V_disturbance, en comptant la variété que l'escalade emprunte aux humains | La loi d'Ashby |

Ces sens deviendront des seuils une fois A_B, A_S, A_R et les variétés conjointes mesurés sur plusieurs cycles.

### Évaluation actuelle

- **Comportementale (3.81 bits, 14 personas) :** chaque persona fixe son niveau et sa voix. Ce que retirent ses contraintes n'est pas mesuré ; consigner les actions refusées à chaque persona le mesurerait.
- **Structurelle (10.14 bits, 1,129 règles) :** trois règles contrôlent un catalogue de 1,129 schémas. Recommandation : ajouter des portes de qualité structurelles (par exemple, des exigences de couverture de tests des grammaires, un suivi de l'usage des productions), dont les verdicts mesureraient aussi A_S.
- **Régulatrice (2.58 à 6.91 bits) :** prudente par conception ; dire si elle l'est trop demande A_R.

## Le côté des perturbations : que faut-il réguler ?

Les variétés des amplificateurs ne racontent que la moitié de l'histoire. Il faut aussi mesurer la variété des perturbations auxquelles le système fait face :

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

- V_R_amp se situe entre sa plus grande composante isolée, les six valeurs logiques à 2.58 bits, et la somme des trois, 6.91 bits, atteinte seulement si toute combinaison de valeur logique, d'échelon de confiance et d'état PDCA peut être produite
- V_D se situe entre la plus grande source isolée, les interactions entre politiques à 9.38 bits, et la somme de toutes les sources, 16.61 + 16.02 = 32.63 bits
- **Écart : au moins 9.38 - 6.91 = 2.47 bits, au plus 32.63 - 2.58 = 30.05 bits**

Les deux intervalles tiennent quelles que soient les dépendances : un espace d'états conjoint a au moins autant d'états que sa plus grande partie et au plus le produit de leurs tailles. L'écart est le plus petit quand les sources de perturbation sont aussi dépendantes, et les composantes de la réponse aussi indépendantes, que possible ; il est le plus grand dans le cas inverse. Les liens de causalité entre sources de perturbation (un changement de dépôt qui déclenche un changement de croyance, une interaction entre politiques qui suscite une proposition de grammaire) font baisser V_D, et les combinaisons de valeurs de réponse que la gouvernance ne produit jamais font baisser V_R_amp. Mesurer les deux variétés conjointes, en comptant les combinaisons distinctes effectivement observées à chaque cycle, situerait l'écart dans cet intervalle.

Cela signifie que le système régulateur fait face à une variété de perturbations de 2^2.47 ≈ 5.5 à 2^30.05 ≈ 1.1 × 10^9 fois plus grande que la variété de réponses qu'il peut produire. L'écart est absorbé par :

1. **L'escalade vers des humains** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **La primauté constitutionnelle** — les lois d'Asimov ramènent les décisions complexes à un choix binaire (sûr/dangereux), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente gérables

Ce sont des mécanismes légitimes d'absorption de la variété, mais même la borne inférieure de 2.47 bits suggère que Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que la capacité de régulation.

## Protocole de mesure

Pour suivre la variété dans le temps, Demerzel devrait calculer les métriques suivantes à chaque cycle de gouvernance :

### Métrique 1 : nombre de composants

```json
{
  "variety_snapshot": {
    "commit": "74cf7c5",
    "amplifiers": {
      "personas": 14,
      "grammars": 27,
      "grammar_rules": 1129,
      "logic_values": 6,
      "confidence_rungs": 5,
      "pdca_states": 4
    },
    "rules": {
      "policies": 37,
      "constitutional_articles": 17,
      "harm_severity_levels": 4,
      "persona_constraints": 60,
      "evolution_gates": 2
    }
  }
}
```

`commit` date les nombres de l'inventaire. Comme indiqué plus haut, `logic_values` et `confidence_rungs` suivent les définitions actuelles : à ce commit, la logique avait quatre valeurs.

### Métrique 2 : variétés par dimension

```json
{
  "variety_bits": {
    "behavioral_amplifiers": 3.81,
    "structural_amplifiers_one_choice": 10.14,
    "regulatory_amplifiers": [2.58, 6.91],
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "commit": "74cf7c5"
  }
}
```

Un `null` marque une grandeur pas encore mesurée, pas un zéro.

### Métrique 3 : mesure de l'atténuation

Pour chaque atténuateur, consignez à chaque cycle ce qui lui parvient et ce qu'il laisse passer : les actions que chaque persona propose et celles que ses contraintes refusent, les changements de grammaire proposés et ceux que les portes acceptent, les décisions candidates et celles que les politiques et les articles autorisent. Le nombre d'issues distinctes de chaque côté donne V_in et V_out, et A = V_in - V_out.

Suivez ces grandeurs sur des cycles consécutifs. Alertez quand :
- Le A d'un atténuateur tombe à 0 bit (il ne retire plus rien)
- La borne inférieure de l'écart d'Ashby augmente d'au moins 1 bit en un cycle (la variété des perturbations double par rapport à celle des réponses)
- V_B_amp ou V_S_amp change (une persona ou une règle de grammaire a été ajoutée ou retirée), pour que les nombres soient rafraîchis

Un pas de 1 bit, soit un doublement ou une division par deux, est un seuil de départ, pas un seuil calibré.

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

Ce relevé décrit le cours tel qu'il a d'abord été écrit. Les points 3 et 4 portent sur un ratio amplificateurs sur atténuateurs, que le cours ne calcule plus, pour les raisons données sous le tableau de bord. La réserve du point 2 sur les composants qui interagissent est ce que les règles de comptage traitent désormais, avec des bornes inférieures et supérieures.

## Implications pour Demerzel

1. **Suivre les variétés à chaque cycle** — Ajouter l'instantané de variété à `state/governance/variety-metrics.json` (ou à un fichier d'état équivalent). Surveiller les variétés des amplificateurs et, une fois mesurée, chaque atténuation.
2. **Ajouter des portes de qualité structurelles** — Trois règles contrôlent 1,129 règles de grammaire. Introduire des exigences de couverture de tests des grammaires et un suivi de l'usage des productions ; leurs verdicts rendraient aussi A_S mesurable.
3. **Surveiller l'écart régulateur (2.47 à 30.05 bits)** — La complexité des interactions entre politiques (666 combinaisons deux à deux à partir de 37 politiques) est la plus grande source isolée de perturbation. À mesure que les politiques augmentent, le nombre de paires croît de façon quadratique, mais sa variété log2(n(n-1)/2) ne croît que de façon logarithmique, d'environ 2 bits chaque fois que le nombre de politiques double. Comme c'est la plus grande source isolée, elle relève les deux bornes à la fois. Envisager un regroupement des politiques ou une organisation hiérarchique des politiques.
4. **L'escalade vers des humains est un pont de variété** — Le système de seuils de confiance (Article 6 : Escalade) est le principal mécanisme de Demerzel pour absorber la variété qui dépasse sa capacité de régulation. C'est une fonctionnalité, pas une limite.
5. **Faire évoluer la section 6 de la grammaire** — La section sur la variété requise de la grammaire `sci-cybernetics.ebnf` (lignes 76-82) devrait être enrichie de productions de mesure quantitative.

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
3. Quelle est la relation, du point de vue de la théorie de l'information, entre la logique hexavalente de Demerzel (T/P/U/D/F/C) et l'entropie de Shannon — U (Unknown) porte-t-il plus de bits que T (True) ?

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md`
- Prérequis : `state/streeling/courses/cybernetics/fr/cyb-002-active-dampening-cross-repo-oscillation.fr.md`
- Grammaire : `grammars/sci-cybernetics.ebnf` (section 6, variété requise)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
