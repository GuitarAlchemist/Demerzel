---
module_id: gas-001-open-string-audio-evidence
department: guitar-acoustics
course: Ce qu'une corde à vide peut apprendre au moteur guitare WASM
level: beginner
prerequisites: []
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-acoustics-2026-10-04-001
version: "0.1.0"
---

# Ce qu'une corde à vide peut apprendre au moteur guitare WASM

> **Département d'acoustique de la guitare et de synthèse sonore** | Niveau : débutant | Durée estimée : 40 minutes | Statut : en attente de relecture

## Objectifs

À la fin de ce cours, vous saurez :

- comparer un enregistrement de corde à vide et une note produite par le moteur guitare Rust/WASM existant de GA ;
- repérer l'attaque avant de mesurer hauteur, partiels et décroissance ;
- utiliser une FFT fenêtrée pour les pics harmoniques locaux et des wavelets pour suivre l'attaque et l'évolution des partiels ;
- distinguer un écart mesuré d'un jugement sur le réalisme perçu ;
- évaluer hors ligne une variante créée avec ComfyUI avant de modifier le moteur WASM temps réel.

## La question du projet et les fichiers d'exercice

GA possède déjà un [moteur guitare Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) chargé par un [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js). Il modélise une corde pincée, des résonances de caisse, l'attaque et une réverbération. GA dispose aussi d'une [boucle hors ligne d'enregistrement et d'analyse](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), avec une coloration DDSP facultative. **Le code GA inspecté ne raccorde pas encore ComfyUI à cette boucle.** L'objectif du projet est d'explorer des variantes dans ComfyUI hors ligne, de les mesurer et de les écouter, puis de décider d'un changement dans le moteur WASM existant. Le modèle génératif n'a pas à fonctionner dans l'AudioWorklet.

Le dossier `state/streeling/fixtures/guitar-acoustics/gas-001/` contient deux fichiers :

