---
module_id: mus-021-pitch-class-dft-magnitudes-phases-homometry
department: music
course: La TFD des classes de hauteurs — modules, phases et homométrie
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites: [mus-020-set-classes-interval-vectors-prime-forms, mat-021-fourier-analysis-signals]
estimated_duration: "75 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# La TFD des classes de hauteurs — Ce que gardent les modules, ce qu'ajoutent les phases

> **Département de musique** | Stade : Citrinitas (Intermédiaire à avancé) | Durée estimée : 75 minutes

## Objectifs

À la fin de cette leçon, vous saurez :
- Calculer les coefficients de Fourier d'un ensemble de classes de hauteurs et les lire comme des sommes de points sur un cercle
- Démontrer que la transposition et l'inversion conservent les modules, dire ce qu'elles font aux phases, et dire ce que M5 fait aux modules
- Établir le lemme de Lewin, et s'en servir pour expliquer pourquoi des ensembles en relation Z partagent tous leurs modules
- Nommer les ensembles qui maximisent chacun des six modules, et prédire d'après la symétrie d'un ensemble quels coefficients s'annulent
- Comparer deux ensembles par leurs phases, et dire exactement ce qu'une similarité de phase égale à 1 montre et ne montre pas
- Retracer ce que GA calcule pour chacun de ces points, et où ses noms, sa documentation et ses tests disent autre chose

---

## 1. Un ensemble comme signal

Numérotez les classes de hauteurs de do = 0 à si = 11, comme le fait MUS-020, et écrivez un ensemble de classes de hauteurs A comme un signal de 12 échantillons : 1 à chaque classe de hauteurs de A, 0 ailleurs. MAT-021 définit la transformée de Fourier discrète d'un tel signal. Pour un ensemble, la somme porte sur ses notes :

X_k(A) = Σ_(x ∈ A) e^(−2πikx/12), pour k = 0, 1, …, 11.

Chaque note apporte un point du cercle unité, à un angle de −30k·x degrés, et X_k additionne ces points. Pour k = 1, les notes gardent leur place sur le cercle chromatique. Pour k = 5, la note x prend la place de 5x, et le cercle devient le cycle des quartes : do, fa, si♭, mi♭ et ainsi de suite. X_0 est le nombre de notes, n. Le signal est réel, donc X_(12−k) est le conjugué de X_k (MAT-021 §1), et les coefficients pour k = 0 à 6 portent toute l'information. Cette leçon n'utilise que ceux-là.

Un coefficient est grand quand ses points se regroupent et petit quand ils s'étalent autour du cercle. Son **module** |X_k| mesure à quel point ils se regroupent, et sa **phase**, l'angle φ_k de X_k, dit où. Pour do majeur {0, 4, 7} et k = 5, les trois points se placent à 0°, 120° et 30° (do, mi et sol, puisque −600° et −1050° valent 120° et 30° sur le cercle), et leur somme est X_5 = 1,366 + 1,366i, de module 1,932 et de phase 45°.

### Exercice pratique

Calculez tous les coefficients du triton do fa♯, {0, 6}.

> *Solution :* X_k = 1 + e^(−2πi·6k/12) = 1 + e^(−πik) = 1 + (−1)^k. Les coefficients valent 2 pour k pair et 0 pour k impair.

---

## 2. Transposition, inversion et M5

Transposer A de t envoie chaque note x sur x + t, et son terme devient e^(−2πik(x+t)/12) = e^(−2πikt/12) e^(−2πikx/12). Chaque terme est multiplié par le même facteur, donc

X_k(T_t A) = e^(−2πikt/12) X_k(A).

C'est le **théorème de décalage**. Le module ne change pas, et la phase tourne de −30kt degrés : chaque coefficient tourne à sa propre vitesse, k fois plus vite que le premier. L'inversion I0 envoie x sur −x, ce qui remplace chaque terme par son conjugué, donc X_k(I0 A) est le conjugué de X_k(A) : le module reste, et la phase change de signe. Ces opérations mènent de n'importe quel ensemble d'une classe d'ensembles à n'importe quel autre, donc les six modules |X_1| à |X_6| sont les mêmes pour tous les ensembles d'une classe.

M5, qui multiplie chaque classe de hauteurs par 5, ne fait pas partie de ces opérations, mais son effet est simple. Elle envoie le terme de la note x sur e^(−2πik·5x/12), qui est le terme de x dans X_5k. Donc X_k(M5 A) = X_(5k mod 12)(A). Pour k = 1 à 6, 5k mod 12 vaut 5, 10, 3, 8, 1 et 6, et |X_10| = |X_2|, |X_8| = |X_4|. M5 échange |X_1| et |X_5| et garde les autres modules. C'est le versant spectral du §2 de MUS-020, où M5 échange les décomptes des classes d'intervalles 1 et 5. Le pentacorde chromatique do do♯ ré mi♭ mi a |X_1| = 3,732 et |X_5| = 0,268. Son image par M5, la gamme pentatonique, a l'inverse.

