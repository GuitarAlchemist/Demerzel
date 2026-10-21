---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Épaisseur des feuilles des coordonnées IX aux unités de scène proposées
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Épaisseur des feuilles : des coordonnées IX aux unités de scène proposées

> **Département de physique** | 40 minutes | Traduction FR provisoire; relecture spécialisée et essai auprès d'un apprenant en attente. EN/FR/ES sont des brouillons; PT/IT/DE sont absents.

## Objectifs et problème du projet

Une feuille IX peut avoir des coordonnées comprises entre zéro et un, alors que son épaisseur se mesure en millimètres. Un futur artefact Blender ou Godot nécessite encore une autre échelle déclarée. Transmettre le nombre brut `0.4` dans ces trois représentations rendrait un carton courant 150 fois trop épais, ou introduirait une erreur d'un facteur 1000 entre millimètres et mètres de scène.

À la fin de cette leçon, vous saurez calculer l'épaisseur et les hauteurs d'empilement dans chaque représentation, distinguer le nombre de plis superposés des niveaux de panneaux parallèles, diagnostiquer deux erreurs d'échelle et préparer une transmission aux affirmations vérifiables. Prévoyez 12 minutes de lecture, 18 minutes pour les exercices avant de consulter les réponses, puis 10 minutes pour la tâche de transfert. Cette leçon traite des longueurs géométriques et des conversions. La vitesse d'excitation d'une guitare relève de PHY-004; la reconstruction d'un état plié relève de la séquence de visual computing.

Les sources sont figées au commit IX `d7c22fdd6a62becb66b9d7246ea85850e7c55854` : [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), ses [tests existants](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs) et [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). Leurs définitions et assertions ont été examinées. L'agent coordinateur a exécuté la cible ciblée des tests d'épaisseur à ce HEAD inchangé : 11 réussites, aucun échec. Ce résultat ne couvre pas toute la suite. Le [jeu arithmétique](../../../fixtures/physics/phy-005/scenarios.json) contient les exemples modélisés; son [README](../../../fixtures/physics/phy-005/README.md) explique leur reproduction.

## 1. Déclarer une règle graduée avant toute conversion

Soit `C` la largeur de la feuille en unités du patron de plis, `W` sa largeur physique supposée en mm et `h` l'épaisseur totale du matériau en mm. Posons `a=W/C`, en mm par unité de coordonnées :

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

L'indice indique une représentation; il n'affirme pas qu'IX stocke des métadonnées physiques. Ici, `W` est une hypothèse externe. Un fichier contenant un carré unité ne permet pas de savoir si la feuille réelle mesure 150 ou 300 mm. L'épaisseur est l'épaisseur totale, jamais une demi-épaisseur ou un nombre de faces.

Le test de la grue décrit explicitement un carton de 0.4 mm et une feuille de 150 mm représentée par le carré unité. Donc `C=1`, `W=150`, `a=150` et `t_cp=0.4/150=0.0026666667`. Le retour aux unités physiques donne `0.0026666667 × 150 ≈ 0.4 mm`. Gardez la fraction jusqu'à l'affichage final pour limiter les écarts d'arrondi.

`lib.rs` décrit une remise à l'échelle par puissances de deux avant les vérifications à tolérance absolue : la largeur du patron devient comprise entre un et deux. C'est un conditionnement numérique, sans déclaration de mètres ni mesure physique de la feuille. `stack(ctx,t)` conserve le `t` fourni par l'appelant dans ses multiplications; la fonction ne peut déduire `W` ni convertir implicitement une valeur donnée en mm. Conservez une correspondance externe explicite pour la représentation transmise.

### Exercice pratique 1 : corriger l'épaisseur d'entrée

Une transmission du carré unité de la grue indique `t=0.4` avec l'étiquette « 0.4 mm ». Calculez le bon `t_cp`, l'épaisseur physique correspondant à la valeur erronée et le facteur d'erreur.

> **Réponse :** `t_cp=0.4/150=0.0026666667`. Avec `a=150 mm/cp`, `0.4 cp` représente `60 mm`, soit `60/0.4=150` fois l'épaisseur prévue. Il faut remplacer le nombre et préciser la correspondance; changer seulement l'étiquette ne convertit rien.

## 2. Séparer les deux lectures de l'empilement

