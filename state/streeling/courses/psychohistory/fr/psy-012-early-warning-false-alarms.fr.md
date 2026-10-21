---
module_id: psy-012-early-warning-false-alarms
department: psychohistory
course: "Les signaux d'alerte précoce et leurs fausses alertes"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-008-probability-conditional-reasoning", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-012
version: "0.1.0"
---

# Les signaux d'alerte précoce et leurs fausses alertes

> **Département de psychohistoire** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue de fond et essai apprenant en attente

## Objectifs et question de projet

Vous calculerez deux indicateurs glissants, la variance et l'autocorrélation d'ordre 1, vous résumerez chaque tendance par une statistique de rang, et vous mesurerez une règle d'alerte des deux côtés : à quelle fréquence elle se déclenche quand un système approche d'un point de bascule, et à quelle fréquence quand rien n'approche. **Question de projet :** PSY-002 propose des signaux annonçant un changement de régime ; à quelle fréquence une variance et une autocorrélation en hausse apparaissent-elles dans un système qui n'approche d'aucune transition ?

[PSY-002](psy-002-governance-phase-transitions.fr.md), qui s'appuie sur [PSY-001](psy-001-intro-fractal-compounding.fr.md), énumère six signaux et demande que trois d'entre eux ou plus convergent. Ce module prend les deux indicateurs d'alerte précoce les mieux étudiés de la littérature et mesure, pour ces deux-là, ce que PSY-002 ne donne pas pour ses six : un taux de fausses alertes. Les sections 1 à 3 sont **synthétiques** : des entrées supposées, dans [scenarios.json](../../../fixtures/psychohistory/psy-012/scenarios.json), un calcul fait par [analyze.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/analyze.py), des résultats enregistrés dans [results.json](../../../fixtures/psychohistory/psy-012/results.json). Seule la section 4 utilise des données **observées** du projet. Les changements d'instrument relèvent de [PSY-011](psy-011-measurement-change-or-system-change.fr.md), le chaos de [PSY-014](psy-014-prediction-horizons.fr.md).

## 1. Pourquoi un système ralentit avant de basculer

Une *bifurcation pli* (ou bifurcation nœud-col) est le point de bascule le plus simple : quand un *paramètre de contrôle* q varie, un état de repos stable et un seuil instable se rapprochent, se rejoignent et disparaissent, et le système saute ailleurs. Le jeu d'essai utilise la forme classique des manuels, dx/dt = r + x², écrite avec r = −q², à laquelle on ajoute du bruit :

```text
x[t+1] = x[t] + h * (x[t]^2 - q[t]^2) + e[t]      h = 0.005, e ~ Normale(0, 1)
état de repos x = -q     seuil instable x = +q     pli en q = 0
```

Près de l'état de repos, une petite perturbation d se réduit d'un facteur fixe à chaque pas :

```text
d[t+1] ≈ phi * d[t]       phi = 1 - 2 * h * q
variance = 1 / (1 - phi^2)       autocorrélation d'ordre 1 = phi
```

