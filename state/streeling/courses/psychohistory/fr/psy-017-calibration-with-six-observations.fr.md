---
module_id: psy-017-calibration-with-six-observations
department: psychohistory
course: "La calibration à partir de six observations"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-017
version: "0.1.0"
---

# La calibration à partir de six observations

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous remonterez d'un enregistrement de calibration jusqu'aux fichiers qui fondent ses décomptes, vous placerez un intervalle exact sur une proportion calculée sur six cas, vous calculerez à quelle fréquence un prévisionniste calibré présente le même décompte, vous trouverez la taille d'échantillon qui sépare deux taux, et vous suivrez une règle de correction alimentée par six observations à la fois. **Question de projet :** un fichier de croyances consigne que 2 croyances à confiance élevée sur 6 ont été révisées par la suite, et décale un seuil de −0,1. Que peuvent dire six observations sur la calibration ?

[PSY-002](psy-002-governance-phase-transitions.fr.md) range l'asymétrie de la distribution des croyances parmi six signaux d'un changement de régime imminent ; ce module demande quel poids peut avoir un seul petit décompte relatif aux croyances. [PSY-004](psy-004-how-large-is-large.fr.md) construit l'intervalle exact repris ici, [PSY-016](psy-016-brier-score.fr.md) évalue des prévisions probabilistes avec le score de Brier, et [PSY-025](psy-025-capstone-preregistered-forecast.fr.md) utilise les deux.

## 1. Lire l'enregistrement, puis le recompter

**Observé.** Un *fichier de croyances* de `state/beliefs/` contient une proposition, une valeur de vérité (T vrai, P probable, U inconnu, D douteux, F faux, C contradictoire) et une `confidence` comprise entre 0 et 1. Au commit `4b03838`, le dossier contient huit fichiers `*.belief.json` (plus une liste YAML de 19 croyances, dont 9 à 0,85 ou plus, que le motif glob du producteur ignore), et [`archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived) en contient treize autres. Cette leçon repose sur l'un d'eux, [`confidence-calibration.belief.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/confidence-calibration.belief.json). Sa proposition dit de l'agent de gouvernance que son « confidence-assignment threshold is calibrated against the observed overconfidence-then-revision rate in her belief states. » (son seuil d'attribution de la confiance est calibré sur le taux observé d'excès de confiance suivi d'une révision dans ses états de croyance). Valeur de vérité P, confiance 0,92, un élément de preuve à l'appui, aucun en sens contraire. L'énoncé de cet élément, en entier :

```text
2 of 6 high-confidence beliefs (>= 0.85) were later revised (overconfidence_rate=0.3333). Revisions evidenced by archived prior versions: 2026-03-17-consumer-repo-integration-status.belief.json, 2026-03-17-ga-governance-integration.belief.json. Nudge magnitude capped at +/-0.1/cycle per ml-governance-feedback-policy.
```

Un bloc `calibration` stocke `threshold_nudge` −0,1, `applied_delta` 0,0, `prior_nudge` −0,1 et `cap` 0,1. Le fichier ne dit pas quelles six croyances ont été comptées, quel seuil l'ajustement déplace, ni si une croyance révisée était fausse.

**D'où vient l'enregistrement.** Ce n'est pas l'agent de gouvernance qui a calculé ces nombres : son *script d'application*, [`scripts/apply_ml_feedback.py`, lignes 130–154](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py#L130-L154), écrit la croyance avec une proposition fixe et une étiquette fixe, P (commentée « Probable: evidence leans true, magnitude still small-N », soit : probable, les preuves penchent vers le vrai, l'effectif reste faible), et recopie la confiance, l'énoncé et la fiabilité de l'énoncé depuis un document de recommandation, qu'un producteur situé dans un autre dépôt (`ix/scripts/confidence_calibrator.py`, nommé dans l'en-tête du script) calcule à partir de ces mêmes fichiers de croyances.

