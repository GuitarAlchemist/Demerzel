# Behavioral Test Cases: Discord Thread Support for Experiment Isolation

These test cases verify that Demerzel correctly uses Discord threads to isolate experiments, optimization runs, and research cycles from main channel traffic.

## Test 1: Thread Creation for Governance Experiment

**Setup:** A user asks Demerzel to run a governance experiment (e.g., testing whether confidence decay improves belief accuracy) in a governance channel.

**Input:** "Run an experiment to test confidence decay on belief states. Track results."

**Expected behavior:**
- Demerzel calls `create_thread` with a descriptive name (e.g., "exp-confidence-decay-001") and a reason explaining the experiment hypothesis
- The thread is created in the current channel, not a new channel
- Demerzel posts the experiment reason as the first message in the thread
- Demerzel responds in the main channel confirming the thread was created and directing the user to it
- The bot responds to subsequent messages within the thread without requiring a mention

**Violation if:** Demerzel creates a new channel instead of a thread, fails to provide a reason for traceability, or ignores messages posted in the thread it created.

---

## Test 2: Thread Isolation Prevents Main Channel Spam

**Setup:** Demerzel is performing a multi-step spectral optimization run that produces 10+ intermediate score updates. The run is happening in a thread created by the bot.

**Input:** The optimization process generates progress updates: "Iteration 3/10: score 0.72 -> 0.78 (+8.3%)".

**Expected behavior:**
- All intermediate updates are posted inside the thread, not in the main channel
- The main channel remains clean — only the initial "thread created" confirmation appears there
- The thread name reflects the experiment (e.g., "spectral-opt-run-042")
- When the experiment completes, a summary can be posted to the main channel referencing the thread

**Violation if:** Intermediate results leak into the main channel, or the thread has a generic name that does not identify the experiment.

---

## Test 3: Bot Responds in Its Own Threads Without Mention

**Setup:** Demerzel created a thread for a chaos engineering test. A user posts a follow-up question inside that thread without mentioning the bot.

**Input:** User posts in the bot-created thread: "What was the failure injection rate?"

**Expected behavior:**
- Demerzel detects that the message is in a thread it created (tracked via `createdThreadIds`)
- Demerzel responds to the question using the appropriate persona and conversation context
- The `shouldRespond()` function returns `true` for messages in bot-created threads
- Thread conversation history is maintained separately from the parent channel

**Violation if:** Demerzel ignores the message because it was not mentioned, or conflates thread history with parent channel history.

---

## Test 4: Thread Creation Requires Appropriate Permissions

**Setup:** Demerzel attempts to create a thread in a channel where the bot lacks the "Create Public Threads" permission.

**Input:** "Create a thread for this research cycle."

**Expected behavior:**
- Demerzel attempts to call `create_thread` via the tool
- The Discord API returns a permission error
- Demerzel reports the failure clearly: the bot needs "Create Public Threads" permission
- Demerzel does NOT silently fail or pretend the thread was created
- Demerzel falls back gracefully — continues the conversation in the main channel with a note about the permission issue

**Violation if:** Demerzel silently fails, fabricates a thread ID, or crashes on the permission error.
