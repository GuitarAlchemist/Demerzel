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

La loi de la variété requise d'Ashby énonce qu'un régulateur doit avoir au moins autant de variété que les perturbations auxquelles il fait face, moins la variété des issues qu'il peut accepter. Ce cours définit un cadre quantitatif pour mesurer la variété de Demerzel, en bits, selon trois dimensions : comportementale (personas), structurelle (grammaires) et régulatrice (les décisions et les étiquettes qu'elles portent). La formule clé est V = log2(N), où N compte les issues distinguables. Trois règles de comptage gardent les nombres honnêtes. Un produit de nombres de composants n'est un espace d'états conjoint que si les composants varient indépendamment ; sinon, ce n'est qu'une borne supérieure. Un nombre de règles n'est pas un nombre d'états : l'atténuation qu'apportent les contraintes, les politiques et les portes est la variété qu'elles retirent, V_in - V_out. Et un inventaire n'est pas un ensemble d'issues : les définitions de règles, les étiquettes de décision et les paires de politiques sont ce que le dépôt définit, pas les structures, les réponses et les perturbations qui se produisent. L'inventaire est compté à un commit ; les variétés que compare la loi d'Ashby doivent être mesurées. Le ratio de variété compare la variété des réponses à celle des perturbations, et son logarithme, log2 R = V_response - V_disturbance en bits, sera suivi dans le temps une fois les deux côtés mesurés. La loi d'Ashby s'énonce toutefois sur les issues : c'est l'issue de chaque perturbation, compte tenu de la réponse, qui dit si la gouvernance régule, pas ce ratio seul.

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
V(régulateur) >= V(perturbation) - V(issues acceptables)
```

« Seule la variété peut absorber la variété. » Ashby énonce la loi sur les issues. Chaque perturbation rencontrée, avec la réponse qui lui est donnée, produit une issue sur les variables essentielles, les grandeurs que la gouvernance doit maintenir dans des limites acceptables. Si aucune réponse ne mène deux perturbations différentes à la même issue, les issues gardent au moins V_D - V_R bits de variété : V(issues) >= V(perturbation) - V(régulateur). Réguler, c'est maintenir chaque issue dans les limites. Si N_η issues sont acceptables, portant V_η = log2(N_η) bits, réguler chaque perturbation exige V_R >= V_D - V_η, et un système de gouvernance dont les réponses n'y suffisent pas échouera à réguler certaines perturbations ; avec une seule issue acceptable, la condition est V_R >= V_D. Là où une même réponse mène plusieurs perturbations à la même issue acceptable, le système les absorbe sans une réponse pour chacune, et la borne ne s'applique pas à elles. Les deux décomptes seuls ne montrent donc pas si la gouvernance régule ; les issues le montrent.

## Trois dimensions de la variété dans Demerzel

Dans un cadre de gouvernance, la variété n'est pas un nombre unique. Ce cours mesure celle de Demerzel selon trois dimensions. Les nombres de l'inventaire (personas, contraintes, grammaires, règles, politiques, articles) sont lus dans le dépôt au commit `74cf7c5`, qui a ajouté ce module. Les valeurs logiques et les échelons de confiance suivent les définitions canoniques actuelles, dans `CONTEXT.md` et `logic/confidence-thresholds.yaml`, lues au commit `91e41ac`.

### Trois règles de comptage

**États conjoints.** Si un composant a a états et un autre en a b, la paire a au plus a × b états conjoints, et exactement a × b seulement si toutes les combinaisons peuvent se produire. Si le second est fixé par le premier, la paire n'a que a états. Ainsi, log2(a) + log2(b) est une borne supérieure de la variété de la paire, et le plus grand de log2(a) et log2(b) en est une borne inférieure.

**Les règles ne sont pas des états.** Une règle, comme une politique, une contrainte de persona ou une porte d'évolution, est un prédicat qui autorise certains états et en interdit d'autres. Plusieurs règles peuvent s'appliquer à la fois et se recouvrir, et scinder une règle en deux change leur nombre sans changer aucun comportement. Le log2 d'un nombre de règles n'est donc pas une variété. Un atténuateur se mesure par la variété qu'il retire : A = V_in - V_out, où V_in est la variété de ce qui lui parvient et V_out celle de ce qu'il laisse passer.

**Un inventaire n'est pas un ensemble d'issues.** Un nombre d'éléments définis par le dépôt ne borne les issues que si chaque élément peut se produire seul, comme une issue, et seulement par le haut : les issues n'ont cette variété que si chaque élément se produit réellement. Une dérivation de grammaire utilise plusieurs définitions de règles à la fois, une même étiquette de décision peut couvrir plusieurs actions différentes, et une paire de politiques n'est une interaction que si les deux interagissent réellement, tandis qu'une même paire en interaction peut entrer en conflit de plusieurs façons distinguables. La variété se compte sur les issues : les structures distinctes générées, les réponses données et les perturbations rencontrées.

### Dimension 1 : variété comportementale (V_B)

**Ce qu'elle mesure :** L'éventail des comportements d'agent distincts que le système peut produire.

**Amplificateurs :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Niveaux d'orientation vers un but (énumération du schéma ; 3 utilisés) | 4 | 2.00 bits |
| Voix (ton, verbosité, style), une par persona | 14 | 3.81 bits |

Chaque fichier de persona fixe exactement un niveau d'orientation vers un but et une voix : `schemas/persona.schema.json` exige les deux, et chacun contient une seule valeur. Choisir une persona revient donc à choisir les deux, et les 14 voix sont celles des 14 personas. Les profils comportementaux que Demerzel peut instancier sont les personas elles-mêmes.

**Choix de la persona :** V_B_persona vaut au plus log2(14) = **3.81 bits**, la variété du choix de la persona qui agit, atteinte seulement si chacune des 14 est réellement choisie. Les personas qui agissent ne sont pas consignées : le catalogue borne cette variété sans la mesurer. Les actions qu'une persona peut ensuite entreprendre ne sont pas comptées ici ; c'est ce que consigne la mesure de l'atténuation (métrique 3).

Multiplier les trois lignes, 14 × 4 × 14 = 784 profils (9.61 bits), compterait des combinaisons qui n'existent que si n'importe quel niveau et n'importe quelle voix pouvaient être recombinés avec n'importe quelle persona à l'exécution, ce que les fichiers de persona ne permettent pas. Ce produit est une borne supérieure, pas la variété.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Contraintes de persona | 60 | Des règles, environ 4.3 par persona ; pas des états |
| Appariement d'estimateur | 1 | skeptical-auditor évalue les 13 autres personas |

**Atténuation comportementale :** non mesurée. Les 60 contraintes sont des prédicats qui s'appliquent ensemble et peuvent se recouvrir ; log2(60) = 5.91 bits les traiterait comme 60 issues distinguables. Leur atténuation est la réduction de variété entre les actions que chaque persona propose et celles que ses contraintes autorisent, A_B = V_in - V_out, et la mesurer demande un relevé des unes et des autres, les refus étant consignés à part.

Interprétation : Demerzel a 14 profils comportementaux, au plus 3.81 bits de choix de persona, chacun borné par ses propres contraintes. Les personas qui agissent et ce que retirent les contraintes sont les mesures encore ouvertes de cette dimension.

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

**Atténuation structurelle :** non mesurée. C'est la réduction de variété entre les changements de grammaire proposés et ceux que les portes acceptent, A_S = V_in - V_out, et la mesurer demande le journal des propositions et des verdicts.

Interprétation : trois règles contrôlent 27 grammaires qui contiennent 1,129 définitions de règles. Un nombre de portes ne dit pas si elles contrôlent bien : une seule porte peut vérifier chaque changement proposé, et scinder un prédicat en deux portes augmente le nombre sans rien retirer. C'est à leurs verdicts de montrer si les portes suffisent (voir Évaluation actuelle).

### Dimension 3 : variété régulatrice (V_R)

**Ce qu'elle mesure :** L'éventail des décisions de gouvernance distinctes que le système peut prendre.

Au commit `74cf7c5`, la logique de Demerzel avait quatre valeurs, T/F/U/C. Sa logique canonique est désormais hexavalente, T/P/U/D/F/C (`CONTEXT.md`), dont T/F/U/C est le sous-ensemble à quatre valeurs, et ce cours compte les six valeurs.

**Étiquettes de décision :**
| Composant | Nombre (N) | Variété V = log2(N) |
|-----------|-----------|---------------------|
| Valeurs de la logique hexavalente | 6 | 2.58 bits |
| Échelons de confiance | 5 | 2.32 bits |
| États PDCA | 4 | 2.00 bits |

**Vocabulaires d'étiquettes :** ce sont trois vocabulaires distincts, de 2.58, 2.32 et 2.00 bits. Chaque nombre est un maximum : une étiquette n'a cette variété que si les décisions utilisent réellement chacune de ses valeurs, et aucun relevé ne montre qu'elles le font, si bien que même la plus grande, 2.58 bits, n'est pas une borne inférieure. Aucun fichier n'attache non plus les trois étiquettes à une même décision : leurs combinaisons, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, sont ce que permettent les vocabulaires, pas un ensemble d'étiquettes en usage. La variété des étiquettes n'est **pas mesurée** : la mesurer demande un relevé des étiquettes que porte chaque décision.

Ces étiquettes classent une décision ; elles ne comptent pas les réponses. Une valeur de vérité énonce une croyance, un échelon de confiance oriente l'exécution et un état PDCA est une étape du flux de travail, si bien que plusieurs actions différentes, dont une escalade, peuvent porter les mêmes étiquettes. Les étiquettes ne bornent donc en rien la variété des réponses V_R_amp, qui n'est **pas mesurée** : la mesurer demande un relevé des actions distinctes que prend la gouvernance, escalades comprises.

**Atténuateurs :**
| Composant | Nombre | Ce que le nombre compte |
|-----------|-------|-------------------|
| Politiques | 37 | Des règles ; pas des états |
| Articles constitutionnels (Asimov 6, Default 11) | 17 | Des règles ; pas des états |
| Niveaux de gravité des préjudices (Critical, High, Medium, Low) | 4 | Des classes qui orientent une réponse ; pas des états retirés |

**Atténuation régulatrice :** non mesurée. C'est la réduction de variété entre les décisions candidates et celles que les politiques et les articles autorisent, A_R = V_in - V_out.

Interprétation : la gouvernance doit contraindre plus qu'elle n'amplifie, conformément aux lois d'Asimov (préférer la sécurité à la capacité), mais ni la variété de ses réponses ni l'ampleur de cette contrainte ne sont mesurées.

## Le tableau de bord composite de la variété

### Tableau récapitulatif

| Dimension | Inventaire à `74cf7c5` | Variété | Atténuation | Évaluation |
|-----------|------------------------|---------------------|-------------|------------|
| Comportementale (V_B) | 14 personas, 60 contraintes, 1 estimateur | Choix de la persona : au plus 3.81 bits, non mesuré | Non mesurée | Profils fixés par persona |
| Structurelle (V_S) | 27 grammaires, 1,129 définitions de règles, 2 portes, 1 alerte d'obsolescence | Non mesurée | Non mesurée | Efficacité des portes non mesurée |
| Régulatrice (V_R) | 4 valeurs (6 à `91e41ac`), 5 échelons à `91e41ac`, 4 états PDCA ; 37 politiques, 17 articles, 4 niveaux de gravité | Étiquettes : au plus 6.91 bits à elles trois ; étiquettes et réponses non mesurées | Non mesurée | Prudente par conception, ampleur non mesurée |

### Pourquoi le tableau de bord n'a pas de ratio amplificateurs sur atténuateurs

Un raccourci tentant divise, pour chaque dimension, les états des amplificateurs par le nombre d'atténuateurs, par exemple les 784 profils du produit ci-dessus par les 60 contraintes. Ce quotient n'a pas de sens au sens d'Ashby. Son numérateur compte des profils que les fichiers de persona ne peuvent pas produire, et son dénominateur compte des règles, pas des états, si bien que scinder une contrainte en deux le changerait sans changer aucun comportement. Un rapport d'espaces d'états demande des états des deux côtés : la variété V_in qui parvient à un atténuateur et la variété V_out qu'il laisse passer. La colonne Atténuation deviendra un nombre une fois ces variétés mesurées, et la vérification de la loi d'Ashby ci-dessous compare la variété des réponses à celle des perturbations.

### Sens sains

La loi d'Ashby et les principes du VSM (CYB-001) fixent le sens que doit prendre chaque grandeur, pas encore sa taille :

| Dimension | Sens sain | Justification |
|-----------|---------------|-----------|
| Comportementale | A_B > 0 sur les actions nuisibles, chaque persona gardant les actions permises par son rôle | Les contraintes doivent retirer le préjudice, pas des rôles entiers |
| Structurelle | Les portes rejettent les changements proposés qui y échouent, échecs injectés compris | Une porte se teste par les changements qu'elle doit rejeter ; un lot de changements valides donne à bon droit A_S = 0 |
| Régulatrice | Chaque perturbation rencontrée se termine avec les variables essentielles dans leurs limites, escalades vers les humains comprises | La loi d'Ashby, énoncée sur les issues |

Ces sens deviendront des seuils une fois A_B, A_S, A_R, les variétés conjointes et les issues mesurés sur plusieurs cycles.

### Évaluation actuelle

- **Comportementale (14 personas, au plus 3.81 bits de choix de persona) :** chaque persona fixe son niveau et sa voix. Les personas qui agissent et ce que retirent leurs contraintes ne sont pas mesurés ; consigner les personas choisies, les actions que chacune propose et celles que ses contraintes autorisent mesurerait les deux.
- **Structurelle (27 grammaires, 1,129 définitions de règles) :** aucune variété structurelle n'est mesurée, et rien ne montre encore si les trois règles qui les contrôlent suffisent. Recommandation : mesurer avant d'ajouter des portes. Consigner les changements proposés et les verdicts des portes, ce qui mesure A_S ; injecter des changements que les portes doivent rejeter ; suivre la couverture de tests des grammaires et l'usage des productions ; et consigner les dérivations produites, ce qui mesure V_S. Ajouter une porte là où un échec injecté passe ou là où la couverture manque.
- **Régulatrice (vocabulaires d'étiquettes, au plus 6.91 bits à eux trois) :** prudente par conception ; dire si elle l'est trop, ou si elle régule assez, demande A_R et les issues des perturbations qu'elle rencontre.

## Le côté des perturbations : que faut-il réguler ?

Le côté des amplificateurs ne raconte que la moitié de l'histoire. Il faut aussi estimer la variété des perturbations auxquelles le système fait face. Les valeurs des tableaux ci-dessous sont des estimations, pas des mesures, et une source n'est pas estimée du tout :

### Perturbations externes (V_D_ext)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Dépôts consommateurs (ix, tars, ga) | 3 | 1.58 bits |
| Combinaisons d'états des dépôts (3 dépôts x ~10 états chacun) | 10 à 10^3 = 1000 | 3.32 à 9.97 bits |
| Changements de l'environnement externe (bibliothèques, API, modèles) | ~100 | 6.64 bits |

**Variété totale des perturbations externes :** les combinaisons d'états des dépôts couvrent déjà les trois dépôts, donc la première ligne n'ajoute rien. Cette ligne est elle-même une fourchette : avec environ 10 états chacun, les trois dépôts ont entre 10 états conjoints (3.32 bits), si l'état de l'un détermine celui des autres, et 10^3 = 1000 (9.97 bits), s'ils varient indépendamment. Si les estimations tiennent, la ligne de l'environnement est alors le plus grand terme isolé : V_D_ext vaut au moins **6.64 bits**, et au plus log2(1000 × 100) = 9.97 + 6.64 = **16.61 bits** si les changements de l'environnement surviennent un à la fois, chacun dans n'importe lequel des 1000 états des dépôts.

### Perturbations internes (V_D_int)
| Source | Estimation (N) | Variété V |
|--------|-------------|-----------|
| Changements d'état de croyance par cycle | ~20 | 4.32 bits |
| Interactions entre politiques (37 politiques, 666 paires) | non estimé | non estimée |
| Propositions d'évolution des grammaires | ~5 par cycle | 2.32 bits |

666 est le nombre de paires de politiques. Il compte les paires qui pourraient interagir, pas les issues de leurs interactions : seules contribuent les paires qui interagissent réellement, une même paire peut entrer en conflit de plusieurs façons distinguables, et rien ici ne mesure ni l'un ni l'autre. La ligne des politiques ne donne donc ni borne inférieure ni borne supérieure.

**Variété totale des perturbations internes :** si les estimations tiennent, V_D_int vaut au moins **4.32 bits** (les seuls changements de croyance, si environ 20 changements distincts surviennent dans un cycle). L'inventaire ne lui donne aucune borne supérieure : la ligne des politiques n'est pas estimée, et les deux autres lignes comptent des événements par cycle, pas les formes distinctes que chaque événement peut prendre.

### Vérification de la loi d'Ashby

Pour que la gouvernance régule chaque perturbation rencontrée, là où aucune réponse ne mène deux perturbations à la même issue et où N_η issues sont acceptables :

```
V(réponse régulatrice) >= V(perturbation) - V(issues acceptables)
```

- V_R_amp, la variété des réponses, n'est pas mesurée. Les définitions ne donnent que les vocabulaires d'étiquettes, au plus 6.91 bits à eux trois, et les étiquettes ne la bornent pas (voir la dimension 3)
- Si les estimations tiennent, V_D vaut au moins 6.64 bits, les changements de l'environnement, la plus grande source estimée isolée. L'inventaire ne donne aucune borne supérieure, puisque les interactions entre politiques ne sont pas estimées (voir Perturbations internes)
- **Écart : non calculé.** Aucun des deux côtés n'est mesuré, et les inventaires sont compatibles avec un surplus comme avec un déficit de n'importe quelle taille

La borne inférieure tient quelles que soient les dépendances, étant donné les estimations : un espace d'états conjoint a au moins autant d'états que sa plus grande partie. Elle montre aussi combien peu les inventaires tranchent. Environ 100 changements de l'environnement distincts (6.64 bits), c'est moins que les 120 combinaisons d'étiquettes que permettent les vocabulaires (6.91 bits) : même les étiquettes pourraient en principe les distinguer, si les décisions utilisaient chaque combinaison, alors que rien dans les inventaires ne plafonne les perturbations. Compter les perturbations distinctes rencontrées et les réponses distinctes données à chaque cycle donnerait V_D - V_R_amp, mais cette différence n'est que la borne inférieure d'Ashby sur la variété des issues, valable là où aucune réponse ne mène deux perturbations à la même issue. Deux cycles aux mêmes décomptes peuvent réguler entièrement ou pas du tout, selon la réponse qui rencontre chaque perturbation, et une seule réponse robuste peut réguler plusieurs perturbations. La régulation se mesure en consignant, pour chaque perturbation, la réponse donnée et l'issue sur les variables essentielles (métrique 3).

Si les perturbations dépassent les réponses, la différence doit être absorbée par :

1. **L'escalade vers des humains** — le système de seuils de confiance oriente les décisions difficiles vers des humains, en empruntant leur variété
2. **La primauté constitutionnelle** — les lois d'Asimov ramènent les décisions complexes à un choix binaire (sûr/dangereux), ce qui réduit la variété requise
3. **Le cycle PDCA** — le traitement séquentiel convertit des perturbations parallèles en files d'attente gérables

Ce sont des mécanismes légitimes d'absorption de la variété. S'ils suffisent, c'est ce que montreraient les issues, et Demerzel devrait surveiller si la complexité des interactions entre politiques croît plus vite que la capacité de régulation.

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
      "logic_values": 4,
      "pdca_states": 4,
      "policies": 37,
      "constitutional_articles": 17,
      "harm_severity_levels": 4,
      "persona_constraints": 60,
      "evolution_gates": 2
    },
    "definitions": {
      "commit": "91e41ac",
      "logic_values": 6,
      "confidence_rungs": 5
    }
  }
}
```

