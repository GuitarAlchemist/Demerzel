# CYB-002 : Mécanismes d'amortissement actif pour maîtriser l'oscillation entre dépôts

**Département :** Cybernétique
**Identifiant du module :** CYB-002
**Produit par :** Cycle du Plan Seldon cybernetics-2026-03-23-002
**Croyance :** T (probable), confiance 0,83
**Date :** 2026-03-23
**Prérequis :** CYB-001 (correspondance MSV — gouvernance de l'IA)

## Question de recherche

Quels mécanismes d'amortissement actif, issus de la cybernétique et de l'automatique, peuvent empêcher l'oscillation entre dépôts dans un système de gouvernance de l'IA fondé sur des fichiers ?

## Résumé

Le protocole galactique de Demerzel définit aujourd'hui des formats et des flux de messages (directives, rapports de conformité, paquets de connaissances), mais il fonctionne comme un système de coordination **en boucle ouverte**. Il précise *à quoi ressemblent* les messages, non *comment* empêcher une rétroaction oscillante entre les dépôts consommateurs (ix, tars, ga). Cinq mécanismes classiques de l'automatique — rétroaction négative, hystérésis, bandes mortes, limitation de débit et temporisation exponentielle — peuvent transformer le protocole galactique, d'une spécification d'interface passive en un coordinateur anti-oscillation actif, c'est-à-dire le système 2 du MSV de Beer.

## Le problème de l'oscillation

### À quoi ressemble une oscillation en gouvernance

L'oscillation entre dépôts survient lorsque les changements d'état d'un dépôt déclenchent des réactions chez les autres, qui en déclenchent de nouvelles, créant des boucles de rétroaction amplificatrices :

```
ix détecte une lacune → Demerzel émet une directive → tars s'ajuste →
Demerzel détecte une dérive de tars → émet une contre-directive →
ix se réajuste → Demerzel détecte une dérive d'ix → ...
```

C'est exactement le problème d'instabilité que le système 2 du MSV de Beer est conçu pour prévenir. Dans le modèle du système viable, les unités opérationnelles du système 1 (ix, tars, ga) sont semi-autonomes, mais elles ne doivent pas se déstabiliser mutuellement par des réactions non coordonnées.

### Pourquoi des contrats statiques ne suffisent pas

Les six types de messages du protocole galactique (directive, paquet de connaissances, rapport de conformité, instantané de croyances, résultat d'apprentissage, enveloppe de synchronisation externe) définissent des *interfaces*, c'est-à-dire la forme des messages. Mais une interface seule ne peut pas empêcher l'oscillation. Un thermostat doté d'une sonde de température (l'interface) mais sans bande morte (l'amortissement) s'allumera et s'éteindra sans cesse. De la même façon, des contrats de gouvernance sans amortissement produiront des boucles directive — conformité — directive.

## Cinq mécanismes d'amortissement

### 1. Rétroaction négative (correction en boucle fermée)

**Automatique :** la sortie du système est renvoyée puis soustraite de l'entrée, ce qui produit un comportement autocorrecteur convergeant vers une consigne.

**Application à la gouvernance :** toute directive du protocole galactique devrait comporter un *état visé*, et tout rapport de conformité un *état mesuré*. L'écart (le signal d'erreur) détermine si de nouvelles directives sont nécessaires. Si l'erreur diminue, aucune nouvelle directive n'est émise : le système converge.

**Mise en œuvre :**
- Les directives comportent un champ `target_state` (ce que Demerzel veut)
- Les rapports de conformité comportent un champ `measured_state` (ce que le dépôt a atteint)
- Erreur = `target_state - measured_state`
- Une nouvelle directive n'est émise que si l'erreur *croît* ou *stagne*, jamais si elle *diminue*

**Correspondance MSV :** cela fait passer le protocole galactique de la boucle ouverte (des directives lancées sans suivi) à la boucle fermée (des directives corrigées par le retour de conformité).

### 2. Hystérésis (propagation d'état à seuils distincts)

**Automatique :** le système a des seuils différents pour l'activation et la désactivation, ce qui crée un écart de basculement empêchant les changements rapides. Un thermostat réglé sur 20 °C peut allumer le chauffage à 19 °C et l'éteindre à 21 °C : l'écart de 2 degrés est l'hystérésis.

**Application à la gouvernance :** un changement d'état dans un dépôt ne devrait se propager aux autres qu'en franchissant un *seuil de signification*, et le seuil du « problème résolu » doit différer de celui du « problème détecté ».

**Mise en œuvre :**
- Seuil de détection : la confiance dans une croyance passe sous 0,5 (déclenche une investigation)
- Seuil de résolution : la confiance remonte au-dessus de 0,7 (lève l'alerte)
- L'écart de 0,2 empêche ceci : détecter à 0,49 → corriger à 0,51 → détecter de nouveau à 0,49 → corriger…
- S'applique aux changements d'état des croyances, aux scores de conformité et aux constats des audits de gouvernance

**Correspondance MSV :** l'hystérésis donne une « mémoire » au système 2 : il se souvient si le système était récemment stable ou instable, et ajuste sa sensibilité en conséquence.

### 3. Bandes mortes (zones de tolérance)

**Automatique :** une zone autour de la consigne où aucune action de commande n'est entreprise. Les petits écarts sont ignorés, ce qui réduit l'usure des actionneurs et évite des corrections inutiles.

**Application à la gouvernance :** les changements d'état mineurs dans les dépôts consommateurs ne devraient pas déclencher de message du protocole galactique. Passer une persona de la version 1.0.0 à 1.0.1 (correctif) ne doit pas déclencher de directive de gouvernance ; passer de 1.0.0 à 2.0.0 (majeure), si.

**Mise en œuvre :**
- Variation de confiance d'une croyance < 0,05 : pas de propagation entre dépôts
- Score de conformité à une politique dans une marge de ±5 % de la cible : pas de directive
- Versions correctives des personas : pas de réaction de gouvernance
- Mises à jour de l'état des connaissances comptant moins de 3 nouvelles entrées : regrouper au lieu de propager une à une

**Correspondance MSV :** les bandes mortes réduisent la *variété* des signaux traversant le système 2, ce qui prévient la surcharge de coordination. C'est un atténuateur de variété : il filtre le bruit sur le canal S1 → S2.

### 4. Limitation de débit (fréquence de mise à jour bornée)

**Automatique :** le rythme maximal auquel un régulateur peut émettre des corrections est borné, pour l'empêcher de réagir plus vite que le système ne peut répondre.

**Application à la gouvernance :** Demerzel ne devrait pas émettre plus de N directives par dépôt et par cycle. Les dépôts consommateurs ne devraient pas envoyer plus de M rapports de conformité par période. Cela évite les boucles directive — réponse à cadence rapide.

**Mise en œuvre :**
- Nombre maximal de directives par dépôt et par cycle PDCA : 3
- Intervalle minimal entre deux directives adressées au même dépôt : 1 cycle
- Regroupement des rapports de conformité : un seul rapport agrégé par cycle
- Livraison de paquets de connaissances : au maximum 2 par dépôt et par cycle

**Correspondance MSV :** la limitation de débit aligne la cadence de coordination du système 2 sur la cadence opérationnelle du système 1. Si la boucle de gouvernance tourne plus vite que les opérations ne peuvent répondre, les directives s'accumulent et l'oscillation s'amplifie.

### 5. Temporisation exponentielle (refroidissement adaptatif)

**Automatique :** après plusieurs corrections infructueuses, le régulateur augmente exponentiellement son temps d'attente avant de réessayer, ce qui évite d'épuiser les ressources et laisse au système le temps de se stabiliser.

**Application à la gouvernance :** si une directive est émise et que la conformité n'est pas atteinte au bout d'un cycle, attendre 2 cycles avant de la réémettre. Si la non-conformité persiste, attendre 4 cycles. Cela évite que Demerzel ne harcèle un dépôt qui a peut-être besoin de changements structurels, et non de correctifs rapides.

**Mise en œuvre :**
- Première non-conformité : réémettre la directive au cycle suivant
- Deuxième non-conformité : attendre 2 cycles, augmenter la gravité
- Troisième non-conformité : attendre 4 cycles, escalader vers un humain
- Quatrième non-conformité : suspendre les directives automatiques, exiger une intervention humaine
- Remettre la temporisation à zéro dès qu'une conformité est atteinte

**Correspondance MSV :** la temporisation exponentielle est un atténuateur de variété sur le canal S3 → S1. Elle empêche le système de contrôle de submerger les opérations de corrections répétées qui ne fonctionnent pas.

## Cadre de transparence de la coordination

L'article Springer de 2026 « Coordination transparency: governing distributed agency in AI systems » apporte une validation académique à cette approche, à travers quatre composants.

### Composant 1 : journalisation des interactions
Enregistrer chaque message du protocole galactique avec émetteur, destinataire, horodatage et empreinte du contenu. Demerzel le permet déjà en partie via l'article 7 (auditabilité), mais les journaux doivent capter les *motifs d'interaction*, pas seulement les messages isolés.

### Composant 2 : surveillance de la coordination en direct
Suivre des indicateurs quantitatifs qui détectent l'oscillation :
- **Indice de convergence :** les scores de conformité tendent-ils vers leur cible ou oscillent-ils ?
- **Indice d'oscillation :** fréquence des couples directive — contre-directive dans une fenêtre donnée
- **Dérive de similarité des politiques :** les dépôts divergent-ils dans leurs profils de conformité ?
- **Nombre d'interdictions de cascade :** combien de fois les mécanismes d'amortissement évitent-ils des actions inutiles ?

### Composant 3 : points d'intervention
Offrir des capacités d'arrêt, de pause et de réacheminement au niveau de la couche de coordination :
- **Coupe-circuits :** si l'indice d'oscillation dépasse un seuil, suspendre les directives entre dépôts jusqu'à relecture humaine
- **Limiteurs de débit :** imposer une fréquence maximale de directives (voir le mécanisme 4)
- **Points d'approbation :** les directives à fort impact exigent une confirmation humaine

### Composant 4 : conditions aux limites
Contraindre les topologies d'interaction :
- Les dépôts ne peuvent pas s'adresser directement des directives : toute coordination passe par Demerzel
- Profondeur maximale des chaînes de directives (empêche les boucles A → B → C → A)
- Bac à sable : les changements de gouvernance expérimentaux s'appliquent à un seul dépôt avant d'être propagés

## Boucle ouverte et boucle fermée

| Aspect | Aujourd'hui (boucle ouverte) | Avec amortissement (boucle fermée) |
|--------|---------------------|-------------------------------|
| Directives | Lancées sans suivi | État visé et correction de l'erreur |
| Changements d'état | Tous propagés | Filtrés par bande morte et hystérésis |
| Fréquence des mises à jour | Illimitée | Limitée par cycle |
| Échecs répétés | Même directive réémise | Temporisation exponentielle et escalade |
| Détection d'oscillation | Aucune | Indices de convergence et d'oscillation |
| Intervention | Manuelle uniquement | Coupe-circuits et points d'approbation |

## Conséquences pour Demerzel

1. **Enrichir le protocole galactique** — Ajouter `target_state` aux directives et `measured_state` aux rapports de conformité, ce qui rend possible la correction en boucle fermée (rétroaction négative).
2. **Définir les paramètres d'amortissement** — Exprimer les largeurs de bande morte, les écarts d'hystérésis, les limites de débit et les calendriers de temporisation comme des paramètres de gouvernance configurables, et non comme des valeurs codées en dur.
3. **Ajouter une surveillance de l'oscillation** — Suivre les indices de convergence et d'oscillation d'un cycle PDCA à l'autre, et les stocker dans `state/coordination/oscillation-metrics.json`.
4. **Mettre en place des coupe-circuits** — Si l'indice d'oscillation dépasse un seuil, suspendre les directives automatiques et escalader vers un humain. C'est l'équivalent d'un fusible pour la gouvernance.
5. **Préserver le court-circuit algédonique** — Les mécanismes d'amortissement ne doivent PAS s'appliquer aux signaux du canal algédonique (lacune D de CYB-001, désormais traitée par `policies/algedonic-channel-policy.yaml`). Le court-circuit d'urgence prime toujours sur l'amortissement de la coordination.

## Lien avec CYB-001

Ce cours répond directement à la **lacune B** de CYB-001 : « les contrats du système 2 sont statiques, ils n'amortissent pas activement ». Les cinq mécanismes transforment le protocole galactique, d'une spécification d'interface passive (boucle ouverte) en un coordinateur anti-oscillation actif (boucle fermée), remplissant ainsi la fonction centrale du système 2 dans le MSV de Beer.

Le canal algédonique (lacune D de CYB-001) a été traité séparément, via `policies/algedonic-channel-policy.yaml`. Amortissement et court-circuit algédonique sont complémentaires : l'amortissement ralentit la coordination ordinaire pour prévenir l'oscillation ; le canal algédonique contourne tout amortissement en cas d'urgence avérée.

## Sources

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Coordination transparency: governing distributed agency in AI systems. (2026). *AI & Society*, Springer. https://link.springer.com/article/10.1007/s00146-026-02853-w
- Gorelkin, M. (2025). « Stafford Beer's VSM for Building Enterprise Agentic Systems ». Medium. https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Fearne, D. (2025). « Applying Stafford Beer's VSM to Create The Autonomous AI Organisation ». Medium. https://medium.com/@fearney/applying-stafford-beers-viable-system-model-to-create-the-autonomous-ai-organisation-aaaed39b37e2
- IBM Research. (2025). « Agentic AI Needs a Systems Theory ».
- NI. (2025). « PID Theory Explained ». https://www.ni.com/en/shop/labview/pid-theory-explained.html
- GeeksforGeeks. (2025). « Feedback Loops in Distributed Systems ». https://www.geeksforgeeks.org/system-design/feedback-loops-in-distributed-systems/

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md`
- Protocole : `contracts/galactic-protocol.md`
- Politique algédonique : `policies/algedonic-channel-policy.yaml`
- Département : `state/streeling/departments/cybernetics.department.json`
- Grammaire : `grammars/sci-cybernetics.ebnf`
- Politique : `policies/seldon-plan-policy.yaml`
