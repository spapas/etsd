import { createApp } from 'vue';

import * as VueRouter from 'vue-router';
import { mapState } from 'vuex'

import Store from './Store';

import Home from './components/Home';
import Nav from './components/Nav';
import Login from './components/Login';

const Logout = { template: '<div>Logout</div>' }
const Messages = { template: '<div>Messages</div>' }
const Help = { template: '<div>Help</div>' }
const PublicKeyList = { template: '<div>PublicKeyList</div>' }
const PrivateKeyLoad = { template: '<div>PrivateKeyLoad</div>' }

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/logout', component: Logout },
  { path: '/messages', component: Messages },
  { path: '/help', component: Help },
  { path: '/public_key_list', component: PublicKeyList },
  { path: '/privatekey_load', component: PrivateKeyLoad },
]

const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes, 
})


const app = createApp({
  computed: mapState([
    'user', 'pkdata', 'loading'
  ])
})
app.use(router)
app.use(Store)

app.component('etsd-nav', Nav)

app.mount('#app')