# Circuit API Reference

Quick reference for Circuit imports, setup, theme tokens, and file locations. Use this as the **technical map** when resolving the design system from `package.json` and when applying theme tokens.

## File Structure (Where to Find Definitions)

The agent must resolve the design system location from the app’s `package.json`, then use the right paths for components and theme.

| Context | Design system location | Component exports | Tailwind theme config | Docs / tokens |
|--------|------------------------|-------------------|------------------------|---------------|
| **Consumed via npm** (e.g. Admin Portal) | `node_modules/@jumpcloud/circuit` | `node_modules/@jumpcloud/circuit/dist/components.js` (and `.d.ts`) | `@jumpcloud/circuit/tailwind` (app references via `@config '@jumpcloud/circuit/tailwind'` in CSS) | `node_modules/@jumpcloud/circuit/` has no docs; use this reference and [examples](examples.md). For token lists, see Circuit repo or published docs. |
| **Local in monorepo** (e.g. jumpcloud-common-ui) | `jumpcloud-common-ui/packages/circuit` or workspace path | Package `exports["./components"]` → `dist/components.js` | `packages/circuit/src/tailwind/index.ts` (builds to `dist/tailwind.js`) | `packages/circuit/docs/` — e.g. `docs/tailwind/spacing.md`, `typography.md`, `color-tokens.md`, `configuration.md`. **Which PrimeVue components are styled**: `packages/circuit/src/primevue-primitives/index.ts` |

**Import paths in app code** are the same in both cases: use the **package name** as declared in the app’s `package.json` (e.g. `@jumpcloud/circuit`). So:

- **Components**: `import { FormField, PageHeader } from '@jumpcloud/circuit/components';`
- **Composables**: `import { useContainer } from '@jumpcloud/circuit/composables';`
- **Tailwind**: App does not import the theme file directly; it points to it in CSS with `@config '@jumpcloud/circuit/tailwind';` so that Circuit tokens (e.g. `bg-button-primary-base`, `text-heading-3`) are available in utility classes.

**When the package is local**, the agent can read token and doc files from the repo for accuracy:

- Theme source: `jumpcloud-common-ui/packages/circuit/src/tailwind/` (e.g. `colors/`, `spacing/`, `typography/`, `figma/variables.json`)
- Built theme entry: `packages/circuit/dist/tailwind.js` (or consumed as `@jumpcloud/circuit/tailwind`)
- Docs: `jumpcloud-common-ui/packages/circuit/docs/` and `docs/tailwind/` for spacing, typography, color-tokens, configuration.

## Tailwind Theme Schema Reference

Use these **Custom Theme Tokens** instead of raw Tailwind utilities (e.g. avoid `bg-blue-500`). Token names map to Tailwind utilities as `{utility}-{tokenKey}`.

### Colors

| Category | Utility prefix | Example tokens (class examples) | Notes |
|----------|----------------|----------------------------------|--------|
| **Background** | `bg-` | `neutral-base`, `neutral-muted`, `button-primary-base`, `button-secondary-base`, `button-danger-base`, `error-base`, `success-base` | e.g. `bg-neutral-base`, `bg-button-primary-base` |
| **Text** | `text-` | `neutral-base`, `neutral-muted`, `error-base`, `error-bold`, `success-base`, `success-bold`, `warning-base`, `warning-bold`, `branding-base` | e.g. `text-neutral-base`, `text-error-base` |
| **Border** | `border-` | `neutral-base`, `error-base` | e.g. `border-neutral-base` |
| **Icon (SVG)** | `fill-color-` / `stroke-color-` | Same semantic names as above; icon-specific tokens under `icon/` | e.g. `stroke-color-icon-error-base` |

Full token sets are driven by Figma variables; see `circuit/docs/tailwind/color-tokens.md` (or `color-palette.md`) when available. Prefer semantic tokens (e.g. `button-primary-base`) over primitive names.

### Spacing

| Token | Utility examples | Typical use |
|-------|------------------|-------------|
| **Size aliases** | `p-xs`, `p-sm`, `p-md`, `p-lg`, `p-xl`, `m-*`, `gap-*` | Padding, margin, gap (e.g. `gap-md`, `p-sm`) |
| **Scale** | `xs`: 4px, `sm`: 8px, `md`: 16px, `lg`: 24px, `xl`: 32px | From `--spacing(n)`; values in rem/px depend on theme |
| **Border radius** | `rounded`, `rounded-xs`, `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-full` | From theme `borderRadius` |

