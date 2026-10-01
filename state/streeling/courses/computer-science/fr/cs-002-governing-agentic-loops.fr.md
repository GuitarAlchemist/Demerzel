---
module_id: cs-002-governing-agentic-loops
department: computer-science
course: "IA agentique — Systèmes multi-agents, utilisation d'outils, boucles de raisonnement"
level: intermediate
prerequisites: ["Modèles d'orchestration multi-agents"]
estimated_duration: "25 minutes"
produced_by: seldon-auto-research
research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.0.0"
---

# Gouverner les boucles agentiques : empêcher l'itération illimitée dans les systèmes pilotés par LLM

> **Département d'informatique** | Niveau : Intermédiaire | Durée : 25 minutes

## Objectifs

- Distinguer l'itération productive (convergente) des boucles pathologiques (divergentes) chez les agents pilotés par LLM
- Comprendre pourquoi les conditions d'arrêt doivent être imposées de l'extérieur plutôt qu'autodéclarées
- Appliquer les six propriétés requises d'une boucle gouvernée à des conceptions de systèmes réels
- Relier la gouvernance des boucles à l'article Default 9 (Autonomie bornée) de la constitution de Demerzel

---

## 1. Le problème de la boucle

Un agent LLM à qui l'on donne un objectif va itérer pour l'atteindre. C'est utile — le raffinement itératif est
la façon dont les tâches complexes s'accomplissent. Mais cela crée un danger structurel : **le raisonnement même qui a produit
la boucle peut produire le constat « j'ai convergé ».**

Ce n'est pas un bogue d'un modèle particulier. C'est une propriété intrinsèque de la génération autorégressive :
le modèle ne peut pas observer son propre comportement de l'extérieur. Il peut décrire la convergence, mais ne peut pas
la garantir. La garantie doit venir du framework.

### Le parallèle avec l'arrêt

Alan Turing a prouvé (1936) qu'aucun algorithme ne peut décider, pour tous les programmes, s'ils s'arrêteront.
Aucune procédure générale ne peut davantage trancher pour une boucle d'agent quelconque. La terminaison est donc imposée
plutôt que détectée : un plafond appliqué par le framework borne le nombre d'itérations, et un délai maximal appliqué par le framework à chaque itération entière l'arrête à son expiration, au besoin en tuant le processus qui l'exécute. Seuls les deux ensemble font s'arrêter la boucle par construction : une itération qui ne finit jamais n'atteint jamais le compteur, et un délai sur chaque appel ne suffit pas, puisqu'une itération peut enchaîner autant d'appels qu'elle veut ou calculer entre eux.

**Conséquence :** Tout framework agentique qui compte sur le modèle pour déclarer lui-même qu'il a terminé
est défectueux par construction.

---

## 2. Taxonomie : boucles productives et boucles pathologiques

| Propriété | Productive | Pathologique |
|---|---|---|
| Chaque itération produit un état distinct | Oui | Non — les sorties se répètent ou dérivent |
| Le critère d'arrêt peut être défini avant la boucle | Oui | Non — le critère est généré dans la boucle |
| La progression est mesurable de l'extérieur | Oui | Non — seulement autodéclarée |
| Un humain peut inspecter l'état intermédiaire | Oui | Non — interne uniquement |
| La boucle peut être mise en pause et reprise | Oui | Non — l'état n'est pas sérialisable |

Une boucle est **productive** quand chaque itération rapproche le système, de façon mesurable, d'un état
terminal définissable. Elle est **pathologique** quand elle génère des tokens sans générer de transitions d'état.

---

## 3. Six propriétés requises d'une boucle gouvernée

Ces six propriétés rendent une itération bornée et auditable. Une boucle qui doit pouvoir être mise en pause et reprise a aussi besoin d'un état sérialisable (sections 2 et 6) :

