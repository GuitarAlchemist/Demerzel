---
module_id: mat-014-pca-variance-preservation
department: mathematics
course: L'ACP comme préservation de la variance
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-005-symmetric-eigenproblems, mat-006-svd-low-rank-approximation, mat-009-estimation-uncertainty-sampling]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# L'ACP comme préservation de la variance — Ce que gardent les composantes principales, et ce qu'elles ne promettent pas

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Obtenir les composantes principales comme les directions de plus grande variance, et montrer que ce sont des vecteurs propres de la matrice de covariance
- Montrer que les mêmes composantes minimisent l'erreur de reconstruction quadratique, et calculer cette erreur à partir des valeurs propres écartées
- Calculer l'ACP à partir de la SVD des données centrées, et expliquer pourquoi cette voie est plus précise que la formation de la matrice de covariance
- Lire correctement un ratio de variance expliquée, et expliquer comment les unités changent les composantes
- Dire quand les composantes principales ne sont ni uniques ni stables, et distinguer l'ACP du blanchiment
- Retracer ce que calcule l'ACP d'IX, et où son ratio, son test d'arrêt et son état sauvegardé s'écartent de ces définitions

---

## 1. La variance le long d'une direction

Soient x₁, …, xₙ des observations en dimension p de moyenne x̄, et X_c la matrice n × p dont les lignes sont les xᵢ − x̄. La **matrice de covariance empirique** est S = X_cᵀX_c/(n − 1), avec le n − 1 du MAT-009. Pour un vecteur unitaire w, les **scores** zᵢ = wᵀ(xᵢ − x̄) ont une moyenne nulle et une variance empirique wᵀSw. La première **composante principale** est le vecteur unitaire qui maximise cette variance.

S est symétrique et semi-définie positive, donc par le MAT-005 le maximum du quotient de Rayleigh wᵀSw sur les vecteurs unitaires est sa plus grande valeur propre λ₁, atteinte en un vecteur propre q₁. La deuxième composante maximise wᵀSw sur les vecteurs unitaires orthogonaux à q₁, ce qui donne λ₂ et q₂, et ainsi de suite. Les composantes sont orthonormées, les scores selon des composantes différentes sont non corrélés, et leurs variances sont λ₁ ≥ λ₂ ≥ … ≥ λ_p ≥ 0. La variance totale, la trace de S, vaut λ₁ + … + λ_p : l'ACP fait tourner les données sans changer leur dispersion totale.

### Exercice pratique

Des données ont pour covariance S = [[2, 1], [1, 2]]. Quelle est la première composante principale, et quelle fraction de la variance totale porte-t-elle ? Comparez avec la variance le long de (1, 0).

> *Solution :* S (1, 1) = (3, 3) et S (1, −1) = (1, −1), donc les valeurs propres sont 3 et 1, pour (1, 1)/√2 et (1, −1)/√2. La première composante est (1, 1)/√2, de variance 3 sur un total de 4, soit une fraction 3/4. Le long de (1, 0), la variance n'est que S₁₁ = 2 : la corrélation entre les deux coordonnées incline la direction de plus grande dispersion vers la diagonale.

---

## 2. La meilleure approximation de faible dimension

Garder k composantes remplace chaque observation par x̂ᵢ = x̄ + Σⱼ≤ₖ zᵢⱼ qⱼ, sa projection orthogonale sur le sous-espace affine passant par x̄ et engendré par q₁, …, qₖ. Par Pythagore, ‖xᵢ − x̄‖² = ‖x̂ᵢ − x̄‖² + ‖xᵢ − x̂ᵢ‖². Sommé sur les observations, le membre de gauche vaut (n − 1) fois la trace de S, fixée par les données ; maximiser la variance gardée revient donc à minimiser l'**erreur de reconstruction** quadratique Σ‖xᵢ − x̂ᵢ‖². Le minimum vaut (n − 1)(λₖ₊₁ + … + λ_p), les valeurs propres écartées. C'est le théorème d'Eckart–Young du MAT-006, appliqué à X_c : aucun autre sous-espace de dimension k ne fait mieux.

### Exercice pratique

