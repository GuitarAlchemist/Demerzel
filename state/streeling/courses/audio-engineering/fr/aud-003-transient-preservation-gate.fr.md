---
module_id: aud-003-transient-preservation-gate
department: audio-engineering
course: "Préserver l'attaque d'une corde de guitare pendant une analyse spectrale hors ligne"
level: intermediate
prerequisites: [aud-002-level-matched-guitar-comparison, phy-002-time-frequency-guitar-transients]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: audio-engineering-2026-10-11-003
version: "0.1.0"
---

# Préserver l'attaque d'une corde de guitare pendant une analyse spectrale hors ligne

> **Département d'ingénierie audio** | Niveau : intermédiaire | Durée estimée : 35 minutes | Statut : brouillon français ; révision et publication en attente

## Objectifs

À la fin de cette leçon, vous pourrez :

- choisir une FFT sur un intervalle complet ou une STFT selon la décision à prendre sur le signal audio ;
- régler une taille de fenêtre et un pas de STFT valides dans IX, tout en conservant l'attaque dans au moins une trame ;
- distinguer le débruiteur Haar d'IX des analyses par ondelettes ciblées en fréquence de la fixture GAS-001 ;
- rejeter une réduction de bruit qui modifie une attaque de guitare au-delà d'un seuil annoncé ;
- définir une évaluation hors ligne qu'un autre ingénieur pourrait réfuter avec les mêmes fichiers WAV.

## La décision à prendre pour le projet

