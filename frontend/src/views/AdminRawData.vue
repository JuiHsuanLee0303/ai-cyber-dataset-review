<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row justify-between items-center mb-6">
      <!-- Title and Auto Update Indicator -->
      <div class="flex flex-col sm:flex-row items-center justify-between mb-4 sm:mb-0">
        <!-- Title Section -->
        <h1 class="text-3xl font-bold text-gray-800">待審核資料集管理</h1>
        
        <!-- Auto Update Indicator -->
        <div v-if="isPolling" class="flex items-center space-x-1 sm:space-x-2 px-2 sm:px-3 py-1 bg-blue-50 border border-blue-200 rounded-full mt-2 mb-3 sm:my-0 sm:ms-4">
          <div class="animate-spin rounded-full h-2 w-2 sm:h-3 sm:w-3 border-b-2 border-blue-600"></div>
          <span class="text-xs font-medium text-blue-700">
            <span class="sm:hidden">更新中</span>
            <span class="hidden sm:inline">自動更新中</span>
          </span>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="grid grid-cols-2 sm:flex sm:items-center sm:space-x-2 gap-2 sm:gap-0 mb-4 sm:mb-0">
        <button 
          @click="fetchDatasets" 
          class="btn btn-primary btn-sm w-full sm:w-auto"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>刷新</span>
        </button>
        
        <button 
          @click="openModal()" 
          class="btn btn-success btn-sm w-full sm:w-auto"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <span>新增<span class="hidden sm:inline">資料</span></span>
        </button>
        
        <button 
          @click="openBatchModal()" 
          class="btn btn-secondary btn-sm w-full sm:w-auto"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <span>批量新增</span>
        </button>
        
        <button 
          @click="openGenerateModal()" 
          class="btn btn-info btn-sm w-full sm:w-auto"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <span><span class="sm:hidden">法規</span><span class="hidden sm:inline">從法規</span>生成</span>
        </button>
      </div>

      <!-- Display Mode Toggle and Batch Actions -->
      <div class="flex items-center justify-between sm:justify-end sm:space-x-4">
        <!-- Display Mode Toggle -->
        <div class="flex items-center space-x-2 sm:space-x-3">
          <span class="text-xs sm:text-sm font-medium text-gray-700">
            <span class="sm:hidden">顯示</span>
            <span class="hidden sm:inline">顯示模式</span>
          </span>
          <div class="relative flex bg-gray-300 rounded-lg p-1">
            <div 
              class="absolute top-1 bottom-1 bg-white rounded-md shadow-sm transition-all duration-300 ease-in-out"
              :class="displayMode === 'card' ? 'left-1 w-6 sm:w-8' : 'left-7 sm:left-9 w-6 sm:w-8'"
            ></div>
            
            <button 
              @click="displayMode = 'card'"
              class="relative z-10 w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center rounded-md transition-all duration-300 ease-in-out"
              :class="displayMode === 'card' ? 'text-gray-800' : 'text-gray-500 hover:text-gray-700'"
              title="卡片式顯示"
            >
              <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
              </svg>
            </button>
            
            <button 
              @click="displayMode = 'list'"
              class="relative z-10 w-6 h-6 sm:w-8 sm:h-8 flex items-center justify-center rounded-md transition-all duration-300 ease-in-out"
              :class="displayMode === 'list' ? 'text-gray-800' : 'text-gray-500 hover:text-gray-700'"
              title="列表式顯示"
            >
              <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Batch Actions -->
        <div v-if="selectedItems.length > 0" class="flex items-center space-x-2">
          <span class="text-xs sm:text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded-full">
            <span class="sm:hidden">{{ selectedItems.length }} 項</span>
            <span class="hidden sm:inline">已選擇 {{ selectedItems.length }} 項</span>
          </span>
          <button 
            @click="handleBatchDelete"
            class="btn btn-danger btn-sm"
          >
            <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
            <span class="hidden sm:inline">批量刪除</span>
            <span class="sm:hidden">刪除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 sm:px-0 lg:px-0 py-4 sm:py-8">
      <!-- Filter Section -->
      <div v-if="filteredDatasets.length > 0" class="pr-0 sm:pr-4 pb-6 w-full sm:w-auto">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <!-- Filter Controls -->
          <div class="w-full sm:w-auto">
            <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
              <!-- Search Input -->
              <div class="flex-1 sm:flex-none sm:w-64 w-full sm:w-auto">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                </div>
                <input
                  v-model="filters.search"
                  type="text"
                  placeholder="搜尋指令、輸出或模型..."
                  class="block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  @input="applyFilters"
                />
              </div>
              
              <!-- Status Filter -->
              <div class="flex-1 sm:flex-none sm:w-40 w-full sm:w-auto">
                <select
                  v-model="filters.status"
                  @change="applyFilters"
                  class="block w-full sm:w-40 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
                >
                  <option value="">所有狀態</option>
                  <option value="pending">待審核</option>
                  <option value="reviewing">審核中</option>
                  <option value="done">已完成</option>
                  <option value="regenerating">重新生成中</option>
                </select>
              </div>
              
              <!-- Model Filter -->
              <div class="flex-1 sm:flex-none sm:w-40 w-full sm:w-auto">
                <select
                  v-model="filters.model"
                  @change="applyFilters"
                  class="block w-full sm:w-40 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
                >
                  <option value="">所有模型</option>
                  <option v-for="model in availableModels" :key="model" :value="model">{{ model }}</option>
                </select>
              </div>
              
              <!-- Clear Filters Button -->
              <button
                v-if="hasActiveFilters"
                @click="clearFilters"
                class="btn btn-secondary btn-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span class="hidden sm:inline">清除篩選</span>
                <span class="sm:hidden">清除</span>
              </button>
            </div>
          </div>
          
          <!-- Results Count -->
          <div class="text-sm text-gray-600 flex justify-center w-full sm:w-auto">
            <span v-if="filteredDatasets.length === datasets.length">
              共 {{ datasets.length }} 筆資料
            </span>
            <span v-else>
              顯示 {{ filteredDatasets.length }} / {{ datasets.length }} 筆資料
            </span>
          </div>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-12 sm:py-16">
        <div class="relative">
          <div class="w-12 h-12 sm:w-16 sm:h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-6 h-6 sm:w-8 sm:h-8 bg-white rounded-full"></div>
          </div>
        </div>
        <p class="mt-4 text-base sm:text-lg font-medium text-gray-700">載入資料中...</p>
        <p class="mt-2 text-sm text-gray-500">請稍候，正在獲取最新資料</p>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="filteredDatasets.length === 0" class="flex flex-col items-center justify-center py-12 sm:py-16">
        <div class="w-16 h-16 sm:w-24 sm:h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4 sm:mb-6">
          <svg class="w-8 h-8 sm:w-12 sm:h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
          {{ hasActiveFilters ? '沒有符合篩選條件的資料' : '沒有待審核資料' }}
        </h3>
        <p class="text-gray-500 text-center max-w-md mb-4 sm:mb-6 text-sm sm:text-base">
          {{ hasActiveFilters ? '請嘗試調整篩選條件或清除篩選來查看所有資料。' : '目前沒有需要審核的資料集。您可以點擊「新增資料」按鈕開始新增資料。' }}
        </p>
        <div class="flex flex-col sm:flex-row gap-2">
          <button v-if="hasActiveFilters" @click="clearFilters" class="btn btn-secondary px-4 py-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            <span>清除篩選</span>
          </button>
          <button @click="openModal()" class="btn btn-primary px-4 py-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>{{ hasActiveFilters ? '新增資料' : '新增第一筆資料' }}</span>
          </button>
        </div>
      </div>
      
      <!-- Data Content -->
      <div v-else>
        <!-- Display Mode Content -->
        <transition 
          name="display-mode" 
          mode="out-in"
          appear
        >
          <!-- Card View -->
          <div v-if="displayMode === 'card'" key="card" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <transition-group 
              name="card-item" 
              tag="div" 
              class="contents"
            >
              <div 
                v-for="(item, index) in filteredDatasets" 
                :key="item.id" 
                class="card"
                :class="{ 'ring-2 ring-blue-500': selectedItems.includes(item.id) }"
                :style="{ animationDelay: `${index * 50}ms` }"
              >
              <!-- Header -->
              <div class="card-header">
                <div class="flex justify-between items-start mb-3">
                  <div class="flex items-center space-x-2 sm:space-x-3">
                    <input 
                      type="checkbox" 
                      :value="item.id" 
                      v-model="selectedItems"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-xs sm:text-sm font-medium text-gray-500">#{{ item.id }}</span>
                    <!-- Status Badge -->
                    <span :class="getStatusBadgeClass(item.review_status)" class="status-badge">
                      {{ getStatusText(item.review_status) }}
                    </span>
                  </div>
                  <div class="flex space-x-1 sm:space-x-2">
                    <button @click="openModal(item)" class="btn btn-primary btn-sm">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                      </svg>
                      <span class="hidden sm:inline">編輯</span>
                    </button>
                    <button @click="handleDelete(item.id)" class="btn btn-danger btn-sm">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                      <span class="hidden sm:inline">刪除</span>
                    </button>
                  </div>
                </div>
                
                <!-- Stats -->
                <div class="flex justify-between items-center">
                  <div class="flex space-x-3 sm:space-x-4 text-xs sm:text-sm">
                    <span class="text-green-600 font-medium">通過: {{ item.accept_count }}</span>
                    <button 
                      @click="viewRejectionReasons(item)" 
                      :class="[item.reject_count > 0 ? 'text-red-600 hover:text-red-900 font-medium' : 'text-gray-400 cursor-not-allowed']"
                      :disabled="item.reject_count === 0"
                    >
                      拒絕: {{ item.reject_count }}
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Content -->
              <div class="card-body">
                <div class="space-y-3 sm:space-y-4">
                  <!-- Instruction -->
                  <div v-if="item.instruction">
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-green-500 rounded-full mr-2"></span>
                      指令 (Instruction)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <p class="text-xs sm:text-sm text-gray-800 line-clamp-3">{{ item.instruction }}</p>
                    </div>
                  </div>
                  
                  <!-- Output -->
                  <div>
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-blue-500 rounded-full mr-2"></span>
                      輸出 (Output)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <p class="text-xs sm:text-sm text-gray-800 line-clamp-4">{{ item.output }}</p>
                    </div>
                  </div>
                  
                  <!-- System Prompt (if exists) -->
                  <div v-if="item.system">
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-purple-500 rounded-full mr-2"></span>
                      系統提示 (System)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <p class="text-xs sm:text-sm text-gray-800 line-clamp-2">{{ item.system }}</p>
                    </div>
                  </div>
                  
                  <!-- Input (if exists) -->
                  <div v-if="item.input">
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-yellow-500 rounded-full mr-2"></span>
                      輸入 (Input)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <p class="text-xs sm:text-sm text-gray-800 line-clamp-2">{{ item.input }}</p>
                    </div>
                  </div>
                  
                  <!-- Model Name (if exists) -->
                  <div v-if="item.model_name">
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-indigo-500 rounded-full mr-2"></span>
                      模型 (Model)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <p class="text-xs sm:text-sm text-gray-800">{{ item.model_name }}</p>
                    </div>
                  </div>
                  
                  <!-- History (if exists) -->
                  <div v-if="item.history && item.history.length > 0">
                    <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-2 flex items-center">
                      <span class="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-orange-500 rounded-full mr-2"></span>
                      對話歷史 (History)
                    </h4>
                    <div class="bg-gray-50 rounded-md p-2 sm:p-3">
                      <div class="space-y-2">
                        <div v-for="(conversation, index) in item.history" :key="index" class="text-xs sm:text-sm">
                          <div class="flex items-start space-x-2">
                            <div class="flex-shrink-0 w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center">
                              <span class="text-xs font-bold text-orange-600">{{ index + 1 }}</span>
                            </div>
                            <div class="flex-1 space-y-1">
                              <div class="bg-white border border-orange-200 rounded p-2">
                                <div class="text-orange-600 font-medium text-xs mb-1">問題:</div>
                                <div class="text-gray-700 text-xs">{{ Array.isArray(conversation) && conversation.length > 0 ? conversation[0] : conversation }}</div>
                              </div>
                              <div class="bg-white border border-orange-200 rounded p-2">
                                <div class="text-orange-600 font-medium text-xs mb-1">回答:</div>
                                <div class="text-gray-700 text-xs">{{ Array.isArray(conversation) && conversation.length > 1 ? conversation[1] : '' }}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Footer -->
              <div class="card-footer">
                <button 
                  @click="handleManualRegenerate(item)" 
                  :disabled="item.review_status === 'regenerating'"
                  :class="[
                    item.review_status === 'regenerating'
                      ? 'btn btn-secondary btn-sm opacity-50 cursor-not-allowed'
                      : 'btn btn-warning btn-sm'
                  ]"
                  class="w-full"
                >
                  <svg v-if="item.review_status === 'regenerating'" class="animate-spin h-3 w-3 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else class="h-3 w-3 sm:h-4 sm:w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  <span class="text-xs sm:text-sm">{{ item.review_status === 'regenerating' ? '重新生成中...' : '手動重新生成' }}</span>
                </button>
              </div>
            </div>
          </transition-group>
          </div>
          
          <!-- List View -->
          <div v-else key="list" class="card">
            <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 sm:px-6 py-3 text-left">
                    <input 
                      type="checkbox" 
                      @change="toggleSelectAll"
                                      :checked="selectedItems.length === filteredDatasets.length && filteredDatasets.length > 0"
                :indeterminate="selectedItems.length > 0 && selectedItems.length < filteredDatasets.length"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">狀態</th>
                  <th class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">指令</th>
                  <th class="hidden lg:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">輸入</th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">輸出</th>
                  <th class="hidden md:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">模型</th>
                  <th class="hidden lg:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">歷史</th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">統計</th>
                  <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in filteredDatasets" :key="item.id" class="hover:bg-gray-50 transition-colors duration-150">
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
                    <input 
                      type="checkbox" 
                      :value="item.id" 
                      v-model="selectedItems"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-xs sm:text-sm font-medium text-gray-900">
                    #{{ item.id }}
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
                    <span :class="getStatusBadgeClass(item.review_status)" class="status-badge">
                      {{ getStatusText(item.review_status) }}
                    </span>
                  </td>
                  <td class="hidden sm:table-cell px-6 py-4 text-xs sm:text-sm text-gray-900 max-w-xs">
                    <div class="truncate" :title="item.instruction">{{ item.instruction || '-' }}</div>
                  </td>
                  <td class="hidden lg:table-cell px-6 py-4 text-xs sm:text-sm text-gray-900 max-w-xs">
                    <div class="truncate" :title="item.input">{{ item.input || '-' }}</div>
                  </td>
                  <td class="px-3 sm:px-6 py-4 text-xs sm:text-sm text-gray-900 max-w-xs">
                    <div class="truncate" :title="item.output">{{ item.output }}</div>
                  </td>
                  <td class="hidden md:table-cell px-6 py-4 text-xs sm:text-sm text-gray-900">
                    <div class="truncate" :title="item.model_name">{{ item.model_name || '-' }}</div>
                  </td>
                  <td class="hidden lg:table-cell px-6 py-4 text-xs sm:text-sm text-gray-900">
                    <div v-if="item.history && item.history.length > 0" class="truncate" :title="`${item.history.length} 輪對話`">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                        {{ item.history.length }} 輪
                      </span>
                    </div>
                    <div v-else class="text-gray-400">-</div>
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-xs sm:text-sm text-gray-500">
                    <div class="space-y-1">
                      <div class="text-green-600">通過: {{ item.accept_count }}</div>
                      <div class="text-red-600">拒絕: {{ item.reject_count }}</div>
                    </div>
                  </td>
                  <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
                    <div class="flex flex-col sm:flex-row space-y-1 sm:space-y-0 sm:space-x-2">
                      <button @click="openModal(item)" class="btn btn-primary btn-sm">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                        </svg>
                        <span class="hidden sm:inline">編輯</span>
                      </button>
                      <button @click="handleDelete(item.id)" class="btn btn-danger btn-sm">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                        <span class="hidden sm:inline">刪除</span>
                      </button>
                      <button @click="viewRejectionReasons(item)" class="btn btn-warning btn-sm">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                        <span class="hidden sm:inline">拒絕原因</span>
                      </button>
                      <button 
                        v-if="item.review_status !== 'regenerating'"
                        @click="handleManualRegenerate(item)" 
                        class="btn btn-secondary btn-sm"
                      >
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                        </svg>
                        <span class="hidden sm:inline">重新生成</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        </transition>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content max-w-4xl max-h-[90vh] flex flex-col">
        <div class="modal-header bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-200 flex-shrink-0">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold text-gray-900">{{ editingItem ? '編輯資料' : '新增資料' }}</h3>
              <p class="text-sm text-gray-600">{{ editingItem ? '修改現有資料集內容' : '建立新的指令微調資料集' }}</p>
            </div>
          </div>
          <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="modal-body overflow-y-auto">
          <form @submit.prevent="handleSubmit" class="space-y-8">
            <!-- 主要內容區域 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <!-- 左側：核心欄位 -->
              <div class="space-y-6">
                <!-- 指令欄位 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    指令 (Instruction) <span class="text-red-500 ml-1">*</span>
                  </label>
                  <textarea 
                    v-model="form.instruction" 
                    rows="4" 
                    class="form-textarea focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                    required 
                    placeholder="請輸入明確的指令，例如：請解釋這個資安法規的適用範圍..."
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">這是AI需要執行的主要任務</p>
                </div>
                
                <!-- 輸出欄位 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    輸出 (Output) <span class="text-red-500 ml-1">*</span>
                  </label>
                  <textarea 
                    v-model="form.output" 
                    rows="6" 
                    class="form-textarea focus:ring-2 focus:ring-green-500 focus:border-green-500" 
                    required 
                    placeholder="請輸入期望的輸出結果..."
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">這是AI應該產生的理想回答</p>
                </div>
                
                <!-- 輸入內容 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-yellow-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                    輸入內容 (Input)
                  </label>
                  <textarea 
                    v-model="form.input" 
                    rows="3" 
                    class="form-textarea focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500" 
                    placeholder="可選的輸入內容或上下文..."
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">提供額外的上下文或輸入資訊</p>
                </div>
              </div>
              
              <!-- 右側：輔助欄位 -->
              <div class="space-y-6">
                <!-- 系統提示 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                    系統提示 (System)
                  </label>
                  <textarea 
                    v-model="form.system" 
                    rows="3" 
                    class="form-textarea focus:ring-2 focus:ring-purple-500 focus:border-purple-500" 
                    placeholder="設定AI的角色或行為模式..."
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">定義AI應該扮演的角色或行為</p>
                </div>
                
                <!-- 模型名稱 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-indigo-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
                    </svg>
                    模型名稱 (Model Name)
                  </label>
                  <input 
                    v-model="form.model_name" 
                    type="text" 
                    class="form-input focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" 
                    placeholder="例如：llama3, qwen2.5, gemma2" 
                  />
                  <p class="text-xs text-gray-500 mt-1">記錄生成此資料所使用的AI模型名稱</p>
                </div>
                
                <!-- 資料來源 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    資料來源 (Source)
                  </label>
                  <textarea 
                    v-model="form.source" 
                    rows="3" 
                    class="form-textarea focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                    placeholder="每行一個資料來源&#10;例如：資通安全管理法第15條&#10;資安事件通報及應變辦法"
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">列出資料的來源法規或文件</p>
                </div>
                
                <!-- 歷史紀錄 -->
                <div class="form-group">
                  <label class="form-label flex items-center">
                    <svg class="w-4 h-4 text-gray-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    歷史紀錄 (History)
                  </label>
                  <textarea 
                    v-model="form.history" 
                    rows="3" 
                    class="form-textarea focus:ring-2 focus:ring-gray-500 focus:border-gray-500 font-mono text-sm" 
                    placeholder='[["問題1", "回答1"], ["問題2", "回答2"]]'
                  ></textarea>
                  <p class="text-xs text-gray-500 mt-1">二維陣列格式的對話歷史紀錄，格式為 [指令, 回答]</p>
                </div>
              </div>
            </div>
            
            <!-- 錯誤訊息 -->
            <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <p class="text-red-700 text-sm font-medium">{{ error }}</p>
              </div>
            </div>
          </form>
        </div>
        
        <div class="modal-footer bg-gray-50 border-t border-gray-200 flex-shrink-0">
          <div class="flex justify-between items-center w-full">
            <div class="text-sm text-gray-500">
              <span class="text-red-500">*</span> 為必填欄位
            </div>
            <div class="flex space-x-3">
              <button 
                type="button" 
                @click="showModal = false" 
                class="btn btn-secondary px-6 py-2.5 hover:bg-gray-600 transition-colors"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                取消
              </button>
              <button 
                type="submit" 
                @click="handleSubmit" 
                class="btn btn-primary px-6 py-2.5 hover:bg-blue-700 transition-colors shadow-lg"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ editingItem ? '更新資料' : '新增資料' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rejection Reasons Modal -->
    <div v-if="showRejectionModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-xl font-bold text-gray-900">查看拒絕原因 (ID: {{ selectedDataset.id }})</h3>
          <button @click="closeRejectionModal" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div v-if="rejectionLoading" class="flex flex-col items-center justify-center py-10">
            <div class="loading-spinner w-8 h-8"></div>
            <p class="mt-4 text-gray-600">載入拒絕原因中...</p>
          </div>
          
          <div v-else-if="rejectionReasons.length === 0" class="text-center py-10">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h4 class="text-lg font-medium text-gray-900 mb-2">沒有拒絕紀錄</h4>
            <p class="text-gray-500">此資料集目前沒有被拒絕的紀錄。</p>
          </div>
          
          <div v-else class="space-y-4">
            <div class="flex items-center space-x-2 mb-4">
              <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              <span class="text-lg font-medium text-gray-900">拒絕原因列表</span>
            </div>
            
            <div class="max-h-96 overflow-y-auto space-y-3">
              <div v-for="reason in rejectionReasons" :key="reason.id" class="card">
                <div class="card-body">
                  <p class="text-gray-800 mb-3">{{ reason.comment || '沒有提供原因' }}</p>
                  <div class="flex justify-between items-center text-xs text-gray-500">
                    <span>審核者: {{ reason.reviewer_username }}</span>
                    <span>{{ new Date(reason.timestamp).toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeRejectionModal" class="btn btn-secondary">
            <span>關閉</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Batch Add Modal -->
    <div v-if="showBatchModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-xl font-bold text-gray-900">批量新增資料</h3>
          <button @click="closeBatchModal" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Input Methods -->
          <div class="mb-6">
            <div class="flex space-x-4 mb-4">
              <button 
                @click="batchInputMethod = 'text'"
                :class="[batchInputMethod === 'text' ? 'btn btn-primary' : 'btn btn-secondary']"
                class="px-4 py-1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span>貼上 JSON 文字</span>
              </button>
              <button 
                @click="batchInputMethod = 'file'"
                :class="[batchInputMethod === 'file' ? 'btn btn-primary' : 'btn btn-secondary']"
                class="px-4 py-1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                <span>上傳 JSON 檔案</span>
              </button>
            </div>
          </div>
          
          <!-- Text Input -->
          <div v-if="batchInputMethod === 'text'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                JSON 格式資料 (支援多筆資料的陣列格式)
              </label>
              <textarea 
                v-model="batchJsonText" 
                rows="15" 
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 font-mono text-sm"
                placeholder='[
  {
    "instruction": "這個資安獎懲辦法是根據什麼法律訂出來的？",
    "input": "為什麼政府要特別訂資安獎懲規定？",
    "output": "這是根據《資通安全管理法》第15條與第19條訂定的...",
    "system": "說明本辦法與母法的法律關係。",
    "history": [["什麼是資安法規？", "資安法規是保護資訊安全的相關法律規定"]],
    "source": ["公務機關所屬人員資通安全事項獎懲辦法第1條"],
    "model_name": "llama3"
  }
]'
              ></textarea>
            </div>
          </div>
          
          <!-- File Input -->
          <div v-if="batchInputMethod === 'file'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                選擇 JSON 檔案
              </label>
              <input 
                type="file" 
                @change="handleFileUpload" 
                accept=".json"
                class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
              />
              <p class="text-sm text-gray-500 mt-1">支援 .json 檔案格式</p>
            </div>
          </div>
        </div>
        
        <!-- Preview -->
        <div v-if="batchPreview.length > 0" class="mb-6 mx-4">
          <h4 class="text-lg font-semibold mb-3">預覽 ({{ batchPreview.length }} 筆資料)</h4>
          <div class="max-h-64 overflow-y-auto border border-gray-200 rounded-lg p-4 bg-gray-50">
            <div v-for="(item, index) in batchPreview" :key="index" class="mb-3 p-3 bg-white rounded border">
              <div class="text-sm">
                <div class="font-medium text-gray-800">#{{ index + 1 }}</div>
                <div class="text-gray-600 mt-1">
                  <div><strong>指令:</strong> {{ item.instruction || '無' }}</div>
                  <div><strong>輸入:</strong> {{ item.input || '無' }}</div>
                  <div><strong>輸出:</strong> {{ item.output || '無' }}</div>
                  <div><strong>模型:</strong> {{ item.model_name || '無' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Error Display -->
        <div v-if="batchError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700 text-sm">{{ batchError }}</p>
        </div>
        
        <!-- Actions -->
        <div class="flex justify-between items-center mb-4 mx-4">
          <div class="flex space-x-3">
            <button 
              @click="parseBatchData" 
              :disabled="!batchJsonText && batchInputMethod === 'text'"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              解析資料
            </button>
            <button 
              @click="clearBatchData" 
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
            >
              清除
            </button>
          </div>
          <div class="flex space-x-3">
            <button @click="closeBatchModal" class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400">
              取消
            </button>
            <button 
              @click="submitBatchData" 
              :disabled="batchPreview.length === 0 || batchSubmitting"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {{ batchSubmitting ? '新增中...' : `確認新增 ${batchPreview.length} 筆資料` }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate from Regulations Modal -->
    <div v-if="showGenerateModal" class="modal-overlay">
      <div class="modal-content max-w-6xl max-h-[90vh] flex flex-col">
        <div class="modal-header bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-200 flex-shrink-0">
          <h3 class="text-xl font-bold text-gray-900">從法規生成資料</h3>
          <button @click="closeGenerateModal" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="modal-body overflow-y-auto flex-1">
          <!-- Step 1: Select Regulations -->
          <div v-if="generateStep === 1" class="space-y-6">
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
              <h4 class="text-lg font-semibold text-gray-900">選擇法規條文</h4>
            </div>
            
            <!-- Generation Type Selection -->
            <div class="mb-6">
              <h5 class="font-medium text-gray-700 mb-3">生成模式</h5>
              <div class="grid grid-cols-2 gap-4">
                <div 
                  @click="generationType = 'single'"
                  :class="[
                    'p-4 rounded-lg border cursor-pointer transition-all duration-200',
                    generationType === 'single'
                      ? 'bg-blue-50 border-blue-300 ring-2 ring-blue-200'
                      : 'bg-white border-gray-200 hover:bg-gray-50'
                  ]"
                >
                  <div class="flex items-center space-x-3">
                    <input 
                      type="radio" 
                      value="single"
                      v-model="generationType"
                      class="rounded-full border-gray-300 text-blue-600 focus:ring-blue-500"
                      @click.stop
                    />
                    <div>
                      <div class="font-medium text-gray-900">單筆生成</div>
                      <div class="text-sm text-gray-500">生成一筆資料</div>
                    </div>
                  </div>
                </div>
                <div 
                  @click="generationType = 'batch'"
                  :class="[
                    'p-4 rounded-lg border cursor-pointer transition-all duration-200',
                    generationType === 'batch'
                      ? 'bg-blue-50 border-blue-300 ring-2 ring-blue-200'
                      : 'bg-white border-gray-200 hover:bg-gray-50'
                  ]"
                >
                  <div class="flex items-center space-x-3">
                    <input 
                      type="radio" 
                      value="batch"
                      v-model="generationType"
                      class="rounded-full border-gray-300 text-blue-600 focus:ring-blue-500"
                      @click.stop
                    />
                    <div>
                      <div class="font-medium text-gray-900">批量生成</div>
                      <div class="text-sm text-gray-500">批量生成多筆資料</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Batch Generation Settings -->
            <div v-if="generationType === 'batch'" class="mb-6">
              <h5 class="font-medium text-gray-700 mb-3">批量生成設定</h5>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">生成數量</label>
                  <input 
                    v-model.number="batchSize" 
                    type="number" 
                    min="1" 
                    max="20"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="1-20"
                  />
                  <p class="text-xs text-gray-500 mt-1">建議一次生成 1-20 筆資料</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">法規選擇方式</label>
                  <div class="space-y-2">
                    <label class="flex items-center">
                      <input 
                        v-model="randomSelection" 
                        type="checkbox" 
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span class="ml-2 text-sm text-gray-700">隨機選擇法規</span>
                    </label>
                    <p class="text-xs text-gray-500">
                      {{ randomSelection ? '啟用後系統會自動隨機選擇法規，無需手動選擇' : '啟用後每次生成會隨機選擇 1-3 個法規' }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Model Selection -->
            <div class="mb-6">
              <h5 class="font-medium text-gray-700 mb-3">選擇生成模型</h5>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <div 
                  v-for="model in availableModels" 
                  :key="model"
                  @click="toggleModelSelection(model)"
                  :class="[
                    'p-3 rounded-lg border cursor-pointer transition-all duration-200 text-center',
                    selectedModel === model
                      ? 'bg-blue-50 border-blue-300 ring-2 ring-blue-200'
                      : 'bg-white border-gray-200 hover:bg-gray-50'
                  ]"
                >
                  <div class="flex items-center justify-center space-x-2">
                    <input 
                      type="radio" 
                      :value="model"
                      v-model="selectedModel"
                      class="rounded-full border-gray-300 text-blue-600 focus:ring-blue-500"
                      @click.stop
                    />
                    <span class="text-sm font-medium text-gray-700">{{ model }}</span>
                  </div>
                </div>
              </div>
              <p class="text-xs text-gray-500 mt-2">選擇要使用的 AI 模型來生成資料</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Available Regulations -->
              <div class="space-y-4">
                <h5 class="font-medium text-gray-700">
                  可選法規 ({{ availableRegulations.length }})
                  <span v-if="generationType === 'batch' && randomSelection" class="text-sm text-blue-600 font-normal">
                    - 隨機選擇模式
                  </span>
                </h5>
                <div 
                  :class="[
                    'max-h-96 overflow-y-auto border rounded-lg p-4',
                    generationType === 'batch' && randomSelection
                      ? 'bg-gray-100 border-gray-300 h-64 flex items-center justify-center'
                      : 'bg-gray-50 border-gray-200'
                  ]"
                >
                  <div v-if="regulationsLoading" class="flex items-center justify-center py-8">
                    <div class="loading-spinner w-6 h-6"></div>
                    <span class="ml-2 text-gray-600">載入法規中...</span>
                  </div>
                  <div v-else-if="availableRegulations.length === 0" class="text-center py-8 text-gray-500">
                    沒有可用的法規
                  </div>
                  <div v-else-if="generationType === 'batch' && randomSelection" class="text-center py-8">
                    <div class="text-gray-500 mb-2">
                      <svg class="w-12 h-12 mx-auto mb-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                      <p class="text-sm">隨機選擇模式已啟用</p>
                      <p class="text-xs mt-1">系統將自動從所有法規中隨機選擇</p>
                    </div>
                  </div>
                  <div v-else class="space-y-2">
                    <div 
                      v-for="regulation in availableRegulations" 
                      :key="regulation.id"
                      @click="toggleRegulationSelection(regulation.id)"
                      :class="[
                        'p-3 rounded-lg border cursor-pointer transition-all duration-200',
                        selectedRegulations.includes(regulation.id)
                          ? 'bg-blue-50 border-blue-300 ring-2 ring-blue-200'
                          : 'bg-white border-gray-200 hover:bg-gray-50'
                      ]"
                    >
                      <div class="flex items-start space-x-3">
                        <input 
                          type="checkbox" 
                          :checked="selectedRegulations.includes(regulation.id)"
                          class="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          @click.stop
                          @change="toggleRegulationSelection(regulation.id)"
                        />
                        <div class="flex-1">
                          <div class="font-medium text-gray-900">{{ regulation.title }}第{{ regulation.number }}條</div>
                          <div class="text-sm text-gray-600 mt-1 line-clamp-2">{{ regulation.content }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Selected Regulations -->
              <div class="space-y-4">
                <h5 class="font-medium text-gray-700">
                  已選法規 ({{ selectedRegulations.length }})
                  <span v-if="generationType === 'batch' && randomSelection" class="text-sm text-blue-600 font-normal">
                    - 隨機選擇模式
                  </span>
                </h5>
                <div 
                  :class="[
                    'max-h-96 overflow-y-auto border rounded-lg p-4',
                    generationType === 'batch' && randomSelection
                      ? 'bg-blue-100 border-blue-300 h-64 flex items-center justify-center'
                      : 'bg-blue-50 border-gray-200'
                  ]"
                >
                  <div v-if="generationType === 'batch' && randomSelection" class="text-center py-8">
                    <div class="text-blue-600 mb-2">
                      <svg class="w-12 h-12 mx-auto mb-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                      </svg>
                      <p class="text-sm font-medium">隨機選擇模式</p>
                      <p class="text-xs mt-1">系統將自動從所有法規中隨機選擇 1-3 個</p>
                      <p class="text-xs mt-1">無需手動選擇法規</p>
                    </div>
                  </div>
                  <div v-else-if="selectedRegulations.length === 0" class="text-center py-8 text-gray-500">
                    請選擇法規條文
                  </div>
                  <div v-else class="space-y-3">
                    <div 
                      v-for="regulationId in selectedRegulations" 
                      :key="regulationId"
                      class="p-3 bg-white rounded-lg border border-blue-200"
                    >
                      <div class="flex items-start justify-between">
                        <div class="flex-1">
                          <div class="font-medium text-gray-900">
                            {{ getRegulationById(regulationId)?.title }}第{{ getRegulationById(regulationId)?.number }}條
                          </div>
                          <div class="text-sm text-gray-600 mt-1 line-clamp-2">
                            {{ getRegulationById(regulationId)?.content }}
                          </div>
                        </div>
                        <button 
                          @click="removeRegulationSelection(regulationId)"
                          class="ml-2 text-red-500 hover:text-red-700"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Generate Button -->
            <div class="flex justify-center pt-6 border-t border-gray-200">
              <button 
                @click="generateData" 
                :disabled="(!selectedModel || generating || (generationType === 'batch' && (!batchSize || batchSize < 1 || batchSize > 20)) || (!randomSelection && selectedRegulations.length === 0))"
                class="btn btn-primary px-8 py-3"
              >
                <svg v-if="generating" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                <span>{{ generating ? '生成中...' : (generationType === 'batch' ? `批量生成 ${batchSize} 筆資料` : '生成資料') }}</span>
              </button>
            </div>
          </div>
          
          <!-- Step 2: Generated Result -->
          <div v-if="generateStep === 2" class="space-y-6">
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
              <h4 class="text-lg font-semibold text-gray-900">
                {{ generationType === 'batch' ? '批量生成結果' : '生成結果' }}
              </h4>
            </div>
            
            <div v-if="generating" class="flex flex-col items-center justify-center py-12">
              <div class="loading-spinner w-12 h-12"></div>
              <p class="mt-4 text-lg font-medium text-gray-700">
                {{ generationType === 'batch' ? `正在批量生成 ${batchSize} 筆資料...` : '正在生成資料...' }}
              </p>
              <p class="mt-2 text-sm text-gray-500">請稍候，AI正在根據選取的法規生成內容</p>
            </div>
            
            <div v-else-if="generatedData || batchGeneratedData" class="space-y-6">
              <!-- Batch Generation Summary -->
              <div v-if="generationType === 'batch' && batchGeneratedData" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <h5 class="font-medium text-blue-900">批量生成摘要</h5>
                    <p class="text-sm text-blue-700 mt-1">
                      成功生成 {{ batchGeneratedData.success_count }} 筆，失敗 {{ batchGeneratedData.failed_count }} 筆
                    </p>
                  </div>
                  <div class="text-right">
                    <div class="text-2xl font-bold text-blue-600">{{ batchGeneratedData.success_count }}</div>
                    <div class="text-sm text-blue-500">成功筆數</div>
                  </div>
                </div>
              </div>
              <!-- Generated Content -->
              <div v-if="generationType === 'single'">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div class="space-y-4">
                    <h5 class="font-medium text-gray-700">生成的內容</h5>
                    <div class="space-y-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">指令 (Instruction)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ generatedData.instruction }}</div>
                      </div>
                      <div v-if="generatedData.input">
                        <label class="block text-sm font-medium text-gray-700 mb-2">輸入 (Input)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ generatedData.input }}</div>
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">輸出 (Output)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800 whitespace-pre-wrap">{{ generatedData.output }}</div>
                      </div>
                      <div v-if="generatedData.system">
                        <label class="block text-sm font-medium text-gray-700 mb-2">系統提示 (System)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ generatedData.system }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="space-y-4">
                    <h5 class="font-medium text-gray-700">資料來源</h5>
                    <div class="space-y-3">
                      <div 
                        v-for="source in generatedData.source" 
                        :key="source"
                        class="p-3 bg-blue-50 rounded-lg border border-blue-200"
                      >
                        <div class="text-sm text-gray-800">{{ source }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Batch Generated Content -->
              <div v-else-if="generationType === 'batch' && batchGeneratedData" class="space-y-6">
                <div class="flex items-center justify-between mb-4">
                  <h5 class="font-medium text-gray-700">逐筆審批 ({{ currentBatchIndex + 1 }}/{{ batchGeneratedData.datasets.length }})</h5>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="previousBatchItem" 
                      :disabled="currentBatchIndex === 0"
                      class="btn btn-secondary btn-sm"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                      </svg>
                      上一筆
                    </button>
                    <button 
                      @click="nextBatchItem" 
                      :disabled="currentBatchIndex === batchGeneratedData.datasets.length - 1"
                      class="btn btn-secondary btn-sm"
                    >
                      下一筆
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div class="space-y-4">
                    <h5 class="font-medium text-gray-700">生成的內容</h5>
                    <div class="space-y-4">
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">指令 (Instruction)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ currentBatchData.instruction }}</div>
                      </div>
                      <div v-if="currentBatchData.input">
                        <label class="block text-sm font-medium text-gray-700 mb-2">輸入 (Input)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ currentBatchData.input }}</div>
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">輸出 (Output)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800 whitespace-pre-wrap">{{ currentBatchData.output }}</div>
                      </div>
                      <div v-if="currentBatchData.system">
                        <label class="block text-sm font-medium text-gray-700 mb-2">系統提示 (System)</label>
                        <div class="bg-gray-50 rounded-md p-3 text-sm text-gray-800">{{ currentBatchData.system }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="space-y-4">
                    <h5 class="font-medium text-gray-700">資料來源</h5>
                    <div class="space-y-3">
                      <div 
                        v-for="source in currentBatchData.source" 
                        :key="source"
                        class="p-3 bg-blue-50 rounded-lg border border-blue-200"
                      >
                        <div class="text-sm text-gray-800">{{ source }}</div>
                      </div>
                    </div>
                    
                    <!-- Batch Item Selection -->
                    <div class="mt-6">
                      <h6 class="font-medium text-gray-700 mb-3">選擇此筆資料</h6>
                      <div class="flex space-x-2">
                        <button 
                          @click="selectBatchItem(currentBatchIndex, true)"
                          :class="[
                            'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                            batchSelectedItems[currentBatchIndex] === true
                              ? 'bg-green-100 text-green-800 border border-green-300'
                              : 'bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200'
                          ]"
                        >
                          ✓ 選擇
                        </button>
                        <button 
                          @click="selectBatchItem(currentBatchIndex, false)"
                          :class="[
                            'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                            batchSelectedItems[currentBatchIndex] === false
                              ? 'bg-red-100 text-red-800 border border-red-300'
                              : 'bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200'
                          ]"
                        >
                          ✗ 跳過
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Action Buttons -->
              <div class="flex justify-center space-x-4 pt-6 border-t border-gray-200">
                <!-- Single Generation Actions -->
                <template v-if="generationType === 'single'">
                  <button 
                    @click="regenerateData" 
                    :disabled="generating"
                    class="btn btn-warning px-4 py-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    <span>重新生成</span>
                  </button>
                  <button 
                    @click="confirmGeneratedData" 
                    :disabled="confirming"
                    class="btn btn-success px-4 py-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <span>{{ confirming ? '確認中...' : '確認加入' }}</span>
                  </button>
                </template>
                
                <!-- Batch Generation Actions -->
                <template v-else-if="generationType === 'batch'">
                  <button 
                    @click="regenerateBatchData" 
                    :disabled="generating"
                    class="btn btn-warning px-4 py-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    <span>重新生成</span>
                  </button>
                  <button 
                    @click="confirmBatchGeneratedData" 
                    :disabled="confirming || getSelectedBatchCount() === 0"
                    class="btn btn-success px-4 py-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <span>{{ confirming ? '確認中...' : `確認加入 (${getSelectedBatchCount()} 筆)` }}</span>
                  </button>
                </template>
                
                <button @click="closeGenerateModal" class="btn btn-secondary px-4 py-2">
                  <span>取消</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer bg-gray-50 border-t border-gray-200 flex-shrink-0">
          <div class="flex justify-between items-center w-full">
            <div class="text-sm text-gray-500">
              按 ESC 鍵可關閉此視窗
            </div>
            <div class="flex space-x-3">
              <button @click="closeGenerateModal" class="btn btn-secondary px-4 py-2">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                關閉
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'
import useConfirm from '../composables/useConfirm'

