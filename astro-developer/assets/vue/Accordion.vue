<script setup lang="ts">
import { ref } from "vue";

type AccordionItem = {
  id: string;
  title: string;
  content?: string;
};

const props = withDefaults(
  defineProps<{
    items?: AccordionItem[];
    defaultOpenId?: string | null;
  }>(),
  {
    items: () => [],
    defaultOpenId: null,
  }
);

const openId = ref<string | null>(props.defaultOpenId ?? null);

const toggle = (id: string) => {
  openId.value = openId.value === id ? null : id;
};
</script>

<template>
  <div class="divide-y divide-gray-200">
    <div v-for="item in items" :key="item.id" class="py-4">
      <button
        class="flex w-full items-center justify-between text-left font-medium"
        type="button"
        @click="toggle(item.id)"
      >
        <span>{{ item.title }}</span>
        <span class="text-sm" aria-hidden="true">{{ openId === item.id ? "−" : "+" }}</span>
      </button>
      <div v-if="openId === item.id" class="pt-3 text-sm text-gray-600">
        <slot :name="item.id">
          {{ item.content }}
        </slot>
      </div>
    </div>
  </div>
</template>
