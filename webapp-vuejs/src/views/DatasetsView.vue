<template>
  <main class="min-h-screen bg-white">
    <!-- Navigation Bar -->
    <div class="border-b border-gray-200 bg-white">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Left side - Title and navigation -->
          <div class="flex items-center gap-6">
            <RouterLink to="/" class="flex items-center gap-2 text-gray-600 hover:text-gray-900">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              <span class="font-medium">Back to Home</span>
            </RouterLink>
            <div class="h-6 w-px bg-gray-300"></div>
            <h1 class="text-2xl font-bold text-gray-900">Datasets</h1>
          </div>

          <!-- Right side - Create button -->
          <Sheet v-model:open="isSheetOpen">
            <SheetTrigger as-child>
              <Button variant="outline" size="lg">
                <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
                Create Dataset
              </Button>
            </SheetTrigger>
            <SheetContent class="w-[600px] sm:w-[720px] lg:w-[1000px] p-0 overflow-hidden">
              <!-- Header with gradient background -->
              <div
                class="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-950/20 dark:via-indigo-950/20 dark:to-purple-950/20 p-8 border-b"
              >
                <div
                  class="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5"
                ></div>
                <div class="relative">
                  <div class="flex items-center gap-4 mb-4">
                    <div
                      class="h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg"
                    >
                      <svg
                        class="h-6 w-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                        ></path>
                      </svg>
                    </div>
                    <div>
                      <SheetTitle class="text-2xl font-bold text-gray-900 dark:text-white"
                        >Create New Dataset</SheetTitle
                      >
                      <SheetDescription class="text-gray-600 dark:text-gray-300 mt-1">
                        Build your computer vision dataset for labeling projects
                      </SheetDescription>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Form content with better spacing and design -->
              <div class="p-8 bg-white dark:bg-gray-900">
                <Form @submit="onSubmit" class="space-y-8">
                  <!-- Dataset Name Field -->
                  <FormField name="name" v-slot="{ componentField }" rules="required|min:1|max:255">
                    <FormItem class="space-y-4">
                      <FormLabel
                        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-3"
                      >
                        <span
                          class="h-3 w-3 rounded-full bg-gradient-to-r from-blue-500 to-blue-600"
                        ></span>
                        Dataset Name
                        <span class="text-red-500 font-bold">*</span>
                      </FormLabel>
                      <FormControl>
                        <div class="relative group">
                          <Input
                            v-bind="componentField"
                            v-model="formData.name"
                            placeholder="e.g., Street Traffic Detection Dataset"
                            required
                            class="h-14 pl-5 pr-12 text-base border-2 border-gray-200 dark:border-gray-700 rounded-2xl focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all duration-300 bg-white dark:bg-gray-800/50 group-hover:border-blue-300 dark:group-hover:border-blue-600"
                          />
                          <div class="absolute right-4 top-1/2 -translate-y-1/2">
                            <svg
                              class="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors duration-200"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                              ></path>
                            </svg>
                          </div>
                        </div>
                      </FormControl>
                      <FormDescription
                        class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2 ml-6"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          ></path>
                        </svg>
                        Choose a descriptive name (1-255 characters)
                      </FormDescription>
                      <FormMessage class="text-red-500 text-sm font-medium ml-6" />
                    </FormItem>
                  </FormField>

                  <!-- Description Field -->
                  <FormField name="description" v-slot="{ componentField }" rules="max:1000">
                    <FormItem class="space-y-4">
                      <FormLabel
                        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-3"
                      >
                        <span
                          class="h-3 w-3 rounded-full bg-gradient-to-r from-green-500 to-green-600"
                        ></span>
                        Description
                      </FormLabel>
                      <FormControl>
                        <div class="relative group">
                          <Textarea
                            v-bind="componentField"
                            v-model="formData.description"
                            placeholder="Describe your dataset's purpose, content, and use cases..."
                            class="min-h-[140px] p-5 text-base border-2 border-gray-200 dark:border-gray-700 rounded-2xl focus:border-green-500 focus:ring-4 focus:ring-green-500/20 transition-all duration-300 bg-white dark:bg-gray-800/50 resize-none group-hover:border-green-300 dark:group-hover:border-green-600"
                          />
                          <div
                            class="absolute bottom-4 right-4 text-xs text-gray-400 bg-white dark:bg-gray-800 px-2 py-1 rounded-lg"
                          >
                            {{ formData.description.length }}/1000
                          </div>
                        </div>
                      </FormControl>
                      <FormDescription
                        class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2 ml-6"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          ></path>
                        </svg>
                        Optional description to help others understand your dataset
                      </FormDescription>
                      <FormMessage class="text-red-500 text-sm font-medium ml-6" />
                    </FormItem>
                  </FormField>

                  <!-- Labels Field -->
                  <FormField name="labels" v-slot="{}">
                    <FormItem class="space-y-4">
                      <FormLabel
                        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-3"
                      >
                        <span
                          class="h-3 w-3 rounded-full bg-gradient-to-r from-purple-500 to-purple-600"
                        ></span>
                        Labels
                      </FormLabel>
                      <FormControl>
                        <div class="relative group">
                          <div class="relative">
                            <input
                              v-model="labelInput"
                              @input="handleLabelInput"
                              @focus="showFormLabelDropdown = true"
                              @blur="handleFormLabelBlur"
                              @keydown.enter.prevent="addLabelFromInput"
                              @keydown.escape="showFormLabelDropdown = false"
                              type="text"
                              placeholder="Search or add labels..."
                              class="h-14 w-full pl-5 pr-12 text-base border-2 border-gray-200 dark:border-gray-700 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 transition-all duration-300 bg-white dark:bg-gray-800/50 group-hover:border-purple-300 dark:group-hover:border-purple-600"
                            />
                            <div class="absolute right-4 top-1/2 -translate-y-1/2">
                              <svg
                                class="h-5 w-5 text-gray-400 group-hover:text-purple-500 transition-colors duration-200"
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
                          </div>

                          <!-- Label Dropdown -->
                          <div
                            v-if="showFormLabelDropdown"
                            class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto"
                          >
                            <!-- Add new label option -->
                            <div
                              v-if="
                                labelInput.trim() && !existingLabels.includes(labelInput.trim())
                              "
                              @click="addLabelFromInput"
                              class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-200 dark:border-gray-600 flex items-center gap-2 text-green-600 dark:text-green-400"
                            >
                              <svg
                                class="h-4 w-4"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  stroke-width="2"
                                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                                />
                              </svg>
                              Create "{{ labelInput.trim() }}"
                            </div>

                            <!-- Existing labels -->
                            <div
                              v-for="label in filteredFormLabels"
                              :key="label.id"
                              @click="toggleFormLabel(label.name)"
                              class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer flex items-center gap-2"
                              :class="{
                                'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300':
                                  formData.label_names.includes(label.name),
                              }"
                            >
                              <svg
                                class="h-4 w-4"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  v-if="formData.label_names.includes(label.name)"
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  stroke-width="2"
                                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                                />
                                <path
                                  v-else
                                  stroke-linecap="round"
                                  stroke-linejoin="round"
                                  stroke-width="2"
                                  d="M12 4v16m8-8H4"
                                />
                              </svg>
                              {{ label.name }}
                            </div>

                            <div
                              v-if="filteredFormLabels.length === 0 && !labelInput.trim()"
                              class="px-4 py-2 text-gray-500 dark:text-gray-400 text-sm"
                            >
                              No labels available
                            </div>
                          </div>
                        </div>
                      </FormControl>

                      <!-- Selected Labels Display -->
                      <div v-if="formData.label_names.length > 0" class="flex flex-wrap gap-2 ml-6">
                        <span
                          v-for="labelName in formData.label_names"
                          :key="labelName"
                          class="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-800 dark:text-purple-300 text-xs rounded-full"
                        >
                          {{ labelName }}
                          <button
                            @click="removeFormLabel(labelName)"
                            class="hover:bg-purple-200 dark:hover:bg-purple-800/30 rounded-full p-0.5"
                          >
                            <svg
                              class="h-3 w-3"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"
                              />
                            </svg>
                          </button>
                        </span>
                      </div>

                      <FormDescription
                        class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-2 ml-6"
                      >
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                          ></path>
                        </svg>
                        Select existing labels or create new ones for your dataset
                      </FormDescription>
                      <FormMessage class="text-red-500 text-sm font-medium ml-6" />
                    </FormItem>
                  </FormField>
                </Form>
              </div>

              <!-- Footer with gradient background -->
              <div
                class="relative bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-900/50 p-6 border-t"
              >
                <div
                  class="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5"
                ></div>
                <div class="relative flex items-center justify-between gap-4">
                  <SheetClose as-child>
                    <Button
                      variant="outline"
                      class="h-12 px-6 border-2 border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 rounded-xl font-medium transition-all duration-200 hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      Cancel
                    </Button>
                  </SheetClose>
                  <Button
                    @click="onSubmit"
                    :disabled="!formData.name.trim()"
                    class="h-12 px-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 rounded-xl font-semibold text-white shadow-lg hover:shadow-xl transition-all duration-200 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                      ></path>
                    </svg>
                    Create Dataset
                  </Button>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </div>

    <!-- Search and Filters Bar -->
    <div class="border-b border-gray-200 bg-white">
      <div class="px-6 py-4">
        <div class="flex items-center gap-4">
          <!-- Search Input -->
          <div class="relative flex-1 max-w-md">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              placeholder="Search datasets..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <!-- Label Filter -->
          <div class="relative">
            <div class="relative">
              <input
                v-model="labelSearchQuery"
                @input="handleLabelSearch"
                @focus="showLabelDropdown = true"
                @blur="handleLabelBlur"
                @keydown.enter="handleLabelEnter"
                type="text"
                placeholder="Search labels..."
                class="w-full bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                <svg
                  class="h-4 w-4 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </div>

            <!-- Label Dropdown -->
            <div
              v-if="showLabelDropdown"
              class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto"
            >
              <div
                v-for="label in filteredLabels"
                :key="label.id"
                @click="toggleLabel(label.name)"
                class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-2"
                :class="{ 'bg-blue-50 text-blue-700': selectedLabels.includes(label.name) }"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    v-if="selectedLabels.includes(label.name)"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                  <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                {{ label.name }}
              </div>
              <div
                v-if="filteredLabels.length === 0 && labelSearchQuery.trim()"
                class="px-4 py-2 text-gray-500 text-sm"
              >
                No labels found
              </div>
            </div>
          </div>

          <!-- Sort Filter -->
          <div class="flex items-center gap-2">
            <div class="relative">
              <select
                v-model="sortBy"
                @change="handleSort"
                class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option>Sort by</option>
                <option>Name</option>
                <option>Created Date</option>
                <option>Updated Date</option>
                <option>Image Count</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                <svg
                  class="h-4 w-4 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
            </div>

            <!-- Sort Order Toggle -->
            <Button
              v-if="sortBy && sortBy !== 'Sort by'"
              @click="toggleSortOrder"
              variant="outline"
              size="sm"
              class="h-9 w-9 p-0"
              :title="sortOrder === 'asc' ? 'Sort ascending' : 'Sort descending'"
            >
              <svg
                class="h-4 w-4 transition-transform"
                :class="{ 'rotate-180': sortOrder === 'desc' }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"
                />
              </svg>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected Labels Display -->
    <div v-if="selectedLabels.length > 0" class="border-b border-gray-200 bg-white">
      <div class="px-6 py-3">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-700">Selected labels:</span>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="label in selectedLabels"
              :key="label"
              class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
            >
              {{ label }}
              <button @click="removeLabel(label)" class="hover:bg-blue-200 rounded-full p-0.5">
                <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </span>
            <button
              @click="clearAllLabels"
              class="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full hover:bg-gray-200"
            >
              <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
              Clear All
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="px-6 py-8">
      <!-- Datasets Grid or Empty State -->
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
            Loading datasets...
          </h3>
          <p class="text-gray-500 dark:text-gray-400">Please wait while we fetch your datasets</p>
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
          Error loading datasets
        </h3>
        <p class="text-red-700 dark:text-red-300 mb-4">{{ datasetsStore.error }}</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!datasetsStore.hasDatasets" class="flex items-center justify-center py-24">
        <div class="text-center max-w-md mx-auto">
          <!-- Icon -->
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
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
          </div>

          <!-- Content -->
          <h2 class="text-xl font-semibold text-gray-900 mb-2">
            {{ getNoResultsMessage().title }}
          </h2>
          <p class="text-gray-500 mb-6">
            {{ getNoResultsMessage().description }}
          </p>

          <!-- Create Button (only show if no active filters) -->
          <Button
            v-if="getNoResultsMessage().showCreateButton"
            @click="isSheetOpen = true"
            variant="outline"
            size="lg"
          >
            <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Create Your First Dataset
          </Button>

          <!-- Clear Filters Button (only show if active filters) -->
          <div v-else class="flex gap-3 justify-center">
            <Button @click="clearFilters" variant="outline" size="lg">
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
              Clear Filters
            </Button>
            <Button @click="isSheetOpen = true" variant="outline" size="lg">
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Create Dataset
            </Button>
          </div>
        </div>
      </div>

      <!-- Datasets Grid -->
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div
            v-for="dataset in datasetsStore.datasets"
            :key="dataset.id"
            @click="navigateToDataset(dataset.id)"
            class="group bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden relative cursor-pointer"
          >
            <!-- Dataset Image Placeholder -->
            <div class="relative h-32 bg-gray-100 flex items-center justify-center">
              <svg
                class="h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>

              <!-- Hover Action Buttons -->
              <div
                class="absolute top-2 left-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex gap-1"
                @click.stop
              >
                <Button
                  size="sm"
                  variant="secondary"
                  class="h-7 w-7 p-0 bg-white/90 hover:bg-white text-gray-700 shadow-sm"
                >
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                </Button>
                <AlertDialog v-model:open="isDeleteDialogOpen">
                  <AlertDialogTrigger as-child>
                    <Button
                      @click="
                        (event: { stopPropagation: () => void }) => {
                          event.stopPropagation()
                          datasetToDelete = dataset
                          isDeleteDialogOpen = true
                        }
                      "
                      size="sm"
                      variant="secondary"
                      class="h-7 w-7 p-0 bg-red-500/90 hover:bg-red-600 text-white shadow-sm"
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
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Delete Dataset</AlertDialogTitle>
                      <AlertDialogDescription>
                        Are you sure you want to delete
                        <strong>"{{ datasetToDelete?.name }}"</strong>? This action cannot be undone
                        and will permanently remove the dataset and all its associated data.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel @click="isDeleteDialogOpen = false"
                        >Cancel</AlertDialogCancel
                      >
                      <AlertDialogAction
                        @click="deleteDataset"
                        class="bg-red-600 hover:bg-red-700 text-white"
                      >
                        Delete Dataset
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </div>

            <!-- Dataset Content -->
            <div class="p-3">
              <h3 class="font-semibold text-gray-900 text-sm mb-1 line-clamp-1">
                {{ dataset.name }}
              </h3>
              <p v-if="dataset.description" class="text-xs text-gray-600 mb-3 line-clamp-2">
                {{ dataset.description }}
              </p>

              <!-- Dataset Metadata -->
              <div class="flex items-center justify-between text-xs text-gray-500">
                <div class="flex items-center gap-1">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  {{ dataset.image_count.toLocaleString() }} images
                </div>
                <div class="flex items-center gap-1">
                  <svg class="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  {{ formatDate(dataset.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetTitle,
  SheetTrigger,
  SheetClose,
} from '@/components/ui/sheet'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { useDatasetsStore, useLabelsStore } from '@/stores'
import { toast } from 'vue-sonner'