const { instance } = useAuth()
const toast = useToast()
const { confirm } = useConfirm()

const datasets = ref([])
const loading = ref(true)
const error = ref(null)
const pollingInterval = ref(null)
const isPolling = ref(false)

const getInitialForm = () => ({
  instruction: '',
  input: '',
  output: '',
  system: '',
  source: '',
  history: '[]', // Default to empty JSON array string
  model_name: '' // Default to empty model name
});

// For Add/Edit Modal
const showModal = ref(false)
const editingItem = ref(null)
const form = ref(getInitialForm());

// For Rejection Reasons Modal
const showRejectionModal = ref(false)
const rejectionLoading = ref(false)
const rejectionReasons = ref([])
const selectedDataset = ref(null)

// For Batch Add Modal
const showBatchModal = ref(false)
const batchInputMethod = ref('text') // 'text' or 'file'
const batchJsonText = ref('')
const batchPreview = ref([])
const batchError = ref('')
const batchSubmitting = ref(false)

// For Display Mode and Batch Operations
const displayMode = ref('card') // 'card' or 'list'
const selectedItems = ref([])

// For Generate from Regulations Modal
const showGenerateModal = ref(false)
const generateStep = ref(1) // 1 for select, 2 for generate
const availableRegulations = ref([])
const selectedRegulations = ref([])
const regulationsLoading = ref(false)
const generating = ref(false)
const generatedData = ref(null)
const confirming = ref(false)

