<template>
  <div class="absolute inset-0 overflow-hidden pointer-events-none">
    <!-- Gradient orbs -->
    <div
      class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-emerald-400/20 to-transparent rounded-full blur-3xl"
    />
    <div
      class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-violet-400/20 to-transparent rounded-full blur-3xl"
    />
    <div
      class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-sky-400/10 to-emerald-400/10 rounded-full blur-3xl"
    />

    <!-- Grid pattern -->
    <div class="absolute inset-0 bg-grid-pattern opacity-5" />
  </div>
</template>

<style scoped>
.bg-grid-pattern {
  background-image:
    linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}
</style>
