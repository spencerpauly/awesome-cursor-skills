---
name: converting-css-to-tailwind
description: Convert plain CSS stylesheets to Tailwind CSS utility classes. Handles selectors, media queries, pseudo-classes, custom properties, and animations.
user-invocable: true
---

# Converting CSS to Tailwind

Migrate plain CSS files to Tailwind utility classes applied directly in markup.

## Workflow

1. **Read the CSS file** and inventory every rule
2. **Find the corresponding markup** (HTML, JSX, TSX, Vue, Svelte) that references each selector
3. **Convert each rule** using the mapping below
4. **Delete the CSS rule** once all its properties are expressed as utilities
5. **Remove the CSS file** (or import) once it's empty
6. **Verify** the page looks identical — check for visual regressions

## Conversion Reference

### Layout & Box Model

| CSS | Tailwind |
|-----|----------|
| `display: flex` | `flex` |
| `display: grid` | `grid` |
| `display: none` | `hidden` |
| `position: relative` | `relative` |
| `position: absolute` | `absolute` |
| `justify-content: center` | `justify-center` |
| `align-items: center` | `items-center` |
| `gap: 16px` | `gap-4` |
| `width: 100%` | `w-full` |
| `max-width: 768px` | `max-w-3xl` |
| `margin: 0 auto` | `mx-auto` |
| `padding: 16px` | `p-4` |
| `overflow: hidden` | `overflow-hidden` |

### Typography

| CSS | Tailwind |
|-----|----------|
| `font-size: 14px` | `text-sm` |
| `font-weight: 700` | `font-bold` |
| `line-height: 1.5` | `leading-normal` |
| `text-align: center` | `text-center` |
| `text-transform: uppercase` | `uppercase` |
| `color: #333` | `text-[#333]` or a theme color |
| `letter-spacing: 0.05em` | `tracking-wide` |

### Backgrounds & Borders

| CSS | Tailwind |
|-----|----------|
| `background-color: #f5f5f5` | `bg-[#f5f5f5]` or `bg-neutral-100` |
| `border: 1px solid #e5e7eb` | `border border-gray-200` |
| `border-radius: 8px` | `rounded-lg` |
| `box-shadow: 0 1px 3px ...` | `shadow-sm` |

### Responsive — Media Queries

```css
@media (min-width: 768px) { .card { flex-direction: row; } }
```
→ `<div class="flex-col md:flex-row">`

Map breakpoints: `sm:` (640), `md:` (768), `lg:` (1024), `xl:` (1280), `2xl:` (1536)

### Pseudo-classes & States

```css
.btn:hover { background-color: #1d4ed8; }
```
→ `<button class="hover:bg-blue-700">`

Prefixes: `hover:`, `focus:`, `active:`, `disabled:`, `first:`, `last:`, `odd:`, `even:`, `group-hover:`, `peer-checked:`

### Animations & Transitions

```css
transition: all 0.2s ease-in-out;
```
→ `transition-all duration-200 ease-in-out`

```css
@keyframes spin { ... }
animation: spin 1s linear infinite;
```
→ `animate-spin` (built-in) or define in `tailwind.config`

### Custom Properties / Arbitrary Values

For anything without a direct utility, use arbitrary values:
- `w-[calc(100%-2rem)]`
- `grid-cols-[200px_1fr_1fr]`
- `text-[clamp(1rem,2vw,1.5rem)]`

## Handling Remaining CSS

Some things can't be expressed purely as utilities:

- **Complex selectors** (`.parent > .child + .sibling`) — restructure the markup or use `@apply` as a last resort
- **`@font-face`** — keep in a global CSS file or `globals.css`
- **Complex `@keyframes`** — define in `tailwind.config.ts` under `theme.extend.keyframes`
- **CSS variables** — migrate to Tailwind theme values in `tailwind.config.ts`

## Rules

- Prefer semantic Tailwind classes (`bg-primary`) over arbitrary hex values when a theme exists
- Don't use `@apply` to recreate the same CSS you're migrating away from — that defeats the purpose
- Group related utilities logically: layout → spacing → typography → colors → effects
- If a component has 10+ utilities, consider extracting a reusable component rather than a CSS class
