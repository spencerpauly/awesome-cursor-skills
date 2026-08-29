# Alibaba Java Coding Guidelines (English Edition) — Agent Skill

> Enforce the **official English edition** of the Alibaba Java Coding Guidelines (5 sections, **181 rules**: 124 Mandatory / 57 Recommended / 24 For Reference) as an AI-executable Java coding standard: self-check before coding, verify item by item during review, and look up the original rules when in doubt. Bundled with an upstream-sync pipeline that regenerates the manual from the official GitHub Markdown source in one command.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## What this is

The official English translation of the *Alibaba Java Coding Guidelines*, published by Alibaba in the [`alibaba/Alibaba-Java-Coding-Guidelines`](https://github.com/alibaba/Alibaba-Java-Coding-Guidelines) repository. This package turns the manual into an **AI-executable development standard**:

- `SKILL.md` — trigger conditions + workflow (self-check / review / query / update)
- `references/review-checklist-en.md` — tickable English review checklist (204 items, grouped by section)
- `references/java-coding-guidelines-en.md` — full English manual (cleaned Markdown transcription, 5 sections)
- `scripts/update_guidelines_en.py` — upstream-sync pipeline (download + clean + rebuild, stdlib only)

Coverage (5 sections):

- **1. Programming Specification** — naming, constants, formatting, OOP, collections, concurrency, flow control, comments, other
- **2. Exception and Logs**
- **3. MySQL Rules** — table schema, index, SQL, ORM
- **4. Project Specification** — application layers, library, server
- **5. Security Specification**

> **Version note:** this English edition corresponds to an **early version** of the Chinese manual (approx. 1.0.x). It predates the Huangshan v1.7.1 manual (7 sections, 327 rules). For the complete up-to-date Chinese manual, use the companion skill [`alibaba-java-coding-guidelines`](https://github.com/Castlebin/alibaba-java-coding-guidelines).

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.claude/skills/alibaba-java-coding-guidelines-en
```

### Codex (OpenAI Codex CLI)

```bash
# User-level (global):
mkdir -p ~/.codex/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.codex/skills/alibaba-java-coding-guidelines-en

# Or project-level:
mkdir -p .codex/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" .codex/skills/alibaba-java-coding-guidelines-en
```

### Cursor

```bash
# Project-level (recommended): place it in the project root
mkdir -p .cursor/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" .cursor/skills/alibaba-java-coding-guidelines-en

# Or user-level (global):
mkdir -p ~/.cursor/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.cursor/skills/alibaba-java-coding-guidelines-en
```

### OpenCode

```bash
# Project-level:
mkdir -p .opencode/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" .opencode/skills/alibaba-java-coding-guidelines-en

# Or user-level (global):
mkdir -p ~/.config/opencode/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.config/opencode/skills/alibaba-java-coding-guidelines-en
```

### WorkBuddy (CodeBuddy)

```bash
git clone https://github.com/Castlebin/alibaba-java-coding-guidelines-en.git
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.workbuddy/skills/alibaba-java-coding-guidelines-en
```

Or simply copy the directory into `~/.workbuddy/skills/`. The skill then triggers automatically whenever you write or review Java code in English.

### Trae (TraeWork)

```bash
# User-level (global):
mkdir -p ~/.trae/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.trae/skills/alibaba-java-coding-guidelines-en

# Or project-level:
mkdir -p .trae/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" .trae/skills/alibaba-java-coding-guidelines-en
```

### Qoder (QoderWork)

```bash
# User-level (global):
mkdir -p ~/.qoder/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" ~/.qoder/skills/alibaba-java-coding-guidelines-en

# Or project-level:
mkdir -p .qoder/skills
ln -s "$(pwd)/alibaba-java-coding-guidelines-en" .qoder/skills/alibaba-java-coding-guidelines-en
```

### Generic (any agent)

```bash
git clone https://github.com/Castlebin/alibaba-java-coding-guidelines-en.git
```

Then wire `SKILL.md` + `references/` + `scripts/` into your agent environment as a skill package.

## Usage

| Scenario | Behavior |
| --- | --- |
| Writing / editing Java code | Auto-load the checklist; self-check the affected sections (naming / OOP / collections / concurrency / exceptions / MySQL, etc.) |
| Java code review | Tick items section by section; output a Pass / Conditional pass / Fail verdict + violation list (mandatory violations block the merge) |
| Querying rules | `grep` the manual for positive/counter examples and notes |
| Updating the manual | Run `scripts/update_guidelines_en.py`; it downloads the official English README from GitHub and regenerates the Markdown |

## Layout

```
alibaba-java-coding-guidelines-en/
├── SKILL.md                          # skill entry: triggers + workflow
├── references/
│   ├── java-coding-guidelines-en.md  # full English manual (auto-transcribed, do not hand-edit)
│   └── review-checklist-en.md        # tickable English review checklist
├── scripts/
│   └── update_guidelines_en.py       # upstream README → Markdown pipeline
├── LICENSE                           # Apache-2.0
└── README.md
```

## Contributing / PRs

This skill has been submitted to the following community skill collections (PRs):

| Collection | PR |
| --- | --- |
| BehiSecc/awesome-claude-skills | [#644](https://github.com/BehiSecc/awesome-claude-skills/pull/644) |
| travisvn/awesome-claude-skills | [#1182](https://github.com/travisvn/awesome-claude-skills/pull/1182) |
| spencerpauly/awesome-cursor-skills | [#58](https://github.com/spencerpauly/awesome-cursor-skills/pull/58) |
| TheArchitectit/awesome-opencode-skills | [#7](https://github.com/TheArchitectit/awesome-opencode-skills/pull/7) |
| ComposioHQ/awesome-claude-skills | [#1757](https://github.com/ComposioHQ/awesome-claude-skills/pull/1757) |

## License

Apache-2.0. The manual content is derived from the official Alibaba repositories (also Apache-2.0).
