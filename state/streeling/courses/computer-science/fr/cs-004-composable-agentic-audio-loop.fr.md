---
module_id: cs-004-composable-agentic-audio-loop
department: computer-science
course: Composer et éprouver une boucle agentique d'amélioration audio
level: intermediate
prerequisites: ["cs-002-governing-agentic-loops", "gas-001-open-string-audio-evidence"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: cs-2026-10-04-004
version: "0.1.0"
---

# Composer et éprouver une boucle agentique d'amélioration audio

> **Département d'informatique** | Niveau intermédiaire | 45 minutes | Brouillon : révision du contenu et de la traduction en attente

## Objectifs

Vous saurez séparer les fonctions qui transforment des données des opérations qui agissent sur le monde, exécuter un témoin sans amélioration, traiter honnêtement une reprise après expiration du délai et refuser une réussite proclamée par un agent lorsque les preuves indépendantes ne la soutiennent pas.

## 1. Partir du besoin du guitariste et d'un témoin

Un guitariste veut que l'instrument WASM temps réel de GA soit plus convaincant. GA possède déjà un moteur de guitare en Rust, un AudioWorklet et une boucle de capture hors ligne. Le prototype GA local, non fusionné, au commit `6fac5735f7ffbb4116ebee05cfc9d7911bb12ce9` ajoute `Rust/guitar-web-wasm-demo/scripts/run-comfy-audio.js` et `compare-audio.js`. Le premier soumet un WAV à un workflow ComfyUI local et conserve sa provenance. Le second compare le son de départ, le candidat et la référence avec des résumés FFT, ainsi que des mesures RMS et Haar par tranches de 250 ms. Le workflow fourni ne fait que charger et enregistrer le son : il **ne l'améliore pas**. Aucun candidat produit par une véritable instance ComfyUI ni aucune écoute à l'aveugle n'a été vérifié.

La [paire GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) comprend un mi grave à vide enregistré, avec attribution, et un rendu natif du moteur Rust de GA. Ce rendu partage le code du moteur WASM, mais ne provient pas de l'AudioWorklet. La première attaque de l'enregistrement se situe vers 1,1 seconde; une autre arrive vers 2,75 secondes. On doit choisir des fenêtres correspondant à la même note avant de donner un sens à une distance.

Commençons par poser **candidat = son de départ**. En utilisant deux fois `ga-engine-e2-open-4s.wav`, la référence `deb-low-e-open.wav`, `--reference-offset 1.1` et `--seconds 1.5`, le comparateur a donné la même erreur RMS moyenne sur 250 ms aux deux fichiers : `0.124158746`. Toutes les erreurs FFT et Haar étaient également identiques. Ce témoin négatif est utile : si la chaîne annonce un progrès, c'est sa règle de décision qui est défectueuse, même si les commandes se sont bien exécutées.

### Exercice 1

Que conclure lorsque le candidat et le son de départ ont tous deux l'empreinte SHA-256 `a78a70243a81aa79d806d9ef3db7baa1385c479505f7d5e97b8bf0c7866c3f98` ?

> **Réponse :** Rejeter toute affirmation d'amélioration. Les fichiers sont identiques octet pour octet; ni les mesures ni l'écoute ne peuvent attribuer un changement à ComfyUI. Conserver cet essai comme témoin et vérifier si le workflow a réellement transformé le son.

## 2. Composer des transformations, isoler les effets

Chaque flèche de la chaîne porte un contrat. Une fonction pure donne la même sortie pour la même entrée et ne lit ni horloge ni fichier, n'appelle aucun service et n'écrit rien. Les opérations à effets restent aux frontières :

```text
captureWasm(note, profil)              EFFET -> WAV de départ
chargerEtValider(fichiers, note, attaques) EFFET + validation PURE -> manifeste fixe
soumettreComfy(workflow, départ)       EFFET -> identifiant de requête ou erreur
récupérerCandidat(identifiant)        EFFET -> WAV et empreintes
décoderEtAligner(manifeste)           EFFET -> tableaux d'échantillons
caractéristiques(échantillons)        PUR -> FFT, RMS, Haar
comparer(caractéristiques, référence) PUR -> écarts et alertes
proposerDécision(preuves, règles)      PUR -> rejeter/accepter/écouter
écouterEnAveugle(A, B, question)       OBSERVATION HUMAINE -> compte rendu
consignerDécision(toutesLesPreuves)   EFFET -> reçu durable
```

On peut ainsi tester `caractéristiques` avec des tableaux connus et `proposerDécision` avec des fiches fixes, sans lancer ComfyUI ni croire la prose de l'agent. Le prototype sépare déjà certains calculs (`timeFeatures`, `compareFeatures`) de son réseau et de ses fichiers. C'est un premier point de découpage, pas la preuve que tout le programme est pur. Le décodage par FFmpeg et la lecture d'un WAV restent des effets. À chaque frontière, préférer un résultat explicite, par exemple `Ok(candidat)` ou `Err(type, prompt_id, preuves)`; ne jamais remplacer silencieusement un candidat manquant par le son de départ.

La règle minimale est claire : candidat identique octet pour octet, **aucune amélioration**; fichier absent, mauvaise note ou attaques non alignées, **réparation nécessaire**; différence spectrale plausible, **écoute à l'aveugle nécessaire**, pas acceptation. Une valeur de perte ne parle pas à la place du guitariste. L'évaluation conserve la référence fixe et rapporte autant les progrès que les régressions de l'attaque, de la hauteur, du déclin, du bruit et des artefacts.

### Exercice 2

Classez `timeFeatures(samples)`, `fetch('/prompt')`, `hash(bytes)`, le décodage FFmpeg et l'écriture du reçu. À quel moment l'agent peut-il proposer une nouvelle seed ?

> **Réponse :** `timeFeatures` et `hash` peuvent être purs si toutes leurs entrées sont fournies. L'appel réseau, FFmpeg et l'écriture sont des effets. L'agent peut proposer une seed avant `soumettreComfy`; la seed réellement soumise et l'empreinte du workflow doivent figurer au reçu.

### Exercice 3

Le candidat réduit l'erreur du centroïde spectral, mais son attaque paraît floue lors d'une écoute A/B à niveau égal. Peut-on modifier le moteur ?

> **Réponse :** Non. La mesure n'est qu'un diagnostic. Consigner à la fois la variation chiffrée et l'observation du guitariste, rejeter ou retravailler le candidat, puis garder le moteur de départ. Aucune écriture automatique des paramètres Rust/WASM n'en découle.

## 3. Reprendre sans inventer le résultat

Supposons que ComfyUI accepte `/prompt`, puis que le client expire avant de lire `/history/{prompt_id}`. Le serveur peut encore travailler. L'issue est **inconnue**; elle n'est pas forcément un échec. Si l'identifiant est connu, interroger l'historique avant de soumettre à nouveau. S'il est perdu, consigner l'incertitude et ne pas compter la reprise comme une nouvelle expérience indépendante. L'expérience logique se définit par les empreintes du son de départ et du workflow, les champs du modèle et la seed; chaque tentative garde séparément son identifiant. Un nom de fichier dérivé de l'empreinte facilite le repérage du même WAV, mais ne rend pas l'exécution du modèle idempotente.

Le prototype ne persiste pas encore l'identifiant avant de récupérer le candidat : la reprise après interruption reste donc une lacune. Une correction ultérieure de la provenance distingue `comparison_pending`, `completed` et `comparison_failed`; un échec de comparaison ne doit jamais laisser un verdict de qualité « réussi ». On ajoutera la reprise après avoir reproduit ce cas dans un test et rendu son reçu inspectable.

### Exercice 4

Le WAV candidat existe, mais le décodage de la référence échoue. Quel statut inscrire et que peut-on reprendre ?

> **Réponse :** Garder le candidat et ses empreintes, marquer `comparison_failed` et noter l'erreur. Corriger la référence ou le décodeur, puis relancer **la comparaison du même candidat**. Il n'y a aucune raison de relancer ComfyUI.

## 4. Faire du dogfooding sur toute la chaîne

Depuis un checkout contenant GA et les fixtures Streeling, adaptez le chemin. Le prototype GA est actuellement un **commit local**; ceci est un exercice pour son réviseur, pas une procédure d'installation publique :

```powershell
$fixture = '<chemin-du-checkout-Demerzel>\state\streeling\fixtures\guitar-acoustics\gas-001'
node scripts/compare-audio.js `
  --baseline "$fixture\ga-engine-e2-open-4s.wav" `
  --candidate "$fixture\ga-engine-e2-open-4s.wav" `
  --reference "$fixture\deb-low-e-open.wav" `
  --reference-offset 1.1 --seconds 1.5 --output control-comparison.json
```

Dans le JSON, vérifiez l'égalité des empreintes et des erreurs. Ensuite seulement, si un modèle audio local et sa licence sont connus, utilisez un vrai workflow ComfyUI. Gardez les mêmes fichiers de départ et de référence, changez un seul paramètre, notez modèle, seed et empreintes, puis mesurez et faites écouter à l'aveugle, à niveau égal. Le reçu doit contenir l'observation de l'utilisateur, les mesures, la décision et la prochaine expérience. Le dogfooding consiste à utiliser notre propre moteur et nos propres outils pour découvrir les problèmes de préparation, d'erreur, de reprise et de révision. Un agent qui ne peut ni lire la fixture ni écrire son reçu a découvert un défaut d'expérience; l'envoi d'un prompt ne vaut pas progrès.

### Exercice 5

Proposez une condition de réussite et un critère de rejet. Qui décide d'une modification du moteur temps réel ?

> **Réponse :** Par exemple, exiger un candidat reproductible, un son de départ et une référence fixes, aucune régression de l'attaque ou de la hauteur, et une préférence notée lors d'une écoute à l'aveugle. Une sortie identique, une provenance absente ou des refus répétés à l'écoute réfutent l'amélioration. L'agent propose; une évaluation indépendante et une personne habilitée décident du test d'un changement Rust/WASM. Le candidat hors ligne ne devient pas à lui seul le moteur temps réel.

## Sources et limites

Le pont GA correspond au commit local `6fac5735`; ses tests simulés passent, mais ComfyUI ne répondait pas sur `127.0.0.1:8188` et aucune nouvelle capture WASM dans le navigateur n'a été effectuée. Le témoin a été relancé indépendamment avec les [WAV GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md). [CS-002](cs-002-governing-agentic-loops.fr.md) traite des bornes externes d'une boucle agentique; ce cours porte sur la composition d'une expérience observable. Le fichier GA `docs/methodology/agentic-engineering.md` décrit les files de tâches et le harness. Les [nœuds audio](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_audio.py) et les [routes du serveur](https://github.com/Comfy-Org/ComfyUI/blob/master/server.py) documentent l'interface ComfyUI. Les distances FFT/Haar ne prouvent pas le réalisme perçu, et nous n'avons pas observé la séance d'enregistrement d'origine.
