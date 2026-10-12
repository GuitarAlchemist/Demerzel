---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Tester l'ordre de l'égalisation et de la compression sur une guitare"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-12-004
version: "1.1.0"
---

# Tester l'ordre de l'égalisation et de la compression sur une guitare

> **Département d'ingénierie audio** | Niveau intermédiaire | 35 minutes | Brouillon français révisé ; révision disciplinaire, essais d'apprenants et publication en attente

## Objectifs et question du projet

Vous distinguerez un filtre d'un processeur dépendant du niveau, démontrerez par un petit calcul que leur ordre compte et préparerez une comparaison hors ligne qu'une future implémentation de compresseur pourra réellement réfuter. **Question du projet :** si GA envisage de traiter un Mi2 à vide enregistré ou son rendu par le moteur de guitare, placer une égalisation donnée avant la compression modifie-t-il l'attaque et le niveau par rapport à la *même* égalisation placée après ? Une décision de traitement exige des sorties mesurées à partir de la même entrée, et non une règle générale sur l'ordre qui semblerait le plus naturel.

Le [fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) fournit une paire concrète : un WAV mono de Mi2 à vide enregistré et un WAV mono rendu par le moteur natif GA, chacun durant quatre secondes à 44 100 Hz. La première attaque enregistrée commence **approximativement à 1,1 s** dans le fichier ; une autre survient vers **2,75 s**. Le rendu commence au temps zéro. Les [mesures du fixture](../../../fixtures/guitar-acoustics/gas-001/measurements.json) montrent des différences de répartition des partiels et de décroissance dans certains intervalles, sans classer le réalisme ni établir qu'une compression est nécessaire. Conservez les deux WAV d'origine. Pour cette leçon, prenez le fichier *enregistré* comme première entrée proposée et réservez le rendu à une réplication ultérieure, étiquetée séparément. Ne comparez pas un fichier traité à un autre non traité comme si l'ordre était la seule cause de l'écart.

Le [moteur audio du navigateur GA au commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) charge un moteur WASM dans un [AudioWorklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), le relie aux haut-parleurs et propose un chemin MediaRecorder. Le rendu GAS-001 provient d'une **compilation native du même code Rust**, pas d'une capture de ce worklet. Ces sources documentent la provenance du signal de guitare, sans montrer de chaîne égaliseur-compresseur dans la démonstration. Au [commit IX `bd1336b`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), `FirFilter` fournit la conception de filtres passe-bas et passe-haut ainsi qu'une méthode `apply` sur des échantillons. C'est un composant possible pour un filtre hors ligne. Ces artefacts ne prouvent l'existence d'aucun compresseur ; il faudra en préciser et examiner un avant un véritable essai A/B.

## 1. Définir précisément les deux opérations

Un filtre FIR est linéaire. Avec des coefficients `h`, sa sortie est `E(x)[n] = Σ_k h[k] x[n-k]`, selon une règle de bord explicite. La méthode `FirFilter::apply` d'IX commence avec une sortie remplie de zéros et n'inclut que les termes dont l'indice d'entrée est positif ou nul. Un passe-bas ou passe-haut peut modifier le niveau présenté ensuite au détecteur. La réponse exacte dépend des coefficients ; le filtre peut aussi déplacer ou étaler une attaque. Appeler tout réglage « égalisation corrective » ne démontre pas son utilité pour la guitare.

Un compresseur dépend du **niveau**. Son gain dépend de l'entrée et, dans une conception classique, de l'enveloppe d'un détecteur avec états d'attaque et de relâchement. La forme d'onde peut dépendre du seuil, du ratio, du type de détecteur, des constantes de temps, du couplage des canaux, du gain de compensation et de l'initialisation. Il faut consigner ces détails. Un compresseur large bande n'est pas automatiquement sélectif en fréquence : son détecteur réagit au niveau de la forme d'onde d'entrée, que plusieurs partiels peuvent influencer. Dire qu'il « entend 200 Hz » est une image, pas une garantie quant au composant responsable de la réduction de gain. Filtrage de la chaîne latérale, compression multibande et égalisation dynamique seraient d'autres expériences.

