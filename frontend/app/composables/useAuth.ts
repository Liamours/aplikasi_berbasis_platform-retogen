import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  UserDetailsResponse
} from '~/types/api'

export const useAuth = () => {
  const { post } = useApi()
  const authStore = useAuthStore()

  const login = async (payload: LoginRequest) => {
    const response = await post<LoginResponse>('/auth/login', payload, false)

    if (response.confirmation === 'login successful' && response.token) {
      authStore.setAuth({
        token: response.token
      })

      await fetchSelf()
    }

    return response
  }

  const register = async (payload: RegisterRequest) => {
    return await post<RegisterResponse>('/auth/registration', payload, false)
  }

  const fetchSelf = async () => {
    const response = await post<UserDetailsResponse>('/user/get_details', {}, true)

    if (response.confirmation === 'successful') {
      authStore.setUser({
        email: response.user.email,
        username: response.user.username,
        fullname: response.user.fullname,
        role: response.user.role === 'admin' ? 'admin' : 'user'
      })
    }

    return response
  }

  const logout = () => {
    authStore.clearAuth()
    return navigateTo('/')
  }

  return {
    login,
    register,
    fetchSelf,
    logout
  }
}