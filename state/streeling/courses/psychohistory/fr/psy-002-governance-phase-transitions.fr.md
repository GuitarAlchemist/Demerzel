---
module_id: psy-002-governance-phase-transitions
department: psychohistory
course: "Tester l'analogie des transitions de phase en gouvernance"
level: intermediate
prerequisites: [psy-001-intro-fractal-compounding]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
research_cycle: psychohistory-2026-03-23-001
version: "1.1.0"
---

# Tester les changements de régime en gouvernance

> **Département de psychohistoire** | Niveau : Intermédiaire | Durée : 35 minutes | Statut : brouillon révisé, revue de fond et essai apprenant en attente

## Objectifs

Après cette leçon, vous serez capable de :
- Distinguer une transition de phase physique d'une analogie proposée pour la gouvernance
- Repérer cinq indicateurs proposés et une hypothèse non mesurée sur la variété pour étudier les changements de régime
- Nommer les preuves requises avant de qualifier un changement de gouvernance de brutal, continu ou prévisible
- Expliquer quelles preuves seraient nécessaires avant de tester la variété requise comme signal de transition de gouvernance
- Concevoir un tableau de bord de surveillance à partir des fichiers d'état de la gouvernance

---

## 1. L'analogie et ses limites

En physique, l'eau devient glace à 0 degré C. Les molécules sont les mêmes, mais leur comportement collectif change qualitativement. C'est une **transition de phase** — le système passe d'un régime à un autre.

Pour Demerzel, la « transition de phase » est une analogie à tester, pas une loi observée. Un inventaire plus grand peut modifier le travail, mais le nombre de fichiers ne démontre ni un changement qualitatif ni le moment où il surviendrait. Un essai définirait le comportement étudié, figerait les observations avant et après un changement et comparerait d'autres explications.

### Transitions du premier ordre et du second ordre

| Type | Analogie physique | Exemple en gouvernance |
|------|----------------|-------------------|
| Premier ordre | Eau → glace (brutale, chaleur latente) | Activation de l'arrêt d'urgence comme **analogie** d'un changement brutal |
| Second ordre | Ferromagnétique à la température de Curie (continue) | Changement graduel du travail comme **analogie** ; aucun point critique mesuré |

On n'a pas établi ici qu'un changement de gouvernance possède la structure d'une transition de phase physique. Les indicateurs ci-dessous servent à enquêter ; leur pouvoir prédictif n'a pas été validé sur des transitions passées.

---

## 2. Cinq indicateurs proposés et une mesure à construire

### Signal 1 : asymétrie de la distribution des croyances

La logique de Demerzel est hexavalente : T (Vrai), P (Probable), U (Inconnu), D (Douteux), F (Faux), C (Contradictoire). Le ratio `T/U` est l'**indice de cristallisation** — la part de vos connaissances qui s'est solidifiée. C'est une projection sur quatre états : les fichiers de poids des départements ne comptent que `total_T`, `total_F`, `total_U` et `total_C`, sans compte pour P ni pour D, de sorte que l'indice ne voit ni une croyance probable ou douteuse, ni un passage entre T et P ou entre D et F. Le calculer sur les six valeurs demanderait des comptes de P et de D que ces fichiers ne contiennent pas.

```
crystallization_index = total_T / max(total_U, 1)
```

Si ce ratio s'écarte de plus de deux écarts-types historiques, examinez les comptes et leur méthode de collecte. Ce seuil illustre un déclencheur d'enquête, pas un prédicteur validé ; sur quelques cycles, l'écart-type lui-même peut être instable.

- **Hausse rapide :** Davantage de T que de U sont consignés ; vérifiez les reclassements et la couverture.
- **Baisse rapide :** Davantage de U que de T sont consignés ; vérifiez l'entrée de nouveaux sujets.

**Où mesurer :** `state/streeling/departments/*.weights.json` → `metadata.total_T`, `metadata.total_U`

### Signal 2 : vitesse du score de santé

Le score R de Demerzel est défini dans `CONTEXT.md` par `R = injections_caught / injections_total` : la part des défauts injectés que la détection intercepte. `state/resilience/history.json` consigne `overall_score` par cycle de chaos, et `governance-health.json` garde la dernière valeur. Une variation de R décrit ces tests ; ce n'est ni un potentiel thermodynamique ni une mesure de proximité d'une frontière de régime :

```
velocity = dR/dt (variation du score de santé par cycle)
```

| Profil | Signification |
|---------|---------|
| Vitesse positive, en accélération | Le score déclaré croît plus vite ; vérifier les cas de test modifiés |
| Vitesse positive, en décélération | Le score déclaré croît encore, mais moins vite |
| Vitesse proche de zéro | Le score déclaré varie peu ; cela ne prouve aucun équilibre |
| Vitesse négative | Le score déclaré baisse ; examiner les cas et la détection |

