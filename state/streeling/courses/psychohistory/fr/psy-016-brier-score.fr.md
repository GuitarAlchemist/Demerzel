---
module_id: psy-016-brier-score
department: psychohistory
course: "Les prévisions probabilistes et le score de Brier"
level: intermediate
prerequisites: ["psy-005-persistence-baseline"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-016
version: "0.1.0"
---

# Les prévisions probabilistes et le score de Brier

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un historique d'étiquettes en un événement qui se produit ou non, vous évaluerez des probabilités annoncées avec le score de Brier et le score logarithmique, vous mesurerez la compétence par rapport à une prévision par le taux de base, et vous vérifierez si une règle de score est *propre*. **Question de projet :** comment évaluer une prévision probabiliste portant sur des étiquettes de gouvernance, et que récompense le score ?

[PSY-005](psy-005-persistence-baseline.fr.md) évaluait la prévision « l'étiquette reste la même » en comptant les annonces justes et les annonces fausses. Un prévisionniste qui dit « un changement a 2 % de chances de se produire » n'a, sur une paire donnée, ni raison ni tort : le nombre annoncé appelle un score spécifique, construit ici sur les paires de PSY-005. [PSY-017](psy-017-calibration-with-six-observations.fr.md) traite de la calibration (les probabilités annoncées correspondent-elles aux fréquences observées ?) sur une poignée d'issues ; [PSY-025](psy-025-capstone-preregistered-forecast.fr.md) applique le score à une prévision écrite à l'avance.

## 1. Un événement, une probabilité annoncée, un score

**Observé.** À chaque exécution du [script d'alimentation](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py) (le *feeder*), la [tendance de qualité](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) du dépôt gagne une ligne par artefact de gouvernance (une politique, une compétence), avec une étiquette d'efficacité (`effectiveness_to`) : une valeur de vérité, comme T (vrai) ou U (inconnu), attribuée à une proposition écrite portant sur l'artefact. Comme dans PSY-005, une *paire* est formée de deux lignes consécutives d'un même artefact, toutes deux étiquetées. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/extract.py) fige les cinq fichiers au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-016/observed-input.json) : 1 548 lignes, 18 artefacts, **1 529 paires**. L'étiquette diffère entre les deux lignes dans **1** paire. Onze paires partent d'une *ligne d'amorçage* (un état de départ consigné) et se terminent 78,5 jours plus tard, à la première exécution du feeder ; l'unique changement en fait partie. Les **1 518** autres paires relient deux exécutions du feeder séparées de 0,001 à 6,453 jours, et aucune n'a changé.

L'*événement* est « l'étiquette diffère à la ligne suivante de l'artefact » ; l'issue `o` vaut 1 s'il s'est produit et 0 sinon. Une *prévision probabiliste* annonce pour l'événement un nombre `p` compris entre 0 et 1, avant que l'issue soit connue. « La ligne suivante » ne correspond pas à une durée fixe : un prévisionniste qui annonce un même `p` pour toutes les paires traite un pas de 78,5 jours comme un pas de quelques minutes.

Le *score de Brier* est la moyenne des carrés des écarts entre la probabilité annoncée et l'issue :

```text
BS = (1/N) × somme des (p_i - o_i)²
```

Plus il est bas, mieux c'est : 0 correspond à un prévisionniste toujours certain et toujours dans le vrai, 1 à un prévisionniste toujours certain et toujours dans l'erreur. Brier (1950) ajoute le même terme pour « pas de changement », ce qui double chaque valeur (de 0 à 2) ; cette leçon utilise la forme courante, à un seul terme.

**Prévisionnistes synthétiques, scores calculés.** Personne n'a émis de prévision pour ces paires. [`scenarios.json`](../../../fixtures/psychohistory/psy-016/scenarios.json) définit des prévisionnistes imaginaires par la probabilité que chacun annonce, et [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-016/analyze.py) les évalue sur les issues observées ([`results.json`](../../../fixtures/psychohistory/psy-016/results.json)). Les scores sont arrondis à six décimales, ou à neuf quand c'est nécessaire.

| Prévisionniste | Annonce | Somme des carrés des erreurs | Score de Brier, 1 529 paires | Score de Brier, 1 518 paires |
|---|---|---|---|---|
| `never` | 0 | 1 | 0,000654022 | 0 |
| `base_rate` | 1/1 529 | 0,999346 | 0,000653594 | 0,000000428 |
| `one_percent` | 0,01 | 1,1329 | 0,000741 | 0,0001 |
| `five_percent` | 0,05 | 4,7225 | 0,003089 | 0,0025 |
| `coin` | 0,5 | 382,25 | 0,25 | 0,25 |

