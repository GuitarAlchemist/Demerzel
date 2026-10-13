---
module_id: cog-003-calibrating-fretboard-confidence
department: cognitive-science
course: "Étalonner sa confiance pour identifier les notes sur le manche"
level: intermediate
prerequisites: [cog-002-feedback-integrity-fretboard-recall]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: cognitive-science-2026-10-12-003
version: "0.1.0"
---

# Étalonner sa confiance pour identifier les notes sur le manche

> **Département des sciences cognitives** | Niveau intermédiaire | 40 minutes | Brouillon français ; révision et publication en attente

## Objectifs

Vous convertirez « j'en suis sûr » en une probabilité recueillie **avant** le retour, calculerez un score de Brier binaire avec une grille de réponses GA vérifiée, distinguerez six exemples inventés de résultats mesurés auprès d'apprenants et concevrez un test susceptible de réfuter une hypothèse d'étalonnage. [COG-002 (en anglais)](../en/cog-002-feedback-integrity-fretboard-recall.md) vérifie la grille affichée ; ici, nous demandons : **la confiance déclarée correspond-elle à la fréquence des bonnes réponses ?**

## La décision du projet

Imaginez un exercice GA « nommez cette note » sur un manche SVG. Deux guitaristes trouvent chacun quatre positions sur six. L'un exprime peu de confiance pour ses erreurs ; l'autre en est certain. La précision brute les classe à égalité, mais ils pourraient avoir besoin de retours différents. Pour décider, il faut définir l'événement prédit, garantir la grille et mesurer l'effet d'un éventuel retour sur de vrais apprenants.