Une vérification en Python sur les 4 096 ensembles et les 12 transpositions trouve le théorème de décalage, la conjugaison et la règle de M5 exacts aux arrondis près, avec des écarts inférieurs à 10⁻¹³.

### Exercice pratique

Pour do majeur, X_5 a une phase de 45°. Sans additionner aucun terme, trouvez la phase de X_5 pour ré majeur et pour do mineur.

> *Solution :* Ré majeur est T2 de do majeur, donc la phase tourne de −30 × 5 × 2 = −300°, soit +60° : 105°. Do mineur {0, 3, 7} est I7 de do majeur, puisque 7 − {0, 4, 7} = {7, 3, 0}, et I7 est I0 suivie de T7. I0 change 45° en −45°, et T7 le fait tourner de −30 × 5 × 7 = −1050°, soit +30° : −15°. Le module reste 1,932 dans les deux cas.

---

## 3. Le lemme de Lewin et l'homométrie

Multipliez X_k par son conjugué :

|X_k|² = Σ_(x ∈ A) Σ_(y ∈ A) e^(−2πik(x−y)/12).

Les n termes où x = y donnent n. Chaque paire de notes distinctes apparaît deux fois, comme x − y et comme y − x, et les deux termes ont pour somme 2 cos(2πk(x − y)/12). Ce cosinus ne dépend que de la classe d'intervalles d de la paire, sous la forme cos(πkd/6). En regroupant les paires par classe d'intervalles :

|X_k|² = n + 2 Σ_(d=1..6) ICV_d cos(πkd/6),

où ICV_d est le décompte de la classe d'intervalles d dans le vecteur de classes d'intervalles du §2 de MUS-020. C'est le **lemme de Lewin**, d'après Lewin (1959). Pour do majeur, n = 3 et le vecteur est <001110>. Pour k = 3, les cosinus pour d = 3, 4 et 5 sont cos 270° = 0, cos 360° = 1 et cos 450° = 0, donc |X_3|² = 3 + 2 = 5 et |X_3| = 2,236.

La formule se lit aussi à l'envers. Ses sept équations, pour k = 0 à 6, forment une transformée en cosinus, et on peut les résoudre pour retrouver n et les six décomptes. Les sept modules |X_0| à |X_6| et la paire (n, vecteur) portent donc la même information : les 4 096 ensembles ont 201 profils distincts de sept modules et 201 paires distinctes, en bijection. n compte des deux côtés : l'ensemble vide et une note seule partagent le vecteur <000000> mais pas n, et sans |X_0| les six modules |X_1| à |X_6| ne donnent que 118 profils, et ne distinguent même pas un ensemble de son complémentaire, dont les coefficients sont −X_k pour tout k autre que 0, puisque ceux de l'agrégat valent 0.

Deux ensembles sont **homométriques** quand ils ont les mêmes sept modules |X_0| à |X_6|, c'est-à-dire la même taille et les mêmes |X_1| à |X_6|. Des classes d'ensembles en relation Z (§5 de MUS-020) ont la même taille et le même vecteur, donc par le lemme de Lewin elles partagent les sept. Les tétracordes à tous les intervalles 4-Z15 (0146) et 4-Z29 (0137) ne peuvent être distingués par aucune fonction des modules, et il en va de même pour les 23 paires en relation Z.

### Exercice pratique

Calculez |X_5| de do majeur à partir de son vecteur, et comparez avec le §1.

> *Solution :* Pour k = 5, les cosinus pour d = 3, 4 et 5 sont cos 450° = 0, cos 600° = −0,5 et cos 750° = 0,866. Donc |X_5|² = 3 + 2(−0,5 + 0,866) = 3,732, et |X_5| = 1,932, comme au §1.

---

## 4. Six qualités

Chaque module mesure une sorte de régularité. Quinn (2006–07) a lu les six modules comme six qualités harmoniques, chacune jugée par la proximité d'un ensemble avec les ensembles qui la maximisent. Une recherche en Python sur tous les ensembles de chaque taille trouve ces ensembles :

- **k = 1**, les clusters chromatiques : do do♯ ré parmi les ensembles de trois notes, avec 2,732, et l'hexacorde chromatique parmi ceux de six, avec 3,864.
- **k = 2**, deux clusters à un triton l'un de l'autre : do fa♯ avec 2, le seul ensemble de deux notes à l'atteindre à transposition près, do do♯ fa♯ sol avec 3,464, et do do♯ ré fa♯ sol la♭ avec 4.
- **k = 3**, le cycle des tierces majeures : l'accord parfait augmenté avec 3, et la gamme hexatonique do do♯ mi fa sol♯ la avec 4,243.
- **k = 4**, le cycle des tierces mineures : l'accord de septième diminuée et la gamme octatonique, tous deux avec 4.
- **k = 5**, les chaînes de quintes : do ré sol avec 2,732, la gamme pentatonique avec 3,732, do ré mi fa sol la parmi ceux de six, avec 3,864, et parmi les ensembles de sept notes la collection diatonique, avec 3,732 elle aussi.
- **k = 6**, la gamme par tons, avec 6. Les classes de hauteurs paires et impaires forment les deux gammes par tons, et X_6 = Σ_(x ∈ A) (−1)^x compte les notes paires d'un ensemble moins ses notes impaires.