// For Batch Generation
const generationType = ref('single') // 'single' or 'batch'
const batchSize = ref(5)
const randomSelection = ref(true)
const batchGeneratedData = ref(null)
const currentBatchIndex = ref(0)
const batchSelectedItems = ref({})

// For Model Selection
const availableModels = ref([])
const selectedModel = ref('')

// For Filtering
const filters = ref({
  search: '',
  status: '',
  model: ''
})

const filteredDatasets = computed(() => {
  let result = datasets.value

  // Search filter
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    result = result.filter(item => 
      item.instruction?.toLowerCase().includes(searchTerm) ||
      item.output?.toLowerCase().includes(searchTerm) ||
      item.model_name?.toLowerCase().includes(searchTerm) ||
      item.input?.toLowerCase().includes(searchTerm) ||
      item.system?.toLowerCase().includes(searchTerm)
    )
  }

  // Status filter
  if (filters.value.status) {
    result = result.filter(item => item.review_status === filters.value.status)
  }

  // Model filter
  if (filters.value.model) {
    result = result.filter(item => item.model_name === filters.value.model)
  }

  return result
})

const hasActiveFilters = computed(() => {
  return filters.value.search || filters.value.status || filters.value.model
})

const applyFilters = () => {
  // 篩選邏輯已在 computed 中處理
  // 這裡可以添加額外的邏輯，比如保存篩選條件到 localStorage
}