`never` est la prévision par persistance de PSY-005, annoncée avec certitude. Pour une prévision qui vaut 0 ou 1, le score de Brier est le taux d'erreur, ici 1/1 529, le taux de base de changement de PSY-005 ; `base_rate` annonce cette proportion pour chaque paire.

### Exercice pratique 1

Un prévisionniste annonce 0,02 pour chaque paire. Calculez sa somme des carrés des erreurs et son score de Brier sur les 1 529 paires, puis son score de Brier sur les 1 518 paires entre exécutions du feeder.

> **Réponse :** La paire qui a changé apporte `(0.02 − 1)² = 0.9604` ; les 1 528 paires inchangées apportent `1,528 × 0.02² = 0.6112`. Somme `1.5716` ; score de Brier `1.5716 / 1,529 = 0.001028`. Entre exécutions du feeder, rien n'a changé : chaque paire apporte donc `0.02² = 0.0004`, et c'est là le score.

## 2. Une seule paire porte le score

Le *score de compétence de Brier* (*Brier skill score*) compare une prévision à une référence sur les mêmes paires, comme PSY-005 le faisait pour l'exactitude ; mais cette leçon remplace la référence de PSY-005, la persistance, par le taux de base `b`, la proportion des paires où l'événement s'est produit, annoncé pour chaque paire :

```text
compétence = 1 - BS / BS_ref        BS_ref : score de Brier de la référence sur les mêmes paires
```

Pour la prévision par le taux de base, `BS_ref = b × (1 − b)`. Quand la référence ne commet aucune erreur, la compétence est indéfinie, comme elle l'était pour la persistance dans PSY-005 : sur les 1 518 paires, la référence annonce leur taux de base, 0, tandis que le prévisionniste `base_rate` garde 1/1 529.

**Calculé.** Chaque somme des carrés des erreurs se partage entre la part de la paire qui a changé et le reste :

| Prévisionniste | Part due à la paire qui a changé | Compétence |
|---|---|---|
| `never` | 100 % | −0,000654 |
| `base_rate` | 99,93 % | 0 |
| `one_percent` | 86,51 % | −0,133641 |
| `five_percent` | 19,11 % | −3,725591 |
| `coin` | 0,07 % | −381,500164 |
| `long_step_hedge` | 88,86 % | 0,087885 |

Pour un prévisionniste qui annonce le même `p` partout, le score vaut `(p - b)² + b × (1 - b)` : c'est le cas à une seule valeur de la décomposition de Murphy (1973), fiabilité moins résolution plus incertitude, où la résolution vaut 0. Le second terme, l'incertitude, ici 0,000654, est le même pour tous. Le premier, la fiabilité, est tout ce qu'un prévisionniste constant maîtrise : `(0.01 − 0.000654)² = 0.000087` pour `one_percent`. Aucune prévision constante ne peut donc battre le taux de base des paires sur lesquelles elle est évaluée : c'est une identité, non un résultat. Une compétence positive exige des probabilités différentes selon les paires, plus élevées là où les changements se produisent.

`long_step_hedge` (synthétique) y parvient avec une seule règle : 0,1 quand la ligne antérieure est une ligne d'amorçage, 0,001 sinon. Il arrive en tête, devant `base_rate` et `never`, avec une compétence de 0,087885. Mais ses probabilités ont été choisies par l'auteur de cette leçon après avoir vu où se trouvait le changement, et toute son avance vient d'une seule paire : retirez n'importe laquelle des 1 528 paires inchangées, le classement reste le même ; retirez la paire qui a changé, et ces trois places s'inversent.

**Après coup.** `base_rate` connaît lui aussi la réponse : 1/1 529 ne pouvait être annoncé qu'une fois toutes les issues connues. Son avance sur `never` est de 0,000000428, le carré de 1/1 529. Quand l'issue de la paire qui a changé a été connue, à la première exécution du feeder, aucune autre issue ne l'avait été avant elle : l'historique n'offrait donc aucun taux de base à annoncer.

Sur cet historique, les quatre premiers prévisionnistes obtiennent entre 0,000596 et 0,000741, et l'ordre des trois premiers repose sur une seule paire. Le score les sépare bien, en revanche, de `five_percent` et de `coin`.

### Exercice pratique 2

Recalculez la somme des carrés des erreurs de `long_step_hedge` à partir de ses deux probabilités et des décomptes de la section 1, puis son score de Brier et sa compétence. Que reste-t-il de la somme sans la paire qui a changé ?

