---
module_id: psy-020-goodhart-and-reflexivity
department: psychohistory
course: "Quand la mesure devient la cible : les citations comme indicateur de substitution"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-011-measurement-change-or-system-change"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-020
version: "0.1.0"
---

# Quand la mesure devient la cible : les citations comme indicateur de substitution

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous lirez une règle de comptage et direz ce qu'elle ne peut pas voir, vous calculerez l'effet d'un seul fichier ajouté sur les nombres, vous établirez à quelles conditions le fait de récompenser un indicateur de substitution (*proxy*) le dégrade, et vous corrigerez une prévision qui déplace sa cible. **Question de projet :** la tendance de qualité compte les citations avec `git grep` ; qu'advient-il d'un tel indicateur une fois que les agents savent qu'il est surveillé ?

Un *indicateur de substitution* se mesure à la place d'une *cible* qui, elle, ne peut pas l'être. [PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) oppose le LOLLI, « artifact count without regard to quality » (le nombre d'artefacts, sans égard à leur qualité), à l'ERGOL, « real productive capacity » (la capacité productive réelle), et donne « Citations per artifact » (les citations par artefact) comme l'ERGOL à optimiser. [PSY-011](psy-011-measurement-change-or-system-change.fr.md) demande si l'instrument a changé ; ici, il est fixe, et la question devient ce que ceux qu'il mesure peuvent lui faire. Personne dans le projet n'a été observé en train de gonfler ce nombre : l'objet de la leçon est un mécanisme, et les conditions dans lesquelles il opère.

## 1. Ce que le décompte peut voir

**Observé.** Un *artefact* de gouvernance (une politique, une constitution, un schéma, une compétence) possède un enregistrement d'évolution qui énumère ses *chemins de citation*. Le *producteur*, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), [définit](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) `citation_count` comme les « tracked files that mention any of the artifact's citation paths (`git grep -lF`) » (les fichiers suivis qui mentionnent l'un des chemins de citation de l'artefact), moins les fichiers propres à l'artefact et [quatre emplacements exclus](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L43). [La recherche](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L80-L82) porte sur une chaîne littérale ; [le feeder](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L76) recopie le résultat dans la tendance de qualité quotidienne. Une « citation » est donc un fichier où un chemin apparaît sous forme de texte.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/extract.py) applique la règle aux 2 062 fichiers du commit `4b03838` et écrit [`observed-input.json`](../../../fixtures/psychohistory/psy-020/observed-input.json) : 18 enregistrements, 16 artefacts mesurables (deux sont [marqués comme se trouvant](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23) hors du dépôt), 19 chemins de citation distincts. **Calculé :** le recomptage est égal au nombre enregistré pour 16 artefacts sur 16. Par ordre décroissant, les nombres sont 65, 47, 45, 44, 29, 29, 23, 17, 15, 14, 13, 6, 6, 5, 1, 0 ; leur somme vaut 359, et ces citations proviennent de 200 fichiers.

La règle a deux angles morts.

- **La mention sans l'usage.** Sur les 200 fichiers comptés, 123 sont en Markdown et 9 sont des programmes Python, même si le type d'un fichier ne dit pas s'il utilise un artefact ou s'il le mentionne ; 92 nomment au moins deux artefacts. Neuf fichiers de cours, trois leçons en trois langues, apportent 12 des 359 citations comptées, dont 8 par des traductions.
- **L'usage sans la mention.** Un artefact a un nombre de 0, ce que son [enregistrement](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-04-30-the-sentinel.evolution.json) commente ainsi : « reads as 'nothing uses this spec' » (se lit comme « rien n'utilise cette spécification »), en ajoutant : « That is true only inside Demerzel: the metric cannot see sibling repositories. » (ce n'est vrai qu'à l'intérieur de Demerzel : la métrique ne voit pas les dépôts voisins).

Dans la tendance, 20 lignes ont un `delta_citations` non nul (énumérées dans [`results.json`](../../../fixtures/psychohistory/psy-020/results.json)) : 16 premiers nombres enregistrés et quatre hausses de 2 le 2026-10-03, pour `policies / alignment-policy.yaml`, `contracts / galactic-protocol.md` et les deux artefacts qui partagent un même chemin de politique. Une hausse dit que des fichiers ont bougé, non lesquels ni pourquoi : aucune cause n'est attribuée ici.

### Exercice pratique 1

Synthétique (`toy_rule` dans [`scenarios.json`](../../../fixtures/psychohistory/psy-020/scenarios.json)). Le seul chemin de citation d'un artefact est `toy/rule.yaml`. (a) `docs/index.md` mentionne ce chemin ; (b) `scripts/check.py` charge la règle avec `os.path.join("toy", "rule.yaml")` ; (c) le fichier de la règle nomme son propre chemin ; (d) `state/evolution/toy.json` et (e) `notes/archived/2025.md` le nomment ; (f) `data/labels.json` écrit `toy / rule.yaml` ; (g) une leçon et (h) sa traduction le nomment. Quel est le nombre de citations, et le fichier qui utilise la règle y est-il compté ?

> **Réponse :** Le nombre vaut 3 : les fichiers a, g et h. Le fichier c appartient à l'artefact lui-même ; d et e sont exclus ; b et f ne contiennent pas la chaîne littérale. Ainsi b, le seul fichier qui utilise la règle, n'est pas compté, tandis qu'une même leçon compte deux fois.

## 2. Un fichier, seize nombres

**Cas synthétiques, de type « et si », appliqués à des nombres observés.** Aucun de ces fichiers n'existe ; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/analyze.py) les ajoute aux nombres épinglés. Une *relation d'ordre* dit lequel de deux artefacts a le plus grand nombre ; 16 artefacts forment 120 paires.

| Fichier ajouté | Nombres augmentés | Somme | Relations d'ordre modifiées |
|---|---|---|---|
| Un catalogue des 19 chemins | 16, de 1 chacun | de 359 à 375 (+4,46 %) | 0 sur 120 |
| Un fichier qui nomme un seul chemin | 1 (2 pour le chemin partagé) | 359 + 1 (ou + 2) | au moins 1 pour 11 des 19 chemins |

Le catalogue ne modifie aucun ordre, puisqu'il ajoute la même quantité à chaque nombre ; placé dans un dossier exclu, ou écrit avec des étiquettes espacées, il n'augmente rien. Il déplace le niveau, et avec lui toute part et tout seuil calculés à partir de ce niveau : l'unique nombre égal à 0 devient 1. Un fichier ciblé ne déplace presque pas la somme et réordonne des voisins : pour chacun de cinq artefacts, deux fichiers qui ne nomment que son chemin suffisent à le faire passer devant son voisin du dessus.

**Une mesure hors de ce jeu d'essai.** La description de la demande de fusion (*pull request*) [GuitarAlchemist/Demerzel#1217](https://github.com/GuitarAlchemist/Demerzel/pull/1217) consigne que, selon la règle du producteur, les fichiers de données des deux premiers modules de ce parcours, qui se contentaient d'énumérer des chemins d'artefacts, auraient augmenté onze des seize nombres de 4 à 6 à l'exécution nocturne suivante, sur une tête de branche antérieure, `fb6c317`, et aucun sur `b938cc3`, une fois les noms devenus des étiquettes. Cette mesure n'étant pas reproductible à partir du commit épinglé, elle ne fonde ici aucune conclusion ; c'est elle qui explique pourquoi cette leçon espace ses étiquettes.

### Exercice pratique 2

À partir des seize nombres : (a) ajoutez un catalogue ; donnez la nouvelle somme et sa variation relative. (b) Ajoutez plutôt un fichier qui ne nomme que le chemin de l'artefact à 44. Quelles relations d'ordre changent ?

> **Réponse :** (a) `359 + 16 = 375`, `16 / 359 = 4.46%` ; aucune relation d'ordre ne change (0 sur 120). (b) 44 devient 45 et rejoint l'artefact à 45 : une relation passe de « derrière » à « à égalité ».

## 3. Quand l'indicateur rapporte

Goodhart (1975), à propos des objectifs monétaires, cité par Manheim et Garrabrant (2018) : « any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes » (toute régularité statistique observée tend à s'effondrer dès qu'on exerce sur elle une pression à des fins de contrôle). Campbell (1979), à propos des indicateurs sociaux, cité au même endroit : « The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort and corrupt the social processes it is intended to monitor. » (plus un indicateur social quantitatif sert à la prise de décision sociale, plus il est exposé aux pressions qui le corrompent, et plus il tend à fausser et à corrompre les processus sociaux qu'il est censé suivre). Le titre reprend Strathern (1997) : « When a measure becomes a target, it ceases to be a good measure. » (quand une mesure devient une cible, elle cesse d'être une bonne mesure). Chacun nomme une condition, la pression ou l'usage dans les décisions, et non une fatalité.

**Observé : le décompte sert-il à décider ?** Sur le papier. La [politique anti-LOLLI](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml) calcule [`ratio_n = LOLLI_n / max(ERGOL_n, 1)`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L69), compte le [« citation_count delta »](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L305) (la variation du nombre de citations) comme de l'ERGOL, et [gèle la création d'artefacts](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L97) quand le rapport reste au-dessus de 3,0 pendant 3 cycles consécutifs ; son [fichier d'historique](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json) ne contient qu'un cycle, daté du 2026-03-23. Une [règle de détection](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56) porte aussi un jugement sur les nombres : « If the top 20% of governance artifacts account for more than 60% of citations, a power law is present. This is healthy » (au-delà de ce seuil, une loi de puissance est présente, et c'est « sain »). `policies / compounding-metrics-policy.yaml` la reprend, tire ses données du `citation_count` des enregistrements (lignes 117–122) et fixe à cette part une « target » (cible) de « 0,60–0,85 » (lignes 219–222). Sur les nombres saisis à la main avant le 2026-09-13, [PSY-007](psy-007-power-law-or-not.fr.md) trouve le verdict inverse ; celui-ci a changé en même temps que l'instrument. **Cet échantillon ne permet pas de dire si le décompte commande aujourd'hui la moindre décision.**

**Synthétique : ce que ferait une pression.** Chaque agent supposé consacre une unité d'effort soit au travail (une valeur `a`, qui se retrouve telle quelle dans l'indicateur), soit à l'inflation (`g` points d'indicateur, sans aucune valeur).

