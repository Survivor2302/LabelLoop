<template>
  <div
    class="group relative rounded-xl border bg-card p-6 shadow-sm transition-all duration-200 hover:shadow-md"
  >
    <!-- Color accent -->
    <div class="absolute top-0 left-0 w-full h-1 rounded-t-xl" :class="colorClasses" />

    <div class="space-y-3">
      <h3 class="text-lg font-semibold group-hover:text-primary transition-colors">
        {{ title }}
      </h3>
      <p class="text-sm text-muted-foreground leading-relaxed">
        {{ desc }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  desc: string
  color: 'emerald' | 'violet' | 'sky' | 'amber' | 'rose' | 'slate'
}

const props = defineProps<Props>()

const colorClasses = computed(() => {
  const colors = {
    emerald: 'bg-gradient-to-r from-emerald-500 to-emerald-600',
    violet: 'bg-gradient-to-r from-violet-500 to-violet-600',
    sky: 'bg-gradient-to-r from-sky-500 to-sky-600',
    amber: 'bg-gradient-to-r from-amber-500 to-amber-600',
    rose: 'bg-gradient-to-r from-rose-500 to-rose-600',
    slate: 'bg-gradient-to-r from-slate-500 to-slate-600',
  }
  return colors[props.color]
})
</script>
