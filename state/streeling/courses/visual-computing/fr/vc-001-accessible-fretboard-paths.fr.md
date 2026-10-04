---
module_id: vc-001-accessible-fretboard-paths
department: visual-computing
course: Un manche, trois modes d'accès
level: beginner
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-04-001
version: "0.1.0"
---

# Un manche, trois modes d'accès

> **Département de visual computing** | Niveau : débutant | Durée estimée : 35 minutes | Statut : en attente de relecture

## Objectifs

À la fin de ce cours, vous saurez :

- décrire une position de guitare sans dépendre du marqueur dessiné ;
- distinguer un diagramme informatif d'une commande interactive ;
- donner accès à la même information et, lorsqu'elle existe, à la même action avec la souris, le clavier et un lecteur d'écran ;
- définir des vérifications comparables pour les rendus SVG, Canvas et 3D.

## La question du projet et l'exemple fixe

Une personne peut-elle repérer une position sur un manche GA et, si la sélection est possible, l'activer avec la souris, le clavier ou un lecteur d'écran ? Au commit GA [`dc2e74c`, le composant partagé `GuitarFretboard`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx) dessine des marqueurs SVG. Chaque cercle gère le survol et le clic à la souris. Dans le code inspecté, il n'a ni activation au clavier, ni nom, rôle ou cible de focus explicites. Le [rendu Canvas](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx) attache des événements pointer aux objets Pixi. Le [composant qui choisit le rendu](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx) transmet les callbacks de position aux branches SVG, Canvas et 3D.

Il s'agit d'une lecture du code, pas d'un audit effectué dans le navigateur ou avec une technologie d'assistance. Dans [la carte de voicing de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx), aucun callback de clic n'est fourni au diagramme : cette utilisation sert à informer, pas à sélectionner. Il serait trompeur d'annoncer une action inexistante.

Gardons les deux positions suivantes, avec l'accordage standard. Dans GA, l'index des cordes commence à zéro, la corde de mi aigu en premier. Pour le guitariste, ce sont les cordes 1 et 2.

| Position GA | Description pour le guitariste | Note attendue |
|---|---|---|
| `{ string: 0, fret: 3, label: "G" }` | Corde 1 (mi aigu), case 3, sol | Sol |
| `{ string: 1, fret: 1, label: "C" }` | Corde 2 (si), case 1, do | Do |

### Exercice

Le SVG n'inscrit que `G` dans le premier marqueur. Que manque-t-il, et pourquoi ne faut-il pas annoncer « corde 0 » ?

> **Réponse :** `G` ne donne ni la corde ni la case. L'index `0` est une convention du code ; le guitariste attend « corde 1, case 3, sol ».

## 1. Séparer la position de son dessin

La source de vérité d'une position réunit le contexte de l'instrument et de l'accordage, la corde, la case, la note lorsqu'elle est connue et la possibilité de sélectionner. Cercle SVG, objet Pixi et objet 3D ne sont que des représentations de ces données. La version textuelle doit venir des mêmes données, pas des coordonnées à l'écran ou d'une légende rédigée séparément. Un capodastre, un mode gaucher ou un autre accordage peut sinon rendre le texte incohérent avec l'image.

Pour cet exemple : « Accordage standard. Deux positions marquées : corde 1, case 3, sol ; corde 2, case 1, do. » Une liste voisine peut détailler chaque position. Si le clic sélectionne une position, la liste doit offrir une commande qui appelle la même action. Si le diagramme illustre seulement un voicing, du texte suffit. Les [explications du W3C sur les contenus non textuels](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) demandent de transmettre le sens de l'image ; le seul nom du diagramme ne décrit pas ses positions.

### Exercice

Un développeur ajoute `aria-label="Manche de guitare"` au SVG. Le lecteur peut-il retrouver les deux positions grâce à ce seul nom ?

> **Réponse :** Non. Le nom du diagramme ne donne ni les cordes, ni les cases, ni les notes. Il faut une description ou une liste structurée, ainsi que les commandes de sélection si elles existent.

## 2. Donner la même action selon le rôle du diagramme

Si un marqueur appelle `onPositionClick`, le clavier doit aussi permettre cette sélection. Le critère [Keyboard de WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) porte sur la fonctionnalité : une liste de vrais boutons HTML à côté du SVG peut fournir le chemin clavier. « Sélectionner corde 1, case 3, sol » peut appeler le même callback que le clic. Le focus doit être visible et l'état sélectionné communiqué. Les boutons natifs fonctionnent avec Tab, Entrée et Espace. Une grille ARIA n'est justifiée que si sa navigation et son focus suivent réellement le [modèle de grille WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/patterns/grid/) et sont testés.

