---
module_id: dv-001-observed-degraded-stale-quality
department: data-visualization
course: Mesures, exécutions dégradées et données périmées
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-04-001
version: "0.1.0"
---

# Mesures, exécutions dégradées et données périmées

> **Département de visualisation des données** | Niveau : débutant | Durée estimée : 35 minutes | Statut : en attente de relecture

## Objectifs

À la fin de ce cours, vous saurez :

- distinguer un taux de réussite mesuré d'une exécution indisponible et d'une ancienne valeur reportée ;
- tracer une chronologie sans transformer une absence de mesure en échec ni relier silencieusement les points de part et d'autre d'une panne ;
- vérifier le dénominateur, la fraîcheur et l'environnement avant de comparer deux mesures ;
- accompagner un graphique d'une description et d'un tableau accessibles.

## La question du projet

GA conserve les snapshots du contrôle qualité de son chatbot dans `state/quality/chatbot-qa/`. Une personne qui consulte le tableau de bord demande : « Le chatbot s'est-il dégradé ? » Le graphique ne doit répondre que dans la mesure où les données le permettent. Nous utiliserons quatre **snapshots historiques**, épinglés au commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924). Ils servent d'exercice et ne décrivent pas l'état actuel du chatbot.

| Date du snapshot | `total_prompts` | `pass_pct` | `degraded` | Ce que la fiche permet de dire |
|---|---:|---:|---|---|
| [08-06-2026](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-08.json) | 52 | `null` | `true` | Le backend était indisponible ; aucun taux de réussite n'a été publié. |
| [15-06-2026](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-15.json) | 52 | 75,00 | `false` | Un taux de réussite a été publié pour cette exécution. |
| [19-06-2026](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-06-19.json) | 52 | 7,69 | `false` | Un faible taux a été publié ; ce snapshot n'en explique pas la cause. |
| [19-07-2026](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa/2026-07-19.json) | 52 | 98,08 | `false` | Un taux plus élevé a été publié pour cette exécution ultérieure. |

### Exercice

Classez chaque ligne : taux observé ou exécution indisponible. Laquelle peut être placée à 0 % sur l'axe des taux ?

> **Réponse :** Les 15 juin, 19 juin et 19 juillet ont un taux publié. L'exécution du 8 juin est indisponible. Aucune ligne ne publie un taux de 0 % ; placer le 8 juin à zéro inventerait une mesure.

## 1. Trois états différents

Une **observation** est une valeur effectivement publiée par une exécution. Une **exécution indisponible** indique que la mesure n'a pas pu être faite ou jugée fiable dans les conditions indiquées. Une **valeur reportée** est une ancienne observation rappelée pour donner du contexte : ce n'est pas une nouvelle mesure à la date affichée.

Le fichier du 8 juin contient `pass_pct: null`, `degraded: true` et `degraded_reason: "backend_unavailable"`. Il contient aussi `last_known_good_pass_pct: 94.0`, avec une date antérieure et `last_known_good_source: "carryforward"`. Ce 94 % appartient à l'observation passée. Le dessiner au 8 juin donnerait l'illusion d'une performance stable pendant la panne. Dessiner `null` à zéro donnerait l'illusion d'un échec du chatbot. Dans les deux cas, on change le sens des données.

Conservez deux champs dans le modèle du graphique : `quality_value` pour le taux mesuré et `run_status` pour l'état observé, dégradé ou inconnu. Gardez la date source d'une ancienne valeur séparée de la date à laquelle on la montre. Ne déduisez pas un taux de `total_prompts` : la note du 8 juin signale des erreurs du backend plutôt que des réponses du chatbot évaluées.

### Exercice

Une carte affiche « 94 % de réussite le 8 juin » parce que le fichier contient `last_known_good_pass_pct: 94.0`. Réécrivez-la en une phrase.

> **Réponse :** « Contrôle qualité indisponible le 8 juin : backend inaccessible ; dernière bonne mesure connue, 94 % le 16 mai. » La date historique doit être visible et le taux du 8 juin doit rester inconnu.

## 2. Séparer qualité et disponibilité

Réservez l'axe des taux aux mesures effectives. Laissez un trou quand `pass_pct` vaut `null`, au lieu de relier les points de part et d'autre. Une seconde ligne, alignée sur les dates, peut marquer l'exécution du 8 juin comme dégradée avec une icône **et un libellé**. Le lecteur obtient alors deux réponses distinctes : quelle qualité a été mesurée et si une mesure était disponible.

Pour les quatre snapshots, une esquisse textuelle suffit :

```text
Date          Qualité               Disponibilité
2026-06-08    aucun point           DÉGRADÉ : backend indisponible
2026-06-15    75,00 %               observé
2026-06-19     7,69 %               observé ; à examiner
2026-07-19    98,08 %               observé
```