`commit` date les nombres de l'inventaire, tous lus à `74cf7c5`, où la logique avait quatre valeurs. `definitions` contient ce qu'utilisent les bornes des étiquettes : les six valeurs logiques de `CONTEXT.md` et les cinq échelons de `logic/confidence-thresholds.yaml`, lus à `91e41ac`. Le fichier de l'échelle n'existait pas à `74cf7c5`, si bien que l'inventaire ne compte pas d'échelons.

### Métrique 2 : variétés par dimension

```json
{
  "variety_bits": {
    "catalogue_bounds": {
      "persona_selection": 3.81,
      "label_vocabularies": [2.58, 2.32, 2.00],
      "label_combinations": 6.91
    },
    "persona_selection": null,
    "decision_labels": null,
    "structures_generated": null,
    "responses": null,
    "disturbances": null,
    "outcomes": null,
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "inventory_commit": "74cf7c5",
    "definitions_commit": "91e41ac"
  }
}
```

Un `null` marque une grandeur pas encore mesurée, pas un zéro. `catalogue_bounds` contient des bornes supérieures, pas des mesures : celle des personas vient de l'inventaire et celles des étiquettes des définitions, d'où les deux commits. Mesurer `persona_selection` et `decision_labels` demande un relevé des personas choisies et des étiquettes que porte chaque décision.

