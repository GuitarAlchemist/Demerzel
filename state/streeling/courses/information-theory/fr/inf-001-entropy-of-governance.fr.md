---
module_id: inf-001-entropy-of-governance
department: information-theory
course: "Théorie de l'information appliquée à la gouvernance"
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: seldon-plan
version: "1.0.0"
---

# L'entropie de la gouvernance — mesurer la complexité des politiques

> **Département de théorie de l'information** | Stade : Nigredo (Débutant) | Durée : 25 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Définir l'entropie de Shannon et expliquer ce qu'elle mesure
- Identifier l'alphabet de symboles d'un document structuré comme un fichier YAML
- Calculer une estimation d'entropie élémentaire pour une politique de gouvernance
- Interpréter une entropie forte ou faible dans le contexte de la conception des politiques
- Reconnaître les limites de l'entropie comme indicateur indirect de complexité

---

## 1. Qu'est-ce que l'entropie ?

Claude Shannon a défini en 1948 l'entropie comme une mesure de l'**incertitude**, ou du contenu en information, d'un message. La formule est d'une simplicité trompeuse :

```
H(X) = -somme(p(x) * log2(p(x))) pour tous les symboles x de l'alphabet X
```

où `p(x)` est la probabilité d'apparition du symbole `x`. L'entropie est maximale quand tous les symboles sont équiprobables (surprise maximale) et minimale quand un symbole domine (aucune surprise).

**Idée essentielle :** l'entropie mesure à quel point le prochain symbole est *imprévisible*. Un document dont chaque ligne ressemble aux autres a une entropie faible. Un document à la structure très variée a une entropie élevée.

---

## 2. Les politiques comme suites de symboles

Une politique de gouvernance en YAML est un document structuré. Nous pouvons définir un **alphabet structurel** en découpant ses éléments en jetons :

| Type de jeton | Exemples |
|-----------|----------|
| `KEY` | Toute clé YAML (par exemple `name:`, `version:`, `rationale:`) |
| `SCALAR` | Valeurs de type chaîne, nombre ou booléen |
| `LIST_ITEM` | Chaque entrée `- ` d'une liste |
| `NEST_IN` | Augmentation de la profondeur d'indentation |
| `NEST_OUT` | Diminution de la profondeur d'indentation |
| `COMMENT` | Lignes commençant par `#` |
| `SEPARATOR` | Séparateurs de documents `---` |

En convertissant une politique en cette suite de jetons, on obtient une chaîne sur un alphabet fini. L'entropie de Shannon nous dit alors à quel point le document est structurellement varié.

---

## 3. Ce que signifie une entropie élevée

Considérons deux politiques hypothétiques :

**Politique A** (entropie faible) : une liste plate de 20 règles, toutes à la même profondeur d'imbrication, chacune formant une simple paire clé-valeur. Suite de jetons : `KEY SCALAR KEY SCALAR KEY SCALAR ...` La distribution est dominée par deux jetons. L'entropie est faible.

**Politique B** (entropie élevée) : un document profondément imbriqué comportant des tableaux, des listes dans des listes, des blocs conditionnels, des renvois croisés et des types de valeurs mêlés. La suite de jetons emploie tous les types de jetons à peu près également. L'entropie est élevée.

**Interprétation :**
- Une **entropie faible** suggère régularité et prévisibilité — la politique a une structure simple et répétitive.
- Une **entropie élevée** suggère une variété structurelle — de nombreux modes d'organisation coexistent. Cela *peut* indiquer :
  - que la politique couvre un domaine réellement complexe (complexité justifiée) ;
  - que la politique s'est développée de façon organique, sans structure cohérente (complexité accidentelle) ;
  - que la politique tente de faire trop de choses à la fois (dérive du périmètre).

La distinction décisive : **l'entropie signale la complexité, elle n'en diagnostique pas la cause**. Une politique à forte entropie exige un jugement humain pour déterminer si cette complexité est essentielle ou accidentelle.

---

## 4. Un exemple travaillé

Prenons le fichier `seldon-plan-policy.yaml` de Demerzel. Ses jetons structurels comprennent :
- des clés de métadonnées de premier niveau (name, version, description, rationale) ;
- des tables de configuration imbriquées (bornes de ressources) ;
- des sections procédurales en plusieurs phases (7 phases) ;
- des blocs de code, des listes, des renvois croisés.

