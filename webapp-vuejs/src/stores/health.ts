import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface ComponentHealth {
  status: 'ok' | 'error'
  message?: string | null
  latency_ms?: number | null
}

export interface Health {
  status: 'ok' | 'degraded'
  components: Record<string, ComponentHealth>
}

export const useHealthStore = defineStore('health', () => {
  const healthData = ref<Health | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastChecked = ref<Date | null>(null)

  // Computed properties
  const overallStatus = computed(() => {
    if (loading.value) return 'checking'
    if (error.value) return 'error'
    if (!healthData.value) return 'unknown'
    return healthData.value.status
  })

  const overallColor = computed(() => {
    switch (overallStatus.value) {
      case 'checking':
        return 'bg-yellow-500'
      case 'error':
        return 'bg-red-500'
      case 'ok':
        return 'bg-green-500'
      case 'degraded':
        return 'bg-yellow-500'
      default:
        return 'bg-gray-500'
    }
  })

  const overallText = computed(() => {
    switch (overallStatus.value) {
      case 'checking':
        return 'Checking services...'
      case 'error':
        return 'Service unavailable'
      case 'ok':
        return 'All systems operational'
      case 'degraded':
        return 'Service degraded'
      default:
        return 'Unknown status'
    }
  })

  const components = computed(() => {
    if (!healthData.value) return []

    const componentOrder = ['db', 'api', 's3']
    return componentOrder
      .map((key) => ({ key, component: healthData.value?.components?.[key] }))
      .filter(({ component }) => component !== undefined)
  })

  // Actions
  const fetchHealth = async () => {
    loading.value = true
    error.value = null

    try {
      // Try to get API URL from environment or use default
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/health/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        // Add timeout
        signal: AbortSignal.timeout(10000), // 10 second timeout
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data = await response.json()

      // Validate response structure
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid response format')
      }

      healthData.value = data
      lastChecked.value = new Date()
    } catch (err) {
      if (err instanceof Error) {
        if (err.name === 'TimeoutError') {
          error.value = 'Request timeout - service may be unavailable'
        } else if (err.message.includes('Failed to fetch')) {
          error.value = 'Network error - unable to connect to service'
        } else {
          error.value = err.message
        }
      } else {
        error.value = 'Unknown error occurred'
      }
      console.error('Health check failed:', err)
    } finally {
      loading.value = false
    }
  }

  const getComponentDisplayName = (key: string) => {
    const displayNames: Record<string, string> = {
      db: 'Database',
      api: 'API',
      s3: 'S3 Storage',
    }
    return displayNames[key] || key.toUpperCase()
  }

  const getIndicatorColor = (status?: 'ok' | 'error') => {
    if (loading.value) return 'bg-yellow-500 animate-pulse'
    if (error.value) return 'bg-red-500'
    return status === 'ok' ? 'bg-green-500' : 'bg-red-500'
  }

  // Utility functions
  const getLastCheckedText = computed(() => {
    if (!lastChecked.value) return 'Never checked'

    const now = new Date()
    const diff = now.getTime() - lastChecked.value.getTime()
    const seconds = Math.floor(diff / 1000)

    if (seconds < 60) return `${seconds}s ago`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    return `${Math.floor(seconds / 3600)}h ago`
  })

  const resetError = () => {
    error.value = null
  }

  const clearHealthData = () => {
    healthData.value = null
    lastChecked.value = null
    error.value = null
  }

  return {
    // State
    healthData,
    loading,
    error,
    lastChecked,

    // Computed
    overallStatus,
    overallColor,
    overallText,
    components,
    getLastCheckedText,

    // Actions
    fetchHealth,
    getComponentDisplayName,
    getIndicatorColor,
    resetError,
    clearHealthData,
  }
})
