import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import { getToken, isTokenExpired, removeToken } from '@/lib/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
  ],
})

router.beforeEach((to) => {
  const token = getToken()

  if (token && isTokenExpired(token)) {
    removeToken()
  }

  const validToken = getToken()

  if (to.meta.requiresAuth && !validToken) {
    return '/login'
  }

  if (to.path === '/login' && validToken) {
    return '/'
  }

  return true
})

export default router