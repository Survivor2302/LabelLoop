<template>
  <main class="min-h-screen bg-white">
    <!-- Navigation Bar -->
    <div class="border-b border-gray-200 bg-white">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Left side - Title and navigation -->
          <div class="flex items-center gap-6">
            <RouterLink
              to="/datasets"
              class="flex items-center gap-2 text-gray-600 hover:text-gray-900"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              <span class="font-medium">Back to Datasets</span>
            </RouterLink>
            <div class="h-6 w-px bg-gray-300"></div>
            <h1 class="text-2xl font-bold text-gray-900">Dataset Detail</h1>
          </div>

          <!-- Right side - Actions -->
          <div class="flex gap-3">
            <Button variant="outline" size="lg">
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
              Edit Dataset
            </Button>
            <Button variant="outline" size="lg" class="text-red-600 border-red-300 hover:bg-red-50">
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
              Delete Dataset
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="px-6 py-8">
      <!-- Loading State -->
      <div v-if="datasetsStore.loading" class="flex items-center justify-center py-16">
        <div class="text-center">
          <div
            class="h-12 w-12 mx-auto mb-4 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center animate-pulse"
          >
            <svg
              class="h-6 w-6 text-white animate-spin"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              ></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Loading dataset...
          </h3>
          <p class="text-gray-500 dark:text-gray-400">
            Please wait while we fetch the dataset details
          </p>
        </div>
      </div>

      <!-- Error State -->
      <div
        v-else-if="datasetsStore.error"
        class="rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/20 p-8 text-center"
      >
        <div
          class="h-12 w-12 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/50 flex items-center justify-center"
        >
          <svg
            class="h-6 w-6 text-red-600 dark:text-red-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-red-900 dark:text-red-100 mb-2">
          Error loading dataset
        </h3>
        <p class="text-red-700 dark:text-red-300 mb-4">{{ datasetsStore.error }}</p>
        <Button @click="loadDataset" variant="outline"> Try Again </Button>
      </div>

      <!-- Dataset Content -->
      <div v-else-if="datasetsStore.currentDataset" class="max-w-7xl mx-auto">
        <!-- Dataset Header -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-8 mb-8">
          <div class="flex items-start justify-between mb-8">
            <div class="flex-1">
              <h2 class="text-3xl font-bold text-gray-900 mb-2">
                {{ datasetsStore.currentDataset.name }}
              </h2>
              <p v-if="datasetsStore.currentDataset.description" class="text-gray-600 text-lg mb-4">
                {{ datasetsStore.currentDataset.description }}
              </p>
              <div class="flex items-center gap-4 text-sm text-gray-500">
                <span>Created {{ formatDate(datasetsStore.currentDataset.created_at) }}</span>
                <span>•</span>
                <span>Updated {{ formatDate(datasetsStore.currentDataset.updated_at) }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <!-- Upload Button -->
              <Button
                @click="triggerFileUpload"
                :disabled="imagesStore.loading"
                class="flex items-center gap-2"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                {{ imagesStore.loading ? 'Uploading...' : 'Upload Images' }}
              </Button>

              <!-- Delete All Images Button -->
              <Button
                @click="confirmDeleteAllImages"
                :disabled="imagesStore.loading || !imagesStore.hasImages"
                variant="outline"
                class="flex items-center gap-2 text-red-600 border-red-300 hover:bg-red-50"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                Delete All Images
              </Button>

              <!-- Hidden file input -->
              <input
                ref="fileInput"
                type="file"
                multiple
                accept="image/*"
                @change="handleFileUpload"
                class="hidden"
              />
            </div>
          </div>

          <!-- Dataset Stats Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-blue-500 flex items-center justify-center">
                  <svg
                    class="h-4 w-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-600">Total Images</p>
                  <p class="text-lg font-bold text-gray-900">
                    {{ datasetsStore.currentDataset.image_count.toLocaleString() }}
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-green-500 flex items-center justify-center">
                  <svg
                    class="h-4 w-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-600">Annotations</p>
                  <p class="text-lg font-bold text-gray-900">
                    {{ datasetsStore.currentDataset.annotation_count.toLocaleString() }}
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-purple-500 flex items-center justify-center">
                  <svg
                    class="h-4 w-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                    />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-600">Labels</p>
                  <p class="text-lg font-bold text-gray-900">
                    {{ datasetsStore.currentDataset.label_count.toLocaleString() }}
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-orange-500 flex items-center justify-center">
                  <svg
                    class="h-4 w-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-600">Progress</p>
                  <p class="text-lg font-bold text-gray-900">
                    {{
                      Math.round(
                        (datasetsStore.currentDataset.annotation_count /
                          datasetsStore.currentDataset.image_count) *
                          100,
                      ) || 0
                    }}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="my-8">
          <div class="h-px bg-gray-200"></div>
        </div>

        <!-- Images Grid Section -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-8">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-semibold text-gray-900">Dataset Images</h3>
              <p class="text-gray-600 mt-1">
                {{ imagesStore.total.toLocaleString() }} images in this dataset
              </p>
            </div>
            <div class="flex items-center gap-3">
              <Button variant="outline" size="sm">
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z"
                  />
                </svg>
                Filter
              </Button>
            </div>
          </div>

          <!-- Loading State for Images -->
          <div v-if="imagesStore.loading" class="flex items-center justify-center py-16">
            <div class="text-center">
              <div
                class="h-12 w-12 mx-auto mb-4 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center animate-pulse"
              >
                <svg
                  class="h-6 w-6 text-white animate-spin"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  ></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Loading images...
              </h3>
              <p class="text-gray-500 dark:text-gray-400">Please wait while we fetch the images</p>
            </div>
          </div>

          <!-- Error State for Images -->
          <div
            v-else-if="imagesStore.error"
            class="rounded-xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/20 p-8 text-center"
          >
            <div
              class="h-12 w-12 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/50 flex items-center justify-center"
            >
              <svg
                class="h-6 w-6 text-red-600 dark:text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-red-900 dark:text-red-100 mb-2">
              Error loading images
            </h3>
            <p class="text-red-700 dark:text-red-300 mb-4">{{ imagesStore.error }}</p>
            <Button @click="loadImages" variant="outline"> Try Again </Button>
          </div>

          <!-- Empty State for Images -->
          <div v-else-if="!imagesStore.hasImages" class="flex items-center justify-center py-16">
            <div class="text-center max-w-md mx-auto">
              <div
                class="mx-auto mb-6 h-16 w-16 rounded-full bg-gray-100 flex items-center justify-center"
              >
                <svg
                  class="h-8 w-8 text-gray-400 flex-shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h2 class="text-xl font-semibold text-gray-900 mb-2">No images yet</h2>
              <p class="text-gray-500 mb-6">
                Upload your first images to get started with this dataset.
              </p>
              <Button @click="triggerFileUpload" variant="outline" size="lg">
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                  />
                </svg>
                Upload Images
              </Button>
            </div>
          </div>

          <!-- Images Grid -->
          <div v-else class="grid grid-cols-5 gap-4">
            <div
              v-for="image in imagesStore.images"
              :key="image.id"
              class="group relative aspect-square bg-gray-100 rounded-lg overflow-hidden border border-gray-200 hover:border-gray-300 transition-all duration-200 cursor-pointer"
            >
              <!-- Real Image or Placeholder -->
              <div v-if="image.download_url" class="w-full h-full">
                <img
                  :src="image.download_url"
                  :alt="image.filename"
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
              </div>
              <div
                v-else
                class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200"
              >
                <svg
                  class="h-8 w-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>

              <!-- Image Info Overlay -->
              <div
                class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center"
              >
                <div class="text-center text-white">
                  <p class="text-sm font-medium">{{ image.filename }}</p>
                  <p class="text-xs text-gray-300">{{ formatFileSize(image.file_size) }}</p>
                </div>
              </div>

              <!-- Delete Button -->
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200"
              >
                <Button
                  @click.stop="deleteImage(image.id)"
                  size="sm"
                  variant="secondary"
                  class="h-6 w-6 p-0 bg-red-500/90 hover:bg-red-600 text-white"
                >
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </Button>
              </div>
            </div>
          </div>

          <!-- Pagination Controls -->
          <div v-if="imagesStore.hasImages" class="mt-8">
            <!-- Pagination Info -->
            <div class="text-center text-sm text-gray-500 mb-4">
              Showing {{ (imagesStore.currentPage - 1) * 100 + 1 }}-{{
                Math.min(imagesStore.currentPage * 100, imagesStore.total)
              }}
              of {{ imagesStore.total.toLocaleString() }} images (Page
              {{ imagesStore.currentPage }} of {{ Math.ceil(imagesStore.total / 100) }})
            </div>

            <!-- Single Page Message -->
            <div
              v-if="Math.ceil(imagesStore.total / 100) === 1"
              class="text-center text-sm text-gray-400"
            >
              All images are displayed on this page
            </div>

            <!-- Pagination Buttons -->
            <div
              v-if="Math.ceil(imagesStore.total / 100) > 1"
              class="flex items-center justify-center gap-2"
            >
              <!-- Previous Page -->
              <Button
                @click="goToPreviousPage"
                variant="outline"
                size="sm"
                :disabled="imagesStore.currentPage <= 1 || imagesStore.loading"
              >
                <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
                Previous
              </Button>

              <!-- Page Numbers -->
              <div class="flex items-center gap-1">
                <template v-for="page in imagesStore.getPageNumbers()" :key="page">
                  <Button
                    v-if="page !== '...'"
                    @click="goToPage(page as number)"
                    :variant="page === imagesStore.currentPage ? 'default' : 'outline'"
                    size="sm"
                    :disabled="imagesStore.loading"
                    class="w-10 h-10 p-0"
                  >
                    {{ page }}
                  </Button>
                  <span v-else class="px-2 text-gray-400">...</span>
                </template>
              </div>

              <!-- Next Page -->
              <Button
                @click="goToNextPage"
                variant="outline"
                size="sm"
                :disabled="
                  imagesStore.currentPage >= Math.ceil(imagesStore.total / 100) ||
                  imagesStore.loading
                "
              >
                Next
                <svg class="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete All Images Confirmation Dialog -->
    <AlertDialog v-model:open="isDeleteAllDialogOpen" class="alert-dialog-custom">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle class="flex items-center gap-2 text-red-600">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
            Delete All Images
          </AlertDialogTitle>
          <AlertDialogDescription class="text-gray-600">
            <strong class="text-red-600">⚠️ WARNING: This action cannot be undone!</strong
            ><br /><br />
            This will permanently delete
            <strong>{{ imagesStore.total.toLocaleString() }} images</strong> from both the database
            and S3 storage. <br /><br />
            Are you absolutely sure you want to proceed?
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel @click="isDeleteAllDialogOpen = false"> Cancel </AlertDialogCancel>
          <AlertDialogAction
            @click="deleteAllImages"
            class="bg-red-600 hover:bg-red-700 text-white"
            :disabled="imagesStore.loading"
          >
            <svg
              v-if="imagesStore.loading"
              class="h-4 w-4 mr-2 animate-spin"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            {{ imagesStore.loading ? 'Deleting...' : 'Yes, Delete All Images' }}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from '@/components/ui/button'
import { RouterLink } from 'vue-router'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { useDatasetsStore, useImagesStore } from '@/stores'
import { toast } from 'vue-sonner'

// Stores
const datasetsStore = useDatasetsStore()
const imagesStore = useImagesStore()

// Router
const route = useRoute()

// Get dataset ID from route params
const datasetId = computed(() => parseInt(route.params.id as string))

// File input ref
const fileInput = ref<HTMLInputElement | null>(null)

// Dialog state
const isDeleteAllDialogOpen = ref(false)

// Format date for display
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

// Format file size for display
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Handle image error
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

// Load dataset details
const loadDataset = async () => {
  try {
    await datasetsStore.getDataset(datasetId.value)
  } catch (error) {
    console.error('Error loading dataset:', error)
  }
}

// Load images
const loadImages = async () => {
  try {
    await imagesStore.fetchImages(datasetId.value, { expires_in: 3600, limit: 100 })
  } catch (error) {
    console.error('Error loading images:', error)
  }
}

// Page navigation functions
const goToPage = async (page: number) => {
  try {
    await imagesStore.goToPage(page, datasetId.value, { expires_in: 3600 })
  } catch (error) {
    console.error('Error going to page:', error)
    toast.error('Failed to load page', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  }
}

const goToNextPage = async () => {
  try {
    await imagesStore.goToNextPage(datasetId.value, { expires_in: 3600 })
  } catch (error) {
    console.error('Error going to next page:', error)
    toast.error('Failed to load next page', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  }
}

const goToPreviousPage = async () => {
  try {
    await imagesStore.goToPreviousPage(datasetId.value, { expires_in: 3600 })
  } catch (error) {
    console.error('Error going to previous page:', error)
    toast.error('Failed to load previous page', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  }
}

// Trigger file upload
const triggerFileUpload = () => {
  fileInput.value?.click()
}

// Confirm delete all images
const confirmDeleteAllImages = () => {
  if (imagesStore.hasImages) {
    isDeleteAllDialogOpen.value = true
  }
}

// Delete all images
const deleteAllImages = async () => {
  try {
    const result = await imagesStore.deleteAllImages(datasetId.value)

    // Close dialog
    isDeleteAllDialogOpen.value = false

    // Show success toast
    toast.success('All images deleted successfully', {
      description: result.message || `Deleted ${result.deleted_count} images`,
    })

    // Refresh dataset data to update counts
    await loadDataset()
  } catch (error) {
    console.error('Error deleting all images:', error)
    toast.error('Failed to delete all images', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  }
}

// Handle file upload
const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files

  if (!files || files.length === 0) return

  try {
    const fileArray = Array.from(files)
    const result = await imagesStore.uploadImages(datasetId.value, fileArray)

    // Show success notification
    toast.success('Images uploaded successfully!', {
      description: `${result.success} images uploaded, ${result.failed} failed.`,
    })

    // Refresh dataset details to update counts
    await loadDataset()
  } catch (error) {
    console.error('Error uploading images:', error)
    toast.error('Failed to upload images', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  } finally {
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

// Delete image
const deleteImage = async (imageId: number) => {
  try {
    await imagesStore.deleteImage(imageId)

    // Show success notification
    toast.success('Image deleted successfully!')

    // Refresh dataset details to update counts
    await loadDataset()
  } catch (error) {
    console.error('Error deleting image:', error)
    toast.error('Failed to delete image', {
      description: imagesStore.error || 'An unexpected error occurred.',
    })
  }
}

// Load data on component mount
onMounted(async () => {
  await Promise.all([loadDataset(), loadImages()])
})
</script>