Soit `E` l'égalisation choisie et `C` le compresseur. Les deux chaînes proposées sont `A = E(C(x))` (**Comp→EQ**) et `B = C(E(x))` (**EQ→Comp**). Les deux doivent recevoir le même `x` et utiliser les mêmes coefficients EQ, paramètres de compression, fréquence d'échantillonnage et format de canaux. `C` reçoit le signal brut `x` dans A et le signal filtré `E(x)` dans B. L'égalisation finale de A ne peut annuler une décision de détection déjà prise. À l'inverse, le compresseur de B peut réagir à des crêtes créées ou atténuées par l'égalisation. Aucun ordre n'est universel : le son recherché et les compromis mesurés guident le choix.

### Exercice pratique 1 : repérer l'entrée du détecteur

Qu'entre-t-il précisément dans `C` pour A et B ? Si l'égalisation augmente un partiel choisi de la guitare, dans quelle chaîne la réduction de gain *pourrait-elle* changer à cause de cette hausse ?

> **Réponse :** Dans A, `C` reçoit `x` non filtré ; dans B, il reçoit `E(x)`. L'augmentation du partiel peut influer directement sur le détecteur large bande de B. Dans A, l'égalisation vient après le compresseur et ne peut modifier sa décision antérieure de gain. C'est une relation causale, pas une prédiction de l'audibilité ni de la quantité de réduction de gain.

## 2. Démontrer l'effet de l'ordre avec un fixture synthétique

Prenez un signal de quatre échantillons **synthétique**, `x=[0,2,0,0]`, avec un historique nul. Définissez le FIR `E` par `h=[0.5,0.5]`, de sorte que `E(x)[n]=0.5x[n]+0.5x[n-1]` pour les échantillons disponibles. Cette moyenne à deux coefficients est un exemple mathématique de passe-bas, **ni** un réglage EQ recommandé pour la guitare **ni** les coefficients produits par le concepteur `lowpass` d'IX. Définissez un compresseur pédagogique sans mémoire, seuil `T=1`, ratio `R=2:1`, sans gain de compensation, attaque ou relâchement : `C(v)=sign(v) × (|v| if |v|<=1 else 1+(|v|-1)/2)`. Il transforme l'échantillon positif `2` en `1.5`. Un véritable compresseur à enveloppe demanderait un état supplémentaire et pourrait donner d'autres valeurs.

Calculez A : `C(x)=[0,1.5,0,0]`, puis `E(C(x))=[0,0.75,0.75,0]`. Calculez B : `E(x)=[0,1,1,0]`, puis `C(E(x))=[0,1,1,0]`, car aucun échantillon filtré non nul ne dépasse le seuil. Les sorties diffèrent de `0.25` aux indices 1 et 2. C'est un contre-exemple exact à `E∘C = C∘E` pour ces opérateurs définis. Ce n'est **ni** une mesure de l'enregistrement GAS-001, **ni** la sortie prédite d'un plugin non spécifié, **ni** une preuve que B sonne mieux.

Les crêtes différentes, `0.75` pour A et `1` pour B, rappellent qu'on ne doit pas juger l'ordre avec un niveau d'écoute incontrôlé. Une écoute comparative exige un ajustement de niveau déclaré **après** chaque chaîne complète, avec les gains appliqués consignés. Ne modifiez pas séparément les seuils pour imposer une réduction de gain semblable : cela changerait la question expérimentale. Sur un passage réel où les deux chaînes restent sous le seuil, elles peuvent produire des résultats identiques ou presque malgré ce contre-exemple.

### Exercice pratique 2 : calculer les deux chaînes

