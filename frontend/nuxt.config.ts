// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@pinia/nuxt',
  ],
  css: [
    '~/assets/tokens.css',
    '~/assets/main.css',
  ],
  fonts: {
    families: [
      { name: 'Poppins', provider: 'google', weights: [400, 600, 700, 800] },
    ],
  },
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
      ],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },
})
