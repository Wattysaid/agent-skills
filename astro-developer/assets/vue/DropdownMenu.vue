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
      class="absolute right-0 mt-2 w-48 rounded-md border border-gray-200 bg-white shadow-lg"
    >
      <div class="py-2" @click="close">
        <slot name="content" />
      </div>
    </div>
  </div>
</template>
