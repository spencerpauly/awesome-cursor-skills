---
name: verifying-markdown-formatting
description: Verify that a Markdown file has correct formatting — headings, lists, links, code blocks, spacing, and consistent style.
user-invocable: true
---

# Verifying Markdown Formatting

Check a Markdown file for formatting issues and fix them.

## What to Check

### Structure

- [ ] Exactly one `# H1` heading at the top of the file
- [ ] Headings increment by one level (no jumping from `##` to `####`)
- [ ] Blank line before and after every heading
- [ ] Blank line before and after every code block, list, and blockquote
- [ ] File ends with a single trailing newline

### Lists

- [ ] Consistent marker style within each list (`-` not mixed with `*` or `+`)
- [ ] Nested items indented with 2 or 4 spaces (consistent throughout)
- [ ] Blank line before the first item in a top-level list
- [ ] No blank lines between items in a tight list (or all items separated — pick one)

### Links & Images

- [ ] All links have non-empty display text: `[text](url)` not `[](url)`
- [ ] No bare URLs outside of code blocks — wrap in `<url>` or `[text](url)`
- [ ] Reference-style links have matching definitions
- [ ] Image alt text is present: `![alt](src)` not `![](src)`

### Code Blocks

- [ ] Fenced code blocks use triple backticks, not tildes
- [ ] Language identifier is present on every fenced block (` ```python `, ` ```bash `, etc.)
- [ ] Inline code uses single backticks for short references
- [ ] No indented code blocks (use fenced instead for clarity)

### Formatting

- [ ] Bold uses `**text**` not `__text__`
- [ ] Italic uses `*text*` not `_text_`
- [ ] No trailing whitespace on any line
- [ ] Lines under 120 characters where practical (prose, not tables)
- [ ] Consistent use of ATX-style headings (`# Heading`, not underline style)

### Tables

- [ ] Header row has separator row with `---` in each column
- [ ] Cell content is trimmed (no excessive padding)
- [ ] Column alignment markers (`:---`, `:---:`, `---:`) used consistently if present

### Horizontal Rules

- [ ] Use `---` on its own line with blank lines above and below
- [ ] Consistent style (don't mix `---`, `***`, `___`)

## Workflow

1. Read the target Markdown file
2. Walk through each check above
3. Fix any issues found using exact string replacements
4. Re-read the file to confirm all fixes applied cleanly
5. Report what was fixed and what was already correct

## Notes

- This skill is formatting-only — it does not validate content accuracy, broken links, or spelling
- Preserve the author's intended structure; don't reorganize sections
- When fixing list markers, match whatever style the file already uses most
