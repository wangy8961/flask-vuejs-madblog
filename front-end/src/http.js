import Vue from 'vue'
import axios from 'axios'
import router from './router'
import store from './store'


// 基础配置
axios.defaults.timeout = 5000  // 超时时间
axios.defaults.baseURL = 'http://localhost:5000'

// Add a request interceptor
axios.interceptors.request.use(function (config) {
  // Do something before request is sent
  const token = window.localStorage.getItem('madblog-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, function (error) {
  // Do something with request error
  return Promise.reject(error)
})

// Add a response interceptor
axios.interceptors.response.use(function (response) {
  // Do something with response data
  return response
}, function (error) {
  // Do something with response error
  switch  (error.response.status) {
    case 401:
      // 清除 Token 及 已认证 等状态
      store.logoutAction()
      // 跳转到登录页
      if (router.currentRoute.path !== '/login') {
        Vue.toasted.error('401: 认证已失效，请先登录', { icon: 'fingerprint' })
        router.replace({
          path: '/login',
          query: { redirect: router.currentRoute.path },
        })
      }
      break

    case 403:
      Vue.toasted.error('403: Forbidden', { icon: 'fingerprint' })
      router.back()
      break

    case 404:
      Vue.toasted.error('404: Not Found', { icon: 'fingerprint' })
      router.back()
      break
    
    case 500:  // 根本拿不到 500 错误，因为 CORs 不会过来
      Vue.toasted.error('500: Oops... INTERNAL SERVER ERROR', { icon: 'fingerprint' })
      router.back()
      break
  }
  return Promise.reject(error)
})

export default axios