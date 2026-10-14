---
module_id: psy-010-growth-curves-short-series
department: psychohistory
course: "Exponentielle, logistique ou escalier ? Ajuster une croissance à une histoire courte"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-010
version: "0.1.0"
---

# Exponentielle, logistique ou escalier ? Ajuster une croissance à une histoire courte

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un historique de commits en une série journalière, vous y ajusterez trois courbes de croissance par les moindres carrés, vous lirez sur chacune la date d'une cible, et vous éprouverez la capacité des données à les distinguer. **Question de projet :** les modules de cours en anglais ont été ajoutés par salves. Que prévoient respectivement un ajustement exponentiel, logistique et linéaire de l'effectif cumulé pour atteindre 525, et l'historique permet-il de les distinguer ?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) dépeint une croissance saine comme des intérêts composés. Si la bibliothèque capitalisait, son effectif serait exponentiel ; ici, c'est un candidat parmi trois. PSY-022 compare des modèles avec des critères de vraisemblance, PSY-018 éprouve des prévisions sur des données réservées, et PSY-023 surveille un plan dès qu'un calendrier existe.

## 1. Transformer l'historique en série

**Observé.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/extract.py) demande à git lesquels des 1 599 commits accessibles depuis le commit `4b03838` ont modifié le dossier [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses) : 73 commits, du 2026-03-21 au 2026-10-13. Il écrit [`observed-input.json`](../../../fixtures/psychohistory/psy-010/observed-input.json) à partir des seules dates de commit et des seuls noms de fichiers. Un *module* est un chemin `DEPARTMENT/en/NAME.md`. Les traductions (181 fichiers à l'épinglage), les fichiers README (4, et 2 de plus à l'intérieur de dossiers `en/`) et les 10 noms de fichiers d'une ancienne organisation sans dossiers de langue ne sont pas comptés. Ensemble, les commits ajoutent 73 chemins de module et en retirent 5 (un renommage compte pour un retrait et un ajout) : **68** modules à l'épinglage, dans 18 des 21 dossiers de département.

**Supposé.** Le plan de programme prévoit 21 départements de 25 cours chacun, 21 × 25 = **525**, le chiffre d'une spécification à l'état de brouillon, repris tel quel bien que le dépôt consigne 23 départements, dont deux sans dossier de cours. 68 représente 13,0 % de 525.

Chaque commit est daté par sa date de committer en UTC ; les commits qui partagent une seconde gardent leur ordre d'ascendance. La série est l'effectif à la fin de chaque jour UTC, le jour 0 étant le 2026-03-21 : 207 jours. **Calculé :** l'effectif change sur 12 d'entre eux.

```text
jour     0   1   2   3  15  190  191  195  196  197  200  206
nombre  13  17  19  23  31   32   37   60   63   66   67   68
```

Appelons ces 12 jours *actifs*, et appelons *salve* une suite de jours actifs séparés d'au plus 7 jours (une convention, consignée dans [`scenarios.json`](../../../fixtures/psychohistory/psy-010/scenarios.json) ; [PSY-008](psy-008-bursts-are-not-rates.fr.md) nomme *épisode* un tel groupe) :

| Salve | Jours | Modules ajoutés | Part des 68 |
|---|---|---|---|
| Du 21 au 24 mars | 4 | 23 | 33,8 % |
| 5 avril | 1 | 8 | 11,8 % |
| Du 27 septembre au 13 octobre, encore ouverte | 17 | 37 | 54,4 % |

La troisième salve est encore ouverte : l'épinglage lui-même a ajouté un module, de sorte que, sous la règle des 7 jours, ses 37 modules et ses 17 jours sont des bornes inférieures, et les modules du lot de cette leçon la prolongent s'ils sont fusionnés avant le 2026-10-20. Pendant 174 jours, du 6 avril au 26 septembre, l'effectif est resté à 31. Une règle de 3 jours donne 5 salves et une règle de 12 jours en donne 2 : « salve » est un choix. L'horloge aussi : cinq autres fuseaux horaires donnent de 10 à 13 jours actifs, toujours en trois salves.

### Exercice pratique 1

