import { createRouter, createWebHistory } from 'vue-router'
import BasePage from './components/BasePage.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import AdminDash from './components/AdminDash.vue'
import AdminHome from './components/AdminHome.vue'
import ParkingLot from './components/ParkingLot.vue'
import UserDash from './components/UserDash.vue'
import UserHome from './components/UserHome.vue'
import UserSummary from './components/UserSummary.vue'
import AdminViewUser from './components/AdminViewUser.vue'


const routes = [
  { path: '/', component: BasePage },
  { path: '/smartpark/login', component: Login },
  { path: '/smartpark/register', component: Register },
  {
    path: '/admin/dashboard',
    component: AdminDash,
    children: [
      { path: '', component: AdminHome },
      { path: '/admin/dashboard/parkinglots', component: ParkingLot },
      { path: '/admin/dashboard/users', component: AdminViewUser }
    ]
  },
  {
    path: '/user/dashboard',
    component: UserDash,
    children: [
      { path: '', component: UserHome },
      { path: 'summary', component: UserSummary }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
