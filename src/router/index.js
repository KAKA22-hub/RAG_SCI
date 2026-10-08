import {createRouter, createWebHashHistory,createWebHistory} from "vue-router"

const router = createRouter({
    history: createWebHistory(),
    routes:[
        {path: '/',redirect: 'login'},
        {
            path: '/login',
            meta: {
                isLogin: false
            },
            component: () => import('../components/Login.vue')
        },
        {
            path: '/chat',
            meta: {
                isLogin: true
            },
            component: () => import('../components/Chat.vue')
        },
        {
            path: '/regist',
            component: () => import('../components/Regist.vue')
        }
    ],
});

export default router;