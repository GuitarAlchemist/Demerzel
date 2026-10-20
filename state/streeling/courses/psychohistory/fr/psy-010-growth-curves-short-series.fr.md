---
module_id: psy-010-growth-curves-short-series
department: psychohistory
course: "Exponentielle, logistique ou en paliers ? Ajuster une croissance à un historique court"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-010
version: "0.1.0"
---

# Exponentielle, logistique ou en paliers ? Ajuster une croissance à un historique court

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous transformerez un historique de commits en série quotidienne, vous y ajusterez trois courbes de croissance par les moindres carrés, vous lirez sur chacune la date à laquelle une cible est atteinte, et vous vérifierez si les données permettent de les distinguer. **Question de projet :** les modules de cours en anglais ont été ajoutés par rafales. Que prédit chacun des ajustements exponentiel, logistique et linéaire du nombre cumulé de modules quant à la date où il atteint 525, et l'historique permet-il de les distinguer ?

[PSY-001](psy-001-intro-fractal-compounding.fr.md) assimile une croissance saine à des intérêts composés. Si la bibliothèque croissait par capitalisation, le nombre de ses modules suivrait une exponentielle ; ici, ce n'est qu'une loi candidate parmi trois. [PSY-022](psy-022-competing-explanations.fr.md) compare des modèles au moyen de critères de vraisemblance, [PSY-018](psy-018-backtesting-without-leakage.fr.md) teste des prévisions sur des données mises de côté, et [PSY-023](psy-023-monitoring-a-plan.fr.md) surveille un plan dès qu'un calendrier existe.

## 1. Transformer l'historique en série