Au commit GA [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), la [page de démonstration](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/pages/GuitarFretboardTest.tsx#L5-L13) contient six positions. Le [composant SVG](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L4-L85) numérote les cordes depuis le mi aigu (`string: 0`), définit la frette 0 comme corde à vide et accorde par défaut `E, B, G, D, A, E` de l'aigu au grave. La page ne modifie pas cet accordage. Sa sixième position affiche **C** sur la corde 5 à la frette 3 ; le mi grave plus trois demi-tons donne pourtant **G**. Il s'agit d'une incohérence du code source, pas d'une observation sur un utilisateur. La séquence corrigée est `E, C, G, E, C, G`.

La page se présente comme un test d'un ancien composant SVG. Le [gestionnaire de clic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx#L154-L157) n'envoie que corde et frette. Ces sources ne montrent ni saisie de confiance, ni séance évaluée, ni tableau d'étalonnage, ni cours déployé. **Toutes les réponses d'apprenants ci-dessous sont inventées pour l'exercice.**

## 1. Définir la prédiction avant de révéler la réponse

À chaque essai, l'apprenant choisit une note `a_i` pour une corde et une frette, puis indique `p_i` entre 0 et 1 : « Quelle est la probabilité que **ma note choisie** corresponde à la grille vérifiée ? » Ce n'est ni la probabilité qu'une guitare produise un son, ni la confiance dans l'étiquette de la démo. Consignez `a_i` et `p_i` avant d'afficher la réponse. Ensuite, `y_i=1` si `a_i` correspond à la grille, sinon `y_i=0`.

Pour établir cette grille, conservez l'ordre des cordes, l'accordage, la frette et la révision du code. Le mi grave porte l'indice 5 ; sa classe de hauteur E vaut 4. À la frette 3, `(4+3) mod 12=7`, soit G. Le C affiché à cette position ne doit pas servir de réponse sans la correction documentée dans COG-002.

L'interface nécessiterait de **nouvelles** saisies pour la note choisie et la confiance. Le clic actuel ne transmet qu'une coordonnée. Une fiche d'essai proposée serait `{source_sha, tuning, string, fret, chosen_note, confidence_before_feedback, verified_note, answer_time, feedback_time}` : c'est un plan d'étude, **pas** une API GA existante. Il faut aussi masquer la réponse avant `p_i` : les marqueurs de la démo affichent déjà leurs étiquettes.

### Exercice 1 — Définir l'événement

Un apprenant choisit C sur la corde 5 à la frette 3 avec `p=0.9`. Quelle est la note vérifiée, que vaut `y` et le clic actuel enregistre-t-il `p` ?

> **Réponse :** La corde 5 est le mi grave. `(4+3) mod 12=7` donne G ; pour C, `y=0`. Le clic n'envoie que `{string, fret}`, sans note choisie ni confiance. Cette réponse avec `p=0.9` est hypothétique.

## 2. Calculer un score sur six essais fictifs

Le **score de Brier binaire** est `BS=(1/n) Σ_i (p_i-y_i)^2`. Il va de 0 à 1 ; **plus bas est meilleur**. Contrairement au simple nombre de réponses exactes, il distingue une erreur à 0.9 de confiance d'une erreur à 0.6. Les six choix et probabilités qui suivent sont **inventés** ; seules les coordonnées, l'accordage et la grille corrigée proviennent de GA.

| Essai | Corde, frette | Note vérifiée | Choix fictif | `p_i` | `y_i` | `(p_i-y_i)^2` |
|---:|---|---|---|---:|---:|---:|
| 1 | 0, 0 | E | E | 0.9 | 1 | 0.01 |
| 2 | 1, 1 | C | C | 0.8 | 1 | 0.04 |
| 3 | 2, 0 | G | A | 0.7 | 0 | 0.49 |
| 4 | 3, 2 | E | E | 0.6 | 1 | 0.16 |
| 5 | 4, 3 | C | C | 0.9 | 1 | 0.01 |
| 6 | 5, 3 | G | C | 0.9 | 0 | 0.81 |

Ce personnage fictif réussit `4/6≈0.6667`. La somme des pertes est `0.01+0.04+0.49+0.16+0.01+0.81=1.52`, donc `BS=1.52/6≈0.2533`. Rien ici n'estime la capacité d'une vraie personne. Si l'on utilisait à tort le C affiché comme réponse à l'essai 6, sa perte deviendrait 0.01 au lieu de 0.81 et le score apparent tomberait à `(1.52-0.81+0.01)/6=0.12`. Un bon score ne corrige pas une mauvaise grille.

### Exercice 2 — Calculer le score

Calculez la précision brute, la somme des pertes et le score moyen. Quelle erreur coûte le plus ?

> **Réponse :** Quatre bonnes réponses sur six donnent `4/6≈0.6667`. La somme vaut `1.52` et le score `1.52/6≈0.2533`. L'essai 6 coûte `0.81`, plus que les `0.49` de l'essai 3, car sa mauvaise réponse était accompagnée de 0.9 de confiance au lieu de 0.7.

### Exercice 3 — Examiner une classe de confiance

Parmi les essais à `p_i=0.9`, quelle proportion est correcte et de combien est-elle inférieure à 0.9 ? Cela suffit-il pour établir un étalonnage stable ?

> **Réponse :** Les essais 1, 5 et 6 sont à 0.9 ; deux sont corrects, soit `2/3≈0.6667`. L'écart vaut `0.9-2/3≈0.2333`. Trois essais fictifs et liés ne suffisent pas à établir une courbe individuelle stable.

### Exercice 4 — Repérer une grille contaminée

Si l'essai 6 était évalué contre le C affiché plutôt que G, que deviendraient son résultat, sa perte et la moyenne ? Cela prouverait-il que l'apprenant s'est amélioré ?

> **Réponse :** Le choix C serait marqué `y_6=1` ; la perte passerait de `(0.9-0)^2=0.81` à `(0.9-1)^2=0.01`. La somme serait `0.72`, la moyenne `0.72/6=0.12`. La prédiction n'a pas changé : seule la grille erronée crée l'amélioration apparente.

## 3. Pourquoi minimiser cette erreur quadratique ?

Soit `q` la probabilité réelle de justesse pour une catégorie donnée d'essais futurs, et `p` la probabilité annoncée. La perte de Brier attendue est `q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q)`. Le second terme ne dépend pas de `p` : le minimum unique est atteint pour `p=q`. Le score récompense donc des probabilités sincères **en espérance**, sans garantir qu'une personne bien étalonnée gagne sur chaque échantillon de six essais. Il ne diagnostique pas à lui seul une inversion des cordes, un oubli ou un retour trompeur.

Si `q=0.7` dans un exemple hypothétique, annoncer `p=0.7` donne `0.7(0.3)^2+0.3(0.7)^2=0.21` de perte attendue ; `p=0.9` donne `0.7(0.1)^2+0.3(0.9)^2=0.25`, soit 0.04 de plus, `(0.9-0.7)^2`. Les six essais fictifs n'établissent **pas** que le véritable `q` des guitaristes vaut 0.7.

Un score inférieur ne signifie pas forcément une meilleure connaissance des notes : se rapprocher de 0.5 partout peut réduire le coût des erreurs trop confiantes sans identifier plus de notes. Consignez aussi la précision, les cordes et frettes, et les probabilités originales **avant** retour. Les modifier après le retour fausserait la mesure de la prévision initiale.

### Exercice 5 — Vérifier le sens du score

Avec `q=0.7` hypothétique, comparez les pertes attendues pour `p=0.7` et `p=0.9`. Laquelle est moindre et de combien ?

> **Réponse :** Pour `p=0.7`, `0.7(1-0.7)^2+0.3(0.7)^2=0.21`. Pour `p=0.9`, `0.7(1-0.9)^2+0.3(0.9)^2=0.25`. La différence est 0.04 en faveur de `p=0.7`. Les six essais n'ont pas mesuré `q`.

## 4. Concevoir un essai qui pourrait échouer

Hypothèse à tester : **un retour explicite sur l'étalonnage de la confiance, après chaque réponse vérifiée, réduit le score de Brier sur des positions inédites le lendemain sans diminuer la précision des notes**, comparé à l'affichage de la bonne note seule. Dans les deux groupes, note choisie et confiance doivent être recueillies avant le retour. Le groupe « étalonnage » pourrait voir sa confiance, la justesse et un score cumulatif ; le groupe témoin verrait la même note vérifiée et la justesse sans résumé de confiance. Ce dispositif est proposé, il n'existe pas dans la page GA épinglée.

Corrigez d'abord la mauvaise étiquette ou utilisez une grille vérifiée séparément. Créez deux états de question sans étiquette de note, avec le même accordage, afin que personne ne voie la réponse avant de prédire. Recrutez de vrais apprenants, consignez leur consentement et expérience, puis répartissez-les avant l'entraînement. Contrebalancez les positions entre conditions et réservez des positions inédites pour le lendemain. Enregistrez révision source, question, réponse, confiance, heure de réponse, retour affiché et délai exact. Reconnaître une coordonnée sur un dessin ne prouve pas que l'on sait jouer ou entendre la note.

Déclarez à l'avance le critère principal : score moyen de Brier le lendemain sur les positions réservées, avec précision des notes comme garde-fou. L'hypothèse **n'est pas soutenue** si le groupe « étalonnage » ne baisse pas ce score face au témoin, ou si un gain de score s'accompagne d'une précision plus faible selon le garde-fou annoncé. Rapportez incertitude, nombre d'apprenants et nombre de questions. Un pilote peut révéler une interface mal comprise ou un effet plafond ; il faudrait alors réviser l'étude, sans annoncer un succès après coup. **Aucune** de ces séances, répartitions ou mesures n'a été réalisée pour ce cours.

### Exercice 6 — Donner un résultat réfutant l'hypothèse

Un agent affirme : « Le score fictif de `0.2533` prouve que notre retour sur la confiance améliore le rappel. » Donnez deux raisons pour lesquelles c'est injustifié et un résultat concret qui ferait échouer l'hypothèse de l'étude.

> **Réponse :** Les six probabilités et réponses ont été inventées ; la page GA n'a ni intervention sur la confiance ni mesure le lendemain. L'hypothèse échoue si le groupe « étalonnage » n'obtient pas un score de Brier inférieur le lendemain sur les positions réservées, ou si un score plus faible s'accompagne d'une baisse de précision selon le garde-fou prévu. Il faut une grille corrigée et des probabilités saisies avant le retour.

## Limites des preuves

Les sources GA épinglées établissent les six coordonnées, l'ordre des cordes, les étiquettes visibles et les données envoyées au clic. La grille corrigée et les calculs de Brier sont vérifiables. Les six choix et probabilités, `q=0.7`, les variantes d'interface et l'étude sont des constructions pédagogiques. Il n'y a ici ni confiance mesurée auprès d'apprenants, ni bénéfice d'intervention, ni exécution dans le navigateur, ni revue du sujet ou des langues, ni build Learn ou lecture publique. Il faudra des artefacts et des réviseurs distincts avant de qualifier ce brouillon de cours revu ou publié.
