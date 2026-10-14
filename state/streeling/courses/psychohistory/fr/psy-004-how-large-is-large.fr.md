---
module_id: psy-004-how-large-is-large
department: psychohistory
course: "Qu'est-ce qu'un grand nombre ? La prévisibilité d'un agrégat de quatorze agents"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-002-governance-phase-transitions"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-004
version: "0.1.0"
---

# Qu'est-ce qu'un grand nombre ? La prévisibilité d'un agrégat de quatorze agents

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous placerez un intervalle exact sur une proportion observée parmi quelques agents qui répondent par oui ou par non, vous direz comment sa largeur diminue quand le groupe grandit, et vous remplacerez le nombre d'agents par une taille d'échantillon effective quand les agents partagent une cause. **Question de projet :** le département affirme que le comportement agrégé de 14 personas sur 4 dépôts suit des lois mathématiques. Quelle est l'ampleur de l'incertitude sur un agrégat de 14, et qu'y change un contexte partagé ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) affirme que l'agrégat suit des lois statistiques, et lit la corrélation entre dépôts comme un signal de couplage. [PSY-019](../en/psy-019-combining-correlated-forecasters.md) applique la même arithmétique aux erreurs de prévision ; [PSY-024](../en/psy-024-the-single-actor.md) demande qui a agi dans les événements enregistrés.

## 1. Ce que dit la fiche et ce que contient le dépôt

**Observé.** La [fiche du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) conclut son principe clé par : « One agent's decision is unpredictable, but the aggregate behavior of 14 personas across 4 repos follows mathematical laws. » [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/extract.py) fige cette fiche, ainsi que les fichiers auxquels la phrase pourrait renvoyer, dans [`observed-input.json`](../../../fixtures/psychohistory/psy-004/observed-input.json).

- La fiche énumère 4 dépôts consommateurs, comme annoncé. Le dossier [`personas/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/personas) contient **17** fichiers de persona, 3 de plus qu'annoncé ; il en contenait 14 au [commit `e9fe8b7`](https://github.com/GuitarAlchemist/Demerzel/tree/e9fe8b7d711ede390b602896e4a5c571d0ad1f67/personas), qui a ajouté la fiche le 2026-03-21 (relevé avec `git ls-tree`, hors du jeu d'essai).
- Un fichier de persona décrit un rôle et n'enregistre aucune décision.
- Un [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) soumettrait une pull request à un panel de **5** personas, chacun la jugeant sous l'angle d'une préoccupation différente et répondant `block`, `merge_with_followups` ou `pass`. Les cinq reçoivent le même titre, la même description, la même liste de fichiers et le même diff tronqué, et la [tâche qui le lance](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) fixe un seul `--model`. Des commentaires y indiquent que le workflow a été « observed failing on every sibling-pr-opened dispatch » (vu en échec à chaque déclenchement sibling-pr-opened) et « silently never produced a verdict » (n'a jamais produit de verdict, sans rien signaler) en l'absence d'une permission que le fichier accorde ; aucun verdict n'est stocké au commit épinglé, où son dossier de verdicts, `state/quality/verdicts/`, n'existe pas.
- Parmi les fichiers lus, les seules réponses enregistrées de plusieurs relecteurs à une même question se trouvent dans [`state/council/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/council) : 5 verdicts sur une seule pull request, datés du 2026-06-24, avec 9 avis `pass` ou `fail`, au plus 2 par verdict (la limite fixée par le [schéma](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/council-verdict.schema.json)). Selon le [script qui les écrit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py), les relecteurs sont deux rôles, un contrôle automatisé (`reviewer_a`) et un relecteur fondé sur un modèle de langage (`reviewer_b`), et jamais un persona (0 sur 9). Dans les 4 verdicts qui comptent deux avis, les réponses concordent une fois et divergent trois fois.

**Calculé.** Le plus grand groupe dont l'instantané montre les réponses à une même question compte 2 membres ; le panel du workflow en compte 5, et non 14, et n'a rendu aucun verdict. Ce jeu d'essai ne peut donc pas tester l'affirmation. Tout ce qui suit est **synthétique** : des « agents » qui répondent oui ou non avec des probabilités supposées.

### Exercice pratique 1

