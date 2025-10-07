<template>
  <div class="space-y-1">
    <div class="flex items-center gap-2">
      <span class="text-2xl font-bold">{{ value }}</span>
      <div v-if="trend" class="flex items-center gap-1 text-xs" :class="trendClasses">
        <svg v-if="trend === 'up'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          />
        </svg>
        <svg v-else-if="trend === 'down'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </div>
    <p class="text-xs text-muted-foreground">{{ label }}</p>
  </div>
</template>

<script setup lang="ts" name="StatCard">
import { computed } from 'vue'

interface Props {
  label: string
  value: string
  trend?: 'up' | 'down'
}

const props = defineProps<Props>()

const trendClasses = computed(() => {
  if (props.trend === 'up') {
    return 'text-emerald-600 dark:text-emerald-400'
  } else if (props.trend === 'down') {
    return 'text-red-600 dark:text-red-400'
  }
  return ''
})
</script>
