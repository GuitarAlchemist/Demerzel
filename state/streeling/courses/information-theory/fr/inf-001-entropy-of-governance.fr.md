---
module_id: inf-001-entropy-of-governance
department: information-theory
course: Théorie de l'information appliquée à la gouvernance
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: seldon-plan
version: "1.0.0"
---

# L'entropie de la gouvernance — Mesurer la complexité des politiques

> **Département de théorie de l'information** | Stade : Nigredo (Débutant) | Durée : 25 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Définir l'entropie de Shannon et expliquer ce qu'elle mesure
- Identifier l'alphabet de symboles d'un document structuré comme du YAML
- Calculer une estimation élémentaire de l'entropie d'une politique de gouvernance
- Interpréter une entropie élevée ou faible dans le contexte de la conception des politiques
- Reconnaître les limites de l'entropie comme indicateur de complexité

---

## 1. Qu'est-ce que l'entropie ?

Claude Shannon a défini l'entropie en 1948 comme une mesure de l'**incertitude** ou du **contenu informationnel** d'un message. La formule est d'une simplicité trompeuse :

```
H(X) = -sum(p(x) * log2(p(x))) pour tous les symboles x de l'alphabet X
```

Où `p(x)` est la probabilité d'apparition du symbole `x`. L'entropie est maximale lorsque tous les symboles sont équiprobables (surprise maximale) et minimale lorsqu'un symbole domine (aucune surprise).

**Idée clé :** calculée à partir des seules fréquences des symboles, comme dans cette leçon, l'entropie mesure à quel point un symbole est *imprévisible* quand on le tire au hasard dans le document, sans tenir compte de l'ordre : elle mesure à quel point le document utilise ses types de symboles de manière égale. L'imprévisibilité du symbole *suivant*, connaissant celui qui le précède, est l'entropie conditionnelle H(X_n | X_(n-1)). On l'estime à partir des fréquences des paires consécutives par H(paires) - H(premiers), où H(premiers) est l'entropie des premiers symboles des paires, c'est-à-dire de tous les symboles sauf le dernier. Elle ne dépasse jamais l'entropie des seconds symboles des paires, et ne l'égale que si les deux symboles d'une paire sont indépendants ; sur un long document, les deux marginales sont proches de H(X). Un document qui utilise peu de types de symboles a une entropie faible selon les deux mesures ; un document qui répète un même motif fait de nombreux types de symboles a une entropie des fréquences élevée et une entropie conditionnelle faible.

---

## 2. Les politiques comme séquences de symboles

Une politique de gouvernance en YAML est un document structuré. On peut définir un **alphabet structurel** en découpant ses éléments en jetons :

| Type de jeton | Exemples |
|-----------|----------|
| `KEY` | N'importe quelle clé YAML (p. ex. `name:`, `version:`, `rationale:`) |
| `SCALAR` | Valeurs chaîne, nombre ou booléen |
| `LIST_ITEM` | Chaque entrée `- ` d'une liste |
| `NEST_IN` | Augmentation de la profondeur d'indentation |
| `NEST_OUT` | Diminution de la profondeur d'indentation |
| `COMMENT` | Lignes commençant par `#` |
| `SEPARATOR` | Séparateurs de documents `---` |

En convertissant une politique en cette séquence de jetons, on obtient une chaîne sur un alphabet fini. L'entropie de Shannon des fréquences des jetons nous dit alors à quel point les types de jetons du document sont variés, pas dans quel ordre ils viennent : mélanger les jetons ne la change pas, si bien que deux politiques ayant le même nombre de jetons de chaque type ont la même entropie, même si l'une répète un seul motif et que l'autre ordonne ses jetons de façon erratique. La régularité structurelle est une affaire d'ordre, et la mesure qui la voit est l'entropie conditionnelle de la section 1, estimée à partir des paires de jetons consécutifs.

---

## 3. Ce que signifie une entropie élevée

Considérons deux politiques hypothétiques :

**Politique A** (entropie faible) : une liste plate de 20 règles, toutes à la même profondeur d'imbrication, chacune étant une simple paire clé-valeur. Séquence de jetons : `KEY SCALAR KEY SCALAR KEY SCALAR ...` La distribution est dominée par deux jetons. L'entropie est faible.

**Politique B** (entropie élevée) : un document profondément imbriqué avec des tables, des listes dans des listes, des blocs conditionnels, des références croisées et des types de valeurs mélangés. La séquence de jetons utilise tous les types de jetons à peu près également. L'entropie est élevée.

**Interprétation :**
- Une **entropie faible** indique que quelques types de jetons dominent la politique, ce qui suggère une structure simple. Elle ne montre pas que cette structure se répète : c'est une entropie conditionnelle faible qui le montre.
- Une **entropie élevée** indique que de nombreux types de jetons sont utilisés à peu près également, ce qui suggère une variété structurelle, bien qu'un seul motif fait de nombreux types de jetons la donne aussi. Cela *peut* indiquer que :
  - La politique couvre un territoire réellement complexe (complexité justifiée)
  - La politique a grandi de façon organique sans structure cohérente (complexité accidentelle)
  - La politique essaie de faire trop de choses (dérive du périmètre)

La distinction essentielle : **l'entropie signale la complexité, elle n'en diagnostique pas la cause**. Une politique à entropie élevée nécessite un jugement humain pour déterminer si la complexité est essentielle ou accidentelle.

---

## 4. Un exemple détaillé

