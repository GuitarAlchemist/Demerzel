---
module_id: psy-021-conservation-claims
department: psychohistory
course: "Des énoncés de conservation que l'on peut vérifier"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-021
version: "0.1.0"
---

# Des énoncés de conservation que l'on peut vérifier

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous rangerez en quatre catégories des énoncés que l'on qualifie de « conservation », vous contrôlerez une identité stock-flux sur un véritable journal d'événements, et vous nommerez l'enregistrement sans lequel un énoncé ne peut pas être mis en défaut. **Question de projet :** PSY-001 emprunte le théorème de Noether pour son « learning momentum » (la dynamique d'apprentissage). Quels énoncés de conservation portant sur ce projet peut-on réellement vérifier ?

[PSY-001](psy-001-intro-fractal-compounding.fr.md) annonce une loi de conservation pour la gouvernance. Ce module demande ce qu'exige une telle loi, puis contrôle ce que le dépôt offre de plus proche : la comptabilité de son journal des déclenchements. [PSY-008](psy-008-bursts-are-not-rates.fr.md) et [PSY-009](psy-009-concentration-and-heavy-tails.fr.md) lisent ce journal comme une suite d'arrivées, [PSY-024](psy-024-the-single-actor.fr.md) demande qui les a envoyées, et [PSY-003](psy-003-review-throughput-and-compounding.fr.md) applique des identités semblables à des files d'attente de revue.

## 1. Quatre choses que l'on appelle conservation

En physique, une loi de conservation dit qu'un nombre calculé à partir de l'état d'un système isolé garde sa valeur pendant que cet état change : l'énergie, la quantité de mouvement, la charge électrique. Le théorème de Noether (1918) est l'une des sources de telles lois. Il porte sur un système dont les mouvements rendent stationnaire une *action*, l'action étant un nombre calculé à partir de toute une trajectoire du système. Si une famille continue de transformations (décaler chaque instant d'une même quantité, quelle qu'elle soit) laisse l'action inchangée, le théorème construit une grandeur qui reste constante le long de tout mouvement : l'énergie pour les translations dans le temps, la quantité de mouvement pour les translations dans l'espace. Personne ne choisit cette grandeur ; elle est dérivée.

**Observé.** [La section 5 de PSY-001](psy-001-intro-fractal-compounding.fr.md#5-conservation-de-la-dynamique-dapprentissage) énonce le théorème sous la forme « every continuous symmetry of a system has a corresponding conserved quantity » (toute symétrie continue d'un système possède une quantité conservée correspondante) et l'applique : « In fractal compounding, the symmetry is **scale invariance** — the compound operation has the same shape at every level. The conserved quantity is **learning momentum (p_L)** » (dans la capitalisation fractale, la symétrie est l'invariance d'échelle, l'opération de capitalisation ayant la même forme à chaque niveau ; la quantité conservée est la dynamique d'apprentissage, p_L), avec

```text
p_L = (beliefs_gained_T - beliefs_lost_T) / cycles_elapsed
```

et « If your compounding process is consistent (symmetric across scales), p_L stays constant or grows. If you break the symmetry — by skipping compounding at some level, or by compounding differently at different scales — p_L decays. » (si votre processus de capitalisation est cohérent, c'est-à-dire symétrique à toutes les échelles, p_L reste constant ou croît ; si vous brisez la symétrie, en sautant la capitalisation à un niveau ou en capitalisant différemment selon les échelles, p_L décroît).

**C'est une analogie.** Son intuition se défend : un processus mené de la même façon à chaque niveau devrait continuer à produire des croyances validées. Mais les conditions du théorème ne sont pas remplies (c'est la lecture de l'auteur, consignée dans [`scenarios.json`](../../../fixtures/psychohistory/psy-021/scenarios.json)). Aucune action n'est écrite pour les cycles de gouvernance. La symétrie relie cinq niveaux nommés (étape, pipeline, cycle, session, évolution) : c'est une correspondance discrète, non une famille continue. Et p_L est défini par une formule et peut croître, ce qu'une grandeur conservée ne peut pas faire.

Un projet a bien des énoncés de conservation qu'il peut vérifier : les identités comptables d'un *stock*, la quantité de quelque chose présente à un instant donné (Meadows 2008).

```text
stock actuel = tout ce qui est entré - tout ce qui est sorti
```

Ce que vaut un tel énoncé dépend d'une seule question : les enregistrements auraient-ils pu le rendre faux ? Ce module utilise quatre étiquettes :

- **par construction** : vrai quoi que disent les enregistrements, par l'arithmétique ou par la façon dont ses deux membres sont obtenus (souvent tous deux à partir des mêmes enregistrements) ; il ne dit rien du système ;
- **vérifiable** : les enregistrements auraient pu le rendre faux, souvent parce que ses deux membres ont été écrits séparément ;
- **non enregistré** : l'une des grandeurs n'a jamais été consignée ;
- **analogie** : le vocabulaire d'une loi, sans ses conditions.

## 2. Ce que les fichiers épinglés permettent d'équilibrer

**Observé.** Un *déclencheur* est un petit fichier JSON qu'un [workflow GitHub](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) écrivait dans `state/triggers/` à chaque push, à chaque ticket (*issue*) ouvert et à chaque discussion créée, pour qu'un agent autonome, le pilote (*driver*), le consomme. Tous deux ont été retirés le 2026-07-18 ; le fichier lié en est une version ultérieure. Les tickets rouverts et les exécutions de CI en échec, que ce workflow traite aussi, n'apparaissent jamais dans l'historique. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/extract.py) prend un instantané [du dossier](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) au commit `4b03838` dans [`observed-input.json`](../../../fixtures/psychohistory/psy-021/observed-input.json) : 603 fichiers d'événements.

| Type | En attente | Archivés | Total |
|---|---|---|---|
| discussion_created | 5 | 252 | 257 |
| issue_opened | 3 | 135 | 138 |
| push | 0 | 207 | 207 |
| research_followup | 1 | 0 | 1 |
| Total | 9 | 594 | 603 |

« En attente » signifie que le fichier est encore dans `state/triggers/` lui-même ; « archivé », qu'il est dans son sous-dossier `archived/` ; le troisième dossier, `processing/`, est vide. Sur les 603 fichiers, 602 partagent une même forme : six clés (`type`, `repo`, `ref`, `priority`, `details`, `timestamp`), avec `event`, `sender` et `run_id` (l'identifiant unique de l'exécution du workflow) dans `details`. Aucune clé n'enregistre un instant d'archivage, une étape de traitement ni un résultat : un déclencheur traité et un déclencheur abandonné se ressemblent en tout point.

**Calculé** à partir de ces seuls fichiers par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-021/analyze.py) dans [`results.json`](../../../fixtures/psychohistory/psy-021/results.json) :

