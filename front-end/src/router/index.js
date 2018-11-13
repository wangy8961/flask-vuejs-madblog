import Vue from 'vue'
import Router from 'vue-router'
// 首页
import Home from '@/components/Home'
// 用户认证：注册与登录
import Register from '@/components/User/Auth/Register'
import Login from '@/components/User/Auth/Login'
// 用户个人主页
import User from '@/components/User/User'
import Overview from '@/components/User/Overview'
import Followers from '@/components/User/Followers'
import Following from '@/components/User/Following'
import UserPostsList from '@/components/Post/UserPostsList'
import UserFollowedsPostsList from '@/components/Post/UserFollowedsPostsList'
// 用户个人设置
import Settings from '@/components/User/Settings/Settings'
import Profile from '@/components/User/Settings/Profile'
import Account from '@/components/User/Settings/Account'
import Email from '@/components/User/Settings/Email'
import Notification from '@/components/User/Settings/Notification'
// 博客详情页
import PostDetail from '@/components/PostDetail'
// 测试与后端连通性
import Ping from '@/components/Ping'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      // 博客文章详情页
      path: '/post/:id',
      name: 'PostDetail',
      component: PostDetail
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user/:id',
      // name: 'User',
      component: User,
      children: [
        // Overview will be rendered inside User's <router-view>
        // when /user/:id is matched
        // 注意： 要有默认子路由，父路由不能指定 name
        { path: '', component: Overview },
        { path: 'overview', name: 'UserOverview', component: Overview },
				
        // Followers will be rendered inside User's <router-view>
        // when /user/:id/followers is matched
        { path: 'followers', name: 'UserFollowers', component: Followers },

        // Following will be rendered inside User's <router-view>
        // when /user/:id/following is matched
        { path: 'following', name: 'UserFollowing', component: Following },

        // UserPostsList will be rendered inside User's <router-view>
        // when /user/:id/posts is matched
        { path: 'posts', name: 'UserPostsList', component: UserPostsList },

        // UserFollowedsPostsList will be rendered inside User's <router-view>
        // when /user/:id/followeds-posts is matched
        { path: 'followeds-posts', name: 'UserFollowedsPostsList', component: UserFollowedsPostsList }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      // 用户修改自己的个人信息
      path: '/settings',
      component: Settings,
      children: [
        { path: '', component: Profile },
        { path: 'profile', name: 'SettingProfile', component: Profile },
        { path: 'account', name: 'SettingAccount', component: Account },
        { path: 'email', name: 'SettingEmail', component: Email },
        { path: 'notification', name: 'SettingNotification', component: Notification }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('madblog-token')
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    Vue.toasted.show('Please log in to access this page.', { icon: 'fingerprint' })
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name == 'Login') {
    // 用户已登录，但又去访问登录页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {  // 要前往的路由不存在时
    Vue.toasted.error('404: Not Found', { icon: 'fingerprint' })
    if (from.name) {
      next({
        name: from.name
      })
    } else {
      next({
        path: '/'
      })
    }
  } else {
    next()
  }
})

export default router