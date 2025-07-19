<template>
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- Header Section -->
    <div class="text-center mb-12">
      <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-slate-700 to-slate-900 rounded-2xl mb-6 shadow-lg">
        <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
      </div>
      <h1 class="md:text-4xl text-2xl font-bold text-slate-900 mb-4 tracking-tight">AI 資安資料集審核系統</h1>
      <p class="hidden md:block md:text-lg text-slate-600 max-w-4xl mx-auto leading-relaxed font-medium">
        結合 AI 生成與資安專家審核機制的資料集建構平台
      </p>
      <div class="mt-4 flex flex-col md:flex-row items-center justify-center space-x-6 text-sm text-slate-500 font-medium">
        <span class="flex items-center space-x-2 mb-2 md:mb-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
          </svg>
          <span>國立臺北商業大學 人工智慧與商業應用碩士班</span>
        </span>
        <span class="text-slate-300 md:block hidden">|</span>
        <span class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
          <span>研究生：李睿軒 論文研究與實作平台</span>
        </span>
      </div>
    </div>

    <!-- 第一區塊：關於本系統 -->
    <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 mb-8">
      <div class="flex items-center space-x-3 mb-6">
        <div class="p-3 bg-slate-100 rounded-xl">
          <svg class="w-6 h-6 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-slate-900">關於本系統</h2>
      </div>
      <div class="prose prose-lg max-w-none text-slate-700 leading-relaxed">
        <p class="mb-4 text-sm md:text-base">
          隨著大型語言模型在專業場域的應用普及，如何建立兼具可靠性與可追溯性的高品質指令微調資料集已成為關鍵挑戰。傳統上完全仰賴領域專家建立資料集需耗費大量人力成本，且缺乏標準化的審核流程。
        </p>
        <p class="mb-4 text-sm md:text-base">
          為解決此一問題，本系統提出結合生成式人工智慧、領域專家審核與迴圈式自動再生成之協同流程，並以資安法規文本為驗證情境，旨在建立一套可重複、可追溯且高效率的專業領域資料集建構方法。
        </p>
        <div class="bg-gradient-to-r from-slate-50 to-slate-100 rounded-xl p-4 border border-slate-200">
          <h4 class="font-bold text-slate-800 mb-3 text-base">系統創立理由</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h5 class="font-semibold text-slate-800 mb-1 text-sm">1. 解決專業領域資料集建構挑戰</h5>
              <p class="text-slate-700 text-xs">專業性要求高、審核標準複雜、需要多方專家協作</p>
            </div>
            <div>
              <h5 class="font-semibold text-slate-800 mb-1 text-sm">2. 降低人工成本與提升效率</h5>
              <p class="text-slate-700 text-xs">透過AI輔助減少重複性工作，標準化審核流程</p>
            </div>
            <div>
              <h5 class="font-semibold text-slate-800 mb-1 text-sm">3. 確保資料品質與可追溯性</h5>
              <p class="text-slate-700 text-xs">建立完整的審核軌跡，支援合規性要求</p>
            </div>
            <div>
              <h5 class="font-semibold text-slate-800 mb-1 text-sm">4. 提供可擴展的解決方案</h5>
              <p class="text-slate-700 text-xs">方法論可應用於其他高度規範的專業領域</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 第二區塊：本系統使用方式 -->
    <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 mb-8">
      <div class="flex items-center space-x-3 mb-6">
        <div class="p-3 bg-slate-100 rounded-xl">
          <svg class="w-6 h-6 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-slate-900">本系統使用方式</h2>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 class="text-base md:text-lg font-bold text-slate-800 mb-4">系統角色與功能</h3>
          <p class="mb-4 text-sm md:text-base">
            本系統作為碩士論文研究的核心實驗平台，整合研究過程中的各個關鍵環節，從資料生成到品質評估，提供端到端的實驗環境。
          </p>
          <ul class="space-y-3 text-slate-700">
            <li class="flex items-start space-x-3">
              <div class="w-2 h-2 bg-slate-600 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <span class="text-sm md:text-base font-medium">實驗驗證平台</span>
                <p class="text-xs md:text-sm text-slate-600 mt-1">驗證協同流程的理論假設</p>
              </div>
            </li>
            <li class="flex items-start space-x-3">
              <div class="w-2 h-2 bg-slate-600 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <span class="text-sm md:text-base font-medium">資料收集工具</span>
                <p class="text-xs md:text-sm text-slate-600 mt-1">系統化收集實驗數據</p>
              </div>
            </li>
            <li class="flex items-start space-x-3">
              <div class="w-2 h-2 bg-slate-600 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <span class="text-sm md:text-base font-medium">流程管理系統</span>
                <p class="text-xs md:text-sm text-slate-600 mt-1">標準化協同審核流程</p>
              </div>
            </li>
            <li class="flex items-start space-x-3">
              <div class="w-2 h-2 bg-slate-600 rounded-full mt-2 flex-shrink-0"></div>
              <div>
                <span class="text-sm md:text-base font-medium">成果展示介面</span>
                <p class="text-xs md:text-sm text-slate-600 mt-1">直觀呈現研究成果</p>
              </div>
            </li>
          </ul>
        </div>
        <div>
          <h3 class="text-base md:text-lg font-bold text-slate-800 mb-4">核心特色</h3>
          <div class="grid grid-cols-1 gap-3">
            <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 border border-slate-200">
              <h4 class="font-bold text-slate-800 mb-1 text-sm">AI 輔助生成</h4>
              <p class="text-slate-700 text-xs">整合多種大型語言模型，透過智能提示詞工程生成高品質的資安指令微調資料集</p>
            </div>
            <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 border border-slate-200">
              <h4 class="font-bold text-slate-800 mb-1 text-sm">多專家協同</h4>
              <p class="text-slate-700 text-xs">支援多位資安專家同時參與審核，建立標準化的協同審核機制</p>
            </div>
            <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 border border-slate-200">
              <h4 class="font-bold text-slate-800 mb-1 text-sm">迴圈優化</h4>
              <p class="text-slate-700 text-xs">基於專家回饋自動觸發重新生成流程，實現持續改進的迭代優化機制</p>
            </div>
            <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 border border-slate-200">
              <h4 class="font-bold text-slate-800 mb-1 text-sm">品質監控</h4>
              <p class="text-slate-700 text-xs">提供即時品質指標與統計分析，支援資料集品質的量化評估</p>
            </div>
            <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg p-3 border border-slate-200">
              <h4 class="font-bold text-slate-800 mb-1 text-sm">可追溯性</h4>
              <p class="text-slate-700 text-xs">完整的審核軌跡記錄與版本控制，確保資料集建構過程的透明性</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 第三區塊：研究概述 -->
    <div class="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 mb-8">
      <div class="flex items-center space-x-3 mb-6">
        <div class="p-3 bg-slate-100 rounded-xl">
          <svg class="w-6 h-6 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
          </svg>
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-slate-900">研究概述</h2>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 class="text-base md:text-lg font-bold text-slate-800 mb-4">研究背景</h3>
          <p class="mb-4 text-sm md:text-base">
            本研究以資安法規文本為驗證情境，提出結合生成式人工智慧、領域專家審核與迴圈式自動再生成之協同流程，旨在解決專業領域資料集建構的實務挑戰。
          </p>
          <div class="bg-slate-50 rounded-xl p-4 border-l-4 border-slate-300">
            <h4 class="font-semibold text-slate-800 mb-2 text-base">研究重點</h4>
            <ul class="space-y-1 text-slate-700">
              <li class="flex items-start space-x-2">
                <div class="w-1.5 h-1.5 bg-slate-600 rounded-full mt-1.5 flex-shrink-0"></div>
                <span class="text-xs">協同流程設計與人機協作機制</span>
              </li>
              <li class="flex items-start space-x-2">
                <div class="w-1.5 h-1.5 bg-slate-600 rounded-full mt-1.5 flex-shrink-0"></div>
                <span class="text-xs">多層次審核標準與品質控制機制</span>
              </li>
              <li class="flex items-start space-x-2">
                <div class="w-1.5 h-1.5 bg-slate-600 rounded-full mt-1.5 flex-shrink-0"></div>
                <span class="text-xs">可追溯性架構與版本控制系統</span>
              </li>
              <li class="flex items-start space-x-2">
                <div class="w-1.5 h-1.5 bg-slate-600 rounded-full mt-1.5 flex-shrink-0"></div>
                <span class="text-xs">效率優化策略與自動化流程</span>
              </li>
            </ul>
          </div>
        </div>
        <div>
          <h3 class="text-base md:text-lg font-bold text-slate-800 mb-4">研究流程</h3>
          <div class="space-y-4">
            <div class="flex items-start space-x-3">
              <div class="w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">1</div>
              <div>
                <h4 class="font-semibold text-slate-800 mb-1 text-sm">AI 生成階段</h4>
                <p class="text-slate-600 text-xs">透過提示詞工程導入相關法規條文，驅動模型生成候選指令微調資料集</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">2</div>
              <div>
                <h4 class="font-semibold text-slate-800 mb-1 text-sm">專家審核階段</h4>
                <p class="text-slate-600 text-xs">多位資安專家基於正確性、完整性與可操作性進行多重審核</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">3</div>
              <div>
                <h4 class="font-semibold text-slate-800 mb-1 text-sm">品質評估階段</h4>
                <p class="text-slate-600 text-xs">符合門檻者納入最終資料庫，未通過者進入重新生成流程</p>
              </div>
            </div>
            <div class="flex items-start space-x-3">
              <div class="w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">4</div>
              <div>
                <h4 class="font-semibold text-slate-800 mb-1 text-sm">迭代優化階段</h4>
                <p class="text-slate-600 text-xs">利用專家回饋作為大型語言模型重新生成之參考，迭代至達到既定品質標準</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 第四區塊：作者介紹 -->
    <div class="bg-gradient-to-br from-slate-50 via-slate-100 to-slate-200 rounded-2xl p-6 shadow-xl border border-slate-200">
      <div class="text-center mb-6">
        <h2 class="text-xl md:text-2xl font-bold text-slate-900 mb-4">作者介紹</h2>
        <p class="text-base md:text-lg text-slate-700 max-w-5xl mx-auto leading-relaxed font-medium">
          本研究透過系統化的協同流程設計，為專業領域資料集建構提供可參考的解決方案。
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-4 shadow-md">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-800">李睿軒 Jui-Hsuan Lee</h3>
              <p class="text-xs text-slate-600">研究生</p>
            </div>
          </div>
          <div class="space-y-1 text-xs text-slate-700">
            <div class="flex items-center">
              <span class="font-medium text-slate-800">學位：</span>
              <span class="ml-2">人工智慧與商業應用碩士班</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium text-slate-800">學校：</span>
              <span class="ml-2">國立臺北商業大學</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium text-slate-800">聯絡信箱：</span>
              <span class="ml-2 font-mono text-indigo-700">11365008@ntub.edu.tw</span>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-md">
          <div class="flex items-center space-x-3 mb-3">
            <div class="w-12 h-12 bg-gradient-to-br from-green-600 to-teal-700 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-800">徐國鈞 教授</h3>
              <p class="text-xs text-slate-600">指導教授</p>
            </div>
          </div>
          <div class="space-y-1 text-xs text-slate-700">
            <div class="flex items-center">
              <span class="font-medium text-slate-800">職稱：</span>
              <span class="ml-2">教授</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium text-slate-800">系所：</span>
              <span class="ml-2">資訊管理系</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium text-slate-800">學校：</span>
              <span class="ml-2">國立臺北商業大學</span>
            </div>
          </div>
        </div>
      </div>
      <div class="mt-6 text-center">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded-xl p-3 shadow-md">
            <div class="md:hidden w-8 h-8 bg-slate-200 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg class="w-4 h-4 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="font-bold text-slate-800 mb-1 text-xs md:text-sm">理論貢獻</h3>
            <p class="text-slate-600 text-xs">提出協同流程的理論框架，為專業領域資料集建構提供新的方法論</p>
          </div>
          <div class="bg-white rounded-xl p-3 shadow-md">
            <div class="md:hidden w-8 h-8 bg-slate-200 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg class="w-4 h-4 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="font-bold text-slate-800 mb-1 text-xs md:text-sm">實務價值</h3>
            <p class="text-slate-600 text-xs">提供完整的實作平台，可直接應用於資安法規領域的資料集建構</p>
          </div>
          <div class="bg-white rounded-xl p-3 shadow-md">
            <div class="md:hidden w-8 h-8 bg-slate-200 rounded-lg flex items-center justify-center mx-auto mb-2">
              <svg class="w-4 h-4 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="font-bold text-slate-800 mb-1 text-xs md:text-sm">推廣潛力</h3>
            <p class="text-slate-600 text-xs">方法論可擴展至其他專業領域，具有廣泛的應用前景</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 這個頁面不需要特殊的邏輯
</script>

<style scoped>
/* 自定義樣式 */
.prose {
  line-height: 1.6;
}

.prose p {
  margin-bottom: 1rem;
}

/* 漸變背景動畫 */
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.bg-gradient-to-br {
  background-size: 200% 200%;
  animation: gradient 20s ease infinite;
}

/* 學術性字體優化 */
.font-bold {
  font-weight: 700;
}

.font-semibold {
  font-weight: 600;
}

.font-medium {
  font-weight: 500;
}

/* 陰影效果 */
.shadow-xl {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 圓角優化 */
.rounded-2xl {
  border-radius: 1rem;
}

.rounded-xl {
  border-radius: 0.75rem;
}

.rounded-lg {
  border-radius: 0.5rem;
}

/* 間距優化 */
.space-x-3 > * + * {
  margin-left: 0.75rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

/* 過渡效果 */
.transition-colors {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style> 