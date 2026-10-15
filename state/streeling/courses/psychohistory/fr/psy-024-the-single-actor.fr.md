---
module_id: psy-024-the-single-actor
department: psychohistory
course: "L'acteur unique : quand un seul expéditeur forme tout l'ensemble"
level: intermediate
prerequisites: ["psy-004-how-large-is-large", "psy-009-concentration-and-heavy-tails"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-024
version: "0.1.0"
---

# L'acteur unique : quand un seul expéditeur forme tout l'ensemble

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous compterez les acteurs que nomme un relevé, vous mesurerez la concentration de leur activité, vous bornerez cette mesure quand une partie du relevé est perdue, et vous direz ce que le résultat établit sur la question de savoir qui a agi. **Question de projet :** les lois portant sur un agrégat supposent de nombreux acteurs indépendants. Qui a réellement produit les événements enregistrés ?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) lit le comportement agrégé de l'écosystème comme obéissant à des lois statistiques ; [PSY-004](psy-004-how-large-is-large.fr.md) montre à combien peu d'agents indépendants équivalent quatorze agents corrélés. Ce module pose une question préalable : combien d'acteurs les relevés contiennent-ils ? [PSY-009](psy-009-concentration-and-heavy-tails.fr.md) mesure la concentration du même journal entre les jours ; celui-ci, entre les acteurs.

## 1. Un seul expéditeur, et ce que veut dire « sender »

**Observé.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/extract.py) lit les 594 fichiers de [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) au commit `4b03838` et remplace chaque identité par une étiquette avant d'écrire [`observed-input.json`](../../../fixtures/psychohistory/psy-024/observed-input.json). Les **594** événements archivés, du 2026-03-20 au 2026-07-16, portent tous le même `sender`, étiqueté *compte A* (*account A* dans le jeu d'essai), et le même `repo`. C'est aussi le cas de 8 événements plus tardifs restés dans le dossier parent : 602 événements dont l'expéditeur est lisible, un seul compte.

