---
module_id: inf-003-verdict-distribution-drift
department: information-theory
course: "Mesurer la dérive des distributions de verdicts avec la divergence de Jensen-Shannon"
level: intermediate
prerequisites: [inf-001-entropy-of-governance]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: information-theory-2026-10-11-003
version: "0.1.0"
---

# Mesurer la dérive des distributions de verdicts avec la divergence de Jensen-Shannon

> **Département de théorie de l'information** | Niveau : intermédiaire | Durée estimée : 35 minutes | Statut : brouillon français ; revues métier, pédagogique et linguistique et publication en attente

## Objectifs

À la fin de cette leçon, vous pourrez :

- transformer des effectifs comparables de verdicts de l'analyseur IX en vecteurs de probabilités alignés ;
- calculer la divergence directionnelle de Kullback–Leibler (KL) et la divergence symétrique de Jensen–Shannon (JS), dans les unités renvoyées par IX ;
- expliquer pourquoi une nouvelle catégorie peut provoquer une erreur dans un sens de KL alors que JS reste finie ;
- utiliser une divergence pour décider quelles preuves examiner, en tenant compte des limites d'analyse et de la composition des lots.

## La question du projet

L'[analyseur de réseaux de Petri IX épinglé](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L105) sérialise le résultat d'une propriété en `holds`, `fails` ou `unknown`. `Fails` peut être accompagné d'un contre-exemple ; `unknown` signifie que l'analyseur n'a pas tranché dans les limites d'exploration. Un changement dans leurs fréquences entre deux analyses mérite parfois examen. Comment le quantifier sans confondre un nombre avec une preuve de régression ?

La question réfutable est : **pour une propriété, les mêmes identifiants de réseaux, la même révision d'analyseur et les mêmes limites, de combien la distribution des catégories a-t-elle changé après modification des réseaux ?** IX fournit déjà des [fonctions KL et JS](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L222), également exposées comme [fonctions scalaires DuckDB](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-duck/src/inference.rs#L186-L210). Nous calculons ici un résultat reproductible pour des effectifs **synthétiques** : aucun lot IX de production ni changement de qualité perçu par les utilisateurs n'a été mesuré.

INF-001 étudiait l'entropie d'une seule distribution de jetons de politique. INF-002 montrait des distinctions perdues dans la représentation compacte OPTIC-K de GA. Ici, nous comparons **deux distributions sur les mêmes catégories de verdicts**. Le score agrège des fréquences ; il ne révèle ni quel réseau a changé, ni pourquoi, ni si le changement est souhaitable.

## 1. Choisir une observation stable

L'[énumération `Verdict<T>`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L83-L95) possède trois étiquettes. Sa méthode `holds()` n'est vraie que pour `Holds` : `Unknown` n'est pas un succès implicite. Le rapport `Analysis` contient plusieurs propriétés différentes, dont `deadlock_free`, `bounded`, `quasi_live`, `live` et `reversible`. Les additionner mélangerait des questions aux conditions de preuve différentes. Retenons seulement `deadlock_free`, un verdict par réseau, et l'ordre `[holds, fails, unknown]`.

