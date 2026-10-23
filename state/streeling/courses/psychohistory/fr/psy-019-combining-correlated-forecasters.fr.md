---
module_id: psy-019-combining-correlated-forecasters
department: psychohistory
course: "Combiner des prévisionnistes qui partagent une source"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-019
version: "0.1.0"
---

# Combiner des prévisionnistes qui partagent une source

> **Département de psychohistoire** | Intermédiaire | 45 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous écrirez l'erreur quadratique moyenne d'une moyenne de k prévisions aux erreurs corrélées, vous trouverez le plancher sous lequel aucun effectif ne permet de descendre, vous comparerez un prévisionniste de plus du même type à un prévisionniste issu d'une autre source, et vous direz ce que montre l'accord. **Question de projet :** faire la moyenne des jugements de plusieurs agents aide-t-il quand ils lisent le même contexte ?

[PSY-016](psy-016-brier-score.fr.md) évalue une prévision ; ce module évalue une *moyenne de prévisions* avec l'arithmétique de [PSY-004](psy-004-how-large-is-large.fr.md).

## 1. Ce que partagent les juges

**Observé** au commit épinglé, et figé par [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/extract.py) dans [`observed-input.json`](../../../fixtures/psychohistory/psy-019/observed-input.json) :

- La [politique d'orchestration multimodèle](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/multi-model-orchestration-policy.yaml#L198-L203) fixe `single_model: max 0.8`, `two_model_agreement: 0.9` et `two_model_disagreement: 0.5`. Sa règle `cross-validation` exige l'accord d'au moins deux modèles et nomme claude et chatgpt, que son registre des modèles attribue à deux fournisseurs différents.
- Le [script du panel du tribunal](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/workflows/demerzel-tribunal-panel.js) soumettrait une même pull request à 5 personas. Chaque requête adressée au modèle porte le même titre, la même description, la même liste de fichiers et le même extrait de diff ; seuls le persona et la préoccupation qui lui est assignée diffèrent, et le workflow transmet un seul `--model`. Chaque persona répond `block`, `merge_with_followups` ou `pass`, et peut renvoyer un `score`, « 0..1 confidence in this PR for my concern (1 = clean) » (sa confiance dans cette PR au regard de sa préoccupation, la valeur maximale signifiant que la PR est propre) ; le verdict retient la réponse la plus sévère, au lieu d'une moyenne.
- Le [script du conseil](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/council_emit.py#L12-L35) associe le contrôle d'un analyseur statique à la relecture d'un modèle, deux relecteurs qu'il dit « deliberately heterogeneous » (délibérément hétérogènes), et retient le minimum de leurs scores ; un verdict à deux relectures, dit-il, « lifts the single-model confidence cap honestly » (relève honnêtement le plafond de confiance d'un modèle unique), une hypothèse qu'aucun fichier ne mesure.

Aucun d'eux ne contient la réponse d'un persona ni une issue ; les cinq verdicts enregistrés du conseil contiennent neuf scores (celui de reviewer_a vaut 0,75 chaque fois) et aucune issue. **Aucune corrélation entre les agents du projet n'a été mesurée : ni par ce module, ni dans aucun des fichiers qu'il a lus.** Tout ce qui suit est **synthétique**.

Une *prévision* est un nombre énoncé avant que l'issue soit connue ; son *erreur* est la prévision moins l'issue. Le modèle attribue au prévisionniste i l'erreur

```text
erreur_i = biais + sigma × ( sqrt(rho) × C + sqrt(1 − rho) × I_i )
```

C, la *part commune*, est tirée une fois par occasion et partagée par tous ; I_i, la *part individuelle*, est tirée pour chaque prévisionniste ; toutes deux ont une moyenne de 0 et une variance de 1. Chaque erreur a alors la variance sigma², et deux erreurs ont la corrélation rho, la part commune de cette variance. Des agents peuvent partager le *contexte* (ce que l'extrait omet, tous les lecteurs le manquent) et le *modèle* (les habitudes d'un même jeu de poids) ; un scénario répartit rho = 0,6 en 0,3 pour chacun, une répartition inventée. Tous ceux qui prévoient un même événement partagent aussi la part de son issue que personne ne pouvait anticiper : aucun effectif ni aucune autre source ne la supprime, et elle gonfle la corrélation des erreurs évaluées par rapport aux issues. Jusqu'au dernier paragraphe de la section 4, les erreurs sont mesurées par rapport à la meilleure prévision possible, sans cette part.

### Exercice pratique 1

Avec cette répartition, donnez la corrélation des erreurs entre un persona du panel et (a) un autre persona du panel ; (b) un relecteur sur un autre modèle qui lit le même extrait ; (c) une seconde exécution du modèle du panel à qui l'on fournit d'autres éléments ; (d) un relecteur sur un autre modèle à qui l'on fournit d'autres éléments. Quel cas correspond à un sixième persona ?

> **Réponse :** (a) Les deux parts sont communes : `0.3 + 0.3 = 0.6`. (b) Le contexte seulement : 0,3. (c) Le modèle seulement : 0,3. (d) Rien : 0. Un sixième persona relève du cas (a) : un prévisionniste de plus, le même rho. Ces valeurs classent des sources ; elles ne mesurent rien.

## 2. La variance d'une moyenne

Posons biais = 0. L'*erreur quadratique moyenne* (MSE, pour *mean squared error*), moyenne du carré de l'erreur sur de nombreuses occasions, est alors la variance de l'erreur. Une moyenne de k prévisions laisse la part commune intacte, tandis que la moyenne de k parts individuelles a la variance 1/k :

```text
MSE de la moyenne de k prévisions = sigma² × ( rho + (1 − rho) / k )
plancher, si grand que soit k     = rho × sigma²
```

[`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-019/analyze.py) le vérifie sans échantillonnage : avec des parts valant +1 ou −1, les 32 768 combinaisons de signes pour k = 14 donnent pour moyennes de C², de C × moyenne(I) et de moyenne(I)² exactement 1, 0 et 1/k.

**Calculé à partir de la forme close**, en unités de la MSE d'un prévisionniste (sigma² = 1), à quatre décimales :

| Prévisionnistes k | rho = 0 | rho = 0,3 | rho = 0,6 | rho = 0,9 |
|---|---|---|---|---|
| 5 | 0,2 | 0,44 | 0,68 | 0,92 |
| 14 | 0,0714 | 0,35 | 0,6286 | 0,9071 |
| plancher | 0 | 0,3 | 0,6 | 0,9 |
| 14, simulé | 0,0716 | 0,3504 | 0,6284 | 0,9061 |

**Vérification synthétique.** La dernière ligne provient de 200 000 occasions à graine fixée, avec des parts uniformes. Dans les 56 cases (k = 1 à 14), la simulation reste à moins de 1,02 erreur type de la forme close, et à au moins 82,26 erreurs types de sigma²/k dans les 39 cases où rho > 0 et k ≥ 2.

### Exercice pratique 2

Cinq prévisionnistes ont rho = 0,3. Calculez la MSE de leur moyenne et celle de cinq prévisionnistes indépendants. De ce que la moyenne peut au mieux supprimer, quelle part les cinq ont-ils supprimée ?

> **Réponse :** `0.3 + 0.7 / 5 = 0.44`, contre `1 / 5 = 0.2`. Le plancher est de 0,3 : la moyenne peut donc supprimer au plus `1 − 0.3 = 0.7` ; les cinq ont supprimé `1 − 0.44 = 0.56`, et `0.56 / 0.7 = 80%`. Cette part vaut `1 − 1/k` quel que soit rho : la corrélation ne ralentit pas le moyennage, elle réduit ce qu'il peut faire disparaître.

## 3. L'effectif contre une autre source

Appelons *équivalent indépendant* d'un groupe le nombre de prévisionnistes indépendants dont la moyenne a la même MSE : `k / (1 + (k − 1) rho)`, jamais plus de `1 / rho` (Clemen et Winkler 1985). C'est la taille d'échantillon effective de PSY-004, appliquée aux erreurs : quatorze prévisionnistes en valent 2,857 à rho = 0,3 ; 1,591 à 0,6 et 1,102 à 0,9.

Un prévisionniste de plus, du même type, abaisse la MSE de `sigma² (1 − rho) / (k (k − 1))` : en passant de 13 à 14 à rho = 0,6, la baisse est de 0,002198, soit 0,35 % (7,14 % pour des prévisionnistes indépendants).

**Synthétique.** Treize prévisionnistes à rho = 0,6 (MSE 0,6308), puis un quatorzième de même précision :

| Le quatorzième partage | Corrélation avec un membre du panel | MSE, poids égaux | MSE, poids optimaux |
|---|---|---|---|
| le contexte et le modèle | 0,6 | 0,6286 | 0,6286 |
| l'un des deux | 0,3 | 0,5888 | 0,5246 |
| ni l'un ni l'autre | 0 | 0,5490 | 0,3868 |

Les *poids optimaux* minimisent la MSE de la moyenne pondérée (Bates et Granger 1969). Avec v la MSE de la moyenne du panel, c la corrélation du nouveau venu avec un membre du panel et sigma² = 1 :

```text
poids du nouveau venu = (v − c) / (v + 1 − 2c)        MSE = (v − c²) / (v + 1 − 2c)
```

Un quatorzième qui n'a rien en commun avec le panel abaisse la MSE de 12,97 % avec une voix sur quatorze, et de 38,68 % avec son poids optimal, 0,3868 (avec c = 0, le poids, la MSE et la baisse coïncident) : les treize valent 1,585 prévisionniste et il en ajoute un.

### Exercice pratique 3

Un panel de 5 a rho = 0,6. Option A : le porter à 14 membres du même type. Option B : garder les 5 et ajouter un prévisionniste indépendant de même précision. Calculez la MSE de A, celle de B à poids égaux et celle de B avec le poids optimal.

> **Réponse :** A : `0.6 + 0.4 / 14 = 0.6286`. B à poids égaux : les cinq apportent `5 + 5 × 4 × 0.6 = 17` en variances et covariances, le prévisionniste extérieur 1 et aucune covariance, d'où `18 / 6² = 0.5`. B avec le poids optimal : `v = 0.6 + 0.4 / 5 = 0.68` et `c = 0`, donc le poids vaut `0.68 / 1.68 = 0.4048` et la MSE 0,4048. Un seul prévisionniste extérieur, avec une voix sur six, fait mieux que neuf membres supplémentaires du même type, et descend sous leur plancher de 0,6.

## 4. Ce qu'une moyenne ne peut pas supprimer, et ce que montre l'accord

**Un biais partagé.** Si tous les prévisionnistes penchent du même côté, la MSE de la moyenne vaut `bias² + sigma² (rho + (1 − rho) / k)`. **Synthétique**, avec un biais de 0,5 et rho = 0,3 : 1,25 pour un prévisionniste, 0,6 pour quatorze, au-dessus d'un plancher de 0,55. Un biais peut être estimé à partir de prévisions évaluées, puis soustrait ; la part commune change à chaque occasion et ne peut pas l'être.

### Exercice pratique 4

Avec un biais de 0,5 et rho = 0,3, une équipe de 14 peut soit doubler son effectif, à 28, soit évaluer ses prévisions passées et soustraire le biais qu'elle y trouve. Laquelle des deux options abaisse le plus la MSE ?

> **Réponse :** Aujourd'hui : `0.25 + 0.3 + 0.7 / 14 = 0.6`, dont la part du biais est `0.25 / 0.6 = 41.67%`. En doublant : `0.25 + 0.3 + 0.7 / 28 = 0.575`, soit 4,17 % de moins. En soustrayant le biais : `0.3 + 0.7 / 14 = 0.35`, soit 41,67 % de moins. La soustraction l'emporte, si le biais est stable et connu.

**L'accord.** La *dispersion* d'un panel, c'est-à-dire la distance quadratique moyenne de ses prévisions à leur propre moyenne, ne demande aucune issue. Mais la part commune s'y annule : son espérance vaut `sigma² (1 − rho) (k − 1) / k`. Avec k = 14 et rho = 0,9, les prévisions se trouvent à 0,30 de leur moyenne, tandis que cette moyenne se trouve à 0,95 de la meilleure prévision (en moyenne quadratique) ; à rho = 0, ces valeurs sont 0,96 et 0,27. **De deux panels de prévisionnistes également précis, celui dont les prévisions concordent le plus a, en espérance, la moyenne la moins précise.**

**Une lecture que la politique n'énonce pas.** Prenons 0,8 comme la probabilité p qu'un modèle ait raison sur une question fermée (oui ou non), et rho comme la corrélation entre « le modèle 1 a raison » et « le modèle 2 a raison ». Sur une question fermée, deux réponses fausses coïncident ; donc, avec q = 1 − p,

```text
P(juste | les deux concordent) = (p² + rho p q) / (p² + q² + 2 rho p q)
```

Cela donne 0,941 à rho = 0 ; 0,844 à 0,6 et 0,8 à 1, et atteint le 0,9 de la politique exactement à rho = 7/32 = 0,21875. Quand les deux divergent, chacun a raison une fois sur deux, quel que soit rho : le 0,5 de la politique.

### Exercice pratique 5

Deux personas du panel, sur un même extrait et un même `--model`, s'accordent sur la question de bloquer ou non (une lecture en oui ou non de leurs trois verdicts), et un collègue applique le 0,9 de la politique. Selon la lecture ci-dessus, calculez ce que vaut leur accord à rho = 0 et à rho = 0,6, puis tranchez.

> **Réponse :** À rho = 0 : `0.64 / 0.68 = 0.941`. À rho = 0,6 : `(0.64 + 0.6 × 0.16) / (0.68 + 2 × 0.6 × 0.16) = 0.736 / 0.872 = 0.844`. Décision : cet usage n'est pas étayé. Le 0,9 exige un rho d'au plus 0,21875 ; la règle de la politique associe des modèles de deux fournisseurs, ce que ces personas ne sont pas ; et personne n'a mesuré rho pour l'une ou l'autre paire.

**L'objection la plus forte à cette lecture** est que tous les rho sont ici inventés. Les personas jugent des préoccupations différentes ; si cela rend leurs erreurs presque indépendantes, cinq d'entre eux suppriment 80 % de la MSE d'un persona (section 2). Un extrait partagé plaide pour un rho élevé, des consignes différentes pour un rho faible : **ce module ne permet pas de distinguer un rho de 0,1 d'un rho de 0,9.** Les issues seules ne suffisent pas à trancher. **Synthétique** : sur une question fermée dont la probabilité vraie se situe entre 0,3 et 0,7, cinq personas s'en écartent de 0,21 (écart-type) ; 84 % de la MSE d'un persona tient à la part imprévisible, et `1 − (k / (k − 1)) × spread / error variance` tend vers 0,843 pour des personas qui ne partagent rien, et vers 0,937 à rho = 0,6 (90 % de 1 000 journaux de 20 pull requests : de 0,79 à 0,87, et de 0,91 à 0,95).

## Sources, limites et prochaine vérification

**Observé, épinglé au commit `4b03838800dcd4894f1e026461979bff1d985ca8` de Demerzel :** les fichiers dont les liens figurent à la section 1, le [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/tribunal-panel.yml) qui lance le panel et les cinq enregistrements du conseil. `extract.py` s'arrête si l'un d'eux diffère de son blob Git épinglé.

**Jeu d'essai.** Depuis la racine du dépôt, `python -I -B scripts/streeling_fixtures/psychohistory/psy-019/extract.py`, puis `analyze.py` et `analyze.py --check` dans le même dossier. Hypothèses : [`scenarios.json`](../../../fixtures/psychohistory/psy-019/scenarios.json). Tous les nombres ci-dessus : [`results.json`](../../../fixtures/psychohistory/psy-019/results.json). Autocontrôles et limites : [README](../../../fixtures/psychohistory/psy-019/README.md).

**Références de méthode.** Bates, J. M., et Granger, C. W. J. (1969), « The Combination of Forecasts », *Operational Research Quarterly* 20(4), 451–468, doi:10.1057/jors.1969.103. Clemen, R. T., et Winkler, R. L. (1985), « Limits for the Precision and Value of Information from Dependent Sources », *Operations Research* 33(2), 427–442, doi:10.1287/opre.33.2.427.

**Non fait.** Aucun agent n'a été exécuté et aucune issue n'a été lue : la corrélation entre les agents du projet est inconnue. Le modèle donne à tous les prévisionnistes la même précision et à toutes les paires la même corrélation, et tire des erreurs à queues légères, ce qui flatte le dimensionnement ci-dessus. La règle du panel, qui retient le verdict le plus sévère, et le minimum du conseil ne sont pas modélisés. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Prochaine vérification.** Sur chaque pull request, demander à chaque persona et à un *agent extérieur* (un agent sur un autre modèle, à qui l'on fournit d'autres éléments) la probabilité d'un événement oui ou non (un *revert* dans le mois), et enregistrer l'issue. La part imprévisible s'annule dans `(persona–persona covariance − persona–outsider covariance) / (persona variance − persona–outsider covariance)`, qui tend vers rho si l'agent extérieur ne partage rien d'autre avec le panel (moins s'il partage le contexte ou le modèle, davantage si ses erreurs vont en sens contraire de celles du panel ; le journal ne permet pas de le savoir). Dans le cadre synthétique, 500 pull requests séparent rho = 0 de rho = 0,6 (90 % des journaux : de −0,22 à 0,15, et de 0,49 à 0,67) ; 100 n'y suffisent pas. Contrairement au journal de PSY-004, celui-ci a besoin des issues. Une estimation proche de 0 ferait valoir cinq personas autant que cinq prévisionnistes ; une estimation proche de 0,6, autant que 1,471 prévisionniste, et le prochain agent devrait alors lire autre chose.
