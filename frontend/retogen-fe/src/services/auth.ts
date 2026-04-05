import { api } from '@/lib/api'

export type LoginRequest = {
  email: string
  password: string
}

export type LoginResponse = {
  confirmation: string
  token?: string
}

export async function login(payload: LoginRequest) {
  const response = await api.post<LoginResponse>('/auth/login', payload)
  return response.data
}