Classez chaque énoncé comme observé, calculé à partir de données observées ou non étayé par l'instantané, en donnant la raison : (a) `personas/` contient 17 fichiers de persona ; (b) trois des quatre verdicts à deux avis sont partagés ; (c) les cinq verdicts du conseil sont cinq observations indépendantes de l'accord entre relecteurs ; (d) le comportement agrégé de 14 personas suit une loi statistique.

> **Réponse :** (a) Observé : un décompte de fichiers au commit épinglé. (b) Calculé à partir des avis observés : dans 3 des 4 verdicts à deux avis, les réponses divergent. (c) Non étayé : les 5 portent sur une même pull request, en l'espace d'une heure, et `reviewer_a` répond `pass` dans 5 cas sur 5 ; cela tient davantage d'une seule consultation répétée que de cinq. (d) Non étayé : le plus grand groupe enregistré compte 2 membres, aucun avis ne nomme un persona, et le panel de 5 n'a laissé aucun verdict.

## 2. Quatorze agents indépendants

Prenez n agents qui disent chacun oui, indépendamment les uns des autres, avec la même probabilité inconnue p. La *proportion* de oui, k/n, estime p. La loi des grands nombres dit que cette proportion se rapproche de p quand n grandit ; son écart-type, `sqrt(p (1 - p) / n)`, dit à quelle vitesse. Un *intervalle de confiance exact à 95 %* (Clopper et Pearson) retient toutes les valeurs de p sous lesquelles le nombre observé k ne tombe dans aucune des deux queues de 2,5 % (intervalle bilatéral ; la borne unilatérale de [PSY-006](psy-006-transition-matrix-from-counts.fr.md) place les 5 % dans une seule queue) :