La seconde ligne est le résultat classique pour un *processus AR(1)*, où chaque valeur vaut phi fois la précédente plus un bruit nouveau ; l'*autocorrélation d'ordre 1* est la corrélation entre la série et elle-même décalée d'un pas. Quand q diminue vers 0, phi monte vers 1 : le retour à l'état de repos ralentit, si bien que les fluctuations durent plus longtemps (l'autocorrélation augmente) et s'accumulent (la variance augmente). Ce *ralentissement critique* est le mécanisme qui sous-tend les signaux d'alerte précoce passés en revue par Scheffer et al. (2009).

Dans le jeu d'essai, q décroît linéairement de 50 à 10 et n'atteint jamais le pli : à la fin, le seuil instable se trouve encore à 8,72 écarts-types des fluctuations, et aucune simulation d'approche ne l'a franchi.

L'estimateur (section 2) est d'abord éprouvé sur des réponses connues. Sur 200 000 points d'un AR(1) stationnaire avec phi = 0,9, il renvoie une variance de 5,2742 (théorie : 5,2632) et une autocorrélation de 0,9002 ; le simulateur du pli maintenu à q = 25 renvoie 0,7513 pour une valeur prédite de 0,75. Les fenêtres courtes donnent des valeurs trop basses : sur 1 000 simulations **synthétiques** avec phi = 0,9, l'autocorrélation estimée moyenne vaut 0,555 dans une fenêtre de 25 points, 0,7279 à 50, 0,8641 à 200 et 0,8913 à 800, et la variance moyenne à 25 points vaut 1,7243 pour une vraie valeur de 5,2632. Le biais est le plus fort pour un système lent, là où le signal est censé apparaître.

### Exercice pratique 1

Calculez phi, la variance et l'écart-type des fluctuations au début (q = 50) et à la fin (q = 10) de l'approche. Par quel facteur la variance est-elle multipliée ? Combien de pas faut-il pour perdre la moitié d'une perturbation à chaque extrémité (résolvez phi^k = 0,5) ?

> **Réponse :** Au début : phi = 1 − 2 × 0,005 × 50 = 0,5 ; variance 1 / (1 − 0,25) = 1,3333 ; écart-type 1,1547. À la fin : phi = 0,9 ; variance 1 / (1 − 0,81) = 5,2632 ; écart-type 2,2942. La variance est multipliée par 3,9474. Avec k = ln 0,5 / ln phi, la moitié d'une perturbation est perdue en 1 pas au début et en 6,58 pas à la fin.

## 2. Deux indicateurs glissants et un nombre pour la tendance

Un analyste dispose d'une seule série et ne voit pas q. La recette habituelle (Dakos et al. 2012) fait glisser le long de la série une *fenêtre* de W points consécutifs et calcule les deux indicateurs à chaque position. Le jeu d'essai retire d'abord, dans chaque fenêtre, la droite la mieux ajustée : le niveau de repos lui-même dérive, ici de 34,64 écarts-types initiaux, et un niveau qui dérive serait compté comme de la variance.

```text
e[u] = y[u] - (a + b * u)        u = 0 .. W-1
variance        = sum(e[u]^2) / (W - 2)
autocorrélation = sum(e[u] * e[u+1]) / sum(e[u]^2)
```

Une série de n points donne m = n − W + 1 valeurs glissantes de chaque indicateur. Le *tau de Kendall*, une corrélation de rang avec le temps, dit en un seul nombre si elles montent : parmi les P = m(m − 1)/2 paires de positions, C sont concordantes (la valeur la plus tardive est la plus grande), D discordantes (elle est la plus petite) et t ex æquo (les deux valeurs sont égales). Le programme calcule la forme corrigée pour les ex æquo, le tau-b.

```text
tau = (C - D) / sqrt(P * (P - t))       +1 toujours croissant, -1 toujours décroissant
    = (C - D) / P                       quand il n'y a pas deux valeurs égales (t = 0)
M   = min(tau de la variance, tau de l'autocorrélation)       alerte quand M >= T
```

M exige que les deux indicateurs montent, comme le fait la convergence de PSY-002. Trois seuils T sont comparés :

- **test usuel** : chaque tau doit être « significatif à 5 % » selon la formule unilatérale standard, qui traite les m valeurs comme indépendantes : T = 1,645 × sqrt(2(2m + 5) / (9m(m − 1))) ;
- **seuil fixe** : T = 0,5 ;
- **seuil calibré** : T est la valeur qu'atteignent 5 % de 1 000 simulations stationnaires distinctes (AR(1), phi = 0,7, mêmes n et W), selon l'idée des séries de substitution de Dakos et al. (2012).

### Exercice pratique 2

Six valeurs glissantes consécutives valent 0,8 ; 0,5 ; 1,1 ; 1,4 ; 1,2 ; 1,9 (inventées). Comptez les paires concordantes et discordantes et calculez tau. Cet indicateur atteint-il à lui seul T = 0,5 ?

> **Réponse :** 6 × 5 / 2 = 15 paires. Deux sont discordantes, (0,8 ; 0,5) et (1,4 ; 1,2), donc C = 13, D = 2 et tau = (13 − 2) / 15 = 0,7333, au-dessus de 0,5.

## 3. Détection et fausses alertes, mesurées

Pour chaque longueur de relevé n et chaque fenêtre (un quart et la moitié de n), le jeu d'essai a lancé 1 000 simulations d'approche et 1 000 simulations de chaque témoin stationnaire : un AR(1) avec phi = 0,5 ; 0,7 et 0,9. Le *taux de détection* est la part des simulations d'approche dans lesquelles l'alerte se déclenche ; le *taux de fausses alertes* est cette même part parmi les simulations témoins. Chaque taux, pour un seuil donné, a une erreur type d'au plus 1,58 point de pourcentage ; les seuils calibrés, estimés à partir de 1 000 simulations et affichés avec deux décimales, ajoutent leur propre erreur. Toutes les valeurs sont des pourcentages **synthétiques** ; les fausses alertes sont données pour phi = 0,5/0,7/0,9.

| n/W | Test usuel : fausses alertes | Seuil fixe : détection | Seuil fixe : fausses alertes | T calibré | Seuil calibré : détection | Seuil calibré : fausses alertes |
|---|---|---|---|---|---|---|
| 100/25 | 21,6/21,4/26,7 | 6,0 | 0,9/2,0/2,2 | 0,40 | 12,4 | 4,4/4,8/5,0 |
| 100/50 | 26,5/29,2/32,8 | 29,7 | 8,7/11,3/10,7 | 0,63 | 18,9 | 3,4/5,2/4,7 |
| 400/100 | 28,6/30,7/36,9 | 49,8 | 2,6/4,5/4,1 | 0,46 | 55,8 | 3,7/5,6/5,1 |
| 400/200 | 30,8/32,9/41,5 | 78,2 | 9,6/11,3/15,1 | 0,64 | 65,3 | 4,6/4,5/6,1 |
| 1 600/400 | 31,2/35,8/40,7 | 97,6 | 3,1/3,9/5,5 | 0,50 | 97,6 | 3,1/3,9/5,5 |
| 1 600/800 | 33,2/38,2/43,7 | 99,6 | 11,0/14,0/17,2 | 0,66 | 99,0 | 4,4/6,4/8,0 |

Quatre lectures :

1. **La question de projet.** Dans les témoins stationnaires, les deux tau sont positifs dans 334 à 461 simulations sur 1 000, et le test usuel, nominalement à 5 % au plus, se déclenche dans 21,4 % à 43,7 % des simulations. Des fenêtres voisines ont tous leurs points en commun sauf un, de sorte que m valeurs glissantes sont loin de valoir m observations indépendantes.
2. **Le seuil dépend de la fenêtre.** T = 0,5 donne de 0,9 % à 5,5 % de fausses alertes avec les fenêtres d'un quart de n, et de 8,7 % à 17,2 % avec celles de la moitié de n.
3. **Près de 5 % de fausses alertes, la détection dépend de la longueur du relevé.** La règle à seuil calibré détecte cette approche dans 12,4 % à 18,9 % des simulations à 100 points, dans 55,8 % à 65,3 % à 400 points, et dans 97,6 % à 99,0 % à 1 600 points (un relevé plus long est ici le même changement de q étalé sur davantage de pas : une approche plus lente).
4. **Le seuil calibré est une estimation.** Sur de nouvelles simulations à phi = 0,7, il se déclenche dans 3,9 % à 6,4 % des cas, et sur l'ensemble des trois témoins dans 3,1 % à 8,0 % ; 1 000 simulations ne séparent pas son erreur d'échantillonnage d'une dépendance à phi.

Deux vérifications. Un jumeau linéaire (un AR(1) dont le coefficient suit le même chemin de 0,5 à 0,9, sans niveau mobile ni pli) a un taux de déclenchement à moins de 3,7 points de pourcentage de celui du pli, dans chaque ligne et pour chaque règle ; les détections viennent donc du ralentissement. Sans le retrait de la droite, la détection par la règle à seuil fixe à n = 400, W = 200 tombe de 78,2 % à 3,3 %.

### Exercice pratique 3

À n = 100, W = 50, la règle à seuil fixe s'est déclenchée dans 297 des 1 000 simulations d'approche et dans 113 des 1 000 simulations stationnaires (phi = 0,7). Supposons que 1 système surveillé sur 10 approche réellement d'un pli. Quelle part des alertes est vraie ?

> **Réponse :** P(alerte) = 0,1 × 0,297 + 0,9 × 0,113 = 0,1314 ; la part vraie est 0,0297 / 0,1314 = 0,226, soit environ 23 alertes sur 100.

### Exercice pratique 4

Un collègue applique le test usuel à un relevé de 400 points avec W = 200, trouve les deux indicateurs « significatifs à 5 % » et conclut que le hasard est exclu. Qualifiez cette affirmation, puis indiquez le seuil que vous exigeriez et ce qu'il coûte.

> **Réponse :** Non étayée. Sur des séries stationnaires avec phi = 0,7, ce test se déclenche dans 32,9 % des simulations, et non 5 % : il suppose des valeurs indépendantes alors que les fenêtres glissantes se chevauchent. Exigez un seuil calibré sur un modèle stationnaire ajusté à ce relevé. Dans la configuration même du jeu d'essai, c'est M ≥ 0,64, qui s'est déclenché dans 4,5 % des simulations témoins indépendantes et a détecté 65,3 % des approches : environ une approche réelle sur trois est manquée.

## 4. Ce que la tendance de qualité enregistrée peut montrer, et ce qu'elle ne peut pas montrer

**Observé.** La [tendance de qualité](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend) épinglée du dépôt contient 1 548 lignes : 18 artefacts de gouvernance enregistrés lors de 88 exécutions réparties sur 83 jours. [extract.py](../../../../../scripts/streeling_fixtures/psychohistory/psy-012/extract.py) compare chaque fichier source à son blob Git et écrit [observed-input.json](../../../fixtures/psychohistory/psy-012/observed-input.json). Chaque artefact compte de 81 à 87 exécutions qui portent les trois nombres ; les lignes de la première exécution, en mai, n'en portent aucun. **Calculé** à partir de cet extrait :

- `compliance_rate` et `violation_count` : les 18 séries gardent toutes une valeur unique ; 0 changement dans 1 519 paires de lignes consécutives d'un même artefact ([PSY-005](psy-005-persistence-baseline.fr.md) en compte 1 518 : l'une de ces paires part d'une ligne sans étiquette).
- `citation_count` : 2 séries sont constantes ; les 16 autres changent, 20 fois sur 1 519 paires, et les 20 changements tombent tous sur deux exécutions (16 séries le 2026-09-13, 4 le 2026-10-03).

Ce relevé peut montrer la persistance, sujet de [PSY-005](psy-005-persistence-baseline.fr.md), et deux sauts datés ; savoir si ces sauts viennent de l'instrument ou du système est la question de PSY-011.

Il ne peut montrer aucun des deux signaux d'alerte précoce. Dans une fenêtre dont toutes les valeurs sont égales, la variance vaut 0 et l'autocorrélation vaut 0 / 0 : indéfinie, et non faible. C'est le cas de toutes les fenêtres de deux des champs et de 689 des 1 105 fenêtres de 25 exécutions pour les nombres de citations ; ailleurs, la seule variation est un saut. Le ralentissement critique concerne le retour à l'état de repos après de nombreux petits chocs, et un compteur qui n'enregistre aucun petit choc ne porte aucune vitesse de retour. Le jeu d'essai ne calcule donc aucun indicateur sur les données du projet, et l'absence de tendance n'indique ni que le système de gouvernance est loin d'un changement de régime, ni qu'il en est proche. Même une série fluctuante de cette longueur (81 à 87 points) serait courte au regard de la simulation, et les taux simulés reposent sur une approche et une échelle de temps supposées, sans équivalent dans le projet.

### Exercice pratique 5

Dans observed-input.json, les nombres de citations de `policies / alignment-policy.yaml` valent 3 pendant 55 exécutions, puis 42 pendant 21 exécutions, puis 44 pendant 11 exécutions. Combien de fenêtres de 25 exécutions cette série compte-t-elle, et combien sont constantes ? Que valent les deux indicateurs dans une fenêtre constante ? Faut-il lancer le test de tendance ? Énoncez votre critère.

> **Réponse :** 87 − 25 + 1 = 63 fenêtres. Une fenêtre n'est constante qu'à l'intérieur d'un seul segment ; les segments de 21 et de 11 exécutions sont plus courts que 25, si bien que seules les 55 premières exécutions conviennent : 55 − 25 + 1 = 31 fenêtres. Les 32 autres chevauchent un saut. Dans une fenêtre constante, la variance vaut 0 et l'autocorrélation vaut 0 / 0, indéfinie. Ne lancez pas le test : les indicateurs ont besoin de fluctuations à l'intérieur de chaque fenêtre, et ici toute la variation tient en deux sauts.

## Sources, limites et prochaine vérification

**Sources.** Observé : le dossier épinglé de la tendance de qualité ; le [README](../../../fixtures/psychohistory/psy-012/README.md) du jeu d'essai donne les commandes. Références de méthode : Scheffer et al. (2009), « Early-warning signals for critical transitions », *Nature* 461, 53–59, [doi:10.1038/nature08227](https://doi.org/10.1038/nature08227) ; Dakos et al. (2012), « Methods for detecting early warnings of critical transitions in time series illustrated using simulated ecological data », *PLoS ONE* 7(7), e41010, [doi:10.1371/journal.pone.0041010](https://doi.org/10.1371/journal.pone.0041010) ; Boettiger et Hastings (2012), « Quantifying limits to detection of early warning for critical transitions », *Journal of the Royal Society Interface* 9, 2527–2539, [doi:10.1098/rsif.2012.0125](https://doi.org/10.1098/rsif.2012.0125) ; Boettiger et Hastings (2012), « Early warning signals and the prosecutor's fallacy », *Proceedings of the Royal Society B* 279, 4734–4739, [doi:10.1098/rspb.2012.2085](https://doi.org/10.1098/rspb.2012.2085).

**Limites.** Une seule approche (phi de 0,5 à 0,9), un seul niveau de bruit, un niveau qui dérive en ligne droite par construction. Les témoins sont uniquement des AR(1) stationnaires : un bruit qui change, une saisonnalité, un changement d'instrument, ou le fait de choisir les cas après qu'un changement de régime s'est produit (le sophisme du procureur) peuvent chacun faire monter les indicateurs sans aucune transition ; ces taux décrivent donc la forme la plus favorable de « rien n'approche ». La règle M et le retrait de la tendance à l'intérieur de chaque fenêtre sont des simplifications propres à ce jeu d'essai, non la procédure d'un article cité. Aucun humain n'a relu le fond de cette leçon et aucun apprenant ne l'a essayée.

**Objection la plus forte.** La faible détection à 100 points tient peut-être à cette recette, et non à l'alerte précoce en tant que telle : un test de vraisemblance fondé sur un modèle, du type que défendent Boettiger et Hastings, exploite les données plus efficacement, et un relevé qui se termine plus près du pli porte un signal plus fort. Lancer un tel test, ainsi qu'une approche menée plus près du pli, sur les mêmes séries à graines fixées, à taux de fausses alertes égaux, trancherait la question ; cela n'a pas été fait.

**Prochaine vérification.** Une grandeur mesurée à chaque exécution, qui change dans la plupart des paires consécutives et qui serait enregistrée avec un instrument inchangé pendant plusieurs centaines d'exécutions, permettrait de calibrer une telle règle pour le projet. Même alors, une règle silencieuse n'exclurait pas une transition : à 400 points, elle a détecté 55,8 % à 65,3 % des approches simulées.