| Fichier | Provenance | Limite |
|---|---|---|
| `deb-low-e-open.wav` | Enregistrement acoustique mono de quatre secondes, identifié par `source=deb`, `low_E`, `fret=0`, `E2` dans le [jeu de données `collegefishiesd` à la révision `a33a262`](https://huggingface.co/datasets/collegefishiesd/guitar-fretboard-notes/tree/a33a26243e88e7ccd4893bee30eac3219ec8bef8). Licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) et attribution dans le [README de la fixture](../../../fixtures/guitar-acoustics/gas-001/README.md). | L'identification vient du jeu de données ; nous n'avons pas observé la séance d'enregistrement. |
| `ga-engine-e2-open-4s.wav` | Note mono de quatre secondes calculée par le moteur GA épinglé, à 44 100 Hz, profil par défaut 0, avec `engine_note_on(82.4069, 0.1)`, grâce au [script de rendu](../../../fixtures/guitar-acoustics/gas-001/render-ga-e2.py). | Il s'agit d'une compilation native du même code Rust, et non d'une capture de l'AudioWorklet dans le navigateur. |

Les deux WAV et le [script de mesure](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) se trouvent dans le dépôt source. Leur publication exigera la copie des fichiers audio ou des liens stables. Les empreintes SHA-256, la méthode et l'attribution figurent dans le [README](../../../fixtures/guitar-acoustics/gas-001/README.md). Mi2 correspond nominalement à 82,4069 Hz ; un pic mesuré peut tomber sur une autre valeur selon la résolution.

### Exercice

Le comparateur spectral de GA utilise aussi un long fichier `by-the-lake.wav`. Pourquoi le fichier identifié `low_E`, `fret=0` convient-il mieux ici ?

> **Réponse :** Le jeu de données identifie une seule note de mi grave à vide. `by-the-lake.wav` est une longue référence enregistrée dont aucune portion n'est attestée comme une corde de mi à vide isolée. La traiter ainsi fausserait la comparaison.

## 1. Repérer l'événement avant de mesurer

L'enregistrement commence par un passage relativement silencieux. La première attaque arrive vers **1,1 seconde** ; une autre apparaît vers **2,75 secondes**. La note GA commence à zéro. Une FFT sur les quatre secondes mélangerait silence, attaques et décroissances. Même une FFT locale entre 0,2 et 1,2 seconde *depuis le début du fichier* analyserait surtout l'avant-note de l'enregistrement. Alignez les fenêtres sur la première attaque et arrêtez-vous avant la seconde.

Pour cette fixture, le [script de mesure](../../../fixtures/guitar-acoustics/gas-001/measure-pair.py) applique une fenêtre de Hann d'une seconde, de **0,2 à 1,2 seconde après la première attaque**. Il compare aussi le niveau RMS entre 0,2–0,4 et 1,0–1,2 seconde après l'attaque. Le repère d'attaque est approximatif, déduit de niveaux calculés par petites fenêtres. Une autre personne devrait inspecter la forme d'onde et répéter la mesure en déplaçant légèrement ce repère. Le [manuel d'Audacity](https://manual.audacityteam.org/man/plot_spectrum.html) explique le compromis entre la durée de la fenêtre et la résolution fréquentielle.

### Exercice

Un script prend les secondes 0,2 à 1,2 des deux fichiers et conclut que l'enregistrement n'a pas de partiels de mi2. Que faut-il corriger ?

> **Réponse :** Repérer la première attaque de l'enregistrement et déplacer la fenêtre par rapport à elle. La fenêtre choisie précède surtout la note. Il faut aussi écarter la seconde attaque de l'estimation de décroissance et documenter le repère approximatif.

## 2. Donner une tâche distincte à la FFT et aux wavelets

Une **FFT fenêtrée** montre les fréquences fortes pendant un intervalle choisi. Elle sert à vérifier le pic local de mi2 et le niveau relatif des harmoniques, sans dire quand chacune est apparue ou a diminué. Une **STFT** fait glisser la fenêtre pour suivre un son qui évolue, avec une résolution temporelle et fréquentielle imposée par sa taille. [SciPy décrit cet usage temporel de la STFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html).

Une **wavelet complexe** adapte son échelle temporelle à la fréquence. Notre script emploie des wavelets proches de Morlet, de six cycles, centrées vers 82, 165 et 330 Hz. Elles suivent l'attaque et le niveau ultérieur des partiels. Le choix des fréquences, du nombre de cycles et du repère d'attaque influence le résultat ; ce n'est pas une note de réalisme. [Une étude du timbre de la guitare](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218) emploie aussi une analyse en wavelets continues pour suivre l'énergie des partiels.

| Mesure | Mi2 enregistré | Mi2 produit par GA |
|---|---:|---:|
| Pic proche de mi2, FFT locale | 83 Hz | 82 Hz |
| Deuxième partiel relativement au premier, FFT locale | +7,0 dB | −16,9 dB |
| Évolution du RMS, fenêtre tardive moins précoce | −3,9 dB | −1,1 dB |
| Évolution du deuxième partiel par wavelet | −4,5 dB | −12,9 dB |

Les niveaux absolus des deux enregistrements diffèrent : comparez d'abord les **rapports internes** à chaque fichier. L'écart du deuxième partiel vaut 23,9 dB selon cette FFT locale ; cela ne signifie pas qu'un fichier est globalement 23,9 dB plus fort ni plus réaliste. La mesure en wavelets suggère que ce partiel baisse plus vite dans le rendu GA, selon cette méthode. Inspectez la forme d'onde et écoutez avant de désigner un paramètre responsable.

### Exercice

Quel outil choisiriez-vous pour situer une attaque rapide ? Quelle mesure donne les pics harmoniques locaux les plus faciles à comparer ? Que ne prouvent-elles pas ?

> **Réponse :** Une analyse temporelle comme les wavelets ou la STFT aide à situer l'attaque ; une FFT sur une fenêtre annoncée compare les pics locaux. Aucune ne prouve le réalisme perçu à partir d'une seule note.

## 3. Transformer l'écart en essai contrôlé sur le WASM

Le [moteur Rust de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs) expose décroissance, brillance, dispersion, décroissance de l'attaque, réverbération et profil de guitare. Un partiel aigu faible dans cette paire justifie un **essai** sur la brillance ou l'excitation, pas un verdict. Modifiez un paramètre ou un petit ensemble documenté, recalculez la même note, conservez les WAV avant/après et la révision du code. Vérifiez la hauteur, les partiels, l'attaque, l'absence d'écrêtage et la latence sur plusieurs cordes et intensités. Ajoutez ensuite une écoute à niveau égalisé avec des guitaristes. L'[article original de Karplus et Strong](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf) décrit une décroissance des harmoniques qui varie dans le temps : une seule image spectrale ne la résume pas.

ComfyUI peut produire une **troisième variante hors ligne**. Son cœur propose des [nœuds pour charger, écouter et enregistrer l'audio](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py), et un [workflow officiel de génération audio](https://github.com/Comfy-Org/ComfyUI/blob/master/blueprints/Audio%20Generation%20%28Stable%20Audio%203%20Medium%20Base%29.json). Gardez l'empreinte de l'entrée, le workflow JSON, le modèle et sa version, la seed, le prompt, les réglages, l'empreinte de sortie, le format et la licence. Vérifiez que la variante contient toujours une seule note mi2 avant de la comparer. Une sortie compressée doit être exportée sans perte ou convertie de façon documentée pour les mesures. La boucle GA actuelle utilise DDSP ou une coloration spectrale, pas ComfyUI : le raccordement reste à réaliser.

On peut en faire une **boucle agentique de dogfooding** : enregistrer le son que GA produit aujourd'hui, laisser un agent proposer une seule modification testable, explorer au besoin une variante dans ComfyUI, produire le son du moteur WASM modifié, puis comparer tous les fichiers à la même référence externe. Chaque cycle conserve le diff des paramètres, les empreintes, les mesures, le résultat d'écoute et la décision d'accepter ou de rejeter. Le score heuristique de l'agent qui propose n'est qu'un indice : une méthode de mesure fixe et une écoute séparée évitent que la boucle ne récompense sa propre préférence. Un essai rejeté documente aussi ce qui n'a pas marché.

### Exercice

Une sortie ComfyUI semble plus brillante que GA, mais son prompt, sa seed, son entrée et sa version de modèle manquent. Peut-elle guider le moteur WASM ? Donnez deux contrôles pour le prochain essai.

> **Réponse :** Pas encore. Notez exactement le workflow, le modèle, la seed et les empreintes d'entrée et de sortie, puis vérifiez qu'il s'agit d'un mi2 isolé. Comparez à niveau égalisé la référence, GA et cette variante ; modifiez ensuite un paramètre du moteur en conservant l'avant/après. Une écoute ou une évaluation séparée doit contrôler le résultat : l'agent ne peut pas se valider avec son seul score. « Plus brillant » ne désigne pas à lui seul une bonne modification.

## 4. Dire ce que l'on ignore encore

La paire montre une énergie proche de mi2 dans les deux fichiers et des rapports de partiels différents selon les fenêtres choisies. Elle ne dit pas lequel convainc le plus à l'écoute. L'instrument enregistré, le microphone, la pièce, la force du jeu et la chaîne du jeu de données diffèrent du rendu natif de GA. Une seule note ne représente ni les accords ni tout le manche. Les wavelets apportent la dimension temporelle, sans effacer ces différences de source.

Une FFT locale ne peut pas conclure sur **la sensation de l'attaque initiale** ni sur **la réponse à plusieurs forces de jeu**. Même les wavelets de cette seule note ne couvrent pas toutes les situations. Un test d'écoute devrait masquer l'identité des fichiers, égaliser les niveaux, inclure plusieurs cordes et intensités, puis consigner les jugements. Le [comparateur spectral de GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/scripts/run-spectral-critic.js) fournit des indices, pas un verdict validé de réalisme.

### Exercice

Formulez la conclusion la plus forte permise par le tableau, puis donnez deux observations nécessaires avant d'affirmer que « le nouveau moteur WASM sonne davantage comme une guitare ».

> **Réponse :** Les deux mi2 diffèrent quant au niveau et à l'évolution du deuxième partiel selon la méthode annoncée. Une affirmation sur le réalisme exige des écoutes à niveau égalisé et des mesures répétées sur d'autres notes ou intensités, avec les conditions d'enregistrement documentées.

## À retenir

- Alignez les attaques avant de comparer une note enregistrée et une note synthétique.
- La FFT locale mesure des pics pendant une fenêtre ; STFT et wavelets montrent leur évolution.
- Un écart numérique donne une hypothèse de réglage, pas un verdict perceptif.
- ComfyUI sert à explorer et évaluer hors ligne ; le moteur Rust/WASM existant reste le rendu temps réel.
- Le dogfooding donne à l'agent un son GA à améliorer ; des mesures fixes et une écoute indépendante décident si l'essai aide vraiment.
- Séparez référence enregistrée, variante générée, révision du code, méthode et résultat d'écoute.

## Sources et limites

- [Provenance des fichiers, empreintes, scripts, mesures et attribution de la licence audio](../../../fixtures/guitar-acoustics/gas-001/README.md).
- GA : [moteur Rust](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/rust-engine/src/lib.rs), [pont AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js), [boucle d'analyse hors ligne](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/full-auto.ps1), commit `dc2e74c`.
- [Karplus et Strong](https://users.soe.ucsc.edu/~karplus/papers/digitar.pdf), [guide FFT d'Audacity](https://manual.audacityteam.org/man/plot_spectrum.html), [STFT de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html), [étude du timbre par wavelets](https://www.iieta.org/journals/ts/paper/10.18280/ts.380218).

*Recherche : `guitar-acoustics-2026-10-04-001`. Relectures métier et linguistique en attente. La fixture ne comprend ni capture de l'AudioWorklet dans le navigateur, ni raccordement ComfyUI, ni verdict issu d'un panel d'écoute.*
