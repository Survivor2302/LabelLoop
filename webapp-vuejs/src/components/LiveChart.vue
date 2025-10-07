<template>
  <div class="relative h-60 w-full">
    <!-- Chart background -->
    <div class="absolute inset-0 bg-muted/30 rounded-lg" />

    <!-- Mock chart line -->
    <svg class="absolute inset-0 w-full h-full" viewBox="0 0 200 100">
      <defs>
        <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color: rgb(16, 185, 129); stop-opacity: 0.3" />
          <stop offset="100%" style="stop-color: rgb(16, 185, 129); stop-opacity: 0" />
        </linearGradient>
      </defs>

      <!-- Area under curve -->
      <path
        d="M0,80 Q25,60 50,45 T100,35 T150,25 T200,20 L200,100 L0,100 Z"
        fill="url(#chartGradient)"
        class="animate-pulse"
      />

      <!-- Line -->
      <path
        d="M0,80 Q25,60 50,45 T100,35 T150,25 T200,20"
        fill="none"
        stroke="rgb(16,185,129)"
        stroke-width="2"
        class="animate-pulse"
      />

      <!-- Data points -->
      <circle cx="25" cy="60" r="2" fill="rgb(16,185,129)" class="animate-pulse" />
      <circle cx="50" cy="45" r="2" fill="rgb(16,185,129)" class="animate-pulse" />
      <circle cx="100" cy="35" r="2" fill="rgb(16,185,129)" class="animate-pulse" />
      <circle cx="150" cy="25" r="2" fill="rgb(16,185,129)" class="animate-pulse" />
      <circle cx="200" cy="20" r="2" fill="rgb(16,185,129)" class="animate-pulse" />
    </svg>

    <!-- Animated overlay -->
    <div
      class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-pulse"
    />
  </div>
</template>

<script setup lang="ts">
// Mock live chart component - in a real app this would connect to real data
</script>
