---
module_id: sem-001-signs-in-governance
department: semiotics
course: "Sémiotique de la gouvernance de l'IA"
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: seldon-plan
version: "1.0.0"
---

# Les signes dans la gouvernance — lire les constitutions à la lumière de Peirce

> **Département de sémiotique** | Stade : Nigredo (Débutant) | Durée : 25 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Définir les trois types de signes de Peirce : icône, indice et symbole
- Identifier chaque type de signe dans les documents de gouvernance de l'IA
- Expliquer en quoi chaque type de signe remplit une fonction de gouvernance différente
- Analyser un artefact de gouvernance sous l'angle de sa composition sémiotique
- Reconnaître les implications pratiques, pour la conception documentaire, de la conscience des types de signes

---

## 1. Qu'est-ce qu'un signe ?

Charles Sanders Peirce, fondateur de la sémiotique américaine, définit un **signe** comme tout ce qui tient lieu d'autre chose pour quelqu'un. Un signe comporte trois parties :

- **Le représentamen :** la forme que prend le signe (un mot, un diagramme, un nombre)
- **L'objet :** ce à quoi le signe renvoie (la chose dans le monde)
- **L'interprétant :** le sens que l'interprète donne au signe

L'idée décisive est que les signes ne portent pas de sens par eux-mêmes. Le sens naît de la *relation* entre le signe et son objet. Peirce a distingué trois types fondamentaux de cette relation.

---

## 2. Les icônes — des signes qui ressemblent

Une **icône** représente son objet par *ressemblance*. Elle a l'apparence, la sonorité ou la structure de ce qu'elle représente.

**Dans les documents de gouvernance :**

```
asimov.constitution.md        (racine)
  +-- demerzel-mandate.md      (qui applique)
  +-- default.constitution.md  (éthique opérationnelle)
       +-- policies/*.yaml
            +-- personas/*.persona.yaml
```

Ce schéma hiérarchique en ASCII est une **icône**. Sa structure arborescente reflète visuellement la hiérarchie de gouvernance réelle. Vous pouvez *voir* les relations rien qu'en regardant l'indentation. Le signe ressemble à son objet.

Autres icônes de gouvernance :
- Les organigrammes représentant des processus de décision
- Les diagrammes de séquence dans les politiques
- Les diagrammes d'automates (les cycles PDCA figurés par des cercles fléchés)
- Les tableaux dont l'alignement des colonnes reflète des relations catégorielles

**Fonction de gouvernance des icônes :** la compréhension rapide. Les icônes permettent de saisir une structure d'un coup d'œil, sans lire chaque mot. Elles compriment des relations complexes en motifs spatiaux.

---

## 3. Les indices — des signes qui pointent

Un **indice** représente son objet par une *connexion causale ou existentielle*. Il pointe vers son référent : il existe un lien réel entre les deux.

**Dans les documents de gouvernance :**

- `"voir policies/alignment-policy.yaml"` — un renvoi qui pointe physiquement vers un autre fichier
- `version: "2.1.0"` — un numéro de version causalement lié à une livraison précise
- `$ref: "../schemas/persona.schema.json"` — une référence JSON Schema qui se résout mécaniquement vers un schéma
- `effective_date: "2026-03-22"` — un horodatage qui indexe un moment dans le temps
- Des chemins de fichiers comme `state/conscience/signals/` — des chemins de répertoires pointant vers des emplacements réels du système de fichiers

Les indices constituent la **couche de traçabilité** de la gouvernance. Quand un auditeur demande « où cela est-il défini ? » ou « de quelle version s'agit-il ? », il suit des signes indiciels.

**Fonction de gouvernance des indices :** l'auditabilité et la traçabilité. Chaque renvoi, numéro de version et chemin de fichier crée une toile de connexions navigable. Sans indices, les documents de gouvernance seraient des îlots de texte isolés, sans relations vérifiables.

---

## 4. Les symboles — des signes par convention

Un **symbole** représente son objet par *convention arbitraire*. La relation entre le signe et son sens est établie par un accord social, non par ressemblance ni par connexion physique.

**Dans les documents de gouvernance :**

- **« Loi Zéro »** — le terme lui-même ne ressemble pas à l'idée de protéger l'humanité et ne pointe pas vers elle. Son sens vient de la convention fictionnelle d'Asimov, adoptée par le cadre de gouvernance.
- **« Logique tétravalente »** — « tétravalent » (à quatre valeurs) est un terme conventionnel. Rien dans le mot ne ressemble visuellement à quatre valeurs de vérité.
- **« Cycle PDCA »** — Plan-Do-Check-Act est un acronyme dont le sens doit s'apprendre par convention.
- **« Nigredo »** — un nom d'étape alchimique réemployé par convention pour signifier « niveau débutant ».
- **« T(0.85) »** — la convention de notation selon laquelle T signifie « croyance vraie » et 0.85 est un indice de confiance.

**Fonction de gouvernance des symboles :** la précision et la compression. Un symbole comme « Loi Zéro » comprime tout un cadre éthique en deux mots. Mais les symboles exigent un savoir partagé : si vous ignorez la convention, le symbole est opaque. C'est pourquoi les documents de gouvernance ont besoin de glossaires et de parcours d'intégration.

