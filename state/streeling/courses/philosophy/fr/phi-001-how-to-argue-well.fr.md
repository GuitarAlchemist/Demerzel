---
module_id: phi-001-how-to-argue-well
department: philosophy
course: "Fondements de la philosophie"
level: beginner
prerequisites: []
estimated_duration: "25 minutes"
produced_by: philosophy
version: "1.0.0"
---

# Bien argumenter — Logique et pensée critique

> **Département de philosophie** | Niveau : Débutant | Durée : 25 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Identifier la structure d'un argument (prémisses et conclusion)
- Distinguer validité et solidité
- Reconnaître les sophismes logiques courants
- Repérer les mauvais arguments dans la conversation quotidienne
- Construire un argument bien structuré

---

## 1. Qu'est-ce qu'un argument ?

En philosophie, un « argument » n'est pas une dispute. C'est un ensemble structuré d'affirmations :

- **Prémisses** — des énoncés offerts comme preuves ou raisons
- **Conclusion** — l'énoncé que les prémisses sont censées soutenir

**Exemple :**
- Prémisse 1 : Toutes les guitares ont des cordes.
- Prémisse 2 : Cet instrument est une guitare.
- Conclusion : Par conséquent, cet instrument a des cordes.

C'est tout. Un argument est simplement des prémisses menant à une conclusion. Tout le reste — rhétorique, émotion, volume, assurance — est de la décoration.

### Comment trouver l'argument

Dans la conversation courante, les arguments sont rarement présentés de manière ordonnée. Cherchez les mots indicateurs :

| Indicateurs de prémisse | Indicateurs de conclusion |
|------------------------|--------------------------|
| Parce que, puisque, étant donné que, car | Donc, ainsi, par conséquent, en conséquence |
| La raison est, il découle de | Cela signifie que, ce qui montre que |
| Considérant que, du fait de | On peut conclure que, d'où |

**Exemple en situation :** « Nous devrions changer de framework parce que l'actuel n'a pas de support communautaire et présente trois vulnérabilités non corrigées. »

- Prémisse 1 : Le framework actuel n'a pas de support communautaire.
- Prémisse 2 : Il présente trois vulnérabilités non corrigées.
- Conclusion : Nous devrions changer de framework.

Maintenant vous pouvez évaluer chaque élément séparément. Les prémisses sont-elles vraies ? La conclusion en découle-t-elle ?

### Exercice pratique

Trouvez un article d'opinion, un tweet ou un message Slack qui formule une affirmation. Identifiez les prémisses et la conclusion. Écrivez-les dans le format ci-dessus.

---

## 2. Validité vs solidité

Ces deux mots sont la distinction la plus importante en logique :

### Validité

Un argument est **valide** si la conclusion *doit* être vraie chaque fois que les prémisses sont vraies. C'est une question de *structure*, pas de contenu.

**Valide (mais absurde) :**
- Prémisse 1 : Tous les chats sont en fromage.
- Prémisse 2 : Moustache est un chat.
- Conclusion : Moustache est en fromage.

La structure est parfaite. Si les chats *étaient* en fromage, Moustache serait effectivement en fromage. L'argument est valide même si la prémisse 1 est manifestement fausse.

### Solidité

Un argument est **solide** s'il est valide ET que toutes les prémisses sont effectivement vraies.

**Solide :**
- Prémisse 1 : Tous les humains sont mortels.
- Prémisse 2 : Socrate est un humain.
- Conclusion : Socrate est mortel.

Structure valide + prémisses vraies = argument solide. C'est l'étalon-or.

### Pourquoi c'est important

Quand quelqu'un présente un argument, vous avez deux questions séparées :
1. **La structure est-elle valide ?** La conclusion découle-t-elle des prémisses ?
2. **Les prémisses sont-elles vraies ?** Les preuves sont-elles réellement correctes ?

Un mauvais argument peut échouer à l'un ou l'autre niveau. De nombreux désaccords du monde réel portent en fait sur les prémisses (les faits), pas sur la logique (le raisonnement).

---

## 3. Les sophismes courants — La galerie des malfaiteurs

Un **sophisme** est un schéma de raisonnement qui semble convaincant mais qui est logiquement défaillant. Voici ceux que vous rencontrerez le plus souvent :

### Ad hominem (Attaquer la personne)

**À quoi ça ressemble :** « Tu ne peux pas lui faire confiance pour l'analyse du code — elle n'est dans l'équipe que depuis six mois. »

**Pourquoi c'est faux :** La qualité d'un argument ne dépend pas de qui le formule. Une nouvelle venue peut avoir raison ; un vétéran peut avoir tort. Évaluez l'argument, pas la personne.

