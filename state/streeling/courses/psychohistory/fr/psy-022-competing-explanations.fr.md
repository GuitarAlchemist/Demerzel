---
module_id: psy-022-competing-explanations
department: psychohistory
course: "Explications concurrentes : comparer des modèles sur peu de données"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-022
version: "0.1.0"
---

# Explications concurrentes : comparer des modèles sur peu de données

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous ajusterez trois lois de comptage par maximum de vraisemblance, vous les classerez avec l'AIC et le BIC, vous mesurerez à quelle fréquence ces critères désignent le vrai modèle à cette taille d'échantillon, et vous nommerez l'hypothèse que les trois partagent. **Question de projet :** les comptages quotidiens de déclencheurs peuvent s'« expliquer » par une loi de Poisson, une loi géométrique ou une loi binomiale négative ; quelle explication les données favorisent-elles, avec quelle netteté, et que la gagnante ne décrit-elle toujours pas ?

[PSY-008](psy-008-bursts-are-not-rates.fr.md) a montré que ces comptages sont bien plus dispersés que ceux d'un processus de Poisson et que les jours chargés arrivent par séries ; [PSY-007](psy-007-power-law-or-not.fr.md) et [PSY-010](psy-010-growth-curves-short-series.fr.md) ajustent d'autres familles à d'autres données.

## 1. Trois candidats et leurs vraisemblances

**Observé.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/extract.py) lit les 594 fichiers de [`state/triggers/archived`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) au commit `4b03838` et écrit [`observed-input.json`](../../../fixtures/psychohistory/psy-022/observed-input.json) : un comptage par jour civil UTC, n = 119 jours du 2026-03-20 au 2026-07-16, S = 594 événements. Parmi ces jours, 19 n'en comptent aucun, 63 en comptent exactement un et le plus chargé en compte 109 ; la variance, 196,848669 (diviseur n), est sans commune mesure avec la moyenne, 4,991597.

Chaque candidat attribue une probabilité à k événements dans une journée et traite les jours comme des tirages indépendants ; la log-vraisemblance (log L) est donc une somme sur les jours :

```text
Poisson             P(k) = exp(-λ) λ^k / k!                 log L = S ln λ - n λ - Σ ln(x!)
géométrique         P(k) = (1 - q) q^k                      log L = n ln(1 - q) + S ln q
binomiale négative  P(k) = [r (r+1) ... (r+k-1) / k!] (r/(r+μ))^r (μ/(r+μ))^k
```

Annuler la dérivée donne des formes explicites : λ = S/n et q = S/(n + S). Pour la binomiale négative, μ = S/n et r est le zéro de la fonction score d(log L)/dr, trouvé par une recherche à un paramètre ; la variance de cette loi vaut μ + μ²/r (celle de la géométrique vaut μ + μ², à r = 1). **Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-022/analyze.py) :

| Modèle | Estimations | log L |
|---|---|---|
| Poisson | λ = 4,991597 | −1 007,841 |
| géométrique | q = 594/713 = 0,8331 | −321,518 |
| binomiale négative | r = 0,430337 ; μ = 4,991597 | −298,913 |

**Vérification de la recherche.** La dichotomie appliquée au score (tolérance relative de 1e-10 sur r) renvoie 0,430337 à partir de trois intervalles de départ, [1e-6 ; 1e6], [0,01 ; 100] et [0,2 ; 3]. Une recherche par section dorée sur log L concorde à 1e-6 près et retrouve les formes explicites de la loi de Poisson et de la géométrique. Le score ne change de signe qu'une fois sur une grille allant de 1e-4 à 1e4 : il y a un seul maximum. À r = 1, la log L de la binomiale négative est égale à celle de la géométrique ; à r = 10^6, elle approche celle de la loi de Poisson, comme le prévoit la théorie.

### Exercice pratique 1

À partir de n = 119 et S = 594, calculez λ et q. Avec ln(1 − q) = −1,790358 et ln q = −0,182602, reconstruisez la log-vraisemblance de la géométrique. Pourquoi la binomiale négative doit-elle atteindre au moins cette valeur, quelles que soient les données ?

> **Réponse :** `λ = 594 / 119 = 4.991597` ; `q = 594 / (119 + 594) = 594/713 = 0.8331`. Ensuite `log L = 119 × (−1.790358) + 594 × (−0.182602) = −213.0526 − 108.4656 = −321.5182`, soit −321,518. Avec r = 1, la binomiale négative est la géométrique ; son maximum sur r ne peut donc pas être plus bas : le gain du modèle le plus grand est garanti, seule son ampleur est une information.

## 2. Le prix du paramètre supplémentaire : AIC et BIC

