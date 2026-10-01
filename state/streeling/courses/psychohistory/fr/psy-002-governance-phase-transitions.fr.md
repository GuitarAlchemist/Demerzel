---
module_id: psy-002-governance-phase-transitions
department: psychohistory
course: "Théorie des transitions de phase : quand les systèmes de gouvernance changent de régime"
level: intermediate
prerequisites: [psy-001-intro-fractal-compounding]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
research_cycle: psychohistory-2026-03-23-001
cross_model_agreement: {claude: "T", gpt4o: "agree (0.7)", notebooklm: "unavailable"}
version: "1.0.0"
---

# Les transitions de phase de la gouvernance

> **Département de psychohistoire** | Niveau : Intermédiaire | Durée : 35 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Définir ce que signifie une transition de phase dans un système de gouvernance
- Identifier six signaux mesurables qui précèdent les changements de régime
- Distinguer les transitions de gouvernance du premier ordre (brutales) de celles du second ordre (continues)
- Utiliser le ratio de variété comme paramètre d'ordre candidat pour classer les régimes de gouvernance
- Concevoir un tableau de bord de surveillance à partir des fichiers d'état de la gouvernance

---

## 1. Qu'est-ce qu'une transition de phase de la gouvernance ?

En physique, l'eau devient glace à 0 degré C. Les molécules sont les mêmes, mais leur comportement collectif change qualitativement. C'est une **transition de phase** — le système passe d'un régime à un autre.

Les systèmes de gouvernance font la même chose. Un cadre à 3 politiques et 2 personas ne fonctionne pas comme un cadre à 28 politiques et 14 personas. À un moment donné, le système n'est pas seulement devenu plus grand — il a changé *sa façon de fonctionner*. Les interactions sont devenues qualitativement différentes.

**Idée clé de la psychohistoire :** Les effets de chaque changement de politique pris isolément sont imprévisibles. Mais le comportement *agrégé* du système de gouvernance suit des lois statistiques. Les transitions de phase sont les points où ces lois statistiques changent.

### Transitions du premier ordre et du second ordre

| Type | Analogie physique | Exemple en gouvernance |
|------|----------------|-------------------|
| Premier ordre | Eau → glace (brutale, chaleur latente) | Activation de l'arrêt d'urgence, amendement majeur de la constitution |
| Second ordre | Ferromagnétique à la température de Curie (continue) | Passage progressif d'une gouvernance réactive à une gouvernance proactive |

La plupart des transitions de gouvernance sont du second ordre — continues, difficiles à situer précisément, mais mesurables après coup. Les signaux ci-dessous vous aident à les détecter *avant* qu'elles ne s'achèvent.

---

## 2. Les six signaux mesurables

### Signal 1 : asymétrie de la distribution des croyances

La logique de Demerzel est hexavalente : T (Vrai), P (Probable), U (Inconnu), D (Douteux), F (Faux), C (Contradictoire). Le ratio `T/U` est l'**indice de cristallisation** — la part de vos connaissances qui s'est solidifiée. C'est une projection sur quatre états : les fichiers de poids des départements ne comptent que `total_T`, `total_F`, `total_U` et `total_C`, sans compte pour P ni pour D, de sorte que l'indice ne voit ni une croyance probable ou douteuse, ni un passage entre T et P ou entre D et F. Le calculer sur les six valeurs demanderait des comptes de P et de D que ces fichiers ne contiennent pas.

```
crystallization_index = total_T / max(total_U, 1)
```

Quand ce ratio change rapidement — `d(T/U)/dt` s'écartant de plus de 2 écarts-types de sa moyenne glissante — le système approche d'une transition.

- **Hausse rapide :** Le système se cristallise. La phase exploratoire se termine, la consolidation commence.
- **Baisse rapide :** Le système se déstabilise. De nouvelles inconnues apparaissent plus vite qu'elles ne sont résolues.

**Où mesurer :** `state/streeling/departments/*.weights.json` → `metadata.total_T`, `metadata.total_U`

### Signal 2 : vitesse du score de santé

