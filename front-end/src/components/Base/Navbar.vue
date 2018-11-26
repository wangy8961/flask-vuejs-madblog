<template>
<section>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
      <div class="navbar-brand">
      <router-link to="/" class="g-text-underline--none--hover">
        <img src="../../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
          Design by 
      </router-link>
      <a href="http://www.madmalls.com" class="g-text-underline--none--hover">Madman</a>
      </div>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link to="/" class="nav-link">Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ping" class="nav-link">Ping</router-link>
          </li>
        </ul>
        
        <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto">
          <input class="form-control mr-sm-2" type="search" placeholder="Search">
          <!-- 暂时先禁止提交，后续实现搜索再改回 type="submit" -->
          <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
        </form>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
          <li class="nav-item g-mr-20">
            <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link"><i class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"></i> Notifications <span id="new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">0</span></router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <img v-bind:src="sharedState.user_avatar" class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded"> {{ sharedState.user_name }}
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }" class="dropdown-item"><i class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile</router-link>
              <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item"><i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource</router-link>
              <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item"><i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings</router-link>
              <div class="dropdown-divider"></div>
              <a v-on:click="handlerLogout" class="dropdown-item" href="#"><i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out</a>
            </div>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav navbar-right">          
          <li class="nav-item">
            <router-link to="/login" class="nav-link"><i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</section>
</template>

<script>
import store from '../../store'
// 在 JQuery 中使用 axios 的话需要重新导入，不能使用 main.js 中定义的 Vue 全局属性 this.$axios
import axios from 'axios'

export default {
  name: 'Navbar',  //this is the name of the component
  data () {
    return {
      sharedState: store.state
    }
  },
  methods: {
    handlerLogout (e) {
      store.logoutAction()
      this.$toasted.show('You have been logged out.', { icon: 'fingerprint' })
      this.$router.push('/login')
    }
  },
  mounted () {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    $(function() {
      let since = 0
      let total_notifications_count = 0  // 总通知计数
      let unread_recived_comments_count = 0  // 收到的新评论通知计数
      let unread_messages_count = 0  // 收到的新私信通知计数
      let unread_follows_count = 0  // 新粉丝通知计数
      let unread_posts_likes_count = 0  // 新收藏文章的通知计数
      let unread_comments_likes_count = 0  // 新的评论点赞的通知计数
      let unread_followeds_posts_count = 0  // 用户关注的人的新文章通知计数
      
      setInterval(function() {
        if (window.localStorage.getItem('madblog-token')) {
          // 如果用户已登录，才开始请求 API
          const payload = JSON.parse(atob(window.localStorage.getItem('madblog-token').split('.')[1]))
          const user_id = payload.user_id
          const path = `/api/users/${user_id}/notifications/?since=${since}`
          axios.get(path)
            .then((response) => {
              // handle success
              for(var i = 0; i < response.data.length; i++) {
                switch (response.data[i].name) {
                  case 'unread_recived_comments_count':
                    unread_recived_comments_count = response.data[i].payload
                    break
                  
                  case 'unread_messages_count':
                    unread_messages_count = response.data[i].payload
                    break
                  
                  case 'unread_follows_count':
                    unread_follows_count = response.data[i].payload
                    break
                  
                  case 'unread_posts_likes_count':
                    unread_posts_likes_count = response.data[i].payload
                    break
                  
                  case 'unread_comments_likes_count':
                    unread_comments_likes_count = response.data[i].payload
                    break

                  case 'unread_followeds_posts_count':
                    unread_followeds_posts_count = response.data[i].payload
                    break
                }
                since = response.data[i].timestamp
              }

              total_notifications_count = unread_recived_comments_count + unread_messages_count + unread_follows_count + unread_posts_likes_count + unread_comments_likes_count + unread_followeds_posts_count
              // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
              $('#new_notifications_count').text(total_notifications_count)
              $('#new_notifications_count').css('visibility', total_notifications_count ? 'visible' : 'hidden');
            })
            .catch((error) => {
              // handle error
              console.error(error)
            })
        }
      }, 10000)
    })
  }
}
</script>