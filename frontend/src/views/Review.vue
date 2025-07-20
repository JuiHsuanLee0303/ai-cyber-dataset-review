<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 頁面標題和進度 -->
    <div class="mb-6 sm:mb-8">
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 sm:mb-0">資料審核</h1>
        <div class="flex items-center space-x-6">
          <div class="flex items-center justify-between space-x-6">
            <div class="text-center">
              <div class="text-2xl sm:text-3xl font-bold text-primary-main">{{ datasets.length == 0 ? 0 : currentIndex + 1 }}</div>
              <div class="text-xs sm:text-sm text-neutral-500">當前項目</div>
            </div>
            <div class="text-center">
              <div class="text-2xl sm:text-3xl font-bold text-neutral-400">{{ datasets.length }}</div>
              <div class="text-xs sm:text-sm text-neutral-500">總項目</div>
            </div>
          </div>
          <div class="relative w-32 sm:w-40">
            <div class="w-full bg-neutral-200 rounded-full h-4 border-2 border-neutral-300 shadow-inner overflow-hidden">
              <div 
                class="bg-gradient-to-r from-primary-light via-primary-main to-primary-dark h-full rounded-full transition-all duration-700 ease-out shadow-lg relative"
                :style="{ width: `${((currentIndex + 1) / datasets.length) * 100}%` }"
              >
                <!-- 進度條光澤效果 -->
                <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
              </div>
            </div>
            <!-- 進度百分比標籤 -->
            <div class="absolute -top-8 left-1/2 transform -translate-x-1/2">
              <div class="bg-primary-main text-white text-xs font-bold px-2 py-1 rounded-lg shadow-lg">
                {{ Math.round(((currentIndex + 1) / datasets.length) * 100) }}%
              </div>
              <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-primary-main"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin rounded-full h-16 w-16 border-4 border-primary-light border-t-primary-main mx-auto mb-6"></div>
      <p class="text-lg text-neutral-600 font-medium">載入審核資料中...</p>
      <p class="text-sm text-neutral-500 mt-2">請稍候，正在準備您的審核項目</p>
    </div>

    <div v-else-if="!currentItem" class="text-center py-20 bg-white rounded-2xl border border-neutral-200 shadow-sm">
      <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h2 class="text-3xl font-bold text-neutral-900 mb-3">審核完成！</h2>
      <p class="text-sm sm:text-base text-neutral-600 mb-8 max-w-md mx-auto">目前沒有更多待審核的資料。感謝您的辛勤工作！</p>
      <button @click="fetchDatasets" class="inline-flex items-center px-6 py-3 bg-primary-main text-white font-medium rounded-xl hover:bg-primary-dark transition-all duration-200 shadow-sm hover:shadow-md">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        重新載入
      </button>
    </div>

    <!-- 主要審核區域 -->
    <div v-else class="space-y-6">
      <!-- 審核操作 -->
      <div class="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden">
        <div class="bg-gradient-to-r from-orange-100 to-yellow-50 px-6 py-4 border-b border-neutral-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-neutral-900">審核決定</h3>
            <div class="flex items-center space-x-2 text-sm text-neutral-600">
              <div class="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>請仔細審核後做出決定</span>
            </div>
          </div>
        </div>
        <div class="p-6">
          <div v-if="currentItem.review_status === 'regenerating'" class="text-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-light border-t-primary-main mx-auto mb-4"></div>
            <p class="text-lg text-neutral-700 font-medium mb-2">重新生成中...</p>
            <p class="text-sm text-neutral-500">請稍候，系統正在重新生成此筆資料</p>
          </div>
          <div v-else class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button 
                @click="handleAccept"
                class="group flex items-center justify-center space-x-3 px-6 py-4 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-xl hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-105"
              >
                <svg class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span class="text-base">接受</span>
              </button>
              <button 
                @click="showRejectModal = true"
                class="group flex items-center justify-center space-x-3 px-6 py-4 bg-gradient-to-r from-red-500 to-red-600 text-white font-medium rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-105"
              >
                <svg class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                <span class="text-base">拒絕</span>
              </button>
              <button 
                @click="nextItem"
                class="group flex items-center justify-center space-x-3 px-6 py-4 bg-neutral-100 text-neutral-700 font-medium rounded-xl hover:bg-neutral-200 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-105"
              >
                <svg class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                </svg>
                <span class="text-base">跳過此筆</span>
              </button>
            </div>
            <div class="text-center">
              <p class="text-sm text-neutral-500">使用鍵盤快捷鍵：<span class="font-mono bg-neutral-100 px-2 py-1 rounded">A</span> 接受 | <span class="font-mono bg-neutral-100 px-2 py-1 rounded">R</span> 拒絕 | <span class="font-mono bg-neutral-100 px-2 py-1 rounded">S</span> 跳過</p>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <!-- 左側：指令和輸入 -->
        <div class="xl:col-span-2 space-y-6">
          <!-- 指令區域 -->
          <div class="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-purple-100 to-pink-50 px-6 py-4 border-b border-neutral-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-primary-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-neutral-900">指令 (Instruction)</h3>
                    <p class="text-sm text-neutral-600">檢查指令是否清楚明確，能讓AI理解要執行什麼任務</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="bg-neutral-50 border border-neutral-200 rounded-xl p-4 text-neutral-800 whitespace-pre-wrap leading-relaxed text-base">
                {{ currentItem.instruction }}
              </div>
            </div>
          </div>
          <div class="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-100 to-blue-50 px-6 py-4 border-b border-neutral-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-neutral-900">完整對話流程</h3>
                    <p class="text-sm text-neutral-600">評估AI的回答是否符合資安法規要求，對實務有幫助</p>
                  </div>
                </div>
                <div class="hidden sm:flex items-center px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-xs font-medium">
                  {{ (currentItem.history?.length || 0) + 1 }} 輪對話
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="space-y-6">
                <!-- 歷史對話 -->
                <div v-for="(conversation, index) in currentItem.history" :key="index" class="relative">
                  <div class="space-y-4 p-5 rounded-2xl border border-neutral-200 bg-neutral-50">
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 bg-neutral-100 rounded-full flex items-center justify-center">
                        <span class="text-sm font-bold text-neutral-600">{{ index + 1 }}</span>
                      </div>
                      <span class="text-base font-medium text-neutral-500">歷史對話 {{ index + 1 }}</span>
                    </div>
                    <div class="flex space-x-4">
                      <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold bg-neutral-100 text-neutral-600">Q</div>
                      <div class="flex-1">
                        <div class="text-sm text-neutral-400 mb-2 font-medium">問題</div>
                        <div class="bg-neutral-50 border border-neutral-200 rounded-xl p-4 text-neutral-700 whitespace-pre-wrap leading-relaxed text-base">
                          {{ conversation[0] }}
                        </div>
                      </div>
                    </div>
                    <div class="flex space-x-4">
                      <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold bg-neutral-100 text-neutral-600">A</div>
                      <div class="flex-1">
                        <div class="text-sm text-neutral-400 mb-2 font-medium">回答</div>
                        <div class="bg-neutral-50 border border-neutral-200 rounded-xl p-4 text-neutral-700 whitespace-pre-wrap leading-relaxed text-base">
                          {{ conversation[1] }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="relative">
                  <div class="absolute -top-3 left-4 z-10">
                    <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-1 rounded-full text-sm font-bold shadow-lg">
                      🔍 審核重點
                    </div>
                  </div>
                  <div class="border-2 border-blue-300 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
                    <div v-if="currentItem.input" class="space-y-4 mb-6">
                      <div class="flex items-center space-x-3 mb-3">
                        <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                          <span class="text-xs font-bold text-blue-800">Q</span>
                        </div>
                        <span class="text-sm font-bold text-blue-800">當前問題</span>
                      </div>
                      <div class="bg-white border-2 border-blue-200 rounded-xl p-4 text-neutral-800 whitespace-pre-wrap leading-relaxed text-base shadow-sm">
                        {{ currentItem.input }}
                      </div>
                    </div>
                    <div v-if="!currentItem.input" class="space-y-4 mb-6">
                      <div class="flex items-center space-x-3 mb-3">
                        <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                          <span class="text-xs font-bold text-blue-800">指令</span>
                        </div>
                        <span class="text-sm font-bold text-blue-800">指令</span>
                      </div>
                      <div class="bg-white border-2 border-blue-200 rounded-xl p-4 text-neutral-800 whitespace-pre-wrap leading-relaxed text-base shadow-sm">
                        {{ currentItem.instruction }}
                      </div>
                    </div>
                    <div class="space-y-4">
                      <div class="flex items-center space-x-3 mb-3">
                        <div class="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                          <span class="text-xs font-bold text-green-800">A</span>
                        </div>
                        <span class="text-sm font-bold text-green-800">AI回答</span>
                        <div class="flex items-center space-x-2">
                          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                          <span class="text-xs text-green-600 font-medium">需要審核</span>
                        </div>
                      </div>
                      <div class="bg-white border-2 border-green-200 rounded-xl p-4 text-neutral-800 whitespace-pre-wrap leading-relaxed text-base shadow-sm">
                        {{ currentItem.output }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="space-y-6">
          <div v-if="currentItem.source && currentItem.source.length > 0" class="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-green-100 to-emerald-50 px-6 py-4 border-b border-neutral-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-neutral-900">法規依據 (Source)</h3>
                    <p class="text-sm text-neutral-600">確認法規依據是否正確相關，內容是否準確</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div v-for="(src, index) in currentItem.source" :key="index" class="space-y-3">
                  <div class="bg-green-50 border border-green-200 rounded-xl p-4">
                    <div class="text-sm font-medium text-green-800 mb-3">{{ src }}</div>
                    <div v-if="sourceDetails[index]" class="bg-white border border-green-200 rounded-xl p-4">
                      <div class="text-sm text-green-600 font-medium mb-3">法規內容：</div>
                      <div class="text-sm text-neutral-800 whitespace-pre-wrap leading-relaxed">{{ sourceDetails[index].content }}</div>
                    </div>
                    <div v-else-if="sourceLoading[index]" class="flex items-center space-x-3 text-sm text-neutral-500">
                      <div class="animate-spin rounded-full h-4 w-4 border-2 border-green-200 border-t-green-600"></div>
                      <span>載入法規內容...</span>
                    </div>
                    <div v-else-if="sourceErrors[index]" class="text-sm text-green-600 bg-green-50 border border-green-200 rounded-lg p-3">
                      {{ sourceErrors[index] }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl mx-auto max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-neutral-200">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-xl font-semibold text-neutral-900">拒絕原因</h3>
              <p class="text-sm text-neutral-600 mt-1">請選擇常見拒絕理由並填寫詳細說明，這將幫助改進資料品質</p>
            </div>
            <button @click="cancelReject" class="text-neutral-400 hover:text-neutral-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        <div class="p-6 space-y-8">
          <div>
            <label class="block text-lg font-semibold text-neutral-700 mb-4">
              常見拒絕理由 <span class="text-red-500">*</span>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div 
                v-for="reason in commonReasons" 
                :key="reason.id"
                @click="toggleCommonReason(reason.id)"
                :class="[
                  'p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 hover:shadow-md',
                  selectedCommonReasons.includes(reason.id)
                    ? 'border-primary-light bg-primary-light shadow-md'
                    : 'border-neutral-200 hover:border-neutral-300'
                ]"
              >
                <div class="flex items-start space-x-4">
                  <div class="flex-shrink-0 mt-1">
                    <div 
                      :class="[
                        'w-5 h-5 rounded border-2 flex items-center justify-center transition-all duration-200',
                        selectedCommonReasons.includes(reason.id)
                          ? 'border-primary-light bg-primary-light'
                          : 'border-neutral-300'
                      ]"
                    >
                      <svg v-if="selectedCommonReasons.includes(reason.id)" class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-base font-medium text-neutral-900 mb-2">{{ reason.label }}</div>
                    <div class="text-sm text-neutral-500 mb-3">{{ reason.description }}</div>
                    <div class="inline-block px-3 py-1 text-xs font-medium rounded-full" 
                         :class="{
                           'bg-primary-light text-primary-dark': reason.category === 'instruction',
                           'bg-green-100 text-green-800': reason.category === 'output',
                           'bg-red-100 text-red-800': reason.category === 'source',
                           'bg-purple-100 text-purple-800': reason.category === 'input',
                           'bg-yellow-100 text-yellow-800': reason.category === 'format',
                           'bg-indigo-100 text-indigo-800': reason.category === 'content',
                           'bg-orange-100 text-orange-800': reason.category === 'security',
                           'bg-neutral-100 text-neutral-800': reason.category === 'other'
                         }">
                      {{ getCategoryLabel(reason.category) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="selectedCommonReasons.length === 0" class="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
              請至少選擇一個拒絕理由
            </div>
          </div>
          <div>
            <label for="detailed-reason" class="block text-lg font-semibold text-neutral-700 mb-4">
              詳細拒絕理由 <span class="text-neutral-500">(可選)</span>
            </label>
            <textarea 
              id="detailed-reason"
              v-model="detailedRejectReason"
              rows="4"
              class="w-full p-4 border border-neutral-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-light focus:border-transparent resize-none text-base"
              placeholder="請詳細說明拒絕原因，提供具體的改進建議..."
            ></textarea>
          </div>
          <div>
            <label for="additional-comment" class="block text-lg font-semibold text-neutral-700 mb-4">
              額外備註 <span class="text-neutral-500">(可選)</span>
            </label>
            <textarea 
              id="additional-comment"
              v-model="rejectComment"
              rows="3"
              class="w-full p-4 border border-neutral-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-light focus:border-transparent resize-none text-base"
              placeholder="如有其他需要說明的內容，請在此填寫..."
            ></textarea>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-neutral-200 flex justify-end space-x-4">
          <button 
            @click="cancelReject" 
            class="px-6 py-3 bg-neutral-100 text-neutral-700 font-medium rounded-xl hover:bg-neutral-200 transition-all duration-200"
          >
            取消
          </button>
          <button 
            @click="handleReject" 
            class="px-6 py-3 bg-red-600 text-white font-medium rounded-xl hover:bg-red-700 transition-all duration-200 shadow-sm hover:shadow-md"
          >
            確認拒絕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance } = useAuth()
const toast = useToast()

const loading = ref(true)
const showRejectModal = ref(false)
const rejectComment = ref('')
const detailedRejectReason = ref('')
const selectedCommonReasons = ref([])
const datasets = ref([])
const currentIndex = ref(0)
const sourceDetails = ref({})
const sourceLoading = ref({})
const sourceErrors = ref({})

// 鍵盤快捷鍵處理
const handleKeydown = (event) => {
  // 如果正在載入或沒有當前項目，不處理快捷鍵
  if (loading.value || !currentItem.value) return
  
  // 如果拒絕模態框開啟，不處理快捷鍵
  if (showRejectModal.value) return
  
  // 如果正在重新生成，不處理快捷鍵
  if (currentItem.value.review_status === 'regenerating') return
  
  switch (event.key.toLowerCase()) {
    case 'a':
      event.preventDefault()
      handleAccept()
      break
    case 'r':
      event.preventDefault()
      showRejectModal.value = true
      break
    case 's':
      event.preventDefault()
      nextItem()
      break
  }
}

// 常見拒絕理由列表
const commonReasons = ref([
  {
    id: 'instruction_unclear',
    label: '指令不夠清楚',
    description: '指令描述模糊，無法明確理解要執行什麼任務',
    category: 'instruction'
  },
  {
    id: 'output_inaccurate',
    label: '輸出內容不準確',
    description: 'AI 回答內容有錯誤或不符合事實',
    category: 'output'
  },
  {
    id: 'output_not_helpful',
    label: '輸出內容不實用',
    description: '回答過於理論化，缺乏實務價值',
    category: 'output'
  },
  {
    id: 'regulation_incorrect',
    label: '法規依據錯誤',
    description: '引用的法規條文不正確或已過時',
    category: 'source'
  },
  {
    id: 'regulation_irrelevant',
    label: '法規依據不相關',
    description: '引用的法規與指令內容無關',
    category: 'source'
  },
  {
    id: 'input_inappropriate',
    label: '輸入內容不適當',
    description: '輸入內容與資安領域無關或不合適',
    category: 'input'
  },
  {
    id: 'format_inconsistent',
    label: '格式不一致',
    description: '資料格式與其他資料不一致',
    category: 'format'
  },
  {
    id: 'duplicate_content',
    label: '內容重複',
    description: '與其他資料內容重複或過於相似',
    category: 'content'
  },
  {
    id: 'sensitive_info',
    label: '包含敏感資訊',
    description: '內容包含機密或敏感資訊',
    category: 'security'
  },
  {
    id: 'other',
    label: '其他原因',
    description: '其他未列出的拒絕原因',
    category: 'other'
  }
])

const currentItem = computed(() => {
  if (datasets.value.length > 0 && currentIndex.value < datasets.value.length) {
    return datasets.value[currentIndex.value]
  }
  return null
})

// 解析資料來源字串，提取法規標題和條號
const parseSource = (sourceStr) => {
  // 範例: "公務機關所屬人員資通安全事項獎懲辦法第1條" 或 "資通安全管理法第十六條"
  const match = sourceStr.match(/^(.+?)第([一二三四五六七八九十\d]+)條$/)
  if (match) {
    let number = match[2]
    // 若number為中文數字，則轉換為阿拉伯數字
    if (number.match(/^[一二三四五六七八九十]+$/)) {
      number = convertChineseToArabic(number)
    }
    return {
      title: match[1].trim(),
      number: number
    }
  }
  return null
}

// 將中文數字轉換為阿拉伯數字
const convertChineseToArabic = (chineseNum) => {
  const chineseToArabic = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
  }
  
  // 處理特殊情況
  if (chineseNum === '十') return '10'
  if (chineseNum === '十一') return '11'
  if (chineseNum === '十二') return '12'
  if (chineseNum === '十三') return '13'
  if (chineseNum === '十四') return '14'
  if (chineseNum === '十五') return '15'
  if (chineseNum === '十六') return '16'
  if (chineseNum === '十七') return '17'
  if (chineseNum === '十八') return '18'
  if (chineseNum === '十九') return '19'
  if (chineseNum === '二十') return '20'
  if (chineseNum === '二十一') return '21'
  if (chineseNum === '二十二') return '22'
  if (chineseNum === '二十三') return '23'
  if (chineseNum === '二十四') return '24'
  if (chineseNum === '二十五') return '25'
  if (chineseNum === '二十六') return '26'
  if (chineseNum === '二十七') return '27'
  if (chineseNum === '二十八') return '28'
  if (chineseNum === '二十九') return '29'
  if (chineseNum === '三十') return '30'
  if (chineseNum === '三十一') return '31'
  if (chineseNum === '三十二') return '32'
  if (chineseNum === '三十三') return '33'
  if (chineseNum === '三十四') return '34'
  if (chineseNum === '三十五') return '35'
  if (chineseNum === '三十六') return '36'
  if (chineseNum === '三十七') return '37'
  if (chineseNum === '三十八') return '38'
  if (chineseNum === '三十九') return '39'
  if (chineseNum === '四十') return '40'
  if (chineseNum === '四十一') return '41'
  if (chineseNum === '四十二') return '42'
  if (chineseNum === '四十三') return '43'
  if (chineseNum === '四十四') return '44'
  if (chineseNum === '四十五') return '45'
  if (chineseNum === '四十六') return '46'
  if (chineseNum === '四十七') return '47'
  if (chineseNum === '四十八') return '48'
  if (chineseNum === '四十九') return '49'
  if (chineseNum === '五十') return '50'
  
  // 如果是單個數字（1-10），直接轉換
  if (chineseNum.length === 1) {
    return chineseToArabic[chineseNum].toString()
  }
  
  // 如果是複合數字，使用通用算法
  let result = 0
  let temp = 0
  
  for (let i = 0; i < chineseNum.length; i++) {
    const char = chineseNum[i]
    const value = chineseToArabic[char]
    
    if (value === 10) {
      // 遇到「十」，將前面的數字乘以10
      if (temp === 0) temp = 1
      temp *= 10
    } else {
      // 遇到其他數字，加到臨時結果中
      temp += value
    }
  }
  
  result = temp
  return result.toString()
}

