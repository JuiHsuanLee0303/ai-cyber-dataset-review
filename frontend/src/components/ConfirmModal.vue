<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="text-xl font-bold text-neutral-800">{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p class="text-neutral-600">{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button @click="onCancel" class="btn btn-secondary">
          取消
        </button>
        <button @click="onConfirm" class="btn btn-danger">
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