Les modules de quelques ensembles familiers montrent les qualités côte à côte :

| Ensemble | n | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | k = 6 |
|---|---|---|---|---|---|---|---|
| Accord parfait majeur do mi sol | 3 | 0,518 | 1 | 2,236 | 1,732 | 1,932 | 1 |
| Accord parfait augmenté do mi sol♯ | 3 | 0 | 0 | 3 | 0 | 0 | 3 |
| Cluster chromatique do do♯ ré | 3 | 2,732 | 2 | 1 | 0 | 0,732 | 1 |
| Triton do fa♯ | 2 | 0 | 2 | 0 | 2 | 0 | 2 |
| Septième de dominante do mi sol si♭ | 4 | 0,518 | 1 | 1,414 | 2,646 | 1,932 | 2 |
| Septième majeure do mi sol si | 4 | 0,518 | 1,732 | 2,828 | 1 | 1,932 | 0 |
| Septième diminuée do mi♭ sol♭ la | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| Pentatonique do ré mi sol la | 5 | 0,268 | 1 | 1 | 1 | 3,732 | 1 |
| Gamme par tons | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| Hexatonique do do♯ mi fa sol♯ la | 6 | 0 | 0 | 4,243 | 0 | 0 | 0 |
| Gamme diatonique de do majeur | 7 | 0,268 | 1 | 1 | 1 | 3,732 | 1 |
| Octatonique do do♯ mi♭ mi fa♯ sol la si♭ | 8 | 0 | 0 | 0 | 4 | 0 | 0 |

Aucun nombre seul ne dit donc si un accord sonne *par tons* ou *par quintes*, mais un nombre par qualité le dit. C7 et Cmaj7 sont aussi proches l'un que l'autre des quintes, avec 1,932 pour k = 5, mais C7 penche vers la gamme par tons, avec 2 pour k = 6, contre 0 pour Cmaj7, qui penche vers l'accord parfait augmenté, avec 2,828 pour k = 3.

Les zéros découlent de la symétrie. Si T_p envoie A sur lui-même, le théorème de décalage donne X_k(A) = e^(−2πikp/12) X_k(A), donc X_k = 0 sauf si kp est un multiple de 12. Parmi k = 1 à 6, l'accord parfait augmenté et la gamme hexatonique, fixés par T4, ne peuvent être non nuls que pour k = 3 et 6. La septième diminuée et la gamme octatonique, fixées par T3, seulement pour k = 4. La gamme par tons, fixée par T2, seulement pour k = 6, et le triton, fixé par T6, seulement pour les k pairs. La vérification en Python ne trouve aucune exception parmi les 4 096 ensembles. La réciproque est fausse : aucune transposition ne fixe Cmaj7, et pourtant X_6 = 0, puisqu'il a deux notes paires et deux impaires.

### Exercice pratique

Pourquoi |X_6| de la gamme par tons do ré mi fa♯ sol♯ si♭ est-il la plus grande valeur qu'un ensemble puisse atteindre ?

> *Solution :* Ses notes sont les classes de hauteurs paires, donc chaque terme e^(−2πi·6x/12) = (−1)^x vaut +1. Les six termes s'ajoutent en phase, et |X_6| = 6. Aucun ensemble ne fait mieux : X_6 est le nombre de notes paires moins le nombre de notes impaires, au plus 6 en valeur absolue.

---

## 5. Ce qu'ajoutent les phases

Les modules ne distinguent pas un ensemble de ses transpositions et de ses inversions, ni une classe d'une paire en relation Z de l'autre. Les phases le peuvent. D'après le §2, transposer de t fait tourner la phase de X_k de −30kt degrés, tous les coefficients à la fois, chacun à sa propre vitesse. Pour comparer B à A à transposition près, faites tourner les phases de B pour chaque t et mesurez à quel point elles s'alignent sur celles de A, en pondérant chaque coefficient par les deux modules :

S(A, B) = max sur t de Σ_(k=1..6) |X_k(A)| |X_k(B)| cos(φ_k(A) − φ_k(B) + 30°·kt) / Σ_(k=1..6) |X_k(A)| |X_k(B)|.