```text
indicateur = valeur + inflation + erreur
récompense = (1 - w) x valeur + w x indicateur
```

Le travail rapporte `a` quel que soit `w`, et l'inflation rapporte `w x g` : un agent gonfle donc l'indicateur quand `w x g > a`. `scenarios.json` suppose `a` et `g` compris entre 1 et 10, et une erreur de −1, 0 ou 1 : 300 cas équiprobables, énumérés exactement.

| Poids `w` de l'indicateur dans la récompense | 0 | 1/2 | 1 |
|---|---|---|---|
| Indicateur moyen | 5,50 | 6,60 | 7,15 |
| Valeur réelle moyenne | 5,50 | 5,10 | 3,85 |
| Corrélation entre indicateur et valeur | 0,9619 | 0,4374 | 0,2785 |

De `w = 0` à `w = 1`, l'indicateur moyen augmente de 30 % tandis que la valeur moyenne diminue de 30 % : l'indicateur s'améliore à mesure que se réduit la chose qu'il représentait. Dans le modèle, plus l'indicateur est optimisé, moins il renseigne sur la valeur. L'effet exige les trois conditions à la fois : une récompense fondée sur l'indicateur, un moyen de le gonfler, et un travail qui rapporte moins que l'inflation.

### Exercice pratique 3

