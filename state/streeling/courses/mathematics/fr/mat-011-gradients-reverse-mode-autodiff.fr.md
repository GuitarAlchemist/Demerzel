---
module_id: mat-011-gradients-reverse-mode-autodiff
department: mathematics
course: Gradients et différentiation automatique en mode inverse
level: intermediate
alchemical_stage: albedo
prerequisites: [mat-004-vectors-matrices-norms]
estimated_duration: "50 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Gradients et différentiation automatique en mode inverse — La règle de dérivation en chaîne, parcourue à rebours sur une bande

> **Département de mathématiques** | Stade : Albedo (Intermédiaire) | Durée estimée : 50 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Calculer des gradients et des jacobiennes, et appliquer la règle de dérivation en chaîne à une composée comme un produit de matrices
- Écrire un calcul sous forme de trace d'évaluation et y propager des dérivées en mode direct
- Exécuter le mode inverse sur une bande, et expliquer pourquoi un seul balayage inverse donne un gradient entier
- Traiter les produits matriciels, la diffusion et les valeurs réutilisées dans une passe arrière
- Utiliser les différences finies comme oracle, et choisir le pas qui équilibre erreur de troncature et erreur d'arrondi
- Retracer ce que garantissent, ou non, la bande de différentiation automatique d'IX, ses tests par différences finies et son outil MCP

---

## 1. Dérivées, gradients et règle de dérivation en chaîne

Pour une fonction f : Rⁿ → R, la **dérivée partielle** ∂f/∂xᵢ est le taux de variation de f quand seul xᵢ bouge, et le **gradient** ∇f(x) = (∂f/∂x₁, …, ∂f/∂xₙ) les rassemble. Il donne la meilleure approximation linéaire f(x + d) ≈ f(x) + ∇f(x) · d pour d petit, et il pointe dans la direction où f croît le plus vite. Pour une fonction F : Rⁿ → Rᵐ, la **jacobienne** J_F(x) est la matrice m × n dont la ligne i est le gradient de la i-ième sortie : c'est la matrice, au sens de MAT-004, de l'application linéaire qui approche le mieux F près de x.

La **règle de dérivation en chaîne** dit que l'approximation linéaire d'une composée est la composée des approximations linéaires : J_{G∘F}(x) = J_G(F(x)) J_F(x), un produit de matrices, comme dans MAT-004. Pour une fonction scalaire g de y = F(x), elle s'écrit ∇(g∘F)(x) = J_F(x)ᵀ ∇g(y) : le gradient par rapport à x est le gradient par rapport à y multiplié par la jacobienne transposée. Chaque méthode de cette leçon est une façon d'organiser ce produit.

### Exercice pratique

Soit f(x, y) = (xy + x)². Calculez ∂f/∂x et ∂f/∂y en (1, 2).

> *Solution :* Posons u = xy + x, de sorte que f = u², avec u = 3 et f = 9 en (1, 2). Par la règle de dérivation en chaîne, ∂f/∂x = 2u · ∂u/∂x = 2u(y + 1) = 18, et ∂f/∂y = 2u · ∂u/∂y = 2u · x = 6.

---

## 2. Traces d'évaluation et mode direct

Un programme calcule f par une suite d'opérations élémentaires, chacune de dérivée connue. Écrite avec un nom par valeur intermédiaire, cette suite est une **trace d'évaluation**, ou liste de Wengert. Pour la fonction du §1 :

v₁ = x, v₂ = y, v₃ = v₁v₂, v₄ = v₃ + v₁, v₅ = v₄², f = v₅.

Le **mode direct** transporte, à côté de chaque valeur vᵢ, sa **tangente** v̇ᵢ, la dérivée de vᵢ dans une direction d'entrée choisie, et la met à jour avec la dérivée locale de chaque opération : v̇₃ = v̇₁v₂ + v₁v̇₂, v̇₄ = v̇₃ + v̇₁, v̇₅ = 2v₄v̇₄. Amorcer les entrées avec une direction d donne en sortie la dérivée directionnelle J d, un **produit jacobienne–vecteur**, pour un petit multiple constant du coût d'une évaluation de f. Un gradient complet de f : Rⁿ → R demande donc n balayages directs, un par entrée.

