<template>
  <div class="max-w-6xl mx-auto">
    <!-- 頁面標題和進度 -->
    <div class="mb-6 sm:mb-8">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 space-y-2 sm:space-y-0">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">資料審核</h1>
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-600">
            <span class="font-medium">{{ currentIndex + 1 }}</span> / {{ datasets.length }}
          </div>
          <div class="w-24 sm:w-32 bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${((currentIndex + 1) / datasets.length) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
      
      <!-- 審核指引 -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 sm:p-4">
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
            <span class="text-blue-600 text-sm font-bold">?</span>
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-semibold text-blue-900 mb-2">審核指引</h3>
            <div class="text-xs sm:text-sm text-blue-800 space-y-1">
              <p>• <strong>Instruction</strong>：檢查指令是否清楚明確，能讓AI理解要執行什麼任務</p>
              <p>• <strong>Output</strong>：評估AI的回答是否符合資安法規要求，對實務有幫助</p>
              <p>• <strong>Source</strong>：確認法規依據是否正確相關，內容是否準確</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-600">載入審核資料中...</p>
    </div>

    <div v-else-if="!currentItem" class="text-center py-20 bg-white rounded-xl border border-gray-200 shadow-sm">
      <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h2 class="text-2xl font-semibold text-gray-900 mb-2">審核完成！</h2>
      <p class="text-gray-600 mb-6">目前沒有更多待審核的資料。</p>
      <button @click="fetchDatasets" class="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
        重新載入
      </button>
    </div>

    <!-- 主要審核區域 -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
      <!-- 左側：指令和輸入 -->
      <div class="lg:col-span-2 space-y-4 sm:space-y-6">
        <!-- 指令區域 -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-blue-50 to-indigo-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-gray-900">指令 (Instruction)</h3>
                  <p class="text-xs sm:text-sm text-gray-600">告訴AI要執行什麼任務</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="prose prose-sm max-w-none">
              <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 sm:p-4 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
                {{ currentItem.instruction }}
              </div>
            </div>
          </div>
        </div>

        <!-- System Prompt (如果有) -->
        <div v-if="currentItem.system" class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-purple-50 to-pink-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-gray-900">系統設定 (System)</h3>
                  <p class="text-xs sm:text-sm text-gray-600">設定AI的角色和行為準則</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 sm:p-4 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
              {{ currentItem.system }}
            </div>
          </div>
        </div>

        <!-- Input (如果有) -->
        <div v-if="currentItem.input" class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-gray-900">輸入內容 (Input)</h3>
                  <p class="text-xs sm:text-sm text-gray-600">提供給指令的上下文或原始資料</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-3 sm:p-4 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
              {{ currentItem.input }}
            </div>
          </div>
        </div>

        <!-- History (如果有) -->
        <div v-if="currentItem.history && currentItem.history.length > 0" class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-orange-50 to-amber-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-gray-900">對話歷史 (History)</h3>
                  <p class="text-xs sm:text-sm text-gray-600">多輪對話的歷史記錄</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="space-y-4 sm:space-y-6">
              <div v-for="(conversation, index) in currentItem.history" :key="index" class="space-y-3 sm:space-y-4">
                <!-- 對話編號 -->
                <div class="flex items-center space-x-2">
                  <div class="w-5 h-5 sm:w-6 sm:h-6 bg-orange-100 rounded-full flex items-center justify-center">
                    <span class="text-xs font-medium text-orange-800">{{ index + 1 }}</span>
                  </div>
                  <span class="text-sm font-medium text-gray-700">對話 {{ index + 1 }}</span>
                </div>
                
                <!-- 問題 -->
                <div class="flex space-x-2 sm:space-x-3">
                  <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs sm:text-sm font-medium bg-blue-100 text-blue-800">
                    Q
                  </div>
                  <div class="flex-1">
                    <div class="text-xs text-gray-500 mb-1">問題</div>
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-2 sm:p-3 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
                      {{ conversation[0] }}
                    </div>
                  </div>
                </div>
                
                <!-- 回答 -->
                <div class="flex space-x-2 sm:space-x-3">
                  <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs sm:text-sm font-medium bg-gray-100 text-gray-800">
                    A
                  </div>
                  <div class="flex-1">
                    <div class="text-xs text-gray-500 mb-1">回答</div>
                    <div class="bg-gray-50 border border-gray-200 rounded-lg p-2 sm:p-3 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
                      {{ conversation[1] }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI回答 - 重點突出 -->
        <div class="bg-white rounded-xl border-2 border-blue-300 shadow-lg overflow-hidden">
          <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-4 sm:px-6 py-3 sm:py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-white">AI回答 (Output)</h3>
                  <p class="text-xs sm:text-sm text-blue-100">AI應該產生的正確答案</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 sm:p-4 text-gray-800 whitespace-pre-wrap leading-relaxed text-sm sm:text-base">
              {{ currentItem.output }}
            </div>
          </div>
        </div>
      </div>

      <!-- 右側：法規依據和AI回答 -->
      <div class="space-y-4 sm:space-y-6">
        <!-- 法規依據 -->
        <div v-if="currentItem.source && currentItem.source.length > 0" class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-red-50 to-rose-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 sm:w-8 sm:h-8 bg-red-100 rounded-lg flex items-center justify-center">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-base sm:text-lg font-semibold text-gray-900">法規依據 (Source)</h3>
                  <p class="text-xs sm:text-sm text-gray-600">生成資料所依據的資安法規</p>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 sm:p-6">
            <div class="space-y-3 sm:space-y-4">
              <div v-for="(src, index) in currentItem.source" :key="index" class="space-y-2 sm:space-y-3">
                <div class="bg-red-50 border border-red-200 rounded-lg p-2 sm:p-3">
                  <div class="text-xs sm:text-sm font-medium text-red-800 mb-2">{{ src }}</div>
                  <div v-if="sourceDetails[index]" class="bg-white border border-red-200 rounded p-2 sm:p-3">
                    <div class="text-xs text-red-600 font-medium mb-2">法規內容：</div>
                    <div class="text-xs sm:text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">{{ sourceDetails[index].content }}</div>
                  </div>
                  <div v-else-if="sourceLoading[index]" class="flex items-center space-x-2 text-xs sm:text-sm text-gray-500">
                    <div class="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-red-600"></div>
                    <span>載入法規內容...</span>
                  </div>
                  <div v-else-if="sourceErrors[index]" class="text-xs sm:text-sm text-red-600">
                    {{ sourceErrors[index] }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 審核操作 -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <h3 class="text-base sm:text-lg font-semibold text-gray-900">審核決定</h3>
          </div>
          <div class="p-4 sm:p-6">
            <div v-if="currentItem.review_status === 'regenerating'" class="text-center py-6 sm:py-8">
              <div class="animate-spin rounded-full h-6 w-6 sm:h-8 sm:w-8 border-b-2 border-blue-600 mx-auto mb-3 sm:mb-4"></div>
              <p class="text-sm sm:text-base text-gray-600 font-medium">重新生成中...</p>
              <p class="text-xs sm:text-sm text-gray-500 mt-2">請稍候，系統正在重新生成此筆資料</p>
            </div>
            <div v-else class="space-y-3 sm:space-y-4">
              <div class="grid grid-cols-2 gap-3 sm:gap-4">
                <button 
                  @click="handleAccept"
                  class="flex items-center justify-center space-x-1 sm:space-x-2 px-3 sm:px-6 py-3 sm:py-4 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>接受</span>
                </button>
                <button 
                  @click="showRejectModal = true"
                  class="flex items-center justify-center space-x-1 sm:space-x-2 px-3 sm:px-6 py-3 sm:py-4 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors text-sm sm:text-base"
                >
                  <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  <span>拒絕</span>
                </button>
              </div>
              <button 
                @click="nextItem"
                class="w-full px-3 sm:px-4 py-2 sm:py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors text-sm sm:text-base"
              >
                跳過此筆
              </button>
            </div>
          </div>
        </div>

        <!-- 資料狀態 -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
            <h3 class="text-base sm:text-lg font-semibold text-gray-900">資料狀態</h3>
          </div>
          <div class="p-4 sm:p-6">
            <div class="space-y-2 sm:space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-xs sm:text-sm text-gray-600">資料ID</span>
                <span class="text-xs sm:text-sm font-medium text-gray-900">#{{ currentItem.id }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs sm:text-sm text-gray-600">通過次數</span>
                <span class="text-xs sm:text-sm font-medium text-green-600">{{ currentItem.accept_count }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs sm:text-sm text-gray-600">拒絕次數</span>
                <span class="text-xs sm:text-sm font-medium text-red-600">{{ currentItem.reject_count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 拒絕模態框 -->
    <div v-if="showRejectModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-auto">
        <div class="px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900">拒絕原因</h3>
          <p class="text-xs sm:text-sm text-gray-600 mt-1">請說明拒絕這筆資料的原因，這將幫助改進資料品質</p>
        </div>
        <div class="p-4 sm:p-6">
          <textarea 
            v-model="rejectComment"
            rows="4"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm sm:text-base"
            placeholder="請詳細說明拒絕原因，例如：指令不夠清楚、內容不符合法規要求、法規依據錯誤等..."
          ></textarea>
        </div>
        <div class="px-4 sm:px-6 py-3 sm:py-4 border-t border-gray-200 flex justify-end space-x-2 sm:space-x-3">
          <button 
            @click="showRejectModal = false" 
            class="px-3 sm:px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors text-sm sm:text-base"
          >
            取消
          </button>
          <button 
            @click="handleReject" 
            class="px-3 sm:px-4 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors text-sm sm:text-base"
          >
            確認拒絕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

const { instance } = useAuth()
const toast = useToast()

const loading = ref(true)
const showRejectModal = ref(false)
const rejectComment = ref('')
const datasets = ref([])
const currentIndex = ref(0)
const sourceDetails = ref({})
const sourceLoading = ref({})
const sourceErrors = ref({})

const currentItem = computed(() => {
  if (datasets.value.length > 0 && currentIndex.value < datasets.value.length) {
    return datasets.value[currentIndex.value]
  }
  return null
})

// 解析資料來源字串，提取法規標題和條號
const parseSource = (sourceStr) => {
  // 範例: "公務機關所屬人員資通安全事項獎懲辦法第1條"
  const match = sourceStr.match(/^(.+?)第(\d+)條$/)
  if (match) {
    return {
      title: match[1].trim(),
      number: match[2]
    }
  }
  return null
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

const submitReview = async (result, comment = null) => {
  if (!currentItem.value) return
  
  try {
    await instance.post(`/api/v1/review/${currentItem.value.id}`, {
      result: result,
      comment: comment
    })
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
  if (!rejectComment.value) {
    toast.warning('請填寫拒絕原因。');
    return
  }
  submitReview('REJECT', rejectComment.value)
  showRejectModal.value = false
  rejectComment.value = ''
}

onMounted(() => {
  fetchDatasets()
})
</script> 