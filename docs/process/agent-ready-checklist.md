# Agent-Ready Checklist

This checklist summarizes the Hybrid Definition of Ready and Hybrid Definition of Done. It is designed to be copied into issue and pull request templates.

## Definition of Ready (Issue Checklist)

Before delegating an issue (especially to an AI worker), ensure the following are defined:

- [ ] **Clear task goal:** Is the objective precise and achievable?
- [ ] **Context and source links:** Are relevant files, prior PRs, or design docs linked?
- [ ] **Allowed paths:** Are the directories/files to be modified explicitly restricted?
- [ ] **Non-goals:** Is it clear what *should not* be done (e.g., "no broad refactor")?
- [ ] **Expected output artifacts:** What tangible deliverables are required?
- [ ] **Test/validation plan:** How will we verify correctness? (e.g., exact test command)
- [ ] **Stop conditions:** When should the agent halt and escalate?
- [ ] **Risk tier:** Is this Low (docs), Medium (code), or High/Critical (policy)?
- [ ] **Dependency links:** Are blocking/blocked-by issues identified?
- [ ] **Suggested worker:** Which persona or capability is best suited?
- [ ] **Acceptance criteria:** What bullet points must be true to close this?
- [ ] **Reviewer expectations:** Who will review, and what are they looking for?

## Definition of Done (Pull Request Checklist)

Before merging a pull request, ensure the following are met:

- [ ] **Linked source issue:** Does the PR reference the shaping issue?
- [ ] **Clear summary:** Does the description explain what changed and why?
- [ ] **Tests/validation evidence:** Is proof of correctness included (e.g., test logs, validation output)?
- [ ] **Changed-path risk notes:** Are the risks of touching these specific files acknowledged?
- [ ] **Follow-up issues:** If scope was trimmed, are the new issues created and linked?
- [ ] **Review findings resolved:** Have all reviewer comments been addressed or explicitly accepted?
- [ ] **No auto-merge expectation:** Is human-in-the-loop oversight confirmed?
- [ ] **Merge decision:** Has an authorized human or Demerzel tribunal approved the merge?
