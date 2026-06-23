---
name: create-component-from-figma
description: Creates Vue 3 components from Figma designs using @jumpcloud/circuit (Circuit design system), Tailwind, and PrimeVue. Handles folder segregation and optional Vitest tests. Use when given a Figma URL/design, building Vue components from designs, or implementing UI from Figma.
---

# Vue Figma Component

Create Vue 3 components from Figma designs using the Circuit design system
(`@jumpcloud/circuit`), Tailwind CSS, and PrimeVue. Act as a **Senior Frontend Engineer specialized in our Design System**. Your task is to transform Figma designs into functional code that is **100% compliant** with our shared UI library and custom Tailwind theme.

## Core Objective

Transform Figma designs (screenshots, specs, or MCP-fetched nodes) into functional Vue 3 code that:

- Uses **only** components and tokens from our shared design system
- Works whether the design system is **local** (e.g. `jumpcloud-common-ui` in the workspace) or **imported via node_modules** (e.g. `@jumpcloud/circuit` in Admin Portal)
- Avoids standard Tailwind utility colors (e.g. `bg-blue-500`) in favor of **Custom Theme Tokens** (e.g. `bg-button-primary-base`, `text-neutral-base`)
- Maps design elements to **existing library components** before writing any custom markup

## When to Apply

- User provides Figma URL or design reference
- User asks to create/build Vue components from a design
- User mentions Circuit, jumpcloud-common-ui, or design-to-code
- User wants to implement UI matching a Figma design

## Prerequisites

- **Figma MCP**: Ensure frame is selected in Figma; use MCP to fetch node structure
- **Current workspace**: Vue 3 app with `@jumpcloud/circuit` and PrimeVue (skill runs in-context)
- **Dependencies**: `@jumpcloud/circuit`, `primevue`, `tailwindcss`, `vue` ^3.5,
  `@jumpcloud/icons`, `@heroicons/vue`

## Workflow

### Step 0: Dependency Discovery

**Before generating any code**, locate the design system and theme configuration:

1. **Check `package.json`** (app or workspace root) for the design system package:
   - **Admin Portal / npm**: `"@jumpcloud/circuit": "^0.0.xx"` → design system is in `node_modules/@jumpcloud/circuit`
   - **Monorepo / local**: `"@jumpcloud/circuit": "workspace:*"` or path reference → design system may be in a sibling package (e.g. `jumpcloud-common-ui/packages/circuit`)

2. **Resolve where to read from**:
   - **If in node_modules**: Use **exported** entrypoints only. Component signatures → `node_modules/@jumpcloud/circuit/dist/components.js` (or `.d.ts`). Tailwind theme → `@jumpcloud/circuit/tailwind` (consumed via `@config` or preset in app CSS/build).
   - **If local package in workspace**: You may reference source for tokens/docs: `packages/circuit/src/tailwind/`, `packages/circuit/docs/`, and component exports from the package’s `dist` or main entry.

3. **Confirm Tailwind theme usage**: The app must use Circuit’s theme so that **Custom Theme Tokens** (e.g. `bg-button-primary-base`, `text-heading-3`) are available. That is typically done via:
   - `@config '@jumpcloud/circuit/tailwind';` in the app’s root CSS, or
   - A Tailwind preset pointing to `@jumpcloud/circuit/tailwind`.

Do not assume raw Tailwind utilities (e.g. `bg-blue-500`) are valid; prefer tokens from the shared config. See [reference.md](references/reference.md) for theme keys and file locations.

### Step 1: Verify App Setup

Before generating components, verify the app is configured correctly:

1. **Check `index.css`** (or root stylesheet) for Circuit Tailwind config:

   ```css
   @config '@jumpcloud/circuit/tailwind';
   ```

   If missing, add it. See [reference.md](references/reference.md) for complete setup.

2. **Check entry file** (`main.ts`, `initialize.ts`, etc.) for PrimeVue Circuit preset:

   ```typescript
   import PrimeVue from 'primevue/config';
   import circuitPrimevue from '@jumpcloud/circuit/primevue';

   app.use(PrimeVue, circuitPrimevue);
   ```

   If missing, add it so generated components render correctly.