const clearFilters = () => {
  filters.value.search = ''
  filters.value.status = ''
  filters.value.model = ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待審核',
    'reviewing': '審核中',
    'done': '已完成',
    'regenerating': '重新生成中'
  }
  return statusMap[status] || status
}

const fetchDatasets = async () => {
  loading.value = true
  try {
    const response = await instance.get('/api/v1/datasets/')
    datasets.value = response.data
    
    // 更新可用的模型列表
    const models = [...new Set(datasets.value.map(item => item.model_name).filter(Boolean))]
    availableModels.value = models.sort()
    
    // 檢查是否有正在重新生成的資料
    const hasRegenerating = datasets.value.some(dataset => dataset.review_status === 'regenerating')
    
    // 如果有重新生成中的資料且尚未開始輪詢，則開始輪詢
    if (hasRegenerating && !isPolling.value) {
      startPolling()
    }
    // 如果沒有重新生成中的資料且正在輪詢，則停止輪詢
    else if (!hasRegenerating && isPolling.value) {
      stopPolling()
    }
  } catch (err) {
    error.value = '無法獲取資料列表。'
  } finally {
    loading.value = false
  }
}

// 開始輪詢重新生成狀態
const startPolling = () => {
  if (isPolling.value) return
  
  isPolling.value = true
  console.log('開始自動更新重新生成狀態...')
  
  pollingInterval.value = setInterval(async () => {
    try {
      const response = await instance.get('/api/v1/datasets/')
      const newDatasets = response.data
      
      // 檢查是否有狀態變化
      let hasChanges = false
      const oldRegeneratingCount = datasets.value.filter(d => d.review_status === 'regenerating').length
      const newRegeneratingCount = newDatasets.filter(d => d.review_status === 'regenerating').length
      
      // 檢查重新生成數量變化
      if (oldRegeneratingCount !== newRegeneratingCount) {
        hasChanges = true
      } else {
        // 檢查個別資料狀態變化
        for (let i = 0; i < newDatasets.length; i++) {
          const newDataset = newDatasets[i]
          const oldDataset = datasets.value.find(d => d.id === newDataset.id)
          
          if (!oldDataset || oldDataset.review_status !== newDataset.review_status) {
            hasChanges = true
            break
          }
        }
      }
      
      // 如果有變化，更新資料並顯示通知
      if (hasChanges) {
        console.log('檢測到狀態變化，更新資料...')
        datasets.value = newDatasets
        
        // 如果有重新生成完成的資料，顯示通知
        if (newRegeneratingCount < oldRegeneratingCount) {
          const completedCount = oldRegeneratingCount - newRegeneratingCount
          toast.success(`${completedCount} 筆資料重新生成完成！`)
          console.log(`${completedCount} 筆資料重新生成完成`)
        }
        
        // 如果沒有重新生成中的資料，停止輪詢
        if (newRegeneratingCount === 0) {
          console.log('所有重新生成完成，停止自動更新')
          stopPolling()
        }
      }
    } catch (err) {
      console.error('輪詢更新失敗:', err)
      // 如果連續失敗，停止輪詢避免無限重試
      if (err.response?.status === 401 || err.response?.status === 403) {
        console.log('認證失敗，停止自動更新')
        stopPolling()
      }
    }
  }, 3000) // 每3秒檢查一次
}

