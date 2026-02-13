import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DisplayView from '../views/DisplayView.vue'
import UploadView from '../views/UploadView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      component: HomeView
    },
    {
      path: '/display',
      component: DisplayView
    },
    {
      path: '/upload',
      component: UploadView
    },
  ]
})

export default router
