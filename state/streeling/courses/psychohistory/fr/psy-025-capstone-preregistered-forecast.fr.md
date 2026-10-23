---
module_id: psy-025-capstone-preregistered-forecast
department: psychohistory
course: "Projet de synthèse : une prévision préenregistrée que l'on peut noter"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "psy-016-brier-score", "psy-017-calibration-with-six-observations"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-025
version: "0.1.0"
---

# Projet de synthèse : une prévision préenregistrée que l'on peut noter

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous rédigerez une prévision sous la forme d'une fiche qu'un tiers peut résoudre, vous la confronterez à des règles portant sur ses champs, vous tirerez son taux de base de données épinglées, et vous la noterez pour chaque issue avant qu'aucune ne se soit produite. **Question de projet :** pouvons-nous rédiger sur Streeling une prévision qu'un tiers pourra noter plus tard sans nous demander ce que nous voulions dire ?

Ce projet de synthèse reprend [PSY-005](psy-005-persistence-baseline.fr.md) pour la référence qu'une prévision doit battre, [PSY-016](psy-016-brier-score.fr.md) pour le score de Brier et [PSY-017](psy-017-calibration-with-six-observations.fr.md) pour les intervalles exacts sur de petits effectifs.

## 1. Une fiche, pas une conjecture

Le *préenregistrement* est, pour Nosek et ses collègues (2018), « committing to analytic steps without advance knowledge of the research outcomes » (le fait de s'engager sur les étapes de l'analyse sans connaître à l'avance les résultats de la recherche), habituellement déposé dans un registre indépendant qui « preserves the preregistration and makes it discoverable » (conserve le préenregistrement et permet de le retrouver). Il « does not favor prediction over postdiction; its purpose is to make clear which is which » (ne privilégie pas la prédiction sur la postdiction ; son but est de rendre clair ce qui relève de l'une ou de l'autre). Une fiche de prévision fixe, avant l'issue, tout ce qu'il faut pour noter une prévision.

[`scenarios.json`](../../../fixtures/psychohistory/psy-025/scenarios.json) contient quatre fiches. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/analyze.py) confronte chacune d'elles à 22 règles portant sur les champs, énumérées avec leurs messages d'échec dans le [README](../../../fixtures/psychohistory/psy-025/README.md) du jeu d'essai. Elles répondent aux questions d'un tiers :

| Ce que demande un tiers | Champs (règles) |
|---|---|
| Que prévoit-on, exactement ? | `question` (R02), `kind` (R03), `forecast` (R15) |
| Où et quand dois-je regarder ? | `resolution_source` (R04–R06), `resolution_time` (R07, R08) |
| Qu'est-ce qui compte ? | `resolution_rule` : ce qui compte, à quelle fréquence, ce qui ne compte pas (R09) ; si la source a changé de place (R10) ; quand la prévision est caduque (R11) |
| Par rapport à quoi ? | `reference_class`, `base_rate` avec une commande et un commit (R12–R14), `reference_forecast` (R16) |
| Qu'est-ce qui la contredirait ? | `adjustment` (R17), `falsifier` (R18, R19) |
| Qui l'a écrite, qui d'autre décide, et quand ? | `author_can_influence_outcome` (R20) et sa note, `written_at` et ce qui l'atteste (R21, R22) |

**Synthétique.** Le brouillon `library-growth-draft` dit « Streeling will keep growing fast next quarter » (Streeling continuera de croître vite au prochain trimestre), avec pour source « the repo » (le dépôt) et pour prévision « likely » (probable). **Calculé :** le validateur le rejette sur 16 des 22 règles (R02, R04–R07, R09–R16, R18, R20, R22) et ne peut pas juger R08, R17 et R19, dont les champs sont inexploitables. L'un de ces échecs est d'une autre nature : ce lot de modules enrichit la bibliothèque, si bien que l'auteur du brouillon pourrait faire en sorte que sa prévision se réalise, et une issue que son auteur peut orienter est un plan à surveiller, non une prévision à noter. R20 ne juge que l'auteur de la fiche ; les mainteneurs qui fusionneraient les fiches fusionnent aussi les modules de tous les départements, ce que déclare `author_influence_note`. La version réparée, `library-growth-repaired`, porte sur la bibliothèque hors Psychohistoire et passe la validation, comme les deux fiches d'exemple de la section 3.

Le validateur vérifie la forme et la cohérence entre les champs, non la clarté. Six copies modifiées des fiches d'exemple échouent chacune exactement sur la règle enfreinte ; une septième, dont la prévision est égale à sa référence, passe ([`results.json`](../../../fixtures/psychohistory/psy-025/results.json), `validation.controls`).

### Exercice pratique 1