// 停止輪詢
const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
    console.log('停止自動更新')
  }
  isPolling.value = false
}

const openModal = (item = null) => {
  error.value = null
  if (item) {
    editingItem.value = item;
    // Handle source array for textarea
    const sourceAsString = Array.isArray(item.source) ? item.source.join('\n') : '';
    const historyAsString = JSON.stringify(item.history || [], null, 2);
    form.value = { ...item, source: sourceAsString, history: historyAsString };
  } else {
    editingItem.value = null;
    form.value = getInitialForm();
  }
  showModal.value = true
}

const handleSubmit = async () => {
  error.value = null;
  
  let historyPayload;
  try {
    historyPayload = JSON.parse(form.value.history);
  } catch (e) {
    error.value = "History 欄位的 JSON 格式錯誤。";
    return;
  }

  // Convert source textarea back to array
  const payload = {
    ...form.value,
    source: form.value.source.split('\n').filter(s => s.trim() !== ''),
    history: historyPayload
  };

  try {
    if (editingItem.value) {
      await instance.put(`/api/v1/datasets/${editingItem.value.id}`, payload);
    } else {
      await instance.post('/api/v1/datasets/', payload);
    }
    showModal.value = false;
    await fetchDatasets();
  } catch (err) {
    error.value = `操作失敗: ${err.response?.data?.detail || '未知錯誤'}`;
  }
}

