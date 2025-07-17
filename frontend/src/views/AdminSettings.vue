<template>
  <div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-2xl md:text-4xl font-bold text-slate-800 mb-2">系統設定</h1>
      <p class="text-slate-600 text-sm md:text-base">管理 AI 模型配置和審核系統參數</p>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-flex flex-col items-center space-y-4">
        <div class="animate-spin rounded-full h-8 w-8 border-4 border-slate-200 border-t-slate-600"></div>
        <span class="text-slate-600 text-sm md:text-base font-medium">載入系統設定中...</span>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6">
      <div class="flex items-center">
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <span class="font-medium">{{ error }}</span>
      </div>
    </div>
    
    <!-- Main Content -->
    <div v-else class="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
      <form @submit.prevent="saveSettings" class="p-6 md:p-8">
        
        <!-- AI Model Settings Section -->
        <div class="mb-8 pb-8 border-b border-slate-200">
          <div class="flex items-center mb-6">
            <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl md:text-2xl font-semibold text-slate-800">AI 模型設定</h2>
              <p class="text-slate-500 text-sm md:text-base">配置 Ollama 服務和模型選擇</p>
            </div>
          </div>
          
          <!-- Ollama URL -->
          <div class="mb-6">
            <label for="ollama-url" class="block text-slate-700 font-semibold mb-3 text-sm md:text-base">
              Ollama 服務 URL
            </label>
            <div class="flex flex-col lg:flex-row items-stretch lg:items-center space-y-3 lg:space-y-0 lg:space-x-4">
              <div class="flex-1">
                <input
                  type="text"
                  id="ollama-url"
                  v-model="form.ollama_url"
                  class="w-full px-4 py-3 border border-slate-300 rounded-xl text-slate-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm md:text-base bg-slate-50 focus:bg-white"
                  placeholder="例如: http://localhost:11434"
                />
              </div>
              <button
                type="button"
                @click="testConnection"
                :disabled="isTestingConnection"
                class="px-6 py-3 bg-slate-600 text-white font-semibold rounded-xl hover:bg-slate-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-200 text-sm md:text-base whitespace-nowrap shadow-sm hover:shadow-md"
              >
                <span v-if="isTestingConnection" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  測試中...
                </span>
                <span v-else>測試連線</span>
              </button>
            </div>
            <div v-if="testConnectionStatus" class="mt-3 flex items-center">
              <svg v-if="testConnectionStatus.isError" class="w-4 h-4 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
              </svg>
              <svg v-else class="w-4 h-4 text-emerald-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span :class="testConnectionStatus.isError ? 'text-red-600' : 'text-emerald-600'" class="text-sm md:text-base font-medium">
                {{ testConnectionStatus.message }}
              </span>
            </div>
          </div>

          <!-- Ollama Model Selection -->
          <div class="mb-6">
            <label class="block text-slate-700 font-semibold mb-3 text-sm md:text-base">
              Ollama 模型選擇
            </label>
            <p class="text-slate-500 text-sm md:text-base mb-3">
              勾選要使用的模型，有勾選的模型皆可以讓使用者用來重新生成資料。
            </p>
            
            <!-- 操作按鈕區域 -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-4">
              <button
                type="button"
                @click="fetchOllamaModels"
                :disabled="!form.ollama_url"
                class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-200 text-sm md:text-base flex items-center justify-center gap-2 shadow-sm hover:shadow-md"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                刷新模型列表
              </button>
              
              <div v-if="ollamaModels.length > 0" class="flex gap-3">
                <button
                  type="button"
                  @click="selectAllModels"
                  class="px-4 py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 transition-all duration-200 text-sm md:text-base shadow-sm hover:shadow-md"
                >
                  全選
                </button>
                <button
                  type="button"
                  @click="clearAllModels"
                  class="px-4 py-3 bg-slate-600 text-white font-semibold rounded-xl hover:bg-slate-700 transition-all duration-200 text-sm md:text-base shadow-sm hover:shadow-md"
                >
                  清空
                </button>
              </div>
            </div>

            <!-- 搜索框 -->
            <div v-if="ollamaModels.length > 5" class="mb-4">
              <div class="relative">
                <input
                  type="text"
                  v-model="modelSearchQuery"
                  placeholder="搜索模型..."
                  class="w-full px-4 py-3 pl-10 border border-slate-300 rounded-xl text-slate-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm md:text-base bg-slate-50 focus:bg-white"
                />
                <svg class="absolute left-3 top-3.5 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>

            <!-- 模型列表 -->
            <div class="border border-slate-300 rounded-xl overflow-hidden">
              <!-- 空狀態 -->
              <div v-if="ollamaModels.length === 0" class="text-center py-8 bg-slate-50">
                <svg class="w-12 h-12 mx-auto text-slate-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
                <p class="text-slate-500 font-medium text-sm md:text-base">暫無可用模型</p>
                <p class="text-slate-400 text-xs md:text-sm mt-1">請先確認 Ollama URL 並刷新模型列表</p>
              </div>
              
              <!-- 模型列表 -->
              <div v-else>
                <!-- 統計信息 - 固定在頂部 -->
                <div class="bg-blue-50 border-b border-blue-200 px-4 py-3 sticky top-0 z-10">
                  <div class="flex items-center justify-between text-sm md:text-base">
                    <span class="text-blue-700">
                      找到 {{ filteredModels.length }} 個模型
                      <span v-if="modelSearchQuery">（搜索："{{ modelSearchQuery }}"）</span>
                    </span>
                    <span class="text-blue-600 font-medium">
                      已選擇 {{ form.ollama_models?.length || 0 }} 個
                    </span>
                  </div>
                </div>
                
                <!-- 可滾動的模型內容區域 -->
                <div class="max-h-80 overflow-y-auto">
                  <!-- 無搜索結果 -->
                  <div v-if="filteredModels.length === 0 && modelSearchQuery" class="text-center py-6 bg-slate-50">
                    <svg class="w-8 h-8 mx-auto text-slate-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <p class="text-slate-500 text-sm md:text-base">找不到匹配的模型</p>
                  </div>
                  
                  <!-- 模型項目 -->
                  <div v-for="(model, index) in filteredModels" :key="model.name" 
                       class="border-b border-slate-100 last:border-b-0 hover:bg-slate-50 transition-colors">
                    <label :for="'model-' + model.name" class="flex items-center p-4 cursor-pointer group">
                      <!-- 複選框 -->
                      <div class="relative">
                        <input
                          type="checkbox"
                          :id="'model-' + model.name"
                          :value="model.name"
                          v-model="form.ollama_models"
                          class="w-4 h-4 text-blue-600 bg-white border-2 border-slate-300 rounded focus:ring-blue-500 focus:ring-2 transition-colors"
                        />
                        <!-- 自定義選中狀態 -->
                        <svg v-if="form.ollama_models?.includes(model.name)" 
                             class="absolute inset-0 w-4 h-4 text-blue-600 pointer-events-none" 
                             fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                        </svg>
                      </div>
                      
                      <!-- 模型信息 -->
                      <div class="ml-3 flex-1 min-w-0">
                        <div class="flex items-center justify-between">
                          <div class="flex-1 min-w-0">
                            <p class="text-sm md:text-base font-medium text-slate-900 truncate group-hover:text-blue-600 transition-colors">
                              {{ model.name }}
                            </p>
                            <div class="flex items-center gap-4 mt-1">
                              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700">
                                {{ formatModelSize(model.size) }}
                              </span>
                              <span class="text-xs text-slate-500">
                                {{ formatDate(model.modified_at) }}
                              </span>
                            </div>
                          </div>
                          
                          <!-- 選中狀態指示器 -->
                          <div v-if="form.ollama_models?.includes(model.name)" 
                               class="ml-3 flex items-center text-blue-600">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                          </div>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 選中模型摘要 -->
            <div v-if="form.ollama_models && form.ollama_models.length > 0" 
                 class="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <div class="flex-1 min-w-0">
                  <p class="text-sm md:text-base font-medium text-blue-900 mb-1">
                    已選擇 {{ form.ollama_models.length }} 個模型
                  </p>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="model in form.ollama_models" :key="model"
                          class="inline-flex items-center px-2 py-1 rounded-lg text-xs font-medium bg-blue-100 text-blue-900 border border-blue-300">
                      {{ model }}
                      <button @click="removeModel(model)" 
                              class="ml-1 text-blue-600 hover:text-blue-800 focus:outline-none transition-colors">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                      </button>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pull Model -->
          <div class="mb-6">
            <label for="pull-model" class="block text-slate-700 font-semibold mb-3 text-sm md:text-base">
              下載新模型
            </label>
            <div class="flex flex-col lg:flex-row items-stretch lg:items-center space-y-3 lg:space-y-0 lg:space-x-4">
              <div class="flex-1">
                <input
                  type="text"
                  id="pull-model"
                  v-model="modelToPull"
                  class="w-full px-4 py-3 border border-slate-300 rounded-xl text-slate-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm md:text-base bg-slate-50 focus:bg-white"
                  placeholder="例如: llama3:latest"
                />
              </div>
              <button
                type="button"
                @click="pullModel"
                :disabled="isPullingModel"
                class="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-all duration-200 text-sm md:text-base whitespace-nowrap shadow-sm hover:shadow-md"
              >
                <span v-if="isPullingModel" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  下載中...
                </span>
                <span v-else>下載</span>
              </button>
            </div>
            <div v-if="pullStatus" class="mt-4 p-4 bg-slate-50 border border-slate-200 rounded-xl">
              <div class="flex items-center mb-2">
                <svg class="w-4 h-4 text-slate-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-sm md:text-base font-medium text-slate-700">下載進度</span>
              </div>
              <pre class="whitespace-pre-wrap break-all text-xs md:text-sm text-slate-600 bg-white p-3 rounded-xl border">{{ pullStatus }}</pre>
            </div>
          </div>
        </div>

        <!-- Review Threshold Section -->
        <div class="mb-8">
          <div class="flex items-center mb-6">
            <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-xl md:text-2xl font-semibold text-slate-800">審核閾值設定</h2>
              <p class="text-slate-500 text-sm md:text-base">配置自動審核的觸發條件</p>
            </div>
          </div>
          
          <!-- Rejection Threshold -->
          <div class="mb-6">
            <label for="rejection-threshold" class="block text-slate-700 font-semibold mb-3 text-sm md:text-base">
              拒絕閾值 (Rejection Threshold)
            </label>
            <p class="text-slate-500 text-sm md:text-base mb-3">
              當一筆資料的拒絕數量達到此數值，將自動觸發重生成。
            </p>
            <div class="max-w-xs">
              <input
                type="number"
                id="rejection-threshold"
                v-model.number="form.rejection_threshold"
                class="w-full px-4 py-3 border border-slate-300 rounded-xl text-slate-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm md:text-base bg-slate-50 focus:bg-white"
                min="1"
              />
            </div>
          </div>
          
          <!-- Approval Threshold -->
          <div class="mb-6">
            <label for="approval-threshold" class="block text-slate-700 font-semibold mb-3 text-sm md:text-base">
              通過閾值 (Approval Threshold)
            </label>
            <p class="text-slate-500 text-sm md:text-base mb-3">
              當一筆資料的通過數量達到此數值，將自動轉入最終資料集。
            </p>
            <div class="max-w-xs">
              <input
                type="number"
                id="approval-threshold"
                v-model.number="form.approval_threshold"
                class="w-full px-4 py-3 border border-slate-300 rounded-xl text-slate-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm md:text-base bg-slate-50 focus:bg-white"
                min="1"
              />
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4 pt-6 border-t border-slate-200">
          <button
            type="button"
            @click="testAuth"
            class="px-6 py-3 bg-slate-600 text-white font-semibold rounded-xl hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-50 transition-all duration-200 text-sm md:text-base shadow-sm hover:shadow-md"
          >
            測試認證機制
          </button>
          <button
            type="submit"
            :disabled="isSaving"
            class="px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:bg-blue-400 disabled:cursor-not-allowed transition-all duration-200 text-sm md:text-base shadow-sm hover:shadow-md"
          >
            <span v-if="isSaving" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              儲存中...
            </span>
            <span v-else>儲存設定</span>
          </button>
        </div>
      </form>
      
      <!-- Success Message -->
      <div v-if="successMessage" class="mx-6 md:mx-8 mb-6 bg-emerald-50 border border-emerald-200 text-emerald-700 px-6 py-4 rounded-xl">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span class="font-medium text-sm md:text-base">{{ successMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance, refreshToken } = useAuth()
const toast = useToast()

// Page States
const loading = ref(true)
const error = ref(null)
const isSaving = ref(false)
const successMessage = ref('')

// Form and Settings
const form = ref({
  rejection_threshold: 3,
  approval_threshold: 2,
  ollama_models: [],  // 修改：支援多模型列表
  ollama_url: 'http://host.docker.internal:11434'
})

// Ollama Connection and Models
const isTestingConnection = ref(false)
const testConnectionStatus = ref(null) // { isError: boolean, message: string }
const ollamaModels = ref([])
const modelToPull = ref('')
const isPullingModel = ref(false)
const pullStatus = ref('')

// Search and Selection
const modelSearchQuery = ref('')

const filteredModels = computed(() => {
  if (!modelSearchQuery.value) {
    return ollamaModels.value
  }
  const query = modelSearchQuery.value.toLowerCase()
  return ollamaModels.value.filter(model => 
    model.name.toLowerCase().includes(query)
  )
})

const selectAllModels = () => {
  form.value.ollama_models = filteredModels.value.map(model => model.name)
}

const clearAllModels = () => {
  form.value.ollama_models = []
}

const removeModel = (modelName) => {
  form.value.ollama_models = form.value.ollama_models.filter(name => name !== modelName)
}

// 格式化函數
const formatModelSize = (size) => {
  if (!size) return '未知'
  const bytes = typeof size === 'string' ? parseInt(size) : size
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return '無效日期'
  }
}

