---
module_id: psy-014-prediction-horizons
department: psychohistory
course: "Horizons de prévisibilité : à quelle vitesse croissent les petites erreurs"
level: intermediate
prerequisites: ["mat-024-dynamical-systems-stability-feedback"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-014
version: "0.1.0"
---

# Horizons de prévisibilité : à quelle vitesse croissent les petites erreurs

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous lancerez un modèle deux fois à partir de départs presque identiques, vous mesurerez comment évolue l'écart entre les deux trajectoires, vous le résumerez par un exposant de Lyapunov et vous en tirerez un *horizon de prévisibilité* : le nombre de pas pendant lequel une prévision reste dans une tolérance fixée. **Question de projet :** jusqu'à quelle échéance peut-on se fier à un modèle déterministe dont l'état de départ n'est connu qu'approximativement ?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) affirme que la psychohistoire peut « predict the broad strokes » (prédire les grandes lignes), mais non les événements individuels, et [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) que les changements individuels sont imprévisibles alors que le comportement agrégé suit des lois statistiques. Ni l'un ni l'autre ne dit jusqu'à quelle échéance une prévision tient, ni ce que rapporte une meilleure connaissance du présent : ce module répond aux deux questions pour un petit modèle, avec l'exposant de la section 2 de [MAT-024](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/mathematics/en/mat-024-dynamical-systems-stability-feedback.md). Les signaux d'alerte précoce relèvent de [PSY-012](psy-012-early-warning-false-alarms.fr.md), les règles d'alerte de [PSY-023](../en/psy-023-monitoring-a-plan.md). Tous les résultats ci-dessous sont **synthétiques** : ils décrivent le modèle, pas le projet.

## 1. Lancer le modèle deux fois

Un modèle *déterministe* ne contient aucun hasard : le même départ donne toujours la même trajectoire. Le petit exemple classique est l'*application logistique* (May 1976), qui met à jour un état x compris entre 0 et 1 par

```text
x_next = r * x * (1 - x)
```

où r est un paramètre fixé. Après un régime transitoire, l'état reste sur un *attracteur* : un point fixe à r = 2,9, un cycle de deux points à r = 3,2, une bande irrégulière à r = 3,7 et à r = 4. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-014/analyze.py) tire 1 000 points de départ avec une graine fixée ([`scenarios.json`](../../../fixtures/psychohistory/psy-014/scenarios.json)), laisse chacun se stabiliser pendant 1 000 pas, puis le fait évoluer deux fois : une fois tel quel, une fois décalé d'une *erreur initiale* de 1e-9. L'*écart* est la différence absolue entre les deux trajectoires au même pas.

**Synthétique.** Écart médian des 1 000 paires, d'après `gap_table` dans [`results.json`](../../../fixtures/psychohistory/psy-014/results.json) :

| Pas | r = 2,9 | r = 3,2 | r = 3,7 | r = 4 |
|---|---|---|---|---|
| 0 | 1e-9 | 1e-9 | 1e-9 | 1e-9 |
| 10 | 3,49e-10 | 1,05e-13 | 4,85e-8 | 1,04e-6 |
| 20 | 1,22e-10 | 0 | 1,72e-6 | 0,00107 |
| 30 | 4,24e-11 | 0 | 6,14e-5 | 0,537 |
| 60 | 1,8e-12 | 0 | 0,173 | 0,36 |

Un `0` désigne un écart trop petit pour les nombres en virgule flottante 64 bits du programme (section 3), et non un écart nul : recalculée avec des nombres à 1 024 bits, la médiane à r = 3,2 vaut 1,1e-17 au pas 20.

Dans les deux premières colonnes, l'erreur diminue. Ces *régimes stables* oublient leur départ : les 1 000 départs stabilisés se sont tous réduits à l'attracteur, c'est-à-dire aux deux points du cycle à r = 3,2 et, à r = 2,9, au point fixe, que l'arrondi représente par deux nombres distants de 6,66e-16. Ces 1 000 paires répètent donc deux expériences. Dans les *régimes chaotiques* des deux dernières colonnes, l'écart est multiplié à chaque pas par un facteur à peu près constant : c'est la *sensibilité aux conditions initiales*. Puis la croissance s'arrête : un écart ne peut pas dépasser la taille de l'attracteur.

### Exercice pratique 1

À r = 2,9, une petite erreur est multipliée par 0,9 à chaque pas. Vérifiez-le sur dix pas à l'aide du tableau, puis calculez au bout de combien de pas une erreur de 1e-3 passe sous 1e-6.

> **Réponse :** `0.9^10 = 0.3487`, et le tableau donne `3.49e-10 / 1e-9 = 0.349`. Une erreur est divisée par 1 000 en `ln(1e-6 / 1e-3) / ln(0.9) = −6.9078 / −0.105361 = 65.56` pas, soit 66 pas ; le jeu d'essai en compte 66 dans les deux expériences. Ici, une prévision s'améliore avec le temps, pourvu que l'erreur de départ soit petite.

## 2. Le taux : un exposant de Lyapunov

Tant qu'un écart est petit, un pas le multiplie par la valeur absolue de la pente de l'application en l'état courant, |r (1 − 2x)|. L'*exposant de Lyapunov* λ est la moyenne du logarithme de ce facteur le long d'une longue trajectoire :

```text
λ = moyenne de ln|r * (1 - 2 * x)| le long de la trajectoire
écart après n pas ≈ erreur initiale * e^(λ * n)      tant que l'écart reste petit
```

Un λ négatif signifie que les erreurs diminuent ; un λ positif, qu'elles croissent en moyenne d'un facteur e^λ par pas. **Synthétique**, sur 1 000 000 pas pour chaque valeur de r :

| r | λ estimé | λ connu | e^λ |
|---|---|---|---|
| 2,9 | −0,105361 | ln 0,9 = −0,105361 | 0,9 |
| 3,2 | −0,916291 | ln 0,4 = −0,916291 | 0,4 |
| 3,7 | 0,3547 ± 0,0003 | pas de forme close | 1,426 |
| 4 | 0,693144 | ln 2 = 0,693147 | 2 |

À r = 3,7, on ne dispose que de l'estimation ; son erreur type provient de 100 blocs de 10 000 pas. MAT-024 affiche 0,350235 sur 10 000 pas : c'est le premier bloc de cette trajectoire, reproduit à six décimales près.

L'exposant est une moyenne : à r = 3,2, la pente vaut 1,9165 en valeur absolue en un point du cycle et 0,0835 en l'autre, et leur produit vaut 0,16 = 0,4².

### Exercice pratique 2

Estimez λ à partir de deux valeurs du tableau des écarts : pour r = 4, à partir des pas 0 et 20 ; pour r = 3,2, à partir des pas 0 et 10. Pourquoi le pas 30 est-il inutilisable pour r = 4 ?

> **Réponse :** r = 4 : `ln(0.00107 / 1e-9) / 20 = 13.8832 / 20 = 0.6942`, contre ln 2 = 0,6931. r = 3,2 : `ln(1.05e-13 / 1e-9) / 10 = −9.1616 / 10 = −0.9162`, contre −0,9163. Au pas 30, l'écart médian vaut 0,537 : la croissance s'est arrêtée à la taille de l'attracteur.

## 3. L'horizon, et le prix d'un chiffre

Appelons *tolérance* le plus grand écart que l'utilisateur d'une prévision accepte, et *horizon* le premier pas auquel l'écart l'atteint. En égalant l'écart à la tolérance dans la loi de croissance, on obtient

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

De 1e-3 à 1e-12, soit neuf chiffres de plus, l'horizon moyen gagne 58,12 pas à r = 3,7 et 29,9 à r = 4 : 6,46 et 3,32 pas par chiffre, contre 6,49 et 3,32 d'après la formule. **En régime chaotique, chaque chiffre de précision rapporte le même petit nombre de pas.** Les seuils inscrits dans l'hypothèse du cycle de recherche avant la première exécution ont tous été respectés : une pente à moins de 10 % de celle de la formule, un décalage d'au plus 5 pas qui varie de moins de 2 (mesuré : de −0,39 à 0,22 pas).

Là où λ est négatif, il n'y a pas d'horizon : à r = 2,9 et à r = 3,2, aucune des 20 000 combinaisons de paire, d'erreur et de tolérance (1 000 paires, dix erreurs, tolérances 0,1 et 0,01) n'a atteint sa tolérance (40 combinaisons distinctes dans chaque cas : les départs stabilisés se réduisent à 2 nombres). Un détecteur qui ne se déclenche jamais donnerait le même zéro : en guise de témoin, une trajectoire lancée sur l'autre point du cycle de période deux, à 0,286 de distance, est signalée dès le pas 1 et reste à 0,286. « Pas d'horizon » ne vaut que pour les petites erreurs.

L'arithmétique fixe son propre horizon. Un *double*, le format de nombre en virgule flottante 64 bits de Python, offre 15,95 chiffres décimaux : entre 0,5 et 1, deux valeurs voisines sont distantes de 2^-53 ≈ 1,11e-16. L'arrondi agit comme une erreur initiale : comparée à une trajectoire issue du même départ et calculée avec des nombres à 1 024 bits, une trajectoire calculée en doubles s'en écarte de 0,1 au bout de 53,27 pas en moyenne à r = 4 et de 99,55 pas à r = 3,7 ; au-delà, ce n'est plus l'orbite de l'application issue de son départ. Les horizons ci-dessus restent bien ceux de l'application : avec ces nombres-là, 3 horizons sur 10 000 (dix erreurs initiales) changent à r = 3,7 et 1 sur 10 000 à r = 4, d'au plus 2 pas.

### Exercice pratique 3

À r = 3,7, prenez λ = 0,355 et une tolérance de 0,1. Calculez l'horizon pour une erreur initiale de 1e-6, puis ce que rapporte une erreur réduite à 1e-9.

> **Réponse :** `ln(0.1 / 1e-6) / 0.355 = 11.5129 / 0.355 = 32.43` pas (moyenne mesurée : 32,56). Chaque chiffre vaut `ln(10) / 0.355 = 6.49` pas ; trois chiffres rapportent donc 19,46 pas, et l'horizon passe à 51,89. Une mesure 1 000 fois plus précise allonge l'horizon de `19.46 / 32.43 = 0.60`, soit 60 %.

### Exercice pratique 4

À r = 4, quelle erreur initiale maintiendrait une prévision à moins de 0,1 pendant 100 pas ? Un double permet-il de l'atteindre ?

> **Réponse :** `0.1 × e^(−0.693147 × 100) = 0.1 × 2^−100 = 7.89e-32`, ce qui demande 31,1 chiffres décimaux. Un double en offre 15,95 : donc non. Avec pour erreur initiale un seul écart entre doubles voisins, la formule donne `ln(0.1 / 1.11e-16) / 0.693147 = 49.68` pas, proche des 53,27 mesurés.

## 4. Au-delà de l'horizon, et ce dont un plan peut se servir

Au-delà de l'horizon, l'état est perdu, mais pas tout le reste. **Synthétique :** deux trajectoires à r = 4, issues de 0,3 et de 0,3 + 1e-12, sont distantes de 0,1 au pas 37, en doubles comme en nombres à 1 024 bits. Au pas 100, les deux trajectoires calculées valent 0,673899 et 0,002785, des nombres qui dépendent déjà de l'arrondi : à partir des mêmes départs, les trajectoires à 1 024 bits donnent 0,991939 et 0,735222. Pourtant, sur 100 000 pas, la première trajectoire calculée passe 33 353 pas sous 0,25 et la seconde 33 525, face à une proportion connue de 1/3. Les statistiques de l'attracteur restent prévisibles quand l'état ne l'est plus : c'est, à l'échelle du modèle, l'affirmation de PSY-002 sur les agrégats.

### Exercice pratique 5

Une prévision à r = 4 doit rester à moins de 0,1 à chacun de ses 60 pas. Option A : mesurer le départ une seule fois, à 1e-12 près au lieu de 1e-6. Option B : garder 1e-6 et mesurer à nouveau tous les k pas. Sur 1 000 prévisions de ce type, 972 restent dans la tolérance sur l'ensemble des 60 pas pour k = 10, 960 pour 11, 924 pour 12 et 284 pour 16. Quelle option garde au moins 95 % des prévisions à 60 pas dans la tolérance, et avec quel k au plus ?

> **Réponse :** A échoue : l'horizon donné par la formule à 1e-12 est de 36,54 pas, et le plus long des 1 000 horizons mesurés est de 49. B fonctionne jusqu'à k = 11, soit 6 mesures : `960 / 1,000 = 96.0%`, contre 92,4 % pour k = 12. Choisir k = 16, l'horizon de la formule (16,61) arrondi à l'entier inférieur, n'en garde que 28,4 % : un horizon suit une distribution, ici de 9 à 24 pas autour d'une moyenne de 16,78. Le critère, c'est le bas de cette distribution, et le remède consiste à mesurer à nouveau, non à mesurer mieux.

**Analogie, et non mesure.** Une feuille de route est une prévision à longue échéance faite à partir d'un présent connu approximativement. Si le processus qui la sous-tend amplifie les petites différences, connaître plus en détail la situation d'aujourd'hui n'apporte qu'un allongement fixe et faible ; ce qui aide, c'est de mesurer à nouveau et de prévoir des distributions. S'il les amortit, les prévisions à longue échéance coûtent peu. Personne n'a mesuré d'exposant de Lyapunov pour ce projet : cette leçon ne peut pas dire quel cas s'applique.

**L'objection la plus forte** est que l'application logistique n'est qu'un nombre soumis à une règle fixe. Un projet a de nombreuses variables, des personnes qui réagissent aux prévisions, et des chocs extérieurs ; avec des chocs, les erreurs croissent même à partir d'un départ parfaitement connu, et cette formule de l'horizon n'a plus de raison de tenir. Une série du projet évaluée dans [PSY-005](psy-005-persistence-baseline.fr.md) ne tranche pas la question : « rien ne change » avait raison pour 1 528 des 1 529 paires de lignes consécutives (inégalement espacées), ce qui montre des étiquettes qui changent rarement, ou un enregistrement que personne ne révise, et non la façon dont croissent les erreurs de prévision. **Ce jeu d'essai ne permet pas de départager un projet chaotique, un projet bruité et un projet stable.** Des prévisions datées d'une grandeur du projet, évaluées selon leur échéance, pourraient commencer à le faire : une erreur qui croît exponentiellement puis se stabilise indique un exposant positif ; une erreur qui reste constante, un régime stable ; une erreur présente dès le premier pas et qui croît sans phase exponentielle, un régime bruité.

## Sources, limites et prochaine vérification

**Épinglés au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** PSY-001, PSY-002 et MAT-024. Le jeu d'essai reproduit les quatre exposants que MAT-024 affiche pour ces valeurs de r ; le décompte des paires de lignes de la section 4 est celui de PSY-005.

**Jeu d'essai.** Depuis la racine du dépôt, `python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py`, puis la même commande avec `--check`. Le script ne lit que `scenarios.json` et exécute 41 autocontrôles ; son [README](../../../fixtures/psychohistory/psy-014/README.md) explique pourquoi la sortie est identique octet pour octet d'une plateforme à l'autre et en énumère les limites.

**Références de méthode.** May, R. M. (1976), « Simple mathematical models with very complicated dynamics », *Nature* 261, 459–467. Lorenz, E. N. (1963), « Deterministic nonperiodic flow », *Journal of the Atmospheric Sciences* 20, 130–141 (sensibilité aux conditions initiales). Strogatz, S. H. (2015), *Nonlinear Dynamics and Chaos*, 2e édition, Westview Press (exposants de Lyapunov et horizon temporel d'une prévision).

**Non fait.** Aucune donnée du projet n'a été analysée et aucun exposant n'a été estimé pour une quelconque grandeur du projet. Une seule application, à une variable, sans bruit et avec une seule graine, a été étudiée. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Archiver à chaque exécution une prévision datée d'une grandeur du projet, comme le nombre de modules de [PSY-010](psy-010-growth-curves-short-series.fr.md), et tracer l'erreur en fonction de l'échéance une fois qu'assez de prévisions ont pu être vérifiées. Une croissance exponentielle suivie d'un plateau serait un premier indice d'exposant positif, pas encore une estimation ; une courbe plate dirait que ce n'est pas l'horizon qui limite le plan.
