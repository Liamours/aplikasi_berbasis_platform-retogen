import { defineStore } from 'pinia'

type UserRole = 'admin' | 'user' | null

interface AuthUser {
  email: string
  username: string
  fullname?: string
  role: UserRole
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '' as string,
    user: null as AuthUser | null,
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.user?.role === 'admin'
  },

  actions: {
    setAuth(payload: { token: string; user?: AuthUser | null }) {
      this.token = payload.token
      this.user = payload.user ?? null
      this.isAuthenticated = Boolean(payload.token)

      if (import.meta.client) {
        localStorage.setItem('retogen-token', this.token)
        localStorage.setItem('retogen-user', JSON.stringify(this.user))
      }
    },

    clearAuth() {
      this.token = ''
      this.user = null
      this.isAuthenticated = false

      if (import.meta.client) {
        localStorage.removeItem('retogen-token')
        localStorage.removeItem('retogen-user')
      }
    },

    initFromStorage() {
      if (!import.meta.client) return

      const token = localStorage.getItem('retogen-token') || ''
      const userRaw = localStorage.getItem('retogen-user')

      this.token = token
      this.user = userRaw ? JSON.parse(userRaw) : null
      this.isAuthenticated = Boolean(token)
    },

    setUser(user: AuthUser | null) {
      this.user = user

      if (import.meta.client) {
        localStorage.setItem('retogen-user', JSON.stringify(user))
      }
    }
  }
})