const handleDelete = async (id) => {
  const confirmed = await confirm('刪除確認', '確定要刪除這筆資料嗎？此操作無法復原。')
  if (!confirmed) return
  
  error.value = null
  try {
    await instance.delete(`/api/v1/datasets/${id}`)
    await fetchDatasets()
    toast.success('資料已成功刪除。')
  } catch (err) {
    const errorMsg = `刪除失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
  }
}

const showRejections = async (item) => {
  selectedDataset.value = item
  showRejectionModal.value = true
  rejectionLoading.value = true
  rejectionReasons.value = []
  try {
    const response = await instance.get(`/api/v1/datasets/${item.id}/rejections`)
    rejectionReasons.value = response.data
  } catch (err) {
    const errorMsg = `無法獲取拒絕原因: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
  } finally {
    rejectionLoading.value = false
  }
}

const closeRejectionModal = () => {
  showRejectionModal.value = false
  rejectionReasons.value = []
  selectedDataset.value = null
}

const handleManualRegenerate = async (item) => {
  // 獲取可用模型
  let availableModels = []
  try {
    const response = await instance.get('/api/v1/settings/')
    if (response.data && response.data.ollama_models) {
      availableModels = response.data.ollama_models
    }
  } catch (err) {
    console.error('獲取可用模型失敗:', err)
  }

  if (availableModels.length === 0) {
    toast.error('沒有可用的模型，請先在系統設定中配置模型')
    return
  }

  // 如果有多個模型，讓用戶選擇
  let selectedModel = null
  if (availableModels.length === 1) {
    selectedModel = availableModels[0]
  } else {
    // 這裡可以實現一個簡單的模型選擇對話框
    // 暫時使用第一個模型
    selectedModel = availableModels[0]
    toast.info(`使用模型: ${selectedModel}`)
  }

  const confirmed = await confirm(
    '手動重新生成確認', 
    `確定要手動重新生成 ID ${item.id} 的資料嗎？\n使用模型: ${selectedModel}\n此操作將使用 AI 重新生成內容。`
  )
  if (!confirmed) return
  
  try {
    const response = await instance.post(`/api/v1/datasets/${item.id}/regenerate?model_name=${selectedModel}`, null, {
      timeout: 60000 // 60秒超時
    })
    toast.success('重新生成已開始，請稍候...')
    
    // 立即更新本地狀態為重新生成中
    const datasetIndex = datasets.value.findIndex(d => d.id === item.id)
    if (datasetIndex !== -1) {
      datasets.value[datasetIndex].review_status = 'regenerating'
    }
    
    // 如果尚未開始輪詢，則開始輪詢
    if (!isPolling.value) {
      startPolling()
    }
    
    console.log('手動重新生成已啟動:', response.data)
  } catch (err) {
    const errorMsg = `手動重新生成失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('手動重新生成失敗:', err)
  }
}

// Batch Add Functions
const openBatchModal = () => {
  showBatchModal.value = true
  batchError.value = ''
  batchPreview.value = []
  batchJsonText.value = ''
}

const closeBatchModal = () => {
  showBatchModal.value = false
  batchError.value = ''
  batchPreview.value = []
  batchJsonText.value = ''
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.type !== 'application/json' && !file.name.endsWith('.json')) {
    batchError.value = '請選擇有效的 JSON 檔案'
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      batchJsonText.value = e.target.result
      parseBatchData()
    } catch (err) {
      batchError.value = '檔案讀取失敗'
    }
  }
  reader.readAsText(file)
}

const parseBatchData = () => {
  batchError.value = ''
  batchPreview.value = []
  
  if (!batchJsonText.value.trim()) {
    batchError.value = '請輸入 JSON 資料'
    return
  }
  
  try {
    const data = JSON.parse(batchJsonText.value)
    
    if (!Array.isArray(data)) {
      batchError.value = 'JSON 資料必須是陣列格式'
      return
    }
    
    if (data.length === 0) {
      batchError.value = '陣列不能為空'
      return
    }
    
    // Validate each item
    const validData = []
    for (let i = 0; i < data.length; i++) {
      const item = data[i]
      
      if (!item.output) {
        batchError.value = `第 ${i + 1} 筆資料缺少必要的 "output" 欄位`
        return
      }
      
      // Normalize the data
      const normalizedItem = {
        instruction: item.instruction || '',
        input: item.input || '',
        output: item.output,
        system: item.system || '',
        history: Array.isArray(item.history) ? item.history : [],
        source: Array.isArray(item.source) ? item.source : []
      }
      
      // 驗證 history 格式
      if (normalizedItem.history.length > 0) {
        for (let j = 0; j < normalizedItem.history.length; j++) {
          const historyItem = normalizedItem.history[j]
          if (!Array.isArray(historyItem) || historyItem.length !== 2) {
            batchError.value = `第 ${i + 1} 筆資料的 history[${j}] 格式錯誤，應為 [指令, 回答] 格式`
            return
          }
        }
      }
      
      validData.push(normalizedItem)
    }
    
    batchPreview.value = validData
    console.log(`成功解析 ${validData.length} 筆資料`)
    
  } catch (err) {
    batchError.value = `JSON 格式錯誤: ${err.message}`
    console.error('JSON 解析錯誤:', err)
  }
}

const clearBatchData = () => {
  batchJsonText.value = ''
  batchPreview.value = []
  batchError.value = ''
}

const submitBatchData = async () => {
  if (batchPreview.value.length === 0) {
    batchError.value = '沒有可新增的資料'
    return
  }
  
  batchSubmitting.value = true
  batchError.value = ''
  
  try {
    // Use batch API endpoint for better performance
    const response = await instance.post('/api/v1/datasets/batch', batchPreview.value)
    
    toast.success(`成功新增 ${response.data.length} 筆資料`)
    closeBatchModal()
    await fetchDatasets() // Refresh the list
    
  } catch (err) {
    const errorMsg = `批量新增失敗: ${err.response?.data?.detail || '未知錯誤'}`
    batchError.value = errorMsg
    toast.error(errorMsg)
    console.error('批量新增失敗:', err)
  } finally {
    batchSubmitting.value = false
  }
}

// Batch Operations Functions
const toggleSelectAll = () => {
  if (selectedItems.value.length === filteredDatasets.value.length) {
    selectedItems.value = []
  } else {
    selectedItems.value = filteredDatasets.value.map(item => item.id)
  }
}

const handleBatchDelete = async () => {
  if (selectedItems.value.length === 0) {
    toast.error('請選擇要刪除的項目')
    return
  }
  
  const confirmed = await confirm(
    '批量刪除確認', 
    `確定要刪除選中的 ${selectedItems.value.length} 筆資料嗎？此操作無法復原。`
  )
  if (!confirmed) return
  
  try {
    const promises = selectedItems.value.map(id => 
      instance.delete(`/api/v1/datasets/${id}`)
    )
    
    await Promise.all(promises)
    
    toast.success(`成功刪除 ${selectedItems.value.length} 筆資料`)
    selectedItems.value = []
    await fetchDatasets() // Refresh the list
    
  } catch (err) {
    const errorMsg = `批量刪除失敗: ${err.response?.data?.detail || '未知錯誤'}`
    toast.error(errorMsg)
    console.error('批量刪除失敗:', err)
  }
}

// Status Helper Functions

const getStatusBadgeClass = (status) => {
  const classMap = {
    'pending': 'bg-blue-100 text-blue-800',
    'reviewing': 'bg-yellow-100 text-yellow-800',
    'done': 'bg-green-100 text-green-800',
    'regenerating': 'bg-orange-100 text-orange-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

// Generate from Regulations Functions
const fetchRegulations = async () => {
  regulationsLoading.value = true
  try {
    const response = await instance.get('/api/v1/legal-articles/')
    availableRegulations.value = response.data
  } catch (err) {
    error.value = `無法獲取法規列表: ${err.response?.data?.detail || '未知錯誤'}`
    toast.error(error.value)
  } finally {
    regulationsLoading.value = false
  }
}

// Computed properties for batch generation
const currentBatchData = computed(() => {
  if (batchGeneratedData.value && batchGeneratedData.value.datasets && batchGeneratedData.value.datasets[currentBatchIndex.value]) {
    return batchGeneratedData.value.datasets[currentBatchIndex.value]
  }
  return null
})

const openGenerateModal = async () => {
  generateStep.value = 1
  selectedRegulations.value = []
  selectedModel.value = ''
  generationType.value = 'single'
  batchSize.value = 5
  randomSelection.value = true
  batchGeneratedData.value = null
  currentBatchIndex.value = 0
  batchSelectedItems.value = {}
  await fetchRegulations()
  await fetchAvailableModels()
  showGenerateModal.value = true
}

const closeGenerateModal = () => {
  showGenerateModal.value = false
  generateStep.value = 1
  generatedData.value = null
  batchGeneratedData.value = null
  currentBatchIndex.value = 0
  batchSelectedItems.value = {}
  confirming.value = false
}

// Handle ESC key to close modal
const handleKeydown = (event) => {
  if (showGenerateModal.value && event.key === 'Escape') {
    closeGenerateModal()
  }
}

const toggleRegulationSelection = (id) => {
  const index = selectedRegulations.value.indexOf(id)
  if (index > -1) {
    selectedRegulations.value.splice(index, 1)
  } else {
    selectedRegulations.value.push(id)
  }
}

const removeRegulationSelection = (id) => {
  const index = selectedRegulations.value.indexOf(id)
  if (index > -1) {
    selectedRegulations.value.splice(index, 1)
  }
}

const getRegulationById = (id) => {
  return availableRegulations.value.find(r => r.id === id)
}

const fetchAvailableModels = async () => {
  try {
    const response = await instance.get('/api/v1/settings/')
    if (response.data && response.data.ollama_models) {
      availableModels.value = response.data.ollama_models
      // 預設選擇第一個模型
      if (availableModels.value.length > 0 && !selectedModel.value) {
        selectedModel.value = availableModels.value[0]
      }
    }
  } catch (err) {
    console.error('獲取可用模型失敗:', err)
    availableModels.value = []
  }
}

const toggleModelSelection = (model) => {
  selectedModel.value = model
}

const generateData = async () => {
  // 檢查是否啟用隨機選擇，如果沒有則需要選擇法規
  if (!randomSelection.value && selectedRegulations.value.length === 0) {
    toast.error('請選擇至少一個法規條文')
    return
  }

  if (!selectedModel.value) {
    toast.error('請選擇要使用的模型')
    return
  }

  if (generationType.value === 'batch' && (!batchSize.value || batchSize.value < 1 || batchSize.value > 20)) {
    toast.error('請設定有效的生成數量 (1-20)')
    return
  }

  generating.value = true
  generatedData.value = null
  batchGeneratedData.value = null
  currentBatchIndex.value = 0
  batchSelectedItems.value = {}
  generateStep.value = 2
  
  try {
    // 決定要使用的法規ID列表
    let articleIds = selectedRegulations.value
    if (generationType.value === 'batch' && randomSelection.value) {
      // 隨機選擇模式：使用所有可用的法規
      articleIds = availableRegulations.value.map(r => r.id)
    }
    
    if (generationType.value === 'single') {
      // Single generation
      const payload = {
        selected_article_ids: articleIds,
        model_name: selectedModel.value
      }
      const response = await instance.post('/api/v1/datasets/generate-from-regulations', payload, {
        timeout: 60000 // 60秒超時
      })
      generatedData.value = response.data
    } else {
      // Batch generation
      const payload = {
        selected_article_ids: articleIds,
        model_name: selectedModel.value,
        batch_size: batchSize.value,
        random_selection: randomSelection.value
      }
      const response = await instance.post('/api/v1/datasets/batch-generate-from-regulations', payload, {
        timeout: 300000 // 5分鐘超時
      })
      console.log(response.data)
      batchGeneratedData.value = response.data
      // Initialize selection state
      batchGeneratedData.value.datasets.forEach((_, index) => {
        batchSelectedItems.value[index] = null // null = unselected, true = selected, false = skipped
      })
    }
  } catch (err) {
    error.value = `生成資料失敗: ${err.response?.data?.detail || '未知錯誤'}`
    toast.error(error.value)
    console.error('生成資料失敗:', err)
    generateStep.value = 1
  } finally {
    generating.value = false
  }
}

const regenerateData = async () => {
  if (!generatedData.value) {
    toast.error('請先生成資料')
    return
  }

  generating.value = true
  generatedData.value = null
  
  try {
    const payload = {
      selected_article_ids: selectedRegulations.value,
      model_name: selectedModel.value
    }
    const response = await instance.post('/api/v1/datasets/generate-from-regulations', payload, {
      timeout: 60000 // 60秒超時
    })
    generatedData.value = response.data
    toast.success('資料重新生成完成！')
  } catch (err) {
    const errorMsg = `重新生成失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('重新生成失敗:', err)
  } finally {
    generating.value = false
  }
}

