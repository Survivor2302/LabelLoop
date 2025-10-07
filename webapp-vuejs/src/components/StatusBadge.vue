<template>
  <span
    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
    :class="statusClasses"
  >
    <div class="w-1.5 h-1.5 rounded-full mr-1.5" :class="indicatorClasses" />
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  status?: 'ok' | 'error'
}

const props = defineProps<Props>()

const statusText = computed(() => {
  return props.status === 'ok' ? 'Healthy' : 'Error'
})

const statusClasses = computed(() => {
  if (props.status === 'ok') {
    return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
  } else {
    return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
  }
})

const indicatorClasses = computed(() => {
  return props.status === 'ok' ? 'bg-green-500' : 'bg-red-500'
})
</script>
