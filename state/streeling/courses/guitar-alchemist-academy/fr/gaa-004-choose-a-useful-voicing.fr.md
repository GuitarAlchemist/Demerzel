---
module_id: gaa-004-choose-a-useful-voicing
department: guitar-alchemist-academy
course: Choisir et jouer un voicing utile à partir d'une réponse de GA
level: beginner
alchemical_stage: nigredo
prerequisites: ["gaa-001-your-first-chord", "gtr-001-the-fretboard-map"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-alchemist-academy-2026-10-05-004
version: "0.1.0"
---

# Choisir et jouer un voicing utile à partir d'une réponse de GA

> **Guitar Alchemist Academy** | Débutant | 35 minutes | Brouillon : révision musicale et linguistique en attente

## Objectifs

Vous apprendrez à lire une position sans jouer une corde étouffée, à comparer
deux façons de jouer le même accord, à utiliser le classement de GA comme
point de départ, puis à vérifier le résultat avec vos doigts et votre oreille.

## 1. Décoder une position avant de la juger

Demandons un **do majeur**. Le [jeu d'exemples](../../../fixtures/guitar-studies/gtr-003/README.md)
contient trois positions dont les notes ont été vérifiées. Ce ne sont **pas
des résultats capturés de GA**. Les diagrammes se lisent de la corde 6 (mi
grave) à la corde 1 (mi aigu). `x` indique une corde à ne pas jouer et `0`,
une corde à vide.

```text
Corde :          6  5  4  3  2  1
Do ouvert :      x  3  2  0  1  0
Do forme de la : x  3  5  5  5  3
Do forme de mi : 8 10 10  9  8  8
```

Pour le do ouvert, jouez seulement les cordes 5 à 1. Leurs notes sont do,
mi, sol, do, mi. Les trois *classes de hauteur* do, mi et sol définissent
le do majeur. Répéter do ou mi à une autre octave change le voicing, pas
l'identité de base de l'accord. Avant de convertir un tableau `Frets` de GA
en diagramme, vérifiez quel bout du tableau représente le mi grave. Le jeu
d'exemples déclare son propre ordre, grave vers aigu ; il ne démontre pas
l'ordre employé par le service.

### Exercice 1

Dans `x 3 2 0 1 0`, quelle corde reste muette, lesquelles sont à vide et
quelles sont les trois notes différentes de l'accord ?

> **Réponse :** La corde 6 reste muette. Les cordes 3 et 1 sont à vide. Les
> notes jouées sont do, mi, sol, do, mi ; les trois notes différentes sont
> donc do, mi et sol.

## 2. Prendre le classement de GA comme proposition

Au [commit GA `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingFilterService.cs),
`GetVoicingsForChordAsync("C")` produit des positions avec leurs frettes,
étiquettes et scores de difficulté, ainsi que des informations sur les barrés.
Le service les classe ensuite par `DifficultyScore` croissant. Les [tests du
service](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Apps/GaApi.Tests/Services/VoicingFilterServiceTests.cs)
vérifient que C donne des résultats et que les scores sont ordonnés. Ils ne
garantissent ni que la première position convient à tous les guitaristes ni
qu'elle figure parmi les trois exemples ci-dessus.

Dans une version de GA construite à partir de ce commit, relevez les deux
premiers résultats d'une requête `C` : tableau des frettes, score, cordes à
vide et indication de barré. Si l'interface ne montre pas une donnée, notez
« non affichée » au lieu de la deviner sur le dessin. `-1` signifie corde
muette ; `0`, corde à vide. Conservez la requête, la révision et l'accordage
pour qu'une autre personne puisse refaire la comparaison.

Si GA n'est pas disponible, comparez plutôt les formes du jeu d'exemples et
notez « requête au service non exécutée ». Les scores 3 et 5 de l'exercice
suivant sont hypothétiques : ne les attribuez pas à ces formes et ne les
présentez pas comme des résultats de GA.

### Exercice 2

Avec `noOpenStrings: true`, peut-on encore attendre la forme de do ouvert ?
Si deux résultats GA ont les scores 3 et 5, lequel essayer d'abord et que
**ne démontre pas** ce score ?

> **Réponse :** Non. Le service retire les positions contenant la frette `0`
> lorsque `noOpenStrings` est activé. Essayez d'abord celle de score 3 : c'est
> une proposition raisonnable. Le score ne mesure ni la taille de votre
> main, ni votre technique, ni une douleur éventuelle, ni le son de votre
> instrument.

## 3. Vérifier sur la guitare

Commencez par le do ouvert. Posez un doigt sur la corde 5 à la frette 3,
un autre sur la corde 4 à la frette 2 et un troisième sur la corde 2 à la
frette 1. Pincez séparément les cordes 5, 4, 3, 2 et 1. Si une note frise,
rapprochez le doigt de la frette sans appuyer plus que nécessaire. Grattez
ensuite ces cinq cordes seulement. Ne forcez pas un écartement et arrêtez
si vous avez mal.

Essayez ensuite le do en forme de la : étouffez la corde 6, jouez les cordes
5 et 1 à la frette 3, et les cordes 4, 3 et 2 à la frette 5. Un petit barré
ou un autre doigté peut être nécessaire. Comparez la netteté des notes et
l'effort demandé. Si cette forme est trop difficile aujourd'hui, notez-le
et gardez le do ouvert. Un autre voicing est utile s'il convient au morceau
et au musicien, pas simplement parce qu'un algorithme le renvoie.

### Exercice 3

Les deux formes contiennent do, mi et sol. Donnez une raison musicale et
une raison physique de choisir le do ouvert pour une chanson lente. Dans
quel cas préféreriez-vous l'autre forme ?

> **Exemple de réponse :** Les cordes à vide du do ouvert peuvent résonner,
> et cette forme demande moins d'effort à ma main aujourd'hui. Je pourrais
> choisir l'autre forme si l'accord suivant se trouve près de la frette 3,
> une fois toutes les notes jouées proprement. Une autre personne peut faire
> un choix différent après essai.

## 4. Formuler une conclusion à la mesure des preuves

Séparez ce que le service **calcule** de ce que vous **observez**. Une note
de pratique peut suivre cette chaîne : `requête C + révision GA → deux
positions et leurs scores → position jouée → notes nettes ou qui frisent →
effort et contexte musical → choix`. Le programme propose ; le musicien
vérifie. Si vous n'avez pas lancé GA ou joué la forme, indiquez l'étape
qui reste à tester.

### Exercice 4

Un agent écrit : « Le premier do proposé par GA est le plus facile pour
tout le monde. » Reformulez en respectant les preuves du service.

> **Réponse :** « Dans cette requête, le premier résultat a le score de
> difficulté calculé le plus faible parmi les positions renvoyées. Un
> guitariste doit encore vérifier l'accordage, les notes, le doigté et le
> confort. »

## À retenir

- Un tableau de frettes indique quoi faire sur chaque corde ; `-1` et `0`
  n'ont pas le même sens.
- Plusieurs voicings contiennent les mêmes notes d'accord, mais se jouent
  et sonnent différemment.
- Le classement de GA donne un premier choix à essayer. Le musicien décide
  après avoir joué et écouté.

## Preuves et limites

Le [jeu d'exemples et le compte rendu des tests](../../../fixtures/guitar-studies/gtr-003/README.md)
précisent la révision GA et distinguent les formes pédagogiques des résultats
du service. Les tests ciblés du binaire préexistant ont réussi, mais il manque
une réponse GA capturée, un essai avec un débutant et une revue musicale et
linguistique. Ce brouillon n'est pas encore un cours vérifié.
