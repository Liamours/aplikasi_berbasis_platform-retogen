export const useTheme = () => {
  const isDark = useState<boolean>('retogen-theme', () => false)

  const setTheme = (value: 'light' | 'dark') => {
    isDark.value = value === 'dark'

    if (import.meta.client) {
      localStorage.setItem('theme', value)
      document.documentElement.classList.toggle('dark-mode', value === 'dark')
    }
  }

  const toggleTheme = () => {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  const initTheme = () => {
    if (!import.meta.client) return

    const saved = localStorage.getItem('theme')
    if (saved === 'dark' || saved === 'light') {
      setTheme(saved)
      return
    }

    setTheme('light')
  }

  return { isDark, setTheme, toggleTheme, initTheme }
}
