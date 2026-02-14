import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/Home.vue')
        },
        {
          path: '/products',
          name: 'products',
          component: () => import('@/views/ProductList.vue')
        },
        {
          path: '/products/:slug',
          name: 'product-detail',
          component: () => import('@/views/ProductDetail.vue')
        },
        {
          path: '/cart',
          name: 'cart',
          component: () => import('@/views/Cart.vue')
        },
        {
          path: '/checkout',
          name: 'checkout',
          component: () => import('@/views/Checkout.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/orders',
          name: 'orders',
          component: () => import('@/views/OrderHistory.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/orders/:id',
          name: 'order-detail',
          component: () => import('@/views/OrderDetail.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/wishlist',
          name: 'wishlist',
          component: () => import('@/views/Wishlist.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/balance',
          name: 'balance',
          component: () => import('@/views/Balance.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/profile',
          name: 'profile',
          component: () => import('@/views/Profile.vue'),
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/auth',
      component: () => import('@/layouts/AuthLayout.vue'),
      meta: { guestOnly: true },
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/auth/Login.vue')
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/auth/Register.vue')
        }
      ]
    },
    {
      path: '/seller',
      component: () => import('@/layouts/SellerLayout.vue'),
      meta: { requiresAuth: true, requiresSeller: true },
      children: [
        {
          path: 'dashboard',
          name: 'seller-dashboard',
          component: () => import('@/views/seller/Dashboard.vue')
        },
        {
          path: 'products',
          name: 'seller-products',
          component: () => import('@/views/seller/Products.vue')
        },
        {
          path: 'products/create',
          name: 'seller-product-create',
          component: () => import('@/views/seller/ProductForm.vue')
        },
        {
          path: 'products/:id/edit',
          name: 'seller-product-edit',
          component: () => import('@/views/seller/ProductForm.vue')
        },
        {
          path: 'orders',
          name: 'seller-orders',
          component: () => import('@/views/seller/Orders.vue')
        },
        {
          path: 'keys',
          name: 'seller-keys',
          component: () => import('@/views/seller/DigitalKeys.vue')
        }
      ]
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/Dashboard.vue')
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/Users.vue')
        },
        {
          path: 'products',
          name: 'admin-products',
          component: () => import('@/views/admin/Products.vue')
        },
        {
          path: 'products/create',
          name: 'admin-product-create',
          component: () => import('@/views/admin/ProductCreate.vue')
        },
        {
          path: 'products/:id/edit',
          name: 'admin-product-edit',
          component: () => import('@/views/admin/ProductCreate.vue')
        },
        {
          path: 'categories',
          name: 'admin-categories',
          component: () => import('@/views/admin/Categories.vue')
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: () => import('@/views/admin/Orders.vue')
        },
        {
          path: 'reviews',
          name: 'admin-reviews',
          component: () => import('@/views/admin/Reviews.vue')
        },
        {
          path: 'keys',
          name: 'admin-keys',
          component: () => import('@/views/admin/DigitalKeys.vue')
        },
        {
          path: 'payments',
          name: 'admin-payments',
          component: () => import('@/views/admin/Payments.vue')
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  
  // Check if route is for guests only
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  
  // Check if route requires seller role
  if (to.meta.requiresSeller && !authStore.isSeller) {
    next({ name: 'home' })
    return
  }
  
  // Check if route requires admin role
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router
