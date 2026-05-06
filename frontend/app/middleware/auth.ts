export default defineNuxtRouteMiddleware(() => {
  const authStore = useAuthStore()

  if (import.meta.server) {
    return
  }

  authStore.initFromStorage()

  if (!authStore.token) {
    return navigateTo('/')
  }
})