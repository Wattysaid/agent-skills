<script setup lang="ts">
import { ref, watch } from "vue";

type TabItem = {
  id: string;
  label: string;
};

const props = withDefaults(
  defineProps<{
    tabs?: TabItem[];
    defaultTabId?: string | null;
  }>(),
  {
    tabs: () => [],
    defaultTabId: null,
  }
);

const activeId = ref<string | null>(props.defaultTabId ?? props.tabs[0]?.id ?? null);

watch(
  () => props.tabs,
  (tabs) => {
    if (!tabs.length) return;
    if (!activeId.value || !tabs.find((tab) => tab.id === activeId.value)) {
      activeId.value = props.defaultTabId ?? tabs[0]?.id ?? null;
    }
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <div class="flex flex-wrap gap-2 border-b border-gray-200">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="px-4 py-2 text-sm"
        :class="activeId === tab.id ? 'border-b-2 border-black font-medium' : 'text-gray-500'"
        @click="activeId = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="pt-4">
      <slot v-if="activeId" :name="activeId" />
    </div>
  </div>
</template>