// 載入法規文章內容
const loadSourceDetails = async (sourceStr, index) => {
  const parsed = parseSource(sourceStr)
  if (!parsed) {
    sourceErrors.value[index] = '無法解析法規格式'
    return
  }

  sourceLoading.value[index] = true
  sourceErrors.value[index] = null
  
  try {
    const response = await instance.get('/api/v1/legal-articles/search', {
      params: {
        title: parsed.title,
        number: parsed.number
      }
    })
    sourceDetails.value[index] = response.data
  } catch (error) {
    console.error('Failed to load legal article:', error)
    sourceErrors.value[index] = '法規不存在或載入失敗'
  } finally {
    sourceLoading.value[index] = false
  }
}

// 當當前項目改變時，載入資料來源詳情
const loadCurrentItemSources = async () => {
  if (!currentItem.value || !currentItem.value.source) return
  
  // 清理之前的狀態
  sourceDetails.value = {}
  sourceLoading.value = {}
  sourceErrors.value = {}
  
  // 為每個資料來源載入詳情
  for (let i = 0; i < currentItem.value.source.length; i++) {
    await loadSourceDetails(currentItem.value.source[i], i)
  }
}

const fetchDatasets = async () => {
  loading.value = true
  datasets.value = []
  currentIndex.value = 0
  try {
    // For now, we fetch all datasets. In a real app, you'd likely fetch only those needing review.
    const response = await instance.get('/api/v1/datasets/') 
    // A simple filter to find items the current user hasn't reviewed.
    // This is a placeholder and has performance implications on the frontend.
    // Ideally, the backend should provide an endpoint for this.
    const res = await instance.get('/api/v1/auth/me');
    const currentUser = res.data;
    
    datasets.value = response.data.filter(d => {
        return !d.review_logs.some(log => log.reviewer_id === currentUser.id);
    });

    // 載入第一個項目的資料來源
    if (datasets.value.length > 0) {
      await loadCurrentItemSources()
    }

  } catch (error) {
    console.error('Failed to load datasets:', error)
    toast.error('載入待審核資料失敗。')
  } finally {
    loading.value = false
  }
}

