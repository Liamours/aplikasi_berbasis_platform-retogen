export default defineNuxtPlugin(() => {
  const { initTheme } = useTheme()
  const authStore = useAuthStore()

  initTheme()
  authStore.initFromStorage()
})