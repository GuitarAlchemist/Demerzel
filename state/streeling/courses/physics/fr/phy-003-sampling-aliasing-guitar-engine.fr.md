---
module_id: phy-003-sampling-aliasing-guitar-engine
department: physics
course: Échantillonnage et repliement spectral aux frontières du moteur de guitare GA
level: intermediate
prerequisites: ["phy-001-science-of-guitar-sound"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-12-003
version: "0.1.0"
---

# Échantillonnage et repliement spectral aux frontières du moteur de guitare GA

> **Département de physique** | Niveau intermédiaire | 35 minutes | Brouillon français ; révision et publication en attente

## Objectifs

Vous calculerez une fréquence de Nyquist et une fréquence repliée, déterminerez la fréquence d'échantillonnage réellement reçue par le moteur Rust de GA et concevrez un essai hors ligne capable de révéler un repliement sans confondre risque calculé et défaut mesuré. [PHY-001](../fr/phy-001-science-of-guitar-sound.fr.md) présente les harmoniques de la guitare. [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) traite des fenêtres d'analyse de notes changeantes. Ici, la question se situe plus tôt dans la chaîne : **quelles fréquences continues un signal échantillonné peut-il représenter, et que faut-il faire avant la capture, la synthèse ou la conversion de fréquence ?**

## 1. Relier la fréquence à l'artefact, pas au nom de la note

Le [fixture GAS-001 épinglé](../../../fixtures/guitar-acoustics/gas-001/README.md) contient un mi grave à vide enregistré pendant quatre secondes et un rendu natif de quatre secondes du moteur Rust de GA. Les deux fichiers sont mono à **44 100 échantillons par seconde**. Le rendu appelle `engine_note_on(82.4069 Hz, 0.1)` ; l'identité E2 de l'enregistrement est une étiquette du jeu de données, pas une mesure de fréquence. Le rendu provient d'une compilation native, **pas** d'une capture de l'AudioWorklet du navigateur. Ces distinctions comptent lorsqu'on recherche un artefact audio.

Au commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), le [pont audio du navigateur](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) transmet `audioContext.sampleRate` à l'[AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js). Celui-ci appelle `engine_init(srToUse)` et copie les échantillons mono calculés vers les canaux de sortie du navigateur. Le [moteur Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) conserve cette fréquence et l'utilise pour les coefficients des résonateurs et la longueur des lignes à retard. Le WAV épinglé à 44,1 kHz ne prouve donc **pas** que chaque session du navigateur utilise 44,1 kHz. Notez la fréquence réelle du contexte et le chemin de capture avant de comparer un enregistrement du navigateur à GAS-001.

Pour une durée `T`, le nombre d'échantillons vaut `N = f_s T`. Quatre secondes à 44 100 Hz donnent **176 400 échantillons** par canal mono ; à 48 000 Hz, ce serait **192 000**. Aucun de ces nombres n'indique si l'entrée analogique a été filtrée correctement ou si le synthétiseur évite les alias.

### Exercice pratique 1

Une personne voit le rendu GAS-001 à 44,1 kHz et écrit : « Le moteur de GA dans le navigateur tourne toujours à 44,1 kHz. » Que permettent réellement d'affirmer les sources et que doit consigner un test dans le navigateur ?

> **Réponse :** GAS-001 fixe **son WAV rendu nativement** à 44 100 Hz. Le pont du navigateur transmet `audioContext.sampleRate` à l'AudioWorklet et au moteur Rust ; sa valeur réelle doit être observée lors de la session. Consignez la fréquence du contexte, celle de sortie ou d'enregistrement et le codec, la révision du moteur et le chemin de capture. Un WAV natif n'est pas une capture du navigateur.

## 2. Calculer la bande représentable avant de parler d'harmoniques

Pour un signal réel échantillonné uniformément à `f_s`, la fréquence de Nyquist est `f_N = f_s/2` : **22 050 Hz** à 44 100 Hz et **24 000 Hz** à 48 000 Hz. En principe, on peut reconstruire une entrée continue idéale, limitée en bande et dont le contenu est strictement inférieur à `f_N`, à partir de ses échantillons. Une capture réelle demande un filtre antirepliement **avant** l'échantillonnage, avec une bande de transition sous Nyquist. `f_N` est une limite mathématique, pas la promesse d'un filtre parfait dans le microphone, le convertisseur, le moteur ou l'export.

