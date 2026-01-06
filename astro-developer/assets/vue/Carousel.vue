<script setup lang="ts">
import { computed, ref } from "vue";

const props = withDefaults(
  defineProps<{
    startIndex?: number;
  }>(),
  {
    startIndex: 0,
  }
);

const current = ref(props.startIndex);

const slots = defineSlots<{
  default?: () => any[];
}>();

const slides = computed(() => slots.default?.() ?? []);

const next = () => {
  if (!slides.value.length) return;
  current.value = (current.value + 1) % slides.value.length;
};

const prev = () => {
  if (!slides.value.length) return;
  current.value = (current.value - 1 + slides.value.length) % slides.value.length;
};
</script>

<template>
  <div class="relative">
    <div class="overflow-hidden">
      <component :is="slides[current]" v-if="slides.length" />
    </div>
    <div class="mt-3 flex items-center gap-2">
      <button type="button" class="rounded border px-3 py-1 text-sm" @click="prev">Prev</button>
      <button type="button" class="rounded border px-3 py-1 text-sm" @click="next">Next</button>
    </div>
  </div>
</template>
