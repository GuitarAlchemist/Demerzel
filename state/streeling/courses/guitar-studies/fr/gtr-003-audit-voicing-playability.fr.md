---
module_id: gtr-003-audit-voicing-playability
department: guitar-studies
course: Examiner une affirmation sur la jouabilité d'un voicing
level: intermediate
prerequisites: ["gtr-001-the-fretboard-map", "gtr-002-caged-geometry", "gaa-004-choose-a-useful-voicing"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-studies-2026-10-05-003
version: "0.1.0"
---

# Examiner une affirmation sur la jouabilité d'un voicing

> **Département d'études de la guitare** | Intermédiaire | 45 minutes | Brouillon : révision musicale et linguistique en attente

## Objectifs

Vous calculerez un écart simple entre frettes, distinguerez les deux règles
de détection du barré de GA, chercherez un contre-exemple à une affirmation
de confort universel et préparerez un essai avec de vrais guitaristes.

## 1. Un nombre dépend de sa définition

Reprenons les trois [formes pédagogiques de do majeur](../../../fixtures/guitar-studies/gtr-003/voicing-comparison.json)
de GAA-004 : do ouvert `x 3 2 0 1 0`, forme de la `x 3 5 5 5 3` et forme
de mi `8 10 10 9 8 8`. Ce sont des exemples vérifiés par leurs notes,
**pas** des sorties capturées de GA. Leur **écart entre frettes positives est
2** : on ignore les cordes muettes (`-1`) et à vide (`0`), puis on soustrait
la plus petite frette positive de la plus grande. Les trois formes sont donc
égales selon cette mesure, alors qu'elles occupent des zones différentes du
manche et sollicitent la main différemment.

Au [commit GA `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingComfortService.cs),
`VoicingComfortService.ComputeStretch` emploie cet écart en numéros de
frettes et classe les candidats selon cette valeur. C'est un indicateur
géométrique utile, pas une mesure en millimètres, ni de la taille de la main,
de la pression nécessaire ou de la douleur. L'autre composant,
[`VoicingPhysicalAnalyzer`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs),
utilise la distance physique entre frettes comme l'une des composantes du
score de difficulté. Les deux classements peuvent donc diverger.

### Exercice 1

Calculez l'écart des frettes positives pour les formes de la et de mi.
L'égalité des résultats prouve-t-elle une distance égale en millimètres ou
un effort identique ?

> **Réponse :** Forme de la : `5 - 3 = 2` ; forme de mi : `10 - 8 = 2`.
> Cette égalité ne prouve ni une même distance physique ni une même
> disposition des doigts ou un même effort.

## 2. Lire les deux règles de barré

L'indicateur `BarreRequired` de l'analyseur cherche **trois cordes
adjacentes à la même frette positive**. Dans la forme de la, les cordes 4,
3 et 2 sont toutes à la frette 5 : l'indicateur vaut vrai. Dans la forme
de mi, la frette 8 apparaît sur les cordes 6, 2 et 1, mais jamais sur trois
cordes adjacentes : il vaut faux. Ce résultat décrit un motif détecté, pas
le doigté qu'un guitariste doit nécessairement adopter.

Le service « confort » applique une autre règle, `IsFullBarre`, quand
`excludeFullBarre` est activé : au moins quatre cordes frettées doivent
partager la plus petite frette positive. Dans la forme de la, la frette
minimale 3 apparaît deux fois ; dans la forme de mi, la frette minimale 8
apparaît trois fois. Aucune des deux ne satisfait cette règle. Pourtant,
la forme de mi se joue couramment avec un grand barré : c'est un
contre-exemple à l'interprétation « `excludeFullBarre` retire tous les
doigtés avec barré ». Les deux règles sont décrites dans le [dossier de
preuve](../../../fixtures/guitar-studies/gtr-003/README.md).

### Exercice 2

Pour chaque forme, prévoyez `BarreRequired` et si `excludeFullBarre: true`
l'exclurait **si GA renvoyait exactement ce tableau de frettes**. Pourquoi
faut-il conserver cette condition ?

> **Réponse :** Forme de la : `BarreRequired = true`, mais `IsFullBarre =
> false`. Forme de mi : les deux valent `false`. Les deux passeraient donc
> ce filtre. La condition est indispensable parce que notre jeu d'exemples
> ne démontre pas que le générateur de GA produit ces tableaux.

## 3. Confronter le modèle à un guitariste

Le score de difficulté de GA combine une distance physique entre frettes,
un indicateur de barré, la présence de cordes à vide et le nombre de
positions frettées distinctes. Il est plafonné à 10 ; les étiquettes
dépendent de seuils associés. Ces données peuvent aider à trier des
candidats, mais le code examiné ne mesure ni l'extension de la main d'une
personne, ni sa douleur, sa technique, le réglage de sa guitare ou la
netteté des notes. Même « Débutant » désigne une catégorie calculée,
pas une garantie pédagogique ou médicale.

Si vous avez une guitare, essayez chaque forme lentement. Pincez chaque
corde voulue, puis grattez l'accord. Notez `notes nettes / notes tentées`,
votre doigté, votre capacité à quitter et reprendre la forme, ainsi que
toute gêne. Arrêtez si vous avez mal. Une personne ayant une autre main ou
un autre niveau peut obtenir un résultat différent. Un seul essai peut
réfuter une affirmation universelle ; il ne prouve pas qu'une forme est
jouable pour toute une population.

### Exercice 3

Le service donne un faible score à une forme, mais votre troisième corde
frise et vous ne pouvez pas y arriver sur le temps. Que conclure ?

> **Réponse :** Le score est un indicateur calculé. Dans cet essai, il n'a
> prédit ni une exécution nette ni une transition assez rapide pour cette
> personne et ce tempo. Notez le contexte et essayez une autre forme, sans
> transformer le score en jugement universel.

## 4. Rendre la boucle d'amélioration vérifiable

Si un agent propose un nouveau poids dans le score, fixez d'abord une
révision de GA et un petit corpus de requêtes d'accords. Conservez le même
accordage et les mêmes filtres, relevez les classements avant et après,
puis faites essayer des formes à des guitaristes dans une tâche musicale
précise. Cherchez aussi les régressions : davantage de premières positions
sont-elles jouées proprement, et la modification cache-t-elle des options
utiles ? Une meilleure corrélation pour une seule personne ne règle pas
le problème. La revue doit garder les essais et les contre-exemples.

### Exercice 4

Un agent veut fusionner `BarreRequired` et `IsFullBarre` en un seul booléen.
Quelle preuve manque avant ce changement ?

> **Réponse :** Il faut définir la question à laquelle le booléen répond,
> puis comparer les deux règles à de vrais doigtés, aux observations des
> musiciens et aux contrats existants. Les formes de la et de mi montrent
> déjà leur désaccord ; les remplacer sans mesurer leurs consommateurs
> pourrait modifier les filtres et cacher des positions utiles.

## À retenir

- Un écart en numéros de frettes, un score de distance physique et
  l'expérience du musicien répondent à des questions différentes.
- Les deux règles de barré de GA ne sont pas interchangeables : nommez
  celle qui produit chaque résultat.
- Un indicateur calculé est une proposition à tester dans un contexte
  musical, pas la preuve d'un confort universel.

## Preuves et limites

Le [dossier de preuve](../../../fixtures/guitar-studies/gtr-003/README.md)
fixe le code GA et les tests ciblés. Ces derniers ont utilisé un binaire
existant : ni une nouvelle compilation GA, ni une capture du générateur pour
ces trois formes, ni un essai de musicien n'ont encore validé ce cours.
Les revues du contenu et de la traduction restent aussi à faire.
