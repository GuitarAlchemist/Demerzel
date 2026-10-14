---
module_id: psy-007-power-law-or-not
department: psychohistory
course: "Est-ce une loi de puissance ? Dix-huit nombres de citations"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-007
version: "0.1.0"
---

# Est-ce une loi de puissance ? Dix-huit nombres de citations

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous lirez une liste rang-taille, vous verrez pourquoi une droite en échelle log-log n'est pas une preuve de loi de puissance, vous estimerez un exposant par maximum de vraisemblance au-dessus d'une coupure énoncée, vous comparerez la loi de puissance à deux familles plus simples, et vous direz ce qu'un échantillon aussi petit permet de distinguer. **Question de projet :** le département inscrit une « power law dynamics » dans l'efficacité des artefacts ; les derniers nombres de citations soutiennent-ils une loi de puissance plutôt que des solutions plus simples ?

[PSY-001](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md) définit une dimension de capitalisation, `D_c = log(value_ratio) / log(scale_ratio)` (à sa ligne 66) : l'exposant d'une relation en loi de puissance entre deux grandeurs, là où cette leçon demande combien d'objets ont chaque taille. Ni PSY-001 ni [PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) n'emploient le terme. [PSY-009](psy-009-concentration-and-heavy-tails.fr.md) mesure la concentration sans supposer de famille.

## 1. Ce que dit l'enregistrement, et ce que sont ces dix-huit nombres

**Observé.** L'[enregistrement du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) mentionne les lois de puissance trois fois, toujours comme un thème : les axes de recherche « Fractal compounding analysis — measuring D_c, power laws, learning momentum » ([ligne 10](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L10)) et « Power law dynamics — Pareto/Zipf distributions in artifact effectiveness » ([ligne 17](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L17)), ainsi que l'entrée de programme « Power Law Detection: identifying Pareto distributions in governance data » ([ligne 26](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L26)). Aucune ne nomme de jeu de données ni de test. La spécification que PSY-001 [cite en premier](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md#L173) nomme les deux : « If the top 20% of governance artifacts account for more than 60% of citations, a power law is present » ([ligne 56](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56)), sur les nombres de citations des enregistrements d'évolution ([ligne 60](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L60)). C'est un seuil de part, non un ajustement.

Une *loi de puissance* donne à une valeur x une probabilité proportionnelle à `x^-alpha`, d'*exposant* alpha (les distributions de Pareto et de Zipf sont de cette sorte) : les valeurs très au-dessus de la valeur typique restent probables.

Dans la tendance de qualité, l'« efficacité » est une étiquette catégorielle ([PSY-005](psy-005-persistence-baseline.fr.md)) ; la règle, et cette leçon, utilisent `citation_count` : le nombre de fichiers suivis qui mentionnent l'un des *chemins de citation* de l'artefact, compté avec `git grep` ([`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15)).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/extract.py) fige la dernière exécution au commit `4b03838` (2026-10-13T18:43:54Z, [18 lignes](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl#L217-L234)) dans [`observed-input.json`](../../../fixtures/psychohistory/psy-007/observed-input.json). Triés, avec une étoile sur les deux nombres qui n'ont pas été mesurés :

```text
65  55*  47  45  44  29  29  23  17  15  14  13  6  6  5  1  0  0*
```

La somme vaut 414. Trois faits limitent ce qui suit :

- **Seize mesures, et non dix-huit.** Le 55 et le zéro étoilés n'ont ni `citation_source` ni chemin de citation, ce qui marque un artefact qui « [lives outside this repository (unmeasurable here)](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23) » ; tous deux ont conservé une valeur saisie à la main.
- **Des nombres dépendants.** Les deux 29 partagent presque tous leurs fichiers citants : l'un des artefacts inscrit l'autre parmi ses chemins de citation ; et un fichier peut citer plusieurs artefacts.
- **Une correspondance, non un usage.** La recherche porte sur une chaîne littérale ([lignes 76–86](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L76-L86)) : un fichier qui se contente d'énumérer le chemin d'un artefact est compté comme un fichier qui s'en sert.

Une loi de puissance ne donne aucune probabilité à 0 : les deux zéros sont écartés et il reste 16 nombres positifs.

### Exercice pratique 1

Combien de valeurs peuvent entrer dans un graphique log-log, combien d'entre elles ont été mesurées par git grep, et combien de mesures distinctes cela fait-il au plus ?

> **Réponse :** `18 − 2 = 16` nombres positifs entrent dans le graphique. Le 55 étoilé est saisi à la main : `16 − 1 = 15` mesures par git grep. Les deux 29 comptent presque les mêmes fichiers : au plus `15 − 1 = 14` mesures distinctes.

## 2. Une droite sur papier log-log

Sur un *graphique rang-taille*, on porte `log10(count)` contre `log10(rank)`, du plus grand nombre au plus petit. Sous une loi de puissance d'exposant alpha, les points se tiennent près d'une droite de pente `−1 / (alpha − 1)`. La recette tentante : ajuster une droite des moindres carrés, lire `alpha = 1 + 1 / |slope|`, et annoncer un R², la part de variance que la droite explique. **Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/analyze.py) sur les 16 nombres positifs : pente −1,152, R² 0,669, exposant impliqué 1,868.