// Store
const datasetsStore = useDatasetsStore()
const labelsStore = useLabelsStore()

// Router
const router = useRouter()
const route = useRoute()

// Sheet control
const isSheetOpen = ref(false)

// AlertDialog control
const isDeleteDialogOpen = ref(false)
const datasetToDelete = ref<{ id: number; name: string } | null>(null)

// Search and filter state
const searchQuery = ref('')
const selectedLabels = ref<string[]>([])
const labelSearchQuery = ref('')
const showLabelDropdown = ref(false)
const sortBy = ref('Sort by')
const sortOrder = ref<'asc' | 'desc'>('asc')

// Computed for filtered state
const hasActiveFilters = computed(() => {
  return (
    searchQuery.value.trim() !== '' || selectedLabels.value.length > 0 || sortBy.value !== 'Sort by'
  )
})

// Computed for filtered labels
const filteredLabels = computed(() => {
  if (!labelSearchQuery.value.trim()) {
    return labelsStore.labels
  }
  return labelsStore.labels.filter((label) =>
    label.name.toLowerCase().includes(labelSearchQuery.value.toLowerCase()),
  )
})

// Form data matching the Python Pydantic DatasetCreate model
const formData = ref({
  name: '',
  description: '',
  label_names: [] as string[], // Array of label names
})