### Step 2: Fetch Design Data

- Use Figma MCP to fetch node structure when a frame is selected
- Or parse Figma URL to identify design elements
- Identify: components, layout hierarchy, design tokens, spacing, colors, typography

### Step 3: Component Mapping (Inventory First)

**Before writing code**, inventory the Figma design and map each region to **existing library components**. We use **unstyled PrimeVue**; Circuit provides styling via pass-through primitives in `circuit/src/primevue-primitives/`.

1. **List UI elements** in the design (buttons, inputs, modals, cards, tables, headings, etc.).
2. **Map to library components** in priority order:
   - **Circuit custom components** (`@jumpcloud/circuit/components`): FormField, CardButton, Chip, DataTable, Dropdown, PageHeader, AppNavigation, etc.
   - **PrimeVue components** (`primevue/*`) **only if a primitive exists in Circuit**: Check `circuit/src/primevue-primitives/index.ts` (or the package’s exported preset). If the PrimeVue component (e.g. a specific widget) is **not** listed there, **do not** use it in the app yet. Instead, **suggest to the user that the component be created in the design system (Circuit) first** (add a new primitive and wire it in the preset), then proceed in the app. Use Button, Dialog, InputText, Select, Textarea, etc. only when Circuit provides their pass-through.
   - **Custom composition in app** (last resort): Only when no Circuit or PrimeVue component fits; use **only** theme tokens for layout, spacing, typography, and color.

3. **Do not build from scratch** what the library already provides (e.g. do not hand-roll a button or modal when Button/Dialog exist).

Use [reference.md](references/reference.md) for component list and primitives, and [examples.md](references/examples.md) for the gold-standard page example.

#### Style tweaks when the component exists in Circuit

If a Circuit/PrimeVue component exists but needs **small style changes**:

1. **Prefer `class`** on the component or a wrapping element if it can achieve the change (e.g. `class="w-full"`, theme token classes).
2. **Use passThrough (`pt`) as last resort** when you need to target internal parts (e.g. `root`, `label`). Use only theme tokens or minimal utilities in `pt`. When using `pt`, consider **ptOptions** (e.g. `ptOptions="{ mergeProps: true }"` to merge your overrides with Circuit’s default pass-through so base styling is preserved). See [reference.md](references/reference.md) for passThrough and ptOptions.

### Step 4: Map Design Tokens to Tailwind

**Theming priority: Custom Theme Tokens over standard Tailwind.**

- **Avoid** standard Tailwind color/size utilities when a theme token exists: e.g. do **not** use `bg-blue-500`, `text-gray-700`, or arbitrary spacing that bypasses the design system.
- **Use** Circuit Tailwind classes from the shared theme:
  - **Spacing**: `gap-md`, `p-sm`, `m-lg`, `gap-xs`–`gap-xl` (see [reference.md](references/reference.md) and `circuit/docs/tailwind/spacing.md`)
  - **Typography**: `text-heading-1`–`text-heading-6`, `text-body`, `text-sm`, `text-xs`, `font-normal`, `font-semibold`, `font-bold` (see typography.md)
  - **Colors**: `text-neutral-base`, `text-neutral-muted`, `bg-button-primary-base`, `bg-neutral-base`, `border-neutral-base`, `text-error-base`, etc. (see color-tokens.md and reference theme table)
- The `@config '@jumpcloud/circuit/tailwind';` directive (or equivalent) makes these tokens available.
- Never write `<style>` blocks unless absolutely necessary (and document why).

### Step 5: Choose Icons

- **JumpCloud-specific**: Use `@jumpcloud/icons` (e.g. `DeviceGroupsIcon`, `WorkflowIcon`, `NewTrialIcon`, `CustomerSupportIcon`)
- **General icons**: Use `@heroicons/vue/24/outline` or `@heroicons/vue/24/solid` (e.g. `XMarkIcon`, `HomeIcon`, `Cog6ToothIcon`)
- **Decision rule**: If design uses JumpCloud product/feature icon, prefer `@jumpcloud/icons` first; otherwise use heroicons