Quelle part des 68 modules est arrivée dans la dernière salve, et sur quelle part des 207 jours ? Sur combien de jours l'effectif n'a-t-il pas changé ?

> **Réponse :** `37 / 68 = 54.4%` des modules sur `17 / 207 = 8.2%` des jours. `207 − 12 = 195` jours sans changement, soit 94,2 %. Plus de la moitié de la croissance se tient dans les 17 derniers jours : toute courbe ajustée ici dépend fortement d'un seul événement récent.

## 2. Ajuster trois lois de croissance

Trois lois candidates pour l'effectif N au jour t :

```text
droite        N = a + b t                      le même nombre de modules chaque jour
exponentielle N = a exp(b t)                   ajouts proportionnels à l'effectif : capitalisation
logistique    N = K / (1 + exp(-r (t - m)))    capitalisation qui ralentit à l'approche d'un plafond K

ajust. droite b = (n ΣtN - Σt ΣN) / (n Σt² - (Σt)²)      sommes sur les n jours
              a = (ΣN - b Σt) / n
```

Les *moindres carrés* choisissent les paramètres qui minimisent la SSE, la somme sur les 207 jours de (observé − ajusté)². La RMSE, racine carrée de SSE / 207, est l'écart typique, en modules. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/analyze.py) résout la droite exactement à partir de ces sommes et trouve les deux courbes par une recherche déterministe (une grille, puis des pas de Newton). Le plafond logistique est fixé à K = 525, et m est le jour où la courbe passe K / 2. Une courbe logistique ne fait qu'approcher son plafond : « atteindre 525 » signifie donc, pour chaque courbe, le premier jour où sa valeur vaut au moins 524,5.

**Calculé** ([`results.json`](../../../fixtures/psychohistory/psy-010/results.json), `fits.pinned_date`) :

| Courbe | Paramètres (t en jours) | SSE | RMSE | Valeur au jour 206 | Atteint 525 | Années après l'épinglage |
|---|---|---|---|---|---|---|
| Droite | a = 24,5641, b = 0,0767431 | 11 462,4 | 7,441 | 40,37 | 2044-01-21 | 17,3 |
| Exponentielle | a = 24,6004, b = 0,00257104 | 11 100,5 | 7,323 | 41,78 | 2029-06-24 | 2,7 |
| Logistique | r = 0,00272281, m = 1 106,31 | 11 130,8 | 7,333 | 41,65 | 2036-03-29 | 9,5 |

Les trois dates s'étendent sur 14,6 ans. Chaque courbe place entre 40 et 42 modules un jour où le dépôt en contenait 68.

### Exercice pratique 2

À partir des paramètres, calculez le jour où la droite et l'exponentielle atteignent 524,5, puis le nombre d'années après l'épinglage (jour 206, 365,25 jours par an).

> **Réponse :** Droite : `(524.5 − 24.5641) / 0.0767431 = 6,514.4`, soit le jour 6 515, c'est-à-dire `6,515 − 206 = 6,309` jours ou 17,3 ans après l'épinglage. Exponentielle : `ln(524.5 / 24.6004) / 0.00257104 = 1,190.1`, soit le jour 1 191 : 985 jours, 2,7 ans.

### Exercice pratique 3

Combien de temps après son milieu m la logistique atteint-elle 524,5 ? Que dit le résultat sur la question « quand atteignons-nous 525 » ?

> **Réponse :** N = 524,5 quand `exp(−r (t − m)) = 0.5 / 524.5`, donc `t − m = ln(1,049) / r = 6.95559 / 0.00272281 = 2,554.6` jours, soit 7,0 ans. La courbe passe 262,5 au jour 1 107, 2,5 ans après l'épinglage, et met 7,0 ans de plus pour la seconde moitié. Elle n'égale jamais 525 : sous cette loi, la question n'a de réponse qu'avec une convention telle que la marge d'un demi-module.

## 3. L'historique permet-il de les distinguer ?

Quatre vérifications **calculées**.

*Les sommes de résidus sont presque égales.* La plus grande SSE vaut 1,033 fois la plus petite.