See `circuit/docs/tailwind/spacing.md` for the exact scale.

### Typography

| Token type | Utility examples | Notes |
|------------|------------------|--------|
| **Headings** | `text-heading-1` … `text-heading-6` | Font size, weight, line-height from theme |
| **Body** | `text-body`, `text-body-sm`, `text-body-xs`, plus variants (e.g. `-semibold`) | Prefer `text-body-*` over raw `text-sm` where applicable |
| **Font sizes** | `text-xs`, `text-sm`, `text-md`, `text-lg`, `text-xl` | Aliases; prefer heading/body tokens when they match intent |
| **Font weight** | `font-normal` (400), `font-semibold` (500), `font-bold` (600) | From theme `fontWeight` |

See `circuit/docs/tailwind/typography.md` for full heading/body tables.

---

## Circuit Component Imports

Import from `@jumpcloud/circuit/components`:

```typescript
import {
  FormField,
  CardButton,
  Chip,
  DataTable,
  Dropdown,
  CheckboxWithLabel,
  RadioButtonWithLabel,
  SelectWithSlots,
  CollapsiblePanel,
  MessageNotification,
  ToastNotification,
  Paginator,
  Password,
  InputOtp,
  LinkText,
  AppNavigation,
  PageHeader,
} from '@jumpcloud/circuit/components';
```

### Available Components

- **FormField**: Form field wrapper with label, help text, tooltip support
- **CardButton**: Card-style button component
- **Chip**: Badge/chip component
- **DataTable**: Data table with Circuit styling
- **Dropdown**: Dropdown select component
- **CheckboxWithLabel**: Checkbox with integrated label
- **RadioButtonWithLabel**: Radio button with integrated label
- **SelectWithSlots**: Select component with slot support
- **CollapsiblePanel**: Collapsible content panel
- **MessageNotification**: Inline message notification
- **ToastNotification**: Toast notification component
- **Paginator**: Pagination component
- **Password**: Password input with visibility toggle
- **InputOtp**: OTP input component
- **LinkText**: Styled link text component
- **AppNavigation**: Application navigation component
- **PageHeader**: Page title, description, and actions slot (layout component)

## PrimeVue Component Imports

Import PrimeVue components from their subpaths (for tree-shaking):

```typescript
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Select from 'primevue/select';
import Checkbox from 'primevue/checkbox';
import RadioButton from 'primevue/radiobutton';
import Toast from 'primevue/toast';
import Tooltip from 'primevue/tooltip';
```

## Circuit Composables

```typescript
import { useContainer } from '@jumpcloud/circuit/composables';

// Use for Dialog/Drawer container mounting
const { containerElement } = useContainer();
```

## PrimeVue: Unstyled + Circuit Primitives

Circuit uses **unstyled** PrimeVue (`unstyled: true`) and supplies all styling via a global pass-through preset (`pt`). The list of PrimeVue components that are “present” and styled is defined in **`circuit/src/primevue-primitives/index.ts`** (e.g. button, dialog, inputtext, select, textarea, datatable, paginator, chip, tag, tooltip, etc.).

- **If a PrimeVue component is not in that preset**: Do not use it in the app. Suggest to the user to **add the primitive in the design system (Circuit) first**, then use it in the app.
- **If it is in the preset**: Use it; it will be styled by Circuit’s pass-through.

The app must use Circuit’s PrimeVue preset:

```typescript
// In main.ts, initialize.ts, or app entry point
import PrimeVue from 'primevue/config';
import circuitPrimevue from '@jumpcloud/circuit/primevue';

app.use(PrimeVue, circuitPrimevue);
```

**Verify**: Check if the app already has this setup before generating components. Add if missing.

## Tailwind Setup (index.css)

The app's `index.css` must include Circuit Tailwind config:

