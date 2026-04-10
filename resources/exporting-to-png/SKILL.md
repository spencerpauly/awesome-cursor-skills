---
name: exporting-to-png
description: Export code, terminal output, diagrams, or UI components to PNG images using headless browser rendering or CLI tools.
user-invocable: true
---

# Exporting to PNG

Convert code snippets, Markdown content, terminal output, diagrams, or rendered UI components into PNG image files.

## Methods

### 1. HTML → PNG via Headless Browser

The most flexible approach. Render any content as HTML and screenshot it.

```bash
# Using Playwright (if available)
npx playwright screenshot --full-page "file:///path/to/content.html" output.png

# Using Puppeteer one-liner
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(\`<html>...</html>\`);
  await page.screenshot({ path: 'output.png', fullPage: true });
  await browser.close();
})();
"
```

**Steps:**
1. Generate an HTML file with the content styled appropriately (syntax highlighting, padding, fonts)
2. Use a headless browser to render and capture
3. Crop if needed using an image tool

### 2. Code → PNG with Carbon or Silicon

For styled code screenshots:

```bash
# silicon (Rust CLI, fast)
silicon --language python --output code.png source.py
silicon --from-clipboard --output code.png

# Or generate a Carbon URL for browser capture
# https://carbon.now.sh/?l=python&code=<url-encoded-code>
```

### 3. Mermaid Diagrams → PNG

```bash
# Using mermaid-cli
npx @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.png -b transparent

# Or with Docker
docker run --rm -v "$(pwd)":/data minlag/mermaid-cli mmdc -i /data/diagram.mmd -o /data/diagram.png
```

### 4. SVG → PNG

```bash
# Using sharp (Node.js)
node -e "
const sharp = require('sharp');
sharp('input.svg').png().toFile('output.png');
"

# Using Inkscape CLI
inkscape input.svg --export-type=png --export-filename=output.png

# Using ImageMagick
convert input.svg output.png
```

### 5. Terminal Output → PNG

```bash
# Using termshot (if installed)
termshot -- ls -la

# Manual approach: capture output, wrap in HTML with monospace font, screenshot
```

## Workflow

1. Determine the content type (code, diagram, HTML, terminal, SVG)
2. Check which tools are available in the environment (`which silicon`, `npx --help`, etc.)
3. Choose the best method and generate the PNG
4. Verify the output exists and is non-empty: `file output.png && ls -la output.png`
5. Report the file path and dimensions

## Tips

- For code screenshots, use a dark theme with generous padding (32px+) for a polished look
- Set `deviceScaleFactor: 2` in Playwright/Puppeteer for retina-quality output
- For transparent backgrounds, use `--background transparent` or `omitBackground: true`
- If no specialized tool is installed, fall back to the HTML + headless browser method — it works for everything
