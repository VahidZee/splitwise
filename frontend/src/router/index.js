import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/pages/Home'
import Login from "@/pages/Login";
import Login2 from "@/pages/Login2";

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },
        {
            path: '/login',
            name: 'Login2',
            component: Login2
        },
    ]
})
