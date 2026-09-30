---
module_id: mat-021-fourier-analysis-signals
department: mathematics
course: Analyse de Fourier et signaux
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Analyse de Fourier et signaux — Ce que montre un spectre, et ce que cache l'échantillonnage

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Écrire la transformée de Fourier discrète comme un changement de base, l'inverser, et vérifier un spectre avec le théorème de Parseval
- Obtenir la transformée de Fourier rapide en base 2, compter ses opérations, et dire pourquoi la façon de calculer ses facteurs de rotation compte
- Prédire où apparaît une sinusoïde échantillonnée, et dire ce qu'un décimateur doit faire avant de jeter des échantillons
- Expliquer la fuite spectrale, choisir une fenêtre, et distinguer la grille de fréquences de la résolution en fréquence
- Utiliser le théorème de convolution, et lire la transformée de Fourier à court terme et la transformée de Haar comme deux réponses au compromis temps–fréquence
- Retracer ce que garantissent `fft`, `ix_fft`, `welch_psd`, les filtres, le rééchantillonnage et le débruitage de Haar d'IX, et où le schéma, les contrats et les invariants promettent plus que ce que le code tient

---

## 1. La TFD comme changement de base

Échantillonnez un signal N fois et vous obtenez un vecteur x de ℂᴺ. La **transformée de Fourier discrète** (TFD) l'écrit dans la base des exponentielles complexes échantillonnées f_k, de coefficients e^(2πikn/N) : X_k = Σ_n x_n e^(−2πikn/N), pour k = 0, …, N − 1. Deux de ces vecteurs sont orthogonaux, puisque ⟨f_j, f_k⟩ = Σ_n e^(2πi(k−j)n/N) est une somme géométrique qui s'annule sauf si j = k, où elle vaut N. La matrice F de coefficients e^(−2πikn/N) vérifie donc F F* = N I, si bien que F/√N est unitaire, un changement de base qui préserve les longueurs au sens de MAT-004. L'inverse est x_n = (1/N) Σ_k X_k e^(2πikn/N), et le **théorème de Parseval**, Σ|x_n|² = (1/N) Σ|X_k|², est cette préservation des longueurs écrite en toutes lettres.

L'indice k compte des cycles par N échantillons : la case k est la fréquence k/N cycle par échantillon, ou k·fs/N à une fréquence d'échantillonnage fs. Pour un signal réel, X_(N−k) est le conjugué de X_k, donc les cases N/2 + 1 à N − 1 répètent les cases N/2 − 1 à 1 : dans cette plage, la case k est la fréquence négative (k − N)/N, pas une fréquence au-dessus d'un demi, et dans une TFD à 8 points la case 5 est la fréquence −3/8, miroir de la case 3. Un cosinus d'amplitude 1 sur la grille, x_n = cos(2π·3n/8), a X_3 = X_5 = 4 et toutes les autres cases nulles, et Parseval se vérifie : Σ x_n² = 4 et (4² + 4²)/8 = 4.

### Exercice pratique

Calculez la TFD de x = (1, 2, 3, 4) et vérifiez le théorème de Parseval.

> *Solution :* Avec N = 4, e^(−2πik/4) = (−i)ᵏ. X_0 = 1 + 2 + 3 + 4 = 10, X_1 = 1 − 2i − 3 + 4i = −2 + 2i, X_2 = 1 − 2 + 3 − 4 = −2, et X_3 est le conjugué de X_1, −2 − 2i. Alors Σ|X_k|² = 100 + 8 + 4 + 8 = 120, et 120/4 = 30 = 1 + 4 + 9 + 16.

---

## 2. La transformée de Fourier rapide

Évaluer directement chaque X_k coûte N² multiplications complexes. Cooley et Tukey (1965), qui redécouvraient une idée que Gauss avait utilisée vers 1805 (Heideman, Johnson et Burrus 1984), séparent la somme entre échantillons pairs et impairs. Avec E et O les TFD de longueur N/2 de x_0, x_2, … et de x_1, x_3, …, et w = e^(−2πi/N),

X_k = E_k + wᵏ O_k,  X_(k+N/2) = E_k − wᵏ O_k,  pour k < N/2,

un **papillon** qui utilise chaque produit deux fois. Quand N est une puissance de deux, la séparation se répète log₂ N fois, pour (N/2) log₂ N multiplications : 5120 pour N = 1024, contre N² = 2^20. Lire l'entrée dans l'ordre des indices à bits inversés permet à chaque étage d'écraser le tableau sur place.

