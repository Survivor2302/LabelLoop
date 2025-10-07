<template>
  <main
    class="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30"
  >
    <!-- Decorative background effects -->
    <GradientBackground />

    <div class="px-6 py-16 grid gap-y-12">
      <!-- Header -->
      <GradientCard class="mb-16">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">System Health Dashboard</h1>
            <p class="mt-2 text-muted-foreground">
              Monitor API, database, and S3 storage status in real-time
            </p>
          </div>
          <RouterLink to="/">
            <Button variant="outline" size="lg"> ← Back to Home </Button>
          </RouterLink>
        </div>
      </GradientCard>

      <!-- Health Status Card -->
      <div class="rounded-xl border bg-card shadow-sm mb-12">
        <div class="p-8 border-b">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-3 h-3 rounded-full animate-pulse" :class="healthStore.overallColor" />
              <h2 class="text-xl font-semibold">{{ healthStore.overallText }}</h2>
            </div>
            <div class="flex items-center gap-3">
              <div class="text-sm text-muted-foreground">
                Next check in
                <span class="font-mono font-medium text-blue-600 dark:text-blue-400">
                  {{ timeUntilRefresh }}s
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                @click="handleRefresh"
                :disabled="healthStore.loading"
              >
                {{ healthStore.loading ? 'Checking...' : 'Refresh' }}
              </Button>
            </div>
          </div>
        </div>

        <div class="p-8">
          <!-- Error display -->
          <div
            v-if="healthStore.error"
            class="mb-8 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20"
          >
            <div class="flex items-center gap-2">
              <div class="h-2 w-2 rounded-full bg-red-500" />
              <span class="text-sm font-medium text-red-600 dark:text-red-400">
                Connection Error
              </span>
            </div>
            <p class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ healthStore.error }}
            </p>
            <div class="mt-3">
              <Button
                variant="outline"
                size="sm"
                @click="healthStore.resetError"
                class="text-red-600 border-red-200 hover:bg-red-50 dark:text-red-400 dark:border-red-800 dark:hover:bg-red-900/20"
              >
                Dismiss Error
              </Button>
            </div>
          </div>

          <!-- Components accordion -->
          <Accordion type="single" collapsible default-value="components" class="w-full">
            <AccordionItem value="components" class="border-0">
              <AccordionTrigger class="px-0 py-4 hover:no-underline">
                <div class="flex items-center justify-between w-full">
                  <div class="flex items-center gap-3">
                    <div class="w-3 h-3 rounded-full" :class="healthStore.overallColor" />
                    <span class="font-medium">Service Components</span>
                  </div>
                  <div v-if="healthStore.healthData">
                    <span
                      v-if="healthStore.healthData.status === 'ok'"
                      class="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
                    >
                      All Healthy
                    </span>
                    <span
                      v-else
                      class="px-2 py-0.5 rounded-full text-xs bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300"
                    >
                      Issues Detected
                    </span>
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent class="px-0 pb-6">
                <div class="pt-2 divide-y divide-border">
                  <div
                    v-for="{ key, component } in healthStore.components"
                    :key="key"
                    class="group"
                  >
                    <div class="flex items-center justify-between gap-4 py-3 pl-6">
                      <div class="flex items-center gap-3 min-w-0">
                        <div
                          class="w-2.5 h-2.5 rounded-full"
                          :class="healthStore.getIndicatorColor(component?.status)"
                        />
                        <div class="flex flex-col">
                          <span class="text-sm font-medium">
                            {{ healthStore.getComponentDisplayName(key) }}
                          </span>
                          <div class="text-xs text-muted-foreground flex items-center gap-3">
                            <span
                              v-if="typeof component?.latency_ms === 'number'"
                              class="flex items-center gap-1"
                            >
                              <span class="h-1 w-1 rounded-full bg-muted-foreground" />
                              {{ component.latency_ms.toFixed(0) }}ms
                            </span>
                            <span v-if="component?.message" class="truncate max-w-xs">
                              {{ component.message }}
                            </span>
                          </div>
                        </div>
                      </div>
                      <StatusBadge :status="component?.status" />
                    </div>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="rounded-xl border bg-card p-8 shadow-sm">
        <h3 class="text-lg font-semibold mb-4">About This Dashboard</h3>
        <p class="text-sm text-muted-foreground">
          This dashboard monitors the health of LabelLoop's core infrastructure components. The
          system automatically checks API endpoints, database connectivity, and S3 storage
          availability every 30 seconds to ensure optimal performance for your labeling workflows.
        </p>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useHealthStore } from '@/stores/health'
import { GradientBackground, GradientCard, StatusBadge } from '@/components'
import { Button } from '@/components/ui/button'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { RouterLink } from 'vue-router'

const healthStore = useHealthStore()
const timeUntilRefresh = ref(30)

let refreshInterval: number | null = null
let countdownTimer: number | null = null

// Auto-refetch every 30 seconds
const startAutoRefresh = () => {
  refreshInterval = setInterval(() => {
    healthStore.fetchHealth()
    timeUntilRefresh.value = 30
  }, 30000)
}

// Countdown timer
const startCountdown = () => {
  countdownTimer = setInterval(() => {
    if (timeUntilRefresh.value <= 1) {
      timeUntilRefresh.value = 30 // Reset to 30 when it reaches 0
    } else {
      timeUntilRefresh.value -= 1
    }
  }, 1000)
}

const handleRefresh = () => {
  healthStore.fetchHealth()
  timeUntilRefresh.value = 30
}

onMounted(() => {
  // Initial fetch
  healthStore.fetchHealth()

  // Start auto-refresh and countdown
  startAutoRefresh()
  startCountdown()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>
