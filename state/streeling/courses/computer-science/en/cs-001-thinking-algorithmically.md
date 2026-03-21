---
module_id: cs-001-thinking-algorithmically
department: computer-science
course: Foundations of Computer Science
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: computer-science
version: "1.0.0"
---

# Thinking Algorithmically

> **Department of Computer Science** | Stage: Nigredo (Beginner) | Duration: 25 minutes

## Objectives

After this lesson, you will be able to:
- Define what an algorithm is and identify algorithms in everyday life
- Apply four key problem-solving techniques: decomposition, pattern recognition, abstraction, and divide-and-conquer
- Distinguish between greedy and exhaustive approaches
- Develop intuition for Big-O notation and why efficiency matters

---

## 1. What Is an Algorithm?

An **algorithm** is a finite sequence of well-defined steps that takes an input and produces an output. That is it. No computers required.

You follow algorithms every day:
- A cooking recipe is an algorithm (input: ingredients, output: a meal)
- Driving directions are an algorithm (input: current location, output: destination)
- The process of making change at a cash register is an algorithm (input: amount owed, output: fewest coins)

What separates an algorithm from vague instructions is **precision**. "Cook until done" is not an algorithm — it is ambiguous. "Heat to 180C for 25 minutes, then check internal temperature; if below 74C, continue in 5-minute increments" is an algorithm. Every step is unambiguous and the process terminates.

Three properties of a valid algorithm:
1. **Finiteness** — it must eventually stop
2. **Definiteness** — each step must be precisely defined
3. **Effectiveness** — each step must be something that can actually be carried out

### Practice Exercise

Write an algorithm (in plain English, numbered steps) for looking up a word in a physical dictionary. Be precise enough that someone who has never used a dictionary could follow your steps. Compare yours with the approach described in Section 5 (divide and conquer) — are they the same?

---

## 2. Decomposition — Breaking Problems Apart

The most powerful algorithmic thinking skill is **decomposition**: breaking a complex problem into smaller, manageable sub-problems.

**Example:** You want to organize a concert.

This is overwhelming as a single task. But decompose it:
1. Find a venue
2. Book performers
3. Set a date
4. Sell tickets
5. Arrange sound equipment
6. Promote the event

Each sub-problem is still complex, but now you can tackle them individually. And some sub-problems decompose further: "Sell tickets" becomes choose a platform, set prices, design the ticket, open sales.

Decomposition is recursive — you keep breaking things down until each piece is simple enough to solve directly. This is how every large software system is built: not as one giant program, but as thousands of small, composable pieces.

**Key insight:** If you cannot solve a problem, you probably have not decomposed it enough.

### Practice Exercise

Decompose the following problem into sub-problems: "Build a website that lets users search for guitar chords." Keep decomposing until each sub-problem is something one person could complete in a day or less. How many levels of decomposition did you need?

---

## 3. Pattern Recognition

**Pattern recognition** is the ability to notice similarities between problems you have already solved and new problems you face.

**Example:** Sorting a hand of playing cards and sorting a list of student names are the same problem — arranging items in order according to some comparison rule. Once you learn one sorting algorithm, you can apply it to anything that can be compared.

Patterns appear everywhere in computing:
- Searching through a collection (find a book in a library, find a file on disk, find a note on the fretboard)
- Filtering items that match criteria (spam filtering, photo search, chord lookup)
- Transforming data from one format to another (translation, file conversion, transposition)

Experienced programmers solve problems faster not because they are smarter, but because they recognize patterns. They see a new problem and think: "This is essentially a search problem" or "This is a graph traversal" — and they reach for a known solution.

### Practice Exercise

Consider these three problems. What pattern do they share?
1. Finding the shortest route between two cities
2. Finding the fewest chord changes to get from one chord to another
3. Finding the minimum number of moves to solve a puzzle

> They are all **shortest path** problems — finding the minimum-cost sequence of steps between a start state and a goal state.

---

## 4. Abstraction — Ignoring What Does Not Matter

**Abstraction** is the art of stripping away irrelevant detail to focus on what matters for the problem at hand.

