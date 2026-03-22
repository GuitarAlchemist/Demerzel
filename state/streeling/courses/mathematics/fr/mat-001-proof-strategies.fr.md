---
module_id: mat-001-proof-strategies
department: mathematics
course: Fondements du raisonnement mathématique
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "30 minutes"
produced_by: mathematics
version: "1.0.0"
---

# Stratégies de démonstration — Comment prouver les choses

> **Département de mathématiques** | Stade : Nigredo (Débutant) | Durée : 30 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Expliquer ce qu'est une démonstration mathématique et pourquoi elle compte
- Appliquer la démonstration directe pour établir un énoncé à partir de faits connus
- Appliquer la démonstration par l'absurde pour montrer qu'un énoncé est nécessairement vrai
- Appliquer la démonstration par récurrence pour prouver des énoncés sur tous les entiers naturels
- Reconnaître quelle stratégie de démonstration convient à un problème donné

---

## 1. Qu'est-ce qu'une démonstration ?

Une démonstration est un raisonnement logique qui établit, au-delà de tout doute, qu'un énoncé mathématique est vrai. Pas probablement vrai, pas vrai dans la plupart des cas — **toujours** vrai, dans chaque situation possible que l'énoncé décrit.

C'est ce qui rend les mathématiques uniques parmi les disciplines. En sciences, on rassemble des preuves et on formule des théories qui pourraient être renversées par de nouvelles données. En mathématiques, une fois qu'un résultat est démontré, il reste démontré pour toujours. Les démonstrations d'Euclide datant de 300 av. J.-C. sont aussi valides aujourd'hui qu'alors.

Une démonstration part d'**axiomes** (des énoncés acceptés comme vrais) et de **résultats précédemment démontrés**, puis utilise des règles logiques pour arriver à la conclusion. Chaque étape doit découler inévitablement des étapes précédentes.

Trois idées reçues à corriger :
- **« Les exemples prouvent les choses. »** Non. Montrer qu'un énoncé fonctionne pour 10, 100 ou un million de cas ne prouve pas qu'il fonctionne pour tous les cas. Un seul contre-exemple peut détruire une conjecture qui a passé des milliards de tests.
- **« Les démonstrations doivent être longues et compliquées. »** Certaines des plus belles démonstrations sont courtes. L'élégance est valorisée.
- **« Il n'y a qu'une seule façon de démontrer quelque chose. »** La plupart des théorèmes peuvent être démontrés de plusieurs façons. Choisir la bonne stratégie fait partie de l'art.

---

## 2. Démonstration directe

Une **démonstration directe** part de ce que l'on sait et raisonne en avant, étape par étape, vers ce que l'on veut montrer.

**Structure :**
1. Supposer l'hypothèse (la partie « si » de l'énoncé)
2. Appliquer des définitions, des résultats connus et des étapes logiques
3. Arriver à la conclusion (la partie « alors »)

**Exemple : Démontrer que la somme de deux nombres pairs est paire.**

*Énoncé :* Si *a* et *b* sont pairs, alors *a + b* est pair.

*Démonstration :*
- Puisque *a* est pair, par définition *a = 2m* pour un certain entier *m*.
- Puisque *b* est pair, par définition *b = 2n* pour un certain entier *n*.
- Alors *a + b = 2m + 2n = 2(m + n)*.
- Puisque *m + n* est un entier, *a + b* est 2 fois un entier, ce qui est pair par définition.

Voilà une démonstration complète. Chaque étape découle logiquement. Pas de lacune, pas d'approximation.

**Quand utiliser la démonstration directe :** Quand vous voyez clairement un chemin de l'hypothèse à la conclusion. Quand les définitions vous donnent des formes algébriques à manipuler. C'est votre stratégie par défaut — essayez-la en premier.

### Exercice pratique

