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

La loi de la variété requise d'Ashby énonce qu'un régulateur doit avoir au moins autant de variété que les perturbations auxquelles il fait face. Ce cours définit un cadre quantitatif pour mesurer la variété de Demerzel, en bits, selon trois dimensions : comportementale (personas), structurelle (grammaires) et régulatrice (les décisions et les étiquettes qu'elles portent). La formule clé est V = log2(N), où N compte les issues distinguables. Trois règles de comptage gardent les nombres honnêtes. Un produit de nombres de composants n'est un espace d'états conjoint que si les composants varient indépendamment ; sinon, ce n'est qu'une borne supérieure. Un nombre de règles n'est pas un nombre d'états : l'atténuation qu'apportent les contraintes, les politiques et les portes est la variété qu'elles retirent, V_in - V_out. Et un inventaire n'est pas un ensemble d'issues : les définitions de règles, les étiquettes de décision et les paires de politiques sont ce que le dépôt définit, pas les structures, les réponses et les perturbations qui se produisent. L'inventaire est compté à un commit ; les variétés que compare la loi d'Ashby doivent être mesurées. Le ratio de variété que contraint la loi compare la variété des réponses à celle des perturbations ; son logarithme, log2 R = V_response - V_disturbance en bits, sera suivi dans le temps pour détecter une dérive, une fois les deux côtés mesurés.

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

### Trois règles de comptage

**États conjoints.** Si un composant a a états et un autre en a b, la paire a au plus a × b états conjoints, et exactement a × b seulement si toutes les combinaisons peuvent se produire. Si le second est fixé par le premier, la paire n'a que a états. Ainsi, log2(a) + log2(b) est une borne supérieure de la variété de la paire, et le plus grand de log2(a) et log2(b) en est une borne inférieure.

**Les règles ne sont pas des états.** Une règle, comme une politique, une contrainte de persona ou une porte d'évolution, est un prédicat qui autorise certains états et en interdit d'autres. Plusieurs règles peuvent s'appliquer à la fois et se recouvrir, et scinder une règle en deux change leur nombre sans changer aucun comportement. Le log2 d'un nombre de règles n'est donc pas une variété. Un atténuateur se mesure par la variété qu'il retire : A = V_in - V_out, où V_in est la variété de ce qui lui parvient et V_out celle de ce qu'il laisse passer.

**Un inventaire n'est pas un ensemble d'issues.** Un nombre d'éléments définis par le dépôt ne borne les issues que si chaque élément peut se produire seul, comme une issue. Une dérivation de grammaire utilise plusieurs définitions de règles à la fois, une même étiquette de décision peut couvrir plusieurs actions différentes, et une paire de politiques n'est une interaction que si les deux interagissent réellement. La variété se compte sur les issues : les structures distinctes générées, les réponses données et les perturbations rencontrées.

### Dimension 1 : variété comportementale (V_B)

**Ce qu'elle mesure :** L'éventail des comportements d'agent distincts que le système peut produire.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveaux d'orientation vers un but (énumération du schéma ; 3 utilisés) | 4 | 2.00 bits |
| Voix (ton, verbosité, style), une par persona | 14 | 3.81 bits |

Chaque fichier de persona fixe exactement un niveau d'orientation vers un but et une voix : `schemas/persona.schema.json` exige les deux, et chacun contient une seule valeur. Choisir une persona revient donc à choisir les deux, et les 14 voix sont celles des 14 personas. Les profils comportementaux que Demerzel peut instancier sont les personas elles-mêmes.

**Choix de la persona :** V_B_persona = log2(14) = **3.81 bits**, la variété du choix de la persona qui agit. Les actions qu'une persona peut ensuite entreprendre ne sont pas comptées ici ; c'est ce que consigne la mesure de l'atténuation (métrique 3).

Multiplier les trois lignes, 14 × 4 × 14 = 784 profils (9.61 bits), compterait des combinaisons qui n'existent que si n'importe quel niveau et n'importe quelle voix pouvaient être recombinés avec n'importe quelle persona à l'exécution, ce que les fichiers de persona ne permettent pas. Ce produit est une borne supérieure, pas la variété.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Contraintes de persona | 60 | Des règles, environ 4.3 par persona ; pas des états |
| Appariement d'estimateur | 1 | skeptical-auditor évalue les 13 autres personas |

**Atténuation comportementale :** non mesurée. Les 60 contraintes sont des prédicats qui s'appliquent ensemble et peuvent se recouvrir ; log2(60) = 5.91 bits les traiterait comme 60 issues distinguables. Leur atténuation est la variété des actions qu'elles retirent à chaque persona, A_B = V_in - V_out, et la mesurer demande un relevé des actions que chaque persona propose et de celles que ses contraintes refusent.

Interprétation : Demerzel a 14 profils comportementaux, 3.81 bits de choix de persona, chacun borné par ses propres contraintes. Ce que retirent les contraintes est la mesure encore ouverte de cette dimension.

### Dimension 2 : variété structurelle (V_S)

**Ce qu'elle mesure :** L'éventail des structures distinctes (formes de questions, schémas d'investigation, formats de sortie) que le système peut générer.

**Inventaire :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Grammaires | 27 | Des fichiers de grammaire |
| Définitions de règles de grammaire (environ 42 par grammaire) | 1,129 | Des définitions de non-terminaux ; pas des structures |

Une grammaire dérive une structure en composant des définitions de règles : `grammars/sci-cybernetics.ebnf`, par exemple, construit une investigation à partir de plusieurs non-terminaux à la fois, et une grammaire récursive dérive une infinité de structures. Les 1,129 définitions ne sont donc pas 1,129 structures mutuellement exclusives, et log2(1,129) = 10.14 bits est la taille de l'inventaire, pas une variété structurelle.

**Variété structurelle :** non mesurée. C'est le nombre de structures distinctes que les grammaires génèrent réellement au cours d'un cycle, et la mesurer demande un journal des dérivations produites. Les départements de Streeling ne sont pas des structures, et l'inventaire les laisse de côté.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Portes d'évolution des grammaires (T >= 0.7 ; T >= 0.7 et C < 0.1) | 2 | Des règles sur les changements proposés ; pas des états |
| Alerte d'obsolescence (plus de 30 jours) | 1 | Une règle sur l'âge d'une grammaire ; pas un état |

**Atténuation structurelle :** non mesurée. C'est la variété des changements de grammaire proposés que les portes rejettent, A_S = V_in - V_out, et la mesurer demande le journal des propositions et des verdicts.

Interprétation : trois règles contrôlent 27 grammaires qui contiennent 1,129 définitions de règles. L'inventaire ne dit pas à lui seul ce qu'elles retirent, mais il montre combien peu de mécanismes séparent une proposition des grammaires, ce qui plaide pour davantage de portes structurelles (voir Évaluation actuelle).

### Dimension 3 : variété régulatrice (V_R)

**Ce qu'elle mesure :** L'éventail des décisions de gouvernance distinctes que le système peut prendre.

Au commit `74cf7c5`, la logique de Demerzel avait quatre valeurs, T/F/U/C. Sa logique canonique est désormais hexavalente, T/P/U/D/F/C (`CONTEXT.md`), dont T/F/U/C est le sous-ensemble à quatre valeurs, et ce cours compte les six valeurs.

**Étiquettes de décision :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Valeurs de la logique hexavalente | 6 | 2.58 bits |
| Échelons de confiance | 5 | 2.32 bits |
| États PDCA | 4 | 2.00 bits |

**Variété des étiquettes :** selon les règles de comptage, la variété du triplet d'étiquettes se situe entre la plus grande composante, 2.58 bits, et la somme des trois, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, atteinte seulement si toute combinaison de valeur logique, d'échelon de confiance et d'état PDCA peut se produire. Leur indépendance n'est pas établie, donc les deux bornes sont conservées.

Ces étiquettes classent une décision ; elles ne comptent pas les réponses. Une valeur de vérité énonce une croyance, un échelon de confiance oriente l'exécution et un état PDCA est une étape du flux de travail, si bien que plusieurs actions différentes, dont une escalade, peuvent porter le même triplet. La variété des étiquettes ne borne donc en rien la variété des réponses V_R_amp, qui n'est **pas mesurée** : la mesurer demande un relevé des actions distinctes que prend la gouvernance, escalades comprises.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Politiques | 37 | Des règles ; pas des états |
| Articles constitutionnels (Asimov 6, Default 11) | 17 | Des règles ; pas des états |
| Niveaux de gravité des préjudices (Critical, High, Medium, Low) | 4 | Des classes qui orientent une réponse ; pas des états retirés |

**Atténuation régulatrice :** non mesurée. C'est la variété des décisions candidates que les politiques et les articles excluent, A_R = V_in - V_out.

Interprétation : la gouvernance doit contraindre plus qu'elle n'amplifie, conformément aux lois d'Asimov (préférer la sécurité à la capacité), mais ni la variété de ses réponses ni l'ampleur de cette contrainte ne sont mesurées.

## Le tableau de bord composite de la variété

### Tableau récapitulatif

| Dimension | Inventaire à `74cf7c5` | Variété établie | Atténuation | Évaluation |
|-----------|------------------------|---------------------|-------------|------------|
| Comportementale (V_B) | 14 personas, 60 contraintes, 1 estimateur | Choix de la persona : 3.81 bits | Non mesurée | Profils fixés par persona |
| Structurelle (V_S) | 27 grammaires, 1,129 définitions de règles, 2 portes, 1 alerte d'obsolescence | Non mesurée | Non mesurée | Peu de contrôles sur de nombreuses grammaires |
| Régulatrice (V_R) | 6 valeurs, 5 échelons, 4 états PDCA ; 37 politiques, 17 articles, 4 niveaux de gravité | Étiquettes : 2.58 à 6.91 bits ; réponses non mesurées | Non mesurée | Prudente par conception, ampleur non mesurée |

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

- **Comportementale (3.81 bits de choix de persona, 14 personas) :** chaque persona fixe son niveau et sa voix. Ce que retirent ses contraintes n'est pas mesuré ; consigner les actions refusées à chaque persona le mesurerait.
- **Structurelle (27 grammaires, 1,129 définitions de règles) :** trois règles les contrôlent, et aucune variété structurelle n'est mesurée. Recommandation : ajouter des portes de qualité structurelles (par exemple, des exigences de couverture de tests des grammaires, un suivi de l'usage des productions), dont les verdicts mesureraient aussi A_S, et consigner les dérivations produites, ce qui mesurerait V_S.
- **Régulatrice (étiquettes de 2.58 à 6.91 bits) :** prudente par conception ; dire si elle l'est trop, ou si elle a assez de variété de réponse, demande A_R et V_R_amp.

## Le côté des perturbations : que faut-il réguler ?

Le côté des amplificateurs ne raconte que la moitié de l'histoire. Il faut aussi estimer la variété des perturbations auxquelles le système fait face. Les valeurs des tableaux ci-dessous sont des estimations, pas des mesures, et l'une d'elles est une borne supérieure :

### Perturbations externes (V_D_ext)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Dépôts consommateurs (ix, tars, ga) | 3 | 1.58 bits |
| Combinaisons d'états des dépôts (3 dépôts x ~10 états chacun) | 10 à 10^3 = 1000 | 3.32 à 9.97 bits |
| Changements de l'environnement externe (bibliothèques, API, modèles) | ~100 | 6.64 bits |

**Variété totale des perturbations externes :** les combinaisons d'états des dépôts couvrent déjà les trois dépôts, donc la première ligne n'ajoute rien. Cette ligne est elle-même une fourchette : avec environ 10 états chacun, les trois dépôts ont entre 10 états conjoints (3.32 bits), si l'état de l'un détermine celui des autres, et 10^3 = 1000 (9.97 bits), s'ils varient indépendamment. Si les estimations tiennent, la ligne de l'environnement est alors le plus grand terme isolé : V_D_ext vaut au moins **6.64 bits**, et au plus log2(1000 × 100) = 9.97 + 6.64 = **16.61 bits** si un changement de l'environnement peut survenir dans n'importe lequel des 1000 états des dépôts.

### Perturbations internes (V_D_int)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Changements d'état de croyance par cycle | ~20 | 4.32 bits |
| Paires de politiques (37 politiques) | au plus 666 | au plus 9.38 bits |
| Propositions d'évolution des grammaires | ~5 par cycle | 2.32 bits |

666 est le nombre de paires de politiques, une borne supérieure du nombre d'interactions deux à deux distinctes : seules comptent les paires qui interagissent réellement, et rien ici ne mesure combien le font.

**Variété totale des perturbations internes :** si les estimations tiennent, V_D_int vaut au moins **4.32 bits** (les seuls changements de croyance), et au plus log2(20 × 666 × 5) = 4.32 + 9.38 + 2.32 = **16.02 bits** si toutes les paires de politiques interagissent et que les trois sources sont indépendantes. Les paires de politiques ne donnent aucune borne inférieure, puisque leur nombre est lui-même une borne supérieure.

### Vérification de la loi d'Ashby

Pour que la gouvernance soit viable :

```
V(réponse régulatrice) >= V(perturbation)
```

- V_R_amp, la variété des réponses, n'est pas mesurée. L'inventaire ne donne que la variété des étiquettes, entre 2.58 et 6.91 bits, qui ne la borne pas (voir la dimension 3)
- Si les estimations tiennent, V_D se situe entre la plus grande source estimée isolée, les changements de l'environnement à 6.64 bits, et la somme de toutes les sources, 16.61 + 16.02 = 32.63 bits
- **Écart : non calculé.** Aucun des deux côtés n'est mesuré, et les inventaires sont compatibles avec un surplus comme avec un grand déficit

Les deux intervalles tiennent quelles que soient les dépendances, étant donné les estimations : un espace d'états conjoint a au moins autant d'états que sa plus grande partie et au plus le produit de leurs tailles. Les intervalles montrent aussi combien peu les inventaires tranchent. En bas, environ 100 changements de l'environnement distincts (6.64 bits), c'est moins que les 120 triplets d'étiquettes (6.91 bits) : même les étiquettes pourraient en principe les distinguer. En haut, 32.63 bits représentent environ 6.7 × 10^9 états de perturbation, bien au-delà de tout nombre d'étiquettes. Mesurer les deux variétés conjointes, en comptant les perturbations distinctes rencontrées et les réponses distinctes données à chaque cycle, situerait l'écart, s'il existe.

Si les perturbations dépassent les réponses, la différence doit être absorbée par :

1. **L'escalade vers des humains** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **La primauté constitutionnelle** — les lois d'Asimov ramènent les décisions complexes à un choix binaire (sûr/dangereux), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente gérables

Ce sont des mécanismes légitimes d'absorption de la variété. S'ils suffisent, c'est ce que montrerait la mesure des deux côtés, et Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que la capacité de régulation.

## Protocole de mesure

Pour suivre la variété dans le temps, Demerzel devrait calculer les métriques suivantes à chaque cycle de gouvernance :

### Métrique 1 : nombres de l'inventaire

```json
{
  "variety_snapshot": {
    "commit": "74cf7c5",
    "inventory": {
      "personas": 14,
      "grammars": 27,
      "grammar_rule_definitions": 1129,
      "logic_values": 6,
      "confidence_rungs": 5,
      "pdca_states": 4,
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
    "persona_selection": 3.81,
    "decision_labels": [2.58, 6.91],
    "structures_generated": null,
    "responses": null,
    "disturbances": null,
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "commit": "74cf7c5"
  }
}
```

Un `null` marque une grandeur pas encore mesurée, pas un zéro.

### Métrique 3 : mesure des issues et de l'atténuation

Pour chaque atténuateur, consignez à chaque cycle ce qui lui parvient et ce qu'il laisse passer : les actions que chaque persona propose et celles que ses contraintes refusent, les changements de grammaire proposés et ceux que les portes acceptent, les décisions candidates et celles que les politiques et les articles autorisent. Le nombre d'issues distinctes de chaque côté donne V_in et V_out, et A = V_in - V_out. Consignez de la même façon les structures distinctes que génèrent les grammaires (V_S), les réponses distinctes que donne la gouvernance, escalades comprises (V_R_amp), et les perturbations distinctes qu'elle rencontre (V_D).

Suivez ces grandeurs sur des cycles consécutifs. Alertez quand :
- Le A d'un atténuateur tombe à 0 bit (il ne retire plus rien)
- L'écart V_D - V_R_amp augmente d'au moins 1 bit en un cycle (la variété des perturbations double par rapport à celle des réponses)
- L'inventaire change (une persona, une règle de grammaire ou une politique a été ajoutée ou retirée), pour que les nombres soient rafraîchis

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

Ce relevé décrit le cours tel qu'il a d'abord été écrit. Les points 3 et 4 portent sur un ratio amplificateurs sur atténuateurs, et le point 5 sur un écart calculé à partir des nombres de l'inventaire ; le cours ne calcule plus ni l'un ni l'autre, pour les raisons données sous le tableau de bord et dans la vérification de la loi d'Ashby. La réserve du point 2 sur les composants qui interagissent est ce que les règles de comptage traitent désormais, avec des bornes inférieures et supérieures.

## Implications pour Demerzel

1. **Suivre les variétés à chaque cycle** — Ajouter l'instantané de l'inventaire à `state/governance/variety-metrics.json` (ou à un fichier d'état équivalent). Consigner l'inventaire et, une fois mesurées, les variétés des structures, des réponses et des perturbations, ainsi que chaque atténuation.
2. **Ajouter des portes de qualité structurelles** — Trois règles contrôlent 1,129 définitions de règles de grammaire. Introduire des exigences de couverture de tests des grammaires et un suivi de l'usage des productions ; leurs verdicts rendraient aussi A_S mesurable.
3. **Mesurer l'écart régulateur** — Les inventaires ne le bornent que de loin : des perturbations entre 6.64 et 32.63 bits si les estimations tiennent, et aucune borne sur les réponses. Les paires de politiques (666 à partir de 37 politiques) sont la plus grande source possible de perturbation. À mesure que les politiques augmentent, le nombre de paires croît de façon quadratique, mais sa variété log2(n(n-1)/2) ne croît que de façon logarithmique, d'environ 2 bits chaque fois que le nombre de politiques double, et elle relève d'autant la borne supérieure de V_D. Envisager un regroupement des politiques ou une organisation hiérarchique des politiques.
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