When you draw a map, you do not include every tree, every crack in the pavement, every blade of grass. You include roads, landmarks, and distances — the details relevant to navigation. Everything else is abstracted away.

In algorithmic thinking, abstraction means:
- Representing a real-world problem with a simplified model
- Ignoring details that do not affect the solution
- Defining clear inputs and outputs

**Example:** If you want to find the shortest path between two cities, you do not need to model the color of the road signs or the speed limit on each road (unless speed matters for your problem). You abstract the map into a **graph**: cities are nodes, roads are edges, distances are weights. Now you can apply a graph algorithm without thinking about asphalt.

Abstraction is what allows algorithms to be **general-purpose**. A sorting algorithm does not care whether it is sorting numbers, names, or guitar chords. It only needs to know how to compare two items. Everything else is abstracted away.

### Practice Exercise

You are building a system to recommend practice routines for guitar students. What details about each student are relevant to the algorithm? What details can be abstracted away? Write two lists: "include" and "ignore."

---

## 5. Divide and Conquer

**Divide and conquer** is a specific algorithmic strategy:

1. **Divide** the problem into smaller sub-problems of the same type
2. **Conquer** each sub-problem (recursively, if needed)
3. **Combine** the results

This is different from general decomposition. In divide and conquer, the sub-problems have the **same structure** as the original — just smaller.

**Example — Binary Search (finding a word in a dictionary):**
1. Open the dictionary to the middle page
2. Is the word on this page? If yes, done.
3. If the word comes before this page alphabetically, repeat with the first half
4. If the word comes after, repeat with the second half
5. Keep halving until you find the word

Each step cuts the remaining search space in half. A dictionary with 100,000 words requires at most 17 steps (since 2^17 = 131,072 > 100,000). Compare that to starting at page 1 and reading every entry — up to 100,000 steps.

**Classic divide-and-conquer algorithms:**
- **Binary search** — finding an item in a sorted collection
- **Merge sort** — sorting by dividing, sorting halves, then merging
- **Quicksort** — sorting by choosing a pivot and partitioning

### Practice Exercise

You have a sorted list of 1,000 songs. Using binary search, what is the maximum number of comparisons needed to find a specific song? (Hint: how many times can you halve 1,000 before reaching 1?)

> log2(1000) ≈ 10. At most 10 comparisons — compared to 1,000 for a linear search.

---

## 6. Greedy vs Exhaustive Approaches

Two broad families of algorithms represent different philosophies:

**Greedy algorithms** make the locally optimal choice at each step, hoping this leads to a globally optimal solution.

*Example — Making change with the fewest coins:*
- Amount: 67 cents
- Greedy approach: take the largest coin that fits. 50 (quarter+quarter) → 15 (dime) → 5 (nickel) → 2 (penny+penny). Result: 25+25+10+5+1+1 = 6 coins.
- This works for US currency. But for a currency with coins of 1, 3, and 4 cents, greedy fails: for 6 cents, greedy gives 4+1+1 (3 coins) but the optimal is 3+3 (2 coins).

**Exhaustive algorithms** check every possible solution and pick the best one. They always find the optimal answer, but they can be slow.

*Example — The traveling salesman:*
- Visit 10 cities and return home by the shortest route
- Exhaustive: try all possible orderings (10! = 3,628,800 routes), measure each, pick the shortest
- This guarantees the optimal route, but is computationally expensive

| Approach | Advantage | Disadvantage | Use When |
|----------|-----------|-------------|----------|
| Greedy | Fast, simple | May miss the optimal solution | Good enough is good enough |
| Exhaustive | Guaranteed optimal | Slow for large problems | Correctness is critical and input is small |

Many real-world algorithms blend both: use greedy heuristics to prune the search space, then exhaustively check the remaining candidates.

### Practice Exercise

You are packing a suitcase with items of different weights and values, and the suitcase has a weight limit. Describe a greedy approach and an exhaustive approach. Which would you use if you had 5 items? 500 items?

> *Greedy:* Sort items by value-to-weight ratio, add items from highest ratio until the suitcase is full. *Exhaustive:* Try every possible combination, calculate total value for those within weight limit, pick the best. For 5 items (32 combinations), exhaustive is fine. For 500 items (2^500 combinations), exhaustive is impossible — use greedy or a smarter algorithm.