La règle de détection appliquée aux 18 nombres enregistrés (les seize ci-dessus, plus 55 et 0 hors du dépôt ; somme 414). 20 % de 18 artefacts font 3,6 ; prenez les 4 premiers. (a) La règle déclare-t-elle « sains » les nombres épinglés ? (b) Synthétique : chaque fichier ajouté nomme les chemins de citation des trois artefacts mesurables qui figurent parmi les 4 premiers. Combien de fichiers faut-il pour que la part dépasse 60 % ? (c) Que fait, à la place, un catalogue unique de tous les chemins ? (d) Que dit (b) du verdict ?

> **Réponse :** (a) `65 + 55 + 47 + 45 = 212`, et `212 / 414 = 51.21%` : non (les 3 premiers détiennent 40,34 %). (b) Chaque fichier ajoute 3 des deux côtés : `212 + 3n > 0.6 x (414 + 3n)` donne `1.2n > 36.4`, donc `n = 31`, et `305 / 507 = 60.16%` (30 fichiers donnent 59,92 %). (c) Il augmente de 1 les seize nombres mesurables : `215 / 430 = 50.00%`, encore plus loin du verdict « sain ». (d) Trente et un fichiers de mentions, sans aucun changement d'usage, suffiraient à renverser le verdict : celui-ci juge l'endroit où les chemins sont écrits. Personne n'a été observé en train d'écrire de tels fichiers.

### Exercice pratique 4

Synthétique. Le travail d'un agent produit 3 points de valeur ; l'inflation produirait 8 points d'indicateur. (a) Pour `w` = 0, 1/2 et 1, l'agent travaille-t-il ou gonfle-t-il l'indicateur, et quels sont sa valeur et son indicateur (erreur 0) ? (b) Au-dessus de quel poids bascule-t-il ?

> **Réponse :** (a) Il gonfle l'indicateur quand `w x 8 > 3`. À 0, il travaille : valeur 3, indicateur 3. À 1/2, `4 > 3` : il gonfle, valeur 0, indicateur 8 ; à 1, `8 > 3`, de même. (b) `w x 8 > 3` est vrai pour `w > 3 / 8 = 0.375`. L'agent est supposé, non observé.

## 4. Des prévisions qui déplacent leur cible