Prenons `seldon-plan-policy.yaml` de Demerzel. Ses jetons structurels comprennent :
- Des clés de métadonnées de premier niveau (name, version, description, rationale)
- Des tables de configuration imbriquées (limites de ressources)
- Des sections procédurales en plusieurs phases (7 phases)
- Des blocs de code, des listes, des références croisées

Cette politique couvre légitimement un système de recherche autonome complexe. Son entropie structurelle élevée reflète une réelle complexité du domaine — l'entropie est *justifiée*.

Comparez maintenant avec une politique simple comme une convention de nommage : quelques clés, une expression régulière de motif et des exemples. Entropie faible, à juste titre.

**Le signal :** lorsque l'entropie est élevée mais que le domaine est simple, c'est le signal qu'il faut refactoriser. Une entropie disproportionnée par rapport à la complexité du domaine suggère une complexité accidentelle.

---

## 5. Limites

L'entropie de Shannon comme indicateur de complexité a de réelles limites :

1. **Cécité sémantique.** L'entropie mesure la variété structurelle, pas le sens. Deux politiques d'entropie identique peuvent différer considérablement en clarté et en cohérence.

2. **La granularité des jetons compte.** Des jetons grossiers (seulement KEY/SCALAR) donnent une entropie différente de jetons fins (noms de clés individuels). Le choix de l'alphabet façonne la mesure.

3. **La taille est un facteur de confusion.** Les documents plus longs explorent naturellement une plus grande partie de l'espace des jetons, et l'entropie estimée sur un document court est plus bruitée et tend à sortir trop basse. Ne divisez pas H par la longueur : c'est déjà une moyenne par jeton. Comparez des documents de taille similaire, ou indiquez l'incertitude de chaque estimation.

4. **Régularité n'est pas simplicité.** Une structure profondément imbriquée mais parfaitement régulière (comme un arbre de décision) devient prévisible dès qu'on tient compte d'assez de jetons précédents, si bien que son entropie conditionnelle sachant ces jetons est faible, quelles que soient les fréquences de ses jetons ; elle peut pourtant rester difficile à comprendre.

5. **Le contexte est primordial.** Une politique de gouvernance pour la sûreté nucléaire *doit* être complexe. L'entropie doit être interprétée par rapport à la complexité inhérente du domaine.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Entropie de Shannon** | Une mesure du contenu informationnel moyen (surprise) par symbole dans un message |
| **Entropie conditionnelle** | La surprise moyenne d'un symbole sachant les symboles qui le précèdent ; contrairement à l'entropie des fréquences des symboles, elle dépend de leur ordre |
| **Alphabet de symboles** | L'ensemble des types de jetons distincts utilisés pour encoder la structure d'un document |
| **Complexité structurelle** | La variété et la profondeur des schémas d'organisation d'un document |
| **Complexité essentielle** | La complexité inhérente au domaine du problème, qui ne peut pas être supprimée |
| **Complexité accidentelle** | La complexité introduite par de mauvais choix de conception, qui pourrait être éliminée |
| **Normalisation de l'entropie** | Diviser l'entropie brute par log2(taille de l'alphabet) pour obtenir une échelle de 0 à 1 |

---

## Auto-évaluation

**1. Qu'indique une entropie de Shannon élevée dans un document de politique ?**
> Une variété de types de jetons — de nombreux types de jetons différents apparaissent avec une fréquence similaire, ce qui suggère que le document utilise des schémas d'organisation divers. Elle ne dit rien de l'ordre des jetons, et ne montre donc pas si la structure est régulière.

**2. Pourquoi l'entropie seule ne peut-elle pas vous dire si une politique doit être simplifiée ?**
> Parce que l'entropie mesure la variété structurelle, pas si cette variété est justifiée par le domaine. Les domaines complexes exigent des politiques complexes. L'entropie signale des candidats à examiner, pas une refactorisation automatique.

**3. Comment compareriez-vous l'entropie de politiques de longueurs différentes ?**
> Pas en divisant par la longueur : H est déjà une moyenne en bits par jeton, donc deux documents aux mêmes fréquences de jetons ont la même H, quelle que soit leur longueur. Comparez H directement sur le même alphabet, ou divisez-la par l'entropie maximale possible (H/log2(N) où N est la taille de l'alphabet) pour obtenir une échelle comparable de 0 à 1. La longueur compte autrement : H est estimée à partir des fréquences observées, et un document court donne une estimation plus bruitée qui tend à sortir trop basse ; comparez donc des documents de longueur similaire ou indiquez l'incertitude.

**4. Une politique a une entropie très faible mais les utilisateurs la trouvent confuse. Qu'est-ce qui pourrait l'expliquer ?**
> Une entropie faible signifie que quelques types de jetons dominent, une structure simple, mais le contenu à l'intérieur de cette structure peut être peu clair, contradictoire ou mal rédigé. La simplicité structurelle ne garantit pas la clarté sémantique.

**Critères de réussite :** expliquer l'entropie de Shannon, identifier les jetons d'un document structuré et formuler la différence entre complexité structurelle et complexité sémantique.

---

## Fondements de recherche

- « A Mathematical Theory of Communication » de Shannon (1948) — définition fondatrice de l'entropie
- Les métriques de complexité logicielle (cyclomatique, Halstead) montrent que les mesures formelles sont corrélées à la difficulté de maintenance
- L'analyse structurelle du YAML traite les documents comme des séquences de jetons sur un alphabet fini
- Validation croisée avec GPT-4o-mini : accord moyen sur l'hypothèse, fort sur la théorie, validation empirique nécessaire
- État de croyance : T(0.75) F(0.05) U(0.15) C(0.05) — traduction française : U (non relue par un locuteur natif)