```text
AIC = 2k - 2 log L
BIC = k ln(n) - 2 log L        k = paramètres libres, ln(119) = 4.779123
```

La valeur la plus basse est la meilleure ; k vaut 1, 1 et 2 ; chaque paramètre coûte 2 points d'AIC et 4,779 points de BIC. **Calculé** à partir des log L arrondies à trois décimales :

| Modèle | AIC | ΔAIC | BIC | ΔBIC |
|---|---|---|---|---|
| Poisson | 2 017,682 | 1 415,856 | 2 020,461 | 1 413,077 |
| géométrique | 645,036 | 43,21 | 647,815 | 40,431 |
| binomiale négative | 601,826 | 0 | 607,384 | 0 |

Les deux critères donnent le même classement : binomiale négative, géométrique, Poisson. Le double du gain de log-vraisemblance obtenu en libérant r vaut 45,21.

**La netteté du verdict, sur les échelles des sources.** Burnham et Anderson (2004, p. 271) donnent pour ΔAIC des « simple rules of thumb » (règles empiriques simples) : jusqu'à 2, « substantial support » (un soutien substantiel) ; de 4 à 7, « considerably less support » (un soutien nettement moindre) ; au-delà de 10, « essentially no support » (pratiquement aucun soutien) ; les plages de 2 à 4 et de 7 à 10 ne portent pas de nom. Kass et Raftery (1995, p. 777) donnent une échelle pour le double du logarithme du facteur de Bayes, dont une différence de BIC fournit une approximation grossière (p. 778) : de 0 à 2, « not worth more than a bare mention » (ne mérite guère plus qu'une simple mention), de 2 à 6 positif, de 6 à 10 fort, au-delà de 10 très fort ; ils la présentent comme « not a calibration » (non un étalonnage) mais « a rough descriptive statement » (une description approximative). Sur les deux échelles, la géométrique et la loi de Poisson sont loin derrière.

**Ce que ces nombres ne sont pas.** Un ΔAIC de 43,21 n'est pas la probabilité que la géométrique soit fausse ou que la binomiale négative soit vraie. Burnham et Anderson lisent un ΔAIC élevé comme rendant un modèle moins plausible en tant que « the best approximating model in the candidate set » (le modèle qui approche le mieux la réalité parmi les candidats) ; à propos du BIC (p. 279), ils ajoutent qu'une probabilité a posteriori proche de 1 pour un modèle « does not justify an inference » (ne justifie pas de conclure) que ce modèle est la vérité, ce qui « requires an a priori certainty that the true model is in the model set » (exige d'être certain a priori que le vrai modèle figure parmi les modèles comparés).

### Exercice pratique 2

À partir de log L = −321,518 (géométrique) et −298,913 (binomiale négative), avec ln 119 = 4,779123, calculez l'AIC et le BIC des deux modèles ainsi que les deux différences. Lisez chaque différence sur l'échelle citée qui lui correspond.

> **Réponse :** AIC : `2 + 643.036 = 645.036` et `4 + 597.826 = 601.826`, différence 43,21 : « essentially no support » (pratiquement aucun soutien) pour la géométrique. BIC : `4.779123 + 643.036 = 647.815` et `9.558246 + 597.826 = 607.384`, différence 40,431 : « very strong » (très fort) sur l'échelle de Kass et Raftery. Ce sont des règles empiriques appliquées à un classement, pas des probabilités.

## 3. À quelle fréquence les critères désignent-ils le vrai modèle ?

**Synthétique.** Chaque modèle ajusté a généré, avec des graines fixées, 5 000 échantillons de jours indépendants à quatre longueurs (deux sont présentées), et les trois modèles ont été réajustés sur chacun d'eux. Part des échantillons où chaque critère a désigné le vrai générateur (AIC / BIC) :

| Vrai générateur | 15 jours | 119 jours |
|---|---|---|
| Poisson | 95,62 % / 97,54 % | 93,62 % / 98,62 % |
| géométrique | 82,06 % / 88,32 % | 84,30 % / 97,08 % |
| binomiale négative | 57,28 % / 49,84 % | 100 % / 99,94 % |

À 119 jours, les erreurs vont dans un seul sens : quand la géométrique est vraie, l'AIC choisit la binomiale négative dans 785 échantillons sur 5 000 (15,70 %), le BIC dans 146 (2,92 %). La théorie le prévoit : la géométrique est la binomiale négative à r = 1 ; le double du gain obtenu en libérant r se comporte donc, en grand échantillon, comme un khi-deux à 1 degré de liberté (Wilks 1938), et dépasse 2 avec une probabilité de 0,1573 et ln 119 avec une probabilité de 0,0288. Les deux parts simulées se situent à moins de deux erreurs types de ces valeurs. Aucun échantillon tiré de la géométrique n'a approché le gain observé de 45,21 (le plus grand : 12,934) ; 622 échantillons tirés de la binomiale négative l'ont atteint.

**Calculé : ce qui porte le classement.** Réajustement après retrait des jours les plus chargés :

| Jours les plus chargés retirés | r | ΔAIC (G − BN) | ΔBIC (G − BN) |
|---|---|---|---|
| 0 | 0,430337 | 43,21 | 40,431 |
| 1 (109 événements) | 0,493112 | 25,996 | 23,226 |
| 2 (109 et 72) | 0,556301 | 15,182 | 12,42 |
| 4 (45 ou plus) | 0,736965 | 1,578 | −1,167 |
| 11 (18 ou plus) | 2,702526 | 10,178 | 7,496 |

Les quatre jours les plus chargés, deux paires de jours voisins (21–22 mars, 27–28 juin), portent l'écart décisif. Avec onze jours retirés, la binomiale négative l'emporte de nouveau avec r = 2,7, moins dispersée que la géométrique : un même nom, deux formes. Réintégrer les douze fichiers déclencheurs supprimés sans avoir été archivés (un décompte emprunté à PSY-009) donne 44,566 et 41,787 : rien ne change.

### Exercice pratique 3

Synthétique. Un journal imaginaire de 15 jours donne un BIC inférieur de 1,1 pour la géométrique. À cette longueur, avec les paramètres ajustés plus haut, le BIC choisit la géométrique dans 4 416 échantillons sur 5 000 à graines fixées quand la géométrique est vraie, et dans 2 502 sur 5 000 quand la binomiale négative est vraie. Que rapportez-vous ?

> **Réponse :** L'écart de 1,1 se situe dans la plage de 0 à 2, « not worth more than a bare mention » (ne mérite guère plus qu'une simple mention). La vérification concorde : choisir la géométrique est `4,416 / 2,502 = 1.76` fois plus fréquent quand la géométrique est vraie que quand la binomiale négative l'est. Rapportez les deux modèles comme compatibles avec le journal ; 1,76 n'est pas une probabilité que la géométrique soit vraie.

