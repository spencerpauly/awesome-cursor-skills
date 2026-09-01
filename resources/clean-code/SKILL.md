---
name: clean-code
description: >-
  Use when writing, refactoring, or reviewing application code in frontend or
  backend projects; when naming is unclear, functions/classes are large, comments
  apologize for bad code, error handling uses null/error codes, tests are slow or
  sparse, or the user mentions clean code, Boy Scout Rule, SRP, or code smells.
---

# Clean Code

Distilled from Robert C. Martin, *Clean Code* (Prentice Hall). Apply these rules when creating or changing code. Prefer clarity over cleverness. Leave the module cleaner than you found it (**Boy Scout Rule**).

**Stack-agnostic.** Examples assume TypeScript; map the same rules to any language.

For the full smell/heuristic catalog, see [heuristics.md](heuristics.md).

## How to apply (every change)

1. Read surrounding code; match its conventions unless they violate a rule below.
2. Make the smallest change that satisfies the request **and** improves clarity.
3. Before finishing, run the **Done checklist**.
4. Do not rewrite unrelated modules “while you’re here.”

## Core rules

### Names

| Do | Don’t |
| --- | --- |
| Intention-revealing names (`elapsedDays`, `isActive`) | Cryptic abbreviations, `data`, `temp`, `mgr` |
| Pronounceable, searchable names | Single-letter names outside tiny loops |
| One word per concept (`fetch` *or* `get`, not both) | Cute puns, Hungarian/`m_` encodings |
| Classes = nouns; functions = verbs | Names that need mental mapping |

Longer names are fine for larger scopes. Names must describe side effects (`createUserAndSendEmail`, not `createUser` if it also emails).

### Functions

- **Small.** Do **one thing** at one abstraction level (stepdown: high-level → next level down).
- Prefer **0–2 arguments**. Avoid flag booleans; split into two functions or use an options object with a clear type.
- **No surprising side effects.** Command/query separation: mutators don’t return query data unless that is the explicit API.
- Prefer **exceptions** (or Result types) over error codes mixed into happy-path returns.
- Extract `try/catch` bodies; error handling is its own “one thing.”
- **DRY** — duplicated logic is a defect waiting to happen. Three similar blocks → extract.

### Comments

Code should explain *what*. Comments explain *why* (intent, warning, non-obvious constraint).

| Allowed | Forbidden |
| --- | --- |
| Legal headers, public API docs, TODOs with context | Narrating what the next line does |
| Warning of consequences | Commented-out code (delete it; use VCS) |
| Clarifying regex/complex invariant | Journal/changelog comments, noisy markers |

If you need a comment to make bad code readable, **rename or extract** instead.

### Formatting

- File reads like a **newspaper**: top = overview, then details.
- Related code vertically close; concepts separated by blank lines.
- Follow **team** formatting (formatter/linter). Don’t bikeshed style in PRs if CI formats.

### Objects, data, boundaries

- Don’t expose guts through long getter chains (**Law of Demeter** / no train wrecks).
- Keep **DTOs** dumb (data); keep domain objects behavior-rich — don’t hybridize carelessly.
- Third-party APIs: wrap at a **boundary**; write learning tests against the library; don’t leak vendor types through the app core.

### Error handling

- Prefer exceptions / typed failures over return codes strewn through logic.
- Provide **context** in errors (what failed, which id/input shape).
- Don’t return or pass **null** for “missing” when an empty object, `Optional`/`undefined` with narrowing, or a Result is clearer — be consistent per codebase.
- Define the **normal flow**; push edge cases to boundaries.

### Classes & modules

- **Small**, one **responsibility** (SRP). If the name needs “and”, split.
- High cohesion: fields used by most methods. Many small classes beat god classes.
- Depend on abstractions at boundaries; isolate modules from change (DI / ports).

### Tests

- Tests are production code — keep them clean.
- **F.I.R.S.T.**: Fast, Independent, Repeatable, Self-validating, Timely.
- One concept per test; cover boundaries; don’t skip “trivial” cases that lock behavior.
- Three TDD laws when doing TDD: no production code without a failing test; write only enough test to fail; write only enough code to pass.

### Systems & concurrency

- Separate **construction** (wiring, `main`, DI) from **use**.
- Keep configurable values at high levels; don’t bury magic constants.
- Concurrency: minimize shared mutable state; keep concurrent code small and obviously correct; prefer proven libraries over hand-rolled locks.

## Frontend adaptations

| Clean Code idea | Frontend practice |
| --- | --- |
| Small functions | Small components/hooks; one reason to render or one side-effect concern |
| One abstraction level | Page composes features; feature composes UI primitives — no fetch+layout+form in one file |
| Meaningful names | Props/events: `onSubmitSearch`, not `onAction`; state: `isPanelOpen` |
| No side-effect surprises | Hooks named `useX` that also write localStorage must say so; prefer explicit effects |
| Demeter | Avoid `props.user.profile.settings.theme` in leaves — pass what the child needs |
| Errors | Error boundaries for render failures; typed API error mapping near the client boundary |
| Tests | Behavior tests (user-visible), not implementation snapshots of internals |

Avoid: mega-components, inline one-off components redefined every render, “utils.ts” grab-bags with unrelated helpers.

## Backend adaptations

| Clean Code idea | Backend practice |
| --- | --- |
| Small functions | Handlers validate + delegate; services do one use-case; repos do persistence only |
| Boundaries | Wrap DB/HTTP/SDK clients; map to domain types before use-cases |
| Errors | Map domain failures → HTTP/status once at the edge; don’t leak SQL/vendor errors |
| DTOs | Request/response types at the edge; don’t pass raw rows through the app |
| Names | `searchProducts`, `upsertBySku` — say what and the key |
| Tests | Unit-test pure domain/ranking; integration-test repos against real DB when available |

Avoid: god `*Service` classes, flag arguments for divergent use-cases, returning `null` with ambiguous meaning from repositories.

## Done checklist

Copy and tick before claiming done:

```
- [ ] Names reveal intent; no encodings or cute misdirection
- [ ] New/changed functions stay small and do one thing
- [ ] No new flag-argument APIs or surprising side effects
- [ ] No commented-out code; comments only for why/warnings
- [ ] Errors have context; null/error-code mess not introduced
- [ ] Boundaries respected (no vendor types deep in core)
- [ ] Tests updated/added for behavior and boundaries; still fast
- [ ] Module is slightly cleaner than before (Boy Scout)
```

## Red flags (stop and fix)

- Function/component scrolls more than a screen without extraction
- `boolean` parameter that flips behavior
- Comment duplicates the next line
- `// TODO: fix later` on code you just wrote without a ticket/context
- Catch-all `catch (e) {}` or empty catch
- Duplicate blocks differing only by variable names
- Class/module named `Manager`, `Helper`, `Util`, `Common` with mixed duties
- Test that needs the whole app booted for pure logic

## Common rationalizations

| Excuse | Reality |
| --- | --- |
| “I’ll clean it in a follow-up” | You won’t. Boy Scout now, smallest improvement. |
| “Comment makes it clear enough” | Rename/extract; comments rot. |
| “It’s just a DTO / just UI” | Still needs clear names and one responsibility. |
| “Framework requires this mess” | Isolate mess at the boundary; keep core clean. |
| “Tests would take longer than the fix” | Untested clean-looking code is still risky; add a focused test. |

## Source

Principles summarized from *Clean Code* by Robert C. Martin. Heuristic ids (G1, N1, …) in [heuristics.md](heuristics.md) match Chapter 17 for cross-reference — not a substitute for the book.