### Propriété 1 : plafond d'itérations strict
Un nombre maximal d'itérations imposé par le framework, et non par le modèle. Une fois atteint : arrêter,
journaliser le plafond, escalader vers une revue humaine. Le compteur n'avance qu'à la fin d'une itération : le plafond exige donc aussi un délai maximal autour de chaque itération entière, appliqué par le framework, qui arrête l'itération à son expiration, au besoin en tuant le processus qui l'exécute. Des délais sur les appels au modèle, les appels d'outils et les requêtes réseau sont utiles, mais ne bornent pas à eux seuls une itération. La configuration ci-dessous ne fixe que le plafond.

```yaml
# Exemple : configuration de la boucle autonome de Demerzel
max_iterations: 12
cap_behavior: halt_and_escalate
```

### Propriété 2 : test de progression
Chaque itération doit produire un changement d'état mesurable. Le framework compare les empreintes de l'état
avant et après chaque étape. Si `hash(state_n) == hash(state_n-1)`, la boucle est bloquée. Hachez les
champs qui portent le résultat, pas le compteur d'itérations — celui-ci change à chaque étape, si bien que
le test de blocage ne se déclencherait jamais. Et un test de blocage détecte la répétition, pas la dérive : une
boucle qui change sans cesse sans converger ne satisfait jamais le critère externe, et c'est le plafond qui l'arrête, pas ce test.

```python
def stall_test(state_before, state_after):
    return hash(state_before) == hash(state_after)

if stall_test(prev_state, curr_state):
    raise StallDetected("Aucun changement d'état — boucle infinie possible")
```

### Propriété 3 : critère d'arrêt externe
La condition de sortie est spécifiée avant le début de la boucle, et non générée pendant l'exécution.
Le modèle ne peut pas redéfinir la convergence en cours de boucle. Le plafond d'itérations ne fait pas partie du critère : une boucle qui atteint le plafond n'a pas convergé, et elle s'arrête et escalade comme l'exige la propriété 1, au lieu de déclarer son travail terminé.

```python
# Bon : le critère est externe
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85

# Atteindre le plafond n'est pas un succès : arrêter et escalader (propriété 1)
def cap_reached(state) -> bool:
    return state.iteration >= MAX

# Mauvais : le modèle déclare lui-même avoir terminé
result = model.run("continue jusqu'à ce que tu penses avoir fini")
```

### Propriété 4 : point de contrôle lisible par un humain
Toutes les N itérations, le framework émet un point de contrôle : une entrée de journal structurée qu'un humain
peut lire sans exécuter la boucle. Cela sert à la fois d'observabilité et de piste d'audit.

### Propriété 5 : déduplication des sorties
Le framework suit l'ensemble des sorties émises jusqu'ici. Si une sortie candidate est
fonctionnellement identique à une sortie antérieure, elle est signalée comme indice de boucle.

### Propriété 6 : décision de sortie externe
Le modèle propose l'arrêt ; le framework décide. Le « j'ai fini » du modèle est
traité comme un vote, pas comme un ordre.

---

## 4. Le schéma de boucle gouvernée de Demerzel

Le framework Demerzel spécifie ce schéma dans `autonomous-loop-policy.yaml`, avec des limites d'itérations et de stagnation mais sans délai par itération :

```
BOUCLE GOUVERNÉE
├── Préconditions (vérifiées avant la première itération)
│   ├── Vérification du kill switch
│   ├── Vérification du plafond journalier/de session
│   └── Critère de terminaison défini
│
├── Corps de l'itération
│   ├── Exécuter l'étape
│   ├── Test de progression (comparaison de hachages)
│   ├── Émission d'un point de contrôle (toutes les N étapes)
│   └── Vérification de déduplication des sorties
│
└── Postconditions (chacune peut arrêter la boucle)
    ├── Critère de terminaison atteint → terminé
    ├── Plafond d'itérations atteint → escalade
    ├── Stagnation détectée → escalade
    ├── Kill switch activé → arrêt immédiat
    └── Anomalie détectée → signal de conscience + arrêt
```

