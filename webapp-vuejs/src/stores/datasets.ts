import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useLabelsStore } from './labels'

export interface Dataset {
  id: number
  name: string
  description?: string | null
  created_at: string
  updated_at: string
  image_count: number
}

export interface DatasetDetail {
  id: number
  name: string
  description?: string | null
  created_at: string
  updated_at: string
  image_count: number
  annotation_count: number
  label_count: number
}

export interface DatasetCreate {
  name: string
  description?: string | null
  label_names?: string[]
}

export interface DatasetUpdate {
  name?: string
  description?: string | null
}

export interface DatasetsResponse {
  datasets: Dataset[]
  total: number
  skip: number
  limit: number
}

export interface DatasetSearchParams {
  skip?: number
  limit?: number
  search?: string
  label_name?: string
  sort_by?: 'id' | 'name' | 'created_at' | 'image_count'
  sort_order?: 'asc' | 'desc'
}

export const useDatasetsStore = defineStore('datasets', () => {
  const datasets = ref<Dataset[]>([])
  const currentDataset = ref<DatasetDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastFetched = ref<Date | null>(null)
  const total = ref(0)
  const skip = ref(0)
  const limit = ref(100)

  // Get labels store instance
  const labelsStore = useLabelsStore()

  // Computed properties
  const hasDatasets = computed(() => datasets.value.length > 0)

  // Actions
  const fetchDatasets = async (params?: DatasetSearchParams) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.search) queryParams.append('search', params.search)
      if (params?.label_name) queryParams.append('label_name', params.label_name)
      if (params?.sort_by) queryParams.append('sort_by', params.sort_by)
      if (params?.sort_order) queryParams.append('sort_order', params.sort_order)

      const response = await fetch(`${apiUrl}/datasets/?${queryParams.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data = await response.json()

      // Handle both array response and paginated response
      if (Array.isArray(data)) {
        datasets.value = data
        total.value = data.length
      } else if (data.datasets) {
        datasets.value = data.datasets
        total.value = data.total || data.datasets.length
      } else {
        throw new Error('Invalid response format')
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
      console.error('Fetch datasets failed:', err)
    } finally {
      loading.value = false
    }
  }

  const createDataset = async (datasetData: DatasetCreate) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/datasets/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(datasetData),
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const newDataset = await response.json()
      datasets.value.unshift(newDataset) // Add to beginning of list
      total.value += 1
      lastFetched.value = new Date()

      // If the dataset has labels, refresh the labels store to include any new ones
      if (datasetData.label_names && datasetData.label_names.length > 0) {
        await labelsStore.fetchLabels()
      }

      return newDataset
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
      console.error('Create dataset failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateDataset = async (id: number, datasetData: DatasetUpdate) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/datasets/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(datasetData),
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const updatedDataset = await response.json()
      const index = datasets.value.findIndex((d) => d.id === id)
      if (index !== -1) {
        datasets.value[index] = updatedDataset
      }

      lastFetched.value = new Date()
      return updatedDataset
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
      console.error('Update dataset failed:', err)
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

  const deleteDataset = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/datasets/${id}`, {
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
      const index = datasets.value.findIndex((d) => d.id === id)
      if (index !== -1) {
        datasets.value.splice(index, 1)
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
      console.error('Delete dataset failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearDatasets = () => {
    datasets.value = []
    total.value = 0
    lastFetched.value = null
    error.value = null
  }

  // Search and filter helpers
  const searchDatasets = async (searchTerm: string) => {
    return await fetchDatasets({ search: searchTerm })
  }

  const filterByLabel = async (labelName: string) => {
    return await fetchDatasets({ label_name: labelName })
  }

  const sortDatasets = async (
    sortBy: 'id' | 'name' | 'created_at' | 'image_count',
    order: 'asc' | 'desc' = 'asc',
  ) => {
    return await fetchDatasets({ sort_by: sortBy, sort_order: order })
  }

  const getDatasetsWithFilters = async (filters: DatasetSearchParams) => {
    return await fetchDatasets(filters)
  }

  const getDataset = async (id: number) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/datasets/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Dataset not found')
        }
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const datasetDetail = await response.json()
      currentDataset.value = datasetDetail
      lastFetched.value = new Date()

      return datasetDetail
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
      console.error('Get dataset failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    datasets,
    currentDataset,
    loading,
    error,
    lastFetched,
    total,
    skip,
    limit,

    // Computed
    hasDatasets,
    getLastFetchedText,

    // Actions
    fetchDatasets,
    getDataset,
    createDataset,
    updateDataset,
    deleteDataset,
    resetError,
    clearDatasets,

    // Search and filter helpers
    searchDatasets,
    filterByLabel,
    sortDatasets,
    getDatasetsWithFilters,
  }
})