### Step 6: Decide Component Placement

Infer from current workspace structure (e.g. `src/components/`, `apps/*/src/components/`):

- **Feature components**: `components/FeatureName/ComponentName.vue` (e.g. `components/panels/WorkflowPanel.vue`)
- **Shared UI**: `components/ComponentName.vue` for app-level shared
- **Complex components**: `ComponentName/ComponentName.vue` + `ComponentName/index.ts` + `ComponentName/__tests__/`
- **Tests**: `__tests__/ComponentName.test.ts` adjacent to component
- **Barrel exports**: `index.ts` for component folders when several components exist

### Step 7: Generate Vue SFCs

Create Vue Single File Components with:

- `defineOptions({ name: 'ComponentName' })` for component name
- `data-test-id` attributes using `$testId` helper on key elements
- Proper slots when needed (e.g. FormField slot pattern)
- TypeScript props with proper types
- **Tailwind utilities only**—no `<style>` blocks unless absolutely necessary
- **Correct import paths**: From the design system package as resolved in Step 0 (e.g. `import { FormField } from '@jumpcloud/circuit/components'` when using `@jumpcloud/circuit` from node_modules). See [examples.md](references/examples.md) for multi-repo import patterns.
- **PrimeVue styling**: Prefer `class` for tweaks; use `pt` (passThrough) only when necessary, with `ptOptions` (e.g. `mergeProps: true`) when merging with Circuit’s default.

Example structure:

```vue
<template>
  <div class="flex flex-col gap-md" :data-test-id="$testId('root')">
    <!-- Component content using Tailwind utilities -->
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'ComponentName',
});

// Props, composables, logic
</script>
```

### Step 8: Generate Tests (if `includeTests`)

When `includeTests` parameter is true:

- Create Vitest test file following Circuit patterns
- Use `findByTestId`, `data-test-id` for element selection
- Follow [VITEST_SETUP_GUIDE](jumpcloud-common-ui/packages/circuit/VITEST_SETUP_GUIDE.md)
- Mock `@jumpcloud/circuit/composables` when needed
- Test file location: `__tests__/ComponentName.test.ts` adjacent to component

## Component Checklist

- [ ] Discovered design system location (package.json) and resolved theme/component sources (Step 0)
- [ ] Followed component priority: Circuit → PrimeVue → Custom (last resort); inventoried Figma and mapped to library components before coding
- [ ] Verified app has `app.use(PrimeVue, circuitPrimevue)` and Circuit Tailwind config
- [ ] **Theming**: Used Custom Theme Tokens only; avoided standard Tailwind colors (e.g. no `bg-blue-500`)
- [ ] Used `$testId` and `data-test-id` on key elements
- [ ] **CRITICAL**: Used Tailwind utilities only—avoided custom CSS. Circuit tokens come from `@config '@jumpcloud/circuit/tailwind';`.
- [ ] Followed Circuit typography/spacing/color tokens (see references/reference.md and circuit/docs/tailwind/)
- [ ] Used `@jumpcloud/icons` for JumpCloud icons, `@heroicons/vue` for general icons
- [ ] Component has `defineOptions({ name: '...' })`
- [ ] Proper TypeScript types for props
- [ ] Slots used correctly (e.g. FormField slot pattern)
- [ ] Imports use correct package path for the workspace (e.g. `@jumpcloud/circuit/components` for Admin Portal)
- [ ] PrimeVue: Only used components that have a primitive in Circuit; if not present, suggested creating it in Circuit first. Style tweaks: class first, then `pt`/`ptOptions` as last resort.

## Additional Resources

- For Circuit API reference, theme schema, and file locations, see [reference.md](references/reference.md)
- For the gold-standard page example and import paths, see [examples.md](references/examples.md)
- Circuit Tailwind docs: `circuit/docs/tailwind/` (spacing.md, typography.md, color-tokens.md, configuration.md)
- Circuit PrimeVue docs: `circuit/docs/primevue-primitives/configuration.md`
- Circuit testing guide: `circuit/VITEST_SETUP_GUIDE.md`
