export default defineNuxtRouteMiddleware(() => {
  if (import.meta.server) return

  const authStore = useAuthStore()
  authStore.initFromStorage()

  if (!authStore.isAdmin) {
    return navigateTo('/main')
  }
})