Les facteurs wᵏ sont les **facteurs de rotation**, et leur mode de calcul décide de la précision. Si chaque facteur est exact à un ulp près (une unité sur le dernier chiffre), l'erreur relative de toute la FFT ne croît que comme log₂ N fois l'unité d'arrondi (Higham 2002). Les calculer par multiplications répétées, wᵏ = wᵏ⁻¹ · w, reporte l'arrondi de chaque produit sur le suivant, si bien que l'erreur d'un facteur croît à peu près en proportion de son indice (Van Loan 1992) ; une table, ou un appel direct à cos et sin pour chaque facteur, l'évite.

Une FFT en base 2 exige que N soit une puissance de deux, et une commodité répandue consiste à ajouter des zéros jusqu'à en obtenir une. Le résultat n'est pas la TFD des échantillons d'origine : il échantillonne le même spectre sous-jacent Σ_n x_n e^(−2πifn) sur la grille f = k/N′ de la longueur complétée N′. Les six échantillons de cos(2πn/6) ont X_1 = X_5 = 3 sur leur propre grille de sixièmes ; complétés à 8, la grille des huitièmes manque 1/6, et le pic s'étale sur les cases 1/8 et 1/4 (§6).

### Exercice pratique

Montrez que X_(k+N/2) = E_k − wᵏ O_k.

> *Solution :* E et O sont des TFD de longueur N/2, donc E_(k+N/2) = E_k et O_(k+N/2) = O_k. La somme complète est X_k = E_k + wᵏ O_k pour tout k, et w^(k+N/2) = wᵏ · w^(N/2) = wᵏ · e^(−πi) = −wᵏ. Remplacer k par k + N/2 donne X_(k+N/2) = E_k − wᵏ O_k.

---

## 3. Échantillonnage et repliement

Échantillonner un signal continu à la cadence fs garde les valeurs x(n/fs). Les sinusoïdes e^(2πift) et e^(2πi(f + m·fs)t) coïncident en chaque échantillon pour tout entier m, et un cosinus réel à f coïncide aussi avec un cosinus à m·fs − f. Une sinusoïde échantillonnée n'est donc connue qu'à ces **alias** près, et elle apparaît à celui qui se trouve entre 0 et la **fréquence de Nyquist** fs/2 : en |f − m·fs| pour l'entier m qui le rend minimal. Le théorème de Nyquist–Shannon retourne la situation (Nyquist 1928 ; Shannon 1949) : un signal sans contenu à fs/2 ou au-dessus est déterminé par ses échantillons, et x(t) = Σ_n x_n sinc(fs·t − n), avec sinc(u) = sin(πu)/(πu).

La **décimation** par M garde un échantillon sur M, ce qui abaisse la cadence à fs/M et la fréquence de Nyquist à fs/(2M). Tout ce qui se trouve entre fs/(2M) et fs/2 se replie alors, donc un décimateur l'élimine d'abord avec un filtre passe-bas. À 8 kHz, une sinusoïde de 3 kHz décimée par 2 sans ce filtre est échantillonnée à 4 kHz et apparaît à |3 − 4| = 1 kHz : 3/8 de l'ancienne cadence devient 1/4 de la nouvelle.

La somme de sinus cardinaux a une infinité de termes, et la tronquer a un coût. À mi-chemin entre deux échantillons, les 16 termes les plus proches pour un signal constant ont pour somme (4/π)(1 − 1/3 + 1/5 − … − 1/15) ≈ 0,9604, une somme partielle de la série de Leibniz pour π/4, si bien qu'un interpolateur qui garde 8 coefficients de chaque côté et aucune fenêtre y lit une constante 5 comme environ 4,80. Les interpolateurs pratiques atténuent le noyau avec une fenêtre, et certains divisent par la somme des poids pour qu'une constante reste constante.

### Exercice pratique

Un enregistreur échantillonne à 8 kHz. À quelle fréquence apparaît une sinusoïde de 5 kHz, et une de 13 kHz ?

> *Solution :* La fréquence de Nyquist est 4 kHz. La sinusoïde de 5 kHz apparaît à |5 − 8| = 3 kHz, et celle de 13 kHz à |13 − 16| = 3 kHz aussi : après l'échantillonnage, les trois sinusoïdes sont indiscernables. Seul un filtre passe-bas placé avant l'échantillonneur peut l'empêcher.

---

## 4. Fuite spectrale, fenêtres et résolution

Une sinusoïde dont la fréquence tombe sur la grille, f = k/N, met toute son énergie dans ses deux cases. Hors de la grille, l'enregistrement fini agit comme une fenêtre rectangulaire : le spectre de L échantillons de e^(2πif₀n) est le noyau de Dirichlet Σ_(n<L) e^(2πi(f₀ − f)n), dont le module |sin(πL(f − f₀))/sin(π(f − f₀))| a un lobe principal de largeur 2/L entre ses premiers zéros et des lobes secondaires qui décroissent lentement, et chaque case de la TFD l'échantillonne. C'est la **fuite spectrale** : une sinusoïde forte relève toutes les cases, et peut en masquer une faible.

