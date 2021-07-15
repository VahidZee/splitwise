import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '@/pages/Dashboard'
import Login from "@/pages/Login";
import Login2 from "@/pages/Login2";
import AddGroup from "../pages/AddGroup";
import AddPayment from "../pages/AddPayment";
import AddFriend from "@/pages/AddFriend";
import UserInfo from "@/pages/UserInfo";
import Pay from "../pages/Pay";

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
        },
        {
            path: '/add_payment',
            name: 'Add a payment',
            component: AddPayment
        },
        {
            path: '/dash',
            name: 'Dashboard',
            component: Dashboard
        }, {
            path: '/add_friend',
            name: 'Add a friend',
            component: AddFriend
        }, {
            path: '/user_info',
            name: 'User Info',
            component: UserInfo
        }, {
            path: '/pay',
            name: 'Pay expense',
            component: Pay
        },
    ]
})
