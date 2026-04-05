import { computed } from 'vue'
import { clearToken, getToken, parseJwtPayload, setToken } from '@/lib/auth'

type JwtPayload = {
  email: string
  role: 'user' | 'admin'
  exp: number
}

export function useAuth() {
  const token = computed(() => getToken())

  const user = computed(() => {
    const currentToken = token.value
    if (!currentToken) return null
    return parseJwtPayload<JwtPayload>(currentToken)
  })

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  function saveLoginToken(token: string) {
    setToken(token)
  }

  function logout() {
    clearToken()
  }

  return {
    token,
    user,
    isLoggedIn,
    isAdmin,
    saveLoginToken,
    logout,
  }
}