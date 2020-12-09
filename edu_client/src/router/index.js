import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from "@/views/Home";
// import Login from "@/views/Login";
import Register from "../views/Register";
import Home from "../views/Home";
import Login from "../views/login";
import Course from "../views/Course";
import CourseDetail from "../views/CourseDetail";
Vue.use(VueRouter)


const routes = [
    {path: "/", redirect: "/home"},
    {path: "/home", component: Home},
    {path: "/login", component: Login},
    {path: "/register", component: Register},
    {path: "/course", component: Course},
    {path: "/detail/:id", component: CourseDetail},
]

const router = new VueRouter({
    routes
})

export default router
