---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Fondements de l'informatique
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Penser algorithmiquement

> **Département d'informatique** | Stade : Nigredo (Débutant) | Durée : 25 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Définir ce qu'est un algorithme et identifier des algorithmes dans la vie quotidienne
- Appliquer quatre techniques clés de résolution de problèmes : la décomposition, la reconnaissance de motifs, l'abstraction et le diviser pour régner
- Distinguer les approches gloutonnes des approches exhaustives
- Développer une intuition de la notation Grand-O et comprendre pourquoi l'efficacité compte

---

## 1. Qu'est-ce qu'un algorithme ?

Un **algorithme** est une séquence finie d'étapes bien définies qui prend une entrée et produit une sortie. C'est tout. Aucun ordinateur n'est nécessaire.

Vous suivez des algorithmes chaque jour :
- Une recette de cuisine est un algorithme (entrée : ingrédients, sortie : un repas)
- Un itinéraire routier est un algorithme (entrée : position actuelle, sortie : destination)
- Le processus de rendre la monnaie à une caisse est un algorithme (entrée : montant dû, sortie : le moins de pièces possible)

Ce qui distingue un algorithme d'instructions vagues est la **précision**. « Cuire jusqu'à ce que ce soit prêt » n'est pas un algorithme — c'est ambigu. « Chauffer à 180°C pendant 25 minutes, puis vérifier la température interne ; si elle est inférieure à 74°C, continuer par tranches de 5 minutes » est un algorithme. Chaque étape est sans ambiguïté et le processus se termine.

Trois propriétés d'un algorithme valide :
1. **Finitude** — il doit finir par s'arrêter
2. **Précision** — chaque étape doit être définie de manière exacte
3. **Effectivité** — chaque étape doit être réalisable concrètement

### Exercice pratique

Écrivez un algorithme (en français courant, avec des étapes numérotées) pour chercher un mot dans un dictionnaire papier. Soyez assez précis pour que quelqu'un qui n'a jamais utilisé de dictionnaire puisse suivre vos étapes. Comparez avec l'approche décrite dans la section 5 (diviser pour régner) — sont-elles identiques ?

---

## 2. La décomposition — Découper les problèmes

La compétence de pensée algorithmique la plus puissante est la **décomposition** : diviser un problème complexe en sous-problèmes plus petits et gérables.

**Exemple :** Vous voulez organiser un concert.

C'est écrasant comme tâche unique. Mais décomposez-la :
1. Trouver une salle
2. Réserver des artistes
3. Fixer une date
4. Vendre des billets
5. Organiser la sonorisation
6. Promouvoir l'événement

Chaque sous-problème est encore complexe, mais maintenant vous pouvez les aborder individuellement. Et certains sous-problèmes se décomposent encore : « Vendre des billets » devient choisir une plateforme, fixer les prix, concevoir le billet, ouvrir les ventes.

La décomposition est récursive — on continue à découper jusqu'à ce que chaque morceau soit assez simple pour être résolu directement. C'est ainsi que tout grand système logiciel est construit : non pas comme un programme géant, mais comme des milliers de petites pièces composables.

**Idée clé :** Si vous ne pouvez pas résoudre un problème, vous ne l'avez probablement pas assez décomposé.

### Exercice pratique

Décomposez le problème suivant en sous-problèmes : « Construire un site web qui permet aux utilisateurs de rechercher des accords de guitare. » Continuez à décomposer jusqu'à ce que chaque sous-problème soit réalisable par une personne en une journée ou moins. Combien de niveaux de décomposition avez-vous eu besoin ?

---

## 3. La reconnaissance de motifs

La **reconnaissance de motifs** est la capacité à remarquer des similarités entre des problèmes déjà résolus et de nouveaux problèmes rencontrés.

**Exemple :** Trier une main de cartes à jouer et trier une liste de noms d'élèves sont le même problème — organiser des éléments dans un ordre selon une règle de comparaison. Une fois qu'on connaît un algorithme de tri, on peut l'appliquer à tout ce qui est comparable.