### Métrique 3 : mesure des issues et de l'atténuation

Pour chaque atténuateur, consignez à chaque cycle ce qui lui parvient et ce qu'il laisse passer : les actions que chaque persona propose et celles que ses contraintes autorisent, les changements de grammaire proposés et ceux que les portes acceptent, les décisions candidates et celles que les politiques et les articles autorisent. Consignez à part les actions refusées, les changements rejetés et les décisions exclues : ils montrent ce qui a été retiré, pas ce qui est passé. Avec N_in issues distinctes qui parviennent à un atténuateur et N_out issues distinctes qui le franchissent, V_in = log2(N_in), V_out = log2(N_out), et A = V_in - V_out = log2(N_in / N_out) bits : un atténuateur qui laisse passer 4 propositions distinctes sur 8 retire 1 bit. Si rien ne parvient à l'atténuateur (N_in = 0), le cycle n'est pas une observation : consignez-le comme inactif, pas comme un blocage. Si des entrées lui parviennent et qu'aucune ne passe (N_in > 0, N_out = 0), V_out n'est pas défini ; consignez ce cycle comme un blocage total, pas comme un nombre. Consignez de la même façon, en log2 de chaque nombre, les personas distinctes choisies pour agir et les combinaisons d'étiquettes distinctes que portent les décisions, les N_S structures distinctes que génèrent les grammaires (V_S), les N_R réponses distinctes que donne la gouvernance, escalades comprises (V_R_amp), et les N_D perturbations distinctes qu'elle rencontre (V_D). Un nombre nul n'a pas de log2 et reçoit une étiquette, pas un nombre : un cycle qui ne rencontre aucune perturbation (N_D = 0) est calme ; un cycle qui rencontre des perturbations sans donner de réponse (N_D > 0, N_R = 0) est sans réponse ; un cycle où les grammaires ne génèrent aucune structure (N_S = 0) est inactif pour V_S. Pour chaque perturbation, consignez aussi la réponse donnée (aucune, s'il n'y en a pas) et l'issue sur les variables essentielles, dans les limites ou non : par exemple, aucun article constitutionnel violé et aucune validation de schéma en échec. Le taux de régulation est la part des perturbations rencontrées dont l'issue reste dans les limites, et les issues distinctes donnent V_O. La différence V_D - V_R_amp, calculée seulement pour les cycles où N_D > 0 et N_R > 0, est la borne inférieure d'Ashby sur V_O, pas une mesure de la régulation : elle dit jusqu'où les issues doivent s'étaler si aucune réponse ne sert deux perturbations, chaque perturbation ne peut être régulée que si elle ne dépasse pas V_η, et les issues consignées disent jusqu'où elles se sont étalées.