Démontrez que le produit de deux nombres impairs est impair. (Indice : un nombre impair peut s'écrire *2k + 1* pour un certain entier *k*.)

> *Solution :* Posons *a = 2m + 1* et *b = 2n + 1*. Alors *ab = (2m+1)(2n+1) = 4mn + 2m + 2n + 1 = 2(2mn + m + n) + 1*. Puisque *2mn + m + n* est un entier, *ab* a la forme *2k + 1*, donc il est impair.

---

## 3. Démonstration par l'absurde

Parfois le chemin direct n'est pas évident. La **démonstration par l'absurde** adopte une approche différente : supposer le contraire de ce que l'on veut prouver, puis montrer que cette hypothèse mène à quelque chose d'impossible.

**Structure :**
1. Supposer la négation de l'énoncé que l'on veut prouver
2. Raisonner logiquement à partir de cette hypothèse
3. Arriver à une contradiction (quelque chose de manifestement faux, ou qui contredit un fait connu)
4. Conclure que l'hypothèse était fausse, donc l'énoncé original est vrai

**Exemple : Démontrer que la racine carrée de 2 est irrationnelle.**

*Énoncé :* Il n'existe aucune fraction *p/q* (avec *p, q* entiers, *q* non nul, irréductible) telle que *(p/q)^2 = 2*.

*Démonstration :*
- **Supposons le contraire :** Supposons que sqrt(2) est rationnel. Alors sqrt(2) = *p/q* où *p* et *q* sont des entiers sans facteur commun (fraction irréductible).
- En élevant au carré : *2 = p^2 / q^2*, donc *p^2 = 2q^2*.
- Cela signifie que *p^2* est pair, ce qui implique que *p* lui-même est pair (car le carré d'un nombre impair est impair). Donc *p = 2k* pour un certain entier *k*.
- En substituant : *(2k)^2 = 2q^2*, donc *4k^2 = 2q^2*, donc *q^2 = 2k^2*.
- Cela signifie que *q^2* est pair, donc *q* est pair.
- Mais maintenant *p* et *q* sont tous deux pairs, ce qui veut dire qu'ils partagent un facteur 2. **Cela contredit notre hypothèse** que *p/q* était irréductible.
- Par conséquent, notre hypothèse était fausse. La racine carrée de 2 est irrationnelle.

**Quand utiliser l'absurde :** Quand on veut prouver que quelque chose n'existe pas, ou quand l'énoncé contient des mots comme « aucun », « ne peut pas » ou « impossible ». Également utile quand l'approche directe s'embrouille.

### Exercice pratique

Démontrez par l'absurde qu'il n'existe pas de plus grand entier. (Indice : supposez qu'il existe un plus grand entier *N*, puis considérez *N + 1*.)

> *Solution :* Supposons qu'il existe un plus grand entier *N*. Alors *N + 1* est aussi un entier (les entiers sont fermés sous l'addition). Mais *N + 1 > N*, ce qui contredit l'hypothèse que *N* était le plus grand. Par conséquent, il n'existe pas de plus grand entier.

---

## 4. Démonstration par récurrence

La **récurrence** est votre outil pour démontrer des énoncés portant sur tous les entiers naturels (ou toute suite infinie). Elle fonctionne comme une chaîne de dominos.

**Structure :**
1. **Cas de base :** Prouver que l'énoncé est vrai pour la première valeur (habituellement *n = 0* ou *n = 1*)
2. **Étape de récurrence :** Supposer que l'énoncé est vrai pour une valeur arbitraire *n = k* (l'**hypothèse de récurrence**). Puis prouver qu'il est aussi vrai pour *n = k + 1*.
3. **Conclusion :** Puisque le cas de base est vrai et que chaque cas implique le suivant, l'énoncé est vrai pour tous les entiers naturels.

Pourquoi ça marche ? Si le domino 1 tombe (cas de base), et que chaque domino qui tombe fait tomber le suivant (étape de récurrence), alors tous les dominos tombent.

**Exemple : Démontrer que la somme 1 + 2 + 3 + ... + n = n(n+1)/2 pour tout entier positif n.**

*Cas de base (n = 1) :*
- Côté gauche : 1
- Côté droit : 1(1+1)/2 = 1
- Ils correspondent. Le cas de base est vérifié.

*Étape de récurrence :*
- **Hypothèse de récurrence :** Supposons que 1 + 2 + ... + k = k(k+1)/2 pour un certain entier positif *k*.
- **Montrons que c'est vrai pour k + 1 :** On veut que 1 + 2 + ... + k + (k+1) = (k+1)(k+2)/2.
- En partant du côté gauche : 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) (en utilisant l'hypothèse de récurrence)
- = (k+1)(k/2 + 1) = (k+1)(k+2)/2
- Cela correspond à la formule pour *n = k + 1*. L'étape de récurrence est vérifiée.

*Conclusion :* Par récurrence, la formule est vraie pour tout entier positif *n*.

**Quand utiliser la récurrence :** Quand l'énoncé porte sur tous les entiers naturels (ou toutes les valeurs à partir d'un certain point de départ). Cherchez des formules impliquant *n*, des énoncés comme « pour tout *n* >= 1 », ou des définitions récursives.

### Exercice pratique

Démontrez par récurrence que *2^n > n* pour tout entier positif *n*.