La différentiation automatique n'est ni une différentiation symbolique ni une différentiation numérique. Elle ne construit jamais de formule pour la dérivée, si bien que les expressions n'enflent pas et que boucles et branchements sont traités au fil de l'exécution ; et elle n'utilise aucun pas, si bien que son résultat est exact à l'arrondi des opérations elles-mêmes près.

### Exercice pratique

Exécutez le mode direct sur la trace ci-dessus en (x, y) = (1, 2) avec l'amorce (ẋ, ẏ) = (1, 0). Que valent v̇₃, v̇₄ et v̇₅ ? Que donne l'amorce (0, 1) ?

> *Solution :* v̇₁ = 1 et v̇₂ = 0. Alors v₃ = 2 et v̇₃ = 1 · 2 + 1 · 0 = 2 ; v₄ = 3 et v̇₄ = 2 + 1 = 3 ; v₅ = 9 et v̇₅ = 2 · 3 · 3 = 18, c'est-à-dire ∂f/∂x. L'amorce (0, 1) donne v̇₃ = 1, v̇₄ = 1 et v̇₅ = 6, c'est-à-dire ∂f/∂y : deux balayages pour deux dérivées partielles.

---

## 3. Le mode inverse et la bande

Le **mode inverse** exécute la trace une fois vers l'avant, en enregistrant sur une **bande** chaque opération et les valeurs dont elle aura besoin, puis parcourt la bande à rebours. Il transporte pour chaque valeur son **adjoint** v̄ᵢ = ∂f/∂vᵢ, la sensibilité de la sortie à cette valeur. La sortie part avec l'adjoint 1. Chaque opération transmet à chacune de ses entrées son propre adjoint multiplié par la dérivée partielle locale, et une valeur utilisée par plusieurs opérations reçoit la somme des contributions : la règle de dérivation en chaîne somme sur tous les chemins qui mènent de la valeur à la sortie.

Un seul balayage inverse donne l'adjoint de chaque entrée, si bien que le gradient entier d'une fonction scalaire coûte un petit multiple constant d'une évaluation de f, quel que soit le nombre d'entrées. En termes matriciels, un balayage inverse calcule un **produit vecteur–jacobienne** v̄ᵀ J, là où le mode direct calcule J d. Le prix est la mémoire : chaque valeur dont une dérivée locale a besoin doit rester sur la bande jusqu'à ce que le parcours arrière l'atteigne. Le mode direct convient aux fonctions à peu d'entrées et beaucoup de sorties, le mode inverse au cas contraire, comme une perte qui dépend de millions de paramètres. Le mode inverse appliqué à un réseau de neurones est la **rétropropagation**.

### Exercice pratique

Exécutez le mode inverse sur la trace du §2 en (1, 2). Donnez les adjoints de v₄, v₃, x et y.

> *Solution :* v̄₅ = 1. Comme v₅ = v₄², v̄₄ = 2v₄ · v̄₅ = 6. La somme v₄ = v₃ + v₁ transmet 6 à v₃ et 6 à v₁. Le produit v₃ = v₁v₂ transmet v̄₃ · v₂ = 12 à v₁ et v̄₃ · v₁ = 6 à v₂. Donc x̄ = 6 + 12 = 18 et ȳ = 6 : les deux dérivées partielles en un seul balayage. x est utilisé deux fois, et son adjoint est la somme des deux contributions.

---

## 4. Tableaux : produits matriciels, diffusion et réutilisation

Le code d'apprentissage automatique applique les mêmes règles à des tableaux entiers. Pour Z = AB, avec A de taille m × k et B de taille k × n, et une perte scalaire L dont l'adjoint par rapport à Z est le tableau m × n noté Z̄, la règle de dérivation en chaîne donne Ā = Z̄ Bᵀ et B̄ = Aᵀ Z̄. Les formes se vérifient d'elles-mêmes : Z̄ Bᵀ est un m × n fois un n × k, la forme de A.