Le [fichier de workflow au commit épinglé](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L75), version postérieure de celui qui a écrit ces fichiers (les versions antérieures n'ont pas été lues), donne à `sender` la valeur `github.actor`, que GitHub [définit](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts) comme « The username of the user that triggered the initial workflow run » (le nom de l'utilisateur qui a déclenché l'exécution initiale du workflow), et à `repo` le nom du dépôt dans lequel il s'exécute. Par conséquent :

- `repo` ne peut pas varier : l'enregistreur a été installé dans un seul dépôt. « Un seul dépôt » dit où se trouvait l'instrument, non que les autres dépôts étaient silencieux.
- `sender` désigne un *compte*, c'est-à-dire les identifiants de connexion sous lesquels un push, un ticket ou une discussion est parvenu à la plateforme. Le fichier des propriétaires du code (*code owners*) nomme un seul mainteneur, seul propriétaire désigné dans ses 7 lignes de règles ; `extract.py` confirme qu'il s'agit du compte A.
- Un compte n'est ni une personne ni un agent. [`AGENTS.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/AGENTS.md) définit une équipe de 5 rôles d'agents, et pourtant aucune des 9 clés d'un événement ne nomme un rôle, un persona, une session ou un modèle : tout ce qui agit au moyen des identifiants du mainteneur est enregistré comme compte A.

« Un seul acteur » est donc un énoncé sur le pouvoir de résolution du relevé : il distingue des comptes, et il n'en a trouvé qu'un.

Pour mesurer la concentration, attribuez à chacun des k acteurs sa *part* s des événements :

```text
H = s_1² + s_2² + … + s_k²    indice de concentration : 1/k pour k acteurs égaux, 1 pour un seul
N = 1 / H                      nombre effectif d'acteurs : nombre d'acteurs égaux qui donnent ce H
```

H est la somme des carrés des parts (l'indice de Simpson ; les économistes l'appellent indice de Herfindahl–Hirschman). Pour l'archive, H = 1 et N = 1.

**L'archive est un ensemble de survivants. Calculé** à partir des commits et des arbres : 615 événements déclencheurs ont été ajoutés au total (plus un fichier de planification), 603 subsistent au commit épinglé, **12** ont été supprimés sans être archivés. Le `sender` d'un fichier se trouve dans son contenu, que ce clone ne peut pas lire. L'historique montre seulement que des commits faits sous l'identité du workflow en ont ajouté 11, avec des sujets qui nomment un type d'événement et le même dépôt (sur les 602 événements survivants, sujet et fichier concordent), et que le douzième, un déclencheur `self_initiated` et non un événement du dépôt, a été ajouté, sous la chaîne de l'auteur A, par un autre commit dont le sujet annonce le premier cycle autonome du pilote. On peut borner leurs expéditeurs, non les connaître.

### Exercice pratique 1

Prenez le pire cas pour « un seul expéditeur » : chacun des 12 fichiers supprimés provient d'un compte différent, aucun n'étant le compte A. Calculez H et N pour les 606 événements. Supposez ensuite que les 12 proviennent tous d'un même autre compte.

> **Réponse :** Douze nouveaux expéditeurs : `H = (594² + 12 × 1²) / 606² = 352,848 / 367,236 = 0.960821` et `N = 1.0408`. Un seul nouvel expéditeur : `H = (594² + 12²) / 606² = 352,980 / 367,236 = 0.961180` et `N = 1.0404`. Le compte A conserve au moins `594 / 606 = 98.02%`. Toute répartition donne un N compris entre 1 et 1,0408 : un nouvel expéditeur par fichier est ce qui ajoute le moins à la somme des carrés des effectifs, tout attribuer au plus grand compte ce qui ajoute le plus. Ces expéditeurs sont des hypothèses : la perte ne peut pas transformer un seul expéditeur en un ensemble.

## 2. Une échelle pour N

**Synthétique.** [`scenarios.json`](../../../fixtures/psychohistory/psy-024/scenarios.json) définit des ensembles imaginaires de 14 acteurs, l'effectif annoncé dans le principe clé du département ; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-024/analyze.py) calcule :

| Ensemble imaginaire | H | N | Nombre de demi-couverture | Dispersion relative |
|---|---|---|---|---|
| 14 acteurs égaux | 0,071429 | 14 | 8 | 0,2673 |
| 14 acteurs, celui de rang r a 1/r des événements du premier | 0,149063 | 6,7086 | 3 | 0,3861 |
| 14 acteurs, chacun avec la moitié des événements du précédent | 0,333374 | 2,9996 | 1 | 0,5774 |
| 14 acteurs, l'un en détient 90 % | 0,810769 | 1,2334 | 1 | 0,9004 |
| 1 acteur | 1 | 1 | 1 | 1 |

Le *nombre de demi-couverture* est le plus petit nombre d'acteurs qui détiennent ensemble plus de la moitié des événements : un cousin, fondé sur des décomptes, du « bus factor » (*truck factor*, le plus petit nombre de développeurs dont le départ mettrait un projet en difficulté), qu'Avelino et ses collègues estiment à partir des auteurs de chaque fichier.

Si N importe pour une loi statistique, c'est à cause de ce que fait la moyenne. Supposons qu'un agrégat fasse la moyenne sur les événements, chaque acteur y pesant selon sa part, et que les acteurs se comportent indépendamment, avec la même variabilité :

```text
variance de l'agrégat = H × variance d'un acteur
dispersion relative   = sqrt(H) = 1 / sqrt(N)
```

L'agrégat fluctue comme une moyenne de N acteurs égaux. La loi des grands nombres demande un N grand ; à N = 1, l'« agrégat » est l'acteur lui-même et rien n'est moyenné. Une simulation à graine fixée de 20 000 répétitions par ensemble renvoie N = 14,08 ; 6,72 ; 2,98 ; 1,24 et 1,00 pour les cinq lignes.

### Exercice pratique 2

Un journal de 100 événements compte trois acteurs, qui en ont 50, 30 et 20. Calculez H, N, le nombre de demi-couverture et la dispersion relative.

> **Réponse :** `H = 0.5² + 0.3² + 0.2² = 0.38` et `N = 1 / 0.38 = 2.6316`. Le plus grand acteur détient exactement la moitié, ce qui n'est pas plus de la moitié : le nombre de demi-couverture est donc 2. Dispersion relative : `sqrt(0.38) = 0.6164`, soit environ 62 % de celle d'un seul acteur si les trois sont indépendants.

### Exercice pratique 3

Classez chaque énoncé comme observé, calculé, synthétique ou non étayé, en donnant la raison : (a) les 594 événements archivés portent tous un même expéditeur ; (b) en comptant les fichiers supprimés, N vaut au plus 1,0408 ; (c) 14 acteurs égaux donnent une dispersion relative de 0,2673 ; (d) une seule personne a produit tous les événements.

> **Réponse :** (a) Observé : un décompte sur les fichiers épinglés. (b) Calculé, à partir d'un décompte observé et d'une hypothèse de pire cas. (c) Synthétique : cela vaut pour des acteurs imaginaires et indépendants. (d) Non étayé : `sender` désigne le compte qui a déclenché une exécution ; aucun champ n'enregistre la personne, la session ou l'agent qui se trouve derrière.

## 3. Un second relevé : les auteurs des commits

**Observé**, avec des commandes git qui ne lisent que les commits et les arbres : 1 599 commits mènent au commit épinglé, sous **2** chaînes d'auteur, *auteur A* avec 860 commits et *auteur B* avec 739 (*author A* et *author B* dans le jeu d'essai). **Calculé :**

