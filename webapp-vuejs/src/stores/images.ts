import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Image {
  id: number
  filename: string
  s3_key: string
  file_size: number
  mime_type: string
  width?: number | null
  height?: number | null
  status: 'uploading' | 'uploaded' | 'error'
  dataset_id: number
  created_at: string
  updated_at: string
  download_url?: string | null
  url_expires_in?: number | null
}

export interface ImageWithUrl extends Image {
  download_url: string
  url_expires_in: number
}

export interface PrepareUploadRequest {
  files: {
    filename: string
    file_size: number
    mime_type: string
  }[]
}

export interface PrepareUploadResponse {
  uploads: {
    image_id: number
    upload_url: string
    s3_key: string
    expires_in: number
  }[]
}

export interface ConfirmUploadRequest {
  image_ids: number[]
}

export interface ConfirmUploadResponse {
  message: string
  updated_count: number
  total_requested: number
}

export interface ImageSearchParams {
  skip?: number
  limit?: number
  status?: 'uploading' | 'uploaded' | 'error'
  expires_in?: number
}

export interface ImagesWithUrlsResponse {
  total: number
  items: Image[]
}

export const useImagesStore = defineStore('images', () => {
  const images = ref<Image[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastFetched = ref<Date | null>(null)
  const total = ref(0)
  const skip = ref(0)
  const limit = ref(100) // 100 images per page
  const currentPage = ref(1)
  const pageSize = ref(100) // 100 images per page (5 per row × 20 rows)

  // Computed properties
  const hasImages = computed(() => images.value.length > 0)

  const imagesByStatus = computed(() => {
    const grouped: Record<string, Image[]> = {
      uploading: [],
      uploaded: [],
      error: [],
    }

    images.value.forEach((image) => {
      const statusArray = grouped[image.status]
      if (statusArray) {
        statusArray.push(image)
      }
    })

    return grouped
  })

  const statusCounts = computed(() => {
    return {
      uploading: imagesByStatus.value.uploading?.length || 0,
      uploaded: imagesByStatus.value.uploaded?.length || 0,
      error: imagesByStatus.value.error?.length || 0,
      total: images.value.length,
    }
  })

  // Actions
  const fetchImages = async (datasetId: number, params?: ImageSearchParams) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.status) queryParams.append('status', params.status)
      if (params?.expires_in) queryParams.append('expires_in', params.expires_in.toString())

      const response = await fetch(
        `${apiUrl}/datasets/${datasetId}/images/with-urls?${queryParams.toString()}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: AbortSignal.timeout(10000),
        },
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data: ImagesWithUrlsResponse = await response.json()
      images.value = data.items
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
      console.error('Fetch images failed:', err)
    } finally {
      loading.value = false
    }
  }

  const prepareUpload = async (
    datasetId: number,
    files: File[],
  ): Promise<PrepareUploadResponse> => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const requestData: PrepareUploadRequest = {
        files: files.map((file) => ({
          filename: file.name,
          file_size: file.size,
          mime_type: file.type,
        })),
      }

      const response = await fetch(`${apiUrl}/datasets/${datasetId}/images/prepare-upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
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
      console.error('Prepare upload failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const uploadToS3 = async (file: File, uploadUrl: string): Promise<boolean> => {
    try {
      const response = await fetch(uploadUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type,
        },
      })
      return response.ok
    } catch (err) {
      console.error('Upload to S3 failed:', err)
      return false
    }
  }

  const confirmUpload = async (
    datasetId: number,
    imageIds: number[],
  ): Promise<ConfirmUploadResponse> => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const requestData: ConfirmUploadRequest = {
        image_ids: imageIds,
      }

      const response = await fetch(`${apiUrl}/datasets/${datasetId}/images/confirm-upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        signal: AbortSignal.timeout(10000),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
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
      console.error('Confirm upload failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const uploadImages = async (
    datasetId: number,
    files: File[],
  ): Promise<{ success: number; failed: number }> => {
    try {
      // 1. Prepare upload
      const prepareResponse = await prepareUpload(datasetId, files)

      // 2. Upload files to S3 in parallel
      const uploadResults = await Promise.all(
        prepareResponse.uploads.map(async ({ image_id, upload_url }) => {
          const file = files.find(
            (f) =>
              f.name ===
              prepareResponse.uploads
                .find((u) => u.image_id === image_id)
                ?.s3_key.split('_')
                .pop(),
          )
          if (!file) return { image_id, success: false }

          const success = await uploadToS3(file, upload_url)
          return { image_id, success }
        }),
      )

      // 3. Filter successful uploads
      const successfulIds = uploadResults
        .filter((result) => result.success)
        .map((result) => result.image_id)

      // 4. Confirm successful uploads
      if (successfulIds.length > 0) {
        await confirmUpload(datasetId, successfulIds)
      }

      // 5. Refresh images list
      await fetchImages(datasetId)

      return {
        success: successfulIds.length,
        failed: files.length - successfulIds.length,
      }
    } catch (err) {
      console.error('Upload images failed:', err)
      throw err
    }
  }

  const deleteImage = async (imageId: number) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/images/${imageId}`, {
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
      const index = images.value.findIndex((img) => img.id === imageId)
      if (index !== -1) {
        images.value.splice(index, 1)
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
      console.error('Delete image failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteAllImages = async (datasetId: number) => {
    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/datasets/${datasetId}/images`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(30000), // 30 second timeout for bulk delete
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()

      // Clear local state
      images.value = []
      total.value = 0
      currentPage.value = 1
      lastFetched.value = new Date()

      return result
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
      console.error('Delete all images failed:', err)
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

  const clearImages = () => {
    images.value = []
    total.value = 0
    lastFetched.value = null
    error.value = null
    currentPage.value = 1
  }

  // Page navigation functions
  const goToPage = async (page: number, datasetId: number, params?: ImageSearchParams) => {
    if (page < 1 || page > totalPages.value) return

    currentPage.value = page
    const skip = (page - 1) * pageSize.value

    const pageParams = {
      ...params,
      skip,
      limit: pageSize.value,
    }

    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const queryParams = new URLSearchParams()

      if (pageParams.skip !== undefined) queryParams.append('skip', pageParams.skip.toString())
      if (pageParams.limit !== undefined) queryParams.append('limit', pageParams.limit.toString())
      if (pageParams.status) queryParams.append('status', pageParams.status)
      if (pageParams.expires_in) queryParams.append('expires_in', pageParams.expires_in.toString())

      const response = await fetch(
        `${apiUrl}/datasets/${datasetId}/images/with-urls?${queryParams.toString()}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: AbortSignal.timeout(10000),
        },
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data: ImagesWithUrlsResponse = await response.json()
      images.value = data.items
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
      console.error('Go to page failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const goToNextPage = async (datasetId: number, params?: ImageSearchParams) => {
    if (canGoToNextPage.value) {
      await goToPage(currentPage.value + 1, datasetId, params)
    }
  }

  const goToPreviousPage = async (datasetId: number, params?: ImageSearchParams) => {
    if (canGoToPreviousPage.value) {
      await goToPage(currentPage.value - 1, datasetId, params)
    }
  }

  // Pagination helpers
  const loadMoreImages = async (datasetId: number, params?: ImageSearchParams) => {
    const currentSkip = images.value.length
    const paginationParams = {
      ...params,
      skip: currentSkip,
      limit: params?.limit || 20, // Default to 20 for pagination
    }

    loading.value = true
    error.value = null

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const queryParams = new URLSearchParams()

      if (paginationParams.skip !== undefined)
        queryParams.append('skip', paginationParams.skip.toString())
      if (paginationParams.limit !== undefined)
        queryParams.append('limit', paginationParams.limit.toString())
      if (paginationParams.status) queryParams.append('status', paginationParams.status)
      if (paginationParams.expires_in)
        queryParams.append('expires_in', paginationParams.expires_in.toString())

      const response = await fetch(
        `${apiUrl}/datasets/${datasetId}/images/with-urls?${queryParams.toString()}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: AbortSignal.timeout(10000),
        },
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`)
      }

      const data: ImagesWithUrlsResponse = await response.json()
      // Append new images to existing ones
      images.value.push(...data.items)
      lastFetched.value = new Date()
      return data.items.length
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
      console.error('Load more images failed:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const hasMoreImages = computed(() => {
    return images.value.length < total.value
  })

  // Pagination computed properties
  const totalPages = computed(() => {
    return Math.ceil(total.value / pageSize.value)
  })

  const startIndex = computed(() => {
    return (currentPage.value - 1) * pageSize.value
  })

  const endIndex = computed(() => {
    return Math.min(startIndex.value + images.value.length, total.value)
  })

  const canGoToPreviousPage = computed(() => {
    return currentPage.value > 1
  })

  const canGoToNextPage = computed(() => {
    return currentPage.value < totalPages.value
  })

  // Simple pagination helpers
  const getPageNumbers = () => {
    const delta = 2 // Nombre de pages avant/après la page courante
    const range: (number | string)[] = []
    const total = totalPages.value

    for (let i = 1; i <= total; i++) {
      if (
        i === 1 || // Première page
        i === total || // Dernière page
        (i >= currentPage.value - delta && i <= currentPage.value + delta) // Autour de la page courante
      ) {
        range.push(i)
      } else if (range[range.length - 1] !== '...') {
        range.push('...') // Ellipsis
      }
    }

    return range
  }

  return {
    // State
    images,
    loading,
    error,
    lastFetched,
    total,
    skip,
    limit,
    currentPage,
    pageSize,

    // Computed
    hasImages,
    imagesByStatus,
    statusCounts,
    getLastFetchedText,
    totalPages,
    startIndex,
    endIndex,
    canGoToPreviousPage,
    canGoToNextPage,

    // Actions
    fetchImages,
    prepareUpload,
    uploadToS3,
    confirmUpload,
    uploadImages,
    deleteImage,
    deleteAllImages,
    resetError,
    clearImages,

    // Pagination
    loadMoreImages,
    hasMoreImages,
    goToPage,
    goToNextPage,
    goToPreviousPage,
    getPageNumbers,
  }
})