L'implémentation définit `ply` comme le nombre maximal de faces présentes dans une cellule de recouvrement. La hauteur associée est `ply_height=ply × t`. Cette lecture autorise une face à se trouver à des hauteurs différentes selon les cellules, comme une feuille qui se drape. Elle fournit une borne inférieure pour les empilements conservant les positions planaires indiquées.

Dans la lecture en panneaux rigides parallèles, les faces reliées par des joints plats appartiennent à un même panneau. Une arête orientée relie le panneau inférieur au supérieur pour chaque paire superposée ordonnée. Si l'ordre est acyclique et toutes les paires de panneaux superposés sont déterminées, `levels` est la longueur de la plus longue chaîne et `height=levels × t` est la hauteur minimale dans ce modèle restreint. Si des ordres manquent, le nombre de niveaux annoncé est une borne inférieure; `levels_exact=false` et `face_levels` est absent. Un nombre de niveaux est sans dimension; une hauteur possède les unités de `t`.

Le test existant de la grue impose `ply=28`, exactement 36 niveaux rigides, aucune paire indéterminée et 59 entrées de niveaux respectant l'ordre donné. Il présente une chaîne de 36 faces. Ces assertions concernent ce jeu et ce modèle, sans définir toutes les grues. Les deux calculs donnent :

