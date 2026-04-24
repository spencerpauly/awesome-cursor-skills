---
name: generating-images
description: >-
  Generate or edit images using the OpenAI Image API (gpt-image-2). Use when
  the user asks to generate, create, draw, render, illustrate, mock up, or edit
  an image, icon, logo, mockup, illustration, OG image, blog hero, marketing
  asset, or similar visual. Also use when the user supplies a reference image
  and asks to modify, restyle, or remix it. Triggers on: "generate an image",
  "create an image", "make a picture of", "edit this image", "restyle this",
  "make a mockup of", "draw a", "render a", "illustration of".
user-invocable: true
---

# Generating Images (OpenAI gpt-image-2)

Use this skill any time the user asks to generate or edit an image. It wraps
OpenAI's `gpt-image-2` model via a Python script, supports both text-only
prompts and one-or-more reference images, and writes the resulting PNG/JPEG/WebP
to disk.

## Hard rules (do not violate)

1. **Always use `gpt-image-2`.** Never fall back to `gpt-image-1`, `dall-e-3`,
   or any other model. The script has no `--model` flag for this reason.
2. **Fail fast on any error.** Do not retry, do not swap models, do not patch
   around missing credentials, do not silently degrade quality. If the script
   exits non-zero, surface the error to the user verbatim and stop.
3. **Do not "fix" a missing `OPENAI_API_KEY`** by reading from `.env` files,
   1Password, etc. unless the user explicitly tells you to. If the env var is
   missing, ask the user how they want to provide it (or to `export` it) and
   then stop.

## When to use

- User asks for a generated image: icon, logo, illustration, mockup, OG image,
  blog hero, marketing asset, concept art, diagram-style image, etc.
- User provides one or more images and asks to edit, restyle, combine, or use
  them as references.
- User asks to remove/replace part of an image (use `--mask`).

Do **not** use this skill for:
- Charts/plots/data viz (generate via code instead).
- Sourcing existing photos (use a stock photo skill if available).
- Screenshots of the user's app (use a screenshot skill if available).

## Prerequisites

### 1. OpenAI API key

