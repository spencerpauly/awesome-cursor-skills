---
name: design-system-authoring
description: Author and expand the Circuit Design System (jumpcloud-common-ui/packages/circuit). Analyze Figma designs and build production-ready Vue components using strictly configured unstyled PrimeVue and custom Tailwind theme tokens. Handles primitives, custom components, strict pt typing, and documentation.
---

# Design System Authoring

Author and expand the **Circuit Design System** (`jumpcloud-common-ui/packages/circuit`). Analyze Figma designs and build production-ready Vue components using our **strictly configured, unstyled PrimeVue** setup and **custom Tailwind theme**.

## Core Objective

Act as a **Senior Design System Engineer**. Your task is to:

- Analyze Figma designs and determine the correct component architecture
- Build production-ready components with **strict type safety**
- Use **only** our custom Tailwind theme tokens (no arbitrary classes)
- Generate comprehensive documentation for every component
- Maintain architectural consistency with existing Circuit patterns

## When to Apply

- User asks to add a new component to Circuit / the design system
- User provides a Figma design for a component that should live in the shared library
- User asks to create a PrimeVue primitive passthrough
- User asks to extend or modify an existing Circuit component
- User mentions "design system", "circuit", or "shared component library"

## Prerequisites

- **Workspace**: `jumpcloud-common-ui/packages/circuit`
- **Dependencies**: `primevue`, `tailwindcss`, `vue` ^3.5, `@jumpcloud/icons`, `@heroicons/vue`
- **Figma MCP** (optional): For fetching design node structure

---

## Decision Engine

**MANDATORY**: Before writing any code, execute this decision engine.

### Step 1: Analyze the Figma Design

1. **Identify the component type**:
   - Is it a form control (input, select, checkbox)?
   - Is it a feedback element (toast, message, badge)?
   - Is it a layout/container (dialog, drawer, panel)?
   - Is it a navigation element (menu, tabs)?
   - Is it a data display (table, list, card)?

2. **Identify required functionality**:
   - What props/states does it need?
   - Does it have slots?
   - Does it emit events?
   - Does it have variants (size, severity, etc.)?

### Step 2: Primitive vs. Custom Decision

**CRITICAL**: Determine if this is a PrimeVue primitive or a custom component.

| Criteria | → Primitive (pt config) | → Custom Component |
|----------|-------------------------|---------------------|
| 1:1 match with PrimeVue component | ✅ | ❌ |
| Only needs styling, no structural changes | ✅ | ❌ |
| Requires combining multiple PrimeVue components | ❌ | ✅ |
| Requires custom internal state/logic | ❌ | ✅ |
| Requires structural DOM changes | ❌ | ✅ |
| PrimeVue component doesn't exist for this pattern | ❌ | ✅ |

**If Primitive**: Create/update a file in `src/primevue-primitives/` and wire it in `index.ts`.

**If Custom**: Create a Vue SFC in `src/custom-components/`.

### Step 3: Pattern Matching (Search Existing Code)

**MANDATORY**: Before drafting new code, search the Circuit codebase for similar patterns.

1. **Search primitives**: `src/primevue-primitives/*.ts`
   - Look for similar pt structures
   - Copy typing patterns from existing primitives
   - Match class naming conventions

2. **Search custom components**: `src/custom-components/*.vue`
   - Look for similar component structures
   - Match prop/slot/emit patterns
   - Copy test ID patterns (`$testId`)

3. **Search documentation**: `docs/**/*.md`
   - Match documentation structure
   - Copy `<CodeSample>` patterns
   - Match props table format

**Do not invent new patterns**. Mimic existing Circuit architecture.

---

## Strict Typing Rules

### No Loose Types

**FORBIDDEN**:
- `any`
- `Record<string, any>`
- `object`
- Untyped function parameters
- Loose generic definitions

### PrimeVue pt Typing

**MANDATORY**: The passthrough (`pt`) object must be strictly typed using PrimeVue's exported interfaces.

1. **Find the correct interface** in `node_modules/primevue/`:
   - `ButtonPassThroughOptions` from `primevue/button`
   - `DialogPassThroughOptions` from `primevue/dialog`
   - `SelectPassThroughOptions` from `primevue/select`
   - etc.

2. **Import and type the pt object**:

   ```typescript
   import { TagPassThroughOptions } from 'primevue/tag';

   const tagPT: TagPassThroughOptions = {
     root: ({ props }) => {
       // Strictly typed: props is TagProps
       return 'class-string';
     },
   };

   export default tagPT;
   ```

3. **Investigate the interface** if unsure:
   - Check `node_modules/primevue/{component}/index.d.ts`
   - Look for `{Component}PassThroughOptions` export
   - Check the `pt` property structure in the interface

See [reference.md](references/reference.md) for the complete pt typing workflow.

---

## Styling & Theming Rules

### Unstyled Mode

Circuit uses PrimeVue in **completely unstyled mode** (`unstyled: true`). All styling comes from our pt configuration.

### Theme Token Exclusivity

**FORBIDDEN**: Arbitrary Tailwind classes (e.g., `bg-blue-500`, `text-gray-700`, `p-4`).

**REQUIRED**: Only use tokens from our custom Tailwind theme:

