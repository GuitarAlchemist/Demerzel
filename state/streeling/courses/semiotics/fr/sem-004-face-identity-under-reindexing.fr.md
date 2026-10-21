---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "L’identité des faces après réindexation"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# L’identité des faces après réindexation

> **Département de sémiotique** | Niveau intermédiaire | 40 minutes | Traduction provisoire, sans révision linguistique

## Objectifs et décision du projet

Un futur visualiseur de scène sélectionne la face 1 d’un origami. Un autre agent renumérote le modèle, puis annonce que la face 1 a changé de niveau. Le matériau a-t-il bougé ? L’ordre a-t-il changé ? Ou le même nombre désigne-t-il désormais une autre face ? Il faut interpréter ce nombre avant d’interpréter la géométrie.

À la fin de cette leçon, vous saurez transporter une sélection au moyen d’une permutation explicite, inverser cette correspondance, distinguer identité, niveau et orientation, puis rédiger un compte rendu vérifiable entre agents. Prévoyez huit minutes pour le problème et les signes, douze pour le tableau, dix pour les transformations et dix pour les exercices et le transfert. Le résultat attendu est un tableau de correspondance accompagné d’un compte rendu justifié.

Les sources du projet sont figées au commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854` : [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [tests d’épaisseur](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) et [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). Elles décrivent cette version, sans garantir l’état de la branche actuelle. IX fournit ici des vérifications et des transformations de contrôle. Cette leçon ne démontre aucun export Blender, import Godot, rendu ou mécanisme persistant de sélection.

## 1. Un numéro de face est un signe contextuel

En sémiotique, un signe représente un objet selon une interprétation. Ici, `1` est le signe ; une face matérielle précise est l’objet visé ; « consulter la case 1 dans cette version du modèle » est l’interprétation. Un **indice de tableau** est une adresse dans une collection ordonnée. Il faut le distinguer du terme sémiotique *indice*, qui désigne un signe lié à ce qu’il indique. Aucun de ces sens ne confère une identité permanente au nombre.

Un compte rendu doit préciser la version du modèle ou le contexte de transformation. La face 1 de l’entrée et celle de la sortie peuvent être deux références différentes. La forme, la couleur ou le niveau actuel facilitent parfois la reconnaissance humaine, mais plusieurs faces peuvent partager ces propriétés et celles-ci peuvent changer. Elles ne prouvent donc pas, à elles seules, la provenance.

Dans cette leçon, l’**identité matérielle** désigne la correspondance avec la même face d’entrée au cours de la transformation contrôlée étudiée. Cela ne résout ni le remaillage arbitraire, ni la division ou la fusion de faces, ni la reconstruction depuis une image. Une étiquette pédagogique comme A conserve la correspondance fournie pour l’exercice. Ces étiquettes sont explicitement synthétiques : le type IX `Permutation` décrit une transformation, pas un registre universel d’identifiants persistants.

### Exercice 1 — Réparer une référence

Un agent écrit : « La face 1 est incorrecte après renumérotation. » Quelles informations manquent ? Reformulez cette phrase en question vérifiable.

> **Réponse :** Il manque le contexte des modèles d’entrée et de sortie, la correspondance et la propriété comparée. On peut écrire : « Pour la face synthétique d’entrée 1 (B), avec la correspondance ancien-vers-nouveau `[2,0,3,1]`, la face de sortie 0 conserve-t-elle le niveau d’entrée 2 ? » La question identifie le matériau visé et la comparaison sans prétendre avoir découvert un défaut d’IX.

## 2. Respecter le sens de la correspondance

`Permutation` indique où chaque **ancien** indice a été envoyé. La fonction `place` écrit l’ancien élément dans `out[perm[old]]`. Ainsi, `perm.faces[f]` reçoit un indice de face d’entrée et renvoie son indice de sortie. Pour savoir quelle face d’entrée occupe une case de sortie donnée, il faut la permutation inverse.

Voici un exemple à quatre faces explicitement **synthétique**, également conservé dans la [fixture](../../../fixtures/semiotics/sem-004/scenarios.json). Les nombres ne proviennent ni de la grue, ni d’une graine aléatoire d’IX, ni d’une expérience physique d’épaisseur.

| Indice d’entrée | Étiquette pédagogique de provenance | Niveau d’entrée | Indice de sortie `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