**Synthétique.** Le script tire 2 000 échantillons de 16 valeurs dans chacune des trois familles ajustées à la section 4 ([`scenarios.json`](../../../fixtures/psychohistory/psy-007/scenarios.json) consigne leurs paramètres comme des hypothèses) et ajuste la même droite :

| Famille générante | R² médian | R² au moins égal à 0,9 |
|---|---|---|
| Loi de puissance | 0,946 | 81,8 % |
| Lognormale | 0,88 | 40,0 % |
| Exponentielle | 0,776 | 7,3 % |

Clauset, Shalizi et Newman (2009, annexe A) notent qu'« in practice we rarely see a low r², regardless of the actual form of the distribution, so that the value of r² tells us little ». Ici, c'est la valeur basse qui est informative : 1 989 des 2 000 échantillons en loi de puissance atteignent le 0,669 relevé.

### Exercice pratique 2

(a) La droite a une pente de −1,152 : calculez l'exposant qu'elle implique. (b) Les 16 nombres d'un collègue donnent un R² supérieur à 0,9. Que dit le tableau de leur famille ?

> **Réponse :** (a) `1 + 1 / 1.152 = 1.868`. (b) Très peu de chose : un R² de 0,9 ou plus survient dans 81,8 % des échantillons en loi de puissance, mais aussi dans 40,0 % des lognormaux et 7,3 % des exponentiels. Seule une valeur basse discrimine : tous les échantillons en loi de puissance atteignent 0,669 sauf `2,000 − 1,989 = 11` d'entre eux.

## 3. L'exposant par maximum de vraisemblance, au-dessus d'une coupure énoncée

Le *maximum de vraisemblance* retient l'exposant sous lequel les valeurs observées sont les plus probables. Une loi de puissance s'ajuste à une *queue*, les valeurs supérieures ou égales à une coupure `x_min`, et un ajustement doit énoncer la coupure et le nombre de valeurs restantes.

```text
continu :  alpha = 1 + n / somme des ln(x / x_min)      erreur type = (alpha - 1) / sqrt(n)
discret :  p(x) = x^-alpha / zeta(alpha, x_min)         alpha : moyenne du modèle de ln x = moyenne de l'échantillon de ln x
```

`zeta(alpha, x_min)` est la somme des `k^-alpha` sur les entiers `k >= x_min`. Ces nombres sont peu nombreux et sont de petits entiers : cette leçon ajuste donc la forme **discrète** ; la formule continue traite les entiers comme des points d'un continuum et se calcule à la main. Elle donne un exposant supérieur de 0,055 à la coupure 1 et de 0,059 à la coupure 13 ; aucune conclusion ci-dessous ne dépend de ce choix.

**Calculé** (KS, la *distance de Kolmogorov–Smirnov* : le plus grand écart entre les parts cumulées des données et celles de la loi ajustée) :

| Coupure `x_min` | Valeurs retenues | Exposant | Erreur type | KS |
|---|---|---|---|---|
| 1 | 16 | 1,297 | 0,075 | 0,395 |
| 13 | 12 | 2,21 | 0,349 | 0,214 |
| 44 | 5 | 7,602 | 2,955 | 0,174 |

Sur les dix coupures essayées, l'exposant va de 1,297 à 7,602 : il décrit la coupure autant que les données. La règle de l'article cité, la plus petite distance KS, retient 44, une « queue » de cinq nombres. Cette leçon rapporte les coupures 1 (tous les nombres positifs) et 13 (cette règle parmi les coupures qui gardent au moins 10 valeurs, un plancher choisi après avoir vu les nombres).