// Form-specific label handling
const labelInput = ref('')
const showFormLabelDropdown = ref(false)

// Computed properties for form labels
const existingLabels = computed(() => labelsStore.labels.map((label) => label.name))

const filteredFormLabels = computed(() => {
  if (!labelInput.value.trim()) {
    return labelsStore.labels
  }
  return labelsStore.labels.filter((label) =>
    label.name.toLowerCase().includes(labelInput.value.toLowerCase()),
  )
})

// Form submission handler
const onSubmit = async () => {
  if (!formData.value.name.trim()) {
    return
  }

  try {
    // Prepare data according to DatasetCreate schema
    const datasetData = {
      name: formData.value.name.trim(),
      description: formData.value.description.trim() || null,
      label_names: formData.value.label_names,
    }

    // Create dataset using the store
    await datasetsStore.createDataset(datasetData)

    // Reset form
    formData.value = {
      name: '',
      description: '',
      label_names: [],
    }
    labelInput.value = ''
    showFormLabelDropdown.value = false

    // Reset search parameters
    searchQuery.value = ''
    selectedLabels.value = []
    sortBy.value = 'Sort by'
    sortOrder.value = 'asc'

    // Update URL and refresh search
    await updateURL()
    await performSearch()

    // Close the sheet
    isSheetOpen.value = false

    // Show success notification
    toast.success('Dataset created successfully!', {
      description: `"${datasetData.name}" has been created.`,
    })
  } catch (error) {
    console.error('Error creating dataset:', error)

    // Show error notification
    toast.error('Failed to create dataset', {
      description: datasetsStore.error || 'An unexpected error occurred.',
    })
  }
}