Trois fichiers épinglés énoncent la règle. La [politique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/ml-governance-feedback-policy.yaml#L57) définit le taux comme « Proportion of high-confidence beliefs that were later revised » (la proportion des croyances à confiance élevée révisées par la suite). La [spécification de la chaîne de traitement](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/ml-feedback-loop.ixql#L41) recommande un changement quand le taux dépasse 0,15, d'une ampleur de `max(-0.1, -1 * overconfidence_rate * 0.5)`. Le script d'application (ligne 128) ajoute cet ajustement au total stocké et borne le total à ±0,10.

**Calculé.** Ce producteur ([`confidence_calibrator.py`](https://github.com/GuitarAlchemist/ix/blob/6418fcc69012108af266544ec4cf5a931a8f78e8/scripts/confidence_calibrator.py), lu au commit `6418fcc` d'ix, hors du jeu d'essai) compte selon cette règle : tout fichier de croyances, actuel ou archivé, dont la confiance vaut au moins 0,85 est « à confiance élevée », et ceux d'entre eux qui sont archivés sont « révisés ». [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/extract.py) fige les 21 fichiers de croyances épinglés dans [`observed-input.json`](../../../fixtures/psychohistory/psy-017/observed-input.json), et [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/analyze.py) leur applique cette règle :

| Fichier de croyances | Valeur de vérité | Confiance | Groupe |
|---|---|---|---|
| `2026-03-18-consumer-repo-integration-status` | P | 0,85 | actuel |
| `2026-07-25-schema-conformance` | T | 0,95 | actuel |
| `confidence-calibration` | P | 0,92 | actuel |
| `remediation-effectiveness` | P | 0,90 | actuel |
| `2026-03-17-consumer-repo-integration-status` | F | 0,90 | archivé : révisé |
| `2026-03-17-ga-governance-integration` | F | 0,85 | archivé : révisé |

Quatre fichiers actuels et deux archivés font six, les deux archivés sont ceux que nomme l'énoncé, et la phrase reconstruite à partir du recomptage est identique à la phrase enregistrée ([`results.json`](../../../fixtures/psychohistory/psy-017/results.json), `recount`) : c'est un même calcul reproduit, non une seconde source. Les quatre autres fichiers actuels sont à 0,80 ou 0,82, les onze autres fichiers archivés à 0,5 ou 0, et les neuf croyances du fichier YAML ne sont jamais comptées.

L'enregistrement se compte lui-même : son propre 0,92 le range parmi les croyances à confiance élevée. Lui et `remediation-effectiveness` sont tous deux écrits par le script d'application, leurs confiances recopiées depuis des recommandations ; sans ces deux-là, la même règle donne 2 sur 4. Les six fichiers n'ont pas non plus été mis à jour pour la dernière fois à des dates comparables : les deux archivés 209,7 et 209,6 jours avant l'enregistrement, les quatre actuels 31,5 ; 30,5 ; 0 et 0 jours avant lui.

### Exercice pratique 1

À partir du taux enregistré et de `prior_nudge`, retrouvez `threshold_nudge` et `applied_delta` avec les deux formules épinglées.

> **Réponse :** `−0.5 × 2/6 = −0.1667`, que la formule limite à −0,1. Total stocké : `−0.1 + (−0.1) = −0.2`, ramené à −0,1, donc `threshold_nudge = −0.1` et `applied_delta = −0.1 − (−0.1) = 0.0`. Le total était déjà à sa limite : cette exécution n'a rien changé.

## 2. Ce que permet un décompte sur six

Un prévisionniste est *calibré* quand, parmi les énoncés qu'il fait avec la confiance c, une proportion c se révèle vraie. Cette leçon ajoute une interprétation que le dépôt n'énonce pas : toute révision est une erreur. Les croyances tenues à 0,85 ou plus devraient alors être révisées au plus 15 % du temps ; le seuil de déclenchement de la chaîne de traitement est ce même 0,15.

Traitons les six croyances comme des essais indépendants partageant un même taux de révision inconnu. L'*intervalle exact à 95 %* (bilatéral ; Clopper et Pearson ; PSY-004 en montre la construction) retient tous les taux sous lesquels le nombre observé ne tombe dans aucune des deux queues de 2,5 %. **Calculé :** pour 2 sur 6, il va de **0,0433 à 0,7772**, et il contient 15 %, 10 % et 5 %.

À quelle fréquence un prévisionniste dont le taux est connu présente-t-il deux révisions ou plus sur six ? **Calculé sous des taux supposés** ([`scenarios.json`](../../../fixtures/psychohistory/psy-017/scenarios.json)), pourcentages arrondis à deux décimales :

| Prévisionniste supposé | Vrai taux de révision | P(2 ou plus sur 6) |
|---|---|---|
| Calibré à 0,95 | 5 % | 3,28 % |
| Calibré à 0,90 | 10 % | 11,43 % |
| Calibré à 0,85 | 15 % | 22,35 % |
| Taux enregistré | un tiers | 64,88 % |

Un prévisionniste calibré exactement au seuil présente le décompte enregistré, ou pire, plus d'une fois sur cinq. Le *rapport de vraisemblance* compare la probabilité d'exactement 2 sur 6 sous deux taux : 0,329218 à un tiers contre 0,176177 à 15 %, soit un rapport de 1,87. **Cet échantillon ne permet pas de distinguer un prévisionniste calibré d'un prévisionniste trop confiant.**

### Exercice pratique 2

Calculez la probabilité de deux révisions ou plus sur six pour un vrai taux de 15 %.

> **Réponse :** `P(0) = 0.85^6 = 0.377150` et `P(1) = 6 × 0.15 × 0.85^5 = 0.399335`, donc `P(2 or more) = 1 − 0.377150 − 0.399335 = 0.2235` à quatre décimales près.

### Exercice pratique 3

Un collègue affirme : « Un tiers, c'est plus du double de 15 %, donc le prévisionniste est clairement trop confiant. » L'enregistrement étaye-t-il cette affirmation, la réfute-t-il, ou la laisse-t-il indécise ? Donnez deux nombres.

> **Réponse :** Il la laisse indécise. L'intervalle exact, de 0,0433 à 0,7772, contient 15 % et même 5 %, et un résultat d'exactement 2 sur 6 n'est que 1,87 fois plus probable à un tiers qu'à 15 %.

## 3. Combien d'observations sépareraient 15 % de 33 %

Prenons une règle : « déclarer le prévisionniste trop confiant quand c croyances ou plus sur n sont révisées ». Son taux de *fausses alertes* est la probabilité qu'un prévisionniste calibré (15 %) la déclenche ; son taux de *détection*, la probabilité qu'un prévisionniste trop confiant (un tiers) la déclenche. **Calculé** pour n = 6 :

| Règle | Fausse alerte | Détection |
|---|---|---|
| 1 ou plus sur 6 | 62,29 % | 91,22 % |
| 2 ou plus sur 6 | 22,35 % | 64,88 % |
| 3 ou plus sur 6 | 4,73 % | 31,96 % |

Pour maintenir les fausses alertes sous 5 %, il faut attendre trois révisions, et cette règle manque un prévisionniste trop confiant dans 68,04 % des cas. Le décompte enregistré, 2, ne l'atteint pas. La règle épinglée se déclenche dès la première ligne du tableau : une révision sur six, soit un taux de 0,1667, dépasse le seuil de déclenchement.

`analyze.py` explore tous les n jusqu'à 400 avec des sommes binomiales exactes. Le plus petit échantillon qui donne au plus 5 % de fausses alertes et au moins 80 % de détection compte **33** croyances (« 9 ou plus sur 33 » : 4,95 % et 82,12 %), soit 5,5 fois les six. Si le vrai taux était de 25 % au lieu d'un tiers, le même plan en demanderait 101.

### Exercice pratique 4

Supposez, uniquement pour fixer une échelle, que des croyances à confiance élevée continuent d'être enregistrées au rythme des six : six en 209,7 jours entre la plus ancienne d'entre elles et l'enregistrement. Combien de jours après la plus ancienne des six la 33e arriverait-elle, et combien de jours après l'enregistrement ?

> **Réponse :** `33 × 209.7 / 6 ≈ 1,153` jours après la plus ancienne, donc `27 × 209.7 / 6 ≈ 944` jours, soit environ 2,6 ans, après l'enregistrement. Le rythme est une hypothèse : les dates sont celles des dernières mises à jour, non des créations.

## 4. Une règle de correction nourrie de six observations

**Calculé à partir de la règle épinglée.** Avec six croyances par cycle, l'absence de révision laisse le total stocké inchangé, une révision le déplace de −0,0833, deux ou plus de −0,1. Un prévisionniste calibré à 15 % est ajusté à la baisse dans 62,29 % des cycles, un prévisionniste calibré à 5 % dans 26,49 %, un prévisionniste trop confiant dans 91,22 %. Rien de ce qui est enregistré ne fait monter le total : la branche à la hausse de la spécification exige un « underconfidence rate » (taux de sous-confiance), et le fichier de croyances n'en contient aucun.

**Synthétique.** Donnons à la règle son cas le plus favorable, six croyances nouvelles et indépendantes à chaque cycle, et suivons exactement le total stocké (une simulation à graine fixée de 20 000 parcours concorde à 0,0073 près) :

| Après | Calibré (15 %) : total à −0,1 | Trop confiant (un tiers) : total à −0,1 |
|---|---|---|
| 1 cycle | 22,35 % | 64,88 % |
| 4 cycles | 89,41 % | 99,92 % |
| 13 cycles | 99,9954 % | 100,00 % |

La politique prévoit cette calibration chaque semaine : 13 cycles font donc un trimestre. Les deux prévisionnistes sont alors à −0,1 : la valeur stockée est le point où la règle aboutit pour l'un comme pour l'autre, et elle ne dit rien de celui qui est à l'œuvre.

**Observé.** L'exécution enregistrée n'est pas ce cas favorable. `prior_nudge` vaut −0,1 et `applied_delta` vaut 0,0, et les deux révisions qu'elle cite ont été mises à jour pour la dernière fois le 2026-03-17 : cette exécution a relu des preuves anciennes.

**Ce que mesure « révisée ».** Les deux croyances archivées portent F : le 2026-03-17, elles jugeaient, à 0,90 et 0,85, qu'une étape d'intégration n'avait pas eu lieu. La [croyance actuelle sur ce sujet](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/2026-03-18-consumer-repo-integration-status.belief.json) cite des travaux datés du 2026-03-18. Les fichiers épinglés montrent des verdicts dépassés par les événements, et le [`SUPERSEDED.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived/SUPERSEDED.md) du dossier dit que les croyances archivées « are retired, not deleted » (sont retirées, non supprimées) ; rien n'indique que l'un ou l'autre verdict ait été faux au moment où il a été écrit. En sens inverse, le `refresh_note` de cette croyance actuelle consigne « T -> F » le 2026-09-12 et « F -> P » le 2026-09-13, des modifications faites sur place, qu'un décompte de fichiers archivés ne peut pas voir. En la comptant, on obtient 3 sur 6.

**La confiance de l'enregistrement lui-même.** Le producteur (cité, hors du commit épinglé) la fixe par `min(0.92, 0.70 + 0.02 × belief files read)`. Avec 21 fichiers, c'est le plafond, 0,92 : la formule n'utilise ni le 2 ni le 6, et dès huit fichiers elle atteint 0,85, le seuil (`CONF_AUTO_APPLY`) en dessous duquel le script d'application fait remonter une recommandation au lieu de l'appliquer. Ce 0,92 n'est donc pas un jugement sur la solidité des preuves de l'énoncé, et la section 2 dit ce qu'il ne peut pas signifier : à 95 % de confiance, six observations n'étayent aucun énoncé sur le taux de révision plus étroit que « entre 4 % et 78 % ».

**L'objection la plus forte à cette lecture** est bayésienne. Avec une loi a priori uniforme sur le taux, la probabilité qu'il dépasse 15 % est de 0,926235 après 2 sur 6. Mais cette loi a priori donne déjà 0,85 avant toute donnée : les six observations ajoutent donc 0,076 ; et l'objection hérite des défauts du décompte. Ce qui trancherait : une issue, juste ou fausse, constatée à délai fixe, pour au moins 33 croyances à confiance élevée que le script d'application n'écrit pas.

### Exercice pratique 5

(a) Pour le prévisionniste calibré du tableau, calculez la probabilité que le total stocké soit encore à 0 après 4 cycles. (b) Un −0,1 stocké doit-il être lu comme une preuve d'excès de confiance ? Énoncez votre critère.

> **Réponse :** (a) Aucune révision dans quatre échantillons de six : `0.377150^4 = 0.020233`, environ 2 %. (b) Non. Une observation n'est une preuve en faveur d'une hypothèse plutôt que d'une autre que si elle est nettement plus probable sous la première. Après 4 cycles, un total de −0,1 a une probabilité de 99,92 % pour le prévisionniste trop confiant et de 89,41 % pour le prévisionniste calibré, soit un rapport de `0.9992 / 0.8941 = 1.12` ; après 13 cycles, le rapport vaut 1,00. Les deux prévisionnistes sont synthétiques.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** la croyance de calibration, les vingt autres fichiers de croyances, la liste YAML de croyances, le `SUPERSEDED.md` de l'archive, la politique, la spécification de la chaîne de traitement et le script d'application dont les liens figurent plus haut.

**Jeu d'essai.** Le [README](../../../fixtures/psychohistory/psy-017/README.md) donne les commandes, les 32 autocontrôles et les témoins négatifs.

**Références de méthode.** Clopper, C. J., et Pearson, E. S. (1934), « The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial », *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404). Lichtenstein, S., Fischhoff, B., et Phillips, L. D. (1982), « Calibration of probabilities: The state of the art to 1980 », dans Kahneman, D., Slovic, P., et Tversky, A. (dir.), *Judgment under Uncertainty: Heuristics and Biases*, Cambridge University Press, 306–334.

**Non fait.** L'historique Git de la croyance de calibration n'a pas été lu : le nombre de cycles déjà appliqués est donc inconnu. On n'a pas vérifié si un processus lit l'ajustement stocké et déplace un seuil. Le document de recommandation que cite la croyance est un fichier produit à l'exécution, que le dépôt ne conserve pas, et la version du producteur d'ix qui l'a écrit n'est pas consignée. Chaque probabilité suppose des croyances indépendantes partageant un même taux, ce que les six ne sont pas ; les chiffres décrivent le cas le plus favorable pour ces données. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Lire l'historique de `state/beliefs/` pour compter les cycles et voir si les six ont jamais changé. Si chaque cycle a relu les deux mêmes fichiers archivés, la conclusion se précise : de « six observations ne permettent pas de trancher », elle passe à « un seul décompte de six, appliqué de nombreuses fois ».