Cette politique couvre légitimement un système de recherche autonome complexe. Sa forte entropie structurelle reflète une complexité réelle du domaine — l'entropie est *justifiée*.

Comparez maintenant avec une politique simple, telle qu'une convention de nommage : quelques clés, une expression régulière de motif et des exemples. Entropie faible, et c'est approprié.

**Le signal :** quand l'entropie est élevée alors que le domaine est simple, c'est le signal qu'il faut refactoriser. Une entropie hors de proportion avec la complexité du domaine suggère une complexité accidentelle.

---

## 5. Limites

L'entropie de Shannon comme indicateur indirect de complexité a de vraies limites :

1. **Cécité sémantique.** L'entropie mesure la variété structurelle, non le sens. Deux politiques d'entropie identique peuvent différer énormément en clarté et en cohérence.

2. **La granularité des jetons compte.** Des jetons grossiers (seulement KEY/SCALAR) donnent une entropie différente de jetons fins (les noms de clés individuels). Le choix de l'alphabet façonne la mesure.

3. **La taille perturbe la mesure.** Les documents longs explorent naturellement une plus grande part de l'espace des jetons. Normalisez par la longueur du document, ou comparez des documents de tailles voisines.

4. **Régularité n'est pas simplicité.** Une structure profondément imbriquée mais parfaitement régulière (comme un arbre de décision) a une entropie faible tout en pouvant rester difficile à comprendre.

5. **Le contexte fait tout.** Une politique de gouvernance pour la sûreté nucléaire *doit* être complexe. L'entropie doit s'interpréter relativement à la complexité inhérente au domaine.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Entropie de Shannon** | Une mesure du contenu moyen en information (la surprise) par symbole d'un message |
| **Alphabet de symboles** | L'ensemble des types de jetons distincts servant à encoder la structure d'un document |
| **Complexité structurelle** | La variété et la profondeur des modes d'organisation d'un document |
| **Complexité essentielle** | La complexité inhérente au domaine du problème, qui ne peut être supprimée |
| **Complexité accidentelle** | La complexité introduite par de mauvais choix de conception, qui pourrait être éliminée |
| **Normalisation de l'entropie** | Division de l'entropie brute par log2(taille de l'alphabet) pour obtenir une échelle de 0 à 1 |

---

## Auto-évaluation

**1. Qu'indique une entropie de Shannon élevée dans un document de politique ?**
> Une grande variété structurelle : de nombreux types de jetons différents apparaissent avec des fréquences voisines, ce qui suggère que le document emploie des modes d'organisation divers.

**2. Pourquoi l'entropie seule ne peut-elle pas vous dire si une politique doit être simplifiée ?**
> Parce que l'entropie mesure la variété structurelle, et non si cette variété est justifiée par le domaine. Les domaines complexes exigent des politiques complexes. L'entropie signale des candidats à la revue, pas une refactorisation automatique.

**3. Comment comparer l'entropie de politiques de longueurs différentes ?**
> En normalisant par la longueur du document (entropie par jeton) ou par l'entropie maximale possible (H/log2(N), où N est la taille de l'alphabet), afin d'obtenir une échelle comparable de 0 à 1.

**4. Une politique a une entropie très faible, mais les utilisateurs la trouvent déroutante. Qu'est-ce qui pourrait l'expliquer ?**
> Une entropie faible signifie une structure répétitive, mais le contenu à l'intérieur de cette structure peut être obscur, contradictoire ou mal formulé. La simplicité structurelle ne garantit pas la clarté sémantique.

**Critères de réussite :** expliquer l'entropie de Shannon, identifier les jetons d'un document structuré et formuler la différence entre complexité structurelle et complexité sémantique.

---

## Bases de la recherche

- « A Mathematical Theory of Communication » de Shannon (1948) — définition fondatrice de l'entropie
- Les métriques de complexité logicielle (cyclomatique, Halstead) montrent que les mesures formelles sont corrélées à la difficulté de maintenance
- L'analyse structurelle du YAML traite les documents comme des suites de jetons sur un alphabet fini
- Validation croisée avec GPT-4o-mini : accord moyen sur l'hypothèse, fort sur la théorie, validation empirique nécessaire
- État de croyance : T(0.75) F(0.05) U(0.15) C(0.05)
