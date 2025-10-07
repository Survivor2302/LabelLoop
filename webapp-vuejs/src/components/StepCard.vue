<template>
  <li class="relative rounded-xl border bg-card p-6 shadow-sm hover:shadow-md transition-shadow">
    <span
      class="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg border bg-muted/50 text-sm font-semibold text-foreground"
    >
      {{ step }}
    </span>
    <h4 class="text-base font-semibold mb-2">{{ title }}</h4>
    <p class="text-sm text-muted-foreground leading-relaxed">
      {{ desc }}
    </p>
  </li>
</template>

<script setup lang="ts">
interface Props {
  step: string
  title: string
  desc: string
}

defineProps<Props>()
</script>