| Category | Example Tokens |
|----------|----------------|
| **Background** | `bg-neutral-base`, `bg-button-primary-base`, `bg-field-base` |
| **Text** | `text-neutral-base`, `text-neutral-muted`, `text-error-base` |
| **Border** | `border-neutral-base`, `shadow-field-base`, `shadow-button-primary-default` |
| **Spacing** | `gap-md`, `p-sm`, `m-lg`, `gap-xs`–`gap-xl` |
| **Typography** | `text-heading-3`, `text-body-md`, `text-sm`, `font-semibold` |
| **Effects** | `transition-colors-shadow`, `duration-168`, `rounded`, `rounded-lg` |

**Source of truth**: `src/tailwind/` (colors, spacing, typography, effects, components).

### Class String Patterns

In pt configurations, return class strings or arrays:

```typescript
// String
root: 'flex items-center gap-md p-sm bg-neutral-base'

// Array (for conditional classes)
root: ({ props }) => [
  'flex items-center gap-md',
  props.disabled ? 'bg-field-disabled' : 'bg-field-base',
]

// Object with class and style
root: ({ props }) => ({
  class: 'flex items-center',
  style: { maxWidth: '500px' },
})
```

---

## Component Structure

### Primitive (pt config)

Location: `src/primevue-primitives/{component}.ts`

```typescript
import { {Component}PassThroughOptions } from 'primevue/{component}';

const {component}PT: {Component}PassThroughOptions = {
  root: ({ props, instance }) => {
    // Return class string based on props/state
    let classes = 'base-classes';

    if (props.disabled) {
      classes += ' disabled-classes';
    }

    return classes;
  },
  // ... other pt sections
};

export default {component}PT;
```

Then wire in `src/primevue-primitives/index.ts`:

```typescript
import {component} from './{component}';

const config: PrimeVueConfiguration = {
  unstyled: true,
  pt: {
    // ... existing
    {component},
  },
};
```

### Custom Component

Location: `src/custom-components/{ComponentName}.vue`

```vue
<template>
  <div class="flex flex-col gap-md" :data-test-id="$testId('root')">
    <!-- Use only theme tokens -->
  </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';
// Import PrimeVue components if wrapping
// Import icons from @heroicons/vue or @jumpcloud/icons

defineOptions({
  name: 'ComponentName',
});

// Strictly typed props
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  severity: {
    type: String as PropType<'default' | 'error' | 'warning' | 'success'>,
    default: 'default',
  },
});

// Strictly typed slots
defineSlots<{
  default(props: { inputId: string }): unknown;
  icon?(props: { iconClass: string }): unknown;
}>();

// Strictly typed emits
const emit = defineEmits<{
  change: [value: string];
  click: [];
}>();
</script>
```

Then export in `src/custom-components/index.ts`:

```typescript
export { default as ComponentName } from './ComponentName.vue';
```

---

## Documentation Requirements

**MANDATORY**: Every component must have documentation.

### Documentation Location

- **Primitives**: `docs/primevue-primitives/{component}.md`
- **Custom components**: `docs/custom-components/{ComponentName}.md`

### Documentation Structure

```markdown
<script setup>
import ComponentName from '@/custom-components/ComponentName.vue';
import { ref } from 'vue';

const demoValue = ref('');
</script>

# ComponentName

Brief description of what the component does.

[Figma Link](https://figma.com/...)

## Demo

<CodeSample>
  <ComponentName v-model="demoValue" label="Example" />
</CodeSample>

## Usage

```html
<template>
  <ComponentName label="Field Label" />
</template>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| label | `string` | — | The field label (required) |
| severity | `'default' \| 'error' \| 'warning' \| 'success'` | `'default'` | Visual severity |

## Slots

| Slot | Props | Description |
|------|-------|-------------|
| default | `{ inputId: string }` | The input element |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| change | `string` | Emitted when value changes |
```

### Update Sidebar Config

**MANDATORY**: Add the component to `docs/.vitepress/config.ts`:

```typescript
sidebar: [
  {
    text: 'PrimeVue Primitives', // or 'Custom Components'
    items: [
      // ... existing items
      { text: 'ComponentName', link: '/primevue-primitives/componentname' },
    ],
  },
],
```

---

## Workflow Summary

1. **Analyze Figma** → Identify component type and requirements
2. **Decision Engine** → Primitive or Custom?
3. **Pattern Match** → Search existing Circuit code for similar patterns
4. **Type Investigation** → Find PrimeVue pt interfaces in node_modules
5. **Implement** → Write strictly typed code using only theme tokens
6. **Document** → Create comprehensive documentation
7. **Wire Up** → Export component and update sidebar config

---

## Component Checklist

- [ ] **Decision Engine**: Determined primitive vs. custom
- [ ] **Pattern Matching**: Searched existing Circuit code for similar patterns
- [ ] **Strict Typing**: No `any`, `Record<string, any>`, or loose types
- [ ] **pt Typing**: Used correct `{Component}PassThroughOptions` interface
- [ ] **Theme Tokens Only**: No arbitrary Tailwind classes
- [ ] **Test IDs**: Used `$testId` helper on key elements
- [ ] **Documentation**: Created comprehensive docs in `docs/` folder
- [ ] **Sidebar**: Updated `docs/.vitepress/config.ts`
- [ ] **Exports**: Added to `index.ts` (primitives or custom-components)

## Additional Resources

- For pt typing workflow and theme token mapping, see [reference.md](references/reference.md)
- For primitive and custom component examples, see [examples.md](references/examples.md)
- Circuit Tailwind docs: `docs/tailwind/` (color-tokens.md, typography.md, spacing.md)
- PrimeVue docs: https://primevue.org/