*Les trois courbes manquent de la même façon.* Un *résidu* est l'observé moins l'ajusté. Le long des 207 jours, les résidus de chaque courbe changent 3 fois de signe, et la plus longue série d'un même côté dure de 105 à 111 jours. Les moindres carrés sont à leur meilleur quand les écarts sont un bruit indépendant : une droite **synthétique** plus un tel bruit, ajustée par une droite, change 107 fois de signe. Ces résidus ne sont pas du bruit : ils sont l'escalier.

*Dans l'échantillon, un escalier sans aucune loi de croissance s'ajuste bien mieux.* Deux paliers plats, 30,41 avant le 2 octobre et 65,92 à partir de ce jour, laissent une SSE de 1 564,1 : 7,1 fois moins que la meilleure courbe, avec 3 paramètres contre 2. Avec 11 points de rupture, la SSE est nulle. Un escalier ne dit rien de la marche suivante. Comment peser l'ajustement face au nombre de paramètres est le sujet de PSY-022.

*Aucun plafond n'est estimable.* Avec K fixé à 12 valeurs de 69 à 100 000, la SSE de la logistique diminue à chaque pas, de 11 469,8 à 11 100,7, vers les 11 100,5 de l'exponentielle. Un plafond situé un module au-dessus de l'effectif actuel et un plafond de 100 000 diffèrent de 3,3 % : K n'est pas *identifiable* à partir de ces données. La méthode n'est pas en cause : sur une logistique synthétique vue après son coude, le même protocole retrouve le plafond planté de 525 (SSE 8 751,7, contre 29 596,0 à 550) ; vue avant son coude, elle est plate à 0,4 % près. Cet historique n'a pas atteint de coude, s'il en existe un.

### Exercice pratique 4

Un collègue écrit : « L'exponentielle a la plus faible SSE, donc la bibliothèque capitalise et nous atteignons 525 en 2029. » Acceptez ou rejetez, et énoncez votre critère.

> **Réponse :** Rejeter comme non soutenu. Un classement ne compte que si l'écart entre les candidats est grand au regard de ce qu'ils manquent tous. Ici, `11,462.4 / 11,100.5 = 1.033`, tandis qu'un escalier à deux paliers fait `11,100.5 / 1,564.1 = 7.1` fois mieux et que les trois courbes laissent les mêmes 3 changements de signe. Cet échantillon ne permet pas de distinguer les trois lois ; la capitalisation reste un candidat, non un résultat.

## 4. Déplacer la date de coupure, puis compter les salves

Un ajustement qui aurait saisi la loi donnerait des dates qui cessent de bouger à mesure que l'historique s'allonge. **Calculé :** les mêmes ajustements sur l'historique à la fin de la deuxième salve, à la veille de la troisième, et à l'épinglage.

| Historique jusqu'au | Jours | Effectif | Droite | Exponentielle | Logistique |
|---|---|---|---|---|---|
| 5 avril | 16 | 31 | 2028-08-16 | 2026-08-02 | 2027-04-16 |
| 26 septembre | 190 | 31 | 2088-12-21 | 2037-10-26 | 2062-12-02 |
| 13 octobre | 207 | 68 | 2044-01-21 | 2029-06-24 | 2036-03-29 |

Entre les deux premières lignes, 174 jours calmes ont repoussé les dates de 60,3, 11,2 et 35,6 ans. La dernière salve les a ensuite ramenées de 44,9, 8,3 et 26,7 ans. Pour le 13 octobre, les ajustements d'avril prévoyaient 136,68, 3 267,78 et 467,68 modules, ceux de septembre 32,68, 32,66 et 32,66 ; l'effectif était de 68. Ici, une courbe ajustée à un escalier extrapole ce qu'elle a vu en dernier, une contremarche ou un giron.

