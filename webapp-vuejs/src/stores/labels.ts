import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Label {
  id: number
  name: string
}

export interface LabelCreate {
  name: string
}

export interface LabelListResponse {
  total: number
  items: Label[]
}

export interface LabelSearchParams {
  skip?: number
  limit?: number
  search?: string
}

export const useLabelsStore = defineStore('labels', () => {
  const labels = ref<Label[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastFetched = ref<Date | null>(null)
  const total = ref(0)
  const skip = ref(0)
  const limit = ref(100)

  // Computed properties
  const hasLabels = computed(() => labels.value.length > 0)

  // Actions
  const fetchLabels = async (params?: LabelSearchParams) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.search) queryParams.append('search', params.search)

      const response = await fetch(`${apiUrl}/labels/?${queryParams.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data: LabelListResponse = await response.json()
      labels.value = data.items
      total.value = data.total

      lastFetched.value = new Date()
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
      console.error('Fetch labels failed:', err)
    } finally {
      loading.value = false
    }
  }

  const createLabel = async (labelData: LabelCreate) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/labels/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(labelData),
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const newLabel = await response.json()
      labels.value.unshift(newLabel) // Add to beginning of list
      total.value += 1
      lastFetched.value = new Date()

      return newLabel
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
      console.error('Create label failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteLabel = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/labels/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      // Remove from local state
      const index = labels.value.findIndex((l) => l.id === id)
      if (index !== -1) {
        labels.value.splice(index, 1)
        total.value = Math.max(0, total.value - 1)
      }

      lastFetched.value = new Date()
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
      console.error('Delete label failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Utility functions
  const getLastFetchedText = computed(() => {
    if (!lastFetched.value) return 'Never fetched'

    const now = new Date()
    const diff = now.getTime() - lastFetched.value.getTime()
    const seconds = Math.floor(diff / 1000)

    if (seconds < 60) return `${seconds}s ago`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    return `${Math.floor(seconds / 3600)}h ago`
  })

  const resetError = () => {
    error.value = null
  }

  const clearLabels = () => {
    labels.value = []
    total.value = 0
    lastFetched.value = null
    error.value = null
  }

  // Search helpers
  const searchLabels = async (searchTerm: string) => {
    return await fetchLabels({ search: searchTerm })
  }

  const getLabelsWithFilters = async (filters: LabelSearchParams) => {
    return await fetchLabels(filters)
  }

  return {
    // State
    labels,
    loading,
    error,
    lastFetched,
    total,
    skip,
    limit,

    // Computed
    hasLabels,
    getLastFetchedText,

    // Actions
    fetchLabels,
    createLabel,
    deleteLabel,
    resetError,
    clearLabels,

    // Search helpers
    searchLabels,
    getLabelsWithFilters,
  }
})
