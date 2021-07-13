import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/pages/Home'
import Login from "@/pages/Login";
import Login2 from "@/pages/Login2";
import AddGroup from "../pages/AddGroup";

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Login2',
            component: Login2
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/add_group',
            name: 'Add a group',
            component: AddGroup
        }
    ]
})
