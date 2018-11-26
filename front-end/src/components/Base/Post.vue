<template>
  <div class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20">
    <router-link v-bind:to="{ path: `/user/${post.author.id}` }" v-bind:title="post.author.name || post.author.username">
      <span v-if="post.is_new" class="d-inline-block g-pos-rel">
        <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
        <img class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="post.author.avatar" v-bind:alt="post.author.name || post.author.username">
      </span>
      <img v-else class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="post.author.avatar" v-bind:alt="post.author.name || post.author.username">
    </router-link>
    
    <div class="media-body">
      <div class="g-mb-15">
        <h5 class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${post.author.id}` }" class="g-text-underline--none--hover">{{ post.author.name || post.author.username }}</router-link> <span class="h6">发布了文章<router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id } }" class="g-text-underline--none--hover">《{{ post.title }}》</router-link></span></h5>
        <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(post.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
      </div>

      <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
      v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
      <vue-markdown
        :source="post.summary"
        class="markdown-body g-mb-15"
        v-highlight>
      </vue-markdown>

      <div class="d-flex justify-content-start">
        <ul class="list-inline mb-0">
          <li class="list-inline-item g-mr-20">
            <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
              <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.views }}
            </a>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/post/${post.id}#like-post` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ post.likers_count }}
            </router-link>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/post/${post.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ post.comments_count }}
            </router-link>
          </li>
        </ul>
        <ul class="list-inline mb-0 ml-auto">
          <li class="list-inline-item g-mr-5">
            <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id } }" class="btn btn-xs u-btn-outline-primary">阅读全文</router-link>
          </li>
          <li v-if="post.author.id == sharedState.user_id" class="list-inline-item g-mr-5">
            <button v-on:click="$emit('edit-post')" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editPostModal">编辑</button>
          </li>
          <li v-if="post.author.id == sharedState.user_id" class="list-inline-item">
            <button v-on:click="$emit('delete-post')" class="btn btn-xs u-btn-outline-red">删除</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'

export default {
  props: ['post'],
  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state
    }
  },
  /*
  computed: {
    leftBrdColor: function () {
      const colors = ['primary', 'blue', 'red', 'purple', 'orange', 'yellow', 'aqua', 'cyan', 'teal', 'brown', 'pink', 'black']
      let index = Math.floor((Math.random() * colors.length))
      return 'g-brd-' + colors[index] + '-left'
    }
  }
  */
}
</script>