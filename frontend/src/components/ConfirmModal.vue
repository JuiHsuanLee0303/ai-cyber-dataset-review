<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md mx-4">
      <h3 class="text-xl font-bold mb-4 text-gray-800">{{ title }}</h3>
      <p class="text-gray-600 mb-6">{{ message }}</p>
      <div class="mt-6 flex justify-end space-x-4">
        <button @click="onCancel" class="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 font-semibold">
          取消
        </button>
        <button @click="onConfirm" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold">
          確認
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import useConfirm from '../composables/useConfirm'

const { show, title, message, onConfirm, onCancel } = useConfirm()
</script> 