import api from '@/lib/axios'

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  confirmation: string
  token?: string
}

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const { data } = await api.post<LoginResponse>('/auth/login', payload)
  return data
}