import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import VendorHome from '../views/VendorHome.vue'
import VendorLogin from '../views/VendorLogin.vue'
import VendorSignUp from '../views/VendorSignUp.vue'
import VendorAdd from '../views/VendorAdd.vue'
import VendorSingleProduct from '../views/VendorSingleProduct.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/vendors/login',
    name: 'vendor-login',
    component: VendorLogin,
    meta: {
      title: `Jiji | Vendor Login`
    }
  },
  {
    path: '/become-a-vendor',
    name: 'vendor-signup',
    component: VendorSignUp,
    meta: {
      title: `Jiji | Become A Vendor`
    }
  },
  {
    path: '/vendors',
    name: 'vendor-home',
    component: VendorHome,
    meta: {
      title: `Jiji | Vendors`,
      requireAuth: true
    }
  },
  {
    path: '/vendors/add-product',
    name: 'vendor-add-product',
    component: VendorAdd,
    meta: {
      title: `Jiji | Vendors | Add Product`,
      requireAuth: true
    }
  },
  {
    path: '/vendors/products/:slug',
    name: 'candidates',
    component: VendorSingleProduct,
    meta: {
      title: `Jiji | Vendors | Products`,
      requireAuth: true
    }
  },
]


const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);

  if(nearestWithTitle) document.title = nearestWithTitle.meta.title;

  if(to.matched.some(record => record.meta.requireAuth)) {
    let token = localStorage.getItem('token');
    if (token) {
      return next()
    }
    next({
      path: '/vendors/login',
      nextUrl: to.fullPath
    }) 
  } 
  
  else {
    next() 
  }
})

export default router