You need an `OPENAI_API_KEY` exported in your environment. Get one at
[platform.openai.com/api-keys](https://platform.openai.com/api-keys).

The skill ships with a `.env.example` next to this `SKILL.md`. Copy it and
fill in your key:

```bash
cp .env.example .env
# then edit .env and put your real key in
```

Then export it before running the script:

```bash
set -a && source .env && set +a
```

Or just export it directly in your shell:

```bash
export OPENAI_API_KEY="sk-..."
```

If `OPENAI_API_KEY` is not set, the script exits with code 2 immediately.
**Do not** try to read it from anywhere else without the user's explicit
permission.

### 2. Org verification

Your OpenAI org must be verified for `gpt-image-2` at
[platform.openai.com/settings/organization/general](https://platform.openai.com/settings/organization/general).
If you see a 403 mentioning "organization must be verified", surface it and
stop — do not switch models.

### 3. Python dependency

```bash
pip install --upgrade openai
```

## Script location

The Python script lives next to this `SKILL.md` at `scripts/generate_image.py`.
When this skill is installed at `~/.cursor/skills/generating-images/`, the
script will be at `~/.cursor/skills/generating-images/scripts/generate_image.py`.

It prints the absolute path(s) of the written image(s) to stdout. Errors go
to stderr with a non-zero exit code, and the script exits immediately on the
first error.

## How to invoke

Always run via the Shell tool. Pick a sensible output path inside the user's
current workspace (e.g. `./public/generated/<slug>.png` for web projects, or
`./<slug>.png` otherwise).

### 1. Text-to-image

```bash
python3 ~/.cursor/skills/generating-images/scripts/generate_image.py \
  --prompt "Minimal flat-vector app icon for a note-taking app, indigo gradient, rounded square, soft shadow" \
  --size 1024x1024 \
  --quality high \
  --out ./icon.png
```

### 2. Image-to-image (one reference)

```bash
python3 ~/.cursor/skills/generating-images/scripts/generate_image.py \
  --prompt "Restyle this photo as a watercolor painting with warm tones" \
  --image ./photo.jpg \
  --out ./photo-watercolor.png
```

### 3. Multiple reference images

```bash
python3 ~/.cursor/skills/generating-images/scripts/generate_image.py \
  --prompt "Photorealistic flat-lay product shot combining all of these items on a white background" \
  --image ./a.png --image ./b.png --image ./c.png \
  --out ./flatlay.png
```

### 4. Masked edit (inpainting)

The mask must be the same size and format as the first input image, with an
alpha channel marking the editable region.

```bash
python3 ~/.cursor/skills/generating-images/scripts/generate_image.py \
  --prompt "Replace the sky with a vivid sunset" \
  --image ./scene.png --mask ./sky-mask.png \
  --out ./scene-sunset.png
```

### 5. Batch / parallel mode (many distinct images at once)

When you need to generate **multiple different images** in one go (e.g. a set
of blog heroes, several icon variations with different prompts, OG images for
many pages), use `--batch` instead of running the script N times. It runs all
jobs in parallel from a single Python process — much faster than serial calls
and avoids repeated SDK startup cost.

Write a JSON file describing every job, then call the script once:

```bash
cat > /tmp/img-jobs.json <<'EOF'
[
  {
    "prompt": "Minimal flat-vector app icon for a note-taking app, indigo gradient, rounded square",
    "out": "./public/icons/notes.png",
    "size": "1024x1024",
    "quality": "high"
  },
  {
    "prompt": "Photoreal blog hero: a cozy library with warm afternoon light, 5:3 ratio",
    "out": "./public/static/blog/library.png",
    "size": "1600x960",
    "quality": "medium"
  },
  {
    "prompt": "Restyle this product photo as a watercolor painting with warm tones",
    "image": ["./public/products/mug.jpg"],
    "out": "./public/products/mug-watercolor.png"
  }
]
EOF

python3 ~/.cursor/skills/generating-images/scripts/generate_image.py \
  --batch /tmp/img-jobs.json --concurrency 5
```

Each job object accepts the same fields as the CLI flags: `prompt` (required),
`out`, `size`, `quality`, `format`, `n`, `image` (string or array of strings),
`mask`. Defaults match the single-shot CLI.

Behavior:

- All jobs run concurrently up to `--concurrency` (default 4). A reasonable
  range is 3–8; OpenAI rate-limits per org so don't go too wild.
- Each successfully written image's absolute path is printed to stdout as soon
  as that job finishes, one per line.
- If any job fails, its error is printed to stderr (`ERROR: job <i> failed: ...`)
  and the script exits with code 1 **after** the remaining jobs finish. Other
  jobs are not cancelled — partial output is fine and you can retry only the
  failed ones.
- `--batch` is mutually exclusive with `--prompt` / `--image` / `--mask`.

**When to prefer `--batch` over parallel Shell calls:** any time you're
generating ≥2 distinct images in the same turn. Don't fire multiple parallel
Shell invocations of this script — use one batch call instead.

**Don't confuse with `--n`.** `--n` produces multiple variations of the *same*
prompt in a single API call (cheaper, but all the same idea). `--batch` runs
*different* prompts in parallel. They can be combined: a batch job can set
`"n": 4` to get 4 variations of that one prompt.

## Flags reference

| Flag | Default | Notes |
|------|---------|-------|
| `--prompt` | required* | Required unless `--batch` is used. Always include, even when editing. |
| `--image` | none | Pass multiple times for multiple references. Triggers `images.edit`. |
| `--mask` | none | Optional inpainting mask (PNG with alpha). |
| `--out` | `./image.png` | Output path; index suffix added when `--n > 1`. |
| `--size` | `auto` | `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `3840x2160`, etc. Edges must be multiples of 16, max 3840px, ratio ≤ 3:1. |
| `--quality` | `auto` | `low` (fast drafts), `medium`, `high` (final assets). |
| `--format` | `png` | `png`, `jpeg`, `webp`. |
| `--n` | `1` | Variations of the SAME prompt in one call. |
| `--batch` | none | Path to JSON array of job objects; runs them in parallel. |
| `--concurrency` | `4` | Max parallel workers in `--batch` mode. |

There is intentionally **no `--model` flag**. The model is hardcoded to
`gpt-image-2`.

## Sizing guidance

- App icons / square thumbnails → `1024x1024`
- Landing-page heroes / OG images → `1536x1024`
- Blog hero (5:3) → `1600x960` (both edges multiples of 16, ratio = 5:3)
- Mobile / portrait illustrations → `1024x1536`
- Marketing posters / 4K assets → `3840x2160`

## Quality guidance

- `low` for quick exploration / drafts (cheapest, fastest).
- `medium` is a good default.
- `high` only for final, ship-ready assets — significantly more expensive
  and can take up to ~2 minutes.

If the user just says "generate an image" with no signal of finality, default
to `--quality medium`.

## Prompt-writing tips

For best results, include in the prompt:
- Subject (what is in the image)
- Style (flat vector, watercolor, photoreal, isometric, line drawing, 3D render…)
- Composition / camera (close-up, top-down, wide shot)
- Color palette / mood
- Background (white, gradient, scene — note: `gpt-image-2` does not support
  transparent backgrounds)
- Any text that must appear, in quotes (`gpt-image-2` renders text well)

If the user gives a vague prompt, expand it with sensible defaults rather than
asking back, unless the request is genuinely ambiguous.

## After generating

1. Print the output path back to the user.
2. Do **not** embed the image in markdown — Cursor displays generated files
   automatically when they are written into the workspace.
3. If the result is meant for a website/app, consider also running it through
   an optimizer (e.g. `pngquant`, `cwebp`) when file size matters.

## Gather context BEFORE generating

Unless the user has spelled out exactly what they want (subject, style, palette,
size, destination), do a quick context-gathering pass first. The goal is for
the generated image to feel like it belongs where it's going, not like a
random asset dropped into the project. Skipping this step is the #1 way this
skill produces off-brand results.

Things to look at, in roughly this order:

1. **Sibling images at the destination.** If the image will live in
   `public/static/blog/`, `public/static/marketing/`, `assets/`, etc., open
   one or two existing images in that folder with the Read tool. Match their:
   - Illustration style (3D cartoon, flat vector, photoreal, line art, isometric…)
   - Color palette and lighting
   - Subject conventions (e.g. "always features the product mascot", "always a
     metaphor, never literal screenshots", etc.)
   - Aspect ratio and resolution

2. **The surface that will display it.** Read the relevant file:
   - Blog post → read the MDX/Markdown (title, tags, opening paragraphs, key metaphors).
   - Landing page section → read the component, headline, and surrounding copy.
   - README → read the top of the README.
   - Component → read the component to understand what it represents.

   Pull the image's *meaning* from the actual content, not just the filename.

3. **Brand / design tokens.** If the project has a clearly defined palette,
   logo, or mascot, mirror them. Quick places to check:
   - `tailwind.config.*` for brand colors
   - `globals.css` / theme files for CSS variables
   - `public/` for logos / mascot assets
   - Any existing OG images or marketing assets

4. **Aspect ratio / size.** Pick `--size` based on the surface:
   blog hero, OG image, square avatar, mobile portrait, etc. Match what's
   already there.

Then write the prompt incorporating what you learned: subject pulled from the
content, style + palette pulled from sibling assets and brand tokens,
composition matched to the surface.

If the user *did* give explicit direction (style, colors, exact subject),
honor it and skip context-gathering. If they gave partial direction, gather
context for the parts they left open.

Don't ask the user clarifying questions for things you can reasonably infer
from the codebase — infer first, ask only when something is genuinely
ambiguous (e.g. two equally valid styles already exist in the project).

## Place it AND wire it up — don't just dump a file

When the user asks for an image for a specific surface (a blog post, a landing
page, an OG card, a README, a component, etc.), you are responsible for the
whole job, not just the PNG. Always do these in order:

1. **Pick the correct on-disk location** for that surface. Look at what already
   exists and match it. Examples:
   - Blog hero → wherever existing blog images live (e.g.
     `apps/<app>/public/static/blog/<slug>.png`).
   - Landing page asset → wherever other landing assets live (e.g.
     `apps/<app>/public/static/marketing/...`).
   - README / docs image → `docs/images/`, `assets/`, or next to the doc.
   - Component-specific asset → next to the component or in its
     `public/`/`assets/` folder.

   Use the file's slug, component name, or section name for the filename. Don't
   invent a new convention if one already exists.

2. **Wire the image up** so it actually shows where the user wanted it. This is
   not optional. Examples:
   - Blog post MDX → update the `image:` (or equivalent) frontmatter field to
     point at the new path. Replace any placeholder Unsplash/stock URL.
   - Landing page section → import or reference the new asset in the relevant
     component/JSX.
   - OG image → update the `<meta property="og:image">` / metadata config.
   - README → add the appropriate Markdown image tag.

3. **Match existing conventions** for paths (relative vs `/static/...` vs
   `@/assets/...`), file format (png/webp/jpg), and any wrapper components
   (`next/image`, custom `<Image>`, etc.).

4. **Don't ask first.** If the user asked for an image for a known surface, do
   the placement + wiring automatically and tell them what you changed at the
   end. Only ask when the destination is genuinely ambiguous.

## Errors — surface, don't hide

If any of the following happen, **stop immediately** and report the error to
the user. Do not retry, do not change the model, do not change the prompt.

- `OPENAI_API_KEY is not set` → ask the user how to provide it.
- `openai package not installed` → tell the user to run `pip install --upgrade openai`.
- 403 "organization must be verified" → tell the user to verify at
  [platform.openai.com/settings/organization/general](https://platform.openai.com/settings/organization/general).
  Do not switch models.
- 400 size error → report it; let the user pick a valid size.
- 400 about transparent background → report it; `gpt-image-2` doesn't
  support transparency.
- Any other API error → report verbatim and stop.
