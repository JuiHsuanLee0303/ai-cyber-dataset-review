import { ref, readonly } from 'vue'

const show = ref(false)
const title = ref('')
const message = ref('')

let resolvePromise = null

const useConfirm = () => {
  const confirm = (newTitle, newMessage) => {
    title.value = newTitle
    message.value = newMessage
    show.value = true
    return new Promise((resolve) => {
      resolvePromise = resolve
    })
  }

  const onConfirm = () => {
    show.value = false
    if (resolvePromise) {
      resolvePromise(true)
    }
  }

  const onCancel = () => {
    show.value = false
    if (resolvePromise) {
      resolvePromise(false)
    }
  }

  return {
    show: readonly(show),
    title: readonly(title),
    message: readonly(message),
    confirm,
    onConfirm,
    onCancel,
  }
}

export default useConfirm 