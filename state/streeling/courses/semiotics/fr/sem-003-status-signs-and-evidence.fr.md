---
module_id: sem-003-status-signs-and-evidence
department: semiotics
course: "Signes de statut et preuves dans le travail agentique"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-12-003
version: "0.1.0"
---

# Signes de statut et preuves dans le travail agentique

> **Département de sémiotique** | Niveau : intermédiaire | Stade : Albedo | Durée : 35 minutes | Brouillon français en attente de révision

## Objectifs

Vous apprendrez à distinguer un mot de statut de l'événement qu'il prétend décrire, à lire une fiche de production Streeling sans transformer un contrôle limité en verdict final et à rédiger un handoff vérifiable à partir d'un artefact épinglé. Vous distinguerez aussi ce que prouvent un schéma, une compilation locale et une lecture publique.

## La décision du projet

Un agent rédige un cours Streeling. Un autre ne trouve « aucun problème » après avoir lu sa source et ses réponses. Que doit dire le coordinateur au prochain agent : **brouillon**, **prêt**, **revu** ou **publié** ? Selon le terme choisi, on dirigera un apprenant vers un cours public, un réviseur vers le texte ou l'auteur vers une correction. Une formulation trop forte peut faire sauter une étape.

Ce cours examine la véritable [fiche de production SEM-002](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/course-productions/cp-semiotics-2026-10-11-002.json), son [compte rendu de revue IA limitée](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/sem-002-subject-review-2026-10-11.md), le [schéma de production](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/schemas/course-production.schema.json) et le [rapporteur de progression](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py). Les liens Demerzel pointent vers le commit `c453a91d1c4d913af72c28779eff826659c1d654`. Il s'agit de cet instantané, pas d'une affirmation sur l'état actuel du projet ou du site.

## 1. Que désigne un signe de statut ?

[SEM-001](sem-001-signs-in-governance.fr.md) présente le signe, son objet et l'interprétation qu'en fait le lecteur. Dans un handoff, `reviewed` est un **symbole** régi par une convention commune. Un lien vers un compte rendu peut servir d'**indice** vers un artefact précis. Une coche verte est également un signe compact ; il lui faut pourtant une signification convenue, un critère nommé et une provenance. Aucun de ces signes ne réalise une revue à lui seul.

Les mots du problème désignent des affirmations possibles, **pas** une nouvelle machine à états Streeling :

| Mot du message | Affirmation vérifiable possible | Preuve nécessaire avant de l'employer sans réserve |
| --- | --- | --- |
| `draft` | Un fichier source existe | Chemin et révision exacte |
| `ready` | Une étape définie est franchie | Étape, entrées, résultat et date ; prêt *pour quoi* ? |
| `reviewed` | Un réviseur a examiné une portée définie | Compte rendu, auteur de la revue, portée, résultat et étapes restantes |
| `published` | L'apprenant peut obtenir la version voulue | Route déployée, lecture anonyme et provenance concordante |

Ce sont des **tests de communication**, non quatre valeurs implémentées dans le dépôt. Le schéma épinglé autorise `in_progress`, `review_pending`, `published`, `rejected` et `failed`, mais pas `draft`, `ready` ou `reviewed`. Il faut dire « le brouillon anglais existe » ou « prêt pour une revue limitée de la source », selon la preuve, sans inventer de transition du schéma.

### Exercice 1 — Nommer l'objet

Un handoff dit seulement « SEM-002 est prêt ». Donnez deux sens matériellement différents de `ready`, puis reformulez pour que l'un soit vérifiable. `ready` figure-t-il parmi les valeurs du schéma ?

> **Réponse :** Le texte peut être prêt pour une revue de source ou prêt à être déployé après toutes les revues. Formulation vérifiable : « La source anglaise SEM-002 au commit `c453a91d1c4d913af72c28779eff826659c1d654` est prête **pour une revue limitée de la source et des réponses** ; la revue finale de production et la publication restent inachevées. » Le schéma ne contient aucune valeur `ready`.

## 2. Lire la fiche, puis le compte rendu

