# Design System Authoring Reference

Technical reference for authoring Circuit Design System components. Covers pt typing workflow, type extraction from node_modules, and theme token mapping.

---

## pt Typing Workflow

### Step 1: Identify the PrimeVue Component

Determine which PrimeVue component you're creating a primitive for:

| Component | Import Path | PassThrough Interface |
|-----------|-------------|----------------------|
| Avatar | `primevue/avatar` | `AvatarPassThroughOptions` |
| Badge | `primevue/badge` | `BadgePassThroughOptions` |
| Button | `primevue/button` | `ButtonPassThroughOptions` |
| Checkbox | `primevue/checkbox` | `CheckboxPassThroughOptions` |
| Chip | `primevue/chip` | `ChipPassThroughOptions` |
| Column | `primevue/column` | `ColumnPassThroughOptions` |
| DataTable | `primevue/datatable` | `DataTablePassThroughOptions` |
| Dialog | `primevue/dialog` | `DialogPassThroughOptions` |
| Divider | `primevue/divider` | `DividerPassThroughOptions` |
| Drawer | `primevue/drawer` | `DrawerPassThroughOptions` |
| IconField | `primevue/iconfield` | `IconFieldPassThroughOptions` |
| InputGroup | `primevue/inputgroup` | `InputGroupPassThroughOptions` |
| InputText | `primevue/inputtext` | `InputTextPassThroughOptions` |
| Menu | `primevue/menu` | `MenuPassThroughOptions` |
| Message | `primevue/message` | `MessagePassThroughOptions` |
| MultiSelect | `primevue/multiselect` | `MultiSelectPassThroughOptions` |
| Paginator | `primevue/paginator` | `PaginatorPassThroughOptions` |
| Panel | `primevue/panel` | `PanelPassThroughOptions` |
| Popover | `primevue/popover` | `PopoverPassThroughOptions` |
| ProgressSpinner | `primevue/progressspinner` | `ProgressSpinnerPassThroughOptions` |
| RadioButton | `primevue/radiobutton` | `RadioButtonPassThroughOptions` |
| Select | `primevue/select` | `SelectPassThroughOptions` |
| SelectButton | `primevue/selectbutton` | `SelectButtonPassThroughOptions` |
| Skeleton | `primevue/skeleton` | `SkeletonPassThroughOptions` |
| Tab | `primevue/tab` | `TabPassThroughOptions` |
| TabList | `primevue/tablist` | `TabListPassThroughOptions` |
| TabPanels | `primevue/tabpanels` | `TabPanelsPassThroughOptions` |
| Tag | `primevue/tag` | `TagPassThroughOptions` |
| Textarea | `primevue/textarea` | `TextareaPassThroughOptions` |
| TieredMenu | `primevue/tieredmenu` | `TieredMenuPassThroughOptions` |
| Toast | `primevue/toast` | `ToastPassThroughOptions` |
| ToggleSwitch | `primevue/toggleswitch` | `ToggleSwitchPassThroughOptions` |
| Tooltip | `primevue/tooltip` | `TooltipDirectivePassThroughOptions` |

### Step 2: Extract Type from node_modules

If the interface isn't in the table above, investigate `node_modules/primevue/`:

```bash
# Find the type definition file
ls node_modules/primevue/{component}/

# Look for index.d.ts or {component}.d.ts
cat node_modules/primevue/{component}/index.d.ts | grep PassThrough
```

**Example**: Finding `SelectPassThroughOptions`:

```typescript
// In node_modules/primevue/select/index.d.ts:
export interface SelectPassThroughOptions {
  root?: SelectPassThroughOptionType;
  label?: SelectPassThroughOptionType;
  dropdown?: SelectPassThroughOptionType;
  overlay?: SelectPassThroughOptionType;
  list?: SelectPassThroughOptionType;
  option?: SelectPassThroughOptionType;
  // ... etc
}
```

### Step 3: Understand the PassThrough Structure

Each `PassThroughOptions` interface defines sections corresponding to DOM elements:

```typescript
interface ButtonPassThroughOptions {
  root?: ButtonPassThroughOptionType;   // <button> element
  label?: ButtonPassThroughOptionType;  // Label span
  icon?: ButtonPassThroughOptionType;   // Icon element
  loadingIcon?: ButtonPassThroughOptionType;
  badge?: ButtonPassThroughOptionType;
  // ...
}
```

Each section can be:

1. **String**: Static class string
   ```typescript
   root: 'flex items-center gap-md'
   ```

2. **Function**: Dynamic classes based on props/state
   ```typescript
   root: ({ props, instance, state }) => {
     return props.disabled ? 'opacity-50' : 'opacity-100';
   }
   ```

3. **Object**: Class + style + attributes
   ```typescript
   root: ({ props }) => ({
     class: 'flex items-center',
     style: { maxWidth: '500px' },
   })
   ```

### Step 4: Type the pt Object

