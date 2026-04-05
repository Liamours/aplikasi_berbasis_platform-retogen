export type LoginPayload = {
  email: string
  password: string
}

export type LoginResponse = {
  confirmation: string
  token?: string
}

export type DecodedToken = {
  email: string
  role: 'user' | 'admin'
  exp: number
}

export function saveToken(token: string) {
  localStorage.setItem('retogen_token', token)
}

export function getToken() {
  return localStorage.getItem('retogen_token')
}

export function removeToken() {
  localStorage.removeItem('retogen_token')
}

export function decodeJwt<T = DecodedToken>(token: string): T | null {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null

    const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), '=')
    const json = atob(padded)

    return JSON.parse(json) as T
  } catch {
    return null
  }
}

export function isTokenExpired(token: string) {
  const decoded = decodeJwt(token)

  if (!decoded?.exp) return true

  const nowInSeconds = Math.floor(Date.now() / 1000)
  return decoded.exp < nowInSeconds
}