<script lang="ts" setup>
import type { ToasterProps } from 'vue-sonner'
import { Toaster as Sonner } from 'vue-sonner'
import { cn } from '@/lib/utils'

defineOptions({
  name: 'SonnerToaster',
})

interface SonnerToasterProps extends ToasterProps {
  class?: string
}

const props = withDefaults(defineProps<SonnerToasterProps>(), {
  position: 'top-right',
  toastOptions: () => ({
    class: '',
    description: '',
    duration: 4000,
  }),
})
</script>

<template>
  <Sonner
    :class="cn('group toaster', props.class)"
    v-bind="props"
    :toast-options="{
      ...props.toastOptions,
      class: cn(
        'bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700 shadow-lg rounded-lg p-3',
        props.toastOptions?.class,
      ),
    }"
  />
</template>