La correspondance directe est `p = [2,0,3,1]`. En parcourant les cases de sortie 0 à 3, on obtient les étiquettes `[B,D,A,C]` et les niveaux `[2,3,0,1]`. L’inverse est `q = [1,3,0,2]` : la sortie 0 vient de l’entrée 1, et la sortie 1 vient de l’entrée 3. Les deux vérifications sont `q[p[f]] = f` et `p[q[j]] = j`.

La comparaison correcte est `new[p[f]] == old[f]`. Pour B, cela donne `new[0] == old[1]`, donc `2 == 2`. Les tableaux bruts sont différents alors que chaque matériau conserve sa valeur. Réutiliser le nombre sélectionné 1 désigne désormais D, de niveau 3. La sélection peut donc être erronée sans que le calcul des niveaux soit corrompu.

L’inverse sert aussi à interpréter un clic sur la sortie 3 : il désigne C, à l’entrée 2. Employer `new[q[f]]` dans la comparaison directe mélange les domaines. Pour notre permutation volontairement différente de son inverse, l’entrée 0 comparerait `new[1] = 3` à `old[0] = 0`. Un exemple limité à un échange pourrait masquer cette erreur, car un échange est son propre inverse.

### Exercice 2 — Transporter la sélection

Transportez la sélection C depuis l’entrée. Retrouvez ensuite l’origine d’un clic sur la sortie 1. Conserver le nombre 2 préserverait-il la sélection C ?

> **Réponse :** C est à l’entrée 2 ; sa sortie est `p[2] = 3`, avec le niveau 1. La sortie 1 vient de `q[1] = 3`, donc de D. Conserver le nombre 2 sélectionnerait A dans la sortie. L’adresse change, tandis que la correspondance matérielle stipulée reste conservée.

### Exercice 3 — Comparer les bons objets

Trouvez la première différence brute entre `[0,2,1,3]` et `[2,3,0,1]`. Donnez les quatre comparaisons avec correspondance et vérifiez une équation de l’inverse.

> **Réponse :** La case brute 0 diffère : `0 != 2`. Les comparaisons correctes sont `new[2]=0`, `new[0]=2`, `new[3]=1` et `new[1]=3`, qui correspondent respectivement aux entrées 0 à 3. Par exemple, `q[p[2]] = q[3] = 2`. L’inégalité brute ne réfute pas la correspondance annoncée.

## 3. Conserver les relations et interpréter leurs signes

La renumérotation transforme aussi les références aux sommets et aux arêtes. Elle effectue une rotation cyclique de la liste des sommets de chaque face, en conservant son sens de parcours ; elle peut échanger les extrémités d’une arête ; elle mélange l’ordre des entrées de `faceOrders`. Ces opérations sont distinctes. Passer de `[0,1,2]` à `[1,2,0]` change le point de départ du contour. Passer à `[0,2,1]` inverse le parcours. Ces petits exemples illustrent des conventions ; ce ne sont pas des données géométriques extraites d’IX.

Pour chaque triplet `[f,g,s]` de `faceOrders`, `renumber` produit `[p[f],p[g],s]`, sans changer le signe. Notre triplet synthétique `[1,3,1]` devient `[0,1,1]`. Le signe s’interprète relativement aux normales des faces : il ne suffit pas à établir une relation globale « au-dessus » sans tenir compte de l’orientation. Mélanger l’ordre de la collection de relations ne revient pas non plus à inverser chaque relation. Position dans une liste, position d’une extrémité, sens d’un contour et signe d’ordre ont des rôles différents.

