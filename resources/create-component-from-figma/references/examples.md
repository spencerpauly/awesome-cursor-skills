# Component Examples

Examples showing Figma design → Vue component conversion using Circuit.

## Import Paths (Multi-Repo / Admin Portal)

When the design system is consumed from **node_modules** (e.g. JumpCloud Admin Portal):

```typescript
// Circuit components and composables — use package name
import { FormField, PageHeader } from '@jumpcloud/circuit/components';
import { useContainer } from '@jumpcloud/circuit/composables';

// PrimeVue components — subpaths for tree-shaking
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';

// Icons
import { WorkflowIcon } from '@jumpcloud/icons';
import { PlusIcon, XMarkIcon } from '@heroicons/vue/24/outline';
```

When the design system is **local in the same monorepo** (e.g. `jumpcloud-common-ui`), the app still typically imports via the package name (e.g. `@jumpcloud/circuit`) as resolved by the workspace; only the physical location of the package differs, not the import path in app code.

---

## Gold Standard: Page Layout (Layout + Custom Composition)

A full page that uses **layout components from the library** and **custom composition** with **theme tokens only**. This is the pattern to follow for complex screens.

### Figma Design

- Page with header (title, description, primary action)
- Main content area: custom card grid using theme tokens
- Cards: icon, title, description, optional action
- Footer with secondary action

### Vue Component

```vue
<template>
  <div class="flex flex-col gap-lg min-h-0" :data-test-id="$testId('root')">
    <!-- Layout component from library -->
    <PageHeader
      :data-test-id="$testId('pageHeader')"
      title="Workflows"
      description="Create and manage automation workflows."
    >
      <template #actions>
        <Button
          :data-test-id="$testId('createButton')"
          label="Create Workflow"
          severity="primary"
          @click="emit('create')"
        >
          <template #icon="iconProps">
            <PlusIcon :class="iconProps.class" />
          </template>
        </Button>
      </template>
    </PageHeader>

    <!-- Custom composition using only theme tokens -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-md flex-1 min-h-0">
      <div
        v-for="(item, index) in items"
        :key="item.id"
        class="flex gap-md p-md rounded border border-neutral-base bg-neutral-base hover:bg-neutral-muted transition-colors cursor-pointer"
        :data-test-id="$testId('card', index)"
        @click="emit('select', item)"
      >
        <div class="flex-shrink-0" :data-test-id="$testId('cardIcon', index)">
          <WorkflowIcon class="size-8 text-branding-base" />
        </div>
        <div class="flex flex-col gap-1 flex-1 min-w-0">
          <span class="text-heading-5 text-neutral-base truncate">
            {{ item.name }}
          </span>
          <span class="text-body text-neutral-muted line-clamp-2">
            {{ item.description }}
          </span>
        </div>
      </div>
    </div>

    <div class="flex justify-end pt-md border-t border-neutral-base">
      <Button
        :data-test-id="$testId('secondaryAction')"
        label="View all"
        severity="secondary"
        variant="text"
        @click="emit('viewAll')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { PageHeader } from '@jumpcloud/circuit/components';
import { WorkflowIcon } from '@jumpcloud/icons';
import { PlusIcon } from '@heroicons/vue/24/outline';
import Button from 'primevue/button';

defineOptions({
  name: 'WorkflowsPage',
});

interface Item {
  id: string;
  name: string;
  description: string;
}

defineProps<{
  items: Item[];
}>();

const emit = defineEmits<{
  create: [];
  select: [item: Item];
  viewAll: [];
}>();
</script>
```

**Notes (Gold Standard)**:

- **Layout from library**: `PageHeader` from `@jumpcloud/circuit/components` for title, description, and actions slot.
- **Custom composition**: Card grid and cards are custom markup but use **only** theme tokens: `gap-lg`, `gap-md`, `p-md`, `rounded`, `border-neutral-base`, `bg-neutral-base`, `hover:bg-neutral-muted`, `text-heading-5`, `text-neutral-base`, `text-body`, `text-neutral-muted`, `text-branding-base`.
- **No raw Tailwind colors**: No `bg-blue-500`, `text-gray-700`, etc.
- **Imports**: All from `@jumpcloud/circuit/components`, `primevue/button`, `@jumpcloud/icons`, `@heroicons/vue` — correct for Admin Portal / multi-repo.
- **Test IDs**: On root, page header, each card, and secondary action.

---

## Example 1: Form Field with Input

### Figma Design - Form Field

- Text input field
- Label: "Workflow Name"
- Required indicator (*)
- Help text: "Enter a descriptive name"
- Placeholder: "Enter workflow name"