Le score de santé de la gouvernance R est le score de résilience de Demerzel, défini dans `CONTEXT.md` par `R = injections_caught / injections_total` : la part des défauts injectés dans la gouvernance que sa détection intercepte. `state/resilience/history.json` l'enregistre sous `overall_score`, un enregistrement par cycle de chaos, et le fichier `governance-health.json` à la racine en garde la dernière valeur. R joue le rôle d'un potentiel thermodynamique, et sa dérivée renseigne sur la proximité d'un changement de régime :

```
velocity = dR/dt (variation du score de santé par cycle)
```

| Profil | Signification |
|---------|---------|
| Vitesse positive, en accélération | Approche d'un régime supérieur |
| Vitesse positive, en décélération | Approche d'un plateau (saturation) |
| Vitesse proche de zéro | À une frontière de régime ou à l'équilibre |
| Vitesse négative | Régression — une transition antérieure est peut-être en train de s'inverser |

**Seuils de régime (empiriques) :**
- R < 0.5 : **régime réactif** — la gouvernance répond aux problèmes
- 0.5 <= R < 0.7 : **régime structuré** — la gouvernance prévient les problèmes connus
- 0.7 <= R < 0.9 : **régime proactif** — la gouvernance anticipe les problèmes
- R >= 0.9 : **régime autonome** — la gouvernance s'améliore d'elle-même

### Signal 3 : saturation de la densité de politiques

Chaque nouvelle politique devrait améliorer la santé de la gouvernance. Quand ce n'est plus le cas, vous avez atteint la saturation :

```
marginal_return = delta_R / delta_policy_count
```

