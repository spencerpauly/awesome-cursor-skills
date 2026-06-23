---
name: cursor-insights
description: "Analyze Cursor IDE usage patterns and improve prompting effectiveness. Use when the user asks to: (1) Analyze their Cursor IDE usage or prompting habits, (2) Get insights from their Cursor state database (state.vscdb), (3) Improve how they use Cursor AI features (chat, composer, inline edit, tab completion), (4) Review their Cursor conversation history, (5) Get a prompting score or usage report, (6) Optimize their AI-assisted coding workflow in Cursor. Triggers on keywords: cursor insights, cursor analysis, cursor usage, cursor prompting, improve cursor, cursor tips, cursor habits, state.vscdb."
---

# Cursor Insights

Analyze the Cursor IDE state database to extract usage patterns, evaluate prompting quality, and generate actionable recommendations for more effective AI-assisted coding.

## Workflow

### Step 1: Ensure Prerequisites

1. Verify the Cursor state database exists:
   ```
   ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
   ```
   If missing, inform the user that Cursor must be installed and run at least once.

2. Ensure `cursor-agent` CLI is available. Run `scripts/ensure_cursor_cli.sh` to check and install if needed:
   ```bash
   bash scripts/ensure_cursor_cli.sh
   ```
   If installation fails, instruct the user to install manually: `curl https://cursor.com/install -fsS | bash`

### Step 2: Extract Data

Run the extraction script to pull data from the SQLite database:

```bash
python3 scripts/extract_cursor_db.py --output json
```

**Available modes:**
- `--schema-only` — Print just the database schema (use first for discovery)
- `--keys-only` — List all stored keys (useful for finding relevant data)
- `--dump-key "key.name"` — Extract a specific key's value
- `--output json` — Full analysis as JSON (default: text)
- `--days N` — Limit analysis window (default: 60 days)

**Recommended sequence:**
1. Run `--schema-only` first to understand the database structure
2. Run `--keys-only` to discover what data is available
3. Run full extraction with `--output json` for complete analysis
4. Use `--dump-key` to deep-dive into specific conversation entries

### Step 3: Analyze and Score

Using the extracted data, evaluate across these dimensions:

**Prompting Quality (score 1-10):**
- Context richness: Do prompts reference files, errors, and constraints?
- Specificity: Are goals clear and actionable in a single message?
- Efficiency: How many turns does it take to get the desired result?
- Feature usage: Are @-mentions, file refs, and context features used?

Refer to `references/prompting-guide.md` for the scoring rubric, anti-pattern catalog, and best practices to compare against.

**Feature Utilization:**
- Which Cursor features are used (chat, composer, inline edit, tab, terminal)?
- Which are underused relative to the user's workflow?
- Accept/reject ratio for AI suggestions

**Usage Patterns:**
- Session frequency and duration
- Languages and file types
- Multi-turn vs single-turn conversation ratio

### Step 4: Generate Report

Format the final report using the structure in `references/analysis-template.md`. Use the `generated_date`, `analysis_start_date`, and `analysis_end_date` fields from the script output for all dates — do NOT infer or estimate dates. The report must include:

1. **Executive Summary** — 2-3 sentence overview
2. **Prompt Statistics** — Quantitative metrics table
3. **Prompting Score** — 1-10 with justification
4. **Top 5 Improvements** — Each with a before/after example drawn from actual user prompts
5. **Anti-Patterns Found** — Matched against the catalog in `references/prompting-guide.md`
6. **Underused Features** — With concrete suggestions for adoption
7. **Actionable Recommendations** — Grouped by immediate, medium-term, and advanced

### Step 5: Optionally Delegate to cursor-agent

If the user wants deeper or real-time analysis, invoke `cursor-agent` with a focused prompt:

```bash
cursor-agent --prompt "Analyze the Cursor state database at ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb. [specific analysis request]"
```

## Quick Commands

| User Request | Action |
|---|---|
| "Analyze my Cursor usage" | Run full workflow (Steps 1-4) |
| "Score my prompting" | Run Steps 1-3, focus on prompting score |
| "What Cursor features am I not using?" | Run Steps 1-2, focus on feature utilization |
| "Show me my worst prompts" | Extract conversations, identify anti-patterns |
| "How can I improve my Cursor prompting?" | Run full workflow + reference prompting-guide.md |
| "Install cursor CLI" | Run Step 1 only |

## Resources

### scripts/
- **`extract_cursor_db.py`** — Python script to extract and analyze data from state.vscdb. Reads the SQLite database in read-only mode, extracts conversations, feature usage, settings, and generates statistics. Supports multiple output modes.
- **`ensure_cursor_cli.sh`** — Checks if `cursor-agent` CLI is installed; installs via `curl https://cursor.com/install -fsS | bash` if missing.

### references/
- **`prompting-guide.md`** — Comprehensive guide to Cursor prompting best practices, quality scoring rubric (tiers 1-4), common anti-patterns with before/after examples, feature usage tips, and context maximization strategies. Read this when evaluating prompt quality or generating improvement recommendations.
- **`analysis-template.md`** — Report template with all sections and placeholder fields. Use when formatting the final analysis output.
