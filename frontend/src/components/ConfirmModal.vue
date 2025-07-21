<template>
  <Transition name="modal" appear>
    <div v-if="show" class="modal-overlay" @click="onCancel">
      <div class="modal-content" @click.stop>
        <!-- Header with Icon -->
        <div class="modal-header bg-gradient-to-r from-red-50 to-orange-50 border-b border-red-200">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-bold text-gray-900">{{ title }}</h3>
              <p class="text-sm text-gray-600">請仔細確認您的操作</p>
            </div>
          </div>
          <button @click="onCancel" class="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- Body with Enhanced Content -->
        <div class="modal-body">
          <div class="flex items-start space-x-4">
            <!-- Warning Icon -->
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p class="text-gray-700 leading-relaxed">{{ message }}</p>
              
              <!-- Warning Box -->
              <div class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-start space-x-3">
                  <svg class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                  </svg>
                  <div>
                    <h4 class="text-sm font-semibold text-red-800 mb-1">重要提醒</h4>
                    <p class="text-sm text-red-700">此操作無法復原，請確認您要刪除的資料是正確的。</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer with Enhanced Buttons -->
        <div class="modal-footer bg-gray-50 border-t border-gray-200">
          <div class="flex justify-between items-center w-full">
            <div class="text-sm text-gray-500">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                按 ESC 鍵可取消操作
              </span>
            </div>
            <div class="flex items-center space-x-4">
              <button 
                @click="onCancel" 
                class="cancel-btn"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                取消
              </button>
              <button 
                @click="onConfirm" 
                class="confirm-btn"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                確認刪除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import useConfirm from '../composables/useConfirm'
import { onMounted, onUnmounted } from 'vue'

const { show, title, message, onConfirm, onCancel } = useConfirm()

// Keyboard event handling
const handleKeydown = (event) => {
  if (show.value && event.key === 'Escape') {
    onCancel()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4;
  backdrop-filter: blur(4px);
}

.modal-content {
  @apply bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] flex flex-col;
  animation: modalSlideIn 0.3s ease-out;
}

.modal-header {
  @apply flex justify-between items-center p-6 flex-shrink-0;
}

.modal-body {
  @apply p-6 overflow-y-auto flex-1;
}

.modal-footer {
  @apply flex justify-between items-center p-6 flex-shrink-0;
}

/* Enhanced Button Styles */
.cancel-btn {
  @apply inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg transition-all duration-200 ease-in-out;
  @apply bg-white border border-gray-300 text-gray-700;
  @apply hover:bg-gray-50 hover:border-gray-400 hover:text-gray-800;
  @apply focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2;
  @apply active:transform active:scale-95;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.cancel-btn:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.confirm-btn {
  @apply inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg transition-all duration-200 ease-in-out;
  @apply bg-gradient-to-r from-red-600 to-red-700 text-white;
  @apply hover:from-red-700 hover:to-red-800;
  @apply focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2;
  @apply active:transform active:scale-95;
  box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.3), 0 2px 4px -1px rgba(220, 38, 38, 0.2);
}

.confirm-btn:hover {
  box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.4), 0 4px 6px -2px rgba(220, 38, 38, 0.3);
}

.confirm-btn:active {
  box-shadow: 0 2px 4px -1px rgba(220, 38, 38, 0.3), 0 1px 2px -1px rgba(220, 38, 38, 0.2);
}

/* Modal animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .modal-content {
    @apply max-w-md;
  }
  
  .modal-header {
    @apply p-4;
  }
  
  .modal-body {
    @apply p-4;
  }
  
  .modal-footer {
    @apply p-4;
  }
  
  .cancel-btn,
  .confirm-btn {
    @apply px-4 py-2.5 text-sm;
  }
}

@media (max-width: 480px) {
  .modal-content {
    @apply max-w-sm;
  }
  
  .modal-footer {
    @apply flex-col space-y-3;
  }
  
  .modal-footer > div:first-child {
    @apply order-2;
  }
  
  .modal-footer > div:last-child {
    @apply order-1 w-full;
  }
  
  .cancel-btn,
  .confirm-btn {
    @apply w-full justify-center;
  }
}
</style> 