Quand `marginal_return → 0` sur 3 ajouts de politiques consécutifs ou plus, le système a extrait toute la valeur disponible de son régime actuel. Toute amélioration supplémentaire exige un changement qualitatif (nouvelle architecture, nouvel article constitutionnel, nouvelle couche d'observabilité) — une transition de phase.

**Réserve issue de la revue par GPT-4o :** Toutes les politiques ne sont pas également efficaces. Une meilleure mesure pondère chaque politique par sa portée (le nombre de personas qu'elle contraint). C'est un domaine de recherche ouvert.

### Signal 4 : force du couplage entre dépôts

Demerzel gouverne quatre dépôts (demerzel, ix, tars, ga). Relevez le taux de conformité de chaque dépôt à chaque cycle et, sur une fenêtre des W derniers cycles, faites la moyenne des valeurs absolues des corrélations de Pearson des six paires de dépôts (un seul cycle ne donne qu'un taux par dépôt, dont on ne peut tirer aucune corrélation). Prenez W d'au moins 30 cycles, le même dans toutes les fenêtres que vous comparez : avec W = 2, chaque corrélation vaut exactement ±1, et sur des fenêtres courtes le hasard seul donne de grandes valeurs, puisque pour deux dépôts indépendants l'espérance de |r| vaut environ 0.8/√(W − 1), soit 0.27 à W = 10 et 0.15 à W = 30, face au seuil de 0.3 ci-dessous. Prenez les valeurs absolues, car deux dépôts qui évoluent en sens opposés, avec une corrélation proche de −1, sont aussi fortement couplés que deux dépôts qui évoluent ensemble, et des corrélations de signes opposés s'annuleraient dans une moyenne signée. Une série constante, comme celle d'un dépôt qui reste à 100 %, n'a de corrélation avec rien : laissez ses paires de côté, et ne comparez deux fenêtres que sur les paires définies dans les deux. Une moyenne sur un autre ensemble de paires mesure autre chose, et écarter des paires faibles suffit à la faire monter jusqu'au régime fortement couplé. S'il ne reste aucune paire, le couplage n'est pas défini pour la fenêtre :

```
coupling = mean_{i<j} |pearson_correlation(rates_i[W], rates_j[W])|
```

| Couplage | Régime |
|----------|--------|
| < 0.3 | Faiblement couplé — les dépôts évoluent indépendamment |
| 0.3 - 0.7 | Couplage normal — les dépôts évoluent en partie en phase, ensemble ou en opposition |
| > 0.7 | Fortement couplé — les changements se propagent partout |

Un saut soudain du couplage (faible → fort) signifie que les dépôts se sont mis à évoluer en phase, mais pas dans quel sens : la moyenne écarte les signes, si bien que deux dépôts qui s'améliorent pendant que les deux autres déclinent en phase donnent |r| = 1 pour chaque paire, le couplage maximal, alors que l'écosystème se polarise au lieu de se centraliser. Avant de lire un saut comme une centralisation, regardez les signes des six corrélations : toutes positives, les dépôts évoluent ensemble ; positives à l'intérieur de deux groupes et négatives entre eux, ce sont deux camps. Une chute soudaine signifie que les dépôts évoluent plus indépendamment, comme dans une fragmentation. L'un comme l'autre peut marquer une transition de phase si d'autres signaux convergent vers elle (section 3).

### Signal 5 : fréquence des signaux de conscience

En mécanique statistique, les fluctuations croissent sans limite à l'approche d'un point critique, où la transition est continue (du second ordre). Près du point critique liquide–gaz, cela se manifeste par l'**opalescence critique** : les fluctuations de densité atteignent l'échelle de la longueur d'onde de la lumière, et le fluide devient laiteux. L'ébullition ordinaire, transition du premier ordre, n'a pas de tel signe avant-coureur.

L'analogie en gouvernance vaut donc pour les transitions continues : les signaux de conscience (anomalies, escalades, contradictions) deviendraient plus fréquents à l'approche de l'une d'elles. Une transition brutale, du premier ordre, comme l'activation d'un coupe-circuit, peut survenir sans prévenir.

```
signal_rate = conscience_signals_count / time_window
```

Un doublement du taux de signaux sur 3 cycles est un indicateur fort que le système est proche d'un point de transition. Les signaux eux-mêmes vous indiquent *dans quelle direction* va la transition.

**Où mesurer :** le répertoire `state/conscience/signals/`

### Signal 6 : le ratio de variété comme paramètre d'ordre candidat

D'après la cybernétique (CYB-003), le ratio de variété compare le régulateur à son environnement, et non les amplificateurs aux atténuateurs à l'intérieur du régulateur. Il se calcule à chaque cycle à partir des nombres de réponses distinctes que donne la gouvernance et de perturbations distinctes qu'elle rencontre :

```
variety_ratio = distinct_responses / distinct_disturbances
```

En bits, log2(variety_ratio) = V_R - V_D, avec V = log2 de chaque nombre. Un rapport des valeurs en bits, V_R / V_D, romprait cette identité, et diviserait par zéro dans un cycle qui rencontre une seule perturbation distincte, où V_D = log2(1) = 0. Un cycle qui ne rencontre aucune perturbation n'a pas de ratio.

C'est un **paramètre d'ordre candidat** pour les régimes de gouvernance, avec 1.0 comme frontière choisie :

- `variety_ratio < 1.0` : régime réactif (moins de réponses distinctes que de perturbations distinctes)
- `variety_ratio ≈ 1.0` : frontière (autant de réponses distinctes que de perturbations distinctes)
- `variety_ratio > 1.0` : régime proactif (plus de réponses distinctes que de perturbations distinctes)

Le ratio ne dit pas si la gouvernance régule. La loi d'Ashby s'énonce sur les issues : là où aucune réponse ne mène deux perturbations à la même issue et où N_η issues sont acceptables, portant V_η = log2(N_η) bits, réguler chaque perturbation demande V_R >= V_D - V_η. Un ratio inférieur à 1 est donc compatible avec une régulation complète quand assez d'issues sont acceptables, ou quand une même réponse mène plusieurs perturbations à la même issue acceptable, cas où la loi ne s'applique pas. Un ratio supérieur à 1 peut encore échouer, quand les réponses données ne sont pas celles dont les perturbations ont besoin. La régulation se lit sur l'issue de chaque perturbation, compte tenu de la réponse, et les nombres eux-mêmes viennent des relevés des perturbations rencontrées et des réponses données à chaque cycle.

Franchir 1.0 signifie seulement que les réponses distinctes égalent pour la première fois en nombre les perturbations distinctes ; ce n'est pas en soi une transition de phase. Le ratio peut passer 1 en douceur, quand une réponse de plus devient disponible, sans aucun changement qualitatif du système. Qualifier un franchissement de transition du second ordre exigerait un modèle du paramètre d'ordre qui montre un comportement critique près de 1.0, comme les fluctuations croissantes du signal 5 ; d'ici là, traitez 1.0 comme une frontière de régime.

---

## 3. Tout assembler : le diagramme de phases

```
                    R (score de santé)
                    │
     Autonome       │         ╱
     R >= 0.9       │       ╱
                    │     ╱
     ─ ─ ─ ─ ─ ─ ─│─ ─╱─ ─ ─ ─ ─ variety_ratio = 1.0
     Proactif       │ ╱
     R >= 0.7       │╱
                    ╱
     ─ ─ ─ ─ ─ ─ ╱│─ ─ ─ ─ ─ ─ ─ saturation des politiques
     Structuré    ╱ │
     R >= 0.5   ╱   │
              ╱     │
     ─ ─ ─ ╱─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ couplage critique
     Réactif        │
     R < 0.5        │
                    └────────────────── t (temps/cycles)
```

Chaque ligne horizontale est une frontière de régime choisie, pas une frontière de phase mesurée. Le système de gouvernance franchit ces frontières quand suffisamment de signaux s'alignent. Aucun signal isolé ne suffit — cherchez la **convergence** d'au moins 3 signaux indiquant la même direction de transition.

---

## 4. Exercice pratique

À partir de l'état actuel de la gouvernance de Demerzel :

1. Calculez l'indice de cristallisation à partir du fichier de poids de la psychohistoire :
   - `total_T = ?`, `total_U = ?`
   - `crystallization_index = total_T / max(total_U, 1)`

2. Prenez pour R l'`overall_score` du dernier enregistrement de `state/resilience/history.json`. Dans quel régime se trouve le système ? Que faudrait-il changer pour franchir la frontière suivante ?

3. Dans le même fichier, le cycle chaos-003 consigne, dans `metafixes_applied`, un nouveau fichier de politique et une section ajoutée à une politique existante, et dans `level_deltas` un gain au niveau L4, pendant que R passait de 0.64 (chaos-002) à 0.73. Calculez le rendement global des changements de ce cycle. Pourquoi la hausse de 0.09 ne peut-elle pas être attribuée à la seule nouvelle politique, et quelle observation isolerait son rendement ? Entre chaos-003 et chaos-004, R est monté à 0.82 sans nouveau fichier de politique : qu'est-ce que cela dit de la mesure des rendements par nombre de politiques ?

4. **Expérience de pensée :** Si les trois dépôts consommateurs (ix, tars, ga) atteignaient soudain 100 % de conformité, quelle transition de phase cela représenterait-il ? Est-ce souhaitable ?

---

## Points clés à retenir

- Les transitions de phase de la gouvernance sont des changements qualitatifs dans le fonctionnement du système, et pas seulement une croissance quantitative
- Six signaux mesurables permettent de détecter l'approche d'une transition : asymétrie des croyances, vitesse de la santé, saturation des politiques, force du couplage, fréquence des signaux de conscience et ratio de variété
- Le ratio de variété (issu de la cybernétique) est un paramètre d'ordre candidat — franchir 1.0 marque une frontière de régime, pas en soi une transition de phase, et la régulation se lit sur les issues, pas sur le ratio
- La plupart des transitions de gouvernance sont du second ordre (continues) — détectables mais pas brutales
- Aucun signal isolé ne suffit ; cherchez la convergence d'au moins 3 signaux

## Pour aller plus loin

- [PSY-001 : Introduction à la capitalisation fractale](psy-001-intro-fractal-compounding.fr.md) — prérequis sur D_c et ERGOL/LOLLI
- [CYB-003 : Mesurer quantitativement le ratio de variété](../../cybernetics/en/cyb-003-measuring-variety-ratio-quantitatively.md) (en anglais) — le paramètre d'ordre candidat
- [CYB-001 : Correspondance entre le VSM et la gouvernance de l'IA](../../cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md) — prérequis structurels
- Mécanique statistique des transitions de phase (théorie de Landau, paramètres d'ordre, exposants critiques)
- Fondation d'Asimov — la psychohistoire prédit des tendances agrégées, pas des événements individuels

---
*Produit par Seldon Auto-Research psychohistory-2026-03-23-001 le 2026-03-23.*
*Question de recherche : Quels signaux mesurables dans l'état d'une gouvernance de l'IA fondée sur des fichiers indiquent qu'un système de gouvernance approche d'une transition de phase ?*
*Croyance : T (confiance : 0.80) — accord entre Claude et GPT-4o, NotebookLM indisponible ; traduction française : U (non relue par un locuteur natif)*