### Vue Component - Form Field

```vue
<template>
  <FormField
    helpText="Enter a descriptive name"
    label="Workflow Name"
    required
  >
    <template #default="{ inputId }">
      <InputText
        :id="inputId"
        v-model="workflowName"
        class="w-full"
        :data-test-id="$testId('workflowNameInput')"
        placeholder="Enter workflow name"
      />
    </template>
  </FormField>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { FormField } from '@jumpcloud/circuit/components';
import InputText from 'primevue/inputtext';

defineOptions({
  name: 'WorkflowNameField',
});

const workflowName = ref('');
</script>
```

**Notes**:

- Uses Circuit `FormField` component (priority 1)
- Uses PrimeVue `InputText` with Circuit pass-through (priority 2)
- Tailwind utilities only (`w-full`)
- Proper test ID using `$testId`
- FormField slot pattern for input integration

## Example 2: Modal Dialog with Form

### Figma Design - Modal Dialog

- Modal dialog
- Header: "Edit Workflow Details" (heading-3)
- Close button (X icon)
- Form fields: Name (required), Description
- Footer: Cancel button (text variant), Save button (primary)

### Vue Component - Modal Dialog

```vue
<template>
  <Dialog
    :appendTo="containerElement"
    :closable="false"
    :data-test-id="$testId('editWorkflowModal')"
    :draggable="false"
    modal
    :style="{ maxWidth: '42rem' }"
    :visible="visible"
    @update:visible="handleCancel"
  >
    <template #header>
      <div class="flex items-center justify-between w-full">
        <div class="text-heading-3 text-neutral-base">
          Edit Workflow Details
        </div>
        <Button
          aria-label="Close edit modal"
          :data-test-id="$testId('closeButton')"
          :disabled="isSaving"
          rounded
          severity="secondary"
          size="small"
          variant="text"
          @click="handleCancel"
        >
          <template #icon="iconProps">
            <XMarkIcon :class="iconProps.class" />
          </template>
        </Button>
      </div>
    </template>

    <template #default>
      <div class="flex flex-col gap-md">
        <FormField
          helpText="Enter a descriptive name for this workflow."
          label="Name"
          required
        >
          <template #default="{ inputId }">
            <InputText
              :id="inputId"
              v-model="localName"
              class="w-full"
              :data-test-id="$testId('nameInput')"
              :disabled="isSaving"
              :invalid="!!nameError"
              placeholder="Enter workflow name"
            />
          </template>
        </FormField>

        <FormField label="Description">
          <template #default="{ inputId }">
            <Textarea
              :id="inputId"
              v-model="localDescription"
              autoResize
              class="w-full"
              :data-test-id="$testId('descriptionInput')"
              :disabled="isSaving"
              placeholder="Enter workflow description"
              rows="3"
            />
          </template>
        </FormField>
      </div>
    </template>

    <template #footer>
      <div class="flex justify-end gap-sm w-full">
        <Button
          :data-test-id="$testId('cancelButton')"
          :disabled="isSaving"
          label="Cancel"
          severity="secondary"
          variant="text"
          @click="handleCancel"
        />
        <Button
          :data-test-id="$testId('saveButton')"
          :disabled="isSaving || !isValid"
          label="Save"
          severity="primary"
          @click="handleSave"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { FormField } from '@jumpcloud/circuit/components';
import { useContainer } from '@jumpcloud/circuit/composables';
import { XMarkIcon } from '@heroicons/vue/24/outline';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';

defineOptions({
  name: 'EditWorkflowModal',
});

interface Props {
  visible: boolean;
  name: string;
  description?: string;
  isSaving?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  description: '',
  isSaving: false,
});

const emit = defineEmits<{
  'update:visible': [value: boolean];
  cancel: [];
  save: [data: { name: string; description: string }];
}>();

const { containerElement } = useContainer();

const localName = ref(props.name);
const localDescription = ref(props.description);
const nameError = ref('');

watch(
  () => props.name,
  (newName) => {
    localName.value = newName;
  }
);

watch(
  () => props.description,
  (newDesc) => {
    localDescription.value = newDesc ?? '';
  }
);

const isValid = computed(() => {
  return localName.value.trim().length > 0;
});

const handleCancel = () => {
  emit('update:visible', false);
  emit('cancel');
};

const handleSave = () => {
  if (!isValid.value) {
    nameError.value = 'Name is required';
    return;
  }

  nameError.value = '';
  emit('save', {
    name: localName.value.trim(),
    description: localDescription.value.trim(),
  });
};
</script>
```

