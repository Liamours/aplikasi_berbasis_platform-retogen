export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const buildHeaders = (requiresAuth: boolean): Record<string, string> => {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (requiresAuth && authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    }
    return headers
  }

  const get = async <T>(path: string, requiresAuth = false): Promise<T> => {
    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      method: 'GET',
      headers: buildHeaders(requiresAuth)
    })
  }

  const post = async <T>(path: string, body: Record<string, any> = {}, requiresAuth = false): Promise<T> => {
    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      method: 'POST',
      headers: buildHeaders(requiresAuth),
      body
    })
  }

  const put = async <T>(path: string, body: Record<string, any> = {}, requiresAuth = false): Promise<T> => {
    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      method: 'PUT',
      headers: buildHeaders(requiresAuth),
      body
    })
  }

  const del = async <T>(path: string, requiresAuth = false): Promise<T> => {
    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      method: 'DELETE',
      headers: buildHeaders(requiresAuth)
    })
  }

  return { get, post, put, del }
}