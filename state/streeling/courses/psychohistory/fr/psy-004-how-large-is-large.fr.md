---
module_id: psy-004-how-large-is-large
department: psychohistory
course: "Grand comment ? La prévisibilité d'un agrégat de quatorze agents"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-002-governance-phase-transitions"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-004
version: "0.1.0"
---

# Grand comment ? La prévisibilité d'un agrégat de quatorze agents

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous poserez un intervalle exact sur une proportion observée chez quelques agents répondant par oui ou non, vous direz comment sa largeur se resserre quand le groupe grandit, et vous remplacerez l'effectif par une taille d'échantillon effective lorsque les agents partagent une cause. **Question de projet :** le département affirme que le comportement agrégé de 14 personas sur 4 dépôts suit des lois mathématiques. Quelle est la largeur de l'incertitude sur un agrégat de 14, et qu'y fait un contexte partagé ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) énonce que l'agrégat suit des lois statistiques et lit une corrélation entre dépôts comme un signal de couplage. PSY-019 applique la même arithmétique aux erreurs de prévision ; PSY-024 demande qui a agi dans les événements enregistrés.

## 1. Ce que le registre énonce et ce que le dépôt contient

**Observé.** Le [registre du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) termine son principe clé par : « One agent's decision is unpredictable, but the aggregate behavior of 14 personas across 4 repos follows mathematical laws. » [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/extract.py) prend un instantané de ce registre, et des fichiers auxquels la phrase pourrait renvoyer, dans [`observed-input.json`](../../../fixtures/psychohistory/psy-004/observed-input.json).

- Le registre énumère 4 dépôts consommateurs, comme annoncé. [`personas/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/personas) contient **17** fichiers de persona, 3 de plus qu'annoncé ; il en contenait 14 au [commit `e9fe8b7`](https://github.com/GuitarAlchemist/Demerzel/tree/e9fe8b7d711ede390b602896e4a5c571d0ad1f67/personas), qui a ajouté le registre le 2026-03-21 (lu avec `git ls-tree`, hors fixture).
- Un fichier de persona décrit un rôle et n'enregistre aucune décision.
- Un [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) soumettrait une pull request à un jury de **5** personas, chacune la jugeant sous un angle différent et répondant `block`, `merge_with_followups` ou `pass`. Les cinq reçoivent le même titre, le même corps, la même liste de fichiers et le même diff tronqué, et l'[exécution](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) fixe un seul `--model`. Des commentaires y indiquent que le workflow a été « observed failing on every sibling-pr-opened dispatch » et qu'il « silently never produced a verdict » faute d'une permission que le fichier accorde ; aucun verdict n'est stocké à l'épingle, où son dossier, `state/quality/verdicts/`, n'existe pas.
- Parmi les fichiers lus, les seules réponses enregistrées de plusieurs relecteurs à une même question sont dans [`state/council/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/council) : 5 verdicts sur une pull request, datés du 2026-06-24, avec 9 relectures `pass` ou `fail`, au plus 2 par verdict (la limite du [schéma](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/schemas/council-verdict.schema.json)). Les relecteurs sont deux rôles, une vérification automatisée (`reviewer_a`) et un relecteur à modèle de langage (`reviewer_b`) selon le [script qui les écrit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py), jamais une persona (0 sur 9). Dans les 4 verdicts à deux relectures, les réponses concordent une fois et diffèrent trois fois.

**Calculé.** Le plus grand groupe que l'instantané montre répondant à une même question compte 2 membres ; le jury du workflow en a 5, pas 14, et aucun verdict. Cette fixture ne peut donc pas éprouver l'affirmation. Tout ce qui suit est **synthétique** : des « agents » qui répondent oui ou non avec des probabilités supposées.

### Exercice pratique 1

Classez chaque énoncé comme observé, calculé à partir de données observées, ou non étayé par l'instantané, et donnez la raison : (a) `personas/` contient 17 fichiers de persona ; (b) trois des quatre verdicts à deux relectures sont partagés ; (c) les cinq verdicts du conseil sont cinq observations indépendantes de l'accord entre relecteurs ; (d) le comportement agrégé de 14 personas suit une loi statistique.