Deux lecteurs traduisent le « likely » du brouillon, l'un par 0,6, l'autre par 0,8. Donnez le score de Brier de chaque lecture si l'événement se produit et s'il ne se produit pas. Qu'est-ce que cela dit de la notation d'un mot ?

> **Réponse :** 0,6 : `(0.6 − 1)² = 0.16` s'il se produit, `0.6² = 0.36` sinon. 0,8 : `0.04` et `0.64`. Une même issue reçoit deux scores selon le lecteur ; le score mesurerait donc le lecteur, non le prévisionniste : R15 exige un nombre.

## 2. Un taux de base tiré de l'historique épinglé

**Observé.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/extract.py) lit les 73 commits qui ont modifié [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses) jusqu'au commit `4b03838`, ainsi que les 255 fichiers du dossier à ce commit, chacun comparé à son blob épinglé ([`observed-input.json`](../../../fixtures/psychohistory/psy-025/observed-input.json)). Un *module* anglais est un fichier `<department>/en/<name>.md` autre qu'un README : 68 au commit épinglé, répartis dans 18 départements. Musique en compte 19, Psychohistoire 2.

Les prévisions d'exemple portent sur le département Musique, auquel ce lot ne touche pas : une prévision portant sur Psychohistoire mesurerait le plan même de ce lot.

Une *classe de référence* est l'ensemble des cas passés auxquels on compare une prévision ; son *taux de base* est la part des cas dans lesquels l'événement s'est produit. Ici, un cas est un département sur une fenêtre de 92 jours, l'horizon des prévisions, et l'événement est « son nombre de modules a augmenté ». Deux fenêtres consécutives se terminent au commit épinglé et se situent toutes deux après le premier commit de module, daté du 2026-03-21. **Calculé :**

| Classe de référence | Hausses / cas | Taux de base | Intervalle exact à 95 % (PSY-017) |
|---|---|---|---|
| Départements comptant un module au début de la fenêtre | 2 / 36 | 0,055556 | 0,0068 à 0,1866 |
| Musique seule | 1 / 2 | 0,5 | 0,0126 à 0,9874 |

Les deux hausses sont celles de Mathématiques (de 1 à 25 modules) et de Musique (de 6 à 19), toutes deux dans la fenêtre qui se termine au commit épinglé.

L'avertissement de [PSY-010](psy-010-growth-curves-short-series.fr.md) s'applique : le décompte avance par rafales, si bien que le taux de base dépend de l'endroit où tombent les fenêtres. Reculer les deux fenêtres d'un jour à la fois (`base_rate.alignment`) donne pour la classe large un taux allant de 0,055556 à 0,151515 (5 sur 33, avec un recul de 21 jours), et pour Musique de 0 à 2 hausses. Déclarer l'alignement rend le nombre reproductible, non précis.

### Exercice pratique 2

Le tableau ne donne pas la classe large sans Musique. Calculez son taux. Dites ensuite quelle valeur se trouve dans l'intervalle exact de l'autre classe, et ce qui en découle pour le choix d'une classe.

> **Réponse :** Sans Musique, qui compte 1 hausse en 2 fenêtres, `(2 − 1) / (36 − 2) = 1 / 34 = 0.029412` : retirer un seul département divise presque le taux par deux. Le taux large, 0,055556, se trouve dans l'intervalle de Musique (0,0126 à 0,9874) ; 0,5 se trouve hors de celui de la classe large (0,0068 à 0,1866), mais seulement parce que cette classe traite Musique comme les départements calmes. Les données ne peuvent pas choisir la classe : la fiche doit en nommer une et justifier tout écart par rapport à son taux.

## 3. La prévision d'exemple et sa règle de résolution

**Synthétique : un exercice de rédaction d'une prévision, qui n'engage pas le département et n'est pas une prédiction qu'il fait sienne.** Deux fiches partagent une source, une règle et une date :