```text
hauteur ply :    28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
hauteur rigide : 36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

Avec une convention illustrative plaçant les surfaces inférieures à `z_k=k×t`, la plus haute surface inférieure se situe à `35t` pour 36 niveaux occupés. Le dessus de la dernière plaque atteint `36t`. Un décalage de surface diffère donc de l'étendue totale de l'empilement. Il s'agit d'une convention de dessin proposée, pas d'une géométrie exportée par IX.

### Exercice pratique 2 : décalage ou étendue totale

Un descriptif affirme : « La grue fait 28 couches, donc l'empilement rigide mesure 11.2 mm; le niveau rigide le plus haut est 35, donc sa hauteur est 35t. » Corrigez les deux affirmations avec les hypothèses du test.

> **Réponse :** Les 28 couches locales donnent 11.2 mm. La lecture rigide parallèle comporte exactement 36 niveaux et une étendue totale de `36×0.4=14.4 mm`. Selon la convention proposée, le niveau 35 commence à `35×0.4=14.0 mm` et se termine à 14.4 mm. L'indice entier du niveau n'est pas le nombre de niveaux occupés.

## 3. Déduire explicitement une future échelle de scène

Supposons qu'un futur artefact choisisse `u=1 unité de scène par mètre`. C'est un choix pédagogique, sans configuration Blender ou Godot vérifiée. Le facteur est `b=u/1000` unité de scène par mm, donc `x_scene=x_cp×a×b`. Appliquez le même multiplicateur à toutes les longueurs de la même géométrie, y compris l'épaisseur et les hauteurs calculées.

Pour la feuille de référence, une unité de coordonnées vaut `150/1000=0.15` unité de scène. On obtient `t_scene=(0.4/150)×0.15=0.0004`, une hauteur ply de `0.0112` et une hauteur rigide de `0.0144`. La conversion physique indépendante donne `14.4 mm × (1/1000)=0.0144 unité de scène`. L'accord entre les chemins vérifie le calcul, sans valider une chaîne d'importation.

Si un aperçu pédagogique choisit plutôt `u=100 unités de scène par mètre`, toutes les longueurs de scène sont multipliées par 100. La largeur devient 15 et la hauteur rigide 1.44. L'épaisseur physique reste 0.4 mm. Le choix d'échelle change la représentation du matériau.

### Exercice pratique 3 : détecter un facteur 1000

Une scène proposée à l'échelle du mètre utilise une largeur de `0.15`, une épaisseur de `0.4` et une hauteur rigide de `14.4`. Calculez les deux bonnes petites longueurs et un rapport révélant l'erreur indépendamment de l'échelle de scène.

> **Réponse :** L'épaisseur vaut `0.0004` et la hauteur rigide `0.0144` unité de scène. Les valeurs fournies sont 1000 fois trop grandes. Les rapports corrects sont `épaisseur/largeur=0.4/150≈0.0026666667` et `hauteur rigide/largeur=14.4/150=0.096`. La scène erronée donne environ 2.6667 et 96. Une échelle uniforme cohérente conserve ces rapports sans dimension.

## 4. Modifier une hypothèse à la fois

Changer de matériau et agrandir la géométrie répondent à des questions différentes. Sur la même feuille de 150 mm, doubler l'épaisseur à 0.8 mm double `t_cp`, les deux hauteurs et leurs longueurs de scène. L'ordre des faces de l'entrée ne change pas. Le test existant `heights_scale_with_the_thickness` compare `t=0.25` et `0.5`, impose le doublement des hauteurs et des niveaux de faces inchangés. Ces valeurs vérifient une relation algébrique, sans mesurer du carton.

Avec le même matériau de 0.4 mm sur une feuille de 300 mm, `t_cp` est divisé par deux dans le carré unité. Les hauteurs physiques restent 11.2 et 14.4 mm pour la même configuration combinatoire donnée. Si l'on double toutes les longueurs physiques, épaisseur comprise, `t_cp` reste inchangé et les hauteurs physiques doublent. Précisez la transformation visée par « agrandir ».

Représenter la même feuille de 150 mm avec `C=2` donne `a=75 mm/cp`, `t_cp=0.0053333333` et une hauteur rigide de `0.192 cp`. Multiplier par 75 restitue 14.4 mm. C'est une déduction dimensionnelle pour une représentation modifiée de façon cohérente, pas une nouvelle exécution observée d'IX.

### Exercice pratique 4 : comparer trois modifications

À partir de la référence, calculez `t_cp` et la hauteur rigide en mm pour A : épaisseur 0.8 mm, largeur 150 mm, `C=1`; B : épaisseur 0.4 mm, largeur 300 mm, `C=1`; C : feuille physique initiale représentée avec `C=2`. Supposez le même ordre exact de 36 niveaux.

> **Réponse :** A : `t_cp=0.8/150≈0.0053333333`, hauteur `36×0.8=28.8 mm`. B : `t_cp=0.4/300≈0.0013333333`, hauteur 14.4 mm. C : `t_cp=0.4×2/150≈0.0053333333`, hauteur 14.4 mm. A et C ont la même épaisseur en coordonnées avec des hypothèses physiques différentes. Chaque valeur requiert sa règle graduée.

## 5. Dire ce qu'établit une hauteur convertie

Le vérificateur lit un état plié à plat déclaré. `lib.rs` précise que ses vérifications locales ne prouvent pas la possibilité globale d'un pliage à plat et ne calculent pas d'ordre des couches. `thickness.rs` restreint son interprétation à des panneaux parallèles ayant chacun une hauteur unique. Un cycle interdit cette interprétation lorsque `t` est positif; à épaisseur nulle, il est signalé sans refus. Une hauteur rigide absente à cause d'un cycle n'est pas une mesure nulle.

Même une hauteur exacte et acyclique ne prouve pas qu'un pliage épais est physiquement réalisable : charnières, contacts, flexion et trajectoire restent hors du calcul. La source précise que des panneaux inclinés peuvent échapper à un refus du modèle parallèle et que le contact exact aux plis épais impose une autre limite. Ce cours ne produit aucun exporteur, maillage, collider, simulation dynamique, essai de matériau ou intégration active Blender/Godot/DLSS.

### Exercice pratique 5 : rédiger la transmission

Rédigez trois phrases pour l'auteur d'un futur artefact visuel : une sur les preuves, une sur la correspondance de scène et une sur une affirmation physique ou d'intégration encore non établie.

> **Réponse :** « Au commit IX figé `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, les assertions examinées du test de grue indiquent 28 couches locales et 36 niveaux parallèles exacts pour `t=0.4/150`; le coordinateur rapporte aussi 11 tests d'épaisseur réussis à cette révision inchangée. En supposant une feuille de 150 mm et une unité de scène par mètre, les étendues ply et rigide déduites sont 0.0112 et 0.0144 unité de scène. Ces conversions ne démontrent ni la faisabilité physique du pliage ni un import Blender/Godot opérationnel. » Joignez le lien du jeu arithmétique.

## Transfert et relecture

Effectuez la [tâche sans corrigé](../../../reviews/phy-005-learner-task.md) avec une autre largeur et une autre échelle. Le relecteur doit vérifier les sources figées, refaire les conversions et comparer les langues selon le [dossier de relecture](../../../reviews/phy-005-review-brief.md). Aucun essai d'apprenant, accord de relecteur francophone ou contrôle de publication n'est enregistré. Les livrables sont une leçon provisoire et un dossier de calculs; leur utilité devra être éprouvée par un véritable transfert sans aide.