const nextItem = async () => {
  if (currentIndex.value < datasets.value.length - 1) {
    currentIndex.value++
    // 載入新項目的資料來源
    await loadCurrentItemSources()
  } else {
    // Reached the end
    currentIndex.value = datasets.value.length
    // Optionally show a message or fetch more data
  }
}

const submitReview = async (result, comment = null, commonReasons = null, detailedReason = null) => {
  if (!currentItem.value) return
  
  try {
    const reviewData = {
      result: result,
      comment: comment
    }
    
    // 如果是拒絕，添加新的欄位
    if (result === 'REJECT') {
      reviewData.common_reasons = commonReasons || []
      reviewData.detailed_reason = detailedReason || ''
    }
    
    await instance.post(`/api/v1/review/${currentItem.value.id}`, reviewData)
    toast.success('審核結果已提交！');
    nextItem() // Move to the next item
  } catch (error) {
     console.error('Failed to submit review:', error)
     toast.error(`提交審核失敗: ${error.response?.data?.detail || '未知錯誤'}`)
  }
}

const handleAccept = () => {
  submitReview('ACCEPT')
}

const handleReject = () => {
  if (selectedCommonReasons.value.length === 0) {
    toast.warning('請至少選擇一個常見拒絕理由。');
    return
  }
  
  // 構建完整的拒絕理由
  const selectedReasonLabels = selectedCommonReasons.value.map(id => {
    const reason = commonReasons.value.find(r => r.id === id)
    return reason ? reason.label : id
  }).join('、')
  
  let fullComment = `選擇的拒絕理由：${selectedReasonLabels}`
  if (detailedRejectReason.value.trim()) {
    fullComment += `\n\n詳細說明：${detailedRejectReason.value.trim()}`
  }
  if (rejectComment.value.trim()) {
    fullComment += `\n\n額外備註：${rejectComment.value.trim()}`
  }
  
  submitReview(
    'REJECT', 
    fullComment,
    selectedCommonReasons.value,
    detailedRejectReason.value.trim()
  )
  
  // 重置表單
  showRejectModal.value = false
  detailedRejectReason.value = ''
  rejectComment.value = ''
  selectedCommonReasons.value = []
}

const cancelReject = () => {
  showRejectModal.value = false
  detailedRejectReason.value = ''
  rejectComment.value = ''
  selectedCommonReasons.value = []
}

const toggleCommonReason = (reasonId) => {
  const index = selectedCommonReasons.value.indexOf(reasonId)
  if (index > -1) {
    selectedCommonReasons.value.splice(index, 1)
  } else {
    selectedCommonReasons.value.push(reasonId)
  }
}

const getCategoryLabel = (category) => {
  const categoryLabels = {
    'instruction': '指令',
    'output': '回答',
    'source': '法規',
    'input': '輸入',
    'format': '格式',
    'content': '內容',
    'security': '安全',
    'other': '其他'
  }
  return categoryLabels[category] || '未知'
}

onMounted(() => {
  fetchDatasets()
  // 添加鍵盤事件監聽器
  document.addEventListener('keydown', handleKeydown)
})

// 組件卸載時移除事件監聽器
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script> 