- *Par construction :* les totaux par type ont pour somme 603 : un même décompte, découpé puis additionné à nouveau.
- *Vérifiable, et confirmé :* 603 noms de fichiers, tous distincts, si bien qu'aucun fichier ne se trouve dans deux dossiers ; 602 identifiants d'exécution, tous distincts ; et le fichier du workflow comme le fichier de compétence du pilote font état de 594 déclencheurs orphelins, soit exactement le contenu de l'archive.
- *Non enregistré :* les dossiers suggèrent un circuit fermé, `created = archived + pending + in processing`, mais rien, au commit épinglé, ne compte ce qui a été créé : l'identité n'a pas de membre de gauche. La [règle du pilote lui-même](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md#L331) dit pourquoi : « On WAKE: move triggers to `state/triggers/processing/` before reading, delete after processing. » (au réveil, déplacer les déclencheurs dans le dossier de traitement avant de les lire, et les supprimer une fois traités). La sortie prévue ne laisse aucun fichier.

### Exercice pratique 1

À partir du tableau, calculez le nombre de fichiers d'événements par dossier et par type. Trouvez ensuite, dans cette section, la somme qui aurait pu contredire un nombre écrit indépendamment des fichiers.

> **Réponse :** Par dossier, `9 + 0 + 594 = 603` ; par type, `257 + 138 + 207 + 1 = 603`. Ces deux sommes ne peuvent pas se contredire : chacune additionne à nouveau un même décompte. La colonne de l'archive, elle, le pourrait : `252 + 135 + 207 = 594` est compté à partir des fichiers, et 594 figure aussi dans deux documents. Les deux concordent.

### Exercice pratique 2

Attribuez à chaque énoncé l'une des quatre étiquettes : (a) « aucun identifiant d'exécution n'apparaît dans deux fichiers » ; (b) « chaque déclencheur archivé a été traité » ; (c) « les nombres par type ont pour somme le nombre de fichiers » ; (d) « la dynamique d'apprentissage est conservée ».

> **Réponse :** (a) Vérifiable : un fichier copié aurait répété un identifiant ; l'énoncé tient, avec 602 identifiants distincts sur 602. (b) Non enregistré : aucune clé n'enregistre le traitement. (c) Par construction. (d) Analogie : les conditions du théorème font défaut.

## 3. L'historique fournit le membre manquant, et l'identité échoue

**Observé, à partir de l'historique.** `extract.py` lit aussi l'historique Git du commit épinglé : le long de la *chaîne des premiers parents* (les états successifs de la branche principale : 1 528 commits, dont 623 touchent le dossier), il relève chaque ajout et chaque suppression d'un fichier déclencheur.

| Dossier | Ajoutés | Supprimés | Ajoutés − supprimés | Sur le disque |
|---|---|---|---|---|
| en attente | 615 | 606 | 9 | 9 |
| en traitement | 5 | 5 | 0 | 0 |
| archivés | 594 | 0 | 594 | 594 |

Ainsi, 615 fichiers déclencheurs ont été créés, et l'identité fermée a un membre de gauche. **Elle échoue :** 615 contre 594 + 9 + 0 = 603. Douze fichiers, soit 1,95 % des fichiers créés, ne se trouvent dans aucun dossier :

- 2 supprimés du dossier en attente par `c5cca0c` et `49a573c`, chacun retirant un « trigger file with invalid Windows filename » (fichier déclencheur dont le nom est invalide sous Windows) ;
- 5 supprimés de `processing/` par `2b752a7`, « Driver cycle 002 complete — 9 tasks, all repos healthy » ;
- 5 supprimés du dossier en attente par `a2c1ef0`, « docs(seldon): Markov + state-space model architecture and schemas (#605) ».

Les cinq fichiers supprimés de `processing/` ont pris la sortie prévue : le commit qui les y avait déplacés dit « consume 5 triggers », et aucun autre déclencheur n'y a jamais été déplacé ; les sept autres sont sortis par d'autres portes. Et « 594 orphelins » est la taille de l'archive, non le nombre de déclencheurs que personne n'a consommés : 615 − 5 = 610 n'ont jamais été consommés (dont 609 écrits par le producteur) : 594 archivés, 9 en attente et 7 retirés.

Avec un terme de *retraits*, les comptes bouclent : 615 = 603 + 12, chaque dossier s'équilibre et, nom par nom, les 603 fichiers sont là où l'historique les laisse. **Ce bouclage est vrai par construction.** Git stocke des instantanés et calcule les ajouts et les suppressions en comparant des instantanés consécutifs ; additionner les différences redonne le dernier instantané, c'est-à-dire les fichiers. Le bouclage montre que l'historique a été lu en entier (un témoin négatif qui efface un enregistrement de suppression décale les comptes d'une unité), et il ne dit rien des déclencheurs. Deux résultats auraient pu être autres : les 12, et la concordance entre 613 titres de commit annonçant un déclencheur et les fichiers ajoutés par ces commits, un fichier du type annoncé pour chacun. Le titre et le type du fichier viennent tous deux d'une même variable d'une même étape du workflow : cela montre seulement que chaque exécution a intégré son propre fichier dans un commit. Les deux autres fichiers sont arrivés, l'un avec un commit rapportant le premier cycle autonome du pilote, l'autre avec un commit de recherche.

### Exercice pratique 3

Rendez compte des 606 suppressions du dossier en attente. Calculez ensuite l'écart du système fermé et la part des fichiers créés que contient l'archive.

> **Réponse :** `5` déplacés vers `processing/`, `594` déplacés vers `archived/` et `2 + 5 = 7` supprimés purement et simplement : `5 + 594 + 7 = 606`. Écart : `615 − 603 = 12`. Part de l'archive : `594 / 615 = 96.59%`.

**Synthétique.** Là où un registre et des rayonnages sont comptés séparément, comme dans un entrepôt, c'est l'équilibre lui-même qui peut être pris en défaut. `scenarios.json` contient cinq cas écrits à la main, de huit événements imaginaires chacun, aux réponses fixées d'avance :

| Cas | Créés − listés | Idem, moins les retraits enregistrés | Dossiers déséquilibrés | Éléments mal placés |
|---|---|---|---|---|
| sans erreur | 0 | 0 | 0 | 0 |
| retrait enregistré | 1 | 0 | 0 | 0 |
| perte non enregistrée | 1 | 1 | 1 | 1 |
| copie non enregistrée | −1 | −1 | 1 | 1 |
| perte et copie à la fois | 0 | 0 | 0 | 2 |

### Exercice pratique 4

Un tableau de bord n'affiche que les trois premières colonnes, et toutes indiquent 0. Quels cas cela laisse-t-il ouverts, et quel contrôle permet de les séparer ?

> **Réponse :** Deux : le cas sans erreur, et une perte et une copie qui se compensent. Seule la comparaison nom par nom les sépare : dans le dernier cas, un événement attendu dans l'archive y manque, et un autre figure dans deux dossiers. Des comptes équilibrés montrent l'erreur nette, non le nombre d'erreurs.

## 4. Faire de l'analogie un énoncé qui peut échouer

**Observé.** La [politique qui définit p_L](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/compounding-metrics-policy.yaml#L124-L131) indique où cette grandeur est suivie : « state/driver/health-scores.json trend fields » (les champs de tendance de ce fichier). Au commit épinglé, [ce fichier](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/health-scores.json) contient, pour chacun de quatre dépôts, un score composite, une date et une tendance exprimée en un mot : 0 valeur de p_L, et aucun décompte de croyances. La même politique lit p_L de trois façons : constant, « symmetry preserved » (symétrie préservée) ; croissant, « healthy compounding » (capitalisation saine) ; décroissant, « symmetry broken; investigate root cause » (symétrie brisée ; en rechercher la cause profonde).

Un énoncé ne dit quelque chose que par les issues qu'il interdit (Popper 1959). D'un cycle à l'autre, p_L peut baisser, rester stable ou monter. La conservation stricte interdit deux de ces trois issues. La première phrase de PSY-001 en interdit une, une baisse alors que le processus est cohérent, à condition que la cohérence soit enregistrée sans regarder p_L ; sa seconde phrase en interdit une autre, l'absence de décroissance après une rupture enregistrée. La lecture en trois cas n'en interdit aucune : une baisse y est elle-même prise comme le signe que la symétrie a été brisée.

### Exercice pratique 5

Synthétique. Six cycles imaginaires ont gagné 6, 7, 5, 4, 6, 6 croyances validées et en ont perdu 1, 2, 2, 3, 1, 1. Un journal distinct indique que la phase de capitalisation a tourné aux cinq niveaux à chaque cycle, sauf au quatrième. Calculez p_L par cycle (cycles_elapsed = 1) et mettez à l'épreuve les trois versions.

> **Réponse :** p_L = 5, 5, 3, 1, 5, 5. *Conservation :* p_L change sur 3 des 5 pas : réfutée. *Première phrase de PSY-001 :* 3 pas relient deux cycles cohérents (de 1 à 2, de 2 à 3, de 5 à 6) et p_L baisse sur l'un d'eux, de 2 à 3 : réfutée. *Lecture en trois cas :* les pas reçoivent les étiquettes stable, en baisse, en baisse, en hausse, stable ; rien ne la contredit, et aucune série ne le pourrait. La série est inventée ; l'enregistrement qui rend l'énoncé testable est un journal de cohérence tenu à part de p_L.

**L'objection la plus forte à la lecture que fait cette leçon** est que son membre de gauche ne mesure pas non plus la production. « Créé » signifie « entré dans un commit » : au commit épinglé, le workflow [écrit un fichier, puis fait un pull et un push](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml#L82-L90), et une exécution dont le push a échoué n'a rien laissé dans le dépôt. Les 615 et les 12 sont des bornes inférieures. **Cet historique ne permet pas de distinguer un workflow qui n'a jamais perdu d'événement d'un workflow qui en a perdu avant qu'ils n'entrent dans un commit.** La liste des exécutions du workflow tenue par GitHub trancherait.

## Sources, limites et prochaine vérification

**Observé** au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel : `state/triggers/` (contrôlé par l'identifiant de son arbre Git), son historique Git et les cinq fichiers dont les liens figurent plus haut.

**Jeu d'essai.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-021/extract.py`, puis `analyze.py` dans le même dossier ; `analyze.py --check` compare une nouvelle exécution aux résultats enregistrés. Le [README](../../../fixtures/psychohistory/psy-021/README.md) donne un recomptage sans les scripts.

**Références de méthode.** Noether, E. (1918), « Invariante Variationsprobleme », *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257 ([EuDML](https://eudml.org/doc/59024)) ; traduction anglaise de M. A. Tavel, *Transport Theory and Statistical Physics* 1(3), 1971, doi:10.1080/00411457108231446. Meadows, D. H. (2008), *Thinking in Systems: A Primer*, Chelsea Green. Popper, K. (1959), *The Logic of Scientific Discovery*, Hutchinson. Chacon, S., et Straub, B. (2014), *Pro Git*, 2e édition, Apress, [« What is Git? »](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F).

**Non fait.** Le contenu des douze fichiers supprimés n'a pas été lu : leurs types et leurs dates viennent de leurs noms, les raisons de leur suppression des titres de commit. Ni la liste des exécutions du workflow ni ses versions antérieures n'ont été lues. Aucune valeur de p_L n'a été calculée à partir des données du projet : le fichier désigné pour la contenir n'en contient aucune, et aucune autre source n'a été cherchée. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Sur GitHub, compter les exécutions du workflow qui ont écrit un déclencheur et les comparer aux 613 commits du producteur. Plus d'exécutions que de commits signifierait que des événements ont été perdus avant d'être comptés ; l'égalité, que les 12 suppressions constituent toute la perte.
