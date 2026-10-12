---
module_id: cs-002-governing-agentic-loops
department: computer-science
course: "IA agentique — Systèmes multi-agents, utilisation d'outils, boucles de raisonnement"
level: intermediate
prerequisites: ["Modèles d'orchestration multi-agents"]
estimated_duration: "35 minutes"
produced_by: seldon-auto-research
revised_by: codex-project-pilot
research_cycle: computer-science-2026-10-12-002
original_research_cycle: cs-2026-03-22-001
coverage_ratio_at_selection: 0.0
version: "1.1.0"
---

# Gouverner les boucles agentiques : empêcher l'itération illimitée dans les systèmes pilotés par LLM

> **Département d'informatique** | Niveau : Intermédiaire | Durée : 35 minutes | Brouillon révisé ; relecture humaine du contenu et essai apprenant en attente

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

Le théorème de l'arrêt ne prouve **pas** que tout agent se trompe lorsqu'il annonce avoir terminé. Il exclut une procédure de décision universelle pour les programmes arbitraires. Pour les cours et les releases de ce projet, la règle pratique est plus simple : vérifier l'achèvement à partir d'artefacts externes plutôt que d'accepter la déclaration de l'agent.

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
# Exemple : configuration d'une boucle (défaut de la politique 10, maximum absolu 25)
max_iterations: 12
cap_behavior: halt_and_escalate
```

La valeur `12` est un exemple de configuration, pas le défaut actuel de Demerzel. La [politique de boucles épinglée](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) indique `default_max: 10`, `absolute_max: 25` et `stall_limit: 3`. Le journal de recherche de mars parlait d'un « plafond de 12 cycles » ; la présente vérification corrige cette ancienne affirmation sans la reprendre comme règle actuelle.

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
- **Seldon Plan :** plafond de 6 cycles par jour, registre de nouveauté comme test de progression, limite souple de 30 minutes par cycle (`policies/seldon-plan-policy.yaml`) et arrêt forcé à 35 minutes (`timeout-minutes` dans `.github/workflows/seldon-plan.yml`)
- **Demerzel Driver :** une pause pour revue humaine après 5 cycles consécutifs sans intervention, signaux de conscience comme détection d'anomalie, délai de cycle (2 heures en souple, puis arrêt forcé à 2h15)
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

## Atelier pratique : décider à partir des traces

Consultez la [politique de boucles épinglée](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/policies/autonomous-loop-policy.yaml) et le [workflow Seldon](https://github.com/GuitarAlchemist/Demerzel/blob/bb034ca0e7ab2b391401c1f042d73a5c4e5dc67e/.github/workflows/seldon-plan.yml) avant de répondre. Les cas ci-dessous sont des **situations fictives**, sauf lorsqu'une source est citée. Une règle écrite, une configuration de workflow et une exécution observée ne constituent pas la même preuve.

### Exercice pratique 1

Une boucle a `max_iterations: 10`. Elle termine deux itérations, puis reste bloquée pour toujours dans le troisième appel d'outil. Le plafond borne-t-il cette boucle ? Nommez la limite manquante et le fichier du projet qui configure un délai maximal pour un job entier.

> **Réponse :** Non. Le compteur n'atteint trois qu'à la fin de la troisième itération ; le plafond de dix ne peut donc pas interrompre cet appel. Il faut un délai maximal appliqué à l'itération entière, ou un délai strict englobant le job et capable de terminer son processus. Le workflow GitHub de Seldon déclare `timeout-minutes: 35` pour son job ; la politique générale donne un nombre d'itérations et une limite de stagnation, mais aucun délai par itération. Une configuration de timeout ne prouve pas qu'une exécution locale arbitraire a été interrompue.

### Exercice pratique 2

Un état passe de `{payload: "A", iteration: 4}` à `{payload: "A", iteration: 5}`. Un autre passe de `{payload: "A", iteration: 5}` à `{payload: "B", iteration: 6}`, mais l'artefact cible reste absent. Quelle transition est une stagnation exacte si l'on exclut le compteur ? La seconde prouve-t-elle la convergence ?

> **Réponse :** La première est une stagnation exacte si l'empreinte ne porte que sur `payload`. Dans la seconde, la valeur change : le test d'égalité ne se déclenche pas, mais cela ne prouve aucun rapprochement de l'artefact cible. Un critère de réussite distinct doit inspecter cet artefact ou les autres preuves requises. La politique distingue ainsi les vérifications de convergence, de régression et de dérive ; changer d'empreinte ne suffit pas à réussir.

### Exercice pratique 3

Un agent chargé d'un cours atteint sa dixième itération terminée, annonce une confiance de `0.90` et a rédigé le cours promis. Le verdict humain sur le contenu et la lecture de la page publique manquent. Choisissez `complete`, `halt_and_escalate` ou `continue`, puis expliquez pourquoi l'exemple `is_complete` de la section 3 ne suffit pas pour publier.

> **Réponse :** `halt_and_escalate` pour cette boucle bornée : elle a atteint le plafond sans satisfaire le critère externe complet. Le brouillon est un progrès, mais ni la confiance ni le fichier seul ne prouvent la revue humaine ou la publication. La fonction `belief_confidence >= 0.85` montre où placer un contrôle externe ; ce n'est pas un critère suffisant pour Streeling. Un nouveau travail autorisé peut avancer sur d'autres cours, mais cette boucle épuisée ne doit pas appeler son résultat partiel « terminé ».

### Exercice pratique 4

La politique indique `default_max: 10`, `absolute_max: 25` et `stall_limit: 3` ; un journal de 2026 affirme « plafond de 12 cycles » ; l'exemple de cours configure 12. Quelle valeur est le défaut ? Quelle valeur est un exemple permis si les surcharges sont autorisées ? Quelle preuve montrerait qu'une boucle précise utilisait effectivement 12 ?

> **Réponse :** Dix est le défaut de la politique épinglée et 25 son plafond absolu. Douze est un exemple de plafond particulier situé dans ces bornes, pas le défaut. Le libellé de l'ancien journal contredit la politique épinglée et ne doit pas être repris comme règle actuelle. Pour une exécution précise, il faut sa configuration effective et une trace qui la rattache à cette exécution ; la politique générale et ce cours ne suffisent pas.

### Exercice pratique 5

Un relecteur demande si `timeout-minutes: 35` prouve que chaque boucle Demerzel ou Ralph possède un délai par itération et s'arrête toujours proprement. Répondez en deux phrases limitées aux preuves, puis nommez une observation nécessaire pour vérifier un timeout lors d'une vraie exécution Seldon.

> **Réponse :** Le workflow épinglé configure une limite de 35 minutes pour ce job Seldon, tandis que la politique générale ne fixe aucun délai par itération ; on ne peut pas généraliser à toutes les boucles Demerzel ou Ralph. Un timeout strict peut terminer le travail sans point de contrôle propre, ce qui exige aussi une trace pour parler d'arrêt propre. Pour une exécution réelle, examinez la conclusion et les horodatages du job ainsi que le dernier point de contrôle ou la preuve de sortie du processus ; le YAML seul reste une déclaration.

Ces réponses vérifient un raisonnement sur des sources épinglées et des cas fixes. Elles n'attestent ni l'observation d'un agent en activité, ni l'application des six propriétés par tout le framework. Une revue humaine du contenu et un essai apprenant sans réponses restent nécessaires ; cette traduction n'a pas été relue par un francophone désigné.

## Points clés à retenir

- Un LLM ne peut pas détecter de façon fiable ses propres boucles infinies — l'arrêt doit être externe
- Une boucle gouvernée a six propriétés : plafond strict avec un délai maximal sur chaque itération, test de progression, critère externe, point de contrôle, déduplication, décision de sortie externe — plus un état sérialisable si elle doit pouvoir être mise en pause et reprise
- Le framework Demerzel applique le schéma dans seldon-plan, demerzel-drive et Ralph Loop ; seuls les deux premiers fixent un délai par itération, si bien que Ralph Loop ne s'arrête pas encore par construction
- L'article 9 (Autonomie bornée) en est la base constitutionnelle — les limites sont prédéfinies, les étendre exige une escalade

## Pour aller plus loin

- `policies/autonomous-loop-policy.yaml` — spécification de la boucle gouvernée de Demerzel
- `policies/seldon-plan-policy.yaml` — phase 1 (WAKE) : arrêt d'urgence et logique de plafond
- `policies/continuous-learning-policy.yaml` — bornes d'itération dans les pipelines d'apprentissage
- `.claude/skills/demerzel-drive/SKILL.md` — cycle du Driver (pause après 5 cycles sans intervention)
- `.claude/skills/seldon-plan/SKILL.md` — cycle de recherche (plafond de 6 par jour + registre de nouveauté comme test de progression)

---
*Produit par Seldon Auto-Research cs-2026-03-22-001 le 2026-03-22.*
*Question de recherche : Quelles propriétés de gouvernance un framework d'orchestration multi-agents doit-il satisfaire pour empêcher les boucles de raisonnement illimitées tout en préservant la résolution itérative légitime de problèmes ?*
*Croyance : T (confiance : 0.82) — cohérente en interne avec la théorie du problème de l'arrêt et l'architecture de gouvernance de Demerzel ; traduction française : U (non relue par un locuteur natif)*
