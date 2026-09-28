---
module_id: mat-007-least-squares-regularisation
department: mathematics
course: Moindres carrés, régularisation et identifiabilité
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-003-floating-point-conditioning, mat-006-svd-low-rank-approximation]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Moindres carrés, régularisation et identifiabilité — Quand les données ne suffisent pas à fixer les paramètres

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

Après cette leçon, vous serez capable de :
- Déduire les équations normales de l'orthogonalité du résidu, et résoudre à la main un petit ajustement par moindres carrés
- Dire quand les paramètres d'un modèle linéaire sont identifiables, et trouver la solution de norme minimale quand ils ne le sont pas
- Expliquer pourquoi résoudre les équations normales perd deux fois plus de chiffres qu'une résolution par la SVD, et pourquoi centrer une variable aide
- Écrire la solution ridge (Tikhonov) avec la SVD, et expliquer pourquoi elle est unique pour tout λ positif
- Dire ce que calcule la régression linéaire d'IX, où elle échoue, et ce que son échec fait aux processus qui l'appellent

---

## 1. Le problème des moindres carrés

Un modèle linéaire prédit y à partir de variables : y ≈ X w, où la **matrice de plan** X, de taille n × p, a une ligne par observation et une colonne par paramètre. Avec plus d'observations que de paramètres, les équations X w = y n'ont en général pas de solution. Les **moindres carrés** choisissent le w qui minimise la longueur du **résidu** r = y − X w, c'est-à-dire ‖X w − y‖₂.

Les vecteurs X w remplissent l'espace des colonnes de X, et le plus proche de y est sa projection orthogonale : le résidu du meilleur w est orthogonal à chaque colonne de X. C'est Xᵀ(y − X w) = 0, les **équations normales**

XᵀX w = Xᵀy.

Réciproquement, tout w qui les vérifie minimise le résidu : pour tout autre w′, X(w′ − w) est dans l'espace des colonnes, donc ‖X w′ − y‖² = ‖X (w′ − w)‖² + ‖X w − y‖² par Pythagore.

### Exercice pratique

Ajustez la droite y = a + b x aux points (0, 0), (1, 1) et (2, 3).

> *Solution :* Les lignes de X sont (1, 0), (1, 1) et (1, 2), et y = (0, 1, 3). Alors XᵀX = [[3, 3], [3, 5]] et Xᵀy = (4, 7). Le déterminant vaut 15 − 9 = 6, donc (a, b) = (1/6) · (5 · 4 − 3 · 7, −3 · 4 + 3 · 7) = (−1/6, 3/2). Les valeurs ajustées sont −1/6, 4/3 et 17/6, et le résidu vaut (1/6, −1/3, 1/6) : sa somme est nulle et 0 · 1/6 + 1 · (−1/3) + 2 · 1/6 = 0, donc il est orthogonal aux deux colonnes.

---

## 2. Identifiabilité

Les paramètres sont **identifiables** quand les données les déterminent : quand la solution des moindres carrés est unique. C'est le cas exactement quand X est de **rang colonne plein**. Si X v = 0 pour un v ≠ 0, alors w + t v s'ajuste exactement aussi bien que w pour tout t, et les données ne peuvent pas distinguer ces vecteurs de paramètres. Si au contraire X v = 0 seulement pour v = 0, alors vᵀXᵀX v = ‖X v‖² > 0 pour tout v ≠ 0, donc XᵀX est inversible et les équations normales ont une seule solution.

Les causes typiques d'un rang déficient sont une variable qui en duplique une autre, une variable combinaison d'autres, une variable constante à côté du biais, et moins d'observations que de paramètres. Quand le rang est déficient, on peut encore choisir une réponse : la **solution de norme minimale** w⁺ = X⁺y, avec la pseudo-inverse de MAT-006 §4, est la solution des moindres carrés de plus petite longueur. Elle n'a aucune composante selon les directions que les données ne voient pas.

### Exercice pratique

Avec X = [[1, 2], [1, 2]] et y = (3, 3), décrivez toutes les solutions des moindres carrés, et donnez celle de norme minimale.