La **diffusion** (broadcasting) permet à une opération de combiner des tableaux de formes différentes en répétant le plus petit : ajouter une ligne b de taille 1 × 3 à chaque ligne d'une matrice 2 × 3 utilise b deux fois. Chaque utilisation renvoie un adjoint, donc b̄ est la somme de Z̄ sur les lignes. La règle générale, souvent appelée **dédiffusion** (unbroadcasting), somme l'adjoint entrant sur chaque axe que la diffusion a créé ou étiré, jusqu'à retrouver la forme de l'opérande. La **réutilisation** est la même règle sous une autre forme : dans x · x, le même tableau est les deux opérandes, chaque opérande reçoit Z̄ multiplié par l'autre, x, et l'adjoint de x est leur somme, 2x multiplié par Z̄ élément par élément.

### Exercice pratique

Soit L = sum(AB) avec A = [[0,1 ; −0,5 ; 1,2] ; [0,3 ; −0,8 ; 0,7]] et B = [[0,5 ; −0,2] ; [0,8 ; 1,1] ; [−0,4 ; 0,3]], écrites ligne par ligne. Calculez Ā et B̄.

> *Solution :* La somme donne l'adjoint 1 à chaque coefficient de Z = AB, donc Z̄ est la matrice 2 × 2 remplie de uns. Ā = Z̄ Bᵀ : les deux lignes de Ā contiennent les sommes des lignes de B, (0,5 − 0,2 ; 0,8 + 1,1 ; −0,4 + 0,3) = (0,3 ; 1,9 ; −0,1). B̄ = Aᵀ Z̄ : les deux colonnes de B̄ contiennent les sommes des colonnes de A, (0,1 + 0,3 ; −0,5 − 0,8 ; 1,2 + 0,7) = (0,4 ; −1,3 ; 1,9). Ce sont les tableaux de `verify_matmul_backward` d'IX (§6).

---

## 5. Les différences finies comme oracle

Avant de faire confiance à une passe arrière écrite à la main, comparez-la avec un quotient de différences. La formule de Taylor donne f(x ± h) = f(x) ± h f′(x) + (h²/2) f″(x) ± (h³/6) f‴(x) + …, si bien que la **différence avant** (f(x + h) − f(x))/h = f′(x) + (h/2) f″(x) + … a une **erreur de troncature** d'ordre h, tandis que dans la **différence centrée** (f(x + h) − f(x − h))/(2h) les termes d'ordre pair s'annulent et l'erreur vaut (h²/6) f‴(x) + …, d'ordre h². Pour f(x) = x³ en 1, la différence centrée vaut exactement 3 + h², et la différence avant 3 + 3h + h².

L'arrondi tire dans l'autre sens. Chaque valeur calculée de f porte une erreur d'environ u|f|, ou davantage si le calcul de f perd lui-même en précision, où u = 2^-53 ≈ 1,1 · 10^-16 est l'unité d'arrondi de MAT-003, et le quotient la divise par h. L'erreur de la différence centrée vaut donc environ E(h) = h²|f‴|/6 + u|f|/h : elle décroît comme h² quand h diminue, puis croît comme 1/h, une courbe en U dont le minimum se situe près de h = (3u|f|/|f‴|)^(1/3), de l'ordre de u^(1/3) ≈ 5 · 10^-6 pour des grandeurs d'ordre 1, avec une erreur de l'ordre de u^(2/3) ≈ 10^-11. Pour la différence avant, le meilleur pas et la meilleure erreur sont tous deux de l'ordre de √u ≈ 10^-8. Une vérification par différence centrée peut donc confirmer une dizaine de chiffres d'un gradient, pas davantage, et elle demande deux évaluations par entrée : un oracle pour les tests, pas un moyen d'entraîner.

Deux cas échappent à ce modèle. Si f est un polynôme de degré au plus 2 en la variable perturbée, alors f‴ = 0 et la différence centrée n'a aucune erreur de troncature : la vérification ne voit que l'arrondi. Et en un point anguleux, où f n'a pas de dérivée, les deux méthodes peuvent légitimement diverger.