Le test figé `controls_leave_the_stack_unchanged` renumérote la grue avec les graines 1 à 5. Il vérifie 28 faces superposées au maximum (`ply`), 36 niveaux rigides et, pour chaque face d’entrée, `new[perm.faces[f]] == old[f]`. Il apporte une preuve concrète pour ces contrôles et cette fixture, sans démontrer une invariance universelle pour tout pliage.

`face_levels` est un témoin d’empilement respectant les paires déclarées, avec le niveau zéro en bas. L’implémentation peut ne fournir aucun niveau par face en présence d’un cycle ou d’informations d’ordre insuffisantes. Un niveau n’est donc ni un identifiant matériel unique ni une description canonique de tous les empilements admissibles. Plusieurs faces peuvent partager un niveau. Des totaux identiques ne prouvent pas qu’une sélection désigne toujours la face attendue.

### Exercice 4 — Distinguer trois opérations d’ordre

Un lecteur appelle « réorganisation de tableau » la rotation d’un contour, le mélange des entrées de `faceOrders` et le retournement du modèle. Quelles distinctions perd-il ? Transformez `[1,3,1]`.

> **Réponse :** La rotation du contour conserve le sens cyclique ; le mélange des relations conserve chacune d’elles tout en changeant leur énumération ; le retournement change les orientations et l’interprétation du haut. Les vérifications nécessaires diffèrent. Le triplet devient `[0,1,1]` : les références suivent p et le signe relatif reste conservé, sans prouver à lui seul une relation globale « au-dessus ».

## 4. Préciser la transformation et la portée des preuves

`move_folded` effectue une rotation dans le plan du modèle plié, puis une translation, en conservant les orientations. Le test utilise 0,7 radian et le déplacement `[3,-2]`, puis compare la structure d’empilement retournée entière au résultat initial. Cela étaye ce mouvement rigide testé, sans couvrir changement d’échelle, déformation ou remaillage arbitraire.

`turn_over` applique la réflexion `y -> -y` aux coordonnées pliées. Sa documentation indique que les orientations et le haut s’inversent ensemble ; `faceOrders`, relatif aux normales, reste donc inchangé. Le test compare `ply`, son épaisseur, le nombre de niveaux rigides et leur hauteur. Il ne vérifie explicitement **pas** quelle face occupe quel niveau. Affirmer que chaque face conserve son niveau dépasserait les preuves. Correspondance matérielle et ordre vertical sont deux questions distinctes.

Un compte rendu utile précise la version source, la transformation, le sens de la correspondance, les indices sélectionnés avant et après, la propriété comparée et le résultat. Sans correspondance après une régénération arbitraire, l’identité reste indéterminée. Une épaisseur totale égale ou une silhouette familière ne remplace pas cette information. Il s’agit d’une exigence de communication proposée, pas d’un protocole de sélection déjà implémenté dans IX.

### Exercice 5 — Préparer un essai réfutable de sélection

Proposez un futur essai Godot pouvant réfuter la conservation correcte de la sélection après cette permutation synthétique. Ajoutez une affirmation sur le retournement que les sources actuelles ne justifient pas.

> **Réponse :** Avant transformation, sélectionner B à l’entrée 1 et consigner l’étiquette pédagogique, la version du modèle et la correspondance. Après application de p, le surlignage et le compte rendu doivent désigner la sortie 0, B, niveau 2. Un surlignage sur la sortie 1/D réfute la conservation, même si les totaux correspondent. Conserver les événements bruts et les captures avant et après ; aucun essai n’a été exécuté ici. « B garde son niveau après retournement » n’est pas justifié par les seules assertions agrégées du test.

Cet essai proposé exige un véritable adaptateur de scène et une observation indépendante. Les livrables présents sont l’analyse des sources, le tableau synthétique et des tâches préparées pour un apprenant. Révision de fond humaine, tentative d’un apprenant, révision linguistique et publication restent à réaliser.