const fetchSettings = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await instance.get('/api/v1/settings/')
    form.value = response.data
    if (form.value.ollama_url) {
      await fetchOllamaModels()
    }
  } catch (err) {
    const errorMessage = err.response?.data?.detail || '無法載入系統設定。'
    error.value = errorMessage
    toast.error(errorMessage)
  } finally {
    loading.value = false
  }
}

const testConnection = async () => {
  isTestingConnection.value = true
  testConnectionStatus.value = null
  
  try {
    // 檢查 URL 格式
    if (!form.value.ollama_url) {
      throw new Error('請輸入 Ollama URL')
    }
    
    if (!form.value.ollama_url.startsWith('http://') && !form.value.ollama_url.startsWith('https://')) {
      throw new Error('URL 必須以 http:// 或 https:// 開頭')
    }
    
    const response = await instance.post('/api/v1/ollama/test', { 
      url: form.value.ollama_url 
    })
    
    testConnectionStatus.value = { 
      isError: false, 
      message: response.data.message || '連線成功！' 
    }
    toast.success('連線成功！')
    
    // 連線成功後自動獲取模型列表
    await fetchOllamaModels()
    
  } catch (err) {
    console.error('Ollama 連線測試失敗:', err)
    
    let errorMessage = '連線失敗，請檢查 URL 或 Ollama 服務狀態。'
    
    if (err.response?.data?.detail) {
      errorMessage = err.response.data.detail
    } else if (err.message) {
      errorMessage = err.message
    }
    
    testConnectionStatus.value = { 
      isError: true, 
      message: errorMessage 
    }
    toast.error(errorMessage)
  } finally {
    isTestingConnection.value = false
  }
}

