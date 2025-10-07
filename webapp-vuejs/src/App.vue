<script setup lang="ts">
import { RouterView } from 'vue-router'
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Navigation -->
    <!-- <nav
      class="sticky top-0 z-50 border-b bg-background/95 backdrop-blur-md supports-[backdrop-filter]:bg-background/80 shadow-sm"
    >
      <div class="mx-auto px-6">
        <div class="flex h-16 items-center justify-between">
          <div class="flex items-center gap-6">
            <RouterLink to="/" class="flex items-center gap-2">
              <div class="h-8 w-8 rounded-lg bg-gradient-to-br from-emerald-500 to-violet-500" />
              <span class="text-xl font-bold">LabelLoop</span>
            </RouterLink>
          </div>

          <div class="hidden items-center gap-4 md:flex">
            <RouterLink
              to="/"
              class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              active-class="text-primary"
            >
              Home
            </RouterLink>
            <RouterLink
              to="/dashboard"
              class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              active-class="text-primary"
            >
              Dashboard
            </RouterLink>
            <RouterLink
              to="/datasets"
              class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              active-class="text-primary"
            >
              Datasets
            </RouterLink>
            <RouterLink
              to="/about"
              class="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
              active-class="text-primary"
            >
              About
            </RouterLink>
          </div>

          <button class="md:hidden p-2">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </nav> -->

    <!-- Main content -->
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>

    <!-- Toast notifications -->
    <Toaster />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
/* Sonner toast styles */
[data-sonner-toaster] {
  position: fixed;
  z-index: 9999;
  top: 1rem;
  right: 1rem;
  pointer-events: none;
}

[data-sonner-toast] {
  pointer-events: auto;
  margin-bottom: 0.5rem;
}

[data-sonner-toast] {
  background: white !important;
  color: #111827 !important;
  border: 2px solid #e5e7eb !important;
  border-radius: 0.5rem !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  padding: 0.75rem 1rem !important;
  opacity: 1 !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}

[data-sonner-toast] [data-icon] {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

[data-sonner-toast] [data-content] {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.25rem !important;
  flex: 1 !important;
}

/* Success toast - Green border */
[data-sonner-toast][data-type='success'] {
  border-color: #10b981 !important;
}

/* Error toast - Red border */
[data-sonner-toast][data-type='error'] {
  border-color: #ef4444 !important;
}

/* Info toast - Blue border */
[data-sonner-toast][data-type='info'] {
  border-color: #3b82f6 !important;
}

/* Warning toast - Yellow border */
[data-sonner-toast][data-type='warning'] {
  border-color: #f59e0b !important;
}

.dark [data-sonner-toast] {
  background: #111827 !important;
  color: #f9fafb !important;
  border: 2px solid #374151 !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}

.dark [data-sonner-toast] [data-icon] {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

.dark [data-sonner-toast] [data-content] {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.25rem !important;
  flex: 1 !important;
}

/* Dark mode success */
.dark [data-sonner-toast][data-type='success'] {
  border-color: #059669 !important;
}

/* Dark mode error */
.dark [data-sonner-toast][data-type='error'] {
  border-color: #dc2626 !important;
}

/* Dark mode info */
.dark [data-sonner-toast][data-type='info'] {
  border-color: #2563eb !important;
}

/* Dark mode warning */
.dark [data-sonner-toast][data-type='warning'] {
  border-color: #d97706 !important;
}
</style>