Prenez les quatre points B : (2, 0), (−2, 0), (0, 1) et (0, −1). Calculez S, la somme des carrés des distances à la moyenne, et l'erreur de reconstruction avec une composante.

> *Solution :* La moyenne est nulle, et X_cᵀX_c = [[8, 0], [0, 2]], donc S = diag(8/3, 2/3). La somme des carrés des distances vaut 4 + 4 + 1 + 1 = 10 = 3 (8/3 + 2/3). La première composante est le premier axe, et la projection sur celui-ci laisse les résidus de (0, 1) et (0, −1), d'erreur quadratique 1 + 1 = 2 = 3 · 2/3, la valeur propre écartée fois n − 1. La composante garde 8/(8 + 2) = 0,8 de la variance.

---

## 3. L'ACP par la SVD

Écrivons la SVD du MAT-006 sous la forme X_c = UΣVᵀ. Alors S = VΣ²Vᵀ/(n − 1) : les directions principales sont les vecteurs singuliers à droite, les variances sont λᵢ = σᵢ²/(n − 1), et les scores sont X_cV = UΣ. Calculer l'ACP ainsi ne forme jamais X_cᵀX_c, dont le conditionnement est le carré de celui de X_c : la former peut faire perdre deux fois plus de chiffres, et les petites composantes les perdent en premier (MAT-003, MAT-007). Chaque vecteur singulier, et donc chaque composante, n'est défini qu'au signe près : deux programmes corrects peuvent renvoyer q et −q, et leurs résultats doivent être comparés au signe près.

### Exercice pratique

Calculez les valeurs singulières de la matrice centrée de B, les variances qu'elles donnent, et les conditionnements de X_c et de S.

> *Solution :* Les colonnes de X_c sont (2, −2, 0, 0) et (0, 0, 1, −1). Elles sont orthogonales, de normes √8 et √2, donc σ₁ = √8 et σ₂ = √2, et λ = 8/3 et 2/3 comme au §2. κ(X_c) = √8/√2 = 2, tandis que κ(S) = (8/3)/(2/3) = 4 = κ(X_c)².

---

## 4. Variance expliquée et unités

Le **ratio de variance expliquée** de la composante i vaut λᵢ/(λ₁ + … + λ_p) = λᵢ/trace(S). Son dénominateur est la variance totale, la somme des p valeurs propres, et pas seulement de celles que l'on garde ; il se calcule à partir de la diagonale de S, sans aucune valeur propre. Le ratio dit quelle part de la dispersion porte une composante, pas si elle compte : une direction de faible variance peut être celle qui sépare deux classes.

L'ACP sur la covariance dépend des unités de chaque variable. Multiplier une variable par 100 multiplie sa variance par 10^4 et attire la première composante vers elle. L'**ACP normée** divise d'abord chaque variable par son écart type, ce qui revient à prendre les vecteurs propres de la matrice de corrélation : elle supprime les unités, et donne à chaque variable le même poids par décision. Une variable constante a un écart type nul, donc des corrélations indéfinies : elle ne porte aucune variance et doit être retirée avant la normalisation. Multiplier toutes les variables par le même facteur doit en revanche laisser les composantes inchangées et multiplier chaque variance par le carré du facteur.

### Exercice pratique

La taille a un écart type de 0,1 m et le poids de 10 kg, et ils sont non corrélés. Quelle est la première composante principale, et son ratio ? Qu'est-ce qui change si la taille est mesurée en centimètres ?

> *Solution :* S = diag(0,01 ; 100), donc la première composante est l'axe du poids, de ratio 100/100,01 ≈ 0,9999. En centimètres, la taille a un écart type de 10 et une variance de 100, donc S = diag(100, 100) : les deux variances sont égales, la première composante n'est pas unique, et chaque axe porte 1/2. Aucune des deux réponses ne dit quelle variable compte le plus ; les unités ont décidé.

---

## 5. Unicité, stabilité et blanchiment

