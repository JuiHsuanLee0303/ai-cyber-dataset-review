import { createRouter, createWebHistory } from 'vue-router'
import useAuth from '../store/auth'
import { useToast } from 'vue-toastification'

import Layout from '../components/Layout.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Review from '../views/Review.vue'
import AdminUsers from '../views/AdminUsers.vue'
import AdminSettings from '../views/AdminSettings.vue'
import AdminData from '../views/AdminData.vue'
import AdminRawData from '../views/AdminRawData.vue'
import AdminLegalArticles from '../views/AdminLegalArticles.vue'


const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
      },
      {
        path: 'review',
        name: 'Review',
        component: Review,
      },
      {
        path: 'admin/users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/settings',
        name: 'AdminSettings',
        component: AdminSettings,
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/data',
        name: 'AdminData',
        component: AdminData,
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/raw-data',
        name: 'AdminRawData',
        component: AdminRawData,
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/legal-articles',
        name: 'AdminLegalArticles',
        component: AdminLegalArticles,
        meta: { roles: ['admin'] },
      }
    ]
  },
  // Redirect any other path to login
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const { state } = useAuth()
  const toast = useToast()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiredRoles = to.matched.flatMap(record => record.meta.roles || [])

  if (requiresAuth && !state.isLoggedIn) {
    // Need to login
    next('/login')
  } else if (requiresAuth && requiredRoles.length > 0 && !requiredRoles.includes(state.user.role)) {
    // User does not have the required role
    toast.error('您沒有權限訪問此頁面。')
    next('/') // Redirect to dashboard
  } else {
    // Proceed as normal
    next()
  }
})

export default router 