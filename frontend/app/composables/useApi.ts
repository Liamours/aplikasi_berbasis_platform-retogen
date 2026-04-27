export const useApi = () => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const apiBase = String(config.public.apiBase).replace(/\/$/, '')

  const buildHeaders = (requiresAuth: boolean): Record<string, string> => {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    }

    if (requiresAuth && authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    }

    return headers
  }

  const request = async <T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    path: string,
    body?: Record<string, any>,
    requiresAuth = false
  ): Promise<T> => {
    return await $fetch<T>(`${apiBase}${path}`, {
      method,
      headers: buildHeaders(requiresAuth),
      body
    })
  }

  const get = <T>(path: string, requiresAuth = false) =>
    request<T>('GET', path, undefined, requiresAuth)

  const post = <T>(path: string, body: Record<string, any> = {}, requiresAuth = false) =>
    request<T>('POST', path, body, requiresAuth)

  const put = <T>(path: string, body: Record<string, any> = {}, requiresAuth = false) =>
    request<T>('PUT', path, body, requiresAuth)

  const del = <T>(path: string, requiresAuth = false) =>
    request<T>('DELETE', path, undefined, requiresAuth)

  return { get, post, put, del }
}