> *Solution :*
> *Cas de base (n = 1) :* 2^1 = 2 > 1. Vrai.
> *Étape de récurrence :* Supposons 2^k > k. Alors 2^(k+1) = 2 * 2^k > 2k (par l'hypothèse). Puisque 2k = k + k >= k + 1 pour tout k >= 1, on a 2^(k+1) > k + 1.
> Par récurrence, 2^n > n pour tout entier positif n.

---

## 5. Choisir sa stratégie

Face à un énoncé à démontrer, posez-vous ces questions :

| Question | Si oui, essayez... |
|----------|-------------------|
| Puis-je aller de l'hypothèse à la conclusion en utilisant des définitions et de l'algèbre ? | Démonstration directe |
| L'énoncé dit-il que quelque chose est impossible, ou que quelque chose n'existe pas ? | Par l'absurde |
| L'énoncé porte-t-il sur tous les entiers naturels, ou a-t-il une structure récursive ? | Par récurrence |
| Je suis bloqué avec la démonstration directe ? | Essayez l'absurde comme alternative |

En pratique, les mathématiciens tentent souvent d'abord la démonstration directe. Si elle cale, ils passent à l'absurde. Si l'énoncé porte sur les entiers naturels, la récurrence est généralement le bon choix.

Certains énoncés peuvent être démontrés par chacune des trois méthodes. Avec l'expérience, on développe l'intuition de l'approche la plus élégante.

---

## 6. Pièges courants

- **Supposer ce que l'on essaie de prouver.** C'est ce qu'on appelle un raisonnement circulaire (ou pétition de principe). Dans une démonstration directe, votre point de départ doit être l'hypothèse, pas la conclusion.
- **Oublier le cas de base en récurrence.** Sans le cas de base, vous n'avez pas de premier domino. L'étape de récurrence seule ne prouve rien.
- **Ne pas énoncer clairement l'hypothèse de récurrence.** Soyez explicite : « Supposons que l'énoncé est vrai pour *n = k*. » Puis utilisez cette hypothèse pour démontrer le cas *k + 1*.
- **En raisonnement par l'absurde, ne pas atteindre réellement une contradiction.** Vous devez arriver à quelque chose de définitivement faux — pas juste bizarre ou inattendu.

---

## Termes clés

| Terme | Définition |
|-------|-----------|
| **Démonstration** | Un raisonnement logique établissant qu'un énoncé mathématique est vrai dans tous les cas |
| **Axiome** | Un énoncé accepté comme vrai sans démonstration, servant de point de départ |
| **Démonstration directe** | Raisonner en avant de l'hypothèse à la conclusion en utilisant définitions et logique |
| **Démonstration par l'absurde** | Supposer la négation de la conclusion souhaitée et en déduire une contradiction |
| **Démonstration par récurrence** | Prouver un cas de base et une étape de récurrence pour établir un énoncé pour tous les entiers naturels |
| **Hypothèse de récurrence** | L'hypothèse que l'énoncé est vrai pour *n = k*, utilisée dans l'étape de récurrence |
| **Contre-exemple** | Un seul cas montrant qu'un énoncé est faux — un contre-exemple réfute une affirmation universelle |

---

## Auto-évaluation

**1. Quelle est la différence fondamentale entre une démonstration et un grand nombre d'exemples ?**
> Une démonstration établit la vérité pour tous les cas par déduction logique. Les exemples ne montrent que des cas spécifiques et ne peuvent pas exclure un contre-exemple non examiné.

**2. Dans une démonstration par l'absurde, quelles sont les trois étapes après avoir supposé la négation ?**
> Raisonner logiquement à partir de l'hypothèse, arriver à un énoncé qui contredit un fait connu, puis conclure que l'hypothèse était fausse.

**3. Quels sont les deux composants d'une démonstration par récurrence ?**
> Le cas de base (prouver l'énoncé pour la première valeur) et l'étape de récurrence (prouver que si l'énoncé est vrai pour *k*, il est aussi vrai pour *k + 1*).

**4. Vous voulez démontrer qu'aucun nombre pair supérieur à 2 n'est premier. Quelle stratégie utiliseriez-vous ?**
> Démonstration directe : par définition, un nombre pair supérieur à 2 peut s'écrire *2k* où *k > 1*, donc il a pour diviseurs 1, 2, k et 2k — ce qui signifie qu'il a un diviseur autre que 1 et lui-même, donc il n'est pas premier.

**Critères de réussite :** Appliquer avec succès la démonstration directe, par l'absurde et par récurrence à des exemples simples, et expliquer quand chaque stratégie est appropriée.

---

## Bases de recherche

- La démonstration est la méthodologie fondamentale des mathématiques, remontant aux mathématiques de la Grèce antique
- La démonstration directe, par l'absurde et par récurrence couvrent la grande majorité des techniques de démonstration de premier cycle
- Les erreurs courantes en démonstration (raisonnement circulaire, cas de base oublié) sont bien documentées dans la recherche en didactique des mathématiques
- Sur le plan pédagogique, apprendre les stratégies de démonstration avant les contenus mathématiques spécifiques améliore la capacité de raisonnement à long terme
- Sources : Consensus en enseignement des mathématiques, programme du Département de mathématiques de Streeling
- État de croyance : T(0.92) F(0.01) U(0.05) C(0.02)
