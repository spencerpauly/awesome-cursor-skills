# Design System Authoring Examples

Gold-standard examples for authoring Circuit Design System components. Use these as templates.

---

## Example A: PrimeVue Primitive (Strict pt Typing)

A customized PrimeVue primitive using strict pt typing and custom Tailwind theme tokens.

### Figma Design

- Tag/Badge component
- Variants: primary, secondary, success, danger, warning, info, contrast, accent colors
- Small height (20px), rounded corners
- Icon support on left

### Decision Engine Result

| Question | Answer |
|----------|--------|
| 1:1 match with PrimeVue? | ✅ Yes — PrimeVue `Tag` component |
| Only needs styling? | ✅ Yes — no structural changes |
| Requires combining components? | ❌ No |
| Requires custom state? | ❌ No |

**Decision**: → **Primitive** (pt configuration)

### Implementation

**File**: `src/primevue-primitives/tag.ts`

```typescript
import { TagPassThroughOptions } from 'primevue/tag';

// STRICT TYPING: TagPassThroughOptions from PrimeVue
// No `any`, no `Record<string, any>`, no loose types

const tagPT: TagPassThroughOptions = {
  root: ({ props }) => {
    // props is strictly typed as TagProps
    const severity = props.severity;

    // THEME TOKENS ONLY: No arbitrary classes like bg-blue-500
    let colorClassName = 'bg-tag-primary';
    let textClassName = 'text-tag-primary-text';
    let fontWeightClassName = 'font-semibold';

    if (severity === 'secondary') {
      colorClassName = 'bg-tag-secondary';
      textClassName = 'text-tag-secondary-text';
    } else if (severity === 'success') {
      colorClassName = 'bg-tag-success';
      textClassName = 'text-tag-success-text';
    } else if (severity === 'danger') {
      colorClassName = 'bg-tag-danger';
      textClassName = 'text-tag-danger-text';
    } else if (severity === 'warning') {
      colorClassName = 'bg-tag-warning';
      textClassName = 'text-tag-warning-text';
    } else if (severity === 'info') {
      colorClassName = 'bg-tag-info';
      textClassName = 'text-tag-info-text';
    } else if (severity === 'contrast') {
      colorClassName = 'bg-tag-contrast';
      textClassName = 'text-tag-contrast-text';
    } else if (severity === 'accent-aster') {
      colorClassName = 'bg-tag-accent-aster';
      textClassName = 'text-tag-accent-aster-text';
    } else if (severity === 'accent-purple') {
      colorClassName = 'bg-tag-accent-purple';
      textClassName = 'text-tag-accent-purple-text';
    } else if (severity === 'accent-coral') {
      colorClassName = 'bg-tag-accent-coral';
      textClassName = 'text-tag-accent-coral-text';
    } else if (severity === 'accent-yellow') {
      colorClassName = 'bg-tag-accent-yellow';
      textClassName = 'text-tag-accent-yellow-text';
    } else if (severity === 'neutral') {
      colorClassName = 'bg-neutral_solid-n20';
      textClassName = 'text-neutral_alpha-n200a';
      fontWeightClassName = 'font-normal';
    }

    // Return array of class strings
    return [
      'flex items-center gap-0.5 px-0.5 text-body-sm rounded-sm w-fit h-5 whitespace-nowrap',
      colorClassName,
      textClassName,
      fontWeightClassName,
    ];
  },

  // Icon section — also strictly typed
  icon: 'size-4 -ml-0.5',
};

export default tagPT;
```

### Wiring in index.ts

**File**: `src/primevue-primitives/index.ts`

```typescript
import { PrimeVueConfiguration } from 'primevue';
import tag from './tag';
// ... other imports

const config: PrimeVueConfiguration = {
  unstyled: true,
  pt: {
    // ... existing primitives
    tag,
  },
};

export default config;
```

### Documentation

**File**: `docs/primevue-primitives/tag.md`

```markdown
---
outline: deep
---

<script setup>
import Tag from 'primevue/tag';
import { HomeIcon } from '@heroicons/vue/24/outline';
</script>

# Tag

[PrimeVue Docs](https://primevue.org/tag) / [Figma Page](https://figma.com/...)

## Severities

<CodeSample>
  <div class="flex flex-wrap gap-2">
    <Tag value="Primary" />
    <Tag value="Secondary" severity="secondary" />
    <Tag value="Success" severity="success" />
    <Tag value="Danger" severity="danger" />
    <Tag value="Warning" severity="warning" />
    <Tag value="Info" severity="info" />
    <Tag value="Contrast" severity="contrast" />
  </div>
</CodeSample>

## With Icon

<CodeSample>
  <Tag value="With Icon">
    <template #icon>
      <HomeIcon class="size-4" />
    </template>
  </Tag>
</CodeSample>

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| value | `string` | — | The tag text |
| severity | `'primary' \| 'secondary' \| 'success' \| 'danger' \| 'warning' \| 'info' \| 'contrast'` | `'primary'` | Visual severity |
| icon | `string` | — | Icon class (or use slot) |
```