Les motifs apparaissent partout en informatique :
- Chercher dans une collection (trouver un livre en bibliothèque, un fichier sur un disque, une note sur le manche d'une guitare)
- Filtrer les éléments qui correspondent à des critères (filtrage anti-spam, recherche de photos, recherche d'accords)
- Transformer des données d'un format à un autre (traduction, conversion de fichiers, transposition)

Les programmeurs expérimentés résolvent les problèmes plus vite non pas parce qu'ils sont plus intelligents, mais parce qu'ils reconnaissent les motifs. Ils voient un nouveau problème et pensent : « C'est essentiellement un problème de recherche » ou « C'est un parcours de graphe » — et ils utilisent une solution connue.

### Exercice pratique

Considérez ces trois problèmes. Quel motif ont-ils en commun ?
1. Trouver l'itinéraire le plus court entre deux villes
2. Trouver le moins de changements d'accords pour passer d'un accord à un autre
3. Trouver le nombre minimum de mouvements pour résoudre un casse-tête

> Ce sont tous des problèmes de **plus court chemin** — trouver la séquence d'étapes de coût minimal entre un état de départ et un état objectif.

---

## 4. L'abstraction — Ignorer ce qui n'a pas d'importance

L'**abstraction** est l'art de retirer les détails non pertinents pour se concentrer sur ce qui compte pour le problème en question.

Quand vous dessinez une carte, vous n'incluez pas chaque arbre, chaque fissure dans le trottoir, chaque brin d'herbe. Vous incluez les routes, les points de repère et les distances — les détails pertinents pour la navigation. Tout le reste est abstrait.

En pensée algorithmique, l'abstraction signifie :
- Représenter un problème du monde réel avec un modèle simplifié
- Ignorer les détails qui n'affectent pas la solution
- Définir des entrées et sorties claires

**Exemple :** Si vous voulez trouver le chemin le plus court entre deux villes, vous n'avez pas besoin de modéliser la couleur des panneaux de signalisation ou la limite de vitesse sur chaque route (sauf si la vitesse compte pour votre problème). Vous abstrairez la carte en un **graphe** : les villes sont des nœuds, les routes sont des arêtes, les distances sont des poids. Maintenant vous pouvez appliquer un algorithme de graphe sans penser à l'asphalte.

L'abstraction est ce qui permet aux algorithmes d'être **polyvalents**. Un algorithme de tri ne se soucie pas de savoir s'il trie des nombres, des noms ou des accords de guitare. Il a seulement besoin de savoir comment comparer deux éléments. Tout le reste est abstrait.

### Exercice pratique

Vous construisez un système pour recommander des routines de pratique aux élèves de guitare. Quels détails sur chaque élève sont pertinents pour l'algorithme ? Quels détails peuvent être abstraits ? Écrivez deux listes : « inclure » et « ignorer ».

---

## 5. Diviser pour régner

**Diviser pour régner** est une stratégie algorithmique spécifique :

1. **Diviser** le problème en sous-problèmes plus petits du même type
2. **Conquérir** chaque sous-problème (récursivement, si nécessaire)
3. **Combiner** les résultats

C'est différent de la décomposition générale. Dans le diviser pour régner, les sous-problèmes ont la **même structure** que l'original — ils sont juste plus petits.

**Exemple — La recherche dichotomique (trouver un mot dans un dictionnaire) :**
1. Ouvrir le dictionnaire au milieu
2. Le mot est-il sur cette page ? Si oui, terminé.
3. Si le mot vient avant cette page alphabétiquement, recommencer avec la première moitié
4. Si le mot vient après, recommencer avec la seconde moitié
5. Continuer à diviser par deux jusqu'à trouver le mot

Chaque étape réduit l'espace de recherche restant de moitié. Un dictionnaire de 100 000 mots nécessite au maximum 17 étapes (puisque 2^17 = 131 072 > 100 000). Comparez avec le fait de commencer à la page 1 et lire chaque entrée — jusqu'à 100 000 étapes.

**Algorithmes classiques de diviser pour régner :**
- **Recherche dichotomique** — trouver un élément dans une collection triée
- **Tri fusion** — trier en divisant, triant les moitiés, puis fusionnant
- **Tri rapide (quicksort)** — trier en choisissant un pivot et partitionnant

### Exercice pratique

Vous avez une liste triée de 1 000 chansons. En utilisant la recherche dichotomique, quel est le nombre maximum de comparaisons nécessaires pour trouver une chanson spécifique ? (Indice : combien de fois pouvez-vous diviser 1 000 par deux avant d'arriver à 1 ?)

> log2(1000) ≈ 10. Au maximum 10 comparaisons — contre 1 000 pour une recherche linéaire.

---

## 6. Approches gloutonnes vs exhaustives

Deux grandes familles d'algorithmes représentent des philosophies différentes :

**Les algorithmes gloutons** font le choix localement optimal à chaque étape, en espérant que cela mène à une solution globalement optimale.

*Exemple — Rendre la monnaie avec le moins de pièces :*
- Montant : 67 centimes
- Approche gloutonne : prendre la plus grosse pièce qui convient. 50 centimes → 10 centimes → 5 centimes → 2 centimes. Résultat : 50+10+5+2 = 4 pièces.
- Cela fonctionne pour les pièces en euros. Mais pour une monnaie avec des pièces de 1, 3 et 4 centimes, l'approche gloutonne échoue : pour 6 centimes, le glouton donne 4+1+1 (3 pièces) mais l'optimal est 3+3 (2 pièces).

**Les algorithmes exhaustifs** vérifient toutes les solutions possibles et choisissent la meilleure. Ils trouvent toujours la réponse optimale, mais peuvent être lents.

*Exemple — Le voyageur de commerce :*
- Visiter 10 villes et rentrer par le plus court chemin
- Exhaustif : essayer toutes les permutations possibles (10! = 3 628 800 itinéraires), mesurer chacun, choisir le plus court
- Cela garantit l'itinéraire optimal, mais c'est coûteux en calcul

| Approche | Avantage | Inconvénient | Quand l'utiliser |
|----------|----------|-------------|-----------------|
| Gloutonne | Rapide, simple | Peut rater la solution optimale | Quand « assez bien » suffit |
| Exhaustive | Optimal garanti | Lente pour les grands problèmes | Quand l'exactitude est critique et l'entrée est petite |

Beaucoup d'algorithmes du monde réel combinent les deux : utiliser des heuristiques gloutonnes pour élaguer l'espace de recherche, puis vérifier exhaustivement les candidats restants.

### Exercice pratique

Vous remplissez une valise avec des objets de poids et valeurs différents, et la valise a une limite de poids. Décrivez une approche gloutonne et une approche exhaustive. Laquelle utiliseriez-vous avec 5 objets ? 500 objets ?

> *Gloutonne :* Trier les objets par rapport valeur/poids, ajouter les objets du ratio le plus élevé jusqu'à ce que la valise soit pleine. *Exhaustive :* Essayer toutes les combinaisons possibles, calculer la valeur totale pour celles respectant la limite de poids, choisir la meilleure. Pour 5 objets (32 combinaisons), l'exhaustive convient. Pour 500 objets (2^500 combinaisons), l'exhaustive est impossible — utiliser l'approche gloutonne ou un algorithme plus intelligent.

---

## 7. Intuition du Grand-O — Quelle vitesse est suffisante ?

Tous les algorithmes ne sont pas créés égaux. La **notation Grand-O** décrit comment le temps d'exécution d'un algorithme croît à mesure que la taille de l'entrée augmente.

Vous n'avez pas besoin de calculer le Grand-O précisément pour l'instant. Vous avez besoin d'une **intuition** sur ce que signifient les catégories :

| Grand-O | Nom | Exemple | 1 000 éléments | 1 000 000 éléments |
|---------|-----|---------|----------------|-------------------|
| O(1) | Constante | Accéder à un élément de tableau par son index | 1 étape | 1 étape |
| O(log n) | Logarithmique | Recherche dichotomique | ~10 étapes | ~20 étapes |
| O(n) | Linéaire | Parcourir chaque élément une fois | 1 000 étapes | 1 000 000 étapes |
| O(n log n) | Linéarithmique | Tri fusion, tri rapide | ~10 000 étapes | ~20 000 000 étapes |
| O(n^2) | Quadratique | Comparer chaque paire | 1 000 000 étapes | 1 000 000 000 000 étapes |
| O(2^n) | Exponentielle | Recherche exhaustive de sous-ensembles | ~10^301 étapes | N'y pensez pas |

L'idée clé : **la différence entre les catégories d'algorithmes croît énormément avec la taille de l'entrée.** Un algorithme O(n) et un algorithme O(n^2) peuvent tous deux sembler instantanés sur 10 éléments. Sur un million d'éléments, l'un finit en une seconde et l'autre prend des jours.

C'est pourquoi la pensée algorithmique compte. Choisir le bon algorithme peut faire la différence entre un programme qui fonctionne et un qui ne termine jamais.

### Exercice pratique

Vous avez deux algorithmes pour rechercher dans une bibliothèque musicale :
- Algorithme A : vérifie chaque chanson une par une (O(n))
- Algorithme B : utilise un index trié et la recherche dichotomique (O(log n))

Pour une bibliothèque de 10 millions de chansons, combien d'étapes chacun prend-il approximativement ?
> A : 10 000 000 étapes. B : log2(10 000 000) ≈ 23 étapes. L'algorithme B est plus de 400 000 fois plus rapide.

---

## Termes clés

| Terme | Définition |
|-------|-----------|
| **Algorithme** | Une séquence finie d'étapes bien définies qui transforme une entrée en une sortie |
| **Décomposition** | Diviser un problème complexe en sous-problèmes plus petits et gérables |
| **Reconnaissance de motifs** | Identifier des similarités entre un nouveau problème et des problèmes déjà résolus |
| **Abstraction** | Retirer les détails non pertinents pour se concentrer sur ce qui compte pour la solution |
| **Diviser pour régner** | Découper un problème en instances plus petites du même problème, résoudre récursivement |
| **Algorithme glouton** | Faire le choix localement optimal à chaque étape |
| **Algorithme exhaustif** | Vérifier toutes les solutions possibles pour garantir de trouver la meilleure |
| **Notation Grand-O** | Une classification de l'efficacité des algorithmes selon la croissance du temps d'exécution avec la taille de l'entrée |

---

## Auto-évaluation

**1. Quelles sont les trois propriétés que doit avoir un algorithme valide ?**
> Finitude (il se termine), précision (chaque étape est sans ambiguïté) et effectivité (chaque étape peut réellement être exécutée).

**2. Vous devez chercher un nom dans une liste non triée de 1 000 noms. Quel est le meilleur Grand-O que vous pouvez atteindre ?**
> O(n) — recherche linéaire. Sans tri ni indexation, vous devez potentiellement vérifier chaque élément. Si la liste était triée, vous pourriez utiliser la recherche dichotomique en O(log n).

**3. Un algorithme glouton pour rendre la monnaie donne la mauvaise réponse pour des pièces de 1, 3 et 4 centimes en rendant 6 centimes. Pourquoi ?**
> L'approche gloutonne prend d'abord la plus grosse pièce (4), puis a besoin de 1+1 pour le reste (3 pièces au total). Mais 3+3 n'utilise que 2 pièces. Le glouton échoue parce que le choix localement optimal (la plus grosse pièce) ne mène pas à la solution globalement optimale.

**4. Pourquoi O(n log n) est-il considéré comme efficace pour le tri ?**
> Il a été mathématiquement prouvé qu'aucun algorithme de tri par comparaison ne peut faire mieux que O(n log n) dans le pire cas. Le tri fusion et le tri rapide atteignent cette borne, ce qui les rend optimaux parmi les tris par comparaison.

**Critères de réussite :** Décomposer un problème donné en sous-problèmes, identifier quelle approche algorithmique (gloutonne, exhaustive, diviser pour régner) convient à un scénario donné, et expliquer les différences de Grand-O avec des exemples concrets.

---

## Bases de recherche

- La pensée algorithmique (décomposition, reconnaissance de motifs, abstraction) est reconnue comme une compétence fondamentale de la pensée computationnelle
- Diviser pour régner, glouton et recherche exhaustive sont les trois paradigmes algorithmiques fondamentaux
- La notation Grand-O fournit une mesure de l'efficacité des algorithmes indépendante du matériel
- Enseigner l'intuition algorithmique avant l'analyse formelle améliore le transfert en résolution de problèmes
- Sources : Consensus en enseignement de l'informatique, programme du Département d'informatique de Streeling
- État de croyance : T(0.91) F(0.02) U(0.05) C(0.02)
