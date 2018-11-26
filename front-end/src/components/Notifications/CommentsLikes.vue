<template>
  <div>
    <!-- 收到的喜欢或赞列表 -->
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> Recived Comments Likes <small v-if="likes">(共 {{ likes._meta.total_items }} 条, {{ likes._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 条
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 条
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 条
            </router-link>
            
            <div class="dropdown-divider"></div>
            
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 条
            </router-link>
            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="likes" class="card-block g-pa-0" >
        
        <div class="media g-brd-around g-brd-gray-light-v4 g-pa-30 g-mb-20"
          v-for="(like, index) in likes.items" v-bind:key="index">
          <router-link v-bind:to="{ path: `/user/${like.user.id}` }">  
            <span v-if="like.is_new" class="d-inline-block g-pos-rel">
              <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
              <img class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded rounded-circle mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="like.user._links.avatar" v-bind:alt="like.user.name || like.user.username">
            </span>
            <img v-else class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded rounded-circle mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="like.user._links.avatar" v-bind:alt="like.user.name || like.user.username">
          </router-link>
          <div class="media-body">
            <div class="g-mb-15">
              <h5 class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${like.user.id}` }" class="comment-author g-text-underline--none--hover">{{ like.user.name || like.user.username }}</router-link> <span class="h6">点赞了你的 <router-link v-bind:to="{ path: `/post/${like.comment.post.id}#c${like.comment.id}` }" class="g-text-underline--none--hover"> 评论 </router-link></span></h5>
              <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(like.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
            </div>

            <div v-if="like.comment.disabled" class="g-color-red g-mb-15">此评论包含不良信息，已被禁止显示.</div>
            <div v-else>
              <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
              v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
              <vue-markdown
                :source="like.comment.body"
                class="markdown-body g-mb-15"
                v-highlight>
              </vue-markdown>
            </div>

            <ul class="list-inline d-sm-flex my-0">
              <li v-if="!like.comment.disabled" class="list-inline-item g-mr-20">
                <span class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover">
                  <i v-bind:class="{ 'g-color-red': like.comment.likers_id.indexOf(sharedState.user_id) != -1 }" class="icon-like g-pos-rel g-top-1 g-mr-3"></i>
                  <span> {{ like.comment.likers_id.length }} 人赞</span>
                </span>
              </li>
              <li class="list-inline-item g-mr-20">
                <router-link v-bind:to="{ path: `/post/${like.comment.post.id}#c${like.comment.id}` }" class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover" href="javascript:;">
                  <i class="icon-action-redo g-pos-rel g-top-1 g-mr-3"></i>
                  查看对话
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      
      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="likes">
      <pagination
        v-bind:cur-page="likes._meta.page"
        v-bind:per-page="likes._meta.per_page"
        v-bind:total-pages="likes._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
import Pagination from '../Base/Pagination'

export default {
  name: 'Likes',  // this is the name of the component
  components: {
    VueMarkdown,
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      likes: ''
    }
  },
  methods: {
    getUserRecivedCommentsLikes (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/recived-comments-likes/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.likes = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    this.getUserRecivedCommentsLikes(this.sharedState.user_id)
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUserRecivedCommentsLikes(this.sharedState.user_id)
  }
}
</script>