```typescript
import { SelectPassThroughOptions } from 'primevue/select';

// STRICTLY TYPED — TypeScript will enforce correct sections
const selectPT: SelectPassThroughOptions = {
  root: ({ props, state }) => {
    // props is SelectProps, state is SelectState
    // TypeScript knows the exact shape
    const baseClass = 'rounded flex justify-between';

    if (props.disabled) {
      return `${baseClass} bg-field-disabled`;
    }

    if (state.focused) {
      return `${baseClass} bg-field-focused shadow-field-focus`;
    }

    return `${baseClass} bg-field-base`;
  },

  label: 'text-body-md text-neutral-base truncate',

  dropdown: 'flex items-center justify-center',

  // TypeScript error if you use a section that doesn't exist
  // invalidSection: 'foo' // ❌ Error!
};

export default selectPT;
```

### Step 5: Handle Nested Components (pc* sections)

Some components have nested PrimeVue components. These are prefixed with `pc`:

```typescript
const dialogPT: DialogPassThroughOptions = {
  root: '...',
  header: '...',
  content: '...',

  // Nested Button component for close button
  pcCloseButton: {
    root: 'p-1.5 rounded text-button-text-secondary-base',
  },

  // Nested Button component for maximize button
  pcMaximizeButton: {
    root: 'hidden', // Hide it
  },
};
```

---

## Theme Token Mapping

### File Locations

| Category | Source File | Docs |
|----------|-------------|------|
| **Colors** | `src/tailwind/colors/` | `docs/tailwind/color-tokens.md` |
| **Typography** | `src/tailwind/typography/` | `docs/tailwind/typography.md` |
| **Spacing** | `src/tailwind/spacing/` | `docs/tailwind/spacing.md` |
| **Effects** | `src/tailwind/effects/` | `docs/tailwind/box-shadow.md` |
| **Components** | `src/tailwind/components/` | (component-specific tokens) |

### Color Token Categories

#### Background Colors (`bg-*`)

```
bg-neutral-base          # Default background
bg-neutral-muted         # Muted/hover background
bg-field-base            # Form field background
bg-field-hover           # Form field hover
bg-field-focused         # Form field focused
bg-field-disabled        # Form field disabled
bg-button-primary-base   # Primary button
bg-button-primary-hover  # Primary button hover
bg-button-primary-pressed # Primary button active
bg-button-secondary-base # Secondary button
bg-button-danger-base    # Danger button
bg-tag-primary           # Tag primary
bg-tag-secondary         # Tag secondary
bg-tag-success           # Tag success
bg-tag-danger            # Tag danger
bg-tag-warning           # Tag warning
bg-tag-info              # Tag info
```

#### Text Colors (`text-*`)

```
text-neutral-base        # Default text
text-neutral-muted       # Muted text
text-error-base          # Error text
text-error-bold          # Bold error text
text-success-base        # Success text
text-success-bold        # Bold success text
text-warning-base        # Warning text
text-warning-bold        # Bold warning text
text-branding-base       # Brand color
text-button-primary-base # Button text
text-tag-primary-text    # Tag text
```

#### Border/Shadow Colors

```
border-neutral-base      # Default border
border-neutral-default_solid # Solid border
shadow-field-base        # Field shadow
shadow-field-focus       # Field focus shadow
shadow-field-error       # Field error shadow
shadow-button-primary-default # Button shadow
shadow-button-primary-pressed # Button pressed shadow
```

#### Icon Colors (SVG)

```
stroke-color-icon-error-base    # Error icon
stroke-color-icon-warning-base  # Warning icon
stroke-color-icon-success-base  # Success icon
stroke-color-neutral-muted      # Muted icon
```

### Typography Tokens

```
text-heading-1           # Largest heading
text-heading-2           # H2
text-heading-3           # H3
text-heading-4           # H4
text-heading-5           # H5
text-heading-6           # Smallest heading
text-body-md             # Body medium
text-body-sm             # Body small
text-sm                  # Small text
text-xs                  # Extra small text
font-normal              # 400
font-semibold            # 500
font-bold                # 600
leading-4                # Line height 16px
leading-5                # Line height 20px
```

### Spacing Tokens

```
gap-xs                   # 4px
gap-sm                   # 8px
gap-md                   # 16px
gap-lg                   # 24px
gap-xl                   # 32px
p-xs, p-sm, p-md, p-lg, p-xl  # Padding
m-xs, m-sm, m-md, m-lg, m-xl  # Margin
gap-0.5, gap-1, gap-2, ...    # Standard Tailwind scale
```

### Effect Tokens

```
rounded                  # Default border radius
rounded-sm               # Small radius
rounded-lg               # Large radius
rounded-full             # Full radius (pill)
transition-colors-shadow # Color + shadow transition
duration-168             # 168ms duration
shadow-e500              # Elevation shadow
```

---

## Applying Tokens in pt

### Pattern: Conditional Classes