// Format date for display
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

// Delete dataset
const deleteDataset = async () => {
  if (!datasetToDelete.value) return

  try {
    await datasetsStore.deleteDataset(datasetToDelete.value.id)

    // Show success notification
    toast.success('Dataset deleted successfully!', {
      description: `"${datasetToDelete.value.name}" has been deleted.`,
    })

    // Close dialog and reset
    isDeleteDialogOpen.value = false
    datasetToDelete.value = null
  } catch (error) {
    console.error('Error deleting dataset:', error)

    // Show error notification
    toast.error('Failed to delete dataset', {
      description: datasetsStore.error || 'An unexpected error occurred.',
    })
  }
}

// Search and filter functions
const performSearch = async () => {
  const params: Record<string, string | number> = {}

  if (searchQuery.value.trim()) {
    params.search = searchQuery.value.trim()
  }

  if (selectedLabels.value.length > 0) {
    // For now, use the first selected label for the API
    // In a real implementation, you might want to send multiple labels
    params.label_name = selectedLabels.value[0]?.toLowerCase() || ''
  }

  if (sortBy.value && sortBy.value !== 'Sort by') {
    params.sort_by =
      sortBy.value === 'Name'
        ? 'name'
        : sortBy.value === 'Created Date'
          ? 'created_at'
          : sortBy.value === 'Updated Date'
            ? 'created_at'
            : sortBy.value === 'Image Count'
              ? 'image_count'
              : 'id'
    params.sort_order = sortOrder.value
  }

  // Only fetch with params if there are actual filters applied
  if (Object.keys(params).length > 0) {
    await datasetsStore.fetchDatasets(params)
  } else {
    // Fetch all datasets without filters
    await datasetsStore.fetchDatasets()
  }
}