**Synthétique.** Sur 2 000 queues de 12 valeurs tirées d'une loi de puissance d'exposant 2,21, 95 % des exposants ajustés se situent entre 1,729 et 3,339.

### Exercice pratique 3

À la coupure 13, il reste 12 valeurs et la somme des `ln(x / 13)` vaut 9,459. Calculez l'exposant continu et son erreur type ; comparez à l'ajustement discret.

> **Réponse :** `alpha = 1 + 12 / 9.459 = 2.269`, et `(2.269 − 1) / sqrt(12) = 0.366`. L'ajustement discret donne 2,21 avec une erreur type de 0,349 : les deux formes diffèrent de 0,059, environ un sixième de l'une ou l'autre erreur type.

## 4. Des familles plus simples, et ce que dix-huit nombres peuvent dire

Deux familles plus simples vivent sur les mêmes entiers : une *exponentielle* discrète (chaque unité supplémentaire multiplie la probabilité par une constante ; pas de queue lourde) et une *lognormale* (`ln x` suit une loi normale ; arrondie ici à l'entier supérieur ; deux paramètres). La *log-vraisemblance* d'une famille ajustée est le logarithme de la probabilité qu'elle donne aux données ; plus elle est haute, mieux c'est. R est la log-vraisemblance d'une famille moins celle d'une autre (négatif : la seconde s'ajuste mieux), et le test de Vuong (1989, tel que l'article cité l'applique) donne la probabilité d'un rapport aussi éloigné de zéro si les deux s'ajustent également bien ; l'article se fie au signe quand p < 0,1, ce que cette leçon appelle décisif.

**Calculé**, les log-vraisemblances, d'après [`results.json`](../../../fixtures/psychohistory/psy-007/results.json) :

| Valeurs | Loi de puissance | Exponentielle | Lognormale |
|---|---|---|---|
| Les 16 nombres positifs | −80,97 | −67,74 | −69,93 |
| Les 12 nombres égaux ou supérieurs à 13 | −49,96 | −48,24 | non ajustée |

Sur tous les nombres positifs, la loi de puissance est la pire des trois, et de façon décisive : R = −13,23 contre l'exponentielle (p < 0,0001) et −11,04 contre la lognormale (p = 0,012). L'exponentielle et la lognormale ne sont pas séparées (R = 2,19, p = 0,1779). Un test d'adéquation confirme : la distance KS relevée, 0,395, dépasse celle des 2 000 échantillons synthétiques de la loi de puissance ajustée.

Sur la queue au-dessus de 13, rien n'est tranché : R = −1,71 contre l'exponentielle (sans arrondi ; p = 0,2557), et la loi de puissance n'est pas écartée non plus (501 des 2 000 queues synthétiques sont au moins aussi éloignées de leur ajustement, p = 0,2505, au-dessus du 0,1 de l'article). Pourtant, aux coupures 15 et 17, l'exponentielle gagne de façon décisive (p = 0,0832 et 0,0364).

**Synthétique : que peuvent distinguer si peu de valeurs ?** Parmi des échantillons de 16 valeurs, la famille générante a la plus grande vraisemblance dans 3 785 cas sur 6 000, soit 63,1 %. Les nombres relevés placent l'exponentielle en tête ; cela arrive dans 2 échantillons sur 2 000 tirés de la loi de puissance. Sur la queue, avec une loi de puissance (alpha 2,21) et une exponentielle (moyenne 33) au-dessus de 13 comme générantes :

| Valeurs de queue | Loi de puissance : bon signe / et décisif | Exponentielle : bon signe / et décisif |
|---|---|---|
| 12 | 66,2 % / 27,0 % | 92,2 % / 48,6 % |
| 50 | 96,4 % / 66,0 % | 98,7 % / 74,5 % |
| 200 | 100,0 % / 99,3 % | 100,0 % / 99,3 % |

**Réponse à la question de projet :** non. Lus comme 16 tirages indépendants, les nombres écartent une loi de puissance qui commencerait à 1 ; sur les 12 nombres égaux ou supérieurs à 13, **cet échantillon ne permet pas de distinguer une loi de puissance d'une exponentielle**.

### Exercice pratique 4

Classez les quatre comparaisons aux coupures 1 et 13 avec la règle du 0,1, puis dites laquelle de ces phrases les résultats soutiennent : « les nombres suivent une loi exponentielle », « les nombres ne suivent pas une loi de puissance sur toute leur étendue », ou « la queue suit une loi de puissance ».

> **Réponse :** Sur tous les nombres positifs, loi de puissance contre exponentielle (p < 0,0001) et contre lognormale (p = 0,012) : décisif, contre la loi de puissance. Les deux autres (p = 0,1779 et p = 0,2557) : indécis. Seule la deuxième phrase est soutenue. La première échoue parce que la lognormale reste en jeu ; la troisième parce que « non écartée » est plus faible que « soutenue ».

**L'objection la plus forte à cette lecture** est qu'elle décrit l'instrument autant que les artefacts ([PSY-011](../en/psy-011-measurement-change-or-system-change.md)). Jusqu'au 2026-09-13, les nombres étaient [saisis à la main](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8). À la dernière exécution avant git grep, les mêmes artefacts affichaient 55, 12, 11, 8, 5, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1, 0, 0 : le R² vaut 0,959, aucune comparaison de vraisemblances n'est décisive (contre l'exponentielle : R = 1,27, p = 0,7688), et la valeur p d'adéquation vaut 0,0805, déjà sous 0,1 (aujourd'hui : 0 sur 2 000). La règle même du projet bascule avec l'instrument : les trois ou quatre plus grands nombres (20 % de 18 vaut 3,6) détenaient 67,2 % ou 74,1 % des citations, une loi de puissance selon sa barre des 60 %, et en détiennent aujourd'hui 40,3 % ou 51,2 %. Retirer les deux nombres saisis à la main ne change presque rien (R = −12,08 contre l'exponentielle, p = 0,0001).

### Exercice pratique 5

Vous pouvez mesurer davantage d'artefacts. D'après le tableau des queues, combien de valeurs de queue demandez-vous, et quels résultats vous feraient accepter « loi de puissance » pour la queue ?

> **Réponse :** Environ 200, étalonnées contre une exponentielle seule : un verdict décisif et correct arrive dans 66,0 % et 74,5 % des échantillons à 50 valeurs, et dans 99,3 % à 200. N'acceptez qu'avec une coupure et une taille de queue énoncées, une valeur p d'adéquation supérieure à 0,1, et un R favorable à la loi de puissance contre les deux solutions de rechange avec p < 0,1.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** `extract.py` lit 27 fichiers (les cinq fichiers de tendance de qualité, les 18 enregistrements de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution), l'enregistrement du département, la spécification, PSY-001 et PSY-002) et s'arrête si l'un d'eux diffère de son blob Git épinglé. Le [README](../../../fixtures/psychohistory/psy-007/README.md) donne les commandes, les 46 autovérifications et les contrôles négatifs.

