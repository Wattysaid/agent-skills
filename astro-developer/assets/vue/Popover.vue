<script setup lang="ts">
import { ref } from "vue";

const open = ref(false);

const toggle = () => {
  open.value = !open.value;
};

const close = () => {
  open.value = false;
};
</script>

<template>
  <div class="relative inline-block" @keydown.esc="close">
    <div @click="toggle">
      <slot name="trigger" />
    </div>
    <div
      v-if="open"
      class="absolute z-10 mt-2 w-64 rounded-md border border-gray-200 bg-white p-3 shadow-lg"
    >
      <slot name="content" />
    </div>
  </div>
</template>