La cible du mi grave à vide est `f_0 = 82.4069 Hz`. Son partiel entier idéal `k` se trouverait à `k f_0`, mais une guitare physique ou synthétisée ne possède pas nécessairement tous ces partiels ni des fréquences exactement entières. À 44,1 kHz, `267 f_0 = 22,002.6423 Hz` reste sous Nyquist et `268 f_0 = 22,085.0492 Hz` le dépasse. À 48 kHz, la limite sépare le partiel **291** (`23,980.4079 Hz`) du **292** (`24,062.8148 Hz`). Ce sont des *limites théoriques d'indice* pour la fondamentale choisie, pas un décompte de partiels audibles ou mesurés. Une marge de production utile se situe sous la limite exacte, car les filtres demandent une bande de transition et l'implémentation importe.

### Exercice pratique 2

Pour cette même cible E2 idéale, calculez l'harmonique entier le plus élevé strictement sous Nyquist à 44,1 et 48 kHz. Cela prouve-t-il que ces harmoniques figurent dans les WAV du fixture ?

> **Réponse :** `floor(22,050 / 82.4069) = 267` et `floor(24,000 / 82.4069) = 291`. Les partiels voisins 268 et 292 dépassent leur limite de Nyquist respective. Ce calcul ne prouve pas qu'un 267e ou 291e partiel détectable se trouve dans les formes d'onde. Il faudrait mesurer les niveaux dans les WAV avec une fenêtre, un plancher de bruit et des limites d'analyse explicites.

## 3. Calculer un alias à la main

Échantillonner un sinus continu à `f` Hz produit `sin(2π f n / f_s)` aux indices entiers `n`. Ajouter ou retrancher un multiple entier de `f_s` donne les mêmes échantillons, à un signe ou à une phase près. Pour obtenir la fréquence d'alias en valeur absolue, repliez `f` par multiples de `f_s` dans `[0, f_s/2]` ; autrement dit, choisissez un entier `m` tel que `|f - m f_s|` tombe dans cet intervalle. C'est un calcul **synthétique sur un seul sinus**, pas une observation de GAS-001.

Prenons un sinus continu à **23 000 Hz**. À 44,1 kHz, il dépasse Nyquist de 950 Hz et se replie à `|23,000 - 44,100| = 21,100 Hz`. La suite échantillonnée est équivalente à celle d'un sinus à 21 100 Hz, avec changement de signe ou de phase. À 48 kHz, 23 000 Hz reste sous la limite de 24 000 Hz : il ne se replie pas. Rééchantillonner ensuite la capture à 44,1 kHz vers 48 kHz ne retrouve pas l'entrée originale à 23 000 Hz ; les échantillons ne permettent pas de distinguer ces deux origines continues.

Dans un moteur de guitare, l'excitation large bande du pincement, les traitements non linéaires et les partiels aigus incitent à **vérifier** cette limite. L'[excitation Rust épinglée](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) utilise du bruit filtré dans une ligne à retard et un traitement échantillon par échantillon. Cette inspection ne prouve aucun alias audible ou mesurable en sortie. Une fréquence d'échantillonnage plus élevée peut déplacer la limite de repliement, mais change aussi les tailles de tampon et le coût de calcul ; elle ne remplace ni une limitation de bande maîtrisée ni les mesures.

### Exercice pratique 3

Une excitation proposée possède une composante continue à 30 000 Hz. Où un échantillonneur idéal placerait-il son alias à 44,1 et à 48 kHz ?

> **Réponse :** À 44,1 kHz, `|30,000 - 44,100| = 14,100 Hz`. À 48 kHz, `|30,000 - 48,000| = 18,000 Hz`. Il s'agit des replis d'un sinus idéal, pas de pics spectraux prédits pour le moteur GA. Un filtre antirepliement en amont peut atténuer la composante avant la capture ; un générateur numérique doit éviter de créer un contenu hors bande ou en maîtriser le repliement.

### Exercice pratique 4

Une personne rééchantillonne vers 48 kHz un enregistrement à 44,1 kHz présentant un pic à 21,1 kHz et affirme : « Avec Nyquist à 24 kHz, le sinus initial à 23 kHz est rétabli. » Expliquez l'erreur.