### Update Sidebar

**File**: `docs/.vitepress/config.ts`

```typescript
{
  text: 'PrimeVue Primitives',
  items: [
    // ... existing
    { text: 'Tag', link: '/primevue-primitives/tag' },
  ],
},
```

---

## Example B: Custom/Compound Component

A custom component that wraps multiple PrimeVue primitives, showing how state and pt props are passed down correctly.

### Figma Design

- Form field with label, input, help text
- Required indicator (*)
- Label tooltip
- Help text with severity icons (error, warning, success, info)

### Decision Engine Result

| Question | Answer |
|----------|--------|
| 1:1 match with PrimeVue? | ❌ No — PrimeVue has no "FormField" |
| Only needs styling? | ❌ No — needs structural composition |
| Requires combining components? | ✅ Yes — label + slot + help text |
| Requires custom state? | ✅ Yes — inputId generation |

**Decision**: → **Custom Component**

### Implementation

**File**: `src/custom-components/FormField.vue`

```vue
<template>
  <div class="flex flex-col gap-1" :data-test-id="$testId('root')">
    <!-- Label row -->
    <div class="flex gap-1 items-center">
      <label
        :for="inputId"
        class="text-sm font-bold leading-4"
        :data-test-id="$testId('label')"
      >
        {{ props.label
        }}<span v-if="props.required" class="text-error-base">*</span>
      </label>

      <!-- Label tooltip -->
      <div
        v-if="props.labelTooltip && props.labelTooltip.length > 0"
        v-tooltip.right="props.labelTooltip"
        class="px-0.5 py-0.5 pr-1"
      >
        <QuestionMarkCircleIcon class="text-branding-base size-3" />
      </div>
    </div>

    <!-- Input slot -->
    <div :data-test-id="$testId('input-container')">
      <slot :inputId="inputId"></slot>
    </div>

    <!-- Help text -->
    <div
      v-if="helpText && helpText.length > 0"
      class="flex gap-0.5 items-start leading-3.5"
      :data-test-id="$testId('help-text')"
    >
      <!-- Severity icon -->
      <div v-if="props.helpTextSeverity !== 'default'">
        <ExclamationCircleIcon
          v-if="props.helpTextSeverity === 'error'"
          class="stroke-color-icon-error-base size-4"
        />
        <ExclamationTriangleIcon
          v-if="props.helpTextSeverity === 'warning'"
          class="stroke-color-icon-warning-base size-4"
        />
        <CheckCircleIcon
          v-if="props.helpTextSeverity === 'success'"
          class="stroke-color-icon-success-base size-4"
        />
        <InformationCircleIcon
          v-if="props.helpTextSeverity === 'info'"
          class="stroke-color-neutral-muted size-4"
        />
      </div>

      <!-- Help text content -->
      <div
        class="text-xs py-0.25"
        :class="{
          'text-success-bold': props.helpTextSeverity === 'success',
          'text-error-bold': props.helpTextSeverity === 'error',
          'text-warning-bold': props.helpTextSeverity === 'warning',
          'text-neutral-muted':
            props.helpTextSeverity === 'default' ||
            props.helpTextSeverity === 'info',
        }"
      >
        {{ props.helpText }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType, useId, computed } from 'vue';
import vTooltip from 'primevue/tooltip';

import {
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  QuestionMarkCircleIcon,
} from '@heroicons/vue/24/outline';

defineOptions({
  name: 'FormField',
});

// STRICTLY TYPED PROPS — no `any`
const props = defineProps({
  /**
   * The field label
   */
  label: {
    type: String,
    required: true,
  },

  /**
   * Whether the field is required
   */
  required: Boolean,

  /**
   * Tooltip content for the label
   */
  labelTooltip: String,

  /**
   * Help text below the input
   */
  helpText: String,

  /**
   * Severity determines icon and color
   */
  helpTextSeverity: {
    type: String as PropType<
      'default' | 'info' | 'warning' | 'error' | 'success'
    >,
    default: 'default',
  },

  /**
   * Custom input ID (auto-generated if not provided)
   */
  inputId: String,
});

// Generate inputId if not provided
const inputId = computed(() => props.inputId ?? useId());

// STRICTLY TYPED SLOTS
defineSlots<{
  /**
   * The input element
   * @param props.inputId - ID to bind to the input
   */
  default(props: { inputId: string }): unknown;
}>();
</script>
```