La [fixture GAS-001 de la corde de mi grave à vide](../../../fixtures/guitar-acoustics/gas-001/README.md), figée au commit Demerzel [`5c496745`](https://github.com/GuitarAlchemist/Demerzel/tree/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001), contient un enregistrement sous licence de E2 à vide et un rendu du moteur natif de GA. Ce sont deux WAV mono de quatre secondes à 44 100 Hz. La première attaque de l'enregistrement se situe environ 1,1 seconde après le début du fichier ; le rendu commence à zéro. La fixture consigne une attaque ultérieure vers 2,75 secondes dans l'enregistrement. Cette paire sert à l'enseignement ; ce n'est ni un banc d'essai validé du réalisme ni une capture de l'AudioWorklet du navigateur.

[PHY-002](../../physics/en/phy-002-time-frequency-guitar-transients.md) explique le compromis temps-fréquence et interprète les mesures FFT et par ondelettes de type Morlet enregistrées dans la fixture. [AUD-002](../en/aud-002-level-matched-guitar-comparison.md) contrôle l'alignement des attaques et le niveau d'écoute avant toute comparaison auditive. Cette leçon traite d'un autre choix d'ingénierie : **faut-il débruiter la référence enregistrée avant d'utiliser son attaque pour juger un rendu GA ?** Une baisse apparente du bruit ne suffit pas. Le débruiteur peut aussi émousser, étaler ou déplacer l'attaque qu'on voulait préserver.

Le cas d'implémentation est figé au commit IX [`bd1336b7`](https://github.com/GuitarAlchemist/ix/tree/bd1336b7c4045e427dcdbe80b102790e45da5ce1). IX expose un [handler FFT](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1297-L1315), un [handler de spectrogramme](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L1143-L1189) et un [handler de débruitage par ondelettes Haar](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/handlers.rs#L759-L797). Ils acceptent des tableaux numériques d'échantillons, pas des chemins vers des fichiers WAV. Il faudrait un décodeur WAV et un banc d'essai hors ligne reproductible pour les appliquer à cette paire audio ; cette leçon n'a pas effectué cet essai.

## 1. Choisir la vue selon l'affirmation à vérifier

La fonction [`rfft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/fft.rs#L84-L115) d'IX transforme un tableau fini d'échantillons réels ; elle complète de zéros une longueur qui n'est pas une puissance de deux jusqu'à la puissance de deux suivante. Malgré son nom, elle renvoie le tableau FFT complet. Le handler `ix_fft` renvoie des amplitudes et des fréquences en **cycles par échantillon**, avec une fréquence d'échantillonnage supposée de 1,0. À 44 100 échantillons par seconde, multipliez par 44 100 une fréquence normalisée **jusqu'à Nyquist** pour l'exprimer en hertz ; la moitié supérieure reflète les fréquences négatives. Le spectre d'amplitude du fichier entier est valable pour un signal changeant, mais il ne précise pas quelle attaque a produit un pic. Une FFT limitée à la première note aide à résumer localement ses harmoniques, mais elle moyenne tout de même l'intervalle choisi.

La fonction [`stft`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L6-L30) d'IX répète des FFT fenêtrées à des positions successives. La fonction [`spectrogram`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L32-L54) utilise une fenêtre de Hann et conserve les amplitudes d'un seul côté du spectre. Elle permet de voir si l'énergie liée à l'attaque apparaît dans une trame précoce et comment elle évolue. Avec `db=true`, elle calcule `20 log10(max(magnitude, 1e-10))` ; il ne s'agit pas d'une mesure dBFS étalonnée. Ne comparez pas directement ces valeurs brutes en dB aux valeurs RMS en dBFS de GAS-001.

### Exercice pratique 1 : choisir une sortie capable de répondre

Un analyste calcule `ix_fft` sur les quatre secondes du WAV enregistré et affirme qu'un pic aigu appartient à la *première* attaque, et non à l'attaque ultérieure. Quelle partie du résultat est utile et que faut-il calculer avant d'attribuer le pic à un événement ?

> **Réponse :** La FFT du fichier entier peut montrer que le fichier contient de l'énergie près de cette fréquence, après conversion des cycles par échantillon en hertz. Ses amplitudes n'ont aucun repère temporel : elles ne permettent donc pas d'attribuer le pic à la première attaque. Décodez le WAV, marquez la première attaque approximative, calculez séparément un intervalle annoncé pour la première note et examinez une STFT alignée sur les attaques si leur chronologie importe. Conservez le fichier brut et les intervalles d'analyse dans le compte rendu.

## 2. Adapter les réglages STFT d'IX à la question de l'attaque

Le **handler de l'agent** IX exige que `window_size` soit une puissance de deux, au moins égale à deux et au plus égale à la longueur du signal. Cette contrainte importe : sinon, la FFT sous-jacente complète une trame de zéros et le nombre de bins ainsi que la correspondance des fréquences annoncés par le handler seraient erronés. Le handler fixe par défaut `hop_size` à la moitié de la fenêtre, ramène un pas fourni de zéro à un et indique `n_frames` et `n_bins`. La fonction centrale `stft` ne fournit pas ces garde-fous ; un banc d'essai qui l'appelle directement doit valider ses propres paramètres. Elle ne traite que les trames complètes et ne prolonge donc pas discrètement une fin de signal trop courte.

Pour une vue **proposée** de la première attaque à 44,1 kHz, choisissez une fenêtre de 2 048 échantillons et un pas de 512 échantillons. La fenêtre couvre environ **46,44 ms**, le pas environ **11,61 ms**, et la grille FFT offre `44,100 / 2,048 ≈ 21.53 Hz` par bin ; le spectre d'amplitude unilatéral comporte **1 025 bins**. Cette grille est trop grossière pour trancher avec une seule trame un désaccord d'un hertz sur la hauteur. Une fenêtre de 8 192 échantillons couvre environ 185,76 ms et espace les bins de 5,38 Hz, mais mélange davantage l'attaque et la décroissance. Réduire le pas crée plus de trames chevauchantes ; cela n'améliore pas la discrimination fréquentielle de chaque trame. Ce sont des calculs issus des réglages, **pas** des sorties IX mesurées sur les WAV.

### Exercice pratique 2 : préciser une requête IX valide

À 44 100 Hz, calculez la durée de la fenêtre, l'intervalle entre trames et l'espacement nominal des bins pour `window_size=2048` et `hop_size=512`. Combien de bins le handler de spectrogramme d'IX doit-il annoncer ? Pourquoi rejetterait-il `window_size=2205`, soit exactement 50 ms ?

> **Réponse :** La fenêtre dure `2048/44100 ≈ 46.44 ms`, le pas `512/44100 ≈ 11.61 ms` et l'espacement vaut `44100/2048 ≈ 21.53 Hz`. Le handler annonce `2048/2 + 1 = 1025` bins. Il rejette 2 205 parce que ce nombre n'est pas une puissance de deux. Un appel direct à la fonction centrale pourrait compléter la trame de zéros, mais interpréter les bins comme si la longueur FFT était 2 205 serait erroné.

Une fenêtre de Hann s'annule à ses extrémités. Elle atténue les discontinuités aux bords, mais une attaque exactement placée à une extrémité peut disparaître de cette trame. Grâce au chevauchement, le même échantillon se retrouve ailleurs dans une autre trame. Il s'agit du **placement de l'analyse**, pas d'une création d'information par chevauchement. La [fonction de fenêtrage](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/window.rs#L10-L15) et la [boucle sur les trames](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/spectral.rs#L14-L29) d'IX permettent de vérifier cet effet de bord sans enregistrement de guitare.

### Exercice pratique 3 : rendre visible une impulsion située au bord

Prenez un tableau synthétique de 64 échantillons, nul partout sauf à l'indice 16 où il vaut 1. IX utilise une fenêtre de Hann de 16 échantillons. Avec un pas de 16, quelle trame complète contient l'impulsion et que lui arrive-t-il ? Qu'est-ce qui change avec un pas de 8 ?

> **Réponse :** Avec un pas de 16, les trames commencent aux indices 0, 16, 32 et 48. Seule celle qui commence à 16 contient l'indice 16 ; l'impulsion occupe l'offset 0 de la fenêtre, où le poids de Hann est nul. Tous les spectres renvoyés peuvent donc manquer cette impulsion isolée. Avec un pas de 8, la trame qui commence à 8 la contient aussi à l'offset 8, dont le poids de Hann est d'environ 0,989 : cette trame montre de l'énergie. C'est un calcul synthétique dérivé du code source, pas une mesure IX sur un WAV. Il montre pourquoi le pas proposé de 512 échantillons doit être vérifié près des limites des attaques réelles.

## 3. Un débruiteur Haar peut modifier la preuve

La fonction [`haar_forward`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L5-L18) d'IX forme des moyennes et des différences par paires. [`wavelet_denoise`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-signal/src/wavelet.rs#L60-L82) applique un seuillage souple aux coefficients de détail, puis reconstruit le signal. C'est un traitement discret de Haar, **pas** l'analyse par ondelettes complexes de type Morlet centrée sur des fréquences, enregistrée dans GAS-001. Les deux méthodes produisent des sorties différentes et répondent à des questions différentes. Un coefficient de détail Haar peut signaler un changement rapide, mais le seuiller peut supprimer une partie d'une vraie attaque en même temps que le bruit.

Le handler IX exige `levels >= 1`, un seuil fini et non négatif, ainsi qu'une longueur d'entrée divisible par `2^levels`. Il rejette sinon la requête, car la transformée de Haar centrale peut perdre les derniers échantillons impairs. Son [test de bruit](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1387-L1411) versionné utilise une rampe lisse avec un bruit alternatif ajouté et vérifie une erreur quadratique moyenne plus faible. Il ne vérifie pas la préservation d'une attaque de guitare isolée. Les [tests des garde-fous](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-agent/src/skills/batch1.rs#L1525-L1543) distincts couvrent une taille de spectrogramme invalide et une entrée d'ondelettes de longueur indivisible.

### Exercice pratique 4 : prédire la modification de l'attaque

Pour le signal synthétique de huit échantillons `[0, 1, 0, 0, 0, 0, 0, 0]`, appliquez les équations de Haar d'IX sur un niveau avec un seuil souple de 1. Quels sont les deux premiers échantillons reconstruits ? Cela appuie-t-il l'affirmation selon laquelle le débruitage par ondelettes préserve toujours le pic d'une attaque ?

> **Réponse :** La première paire a pour approximation `1/sqrt(2)` et pour détail `-1/sqrt(2)`. Comme la valeur absolue du détail est inférieure au seuil 1, le seuillage souple le ramène à zéro. La transformée inverse donne `[0.5, 0.5]` pour la première paire ; les autres restent à zéro. Le pic isolé passe de 1 à 0,5 et s'étale un échantillon plus tôt. Ce calcul réfute une préservation inconditionnelle ; il ne prédit pas le seuil adapté à un WAV de guitare enregistré.

## 4. Déclarer à l'avance un critère de préservation hors ligne

Voici un **protocole d'évaluation proposé**, et non un essai réalisé ou une norme d'acceptation GA. Conservez les deux WAV de la fixture ainsi que leurs empreintes complètes. Décodez chacun en échantillons mono `f64` normalisés, sans écraser l'original. Consignez le décodeur, la fréquence d'échantillonnage, le nombre d'échantillons et tout rééchantillonnage ; rejetez tout changement de fréquence silencieux. Utilisez les repères approximatifs d'attaque de la fixture (enregistrement à 1,1 s, rendu à 0,0 s) et examinez séparément les extraits de la première note et l'attaque ultérieure enregistrée. Gardez une branche brute et une branche de copie traitée aux mêmes positions et au même gain. Appliquez la vue STFT d'IX aux deux branches avec les réglages annoncés de 2 048/512 ; étiquetez les trames par leur **échantillon de départ et la durée de la fenêtre**, pas seulement par le centre visuel d'une colonne. Notez si la conclusion sur une attaque en bord de trame résiste à un autre pas ou à un léger déplacement du repère d'attaque.

Avant tout essai Haar, annoncez `levels` et le seuil, vérifiez que la longueur exacte de l'entrée est divisible par `2^levels` et consignez la politique de remplissage ou de découpe si nécessaire. Par exemple, un extrait d'une seconde à 44 100 échantillons n'est **pas** divisible par huit pour trois niveaux : le reste est quatre. Ajouter quatre zéros pour atteindre 44 104 est une option à déclarer ; elle crée une limite qui peut affecter les coefficients voisins. Modifier la limite de l'extrait ou réduire le nombre de niveaux est une autre option. N'appelez pas directement la fonction centrale sur une entrée de longueur impaire en supposant que sa sortie reste alignée.

Pour la référence enregistrée, mesurez un intervalle de bruit avant l'attaque et un intervalle fixe de la première attaque, tous deux annoncés, sur les copies brute et traitée. Un **critère pédagogique**, choisi avant de voir le résultat, pourrait exiger une baisse d'au moins **3 dB** du RMS avant l'attaque, tout en conservant la valeur absolue du pic de la première attaque à **10 %** près de la valeur brute et la position temporelle de ce pic à **1 ms** près. Exigez l'absence d'écrêtage et un nombre d'échantillons inchangé après toute découpe documentée. Revérifiez avec des repères d'attaque décalés de ±5 ms et consignez tous les seuils candidats, y compris les échecs. Le rendu GA commence au temps zéro du fichier et n'a donc pas d'intervalle de bruit équivalent avant l'attaque : ne lui appliquez pas ce critère de bruit. Conservez l'enregistrement non traité comme référence principale. Réussir ces critères de forme d'onde autoriserait une comparaison d'écoute distincte, documentée et à niveau égal ; cela ne **prouverait pas** que le fichier traité est perceptuellement inchangé ou que GA sonne de façon réaliste.

### Première vérification sur le WAV enregistré

Une [vérification Haar circonscrite avec IX](../../../reviews/aud-003-ix-probe-2026-10-11.md) a maintenant été effectuée sur `8,192` échantillons de l'enregistrement GAS-001, à partir de l'échantillon `46,966`. L'intervalle de 35 ms avant l'attaque approximative à 1,1 s indiquée par la fixture n'est qu'un indicateur **provisoire** du bruit ; la fenêtre d'attaque couvre 1,1–1,25 s. Avec trois niveaux Haar, les seuils `0.002`, `0.004` et `0.008` ont réduit le RMS de cet intervalle provisoire de seulement `0.0942`, `0.0968` et `0.0968` dB. Les pics d'attaque ont conservé respectivement `96.97%`, `94.83%` et `90.54%` du pic brut, sans décalage mesuré de l'échantillon du pic. Chaque traitement a rendu le nombre initial d'échantillons sans écrêtage. Aucun n'a atteint la cible illustrative de 3 dB de réduction du bruit : aucun ne passe donc ce critère indirect. Ce seul court extrait ne valide ni la segmentation des attaques, ni le critère sur le fichier entier, ni la correspondance du binaire IX utilisé avec le commit source cité, ni l'équivalence perceptive. Conservez l'enregistrement brut comme référence.

### Exercice pratique 5 : appliquer le critère, puis préciser sa limite

Un ingénieur propose un traitement Haar à trois niveaux sur un extrait enregistré de 44 100 échantillons, sans remplissage. Il présente aussi un candidat *hypothétique* dont le RMS avant l'attaque est inférieur de 4 dB, le pic d'attaque vaut 0,82 fois le pic brut et le déplacement temporel du pic est de 0,2 ms. Que faut-il modifier pour que le handler IX accepte l'extrait ? Ce candidat passe-t-il le critère pédagogique ?

> **Réponse :** `44,100 mod 8 = 4` ; le handler rejette donc trois niveaux sur cette longueur. Déclarez l'ajout de quatre échantillons pour atteindre 44 104 et une politique de découpe, choisissez un autre extrait ou réduisez le nombre de niveaux. Le candidat hypothétique échoue même si le bruit baisse de plus de 3 dB et si le décalage reste inférieur à 1 ms : `1 - 0.82 = 0.18`, soit une perte de pic de 18 %, au-delà de la limite annoncée de 10 %. Ce rejet porte sur la préservation de l'attaque selon ce critère indirect ; ce n'est ni un résultat mesuré sur l'un des WAV de la fixture ni un verdict d'écoute.

## Sources et limites

- Les fichiers audio du projet et leur provenance viennent de la [fixture GAS-001 au commit Demerzel `5c496745`](https://github.com/GuitarAlchemist/Demerzel/blob/5c4967454ddc740ed937c87719ca4d71a3522e4b/state/streeling/fixtures/guitar-acoustics/gas-001/README.md). L'enregistrement et le rendu natif de GA proviennent de sources distinctes, avec des chaînes d'interprétation et de production différentes. Leurs résultats FFT et Morlet enregistrés sont des observations de cette fixture, pas des sorties d'IX.
- La STFT, la FFT, les équations de Haar, les garde-fous des handlers et les tests cités plus haut sont des observations du code source IX à `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Les dimensions 2 048/512, l'exemple de l'impulsion au bord de Hann, le résultat Haar à huit échantillons et le calcul de divisibilité sont des **exemples dérivés**. Une vérification locale ultérieure via IX MCP a mesuré un seul extrait d'échantillons du WAV enregistré ; aucun spectrogramme IX, fichier WAV traité ou examen de l'enregistrement entier n'a été produit. La correspondance du binaire MCP utilisé avec le commit source n'a pas été attestée indépendamment.
- Une amplitude d'analyse n'est pas un score étalonné de sonie ou de réalisme. Les repères d'attaque sont approximatifs ; les fenêtres spectrales, le remplissage, les seuils, le décodeur et le gain d'entrée peuvent modifier le résultat. Une impulsion synthétique révèle un mode de défaillance possible, sans prédire le comportement de toutes les attaques.
- La révision du sujet, les essais par les apprenants, la révision linguistique par une personne de langue maternelle, la synchronisation et la compilation de Learn, ainsi que la vérification publique restent à faire. Ce texte français est un brouillon, pas un cours publié.