Dans le [code SVG de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx), le curseur du marqueur suggère un clic même quand le callback est absent. Dans une carte de voicing purement informative, un bouton « Sélectionner » inventerait une fonction. Le critère porte sur l'équivalence des fonctions *réellement proposées*.

### Exercice

Nommez les deux boutons d'une version interactive et dites ce que fait Entrée. Que devient la liste dans la carte de voicing informative ?

> **Réponse :** « Sélectionner corde 1, case 3, sol » et « Sélectionner corde 2, case 1, do ». Entrée appelle la même sélection que la souris. Dans la carte informative, la liste décrit les positions sans boutons ni faux état sélectionné.

## 3. Exposer le nom et l'état des commandes

Pour une commande personnalisée, le critère [Name, Role, Value de WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) exige un nom et un rôle déterminables par programme, ainsi que l'état pertinent. Un cercle avec `onClick` reste un élément dessiné muni d'un gestionnaire ; le `G` visible ne dit pas forcément à une technologie d'assistance qu'il y a une action ni à quelle case elle correspond. Une petite liste de boutons HTML à côté du rendu est une option simple. Si la sélection persiste, affichez la position choisie en texte et exposez son état. Ne confondez pas le survol avec la sélection.

Utilisez les mêmes mots dans les rendus SVG, Canvas et 3D. Les pixels Canvas et les objets 3D ne fournissent pas à eux seuls une liste textuelle navigable. Une liste commune reste disponible après un changement de rendu. C'est une proposition pour GA, pas une fonctionnalité déjà constatée.

### Exercice

Un lecteur d'écran annonce seulement « G » ; la personne à la souris voit la corde de mi aigu, case 3. Que manque-t-il ?

> **Réponse :** Il manque au minimum la corde, la case et la note en contexte. Si le marqueur sert à sélectionner, il faut aussi une commande identifiable, utilisable au clavier et dotée de l'état sélectionné. S'il informe seulement, ne lui donnez pas un rôle d'action.

## 4. Vérifier les trois chemins avec les mêmes données

Chargez les deux positions dans chaque mode de rendu. Dans la variante interactive, cliquez sur le premier marqueur, puis activez son bouton au clavier avec Entrée et Espace : la position sélectionnée doit être la même. Vérifiez que le lecteur d'écran annonce les deux noms complets et l'état utile. Dans la variante informative, les deux positions doivent rester lisibles, sans fausses commandes. Changez de rendu et vérifiez que le focus garde un chemin prévisible. Les assertions sur l'arbre d'accessibilité du navigateur aident, mais une vérification manuelle avec un lecteur d'écran reste nécessaire.

Le [fichier Playwright inspecté](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts) vérifie le rendu et les erreurs de console ; il ne prouve pas ces trois chemins. Notez navigateur, lecteur d'écran, mode de rendu et résultat avant de déclarer l'exercice réussi.

### Exercice

Le test trouve le SVG et aucune erreur de console. Le critère VC-001 est-il satisfait ? Quelles observations manquent ?

> **Réponse :** Non. Il faut vérifier les descriptions, la sélection à la souris lorsqu'elle existe, la sélection au clavier, les noms et états annoncés, puis la cohérence en Canvas et en 3D. Indiquez les modes ou combinaisons de technologies non testés.

## À retenir

- Le sens musical d'une position doit rester accessible sans les pixels.
- Un diagramme informatif donne les données ; un diagramme interactif donne aussi une action clavier équivalente.
- Un modèle commun peut garder les rendus SVG, Canvas, 3D et texte cohérents.
- La lecture du code révèle un risque ; les essais en navigateur et avec lecteur d'écran vérifient le comportement.

## Sources et éléments du projet

- GA : [manche SVG partagé](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/GuitarFretboard.tsx), [Canvas](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/RealisticFretboard.tsx), [choix du rendu](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/src/components/StringedInstrumentFretboard.tsx), [carte de voicing](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-client/src/components/SmartVoicingDisplay.tsx) et [tests Playwright](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/ReactComponents/ga-react-components/tests/fretboard.spec.ts), commit `dc2e74c`.
- W3C : [Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html), [Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) et [Grid Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/).

*Recherche : `visual-computing-2026-10-04-001`. Relectures métier et linguistique, ainsi que test réel avec technologie d'assistance, en attente. Cette ébauche n'est pas un cours validé.*