### Export in index.ts

**File**: `src/custom-components/index.ts`

```typescript
export { default as FormField } from './FormField.vue';
```

### Documentation

**File**: `docs/custom-components/FormField.md`

```markdown
<script setup>
import FormField from '@/custom-components/FormField.vue';
import CheckboxWithLabel from '@/custom-components/CheckboxWithLabel.vue';
import { InputText } from 'primevue';
import { ref } from 'vue';

const showLabelTooltip = ref(true);
const showHelpText = ref(true);
const required = ref(true);
const disabled = ref(false);
</script>

# FormField

FormField provides standard styling for form labels and helper text.

[Figma Link](https://figma.com/...)

## Demo

<CodeSample>
  <div class="flex gap-8 flex-wrap">
    <FormField
      label="Field Label"
      :labelTooltip="showLabelTooltip ? 'Tooltip content' : undefined"
      :helpText="showHelpText ? 'Help text content' : ''"
      helpTextSeverity="default"
      #="{ inputId }"
      :required="required"
    >
      <InputText :disabled="disabled" :id="inputId" />
    </FormField>
  </div>
</CodeSample>

<div class="flex flex-col gap-2 mt-2">
  <CheckboxWithLabel binary v-model="showLabelTooltip">
    <template #label>Show Label Tooltip</template>
  </CheckboxWithLabel>
  <CheckboxWithLabel binary v-model="showHelpText">
    <template #label>Show Help Text</template>
  </CheckboxWithLabel>
  <CheckboxWithLabel binary v-model="required">
    <template #label>Required</template>
  </CheckboxWithLabel>
</div>

## Usage

```html
<template>
  <FormField
    label="Email"
    labelTooltip="Your primary email address"
    helpText="We'll never share your email"
    helpTextSeverity="info"
    required
    #="{ inputId }"
  >
    <InputText :id="inputId" v-model="email" />
  </FormField>
</template>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| label | `string` | — | The field label (required) |
| required | `boolean` | `false` | Shows required indicator (*) |
| labelTooltip | `string` | — | Tooltip content for label |
| helpText | `string` | — | Help text below input |
| helpTextSeverity | `'default' \| 'info' \| 'warning' \| 'error' \| 'success'` | `'default'` | Help text severity |
| inputId | `string` | auto-generated | Custom input ID |

## Slots

| Slot | Props | Description |
|------|-------|-------------|
| default | `{ inputId: string }` | The input element; bind `inputId` to the input's `id` attribute |
```

### Update Sidebar

**File**: `docs/.vitepress/config.ts`

```typescript
{
  text: 'Custom Components',
  items: [
    // ... existing
    { text: 'FormField', link: '/custom-components/FormField' },
  ],
},
```

---

## Key Patterns Summary

### Primitive Pattern

1. Import `{Component}PassThroughOptions` from `primevue/{component}`
2. Type the pt object: `const pt: {Component}PassThroughOptions = { ... }`
3. Use only theme tokens in class strings
4. Wire in `src/primevue-primitives/index.ts`
5. Document in `docs/primevue-primitives/`

### Custom Component Pattern

1. Create Vue SFC in `src/custom-components/`
2. Use `defineOptions({ name: '...' })`
3. Strictly type props with `PropType<...>`
4. Strictly type slots with `defineSlots<{ ... }>()`
5. Use only theme tokens (no arbitrary classes)
6. Use `$testId` helper for test IDs
7. Export in `src/custom-components/index.ts`
8. Document in `docs/custom-components/`

### Forbidden Patterns

```typescript
// ❌ FORBIDDEN: Loose types
const pt: Record<string, any> = { ... }
const pt: any = { ... }
const pt = { ... } // untyped

// ❌ FORBIDDEN: Arbitrary Tailwind classes
'bg-blue-500 text-gray-700 p-4'

// ✅ CORRECT: Strict typing + theme tokens
import { ButtonPassThroughOptions } from 'primevue/button';
const buttonPT: ButtonPassThroughOptions = {
  root: 'bg-button-primary-base text-button-primary-base p-sm'
};
```