Multiplier les échantillons par une **fenêtre** qui s'amincit vers zéro aux bords abaisse les lobes secondaires au prix d'un lobe principal plus large (Harris 1978). Calculé sur des versions de 256 échantillons, le plus haut lobe secondaire est à environ −13 dB pour le rectangle, −31 dB pour Hann, −43 dB pour Hamming et −58 dB pour Blackman, et le lobe principal de Hann est deux fois plus large que celui du rectangle. Une fenêtre change aussi la hauteur du pic : Hann divise à peu près par deux l'amplitude d'une sinusoïde au centre d'une case, ce qu'un spectre étalonné compense.

Deux grandeurs de même unité se confondent facilement. Le pas de la **grille** d'une FFT à N points est fs/N, et le bourrage de zéros le rend aussi fin qu'on veut. La **résolution**, le plus petit écart auquel deux sinusoïdes donnent deux pics, est fixée par la longueur L de l'enregistrement, environ fs/L, et le bourrage ne peut pas l'améliorer. Des sinusoïdes à 0,20 et 0,21 cycle par échantillon, longues de 32 échantillons et complétées à 1024, montrent un seul pic, à 0,2051 ; 128 échantillons complétés aux mêmes 1024 en montrent deux, à 0,1992 et 0,2100 (en comptant les maxima locaux au-dessus de 30 % du plus grand module entre 0,1 et 0,3).

### Exercice pratique

Un enregistrement de 32 échantillons à 1 kHz contient des sinusoïdes à 200 Hz et 210 Hz. Le compléter par des zéros jusqu'à 1024 points les séparera-t-il ?

> *Solution :* Non. La résolution est d'environ fs/L = 1000/32 ≈ 31 Hz, trois fois l'écart de 10 Hz, donc les deux lobes principaux fusionnent en un seul. Le bourrage échantillonne ce lobe fusionné sur une grille plus fine et montre toujours un seul pic. Les séparer demande un enregistrement de plus d'une centaine d'échantillons, un dixième de seconde ; 128 échantillons montrent deux pics.

---

## 5. Convolution, TFCT et ondelettes de Haar

Le **théorème de convolution** change le filtrage en multiplication : la TFD de la convolution circulaire (x ⊛ h)_n = Σ_m x_m h_((n−m) mod N) est X_k H_k. Une convolution linéaire de longueurs L et M replie sa queue sur sa tête à moins que les deux signaux soient complétés à au moins L + M − 1 avant les transformées ; la FFT la calcule alors en O(N log N) opérations au lieu de O(LM).

Un filtre RIF convolue avec un h fini, donc sa réponse en fréquence est H(f) = Σ_k h_k e^(−2πifk). Le passe-bas à sinus cardinal fenêtré d'ordre M prend h_k = 2f_c sinc(2f_c(k − M/2)) w_k pour k = 0, …, M, symétrique autour de M/2, donc H(f) = e^(−iπfM) A(f) avec A réel, proche de 1 sous la fréquence de coupure f_c et proche de 0 au-dessus. L'**inversion spectrale**, δ_(k−M/2) − h_k, le change en passe-haut, ce qui exige un coefficient central : M doit être pair (voir l'exercice du §6).

La **transformée de Fourier à court terme** (TFCT) fait glisser une fenêtre de L échantillons le long du signal par pas de H et calcule une FFT par trame. Chaque trame a L/2 + 1 cases utiles espacées de fs/L et couvre L/fs secondes, donc une fenêtre plus longue affine la fréquence et brouille le temps, et aucun choix de L n'améliore les deux : le produit des deux résolutions est minoré (Gabor 1946). La méthode de Welch moyenne les carrés des modules de trames fenêtrées qui se chevauchent pour réduire la variance d'une estimation de spectre (Welch 1967). Normalisée en densité, une estimation unilatérale double chaque case sauf 0 et L/2, parce que la puissance d'un signal réel se partage également entre f et −f ; l'intégrale de la densité est alors la puissance du signal.

La **transformée de Haar** prend l'autre route de l'analyse temps–fréquence. Elle envoie chaque paire d'échantillons sur une somme et une différence normalisées, a_i = (x_(2i) + x_(2i+1))/√2 et d_i = (x_(2i) − x_(2i+1))/√2, puis recommence sur les sommes : après L niveaux, les détails décrivent les variations aux échelles 2, 4, …, 2ᴸ, chacune localisée dans le temps (Haar 1910 ; Mallat 1989). La transformée est orthonormée, donc elle préserve l'énergie. Le seuillage doux remplace chaque détail d par sign(d) max(|d| − t, 0), ce qui supprime les petites fluctuations et réduit les grandes (Donoho 1995), et quand la longueur est un multiple de 2ᴸ il n'augmente jamais la variance (voir l'exercice).

