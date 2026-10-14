---
module_id: psy-014-prediction-horizons
department: psychohistory
course: "Horizons de prévision : à quelle vitesse grandissent les petites erreurs"
level: intermediate
prerequisites: ["mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-014
version: "0.1.0"
---

# Horizons de prévision : à quelle vitesse grandissent les petites erreurs

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous exécuterez un modèle deux fois depuis des départs presque identiques, vous mesurerez comment la différence entre les deux trajectoires évolue, vous la résumerez par un exposant de Lyapunov, et vous en tirerez un *horizon de prévision* : le nombre de pas pendant lesquels une prévision reste dans une tolérance énoncée. **Question de projet :** jusqu'où peut-on se fier à un modèle déterministe quand son état de départ n'est connu qu'approximativement ?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) dit que la psychohistoire peut « predict the broad strokes » mais non les événements individuels, et [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) que les changements individuels sont imprévisibles tandis que le comportement agrégé suit des lois statistiques. Ni l'un ni l'autre ne dit jusqu'où une prévision tient, ni ce qu'achète une meilleure connaissance du présent : ce module répond aux deux pour un petit modèle, avec l'exposant de la section 2 de [MAT-024](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-024-dynamical-systems-stability-feedback.md). Les signaux d'alerte précoce relèvent de [PSY-012](psy-012-early-warning-false-alarms.fr.md), les règles d'alerte de PSY-023. Tous les résultats ci-dessous sont **synthétiques** : ils décrivent le modèle, non le projet.

## 1. Exécuter le modèle deux fois

Un modèle *déterministe* ne contient aucun hasard : le même départ donne toujours la même trajectoire. Le petit exemple de référence est l'*application logistique* (May 1976), qui fait évoluer un état x compris entre 0 et 1 par

```text
x_next = r * x * (1 - x)
```

où r est un réglage fixe. Après un transitoire, l'état se tient sur un *attracteur* : un point fixe à r = 2,9, un cycle de deux points à r = 3,2, une bande irrégulière à r = 3,7 et à r = 4. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-014/analyze.py) tire 1 000 points de départ à graine fixe ([`scenarios.json`](../../../fixtures/psychohistory/psy-014/scenarios.json)), laisse chacun se stabiliser pendant 1 000 pas, puis l'exécute deux fois : une fois tel quel, une fois décalé d'une *erreur initiale* de 1e-9. L'*écart* est la différence absolue entre les deux trajectoires au même pas.

**Synthétique.** Écart médian des 1 000 paires, d'après `gap_table` dans [`results.json`](../../../fixtures/psychohistory/psy-014/results.json) :

| Pas | r = 2,9 | r = 3,2 | r = 3,7 | r = 4 |
|---|---|---|---|---|
| 0 | 1e-9 | 1e-9 | 1e-9 | 1e-9 |
| 10 | 3,49e-10 | 1,05e-13 | 4,85e-8 | 1,04e-6 |
| 20 | 1,22e-10 | 0 | 1,72e-6 | 0,00107 |
| 30 | 4,24e-11 | 0 | 6,14e-5 | 0,537 |
| 60 | 1,8e-12 | 0 | 0,173 | 0,36 |

Un `0` signifie un écart trop petit pour les nombres sur 64 bits du programme (section 3), non un écart nul : recalculée avec des nombres sur 1 024 bits, la médiane à r = 3,2 vaut 1,1e-17 au pas 20.

Dans les deux premières colonnes, l'erreur se réduit. Ces *régimes stables* oublient leur départ : les 1 000 départs stabilisés se sont effondrés sur l'attracteur, les deux points du cycle à r = 3,2 et, à r = 2,9, le point fixe, que l'arrondi maintient sous la forme de deux nombres distants de 6,66e-16. Ces 1 000 paires répètent donc deux expériences. Dans les *régimes chaotiques* des deux dernières colonnes, l'écart croît d'un facteur à peu près constant par pas : c'est la *sensibilité aux conditions initiales*. Puis il s'arrête : un écart ne peut pas dépasser la taille de l'attracteur.

### Exercice pratique 1

À r = 2,9, une petite erreur est multipliée par 0,9 à chaque pas. Vérifiez-le sur le tableau à dix pas d'intervalle, puis calculez combien de pas font passer une erreur de 1e-3 sous 1e-6.

> **Réponse :** `0.9^10 = 0.3487`, et le tableau donne `3.49e-10 / 1e-9 = 0.349`. Une erreur chute d'un facteur 1 000 en `ln(1e-6 / 1e-3) / ln(0.9) = −6.9078 / −0.105361 = 65.56` pas, donc 66 pas ; le jeu d'essai en compte 66 dans les deux expériences. Ici une prévision s'améliore avec le temps, pourvu que l'erreur de départ soit petite.

## 2. Le taux : un exposant de Lyapunov

Tant qu'un écart est petit, un pas le multiplie par la taille de la pente de l'application à l'état courant, |r (1 − 2x)|. L'*exposant de Lyapunov* λ est la moyenne du logarithme de ce facteur le long d'une longue trajectoire :

```text
λ = moyenne de ln|r * (1 - 2 * x)| le long de la trajectoire
écart après n pas ≈ erreur initiale * e^(λ * n)      tant que l'écart reste petit
```

Un λ négatif signifie que les erreurs se réduisent ; un λ positif, qu'elles croissent en moyenne d'un facteur e^λ par pas. **Synthétique**, sur 1 000 000 de pas par réglage :

| r | λ estimé | λ connu | e^λ |
|---|---|---|---|
| 2,9 | −0,105361 | ln 0,9 = −0,105361 | 0,9 |
| 3,2 | −0,916291 | ln 0,4 = −0,916291 | 0,4 |
| 3,7 | 0,3547 ± 0,0003 | pas de forme fermée | 1,426 |
| 4 | 0,693144 | ln 2 = 0,693147 | 2 |

À r = 3,7, il n'y a que l'estimation ; son erreur type vient de 100 blocs de 10 000 pas. MAT-024 affiche 0,350235 à partir de 10 000 pas : le premier bloc de cette trajectoire, reproduit à six décimales.

L'exposant est une moyenne : à r = 3,2, la pente a une taille de 1,9165 en un point du cycle et de 0,0835 en l'autre, et leur produit vaut 0,16 = 0,4².

### Exercice pratique 2

Estimez λ à partir de deux entrées du tableau des écarts : pour r = 4 à partir des pas 0 et 20, pour r = 3,2 à partir des pas 0 et 10. Pourquoi le pas 30 est-il inutilisable pour r = 4 ?

> **Réponse :** r = 4 : `ln(0.00107 / 1e-9) / 20 = 13.8832 / 20 = 0.6942`, contre ln 2 = 0,6931. r = 3,2 : `ln(1.05e-13 / 1e-9) / 10 = −9.1616 / 10 = −0.9162`, contre −0,9163. Au pas 30, l'écart médian vaut 0,537 : la croissance s'est arrêtée à la taille de l'attracteur.

## 3. L'horizon, et le prix d'un chiffre

Appelons *tolérance* le plus grand écart que l'utilisateur d'une prévision accepte, et *horizon* le premier pas où l'écart l'atteint. En posant l'écart égal à la tolérance dans la loi de croissance, on obtient

```text
horizon ≈ ln(tolérance / erreur initiale) / λ
pas gagnés par chiffre décimal de précision supplémentaire = ln(10) / λ
```

**Synthétique.** Horizon moyen des 1 000 paires pour une tolérance de 0,1, à côté de la formule :

| Erreur initiale | r = 3,7 : moyenne | formule | r = 4 : moyenne | formule |
|---|---|---|---|---|
| 1e-3 | 12,93 | 12,98 | 6,79 | 6,64 |
| 1e-6 | 32,56 | 32,46 | 16,78 | 16,61 |
| 1e-9 | 51,54 | 51,93 | 26,78 | 26,58 |
| 1e-12 | 71,05 | 71,41 | 36,69 | 36,54 |

De 1e-3 à 1e-12, soit neuf chiffres de plus, l'horizon moyen gagne 58,12 pas à r = 3,7 et 29,9 à r = 4 : 6,46 et 3,32 pas par chiffre, contre 6,49 et 3,32 d'après la formule. **Dans un régime chaotique, chaque chiffre de précision achète le même petit nombre de pas.** Les seuils inscrits dans l'hypothèse du cycle de recherche avant la première exécution ont tous tenu : pente à 10 % près de celle de la formule, décalage de 5 pas au plus et variant de moins de 2 (mesuré : de −0,39 à 0,22 pas).

Là où λ est négatif, il n'y a pas d'horizon : à r = 2,9 et r = 3,2, aucune des 20 000 combinaisons de paire, d'erreur et de tolérance n'a atteint une tolérance (40 combinaisons distinctes chacune : les départs stabilisés sont 2 nombres). Un détecteur qui ne déclencherait jamais donnerait le même zéro : à titre de contrôle, une trajectoire partie de l'autre point du cycle de deux, à 0,286 de distance, est signalée au pas 1 et reste à 0,286. « Pas d'horizon » ne vaut que pour de petites erreurs.

L'arithmétique fixe son propre horizon. Un *double*, le format de nombre sur 64 bits de Python, porte 15,95 chiffres décimaux : entre 0,5 et 1, les valeurs voisines sont distantes de 2^-53 ≈ 1,11e-16. L'arrondi agit comme une erreur initiale : face à une trajectoire partie du même départ avec des nombres sur 1 024 bits, une trajectoire en doubles s'en écarte de 0,1 au bout de 53,27 pas en moyenne à r = 4 et de 99,55 à r = 3,7 ; au-delà, ce n'est plus l'orbite de l'application depuis son départ. Les horizons ci-dessus appartiennent bien à l'application : avec ces nombres, 3 horizons sur 10 000 (dix erreurs initiales) changent à r = 3,7 et 1 sur 10 000 à r = 4, de 2 pas au plus.

### Exercice pratique 3

À r = 3,7, prenez λ = 0,355 et une tolérance de 0,1. Calculez l'horizon pour une erreur initiale de 1e-6, puis ce qu'achète son amélioration à 1e-9.

> **Réponse :** `ln(0.1 / 1e-6) / 0.355 = 11.5129 / 0.355 = 32.43` pas (moyenne mesurée 32,56). Chaque chiffre vaut `ln(10) / 0.355 = 6.49` pas : trois chiffres achètent donc 19,46 pas et l'horizon devient 51,89. Une mesure 1 000 fois plus précise allonge l'horizon de `19.46 / 32.43 = 0.60`, soit 60 %.

### Exercice pratique 4

À r = 4, quelle erreur initiale garderait une prévision à 0,1 près pendant 100 pas ? Un double peut-il la fournir ?

> **Réponse :** `0.1 × e^(−0.693147 × 100) = 0.1 × 2^−100 = 7.89e-32`, ce qui exige 31,1 chiffres décimaux. Un double en a 15,95 : non. Avec un écartement de doubles comme erreur initiale, la formule donne `ln(0.1 / 1.11e-16) / 0.693147 = 49.68` pas, proche des 53,27 mesurés.

## 4. Au-delà de l'horizon, et ce dont un plan peut se servir

Passé l'horizon, l'état est perdu, mais pas tout. **Synthétique :** deux trajectoires à r = 4 parties de 0,3 et de 0,3 + 1e-12 sont distantes de 0,1 au pas 37, aussi bien en doubles qu'en nombres sur 1 024 bits. Au pas 100, les deux trajectoires calculées valent 0,673899 et 0,002785, des nombres qui dépendent déjà de l'arrondi : depuis les mêmes départs, les trajectoires sur 1 024 bits donnent 0,991939 et 0,735222. Pourtant, sur 100 000 pas, la première trajectoire calculée passe 33 353 pas sous 0,25 et la seconde 33 525, contre une part connue de 1/3. Les statistiques de l'attracteur restent prévisibles quand l'état ne l'est plus : la version à l'échelle d'un modèle de l'affirmation de PSY-002 sur les agrégats.

### Exercice pratique 5

Une prévision à r = 4 doit rester à 0,1 près à chacun de 60 pas. Option A : mesurer le départ une seule fois, à 1e-12 au lieu de 1e-6. Option B : garder 1e-6 et mesurer de nouveau tous les k pas. Sur 1 000 prévisions de ce genre, 972 restent dans la tolérance aux 60 pas pour k = 10, 960 pour 11, 924 pour 12 et 284 pour 16. Quelle option, et quel k le plus long, garde au moins 95 % des prévisions à 60 pas dans la tolérance ?

> **Réponse :** A échoue : l'horizon donné par la formule à 1e-12 est de 36,54 pas et le plus long des 1 000 horizons mesurés est de 49. B fonctionne jusqu'à k = 11, soit 6 mesures : `960 / 1,000 = 96.0%`, contre 92,4 % pour k = 12. Choisir k = 16, l'horizon 16,61 de la formule arrondi vers le bas, n'en garde que 28,4 % : un horizon est une distribution, ici de 9 à 24 pas autour d'une moyenne de 16,78. Le critère est son bas de fourchette, et le remède est de mesurer de nouveau, non de mesurer mieux.

**Analogie, non mesure.** Une feuille de route est une longue prévision depuis un présent approximativement connu. Si le processus qui la porte amplifie les petites différences, plus de détail sur aujourd'hui achète un allongement fixe et petit ; mesurer de nouveau et prévoir des distributions sont ce qui aide. S'il les amortit, les longues prévisions sont bon marché. Personne n'a mesuré d'exposant de Lyapunov pour ce projet : cette leçon ne peut pas dire lequel des deux cas s'applique.

**L'objection la plus forte** est que l'application logistique est un seul nombre sous une règle fixe. Un projet a de nombreuses variables, des personnes qui réagissent aux prévisions, et des chocs extérieurs ; avec des chocs, les erreurs croissent même depuis un départ parfaitement connu, et cette formule d'horizon n'a pas à tenir. Une série de projet notée dans [PSY-005](psy-005-persistence-baseline.fr.md) ne tranche pas : « rien ne change » a eu raison sur 1 528 des 1 529 paires de lignes consécutives (inégalement espacées), ce qui montre des étiquettes qui changent rarement, ou un relevé que personne ne révise, non la façon dont les erreurs de prévision croissent. **Ce jeu d'essai ne permet pas de distinguer un projet chaotique, un projet bruité et un projet stable.** Des prévisions datées d'une grandeur du projet, notées selon le délai d'anticipation, pourraient commencer à le faire : une erreur qui croît exponentiellement puis se stabilise indique un exposant positif ; une erreur qui reste plate, un régime stable ; une erreur présente dès le premier pas et qui croît sans phase exponentielle, un régime bruité.

## Sources, limites et prochaine vérification

**Épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** PSY-001, PSY-002 et MAT-024. Le jeu d'essai reproduit les quatre exposants que MAT-024 affiche pour ces réglages ; l'effectif de paires de lignes de la section 4 est celui de PSY-005.

**Jeu d'essai.** Depuis la racine du dépôt, `python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py`, puis la même commande avec `--check`. Il ne lit que `scenarios.json` et exécute 41 autovérifications ; son [README](../../../fixtures/psychohistory/psy-014/README.md) explique pourquoi la sortie est identique octet pour octet d'une plateforme à l'autre et énumère les limites.

**Références de méthode.** May, R. M. (1976), « Simple mathematical models with very complicated dynamics », *Nature* 261, 459–467. Lorenz, E. N. (1963), « Deterministic nonperiodic flow », *Journal of the Atmospheric Sciences* 20, 130–141 (la sensibilité aux conditions initiales). Strogatz, S. H. (2015), *Nonlinear Dynamics and Chaos*, 2e édition, Westview Press (les exposants de Lyapunov et l'horizon temporel d'une prévision).

**Non fait.** Aucune donnée de projet n'a été analysée et aucun exposant n'a été estimé pour une grandeur du projet. Une seule application, à une seule variable, sans bruit et avec une seule graine, a été étudiée. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Archiver à chaque exécution une prévision datée d'une grandeur du projet, par exemple l'effectif de modules de [PSY-010](psy-010-growth-curves-short-series.fr.md), et tracer l'erreur en fonction du délai d'anticipation une fois assez de prévisions arrivées à échéance. Une croissance exponentielle suivie d'un plateau serait une première indication d'exposant positif, non encore une estimation ; une courbe plate dirait que ce n'est pas l'horizon qui limite le plan.