const regenerateBatchData = async () => {
  if (!batchGeneratedData.value) {
    toast.error('請先生成資料')
    return
  }

  generating.value = true
  batchGeneratedData.value = null
  currentBatchIndex.value = 0
  batchSelectedItems.value = {}
  
  try {
    // 決定要使用的法規ID列表
    let articleIds = selectedRegulations.value
    if (randomSelection.value) {
      // 隨機選擇模式：使用所有可用的法規
      articleIds = availableRegulations.value.map(r => r.id)
    }
    
    const payload = {
      selected_article_ids: articleIds,
      model_name: selectedModel.value,
      batch_size: batchSize.value,
      random_selection: randomSelection.value
    }
    const response = await instance.post('/api/v1/datasets/batch-generate-from-regulations', payload, {
      timeout: 300000 // 5分鐘超時
    })
    batchGeneratedData.value = response.data
    // Initialize selection state
    batchGeneratedData.value.datasets.forEach((_, index) => {
      batchSelectedItems.value[index] = null
    })
    toast.success('批量資料重新生成完成！')
  } catch (err) {
    const errorMsg = `重新生成失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('重新生成失敗:', err)
  } finally {
    generating.value = false
  }
}

// Batch navigation functions
const nextBatchItem = () => {
  if (currentBatchIndex.value < batchGeneratedData.value.datasets.length - 1) {
    currentBatchIndex.value++
  }
}

const previousBatchItem = () => {
  if (currentBatchIndex.value > 0) {
    currentBatchIndex.value--
  }
}

const selectBatchItem = (index, selected) => {
  batchSelectedItems.value[index] = selected
}

const getSelectedBatchCount = () => {
  return Object.values(batchSelectedItems.value).filter(value => value === true).length
}

const confirmBatchGeneratedData = async () => {
  const selectedDatasets = batchGeneratedData.value.datasets.filter((_, index) => 
    batchSelectedItems.value[index] === true
  )
  
  if (selectedDatasets.length === 0) {
    toast.error('請至少選擇一筆資料')
    return
  }

  confirming.value = true
  try {
    const payload = selectedDatasets.map(dataset => ({
      instruction: dataset.instruction,
      input: dataset.input,
      output: dataset.output,
      system: dataset.system,
      history: dataset.history,
      source: dataset.source,
      model_name: dataset.model_name
    }))
    
    const response = await instance.post('/api/v1/datasets/batch-confirm-generated', payload)
    toast.success(`成功確認加入 ${selectedDatasets.length} 筆資料！`)
    closeGenerateModal()
    await fetchDatasets() // Refresh the list
  } catch (err) {
    const errorMsg = `確認加入失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('確認加入失敗:', err)
  } finally {
    confirming.value = false
  }
}

