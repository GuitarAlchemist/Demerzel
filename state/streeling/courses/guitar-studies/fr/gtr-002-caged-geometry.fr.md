---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Disposition du manche et système CAGED"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# La géométrie du CAGED : pourquoi cinq formes gouvernent le manche

> **Département d'études de guitare** | Niveau : Intermédiaire | Durée : 45 minutes

## Objectifs
- Comprendre pourquoi exactement 5 formes d'accords ouverts recouvrent tout le manche
- Déduire le système CAGED à partir de l'observation de la structure intervallique des accords ouverts
- Démontrer que le CAGED est une conséquence mathématique de l'accordage standard, pas un système arbitraire
- Appliquer les formes de barré mobiles pour naviguer tout accord majeur sur le manche

---

## 1. Les cinq formes ouvertes

Tout guitariste apprend ces cinq accords majeurs ouverts dès le début. Chacun a une empreinte géométrique distincte :

### Forme C
```
x 3 2 0 1 0    Cordes : 5-4-3-2-1
  F 3 5 F 3    Intervalles : Fondamentale-3M-5J-Fondamentale-3M
```

### Forme A
```
x 0 2 2 2 0    Cordes : 5-4-3-2-1
  F 5 F 3 5    Intervalles : Fondamentale-5J-Fondamentale-3M-5J
```

### Forme G
```
3 2 0 0 0 3    Cordes : 6-5-4-3-2-1
F 3 5 F 3 F    Intervalles : Fondamentale-3M-5J-Fondamentale-3M-Fondamentale
```

### Forme E
```
0 2 2 1 0 0    Cordes : 6-5-4-3-2-1
F 5 F 3 5 F    Intervalles : Fondamentale-5J-Fondamentale-3M-5J-Fondamentale
```

### Forme D
```
x x 0 2 3 2    Cordes : 4-3-2-1
  F 5 F 3      Intervalles : Fondamentale-5J-Fondamentale-3M
```

**Observation clé :** Chaque forme ne contient que trois classes de hauteur : la fondamentale, la tierce majeure et la quinte juste. Les différences résident dans le *renversement* — à quelle octave apparaît chaque note et quelles cordes les portent.

---

## 2. Le test du glissement

Voici l'idée centrale : si vous maintenez la *géométrie des doigts* de n'importe quel accord ouvert mais que vous le glissez le long du manche, les relations intervalliques sont préservées. Le doigt du barré remplace le sillet.

**Forme E à la frette 0 :** Mi majeur (ouvert)
**Forme E à la frette 1 :** Fa majeur (accord barré de Fa)
**Forme E à la frette 3 :** Sol majeur
**Forme E à la frette 5 :** La majeur

Cela fonctionne parce que l'intervalle entre chaque paire de cordes adjacentes est fixé par l'accordage. Déplacer tous les doigts du même nombre de frettes transpose chaque note du même intervalle.

Ce n'est pas une astuce pédagogique — c'est un *théorème géométrique* sur le manche.

---

## 3. Pourquoi exactement cinq formes ?

L'accordage standard (Mi-La-Ré-Sol-Si-Mi) crée un motif d'intervalles spécifique entre les cordes :

```
Corde :      6    5    4    3    2    1
Note :       Mi   La   Ré   Sol  Si   Mi
Intervalle :   4J   4J   4J   3M   4J
```

Le motif 4J-4J-4J-3M-4J crée exactement **cinq régions distinctes** où des formes d'accords ouverts peuvent être formées. Chaque forme occupe une étendue différente de frettes et de cordes.

Les cinq formes s'emboîtent comme les pièces d'un puzzle :

```
Frette : 0    3    5    7    8    10   12
         |--E--|--D--|--C--|--A--|--G--|--E--|
         (formes montrées pour la tonalité de Mi majeur)
```

En parcourant l'ordre C-A-G-E-D, on remonte le manche, la fondamentale de chaque forme se connectant à la note la plus haute de la forme suivante. C'est la **séquence CAGED** — un chemin cyclique à travers les cinq régions de renversement.

---

## 4. Le CAGED est-il le seul ordre possible ?

Les cinq formes constituent un **cycle**, donc tout point de départ donne une séquence valide :

- **CAGED** (le plus courant)
- **AGEDC** (en partant de A)
- **GEDCA** (en partant de G)
- **EDCAG** (en partant de E)
- **DCAGE** (en partant de D)

Le nom « CAGED » est une commodité mnémotechnique. Le cycle sous-jacent de 5 formes est déterminé structurellement. Tous les ordres décrivent le même pavage du manche.

---

## 5. Dépendance à l'accordage

Le CAGED est spécifique à l'accordage standard. Changez l'accordage, et les formes changent :

- **Accordage tout en quartes** (Mi-La-Ré-Sol-Do-Fa) : L'irrégularité de la tierce majeure entre les cordes 3-2 disparaît. Les formes d'accords deviennent plus uniformes mais différentes du CAGED.
- **Accordage ouvert en Sol** (Ré-Sol-Ré-Sol-Si-Ré) : Les cordes à vide forment déjà un accord, créant un système de formes complètement différent.
- **Drop D** (Ré-La-Ré-Sol-Si-Mi) : Seule la corde la plus grave change, préservant la plupart des formes CAGED mais modifiant les formes E et G sur les cordes basses.

Cela prouve que le CAGED est *dérivé de* la géométrie de l'accordage standard, et non imposé à celle-ci.

---

## Exercice pratique

### Exercice 1 : Identification des formes
Jouez un accord de Do majeur en utilisant les cinq formes CAGED. Commencez avec la forme C ouverte, puis trouvez la forme A (frette 3), la forme G (frette 5), la forme E (frette 8) et la forme D (frette 10).

### Exercice 2 : Connexion entre les formes
Choisissez deux formes CAGED adjacentes. Trouvez les notes qu'elles partagent sur les mêmes cordes. Ces notes partagées sont vos « points de pivot » pour passer d'une forme à l'autre.

### Exercice 3 : Une corde, cinq formes
Sur la corde 2 uniquement, jouez la note Do dans chacune des cinq positions CAGED. Observez comment chaque forme place le Do sur une frette différente de cette corde.

---

## Points clés à retenir
- Le système CAGED est **découvert, pas inventé** — c'est une conséquence structurelle de la géométrie de l'accordage standard
- Exactement **5 formes** recouvrent le manche à cause du motif d'accordage 4J-4J-4J-3M-4J
- Chaque forme préserve sa structure intervallique quand elle est barrée et déplacée — c'est un théorème géométrique, pas un raccourci pédagogique
- Le nom « CAGED » est l'un des 5 ordres cycliques équivalents
- Des accordages différents produisent des systèmes de formes différents, confirmant que le CAGED est dérivé de l'accordage

## Lectures complémentaires
- [GTR-001 : La carte du manche](gtr-001-the-fretboard-map.fr.md) — prérequis
- Département de musique : Systèmes d'accordage et tempérament
- Département de physique : Acoustique de la vibration des cordes et harmoniques
- Département de mathématiques : Théorie des groupes et symétrie du manche

---
*Produit par le cycle de recherche Seldon guitar-studies-2026-03-23-001 le 2026-03-23.*
*Question de recherche : Les doigtés courants des accords ouverts partagent-ils des motifs structurels qui prédisent leurs formes de barré mobiles ?*
*Croyance : T (confiance : 0.85)*
