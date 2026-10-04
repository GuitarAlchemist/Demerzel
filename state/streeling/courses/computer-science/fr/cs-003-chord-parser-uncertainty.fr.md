---
module_id: cs-003-chord-parser-uncertainty
department: computer-science
course: Signaler l'incertitude à la frontière du parseur d'accords
level: intermediate
prerequisites: ["symboles d'accords élémentaires", "types résultat"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-003
version: "0.1.0"
---

# Signaler l'incertitude à la frontière du parseur d'accords

> **Département d'informatique** | Niveau intermédiaire | 45 minutes | Brouillon : validation de l'exécution et révision musicale en attente

## Objectifs

Vous suivrez une saisie de musicien depuis le parseur d'accords de GA jusqu'à une réponse de doigtés. Vous distinguerez un accord reconnu d'une interprétation partielle, représenterez une notation inconnue par un résultat explicite et construirez un jeu de régression qui vérifie le sens musical, pas seulement la présence d'un objet `Chord`.

## 1. Le problème : une réponse fausse mais crédible

Une guitariste demande des doigtés pour `C7b5`. L'étiquette `C7b5` n'est utile que si la formule contient à la fois la septième dominante et la quinte diminuée. De beaux diagrammes calculés à partir d'un autre ensemble de notes risquent d'induire la personne en erreur pendant sa pratique.

GA possède plusieurs parseurs d'accords. Ce cours suit celui utilisé par `VoicingFilterService` : `Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs`. Son expression régulière accepte une fondamentale suivie de **n'importe quel** suffixe (ligne 8). `ParseChordSuffix` reconnaît des formes précises, puis `ParseComplexSuffix` cherche certaines altérations comme sous-chaînes (lignes 103–133). Faute de correspondance, il renvoie la formule majeure (lignes 138–139). `TryParse` intercepte toute exception et ne renvoie qu'un booléen (lignes 42–53). Le consommateur ne sait donc pas qu'une partie du texte a été ignorée.

Le chemin vers l'utilisateur compte aussi : `VoicingFilterService.cs:28` appelle `TryParse`, puis construit les doigtés avec `chord.PitchClassSet`. `ContextualChordsController.cs:56–63` répond `200 OK` si le service renvoie des doigtés et `400` si une erreur d'argument survient. Une interprétation incorrecte mais construite sans erreur peut donc traverser l'API. C'est une déduction à partir du code, pas le résultat d'un appel réel à l'API.

### Exercice 1

Pour `Cnope`, suivez la fondamentale, le suffixe, la formule, le service et la réponse probable. Quel comportement faudrait-il ?

> **Réponse :** La fondamentale est C. `nope` ne correspond à aucune forme reconnue : le repli produit un accord majeur. `TryParse` réussit et le service peut renvoyer des doigtés de C majeur avec le texte initial et `200 OK`. Il faudrait un résultat « suffixe non reconnu », traduit en message compréhensible. Il ne faut pas supposer que `nope` signifie « majeur ».

## 2. Vérifier le sens, pas le nombre de parsings réussis

Le [jeu CS-003](../../../fixtures/computer-science/cs-003/README.md) comporte huit entrées. `C`, `Am` et `G7` sont des contrôles pris en charge; `Hmaj7` vérifie le rejet d'une fondamentale invalide. Les autres exposent quatre cas distincts :

| Entrée | Interprétation déduite du code actuel | Contrat attendu |
|---|---|---|
| `Cnope` | le suffixe inconnu devient majeur | rejeter le suffixe |
| `Galtxyz` | la sous-chaîne `alt` gagne malgré `xyz` | consommer toute l'entrée ou rejeter |
| `C7b5` | la branche `b5` produit les demi-tons 4 et 6; la septième disparaît | conserver septième et quinte diminuée, ou rejeter |
| `C/E` | le suffixe devient majeur; le symbole reste `C/E`, mais `Chord.Bass` vaut la première note, C | représenter E à la basse ou rejeter |

Dans `ChordSymbolParserTests.cs`, un cas « valide » doit surtout produire un objet, une fondamentale et un symbole. `C/E` figure dans la liste sans vérification de la basse. Ce test prouve la construction d'un objet, pas la bonne interprétation de la notation. Un test de régression doit vérifier les classes de hauteurs, la qualité, l'extension et la basse promises. Une forme non prise en charge doit échouer avec une raison.

Il existe aussi `Chord.TryFromSymbol` dans `Common/GA.Domain.Core/Theory/Harmony/Chord.cs`. Il renvoie `false` pour un suffixe inconnu (lignes 161–166), mais son vocabulaire exact est plus restreint. Le substituer au parseur du service sans corpus de compatibilité pourrait casser des formes actuellement reconnues. On définit d'abord le contrat, puis on mesure la compatibilité.

### Exercice 2

Pourquoi un test qui vérifie seulement que `C7b5` produit un objet `Chord` ne protège-t-il pas la guitariste ? Donnez deux assertions supplémentaires.

> **Réponse :** L'objet peut porter le bon symbole avec les mauvais intervalles. Il faut vérifier la présence de la septième dominante et de la quinte diminuée dans la formule ou l'ensemble de classes de hauteurs, puis vérifier qu'aucun caractère du suffixe n'a été laissé de côté.

### Exercice 3

`C/E` est une notation courante, mais ce chemin de GA ne représente pas sa basse. Faut-il déclarer la saisie invalide ?

> **Réponse :** La notation elle-même peut être valide. C'est sa **sémantique qui n'est pas prise en charge ici**. Il faut implémenter et tester E à la basse, ou renvoyer un résultat explicite « forme non prise en charge ». Conserver `C/E` comme étiquette d'un simple C majeur masque la perte d'information.

## 3. Composer une frontière capable de dire « je ne sais pas »

Une conception possible sépare les étapes :

```text
tokenize(input)                    -> Result<Tokens, SyntaxError>
consumeAll(tokens)                 -> Result<ChordSyntax, TrailingInput>
interpret(syntax, vocabulary)      -> Result<ChordMeaning, UnsupportedForm>
construct(meaning)                 -> Result<Chord, DomainError>
mapForUser(error)                  -> réponse client documentée
```

Les quatre premières étapes peuvent être pures si le vocabulaire est fourni en entrée. L'API et la journalisation sont des effets. Conservez le texte initial pour diagnostiquer le problème, mais ne l'affichez jamais sur une formule différente. `UnsupportedForm` distingue une notation musicale éventuellement correcte d'une fondamentale mal formée. Modifier le statut HTTP ou la forme de réponse serait un changement d'API publique qui demande une étude de compatibilité; ce cours ne l'impose pas.

### Exercice 4

Un agent propose de modifier uniquement la branche `b5` pour « réparer » `C7b5`. Que doivent prouver ses tests ?

> **Réponse :** Ils doivent vérifier les intervalles attendus, dont la septième dominante et la quinte diminuée; préserver le sens de `C`, `Am`, `G7` et des formes déjà prises en charge; rejeter une queue comme `Galtxyz`; puis vérifier que le service ne renvoie pas de doigtés plausibles pour une forme non prise en charge.

## 4. Dogfooder le chemin d'erreur

Exécutez d'abord le corpus contre une révision GA épinglée. Faites ensuite saisir dans l'interface de doigtés un accord pris en charge, une faute de frappe et un accord avec basse non prise en charge. Notez le texte affiché, la facilité de correction et la crédibilité d'un éventuel diagramme erroné. Le test de code vérifie le contrat; l'usage réel montre si le message aide la guitariste. Comparez les résultats avant et après avec les mêmes entrées, y compris les formes que le parseur strict pourrait refuser à tort.

Fixez la règle d'acceptation avant de modifier le code : aucun suffixe inconnu ne doit produire un accord réussi; aucune forme prise en charge ne doit changer silencieusement de classes de hauteurs; le message doit distinguer une faute de frappe d'une forme non prise en charge. Une erreur de test ou un message confus appelle une révision, pas une invention musicale. Les résultats actuels du corpus restent des déductions du code tant qu'un test exécutable ne les a pas confirmés.

### Exercice 5

Un parseur plus strict rejette `C/E` et évite un mauvais diagramme de C majeur, mais les musiciens ne peuvent toujours pas demander d'accords avec basse. Le travail est-il terminé ?

> **Réponse :** Le risque de réponse fausse est contenu, mais le besoin produit subsiste. Notez ce progrès partiel, gardez la prise en charge des basses au backlog et vérifiez que le message aide à se corriger. Ne revendiquez la prise en charge complète qu'après avoir implémenté et testé la basse E dans le parcours utilisateur.

## Preuves et limites

Les chemins de code, les tests et le [corpus](../../../fixtures/computer-science/cs-003/chord-symbol-corpus.json) ont été inspectés dans une copie locale de GA le 4 octobre 2026. Les résultats décrits sont des déductions du code. Il reste à exécuter la régression, épingler un commit GA, observer les réponses de l'API et recueillir des retours de guitaristes avant publication.