> *Solution :* Les deux lignes disent w₁ + 2 w₂ = 3, donc chaque point de cette droite s'ajuste exactement, avec un résidu nul ; la direction (2, −1) vérifie X (2, −1) = 0 et reste invisible. La solution la plus courte est orthogonale à (2, −1), donc multiple de (1, 2) : t (1, 2) avec t + 4 t = 3, soit w⁺ = (3/5, 6/5), de longueur au carré 9/25 + 36/25 = 9/5.

---

## 3. Conditionnement : pourquoi pas les équations normales

Les valeurs singulières de XᵀX sont les carrés de celles de X (MAT-006), donc κ₂(XᵀX) = κ₂(X)² quand X est de rang colonne plein. D'après la règle empirique de MAT-003, une résolution par les équations normales peut perdre environ 2 log₁₀ κ₂(X) chiffres. Une résolution par la SVD, w = V Σ⁻¹ Uᵀ y pour un rang colonne plein, ou par une factorisation QR, travaille sur X elle-même et perd environ log₁₀ κ₂(X) quand le résidu est petit. Quand le résidu est grand, le problème des moindres carrés lui-même contient un terme en κ², et aucun algorithme ne l'évite.

Former XᵀX peut même détruire l'information purement et simplement. La **matrice de Läuchli** X = [[1, 1], [δ, 0], [0, δ]] a les valeurs singulières √(2 + δ²) et δ, donc elle est de rang plein pour tout δ ≠ 0. Mais XᵀX = [[1 + δ², 1], [1, 1 + δ²]], et pour δ = 10^-8, δ² = 10^-16 est sous la moitié de l'epsilon machine de MAT-003 : fl(1 + δ²) = 1, et la matrice XᵀX stockée vaut [[1, 1], [1, 1]], exactement singulière. La SVD de X trouve encore δ.

Le conditionnement dépend aussi de la façon d'écrire le modèle. Prenez la variable x = c + (0, 1, 2) avec un biais. Pour c = 0 le problème est sage ; pour c grand, la colonne x est presque parallèle à la colonne de uns, et le second pivot de XᵀX tombe comme 2/c². Soustraire la moyenne de la variable, le **centrage**, supprime le problème : avec x − x̄ = (−1, 0, 1), XᵀX = diag(2, 3). La droite ajustée est la même, écrite autour de x̄ au lieu de 0.

### Exercice pratique

Pour x = c + (0, 1, 2) avec une colonne de biais, montrez qu'éliminer la première colonne de XᵀX laisse le second pivot 6/(3c² + 6c + 5).

> *Solution :* XᵀX = [[Σx², Σx], [Σx, 3]] avec Σx = 3c + 3 et Σx² = c² + (c + 1)² + (c + 2)² = 3c² + 6c + 5. Le second pivot vaut 3 − (Σx)²/Σx² = (3 (3c² + 6c + 5) − (3c + 3)²)/Σx² = (9c² + 18c + 15 − 9c² − 18c − 9)/Σx² = 6/(3c² + 6c + 5), environ 2/c² pour c grand.

---

## 4. Régression ridge

La **régression ridge**, ou **régularisation de Tikhonov**, minimise ‖X w − y‖² + λ ‖w‖² pour un λ > 0 choisi. Annuler le gradient donne (XᵀX + λI) w = Xᵀy. XᵀX est semi-définie positive, puisque vᵀXᵀX v = ‖X v‖² ≥ 0 (§2), donc chaque valeur propre de XᵀX + λI vaut au moins λ > 0, et la solution est unique pour tout λ > 0, même quand X est de rang déficient. Avec la SVD de MAT-006,

w_λ = Σᵢ σᵢ/(σᵢ² + λ) (uᵢ · y) vᵢ.