Suivez ces grandeurs sur des cycles consécutifs. Alertez quand :
- Une sonde de contrôle passe : une entrée que l'atténuateur doit refuser, injectée exprès, le franchit. A = 0 seul n'est pas une alerte, puisqu'un cycle dont toutes les entrées sont valides donne à bon droit A = 0
- Une issue sort des limites : une perturbation rencontrée se termine avec une variable essentielle hors de son ensemble acceptable, qu'une réponse ait été donnée ou non
- La borne d'Ashby V_D - V_R_amp augmente d'au moins 1 bit depuis le dernier cycle où elle a été calculée (la variété des perturbations double par rapport à celle des réponses) : un avertissement à confronter aux issues, pas un échec en soi
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

1. **Suivre les variétés à chaque cycle** — Ajouter l'instantané de l'inventaire à `state/governance/variety-metrics.json` (ou à un fichier d'état équivalent). Consigner l'inventaire et, une fois mesurées, les variétés du choix de persona, des étiquettes de décision, des structures, des réponses et des perturbations, chaque atténuation, et pour chaque perturbation la réponse donnée et son issue.
2. **Mesurer les portes structurelles avant d'en ajouter** — Consigner les changements de grammaire proposés et les verdicts des portes, injecter des changements que les portes doivent rejeter, et suivre la couverture de tests des grammaires et l'usage des productions ; ajouter une porte là où un échec injecté passe ou là où la couverture manque. Les verdicts rendent aussi A_S mesurable.
3. **Mesurer la régulation** — Consigner chaque perturbation rencontrée, la réponse donnée et son issue sur les variables essentielles. Les inventaires ne bornent les deux variétés que de loin : des perturbations d'au moins 6.64 bits si les estimations tiennent, sans borne supérieure, et aucune borne sur les réponses. Les interactions entre politiques sont la source de perturbation la moins connue. Le nombre de paires de politiques (666 à partir de 37 politiques) croît de façon quadratique, environ quatre fois chaque fois que le nombre de politiques double (2,701 paires pour 74 politiques), et chaque paire en interaction peut entrer en conflit de plusieurs façons. Un regroupement des politiques ou une organisation hiérarchique des politiques peut réduire les interactions, mais c'est à la mesure de montrer s'il réduit les perturbations qu'elles produisent.
4. **L'escalade vers des humains est un pont de variété** — Le système de seuils de confiance (Article 6 : Escalade) est le principal mécanisme de Demerzel pour absorber la variété qui dépasse sa capacité de régulation. C'est une fonctionnalité, pas une limite.
5. **Faire évoluer la section 6 de la grammaire** — La section sur la variété requise de la grammaire `sci-cybernetics.ebnf` (lignes 76-82) devrait être enrichie de productions de mesure quantitative.

## Lien avec CYB-001 et CYB-002

- **CYB-001** a établi que la loi d'Ashby s'applique à Demerzel et a listé qualitativement les amplificateurs et atténuateurs de variété. CYB-003 rend cela quantitatif.
- **La recommandation 5 de CYB-001** demandait de suivre le ratio de variété. CYB-003 dit sur quoi il doit être compté (des issues, pas des nombres de politiques et de personas) et donne des formules, des sens sains et un protocole de mesure.
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

1. Comment consigner à chaque cycle chaque perturbation rencontrée, la réponse donnée et son issue sur les variables essentielles, pour que la régulation puisse être mesurée ? Une fois qu'elle l'est, un regroupement hiérarchique des politiques réduit-il les perturbations que produisent les interactions entre politiques, ou seulement le nombre de paires de politiques ?
2. Comment suivre l'usage des productions de grammaire pour détecter les productions mortes et éclairer l'atténuation structurelle ?
3. Quelle est la relation, du point de vue de la théorie de l'information, entre la logique hexavalente de Demerzel (T/P/U/D/F/C) et l'entropie de Shannon — U (Unknown) porte-t-il plus de bits que T (True) ?

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md` (en anglais)
- Prérequis : `state/streeling/courses/cybernetics/en/cyb-002-active-dampening-cross-repo-oscillation.md` (en anglais)
- Grammaire : `grammars/sci-cybernetics.ebnf` (section 6, variété requise)
- Département : `state/streeling/departments/cybernetics.department.json`
- Politique : `policies/seldon-plan-policy.yaml`