- `music-rise-2027-01-13` : « Will the Streeling course library hold more than 19 distinct Music modules at 2027-01-13T23:59:59Z? » Prévision de référence : 0,055556, le taux de base large ; valeur inscrite dans la fiche : **0,7**.
- `music-count-2027-01-13` : le même décompte, sous la forme de l'intervalle **[19, 25]** avec α = 0,2, contre l'intervalle [19, 19] de la persistance (PSY-005) : dans 34 des 36 cas, le décompte n'a pas bougé. Avec une probabilité de 0,3 sur la valeur 19 (le quantile d'ordre 0,1 selon l'auteur) et au moins six chances sur sept d'obtenir 25 ou moins après une hausse (25 est donc égal ou supérieur au quantile d'ordre 0,9), la probabilité de couverture selon l'auteur est d'au moins `0.3 + 0.7 × 6/7 = 0.9` : ce n'est un intervalle à 80 % que par son niveau déclaré.

Le champ `adjustment` dit pourquoi 0,7 s'écarte de 0,055556 : Musique a augmenté dans la dernière fenêtre, son module le plus récent est daté du jour du commit épinglé, et le taux propre à Musique est trop incertain pour fixer un nombre ; 0,7 est donc un jugement. Un tiers peut contester cette phrase ; le reste est mécanique.

*Source :* `GuitarAlchemist/Demerzel`, lu après l'instant de résolution, au dernier commit de premier parent de `master` (ou de la branche par défaut renommée) dont la date de validation (*committer date*) est antérieure ou égale à cet instant ; la fiche donne les commandes. *Ce qui compte :* les identifiants distincts de modules de Musique dans des fichiers `.md`. L'identifiant d'un fichier est le `module_id` de son en-tête (*front matter*), à défaut son nom de fichier sans `.md` ni suffixe de langue ; son département est celui de l'en-tête, à défaut celui de son dossier (en sautant les dossiers de langue) ; les README, les pages d'index et les copies publiées sont exclus. *En cas de déplacement :* si `master` désigne un autre endroit comme la source de la bibliothèque ou une partie de celle-ci (README, fichier de renvoi, message de commit), appliquer aussi la règle à cet endroit, que ce dossier existe encore ou non ; un identifiant réparti entre plusieurs endroits compte une seule fois. *Caducité :* aucune bibliothèque trouvée ; `4b03838` n'est pas un ancêtre du commit de résolution ; aucun horodatage obtenu au plus tard à l'instant de résolution ; ou un décompte de Musique différent de 19 à un commit de premier parent de `master` postérieur à `4b03838` dont la date de validation précède cet horodatage. Une prévision caduque est déclarée comme telle, et jamais notée 0.

**Calculé :** l'en-tête seul permet de trouver 67 modules, et non 68 : `cyb-003-measuring-variety-ratio-quantitatively.md` n'en a pas. Avec le repli sur le nom de fichier, la règle donne 68 et retrouve le décompte des chemins dans les 18 départements ; les 181 fichiers traduits portent l'identifiant de leur module anglais et n'ajoutent rien. Compter des identifiants, et non des chemins `en/`, permet à la règle de survivre à une organisation sans dossiers `en/`.

*Date de rédaction.* `written_at` (2026-10-14T13:39:06Z) ne repose que sur la parole de l'auteur : le fichier n'a pas été commité. Son horodatage sera le `mergedAt` de GitHub pour la première pull request qui fusionne son texte final dans `master`, ou l'enregistrement de son empreinte par un service d'horodatage, s'il est antérieur ; et non l'heure d'ouverture de la pull request (elle peut précéder le texte final), les heures de push (l'API des événements de GitHub ne les garde que 30 jours) ni les dates de commit (fixées sur la machine de celui qui commite). D'ici là, la fiche a la forme d'un préenregistrement, sans en être l'enregistrement.

### Exercice pratique 3

