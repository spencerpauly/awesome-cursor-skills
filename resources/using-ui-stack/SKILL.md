---
name: using-ui-stack
description: Enforce a configuration-driven design system when generating UI. Ensures consistent spacing, colors, typography, dark mode, interactions, and accessibility across all AI-generated components.
user-invocable: true
---

# Using UI Stack

Apply a structured design system to every UI component you generate. This prevents inconsistent padding, mismatched colors, and forgotten hover states.

## Design System Principles

Follow these rules for **every** component you build:

### Spacing — 8px Grid

Use multiples of 8 for all spacing (padding, margin, gap):
- `4px` — tight internal padding only
- `8px` — inline gaps, icon spacing
- `16px` — standard padding, card gaps
- `24px` — section padding
- `32px` — large section gaps
- `48px / 64px` — page-level spacing

### Color — 60-30-10 Rule

- **60%** neutral/background
- **30%** primary brand color
- **10%** accent for CTAs and highlights
- Semantic colors: success (green), warning (amber), error (red), info (blue)
- Never use pure black (`#000`) for dark mode — use `slate-950` or similar

### Typography — 1.25 Ratio Scale

```
text-xs:   12px / 16px
text-sm:   14px / 20px
text-base: 16px / 24px
text-lg:   18px / 28px
text-xl:   20px / 28px
text-2xl:  24px / 32px
text-3xl:  30px / 36px
text-4xl:  36px / 40px
```

- Headings: `font-semibold` or `font-bold`
- Body: `font-normal`, line-height 1.5–1.75
- Mono: use for code, IDs, numeric data

### Dark Mode

- Provide complete light/dark mappings for every color token
- Background: `white` → `slate-950`, not `black`
- Text: `slate-900` → `slate-100`
- Borders: `slate-200` → `slate-800`

### 5-State Interactions

Every interactive element must have:
1. **Default** — base appearance
2. **Hover** — subtle color shift or shadow
3. **Active/Pressed** — slightly darker or scaled down
4. **Focus** — visible ring (`ring-2 ring-offset-2`)
5. **Disabled** — reduced opacity, `cursor-not-allowed`

### Accessibility

- Contrast ratio ≥ 4.5:1 for text, ≥ 3:1 for large text
- Touch targets ≥ 44×44px
- Semantic HTML (`button` not `div`, `nav`, `main`, etc.)
- Keyboard navigable — all interactions reachable via Tab/Enter/Escape
- Respect `prefers-reduced-motion` for animations

### Animations

- Duration: 150–300ms for micro-interactions
- Easing: `ease-out` for entrances, `ease-in` for exits
- Wrap motion in `motion-safe:` or check `prefers-reduced-motion`

### Overlay Z-Index Scale

```
dropdown:  z-10
sticky:    z-20
overlay:   z-30
modal:     z-40
toast:     z-50
tooltip:   z-60
```

## Workflow

1. Before generating UI, check if the project has a `ui-stack` config or design tokens
2. If not, apply the defaults above
3. For every component, verify spacing is on the 8px grid, colors follow 60-30-10, and all 5 interaction states exist
4. Test dark mode by toggling the class/attribute and confirming all tokens map correctly

## References

- [ui-stack.dev](https://ui-stack.dev) — interactive configurator and full docs
- [GitHub: rashoodkhan/ui-stack](https://github.com/rashoodkhan/ui-stack) — source repo