---

## 7. Big-O Intuition — How Fast Is Fast Enough?

Not all algorithms are created equal. **Big-O notation** describes how an algorithm's running time grows as the input size increases.

You do not need to calculate Big-O precisely right now. You need **intuition** for what the categories mean:

| Big-O | Name | Example | 1,000 items | 1,000,000 items |
|-------|------|---------|-------------|-----------------|
| O(1) | Constant | Looking up an array element by index | 1 step | 1 step |
| O(log n) | Logarithmic | Binary search | ~10 steps | ~20 steps |
| O(n) | Linear | Scanning every item once | 1,000 steps | 1,000,000 steps |
| O(n log n) | Linearithmic | Merge sort, quicksort | ~10,000 steps | ~20,000,000 steps |
| O(n^2) | Quadratic | Comparing every pair | 1,000,000 steps | 1,000,000,000,000 steps |
| O(2^n) | Exponential | Exhaustive subset search | ~10^301 steps | Forget it |

The key insight: **the difference between algorithm categories grows enormously with input size.** An O(n) algorithm and an O(n^2) algorithm might both feel instant on 10 items. On a million items, one finishes in a second and the other takes days.

This is why algorithmic thinking matters. Choosing the right algorithm can be the difference between a program that works and one that never finishes.

### Practice Exercise

You have two algorithms for searching a music library:
- Algorithm A: checks every song one by one (O(n))
- Algorithm B: uses a sorted index and binary search (O(log n))

For a library of 10 million songs, approximately how many steps does each take?
> A: 10,000,000 steps. B: log2(10,000,000) ≈ 23 steps. Algorithm B is over 400,000 times faster.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Algorithm** | A finite sequence of well-defined steps that transforms input into output |
| **Decomposition** | Breaking a complex problem into smaller, manageable sub-problems |
| **Pattern recognition** | Identifying similarities between a new problem and previously solved problems |
| **Abstraction** | Stripping away irrelevant detail to focus on what matters for the solution |
| **Divide and conquer** | Splitting a problem into smaller instances of the same problem, solving recursively |
| **Greedy algorithm** | Making the locally optimal choice at each step |
| **Exhaustive algorithm** | Checking every possible solution to guarantee finding the best one |
| **Big-O notation** | A classification of algorithm efficiency by how running time grows with input size |

---

## Self-Check Assessment

**1. What three properties must a valid algorithm have?**
> Finiteness (it terminates), definiteness (each step is unambiguous), and effectiveness (each step can actually be performed).

**2. You need to search for a name in an unsorted list of 1,000 names. What is the best Big-O you can achieve?**
> O(n) — linear search. Without sorting or indexing, you must potentially check every item. If the list were sorted, you could use binary search for O(log n).

**3. A greedy algorithm for making change gives the wrong answer for coins of 1, 3, and 4 cents when making 6 cents. Why?**
> The greedy approach picks the largest coin first (4), then needs 1+1 for the remainder (3 coins total). But 3+3 uses only 2 coins. Greedy fails because the locally optimal choice (largest coin) does not lead to the globally optimal solution.

**4. Why is O(n log n) considered efficient for sorting?**
> It has been mathematically proven that no comparison-based sorting algorithm can do better than O(n log n) in the worst case. Merge sort and quicksort achieve this bound, making them optimal among comparison sorts.

**Pass criteria:** Decompose a given problem into sub-problems, identify which algorithmic approach (greedy, exhaustive, divide-and-conquer) suits a given scenario, and explain Big-O differences using concrete examples.

---

## Research Basis

- Algorithmic thinking (decomposition, pattern recognition, abstraction) is recognized as a core computational thinking skill
- Divide and conquer, greedy, and exhaustive search are the three foundational algorithmic paradigms
- Big-O notation provides a hardware-independent measure of algorithm efficiency
- Teaching algorithmic intuition before formal analysis improves problem-solving transfer
- Sources: Computer science education consensus, Streeling Department of Computer Science curriculum
- Belief state: T(0.91) F(0.02) U(0.05) C(0.02)
