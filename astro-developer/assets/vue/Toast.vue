<script setup lang="ts">
import { computed, ref } from "vue";

type ToastItem = {
  id: string;
  title?: string;
  description?: string;
};

const props = withDefaults(
  defineProps<{
    items?: ToastItem[];
    duration?: number;
  }>(),
  {
    items: () => [],
    duration: 3000,
  }
);

const active = ref(props.items);

const remove = (id: string) => {
  active.value = active.value.filter((item) => item.id !== id);
};

const items = computed(() => active.value);

const scheduleRemoval = (id: string) => {
  setTimeout(() => remove(id), props.duration);
};

items.value.forEach((item) => scheduleRemoval(item.id));
</script>

<template>
  <div class="fixed right-4 top-4 z-50 space-y-2">
    <div
      v-for="item in items"
      :key="item.id"
      class="rounded-md border border-gray-200 bg-white px-4 py-3 shadow"
    >
      <div class="flex items-start justify-between gap-3">
        <div>
          <p v-if="item.title" class="text-sm font-semibold">{{ item.title }}</p>
          <p v-if="item.description" class="text-sm text-gray-600">
            {{ item.description }}
          </p>
        </div>
        <button type="button" class="text-xs text-gray-500" @click="remove(item.id)">
          Close
        </button>
      </div>
    </div>
  </div>
</template>