```css
@config '@jumpcloud/circuit/tailwind';
@plugin '@tailwindcss/container-queries';
@source './index.html';
@source './**/*.{html,js,ts,vue}';
@source '../node_modules/@jumpcloud/circuit/dist/**/*.{js,ts,vue}';

@layer base {
  /* App-specific base styles, scroll isolation, etc. */
  #app-root *,
  #app-root *::before,
  #app-root *::after {
    border-style: solid;
    border-width: 0;
    font-family: 'Inter', sans-serif;
  }
}

/* App root selector varies (e.g. #single-spa-application\:\@jumpcloud-ap\/workflows_app or #app) */
#app-root {
  @import "tailwindcss/utilities" layer(utilities);
  @import "tailwindcss/theme.css" layer(theme) important;
  @import "tailwindcss/preflight.css" layer(base);
}
```

**Critical**: The `@config '@jumpcloud/circuit/tailwind';` directive makes all
Circuit Tailwind tokens available.

## Icon Imports

### JumpCloud Icons

Use `@jumpcloud/icons` for JumpCloud-specific icons:

```typescript
import {
  DeviceGroupsIcon,
  WorkflowIcon,
  NewTrialIcon,
  CustomerSupportIcon,
  AccessIcon,
  DeviceManagementIcon,
  PasswordManagerIcon,
  SaasManagementIcon,
  VaultIcon,
  // ... see @jumpcloud/icons package for full list
} from '@jumpcloud/icons';
```

### Heroicons

Use `@heroicons/vue` for general icons:

```typescript
// Outline icons (most common)
import {
  XMarkIcon,
  HomeIcon,
  Cog6ToothIcon,
  ArrowRightIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from '@heroicons/vue/24/outline';

// Solid icons (when needed)
import {
  HomeIcon as HomeIconSolid,
  CheckIcon as CheckIconSolid,
} from '@heroicons/vue/24/solid';
```

### Icon Usage in PrimeVue Components

PrimeVue components expose icon slots:

```vue
<Button>
  <template #icon="iconProps">
    <XMarkIcon :class="iconProps.class" />
  </template>
</Button>
```

## Tailwind Token Reference

### Spacing