Ces dates sont espacées ; elles ne forment pas quatre relevés quotidiens consécutifs. Une ligne entre le 19 juin et le 19 juillet suggérerait que les jours absents ont été mesurés et que la trajectoire était régulière. Dans la série complète, interrompez la ligne aux lacunes. Placez les points selon les dates réelles. Le [rapport historique de qualité GA au commit épinglé](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) signale aussi les données périmées : toute valeur dite « récente » a besoin de sa date de mesure.

### Exercice

Esquissez deux lignes pour les 8 et 15 juin, avec les dates et les libellés. Le 94 % reporté doit-il être relié au 75 % du 15 juin ?

> **Réponse :** Le 8 juin n'a aucun point de qualité et porte « backend indisponible ». Le 15 juin porte un point à 75 % et « observé ». Le 94 % est annoté avec sa vraie date, le 16 mai ; ce n'est ni un point du 8 juin ni le début d'un segment vers le 15 juin.

## 3. Un chiffre faible appelle une enquête

Le 19 juin affiche 7,69 % et `degraded: false`. Le graphique doit montrer ce résultat, mais ce fichier seul ne permet pas de conclure que le code GA a régressé, que le modèle a changé, que le corpus a changé ou qu'une dépendance s'est comportée différemment. `degraded: false` est la classification publiée par le producteur pour cette exécution ; ce n'est pas un certificat complet de bon fonctionnement. Il faut examiner la configuration, l'identité des prompts, les journaux du backend, les règles de notation et les exécutions voisines avant d'attribuer une cause.

Les trois lignes observées indiquent chacune 52 prompts. C'est un contexte utile, mais des comptes égaux ne prouvent pas que les questions ou la notation étaient identiques. Une comparaison devrait épingler la révision du corpus et celle de l'évaluateur. Si ces informations manquent, indiquez que la comparaison est provisoire. Un pourcentage isolé peut cacher la fragilité d'un petit échantillon.

### Exercice

Évaluez cette phrase : « GA s'est remis d'une régression logicielle confirmée entre le 19 juin et le 19 juillet. » Qu'observe-t-on ? Que faut-il encore prouver ?

> **Réponse :** Les fichiers publient 7,69 % le 19 juin et 98,08 % le 19 juillet. « S'est remis » et « régression logicielle » attribuent une cause et une continuité que ces quatre snapshots ne démontrent pas. Il faut comparer le même corpus, l'évaluateur et l'environnement, puis examiner les échecs.

## 4. Rendre le graphique lisible sans la couleur

La couleur aide, mais le marqueur d'une panne a aussi besoin d'un libellé ou d'une forme. Les [explications du W3C sur l'usage de la couleur](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color) demandent un autre indice visuel quand la couleur transmet une information. Les [explications sur les contenus non textuels](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content) rappellent qu'un graphique a besoin d'une alternative textuelle qui en restitue le sens ; un tableau peut porter les valeurs exactes.

Voici une description courte : « Contrôle qualité historique du chatbot GA : mesure indisponible le 8 juin ; taux publiés de 75 % le 15 juin, 7,69 % le 19 juin et 98,08 % le 19 juillet. La cause du faible résultat du 19 juin n'est pas établie ici. » Gardez le tableau à côté du graphique. Une personne utilisant un lecteur d'écran doit pouvoir consulter dates, valeurs et états sans déchiffrer une couleur ou une infobulle.

### Exercice

Un point rouge sans libellé marque le 8 juin. Que faut-il ajouter ?

> **Réponse :** Ajoutez un texte visible, par exemple « backend indisponible », et un libellé accessible aux technologies d'assistance. N'attribuez aucun taux au 8 juin. Fournissez un tableau ou une description équivalente avec la date et l'état.

## À retenir

- Une mesure absente n'est ni un score nul ni un score réussi.
- Une ancienne valeur reportée conserve sa date d'origine.
- La disponibilité de la mesure doit apparaître à côté de la qualité mesurée.
- Un faible taux observé peut déclencher une enquête sans prouver sa cause.
- Dates, dénominateurs, révisions des sources et texte accessible font partie de l'affirmation.

## Sources et éléments du projet

- GA : [snapshots historiques du chatbot](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/chatbot-qa) et [rapport historique des tendances](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). Ce rapport daté ne donne pas l'état actuel du système.
- W3C : [Comprendre le critère 1.4.1, usage de la couleur](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color).
- W3C : [Comprendre le critère 1.1.1, contenu non textuel](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content).

*Recherche : `data-visualization-2026-10-04-001`. La relecture du fond et des traductions reste à faire ; ce brouillon n'est pas un cours vérifié.*
