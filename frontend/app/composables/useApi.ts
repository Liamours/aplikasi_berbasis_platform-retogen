export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const post = async <T>(path: string, body: Record<string, any> = {}, requiresAuth = false): Promise<T> => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }

    if (requiresAuth && authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    }

    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      method: 'POST',
      headers,
      body
    })
  }

  return { post }
}