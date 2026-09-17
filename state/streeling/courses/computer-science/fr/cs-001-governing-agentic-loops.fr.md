---
module_id: cs-001-governing-agentic-loops
department: computer-science
course: "IA agentique — Systèmes multi-agents, utilisation d'outils, boucles de raisonnement"
level: intermediate
prerequisites: ["Multi-agent orchestration patterns"]
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
Un LLM dans une boucle fait face au même problème : le système qui exécute la boucle ne peut pas déterminer de façon fiable
si cette boucle se terminera. La vérification doit être externe.

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

Ces propriétés sont nécessaires et suffisantes pour une itération bornée et auditable :

### Propriété 1 : plafond d'itérations strict
Un nombre maximal d'itérations imposé par le framework, et non par le modèle. Une fois atteint : arrêter,
journaliser le plafond, escalader vers une revue humaine.

```yaml
# Example: Demerzel autonomous-loop configuration
max_iterations: 12
cap_behavior: halt_and_escalate
```

### Propriété 2 : test de progression
Chaque itération doit produire un changement d'état mesurable. Le framework compare les empreintes de l'état
avant et après chaque étape. Si `hash(state_n) == hash(state_n-1)`, la boucle est bloquée.

```python
def progress_test(state_before, state_after):
    return hash(state_before) != hash(state_after)

if not progress_test(prev_state, curr_state):
    raise StallDetected("No state change — possible infinite loop")
```

### Propriété 3 : critère d'arrêt externe
La condition de sortie est spécifiée avant le début de la boucle, et non générée pendant l'exécution.
Le modèle ne peut pas redéfinir la convergence en cours de boucle.

```python
# Good: criterion is external
def is_complete(state) -> bool:
    return state.belief_confidence >= 0.85 or state.iteration >= MAX

# Bad: model declares its own completion
result = model.run("keep going until you think you're done")
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

Le framework Demerzel l'implémente via `autonomous-loop-policy.yaml` :

```
GOVERNED LOOP
├── Pre-conditions (checked before first iteration)
│   ├── Kill switch check
│   ├── Daily/session cap check
│   └── Termination criterion defined
│
├── Iteration body
│   ├── Execute step
│   ├── Progress test (hash compare)
│   ├── Checkpoint emit (every N steps)
│   └── Output dedup check
│
└── Post-conditions (any can halt the loop)
    ├── Termination criterion met → complete
    ├── Iteration cap hit → escalate
    ├── Stall detected → escalate
    ├── Kill switch set → halt immediately
    └── Anomaly detected → conscience signal + halt
```

Ce schéma apparaît à trois endroits de l'écosystème Demerzel :
- **Seldon Plan :** plafond de 6 cycles par jour, registre de nouveauté comme test de progression
- **Demerzel Driver :** plafond de 12 cycles consécutifs, signaux de conscience comme détection d'anomalie
- **Ralph Loop :** plafond d'itérations + métrique de convergence (taux de réussite des tests) comme critère externe

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
- Une boucle gouvernée a exactement six propriétés : plafond strict, test de progression, critère externe, point de contrôle, déduplication, décision de sortie externe
- Le framework Demerzel les implémente dans seldon-plan, demerzel-drive et Ralph Loop
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
*Croyance : T (confiance : 0.82) — cohérente en interne avec la théorie du problème de l'arrêt et l'architecture de gouvernance de Demerzel*
