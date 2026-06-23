---
name: remembering-conversations
description: Search past Cursor conversations for decisions, patterns, and solutions. Use when user asks 'how should I...', 'what's the best approach...', references past work ('last time', 'we discussed', 'you implemented'), or when stuck on a problem after exploring current code. Searches conversation history from state.vscdb and agent transcripts.
---

# Remembering Conversations

**Core principle:** Search before reinventing. Searching costs nothing; reinventing or repeating mistakes costs everything.

## Mandatory: Dispatch a Search Agent

**Always dispatch a subagent to search.** This preserves your main context window.

Announce: "Searching past conversations for [topic]..."

Then dispatch using the Task tool:

```
Task tool:
  subagent_type: "generalPurpose"
  description: "Search past conversations for [topic]"
  prompt: |
    Run this search script and return the results:

    python3 /path/to/skills/remembering-conversations/scripts/search_conversations.py "your query here" --limit 5

    Then for the top 2-3 relevant results, read the full conversation:

    python3 /path/to/skills/remembering-conversations/scripts/read_conversation.py <conversation-id>

    Synthesize findings into 200-1000 words covering:
    - Key decisions made
    - Patterns/approaches used
    - Gotchas or warnings
    - Relevant code snippets
    Include conversation IDs as sources.
```

**Use this exact script path:** `SKILL_DIR/scripts/search_conversations.py` where SKILL_DIR is the directory containing this SKILL.md file.

## When to Search

**After understanding the task:**
- User asks "how should I..." or "what's the best approach..."
- You've explored current code and need to make architectural decisions
- User asks for implementation approach after describing requirements

**When you're stuck:**
- Investigated a problem without finding a solution
- Complex problem with no obvious answer in current code
- Need to follow an unfamiliar workflow or process

**When historical signals are present:**
- User says "last time", "before", "we discussed", "you implemented"
- User asks "why did we...", "what was the reason..."
- User says "do you remember...", "what do we know about..."

**Don't search:**
- For current codebase structure (use Grep/Read first)
- For info already in current conversation
- Before understanding what you're being asked to do

## Script Reference

### search_conversations.py

Search past conversations using FTS5 with BM25 ranking.

```bash
# Basic search
python3 scripts/search_conversations.py "authentication middleware"

# With date filter
python3 scripts/search_conversations.py "database migration" --after 2025-01-01

# JSON output for programmatic use
python3 scripts/search_conversations.py "error handling" --output json --limit 5

# Force rebuild the search index
python3 scripts/search_conversations.py "query" --rebuild

# Rebuild index only (no search)
python3 scripts/search_conversations.py --rebuild-only --days 90
```

**Data sources:** Extracts from Cursor's `state.vscdb` (composer conversations) and agent transcript JSONL files from `~/.cursor/projects/*/agent-transcripts/`.

**Index:** Auto-builds a local FTS5 SQLite index. Rebuilds every 4 hours or on `--rebuild`.

### read_conversation.py

Display a specific conversation.

```bash
# By conversation UUID
python3 scripts/read_conversation.py <uuid>

# By file path
python3 scripts/read_conversation.py /path/to/transcript.jsonl

# Paginate long conversations
python3 scripts/read_conversation.py <uuid> --start-line 5 --end-line 15
```

## Search Strategy

1. **Start broad** — use 2-3 keyword terms
2. **Review results** — check titles and snippets for relevance
3. **Read top matches** — use `read_conversation.py` on the 2-3 most relevant
4. **Synthesize** — extract decisions, patterns, gotchas, and code examples
5. **Apply** — use findings to inform current task

## Setup

Scripts use only Python standard library (no external dependencies). If future enhancements add packages:

```bash
bash scripts/setup.sh
```

This creates a `.venv` in the skill directory and installs from `requirements.txt`.
