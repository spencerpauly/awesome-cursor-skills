# Cursor IDE Prompting Best Practices

## Prompt Quality Framework

### Tier 1: Excellent Prompts (Score 9-10)
- Specify the **goal**, **context**, and **constraints** in a single message
- Reference specific files with `@file` or full paths
- Include error messages verbatim when debugging
- State the desired output format or behavior
- Mention frameworks, libraries, or language versions in use

**Example:**
> @auth.ts Fix the JWT token refresh logic. When the access token expires, the refresh
> endpoint returns 401 instead of issuing a new token. The refresh token is stored in
> httpOnly cookies. We use Express 4 + jsonwebtoken. Keep the existing middleware pattern.

### Tier 2: Good Prompts (Score 7-8)
- Clear intent with some context
- May reference files but not always the right ones
- Provides enough for the AI to act but may need one follow-up

**Example:**
> The login page redirects incorrectly after authentication. I think the issue is in
> the auth callback handler. Can you check and fix it?

### Tier 3: Mediocre Prompts (Score 4-6)
- Vague intent, missing context
- No file references or error messages
- Likely requires multiple follow-ups

**Example:**
> The login is broken, fix it

### Tier 4: Poor Prompts (Score 1-3)
- Single word or extremely vague
- No actionable information
- Wastes turns clarifying

**Example:**
> help
> this doesn't work

---

## Common Anti-Patterns

### 1. The Vague Bug Report
**Bad:** "It's not working"
**Good:** "The `/api/users` endpoint returns 500 when the `email` field contains a `+` character. Here's the error from the logs: [paste error]"

### 2. The Missing Context
**Bad:** "Add authentication"
**Good:** "Add JWT authentication to the Express API in `src/routes/`. Use RS256 with keys from env vars. Protect all routes except `/health` and `/auth/login`."

### 3. The Overly Broad Request
**Bad:** "Refactor this codebase"
**Good:** "Extract the database queries from `UserController` into a `UserRepository` class following the repository pattern. Keep the same public interface."

### 4. Not Using @-mentions
**Bad:** "Fix the function that calculates tax"
**Good:** "@utils/tax.ts Fix `calculateTax()` — it doesn't handle the case where `state` is null, causing a TypeError."

### 5. Multi-Task Overload
**Bad:** "Add auth, fix the CSS, update the README, and deploy"
**Good:** Focus on one task per prompt, or explicitly number separate tasks.

---

## Feature Usage Tips

### Chat (Cmd+L)
- Best for: explanations, debugging, learning, code review
- Tip: paste error messages directly; use @-mentions for file context

### Composer (Cmd+I)
- Best for: multi-file edits, new features, refactoring
- Tip: describe the end state, not the steps; let Composer plan the approach

### Inline Edit (Cmd+K)
- Best for: small, localized changes within a single file
- Tip: select the relevant code first, then describe the change

### Tab Completion
- Best for: accepting AI suggestions while typing
- Tip: write a clear comment or function signature first, then let tab fill in

### Terminal (Cmd+`)
- Best for: running commands with AI assistance
- Tip: describe what you want to accomplish, not the exact command

---

## Context Maximization Strategies

1. **Use `.cursorrules`** — project-level instructions that persist across all conversations
2. **Use `@codebase`** — lets the AI search your entire codebase for relevant context
3. **Use `@docs`** — reference external documentation URLs
4. **Use `@web`** — search the web for current information
5. **Pin important files** — keep critical files in context across turns
6. **Use folders** — `@src/components/` to reference an entire directory
7. **Reference recent changes** — `@git` for recent diffs and commits
