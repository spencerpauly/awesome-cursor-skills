---
name: fixing-broken-links
description: Crawl all links in a file or project, test each for a valid HTTP response, report broken ones, and fix or remove them.
user-invocable: true
---

# Fixing Broken Links

Scan a file (or set of files) for URLs, test every link, and fix any that are broken.

## Workflow

### 1. Extract All Links

Read the target file(s) and collect every URL:
- Markdown links: `[text](url)`
- Bare URLs: `https://...`
- HTML `href` and `src` attributes
- Reference-style link definitions: `[id]: url`
- Local relative paths: `./path/to/file`, `resources/foo/SKILL.md`

### 2. Test Each Link

**For external URLs:**
- Use `curl -sL -o /dev/null -w "%{http_code}" --max-time 10 "<url>"` to get the HTTP status code
- Batch independent checks for speed (run multiple curl commands in parallel or in quick succession)
- Classify results:
  - `200`–`299` → OK
  - `301`/`302` → OK but note the redirect target
  - `403` → Might be valid (some sites block curl); try with a browser user-agent header
  - `404` → Broken
  - `429` → Rate limited; retry once after a short pause
  - `000` or timeout → Retry once; if still failing, mark as unreachable

**For local file paths:**
- Check if the file exists on disk with `[ -f "path" ]`
- If it's a relative path, resolve it from the file's directory

### 3. Fix Broken Links

For each broken link:
1. Search the web for the correct/current URL (the resource may have moved)
2. If found, replace the old URL with the new one
3. If the resource no longer exists, note it and either:
   - Remove the link and leave the text
   - Comment it out with a note
   - Replace with an archived version (web.archive.org)

### 4. Report

Produce a summary table:

```
| URL | Status | Action |
|-----|--------|--------|
| https://example.com/page | 200 | OK |
| https://old.example.com/moved | 404 → 301 | Updated to https://new.example.com/page |
| ./docs/missing.md | MISSING | Removed link |
```

## Tips

- For large files with many links, batch curl calls to avoid slowdowns
- Some sites (GitHub, npm) rate-limit aggressively — space out requests
- Always re-read the file after making changes to confirm replacements didn't break formatting
- For Markdown files, verify link syntax is preserved: `[text](url)` not `[text]( url )` (no extra spaces)