```text
borne inférieure : le p tel que  P(X >= k) = 0.025
borne supérieure : le p tel que  P(X <= k) = 0.025      X ~ Binomiale(n, p)
si les n disent oui : borne inférieure = 0.025^(1/n), borne supérieure = 1
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/analyze.py) additionne les termes binomiaux et résout en p par dichotomie. **Calculé à partir d'entrées supposées** (la moitié des agents disent oui ; trois décimales) :

| Agents | Intervalle exact à 95 % | Largeur | Écart-type à p = 0,5 |
|---|---|---|---|
| 14 | 0,230 à 0,770 | 0,539 | 0,134 |
| 100 | 0,398 à 0,602 | 0,203 | 0,050 |
| 10 000 | 0,490 à 0,510 | 0,020 | 0,005 |

Quatorze agents partagés à égalité entre oui et non sont compatibles avec tout p compris entre 0,23 et 0,77, soit plus de la moitié de l'échelle. La largeur décroît comme l'inverse de la racine carrée de la taille du groupe : 100 agents donnent un intervalle 2,652 fois plus étroit (`sqrt(100 / 14) = 2.673`). L'approximation normale `n = z² p (1 - p) / h²`, avec z = 1,959964 et p = 0,5, demande 384,146, donc 385 agents, pour une demi-largeur h de 5 points.

Pour 14 agents, cet intervalle contient p au moins 95,5 % du temps, pour chacune des 99 valeurs de p de 0,01 à 0,99 ([`results.json`](../../../fixtures/psychohistory/psy-004/results.json)). Un panel de 5 en dit moins encore : si les cinq disent oui, la borne inférieure vaut `0.025^(1/5) = 0.478`.

### Exercice pratique 2

Les 14 agents disent tous oui. (a) Calculez la borne inférieure de l'intervalle exact à 95 %. (b) Combien d'agents indépendants doivent être unanimes pour que cette borne atteigne 0,95 ?

> **Réponse :** (a) `0.025^(1/14) = 0.768` : l'unanimité de 14 agents indépendants reste compatible avec une probabilité de oui de 0,77 seulement. (b) `0.025^(1/n) >= 0.95` donne `n >= ln 0.025 / ln 0.95 = 71.917`, donc 72 agents.

## 3. Des agents qui partagent une cause

Le panel de la section 1 donne à ses cinq personas un même diff et un même réglage de modèle : les agents d'un même projet peuvent partager des causes. **Synthétique, modèle supposé :** à chaque consultation (une question posée à tous les agents), un signal commun dit oui avec la probabilité p. Chaque agent le recopie avec la probabilité c et, sinon, décide seul, oui avec la probabilité p. Chaque agent dit toujours oui avec la probabilité p, mais deux réponses ont désormais la corrélation `rho = c²`. On a alors :

```text
variance de la proportion      = p (1 - p) / n × (1 + (n - 1) rho)
effet de plan                  = 1 + (n - 1) rho
taille d'échantillon effective = n / (1 + (n - 1) rho)        tend vers 1 / rho quand n croît
```

La *taille d'échantillon effective* est le nombre d'agents indépendants dont la proportion varierait autant que celle de ce groupe ; l'*effet de plan* (*design effect*) est le terme de Kish pour le rapport entre les deux. Pour 14 agents et p = 0,5, d'après la loi exacte du nombre de oui et 50 000 consultations simulées par ligne :

| rho | Effet de plan | Taille d'échantillon effective | Écart-type de la proportion | Nombre de oui dans au moins 95 % des consultations | Variance simulée ÷ variance sous indépendance |
|---|---|---|---|---|---|
| 0 | 1,0 | 14 | 0,134 | 3 à 11 | 0,990 |
| 0,1 | 2,3 | 6,087 | 0,203 | 2 à 12 | 2,291 |
| 0,3 | 4,9 | 2,857 | 0,296 | 1 à 13 | 4,926 |
| 0,6 | 8,8 | 1,591 | 0,396 | 0 à 14 | 8,792 |

La ligne 1 est le contrôle à réponse connue : rho = 0 redonne la variance binomiale.

Ajouter des agents n'y remédie pas. À rho = 0,1, la taille d'échantillon effective vaut 6,087 pour 14 agents, 9,174 pour 100 et 9,991 pour 10 000, sous un plafond de `1 / rho = 10`, et l'écart-type de la proportion ne peut pas descendre sous `sqrt(rho p (1 - p)) = 0.158`. La loi des grands nombres fait toujours disparaître, en moyenne, ce que chaque agent décide seul, mais pas le signal commun : la proportion de 10 000 agents se stabilise près de 0,658 ou de 0,342 (la probabilité de oui sachant le signal), et non de 0,5. Sous une telle cause commune, le décalage relevé à la section 1 compte peu : à rho = 0,3, 17 agents en valent 2,931 indépendants, contre 2,857 pour 14.

### Exercice pratique 3

Une équipe compte 100 agents avec rho = 0,3. Calculez l'effet de plan et la taille d'échantillon effective. Combien d'agents lui faudrait-il pour une taille d'échantillon effective de 5 ?

> **Réponse :** Effet de plan `1 + 99 × 0.3 = 30.7` ; taille d'échantillon effective `100 / 30.7 = 3.257`. Une taille d'échantillon effective de 5 est hors d'atteinte : le plafond vaut `1 / 0.3 = 3.333`. Seul un rho plus faible relève le plafond, et 5 exige un rho inférieur à `1 / 5 = 0.2`.

## 4. Ce que coûte l'oubli de la cause commune, et l'objection la plus forte

**Synthétique.** Appliquez l'intervalle de la section 2 à des agents qui partagent une cause, comme s'ils étaient indépendants. Avec p = 0,5, il contient p dans 98,7 % des consultations à rho = 0, 90,6 % à 0,1, 64,5 % à 0,3 et 20,4 % à 0,6 : à rho = 0,3, un intervalle « à 95 % » ne tient ici que deux fois sur trois.

Un tableau de bord imaginaire annonce que 12 agents sur 14 approuvent et parle d'un consensus fort. Lu comme un ensemble de réponses indépendantes, le décompte l'étaye : l'intervalle exact, de 0,572 à 0,982, exclut un partage égal. Mais quand p vaut 0,5, au moins 12 des 14 agents donnent la même réponse dans 1,3 % des consultations s'ils sont indépendants, 9,4 % à rho = 0,1, 35,5 % à 0,3 et 79,6 % à 0,6.

### Exercice pratique 4

Décidez si le tableau de bord peut annoncer un « consensus fort » selon ce critère : sous un partage égal, l'accord de 12 agents ou plus doit survenir dans moins de 5 % des consultations.

> **Réponse :** Cela dépend d'un nombre que personne n'a mesuré. Des agents indépendants donnent 1,3 %, sous les 5 % : autorisé. Un rho de 0,1 donne 9,4 %, et un rho de 0,3 en donne 35,5 % : non autorisé. La décision est « pas encore » : « 12 sur 14 » n'est une preuve solide que si les agents répondent de façon presque indépendante.

**L'objection la plus forte à cette lecture** est que les sections 3 et 4 reposent sur un seul modèle inventé et sur des valeurs inventées de rho. Un second modèle, avec les mêmes corrélations (chaque consultation tire un niveau commun q d'une loi bêta, et chaque agent dit oui avec la probabilité q), donne exactement la même variance et la même taille d'échantillon effective, qui ne dépendent que de rho. Ce n'est pas le cas des queues : à rho = 0,3, les 14 agents sont tous d'accord dans 10,7 % des consultations, contre 2,8 % dans le premier modèle. Plus important encore, le rho des personas est inconnu. S'il est proche de 0, la section 2 est toute la réponse. **Rien dans ce module ne permet de distinguer ce cas d'un rho de 0,6.**

Un journal des décisions le mesurerait : une réponse oui ou non par consultation et par persona, d'où l'on estime rho par `(b - m²) / (m (1 - m))`, m étant la proportion de oui et b celle des paires d'agents qui disent oui tous les deux. **Dimensionnement synthétique :** un journal détecte une cause commune quand son estimation dépasse le 95e centile des journaux simulés à rho = 0. Avec 14 agents, des journaux de 20 consultations détectent rho = 0,1 dans 2 312 cas sur 2 500 (92 %) et rho = 0,3 dans les 2 500. Avec les 5 agents du panel, ils détectent rho = 0,3 dans 9 447 cas sur 10 000 (94 %), mais rho = 0,1 dans 3 608 seulement (36 %) ; des journaux de 100 consultations détectent rho = 0,1 dans 1 759 cas sur 2 000 (88 %).

### Exercice pratique 5

Une équipe veut que la proportion de oui parmi ses agents tombe à moins de 5 points du taux de long terme p = 0,5 dans 95 % des consultations. (a) Quel écart-type de la proportion cela exige-t-il, et combien d'agents indépendants ? (b) Il s'avère que les agents ont un rho de 0,1. L'équipe peut-elle atteindre l'objectif en ajoutant des agents ?

> **Réponse :** (a) `0.05 / 1.959964 = 0.0255`, et `n = 1.959964² × 0.25 / 0.05² = 384.146` : environ 385 agents indépendants selon l'approximation normale. En calcul exact, 385 agents restent à moins de 5 points dans 94,7 % des consultations ; tous les groupes de 399 à 1 000 agents atteignent 95 %. (b) Non. Avec rho = 0,1, l'écart-type ne peut pas descendre sous `sqrt(0.1 × 0.25) = 0.158`, et la taille d'échantillon effective ne peut pas dépasser `1 / 0.1 = 10`, contre les 385 nécessaires. L'équipe doit faire baisser rho ou accepter une bande plus large.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers dont les liens figurent à la section 1.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-004/extract.py`, puis `analyze.py` dans le même dossier. Hypothèses et graines : [`scenarios.json`](../../../fixtures/psychohistory/psy-004/scenarios.json). Autocontrôles et témoins négatifs : [README](../../../fixtures/psychohistory/psy-004/README.md).

**Références de méthode.** Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413. Kish, L. (1965), *Survey Sampling*, Wiley (l'effet de plan).

**Non fait.** Aucune décision d'aucun persona n'a été lue et aucune corrélation entre personas n'a été estimée ; ce jeu d'essai a lu le workflow du panel sans l'exécuter. Les agents sont échangeables (un même p et un même rho pour tous) et ne répondent que oui ou non ; les personas du panel ont des préoccupations différentes et trois réponses possibles. Deux modèles générateurs ont été essayés, tous deux avec p = 0,5. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Les verdicts du panel constitueraient le journal des décisions : son script enregistre dans chacun une issue par persona. Une fois que des exécutions auront abouti et que 100 verdicts existeront, estimer rho. Une estimation proche de 0 ferait de la section 2 la réponse ; une estimation de 0,3 ou plus ramènerait les cinq voix du panel à au plus 2,273 voix indépendantes, et quatorze voix de ce type à au plus 2,857.
