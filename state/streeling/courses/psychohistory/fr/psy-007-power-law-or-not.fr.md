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

Vous lirez une liste rang-taille, vous verrez pourquoi une droite en coordonnées log-log ne témoigne pas d'une loi de puissance, vous estimerez un exposant par maximum de vraisemblance au-dessus d'un seuil déclaré, vous comparerez la loi de puissance à deux familles plus simples, et vous direz ce qu'un échantillon aussi petit permet de distinguer. **Question de projet :** le département annonce des « power law dynamics » (dynamiques en loi de puissance) dans l'efficacité des artefacts ; les derniers nombres de citations soutiennent-ils une loi de puissance plutôt que des alternatives plus simples ?

[PSY-001](psy-001-intro-fractal-compounding.fr.md) définit une dimension de capitalisation, `D_c = log(value_ratio) / log(scale_ratio)` (sa ligne 66) : l'exposant d'une relation en loi de puissance entre deux grandeurs, alors que cette leçon demande combien d'éléments ont chaque taille. Ni PSY-001 ni [PSY-002](psy-002-governance-phase-transitions.fr.md) n'emploie le terme de loi de puissance. [PSY-009](psy-009-concentration-and-heavy-tails.fr.md) mesure la concentration sans supposer de famille de lois.

## 1. Ce que dit la fiche du département, et ce que sont les dix-huit nombres

**Observé.** La [fiche du département](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json) mentionne les lois de puissance trois fois, toujours comme un thème : dans les domaines de recherche « Fractal compounding analysis — measuring D_c, power laws, learning momentum » ([ligne 10](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L10)) et « Power law dynamics — Pareto/Zipf distributions in artifact effectiveness » ([ligne 17](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L17)), et dans l'entrée du programme « Power Law Detection: identifying Pareto distributions in governance data » ([ligne 26](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/departments/psychohistory.department.json#L26)). Aucune ne désigne un jeu de données ni un test. La spécification que PSY-001 [cite en premier](psy-001-intro-fractal-compounding.fr.md#base-de-recherche) désigne les deux : « If the top 20% of governance artifacts account for more than 60% of citations, a power law is present » ([ligne 56](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56)), à propos des nombres de citations des enregistrements d'évolution ([ligne 60](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L60)). C'est un seuil sur une part, non un ajustement.

Une *loi de puissance* attribue à une valeur x une probabilité proportionnelle à `x^-alpha`, d'*exposant* alpha (les lois de Pareto et de Zipf sont de ce type) : des valeurs très supérieures à la valeur typique gardent une probabilité appréciable.