Avec les `x`, `h` et `C` déclarés, écrivez A et B. Quelle est la valeur de `B[1]-A[1]` et quelle conclusion le calcul permet-il ?

> **Réponse :** `A=[0,0.75,0.75,0]` ; `B=[0,1,1,0]` ; `B[1]-A[1]=0.25`. Les opérateurs spécifiés ne commutent pas sur cette entrée synthétique. Le calcul ne donne aucun verdict d'écoute ni résultat pour un vrai compresseur à enveloppe ou un WAV de guitare.

### Exercice pratique 3 : traiter le bord

Avec un historique nul et `h=[0.5,0.5]`, combien valent `E([2,0])[0]` et `E([2,0])[1]` ? Pourquoi un dispositif hors ligne doit-il consigner son traitement des bords et de la latence ?

> **Réponse :** Les valeurs sont `1` et `1`. À l'indice 0, l'échantillon précédent manquant vaut zéro ; à l'indice 1, l'échantillon d'entrée précédent vaut `2`. Une autre règle de remplissage ou de préchauffage modifierait les échantillons de l'attaque. Des FIR pratiques plus longs peuvent ajouter un délai de groupe ; il faut aligner les sorties et consigner la règle de bord avant d'interpréter un écart de temps entre crêtes.

## 3. Concevoir un essai A/B réfutable sur la guitare

Ce qui suit est une **expérience hors ligne proposée, non exécutée**. Partez de `deb-low-e-open.wav` dans le [répertoire du fixture](../../../fixtures/guitar-acoustics/gas-001/README.md). Son SHA-256 est `03a1965f275f0858be70476dab2bf55d2cbf2272ef7a50c61453d45e7f38b248`. Décodez une fois ses échantillons WAV mono float32 et préservez les octets originaux. Notez le décodeur, la fréquence d'échantillonnage, le hachage d'entrée et la première attaque approximative. Examinez la forme d'onde avant de fixer un intervalle excluant la seconde attaque. Une deuxième exécution pourrait utiliser `ga-engine-e2-open-4s.wav`, mais doit être présentée séparément : c'est un rendu natif avec un autre début et une autre provenance.

Avant d'implémenter le futur compresseur, rédigez un contrat de paramètres : seuil en dBFS, ratio, unités d'attaque et de relâchement, détecteur de crête ou RMS, anticipation, genou, gain de compensation, remise à zéro de l'état et comportement au premier échantillon. Fixez sa révision de code et ses tests. Utilisez un seul EQ déterministe : publiez les coefficients FIR littéraux ou fixez la [source du filtre IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs) et consignez fréquence de coupure, ordre, coefficients et traitement des bords. Gardez les *mêmes* réglages de compresseur et d'EQ dans les deux ordres ; réinitialisez indépendamment l'état du compresseur avant chaque rendu. Exportez des WAV A et B sans perte à la même fréquence et conservez la trace de réduction de gain, le nombre d'échantillons et le manifeste. Ne prétendez pas que GA ou IX fournit déjà cette chaîne complète.

Choisissez la fenêtre du premier pincement par rapport à l'attaque enregistrée **vers 1,1 s**, et écrivez l'indice d'échantillon choisi dans le manifeste. Pour chaque chaîne, rapportez l'échantillon et le temps du pic, le RMS à court terme ou l'enveloppe près de l'attaque, le RMS plus tard et la trace de réduction de gain. Pour écouter, égalisez le niveau de sortie et rapportez cet ajustement afin de ne pas confondre mesures brutes et ajustées. Évitez l'écrêtage après compensation ou ajustement de niveau. Si la latence du FIR diffère d'un chemin sans traitement, alignez les sorties par une règle de délai ou de corrélation croisée documentée avant de comparer les temps de pic. Un essai d'écoute, s'il est approuvé plus tard, devrait masquer les étiquettes, randomiser l'ordre et admettre « aucune différence perceptible » ; il est distinct de la vérification numérique.