**Tranches de tableau de bord illustratives, pas des seuils empiriques de régime :** `<0,5`, `0,5–<0,7`, `0,7–<0,9` et `≥0,9` peuvent regrouper les valeurs affichées de R. Ces tranches ne démontrent aucun comportement réactif, structuré, proactif ou autonome. De telles interprétations exigent des issues mesurées séparément et des cas d'injection stables.

### Signal 3 : saturation de la densité de politiques

Une politique ajoutée peut aider, ne rien changer ou alourdir le travail. Un calcul descriptif de variation par fichier est :

```
marginal_return = delta_R / delta_policy_count
```

Trois valeurs proches de zéro ne prouvent pas une saturation. Les politiques peuvent changer avec les tests, leur application, les personnes ou d'autres politiques : `delta_R / delta_policy_count` n'isole donc pas l'effet causal d'une politique. Comparez des cas d'injection appariés et consignez les autres changements avant de décider qu'une nouvelle conception s'impose.

Pondérer par le nombre de personas contraints mesurerait encore la portée déclarée, pas l'efficacité. Ce peut être un champ descriptif, pas une mesure validée du rendement.

### Signal 4 : force du couplage entre dépôts

Demerzel gouverne quatre dépôts (demerzel, ix, tars, ga). Relevez le taux de conformité de chaque dépôt à chaque cycle et, sur une fenêtre des W derniers cycles, faites la moyenne des valeurs absolues des corrélations de Pearson des six paires de dépôts (un seul cycle ne donne qu'un taux par dépôt, dont on ne peut tirer aucune corrélation). Prenez W d'au moins 30 cycles, le même dans toutes les fenêtres que vous comparez : avec W = 2, chaque corrélation vaut exactement ±1, et sur des fenêtres courtes le hasard seul donne de grandes valeurs, puisque pour deux dépôts indépendants l'espérance de |r| vaut environ 0.8/√(W − 1), soit 0.27 à W = 10 et 0.15 à W = 30, face au seuil de 0.3 ci-dessous. Prenez les valeurs absolues, car deux dépôts qui évoluent en sens opposés, avec une corrélation proche de −1, sont aussi fortement couplés que deux dépôts qui évoluent ensemble, et des corrélations de signes opposés s'annuleraient dans une moyenne signée. Une série constante, comme celle d'un dépôt qui reste à 100 %, n'a de corrélation avec rien : laissez ses paires de côté, et ne comparez deux fenêtres que sur les paires définies dans les deux. Une moyenne sur un autre ensemble de paires mesure autre chose, et écarter des paires faibles suffit à la faire monter jusqu'au régime fortement couplé. S'il ne reste aucune paire, le couplage n'est pas défini pour la fenêtre :

```
coupling = mean_{i<j} |pearson_correlation(rates_i[W], rates_j[W])|
```

| Couplage | Régime |
|----------|--------|
| < 0,3 | Faible corrélation absolue observée dans cette fenêtre |
| 0,3 - 0,7 | Tranche intermédiaire illustrative ; chercher des causes communes |
| > 0,7 | Forte corrélation absolue observée ; la propagation n'est pas prouvée |

Un saut signifie que ces séries sont devenues plus corrélées dans la fenêtre choisie ; il ne démontre pas un couplage causal. La moyenne ignore les signes : deux dépôts qui progressent et deux qui déclinent ensemble peuvent donner `|r| = 1` pour chaque paire. Examinez les corrélations signées et les changements communs avant de proposer une explication. Une variation de corrélation ne démontre pas à elle seule une transition de phase.

### Signal 5 : fréquence des signaux de conscience

En mécanique statistique, les fluctuations croissent sans limite à l'approche d'un point critique, où la transition est continue (du second ordre). Près du point critique liquide–gaz, cela se manifeste par l'**opalescence critique** : les fluctuations de densité atteignent l'échelle de la longueur d'onde de la lumière, et le fluide devient laiteux. L'ébullition ordinaire, transition du premier ordre, n'a pas de tel signe avant-coureur.

L'idée que le taux d'anomalies ou d'escalades changerait avant certaines modifications de gouvernance est une hypothèse. Cette leçon ne dispose d'aucune série temporelle qui la teste. Un coupe-circuit est un événement administratif ; le qualifier de « premier ordre » est une métaphore, pas une classification physique mesurée.

```
signal_rate = conscience_signals_count / time_window
```

Un doublement sur 3 cycles invite à examiner les événements et leur dénominateur. Aucun seuil ni aucune direction de transition n'ont été validés pour cet indicateur.

**Où mesurer :** le répertoire `state/conscience/signals/`

### Signal 6 : la variété requise, une piste non validée

La version révisée de [CYB-003](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) retire son ancien ratio fondé sur les nombres de politiques et de personas. Compter les catégories de réponses et de perturbations rencontrées pendant un cycle serait reproductible, mais leur quotient ne dirait pas quelle réponse convient à quelle perturbation. Aucune série appariant perturbation → réponse → issue n'a été mesurée ici. Il n'y a donc **ni signal opérationnel de variété ni frontière de régime à 1,0** à tracer pour l'instant.

Un essai utile définirait à l'avance les classes de perturbations, les réponses permises et les issues acceptables, puis conserverait chaque événement apparié sur plusieurs cycles. Il faudrait comparer les réussites vérifiées indépendamment et les cas non résolus avant d'interpréter une mesure d'information. L'idée d'un paramètre d'ordre pour les transitions de gouvernance reste une hypothèse, et non un résultat de CYB-003.

---

## 3. Comparer les preuves avant de nommer un régime

| Quantité consignée | Comparaison utile | Preuve manquante |
|---|---|---|
| R par cycle de chaos | Comparer des cas appariés d'injection de défauts | Jeu de cas stable et issues vérifiées indépendamment |
| Comptes T et U | Examiner la répartition des croyances consignées | Couverture stable et comptes P/D |
| Taux de conformité des dépôts | Comparer des fenêtres alignées et des corrélations signées | Dénominateur commun et enquête causale |
| Variété requise | Expérience proposée perturbation → réponse → issue | Série d'événements appariés ; aucun ratio actuel |

Aucun nombre d'indicateurs alignés ne démontre actuellement une transition de phase. Une affirmation utile nomme le changement de travail observé, la révision, la période et l'autre explication examinée.

---

## 4. Exercice pratique

À partir de l'état actuel de la gouvernance de Demerzel :

1. Calculez l'indice de cristallisation à partir du fichier de poids de la psychohistoire :
   - `total_T = ?`, `total_U = ?`
   - `crystallization_index = total_T / max(total_U, 1)`

2. Prenez pour R l'`overall_score` du dernier enregistrement de `state/resilience/history.json`. Dans quelle tranche illustrative tombe-t-il ? Quelle valeur franchirait la tranche suivante, et quelles autres preuves permettraient de conclure à un changement réel du travail ?

3. Dans le même fichier, le cycle chaos-003 consigne, dans `metafixes_applied`, un nouveau fichier de politique et une section ajoutée à une politique existante, et dans `level_deltas` un gain au niveau L4, pendant que R passait de 0.64 (chaos-002) à 0.73. Calculez le rendement global des changements de ce cycle. Pourquoi la hausse de 0.09 ne peut-elle pas être attribuée à la seule nouvelle politique, et quelle observation isolerait son rendement ? Entre chaos-003 et chaos-004, R est monté à 0.82 sans nouveau fichier de politique : qu'est-ce que cela dit de la mesure des rendements par nombre de politiques ?

4. **Expérience de pensée :** Si les trois dépôts consommateurs (ix, tars, ga) annonçaient soudain 100 % de conformité, cela démontrerait-il une transition de phase ou même une amélioration réelle ? Quelles preuves demanderiez-vous ?

> **Réponse à 4 :** Non. Vérifiez le dénominateur et les versions des politiques, les changements de tests, les exceptions qui auraient disparu des relevés et les issues indépendantes. Le saut déclaré ne classe aucune transition physique ou de gouvernance.

---

## Points clés à retenir

- Un changement qualitatif du travail ne démontre à lui seul ni transition de phase physique ni loi prédictive
- Cinq signaux proposés peuvent être examinés dans les relevés existants ; la variété requise reste une sixième piste non mesurée
- Une mesure de variété exige des perturbations, des réponses et des issues appariées avant d'être testée comme signal de transition
- Aucun ordre de transition physique ni seuil de prévision n'a été établi ici pour les changements de gouvernance
- Examiner plusieurs indicateurs et issues mesurés indépendamment ; la règle des « 3 signaux ou plus » n'est pas validée

## Pour aller plus loin

- [PSY-001 : Introduction à la capitalisation fractale](psy-001-intro-fractal-compounding.fr.md) — prérequis sur D_c et ERGOL/LOLLI
- [CYB-003 : Mesurer la variété requise sans inventer de capacité](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) (en anglais) — limites de mesure et expérience proposée
- [CYB-001 : Correspondance entre le VSM et la gouvernance de l'IA](../../cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md) — prérequis structurels
- Mécanique statistique des transitions de phase (théorie de Landau, paramètres d'ordre, exposants critiques)
- Fondation d'Asimov — la psychohistoire prédit des tendances agrégées, pas des événements individuels

---
*Produit par Seldon Auto-Research psychohistory-2026-03-23-001 le 2026-03-23.*
*Question de recherche : Quels signaux mesurables dans l'état d'une gouvernance de l'IA fondée sur des fichiers indiquent qu'un système de gouvernance approche d'une transition de phase ?*
*Croyance : T (confiance : 0.80) — accord entre Claude et GPT-4o, NotebookLM indisponible ; traduction française : U (non relue par un locuteur natif)*