Comparée à la pseudo-inverse, qui multiplie uᵢ · y par 1/σᵢ, la ridge le multiplie par le **facteur de filtre** σᵢ²/(σᵢ² + λ) : proche de 1 quand σᵢ² ≫ λ, proche de 0 quand σᵢ² ≪ λ. La ridge amortit donc les directions que les données déterminent à peine au lieu de les couper à une tolérance, et w_λ tend vers X⁺y quand λ tend vers 0. Le prix est une estimation biaisée vers 0. Le terme de biais du modèle est en général laissé hors de la pénalité, et les variables sont d'abord centrées, pour que le rétrécissement ne dépende pas de l'emplacement de l'origine.

### Exercice pratique

Pour X = [[1, 2], [1, 2]] et y = (3, 3) du §2, calculez la solution ridge w_λ, et vérifiez sa limite quand λ tend vers 0.

> *Solution :* XᵀX = [[2, 4], [4, 8]] et Xᵀy = (6, 12). Essayez w = α (1, 2) : la première équation donne (2 + λ) α + 8 α = 6, donc α = 6/(10 + λ), et la seconde donne 4 α + 2 (8 + λ) α = 12, le même α. Donc w_λ = (6/(10 + λ)) (1, 2), par exemple (1/2, 1) pour λ = 2. Quand λ tend vers 0, w_λ tend vers (3/5, 6/5), la solution de norme minimale du §2.

---

## 5. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**L'ajustement** (`crates/ix-supervised/src/linear_regression.rs`). [`LinearRegression::fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L57) ajoute une colonne de uns pour le biais et résout les équations normales avec un inverse explicite, mot pour mot aux lignes 57 à 74 :

```rust
    fn fit(&mut self, x: &Array2<f64>, y: &Array1<f64>) {
        let n = x.nrows();
        // Add bias column (column of ones)
        let ones = Array2::ones((n, 1));
        let x_aug = ndarray::concatenate(Axis(1), &[x.view(), ones.view()]).unwrap();

        // Normal equation: w = (X^T X)^{-1} X^T y
        let xtx = x_aug.t().dot(&x_aug);
        let xty = x_aug.t().dot(y);

        // Solve via inverse (fine for small/medium datasets)
        let xtx_inv = ix_math::linalg::inverse(&xtx).expect("X^T X is singular");
        let w = xtx_inv.dot(&xty);

        let p = x.ncols();
        self.weights = Some(w.slice(ndarray::s![..p]).to_owned());
        self.bias = w[p];
    }
```

Trois conséquences découlent du §3 et de MAT-003 :
- **Il élève le conditionnement au carré.** Chaque ajustement paie κ₂(X)², et la colonne de biais rend une variable décalée presque colinéaire avec elle.
- **Son verdict dépend de l'échelle et du décalage.** [`inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L83) répond `Singular` quand un pivot passe [sous 10^-12](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/linalg.rs#L110), un seuil absolu (MAT-003). Pour x = c + (0, 1, 2), le second pivot 6/(3c² + 6c + 5) passe sous ce seuil dès que c dépasse environ 1,41 · 10^6, donc trois relevés d'un horodatage Unix en secondes, de l'ordre de 10^9, pris à une seconde d'intervalle, font échouer l'ajustement bien que le plan soit de rang plein. En deçà, l'ajustement se termine sans erreur, quel que soit le nombre de chiffres perdus ; l'exercice à la fin de cette section montre combien.
- **Il panique.** Le `expect` de la ligne 68 transforme `Singular` en panique, et les appelants la gèrent différemment.

**Ce que la panique fait aux appelants.** [`ix-duck`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L111) documente la panique et [la rattrape](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L114), en renvoyant une erreur SQL. Le gestionnaire de l'outil MCP `ix_linear_regression` appelle [`fit`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L285) sans cette protection, tout comme le [pipeline de ML](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/ml_pipeline.rs#L791). Le serveur MCP exécute chaque [`tools/call`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L175) sur son propre thread de travail, qui n'écrit la réponse qu'[après le retour du gestionnaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/main.rs#L184). `ix_linear_regression` passe par le registre, comme la plupart des outils de base selon un [commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1292) de `tools.rs`, et les appels qui passent par le registre traversent `dispatch_action`, qui tient un verrou global pendant l'exécution de l'outil, mot pour mot aux lignes 236 à 243 de `crates/ix-agent/src/registry_bridge.rs` :