Appliquez la règle à cette liste de fichiers inventée, après un déplacement (chemin, `module_id` de l'en-tête, `department` ; `-` signifie absent). Combien de modules de Musique contient-elle ? Et si, à la date de notation, la bibliothèque a disparu et que rien ne désigne un nouvel emplacement ?

```text
music/index.md - -
music/mus-001-what-is-a-chord.md mus-001-what-is-a-chord music
music/mus-023-voice-leading.md - -
music/fr/mus-001-what-is-a-chord.fr.md mus-001-what-is-a-chord music
music/fr/mus-023-voice-leading.fr.md mus-023-voice-leading music
musicology/mcl-003-performance-practice.md mcl-003-performance-practice musicology
```

> **Réponse :** 2. `index.md` est exclu ; `mus-023-voice-leading` tire son identifiant de son nom de fichier et son département de son dossier ; les fichiers français répètent des identifiants déjà comptés ; `mcl-003` relève de Musicologie. Sans bibliothèque ni renvoi, la prévision est caduque : ni 0, ni « non ».

## 4. La noter avant que l'issue n'existe

Une fiche est terminée quand son score est connu pour chaque issue. **Calculé, sur des issues INVENTÉES**, avec la compétence de PSY-016, `1 − BS / BS_ref` (BS_ref : le score de Brier de la référence, exactement 0,055556, la valeur déclarée, à partir des scores non arrondis) :

| `music-rise` | Brier, prévision 0,7 | Brier, référence 0,055556 | Compétence |
|---|---|---|---|
| Issue 1 (plus de 19) | 0,09 | 0,891974 | 0,8991 |
| Issue 0 (19 ou moins) | 0,49 | 0,003086 | −157,75746 |

L'issue 0, la seule où 0,7 fait moins bien que le taux de base, est l'issue réfutante.

Le *score d'intervalle* d'un intervalle central de niveau (1 − α), [l, u], pour l'issue x est sa largeur `u − l`, plus `(2/α)(l − x)` si x < l, ou plus `(2/α)(x − u)` si x > u ; plus il est bas, mieux c'est. C'est la forme de Gneiting et Raftery (2007, éq. 43), qu'ils font remonter à des travaux antérieurs, dont Winkler (1972). Un *échec* est une issue située hors de l'intervalle. Ici α = 0,2, si bien que chaque module hors de l'intervalle coûte 10, qui s'ajoutent à la largeur, égale à 6.

| Décompte inventé | 18 | 19 | 21 | 25 | 28 |
|---|---|---|---|---|---|
| Couvert par [19, 25] | non | oui | oui | oui | non |
| Score d'intervalle | 16 | 6 | 6 | 6 | 36 |
| Persistance [19, 19] | 10 | 0 | 20 | 60 | 90 |

L'intervalle obtient un moins bon score que la persistance exactement pour les décomptes de 0 à 19 : c'est la même issue réfutante. La couverture ne s'évalue que sur de nombreux intervalles : dix intervalles de ce type, couvrant chacun avec la probabilité 0,9, couvrent sept fois ou moins avec la probabilité 0,070191.

### Exercice pratique 4

Recalculez le score d'intervalle de [19, 25] à α = 0,2, ainsi que celui de la persistance, pour les décomptes inventés 28 et 18. Lesquels sont des échecs, et où la persistance l'emporte-t-elle ?

> **Réponse :** 28 : `6 + 10 × (28 − 25) = 36` ; persistance `10 × 9 = 90`. 18 : `6 + 10 × (19 − 18) = 16` ; persistance `10 × 1 = 10`. Les deux sont des échecs. À 18, la persistance l'emporte, 10 contre 16 : l'intervalle a aussi payé sa largeur.

**L'objection la plus forte** : la fiche peut être notée, mais sa prévision est fragile. Le taux de base repose sur deux fenêtres et varie de 0,055556 à 0,151515 selon leur alignement ; son intervalle exact traite les 36 couples département-fenêtre comme indépendants, alors que les deux hausses tombent dans une même fenêtre et une même rafale, si bien qu'il sous-estime l'incertitude ; le 0,7 est un jugement ; et le décompte de Musique suit les décisions de fusion des mainteneurs, qu'une prévision publiée pourrait elle-même influencer. Un seul score ne dit presque rien de la compétence : 0,8991 ou −157,8 (arrondi). Une série de fiches de ce type, chacune horodatée avant son issue et notée par rapport à sa référence déclarée, trancherait la question.

### Exercice pratique 5

`library-growth-repaired` annonce 0,75 face à son taux de base, 1 hausse en 2 fenêtres. Calculez les deux scores de Brier et la compétence pour chaque issue, et nommez l'issue réfutante. Si le décompte dépasse 66 le 2027-01-13, le prévisionniste a-t-il fait preuve de compétence ?

> **Réponse :** Issue 1 : `(0.75 − 1)² = 0.0625` contre `(0.5 − 1)² = 0.25`, compétence `1 − 0.0625 / 0.25 = 0.75`. Issue 0 : `0.75² = 0.5625` contre `0.25`, compétence `1 − 0.5625 / 0.25 = −1.25`. Issue réfutante : 0. Non : une seule résolution favorable ne permet pas de distinguer un bon prévisionniste d'un prévisionniste chanceux.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** l'historique des commits et les 255 fichiers de la bibliothèque de cours dont le lien figure plus haut.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-025/extract.py`, puis `analyze.py` et `analyze.py --check`. Le README énumère les règles, les 22 autocontrôles et les témoins négatifs.

**Références de méthode.** Nosek, B. A., Ebersole, C. R., DeHaven, A. C., et Mellor, D. T. (2018), « The preregistration revolution », *PNAS* 115(11), 2600–2606, [doi:10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114). Gneiting, T., et Raftery, A. E. (2007), « Strictly Proper Scoring Rules, Prediction, and Estimation », *Journal of the American Statistical Association* 102(477), 359–378, section 6.2. Winkler, R. L. (1972), « A Decision-Theoretic Approach to Interval Estimation », *Journal of the American Statistical Association* 67(337), 187–191. Les intervalles exacts sont ceux de Clopper et Pearson (1934), cités dans PSY-017.

**Non fait.** Aucune fiche n'a été résolue ni horodatée, et toutes les issues notées sont inventées. La règle de décompte n'a été testée que sur la bibliothèque épinglée, non sur des contenus de fichiers plus anciens ni sur des copies publiées. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Après 2027-01-13T23:59:59Z, résoudre les deux fiches d'exemple selon leur propre règle ou les déclarer caduques, et les noter par rapport à leurs références. Plus tôt : un changement du décompte de Musique avant leur horodatage les rend caduques, ce qui montrerait à quelle vitesse une prévision portant sur un dossier actif peut devenir caduque avant que quiconque l'enregistre.
