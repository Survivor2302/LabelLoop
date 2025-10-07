<template>
  <div
    :class="[
      'relative overflow-hidden rounded-2xl border bg-gradient-to-br from-violet-500/10 via-sky-500/10 to-emerald-500/10 p-8 sm:p-12',
      $attrs.class,
    ]"
  >
    <div class="absolute right-[-6%] top-[-6%] h-40 w-40 rounded-full bg-violet-500/20 blur-2xl" />
    <div
      class="absolute bottom-[-6%] left-[-6%] h-40 w-40 rounded-full bg-emerald-500/20 blur-2xl"
    />
    <div class="relative">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
})
</script>
