<template>
  <div class="container">
    <!-- Modal: Edit Post -->
    <div class="modal fade" id="updatePostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="updatePostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <form @submit.prevent="onSubmitUpdate" @reset.prevent="onResetUpdate">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editForm.titleError}">
                <input type="text" v-model="editForm.title" class="form-control" id="editform_title" placeholder="标题">
                <small class="form-control-feedback" v-show="editForm.titleError">{{ editForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editForm.summary" class="form-control" id="editform_summary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editForm.body" class="form-control" id="editform_body" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editForm.bodyError">{{ editForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>
    
          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Edit Post -->

    <div class="row">
      <!-- Articles Content -->
      <div class="col-lg-9">
        
        <article class="g-mb-60 g-pt-15 g-pb-50">
          <header class="g-mb-30">
            <h1 class="g-color-primary g-mb-15">{{ post.title }}</h1>

            <ul class="list-inline d-sm-flex g-color-gray-dark-v4 mb-0">
              <li v-if="post.author && post.author.id == sharedState.user_id" class="list-inline-item">
                <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple g-mr-5" data-toggle="modal" data-target="#updatePostModal">编辑</button>
              </li>
              <li v-if="post.author && post.author.id == sharedState.user_id" class="list-inline-item">
                <button v-on:click="onDeletePost(post)" class="btn btn-xs u-btn-outline-red g-mr-5">删除</button>
              </li>
              <li class="list-inline-item">
                <span class="btn btn-xs u-btn-outline-aqua g-mr-10">评论</span>
              </li>
              <li v-if="post.author" class="list-inline-item">
                <router-link v-bind:to="{ path: `/user/${post.author.id}` }" class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover g-text-underline--none--hover"><span v-if="post.author.name">{{ post.author.name }}</span><span v-else>{{ post.author.username }}</span></router-link>
              </li>
              <li class="list-inline-item g-mx-10">/</li>
              <li class="list-inline-item">
                <i class="icon-clock"></i> {{ $moment(post.timestamp).format('LLL') }}
              </li>
              <li class="list-inline-item g-mx-10">/</li>
              <li class="list-inline-item g-mr-10">
                <a class="u-link-v5 g-color-gray-dark-v4 g-color-primary--hover g-text-underline--none--hover" href="#comment-list-wrap">
                  <i class="icon-bubble"></i> 0
                </a>
              </li>
              <li class="list-inline-item ml-auto">
                <i class="icon-eye"></i> {{ post.views }} 次阅读
              </li>
            </ul>

            <hr class="g-brd-gray-light-v4 g-my-15">
          </header>

          <div id="postBody" class="g-font-size-16 g-line-height-1_8 g-mb-30">
            
            <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
            要指定TOC的级数哦，如果要修改TOC的样式，要在toc-rendered指定的函数中操作，因为要等它把TOC给创建出来
             -->
            <vue-markdown
              :source="post.body"
              :toc="showToc"
              :toc-first-level="1"
              :toc-last-level="3"
              v-on:toc-rendered="tocAllRight"
              toc-id="toc"
              class="markdown-body">
            </vue-markdown>
            
          </div>

        </article>
        
      </div>
      <!-- End Articles Content -->

      <!-- Sidebar -->
      <div class="col-lg-3 g-pt-80">

        <div id="sticker" class="g-mb-50">
          <div id="tocHeader" class="u-heading-v3-1 g-mb-15">
              <h2 class="h5 u-heading-v3__title g-color-primary text-uppercase g-brd-primary">文章目录</h2>
          </div>
          <div id="toc" class="toc"></div>
        </div>
        
      </div>
      <!-- End Sidebar -->
    </div>

  </div>
</template>

<script>
import store from '../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
// vue-router 从 Home 页路由到 Post 页后，会重新渲染并且会移除事件，自定义的指令 v-highlight 也不生效了
// 所以，这个页面，在 mounted() 和 updated() 方法中调用 highlightCode() 可以解决代码不高亮问题
import hljs from 'highlight.js'
const highlightCode = () => {
  let blocks = document.querySelectorAll('pre code');
  blocks.forEach((block)=>{
    hljs.highlightBlock(block)
  })
}
// 固定 TOC
import '../assets/jquery.sticky'


export default {
  name: 'Post',
  components: {
    VueMarkdown
  },
  data() {
    return {
      sharedState: store.state,
      post: {},
      editForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      showToc: true
    }
  },
  methods: {
    getPost (id) {
      const path = `/api/posts/${id}`
      this.$axios.get(path)
        .then((response) => {
          this.post = response.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    onEditPost (post) {
      // 不要使用对象引用赋值： this.editForm = post
      // 这样是同一个 post 对象，用户在 editform 中的操作会双向绑定到该 post 上， 你会看到 modal 下面的博客也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdate() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
      this.editForm = Object.assign({}, post)
    },
    onSubmitUpdate () {
      this.editForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('.form-control-feedback').remove()
      $('.form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editForm.title) {
        this.editForm.errors++
        this.editForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editform_title').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editform_title').after('<small class="form-control-feedback">' + this.editForm.titleError + '</small>')
      } else {
        this.editForm.titleError = null
      }

      if (!this.editForm.body) {
        this.editForm.errors++
        this.editForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('.md-editor').after('<small class="form-control-feedback">' + this.editForm.bodyError + '</small>')
      } else {
        this.editForm.bodyError = null
      }

      if (this.editForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#updatePostModal').modal('hide')

      const path = `/api/posts/${this.editForm.id}`
      const payload = {
        title: this.editForm.title,
        summary: this.editForm.summary,
        body: this.editForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPost(this.editForm.id)
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editForm.title = '',
          this.editForm.summary = '',
          this.editForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onResetUpdate () {
      // 先隐藏 Modal
      $('#updatePostModal').modal('hide')
      // this.getPosts()
      this.$toasted.info('Cancelled, the post is not update.', { icon: 'fingerprint' })
    },
    onDeletePost (post) {
      this.$swal({
        title: "Are you sure?",
        text: "该操作将彻底删除 [ " + post.title + " ], 请慎重",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/posts/${post.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this post', 'success')
              if (typeof this.$route.query.redirect == 'undefined') {
                this.$router.push('/')
              } else {
                this.$router.push(this.$route.query.redirect)
              }
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
            })
          
        } else {
          this.$swal('Cancelled', 'The post is safe :)', 'error')
        }
      })
    },
    tocAllRight: function (tocHtmlStr) {
      // console.log("toc is parsed :", tocHtmlStr);
      // 必须等 vue-markdown 生成 TOC 之后，再用 jquery 操作 DOM!!!
      // 非默认的列表样式
      $('.toc').find('ul').addClass('u-list-inline');
      // 2、3级目录缩进
      $('.toc ul li ul li').addClass('g-ml-15');
      $('.toc ul li ul li ul li').addClass('g-ml-15');
      // 链接颜色，鼠标悬停颜色
      $('.toc').find('a').addClass('u-link-v5 g-color-aqua g-color-red--hover')
    }
  },
  created () {
    const post_id = this.$route.params.id
    this.getPost(post_id)
    // 初始化 bootstrap-markdown 编辑器
    $(document).ready(function() {
      $("#editform_body").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
    // 使用 jquery.sticker.js 插件让 TOC 固定位置
    $(document).ready(function(){
      $("#sticker").sticky({ topSpacing: 10 });
    })
  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    this.getPost(to.params.id)
    next()
  },
  mounted () {
    highlightCode()
  },
  updated () {
    highlightCode()
  }
}
</script>