**Notes**:

- Uses PrimeVue `Dialog` with Circuit pass-through (priority 2)
- Uses Circuit `FormField` for form fields (priority 1)
- Uses PrimeVue `Button` with Circuit pass-through (priority 2)
- Uses `@heroicons/vue` for XMarkIcon (general icon)
- Tailwind utilities only: `flex`, `flex-col`, `gap-md`, `gap-sm`,
  `w-full`, `text-heading-3`, `text-neutral-base`, `justify-end`,
  `items-center`, `justify-between`
- Proper test IDs on all interactive elements
- Uses `useContainer` composable for Dialog mounting

## Example 3: Custom Component (Last Resort)

### Figma Design - Custom Card

- Custom card layout
- Icon on left
- Title and description on right
- Hover effect
- Clickable

### Vue Component - Custom Card

```vue
<template>
  <div
    class="flex gap-md p-md rounded border border-neutral-base bg-neutral-base hover:bg-neutral-muted cursor-pointer transition-colors"
    :data-test-id="$testId('root')"
    @click="handleClick"
  >
    <div class="flex-shrink-0" :data-test-id="$testId('icon')">
      <slot name="icon">
        <WorkflowIcon class="size-6 text-branding-base" />
      </slot>
    </div>
    <div class="flex flex-col gap-1 flex-1" :data-test-id="$testId('content')">
      <div class="text-heading-4 text-neutral-base" :data-test-id="$testId('title')">
        <slot name="title">{{ title }}</slot>
      </div>
      <div class="text-sm text-neutral-muted" :data-test-id="$testId('description')">
        <slot name="description">{{ description }}</slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { WorkflowIcon } from '@jumpcloud/icons';

defineOptions({
  name: 'CustomCard',
});

interface Props {
  title?: string;
  description?: string;
}

withDefaults(defineProps<Props>(), {
  title: '',
  description: '',
});

const emit = defineEmits<{
  click: [];
}>();

const handleClick = () => {
  emit('click');
};
</script>
```

**Notes**:

- Custom component created in app (priority 3 - last resort)
- Uses `@jumpcloud/icons` for WorkflowIcon (JumpCloud-specific icon)
- **Tailwind utilities only** - no `<style>` block
- Uses Circuit tokens: `gap-md`, `p-md`, `border-neutral-base`,
  `bg-neutral-base`, `bg-neutral-muted`, `text-heading-4`,
  `text-neutral-base`, `text-sm`, `text-neutral-muted`, `text-branding-base`
- Proper test IDs
- Slots for flexibility

## Example 4: Button with Icon

### Figma Design - Button

- Primary button
- Icon on left
- Label text
- Hover and active states

### Vue Component

```vue
<template>
  <Button
    :data-test-id="$testId('button')"
    label="Create Workflow"
    severity="primary"
    @click="handleClick"
  >
    <template #icon="iconProps">
      <PlusIcon :class="iconProps.class" />
    </template>
  </Button>
</template>

<script setup lang="ts">
import { PlusIcon } from '@heroicons/vue/24/outline';
import Button from 'primevue/button';

defineOptions({
  name: 'CreateWorkflowButton',
});

const emit = defineEmits<{
  click: [];
}>();

const handleClick = () => {
  emit('click');
};
</script>
```

**Notes**:

- Uses PrimeVue `Button` with Circuit pass-through (priority 2)
- Uses `@heroicons/vue` for PlusIcon (general icon)
- PrimeVue icon slot pattern
- Tailwind utilities handled by Circuit pass-through

## Key Patterns

1. **Import paths**: Use `@jumpcloud/circuit/components` and `@jumpcloud/circuit/composables` when the app depends on `@jumpcloud/circuit` (node_modules or workspace). PrimeVue: `primevue/button`, `primevue/dialog`, etc.
2. **Component Priority**: Always try Circuit → PrimeVue → Custom (last resort). Inventory Figma and map to library components before coding.
3. **Theming**: Use Custom Theme Tokens only (e.g. `bg-button-primary-base`, `text-neutral-base`). Avoid standard Tailwind colors like `bg-blue-500`.
4. **Tailwind Only**: Never use custom CSS unless absolutely necessary.
5. **Test IDs**: Use `$testId` helper on all interactive elements.
6. **Icons**: `@jumpcloud/icons` for JumpCloud-specific, `@heroicons/vue` for general.
7. **Tokens**: Use Circuit Tailwind tokens for spacing, typography, and colors (see reference.md).
8. **Slots**: Use FormField slot pattern for inputs, PrimeVue icon slots for icons.