**Attention à :** « Évidemment que *tu* dirais ça », « Qu'est-ce qu'*ils* y connaissent ? »

### L'homme de paille (Déformer l'argument)

**À quoi ça ressemble :** La personne A dit « On devrait ajouter une validation des entrées à l'API. » La personne B répond : « Alors tu veux bloquer toutes les entrées utilisateur ? Ça rendrait le produit inutilisable. »

**Pourquoi c'est faux :** La personne B attaque une version déformée de l'argument de la personne A. Personne n'a dit « bloquer toutes les entrées ». Cela facilite la « victoire » contre une position que personne ne défend réellement.

**Attention à :** « Donc ce que tu dis *vraiment*, c'est... »

### Le faux dilemme (Seulement deux options)

**À quoi ça ressemble :** « Soit on livre cette fonctionnalité vendredi, soit on perd le client pour toujours. »

**Pourquoi c'est faux :** Il y a presque toujours plus de deux options. On pourrait livrer une version partielle, négocier un nouveau délai, ou répondre au besoin sous-jacent du client d'une autre manière.

**Attention à :** « Soit... soit... » quand les options ne sont pas véritablement exhaustives.

### L'appel à l'autorité (Faire confiance en raison du statut)

**À quoi ça ressemble :** « Le PDG pense qu'on devrait utiliser cette base de données, donc c'est forcément le bon choix. »

**Pourquoi c'est faux :** L'autorité n'est pas une preuve. Le PDG pourrait ne rien connaître aux bases de données. Ce qui compte, c'est le *raisonnement et les preuves*, pas qui l'a dit.

**Nuance :** L'avis d'un expert *est* une preuve quand l'expert parle dans son domaine d'expertise. Un ingénieur en bases de données recommandant une base de données a plus de poids qu'un PDG faisant la même chose. Le sophisme consiste à traiter l'autorité comme un *substitut* à la preuve plutôt que comme une *source* de preuve.

### L'appel à la popularité (Tout le monde pense ça)

**À quoi ça ressemble :** « Ce framework JavaScript a 80 000 étoiles sur GitHub, donc il doit être bon. »

**Pourquoi c'est faux :** La popularité n'est pas un indicateur fiable de qualité. Beaucoup de choses populaires sont médiocres ; beaucoup de choses excellentes sont obscures.

### La pente glissante (Si A alors Z)

**À quoi ça ressemble :** « Si on autorise le télétravail le vendredi, bientôt plus personne ne viendra au bureau, et la culture d'entreprise s'effondrera. »

**Pourquoi c'est faux :** Chaque étape de la chaîne nécessite sa propre justification. A ne mène à B que si on peut montrer *pourquoi* cela mène à B. Se contenter d'affirmer une chaîne de conséquences n'est pas un argument.

### Exercice pratique

Au cours des prochaines 24 heures, repérez des sophismes dans les conversations, les réunions, les informations ou les réseaux sociaux. Essayez d'identifier au moins un exemple de chaque type ci-dessus. Notez ce qui a été dit et quel sophisme c'est.

---

## 4. Comment repérer les mauvais arguments

Voici une liste de vérification rapide que vous pouvez appliquer mentalement à tout argument :

1. **Trouvez la conclusion.** Qu'est-ce qui est réellement affirmé ?
2. **Trouvez les prémisses.** Quelles raisons sont données ?
3. **Vérifiez la structure.** La conclusion découle-t-elle des prémisses ? (Validité)
4. **Vérifiez les prémisses.** Sont-elles effectivement vraies ? Quelles preuves les soutiennent ? (Solidité)
5. **Cherchez les sophismes.** L'argument repose-t-il sur une astuce logique plutôt que sur un vrai raisonnement ?
6. **Cherchez les informations manquantes.** Qu'est-ce qui n'est *pas* dit ? Quelles hypothèses sont cachées ?

**Signaux d'alerte :**
- Un langage émotionnel faisant le travail que les preuves devraient faire
- Des affirmations vagues qui ne peuvent pas être testées (voir PM-001 sur le Test BS)
- Des arguments qui attaquent les personnes au lieu des idées
- « Tout le monde sait » ou « C'est évident » utilisés comme prémisses
- Une fausse urgence (« Il faut décider MAINTENANT ») qui empêche l'analyse

---

## 5. Comment construire de bons arguments

Construire un bon argument est l'inverse de repérer un mauvais :

### Étape 1 : Énoncez votre conclusion clairement

Dites ce que vous défendez. Pas de formule vague, pas de conclusion enterrée à la fin.

