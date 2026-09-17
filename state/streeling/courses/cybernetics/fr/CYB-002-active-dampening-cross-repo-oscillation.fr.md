# CYB-002 : Mécanismes d'amortissement actif pour maîtriser l'oscillation entre dépôts

**Département :** Cybernétique
**Identifiant du module :** CYB-002
**Produit par :** cycle du plan Seldon cybernetics-2026-03-23-002
**Croyance :** T (probable), confiance 0.83
**Date :** 2026-03-23
**Prérequis :** CYB-001 (Correspondance entre le VSM et la gouvernance de l'IA)

## Question de recherche

Quels mécanismes d'amortissement actif issus de la cybernétique et de la théorie du contrôle peuvent empêcher l'oscillation entre dépôts dans un système de gouvernance de l'IA fondé sur des fichiers ?

## Résumé

Le Galactic Protocol de Demerzel définit actuellement des formats et des flux de messages (directives, rapports de conformité, paquets de connaissances), mais fonctionne comme un système de coordination **en boucle ouverte**. Il précise *à quoi* ressemblent les messages, pas *comment* empêcher une rétroaction oscillatoire entre les dépôts consommateurs (ix, tars, ga). Cinq mécanismes classiques de la théorie du contrôle — rétroaction négative, hystérésis, zones mortes, limitation de débit et temporisation exponentielle — peuvent transformer le Galactic Protocol, simple spécification d'interface passive, en un Système 2 actif (coordinateur anti-oscillation) au sens du VSM de Beer.

## Le problème de l'oscillation

### À quoi ressemble l'oscillation en gouvernance

L'oscillation entre dépôts se produit quand des changements d'état dans un dépôt déclenchent des réactions dans les autres, qui déclenchent à leur tour d'autres réactions, créant des boucles de rétroaction amplificatrices :

```
ix detects gap → Demerzel issues directive → tars adjusts →
Demerzel detects tars drift → issues counter-directive →
ix re-adjusts → Demerzel detects ix drift → ...
```

C'est le même problème d'instabilité que le Système 2 du VSM de Beer a été conçu pour empêcher. Dans le modèle du système viable, les unités opérationnelles du Système 1 (ix, tars, ga) sont semi-autonomes, mais ne doivent pas se déstabiliser mutuellement par des réactions non coordonnées.

### Pourquoi les contrats statiques ne suffisent pas

Les six types de messages du Galactic Protocol (directive, knowledge-package, compliance-report, belief-snapshot, learning-outcome, external-sync-envelope) définissent des *interfaces* — la forme des messages. Mais les interfaces seules ne peuvent pas empêcher l'oscillation. Un thermostat doté d'un capteur de température (interface) mais sans zone morte (amortissement) s'allumera et s'éteindra sans cesse. De même, des contrats de gouvernance sans amortissement produiront des boucles directive-conformité-directive.

## Cinq mécanismes d'amortissement

### 1. Rétroaction négative (correction en boucle fermée)

**Théorie du contrôle :** La sortie d'un système est réinjectée et soustraite de l'entrée, ce qui produit un comportement autocorrecteur qui converge vers une consigne.

**Application à la gouvernance :** Chaque directive du Galactic Protocol devrait inclure un *état cible* et chaque rapport de conformité un *état mesuré*. La différence (signal d'erreur) détermine si d'autres directives sont nécessaires. Si l'erreur diminue, aucune nouvelle directive n'est émise — le système converge.

**Mise en œuvre :**
- Les directives incluent un champ `target_state` (ce que Demerzel veut)
- Les rapports de conformité incluent un champ `measured_state` (ce que le dépôt a atteint)
- Erreur = `target_state - measured_state`
- De nouvelles directives ne sont émises que lorsque l'erreur *croît* ou *stagne*, pas lorsqu'elle *diminue*

**Correspondance VSM :** Cela fait passer le Galactic Protocol de la boucle ouverte (directives « tire et oublie ») à la boucle fermée (directives corrigées par le retour de conformité).

### 2. Hystérésis (propagation d'état conditionnée par des seuils)

**Théorie du contrôle :** Un système a des seuils différents pour l'activation et la désactivation, ce qui crée un écart de commutation qui empêche les basculements rapides. Un thermostat réglé sur 20C peut allumer le chauffage à 19C et l'éteindre à 21C — l'écart de 2 degrés est l'hystérésis.

**Application à la gouvernance :** Les changements d'état dans un dépôt ne devraient se propager aux autres que lorsqu'ils franchissent un *seuil de signification*, et le seuil de « problème résolu » devrait différer du seuil de « problème détecté ».

**Mise en œuvre :**
- Seuil de détection : la confiance d'une croyance passe sous 0.5 (déclenche une investigation)
- Seuil de résolution : la confiance d'une croyance remonte au-dessus de 0.7 (lève le signalement)
- L'écart de 0.2 empêche : détection à 0.49 → correction à 0.51 → nouvelle détection à 0.49 → correction...
- S'applique à : changements d'état de croyance, scores de conformité, constats d'audit de gouvernance

**Correspondance VSM :** L'hystérésis donne au Système 2 une « mémoire » — il se souvient si le système était récemment stable ou instable et ajuste sa sensibilité en conséquence.

### 3. Zones mortes (zones de tolérance)

**Théorie du contrôle :** Une région autour de la consigne où aucune action de contrôle n'est entreprise. Les petits écarts sont ignorés, ce qui réduit l'usure des actionneurs et évite les corrections inutiles.

**Application à la gouvernance :** Les changements d'état mineurs dans les dépôts consommateurs ne devraient pas déclencher de messages du Galactic Protocol. Un passage de version d'une persona de 1.0.0 à 1.0.1 (correctif) ne devrait pas déclencher de directive de gouvernance, alors qu'un passage de 1.0.0 à 2.0.0 (majeur) le devrait.

**Mise en œuvre :**
- Variations de confiance d'une croyance < 0.05 : pas de propagation entre dépôts
- Scores de conformité aux politiques à +/-5% de la cible : pas de directive
- Versions correctives des personas : pas de réaction de gouvernance
- Mises à jour de l'état des connaissances avec < 3 nouvelles entrées : regrouper, ne pas propager une à une

**Correspondance VSM :** Les zones mortes réduisent la *variété* des signaux qui traversent le Système 2, évitant la surcharge de coordination. C'est un atténuateur de variété — il filtre le bruit du canal S1 vers S2.

### 4. Limitation de débit (fréquence de mise à jour bornée)

**Théorie du contrôle :** Le débit maximal auquel un contrôleur peut émettre des corrections est borné, ce qui l'empêche de réagir plus vite que le système ne peut répondre.

**Application à la gouvernance :** Demerzel ne devrait pas émettre plus de N directives par dépôt et par cycle. Les dépôts consommateurs ne devraient pas envoyer plus de M rapports de conformité par période. Cela empêche les boucles directive-réponse en rafale.

**Mise en œuvre :**
- Nombre maximal de directives par dépôt par cycle PDCA : 3
- Intervalle minimal entre deux directives au même dépôt : 1 cycle
- Regroupement des rapports de conformité : agréger en un seul rapport par cycle
- Livraison des paquets de connaissances : 2 au maximum par dépôt par cycle

**Correspondance VSM :** La limitation de débit aligne la cadence de coordination du Système 2 sur la cadence opérationnelle du Système 1. Si la boucle de gouvernance tourne plus vite que les opérations ne peuvent répondre, les directives s'accumulent et l'oscillation s'amplifie.

### 5. Temporisation exponentielle (refroidissement adaptatif)

**Théorie du contrôle :** Après des corrections échouées à répétition, le contrôleur augmente exponentiellement le temps d'attente avant de réessayer, ce qui évite l'épuisement des ressources et laisse au système le temps de se stabiliser.

**Application à la gouvernance :** Si une directive est émise et que la conformité n'est pas atteinte après un cycle, attendre 2 cycles avant de la réémettre. En cas de non-conformité persistante, attendre 4 cycles. Cela évite que Demerzel ne martèle un dépôt qui a peut-être besoin de changements structurels (et non de simples correctifs rapides).

**Mise en œuvre :**
- Première non-conformité : réémettre la directive au cycle suivant
- Deuxième non-conformité : attendre 2 cycles, relever la gravité
- Troisième non-conformité : attendre 4 cycles, escalader vers un humain
- Quatrième non-conformité : arrêter les directives automatisées, exiger une intervention humaine
- Remettre la temporisation à 0 en cas de conformité réussie

**Correspondance VSM :** La temporisation exponentielle est un atténuateur de variété sur le canal S3 vers S1. Elle empêche le système de contrôle de submerger les opérations de corrections répétées qui ne fonctionnent pas.

## Cadre de transparence de la coordination

L'article Springer de 2026 « Coordination transparency: governing distributed agency in AI systems » apporte une validation académique à cette approche à travers quatre composantes :

### Composante 1 : journalisation des interactions
Enregistrer chaque message du Galactic Protocol avec l'émetteur, le destinataire, l'horodatage et l'empreinte du contenu. Demerzel le permet déjà en partie via l'article 7 (Auditabilité), mais les journaux doivent capturer les *schémas d'interaction*, et pas seulement des messages isolés.

### Composante 2 : surveillance de la coordination en direct
Suivre des métriques quantitatives qui détectent l'oscillation :
- **Indice de convergence :** Les scores de conformité tendent-ils vers leurs cibles ou oscillent-ils ?
- **Indice d'oscillation :** Fréquence des paires directive-contre-directive dans une fenêtre
- **Dérive de similarité des politiques :** Les dépôts divergent-ils dans leurs profils de conformité à la gouvernance ?
- **Nombre d'interruptions de cascade :** À quelle fréquence les mécanismes d'amortissement empêchent-ils des actions inutiles ?

### Composante 3 : points d'intervention
Fournir des capacités d'arrêt, de pause et de réacheminement au niveau de la couche de coordination :
- **Disjoncteurs :** Si l'indice d'oscillation dépasse un seuil, suspendre les directives entre dépôts jusqu'à une revue humaine
- **Limiteurs de débit :** Imposer une fréquence maximale de directives (voir le mécanisme 4)
- **Portes d'approbation :** Les directives à fort impact exigent une confirmation humaine

### Composante 4 : conditions aux limites
Contraindre les topologies d'interaction :
- Les dépôts ne peuvent pas déclencher directement de directives les uns vers les autres (toute la coordination passe par Demerzel)
- Profondeur maximale des chaînes de directives (empêche les boucles A→B→C→A)
- Bac à sable : les changements de gouvernance expérimentaux s'appliquent à un seul dépôt avant d'être propagés

## Comparaison boucle ouverte / boucle fermée

| Aspect | Actuel (boucle ouverte) | Avec amortissement (boucle fermée) |
|--------|---------------------|-------------------------------|
| Directives | Tire et oublie | État cible + correction d'erreur |
| Changements d'état | Tous propagés | Filtrés par zone morte + hystérésis |
| Fréquence de mise à jour | Illimitée | Limitée par cycle |
| Échecs répétés | Même directive réémise | Temporisation exponentielle + escalade |
| Détection d'oscillation | Aucune | Indices de convergence/d'oscillation |
| Intervention | Manuelle uniquement | Disjoncteurs + portes d'approbation |

## Implications pour Demerzel

1. **Enrichir le Galactic Protocol** — Ajouter `target_state` aux directives et `measured_state` aux rapports de conformité, pour permettre une correction en boucle fermée (rétroaction négative).
2. **Définir les paramètres d'amortissement** — Spécifier la largeur des zones mortes, les écarts d'hystérésis, les limites de débit et les calendriers de temporisation comme des paramètres de gouvernance configurables, et non comme des valeurs codées en dur.
3. **Ajouter une surveillance de l'oscillation** — Suivre les indices de convergence et d'oscillation au fil des cycles PDCA. Les stocker dans `state/coordination/oscillation-metrics.json`.
4. **Mettre en place des disjoncteurs** — Si l'indice d'oscillation dépasse un seuil, arrêter les directives automatisées et escalader vers un humain. C'est l'équivalent, en gouvernance, d'un fusible.
5. **Préserver le contournement algédonique** — Les mécanismes d'amortissement ne doivent PAS s'appliquer aux signaux du canal algédonique (lacune D de CYB-001, désormais résolue via `policies/algedonic-channel-policy.yaml`). Le contournement d'urgence l'emporte toujours sur l'amortissement de la coordination.

## Lien avec CYB-001

Ce cours traite directement la **lacune B** de CYB-001 : « Les contrats du Système 2 sont statiques, pas activement amortissants. » Les cinq mécanismes transforment le Galactic Protocol, spécification d'interface passive (boucle ouverte), en un coordinateur anti-oscillation actif (boucle fermée), remplissant ainsi la fonction centrale du Système 2 dans le VSM de Beer.

Le canal algédonique (lacune D de CYB-001) a été résolu séparément via `policies/algedonic-channel-policy.yaml`. L'amortissement et le contournement algédonique sont complémentaires : l'amortissement ralentit la coordination normale pour empêcher l'oscillation ; le canal algédonique contourne tout amortissement pour les urgences réelles.

## Sources

- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Coordination transparency: governing distributed agency in AI systems. (2026). *AI & Society*, Springer. https://link.springer.com/article/10.1007/s00146-026-02853-w
- Gorelkin, M. (2025). "Stafford Beer's VSM for Building Enterprise Agentic Systems." Medium. https://medium.com/@magorelkin/stafford-beers-viable-system-model-for-building-enterprise-agentic-systems-81982d6f59c0
- Fearne, D. (2025). "Applying Stafford Beer's VSM to Create The Autonomous AI Organisation." Medium. https://medium.com/@fearney/applying-stafford-beers-viable-system-model-to-create-the-autonomous-ai-organisation-aaaed39b37e2
- IBM Research. (2025). "Agentic AI Needs a Systems Theory."
- NI. (2025). "PID Theory Explained." https://www.ni.com/en/shop/labview/pid-theory-explained.html
- GeeksforGeeks. (2025). "Feedback Loops in Distributed Systems." https://www.geeksforgeeks.org/system-design/feedback-loops-in-distributed-systems/

## Références croisées

- Prérequis : `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Protocole : `contracts/galactic-protocol.md`
- Politique algédonique : `policies/algedonic-channel-policy.yaml`
- Département : `state/streeling/departments/cybernetics.department.json`
- Grammaire : `grammars/sci-cybernetics.ebnf`
- Politique : `policies/seldon-plan-policy.yaml`
