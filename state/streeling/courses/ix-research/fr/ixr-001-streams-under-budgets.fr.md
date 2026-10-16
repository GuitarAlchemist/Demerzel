---
module_id: ixr-001-streams-under-budgets
department: ix-research
course: "Pipelines IX en flux, sous budgets"
level: intermediate
prerequisites: []
estimated_duration: "40 minutes"
produced_by: claude-ix-research
research_cycle: null
version: "0.1.0"
---

# Des flux sous budget : contre-pression, porte apprise et vérification de Petri

> **Département de recherche sur IX** | Intermédiaire | 40 minutes | Traduction française du brouillon anglais ; revue humaine en attente. Aucune fiche de cycle de recherche n'existe pour ce module (voir « Provenance »).

## Objectifs et question du projet

À la fin de ce module, vous saurez :

- expliquer comment des canaux bornés transforment un nœud lent en contre-pression, jusqu'au moteur SQL qui alimente le flux, et comment un arrêt remonte dans l'autre sens ;
- envoyer chaque élément à un seul expert sous un budget en argent, et nommer les trois ressources que dépense un tel routeur : la qualité, l'argent et la capacité ;
- renvoyer l'avis d'un juge vers un routeur sans cycle de canaux ;
- dire, avant l'exécution, si un graphe de liens bloquants peut s'interbloquer, et ce que change un seul lien qui perd.

**Question du projet :** peut-on router un flux de questions de guitare entre un routeur local gratuit et un expert payant, sous un budget fixe, de façon à battre une règle fixe à dépense égale, sans file qui grossit ni interblocage ?

L'étude porte sur la crate [`ix-stream`](https://github.com/GuitarAlchemist/ix/tree/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream), commit [`14dccd0`](https://github.com/GuitarAlchemist/ix/commit/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab) de la branche `exp/loop-nodes` de GuitarAlchemist/ix. Tous les liens vers le code ci-dessous sont épinglés sur ce commit.

## 1. Le point de départ : un pipeline qui n'est ni en flux ni parallèle