---

## 5. La composition sémiotique d'une constitution

Tout document de gouvernance est un **système de signes multimodal** : il emploie simultanément les trois types de signes, chacun remplissant une fonction différente.

| Type de signe | Fonction | Exemple | Mode de défaillance |
|-----------|----------|---------|-------------|
| **Icône** | Compréhension structurelle rapide | Diagrammes hiérarchiques | Simplification excessive — le diagramme masque les nuances |
| **Indice** | Traçabilité et auditabilité | Renvois, numéros de version | Liens rompus — l'indice ne pointe vers rien |
| **Symbole** | Précision et compression | Terminologie du domaine | Opacité — le symbole ne dit rien aux nouveaux venus |

Un document de gouvernance bien conçu équilibre les trois :
- **Trop d'icônes, trop peu de symboles :** joli mais imprécis. L'apparence est claire, mais la terminologie manque pour une interprétation sans ambiguïté.
- **Trop de symboles, trop peu d'icônes :** précis mais inaccessible. Correct, mais seuls les experts savent le déchiffrer.
- **Trop peu d'indices :** isolé. Les affirmations ne peuvent pas être rattachées à leurs sources, les versions ne peuvent pas être vérifiées.

---

## 6. Application pratique

Quand vous concevez ou relisez un document de gouvernance, demandez-vous :

1. **Les icônes sont-elles exactes ?** Le diagramme reflète-t-il bien la structure actuelle, ou est-il périmé ?
2. **Les indices se résolvent-ils ?** Chaque renvoi, chemin de fichier et numéro de version peut-il être suivi jusqu'à un artefact réel ?
3. **Les symboles sont-ils définis ?** Un nouveau venu a-t-il accès aux conventions nécessaires pour décoder la terminologie ?
4. **L'équilibre est-il le bon ?** Le document s'appuie-t-il trop lourdement sur un seul type de signe au détriment des autres ?

Cet audit sémiotique est un contrôle qualité léger qui rattrape les défaillances courantes des documents de gouvernance : diagrammes périmés (icônes rompues), liens morts (indices rompus) et jargon sans glossaire (symboles opaques).

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Signe** | Tout ce qui tient lieu d'autre chose pour un interprète |
| **Icône** | Un signe qui représente par ressemblance (diagrammes, reflets structurels) |
| **Indice** | Un signe qui représente par connexion causale ou existentielle (références, pointeurs) |
| **Symbole** | Un signe qui représente par convention arbitraire (terminologie, notation) |
| **Représentamen** | La forme que prend le signe |
| **Objet** | Ce à quoi le signe renvoie |
| **Interprétant** | Le sens que produit l'interprète |
| **Audit sémiotique** | Analyse de la composition en signes d'un document, quant à son équilibre et à sa justesse |

---

## Auto-évaluation

**1. Quelle est la différence essentielle entre une icône et un symbole ?**
> Une icône représente par ressemblance (elle a l'apparence de son objet), tandis qu'un symbole représente par convention arbitraire (son sens doit être appris).

**2. Donnez un exemple d'indice dans un document de gouvernance et expliquez en quoi il est indiciel.**
> Un renvoi comme « voir policies/alignment-policy.yaml » est indiciel parce qu'il pointe physiquement vers un autre artefact : il existe une connexion causale, le chemin se résolvant vers le fichier.

**3. Pourquoi un document de gouvernance a-t-il besoin des trois types de signes ?**
> Les icônes offrent une compréhension structurelle rapide, les indices apportent traçabilité et auditabilité, les symboles assurent la précision. L'absence de l'un des types crée un manque : sans icônes, la structure est inaccessible ; sans indices, les affirmations sont invérifiables ; sans symboles, le langage est imprécis.

**4. Vous trouvez un document de gouvernance saturé de terminologie spécialisée, mais sans aucun diagramme ni renvoi. Quel diagnostic sémiotique posez-vous ?**
> Riche en symboles, pauvre en icônes et pauvre en indices. Le document est précis mais inaccessible (aucune vue d'ensemble structurelle permettant une compréhension rapide) et non traçable (aucun lien permettant de vérifier les affirmations contre les artefacts sources). Recommandation : ajouter des diagrammes hiérarchiques et des renvois.

**Critères de réussite :** classer les signes d'un document de gouvernance en icônes, indices ou symboles, et expliquer la fonction de gouvernance de chaque type.

---

## Bases de la recherche

- La théorie sémiotique de Peirce (des années 1860 aux années 1910) — trichotomie fondatrice de l'icône, de l'indice et du symbole
- Les documents de gouvernance de l'IA contiennent de façon démontrable les trois types de signes, avec des fonctions distinctes
- L'analyse sémiotique fournit un cadre de qualité léger pour la conception documentaire
- Validation croisée avec GPT-4o-mini : fort accord — les trois catégories sont confirmées par des exemples concrets
- État de croyance : T(0.85) F(0.03) U(0.08) C(0.04)
