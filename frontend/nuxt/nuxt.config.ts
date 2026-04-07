// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2026-04-07',
  devtools: { enabled: true },

  modules: [
    '@pinia/nuxt',
    '@nuxtjs/color-mode',
    '@nuxt/icon',
    '@nuxt/fonts'
  ],

  css: [
    '~/assets/css/tokens.css',
    '~/assets/css/main.css'
  ],

  app: {
    head: {
      title: 'RetoGen',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'RetoGen frontend with Nuxt + Vue + FastAPI backend' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },

  colorMode: {
    classSuffix: '',
    preference: 'light',
    fallback: 'light',
    storageKey: 'retogen-theme'
  },

  fonts: {
    families: [
      {
        name: 'Poppins',
        provider: 'google',
        weights: [400, 600, 700, 800]
      }
    ]
  }
})