// Debounced search
let searchTimeout: number | null = null

const handleSearch = async () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  searchTimeout = window.setTimeout(async () => {
    await updateURL()
    await performSearch()
  }, 300) // 300ms debounce
}

// Label handling functions
const handleLabelSearch = () => {
  // Just update the filtered labels, don't trigger search yet
}

const handleLabelBlur = () => {
  // Delay hiding dropdown to allow click events
  setTimeout(() => {
    showLabelDropdown.value = false
  }, 200)
}

// Form label handling functions
const handleLabelInput = () => {
  // Just update the filtered labels, don't trigger search yet
}

const handleFormLabelBlur = () => {
  // Delay hiding dropdown to allow click events
  setTimeout(() => {
    showFormLabelDropdown.value = false
  }, 200)
}

const addLabelFromInput = () => {
  const labelName = labelInput.value.trim()
  if (labelName && !formData.value.label_names.includes(labelName)) {
    formData.value.label_names.push(labelName)
    labelInput.value = ''
    showFormLabelDropdown.value = false
  }
}

const toggleFormLabel = (labelName: string) => {
  const index = formData.value.label_names.indexOf(labelName)
  if (index > -1) {
    formData.value.label_names.splice(index, 1)
  } else {
    formData.value.label_names.push(labelName)
  }
  showFormLabelDropdown.value = false
}