Ce schéma apparaît à trois endroits de l'écosystème Demerzel, et seuls les deux premiers bornent la durée d'une itération :
- **Seldon Plan :** plafond de 6 cycles par jour, registre de nouveauté comme test de progression, durée maximale de 30 minutes par cycle (`policies/seldon-plan-policy.yaml`)
- **Demerzel Driver :** plafond de 12 cycles consécutifs, signaux de conscience comme détection d'anomalie, délai de cycle (2 heures en souple, puis arrêt forcé à 2h15)
- **Ralph Loop :** plafond d'itérations + métrique de convergence (taux de réussite des tests) comme critère externe, mais aucun délai par itération : ni `policies/autonomous-loop-policy.yaml` ni `.claude/skills/demerzel-loop/SKILL.md` n'en définit, si bien qu'une itération qui se bloque n'atteint jamais le compteur

---

## 5. Ancrage constitutionnel

**Article Default 9 — Autonomie bornée :**
> Les agents opèrent dans des limites prédéfinies. L'autonomie est une ressource, pas un droit.
> Quand les limites sont atteintes, escaladez — ne vous autorisez pas vous-même à les étendre.

Les six propriétés ci-dessus rendent l'article 9 opérationnel pour les processus itératifs. Plus précisément :
- Plafond strict = limite prédéfinie
- Arrêt externe = « prédéfini » (et non décidé en vol)
- Escalade au plafond = « escaladez, ne vous autorisez pas vous-même »

**Article Default 7 — Auditabilité :**
> Chaque cycle doit être journalisé avec une trace complète.

Les points de contrôle et les journaux de déduplication des sorties y satisfont : la boucle est auditable même en cours d'exécution.

---

## 6. Anti-patterns

| Anti-pattern | Pourquoi il échoue | Correction |
|---|---|---|
| `while not model.done()` | Le modèle déclare lui-même qu'il a terminé | Remplacer par un critère externe |
| Nombre d'itérations dans le prompt (« essaie 5 fois ») | Le modèle peut passer outre pendant la génération | L'imposer dans le framework, pas dans le prompt |
| « Continue à améliorer jusqu'à satisfaction » | Illimité, la satisfaction est autodéclarée | Définir une métrique de satisfaction mesurable |
| Aucune journalisation de points de contrôle | Boucle non auditable en vol | Émettre un point de contrôle toutes les N itérations |
| État non sérialisé | La boucle ne peut pas être mise en pause/reprise | Utiliser une machine à états, sérialiser chaque étape |

---

## Points clés à retenir

- Un LLM ne peut pas détecter de façon fiable ses propres boucles infinies — l'arrêt doit être externe
- Une boucle gouvernée a six propriétés : plafond strict avec un délai maximal sur chaque itération, test de progression, critère externe, point de contrôle, déduplication, décision de sortie externe — plus un état sérialisable si elle doit pouvoir être mise en pause et reprise
- Le framework Demerzel applique le schéma dans seldon-plan, demerzel-drive et Ralph Loop ; seuls les deux premiers fixent un délai par itération, si bien que Ralph Loop ne s'arrête pas encore par construction
- L'article 9 (Autonomie bornée) en est la base constitutionnelle — les limites sont prédéfinies, les étendre exige une escalade

## Pour aller plus loin

- `policies/autonomous-loop-policy.yaml` — spécification de la boucle gouvernée de Demerzel
- `policies/seldon-plan-policy.yaml` — phase 1 (WAKE) : arrêt d'urgence et logique de plafond
- `policies/continuous-learning-policy.yaml` — bornes d'itération dans les pipelines d'apprentissage
- `.claude/skills/demerzel-drive/SKILL.md` — cycle du Driver (schéma du plafond de 12 cycles)
- `.claude/skills/seldon-plan/SKILL.md` — cycle de recherche (plafond de 6 par jour + registre de nouveauté comme test de progression)

---
*Produit par Seldon Auto-Research cs-2026-03-22-001 le 2026-03-22.*
*Question de recherche : Quelles propriétés de gouvernance un framework d'orchestration multi-agents doit-il satisfaire pour empêcher les boucles de raisonnement illimitées tout en préservant la résolution itérative légitime de problèmes ?*
*Croyance : T (confiance : 0.82) — cohérente en interne avec la théorie du problème de l'arrêt et l'architecture de gouvernance de Demerzel ; traduction française : U (non relue par un locuteur natif)*