**Observé.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/extract.py) demande à git lesquels des 1 599 commits accessibles depuis le commit `4b03838` ont modifié le dossier [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses) : 73 commits, du 2026-03-21 au 2026-10-13. Il écrit [`observed-input.json`](../../../fixtures/psychohistory/psy-010/observed-input.json) à partir des seules dates de commit et des seuls noms de fichiers. Un *module* est un chemin `DEPARTMENT/en/NAME.md`. Ne sont pas comptés les traductions (181 fichiers au commit épinglé), les fichiers README (4, plus 2 à l'intérieur de dossiers `en/`) ni les 10 noms de fichiers d'une ancienne organisation sans dossiers de langue. Au total, les commits ajoutent 73 chemins de modules et en retirent 5 (un renommage compte comme un retrait suivi d'un ajout) : **68** modules au commit épinglé, dans 18 des 21 dossiers de département.

**Supposé.** Le plan du cursus prévoit 21 départements de 25 cours chacun, soit 21 × 25 = **525**, chiffre tiré d'un projet de spécification et pris tel quel, bien que le dépôt recense 23 départements, dont deux sans dossier de cours. 68 représente 13,0 % de 525.

Chaque commit est daté par sa date de commit (*committer date*) en UTC ; les commits qui partagent la même seconde gardent leur ordre de filiation. La série est le nombre de modules à la fin de chaque jour UTC, le jour 0 étant le 2026-03-21 : 207 jours. **Calculé :** ce nombre change lors de 12 d'entre eux.

```text
jour    0   1   2   3  15  190  191  195  196  197  200  206
nombre 13  17  19  23  31   32   37   60   63   66   67   68
```

Appelons ces 12 jours des jours *actifs*, et appelons *rafale* une suite de jours actifs séparés d'au plus 7 jours (une convention, enregistrée dans [`scenarios.json`](../../../fixtures/psychohistory/psy-010/scenarios.json) ; [PSY-008](psy-008-bursts-are-not-rates.fr.md) appelle un tel groupe un *épisode*) :

| Rafale | Jours | Modules ajoutés | Part des 68 |
|---|---|---|---|
| Du 21 au 24 mars | 4 | 23 | 33,8 % |
| 5 avril | 1 | 8 | 11,8 % |
| Du 27 septembre au 13 octobre, encore ouverte | 17 | 37 | 54,4 % |

La troisième rafale est encore ouverte : le commit épinglé a lui-même ajouté un module, si bien qu'avec la règle des 7 jours ses 37 modules et ses 17 jours sont des bornes inférieures, et les modules du lot de cette leçon la prolongeront s'ils sont fusionnés au plus tard le 2026-10-20. Pendant 174 jours, du 6 avril au 26 septembre, le nombre de modules est resté à 31. Une règle de 3 jours donne 5 rafales, une règle de 12 jours en donne 2 : la « rafale » est un choix. L'horloge aussi : cinq autres fuseaux horaires donnent de 10 à 13 jours actifs, toujours répartis en trois rafales.

### Exercice pratique 1

Quelle part des 68 modules est arrivée lors de la dernière rafale, et en quelle part des 207 jours ? Pendant combien de jours le nombre de modules n'a-t-il pas changé ?

> **Réponse :** `37 / 68 = 54.4%` des modules en `17 / 207 = 8.2%` des jours. `207 − 12 = 195` jours sans changement, soit 94,2 %. Plus de la moitié de la croissance se concentre dans les 17 derniers jours : toute courbe ajustée ici dépend fortement d'un seul événement récent.

## 2. Ajuster trois lois de croissance

Trois lois candidates pour le nombre N de modules au jour t :

```text
droite        N = a + b t                      le même nombre de modules chaque jour
exponentielle N = a exp(b t)                   ajouts proportionnels au nombre : capitalisation
logistique    N = K / (1 + exp(-r (t - m)))    capitalisation qui ralentit quand N approche d'un plafond K

ajustement    b = (n ΣtN - Σt ΣN) / (n Σt² - (Σt)²)      sommes sur les n jours
de la droite  a = (ΣN - b Σt) / n
```

Les *moindres carrés* retiennent les paramètres qui minimisent la SSE (*sum of squared errors*, somme des carrés des résidus), somme sur les 207 jours de (observé − ajusté)². La RMSE, racine carrée de SSE / 207, est l'erreur typique, exprimée en modules. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-010/analyze.py) résout la droite exactement à partir de ces sommes et trouve les deux courbes par une recherche déterministe (une grille, puis des itérations de Newton). Le plafond de la logistique, sa capacité limite, est fixé à K = 525, et m est le jour où la courbe passe K / 2. Une courbe logistique ne fait que s'approcher de son plafond ; « atteint 525 » désigne donc, pour chaque courbe, le premier jour où sa valeur vaut au moins 524,5.

**Calculé** ([`results.json`](../../../fixtures/psychohistory/psy-010/results.json), `fits.pinned_date`) :

| Courbe | Paramètres (t en jours) | SSE | RMSE | Valeur au jour 206 | Atteint 525 | Années après le commit épinglé |
|---|---|---|---|---|---|---|
| Droite | a = 24,5641 ; b = 0,0767431 | 11 462,4 | 7,441 | 40,37 | 2044-01-21 | 17,3 |
| Exponentielle | a = 24,6004 ; b = 0,00257104 | 11 100,5 | 7,323 | 41,78 | 2029-06-24 | 2,7 |
| Logistique | r = 0,00272281 ; m = 1 106,31 | 11 130,8 | 7,333 | 41,65 | 2036-03-29 | 9,5 |

Les trois dates s'étalent sur 14,6 ans. Chaque courbe place entre 40 et 42 modules à une date où le dépôt en comptait 68.

### Exercice pratique 2

À partir des paramètres, calculez le jour où la droite et l'exponentielle atteignent 524,5, puis le nombre d'années écoulées après le commit épinglé (jour 206 ; 365,25 jours par an).

> **Réponse :** Droite : `(524.5 − 24.5641) / 0.0767431 = 6,514.4`, donc le jour 6 515, soit `6,515 − 206 = 6,309` jours ou 17,3 ans après le commit épinglé. Exponentielle : `ln(524.5 / 24.6004) / 0.00257104 = 1,190.1`, donc le jour 1 191 : 985 jours, 2,7 ans.

### Exercice pratique 3

Combien de temps après son point milieu m la logistique atteint-elle 524,5 ? Que dit ce résultat de la question de savoir quand nous atteindrons 525 ?

> **Réponse :** N = 524,5 quand `exp(−r (t − m)) = 0.5 / 524.5`, donc `t − m = ln(1,049) / r = 6.95559 / 0.00272281 = 2,554.6` jours, soit 7,0 ans. La courbe passe 262,5 au jour 1 107, soit 2,5 ans après le commit épinglé, et il lui faut encore 7,0 ans pour la seconde moitié. Elle n'est jamais égale à 525 : sous cette loi, la question n'a de réponse qu'avec une convention telle que la marge d'un demi-module.

## 3. L'historique permet-il de les distinguer ?

Quatre vérifications **calculées**.

*Les sommes des carrés des résidus sont presque égales.* La plus grande SSE vaut 1,033 fois la plus petite.

*Les trois courbes se trompent de la même façon.* Un *résidu* est la valeur observée moins la valeur ajustée. Sur les 207 jours, les résidus de chaque courbe changent de signe 3 fois, et la plus longue suite d'un même côté dure de 105 à 111 jours. Les moindres carrés fonctionnent au mieux quand les écarts forment un bruit indépendant : les résidus d'une droite **synthétique** à laquelle on ajoute un tel bruit, ajustée par une droite, changent de signe 107 fois. Ces résidus-ci ne sont pas du bruit : ils sont l'escalier.

*Dans l'échantillon, un escalier sans loi de croissance s'ajuste bien mieux.* Deux niveaux plats, 30,41 avant le 2 octobre et 65,92 à partir de ce jour, laissent une SSE de 1 564,1 : 7,1 fois moins que la meilleure courbe, avec 3 paramètres contre 2. Avec 11 points de rupture, la SSE vaut 0. Un escalier ne dit rien de la marche suivante. Comment mettre en balance la qualité de l'ajustement et le nombre de paramètres, c'est le sujet de PSY-022.

*Aucun plafond ne peut être estimé.* Avec K fixé successivement à 12 valeurs de 69 à 100 000, la SSE de la logistique diminue à chaque pas, de 11 469,8 à 11 100,7, vers les 11 100,5 de l'exponentielle. Un plafond d'un module au-dessus de l'effectif actuel et un plafond de 100 000 donnent des SSE qui ne diffèrent que de 3,3 % : K n'est pas *identifiable* à partir de ces données. La méthode n'est pas en cause : sur une logistique synthétique observée au-delà de son point d'inflexion, le même profil retrouve le plafond de 525 qu'on y a placé (SSE 8 751,7, contre 29 596,0 à 550) ; sur une logistique observée avant ce point, il reste plat à 0,4 % près. Cet historique n'a pas atteint d'inflexion, s'il y en a une.

### Exercice pratique 4

Un collègue écrit : « L'exponentielle a la plus petite SSE, donc la bibliothèque croît par capitalisation et nous atteindrons 525 en 2029. » Acceptez ou rejetez cette affirmation, et énoncez votre critère.

> **Réponse :** À rejeter : l'affirmation n'est pas étayée. Un classement ne compte que si l'écart entre les candidats est grand au regard de ce que tous laissent inexpliqué. Ici `11,462.4 / 11,100.5 = 1.033`, alors qu'un escalier à deux niveaux fait `11,100.5 / 1,564.1 = 7.1` fois mieux et que les trois courbes laissent les mêmes 3 changements de signe. Cet échantillon ne permet pas de distinguer les trois lois ; la capitalisation reste une candidate, pas un constat.

## 4. Déplacer la date de coupure, puis compter les rafales

Un ajustement qui aurait saisi la loi donnerait des dates qui cessent de bouger à mesure que l'historique s'allonge. **Calculé :** les mêmes ajustements sur l'historique arrêté à la fin de la deuxième rafale, à la veille de la troisième, et au commit épinglé.

| Historique jusqu'au | Jours | Modules | Droite | Exponentielle | Logistique |
|---|---|---|---|---|---|
| 5 avril | 16 | 31 | 2028-08-16 | 2026-08-02 | 2027-04-16 |
| 26 septembre | 190 | 31 | 2088-12-21 | 2037-10-26 | 2062-12-02 |
| 13 octobre | 207 | 68 | 2044-01-21 | 2029-06-24 | 2036-03-29 |

Entre les deux premières lignes, 174 jours calmes ont repoussé les dates de 60,3 ; 11,2 et 35,6 ans respectivement. La dernière rafale les a ensuite avancées de 44,9 ; 8,3 et 26,7 ans. Pour le 13 octobre, les ajustements d'avril prédisaient 136,68 ; 3 267,78 et 467,68 modules, ceux de septembre 32,68 ; 32,66 et 32,66 ; le nombre réel était de 68. Ici, une courbe ajustée à un escalier prolonge ce qu'elle a vu en dernier, une montée ou un palier.

D'autres choix défendables déplacent encore les dates : n'ajuster que les 12 jours actifs donne 2033-07-08, 2027-11-09 et 2030-12-15 ; une droite ajustée au logarithme des effectifs (la courbe de tendance exponentielle d'un tableur) donne 2030-04-27 ; dater un seul commit par sa date d'auteur (*author date*), 1,3 jour plus tôt, déplace de 81 jours la date de la droite.

**Synthétique.** Projeter la lecture en paliers exige de supposer que l'avenir répète le passé : il reste 457 modules, les rafales en ont ajouté 23, 8 et au moins 37, et leurs débuts sont séparés de 15 et de 175 jours.

### Exercice pratique 5

Sous cette hypothèse, combien de rafales faut-il et combien de temps prennent-elles (a) avec la taille moyenne et l'intervalle moyen, (b) avec la plus grande taille, au moins 37, et l'intervalle le plus court, (c) avec la plus petite taille et l'intervalle le plus long ?

> **Réponse :** (a) Taille moyenne `68 / 3 = 22.67` ; `457 / 22.67 = 20.16`, donc 21 rafales ; intervalle moyen `(15 + 175) / 2 = 95` jours ; `21 × 95 = 1,995` jours, soit 5,5 ans. (b) `457 / 37 = 12.35`, donc 13 rafales ; `13 × 15 = 195` jours, soit 0,5 an. (c) `457 / 8 = 57.125`, donc 58 rafales ; `58 × 175 = 10,150` jours, soit 27,8 ans. La rafale encore ouverte fait de (a) et (b) des bornes supérieures. Trois rafales donnent une fourchette de 0,5 à 27,8 ans : de l'arithmétique sur une hypothèse, pas une prévision.

**L'objection la plus forte à cette lecture** est que la compétition entre courbes passe à côté de l'essentiel. Le 2 octobre, le nombre de modules a augmenté de 23 en 23 commits d'un module chacun, dont 14 en moins de deux minutes : la signature d'un lot de production. Si les modules arrivent quand quelqu'un décide de lancer un lot, la série enregistre des décisions, pas une loi de croissance, et « ne permet pas de distinguer les courbes » est vrai mais n'apprend rien. Deux choses trancheraient : un calendrier de production écrit, qui transforme la date en un plan à surveiller (PSY-023) ; ou plusieurs rafales de plus selon la même règle des 7 jours, assez pour voir si le nombre de modules ajoutés par unité de temps croît avec l'effectif (des rafales plus grandes ou plus fréquentes : capitalisation), reste stable (linéaire) ou diminue (un plafond).

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** l'historique des commits de `state/streeling/courses` et les enregistrements des départements au commit épinglé (commits et arbres uniquement). `extract.py` refuse un clone superficiel (*shallow clone*) ou tout autre historique que celui qui est épinglé. 525 est le chiffre du plan.

**Jeu d'essai.** `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py`, puis `analyze.py` dans le même dossier ; `analyze.py --check` compare une nouvelle exécution aux résultats enregistrés. Le [README](../../../fixtures/psychohistory/psy-010/README.md) documente la méthode et ses vérifications.

**Références de méthode.** Bates, D. M., et Watts, D. G. (1988), *Nonlinear Regression Analysis and Its Applications*, Wiley (moindres carrés pour les courbes ; itérations de Gauss–Newton). Debecker, A., et Modis, T. (1994), « Determination of the uncertainties in S-curve logistic fits », *Technological Forecasting and Social Change* 46(2), 153–173 (l'incertitude d'un plafond ajusté avant que la courbe s'infléchisse). Meade, N., et Islam, T. (1995), « Forecasting with growth curves: An empirical comparison », *International Journal of Forecasting* 11(2), 199–215.

**Non fait.** Aucune date n'a reçu d'intervalle, et l'on n'a calculé ni vraisemblance, ni AIC, ni BIC (PSY-022). Le contenu des modules, leur qualité et leur statut de relecture n'ont pas été lus : un module, ici, est un nom de fichier. Tous les jours ont le même poids ; aucune autre pondération n'a été justifiée. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Relancer `extract.py` après avoir remplacé ses constantes épinglées par un commit plus récent, une fois qu'au moins cinq nouvelles rafales se seront refermées, avec la règle des 7 jours et les ajustements aux trois dates de coupure figés tels qu'ils sont aujourd'hui. Si les nouvelles rafales restent dans les plages observées (de 8 à au moins 37 modules, des débuts séparés de 15 à 175 jours), la lecture en paliers n'est pas contredite ; si le nombre de modules ajoutés par unité de temps augmente avec l'effectif, la capitalisation obtient son premier appui.
