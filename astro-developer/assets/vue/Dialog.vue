<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    title?: string;
  }>(),
  {
    title: "",
  }
);

const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
}>();

const close = () => emit("update:modelValue", false);
</script>

<template>
  <div v-if="props.modelValue" class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0 bg-black/40" @click="close" />
    <div class="relative z-10 w-full max-w-lg rounded-lg bg-white p-6 shadow-lg">
      <div class="flex items-start justify-between">
        <h2 class="text-lg font-semibold" v-if="title">{{ title }}</h2>
        <button class="text-sm text-gray-500" type="button" @click="close">Close</button>
      </div>
      <div class="mt-4">
        <slot />
      </div>
    </div>
  </div>
</template>
