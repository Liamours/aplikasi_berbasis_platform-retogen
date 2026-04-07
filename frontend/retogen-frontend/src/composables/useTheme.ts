import { ref } from 'vue'

export const isDark = ref(localStorage.getItem('theme') === 'dark')

export function toggleTheme() {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}