```rust
    let chain_guard = middleware_chain()
        .lock()
        .expect("middleware chain mutex poisoned");

    let result = {
        let mut wc = WriteContext { read: cx, sink };
        chain_guard.dispatch(&mut wc, action, &RegistryLookupHandler)
    };
```

La lecture de ce code prédit trois effets d'une seule requête qui fait paniquer `fit` :
1. Le thread de travail se termine sans écrire de réponse, donc le client attend une réponse qui ne vient jamais.
2. La panique se propage pendant que `chain_guard` est tenu, et un `Mutex` Rust est **empoisonné** quand un thread panique en le tenant.
3. Dès lors, chaque appel qui passe par le registre panique sur le `expect` de la [ligne 238](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/registry_bridge.rs#L238), et n'obtient pas non plus de réponse, jusqu'au redémarrage du serveur.

Deux autres faits :
- **Son schéma nomme la mauvaise clé.** Le schéma d'entrée publié de `ix_linear_regression` exige [`"X"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/skills/batch1.rs#L839), alors que le gestionnaire lit [`"x"`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L270). Les clés JSON sont sensibles à la casse, donc un client qui suit le schéma devrait recevoir l'erreur « Missing or invalid field 'x' ». La démo d'IX envoie `"x"`, et son [commentaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/demo/scenarios/sprint_oracle.rs#L71) le dit.
- **Les tests restent dans les cas faciles.** [`test_linear_regression_multivariate`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-supervised/src/linear_regression.rs#L152) ajuste des données exactes sur les quatre points de {1, 2}², un plan bien conditionné, avec une tolérance de 10^-6. `ix-duck` [vérifie](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-duck/src/supervised.rs#L283) que des colonnes exactement colinéaires donnent une erreur SQL plutôt qu'une panique. Aucun test ne couvre un décalage ou un plan presque colinéaire, où l'ajustement se termine sans erreur.

Les crates `ix-supervised` et `ix-math` d'IX n'ont ni régression ridge ou lasso, ni factorisation QR. La voie SVD du §3 est disponible par [`pseudo_inverse`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-math/src/svd.rs#L73), avec les réserves de MAT-006, et IX a déjà un test de rang relatif, [`RankReport.deficiency`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-signal/src/state_space.rs#L356), dans `ix-signal`, qu'un ajustement pourrait consulter avant de résoudre. Corriger tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Prédisez ce que `fit` renvoie pour x = c + (0, 1, 2) et y = 2x + 1, dont la réponse exacte est la pente 2 et le biais 1, pour c = 10^6 et pour c = 10^7.

> *Solution :* Pour c = 10^7, le second pivot vaut environ 2/c² = 2 · 10^-14, sous 10^-12, donc `inverse` répond `Singular` et `fit` panique. Pour c = 10^6, il vaut environ 2 · 10^-12, juste au-dessus du seuil, donc `fit` se termine. Sa réponse est décidée par l'arrondi dans un pivot aussi petit face à des coefficients de l'ordre de 3 · 10^12 : κ₂(XᵀX) vaut environ 1,5 · 10^24, bien au-delà de ce que binary64 peut résoudre. Ici, les coefficients de XᵀX et de Xᵀy sont des entiers inférieurs à 2^53, donc exacts, et une transcription de `inverse` prédit la pente 2 + 2^-11 = 2,00048828125 et le biais exactement 0. Les valeurs ajustées aux données sont alors fausses d'environ 487, sans aucune erreur signalée. C'est une prédiction tirée de la lecture du code, pas une exécution ; le §6 la vérifie.

---

## 6. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats.

1. **Le balayage des décalages.** Pour c = 10^0, 10^1, …, 10^7, ajustez x = c + (0, 1, 2), y = 2x + 1 avec `LinearRegression`, en rattrapant la panique dans le harnais du laboratoire. Prédiction : la pente est à moins de 10^-9 de 2 pour c ≤ 10^3 ; à c = 10^5, la pente vaut 2 − 2^-18 et le biais 1,5 ; à c = 10^6, la pente vaut 2 + 2^-11 et le biais 0 ; à c = 10^7, `fit` panique avec « X^T X is singular ». Sur la variable centrée (−1, 0, 1), les mêmes données donnent la pente exactement 2 et le biais 2c + 3, la valeur ajustée en x̄, à 10^-15 près en relatif, pour tout c.
2. **Équations normales contre SVD.** Prenez x₁ = N · (1, 2, 3, 4), x₂ = x₁ + (1, −1, −1, 1) et y = x₁ + x₂ + 1, de sorte que les poids exacts valent 1, 1 et 1, et que κ₂ croisse comme 10 N. Pour N = 10^0, …, 10^7, comparez `fit` avec la voie SVD : `pseudo_inverse` du plan avec sa colonne de uns, à la tolérance max(m, n) · σ₁ · ε de MAT-006, appliquée à y. Prédiction : la plus grande erreur sur les poids de `fit` est sous 10^-9 pour N ≤ 10^3, environ 3 · 10^-5 à N = 10^5 et environ 0,25 à N = 10^7, sans aucune erreur signalée ; la voie SVD reste sous 10^-7 pour tout N.
3. **Le serveur MCP après une panique.** Dans un processus `ix-mcp` jetable, jamais dans un processus partagé, envoyez à `ix_linear_regression` les données de l'étape 1 à c = 10^7, puis un appel `ix_stats` bien posé. Prédiction : aucun des deux appels ne reçoit de réponse, et la sortie d'erreur du serveur montre la panique « X^T X is singular », puis « middleware chain mutex poisoned ».
4. **Le schéma.** Envoyez à `ix_linear_regression` des données bien posées sous la clé `"X"`, comme l'exige le schéma. Prédiction : l'erreur « Missing or invalid field 'x' ».

### Exercice pratique

L'étape 2 prédit une erreur d'environ 0,25 pour les équations normales à N = 10^7, alors que la voie SVD reste sous 10^-7. Estimez les deux à partir du conditionnement.

> *Solution :* κ₂ du plan vaut environ 10 N = 10^8. Les équations normales travaillent avec κ₂² ≈ 10^16, et 10^16 fois ε ≈ 2,2 · 10^-16 est d'ordre 1 : aucun chiffre n'est garanti, et une erreur de 0,25 reste dans cette borne. La voie SVD travaille avec κ₂ ≈ 10^8, ce qui prédit une erreur d'environ 10^8 · 2,2 · 10^-16 ≈ 2 · 10^-8, cohérente avec le fait de rester sous 10^-7. Ce sont des ordres de grandeur tirés de la règle empirique de MAT-003, pas des bornes.

---

## 7. Pièges courants

- **Résoudre les moindres carrés avec un inverse explicite de XᵀX.** Cela élève le conditionnement au carré ; résolvez par QR ou par la SVD.
- **Ajuster des variables décalées brutes.** Horodatages, coordonnées et autres variables loin de 0 par rapport à leur dispersion rendent la colonne de biais presque colinéaire avec elles ; centrez-les d'abord.
- **Prendre « aucune erreur » pour « un ajustement correct ».** À c = 10^6, `fit` devrait renvoyer une réponse fausse sans le moindre avertissement.
- **Laisser un échec numérique paniquer dans un serveur.** Renvoyez plutôt une erreur, et ne laissez jamais une panique se propager pendant qu'un verrou est tenu : le verrou est empoisonné pour tous les appelants suivants.
- **Régulariser le biais.** La pénalité doit rétrécir les pentes, pas le niveau des données.
- **Faire confiance à un schéma sans appel qui l'utilise.** Un schéma et un gestionnaire peuvent diverger d'une seule lettre.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Matrice de plan** | La matrice X de taille n × p, avec une ligne par observation et une colonne par paramètre |
| **Résidu** | r = y − X w, ce que le modèle laisse inexpliqué |
| **Équations normales** | XᵀX w = Xᵀy : le résidu est orthogonal à chaque colonne de X |
| **Identifiabilité** | Les données déterminent les paramètres de façon unique : X est de rang colonne plein |
| **Solution de norme minimale** | w⁺ = X⁺y, la plus courte solution des moindres carrés |
| **Matrice de Läuchli** | [[1, 1], [δ, 0], [0, δ]] : de rang plein, mais fl(XᵀX) est singulière pour δ petit |
| **Centrage** | Soustraire la moyenne d'une variable avant l'ajustement, pour la rendre orthogonale à la colonne de biais |
| **Régression ridge (Tikhonov)** | Minimiser ‖X w − y‖² + λ ‖w‖², de solution unique (XᵀX + λI)⁻¹Xᵀy |
| **Facteur de filtre** | σᵢ²/(σᵢ² + λ), le poids que la ridge donne à la i-ème direction singulière |
| **Empoisonnement d'un mutex** | L'état d'un verrou Rust après la panique d'un thread qui le tenait ; les appels suivants à `lock` renvoient une erreur |

---

## Auto-évaluation

**1. Pourquoi former XᵀX élève-t-il le conditionnement au carré ?**
> Les valeurs singulières de XᵀX sont les σᵢ², donc pour X de rang colonne plein κ₂(XᵀX) = σ_max²/σ_min² = κ₂(X)².

**2. Pourquoi la solution des moindres carrés est-elle unique exactement quand X est de rang colonne plein ?**
> Si X v = 0 avec v ≠ 0, alors w + t v s'ajuste aussi bien que w pour tout t. Si X v = 0 seulement pour v = 0, alors vᵀXᵀX v = ‖X v‖² > 0, donc XᵀX est inversible et les équations normales ont exactement une solution.

**3. Pourquoi la ridge a-t-elle une solution unique pour tout λ > 0, même quand X est de rang déficient ?**
> XᵀX est semi-définie positive, puisque vᵀXᵀX v = ‖X v‖² ≥ 0, donc chaque valeur propre de XᵀX + λI vaut au moins λ > 0, et la matrice est inversible.

**4. Le test `test_linear_regression_multivariate` d'IX passe. Que vous dit-il sur des données décalées ou colinéaires ?**
> Rien : il ajuste des données exactes sur les quatre points de {1, 2}², un plan petit et bien conditionné. Les échecs du §5 demandent un grand décalage ou des colonnes presque colinéaires, qu'aucun test ne couvre.

**Critères de réussite :** Déduire et résoudre les équations normales d'un petit ajustement, décider de l'identifiabilité et donner la solution de norme minimale, expliquer le κ² des équations normales et l'effet du centrage, écrire la solution ridge avec ses facteurs de filtre, et suivre ce que calcule la régression d'IX et ce que sa panique fait à ses appelants.

---

## Bases de recherche

- Å. Björck, *Numerical Methods for Least Squares Problems*, SIAM, 1996 : les équations normales, les résolutions par QR et par SVD, et leur précision
- L. N. Trefethen et D. Bau, *Numerical Linear Algebra*, SIAM, 1997, leçons 11, 18 et 19 : les moindres carrés, leur conditionnement et la stabilité de leurs algorithmes
- P. Läuchli, « Jordan-Elimination und Ausgleichung nach kleinsten Quadraten », *Numerische Mathematik* 3, 1961 : la matrice que ses équations normales perdent
- A. N. Tikhonov, « Solution of incorrectly formulated problems and the regularization method », *Soviet Mathematics Doklady* 4, 1963 : la régularisation
- A. E. Hoerl et R. W. Kennard, « Ridge regression: biased estimation for nonorthogonal problems », *Technometrics* 12, 1970 : la régression ridge
- T. Hastie, R. Tibshirani et J. Friedman, *The Elements of Statistical Learning*, 2e éd., Springer, 2009, §3.4 : les méthodes de rétrécissement
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §5 renvoie à sa ligne
- Expérience : proposée au §6, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
