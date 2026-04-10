---
name: converting-css-modules-to-tailwind
description: Migrate CSS Modules (.module.css/.module.scss) to Tailwind utility classes. Handles styles object removal, className interpolation, composition, and global overrides.
user-invocable: true
---

# Converting CSS Modules to Tailwind

Migrate a component from CSS Modules (`.module.css` / `.module.scss`) to Tailwind utility classes.

## Workflow

### 1. Inventory the Module

Read the `.module.css` file and the component that imports it. Map every `styles.xxx` reference to the CSS rule it resolves to.

```tsx
// Before
import styles from './Card.module.css';
<div className={styles.card}>
  <h2 className={styles.title}>{title}</h2>
  <p className={styles.body}>{children}</p>
</div>
```

```css
/* Card.module.css */
.card { display: flex; flex-direction: column; gap: 16px; padding: 24px; border-radius: 12px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.title { font-size: 20px; font-weight: 600; color: #111827; }
.body { font-size: 14px; color: #6b7280; line-height: 1.6; }
```

### 2. Convert Each Class

Replace `styles.xxx` with equivalent Tailwind utilities:

```tsx
// After
<div className="flex flex-col gap-4 p-6 rounded-xl bg-white shadow-sm">
  <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
  <p className="text-sm text-gray-500 leading-relaxed">{children}</p>
</div>
```

### 3. Handle CSS Modules Patterns

**`composes` keyword:**
```css
.base { padding: 8px 16px; border-radius: 4px; }
.primary { composes: base; background: blue; color: white; }
```
→ Flatten into a single set of utilities. If reuse is needed, extract a component, not a class.

**Conditional classNames with `clsx`/`classnames`:**
```tsx
// Before
className={clsx(styles.button, isActive && styles.active)}
// After
className={clsx("px-4 py-2 rounded", isActive && "bg-blue-600 text-white")}
```

**Dynamic class selection:**
```tsx
// Before
className={styles[variant]}
// After — use a lookup object
const variantClasses = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
  danger: "bg-red-600 text-white hover:bg-red-700",
};
className={variantClasses[variant]}
```

**CSS Modules global overrides:**
```css
:global(.some-library-class) { ... }
```
→ Move to `globals.css` with `@layer components { }` or use Tailwind's `@apply` in the global stylesheet.

**SCSS features (nesting, variables, mixins):**
- Nested selectors → flatten into utility classes on each element
- SCSS `$variables` → map to `tailwind.config.ts` theme values
- Mixins → replace with utility composition or extract components

### 4. Clean Up

1. Remove the `import styles from './Xxx.module.css'` line
2. Delete the `.module.css` / `.module.scss` file
3. If the component had a co-located `index.ts` barrel that re-exported styles, update it
4. Search the codebase for any other imports of the deleted module
5. Run the app and verify visually — check for regressions

## Rules

- Convert one component at a time — don't batch entire directories
- Keep conditional logic in `clsx()` or template literals, not in CSS
- If a module has pseudo-element styles (`:before`, `:after` with `content`), those need `before:` / `after:` prefixes plus `content-['...']` in Tailwind
- For `:nth-child`, `:first-of-type`, etc. — check if Tailwind has a matching variant, otherwise keep a minimal CSS rule
- Don't create `@apply` classes to replicate what the module did — the goal is to eliminate the indirection