On note t* les valeurs de t qui atteignent le maximum. Si B = T_u A, chaque cosinus vaut 1 en t = −u, donc S = 1. Do majeur contre ré majeur donne S = 1 en t = 10, la transposition qui ramène ré majeur sur do majeur. S ne change pas quand l'un ou l'autre ensemble est transposé. Do majeur contre do mineur donne S = 0,5714, parce qu'une inversion change le signe des phases au lieu de les faire tourner. Comparer A aussi à l'inversion de B, dont les coefficients sont les conjugués de ceux de B, donne S_TnI(A, B), la plus grande des deux valeurs. Elle vaut 1 pour do majeur et do mineur. Sur les 23 paires en relation Z, S_TnI reste inférieur à 1, au plus 0,6667 : les phases séparent les ensembles que les modules ne séparent pas.

**S = 1 ne veut pas dire une transposition.** Chaque terme de S, dans la somme comme au dénominateur, est nul sauf si les deux ensembles ont un coefficient non nul pour ce k, et les modules ne font que pondérer les cosinus. S atteint 1 dès que, pour un t, chaque différence de phase sur les coefficients partagés s'annule. Prenez do ré mi et l'accord parfait augmenté do mi sol♯. Pour k = 1 à 6, les coefficients de l'accord parfait augmenté sont 0, 0, 3, 0, 0 et 3, et ceux de do ré mi sont 1 − 1,732i, 0, 1, 0, 1 + 1,732i et 3. Seuls k = 3 et k = 6 comptent, et là les deux ensembles ont une phase de 0. En t = 0 les deux cosinus valent 1, et S = (1 × 3 + 3 × 3) / (1 × 3 + 3 × 3) = 1, en t = 4 et t = 8 aussi, puisque T4 et T8 fixent l'accord parfait augmenté. Pourtant do ré mi, (024), et do mi sol♯, (048), sont des classes d'ensembles différentes. Quand aucun k n'a ses deux coefficients non nuls, comme pour l'accord parfait augmenté contre la septième diminuée, S vaut 0/0. GA fixe alors S à 0, et à 1 seulement quand chacun des deux ensembles est l'ensemble vide ou l'agrégat. Les décomptes du paragraphe suivant suivent cette convention : parmi les paires qu'ils parcourent, 268 sont de ce type et reçoivent S = 0.

Les zéros ne sont même pas nécessaires. Le pentacorde chromatique do do♯ ré mi♭ mi et la gamme pentatonique do ré mi sol la n'ont aucun coefficient nul, et leurs modules diffèrent (§2), mais leurs phases s'accordent en t = 0, et S = 1. Sur toutes les paires de types Tn distincts, en laissant de côté l'ensemble vide et l'agrégat, 270 paires de même taille et 1 230 paires de tailles différentes atteignent S = 1. Parmi les accords : Csus2 et C9 en t = 0, et Cmaj7 et Cdim7 en t = 1, 4, 7 et 10.

S = 1 donne bien une transposition quand les deux ensembles ont en plus la même taille et les mêmes modules. Les phases s'accordent alors sur chaque coefficient non nul, donc les coefficients de A égalent ceux d'une transposition de B pour k = 0 à 6, et par conjugaison pour tout k. La TFD inverse ramène des coefficients égaux à des ensembles égaux.

### Exercice pratique

Montrez que S = 1 entre la note seule do et le triton do fa♯, et trouvez tous les t qui l'atteignent.

> *Solution :* {0} a X_k = 1 pour tout k, de phase 0. D'après le §1, {0, 6} a X_k = 2 pour k pair et 0 pour k impair. Seuls k = 2, 4 et 6 comptent, tous de phase 0 des deux côtés, donc en t = 0, S = (2 + 2 + 2) / (2 + 2 + 2) = 1. En t = 6, chaque coefficient tourne de 180k degrés, un nombre entier de tours pour k pair, donc S = 1 là aussi. Un ensemble d'une note et un ensemble de deux atteignent S = 1, en t = 0 et t = 6.

---

## 6. Où en est GA

GA est la bibliothèque de théorie musicale et le chatbot de l'écosystème GuitarAlchemist. Les faits ci-dessous sont lus dans son code au commit [`40d3374`](https://github.com/GuitarAlchemist/ga/tree/40d337479af36d987df3f06c8c638ffd35f13458), la branche `main` de GA le 2026-10-06 ; cette leçon documente ce code sans le modifier, et elle n'a exécuté ni GA ni ses tests. Les nombres ci-dessous viennent d'une transcription en Python, ligne à ligne, du code de GA nommé.