> **Réponse :** Paire qui a changé, partie d'une ligne d'amorçage : `(0.1 − 1)² = 0.81`. Dix paires inchangées parties d'une ligne d'amorçage : `10 × 0.1² = 0.1`. Les 1 518 paires entre exécutions du feeder : `1,518 × 0.001² = 0.001518`. Somme `0.911518` ; score de Brier `0.911518 / 1,529 = 0.000596`. La somme du taux de base vaut `0.999346`, d'où une compétence `= 1 − 0.911518 / 0.999346 = 0.087885`. Sans la paire qui a changé, il reste `0.101518` sur 1 528 paires, soit un score de 0,000066 : derrière `never` (0) et `base_rate`, au rang 3.

### Exercice pratique 3

Combien des 1 529 paires devraient changer pour qu'annoncer 0,01 partout obtienne un meilleur score qu'annoncer 0 ? Et pour 0,05 ?

> **Réponse :** Avec `k` paires qui changent parmi `N`, `never` obtient `k/N` et un `p` constant obtient `[k(1 − p)² + (N − k)p²]/N`. Le second score est plus petit quand `Np² < 2kp`, c'est-à-dire quand `k > Np/2`. Pour 0,01 : `1,529 × 0.01 / 2 = 7.645`, donc 8 changements. Pour 0,05 : `38.225`, donc 39.

## 3. Ce que signifie « propre »

Une règle de score est *propre* quand un prévisionniste obtient le meilleur score espéré en annonçant la probabilité à laquelle il croit, et *strictement propre* quand aucune autre annonce ne fait aussi bien (Gneiting et Raftery 2007).

**Synthétique.** Supposons qu'un événement ait une probabilité vraie `t = 0.3` et qu'un prévisionniste annonce `q` à chaque fois. Le score de Brier espéré vaut `t(1 − q)² + (1 − t)q² = (q − t)² + t(1 − t)`. Une solution de rechange tentante, l'erreur absolue moyenne `|q − o|`, a pour espérance `t(1 − q) + (1 − t)q`.

| `q` annoncé | Score de Brier espéré | Erreur absolue espérée | Score de Brier moyen simulé |
|---|---|---|---|
| 0 | 0,3 | 0,3 | 0,30355 |
| 0,1 | 0,25 | 0,34 | 0,25284 |
| 0,3 | 0,21 | 0,42 | 0,21142 |
| 1 | 0,7 | 0,7 | 0,69645 |

Le score de Brier est minimal en `q = 0.3`, la vraie valeur. L'erreur absolue est minimale en `q = 0` : elle récompense le prévisionniste qui croit à 30 % s'il dit « jamais ». Une simulation à graine fixée (6 071 événements sur 20 000 cas) concorde.

Sous le score de Brier, une annonce inexacte coûte en espérance `(q − t)²` par prévision. Pour un événement rare, c'est peu : avec `t = 0.02`, annoncer 0 coûte 0,0004. D'où les premières lignes presque égales du tableau de la section 1 : le score de Brier est propre, mais il rémunère peu la différence entre « jamais » et « rarement ».

### Exercice pratique 4

Synthétique. Vous estimez qu'un événement a une probabilité de 0,2. Calculez le score de Brier espéré et l'erreur absolue espérée si vous annoncez 0,2, puis si vous annoncez 0. Quelle annonce chaque règle récompense-t-elle ?

> **Réponse :** Brier : annoncer 0,2 donne `0.2 × 0.8² + 0.8 × 0.2² = 0.16` ; annoncer 0 donne `0.2 × 1² + 0.8 × 0² = 0.2`. L'annonce sincère l'emporte de `0.04 = (0 − 0.2)²`. Erreur absolue : annoncer 0,2 donne `0.2 × 0.8 + 0.8 × 0.2 = 0.32` ; annoncer 0 donne `0.2`. Cette règle récompense une certitude que le prévisionniste n'a pas : elle n'est donc pas propre.

## 4. Le score logarithmique, et l'objection la plus forte

Le *score logarithmique* (Good 1952) est la moyenne de `−ln` de la probabilité attribuée à ce qui s'est produit : `−ln p` quand l'événement a eu lieu, `−ln(1 − p)` quand il n'a pas eu lieu. Il est lui aussi strictement propre. **Calculé** (logarithme népérien) :

| Prévisionniste | Score logarithmique, 1 529 paires | Score logarithmique, 1 518 paires |
|---|---|---|
| `never` | infini | 0 |
| `base_rate` | 0,005449 | 0,000654 |
| `one_percent` | 0,013056 | 0,01005 |
| `five_percent` | 0,053219 | 0,051293 |
| `coin` | 0,693147 | 0,693147 |
| `long_step_hedge` | 0,003188 | 0,001001 |

