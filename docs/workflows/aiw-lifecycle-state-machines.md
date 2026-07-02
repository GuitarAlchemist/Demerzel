# AIW Lifecycle State Machines

This document defines the explicit lifecycle state machines for Demerzel-managed AI/human work. These machines make allowed transitions explicit, prevent hidden state, and provide stable inputs for policy evaluation, Mission Control, fan-out/fan-in, and learning systems.

## Key Principles

- **Visibility**: Human override transitions must never be hidden.
- **Multiple Views**: Do not use one global AIW status for everything. Each aspect of work has its own lifecycle.
- **Independence**: GitHub comments are not the only source of state.
- **Safety First**: Do not auto-merge based on state alone.
- **MVP Status**: This initial specification remains advisory/dry-run until reviewed and implemented in the policy engine.

## State Transition Output Format

Each transition must emit a standard event format:

```yaml
transition_result:
  subject: string           # e.g., "issue-592", "pr-123"
  from_state: string        # e.g., "ready"
  to_state: string          # e.g., "delegated"
  allowed: true|false       # whether the transition is valid
  required_rules: []        # rules evaluated to permit/deny this transition
  blocking_reasons: []      # if allowed=false, why
  evidence_refs: []         # pointers to justification (e.g. review findings, policy overrides)
```

## State Machines

### IssueLifecycle
Tracks the overall lifecycle of a GitHub issue through the AIW pipeline.

```text
IssueLifecycle:
new -> grooming -> ready -> delegated -> in_progress -> pr_opened -> done
                                      -> blocked -> resumed
                                      -> superseded
```

- **new**: Issue is created, unclassified.
- **grooming**: Issue is actively being shaped (Pocock lane).
- **ready**: Issue meets the Definition of Ready and has `ready-for-agent` label.
- **delegated**: Issue is assigned to an AI worker (e.g. `jules` label applied).
- **in_progress**: Worker has acknowledged and begun work.
- **blocked**: Work cannot continue without external input or dependency resolution.
- **resumed**: Blockage is cleared; work continues.
- **pr_opened**: A pull request has been submitted for this issue.
- **done**: The PR is merged or the issue is otherwise resolved.
- **superseded**: Issue is replaced by a newer or broader issue.

### WorkPackageLifecycle
Tracks a distinct chunk of work dispatched to an agent (often matching a single prompt execution).

```text
WorkPackageLifecycle:
defined -> dispatched -> executing -> evaluating -> completed
                                   -> failed -> retrying -> failed_terminal
                                   -> preempted
```

- **defined**: Task is scoped but not yet sent to a worker.
- **dispatched**: Task is sent to the Tool Gateway / Worker.
- **executing**: Worker is actively processing the task.
- **evaluating**: Worker has produced output that is being verified (e.g. tests running).
- **completed**: Output meets acceptance criteria.
- **failed**: Output failed criteria; worker may try again.
- **retrying**: Worker is attempting the task again after a failure.
- **failed_terminal**: Task failed and retry limits are exhausted.
- **preempted**: Task was cancelled (e.g., by human override or HALT).

### BatchLifecycle
Tracks a group of related WorkPackages, useful for parallel execution and fan-out/fan-in control.

```text
BatchLifecycle:
proposed -> active -> constrained -> draining -> complete
                   -> halted -> recovery -> active
```

- **proposed**: Batch is formulated but not yet executing.
- **active**: Batch is running normally.
- **constrained**: Batch is running but rate-limited (Adaptive Fan-out Policy).
- **draining**: Batch is finishing current tasks but not accepting new ones.
- **complete**: All tasks in the batch have reached a terminal state.
- **halted**: Batch is explicitly paused (e.g. via `HALT-ALL`).
- **recovery**: Batch is being resumed after a halt.

### PullRequestLifecycle
Tracks the lifecycle of an AI-generated Pull Request.

```text
PullRequestLifecycle:
draft -> ready_for_review -> reviewed -> merge_candidate -> merged
                            -> changes_requested -> updated
                            -> rejected
```

- **draft**: PR is opened but not yet ready for human review.
- **ready_for_review**: PR is complete and awaits human or AI Adversarial review.
- **reviewed**: Review is complete with no blocking issues.
- **changes_requested**: Review found issues requiring updates.
- **updated**: PR has new commits addressing feedback.
- **merge_candidate**: PR passed all checks, reviews, and policies (ready for human to click Merge).
- **merged**: PR is merged into the target branch.
- **rejected**: PR is closed without merging.

