---
name: address-github-pr-comments
description: Process outstanding reviewer feedback, apply required fixes, and draft clear responses for each GitHub pull-request comment. Use when addressing PR review comments, implementing fixes from code reviews, or drafting responses to reviewers.
---

# Address GitHub PR Comments

Process and resolve GitHub pull request review comments systematically.

## Process

### 1. Sync and Audit Comments

- Read every unresolved comment
- Group comments by affected files or themes
- Identify dependencies or blockers

### 2. Plan Resolutions

- List the requested code edits for each thread
- Identify clarifications or additional context needed
- Note any dependencies or blockers before implementing

### 3. Implement Fixes

- Apply targeted updates addressing one comment thread at a time
- Run relevant tests or linters after impactful changes
- Stage changes with commits that reference the addressed feedback

### 4. Draft Responses

- Summarize the action taken or reasoning for each comment
- Link to commits or lines when clarification helps reviewers
- Highlight any remaining questions or follow-up needs

## Output Format

For each comment, provide:

1. **Comment Summary**: What the reviewer is asking for
2. **Action Required**: What needs to be done (fix/clarify/discuss)
3. **Suggested Fix**: Code changes or explanation
4. **Response Draft**: Professional reply to the reviewer

## Checklist

- [ ] All reviewer comments acknowledged
- [ ] Required code changes implemented and tested
- [ ] Clarifying explanations prepared for nuanced threads
- [ ] Follow-up items documented or escalated
- [ ] PR status updated for reviewers