> **Réponse :** (a) Observé : un décompte de fichiers au commit épinglé. (b) Calculé à partir des relectures observées : dans 3 des 4 verdicts à deux relectures, les réponses diffèrent. (c) Non étayé : les 5 portent sur une seule pull request en moins d'une heure, et `reviewer_a` répond `pass` 5 fois sur 5 ; cela ressemble davantage à une occasion répétée qu'à cinq. (d) Non étayé : le plus grand groupe enregistré compte 2 membres, aucune relecture ne nomme de persona, et le jury de 5 n'a laissé aucun verdict.

## 2. Quatorze agents indépendants

Prenez n agents qui disent oui chacun avec la même probabilité inconnue p, indépendamment. La *proportion* de oui, k/n, estime p. La loi des grands nombres dit que la proportion tend vers p quand n grandit ; son écart type (ET), `sqrt(p (1 - p) / n)`, dit à quelle vitesse. Un *intervalle exact à 95 %* (Clopper et Pearson) retient tout p sous lequel le compte observé k ne tombe dans aucune des queues à 2,5 % (bilatéral ; la borne unilatérale de [PSY-006](psy-006-transition-matrix-from-counts.fr.md) place les 5 % dans une seule queue) :

```text
borne inférieure : le p pour lequel  P(X >= k) = 0.025
borne supérieure : le p pour lequel  P(X <= k) = 0.025      X ~ Binomiale(n, p)
si les n disent oui : borne inférieure = 0.025^(1/n), borne supérieure = 1
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-004/analyze.py) somme les termes binomiaux et résout en p par bissection. **Calculé à partir d'entrées supposées** (la moitié des agents disent oui ; trois décimales) :

| Agents | Intervalle exact à 95 % | Largeur | ET à p = 0,5 |
|---|---|---|---|
| 14 | 0.230 à 0.770 | 0.539 | 0.134 |
| 100 | 0.398 à 0.602 | 0.203 | 0.050 |
| 10 000 | 0.490 à 0.510 | 0.020 | 0.005 |

Quatorze agents partagés en deux parts égales sont compatibles avec tout p de 0,23 à 0,77, soit plus de la moitié de l'échelle. La largeur se resserre comme la racine carrée du groupe : 100 agents donnent un intervalle 2,652 fois plus étroit (`sqrt(100 / 14) = 2.673`). L'approximation normale `n = z² p (1 - p) / h²`, avec z = 1,959964 et p = 0,5, demande 384,146, donc 385 agents, pour une demi-largeur h de 5 points.

Pour 14 agents, cet intervalle contient p au moins 95,5 % du temps aux 99 valeurs de p de 0,01 à 0,99 ([`results.json`](../../../fixtures/psychohistory/psy-004/results.json)). Un jury de 5 en dit encore moins : si les cinq disent oui, la borne inférieure vaut `0.025^(1/5) = 0.478`.

### Exercice pratique 2

Les 14 agents disent tous oui. (a) Calculez la borne inférieure de l'intervalle exact à 95 %. (b) Combien d'agents indépendants doivent être unanimes pour que cette borne atteigne 0,95 ?

> **Réponse :** (a) `0.025^(1/14) = 0.768` : l'unanimité de 14 agents indépendants autorise une probabilité de oui aussi basse que 0,77. (b) `0.025^(1/n) >= 0.95` donne `n >= ln 0.025 / ln 0.95 = 71.917`, soit 72 agents.

## 3. Des agents qui partagent une cause

Le jury de la section 1 donne à ses cinq personas un seul diff et un seul réglage de modèle : des agents d'un même projet peuvent partager des causes. **Modèle synthétique supposé :** à chaque occasion (une question posée à tous les agents) un signal partagé dit oui avec la probabilité p. Chaque agent le recopie avec la probabilité c et sinon décide seul, oui avec la probabilité p. Chaque agent dit toujours oui avec la probabilité p, mais deux réponses ont désormais la corrélation `rho = c²`. Alors :

```text
variance de la proportion      = p (1 - p) / n × (1 + (n - 1) rho)
effet de plan                  = 1 + (n - 1) rho
taille d'échantillon effective = n / (1 + (n - 1) rho)    tend vers 1 / rho quand n grandit
```

La *taille d'échantillon effective* est le nombre d'agents indépendants dont la proportion varierait autant que celle de ce groupe ; l'*effet de plan* est le terme de Kish pour le facteur qui les sépare. Pour 14 agents et p = 0,5, d'après la distribution exacte des comptes et 50 000 occasions simulées par ligne :

| rho | Effet de plan | Taille d'échantillon effective | ET de la proportion | Comptes de oui sur au moins 95 % des occasions | Variance simulée ÷ indépendante |
|---|---|---|---|---|---|
| 0 | 1.0 | 14 | 0.134 | 3 à 11 | 0.990 |
| 0.1 | 2.3 | 6.087 | 0.203 | 2 à 12 | 2.291 |
| 0.3 | 4.9 | 2.857 | 0.296 | 1 à 13 | 4.926 |
| 0.6 | 8.8 | 1.591 | 0.396 | 0 à 14 | 8.792 |

La ligne 1 est la vérification à réponse connue : rho = 0 redonne la variance binomiale.

Ajouter des agents n'y remédie pas. À rho = 0,1 la taille d'échantillon effective vaut 6,087 pour 14 agents, 9,174 pour 100 et 9,991 pour 10 000, sous un plafond de `1 / rho = 10`, et l'ET de la proportion ne peut descendre sous `sqrt(rho p (1 - p)) = 0.158`. La loi des grands nombres moyenne toujours ce que chaque agent décide seul, mais pas le signal partagé : la proportion de 10 000 agents se fixe près de 0,658 ou 0,342 (la probabilité de oui sachant le signal), pas 0,5. Sous une telle cause partagée, l'écart de la section 1 pèse peu : à rho = 0,3, 17 agents en valent 2,931 indépendants, contre 2,857 pour 14.

### Exercice pratique 3

Une équipe compte 100 agents avec rho = 0,3. Calculez l'effet de plan et la taille d'échantillon effective. Combien d'agents lui faudrait-il pour une taille d'échantillon effective de 5 ?

> **Réponse :** Effet de plan `1 + 99 × 0.3 = 30.7` ; taille d'échantillon effective `100 / 30.7 = 3.257`. Une taille effective de 5 est hors d'atteinte : le plafond vaut `1 / 0.3 = 3.333`. Seul un rho plus bas relève le plafond, et 5 exige un rho inférieur à `1 / 5 = 0.2`.

## 4. Ce que coûte d'ignorer la cause partagée, et l'objection la plus forte

**Synthétique.** Appliquez l'intervalle de la section 2 à des agents qui partagent une cause, comme s'ils étaient indépendants. Avec p = 0,5 il contient p sur 98,7 % des occasions à rho = 0, 90,6 % à 0,1, 64,5 % à 0,3 et 20,4 % à 0,6 : à rho = 0,3, un intervalle « à 95 % » tient ici deux fois sur trois.

Un tableau de bord imaginaire rapporte que 12 des 14 agents approuvent et y voit un consensus fort. Lu comme des réponses indépendantes, le compte le soutient : l'intervalle exact, 0.572 à 0.982, exclut un partage égal. Mais quand p vaut 0,5, au moins 12 des 14 agents donnent la même réponse sur 1,3 % des occasions s'ils sont indépendants, 9,4 % à rho = 0,1, 35,5 % à 0,3 et 79,6 % à 0,6.

### Exercice pratique 4

Décidez si le tableau de bord peut annoncer un « consensus fort » sous ce critère : 12 agents concordants ou plus doivent survenir sur moins de 5 % des occasions sous un partage égal.

> **Réponse :** Cela dépend d'un nombre que personne n'a mesuré. Des agents indépendants donnent 1,3 %, sous 5 % : autorisé. Un rho de 0,1 donne 9,4 % et 0,3 donne 35,5 % : non autorisé. La décision est « pas encore » : « 12 sur 14 » n'est une preuve forte que si les agents répondent presque indépendamment.

**L'objection la plus forte à cette lecture** est que les sections 3 et 4 reposent sur un modèle inventé et des valeurs de rho inventées. Un second modèle aux mêmes corrélations (chaque occasion tire un niveau partagé q d'une loi Bêta, et chaque agent dit oui avec la probabilité q) donne exactement les mêmes variance et taille d'échantillon effective, qui ne dépendent que de rho. Les queues, non : à rho = 0,3 les 14 agents concordent sur 10,7 % des occasions, contre 2,8 % dans le premier modèle. Plus important, le rho des personas est inconnu. S'il est proche de 0, la section 2 est toute la réponse. **Rien dans ce module ne peut distinguer ce cas d'un rho de 0,6.**

Un journal de décisions le mesurerait : une réponse oui/non par occasion et par persona, dont rho s'estime par `(b - m²) / (m (1 - m))`, m étant la proportion de oui et b celle des paires d'agents disant oui tous les deux. **Dimensionnement synthétique :** un journal détecte une cause partagée quand son estimation dépasse le 95e centile de journaux simulés à rho = 0. Avec 14 agents, des journaux de 20 occasions détectent rho = 0,1 dans 2 312 cas sur 2 500 (92 %) et rho = 0,3 dans les 2 500. Avec les 5 agents du jury, ils détectent rho = 0,3 dans 9 447 cas sur 10 000 (94 %) mais rho = 0,1 dans 3 608 (36 %) ; des journaux de 100 occasions détectent rho = 0,1 dans 1 759 cas sur 2 000 (88 %).

### Exercice pratique 5

Une équipe veut que la proportion de oui parmi ses agents tombe à moins de 5 points du taux de long terme p = 0,5 sur 95 % des occasions. (a) Quel ET de la proportion cela exige-t-il, et combien d'agents indépendants ? (b) Les agents se révèlent avoir rho = 0,1. L'équipe peut-elle atteindre la cible en ajoutant des agents ?

> **Réponse :** (a) `0.05 / 1.959964 = 0.0255`, et `n = 1.959964² × 0.25 / 0.05² = 384.146` : environ 385 agents indépendants par l'approximation normale. Comptés exactement, 385 agents tombent à moins de 5 points sur 94,7 % des occasions ; tout groupe de 399 à 1 000 atteint 95 %. (b) Non. Avec rho = 0,1 l'ET ne peut descendre sous `sqrt(0.1 × 0.25) = 0.158`, et la taille d'échantillon effective ne peut dépasser `1 / 0.1 = 10`, contre les 385 requis. L'équipe doit abaisser rho ou accepter une bande plus large.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers liés en section 1.

**Fixture.** `python -I scripts/streeling_fixtures/psychohistory/psy-004/extract.py`, puis `analyze.py` dans le même dossier. Hypothèses et graines : [`scenarios.json`](../../../fixtures/psychohistory/psy-004/scenarios.json). Auto-vérifications et contrôles négatifs : [README](../../../fixtures/psychohistory/psy-004/README.md).

**Références de méthode.** Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413. Kish, L. (1965), *Survey Sampling*, Wiley (l'effet de plan).

**Non fait.** Aucune décision d'une persona n'a été lue et aucune corrélation entre personas n'a été estimée ; cette fixture a lu le jury du tribunal sans l'exécuter. Les agents sont échangeables (un seul p et un seul rho pour tous) et ne répondent que par oui ou non ; les personas du jury ont des angles différents et trois réponses possibles. Deux modèles générateurs ont été essayés, tous deux à p = 0,5. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Les verdicts du jury seraient le journal de décisions : son script y stocke une issue par persona. Dès que les exécutions aboutissent et que 100 verdicts existent, estimer rho. Une estimation proche de 0 ferait de la section 2 la réponse ; une de 0,3 ou plus ramènerait les cinq voix du jury à 2,273 voix indépendantes au plus, et quatorze de ces voix à 2,857.
