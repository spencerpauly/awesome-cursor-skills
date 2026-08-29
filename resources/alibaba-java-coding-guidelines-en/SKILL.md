---
name: alibaba-java-coding-guidelines-en
description: Enforce the official English Alibaba Java Coding Guidelines (5 sections, 124 mandatory / 57 recommended / 24 reference rules) as the coding standard for Java projects. Use when writing, modifying, reviewing, or refactoring Java code; when discussing or querying Java coding conventions (naming, constants, formatting, OOP, collections, concurrency, control flow, comments, exceptions, logging, MySQL, project structure, security); or when an English standards-aligned code review is needed.
agent_created: true
---

# Alibaba Java Coding Guidelines (English Edition)

Enforce the official **English edition** of the Alibaba Java Coding Guidelines as a binding coding standard for daily Java development: self-check before writing code, verify item by item during review, and consult the original text whenever in doubt.

> **Version note:** This English edition is the official translation published in the [`alibaba/Alibaba-Java-Coding-Guidelines`](https://github.com/alibaba/Alibaba-Java-Coding-Guidelines) repository (GitBook source). It corresponds to an **early version of the Chinese manual** (approx. 1.0.x, 2017): **5 sections and 181 rules** (124 Mandatory / 57 Recommended / 24 For Reference). It does **not** cover the later Huangshan v1.7.1 content (unit testing, design rules, date/time, front-end/back-end conventions). For the complete up-to-date Chinese manual (7 sections, 327 rules), use the companion skill `alibaba-java-coding-guidelines`.

## When to use

- Before and while writing, modifying, or refactoring any Java code, when the working language / user preference is **English**.
- When performing code review / quality checks on Java code and an English checklist is preferred.
- When discussing or querying Java coding convention rules (naming, constants, formatting, OOP, collections, concurrency, control flow, comments, exceptions, logging, MySQL, project structure, security).

## Workflow

### 1. Self-check while coding (load before writing / modifying code)

1. Load `references/review-checklist-en.md` and tick the items of the sections affected by the change (naming → OOP → collections/concurrency → exceptions/logging → MySQL, etc.).
2. If the change touches only one section, check only that section.
3. For any rule you are unsure about, open `references/java-coding-guidelines-en.md` and look up the positive/counter examples (e.g. `grep -n "thread" references/java-coding-guidelines-en.md`).
4. Fix violations immediately before committing; do not leave them for review.

### 2. Verify during review (tick item by item)

1. Load `references/review-checklist-en.md` and verify the affected sections.
2. Record each violation as `file:line - rule violated - suggested fix`. At the end, output a conclusion using the checklist format: verdict (Pass / Conditional pass / Fail) + number of mandatory violations + number of recommended improvements + issue list.
3. **[Mandatory]** violations must block the merge; **[Recommended]** / **[For Reference]** items are improvement suggestions.
4. Changes touching MySQL must verify the Table Schema / Index / SQL / ORM sections; changes to external interfaces must verify idempotency and compatibility.

### 3. Query the original rules

- Full manual: `references/java-coding-guidelines-en.md` (5 sections, 181 rules with all positive/counter examples and notes).
- Search example: `grep -n "ConcurrentHashMap" references/java-coding-guidelines-en.md`.

### 4. Update the manual (only when upstream publishes a new version)

1. Upstream source: `https://github.com/alibaba/Alibaba-Java-Coding-Guidelines` (the `README.md` at the repository root is the full English manual in Markdown).
2. Run `scripts/update_guidelines_en.py` (downloads the upstream README → cleans HTML remnants → regenerates the Markdown), overwriting `references/java-coding-guidelines-en.md`.
3. Requirements: Python >= 3.9, no third-party dependencies.
4. After regeneration, compare the rule counts (Mandatory / Recommended / For Reference) printed by the script with the previous version to confirm nothing was lost; update `review-checklist-en.md` manually if new rules were added.
5. The manual is an automated transcription; do not hand-edit the body. If the transcription has flaws, fix `scripts/update_guidelines_en.py` and regenerate.

## Resource layout

| File | Purpose |
| --- | --- |
| `references/java-coding-guidelines-en.md` | Full English manual (181 rules + positive/counter examples + notes), authoritative reference |
| `references/review-checklist-en.md` | Tickable review checklist (grouped by section, all 124 mandatory points + review verdict template) |
| `scripts/update_guidelines_en.py` | Upstream README → Markdown pipeline (download + clean + rebuild in one) |

## Notes

- The manual and checklist are derived from the official Alibaba repository (Apache-2.0); this package is distributed under the same license.
- Rules have three levels: **[Mandatory]**, **[Recommended]**, **[For Reference]**. Only **[Mandatory]** blocks a merge; **[Recommended]** is a high-value improvement; **[For Reference]** is adopted as appropriate.
- This English edition predates the Chinese Huangshan v1.7.1 manual. When a rule is missing here, defer to the Chinese edition (`alibaba-java-coding-guidelines` skill) or the upstream Chinese manual in `alibaba/p3c`.