Si λ₁ = λ₂, tout vecteur unitaire de leur espace propre est une première composante valide, et des programmes corrects différents en renvoient des différentes. Cet espace propre est un plan quand λ₂ > λ₃ ; quand plus de valeurs propres sont égales, sa dimension est le nombre de valeurs propres égales, et pour S = I₃ c'est l'espace entier. Si λ₁ et λ₂ sont proches, la composante existe mais est fragile : par le théorème de Davis–Kahan, une perturbation E de S, due au bruit ou à l'arrondi, peut faire tourner q₁ d'un angle θ dont le sinus atteint environ ‖E‖ divisé par l'**écart spectral** λ₁ − λ₂. L'itération de la puissance du MAT-005 ressent le même écart : la tangente de son angle à q₁ est multipliée à chaque étape par un facteur d'au plus λ₂/λ₁, exactement λ₂/λ₁ quand l'erreur est dans l'espace propre de λ₂, comme dans l'exercice ci-dessous, et la **déflation**, qui soustrait λ v vᵀ pour trouver la composante suivante, transmet l'erreur restante.

L'ACP ne **blanchit** pas. Ses scores gardent les variances λᵢ ; le blanchiment divise le score selon qᵢ par √λᵢ pour chaque composante de λᵢ > 0, de sorte que les données blanchies ont l'identité pour covariance sur ces composantes ; une direction de variance nulle ne peut pas être remise à l'échelle, et elle est écartée ou régularisée. Le blanchiment met les directions de plus faible variance, souvent faites surtout de bruit, sur le même pied que les plus grandes.

### Exercice pratique

Quand la première composante principale cesse-t-elle d'être unique ? Pour S = diag(2/3, 2r²/3) avec r = 0,999, l'itération de la puissance part de (1, 1)/√2. Combien d'étapes faut-il pour que la tangente de son angle au premier axe passe sous 10^-6 ?

> *Solution :* Quand λ₁ = λ₂ : tout vecteur unitaire de leur espace propre est alors une première composante valide. Ici Sᵏ(1, 1) est proportionnel à (1, r²ᵏ), donc la tangente après k étapes vaut r²ᵏ, et le facteur par étape est λ₂/λ₁ = r² = 0,998001. La condition r²ᵏ < 10^-6 demande k ≥ 6905 étapes. Après 1000 étapes, la tangente vaut encore r^2000 ≈ 0,135, soit un angle d'environ 7,7°.

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a exécuté ni IX ni ses tests. Les nombres attribués au comportement d'IX viennent d'une transcription ligne à ligne de `fit`, `power_iteration`, `deflate` et `explained_variance_ratio` en Python, dont les flottants sont en binary64 IEEE comme le `f64` de Rust : ce sont des prédictions, que le §7 propose de vérifier.