### Exercice pratique

Montrez que le seuillage doux des détails d'une transformée de Haar n'augmente jamais la variance d'un signal dont la longueur est un multiple de 2ᴸ.

> *Solution :* La transformée est orthonormée, donc l'énergie Σ x_n² est égale à la somme des carrés des approximations finales et de tous les détails ; le seuillage réduit chaque |d| et laisse les approximations intactes, donc l'énergie ne peut pas croître. À chaque niveau, la synthèse change a_i et d_i en (a_i + d_i)/√2 et (a_i − d_i)/√2, dont la somme √2·a_i ne fait pas intervenir d_i, donc la somme du signal, et avec elle la moyenne, ne dépend que des approximations finales et ne change pas. La variance est l'énergie divisée par n moins le carré de la moyenne : le premier terme ne peut pas croître et le second est fixé.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne en Python de `fft.rs`, `spectral.rs`, `sampling.rs`, `filter.rs` et `wavelet.rs` dans `crates/ix-signal`, des gestionnaires ci-dessous, de la fonction DuckDB `ix_wavelet_denoise` et de `analyze_metric_spectrum`, vérifiée sur la FFT de NumPy. Ces nombres sont des prédictions, et le §7 propose de les vérifier.

**La transformée et son outil.** [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L86) ajoute des zéros jusqu'à [la puissance de deux suivante](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L87) et exécute une transformée en base 2 dont les étages calculent leurs facteurs de rotation ainsi :

```rust
        let w_base = Complex::new(angle.cos(), angle.sin());

        for start in (0..n).step_by(len) {
            let mut w = Complex::new(1.0, 0.0);
            for k in 0..half {
                let even = data[start + k];
                let odd = data[start + k + half] * w;
                data[start + k] = even + odd;
                data[start + k + half] = even - odd;
                w = w * w_base;
            }
        }
```

L'outil MCP `ix_fft` appelle [`fft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1299), qui exécute :

```rust
    let spectrum = ix_signal::fft::rfft(&signal);
    let magnitudes = ix_signal::fft::magnitude_spectrum(&spectrum);
    let n = spectrum.len();
    // Frequency bins assuming sample_rate=1.0 (normalized)
    let frequencies: Vec<f64> = (0..n).map(|k| k as f64 / n as f64).collect();
```