> **Réponse :** La suite à 44,1 kHz est compatible aussi bien avec un sinus à 21,1 kHz qu'avec un sinus à 23 kHz, à une différence de phase ou de signe près. La conversion peut interpoler ou filtrer les données disponibles, mais pas retrouver leur origine continue. Il faut empêcher le repliement **avant** l'échantillonnage initial au moyen d'un filtre antirepliement analogique, ou créer un contenu numérique limité en bande à la fréquence cible.

## 4. Transformer le risque en test réfutable pour GA

Les [mesures GAS-001](../../../fixtures/guitar-acoustics/gas-001/measurements.json) présentent des pics proches de E2 et quelques partiels graves, pas une étude des alias aigus. Un tracé des deux WAV à 44,1 kHz ne permet pas à lui seul de retrouver la fréquence d'origine d'un alias : un pic sous Nyquist a plusieurs causes possibles. L'enregistrement a une première attaque approximative à 1,1 s et une deuxième vers 2,75 s, tandis que le rendu commence à zéro. Alignez les intervalles sur les attaques avant de comparer les spectres ; [PHY-002](../en/phy-002-time-frequency-guitar-transients.md) explique ce choix temporel.

Une expérience hors ligne devrait d'abord prendre une **référence synthétique connue** : générer un sinus à 23 kHz à une fréquence de référence plus élevée, l'échantillonner à 44,1 et 48 kHz en notant le choix de filtre, puis chercher le repli attendu à 21,1 kHz uniquement dans la branche à 44,1 kHz volontairement non filtrée. Rendez ensuite la même source GA épinglée, avec les mêmes note, vélocité, profil et durée, aux deux fréquences par des appels **natifs**, ou capturez les deux par le **navigateur** en consignant sa fréquence ; ne mélangez pas ces chemins sans le dire. Sauvegardez les paramètres d'entrée, la compilation exacte, les empreintes WAV, la fréquence, le niveau de crête et les fenêtres spectrales. Comparez à une référence maîtrisée à fréquence égale, pour plusieurs notes et vélocités. Si une tonalité inattendue se déplace conformément à la prédiction du repliement quand la fréquence de rendu change, examinez l'étape qui l'engendre ; si elle reste à la même fréquence physique, l'hypothèse d'un simple alias s'affaiblit. Confirmez au moyen d'une modification du code visant l'étape suspecte et répétez l'écoute à niveau égal. Ce protocole est **proposé** : ces rendus, captures et écoutes supplémentaires n'ont **pas** été réalisés pour cette leçon.

Pour une future conversion de fréquence, documentez les fréquences source et cible, les bandes passante et coupée du filtre, son délai, les contrôles d'écrêtage et la présence éventuelle d'un encodage avec pertes avant la capture de référence. Le pont du navigateur possède un [chemin MediaRecorder facultatif](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) ; ne supposez pas que son blob est un WAV brut à 44,1 kHz. Gardez ce chemin distinct du rendu natif du fixture.

### Exercice pratique 5

Un pic à 21,1 kHz apparaît dans un rendu du moteur à 44,1 kHz. Suffit-il pour conclure à un alias de synthèse issu de 23 kHz ? Indiquez la comparaison décisive suivante et un contrôle.

> **Réponse :** Non. Le pic peut être une composante dans la bande, un alias d'une autre composante hors bande ou un artefact de capture. Rendez la même configuration du moteur épinglé à 48 kHz et comparez des spectres aigus alignés sur les attaques : une source proche de 23 kHz devrait y paraître vers 23 kHz, alors que son alias à 44,1 kHz se situerait vers 21,1 kHz. Gardez constants la révision du moteur, la note, la vélocité, le profil et le chemin de capture ; inspectez l'étape du signal ou ajoutez une limitation de bande ciblée avant d'attribuer la cause. Le déplacement prévu est un **test**, pas un résultat observé.

## Sources et limites actuelles

- [Fixture GAS-001 épinglé, provenance et fréquences](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), avec son [README local](../../../fixtures/guitar-acoustics/gas-001/README.md). La source enregistrée y est attribuée à **collegefishiesd** sous licence CC BY-SA 4.0 ; cette leçon ne reproduit pas l'audio.
- Commit GA [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo) : [pont du navigateur](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js) et [moteur Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs).
- Les nombres d'échantillons, limites d'indice harmonique et replis de sinus ci-dessus découlent directement des fréquences annoncées. Aucune nouvelle mesure d'alias aigu sur GAS-001, capture du navigateur, révision indépendante du sujet, essai par des apprenants, traduction révisée par un spécialiste ou lecture publique n'a été effectuée pour PHY-003.