**Références de méthode.** Clauset, A., Shalizi, C. R., et Newman, M. E. J. (2009), « Power-law distributions in empirical data », *SIAM Review* 51(4), 661–703, [arXiv:0706.1062](https://arxiv.org/abs/0706.1062) : la méthode suivie ici ; l'article avertit que les jeux de données de moins d'une cinquantaine de valeurs « should be treated with caution ». Vuong, Q. H. (1989), « Likelihood Ratio Tests for Model Selection and Non-Nested Hypotheses », *Econometrica* 57(2), 307–333.

**Non fait.** Le test d'adéquation garde la coupure fixe, là où l'article cité la réestime dans chaque échantillon synthétique : 0,2505 est probablement trop indulgent. Non ajustés : une lognormale sur la queue, une loi de puissance avec coupure haute. Chaque valeur p traite les nombres comme des tirages indépendants d'une même distribution ; ils ne sont ni indépendants, ni un échantillon des fichiers gouvernés, seulement les 18 qui ont un enregistrement d'évolution. La valeur p de Vuong est une approximation pour grands échantillons, employée ici sur 16 et 12 valeurs. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Appliquer la règle du git grep à tous les fichiers suivis et relancer. Une queue d'environ 200 valeurs qui passerait le test d'adéquation et battrait de façon décisive les deux solutions de rechange ferait passer la conclusion à « une loi de puissance est plausible dans la queue ».