### WorkerTaskLifecycle
Tracks the internal state of a specific AI worker processing a task.

```text
WorkerTaskLifecycle:
initializing -> context_gathering -> reasoning -> acting -> finalizing
                                              -> error
```

- **initializing**: Worker is starting up and loading persona/instructions.
- **context_gathering**: Worker is exploring codebase and reading necessary files.
- **reasoning**: Worker is planning and deciding on actions.
- **acting**: Worker is making code changes or running tools.
- **finalizing**: Worker is verifying work and preparing the final output.
- **error**: Worker encountered an unrecoverable error during execution.

### ExecutionEpisodeLifecycle
Tracks a distinct Cherny-lane loop execution, often tied to a single token budget allocation.

```text
ExecutionEpisodeLifecycle:
started -> running -> budget_warning -> budget_exhausted -> suspended
                   -> goal_met -> finished
                   -> context_limit_reached -> summarizing
```

- **started**: Episode begins with a fresh context.
- **running**: Episode is executing normally.
- **budget_warning**: Episode is approaching its token/cost limit.
- **budget_exhausted**: Episode hit its limit and must pause.
- **goal_met**: The explicit goal condition (e.g. `/goal`) was achieved.
- **finished**: Episode concluded successfully.
- **context_limit_reached**: The LLM context window is full.
- **summarizing**: Episode is capturing a digest before restarting (Cherny loop).

### ReviewLifecycle
Tracks the state of a specific review (AI or human) on a PR or WorkPackage.

```text
ReviewLifecycle:
pending -> in_progress -> completed_approve
                       -> completed_request_changes
                       -> completed_comment_only
                       -> dismissed
```

- **pending**: Review is requested but not started.
- **in_progress**: Reviewer is actively examining the changes.
- **completed_approve**: Reviewer approved the changes.
- **completed_request_changes**: Reviewer requested specific changes.
- **completed_comment_only**: Reviewer left non-blocking feedback.
- **dismissed**: The review was explicitly dismissed (e.g. due to new commits).

### PolicyExceptionLifecycle
Tracks the state of an explicit override or exception to a Demerzel governance policy.

```text
PolicyExceptionLifecycle:
requested -> evaluating -> approved -> active -> expired
                        -> denied
                        -> revoked
```

- **requested**: An exception is requested (e.g. via issue or PR comment).
- **evaluating**: The request is being reviewed by a human authority.
- **approved**: The exception is granted.
- **denied**: The exception is refused.
- **active**: The exception is currently in effect.
- **expired**: The time or scope limit of the exception has passed.
- **revoked**: The exception was manually cancelled before expiration.

### EvidenceBundleLifecycle
Tracks the collection and validation of required evidence (e.g. test logs, screenshots) before merging.

```text
EvidenceBundleLifecycle:
empty -> collecting -> partial -> complete -> validated
                                           -> invalid
```

- **empty**: No evidence collected yet.
- **collecting**: Evidence is actively being gathered.
- **partial**: Some evidence is present, but missing required pieces.
- **complete**: All required evidence types are present.
- **validated**: Evidence has been verified as authentic and sufficient.
- **invalid**: Evidence is corrupted, faked, or insufficient.

## Relationships to Other Issues

- **#588 (Policy Engine)**: These state machines provide the stable `from_state` and `to_state` inputs that the policy engine evaluates. The policy engine dictates whether a transition is `allowed`.
- **#568 (AIW Execution Pipeline)**: Defines the overall flow that these state machines track.
- **#570 (Execution Graph)**: The graph nodes and edges will often correspond to transitions in the `WorkPackageLifecycle` and `WorkerTaskLifecycle`.
- **#579 (AI Worker Context & Memory)**: Context resets occur around transitions in the `ExecutionEpisodeLifecycle` (e.g. `summarizing` -> `started`).
- **#584 (Tool Gateway)**: Tool invocation usually happens in the `acting` state of the `WorkerTaskLifecycle`.
- **#586 (Cost & Token Economics)**: Drives the transitions into `budget_warning` and `budget_exhausted` in the `ExecutionEpisodeLifecycle`.
- **#547 (Hybrid Definition of Done)**: Required before transitioning a PR to `merge_candidate`.
- **#490 (Demerzel Authority Rules)**: Governs the `PolicyExceptionLifecycle` and final `merge_candidate` -> `merged` transitions.