La [branche de liberté d'interblocage](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L465-L491) explique ces étiquettes. Un marquage mort découvert donne `Fails`, même si l'énumération est ensuite tronquée ; `max_reported_deadlocks` borne les témoins rapportés et peut valoir zéro. Sans marquage mort découvert, `Holds` exige une exploration complète ; sinon, le verdict est `Unknown`. Cette observation concerne cette propriété, pas toutes les branches de l'analyseur.

Voici un lot **inventé** de dix réseaux, utilisé uniquement pour l'exercice numérique :

| Analyse | Holds | Fails | Unknown | Total |
|---|---:|---:|---:|---:|
| Référence | 8 | 0 | 2 | 10 |
| Candidate | 6 | 2 | 2 | 10 |

Après division par les totaux, `p = [0.8, 0, 0.2]` et `q = [0.6, 0.2, 0.2]`. L'ordre des catégories doit rester identique : la fonction accepterait deux tableaux dont les étiquettes ont été permutées, mais comparerait alors des événements différents. Enregistrez les étiquettes et contrôlez leur ordre.

### Exercice 1 : construire les vecteurs comparables

Écrivez les vecteurs normalisés du tableau dans l'ordre `[holds, fails, unknown]`. Quelles métadonnées doivent accompagner une comparaison réelle ?

> **Réponse :** `p=[8/10,0/10,2/10]=[0.8,0,0.2]` ; `q=[6/10,2/10,2/10]=[0.6,0.2,0.2]`. Conservez la propriété, les identifiants des réseaux, l'ordre des catégories, le commit de l'analyseur, les limites d'exploration et le total de chaque analyse. Le calcul seul ne vérifie pas ces conditions.

## 2. Lire le calcul réel d'IX

La fonction [`normalize`](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L156-L173) divise chaque composante non négative par la somme. Elle rejette un vecteur vide, une valeur négative ou NaN et une somme nulle. Notre protocole exige aussi des effectifs finis avant l'appel : le code ne rejette pas explicitement l'infini positif. KL et JS exigent des vecteurs de même longueur et emploient le logarithme naturel : le résultat est en **nats**. Divisez par `ln(2)` pour obtenir des bits. Dans DuckDB, `ix_kl(p,q)` et `ix_js(p,q)` prennent des `DOUBLE[]` ; une liste SQL `NULL` propage `NULL`, tandis qu'une erreur mathématique devient une erreur SQL. L'existence de ces fonctions ne prouve pas celle d'une tâche planifiée de comparaison.

KL est directionnelle :

`D_KL(p || q) = Σ_i p_i ln(p_i / q_i)`.

Seules les catégories où `p_i > 0` contribuent. Ici, `D_KL(p || q)=0.8 ln(0.8/0.6)+0.2 ln(0.2/0.2)=0.23014565796142483` nats. Dans l'autre sens, la catégorie `fails` impose `0.2 ln(0.2/0)` : mathématiquement, elle diverge ; [IX renvoie une erreur](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L185-L209), pas une valeur infinie. Inverser les arguments change la question. Ne transformez pas l'erreur d'une catégorie nouvelle en score nul.

### Exercice 2 : expliquer le sens de KL

Calculez `D_KL(p || q)`. `D_KL(q || p)` donne-t-elle le même nombre dans IX ?

> **Réponse :** `D_KL(p || q)=0.8 ln(4/3)=0.23014565796142483` nats. Pour `D_KL(q || p)`, `q_fails=0.2` rencontre `p_fails=0` ; après inversion des arguments, IX renvoie son erreur de paramètre « q is zero where p is positive ». KL est asymétrique : seul le sens référence-vers-candidate dispose ici d'un support fini.

## 3. JS : un indicateur fini et symétrique

JS construit `m=(p+q)/2`, puis moyenne deux divergences KL : `D_JS(p,q)=0.5 D_KL(p||m)+0.5 D_KL(q||m)`. Ici, `m=[0.7,0.1,0.2]`. Ce point médian attribue une masse positive à toute catégorie présente dans l'un des vecteurs : JS reste finie pour cet exemple. Le [code et son commentaire](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L210-L222) indiquent que JS est symétrique et bornée par `ln(2)` nats. Zéro signifie distributions **normalisées** identiques, pas analyses ou tailles de lot identiques.

Un calcul indépendant de la formule donne `D_KL(p||m)=0.10682511409961822`, `D_KL(q||m)=0.04613902821563412`, puis `D_JS=0.07648207115762617` nats, soit `0.1103403047760241` bits. Ces nombres viennent de l'exemple synthétique, pas d'un déploiement IX. Les [tests unitaires épinglés](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-math/src/inference.rs#L568-L580) couvrent le maximum pour des vecteurs unitaires disjoints et zéro pour des entrées égales ; nous n'avons pas exécuté ces tests ici.

### Exercice 3 : calculer et borner JS

Calculez le point médian et JS. L'inversion des analyses change-t-elle le résultat ? Quel est le maximum théorique en nats ?

> **Réponse :** `m=[0.7,0.1,0.2]` ; `D_JS=0.5(0.10682511409961822+0.04613902821563412)=0.07648207115762617` nats. Inverser les analyses conserve le point médian et échange les deux termes de même poids ; JS ne change pas. Son maximum est `ln(2)=0.6931471805599453` nats pour des supports disjoints.

### Exercice 4 : ce que cache la normalisation

Comparez `[80,0,20]` et `[8,0,2]` avec `ix_js`. Que prouve le résultat ?

> **Réponse :** Les deux deviennent `[0.8,0,0.2]` après normalisation ; `ix_js` renvoie `0`, sous réserve de la représentation en virgule flottante. Seule l'égalité des proportions est démontrée. Un lot compte 100 observations, l'autre 10 ; JS efface cette différence et ne dit pas si les mêmes réseaux ont obtenu les mêmes verdicts. Conservez les totaux et les identifiants appariés hors du score.

## 4. Décider ce qui mérite une enquête

Imaginons une future règle QA, approuvée séparément, qui déclenche une enquête à `JS > 0.05` nats. Notre valeur **illustrative** dépasse ce seuil inventé. Elle invite à examiner les données ; elle n'établit ni l'existence d'un contrôle déployé ni un motif automatique de rejet. Vérifiez d'abord les dix identifiants de réseaux et la propriété `deadlock_free`, puis la révision de l'analyseur et les `Limits`. Le [rapport expose la troncature et sa cause](https://github.com/GuitarAlchemist/ix/blob/bd1336b7c4045e427dcdbe80b102790e45da5ce1/crates/ix-petri/src/analysis.rs#L161-L175). Augmenter `max_states` peut faire passer `unknown` à `holds` ou `fails` sans changer le réseau. Appariez ensuite les verdicts par identifiant et examinez les témoins disponibles et les raisons d'indécision. Si l'enquête requiert un témoin absent, réexécutez avec `max_reported_deadlocks` strictement positif. L'histogramme ne révèle ni les réseaux concernés ni la validité des contre-exemples pour la propriété voulue.

Pour un petit lot stable, un tableau à trois colonnes et les changements individuels sont parfois plus clairs qu'un score. Celui-ci peut aider à prioriser plusieurs lots cohérents, à condition de garder le tableau et les preuves par réseau. C'est une piste de conception, pas une substitution à l'examen des témoins. Si les alertes répétées proviennent surtout d'une composition ou de budgets d'exploration différents, le signal est réfuté pour cet usage : révisez le protocole au lieu de modifier le seuil jusqu'à disparition des alertes.

### Exercice 5 : interpréter une alerte

Le seuil hypothétique est `0.05` nats et JS vaut `0.07648207115762617`. Une personne affirme : « La candidate a régressé ; il y a deux nouveaux échecs. » Qu'est-ce qui relève du calcul vérifiable, et que faut-il contrôler avant d'accepter la régression ?

> **Réponse :** `0.07648207115762617 > 0.05` : l'exemple synthétique déclencherait la règle d'enquête inventée. Le tableau compte deux `fails` chez la candidate et aucun à la référence, sans identifier les réseaux modifiés. Vérifiez les mêmes identifiants, la propriété, la révision et les limites ; appariez les résultats ; lisez les témoins d'échec rapportés et les raisons d'`unknown`. Exigez `max_reported_deadlocks > 0` et réexécutez si un témoin nécessaire manque. Un changement de limite ou de lot peut expliquer la dérive sans régression du code. Le score ne prouve ni causalité ni significativité statistique.

## Limites et prochaine étape

La formule a été vérifiée sur un tableau synthétique par un petit calcul indépendant ; le code IX a été lu au commit `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Nous n'avons ni lancé l'analyseur sur dix réseaux, ni interrogé une vraie table DuckDB, ni exécuté la suite de tests IX, ni estimé l'incertitude d'échantillonnage, ni validé un seuil de production. Comparer des lots non identiques demanderait un plan d'échantillonnage et d'appariement. L'étape suivante serait de conserver une propriété par identifiant stable à deux révisions épinglées et à limites identiques, de calculer JS, puis d'examiner manuellement chaque verdict changé. Gardez effectifs, résultats par réseau et témoins avec le score pour rendre la conclusion vérifiable. Cette traduction est un brouillon IA : les revues humaines, la synchronisation Learn, la construction et la lecture publique restent en attente.