const fetchOllamaModels = async () => {
  if (!form.value.ollama_url) {
    toast.info('請先輸入 Ollama URL。')
    return
  }
  
  try {
    const response = await instance.get('/api/v1/ollama/models')
    ollamaModels.value = response.data || []
    
    if (ollamaModels.value.length === 0) {
      toast.info('Ollama 服務中目前沒有可用的模型。')
    } else {
      toast.success(`成功獲取 ${ollamaModels.value.length} 個模型`)
    }
  } catch (error) {
    console.error('獲取模型列表失敗:', error)
    const errorMessage = error.response?.data?.detail || '無法獲取模型列表。'
    toast.error(errorMessage)
    ollamaModels.value = []
  }
}

const pullModel = async () => {
  if (!modelToPull.value) {
    toast.warning('請輸入要下載的模型名稱。')
    return
  }
  isPullingModel.value = true
  pullStatus.value = `正在準備下載 ${modelToPull.value}...\n`

  try {
    const response = await instance.post('/api/v1/ollama/pull', 
      { model_name: modelToPull.value },
      { 
        responseType: 'text',
        timeout: 0 // No timeout for long-running operations
      }
    );

    // Parse the streaming response and show only important progress
    if (response.data) {
      const lines = response.data.split('\n').filter(line => line.trim())
      let hasShownDownloading = false
      
      lines.forEach(line => {
        try {
          const progressData = JSON.parse(line)
          if (progressData.status) {
            const status = progressData.status
            
            // Show important milestones
            if (status.includes('pulling manifest')) {
              pullStatus.value += `正在下載模型清單...\n`
            }
            else if (status.includes('verifying sha256 digest')) {
              pullStatus.value += `正在驗證模型完整性...\n`
            }
            else if (status.includes('writing manifest')) {
              pullStatus.value += `正在寫入模型檔案...\n`
            }
            else if (status.includes('success')) {
              pullStatus.value += `模型下載成功！\n`
            }
            else if (status.includes('error') || status.includes('failed')) {
              pullStatus.value += `錯誤: ${status}\n`
            }
            // For layer pulling, show only one message for all layers
            else if (status.includes('pulling') && status.match(/pulling ([a-f0-9]+)/)) {
              if (!hasShownDownloading) {
                pullStatus.value += `正在下載模型檔案...\n`
                hasShownDownloading = true
              }
            }
          }
        } catch(e) {
          // Ignore JSON parsing errors for incomplete lines
        }
      });
    }

    pullStatus.value += '\n下載完成！'
    toast.success(`${modelToPull.value} 模型下載完成！`)
    await fetchOllamaModels()
  } catch (err) {
    const errorMessage = err.response?.data?.detail || `下載模型失敗: ${err.message}`
    pullStatus.value += `\n錯誤: ${errorMessage}`
    toast.error(errorMessage)
  } finally {
    isPullingModel.value = false
    modelToPull.value = ''
  }
}

