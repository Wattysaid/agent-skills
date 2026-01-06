<script setup lang="ts">
import { ref } from "vue";

const props = withDefaults(
  defineProps<{ text?: string }>(),
  {
    text: "",
  }
);

const open = ref(false);
</script>

<template>
  <span class="relative inline-flex" @mouseenter="open = true" @mouseleave="open = false">
    <slot />
    <span
      v-if="open"
      class="absolute left-1/2 top-full z-10 mt-2 -translate-x-1/2 rounded bg-black px-2 py-1 text-xs text-white"
    >
      <slot name="content">{{ props.text }}</slot>
    </span>
  </span>
</template>