Use Circuit spacing aliases (extends Tailwind's default scale):

- `gap-xs`, `gap-sm`, `gap-md`, `gap-lg`, `gap-xl` - Gap utilities
- `p-xs`, `p-sm`, `p-md`, `p-lg`, `p-xl` - Padding utilities
- `m-xs`, `m-sm`, `m-md`, `m-lg`, `m-xl` - Margin utilities
- `gap-0.5`, `gap-1`, `gap-2`, `gap-3`, `gap-4`, etc. - Standard Tailwind spacing

**Reference**: `circuit/docs/tailwind/spacing.md`

### Typography

#### Headings

- `text-heading-1` - Largest heading
- `text-heading-2` - Second largest heading
- `text-heading-3` - Third largest heading
- `text-heading-4` - Fourth largest heading
- `text-heading-5` - Fifth largest heading
- `text-heading-6` - Smallest heading

#### Body Text

- `text-body` - Default body text
- `text-sm` - Small text
- `text-xs` - Extra small text

#### Font Weights

- `font-normal` - 400
- `font-semibold` - 500
- `font-bold` - 600

**Reference**: `circuit/docs/tailwind/typography.md`

### Colors

#### Text Colors

- `text-neutral-base` - Default text color
- `text-neutral-muted` - Muted text
- `text-error-base`, `text-error-bold` - Error text
- `text-success-base`, `text-success-bold` - Success text
- `text-warning-base`, `text-warning-bold` - Warning text
- `text-branding-base` - Branding color

#### Background Colors

- `bg-neutral-base` - Default background
- `bg-button-primary-base` - Primary button background
- `bg-button-secondary-base` - Secondary button background
- `bg-button-danger-base` - Danger button background
- `bg-error-base` - Error background
- `bg-success-base` - Success background

#### Border Colors

- `border-neutral-base` - Default border
- `border-error-base` - Error border

#### Icon Colors

- `stroke-color-icon-error-base` - Error icon color
- `stroke-color-icon-warning-base` - Warning icon color
- `stroke-color-icon-success-base` - Success icon color
- `text-branding-base` - Branding icon color

**Reference**: `circuit/docs/tailwind/color-tokens.md`

## Component Priority Order

When mapping Figma designs to components:

1. **Circuit custom components** (`@jumpcloud/circuit/components`)
   - FormField, CardButton, Chip, DataTable, Dropdown, PageHeader, etc.
   - Use these first when they match the design.

2. **PrimeVue components** (`primevue/*`) **only when a primitive exists in Circuit**
   - See `circuit/src/primevue-primitives/index.ts` for the list (button, dialog, inputtext, select, textarea, datatable, paginator, chip, tag, tooltip, etc.).
   - If the component is **not** in the preset, suggest creating it in the design system (Circuit) first, then use it in the app.
   - Use with Circuit’s preset (app must have `app.use(PrimeVue, circuitPrimevue)`).

3. **Create custom component in app** (last resort)
   - Only if Circuit and PrimeVue don’t provide what’s needed.
   - Use Tailwind utilities only—no custom CSS—and only Circuit theme tokens.

## Styling Tweaks: Class vs passThrough (`pt`) and ptOptions

When a component exists in Circuit but needs **small style changes**:

1. **Prefer `class`** on the component or wrapper if it achieves the change (e.g. `class="w-full"`, or theme token classes).
2. **Use passThrough (`pt`) as last resort** when you must target internal DOM parts (e.g. `root`, `label`, `input`). In `pt`, use only theme tokens or minimal Tailwind utilities so styling stays consistent.
3. **Use ptOptions** when applying `pt`, so that your overrides combine correctly with Circuit’s default:
   - **`mergeProps: true`** – Merge your `pt` with Circuit’s default (add or override classes); use when you want to extend or tweak, not replace.
   - **`mergeProps: false`** / **`mergeSections: false`** – Replace instead of merge; use only when you need to fully override a section.

Example (add classes on top of Circuit’s button):

```vue
<Button
  label="Back"
  severity="secondary"
  variant="text"
  :pt="{ root: 'px-0 bg-transparent' }"
  :ptOptions="{ mergeProps: true }"
/>
```

Example (conditional merge):

```vue
<Button
  :pt="{ root: 'hidden!', label: 'w-max' }"
  :ptOptions="{ mergeProps: isBackButtonVisible }"
/>
```

## Styling Approach

**CRITICAL: Avoid custom CSS. Use Tailwind utilities only.**

- The `@config '@jumpcloud/circuit/tailwind';` directive makes all Circuit tokens available.
- Use Circuit Tailwind tokens exclusively.
- Never write `<style>` blocks unless absolutely necessary (and document why).
- When creating custom components, only use Tailwind utility classes from the Circuit theme.
- For PrimeVue components: prefer `class` for tweaks; use `pt` (and `ptOptions` when merging) only when class cannot target the right part.

## Folder Patterns

Infer from current workspace structure:

- **Feature components**: `components/FeatureName/ComponentName.vue`
- **Shared UI**: `components/ComponentName.vue`
- **Complex components**: `ComponentName/ComponentName.vue` +
  `ComponentName/index.ts` + `ComponentName/__tests__/`
- **Tests**: `__tests__/ComponentName.test.ts` adjacent to component
- **Barrel exports**: `index.ts` for component folders

## Component Structure Pattern

```vue
<template>
  <div class="flex flex-col gap-md" :data-test-id="$testId('root')">
    <!-- Component content using Tailwind utilities -->
  </div>
</template>

<script setup lang="ts">
import { PropType } from 'vue';

defineOptions({
  name: 'ComponentName',
});

const props = defineProps({
  // Props with proper types
});

// Composables, logic
</script>
```

## Test ID Pattern

Use `$testId` helper for test IDs:

```vue
<div :data-test-id="$testId('root')">
  <button :data-test-id="$testId('submit-button')">Submit</button>
</div>
```

The app should have `$testId` available globally (via mixin or plugin).

## FormField Slot Pattern

FormField uses a slot pattern for inputs:

```vue
<FormField label="Name" required>
  <template #default="{ inputId }">
    <InputText
      :id="inputId"
      v-model="name"
      class="w-full"
      :data-test-id="$testId('nameInput')"
    />
  </template>
</FormField>
```

## Additional Resources

- Circuit Tailwind docs: `circuit/docs/tailwind/` (spacing.md, typography.md,
  color-tokens.md, configuration.md)
- Circuit PrimeVue docs: `circuit/docs/primevue-primitives/configuration.md`
- Circuit testing guide: `circuit/VITEST_SETUP_GUIDE.md`