const confirmGeneratedData = async () => {
  if (!generatedData.value) {
    toast.error('請先生成資料')
    return
  }

  confirming.value = true
  try {
    const payload = {
      instruction: generatedData.value.instruction,
      input: generatedData.value.input,
      output: generatedData.value.output,
      system: generatedData.value.system,
      history: generatedData.value.history,
      source: generatedData.value.source,
      model_name: generatedData.value.model_name  // 新增：保存模型名稱
    }
    const response = await instance.post('/api/v1/datasets/confirm-generated', payload)
    toast.success('資料已確認加入！')
    closeGenerateModal()
    await fetchDatasets() // Refresh the list
  } catch (err) {
    const errorMsg = `確認加入失敗: ${err.response?.data?.detail || '未知錯誤'}`
    error.value = errorMsg
    toast.error(errorMsg)
    console.error('確認加入失敗:', err)
  } finally {
    confirming.value = false
  }
}

onMounted(() => {
  fetchDatasets()
  document.addEventListener('keydown', handleKeydown)
})

// 組件卸載時清理輪詢
onUnmounted(() => {
  stopPolling()
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Text truncation utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Button system */
.btn {
  @apply inline-flex items-center justify-center space-x-2 font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-sm {
  @apply px-3 py-2 text-sm;
}

.btn-primary {
  @apply bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 focus:ring-blue-500 shadow-lg transition-all duration-200;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 15px rgba(59, 130, 246, 0.3);
}

.btn-success {
  @apply bg-green-600 text-white hover:bg-green-700 focus:ring-green-500 shadow-sm;
}

.btn-secondary {
  @apply bg-purple-600 text-white hover:bg-purple-700 focus:ring-purple-500 shadow-sm;
}

.btn-danger {
  @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm;
}

.btn-warning {
  @apply bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500 shadow-sm;
}

.btn-info {
  @apply bg-cyan-600 text-white hover:bg-cyan-700 focus:ring-cyan-500 shadow-sm;
}

/* Toggle button system */
.btn-toggle-active {
  @apply bg-white text-gray-800 shadow-sm;
}

.btn-toggle-inactive {
  @apply text-gray-600 hover:text-gray-800 hover:bg-gray-50;
}

/* Card system */
.card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200;
}

.card-header {
  @apply p-4 border-b border-gray-200;
}

.card-body {
  @apply p-4;
}

.card-footer {
  @apply p-4 border-t border-gray-200 bg-gray-50;
}

/* Status badges */
.status-badge {
  @apply px-2 py-1 text-xs font-medium rounded-full;
}

.status-pending {
  @apply bg-blue-100 text-blue-800;
}

.status-reviewing {
  @apply bg-yellow-100 text-yellow-800;
}

.status-done {
  @apply bg-green-100 text-green-800;
}

.status-regenerating {
  @apply bg-orange-100 text-orange-800;
}

/* Custom checkbox styles */
input[type="checkbox"]:indeterminate {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

/* Modal system */
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  @apply bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh];
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  @apply flex justify-between items-center p-6 border-b border-gray-200 flex-shrink-0;
}

.modal-body {
  @apply p-6 overflow-y-auto flex-1;
}

.modal-footer {
  @apply flex justify-between items-center p-6 border-t border-gray-200 bg-gray-50 flex-shrink-0;
}

/* Form system */
.form-group {
  @apply space-y-2 relative;
}

.form-label {
  @apply block text-sm font-semibold text-gray-700 transition-colors duration-200;
}

.form-input {
  @apply mt-1 block w-full border-2 border-gray-200 rounded-lg shadow-sm py-3 px-4 text-sm transition-all duration-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-gray-300;
  background-color: #ffffff;
}

.form-textarea {
  @apply mt-1 block w-full border-2 border-gray-200 rounded-lg shadow-sm py-3 px-4 text-sm transition-all duration-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-gray-300;
  background-color: #ffffff;
  resize: vertical;
  min-height: 2.5rem;
  line-height: 1.5;
}

.form-input:focus,
.form-textarea:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* 特殊欄位樣式 */
.form-textarea[placeholder*="JSON"] {
  @apply font-mono;
}

/* 必填欄位標記 */
.form-label .text-red-500 {
  @apply font-bold;
}

/* 欄位說明文字 */
.form-group p.text-xs {
  @apply mt-1 text-gray-500 italic;
}

/* 滾動條樣式優化 */
.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Loading animations */
.loading-spinner {
  @apply animate-spin rounded-full border-2 border-gray-200 border-t-blue-600;
}

/* Display mode transition animations */
.display-mode-enter-active,
.display-mode-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.display-mode-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.display-mode-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.display-mode-enter-to,
.display-mode-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Responsive utilities */
@media (max-width: 1024px) {
  .modal-content {
    @apply max-w-[95vw] mx-4;
  }
  
  .grid-cols-1.lg\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .btn-sm {
    @apply px-2 py-1 text-xs;
  }
  
  .card-header,
  .card-body,
  .card-footer {
    @apply p-3;
  }
  
  .modal-header {
    @apply p-4;
  }
  
  .modal-body {
    @apply p-4 overflow-y-auto flex-1;
  }
  
  .modal-footer {
    @apply p-4 flex-col space-y-3;
  }
  
  .modal-footer > div {
    @apply flex-col space-y-3;
  }
  
  .form-input,
  .form-textarea {
    @apply py-2 px-3;
  }
}
</style> 