IX exécute déjà des pipelines : `ix-pipeline` traduit un `ix.yaml` en DAG et l'exécute. Son exécuteur avance niveau par niveau, avec une barrière après chaque niveau, et chaque nœud reçoit une valeur JSON entière. La branche qui traite un niveau de plusieurs nœuds annonce « en parallèle », mais elle exécute chaque nœud dans le thread courant, comme le dit le commentaire qu'elle contient, parce que la fonction de calcul d'un nœud n'est pas `Send` ([`executor.rs`, lignes 164 à 211](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-pipeline/src/executor.rs#L164-L211)).

Un pipeline sur une grosse requête attend donc le résultat entier, puis exécute ses nœuds l'un après l'autre. Rien ne freine quand un nœud est lent, puisque rien ne coule. `ix-stream` est une tranche traceuse de l'autre modèle : les valeurs coulent une à une dans un graphe de threads reliés par des canaux bornés.

## 2. Contre-pression et annulation

Chaque nœud d'un graphe `ix-stream` est formé d'un ou plusieurs threads, ses travailleurs, qui partagent un canal d'entrée contenant au plus `cap` valeurs ([`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/lib.rs#L1-L16)). Un envoi vers un canal plein attend. Cette attente est la contre-pression : un nœud lent retient tout ce qui se trouve en amont, jusqu'à la source, au lieu de laisser grossir une file. C'est le `request(n)` de Reactive Streams dans sa forme la plus simple, `n` étant le nombre de places libres.

La source peut être une requête DuckDB. [`source::duckdb`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/source.rs#L28) lance la CLI `duckdb` avec `-jsonlines` et envoie chaque ligne dès qu'elle la lit. Quand le graphe est plein, la source cesse de lire, le tube se remplit et DuckDB attend sur son écriture : la contre-pression atteint le moteur SQL.

L'annulation va dans l'autre sens. Quand un nœud s'arrête, ou que tous ses travailleurs finissent, son entrée est abandonnée et tout envoi vers lui échoue. Un nœud dont tous les liens mènent à des nœuds terminés s'arrête à son tour : l'arrêt remonte jusqu'à la source, et la source DuckDB tue alors son processus. Une requête que plus personne ne lit cesse de calculer.

**Testé.** [`a_full_channel_holds_the_source_back`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L13-L61) construit la chaîne source → `a` (cap 2, 1 travailleur) → `b` (cap 3, 2 travailleurs) → `sink` (cap 4, 1 travailleur), bloque le puits sur sa première valeur, puis compte au bout de 400 ms les valeurs sorties de la source, face à cette borne :

```rust
// Values in channels, plus one in each worker's hand, plus the source's next one.
let bound = (2 + 1) + (3 + 2) + (4 + 1) + 1;
```

(Le commentaire dit : les valeurs dans les canaux, plus une dans la main de chaque travailleur, plus la prochaine de la source.) Au plus 14 des 10 000 valeurs quittent donc la source tant que le puits bloque. [`a_stopped_graph_stops_the_duckdb_query`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L374-L401) vérifie qu'arrêter le graphe arrête la requête. Les 18 tests de `tests/stream.rs` sont passés au commit épinglé le 2026-10-16, y compris les 3 qui demandent la CLI DuckDB (Windows 11, DuckDB v1.5.3, build debug) ; voici la première et la dernière ligne de leur sortie :

```text
running 18 tests
test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.41s
```

### Exercice pratique 1

Une chaîne source → `parse` (cap 8, 4 travailleurs) → `score` (cap 2, 1 travailleur) → `sink` (cap 16, 1 travailleur). Le puits bloque sur sa première valeur. Combien de valeurs, au plus, peuvent avoir quitté la source ?

> **Réponse :** chaque nœud retient son canal plus une valeur par travailleur : (8 + 4) + (2 + 1) + (16 + 1) = 32, plus la valeur que la source tient en attendant de l'envoyer : 33. La borne ne dépend pas de la longueur du flux, et c'est tout l'intérêt de la contre-pression.

## 3. Un retour sans cycle : le bus algédonique

Un routeur qui apprend doit savoir ce qu'ont donné ses choix, et le juge se trouve en aval de lui. Un canal du juge vers le routeur fermerait un cycle de liens bloquants, et la section 6 montre qu'un tel cycle peut se coincer.

`ix-stream` envoie donc les retours sur un [`Bus`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/bus.rs) à part. Un émetteur n'y attend jamais : chaque abonné a sa propre file bornée, et un événement qui la trouve pleine est perdu pour cet abonné, et compté. Les signaux de plaisir (valence +1) et de douleur (−1) y circulent : le juge dit juste ou faux pour chaque élément, une voie payante signale la part de son budget que chaque appel a coûtée, et le routeur signale une douleur quand une voie qu'il voulait était pleine. Avant de router l'élément suivant, le routeur lit les signaux arrivés, et il n'en attend jamais aucun.

Le nom vient du modèle du système viable de Stafford Beer, où un signal algédonique court-circuite la hiérarchie normale. [CYB-001](../../cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md) nomme l'absence de canal algédonique comme la lacune D de la gouvernance de Demerzel. Ce bus applique la même idée à l'intérieur d'un pipeline, et il perd des événements plutôt que de bloquer, parce qu'ici un signal est un indice pour apprendre, pas une alarme.

## 4. Une porte qui route comme celle d'un mélange d'experts, sous budgets

La [porte](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs) envoie chaque élément à un seul expert, un *bras*. Pour chaque contexte, une case que l'appelant calcule, elle tient un bandit UCB1 issu d'`ix-rl`, qui estime la qualité des réponses de chaque bras. Elle classe les bras selon

```text
score(arm) = q(arm) + 0.3 * sqrt(2 * ln(N) / n(arm)) - price(arm)
```

où `q` est la qualité moyenne jugée du bras dans ce contexte, `n` le nombre de fois où il y a été jugé et `N` le total du contexte. Un bras jamais essayé dans un contexte obtient +∞, si bien que chaque bras est essayé une fois. Le 0,3 est le poids d'exploration par défaut de la porte.

Un bras doté d'un budget a un prix fictif qui suit son rythme ([`price`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L178)) :

```text
price(arm) = max(0, base_price + 4 * (spent / cap - share of the stream seen))
```

(`spent / cap` est la part du budget dépensée, `share of the stream seen` la part du flux déjà vue.) Le prix devient infini quand le budget ne peut plus payer un appel, et 4 est le gain par défaut. Dépenser plus vite que le rythme fait monter le prix, ce qui réserve le bras aux contextes où il rapporte le plus ; prendre du retard le fait baisser. Le prix ne fait qu'orienter. L'arrêt ferme, c'est le [`Ledger`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L58), le registre : une voie y dépense, et le registre refuse un appel qu'il ne peut pas payer.

### Exercice pratique 2

Le bras Jev a un prix de base de 0,02. À mi-flux, Jev a dépensé 60 % de son budget. Quel est son prix ? Et s'il en avait dépensé 40 % ?

> **Réponse :** 0,02 + 4 × (0,6 − 0,5) = 0,42 : Jev ne gagne plus un contexte que là où sa qualité estimée, bonus d'exploration compris, dépasse de plus de 0,42 celle du routeur local gratuit. À 40 % : 0,02 + 4 × (0,4 − 0,5) = −0,38, ramené à 0 : Jev ne coûte rien tant qu'il n'a pas rattrapé son rythme.

## 5. L'expérience : 663 questions de guitare, deux experts, un budget

[`examples/route.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs) fait couler les 221 questions étiquetées de l'étude du routeur Jev : 190 demandent l'un des 32 skills de GA, et 31 sont hors sujet, étiquetées `__none__` ([`RESULTS.md`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/RESULTS.md), étape 3). Il les fait couler trois fois, dans un ordre que DuckDB mélange par un hachage à graine : 663 éléments. Chaque élément passe par :

1. `local` : la réponse que le routeur local par embeddings (`c2-merge`) lui a donnée, enregistrée, avec sa confiance ;
2. `kw` : un expert par mots-clés écrit en Zig, compilé pour WASI et exécuté dans le bac à sable d'`ix-wasm` ;
3. `gate` : accepter `local` ou interroger Jev, dans l'un de six contextes ([`context`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs#L279)) : le routeur local a décliné, était sous 0,7 ou au moins à 0,7, croisé avec l'accord ou non de `kw` ;
4. `jev` : la réponse enregistrée de Jev, après une pause qui tient lieu de la latence d'un appel réel, facturée au coût moyen d'un appel de l'étude. Jev est le classifieur hébergé zéro-shot `jev-1.13.0` de TypeSafe. **Rien n'est envoyé à Jev** : les réponses sont rejouées à partir des reçus de l'étude ;
5. `judge` : compare la réponse à l'étiquette et signale juste ou faux sur le bus.

L'exemple peut aussi ajouter une voie Claude Haiku en direct, sur l'abonnement de la personne, plafonnée en appels. Aucune n'est utilisée par défaut, et aucun résultat ci-dessous n'en contient (voir la section 8).

**Le budget.** Les 221 appels Jev enregistrés de l'étude ont coûté 0,026733 USD au tarif public, calculés à partir des tokens d'entrée déclarés, et non facturés ([`full/jev-eval.json`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/jev/full/jev-eval.json)) : 0,000120962 USD par appel. L'exemple accorde à Jev 40 % du flux : 0,4 × 663 × 0,000120962 = **0,0320792472 USD, le prix de 265,2 appels**.

**Les politiques.** `local` garde toujours la réponse locale. `jev` interroge Jev jusqu'à épuisement de son budget, puis garde la réponse locale : « Jev jusqu'à épuisement ». `learned` est la porte de la section 4.

**Attendre ou non.** Avec `--wait`, la porte attend son premier choix quand cette voie est pleine. Sans cette option, une voie pleine est sautée au profit du choix suivant, comme un mélange d'experts laisse tomber ce qui dépasse la capacité d'un expert.

**Observé.** Chaque exécution écrit `results.jsonl`, une ligne par élément. Cette requête compte, pour chaque exécution, les bonnes réponses et les appels Jev effectués :

```sql
SELECT regexp_extract(filename, 'route-[a-z]+(-wait)?-seed[0-9]+') AS run,
       count(*) AS n,
       sum(correct::INT) AS right_n,
       count(*) FILTER (WHERE arm = 'jev' AND fallback IS NULL) AS jev_calls
FROM read_json('route-*/results.jsonl', filename = true, union_by_name = true)
GROUP BY ALL ORDER BY run;
```

```text
┌───────────────────────────┬───────┬─────────┬───────────┐
│            run            │   n   │ right_n │ jev_calls │
│          varchar          │ int64 │ int128  │   int64   │
├───────────────────────────┼───────┼─────────┼───────────┤
│ route-jev-seed7           │   663 │     483 │        84 │
│ route-jev-wait-seed1      │   663 │     523 │       265 │
│ route-jev-wait-seed2      │   663 │     527 │       265 │
│ route-jev-wait-seed3      │   663 │     522 │       265 │
│ route-jev-wait-seed4      │   663 │     525 │       265 │
│ route-jev-wait-seed5      │   663 │     526 │       265 │
│ route-jev-wait-seed7      │   663 │     524 │       265 │
│ route-learned-seed7       │   663 │     471 │        84 │
│ route-learned-wait-seed1  │   663 │     555 │       265 │
│ route-learned-wait-seed11 │   663 │     557 │       265 │
│ route-learned-wait-seed2  │   663 │     554 │       265 │
│ route-learned-wait-seed3  │   663 │     550 │       265 │
│ route-learned-wait-seed4  │   663 │     551 │       265 │
│ route-learned-wait-seed5  │   663 │     550 │       265 │
│ route-learned-wait-seed7  │   663 │     546 │       265 │
│ route-local-seed7         │   663 │     456 │         0 │
└───────────────────────────┴───────┴─────────┴───────────┘
  16 rows                                       4 columns
```

Les exécutions à cinq graines ont rejoué Jev avec une pause de 40 ms (`--jev-ms 40`) ; celles de la graine 7 ont gardé les 400 ms par défaut. Toutes donnaient 4 travailleurs à Jev.

| Politique | Attend | Pause Jev | Graines | Justes sur 663 | Exactitude | Appels Jev |
|---|---|---|---|---|---|---|
| local | — | — | 7 | 456 | 0,688 | 0 |
| Jev jusqu'à épuisement | oui | 40 ms | 1 à 5 | 523, 527, 522, 525, 526 | moyenne 0,791 (0,787 à 0,795) | 265 |
| porte apprise | oui | 40 ms | 1 à 5 | 555, 554, 550, 551, 550 | moyenne 0,833 (0,830 à 0,837) | 265 |
| Jev jusqu'à épuisement | oui | 400 ms | 7 | 524 | 0,790 | 265 |
| porte apprise | oui | 400 ms | 7 | 546 | 0,824 | 265 |
| Jev jusqu'à épuisement | non | 400 ms | 7 | 483 | 0,729 | 84 |
| porte apprise | non | 400 ms | 7 | 471 | 0,710 | 84 |

Le routeur local seul obtient 456 sur 663, soit les 152 sur 221 enregistrés par l'étude, trois fois : ses réponses sont enregistrées, et chaque passe les répète.

**Calculé.** En attendant sa voie choisie, à dépense égale (265 appels Jev, 0,03206 USD), la porte apprise bat « Jev jusqu'à épuisement » à chaque graine, de 32, 27, 28, 26 et 24 questions : **4,1 points** en moyenne (27,4 sur 663). Sur la graine 7, avec une voie à 400 ms, elle gagne de 22.

**D'où vient le gain.** Les mêmes fichiers, regroupés par contexte sur les graines 1 à 5 (`to_jev` : part des éléments envoyés à Jev ; `acc_local` et `acc_jev` : exactitude sur les éléments auxquels chaque bras a répondu) :

```sql
SELECT ctx,
       regexp_extract(filename, 'route-([a-z]+)-wait', 1) AS policy,
       count(*) / 5 AS per_run,
       round(avg((arm = 'jev')::INT), 2) AS to_jev,
       round(avg(correct::INT), 3) AS acc,
       round(avg(correct::INT) FILTER (WHERE arm = 'local'), 2) AS acc_local,
       round(avg(correct::INT) FILTER (WHERE arm = 'jev'), 2) AS acc_jev
FROM read_json('route-*-wait-seed[1-5]/results.jsonl', filename = true, union_by_name = true)
GROUP BY ALL ORDER BY ctx, policy;
```

```text
┌───────┬─────────┬─────────┬────────┬────────┬───────────┬─────────┐
│  ctx  │ policy  │ per_run │ to_jev │  acc   │ acc_local │ acc_jev │
│ int64 │ varchar │ double  │ double │ double │  double   │ double  │
├───────┼─────────┼─────────┼────────┼────────┼───────────┼─────────┤
│     0 │ jev     │   114.0 │   0.41 │  0.602 │      0.35 │    0.97 │
│     0 │ learned │   114.0 │   0.88 │  0.896 │      0.34 │    0.97 │
│     1 │ jev     │    66.0 │    0.4 │  0.894 │      0.82 │     1.0 │
│     1 │ learned │    66.0 │   0.56 │  0.912 │       0.8 │     1.0 │
│     2 │ jev     │    63.0 │   0.38 │  0.584 │      0.47 │    0.77 │
│     2 │ learned │    63.0 │    0.5 │  0.619 │      0.48 │    0.75 │
│     3 │ jev     │    15.0 │    0.4 │    1.0 │       1.0 │     1.0 │
│     3 │ learned │    15.0 │   0.19 │    1.0 │       1.0 │     1.0 │
│     4 │ jev     │   273.0 │   0.41 │  0.805 │      0.71 │    0.94 │
│     4 │ learned │   273.0 │    0.3 │  0.779 │      0.71 │    0.94 │
│     5 │ jev     │   132.0 │   0.41 │   0.95 │      0.93 │    0.97 │
│     5 │ learned │   132.0 │   0.09 │  0.932 │      0.93 │    0.95 │
└───────┴─────────┴─────────┴────────┴────────┴───────────┴─────────┘
  12 rows                                                 7 columns
```

« Jev jusqu'à épuisement » envoie à Jev les premiers 40 % du flux, quel que soit le contexte. La porte apprend que, dans le contexte 0, où le routeur local a décliné et où l'expert par mots-clés propose un skill, le routeur local a raison sur environ un tiers des éléments et Jev sur 97 % : elle lui en envoie 88 %. Elle le paie dans le contexte 5, où le routeur local est sûr de lui et où l'expert par mots-clés est d'accord, en n'y envoyant que 9 %. Elle perd un peu dans les contextes 4 et 5 et gagne bien davantage dans le contexte 0.

**Une remarque sur les reçus.** Le message du commit `14dccd0` donne la porte apprise à 0,832 (0,828 à 0,837). Les fichiers donnent 0,833 (0,830 à 0,837), parce que le dossier de la graine 3 a été réécrit environ cinq minutes après le commit par une version ultérieure de l'exemple, et que cette nouvelle exécution a eu une question juste de plus (550 au lieu de 549, le seul total qui s'arrondit à 0,828). L'écart de 4,1 points est le même dans les deux cas. La section 8 explique pourquoi deux exécutions de même graine peuvent différer.

## 6. La capacité, une troisième ressource

Sans attente, le même budget achète beaucoup moins. La voie de Jev contient 4 éléments et a 4 travailleurs, chacun occupé 400 ms par appel : au plus 10 appels par seconde, alors qu'une exécution entière de 663 éléments a pris environ 8,6 secondes. Une porte qui trouve la voie pleine la saute et garde la réponse locale. Sur la graine 7, seuls **84 des 265 appels payables** ont eu lieu (0,01016 USD sur 0,03208), sous les deux politiques, et toutes deux finissent entre 0,71 et 0,73. Dans cette exécution, la règle fixe a fait mieux que la porte, 483 contre 471 : quand la capacité refuse la plupart des choix de la porte, ce qu'elle a appris sur la qualité ne décide plus rien.

C'est le facteur de capacité des couches à mélange d'experts. Dans le Switch Transformer (Fedus, Zoph et Shazeer, 2021), chaque expert prend au plus un nombre fixe de tokens par lot, et les tokens qui débordent sautent l'expert et passent inchangés par la connexion résiduelle. Un routeur dépense de la qualité et de l'argent, mais aussi le débit de chaque expert. Les prix de la porte ne couvrent que l'argent. Faire d'« attendre ou déborder » un choix que la porte apprend, avec la latence comptée comme un coût, reste à faire.

## 7. Une vérification de Petri avant l'exécution

Les threads peuvent-ils s'interbloquer ? [`petri.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L1-L23) traduit le graphe en réseau de Petri avec `ix-petri`. `ix-petri` n'a pas de capacité de place, donc chaque canal devient deux places : les valeurs qu'il contient, et ses places libres, qui partent de sa capacité. Chaque envoi prend une place libre et chaque réception en rend une, si bien que la paire contient toujours `cap` jetons et que le réseau est borné par construction. Les travailleurs d'un nœud sont des jetons de sa place `idle`. Un travailleur prend une valeur et la garde ; il peut ne rien envoyer, comme un filtre, ou s'engager vers un port et y attendre une place libre ; sur un port qui perd, il peut aussi lâcher ce qu'il tient.

Le réseau peut s'engager vers un port à tout moment, ce qui est plus que ne font les threads : il a donc tous les comportements des threads, et un réseau sans interblocage garantit des threads sans interblocage. La réciproque est fausse : un interblocage signalé peut ne jamais être atteint par les threads.

**Acyclique veut dire sans interblocage, sans exploration.** Supposons que les liens bloquants, tous sauf ceux qui perdent, ne forment aucun cycle. Un marquage mort exigerait un travailleur en attente sur un nœud plein dont tous les travailleurs attendent plus bas. En suivant les liens bloquants vers l'aval d'un graphe acyclique, on finit sur un puits, qui prend toujours : un tel marquage n'existe donc pas. [`check`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L243) répond donc tout de suite pour un graphe acyclique, même une chaîne de centaines de nœuds, et n'explore les marquages accessibles que s'il y a un cycle. C'est le `Dag` d'`ix-pipeline`, qui refuse une arête fermant un cycle, qui dit si les liens bloquants sont acycliques. Le graphe de routage de la section 5 est acyclique : son `petri.json` indique `method: acyclic`, 26 places, 22 transitions, 0 état exploré.

**Une boucle de reprise se coince ; un lien qui perd la libère.** La forme de test [`retry_loop`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L254-L269) est source → porte → expert → juge → fin, plus un lien du juge vers la porte pour ce qu'il rejette ; chaque canal contient une valeur et chaque nœud a un travailleur. Un programme jetable qui appelle `check` et `explore` sur cette forme a affiché, au commit épinglé :

```text
waiting retry, check: method=Reachability deadlock_free=Some(false) states=1728 places=21 transitions=18
dead marking: done free=1 rows waiting on gate=1 gate waiting on expert=1 expert waiting on judge=1 judge waiting on gate=1 gate queued=1 expert queued=1 judge queued=1
witness: 44 firings, the last four: rows picks gate, gate picks expert, expert picks judge, judge picks gate
lossy retry, check: method=Acyclic deadlock_free=Some(true) states=0 places=21 transitions=19
lossy retry, explore: method=Reachability deadlock_free=Some(true) states=1728 places=21 transitions=19
```

Dans le marquage mort, chaque canal de la boucle est plein et chaque travailleur tient une valeur qu'il ne peut pas placer : le juge attend la porte, qui attend l'expert, qui attend le juge. Le témoin est la suite de 44 franchissements qui y mène. Rendez le lien de reprise perdant, et les liens bloquants redeviennent acycliques : `check` répond sans explorer, et une exploration complète des mêmes 1728 marquages le confirme. Une reprise perdue compte comme `refused` dans les statistiques du nœud : la perte reste visible. C'est aussi pourquoi le juge de la section 3 parle à la porte par le bus et non par un canal.

### Exercice pratique 3

Pourquoi l'argument acyclique échoue-t-il pour la boucle de reprise ?

> **Réponse :** il suit les liens bloquants vers l'aval jusqu'à un puits, qui prend toujours. Dans la boucle, juge → porte est un lien bloquant : les liens partis de la porte y reviennent et n'atteignent jamais de puits, si bien que chaque nœud du cycle peut être plein et attendre le suivant.

### Exercice pratique 4

Vous devez garder les reprises. Donnez deux façons de garder la boucle sans interblocage, et ce que chacune coûte.

> **Réponse :** rendre le lien de reprise perdant, et une reprise est perdue chaque fois que la porte est pleine (la perte est comptée) ; ou sortir la reprise des canaux, comme le bus le fait pour les retours, et une reprise arrive alors quand elle arrive, sans garantie qu'elle arrive. Dans les deux cas, on renonce à une garantie sur les reprises pour obtenir une garantie contre l'interblocage.

## 8. Trois leçons sur les reçus

**Décliner, c'est répondre.** La première ébauche de cette expérience était une simulation Python hors ligne. Elle comptait faux les refus du routeur local et lui donnait 55 % ; le flux, qui note les réponses enregistrées face aux étiquettes, a trouvé 68,8 %. Recalculé à partir des fichiers enregistrés : le routeur local décline 60 des 221 questions, et 31 d'entre elles sont les 31 questions hors sujet, toutes. Comptez un refus comme la réponse `__none__`, et le routeur a raison sur 152 des 221 (0,688) ; comptez-le faux, et il a raison sur 121 (0,548). Le code de la simulation n'a pas été conservé ; ses 55 % sont ce que donne cette erreur de notation.

**Une graine fixe l'ordre du flux, pas l'exécution.** La graine fixe l'ordre dans lequel DuckDB envoie les éléments. La porte apprend de signaux qui arrivent pendant que d'autres travailleurs tournent : deux exécutions de même graine peuvent donc faire des choix différents. La nouvelle exécution de la graine 3, en section 5, a bougé d'une question.

**Un reçu peut être écrasé.** La session qui a construit la crate a annoncé une exécution avec une voie Claude Haiku en direct (12 appels sur l'abonnement de la personne) à 0,840, graine 11. Le dossier de la graine 11 contient aujourd'hui une exécution sans cette voie, à 557 sur 663 (0,840), et aucun dossier de travail Claude n'existe. Le nom du dossier encodait la politique, le mode d'attente et la graine, mais pas le plafond Claude : une exécution a écrit par-dessus l'autre, et on ne peut plus dire de laquelle vient le 0,840. Faute de reçu, ce module ne donne aucun chiffre pour la voie Claude. Chaque option qui change le graphe a sa place dans le nom du dossier où une exécution écrit.

## 9. Ce que cela montre, et ce que cela ne montre pas

**Montré :**

- la contre-pression d'un nœud lent jusqu'au processus DuckDB, et l'annulation dans l'autre sens, par des tests qui passent ;
- à dépense égale, quand la porte attend son choix, un bandit par contexte avec un prix fictif réglé sur le rythme bat « Jev jusqu'à épuisement » sur chacune des cinq graines, de 4,1 points en moyenne ;
- sans attente, c'est la capacité d'un expert, et non son budget, qui limite ;
- des liens bloquants acycliques ne peuvent pas s'interbloquer, et une boucle de reprise de liens bloquants le peut.

**Pas montré :**

- Jev en direct : chaque réponse de Jev est rejouée à partir des reçus de l'étude, et sa latence est une pause ;
- la généralité : un seul corpus de 221 questions écrites par un modèle, vues trois fois, si bien que la porte est notée sur les questions dont elle apprend. Une passe réservée est la prochaine vérification. Sur des titres de questions écrits par des personnes (l'étape 4 de l'étude), le même routeur local a envoyé à un skill 32 des 86 questions qu'il aurait dû décliner ;
- la significativité : cinq graines d'un seul dispositif, appariées par graine, sans test ;
- le débit en build release : ces exécutions sont des builds debug ;
- la voie Claude (section 8).

## Points clés

- Un canal borné est tout le mécanisme de contre-pression : un nœud lent bloque ceux qui lui envoient, jusqu'au moteur SQL, et les valeurs en vol ont une borne que l'on peut calculer.
- Les retours passent par un bus qui perd, jamais par un canal en sens inverse : un routeur qui attend ses propres retours peut se coincer.
- Une porte sous budget ne dépense là où elle gagne le plus que si son prix suit le rythme du budget ; c'est le registre, et non le prix, qui est l'arrêt ferme.
- La qualité et l'argent ne suffisent pas : la capacité d'un expert décide quand le routeur ne peut pas attendre.
- Vérifiez le graphe avant l'exécution : des liens bloquants acycliques sont sans interblocage par un argument, et un cycle demande une exploration ou un lien qui perd.

## Provenance

- **Code :** GuitarAlchemist/ix, branche `exp/loop-nodes`, commit `14dccd0ef1fb0f4395d38f5beed9ad42fa458eab` (2026-10-16), crate `crates/ix-stream`. La branche a reçu depuis des nœuds SQL (commit `944f42c`), que ce module ne couvre pas.
- **Données :** l'étude du routeur Jev au commit `7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da`, dans `state/router-spike/` : le corpus `jev/corpora/full-sol.json`, les réponses locales `jev/full/local-c2-merge.json`, les réponses et la consommation de Jev `jev/full/jev-eval.json`, et `RESULTS.md`.
- **Résultats :** les 16 dossiers `route-*` qu'`examples/route.rs` a écrits le 2026-10-16 sur la machine de l'auteur, lus pour ce module le même jour. Ils ne sont pas publiés. Deux d'entre eux, local et « Jev jusqu'à épuisement » sans attente sur la graine 7, précèdent le commit d'environ un quart d'heure : leur premier événement n'a pas les champs `wait` et `jev_workers` qu'écrit l'exemple commité.
- **Tests :** `cargo test -p ix-stream --test stream -- --include-ignored` au commit épinglé : 18 passés.
- **Cycle de recherche :** aucun. Ce module a été écrit à partir d'une tranche traceuse menée dans une session Claude Code, et non par `/seldon research-cycle`, et aucune fiche n'existe pour lui sous `state/streeling/research-cycles/`. Il lui faut une revue humaine avant de compter comme publié.

On peut refaire des exécutions de ce genre avec la CLI DuckDB et Zig dans le chemin (ou `IX_DUCKDB` et `IX_ZIG`). L'exemple du commit nomme ses dossiers de sortie comme le tableau ci-dessus :

```text
cargo run -p ix-stream --example route -- --policy learned --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy jev --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy learned --seed 7
```

## Pour aller plus loin

- [CYB-001](../../cybernetics/fr/cyb-001-vsm-ai-governance-mapping.fr.md) : le canal algédonique dans la gouvernance de Demerzel.
- [CS-002](../../computer-science/fr/cs-002-governing-agentic-loops.fr.md) : des bornes que le cadre impose, et non le modèle.
- [PSY-025](../../psychohistory/fr/psy-025-capstone-preregistered-forecast.fr.md) : le préenregistrement, que l'étude Jev a appliqué à chacune de ses étapes.

## Références

- Reactive Streams, version 1.0, `Subscription.request(n)`.
- Stafford Beer, *Brain of the Firm*, 1972 : le signal algédonique du modèle du système viable.
- Peter Auer, Nicolò Cesa-Bianchi et Paul Fischer, « Finite-time Analysis of the Multiarmed Bandit Problem », *Machine Learning* 47, 2002 : UCB1.
- William Fedus, Barret Zoph et Noam Shazeer, « Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity », arXiv:2101.03961, 2021 : la capacité des experts et le facteur de capacité.
- Tadao Murata, « Petri Nets: Properties, Analysis and Applications », *Proceedings of the IEEE* 77(4), 1989 : des places bornées par des places complémentaires.

---
*Produit pour le Département de recherche sur IX le 2026-10-16 à partir des reçus listés sous « Provenance ». Aucun cycle de recherche ; revue humaine en attente.*