const removeFormLabel = (labelName: string) => {
  const index = formData.value.label_names.indexOf(labelName)
  if (index > -1) {
    formData.value.label_names.splice(index, 1)
  }
}

const handleLabelEnter = async () => {
  // If there's a search query and filtered labels, select the first one
  if (labelSearchQuery.value.trim() && filteredLabels.value.length > 0) {
    const firstLabel = filteredLabels.value[0]
    if (firstLabel) {
      await toggleLabel(firstLabel.name)
      labelSearchQuery.value = ''
      showLabelDropdown.value = false
    }
  }
}

// Label selection functions
const toggleLabel = async (labelName: string) => {
  const index = selectedLabels.value.indexOf(labelName)
  if (index > -1) {
    selectedLabels.value.splice(index, 1)
  } else {
    selectedLabels.value.push(labelName)
  }
  await updateURL()
  await performSearch()
}

const removeLabel = async (labelName: string) => {
  const index = selectedLabels.value.indexOf(labelName)
  if (index > -1) {
    selectedLabels.value.splice(index, 1)
    await updateURL()
    await performSearch()
  }
}

const clearAllLabels = async () => {
  selectedLabels.value = []
  await updateURL()
  await performSearch()
}

const handleSort = async () => {
  await updateURL()
  await performSearch()
}

const toggleSortOrder = async () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  await handleSort()
}

// Generate custom message for no results
const getNoResultsMessage = () => {
  if (!hasActiveFilters.value) {
    return {
      title: 'No datasets yet',
      description: 'Create your first dataset to get started with computer vision projects.',
      showCreateButton: true,
    }
  }

  const filters = []
  if (searchQuery.value.trim()) {
    filters.push(`"${searchQuery.value.trim()}"`)
  }
  if (selectedLabels.value.length > 0) {
    filters.push(`labels: ${selectedLabels.value.join(', ')}`)
  }
  if (sortBy.value !== 'Sort by') {
    filters.push(`sorted by ${sortBy.value}`)
  }

  return {
    title: 'No datasets found',
    description: `No datasets match your current filters (${filters.join(', ')}). Try adjusting your search criteria.`,
    showCreateButton: false,
  }
}

// Clear all filters
const clearFilters = async () => {
  searchQuery.value = ''
  selectedLabels.value = []
  labelSearchQuery.value = ''
  showLabelDropdown.value = false
  sortBy.value = 'Sort by'
  sortOrder.value = 'asc'
  await updateURL()
  await datasetsStore.fetchDatasets()
}

// URL management functions
const updateURL = async () => {
  const params = new URLSearchParams()

  if (searchQuery.value.trim()) {
    params.set('search', searchQuery.value.trim())
  }

  if (selectedLabels.value.length > 0) {
    params.set('labels', selectedLabels.value.join(','))
  }

  if (sortBy.value && sortBy.value !== 'Sort by') {
    params.set('sortBy', sortBy.value)
  }

  if (sortOrder.value !== 'asc') {
    params.set('sortOrder', sortOrder.value)
  }

  await router.replace({ query: Object.fromEntries(params) })
}

const loadFromURL = () => {
  const query = route.query

  if (query.search && typeof query.search === 'string') {
    searchQuery.value = query.search
  }

  if (query.labels && typeof query.labels === 'string') {
    selectedLabels.value = query.labels.split(',').filter(Boolean)
  }

  if (query.sortBy && typeof query.sortBy === 'string') {
    sortBy.value = query.sortBy
  }

  if (query.sortOrder && typeof query.sortOrder === 'string') {
    sortOrder.value = query.sortOrder as 'asc' | 'desc'
  }
}

// Navigate to dataset detail
const navigateToDataset = (datasetId: number) => {
  router.push(`/datasets/${datasetId}`)
}

// Load datasets and labels on component mount
onMounted(async () => {
  // Load from URL first
  loadFromURL()

  // Load data
  await Promise.all([datasetsStore.fetchDatasets(), labelsStore.fetchLabels()])

  // Perform search with URL parameters
  await performSearch()
})
</script>