```typescript
const buttonPT: ButtonPassThroughOptions = {
  root: ({ props }) => {
    // Base classes (always applied)
    const base = 'rounded font-bold transition-colors-shadow duration-168';

    // Severity-based classes
    const severity = (() => {
      switch (props.severity) {
        case 'secondary':
          return 'bg-button-secondary-base text-button-secondary-base';
        case 'danger':
          return 'bg-button-danger-base text-button-danger-base';
        default:
          return 'bg-button-primary-base text-button-primary-base';
      }
    })();

    // State-based classes
    const state = props.disabled
      ? 'opacity-50 cursor-not-allowed'
      : 'hover:bg-button-primary-hover active:bg-button-primary-pressed';

    return `${base} ${severity} ${state}`;
  },
};
```

### Pattern: Size Variants

```typescript
const inputPT: InputTextPassThroughOptions = {
  root: ({ props }) => {
    const base = 'rounded bg-field-base shadow-field-base';

    const size = (() => {
      switch (props.size) {
        case 'small':
          return 'h-6 text-sm px-1.5';
        default:
          return 'h-8 text-md px-2';
      }
    })();

    return `${base} ${size}`;
  },
};
```

### Pattern: Focus/Hover States

```typescript
const selectPT: SelectPassThroughOptions = {
  root: ({ props, state }) => {
    let classes = 'rounded bg-field-base shadow-field-base';

    // Hover state
    classes += ' hover:bg-field-hover';

    // Focus state (from component state)
    if (state.focused) {
      classes += ' shadow-field-focus bg-field-focused';
    }

    // Invalid state
    if (props.invalid) {
      classes += ' shadow-field-error';
    }

    // Disabled state
    if (props.disabled) {
      classes = classes
        .replace('bg-field-base', 'bg-field-disabled')
        .replace('shadow-field-base', 'shadow-field-disabled');
    }

    return classes;
  },
};
```

---

## Documentation Structure

### Primitive Documentation Template

```markdown
---
outline: deep
---

<script setup>
import ComponentName from 'primevue/componentname';
import { ref } from 'vue';
// Import icons, helpers as needed
</script>

# ComponentName

[PrimeVue Docs](https://primevue.org/componentname) / [Figma Page](https://figma.com/...)

## Variants

<CodeSample>
  <div class="flex flex-wrap gap-4">
    <ComponentName ... />
  </div>
</CodeSample>

:::info Implementation
```html
<ComponentName ... />
```
:::

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| ... | ... | ... | ... |

## Slots

| Slot | Props | Description |
|------|-------|-------------|
| ... | ... | ... |

## Accessibility

Notes on keyboard navigation, ARIA attributes, etc.
```

### Custom Component Documentation Template

```markdown
<script setup>
import ComponentName from '@/custom-components/ComponentName.vue';
import { ref } from 'vue';
</script>

# ComponentName

Brief description.

[Figma Link](https://figma.com/...)

## Demo

<CodeSample>
  <ComponentName ... />
</CodeSample>

## Usage

```html
<template>
  <ComponentName ... />
</template>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| ... | ... | ... | ... |

## Slots

| Slot | Props | Description |
|------|-------|-------------|
| ... | ... | ... |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| ... | ... | ... |
```

---

## Sidebar Configuration

### Adding a Primitive

```typescript
// docs/.vitepress/config.ts
{
  text: 'PrimeVue Primitives',
  collapsed: false,
  items: [
    { text: 'Configuration', link: '/primevue-primitives/configuration' },
    // ... existing items (alphabetical order)
    { text: 'NewComponent', link: '/primevue-primitives/newcomponent' },
  ],
},
```

### Adding a Custom Component

```typescript
// docs/.vitepress/config.ts
{
  text: 'Custom Components',
  collapsed: false,
  items: [
    // ... existing items (alphabetical order)
    { text: 'NewComponent', link: '/custom-components/NewComponent' },
  ],
},
```

---

## Checklist for New Components

### Primitive Checklist

- [ ] Created `src/primevue-primitives/{component}.ts`
- [ ] Imported `{Component}PassThroughOptions` from `primevue/{component}`
- [ ] Typed pt object: `const pt: {Component}PassThroughOptions = { ... }`
- [ ] Used only theme tokens (no arbitrary classes)
- [ ] Wired in `src/primevue-primitives/index.ts`
- [ ] Created `docs/primevue-primitives/{component}.md`
- [ ] Added to sidebar in `docs/.vitepress/config.ts`

### Custom Component Checklist

- [ ] Created `src/custom-components/{ComponentName}.vue`
- [ ] Used `defineOptions({ name: '...' })`
- [ ] Strictly typed props with `PropType<...>`
- [ ] Strictly typed slots with `defineSlots<{ ... }>()`
- [ ] Strictly typed emits with `defineEmits<{ ... }>()`
- [ ] Used only theme tokens (no arbitrary classes)
- [ ] Used `$testId` helper for test IDs
- [ ] Exported in `src/custom-components/index.ts`
- [ ] Created `docs/custom-components/{ComponentName}.md`
- [ ] Added to sidebar in `docs/.vitepress/config.ts`