**Les modules et les phases viennent de la forme première.** [`SetClass.GetFourierCoefficients`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L157) calcule la TFD de [`GetSpectralPrimeForm()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L120-L123), la forme première, et non de l'ensemble à partir duquel la classe a été construite. Les modules sont les mêmes pour tous les ensembles de la classe (§2), donc [`GetMagnitudeSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L190) est juste en tant que propriété de la classe. Son test, [`GetMagnitudeSpectrum_IsInvariantUnderTransposition`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L105), construit une classe à partir de do mi sol et une autre à partir de ré fa♯ la. Les deux se ramènent à la forme première (037), donc les deux spectres viennent des mêmes 12 nombres, et le test passerait même si la TFD ne conservait pas les modules par transposition. [`GetPhaseSpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L213) renvoie lui aussi les phases de la forme première, les mêmes pour do majeur, ré majeur et do mineur, bien que [son résumé](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L211) dise « Phase encodes rotational alignment on the chromatic circle ». Le code d'alignement plus récent de GA fait le choix inverse : ses coefficients viennent du [« ACTUAL chroma (not the prime form — phases carry the transposition, which is the point) »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L75-L76) de l'ensemble. Au commit `40d3374`, aucun code de GA n'appelle `GetPhaseSpectrum`.

**Le centroïde et la distance.** [`GetSpectralCentroid`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L230) fait la moyenne de k sur les 12 cases, pondérée par |X_k|. Comme |X_(12−k)| = |X_k|, les cases se répondent en miroir autour de 6, et le centroïde se réduit à 6(1 − n / Σ|X_k|), une mesure de la part du module total qui se trouve hors de la case 0 (voir l'exercice ci-dessous). La transcription retrouve cette formule sur les 223 classes non vides à moins de 10⁻¹³ près. Le centroïde va de 0 pour l'agrégat à 5,5 pour une note seule, la valeur que vérifie [le test de GA](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SetClassTests.cs#L129-L139), et [`UnifiedModeService`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Unified/UnifiedModeService.cs#L133) le lit. [`GetSpectralDistance`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SetClass.cs#L257) additionne les écarts absolus de module sur les 12 cases, donc k = 1 à 5 comptent deux fois et k = 0 et 6 une fois. [`SetClassSpectralIndex.GetNearestBySpectrum`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L16) ordonne les classes selon la même distance, et d'après le §3 chacune des 46 classes en relation Z trouve sa partenaire en premier, seule à distance 0 aux arrondis près. La méthode écarte la source [par référence](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Services/Atonal/SetClassSpectralIndex.cs#L26) : une classe prise dans `SetClass.Items` est écartée, mais une classe construite à neuf avec `new SetClass(...)` est égale à sa copie dans l'index sans être le même objet, et revient en premier, à distance exactement 0, sa partenaire en second. Dans la transcription, la distance de la partenaire est un résidu d'arrondi compris entre 9 × 10⁻¹⁵ et 3 × 10⁻¹⁴, jamais exactement 0. Au commit `40d3374`, aucun code de GA n'appelle `GetSpectralDistance` ni `GetNearestBySpectrum`.

**Les étiquettes de l'embedding.** Le commentaire d'en-tête de la partition spectrale du schéma d'embedding de GA affirme [« Per Lewin's Lemma: ICV = |DFT|² »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L654). D'après le §3, les modules au carré sont une transformée en cosinus de la taille et du vecteur, pas le vecteur : do majeur a <001110>, et |X_1|² à |X_6|² valent 0,268, 1, 5, 3, 3,732 et 1. La [note de recherche](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L24) de GA elle-même énonce la relation presque correctement : elle omet la taille. Lues pour un ensemble, où chaque classe de hauteurs compte une fois (et non pour un chroma pondéré de voicing), les étiquettes du schéma pour les six modules nomment les mauvais ensembles pour quatre d'entre eux. Il appelle k = 2 [« Whole-tone structure »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L683), mais la gamme par tons a |X_2| = 0. Il appelle k = 3 [« Diminished structure »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L690), avec une « minor-third cycle affinity », mais l'accord de septième diminuée a |X_3| = 0 et c'est l'accord parfait augmenté qui le maximise. Il appelle k = 4 [« Augmented structure »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L697), l'inverse. Et il appelle k = 6 [« Tritone structure »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L712), mais c'est la gamme par tons qui maximise |X_6| ; parmi les ensembles de deux notes, le triton partage le plus grand |X_6| avec la seconde majeure et la tierce majeure, alors qu'il est seul à atteindre le plus grand |X_2| (§4). Les étiquettes de k = 2 et 6 sont échangées, et celles de k = 3 et 4 aussi. Les étiquettes de k = 1, « Chromatic clumping », et de k = 5, « Diatonic structure », sont justes. Le [§5](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L61) de la note de recherche reprend les étiquettes fausses et les attribue à Quinn, comme « Quinn's quality semantics already documented in the schema ».

**L'alignement de phase.** [`SpectralPhaseAlignment.Similarity`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L49) et [`SimilarityTnI`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L57) calculent les S et S_TnI du §5 à partir des coefficients de l'ensemble lui-même, avec des poids facultatifs, et fixent S à 1 ou à 0 par [convention](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L111-L119) quand le dénominateur s'annule. La transcription retrouve les exemples de la note de recherche : 1 en t = 10 pour do majeur et ré majeur ; 0,5714, et 1 par l'inversion, pour do majeur et do mineur ; 0,3333 et 0,6667 pour 4-Z15 et 4-Z29 ; 0,4000 pour 6-Z17 et 6-Z43. Elle trouve S_TnI inférieur à 1 sur les 23 paires en relation Z, au plus 0,6667, comme l'affirme le test [`SimilarityTnI_SeparatesAll23ZRelatedPairs`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L73). La documentation promet davantage : [S = 1 « iff the sets are transposition-aligned »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Common/GA.Domain.Core/Theory/Atonal/SpectralPhaseAlignment.cs#L27). Le [théorème 3](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L26-L34) de la note de recherche démontre un sens, S(A, T_t A) = 1, et le test [`Similarity_IsOne_OnEveryTransposition_Randomized`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.Core.Tests/Atonal/SpectralPhaseAlignmentTests.cs#L108) vérifie ce sens sur 1 000 ensembles aléatoires. La réciproque est fausse (§5). Le [corollaire de séparation](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/docs/research/2026-07-04-optick-spectral-phase-alignment.md#L43) de la note soutient que les ensembles en relation Z sont séparés parce qu'ils ne sont pas équivalents par TnI. D'après le §5, cela ne s'ensuit pas : do ré mi et do mi sol♯ ne sont pas équivalents non plus, et atteignent S = 1. La conclusion tient pour les 23 paires parce qu'on peut les vérifier une à une : la transcription trouve S_TnI au plus égal à 0,6667, et le test de GA affirme qu'il reste inférieur à 1 − 10⁻⁶ pour chacune.

**Ce que dit l'outil MCP.** L'outil [`GaHomometricDistinguish`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L198) affiche, dès que S ≥ 1 − 10⁻⁶, [« Same shape up to transposition — one is a transposition of the other. »](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/GaMcpServer/Tools/ChordAtonalTool.cs#L231-L232) D'après la transcription, Csus2 contre C9 et Cmaj7 contre Cdim7 atteignent cette branche. L'outil lit les deux accords avec l'analyseur de `GaChordToSet`, qui demande à la closure `domain.chordIntervals` les intervalles d'un accord, et les tests de GA fixent les quatre lectures : `GaChordToSet` transforme [Cdim7 en `{C, Eb, F#, A}` et C9 en `{C, D, E, G, Bb}`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L17-L18), et la closure épelle [Csus2 `P1 M2 P5`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L36) et [Cmaj7 `P1 M3 P5 M7`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Common/GA.Business.DSL.Tests/ClosureChordIntervalsTests.cs#L41). Les deux classes de tests appellent d'abord [`GaClosureBootstrap.init()`](https://github.com/GuitarAlchemist/ga/blob/40d337479af36d987df3f06c8c638ffd35f13458/Tests/Apps/GaMcpServer.Tests/ChordAtonalToolTests.cs#L14).

Au moment où cette leçon est écrite, aucune issue de GA ne couvre ces points. Corriger l'un ou l'autre de ces points revient aux responsables de GA ; cette leçon ne fait que les décrire.

### Exercice pratique

D'après la transcription, `GetSpectralCentroid` de GA donne 5,044 pour l'accord parfait majeur. Montrez que le centroïde vaut 6(1 − n / Σ|X_k|), et vérifiez-le avec les modules du §4.

> *Solution :* Sur k = 0 à 11, associez la case k à la case 12 − k pour k = 1 à 5 : comme |X_(12−k)| = |X_k|, elles ajoutent k|X_k| + (12 − k)|X_k| = 12|X_k| à la somme pondérée. La case 6 ajoute 6|X_6| et la case 0 n'ajoute rien. Le module total vaut T = n + 2(|X_1| + … + |X_5|) + |X_6|, donc la somme pondérée vaut 6(T − n), et le centroïde 6(T − n)/T = 6(1 − n/T). Pour l'accord parfait majeur, T = 3 + 2(0,518 + 1 + 2,236 + 1,732 + 1,932) + 1, environ 18,84, et 6(1 − 3/18,84) vaut environ 5,04 : les 5,044 de GA, à deux décimales près.

---

## 7. Expérience proposée (pas encore exécutée)

**Statut : non exécutée.** Cette section propose une expérience pour le laboratoire music-theory-ga de Learn, qui compile GA ; l'épinglage de GA dans le laboratoire passerait d'abord à `40d3374`. Rien n'y est une mesure. Les prédictions viennent de la transcription du §6 et sont écrites avant toute exécution ; une version ultérieure de cette leçon en donnera les résultats. Chaque étape appelle les types de GA dans le processus même du laboratoire, jamais un serveur MCP en marche ni un modèle de langage.

1. **Les modules par transposition.** Pour les 4 096 ensembles, comparer `new SetClass(A).GetMagnitudeSpectrum()` aux modules de la TFD de A calculée par le laboratoire lui-même, et appeler `GetPhaseSpectrum` sur les classes de do mi sol, ré fa♯ la et do mi♭ sol. Prédiction : des modules égaux pour chaque ensemble, aux arrondis près ; trois tableaux de phases identiques.
2. **L'homométrie.** Pour chacune des 46 classes en relation Z, appeler `SetClassSpectralIndex.GetNearestBySpectrum` sur la classe prise dans `SetClass.Items`, puis sur la même classe construite avec `new SetClass(...)`, et comparer `GetMagnitudeSpectrum` à celui de la partenaire. Prédiction : la partenaire arrive en premier, seule à distance 0 aux arrondis près, pour 46 sur 46 ; la classe construite à neuf revient elle-même en premier, sa partenaire en second ; et les spectres sont égaux aux arrondis près.
3. **Le centroïde.** Comparer `GetSpectralCentroid` à 6(1 − n / Σ|X_k|) sur les 223 classes non vides. Prédiction : égaux aux arrondis près ; 5,5 pour une note seule, 3,000 pour la gamme par tons, 3,515 pour la gamme hexatonique et 4,091 pour la collection diatonique.
4. **La séparation.** Appeler `SimilarityTnI` sur les formes premières des 23 paires en relation Z. Prédiction : toutes les valeurs inférieures à 1, la plus grande 0,6667, la plus petite 0,3333. Cela refait, à partir d'une exécution réelle, ce qu'affirme le test de GA.
5. **La réciproque.** Pour chaque paire de types Tn distincts, en laissant de côté l'ensemble vide et l'agrégat, appeler `Similarity` sur un représentant de chacun. Prédiction : S ≥ 1 − 10⁻⁶ pour 270 paires de même taille et 1 230 de tailles différentes, dont do ré mi et do mi sol♯ avec t* = 0, 4 et 8.
6. **Le verdict de l'outil MCP.** Appeler `GaClosureBootstrap.init()`, comme le font les tests de GA, puis appeler directement `GaHomometricDistinguish("Csus2", "C9")` et `GaHomometricDistinguish("Cmaj7", "Cdim7")`. Prédiction : les deux se terminent par « Same shape up to transposition — one is a transposition of the other. », avec les quatre lectures que fixent les tests de GA (§6).

### Exercice pratique

L'étape 5 prédit 1 500 paires avec S = 1 qui ne sont pas des transpositions, et pourtant le test aléatoire de GA passerait quand même. Quel test détecterait le « iff » ?

> *Solution :* Un test qui tire des paires qui ne sont pas des transpositions l'une de l'autre et affirme S < 1. Le test de GA ne tire qu'un ensemble et l'une de ses transpositions, donc il vérifie le sens que démontre le théorème 3. D'après la transcription du §6, l'affirmation contraire échouerait sur 270 paires de types Tn distincts de même taille.

---

## 8. Pièges courants

- **Prendre les modules pour une empreinte d'un ensemble.** Avec le nombre de notes, |X_0|, ils n'identifient un ensemble qu'à transposition, inversion et, pour 23 paires de classes, relation Z près. |X_1| à |X_6| seuls ne distinguent même pas un ensemble de son complémentaire.
- **Écrire « ICV = |DFT|² ».** Les modules au carré sont une transformée en cosinus de la taille et du vecteur ; ils portent la même information, pas les mêmes nombres.
- **Nommer un coefficient d'après le mauvais cycle.** k = 3 mesure la proximité avec l'accord parfait augmenté, un cycle de tierces majeures ; k = 4 avec la septième diminuée, un cycle de tierces mineures. Le coefficient k est le plus grand pour les ensembles dont les notes se trouvent près de k points régulièrement espacés, à 12/k demi-tons l'un de l'autre : un cluster pour k = 1, deux clusters à un triton l'un de l'autre pour k = 2, l'accord parfait augmenté pour k = 3, la septième diminuée pour k = 4, la gamme pentatonique pour k = 5 et la gamme par tons pour k = 6.
- **Tester un invariant sur des entrées égales par construction.** Deux classes d'ensembles de même forme première donnent un seul spectre, quoi que fasse la TFD.
- **Lire S = 1 comme « même forme ».** Cela dit que les phases s'accordent, pour un t, partout où les deux ensembles ont un coefficient non nul, et qu'il existe au moins un tel coefficient (la convention de GA donne aussi 1 quand chacun des deux ensembles est l'ensemble vide ou l'agrégat). Cela n'exige même pas le même nombre de notes.
- **Prendre un argument pour une vérification.** Une conclusion peut être vraie alors que l'argument avancé pour elle échoue ; pour les paires en relation Z, c'est le test exhaustif qui fait preuve.
- **Lire les phases d'une forme première.** Elles sont les mêmes pour tous les ensembles de la classe, et ne disent rien de la place de l'ensemble.

---

## Termes clés

| Terme | Définition |
|------|-----------|
| **TFD des classes de hauteurs** | Les coefficients X_k = Σ_(x ∈ A) e^(−2πikx/12) d'un ensemble de classes de hauteurs A, pour k = 0 à 11 |
| **Module** | La taille d'un coefficient X_k, inchangée par transposition et par inversion |
| **Phase** | L'angle d'un coefficient, tourné de −30kt degrés par une transposition de t et changé de signe par I0 |
| **Théorème de décalage** | X_k(T_t A) = e^(−2πikt/12) X_k(A) |
| **Lemme de Lewin** | Le module de X_k au carré vaut n + 2 Σ_d ICV_d cos(πkd/6), donc les modules de X_0 à X_6 et la paire (taille, vecteur de classes d'intervalles) se déterminent mutuellement |
| **Homométrique** | Qui a la même taille et les mêmes modules de X_1 à X_6, comme toute paire d'ensembles en relation Z |
| **Qualité harmonique** | Ce que mesure un module : la proximité avec les ensembles qui le maximisent, comme la gamme par tons pour k = 6 |
| **Similarité par alignement de phase** | S, le meilleur accord des phases de deux ensembles sur les 12 transpositions, pondéré par leurs modules ; S_TnI essaie aussi l'inversion |

---

## Auto-évaluation

**1. Pourquoi do majeur et do mineur ont-ils les mêmes six modules ?**
> Do mineur est I7 de do majeur : I0 remplace chaque coefficient par son conjugué et T7 le multiplie par un nombre de module 1, donc aucun module ne change.

**2. Lesquels des coefficients X_1 à X_6 de la gamme octatonique peuvent être non nuls, et pourquoi ?**
> Seulement X_4. T3 envoie la gamme sur elle-même, donc X_k = 0 sauf si 3k est un multiple de 12, ce qui, parmi k = 1 à 6, laisse k = 4. Son module vaut 4.

**3. Deux ensembles ont S = 1. Que peut-on en conclure ? Et s'ils ont en plus les mêmes modules ?**
> À lui seul, cela montre uniquement que, pour un t, leurs phases s'accordent pour chaque k où les deux coefficients sont non nuls, et qu'il existe au moins un tel k (la convention de GA donne aussi 1 quand chacun des deux ensembles est l'ensemble vide ou l'agrégat). Avec la même taille et les mêmes modules, leurs coefficients s'accordent après cette transposition, donc l'un des ensembles est une transposition de l'autre.

**4. Que renvoie en premier `GetNearestBySpectrum` de GA pour 4-Z15 ?**
> 4-Z29, à distance 0 aux arrondis près : les deux classes sont homométriques, donc leurs spectres de modules sont égaux. Cela vaut quand 4-Z15 est pris dans `SetClass.Items` ; une classe construite à neuf revient elle-même en premier.

**Critères de réussite :** Calculer et lire les coefficients d'un ensemble ; établir le théorème de décalage, l'effet de l'inversion et de M5, et le lemme de Lewin ; expliquer l'homométrie et les paires en relation Z ; nommer le prototype de chaque module et prédire les zéros d'après la symétrie ; et dire ce que montre une similarité de phase égale à 1, avec et sans modules égaux.

---

## Bases de recherche

- D. Lewin, « Re: Intervallic Relations between Two Collections of Notes », *Journal of Music Theory* 3/2, 1959 : la fonction d'intervalles de deux ensembles et sa transformée de Fourier
- I. Quinn, « General Equal-Tempered Harmony », *Perspectives of New Music* 44/2, 2006 (introduction et partie I), et 45/1, 2007 (parties II et III) : les modules de Fourier comme qualités harmoniques
- E. Amiot, *Music Through Fourier Space: Discrete Fourier Transform in Music Theory*, Springer, 2016 : la TFD des ensembles de classes de hauteurs, le lemme de Lewin, l'homométrie et les phases
- MAT-021 de Streeling pour la TFD, et MUS-020 pour les classes d'ensembles, les vecteurs de classes d'intervalles et la relation Z
- Code source de GA au commit `40d337479af36d987df3f06c8c638ffd35f13458`, dont la note de recherche `docs/research/2026-07-04-optick-spectral-phase-alignment.md` : chaque fait de code du §6 renvoie à sa ligne
- Vérifications en Python sur les 4 096 ensembles : chaque nombre des §§1–6 en vient, ou de la transcription du code de GA
- Expérience : proposée au §7, non exécutée ; cette leçon ne contient aucune mesure de GA lui-même
- Provenance : rédigé à la main par une session Claude Code (Opus 5.5) à partir du plan de cursus de Streeling, pas produit par le pipeline de cours Seldon ; en cours de revue
- État de croyance : T(0.85) F(0.02) U(0.10) C(0.03) — traduction française : U (non relue par un locuteur natif)
