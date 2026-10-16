---
module_id: ixr-001-streams-under-budgets
department: ix-research
course: "Streaming IX Pipelines Under Budgets"
level: intermediate
prerequisites: []
estimated_duration: "40 minutes"
produced_by: claude-ix-research
research_cycle: null
version: "0.1.0"
---

# Streams Under Budgets: Back-Pressure, a Learned Gate and a Petri Check

> **Department of IX Research** | Intermediate | 40 minutes | English draft; human review pending. No research-cycle record exists for this module (see "Provenance").

## Objectives and project question

After this module you can:

- explain how bounded channels turn a slow node into back-pressure, up to the SQL engine that feeds the stream, and how a stop travels the other way;
- route each item to one expert under a money budget, and name the three resources such a router spends: quality, money and capacity;
- send feedback from a judge back to a router without a channel cycle;
- tell, before a run, whether a graph of waiting links can deadlock, and what one lossy link changes.

**Project question:** can a stream of guitar questions be routed between a free local router and a paid expert, under a fixed budget, so that it beats a fixed rule at equal spend, with no queue that grows and no deadlock?

The study is the crate [`ix-stream`](https://github.com/GuitarAlchemist/ix/tree/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream), commit [`14dccd0`](https://github.com/GuitarAlchemist/ix/commit/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab) on the branch `exp/loop-nodes` of GuitarAlchemist/ix. Every code link below is pinned to that commit.

## 1. The starting point: a pipeline that neither streams nor runs in parallel

IX already runs pipelines: `ix-pipeline` lowers an `ix.yaml` into a DAG and executes it. Its executor goes level by level, with a barrier after each level, and each node takes one whole JSON value. The branch for a level of several nodes says "run in parallel", but it runs every node in the current thread, as the comment inside it says, because a node's compute function is not `Send` ([`executor.rs`, lines 164–211](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-pipeline/src/executor.rs#L164-L211)).

So a pipeline over a large query waits for the whole result, then runs its nodes one after another. Nothing pushes back when a node is slow, because nothing flows. `ix-stream` is a tracer slice for the other model: values flow one at a time through a graph of threads joined by bounded channels.

## 2. Back-pressure and cancellation

Each node of an `ix-stream` graph is one or more threads that share an input channel holding at most `cap` values ([`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/lib.rs#L1-L16)). A send to a full channel waits. That wait is the back-pressure: a slow node holds back everything upstream of it, down to the source, instead of letting a queue grow. It is the `request(n)` of Reactive Streams in its plainest form, `n` being the free slots.

The source can be a DuckDB query. [`source::duckdb`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/source.rs#L28) runs the `duckdb` CLI with `-jsonlines` and sends each row as it reads it. When the graph is full, the source stops reading, the pipe fills, and DuckDB waits on its write: the back-pressure reaches the SQL engine.

Cancellation runs the other way. When a node stops, or all its workers end, its input is dropped and every send to it fails. A node whose every link leads to ended nodes stops too, so the stop climbs to the source, and the DuckDB source then kills its process: a query nobody reads any more stops computing.

**Tested.** [`a_full_channel_holds_the_source_back`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L13-L61) builds the chain source → `a` (cap 2, 1 worker) → `b` (cap 3, 2 workers) → `sink` (cap 4, 1 worker), holds the sink on its first value, and counts the values that have left the source after 400 ms against this bound:

```rust
// Values in channels, plus one in each worker's hand, plus the source's next one.
let bound = (2 + 1) + (3 + 2) + (4 + 1) + 1;
```

So at most 14 of the 10,000 values leave the source while the sink holds. [`a_stopped_graph_stops_the_duckdb_query`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L374-L401) checks that stopping the graph stops the query. The 18 tests of `tests/stream.rs` passed at the pinned commit on 2026-10-16, including the 3 that need the DuckDB CLI (Windows 11, DuckDB v1.5.3, debug build); the first and last lines of their output:

```text
running 18 tests
test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.41s
```

### Practice Exercise 1

A chain source → `parse` (cap 8, 4 workers) → `score` (cap 2, 1 worker) → `sink` (cap 16, 1 worker). The sink blocks on its first value. At most how many values can have left the source?

> **Answer:** each node holds its channel plus one value per worker: (8 + 4) + (2 + 1) + (16 + 1) = 32, plus the one value the source holds while it waits to send: 33. The bound does not depend on the length of the stream, which is the point of back-pressure.

## 3. Feedback without a cycle: the algedonic bus

A router that learns must hear how its choices turned out, and the judge sits downstream of it. A channel from the judge back to the router would close a cycle of waiting links, and section 6 shows that such a cycle can wedge.

`ix-stream` sends feedback on a separate [`Bus`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/bus.rs) instead. A publisher never waits: each subscriber has its own bounded queue, and an event that finds it full is lost for that subscriber and counted. Signals of pleasure (valence +1) and pain (−1) travel there: the judge says right or wrong about each item, a paid lane reports the share of its budget each call spent, and the router reports pain when a lane it wanted was full. Before it routes the next item, the router reads the signals that have arrived, and it never waits for one.

The name comes from Stafford Beer's Viable System Model, where an algedonic signal bypasses the normal hierarchy. [CYB-001](../../cybernetics/en/cyb-001-vsm-ai-governance-mapping.md) names the missing algedonic channel as Gap D of Demerzel's governance. This bus applies the same idea inside one pipeline, and it loses events rather than block, because here a signal is a hint for learning, not an alarm.

## 4. A gate that routes like a mixture-of-experts router, under budgets

The [gate](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs) sends each item to one expert, an *arm*. For each context, a bucket the caller computes, it keeps a UCB1 bandit from `ix-rl` that estimates how good each arm's answers turned out. It ranks the arms by

```text
score(arm) = q(arm) + 0.3 * sqrt(2 * ln(N) / n(arm)) - price(arm)
```

where `q` is the arm's mean judged quality in that context, `n` how often it was judged there and `N` the context's total. An arm never tried in a context scores +∞, so each arm is tried once. The 0.3 is the gate's default exploration weight.

An arm with a budget has a shadow price that follows its pace ([`price`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L178)):

```text
price(arm) = max(0, base_price + 4 * (spent / cap - share of the stream seen))
```

The price is infinite when the budget cannot pay one more call, and 4 is the default gain. Spending ahead of pace raises the price, which keeps the arm for the contexts where it gains the most; falling behind lowers it. The price only steers. The hard stop is the [`Ledger`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/gate.rs#L58): a lane spends from it, and the ledger refuses a call it cannot pay.

### Practice Exercise 2

The Jev arm has base price 0.02. Halfway through the stream, Jev has spent 60% of its budget. What is its price? And if it had spent 40%?

> **Answer:** 0.02 + 4 × (0.6 − 0.5) = 0.42: Jev now wins a context only where its estimated quality, plus its exploration bonus, beats the free local router's by more than 0.42. At 40%: 0.02 + 4 × (0.4 − 0.5) = −0.38, floored at 0, so Jev costs nothing until it catches up with its pace.

## 5. The experiment: 663 guitar questions, two experts, one budget

[`examples/route.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs) streams the 221 labelled questions of the Jev router study: 190 ask for one of GA's 32 skills and 31 are out of scope, labelled `__none__` ([`RESULTS.md`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/RESULTS.md), Stage 3). It streams them three times, in an order DuckDB shuffles by a seeded hash: 663 items. Each item goes through:

1. `local`: the answer the local embedding router (`c2-merge`) gave it, recorded, with its confidence;
2. `kw`: a keyword expert written in Zig, built for WASI and run in `ix-wasm`'s sandbox;
3. `gate`: accept `local` or ask Jev, in one of six contexts ([`context`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/examples/route.rs#L279)): the local router declined, was below 0.7 or was at least 0.7, times whether `kw` agrees with it;
4. `jev`: Jev's recorded answer, after a sleep that stands for a live call's latency, charged the study's average cost per call. Jev is TypeSafe's hosted zero-shot classifier `jev-1.13.0`. **Nothing is sent to Jev**: the answers are replayed from the receipts of the study;
5. `judge`: compares the answer with the label and signals right or wrong on the bus.

The example can also add a live Claude Haiku lane on the person's plan, capped in calls. None is used by default, and no result below includes one (see section 8).

**The budget.** The study's 221 recorded Jev calls cost $0.026733 at the rate card, computed from reported input tokens, not an invoice ([`full/jev-eval.json`](https://github.com/GuitarAlchemist/ix/blob/7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da/state/router-spike/jev/full/jev-eval.json)): $0.000120962 per call. The example gives Jev 40% of the stream: 0.4 × 663 × $0.000120962 = **$0.0320792472, the price of 265.2 calls**.

**The policies.** `local` always keeps the local answer. `jev` asks Jev until its budget is spent, then keeps the local answer: "Jev until spent". `learned` is the gate of section 4.

**Waiting or not.** With `--wait`, the gate waits for its first choice when that lane is full. Without it, a full lane is passed over for the next choice, as a mixture of experts drops what overflows an expert's capacity.

**Observed.** Each run writes `results.jsonl`, one line per item. This query counts each run's right answers and the Jev calls that were made:

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

The five-seed runs replayed Jev with a 40 ms sleep (`--jev-ms 40`); the seed-7 runs used the default 400 ms. Every run gave Jev 4 workers.

| Policy | Waits | Jev sleep | Seeds | Right of 663 | Accuracy | Jev calls |
|---|---|---|---|---|---|---|
| local | — | — | 7 | 456 | 0.688 | 0 |
| Jev until spent | yes | 40 ms | 1–5 | 523, 527, 522, 525, 526 | mean 0.791 (0.787–0.795) | 265 |
| learned gate | yes | 40 ms | 1–5 | 555, 554, 550, 551, 550 | mean 0.833 (0.830–0.837) | 265 |
| Jev until spent | yes | 400 ms | 7 | 524 | 0.790 | 265 |
| learned gate | yes | 400 ms | 7 | 546 | 0.824 | 265 |
| Jev until spent | no | 400 ms | 7 | 483 | 0.729 | 84 |
| learned gate | no | 400 ms | 7 | 471 | 0.710 | 84 |

The local router alone gets 456 of 663, which is the study's recorded 152 of 221, three times: its answers are recorded, so every pass repeats them.

**Computed.** Waiting on its chosen lane, at the same spend (265 Jev calls, $0.03206), the learned gate beats "Jev until spent" on every seed, by 32, 27, 28, 26 and 24 questions: **4.1 points** on average (27.4 of 663). On seed 7, with a 400 ms lane, it wins by 22.

**Where the gain comes from.** The same files, grouped by context over seeds 1 to 5 (`to_jev`: share of the items sent to Jev; `acc_local` and `acc_jev`: accuracy on the items each arm answered):

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

"Jev until spent" sends the first 40% of the stream to Jev, whatever the context. The gate learns that in context 0, where the local router declined and the keyword expert proposes a skill, local is right on about a third of the items and Jev on 97%: it sends 88% of them to Jev. It pays for that in context 5, where the local router is confident and the keyword expert agrees, by sending only 9% there. It loses a little in contexts 4 and 5 and gains much more in context 0.

**A note on the receipts.** The commit message of `14dccd0` reports the learned gate at 0.832 (0.828–0.837). The files give 0.833 (0.830–0.837), because the seed-3 folder was rewritten about five minutes after the commit by a later version of the example, and that rerun got one more question right (550 instead of 549, the only count that rounds to 0.828). The gap of 4.1 points is the same either way. Section 8 says why a rerun with the same seed can differ.

## 6. Capacity, a third resource

Without waiting, the same budget buys much less. Jev's lane holds 4 items and has 4 workers, each busy 400 ms per call: at most 10 calls a second, while a whole run of 663 items took about 8.6 seconds. A gate that finds the lane full passes it over and keeps the local answer. On seed 7, only **84 of the 265 payable calls** happened ($0.01016 of $0.03208), under both policies, and both landed between 0.71 and 0.73. In that run the fixed rule did better than the gate, 483 against 471: when capacity refuses most of the gate's choices, what it learned about quality is not what decides.

This is the capacity factor of mixture-of-experts layers. In the Switch Transformer (Fedus, Zoph and Shazeer, 2021), each expert takes at most a fixed number of tokens per batch, and the tokens that overflow it skip the expert and pass unchanged through the residual connection. A router spends quality and money, and also each expert's throughput. The gate's prices cover money only. Making "wait or overflow" a choice the gate learns, with latency counted as a cost, is open work.

## 7. A Petri check before the run

Can the threads deadlock? [`petri.rs`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L1-L23) turns the graph into a Petri net with `ix-petri`. `ix-petri` has no place capacities, so each channel becomes two places: the values in it, and its free slots, which start at its capacity. Every send takes a free slot and every receive gives one back, so the pair always holds `cap` tokens and the net is bounded by construction. A node's workers are tokens in its `idle` place. A worker takes a value and holds it; it may send nothing, as a filter does, or commit to one port and wait there for a free slot; on a lossy port it can drop what it holds instead.

The net may commit to a port at any moment, which is more than the threads do, so the net has every behaviour the threads have: a deadlock-free net means deadlock-free threads. The converse does not hold: a reported deadlock can be one the threads never reach.

**Acyclic means deadlock-free, without exploring.** Suppose the waiting links, all but the lossy ones, form no cycle. A dead marking would need a worker waiting on a full node whose workers all wait further down. Following the waiting links down an acyclic graph ends at a sink, which always takes, so no such marking exists. [`check`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/src/petri.rs#L243) therefore answers at once for an acyclic graph, even a chain of hundreds of nodes, and explores the reachable markings only when there is a cycle. Whether the waiting links are acyclic is asked of `ix-pipeline`'s `Dag`, which refuses an edge that would close a cycle. The route graph of section 5 is acyclic: its `petri.json` reads `method: acyclic`, 26 places, 22 transitions, 0 states explored.

**A retry loop wedges; a lossy link frees it.** The test shape [`retry_loop`](https://github.com/GuitarAlchemist/ix/blob/14dccd0ef1fb0f4395d38f5beed9ad42fa458eab/crates/ix-stream/tests/stream.rs#L254-L269) is source → gate → expert → judge → done, plus a link from the judge back to the gate for what it rejects; each channel holds one value and each node has one worker. A throwaway program that calls `check` and `explore` on that shape printed, at the pinned commit:

```text
waiting retry, check: method=Reachability deadlock_free=Some(false) states=1728 places=21 transitions=18
dead marking: done free=1 rows waiting on gate=1 gate waiting on expert=1 expert waiting on judge=1 judge waiting on gate=1 gate queued=1 expert queued=1 judge queued=1
witness: 44 firings, the last four: rows picks gate, gate picks expert, expert picks judge, judge picks gate
lossy retry, check: method=Acyclic deadlock_free=Some(true) states=0 places=21 transitions=19
lossy retry, explore: method=Reachability deadlock_free=Some(true) states=1728 places=21 transitions=19
```

In the dead marking every channel of the loop is full and every worker holds a value it cannot place: the judge waits on the gate, which waits on the expert, which waits on the judge. The witness is the 44-firing sequence that leads there. Make the retry link lossy and the waiting links are acyclic again: `check` answers without exploring, and a full exploration of the same 1728 markings agrees. A dropped retry counts as `refused` in the node's stats, so the loss stays visible. This is also why the judge of section 3 talks to the gate on the bus and not through a channel.

### Practice Exercise 3

Why does the acyclic argument fail for the retry loop?

> **Answer:** it follows waiting links downstream until it reaches a sink, which always takes. In the loop, judge → gate is a waiting link, so the links from the gate lead back to the gate and never reach a sink: every node of the cycle can be full and waiting on the next one.

### Practice Exercise 4

You must keep the retries. Give two ways to keep the loop deadlock-free, and what each costs.

> **Answer:** make the retry link lossy, and a retry is lost whenever the gate is full (the loss is counted); or move the retry off the channels, as the bus does for feedback, and a retry then arrives when it arrives, with no guarantee that it arrives at all. Either way, a guarantee about retries is given up to get a guarantee about deadlock.

## 8. Three lessons about receipts

**A decline is an answer.** The first draft of this experiment was an offline Python simulation. It counted the local router's declines as wrong and put the router at 55%; the stream, scoring the recorded answers against the labels, found 68.8%. Recomputed from the recorded files: the local router declines 60 of the 221 questions, and 31 of them are the 31 out-of-scope questions, every one. Count a decline as the answer `__none__` and the router is right on 152 of 221 (0.688); count it as wrong and it is right on 121 (0.548). The simulation's code was not kept; its 55% is what that scoring error gives.

**A seed fixes the order of the stream, not the run.** The seed sets the order in which DuckDB sends the items. The gate learns from signals that arrive while other workers run, so two runs with the same seed can make different choices: the seed-3 rerun of section 5 moved by one question.

**A receipt can be overwritten.** The session that built the crate reported one run with a live Claude Haiku lane (12 calls on the person's plan) at 0.840, seed 11. The folder for seed 11 now holds a run without that lane, at 557 of 663 (0.840), and no Claude work folder exists. The folder's name encoded the policy, the waiting mode and the seed, not the Claude cap, so one run wrote over the other, and which of them the 0.840 came from can no longer be told. With no receipt left, this module gives no number for the Claude lane. Every flag that changes the graph belongs in the name of the folder a run writes to.

## 9. What this does and does not show

**Shown:**

- back-pressure from a slow node to the DuckDB process, and cancellation the other way, by tests that pass;
- at equal spend, with the gate waiting on its choice, a per-context bandit with a paced shadow price beats "Jev until spent" on each of five seeds, by 4.1 points on average;
- without waiting, an expert's capacity, not its budget, binds;
- acyclic waiting links cannot deadlock, and a retry loop of waiting links can.

**Not shown:**

- live Jev: every Jev answer is replayed from the study's receipts, and its latency is a sleep;
- generality: one corpus of 221 model-written questions, seen three times, so the gate is scored on the questions it learns from. A held-out pass is the next check. On question titles written by people (the study's Stage 4), the same local router sent 32 of the 86 it should have declined to a skill;
- significance: five seeds of one design, paired by seed, with no test;
- throughput in a release build: these runs are debug builds;
- the Claude lane (section 8).

## Key takeaways

- A bounded channel is the whole back-pressure mechanism: a slow node blocks its senders, up to the SQL engine, and the values in flight have a bound you can compute.
- Feedback travels on a lossy bus, never back through a channel: a router that waits for its own feedback can wedge.
- A gate under a budget spends where it gains the most only if its price follows the budget's pace; the ledger, not the price, is the hard stop.
- Quality and money are not enough: an expert's capacity decides when the router cannot wait.
- Check the graph before the run: acyclic waiting links are deadlock-free by argument, and a cycle needs an exploration or a lossy link.

## Provenance

- **Code:** GuitarAlchemist/ix, branch `exp/loop-nodes`, commit `14dccd0ef1fb0f4395d38f5beed9ad42fa458eab` (2026-10-16), crate `crates/ix-stream`. The branch has since gained SQL nodes (commit `944f42c`), which this module does not cover.
- **Data:** the Jev router study at commit `7c37c8c0a2530b9f7e339aba21bcb7f01c3b62da`, in `state/router-spike/`: the corpus `jev/corpora/full-sol.json`, the local answers `jev/full/local-c2-merge.json`, Jev's answers and usage `jev/full/jev-eval.json`, and `RESULTS.md`.
- **Results:** the 16 folders `route-*` that `examples/route.rs` wrote on 2026-10-16 on the author's machine, read for this module the same day. They are not published. Two of them, local and "Jev until spent" without waiting on seed 7, predate the commit by about a quarter of an hour: their first event lacks the `wait` and `jev_workers` fields that the committed example writes.
- **Tests:** `cargo test -p ix-stream --test stream -- --include-ignored` at the pinned commit: 18 passed.
- **Research cycle:** none. This module was written from a tracer slice run in a Claude Code session, not through `/seldon research-cycle`, and no record under `state/streeling/research-cycles/` exists for it. It needs a human review before it counts as published.

Runs like these can be made again with the DuckDB CLI and Zig on the path (or `IX_DUCKDB` and `IX_ZIG`). The commit's example names its output folders as the table above does:

```text
cargo run -p ix-stream --example route -- --policy learned --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy jev --wait --seed 1 --jev-ms 40
cargo run -p ix-stream --example route -- --policy learned --seed 7
```

## Further reading

- [CYB-001](../../cybernetics/en/cyb-001-vsm-ai-governance-mapping.md): the algedonic channel in Demerzel's governance.
- [CS-002](../../computer-science/en/cs-002-governing-agentic-loops.md): bounds that a framework, not the model, enforces.
- [PSY-025](../../psychohistory/en/psy-025-capstone-preregistered-forecast.md): preregistration, which the Jev study used for each of its stages.

## References

- Reactive Streams, version 1.0, `Subscription.request(n)`.
- Stafford Beer, *Brain of the Firm*, 1972: the algedonic signal of the Viable System Model.
- Peter Auer, Nicolò Cesa-Bianchi and Paul Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem", *Machine Learning* 47, 2002: UCB1.
- William Fedus, Barret Zoph and Noam Shazeer, "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", arXiv:2101.03961, 2021: expert capacity and the capacity factor.
- Tadao Murata, "Petri Nets: Properties, Analysis and Applications", *Proceedings of the IEEE* 77(4), 1989: bounded places through complementary places.

---
*Produced for the Department of IX Research on 2026-10-16 from the receipts listed under "Provenance". No research cycle; human review pending.*
