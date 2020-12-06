import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from "@/views/Home";
import Login from "@/views/Login";

Vue.use(VueRouter)

const routes = [
    {path: "/", redirect: "/home"},
    {path: "/home", component: Home},
    {path: "/login", component: Login},
]

const router = new VueRouter({
    routes
})

export default router
