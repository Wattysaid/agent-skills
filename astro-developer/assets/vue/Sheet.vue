<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    side?: "left" | "right";
  }>(),
  {
    side: "right",
  }
);

const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
}>();

const close = () => emit("update:modelValue", false);
</script>

<template>
  <div v-if="props.modelValue" class="fixed inset-0 z-40">
    <div class="absolute inset-0 bg-black/40" @click="close" />
    <div
      class="absolute top-0 h-full w-80 bg-white shadow-xl"
      :class="props.side === 'left' ? 'left-0' : 'right-0'"
    >
      <div class="flex items-center justify-between border-b px-4 py-3">
        <slot name="header" />
        <button class="text-sm text-gray-500" type="button" @click="close">Close</button>
      </div>
      <div class="p-4">
        <slot />
      </div>
    </div>
  </div>
</template>
