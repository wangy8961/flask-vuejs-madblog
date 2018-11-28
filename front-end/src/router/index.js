import Vue from 'vue'
import Router from 'vue-router'
// 导入 vue-scrollto，跳转到锚点时支持平滑过渡
import VueScrollTo from 'vue-scrollto'
// 首页
import Home from '@/components/Home'
// 用户认证：注册、登录、验证账户、重置密码请求、重置密码
import Register from '@/components/Auth/Register'
import Login from '@/components/Auth/Login'
import Unconfirmed from '@/components/Auth/Unconfirmed'
import ResetPasswordRequest from '@/components/Auth/ResetPasswordRequest'
import ResetPassword from '@/components/Auth/ResetPassword'
// 用户个人主页
import User from '@/components/Profile/User'
import Overview from '@/components/Profile/Overview'
import Followers from '@/components/Profile/Followers'
import Following from '@/components/Profile/Following'
import Posts from '@/components/Profile/Posts'
// 用户个人设置
import Settings from '@/components/Settings/Settings'
import Profile from '@/components/Settings/Profile'
import Account from '@/components/Settings/Account'
import Email from '@/components/Settings/Email'
import Notification from '@/components/Settings/Notification'
// 用户资源
import Resource from '@/components/Resources/Resource'
import LikedPostsResource from '@/components/Resources/LikedPosts'
import CommentsResource from '@/components/Resources/CommentsResource'
import MessagesIndexResource from '@/components/Resources/Messages/Index'
import SentMessagesResource from '@/components/Resources/Messages/List'
import MessagesHistoryResource from '@/components/Resources/Messages/History'
// 用户通知
import Notifications from '@/components/Notifications/Notifications'
import RecivedComments from '@/components/Notifications/RecivedComments'
import MessagesIndex from '@/components/Notifications/Messages/Index'
import RecivedMessages from '@/components/Notifications/Messages/List'
import MessagesHistory from '@/components/Notifications/Messages/History'
import PostsLikes from '@/components/Notifications/PostsLikes'
import CommentsLikes from '@/components/Notifications/CommentsLikes'
import FollowingPosts from '@/components/Notifications/FollowingPosts'
// 博客详情页
import PostDetail from '@/components/PostDetail'
// 测试与后端连通性
import Ping from '@/components/Ping'


Vue.use(Router)

// scrollBehavior:
// - only available in html5 history mode
// - defaults to no scroll behavior
// - return false to prevent scroll
const scrollBehavior = (to, from, savedPosition) => {
  if (savedPosition) {
    // savedPosition is only available for popstate navigations.
    return savedPosition
  } else {
    const position = {}
    // new navigation.
    // scroll to anchor by returning the selector
    if (to.hash) {
      // 重要: 延迟1秒等待 DOM 生成，不然跳转到对应的锚点时会提示找不到 DOM
      setTimeout(() => {
        VueScrollTo.scrollTo(to.hash, 200)
      }, 1000)
      position.selector = to.hash
    }
    // check if any matched route config has meta that requires scrolling to top
    if (to.matched.some(m => m.meta.scrollToTop)) {
      // cords will be used if no selector is provided,
      // or if the selector didn't match any element.
      position.x = 0
      position.y = 0
    }
    // if the returned position is falsy or an empty object,
    // will retain current scroll position.
    return position
  }
}

const router = new Router({
  // mode: 'history',  // 文章详情页 TOC 的锚点以数字开头，会被报错不合法: [Vue warn]: Error in nextTick: "SyntaxError: Failed to execute 'querySelector' on 'Document': '#13-git-clone' is not a valid selector."
  scrollBehavior,  // 不用这个，在需要跳转的改用 vue-scrollto
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
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
      path: '/unconfirmed',
      name: 'Unconfirmed',
      component: Unconfirmed,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/reset-password-request',
      name: 'ResetPasswordRequest',
      component: ResetPasswordRequest
    },
    {
      path: '/reset-password',
      name: 'ResetPassword',
      component: ResetPassword
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

        // UserPosts will be rendered inside User's <router-view>
        // when /user/:id/posts is matched
        { path: 'posts', name: 'UserPosts', component: Posts }
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
      // 用户的资源
      path: '/resource',
      component: Resource,
      children: [
        { path: '', component: Posts },
        { path: 'posts', name: 'PostsResource', component: Posts },
        { path: 'liked-posts', name: 'LikedPostsResource', component: LikedPostsResource },
        { path: 'comments', name: 'CommentsResource', component: CommentsResource },
        { 
          path: 'messages', 
          component: MessagesIndexResource,
          children: [
            // 默认匹配，你给哪些人发送过私信
            { path: '', name: 'MessagesIndexResource', component: SentMessagesResource },
            // 与某个用户之间的全部历史对话记录
            { path: 'history', name: 'MessagesHistoryResource', component: MessagesHistoryResource }
          ]
        }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      // 用户通知
      path: '/notifications',
      component: Notifications,
      children: [
        { path: '', component: RecivedComments },
        { path: 'comments', name: 'RecivedComments', component: RecivedComments },
        { 
          path: 'messages', 
          component: MessagesIndex,
          children: [
            // 默认匹配，哪些人给你发送过私信
            { path: '', name: 'MessagesIndex', component: RecivedMessages },
            // 与某个用户之间的全部历史对话记录
            { path: 'history', name: 'MessagesHistory', component: MessagesHistory }
          ]
        },
        { path: 'follows', name: 'Follows', component: Followers },
        { path: 'posts-likes', name: 'PostsLikes', component: PostsLikes },
        { path: 'comments-likes', name: 'CommentsLikes', component: CommentsLikes },
        { path: 'following-posts', name: 'FollowingPosts', component: FollowingPosts }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      // 博客文章详情页
      path: '/post/:id',
      name: 'PostDetail',
      component: PostDetail
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
  if (token) {
    var payload = JSON.parse(atob(token.split('.')[1]))
  }
  
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    // 1. 用户未登录，但想访问需要认证的相关路由时，跳转到 登录 页
    Vue.toasted.show('Please log in to access this page.', { icon: 'fingerprint' })
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && !payload.confirmed && to.name != 'Unconfirmed') {
    // 2. 用户刚注册，但是还没确认邮箱地址时，全部跳转到 认证提示 页面
    Vue.toasted.show('Please confirm your accout to access this page.', { icon: 'fingerprint' })
    next({
      path: '/unconfirmed',
      query: { redirect: to.fullPath }
    })
  } else if (token && payload.confirmed && to.name == 'Unconfirmed') {
    // 3. 用户账户已确认，但又去访问 认证提示 页面时不让他过去
    next({
      path: '/'
    })
  } else if (token && (to.name == 'Login' || to.name == 'Register' || to.name == 'ResetPasswordRequest' || to.name == 'ResetPassword')) {
    // 4. 用户已登录，但又去访问 登录/注册/请求重置密码/重置密码 页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {
    // 5. 要前往的路由不存在时
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
    // 6. 正常路由出口
    next()
  }
})

export default router