À cette révision, la fiche SEM-002 indique `status: in_progress`. Recherche, plan et contenu sont achevés ; la traduction ne l'est pas et `languages: ["en"]`. Revue et publication ont chacune `completed: false`. Le compte rendu IA distinct rapporte **aucun problème dans le périmètre limité de la source et des réponses**. Il laisse expressément ouverts les contrôles humains du sujet, des apprenants, des langues et du site Learn. Une inspection limitée a donc eu lieu alors que la revue finale reste inachevée.

L'erreur sémiotique consiste à faire absorber à `reviewed` toutes les portées possibles. « Le précontrôle IA de la source et des réponses n'a rien relevé » est précis. « Cours revu » peut laisser croire à une approbation éditoriale ou humaine finale. Le nom du réviseur ne suffit pas : son compte rendu doit préciser ce qui a été examiné et exclu. Un drapeau de production est une affirmation dans un fichier ; il lui faut une trace avant de devenir un fait fiable dans un handoff.

Le [rapporteur de progression](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_progress.py#L89-L107) compte une approbation seulement si `phases.review.completed` vaut vrai **et** `phases.review.verdict` vaut `approved`. SEM-002 ne satisfait pas ce critère dans l'instantané. Ce compteur lit des champs : il n'évalue pas indépendamment l'exactitude du sujet. Même si quelqu'un écrivait ces deux valeurs manuellement sans revue fiable, le compteur ne prouverait pas que la revue a eu lieu.

### Exercice 2 — Délimiter la revue

Pour SEM-002 épinglé, choisissez : (A) « Aucune revue n'a eu lieu » ; (B) « Toutes les revues sont passées » ; (C) « Un contrôle IA limité de la source et des réponses n'a rien relevé ; la phase de revue de production reste inachevée ». Pourquoi rejeter les autres ?

> **Réponse :** C. A contredit le compte rendu de contrôle IA limité. B dépasse sa portée : les contrôles humains du sujet, des apprenants, des langues et du site restent ouverts, avec `phases.review.completed=false`. « Aucun problème » ne concerne que le périmètre annoncé, pas tous les défauts possibles.

## 3. Une forme valide n'est pas une transition vérifiée

Le schéma contraint les types de champs et les chaînes `status` autorisées. Il exige le statut, la recherche, le plan, le contenu et un horodatage. Lorsque les phases de revue et de publication sont présentes, leurs champs `completed` sont booléens. Il n'encode **pas** la règle générale « `status: published` implique `publish.completed: true` ». Une fiche peut donc être valide selon le schéma tout en contenant une contradiction opérationnelle. Cela décrit le schéma, pas l'existence prouvée d'une telle fiche en production.

Le [précontrôle de cours](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/scripts/streeling_course_preflight.py) vérifie schémas, noms de fichiers, frontmatter, fichiers de langues déclarées, nombre de mots anglais et signaux d'exercices avec réponses. Sa seule règle explicite de cohérence du statut est que `in_progress` exige des indicateurs de revue et de publication à faux. Il ne visite pas le site public et ne juge pas le fond. Réussir ce précontrôle ne signifie ni « apprenants satisfaits » ni « disponible sur Learn ».

Imaginez une modification **fictive** de SEM-002 : seul `status` devient `published`, tandis que `phases.publish.completed: false` demeure. Le schéma accepte chaque valeur et ne les relie pas. Comme la règle de cohérence du précontrôle ne concerne que `in_progress`, cette contradiction fictive lui échapperait. Ne l'écrivez pas dans le dépôt : elle sert à comprendre la portée de chaque vérification. Consultez plutôt la fiche, un reçu de déploiement et une route anonyme avant de croire le mot `published`.

### Exercice 3 — Distinguer forme et vérité

Le cas fictif `status: published` avec `phases.publish.completed: false` viole-t-il le schéma JSON épinglé ? Sa validité prouverait-elle la disponibilité publique de SEM-002 ?

> **Réponse :** Non, aucune règle du schéma ne relie ces champs. La validation atteste seulement la structure contrôlée ; elle ne prouve ni déploiement ni accès public anonyme. Il faut enquêter sur cette contradiction, pas annoncer la publication.

## 4. Distinguer l'objet local de l'objet public

Le [relevé public de référence](https://github.com/GuitarAlchemist/Demerzel/blob/c453a91d1c4d913af72c28779eff826659c1d654/state/streeling/reviews/public-baseline-2026-10-11.md) consigne une lecture anonyme de l'index Streeling le 11 octobre 2026, cite un commit source et précise que présence publique ne vaut pas revue par l'auteur. Il rapporte aussi que le précontrôle Learn local a généré les pages DV-001 alors que des requêtes GET anonymes vers leurs routes publiques ont obtenu 404. « Page locale générée » renvoie à un artefact de compilation ; « publiée » renvoie à une version récupérable publiquement. Le premier constat n'entraîne pas le second.

Ce relevé est une preuve **historique concernant DV-001**, pas un test actuel de SEM-002 ou du site d'aujourd'hui. Pour publier SEM-003, le coordinateur devrait préciser la route, déployer le site généré, récupérer anonymement cette route et comparer son contenu ou SHA source à la révision voulue. HTTP 200 pourrait servir une ancienne version. Le SHA pointe vers le texte rédigé ; la lecture de route relie ce texte à ce que voit l'apprenant. Le compte rendu du réviseur pointe vers un autre événement. L'un ne remplace pas l'autre.

### Exercice 4 — Identifier l'observation

Dans l'exemple DV-001 daté, une page locale existe et la route anonyme répond 404. Quelle phrase est étayée : « le cours est publié », « la compilation locale a produit une page, mais cette route publique ne la servait pas à la date du contrôle », ou « aucun fichier source n'existait » ? Que faudra-t-il contrôler après un déploiement ultérieur ?

> **Réponse :** La phrase du milieu. Page locale et 404 concernent deux surfaces différentes au jour du constat. Après déploiement, récupérez la route prévue sans authentification et comparez son contenu ou son SHA de provenance à la révision voulue. Une compilation ou une commande de déploiement ne suffit pas.

## 5. Rédiger un handoff exploitable

Un message utile suit une petite chaîne de preuves : **artefact et révision → contrôle nommé → résultat observé → étape manquante → action suivante**. C'est une façon de rédiger cet exercice, **pas un nouveau DSL normatif**. Le destinataire peut suivre les références et rejeter une interprétation trop large ou périmée. Exemple fondé sur l'instantané SEM-002 :

> « La source anglaise SEM-002 existe dans Demerzel au commit `c453a91d1c4d913af72c28779eff826659c1d654`. Une revue IA limitée de la source et des cinq réponses n'a rien relevé. La fiche reste `in_progress`, avec revue et publication inachevées. Ensuite : obtenir la revue humaine du sujet et des apprenants, puis vérifier le déploiement Learn prévu par lecture anonyme. »

Ce message n'invente aucune valeur `ready`. Si une future revue approuve seulement l'exactitude factuelle, il faut en indiquer la portée, sans l'étendre aux langues. Une modification de la source n'est pas automatiquement couverte par l'ancien compte rendu. Les liens de révision immuables relient source, réviseur et lecture publique au même objet ou montrent la rupture de la chaîne.

### Exercice 5 — Corriger un message d'agent

Réécrivez « SEM-002 est revu et publié ; les tests sont verts » avec la seule fiche épinglée et son compte rendu. Donnez une prochaine action précise et signalez une inconnue sans inventer de test ou de déploiement.

> **Réponse :** « Au commit Demerzel `c453a91d1c4d913af72c28779eff826659c1d654`, SEM-002 possède un brouillon anglais et un compte rendu de contrôle IA limité de la source et des réponses sans problème relevé. Sa fiche reste `in_progress`, avec `review.completed=false` et `publish.completed=false`. Ces artefacts n'établissent ni une nouvelle exécution des tests ni une lecture publique de SEM-002. Ensuite : demander une revue humaine du sujet et des apprenants sur cette révision. » Le message initial transforme une vérification limitée en revue finale et affirme sans preuve publication et tests.

## Limites et transfert

Ce cours analyse des fichiers Demerzel épinglés et un relevé public daté ; il n'exécute aucun handoff réel, test apprenant, validation par un sémioticien humain ni publication. Les cinq exercices vérifient la capacité à relier les mots de statut à leurs objets et preuves. Pour savoir si cette méthode améliore la coordination, comparez dans une expérience contrôlée un groupe recevant un statut non qualifié et un groupe recevant la chaîne de preuves ; observez leur choix de la prochaine étape et de la bonne révision source. **Le bénéfice sur les handoffs reste une hypothèse tant que cette expérience n'a pas eu lieu.**