**ACP** (`crates/ix-unsupervised`). `PCA` calcule la matrice de covariance [avec n − 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L168), puis extrait chaque composante par [itération de la puissance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L103), avec au plus 1000 étapes et la tolérance 10^-10 [fixée par `fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L176), et la retire par [déflation](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L141). Le MAT-005 a montré que le vecteur de départ fixe (1, …, 1)/√p peut manquer entièrement la direction dominante ; les constats ci-dessous sont d'une autre nature. L'outil MCP `ix_pca` appelle `PCA` par le gestionnaire [`pca`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L370), qui [rejette](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L382) plus de composantes que de variables, et le pipeline d'apprentissage ne l'utilise que lorsque son option `pca_components` est [inférieure au nombre de colonnes](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L539). Le ratio et l'ajustement s'écrivent :

```rust
    /// Get explained variance ratios (proportion of total variance per component).
    pub fn explained_variance_ratio(&self) -> Option<Array1<f64>> {
        self.explained_variance.as_ref().map(|ev| {
            let total = ev.sum();
            if total > 0.0 {
                ev / total
            } else {
                ev.clone()
            }
        })
    }
```

```rust
    fn fit(&mut self, x: &Array2<f64>) {
        let n = x.nrows();
        let p = x.ncols();
        let k = self.n_components.min(p);

        // Compute column means
        let mean = x.mean_axis(Axis(0)).unwrap();

        // Center the data
        let mut centered = x.clone();
        for mut row in centered.rows_mut() {
            row -= &mean;
        }

        // Compute covariance matrix: (1/(n-1)) X^T X
        let cov = centered.t().dot(&centered) / (n.max(2) - 1) as f64;

        // Extract top-k eigenvectors via repeated power iteration + deflation
        let mut components = Array2::zeros((k, p));
        let mut explained_variance = Array1::zeros(k);
        let mut current_cov = cov;

        for i in 0..k {
            let (eigenvalue, eigenvector) = power_iteration(&current_cov, 1000, 1e-10);
            components.row_mut(i).assign(&eigenvector);
            explained_variance[i] = eigenvalue.max(0.0);
            current_cov = deflate(&current_cov, eigenvalue, &eigenvector);
        }

        self.components = Some(components);
        self.explained_variance = Some(explained_variance);
        self.mean = Some(mean);
    }
```

- **Le ratio divise par la variance gardée, pas par le total.** `ev` ne contient que les k variances calculées, donc avec une composante le ratio vaut 1 dès que la variance trouvée est positive, quelle que soit sa part du total. Quand cette variance est nulle, comme pour des données constantes ou pour des points le long de (1, −1), que le vecteur de départ manque, l'autre branche renvoie [0]. Sur les dix points du tutoriel de Lindsay Smith, les données du test de skill d'IX, la première composante porte une fraction 0,963 de la variance, et le ratio rapporte 1 ; sur les points isotropes (±1, 0) et (0, ±1), où la vraie fraction est 1/2, il rapporte aussi 1. Avec k = p, la somme est la trace quand l'itération de la puissance trouve toutes les valeurs propres, comme sur les mêmes dix points, où le ratio est juste : 0,9632 et 0,0368. Sur les six points du MAT-005, dont le vecteur de départ manque la direction dominante, elle trouve 2/5 et 0 pour une trace de 8/5, et le ratio affiche [1, 0]. Le schéma de sortie promet la [« Fraction of total variance carried by each component »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L187). Deux tests vérifient le ratio avec une composante, [au-dessus de 0,99](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L237) et [au-dessus de 0,9](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L978) : tous deux passent sur toutes les données dont la première variance trouvée est positive.
- **Le test d'arrêt dépend de l'échelle des données.** L'itération de la puissance s'arrête quand l'estimation de Rayleigh [varie de moins de 10^-10](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L126), un seuil absolu. Multiplier les données par une puissance de deux est exact en binary64, donc chaque étape de l'ajustement change d'échelle exactement, sauf cette comparaison. Sur les quatre points B du §2 :
  - à l'échelle 1, le premier appel prend 11 étapes et la première composante est à moins de 2 · 10^-5 degré du premier axe ;
  - à 2^-16, la première composante est décalée de 0,9°, les variances valent environ 2,66 s² et 0,30 s² au lieu de (8/3) s² et (2/3) s², et le ratio vaut 0,90 au lieu de 0,8 ;
  - de 2^-17 ≈ 7,6 · 10^-6 à 2^-24, la première estimation de Rayleigh (5/3) s² est déjà sous 10^-10, donc chaque appel s'arrête après une seule multiplication. Les deux composantes valent (4, 1)/√17, à 14° du premier axe, de variances (5/3) s² et (15/34) s², avec un ratio de 34/43 ≈ 0,791 ;
  - en dessous, la [garde sur la norme du produit](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L120), 10^-15, arrête la boucle avant que l'estimation soit gardée, et l'appel renvoie la variance 0 avec le vecteur de départ : à 2^-25 pour le second appel seulement, donc le ratio affiche [1, 0], et à partir de 2^-26 ≈ 1,5 · 10^-8 pour les deux appels, donc il affiche [0, 0].
- **L'orthogonalité ne vaut que ce que vaut le test d'arrêt.** S'arrêter sur la valeur propre laisse dans le vecteur une erreur d'un ordre plus grand, et la déflation la transmet. Sur B, le produit scalaire des deux composantes vaut environ −7,2 · 10^-7 à l'échelle 1, −1,1 · 10^-5 à 2^-4 et −7,3 · 10^-4 à 2^-10. [`test_pca_components_orthogonal`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L288) exige [moins de 10^-6](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L306) sur des données dont les deux premières variances, 2,82 et 0,0133, sont très éloignées ; là, le produit scalaire prédit vaut −1,9 · 10^-8. Aucun des sept tests de `pca.rs` ne compare les composantes à un solveur spectral ou à la SVD.
- **Des valeurs propres proches atteignent le plafond en silence.** Sur (±1, 0) et (0, ±r), les variances valent 2/3 et 2r²/3, et les itérés sont proportionnels à (1, r²ᵏ) comme au §5. Le premier appel prend 50 étapes pour r = 0,9 et environ 390 pour r = 0,99. Pour r = 0,999, il s'arrête au plafond de 1000 avec une première composante décalée d'environ 7,7°, et rien dans le résultat ne dit que l'itération n'a pas convergé.
- **Un modèle sauvegardé peut refuser de se charger.** `fit` garde [min(n_components, p)](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L156) composantes, mais `save_state` enregistre le [nombre demandé](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L75), et `load_state` [redimensionne avec lui](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L89). Avec trois composantes demandées sur deux variables, l'état contient quatre nombres pour une forme 3 × 2, et le chargement panique avec [« PcaState components dimensions mismatch »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L90). Le gestionnaire et le pipeline ne demandent jamais plus de composantes que de variables, mais un appelant direct de `PCA::new` n'est pas protégé.
- **La transformation ne blanchit pas.** Elle [projette les données centrées](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-unsupervised/src/pca.rs#L198) sur les composantes, donc les scores gardent les variances λᵢ, comme le décrit le §5.

Corriger quoi que ce soit de tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pourquoi `explained_variance_ratio` renvoie-t-il 1 chaque fois qu'une seule composante est demandée et que sa variance est positive, et quel dénominateur en ferait une fraction de la variance totale ?

> *Solution :* Avec une composante, `ev` n'a qu'une entrée λ̂₁, et `ev / total` la divise par elle-même ; seul λ̂₁ = 0 y échappe, et le ratio vaut alors [0]. La fraction de la variance totale demande λ̂₁/trace(S), où trace(S) est la somme des p coefficients diagonaux de la matrice de covariance, que `fit` calcule puis jette. Sur les dix points du tutoriel de Lindsay Smith, cela donne 1,284/(1,284 + 0,0491) ≈ 0,963. Un test capable de détecter le défaut demande des données dont la première composante porte une fraction connue nettement sous son seuil, comme les points isotropes, dont la fraction vaut 1/2.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire et appelle directement les fonctions, jamais un serveur MCP en fonctionnement.

1. **Le ratio.** Appeler le gestionnaire `pca` sur les dix points du tutoriel de Lindsay Smith avec `n_components` égal à 1, puis 2, et sur les points isotropes (±1, 0) et (0, ±1) avec 1. Prédiction : [1], puis environ [0,9632 ; 0,0368], puis [1] ; la trace de la covariance donne les vraies fractions 0,963 et 1/2 dans les cas à une composante.
2. **Face à la SVD.** Ajuster `PCA` avec deux composantes sur les dix points, et calculer `svd` de la matrice centrée. Prédiction : les composantes égalent les vecteurs singuliers à droite au signe près, la première à moins de 10^-6 degré et la seconde à moins de 10^-5 degré, et les variances égalent σ²/9 à 10^-12 près.
3. **L'échelle.** Ajuster `PCA` avec deux composantes sur B multiplié par 1, 2^-4, 2^-10, 2^-16, 2^-17, 2^-20, 2^-25 et 2^-26. Prédiction : les valeurs du §6, d'une première composante à moins de 2 · 10^-5 degré du premier axe à l'échelle 1 jusqu'à la même composante (4, 1)/√17 deux fois à 2^-17 et 2^-20, puis les ratios [1, 0] à 2^-25 et [0, 0] à 2^-26.
4. **L'orthogonalité.** Sur les données de `test_pca_components_orthogonal` et sur B aux échelles de l'étape 3, calculer le produit scalaire des deux composantes. Prédiction : environ −1,9 · 10^-8 sur les données du test, et −7,2 · 10^-7, −1,1 · 10^-5 et −7,3 · 10^-4 sur B à 1, 2^-4 et 2^-10.
5. **Des valeurs propres proches.** Ajuster sur (±1, 0) et (0, ±r) pour r = 0,9, 0,99 et 0,999. Prédiction : la première composante est à moins de 0,002° du premier axe pour r = 0,9, décalée d'environ 0,024° pour r = 0,99, et d'environ 7,7° pour r = 0,999.
6. **Sauvegarder et recharger.** Ajuster `PCA::new(3)` sur les dix points, appeler `save_state`, puis `load_state` dans `std::panic::catch_unwind`. Prédiction : l'ajustement et la transformation réussissent avec deux composantes, et `load_state` panique avec le message du §6.

### Exercice pratique

Pour quels facteurs d'échelle s le premier appel de l'itération de la puissance s'arrête-t-il après une seule multiplication sur B · s, et pourquoi cela fait-il de 2^-17 la première puissance de deux concernée ?

> *Solution :* La première estimation est comparée à la valeur initiale 0, donc la boucle s'arrête aussitôt quand v₀ᵀ(s² S)v₀ < 10^-10, avec v₀ = (1, 1)/√2 et v₀ᵀSv₀ = (8/3 + 2/3)/2 = 5/3. Cela signifie (5/3) s² < 10^-10, soit s < √(6 · 10^-11) ≈ 7,75 · 10^-6. La puissance 2^-17 ≈ 7,63 · 10^-6 est en dessous, alors que 2^-16 ≈ 1,53 · 10^-5 est au-dessus. Bien plus bas, l'appel s'arrête encore après une seule multiplication, mais par la garde sur la norme du produit : ‖s²Sv₀‖ = (√34/3) s² < 10^-15 quand s < √(3 · 10^-15/√34) ≈ 2,27 · 10^-8, donc à partir de 2^-26 ≈ 1,49 · 10^-8, 2^-25 ≈ 2,98 · 10^-8 restant au-dessus, la variance renvoyée est 0. Les données sont les mêmes aux unités près ; seuls les seuils absolus voient la différence.

---

## 8. Pièges courants

- **Diviser par la variance gardée.** Le ratio de variance expliquée demande la trace de la matrice de covariance ; la somme des valeurs propres retenues fait tout expliquer à une seule composante.
- **Mélanger les unités dans l'ACP sur la covariance.** Une variable de grande dispersion numérique domine la première composante ; normez quand les unités sont arbitraires, et dites-le.
- **Lire la variance comme de l'importance.** Une petite composante peut porter le signal qui compte ; le ratio mesure la dispersion, pas la pertinence.
- **Comparer des composantes sans tenir compte du signe.** q et −q sont la même composante ; comparez |qᵀq′|, ou fixez une convention de signe.
- **Faire confiance à une composante de faible écart spectral.** Quand λ₁ ≈ λ₂, interprétez le sous-espace de toutes les composantes dont les valeurs propres se groupent avec elles, jusqu'à un écart net, pas chaque direction.
- **Former XᵀX quand la SVD est disponible.** Cela élève le conditionnement au carré et fait perdre d'abord les petites composantes.
- **S'arrêter sur une variation absolue.** Une tolérance qui ignore la taille de la matrice fait dépendre la réponse des unités ; comparez les variations à la taille de la valeur propre.
- **Confondre ACP et blanchiment.** L'ACP fait tourner ; le blanchiment change aussi l'échelle, et amplifie les directions de plus faible variance.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Matrice de covariance empirique** | S = X_cᵀX_c/(n − 1), pour la matrice des données centrées X_c |
| **Composante principale** | Un vecteur propre unitaire de S ; la première maximise la variance des données projetées |
| **Score** | La coordonnée wᵀ(x − x̄) d'une observation selon une composante |
| **Variance totale** | La trace de S, égale à la somme de ses valeurs propres |
| **Ratio de variance expliquée** | λᵢ divisé par la variance totale |
| **Erreur de reconstruction** | La somme des carrés des distances des observations à leurs projections, (n − 1) fois les valeurs propres écartées |
| **Théorème d'Eckart–Young** | La SVD tronquée est la meilleure approximation de rang donné en norme de Frobenius |
| **ACP normée** | L'ACP de la matrice de corrélation, après retrait des variables constantes et division de chacune des autres par son écart type |
| **Écart spectral** | λ₁ − λ₂, qui règle la stabilité de la première composante |
| **Déflation** | Soustraire λ v vᵀ d'une matrice pour retirer un couple propre déjà trouvé |
| **Blanchiment** | Diviser les scores par √λᵢ, pour les composantes de λᵢ > 0, de sorte que leur covariance devienne l'identité |

---

## Auto-évaluation

**1. Un outil rapporte qu'une composante principale explique 100 % de la variance d'un jeu de données. Que vérifiez-vous avant de le croire ?**
> Si le ratio divise par la variance totale. Calculez la trace de la matrice de covariance et comparez-la à la première valeur propre ; le `explained_variance_ratio` d'IX, par exemple, renvoie 1 chaque fois qu'une seule composante est gardée et que sa variance est positive. Un vrai 100 % signifie que les données centrées sont sur une droite.

**2. Deux bibliothèques renvoient les premières composantes (0,6 ; 0,8) et (−0,6 ; −0,8) sur les mêmes données. L'une d'elles se trompe-t-elle ?**
> Non. Les vecteurs propres et les vecteurs singuliers sont définis au signe près, donc les deux décrivent la même composante ; les scores ne diffèrent que par le signe. Comparez |qᵀq′|, qui vaut 1 ici.

**3. L'ACP d'IX donne des composantes différentes sur les mêmes mesures en centimètres et en kilomètres. Est-ce une propriété de l'ACP ?**
> Non. Multiplier toutes les variables par le même facteur multiplie S par son carré et laisse les vecteurs propres inchangés. La différence vient de la tolérance absolue de 10^-10 de l'itération de la puissance d'IX, sous laquelle tombent les petites variances en kilomètres. Changer l'échelle d'une seule variable, en revanche, change bien les composantes.

**4. Un échantillon donne λ₁ = 1,00 et λ₂ = 0,99. Jusqu'où feriez-vous confiance à la direction de la première composante ?**
> Pas loin. L'écart spectral vaut 0,01, donc par Davis–Kahan une perturbation de S de taille 0,001 pourrait déjà faire tourner la composante d'un angle dont le sinus vaut environ 0,1. Rapportez le plan des deux premières composantes, pourvu que λ₃ soit nettement sous 0,99, et vérifiez sa stabilité, par exemple par rééchantillonnage.

**Critères de réussite :** Obtenir les composantes principales à partir de la variance, les relier à l'erreur de reconstruction et à la SVD des données centrées, calculer un ratio de variance expliquée avec le bon dénominateur, expliquer l'effet des unités, du signe et des faibles écarts spectraux, distinguer l'ACP du blanchiment, et retracer où le ratio, le test d'arrêt et l'état sauvegardé d'IX s'écartent des définitions.

---

## Bases de recherche

- K. Pearson, « On lines and planes of closest fit to systems of points in space », *Philosophical Magazine* 2, 1901 : le sous-espace le mieux ajusté
- H. Hotelling, « Analysis of a complex of statistical variables into principal components », *Journal of Educational Psychology* 24, 1933 : les composantes principales comme directions de plus grande variance
- C. Eckart et G. Young, « The approximation of one matrix by another of lower rank », *Psychometrika* 1, 1936 : la meilleure approximation de rang faible
- C. Davis et W. M. Kahan, « The rotation of eigenvectors by a perturbation. III », *SIAM Journal on Numerical Analysis* 7, 1970 : la stabilité des vecteurs propres et l'écart spectral
- I. T. Jolliffe, *Principal Component Analysis*, 2e éd., Springer, 2002 : l'ACP, la variance expliquée et le choix des échelles
- L. I. Smith, « A tutorial on principal components analysis », 2002 : l'exemple à dix points utilisé par le test de skill d'IX
- G. H. Golub et C. F. Van Loan, *Matrix Computations*, 4e éd., Johns Hopkins University Press, 2013 : la SVD, l'itération de la puissance et la déflation
- I. T. Jolliffe et J. Cadima, « Principal component analysis: a review and recent developments », *Philosophical Transactions of the Royal Society A* 374, 2016 : l'ACP normée et l'interprétation
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