Une prévision est *réflexive* quand sa publication modifie le résultat qu'elle prédit. L'un des canaux est ici mécanique : une prévision du nombre d'un artefact, intégrée au dépôt dans un fichier qui nomme le chemin de cet artefact, est elle-même un fichier compté.

```text
résultat = référence + self_mentions + réaction x (prévision - référence)
```

**Synthétique, à partir d'un nombre observé.** `policies / alignment-policy.yaml` a un nombre de 44. Prévoyez 44 hors du dépôt, sans réaction, et la prévision se réalise ; intégrez-la au dépôt dans un fichier qui nomme le chemin, et elle échoue par construction : le résultat est 45. Si, de plus, les lecteurs ajoutent une demi-mention par point de prévision au-dessus de la référence (réaction 1/2), la prévision qui se réalise est 46, et reprendre à chaque fois le dernier résultat comme prévision donne des erreurs de 1, puis de 0,5, de 0,25 et de 0,125. Grunberg et Modigliani (1954) ont donné des conditions dans lesquelles une prévision publique peut malgré tout être exacte.

### Exercice pratique 5

Synthétique. Votre prévision du nombre qui vaut aujourd'hui 44 sera intégrée au dépôt dans un fichier qui nomme le chemin de l'artefact. (a) Sans réaction, que devient une prévision de 44 ? (b) Avec une réaction de 1/2, quelle prévision est égale à son résultat ? (c) Comment publieriez-vous pour supprimer l'effet, et selon quel critère ?

> **Réponse :** (a) Le résultat est `44 + 1 = 45` : une erreur de 1, commise par la prévision elle-même. (b) `f = 44 + 1 + (f - 44) / 2` donne `f / 2 = 23`, donc `f = 46`. (c) Écrire l'artefact sous forme d'étiquette espacée, ou publier hors des fichiers suivis : `self_mentions` devient 0 et 44 est son propre résultat. Critère : une prévision ne doit pas être une entrée de ce qu'elle prévoit.

**L'objection la plus forte à la lecture que fait cette leçon** est qu'elle reproche au décompte quelque chose que son producteur n'a jamais prétendu faire : la docstring promet des mentions, et un fichier qui nomme une politique a d'ordinaire une raison de le faire. Le jeu d'essai ne range aucun fichier dans l'usage ou dans la mention : **cet échantillon ne permet donc pas de distinguer un nombre honnête d'un nombre gonflé**, et rien n'y montre qu'un nombre ait été gonflé. Pour trancher, trier à la main les 200 fichiers comptés entre usage (le fichier charge, teste ou fait appliquer l'artefact) et mention, et voir si le classement des artefacts résiste.

**Ce qui détecterait une inflation.** Deux signaux sont calculables dès aujourd'hui : les citations apportées par fichier (16 pour un catalogue, au plus 7 au commit épinglé) et la part qui vient de fichiers qui en reprennent un autre, comme les traductions (8 sur 359, soit 2,23 %).

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers dont les liens ou les noms figurent plus haut, et la tendance de qualité. Le [README](../../../fixtures/psychohistory/psy-020/README.md) du jeu d'essai donne les commandes, les autocontrôles et les témoins négatifs.

**Références de méthode.** Goodhart, C. A. E. (1975), « Problems of Monetary Management: The U.K. Experience », *Papers in Monetary Economics*, vol. I, Reserve Bank of Australia ; repris dans Goodhart (1984), *Monetary Theory and Practice: The UK Experience*, Macmillan, 91–121. Campbell, D. T. (1979), « Assessing the Impact of Planned Social Change », *Evaluation and Program Planning* 2(1), 67–90. Strathern, M. (1997), « 'Improving Ratings': Audit in the British University System », *European Review* 5(3), 305–321. Manheim, D., et Garrabrant, S. (2018), « Categorizing Variants of Goodhart's Law », [arXiv:1803.04585](https://arxiv.org/abs/1803.04585). Grunberg, E., et Modigliani, F. (1954), « The Predictability of Social Events », *Journal of Political Economy* 62(6), 465–478.

**Non fait.** Ni l'effort ni le motif d'un agent n'ont été observés ; les deux modèles sont supposés. Les 200 fichiers comptés n'ont pas été triés. Les phrases de Goodhart et de Campbell n'ont pas été vérifiées sur les textes de 1975 et de 1979 ; celle de Strathern a été lue à la page 308 d'une numérisation hébergée sur gwern.net. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Le tri à la main décrit plus haut. Si le classement selon l'usage coïncide avec le classement selon le nombre, la conclusion passe de « le décompte ne sait pas distinguer l'usage de la mention » à « aujourd'hui, il n'a pas besoin de le faire » ; elle ne dirait toujours rien d'un nombre devenu une récompense.
