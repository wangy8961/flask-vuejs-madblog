import Vue from 'vue'
import axios from 'axios'
import router from './router'
import store from './store'


// 基础配置
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = 'http://95.163.198.43:5000';
} else {
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
}
// axios.defaults.baseURL = 'http://127.0.0.1:5000'
// axios.defaults.timeout = 5000  // 超时时间（毫秒）
// axios.defaults.retry = 2  // 重试次数
// axios.defaults.retryDelay = 100  // 重试之间的间隔时间（毫秒）

// 请求拦截器
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

// 响应拦截器
// Add a response interceptor
axios.interceptors.response.use(function (response) {
  // Do something with response data
  return response
}, function (error) {
  // Do something with response error
  if (error.response) {
    // 匹配不同的响应码
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
  } else if (error.request) {
    console.log(error.request)
    Vue.toasted.error('The request has not been sent to Flask API，because OPTIONS get error', { icon: 'fingerprint' })
  } else {
    console.log('Error: ', error.message)
  }
  console.log(error.config)

  return Promise.reject(error)
})

export default axios