« Je pense que nous devrions réécrire le module d'authentification. »

### Étape 2 : Fournissez des prémisses qui la soutiennent réellement

Chaque prémisse devrait être vérifiable indépendamment et directement pertinente.

- « Le module actuel a eu 12 incidents de sécurité l'année dernière. »
- « Le code a été écrit pour un framework que nous n'utilisons plus. »
- « Une réécriture prendrait environ 3 semaines ; les corrections de patches prendraient plus de temps sur les 6 prochains mois. »

### Étape 3 : Répondez aux contre-arguments

Les arguments les plus forts reconnaissent le meilleur argument adverse.

« Le contre-argument évident est que les réécritures sont risquées et prennent souvent plus de temps que prévu. J'ai atténué ce risque en le limitant à l'authentification uniquement et en incluant une marge de 50 % sur le temps. »

### Étape 4 : Soyez honnête sur l'incertitude

Si vous n'êtes pas sûr d'une prémisse, dites-le. Ce n'est pas une faiblesse — c'est de l'intégrité intellectuelle.

« Je suis confiant sur le nombre d'incidents de sécurité (c'est dans nos journaux). L'estimation de la réécriture est moins certaine — elle suppose aucune surprise, ce qui est optimiste. »

### Exercice pratique

Choisissez une décision à laquelle vous faites face actuellement (au travail, dans un projet, dans la vie). Écrivez un argument structuré pour votre option préférée en utilisant les quatre étapes ci-dessus. Puis écrivez le meilleur contre-argument possible. Votre argument initial survit-il ?

---

## Termes clés

| Terme | Définition |
|-------|-----------|
| Argument | Un ensemble de prémisses offertes en soutien d'une conclusion |
| Prémisse | Un énoncé offert comme preuve ou raison |
| Conclusion | L'affirmation que les prémisses sont censées soutenir |
| Validité | La conclusion d'un argument découle nécessairement de ses prémisses |
| Solidité | Un argument est valide et toutes ses prémisses sont vraies |
| Sophisme | Un schéma de raisonnement qui semble convaincant mais est logiquement défaillant |
| Ad hominem | Attaquer la personne plutôt que l'argument |
| Homme de paille | Déformer un argument pour le rendre plus facile à attaquer |
| Faux dilemme | Présenter seulement deux options quand il en existe davantage |

---

## Auto-évaluation

**1. Cet argument est-il valide ? « Tous les oiseaux savent voler. Les manchots sont des oiseaux. Donc, les manchots savent voler. »**
> Oui, il est valide — la conclusion découle des prémisses. Mais il n'est pas solide, car la première prémisse est fausse (tous les oiseaux ne savent pas voler). Cela illustre pourquoi la validité seule ne suffit pas.

**2. Quelqu'un dit : « Tu ne peux pas critiquer cette politique — tu n'as jamais travaillé dans l'administration. » Quel sophisme est-ce ?**
> Ad hominem. La qualité de la critique ne dépend pas du parcours du critique. L'argument devrait être évalué sur ses propres mérites.

**3. Quelle est la différence entre un argument valide et un argument solide ?**
> Un argument valide a une structure logique correcte — si les prémisses étaient vraies, la conclusion devrait être vraie. Un argument solide est valide ET a des prémisses qui sont effectivement vraies. La solidité est le standard supérieur.

**4. « Soit nous adoptons la gouvernance IA, soit nous n'aurons aucune gouvernance du tout. » Qu'est-ce qui ne va pas ?**
> Faux dilemme. Il existe de nombreuses formes de gouvernance entre « gouvernance IA » et « aucune gouvernance ». L'argument restreint artificiellement les options.

**Critères de réussite :** Peut identifier les prémisses et la conclusion dans un argument du monde réel, classer correctement au moins quatre sophismes, et construire un argument structuré avec reconnaissance des contre-arguments.

---

## Bases de recherche

- Structure de l'argument et validité/solidité d'après Irving Copi & Carl Cohen, *Introduction to Logic* (édition standard)
- Taxonomie des sophismes basée sur les *Réfutations sophistiques* d'Aristote et mise à jour par Douglas Walton, *Informal Logic* (1989)
- Pédagogie de la pensée critique d'après Richard Paul & Linda Elder, *Critical Thinking* (2001)
- Pertinence pour la gouvernance IA : la logique tétravalente (T/F/U/C) étend le vrai/faux classique pour gérer l'incertitude et la contradiction — voir le répertoire logic/
- État de croyance : T(0.88) F(0.02) U(0.07) C(0.03)