- **`ix_fft` ignore le paramètre `inverse` qu'il annonce.** Son schéma propose [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L74), décrit comme [« If true, compute the inverse FFT »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L77), et demande un signal dont [la longueur doit être une puissance de 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L71). Le gestionnaire ne lit jamais l'indicateur, complète silencieusement les autres longueurs et rapporte la longueur complétée comme `fft_size`. Il ne renvoie que les modules, et étiquette la case k par k/n pour tout k, donc pour cos(2π·3n/8) il rapporte un module 4 à 0,375 et encore à 0,625, qui est la fréquence négative −0,375 et non une deuxième sinusoïde. Avec `inverse` à vrai, la sortie est la même.
- **Le bourrage change la grille sans avertissement.** Les contrats de la bibliothèque [disent qu'elle complète](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L8). Les six échantillons de cos(2πn/6) reviennent sous forme de huit cases, avec 2,5156 à 1/8 et 2,2361 à 1/4, là où la TFD à six points a 3 à 1/6. Le guide d'IX donne la résolution en fréquence comme la fréquence d'échantillonnage divisée par la taille N de la FFT, et dit que [« Larger N = finer frequency resolution »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/docs/signal-processing/fft-intuition.md#L122), ce qui vaut quand N compte des échantillons et non quand le bourrage agrandit N (§4). Dans `crates/ix-code`, [`analyze_metric_spectrum`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L159) tire une période dominante de la [FFT complétée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-code/src/advanced.rs#L173) : une série de période 6 se lit 16/3 ≈ 5,33 avec 12 échantillons et 32/5 = 6,4 avec 24. Seuls ses propres tests l'appellent.
- **Les facteurs de rotation dérivent.** Chaque étage calcule un facteur avec cos et sin et les autres par [multiplications répétées](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L178). Sur x_n = sin n + ½ cos 3n, la transcription s'écarte de la FFT de NumPy d'une erreur relative de l'ordre de 10^-15 à N = 2^8, 10^-14 à N = 2^12 et 10^-13 à N = 2^16, là où le même code avec chaque facteur calculé directement reste de l'ordre de 10^-15. Les contrats disent que les facteurs viennent de [`f64::cos/sin`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L39) et que les plateformes peuvent les arrondir différemment « at ULP scale » ; la récurrence répand une telle différence sur toute la transformée, et décaler d'un ulp le cosinus ou le sinus qui amorce chaque étage donne à N = 2^16 des erreurs n'importe où entre 10^-13 et 10^-11.
- **Le test de Parseval ne tient que parce que son signal est de longueur 8.** [`test_parsevals_theorem`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L236) divise l'énergie spectrale par [`signal.len()`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L241), là où l'identité demande la longueur complétée. Pour (1, −1, 2, −2, 3, −3), Σ x² = 28 et la formule du test donne 28 · 8/6 = 112/3. L'inverse complète aussi : [`ifft`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/fft.rs#L96) ajoute des zéros après la dernière case, donc la TFD à six cases de (1, 2, 3, 4, 5, 6) revient sous forme de huit valeurs complexes qui commencent par 0,75 et 2,1301 + 0,4949i, et non sous forme des six échantillons.
- **`welch_psd` peut boucler indéfiniment, et rapporte la moitié de la puissance.** [`welch_psd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L57) pose [`hop = window_size - overlap`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L63) : un chevauchement égal à la fenêtre ne fait jamais avancer la boucle, et un plus grand fait sous-déborder la soustraction non signée, une panique en compilation de débogage. Son estimation unilatérale [ajoute chaque carré de module une seule fois](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L80), sans le doublement du §5, donc pour la sinusoïde de son propre test, de puissance 0,5, l'intégrale de l'estimation vaut 0,25. Avec une fenêtre de 500 échantillons, `rfft` complète chaque trame à 512 alors que les [étiquettes de fréquence](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L95) divisent par 500 : le pic d'une sinusoïde de 100 Hz échantillonnée à 1 kHz tombe dans la case 51, à 51 × 1000/512 ≈ 99,6 Hz, et est étiqueté 102 Hz. Son [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/spectral.rs#L124) utilise une fenêtre de 512 échantillons, et rien d'autre ne l'appelle ; le gestionnaire `ix_spectrogram`, lui, rejette une fenêtre qui n'est pas une [puissance de deux](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L1159).
- **La décimation et le rééchantillonnage ne filtrent pas.** [`decimate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L6) fait ce que [dit son commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L5), « take every M-th sample » : 64 échantillons de cos(2π·3n/8) décimés par 2 placent leur pic dans la case 8 sur 32, la fréquence 1/4 du §3. [`resample`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L42) évalue la somme de sinus cardinaux avec 8 coefficients de chaque côté et aucune fenêtre, bien que [son commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L20) dise « windowed sinc » : une constante 5 revient à 4,80 en une position demi-entière, et rééchantillonner 100 échantillons de cette constante en 30 donne des valeurs de 4,739 à 5,152. Son [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/sampling.rs#L83) rééchantillonne 100 échantillons en 50, où chaque position est entière et l'interpolation reproduit les échantillons aux arrondis près. Aucune des deux fonctions n'a d'appelant hors de ses tests.
- **Un ordre impair casse le passe-haut.** La conception RIF documente que l'ordre [« Must be even. »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L16), mais le gestionnaire `ix_fir_filter` vérifie seulement qu'il vaut [au moins 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L809). Le passe-haut place son coefficient central en [`order / 2`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/filter.rs#L42) arrondi vers le bas, donc un ordre impair inverse le passe-bas autour du mauvais échantillon : avec une coupure à 0,25, une sinusoïde à 0,1 cycle par échantillon passe avec un gain de 0,3132 à l'ordre 31, contre 0,0012 à l'ordre 32.
- **Le débruiteur par ondelettes de DuckDB viole son invariant.** `ix_wavelet_denoise` promet que la [variance de sortie ne dépasse pas celle de l'entrée](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L306), ce que le §5 démontre pour les longueurs multiples de 2^levels. Pour les autres longueurs, il [répète la dernière valeur](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L335) jusqu'à un tel multiple, débruite, puis tronque. Sur (0, 0, 0, 0, 1, 2) avec 2 niveaux et un seuil 1, le bourrage (2, 2) est moyenné avec la fin, et la sortie est (0 ; 0 ; 0 ; 0 ; 1,75 ; 1,75) : la variance passe de 7/12 à 49/72, un facteur 7/6. Son [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/graphsig.rs#L739) utilise 8 échantillons, où rien n'est complété, et le gestionnaire MCP [rejette](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L776) de telles longueurs à la place.
- **Les contrats et les commentaires s'écartent du code.** La [liste des modules](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/lib.rs#L9) de la crate et [son module d'ondelettes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L3) annoncent des ondelettes de Daubechies ; seule Haar existe. Les contrats disent que [`wavelet::dwt_haar`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L14) panique sur une longueur qui n'est pas une puissance de deux : la fonction s'appelle `haar_dwt`, et elle [abandonne le dernier échantillon](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/wavelet.rs#L7) d'un bloc impair sans erreur. Ils disent que [`correlation::auto_correlation`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L17) n'est pas normalisée, alors que `autocorrelation` [divise par la valeur au décalage nul](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/correlation.rs#L12), et qu'une [entrée vide de la FFT panique](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/CONTRACTS.md#L31), ce que contredit la parenthèse de la même ligne : `fft` renvoie un seul zéro. Le catalogue qu'envoie `ix_explain_algorithm` liste les hyperparamètres de la FFT comme [`["window", "n_points"]`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L5841) ; `ix_fft` ne prend ni l'un ni l'autre.
- **Autres lacunes.** Il n'y a pas de FFT pour les longueurs qui ne sont pas des puissances de deux (base mixte ou Bluestein), pas de transformée inverse ni de phase par MCP, pas de décimateur avec filtre anti-repliement, pas de rééchantillonneur fenêtré ou normalisé, pas de normalisation en densité des spectres unilatéraux, et pas d'autre ondelette que Haar.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Montrez que l'inversion spectrale d'un passe-bas à sinus cardinal fenêtré d'ordre impair M, avec le coefficient central placé en (M − 1)/2, a un gain d'environ 2|sin(πf/2)| là où le passe-bas laisse passer, et comparez avec le filtre d'ordre 31 d'IX à f = 0,1.

> *Solution :* Le passe-bas est symétrique autour de M/2, donc H(f) = e^(−iπfM) A(f) avec A réel. Avec le coefficient en m = (M − 1)/2, le filtre inversé a G(f) = e^(−2πifm) − H(f) = e^(−iπfM)(e^(iπf) − A(f)). Là où le passe-bas laisse passer, A(f) ≈ 1, donc |G(f)| ≈ |e^(iπf) − 1| = 2|sin(πf/2)|, soit 0,3129 à f = 0,1 ; le filtre d'IX a 0,3132, l'écart venant de ce que A(0,1) ne vaut pas exactement 1. Avec M pair, m = M/2 et G(f) = e^(−iπfM)(1 − A(f)), qui y est proche de 0.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Inverse.** Appeler le gestionnaire `fft` sur les huit échantillons de cos(2π·3n/8), avec `inverse` à faux, puis à vrai. Prédiction : deux fois la même sortie, un module 4 à 0,375 et à 0,625 et 0 ailleurs, avec `fft_size` égal à 8.
2. **Grille.** Appeler `rfft` sur les six échantillons de cos(2πn/6), et `analyze_metric_spectrum` sur sin(2πi/6) pour 12, puis 24 échantillons. Prédiction : huit cases, de module 2,5156 à la case 1 et 2,2361 à la case 2 ; des périodes dominantes de 16/3 et 32/5.
3. **Précision.** Comparer `rfft` de x_n = sin n + ½ cos 3n à une FFT précise pour N = 2^8, 2^12 et 2^16. Prédiction : des erreurs relatives de l'ordre de 10^-15 et 10^-14, puis entre 10^-13 et 10^-11 ; les chiffres varient avec le cos et le sin de la plateforme.
4. **Welch.** Appeler `welch_psd` sur la sinusoïde de son test avec une fenêtre de 512 et un chevauchement de 256, puis avec 500 et 250 ; puis avec un chevauchement de 512, dans un processus enfant avec une limite de temps. Prédiction : l'estimation multipliée par la largeur de case 1000/512 a pour somme 0,25 ; le pic du deuxième appel est étiqueté 102 Hz ; le troisième appel ne rend pas la main.
5. **Échantillonnage.** Décimer 64 échantillons de cos(2π·3n/8) par 2 et prendre `rfft` ; interpoler 100 échantillons de la constante 5 en 50,5 avec 8 coefficients ; les rééchantillonner en 30. Prédiction : un pic de 16 à la case 8 sur 32 ; 4,80 ; des valeurs de 4,739 à 5,152.
6. **Passe-haut.** Appeler le gestionnaire `fir_filter` avec kind égal à highpass et cutoff à 0,25 sur 256 échantillons de cos(2π·0,1n), à l'ordre 31, puis 32. Prédiction : le plus grand module de la sortie après l'échantillon 64 vaut 0,309, puis 0,0012.
7. **Ondelettes.** Exécuter `ix_wavelet_denoise` dans DuckDB sur (0, 0, 0, 0, 1, 2) avec 2 niveaux et un seuil 1, puis sur la série de son test. Prédiction : une variance de population de 49/72 ≈ 0,6806 contre 7/12 ≈ 0,5833 pour l'entrée ; puis 0, puisque le seuil supprime tous les détails de la série du test.

### Exercice pratique

À l'étape 4, pourquoi l'intégrale de l'estimation unilatérale vaut-elle la moitié de la puissance, et qu'est-ce qui corrige cela ?

> *Solution :* Pour un signal réel, |X_(N−k)| = |X_k|, donc les cases k et N − k portent la même puissance, et le théorème de Parseval compte les deux. Ne garder que les cases 0 à N/2 laisse tomber la moitié de fréquence négative de chaque case intérieure. Doubler les cases 1 à N/2 − 1 la rétablit ; les cases 0 et N/2 n'ont pas de miroir et restent simples. Pour une sinusoïde, dont la puissance se trouve dans deux cases miroirs, la somme non doublée vaut exactement la moitié.

---

## 8. Pièges courants

- **Lire les cases au-dessus de N/2 comme des hautes fréquences.** Pour un signal réel, elles reflètent les fréquences négatives ; garder les cases 0 à N/2, ou renuméroter la case k en k − N.
- **Prendre une grille plus fine pour une meilleure résolution.** Le bourrage de zéros interpole le spectre ; seul un enregistrement plus long sépare des sinusoïdes proches.
- **Décimer sans passe-bas.** Filtrer d'abord sous la nouvelle fréquence de Nyquist, sinon la bande écartée se replie sur celle qu'on garde.
- **Comparer des hauteurs de pic entre fenêtres ou longueurs.** Une fenêtre change la hauteur du pic, Hann d'environ la moitié, et la fuite étale une sinusoïde hors grille ; diviser par la somme de la fenêtre, ou comparer des énergies.
- **Oublier une convention de normalisation.** Vérifier où va le 1/N, et si un spectre unilatéral double ses cases intérieures, avec le théorème de Parseval sur un signal connu.
- **Multiplier des spectres sans bourrage.** Compléter à au moins L + M − 1, sinon le produit calcule une convolution circulaire qui replie la queue sur la tête.
- **Inverser un passe-bas d'ordre impair.** Prendre un ordre pair, pour que le coefficient central existe.
- **Faire confiance à une routine en base 2 avec une longueur quelconque.** Vérifier la longueur renvoyée, puisque le bourrage change la grille et la normalisation.
- **Compléter avant une transformée en ondelettes.** Le bourrage par répétition du bord change les statistiques du dernier bloc ; signaler quels échantillons ont été ajoutés, ou tronquer à un multiple de 2^levels.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Transformée de Fourier discrète** | Les coefficients X_k = Σ x_n e^(−2πikn/N) d'un signal dans la base des exponentielles complexes échantillonnées |
| **Théorème de Parseval** | ‖x‖² = (1/N) ‖X‖² : la transformée préserve l'énergie au facteur N près |
| **Transformée de Fourier rapide** | Un algorithme qui calcule la TFD en O(N log N) opérations en la découpant récursivement |
| **Facteur de rotation** | Une puissance de e^(−2πi/N) qui multiplie la moitié impaire dans un papillon |
| **Fréquence de Nyquist** | La moitié de la fréquence d'échantillonnage, la plus haute fréquence que l'échantillonnage représente sans ambiguïté |
| **Repliement** | L'apparition d'une sinusoïde située au-dessus de la fréquence de Nyquist à une fréquence plus basse qui a les mêmes échantillons |
| **Fuite spectrale** | L'étalement de l'énergie d'une sinusoïde hors grille sur toutes les cases d'une TFD finie |
| **Fenêtre** | Une pondération appliquée aux échantillons avant une transformée, qui échange le niveau des lobes secondaires contre la largeur du lobe principal |
| **Résolution en fréquence** | Le plus petit écart auquel deux sinusoïdes donnent des pics distincts, environ la fréquence d'échantillonnage divisée par la longueur de l'enregistrement |
| **Théorème de convolution** | La TFD d'une convolution circulaire est le produit des TFD |
| **Transformée de Fourier à court terme** | Une suite de FFT fenêtrées sur des trames glissantes, qui montre comment un spectre évolue dans le temps |
| **Transformée de Haar** | La transformée en ondelettes orthonormée construite à partir de sommes et de différences normalisées de paires |

---

## Auto-évaluation

**1. `ix_fft` renvoie un module 4 à 0,375 et à 0,625 pour un signal de huit échantillons, et 0 ailleurs. Combien de sinusoïdes le signal contient-il ?**
> Une seule sinusoïde réelle, à 0,375 cycle par échantillon. Pour un signal réel, la case à 0,625 = 1 − 0,375 est le miroir de la case à 0,375, la fréquence négative −0,375 ; l'outil étiquette chaque case par k/n, y compris celles au-dessus d'un demi.

**2. Quelqu'un de votre équipe complète 32 échantillons par des zéros jusqu'à 1024 points, voit un seul pic à 0,2051, et conclut que le signal contient une seule sinusoïde. Que lui répondez-vous ?**
> Que les données ne permettent pas de le dire. La résolution de 32 échantillons est d'environ 1/32 de cycle par échantillon, et deux sinusoïdes distantes de 0,01 fusionnent en un seul lobe principal ; le bourrage ne fait qu'échantillonner ce lobe plus finement. Un enregistrement plus long, ici 128 échantillons, sépare des sinusoïdes à 0,20 et 0,21.

**3. Vous devez ramener un audio à 48 kHz à 8 kHz avec IX. Que doit-il se passer avant `decimate` avec un facteur 6 ?**
> Un filtre passe-bas sous la nouvelle fréquence de Nyquist, 4 kHz, soit 1/12 de l'ancienne cadence, puisque `decimate` ne fait que jeter des échantillons et que tout ce qui se trouve entre 4 et 24 kHz se replierait. Avec `ix_fir_filter`, utiliser kind égal à lowpass, une coupure un peu sous 1/12 et un ordre pair.

**4. Une requête DuckDB montre `ix_wavelet_denoise` qui augmente la variance d'une série de six valeurs. La transformée de Haar est-elle cassée ?**
> Non. Sur une longueur multiple de 2^levels, le seuillage doux de Haar ne peut pas augmenter la variance (§5). La fonction complète la série en répétant le bord jusqu'à une telle longueur et tronque le résultat, et le bourrage déplace de la masse dans les échantillons conservés. Tronquer ou compléter la série soi-même et vérifier quels échantillons ont changé, ou utiliser l'outil MCP, qui rejette de telles longueurs.

**Critères de réussite :** Écrire la TFD comme un changement de base et vérifier un spectre avec le théorème de Parseval ; obtenir la FFT en base 2 et expliquer le rôle de ses facteurs de rotation ; prédire où apparaît une sinusoïde échantillonnée et ce qu'un décimateur doit faire d'abord ; expliquer la fuite spectrale, choisir une fenêtre et distinguer la grille de la résolution ; utiliser le théorème de convolution et comparer la TFCT avec la transformée de Haar ; et retracer où le schéma, les contrats, les invariants et les tests d'IX promettent plus que ce que le code tient.

---

## Bases de recherche

- J. Fourier, *Théorie analytique de la chaleur*, Firmin Didot, 1822 : les séries trigonométriques
- A. Haar, « Zur Theorie der orthogonalen Funktionensysteme », *Mathematische Annalen* 69, 1910 : le système de Haar
- H. Nyquist, « Certain topics in telegraph transmission theory », *Transactions of the AIEE* 47, 1928 : la cadence d'échantillonnage nécessaire pour une bande
- D. Gabor, « Theory of communication », *Journal of the Institution of Electrical Engineers* 93, 1946 : l'incertitude temps–fréquence
- C. E. Shannon, « Communication in the presence of noise », *Proceedings of the IRE* 37, 1949 : le théorème d'échantillonnage et la reconstruction par sinus cardinal
- J. W. Cooley et J. W. Tukey, « An algorithm for the machine calculation of complex Fourier series », *Mathematics of Computation* 19, 1965 : la FFT
- P. D. Welch, « The use of fast Fourier transform for the estimation of power spectra: a method based on time averaging over short, modified periodograms », *IEEE Transactions on Audio and Electroacoustics* 15, 1967 : la méthode de Welch
- F. J. Harris, « On the use of windows for harmonic analysis with the discrete Fourier transform », *Proceedings of the IEEE* 66, 1978 : les fenêtres et leurs lobes secondaires
- M. T. Heideman, D. H. Johnson et C. S. Burrus, « Gauss and the history of the fast Fourier transform », *IEEE ASSP Magazine* 1, 1984 : la FFT avant 1965
- S. G. Mallat, « A theory for multiresolution signal decomposition: the wavelet representation », *IEEE Transactions on Pattern Analysis and Machine Intelligence* 11, 1989 : l'analyse multirésolution
- C. Van Loan, *Computational Frameworks for the Fast Fourier Transform*, SIAM, 1992 : le calcul des facteurs de rotation et ses erreurs
- D. L. Donoho, « De-noising by soft-thresholding », *IEEE Transactions on Information Theory* 41, 1995 : le seuillage doux
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2e éd., SIAM, 2002 : l'analyse d'erreur de la FFT
- A. V. Oppenheim et R. W. Schafer, *Discrete-Time Signal Processing*, 3e éd., Prentice Hall, 2010 : échantillonnage, fenêtres, TFCT et conception de filtres
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