### Exercice pratique

Calculez les différences avant et centrée de f(x) = x³ en x = 1 avec h = 0,1, et expliquez pourquoi leurs erreurs sont d'ordres différents. Que donne la différence centrée pour |x| en 0 ?

> *Solution :* (1,331 − 1)/0,1 = 3,31, une erreur de 0,31 = 3h + h², d'ordre h ; (1,331 − 0,729)/0,2 = 3,01, une erreur de 0,01 = h², d'ordre h². Dans les développements de f(x + h) et de f(x − h), les termes d'ordre pair ont le même signe et s'annulent dans la différence, ce qui laisse 2h f′(x) plus des termes en h³. Pour |x| en 0, la différence centrée vaut (h − h)/(2h) = 0 pour tout h, tandis que les différences unilatérales donnent 1 et −1 : |x| n'a pas de dérivée en 0, et 0 n'est qu'un choix admissible parmi d'autres, une convention qu'IX emploie aussi pour le module d'un spectre (§6).

---

## 6. Où en est IX

IX est la bibliothèque d'apprentissage automatique en Rust de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`e35138b9`](https://github.com/GuitarAlchemist/ix/tree/e35138b9d4c707d48f802649a7fcb3f7fc94934d) ; cette leçon documente ce code et ne le modifie pas, et elle n'a pas exécuté les tests d'IX.

