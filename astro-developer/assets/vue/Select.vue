<script setup lang="ts">
import { ref, watch } from "vue";

type SelectOption = {
  label: string;
  value: string;
};

const props = withDefaults(
  defineProps<{
    options?: SelectOption[];
    modelValue?: string | null;
    placeholder?: string;
  }>(),
  {
    options: () => [],
    modelValue: null,
    placeholder: "Select an option",
  }
);

const emit = defineEmits<{
  (event: "update:modelValue", value: string): void;
}>();

const value = ref(props.modelValue ?? "");

watch(
  () => props.modelValue,
  (next) => {
    if (next !== undefined && next !== null) value.value = next;
  }
);

const onChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  value.value = target.value;
  emit("update:modelValue", target.value);
};
</script>

<template>
  <select
    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
    :value="value"
    @change="onChange"
  >
    <option disabled value="">{{ placeholder }}</option>
    <option v-for="option in options" :key="option.value" :value="option.value">
      {{ option.label }}
    </option>
  </select>
</template>