Entre exécutions du feeder, `never` est parfait sous les deux scores. Une fois l'unique événement ajouté, il est troisième sous le score de Brier, dont la perte est plafonnée à 1 par paire, et dernier sous le score logarithmique, parce que `−ln 0` n'a pas de valeur finie. Le score de Brier pardonne une certitude qui échoue une fois sur 1 529 paires ; le score logarithmique ne la pardonne jamais.

### Exercice pratique 5

Les pertes `−ln(…)` de `one_percent` totalisent 19,962083 sur les 1 529 paires ; la paire qui a changé en fournit `−ln 0.01 = 4.60517`. Vérifiez son score logarithmique et donnez la part de la paire qui a changé. Dites ensuite quel score une équipe devrait choisir si personne ne doit annoncer 0 pour une chose possible, et ce qui, dans les tableaux, le montre.

> **Réponse :** `19.962083 / 1,529 = 0.013056` ; la part est de `4.60517 / 19.962083 = 23.07%`, contre 86,51 % de l'erreur quadratique du même prévisionniste. L'équipe devrait choisir le score logarithmique : `never` passe de 0 sur les 1 518 paires à l'infini dès que la paire qui a changé est incluse, alors que son score de Brier ne passe que de 0 à 0,000654.

**Réponse à la question de projet.** Évaluez une probabilité annoncée avec une règle propre, face à une référence qui aurait pu être annoncée à l'avance. Le score de Brier récompense des probabilités sincères qui diffèrent là où les issues diffèrent ; sur cet historique, la règle `long_step_hedge`, choisie a posteriori, ne devance `base_rate` que de 0,000057, et cette avance tient à une seule paire.

**L'objection la plus forte à cette lecture** est que l'événement n'est peut-être pas de ceux qu'on peut prévoir. L'unique changement se situe sur le pas de 78,5 jours qui part d'une ligne d'amorçage, et PSY-005 y voit un retrait consigné, non une dérive. Entre exécutions du feeder, rien n'a changé : les deux scores y récompensent donc le plus petit nombre annoncé. Les 1 529 paires sont 18 artefacts relus à répétition, non des essais indépendants, et aucun score présenté ici n'est assorti d'une barre d'erreur. **Sous le score de Brier, cet échantillon ne permet pas de classer `never`, `base_rate` et `long_step_hedge` : leur ordre tient à une seule paire. Sous le score logarithmique, ces trois mêmes prévisionnistes échangent leurs places selon cette paire : avec elle, `never` est dernier et infini ; sans elle, premier.**

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les cinq fichiers de tendance de qualité et le script du feeder dont les liens figurent plus haut. `extract.py` refuse de s'exécuter si un fichier diffère de son blob Git épinglé.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-016/extract.py`, puis `analyze.py` dans le même dossier. Le [README](../../../fixtures/psychohistory/psy-016/README.md) énumère les autocontrôles et le témoin négatif.

**Références de méthode.** Brier, G. W. (1950), « Verification of Forecasts Expressed in Terms of Probability », *Monthly Weather Review* 78(1), 1–3. Murphy, A. H. (1973), « A New Vector Partition of the Probability Score », *Journal of Applied Meteorology* 12(4), 595–600. Gneiting, T., et Raftery, A. E. (2007), « Strictly Proper Scoring Rules, Prediction, and Estimation », *Journal of the American Statistical Association* 102(477), 359–378, [doi:10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437) (la règle y est écrite comme une récompense : leur score quadratique d'une prévision par oui ou non est l'opposé du score de Brier à deux termes, `−2(p − o)²`). Good, I. J. (1952), « Rational Decisions », *Journal of the Royal Statistical Society, Series B* 14(1), 107–114, [doi:10.1111/j.2517-6161.1952.tb00104.x](https://doi.org/10.1111/j.2517-6161.1952.tb00104.x).

**Non fait.** Aucune prévision n'a été émise avant son issue : tous les prévisionnistes sont imaginaires, et `base_rate` comme `long_step_hedge` utilisent une information connue après coup. La calibration n'a pas été examinée (PSY-017). Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Dès que l'historique contiendra plusieurs changements entre exécutions du feeder, évaluer des probabilités écrites avant chaque exécution face à une référence fixée à l'avance. Si une règle dont la probabilité croît avec le temps écoulé entre les deux lignes y garde une compétence positive, « une seule paire décide du classement » cède la place à « la longueur du pas porte de l'information ».