D'autres choix défendables déplacent encore les dates : n'ajuster que les 12 jours actifs donne 2033-07-08, 2027-11-09 et 2030-12-15 ; une droite ajustée au logarithme des effectifs (la courbe de tendance exponentielle d'un tableur) donne 2030-04-27 ; dater un commit par sa date d'auteur, 1,3 jour plus tôt, déplace la date de la droite de 81 jours.

**Synthétique.** Projeter la lecture en escalier exige de supposer que l'avenir répète le passé : il reste 457 modules, les salves en ont ajouté 23, 8 et au moins 37, et elles ont commencé à 15 et 175 jours d'intervalle.

### Exercice pratique 5

Sous cette hypothèse, combien de salves faut-il et combien de temps prennent-elles (a) avec la taille moyenne et l'intervalle moyen, (b) avec la plus grande taille, au moins 37, et l'intervalle le plus court, (c) avec la plus petite taille et l'intervalle le plus long ?

> **Réponse :** (a) Taille moyenne `68 / 3 = 22.67` ; `457 / 22.67 = 20.16`, donc 21 salves ; intervalle moyen `(15 + 175) / 2 = 95` jours ; `21 × 95 = 1,995` jours, soit 5,5 ans. (b) `457 / 37 = 12.35`, donc 13 salves ; `13 × 15 = 195` jours, soit 0,5 an. (c) `457 / 8 = 57.125`, donc 58 salves ; `58 × 175 = 10,150` jours, soit 27,8 ans. La salve ouverte fait de (a) et (b) des bornes supérieures. Trois salves donnent une étendue de 0,5 à 27,8 ans : de l'arithmétique sur une hypothèse, non une prévision.

**L'objection la plus forte à cette lecture** est que le concours entre les courbes est hors de propos. Le 2 octobre, l'effectif a augmenté de 23 en 23 commits d'un module chacun, dont 14 en moins de deux minutes : la signature d'un lot de production. Si les modules arrivent quand quelqu'un décide de lancer un lot, la série consigne des décisions, non une loi de croissance, et « on ne peut pas distinguer les courbes » est vrai et sans portée. Deux choses trancheraient : un calendrier de production écrit, qui fait de la date un plan à surveiller (PSY-023) ; ou plusieurs salves de plus sous la même règle des 7 jours, assez pour voir si les modules ajoutés par unité de temps croissent avec l'effectif (des salves plus grandes ou plus fréquentes : la capitalisation), restent stables (linéaire) ou diminuent (un plafond).

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** l'historique des commits de `state/streeling/courses` et les enregistrements de département à l'épinglage (commits et arbres seulement). `extract.py` refuse un clone superficiel et tout autre historique que celui épinglé. 525 est le chiffre du plan.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py`, puis `analyze.py` dans le même dossier ; `analyze.py --check` compare une exécution fraîche aux résultats enregistrés. Le [README](../../../fixtures/psychohistory/psy-010/README.md) documente la méthode et ses vérifications.

**Références de méthode.** Bates, D. M., et Watts, D. G. (1988), *Nonlinear Regression Analysis and Its Applications*, Wiley (les moindres carrés pour les courbes ; les pas de Gauss–Newton). Debecker, A., et Modis, T. (1994), « Determination of the uncertainties in S-curve logistic fits », *Technological Forecasting and Social Change* 46(2), 153–173 (le degré d'incertitude d'un plafond ajusté avant que la courbe ne tourne). Meade, N., et Islam, T. (1995), « Forecasting with growth curves: An empirical comparison », *International Journal of Forecasting* 11(2), 199–215.

**Non fait.** Aucun intervalle n'a été associé à une date, et aucune vraisemblance, aucun AIC ni BIC n'a été calculé (PSY-022). Le contenu, la qualité et l'état de relecture des modules n'ont pas été lus : ici, un module est un nom de fichier. Chaque jour pèse autant ; aucune autre pondération n'a été justifiée. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Relancer `extract.py` après avoir remplacé ses constantes épinglées par un épinglage plus tardif, une fois au moins cinq nouvelles salves refermées, avec la règle des 7 jours et les trois ajustements à date de coupure fixés tels qu'ils le sont aujourd'hui. Si les nouvelles salves restent dans les étendues observées (de 8 à au moins 37 modules, des débuts espacés de 15 à 175 jours), la lecture en escalier n'est pas contredite ; si les modules ajoutés par unité de temps augmentent avec l'effectif, la capitalisation gagne son premier soutien.