| Relevé | Une identité est | Identités | Plus grande part | H | N |
|---|---|---|---|---|---|
| Archive des déclencheurs | le `sender` | 1 | 100 % | 1 | 1 |
| Archive plus les 12 fichiers supprimés, chacun d'un nouvel expéditeur (hypothèse) | le `sender` | 13 | 98,02 % | 0,960821 | 1,0408 |
| Commits | la chaîne d'auteur | 2 | 53,78 % | 0,502863 | 1,9886 |
| Commits | l'adresse de l'auteur | 3 | 46,22 % | 0,387065 | 2,5835 |
| Commits, sans les 613 qui portent le sujet du workflow de déclenchement | la chaîne d'auteur | 2 | 87,22 % | 0,777082 | 1,2869 |

N = 1,99 dit « deux acteurs de même poids ». Quatre propriétés du relevé disent autre chose ; chacune est une limite de l'instrument, non un jugement sur le travail de quiconque.

- **Un auteur est une chaîne configurée.** L'auteur B est le nom que [quatre workflows définissent avant de créer leurs commits](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L85). 613 de ses 739 commits portent le sujet du workflow de déclenchement, un par fichier déclencheur. Sans eux, 860 contre 126 donnent N = 1,2869 (une lecture choisie après avoir vu les décomptes).
- **Un contributeur, plusieurs identifiants.** L'auteur A crée ses commits sous deux adresses (622 et 238). Git enregistre qui a écrit une modification (l'auteur) et qui l'a enregistrée (le *committer*, ou validateur) : une chaîne de validateur qui n'est jamais auteur, avec une adresse *no-reply* sur le domaine de la plateforme d'hébergement, a créé 215 des 238, ce qui est compatible avec des commits faits sur la plateforme. Compter les adresses donne trois « auteurs » et N = 2,5835 ; le `.mailmap` du dépôt, qui associe des adresses à des identités, réunit les deux.
- **Un identifiant, plusieurs contributeurs.** 615 des 860 commits de l'auteur A (71,51 %) portent une mention finale `Co-authored-by` (un [*trailer*](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)) : 620 lignes, dont 610 avec une adresse *no-reply* sur un même domaine, 4 avec un nom qui se termine par `[bot]` et 4 qui nomment le compte A lui-même. Les décomptes par auteur ignorent ces mentions.
- **L'écrasement des commits (*squash*).** 279 sujets se terminent par un numéro de pull request (9 sont des commits de fusion, non des écrasements), et cette chaîne de validateur a créé 228 de ces commits. Une fusion par écrasement (*squash merge*) [combine tous les commits d'une pull request en un seul commit](https://docs.github.com/en/pull-requests/reference/pull-request-merges), qui n'a qu'un champ d'auteur.

### Exercice pratique 4

Calculez H et N pour les auteurs des commits (860 et 739), puis sans les 613 commits qui portent le sujet du workflow de déclenchement. Lequel est le bon nombre ?

> **Réponse :** `H = (860² + 739²) / 1,599² = 1,285,721 / 2,556,801 = 0.502863` et `N = 1.9886`. Sans les 613, l'auteur B garde `739 − 613 = 126` : `H = (860² + 126²) / 986² = 755,476 / 972,196 = 0.777082` et `N = 1.2869`. Ni l'un ni l'autre n'est « le » nombre : N mesure des étiquettes selon une règle de décompte. Donnez la règle avec le nombre, et fixez-la avant de regarder.

## 4. Ce qu'étaye un ensemble d'un seul acteur

Chaque événement dont l'expéditeur est lisible a été déclenché au moyen d'un seul compte, dans un seul dépôt ; les commits relèvent d'une chaîne d'auteur principale et d'une identité de workflow. Ces relevés décrivent le rythme de travail d'un compte. Les rafales de [PSY-008](psy-008-bursts-are-not-rates.fr.md) et la concentration de PSY-009 sont des propriétés de ce rythme, non des lois portant sur une population d'agents : aucune population n'est enregistrée.

**L'objection la plus forte à cette lecture** est que l'instrument rendait l'uniformité probable : `sender` enregistre qui a déclenché une exécution, dans un seul dépôt, pour trois types d'événements. Une personne travaillant seule produirait ce relevé ; de nombreuses sessions d'agents agissant avec les identifiants du mainteneur aussi. Le workflow a poussé 613 commits sous l'auteur B, et pourtant 214 déclencheurs `push` seulement ont été écrits en tout : si chaque exécution lancée par un push en a laissé un dans l'historique, au moins 399 de ces push n'en ont lancé aucune. Le commit [`eb230fb`](https://github.com/GuitarAlchemist/Demerzel/commit/eb230fb8d66c48b39a0b01eac99a738791f59e9f) a ensuite fait passer ses push « to master over a write deploy key, not GITHUB_TOKEN » (vers master par une clé de déploiement en écriture, et non par le GITHUB_TOKEN) ; les push faits avec ce jeton ne lancent aucune exécution, comme le [documente](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) GitHub. **Ce journal ne permet pas de distinguer un seul acteur de nombreux agents derrière un même compte.** Les mentions finales de la section 3 laissent entrevoir la seconde possibilité sans permettre de compter ces agents ; lire les 12 fichiers supprimés trancherait seulement la question de l'existence d'un second compte.

Des données qui décriraient de nombreux acteurs indépendants : sur chaque événement, un identifiant de l'agent ou de la session qui agit, écrit par l'outil qui agit et non déduit des identifiants de connexion ; des événements venant de chaque dépôt ; un nombre effectif nettement supérieur à 1 (ce sont les parts qui comptent, non le nombre de têtes) ; et des preuves d'indépendance (PSY-004). De la littérature, pas une preuve : dans *Foundation and Empire* d'Asimov, le plan est dévié de sa trajectoire quand un individu, le Mulet, échappe à la statistique ; ici, le relevé ne contient aucune foule dont un individu pourrait se démarquer.

### Exercice pratique 5

Un nouveau journal marque chaque événement d'un identifiant de persona : 1 400 événements, un persona en compte 1 010 et treize en comptent 30 chacun. Le critère a été fixé à l'avance : pour parler d'un agrégat d'« environ 14 acteurs », N doit valoir au moins 10. (a) Décidez. (b) Décidez de nouveau si les treize doublent leur production. (c) Que resterait-il à montrer si N satisfaisait un jour le critère ?

> **Réponse :** (a) `H = (1,010² + 13 × 30²) / 1,400² = 1,031,800 / 1,960,000 = 0.526429` et `N = 1.8996` : non. (b) `H = (1,010² + 13 × 60²) / 1,790² = 1,066,900 / 3,204,100 = 0.332980` et `N = 3.0032` : toujours non ; quatorze personas égaux donneraient 14. (c) Qu'un identifiant de persona marque un décideur distinct, et non une étiquette posée sur un seul modèle lisant un seul contexte, et que les décisions des personas ne sont pas fortement corrélées (PSY-004). Le journal est imaginaire.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers dont les liens ou les noms figurent plus haut, et les 1 599 commits qui mènent au commit épinglé. `extract.py` s'arrête si une valeur épinglée diffère.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-024/extract.py`, puis `analyze.py` ; `--check` compare une nouvelle exécution à [`results.json`](../../../fixtures/psychohistory/psy-024/results.json). Le [README](../../../fixtures/psychohistory/psy-024/README.md) donne la règle d'étiquetage, les commandes git et les vérifications.

**Références de méthode.** Simpson, E. H. (1949), « Measurement of Diversity », *Nature* 163, 688 (la somme des carrés des parts). Laakso, M., et Taagepera, R. (1979), « 'Effective' Number of Parties: A Measure with Application to West Europe », *Comparative Political Studies* 12(1), 3–27 (N = 1/H). Avelino, G., Passos, L., Hora, A., et Valente, M. T. (2016), « A Novel Approach for Estimating Truck Factors », *24th IEEE International Conference on Program Comprehension*, 1–10.

**Non fait.** Aucun fichier supprimé n'a été lu. Aucun expéditeur ni aucune chaîne d'auteur n'a été rapproché d'une personne, et les deux relevés n'ont pas été croisés : un nom d'utilisateur de la plateforme et une chaîne d'auteur sont des identifiants différents. Les noms des mentions finales ont été comptés, ni classés ni authentifiés. Aucun autre dépôt n'a été lu, aucune décision d'agent n'a été observée, et aucun *truck factor* n'a été estimé. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Dans un clone complet, lire le `sender` des 12 fichiers supprimés : un autre compte parmi eux changerait « un seul expéditeur » en « N au plus égal à 1,0408 », et rien d'autre. La conclusion ne changerait qu'avec un relevé qui identifie l'agent agissant sur chaque événement : on pourrait alors calculer N sur les agents.