**La bande** (`crates/ix-autograd`). Chaque opération empile un [`TapeNode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L22), qui contient son nom, les identifiants de ses entrées et sa valeur, sur une [`Tape`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L41) en ajout seul, que transporte un [`DiffContext`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L90). Les [opérations documentées](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L6) sont `add`, `sub`, `mul`, `sum`, `matmul`, `div_scalar`, `mean` et `variance`, les deux dernières composées des autres ; il n'y a ni `exp`, ni `log`, ni fonction d'activation, si bien qu'à part une opération de FFT derrière un drapeau de fonctionnalité, toute fonction construite à partir d'elles est un polynôme des entrées, `div_scalar` ne divisant que par une constante. [`backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L382) parcourt la bande [dans l'ordre inverse des indices](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L391), un ordre topologique inverse valide puisque les entrées d'une opération sont toujours empilées avant elle, et [ajoute](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L438) chaque contribution à l'adjoint de son entrée, la règle du §3. La passe arrière de `matmul` calcule [Z̄ Bᵀ](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L249) et [Aᵀ Z̄](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L251), et `unbroadcast`, ci-dessous, est la règle du §4. `variance` [élève son résidu au carré](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L365) par `mul(ctx, residual, residual)`, le même identifiant deux fois, et compte sur cette accumulation.

```rust
fn unbroadcast(mut grad: ArrayD<f64>, target_shape: &[usize]) -> ArrayD<f64> {
    while grad.ndim() > target_shape.len() {
        grad = grad.sum_axis(Axis(0));
    }
    for (i, &t) in target_shape.iter().enumerate() {
        if t == 1 && grad.shape()[i] != 1 {
            let summed = grad.sum_axis(Axis(i));
            grad = summed.insert_axis(Axis(i));
        }
    }
    grad
}
```

- **Les erreurs de forme paniquent au lieu de renvoyer une erreur.** Le commentaire de `add` dit [`// ndarray broadcasts automatically; errors if incompatible`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L78), mais `&av + &bv` renvoie un tableau, pas un `Result`, et ne peut donc pas signaler d'erreur : dans la version que déclare IX, 0.17, ndarray panique quand deux formes ne peuvent pas être diffusées, et `sub` et `mul` emploient les mêmes opérateurs. `matmul` [vérifie que ses deux entrées sont de rang 2](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L193) mais pas que les dimensions intérieures concordent, et [`dot`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops.rs#L215) panique quand elles diffèrent. La crate définit une erreur [`ShapeMismatch`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/lib.rs#L83) pour ces cas, et seule l'opération de FFT [la renvoie](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L139). Une matrice 5 × 3 multipliée par une matrice 2 × 1 se termine donc par une panique, et non par un `Err`.
- **Une cible aplatie change la perte sans erreur.** Le [schéma de `ix_autograd_run`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/tools.rs#L1366) accepte chaque entrée en « 1-D, 2-D, or scalar », et [`parse_array_d`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4359) transforme une liste plate en [tableau à une dimension](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4376). [`build_graph`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L56) [soustrait ensuite la cible](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L73) de la prédiction sans vérifier les formes. Avec y en colonne 5 × 1, le résidu est 5 × 1 ; avec les mêmes cinq nombres en y plat de forme 5, la diffusion le rend 5 × 5 et compare chaque prédiction à chaque cible. Sur les entrées du test MCP, la perte devient 0,16316 au lieu de 0,15116, et le gradient de w change avec elle, sans aucune erreur. Le [test](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L47) passe y en colonne et [ne vérifie de la perte](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/tests/autograd_run.rs#L75) que son caractère fini et positif ou nul, ce que remplissent les deux valeurs. Ces nombres viennent d'une transcription, pas d'une exécution ; le §7 les vérifie.
- **Le mode d'exécution ne change rien.** Un `DiffContext` [stocke un `ExecutionMode`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tape.rs#L94), et [`VerifyFiniteDiff`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L41) est documenté comme le mode qui [exécute le vérificateur par différences finies](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L38) sur chaque outil. Aucun code n'agit selon le mode, que seul l'affichage `Debug` imprime : chaque opération empile sur la bande dans tous les modes, y compris `Eager`, documenté comme [« plain values, no tape »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/mode.rs#L25), dont le trait des outils dit que la passe avant [s'exécute en « pure numeric »](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tool.rs#L37). Le vérificateur, [`verify_gradient`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L43), est une fonction du fichier de tests, pas de la bibliothèque, et en dehors de sa propre définition, le seul code qui nomme `VerifyFiniteDiff` est un test qui [vérifie ses prédicats](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L108). `ix_autograd_run` [s'exécute toujours en `Train`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-agent/src/handlers.rs#L4314).
- **Les tests par différences finies ne peuvent pas voir l'erreur de troncature.** Les 17 vérifications exécutées par défaut utilisent ε = 10^-6, proche du meilleur pas centré du §5, et une tolérance absolue de 10^-5, relâchée à 10^-4 dans cinq d'entre elles ; les commentaires des tests de la [variance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L628) et de l'[erreur quadratique moyenne](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L718) invoquent la profondeur de la chaîne. Or chaque fonction qu'ils vérifient, restreinte au seul élément perturbé, est un polynôme de degré au plus 2 : sommes, produits de deux facteurs, un produit matriciel, une moyenne, une variance, une erreur quadratique. Pour une telle fonction, la différence centrée est exacte à l'arrondi près, quelle que soit la profondeur de la chaîne, si bien que les tests ne mesurent que l'arrondi, environ u|f|/ε ≈ 10^-10 pour des valeurs d'ordre 1, bien en dessous des deux tolérances. La seule vérification non polynomiale, [`verify_rfft_magnitude_backward`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L887), se trouve derrière la fonctionnalité [`fft-autograd`](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/tests/finite_diff.rs#L885), qu'un seul job de CI [active](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/.github/workflows/ci.yml#L111).
- **Un point anguleux reçoit une convention.** La passe arrière de `rfft_magnitude` [met le gradient à 0](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/ops_fft.rs#L152) partout où un module est inférieur à 10^-15, le choix du §5 pour |x| en 0. Son commentaire parle de modules exactement nuls ; le seuil annule aussi le gradient d'un module de 10^-16, qui ne l'est pas.
- **Chaque outil ignore l'adjoint amont.** Les quatre outils différentiables, pour la [régression linéaire](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L139), la [variance](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_variance.rs#L64), la [moyenne](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/stats_mean.rs#L60) et l'[erreur quadratique](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/mse_loss.rs#L109), reçoivent les gradients amont dans un `_out_grads` inutilisé et [amorcent leur propre sortie à 1](https://github.com/GuitarAlchemist/ix/blob/e35138b9d4c707d48f802649a7fcb3f7fc94934d/crates/ix-autograd/src/tools/linear_regression.rs#L144). Au sein d'un balayage inverse plus long, la règle du §3 multiplie par l'adjoint entrant ; ces outils renvoient toujours le gradient de leur propre sortie, comme si c'était la perte finale. `ix_autograd_run` exécute un outil à la fois, il n'est donc pas touché aujourd'hui ; un pipeline qui enchaînerait des outils le serait.

Le vérificateur compare chaque gradient analytique avec une différence centrée et une tolérance absolue :

```rust
        for (flat_idx, &analytical) in grad_values.iter().enumerate().take(input.len()) {
            let f_plus = perturbed_loss(&forward, &inputs, name, flat_idx, epsilon);
            let f_minus = perturbed_loss(&forward, &inputs, name, flat_idx, -epsilon);
            let numerical = (f_plus - f_minus) / (2.0 * epsilon);
            let diff = (numerical - analytical).abs();
            if diff > tolerance {
```

Corriger tout cela revient aux responsables d'IX ; cette leçon se contente de le décrire.

### Exercice pratique

Pourquoi un y plat de longueur 5 donne-t-il un résidu 5 × 5 dans `build_graph`, et que calcule alors la perte ?

> *Solution :* La prédiction a la forme 5 × 1 et un y plat la forme 5. La diffusion traite d'abord y comme une ligne 1 × 5, puis étire les deux en 5 × 5, si bien que le coefficient (i, j) du résidu vaut ŷᵢ − yⱼ. La moyenne de ses 25 carrés compare chaque prédiction à chaque cible, et non chacune à la sienne : avec ŷ = (0,16 ; 0,58 ; −0,31 ; 0,09 ; 0,66) et le y du test, elle vaut 0,16316 au lieu de 0,15116. Rien n'échoue, car les formes sont compatibles ; seule une vérification des formes là où les données entrent, ou un test sur la valeur, le détecte.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire Learn, qui épingle IX au même commit. Rien n'y est une mesure : les prédictions sont écrites avant toute exécution, et une version ultérieure de cette leçon en rapportera les résultats. Chaque étape s'exécute dans le propre processus du laboratoire, jamais contre un serveur MCP en fonctionnement.

1. **L'exemple travaillé.** Construisez f(x, y) = (xy + x)² avec `input`, `mul`, `add`, `mul` et `sum` sur les tenseurs à un élément x = [1] et y = [2], et appelez `backward` avec l'amorce 1. Prédiction : les adjoints de x et de y valent exactement 18 et 6.
2. **La courbe en U.** Construisez f(x) = sum(x · x · x) avec deux opérations `mul` en x = [1] ; son gradient en mode inverse vaut exactement 3. Comparez-le aux différences centrées et avant de la valeur calculée par la bande pour h = 10^-1, 10^-2, …, 10^-12. Prédiction : l'erreur centrée égale h² à 1 % près pour h de 10^-1 à 10^-3, atteint son minimum, inférieur à 10^-9, entre h = 10^-7 et 10^-5, et dépasse 10^-6 en h = 10^-12 ; l'erreur avant est proche de 3h pour les grands h et atteint son minimum entre h = 10^-9 et 10^-7, à une valeur plus grande que le minimum centré.
3. **L'angle mort quadratique.** Refaites l'étape 2 avec sum(x · x), dont le gradient vaut 2. Prédiction : pas de branche en h² ; pour h de 10^-1 à 10^-6, l'erreur centrée reste inférieure à 10^-10.
4. **Le produit matriciel.** Avec les tableaux de `verify_matmul_backward`, calculez le gradient de sum(AB). Prédiction : les deux lignes de Ā valent (0,3 ; 1,9 ; −0,1) et les deux colonnes de B̄ valent (0,4 ; −1,3 ; 1,9), à 10^-15 près.
5. **Une cible aplatie.** Appelez le gestionnaire `autograd_run` avec les entrées du test MCP, une fois avec y en colonne et une fois à plat. Prédiction : les pertes 0,15116 et 0,16316, à 10^-12 près, la seconde sans erreur et avec un gradient de w différent.
6. **Des formes incompatibles.** Sous `std::panic::catch_unwind`, appelez `matmul` sur une matrice 5 × 3 et une matrice 2 × 1, et `add` sur une matrice 2 × 3 et une matrice 2 × 2. Prédiction : les deux appels paniquent, et aucun ne renvoie de `Err`.
7. **Les modes.** Construisez le graphe de régression linéaire dans chacun des quatre modes. Prédiction : la bande contient 10 nœuds dans chaque mode, et aucune vérification par différences finies ne s'exécute.

### Exercice pratique

À l'étape 2, avec f(x) = x³ en 1, le modèle d'erreur du §5 s'écrit E(h) = h² + u/h. Quel h le minimise, et quelle erreur prédit-il au fond de la courbe ?

> *Solution :* E′(h) = 2h − u/h² s'annule quand h³ = u/2 = 2^-54, donc h = 2^-18 ≈ 3,8 · 10^-6. Là, E = 2^-36 + 2^-35 = 3 · 2^-36 ≈ 4,4 · 10^-11. La grille de l'étape 2 encadre ce point par h = 10^-6 et 10^-5, ce qui explique que la prédiction place le minimum entre 10^-7 et 10^-5, en dessous de 10^-9 : le modèle donne la taille de l'erreur d'arrondi, pas sa valeur exacte.

---

## 8. Pièges courants

- **Écraser au lieu d'accumuler.** Une valeur utilisée deux fois doit recevoir la somme de ses adjoints ; écraser garde un seul chemin et divise en silence par deux la dérivée de x · x.
- **Oublier de dédiffuser.** L'adjoint d'un opérande diffusé doit être sommé jusqu'à retrouver la forme de cet opérande.
- **Choisir le pas des différences finies à l'aveugle.** Trop grand, la troncature domine ; trop petit, c'est l'arrondi ; prenez environ u^(1/3) pour les différences centrées et √u pour les différences avant, à l'échelle de x.
- **Ne vérifier que des fonctions quadratiques.** Leurs différences centrées sont exactes à l'arrondi près, si bien que la vérification ne rencontre jamais l'erreur de troncature ; incluez une fonction cubique ou transcendante.
- **Vérifier en un point anguleux.** Au coin de |x|, d'un maximum ou d'un module, la dérivée n'existe pas, et différences finies et différentiation automatique peuvent légitimement différer.
- **Faire confiance à la diffusion silencieuse.** Des formes compatibles mais non voulues donnent un nombre faux au lieu d'une erreur ; vérifiez les formes là où les données entrent.
- **Perdre l'adjoint amont.** Une passe arrière au sein d'une chaîne plus longue doit multiplier par l'adjoint qu'elle reçoit ; amorcer à 1 n'est juste que pour la perte finale.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **Gradient** | Le vecteur des dérivées partielles d'une fonction scalaire, qui pointe là où elle croît le plus vite |
| **Jacobienne** | La matrice des dérivées partielles d'une fonction vectorielle, la matrice de sa meilleure approximation linéaire |
| **Règle de dérivation en chaîne** | La jacobienne d'une composée est le produit des jacobiennes |
| **Trace d'évaluation** | La suite des opérations élémentaires qu'exécute un programme, aussi appelée liste de Wengert |
| **Tangente** | En mode direct, la dérivée d'une valeur intermédiaire dans une direction d'entrée choisie |
| **Adjoint** | En mode inverse, la dérivée de la sortie par rapport à une valeur intermédiaire |
| **Mode direct** | Propage les tangentes en même temps que l'évaluation ; un balayage donne un produit jacobienne–vecteur |
| **Mode inverse** | Parcourt la trace à rebours ; un balayage donne un produit vecteur–jacobienne, le gradient entier d'un scalaire |
| **Bande** | L'enregistrement de la trace et des valeurs dont le balayage inverse a besoin |
| **Dédiffusion** | La sommation d'un adjoint sur les axes que la diffusion a étendus, jusqu'à la forme de l'opérande |
| **Différence centrée** | (f(x + h) − f(x − h))/(2h), avec une erreur de troncature d'ordre h² et une erreur d'arrondi d'ordre u/h |

---

## Auto-évaluation

**1. Une perte dépend de 10^6 paramètres. Pourquoi préfère-t-on le mode inverse au mode direct et aux différences finies pour calculer son gradient ?**
> Un seul balayage inverse donne les 10^6 dérivées partielles pour un petit multiple constant du coût d'une évaluation. Le mode direct demande un balayage par paramètre, et les différences centrées demandent 2 · 10^6 évaluations et ne confirment qu'une dizaine de chiffres. Le prix du mode inverse est la mémoire : la bande conserve les valeurs intermédiaires.

**2. Sur une bande, pourquoi x · x reçoit-il l'adjoint 2x, et que renverrait un parcours qui écraserait les adjoints au lieu de les additionner ?**
> Les deux entrées de l'opération sont le même nœud, et chacune reçoit l'adjoint entrant multiplié par l'autre facteur, x ; leur somme vaut 2x. Un parcours qui écraserait garderait une seule contribution et renverrait x, la moitié de la dérivée.

**3. Les tests par différences finies d'IX passent. Qu'établissent-ils ?**
> Que les passes arrière concordent avec des différences centrées, aux points choisis et dans la tolérance, pour des sommes, des produits, un produit matriciel, des moyennes, des variances et des erreurs quadratiques. Ces fonctions sont de degré au plus 2 en chaque élément, si bien que la différence centrée est exacte à l'arrondi près : les tests détectent une formule de dérivée fausse, mais ils n'exercent jamais l'erreur de troncature, les fonctions non polynomiales en dehors du test de FFT soumis à une fonctionnalité, ni les erreurs de forme.

**4. `ix_autograd_run` renvoie une perte finie et positive ou nulle pour vos données. Pouvez-vous lui faire confiance ?**
> Pas sans vérifier les formes. Un y plat se diffuse contre la prédiction 5 × 1 en un résidu 5 × 5 et donne une autre perte finie et positive ou nulle, 0,16316 au lieu de 0,15116 sur les données du test. Envoyez y en colonne n × 1, et comparez la forme de la prédiction renvoyée à celle de y.

**Critères de réussite :** Calculer des gradients et des jacobiennes et appliquer la règle de dérivation en chaîne, exécuter à la main les modes direct et inverse sur une trace d'évaluation, établir les règles de la passe arrière pour les produits matriciels, la diffusion et la réutilisation, choisir un pas de différences finies à partir de l'équilibre entre troncature et arrondi, et retracer ce que garantissent la bande, les tests et l'outil MCP d'IX.

---

## Bases de recherche

- R. E. Wengert, « A simple automatic derivative evaluation program », *Communications of the ACM* 7, 1964 : la trace d'évaluation et le mode direct
- S. Linnainmaa, « Taylor expansion of the accumulated rounding error », *BIT Numerical Mathematics* 16, 1976 : l'accumulation inverse des dérivées
- D. E. Rumelhart, G. E. Hinton et R. J. Williams, « Learning representations by back-propagating errors », *Nature* 323, 1986 : la rétropropagation
- A. Griewank et A. Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, 2e éd., SIAM, 2008 : bandes, adjoints et coût d'un balayage inverse
- A. G. Baydin, B. A. Pearlmutter, A. A. Radul et J. M. Siskind, « Automatic differentiation in machine learning: a survey », *Journal of Machine Learning Research* 18, 2018 : les modes direct et inverse, et ce qui les distingue des différentiations symbolique et numérique
- P. E. Gill, W. Murray et M. H. Wright, *Practical Optimization*, Academic Press, 1981 : le choix des pas de différences finies
- Code source d'IX au commit `e35138b9d4c707d48f802649a7fcb3f7fc94934d` : chaque fait de code du §6 renvoie à sa ligne
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03)