### Exercice pratique 4

Retirez les quatre jours les plus chargés : il reste 115 jours, avec log L −247,501 (géométrique) et −245,712 (binomiale négative), et ln 115 = 4,744932. Quel modèle chaque critère choisit-il, et avec quel écart ?

> **Réponse :** AIC : `2 + 495.002 = 497.002` contre `4 + 491.424 = 495.424`, la binomiale négative l'emporte de 1,578. BIC : `4.744932 + 495.002 = 499.747` contre `9.489864 + 491.424 = 500.914`, la géométrique l'emporte de 1,167. Les critères se contredisent, et tous deux par moins de 2 : le verdict de 43,21 points repose sur 4 des 119 jours.

## 4. L'hypothèse que les trois partagent

**Calculé : une vérification absolue.** Les critères ne font que classer ; les nombres de jours attendus par tranche montrent ce que décrit chaque ajustement :

| Événements dans la journée | Observés | Poisson | géométrique | binomiale négative |
|---|---|---|---|---|
| 0 | 19 | 0,81 | 19,86 | 40,00 |
| 1 | 63 | 4,04 | 16,55 | 15,85 |
| 2 | 13 | 10,07 | 13,78 | 10,43 |
| 3 à 11 | 13 | 103,44 | 55,51 | 36,50 |
| 12 à 44 | 7 | 0,64 | 13,27 | 15,62 |
| 45 ou plus | 4 | 0,00 | 0,03 | 0,60 |

La gagnante fait mieux dans la queue (0,60 jour attendu à 45 événements ou plus, contre 0,03) et le paie dans le corps de la loi (exercice 5).

**L'ordre.** Permuter les jours laisse les trois log-vraisemblances inchangées (un autocontrôle), mais les données ne sont pas indifférentes à l'ordre : l'autocorrélation d'ordre 1 des comptages vaut 0,4587, une valeur atteinte par 3 permutations aléatoires sur 10 000 (95e centile des permutations : 0,1454) ; sur les rangs (chaque comptage remplacé par son rang, les ex æquo partageant leur rang moyen), elle vaut 0,3861, une valeur qu'aucune n'atteint. Témoins : un ordre permuté donne −0,0057, les jours triés 0,7209. Les jours chargés suivent les jours chargés : l'hypothèse commune de jours indépendants et identiquement distribués est fausse ici.