Dans la tendance de qualité, l'« efficacité » est une étiquette catégorielle ([PSY-005](psy-005-persistence-baseline.fr.md)) ; la règle, comme cette leçon, utilise `citation_count` : le nombre de fichiers suivis qui mentionnent l'un des *chemins de citation* de l'artefact, compté avec `git grep` ([`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15)).

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/extract.py) fige la dernière exécution, au commit `4b03838` (2026-10-13T18:43:54Z, [18 lignes](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend/2026-10.jsonl#L217-L234)), dans [`observed-input.json`](../../../fixtures/psychohistory/psy-007/observed-input.json). Triés, avec un astérisque sur les deux nombres qui n'ont pas été mesurés :

```text
65  55*  47  45  44  29  29  23  17  15  14  13  6  6  5  1  0  0*
```

Leur somme vaut 414. Trois faits limitent ce qui suit :

- **Seize mesures, et non dix-huit.** Le 55 et le zéro marqués d'un astérisque n'ont ni `citation_source` ni chemin de citation, ce qui signale un artefact qui « [lives outside this repository (unmeasurable here)](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23) » (vit hors de ce dépôt, non mesurable ici) ; tous deux ont gardé une valeur saisie à la main.
- **Des nombres dépendants.** Les deux 29 partagent presque tous leurs fichiers citants : l'un des artefacts compte l'autre parmi ses chemins de citation ; et un même fichier peut citer plusieurs artefacts.
- **Une occurrence, non un usage.** La recherche porte sur une chaîne littérale ([lignes 76–86](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L76-L86)) : un fichier qui ne fait que lister le chemin d'un artefact est compté comme un fichier qui l'utilise.

Une loi de puissance n'attribue aucune probabilité à 0 : on écarte les deux zéros, et il reste 16 nombres non nuls.

### Exercice pratique 1

Combien de valeurs peuvent figurer sur un graphique log-log, combien d'entre elles ont été mesurées par git grep, et combien de mesures distinctes cela fait-il au plus ?

> **Réponse :** `18 − 2 = 16` nombres non nuls figurent sur le graphique. Le 55 marqué d'un astérisque est saisi à la main : `16 − 1 = 15` mesures par git grep. Les deux 29 comptent presque les mêmes fichiers : au plus `15 − 1 = 14` mesures distinctes.

## 2. Une droite sur papier log-log

Sur un *diagramme rang-taille*, on porte `log10(count)` en fonction de `log10(rank)`, le plus grand nombre en premier. Sous une loi de puissance d'exposant alpha, les points se placent près d'une droite de pente `−1 / (alpha − 1)`. La recette tentante : ajuster une droite par les moindres carrés, lire `alpha = 1 + 1 / |slope|`, et citer R², la part de la variance qu'explique la droite. **Calculé** par [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-007/analyze.py) sur les 16 nombres non nuls : pente −1,152, R² 0,669, exposant déduit 1,868.

**Synthétique.** Le script tire 2 000 échantillons de 16 valeurs dans chacune des trois familles ajustées à la section 4 ([`scenarios.json`](../../../fixtures/psychohistory/psy-007/scenarios.json) consigne leurs paramètres comme des hypothèses) et ajuste la même droite :

| Famille génératrice | R² médian | R² d'au moins 0,9 |
|---|---|---|
| Loi de puissance | 0,946 | 81,8 % |
| Log-normale | 0,88 | 40,0 % |
| Exponentielle | 0,776 | 7,3 % |

Clauset, Shalizi et Newman (2009, annexe A) notent que « in practice we rarely see a low r², regardless of the actual form of the distribution, so that the value of r² tells us little » (en pratique, un r² faible est rare quelle que soit la forme réelle de la loi, si bien que sa valeur renseigne peu). Ici, c'est la valeur faible qui est informative : 1 989 des 2 000 échantillons tirés de la loi de puissance atteignent le 0,669 enregistré.

### Exercice pratique 2

(a) La droite a une pente de −1,152 : calculez l'exposant qu'elle implique. (b) Les 16 nombres d'un collègue donnent un R² supérieur à 0,9. Que dit le tableau de leur famille ?

> **Réponse :** (a) `1 + 1 / 1.152 = 1.868`. (b) Très peu de chose : un R² de 0,9 ou plus apparaît dans 81,8 % des échantillons tirés de la loi de puissance, mais aussi dans 40,0 % des échantillons log-normaux et 7,3 % des échantillons exponentiels. Seule une valeur faible discrimine : tous les échantillons de la loi de puissance sauf `2,000 − 1,989 = 11` atteignent 0,669.

## 3. L'exposant par maximum de vraisemblance, au-dessus d'un seuil déclaré

Le *maximum de vraisemblance* retient l'exposant sous lequel les valeurs observées sont les plus probables. Une loi de puissance s'ajuste sur une *queue*, les valeurs supérieures ou égales à un seuil `x_min`, et un ajustement doit déclarer le seuil et le nombre de valeurs qui restent.

```text
continue :   alpha = 1 + n / somme des ln(x / x_min)      erreur type = (alpha - 1) / sqrt(n)
discrète :   p(x) = x^-alpha / zeta(alpha, x_min)         alpha : moyenne de ln x sous le modèle = moyenne de ln x dans l'échantillon
```

`zeta(alpha, x_min)` est la somme de `k^-alpha` sur les entiers `k >= x_min`. Ces valeurs sont peu nombreuses et ce sont de petits entiers : cette leçon ajuste donc la forme **discrète** ; la formule continue traite les entiers comme des points d'un continuum, et se calcule à la main. Elle donne un exposant plus élevé de 0,055 au seuil 1 et de 0,059 au seuil 13 ; aucune conclusion ci-dessous ne dépend de ce choix.

**Calculé** (KS, la *distance de Kolmogorov–Smirnov* : le plus grand écart entre les parts cumulées des données et celles de la loi ajustée) :

| Seuil `x_min` | Valeurs retenues | Exposant | Erreur type | KS |
|---|---|---|---|---|
| 1 | 16 | 1,297 | 0,075 | 0,395 |
| 13 | 12 | 2,21 | 0,349 | 0,214 |
| 44 | 5 | 7,602 | 2,955 | 0,174 |

Sur les dix seuils essayés, l'exposant va de 1,297 à 7,602 : il décrit le seuil autant que les données. La règle de l'article cité, la plus petite distance KS, retient 44, une « queue » de cinq nombres. Cette leçon rapporte les seuils 1 (tous les nombres non nuls) et 13 (cette même règle, parmi les seuils qui gardent au moins 10 valeurs, un plancher choisi après avoir vu les nombres).

**Synthétique.** Sur 2 000 queues de 12 valeurs tirées d'une loi de puissance d'exposant 2,21, 95 % des exposants ajustés se situent entre 1,729 et 3,339.

### Exercice pratique 3

Au seuil 13, il reste 12 valeurs, et la somme des `ln(x / 13)` vaut 9,459. Calculez l'exposant continu et son erreur type ; comparez avec l'ajustement discret.

> **Réponse :** `alpha = 1 + 12 / 9.459 = 2.269`, et `(2.269 − 1) / sqrt(12) = 0.366`. L'ajustement discret donne 2,21, avec une erreur type de 0,349 : les deux formes diffèrent de 0,059, environ un sixième de l'une ou l'autre erreur type.

## 4. Des alternatives plus simples, et ce que dix-huit nombres peuvent dire

Deux familles plus simples sont définies sur les mêmes entiers : une loi *exponentielle* discrète (chaque unité supplémentaire multiplie la probabilité par une constante ; pas de queue lourde) et une loi *log-normale* (`ln x` suit une loi normale ; arrondie ici à l'entier supérieur ; deux paramètres). La *log-vraisemblance* d'une famille ajustée est le logarithme de la probabilité qu'elle attribue aux données ; plus elle est élevée, meilleur est l'ajustement. R est la log-vraisemblance d'une famille moins celle d'une autre (négatif : la seconde s'ajuste mieux), et le test de Vuong (1989, tel que l'applique l'article cité) donne la probabilité d'un rapport aussi éloigné de zéro si les deux familles s'ajustent aussi bien l'une que l'autre ; l'article se fie au signe quand p < 0,1, ce que cette leçon qualifie de décisif.

Log-vraisemblances **calculées**, tirées de [`results.json`](../../../fixtures/psychohistory/psy-007/results.json) :

| Valeurs | Loi de puissance | Exponentielle | Log-normale |
|---|---|---|---|
| Les 16 nombres non nuls | −80,97 | −67,74 | −69,93 |
| Les 12 nombres de 13 ou plus | −49,96 | −48,24 | non ajustée |

Sur l'ensemble des nombres non nuls, la loi de puissance est la pire des trois, de façon décisive : R = −13,23 face à l'exponentielle (p < 0,0001) et −11,04 face à la log-normale (p = 0,012). L'exponentielle et la log-normale ne sont pas départagées (R = 2,19 ; p = 0,1779). Un test d'adéquation va dans le même sens : la distance KS enregistrée, 0,395, dépasse celle de chacun des 2 000 échantillons synthétiques tirés de la loi de puissance ajustée.

Sur la queue des valeurs de 13 ou plus, rien n'est tranché : R = −1,71 face à l'exponentielle (calculé sur les valeurs non arrondies ; p = 0,2557), et la loi de puissance n'est pas exclue non plus (501 des 2 000 queues synthétiques s'écartent au moins autant de leur ajustement, soit p = 0,2505, au-dessus du 0,1 de l'article). Pourtant, aux seuils 15 et 17, l'exponentielle l'emporte de façon décisive (p = 0,0832 et 0,0364).

**Synthétique : que peuvent distinguer si peu de valeurs ?** Parmi des échantillons de 16 valeurs, la famille génératrice a la plus forte vraisemblance dans 3 785 cas sur 6 000, soit 63,1 %. Les nombres enregistrés placent l'exponentielle en tête ; cela se produit dans 2 des 2 000 échantillons tirés de la loi de puissance. Sur la queue, avec comme générateurs une loi de puissance (alpha 2,21) et une exponentielle (moyenne 33) à partir de 13 :

| Valeurs dans la queue | Loi de puissance : bon signe / et décisif | Exponentielle : bon signe / et décisif |
|---|---|---|
| 12 | 66,2 % / 27,0 % | 92,2 % / 48,6 % |
| 50 | 96,4 % / 66,0 % | 98,7 % / 74,5 % |
| 200 | 100,0 % / 99,3 % | 100,0 % / 99,3 % |

**Réponse à la question de projet :** non. Lus comme 16 tirages indépendants, les nombres excluent une loi de puissance qui commencerait à 1 ; sur les 12 nombres de 13 ou plus, **cet échantillon ne permet pas de distinguer une loi de puissance d'une exponentielle**.

### Exercice pratique 4

Classez les quatre comparaisons aux seuils 1 et 13 selon la règle du 0,1, puis dites quelle phrase les résultats soutiennent : « les nombres suivent une loi exponentielle », « les nombres ne suivent pas une loi de puissance sur toute leur étendue » ou « la queue suit une loi de puissance ».

> **Réponse :** Sur tous les nombres non nuls, loi de puissance contre exponentielle (p < 0,0001) et contre log-normale (p = 0,012) : décisives, en défaveur de la loi de puissance. Les deux autres (p = 0,1779 et p = 0,2557) : non tranchées. Seule la deuxième phrase est soutenue. La première tombe parce que la log-normale reste en lice ; la troisième parce que « non exclue » est plus faible que « soutenue ».

**L'objection la plus forte à cette lecture** est qu'elle décrit l'instrument autant que les artefacts ([PSY-011](psy-011-measurement-change-or-system-change.fr.md)). Jusqu'au 2026-09-13, les nombres étaient [saisis à la main](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8). Lors de la dernière exécution avant git grep, les mêmes artefacts valaient 55, 12, 11, 8, 5, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1, 1, 0, 0 : R² vaut 0,959, aucune comparaison de vraisemblances n'est décisive (face à l'exponentielle : R = 1,27 ; p = 0,7688), et la valeur p du test d'adéquation vaut 0,0805, déjà sous 0,1 (aujourd'hui : 0 sur 2 000). La propre règle du projet bascule avec l'instrument : les trois ou quatre plus grands nombres (20 % de 18 font 3,6) totalisaient 67,2 % ou 74,1 % des citations, une loi de puissance selon son seuil de 60 %, et en totalisent aujourd'hui 40,3 % ou 51,2 %. Écarter les deux nombres saisis à la main change peu de chose (R = −12,08 face à l'exponentielle ; p = 0,0001).

### Exercice pratique 5

Vous pouvez mesurer davantage d'artefacts. D'après le tableau des queues, combien de valeurs de queue demandez-vous, et quels résultats vous feraient accepter « loi de puissance » pour la queue ?

> **Réponse :** Environ 200, un nombre calibré face à une exponentielle seulement : un verdict décisif et correct survient dans 66,0 % et 74,5 % des échantillons à 50 valeurs, dans 99,3 % à 200. N'acceptez qu'avec un seuil et une taille de queue déclarés, une valeur p du test d'adéquation supérieure à 0,1, et un R favorable à la loi de puissance face aux deux alternatives avec p < 0,1.

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** `extract.py` lit 27 fichiers (cinq fichiers de tendance de qualité, les 18 enregistrements de [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution), la fiche du département, la spécification, PSY-001 et PSY-002) et s'arrête si l'un d'eux diffère de son blob Git épinglé. Le [README](../../../fixtures/psychohistory/psy-007/README.md) donne les commandes, les 46 autocontrôles et les témoins négatifs.

**Références de méthode.** Clauset, A., Shalizi, C. R., et Newman, M. E. J. (2009), « Power-law distributions in empirical data », *SIAM Review* 51(4), 661–703, [arXiv:0706.1062](https://arxiv.org/abs/0706.1062) : la méthode suivie ici ; l'article avertit que les jeux de données de moins de 50 valeurs environ « should be treated with caution » (sont à traiter avec prudence). Vuong, Q. H. (1989), « Likelihood Ratio Tests for Model Selection and Non-Nested Hypotheses », *Econometrica* 57(2), 307–333.

**Non fait.** Le test d'adéquation garde le seuil fixe, là où l'article cité le réestime dans chaque échantillon synthétique : 0,2505 est probablement trop indulgent. Non ajustées : une log-normale sur la queue, une loi de puissance avec coupure. Chaque valeur p traite les nombres comme des tirages indépendants d'une même loi ; ils ne sont ni indépendants ni un échantillon des fichiers gouvernés : ce sont seulement les 18 qui ont un enregistrement d'évolution. La valeur p de Vuong est une approximation pour grands échantillons, utilisée ici sur 16 et 12 valeurs. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Appliquer la règle git-grep à chaque fichier suivi, puis relancer l'analyse. Une queue d'environ 200 valeurs qui passe le test d'adéquation et bat les deux alternatives de façon décisive ferait passer la conclusion à « une loi de puissance est plausible dans la queue ».
