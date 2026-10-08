import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App)

import router from "./router"
app.use(router)

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
app.use(ElementPlus)

import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:8000/'
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.put['Content-Type'] = 'application/json'
app.config.globalProperties.$axios = axios

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

import {marked} from 'marked'
import DOMPurify from 'dompurify'

marked.setOptions({
  breaks: true,
  gfm: true,
  smartLists: true,
  smartypants: false
})

function normalizeMarkdowm(text){
  return text
    .replace(/(#{1,6} )/g, '\n$1')
    .replace(/- /g, '\n- ')
}

function renderMarkdown(text){
  if (!text) return ''
  const rawHtml = marked.parse(normalizeMarkdowm(text))
  return DOMPurify.sanitize(rawHtml)
}
app.config.globalProperties.$renderMarkdown = renderMarkdown

router.beforeEach((to,from,next) => {
  if (to.meta.isLogin){
    let token = localStorage.getItem("token");
    if (token){
      next();
    }else{
      next("/login")
    }
  }else{
    next();
  }
})

app.mount('#app')