**Synthétique : ce que la dépendance fait aux critères.** Dans un processus géométrique *collant* (*sticky geometric*), chaque jour reprend le comptage de la veille avec la probabilité 0,46 et, sinon, est tiré à nouveau de la géométrique ajustée ; chaque jour suit donc toujours la loi géométrique. Sur 5 000 échantillons de 119 jours, l'AIC choisit la binomiale négative dans 2 008 cas (40,16 %, contre 15,70 % pour des jours indépendants) et le BIC dans 961 (19,22 %, contre 2,92 %) : les séries ressemblent à un surcroît de dispersion. Seul 1 échantillon a atteint un gain de 45,21 : de telles séries, à elles seules, produisent rarement l'écart observé. La binomiale négative est le moins mauvais de trois modèles de jours indépendants, non une description de la façon dont arrivent les déclencheurs.

**L'objection la plus forte à la lecture que fait cette leçon :** les quatre jours sont des données, pas du bruit ; un gain de 45,21 n'est apparu dans aucun échantillon géométrique indépendant et dans 1 seul échantillon collant sur 5 000, si bien que la binomiale négative capte à juste titre une queue plus lourde. La queue est effectivement plus lourde. Reste à savoir si une même binomiale négative, tirée à nouveau chaque jour, l'a produite : les quatre jours forment deux épisodes, non quatre tirages indépendants, et le mauvais ajustement à 0 et à 1 événement indique que le corps de la loi est erroné. **Cet échantillon ne permet pas de distinguer une loi marginale binomiale négative (la loi du comptage d'une journée) d'un mélange de jours ordinaires et de rares épisodes de rafales.** Un journal plus long, comptant beaucoup plus d'épisodes, trancherait, ou bien un modèle à deux régimes comparé à la binomiale négative sur des données qui n'ont servi à ajuster ni l'un ni l'autre.

### Exercice pratique 5

La binomiale négative ajustée donne P(0) = 0,336109 et P(1) = 0,13316. Calculez les nombres attendus de jours vides et de jours à un événement sur 119, comparez avec le journal, et réécrivez « les comptages quotidiens de déclencheurs suivent une loi binomiale négative » sous la forme d'un énoncé que ces résultats soutiennent.

> **Réponse :** `119 × 0.336109 = 40.00` jours vides contre 19, et `119 × 0.13316 = 15.85` jours à un événement contre 63 : la gagnante manque les deux comptages les plus fréquents d'un facteur d'environ 2 et 4 respectivement. Un énoncé soutenu : « Parmi trois modèles de jours indépendants, l'AIC et le BIC préfèrent la binomiale négative ; cette préférence repose sur quatre jours répartis en deux épisodes, l'ajustement manque les comptages les plus fréquents, et les jours ne sont pas indépendants. »

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** le dossier des déclencheurs archivés dont le lien figure plus haut ; `extract.py` refuse un dossier qui diffère de la version épinglée.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-022/extract.py`, puis `analyze.py` dans le même dossier ; `analyze.py --check` compare une nouvelle exécution au fichier [`results.json`](../../../fixtures/psychohistory/psy-022/results.json) enregistré. Les graines et les réglages sont dans [`scenarios.json`](../../../fixtures/psychohistory/psy-022/scenarios.json) ; le [README](../../../fixtures/psychohistory/psy-022/README.md) énumère les autocontrôles, un cas calculé à la main et les témoins négatifs.

**Références de méthode.** Akaike, H. (1974), « A new look at the statistical model identification », *IEEE Transactions on Automatic Control* 19(6), 716–723. Schwarz, G. (1978), « Estimating the Dimension of a Model », *The Annals of Statistics* 6(2), 461–464. Kass, R. E., et Raftery, A. E. (1995), « Bayes Factors », *Journal of the American Statistical Association* 90(430), 773–795 ([copie des auteurs](https://sites.stat.washington.edu/raftery/Research/PDF/kass1995.pdf)). Burnham, K. P., et Anderson, D. R. (2004), « Multimodel Inference: Understanding AIC and BIC in Model Selection », *Sociological Methods & Research* 33(2), 261–304. Wilks, S. S. (1938), « The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses », *The Annals of Mathematical Statistics* 9(1), 60–62.

**Non fait.** Aucun modèle de dépendance entre les jours n'a été ajusté, aucune correction de l'AIC pour petits échantillons n'a été appliquée, et aucune comparaison n'a été faite sur des données mises de côté (PSY-018 traite ce point). Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Ajuster aux 119 comptages un modèle à deux états (jours ordinaires et jours de rafale, chacun avec une probabilité de se maintenir) : s'il reproduit les 19 jours vides, les 63 jours à un événement et une autocorrélation d'ordre 1 proche de 0,46, la lecture passe de « le moins mauvais des trois » à « deux régimes ».