const saveSettings = async () => {
  isSaving.value = true
  successMessage.value = ''
  error.value = null
  try {
    await instance.put('/api/v1/settings/', { settings: form.value })
    toast.success('設定已成功儲存！')
    successMessage.value = '設定已成功儲存！'
    setTimeout(() => successMessage.value = '', 3000)
  } catch (err) {
    const errorMessage = err.response?.data?.detail || '儲存設定失敗。'
    toast.error(errorMessage)
    error.value = errorMessage
  } finally {
    isSaving.value = false
  }
}

const testAuth = async () => {
  try {
    toast.info('開始測試認證機制...')
    
    // 測試 1: 手動刷新 token
    toast.info('測試 1: 手動刷新 token')
    await refreshToken()
    toast.success('Token 刷新成功！')
    
    // 測試 2: 發送需要認證的請求
    toast.info('測試 2: 發送需要認證的請求')
    const response = await instance.get('/api/v1/auth/me')
    toast.success(`當前用戶: ${response.data.username} (${response.data.role})`)
    
    // 測試 3: 連續發送多個請求
    toast.info('測試 3: 連續發送多個請求')
    const promises = [
      instance.get('/api/v1/settings/'),
      instance.get('/api/v1/users/'),
      instance.get('/api/v1/stats/')
    ]
    await Promise.all(promises)
    toast.success('所有請求都成功完成！')
    
    toast.success('認證機制測試完成！')
  } catch (error) {
    console.error('認證測試失敗:', error)
    toast.error(`認證測試失敗: ${error.message}`)
  }
}

onMounted(fetchSettings)
</script> 