L'**observation qui réfuterait** l'hypothèse étroite « la place de l'EQ change ce passage de guitare avec ces réglages fixés » serait que A et B restent identiques échantillon par échantillon à une tolérance numérique prédéfinie, ou qu'un écart apparent disparaisse après correction d'une erreur d'alignement, de réinitialisation ou de niveau. Si les sorties diffèrent, examinez l'entrée du détecteur et les traces de réduction de gain pour en attribuer le mécanisme. Une différence ne prouve pas qu'un ordre est plus naturel. Un EQ neutre ou un compresseur qui ne franchit jamais son seuil peut donner utilement un résultat nul. Prétendre qu'un ordre préserve mieux l'attaque demanderait une mesure d'attaque définie, une direction, une tolérance acceptable et un contrôle d'écoute si la perception entre dans la conclusion.

### Exercice pratique 4 : garder le fixture valide

Un dispositif proposé traite le WAV enregistré de `0.0–1.0 s`, le compare au rendu dans le même intervalle de temps du fichier et conclut que EQ→Comp a mieux préservé l'attaque. Donnez deux problèmes indépendants.

> **Réponse :** La première attaque enregistrée n'arrive que vers `1.1 s` : son intervalle `0.0–1.0 s` se situe surtout avant l'attaque, tandis que le rendu commence à zéro. Les fenêtres ne sont pas alignées sur l'attaque. De plus, comparer deux fichiers sources différents n'isole pas l'ordre du traitement : A et B doivent utiliser le **même WAV source**. Aucun des deux fichiers n'est un étalon de réalisme validé.

### Exercice pratique 5 : choisir la vérification suivante

Une future exécution trouve un écart de `0.2 dB` dans le RMS de la première attaque entre A et B, mais les sorties ne sont pas alignées et le manifeste des réglages du compresseur manque. Cela justifie-t-il un ordre préféré ? Quelles preuves faut-il demander ?

> **Réponse :** Non. Préservez d'abord le hachage de l'entrée et la fenêtre ; publiez la version et les réglages du compresseur ; vérifiez les réinitialisations indépendantes, alignez la latence et l'attaque, confirmez les mêmes coefficients EQ et l'absence d'écrêtage. Relancez ensuite et comparez mesures brutes et traces de réduction de gain. Pour une conclusion sonore, ajustez le niveau après traitement lors d'un contrôle d'écoute séparé et à l'aveugle. `0.2 dB` seul n'identifie pas l'étape responsable et ne démontre aucune préférence.

## Preuves et limites

- Le [README du fixture GAS-001](../../../fixtures/guitar-acoustics/gas-001/README.md) documente les fichiers E2 enregistré et rendu nativement, leurs hachages, l'attribution, les attaques approximatives et les limites des mesures. La [leçon GAS-001](../../guitar-acoustics/en/gas-001-open-string-audio-evidence.md) et ses mesures sauvegardées concernent la comparaison *brute*, pas un essai d'EQ et de compression.
- Le [routage navigateur GA](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/audioEngine.js) et son [worklet](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Rust/guitar-web-wasm-demo/src/audio/guitar-worklet.js), ainsi que le [FIR IX](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/filter.rs), établissent un chemin de signal et un filtre disponibles. Ils n'établissent ni compresseur implémenté, ni essai d'ordre EQ-compresseur, ni résultat de WAV traité.
- Le calcul à quatre échantillons est synthétique. Le dispositif A/B, ses seuils et ses mesures sont proposés. Aucun compresseur n'a été construit ou exécuté pour cette leçon ; il n'existe ici ni WAV de guitare traité, ni verdict d'écoute à l'aveugle, ni décision de routage de production. Révisions disciplinaire et pédagogique, traduction, synchronisation et compilation Learn, et lecture publique anonyme restent en attente. Le cycle de recherche du 2026-03-23 demeure un artefact vocal historique ; cette révision utilise le nouveau cycle indiqué en frontmatter.
