<template>
  <div class="container">
    <!-- Modal: Edit Post -->
    <div class="modal fade" id="editPostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editPostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <form id="editPostForm" @submit.prevent="onSubmitUpdatePost" @reset.prevent="onResetUpdatePost">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editPostForm.titleError}">
                <input type="text" v-model="editPostForm.title" class="form-control" id="editPostFormTitle" placeholder="标题">
                <small class="form-control-feedback" v-show="editPostForm.titleError">{{ editPostForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editPostForm.summary" class="form-control" id="editPostFormSummary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editPostForm.body" class="form-control" id="editPostFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editPostForm.bodyError">{{ editPostForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>
    
          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Edit Post -->

    <!-- Modal: Edit Comment -->
    <div class="modal fade" id="editCommentModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editCommentModalTitle">Update Comment</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          
            <form id="editCommentForm" @submit.prevent="onSubmitUpdateComment" @reset.prevent="onResetUpdateComment">
              <div class="form-group">
                <textarea v-model="editCommentForm.body" class="form-control" id="editCommentFormBody" rows="5" placeholder=" 评论内容"></textarea>
                <small class="form-control-feedback" v-show="editCommentForm.bodyError">{{ editCommentForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>
    
          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Edit Comment -->

    <div class="row">
      <!-- Articles Content -->
      <div class="col-lg-9">
        
        <article class="g-mb-30 g-pt-15 g-pb-15">
          <header class="g-mb-30">
            <h1 class="g-color-primary g-mb-15">{{ post.title }}</h1>

            <ul class="list-inline d-sm-flex g-color-gray-dark-v4 mb-0">
              <li v-if="post.author && post.author.id == sharedState.user_id" class="list-inline-item">
                <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple g-mr-5" data-toggle="modal" data-target="#editPostModal">编辑</button>
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

        <!-- Pre / Next -->
        <div class="g-mb-60">
          <ul class="list-inline d-sm-flex mb-0">
            <li v-bind:class="{'u-pagination-v1__item--disabled': !post.prev_id}" class="list-inline-item g-hidden-xs-down" data-toggle="tooltip" data-placement="top" title="" v-bind:data-original-title="post.prev_title || ''">
              <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.prev_id || 0 } }" class="u-pagination-v1__item u-pagination-v1-4 g-brd-gray-light-v3 g-brd-primary--hover g-rounded-50 g-pa-7-16" href="#" aria-label="Previous">
                <span aria-hidden="true">
                  <i class="fa fa-angle-left g-mr-5"></i> 上一篇
                </span>
                <span class="sr-only">上一篇</span>
              </router-link>
            </li>

            <li v-bind:class="{'u-pagination-v1__item--disabled': !post.next_id}" class="list-inline-item ml-auto g-hidden-xs-down" data-toggle="tooltip" data-placement="top" title="" v-bind:data-original-title="post.next_title || ''">
              <router-link router-link v-bind:to="{ name: 'PostDetail', params: { id: post.next_id || 0 } }" class="u-pagination-v1__item u-pagination-v1-4 g-brd-gray-light-v3 g-brd-primary--hover g-rounded-50 g-pa-7-16" href="#" aria-label="Next">
                <span aria-hidden="true">
                  下一篇 <i class="fa fa-angle-right g-ml-5"></i>
                </span>
                <span class="sr-only">下一篇</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- 博客文章的评论列表 -->
        <div class="card border-0 g-mb-15">
          <!-- Panel Header -->
          <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
            <h3 class="h6 mb-0">
              <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> Comments
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

          <!-- Add Comment Form -->
          <form id="addCommentForm" v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAddComment" class="g-mb-40">
            <div class="form-group">
              <textarea v-model="commentForm.body" class="form-control" id="commentFormBody" rows="5" placeholder=" 评论内容"></textarea>
              <small class="form-control-feedback" v-show="commentForm.bodyError">{{ commentForm.bodyError }}</small>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
          <!-- End Add Comment Form -->

          <div v-else class="btn-group g-mr-10 g-mb-15">
            <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              请先登录
            </button>
            <div class="dropdown-menu" x-placement="bottom-start" style="position: absolute; transform: translate3d(0px, 35px, 0px); top: 0px; left: 0px; will-change: transform;">
              <a class="dropdown-item" href="javascript:;">Github</a>
              <a class="dropdown-item" href="javascript:;">Facebook</a>
              <a class="dropdown-item" href="javascript:;">微信</a>
              <div class="dropdown-divider"></div>
              <router-link v-bind:to="{ path: '/login', query: { redirect: $route.fullPath } }" class="dropdown-item">站内账号</router-link>
            </div>
          </div>

          <!-- Panel Body -->
          <div v-if="comments" class="card-block g-pa-0" >
            <comment v-for="(comment, index) in comments.items" v-bind:key="index"
              v-bind:comment="comment"
              v-on:edit-comment="onEditComment(comment)"
              v-on:delete-comment="onDeleteComment(comment)">
            </comment>
          </div>
          <!-- End Panel Body -->
        </div>
      
        <!-- Pagination #04 -->
        <div v-if="comments">
          <pagination
            v-bind:cur-page="comments._meta.page"
            v-bind:per-page="comments._meta.per_page"
            v-bind:total-pages="comments._meta.total_pages">
          </pagination>
        </div>
        <!-- End Pagination #04 -->

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
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
// 评论子组件和分页子组件
import Comment from '../Base/Comment'
import Pagination from '../Base/Pagination'
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
import '../../assets/jquery.sticky'


export default {
  name: 'Post',
  components: {
    VueMarkdown,
    Comment,
    Pagination
  },
  data() {
    return {
      sharedState: store.state,
      post: '',
      comments: '',
      showToc: true,
      editPostForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      commentForm: {
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        bodyError: null
      },
      editCommentForm: {
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        bodyError: null
      }
    }
  },
  methods: {
    getPost (id) {
      const path = `/api/posts/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.post = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onEditPost (post) {
      // 不要使用对象引用赋值： this.editPostForm = post
      // 这样是同一个 post 对象，用户在 editPostForm 中的操作会双向绑定到该 post 上， 你会看到 modal 下面的博客也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdatePost() 中重新加载一次博客列表，不然用户会看到修改后但未提交的不对称信息
      this.editPostForm = Object.assign({}, post)
    },
    onSubmitUpdatePost () {
      this.editPostForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editPostForm.title) {
        this.editPostForm.errors++
        this.editPostForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
      } else {
        this.editPostForm.titleError = null
      }

      if (!this.editPostForm.body) {
        this.editPostForm.errors++
        this.editPostForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
      } else {
        this.editPostForm.bodyError = null
      }

      if (this.editPostForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#editPostModal').modal('hide')

      const path = `/api/posts/${this.editPostForm.id}`
      const payload = {
        title: this.editPostForm.title,
        summary: this.editPostForm.summary,
        body: this.editPostForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPost(this.editPostForm.id)
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editPostForm.title = '',
          this.editPostForm.summary = '',
          this.editPostForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onResetUpdatePost () {
      // 先移除错误
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editPostModal').modal('hide')
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
    getPostComments (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/posts/${id}/comments/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          if (response.data._meta.total_items > 0) {
            this.comments = response.data
          }
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onSubmitAddComment (e) {
      this.commentForm.errors = 0  // 重置

      if (!this.commentForm.body) {
        this.commentForm.errors++
        this.commentForm.bodyError = 'Body is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#addCommentForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.commentForm.bodyError = null
        $('#addCommentForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.commentForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/comments/'
      const payload = {
        post_id: this.$route.params.id,
        body: this.commentForm.body
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getPostComments(this.$route.params.id)
          this.$toasted.success('Successed add a new comment.', { icon: 'fingerprint' })
          this.commentForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onEditComment (comment) {
      // 不要使用对象引用赋值： this.editCommentForm = comment
      // 这样是同一个 comment 对象，用户在 editCommentForm 中的操作会双向绑定到该 comment 上， 你会看到 modal 下面的评论也在变
      // 如果用户修改了一些数据，但是点了 cancel，你就必须在 onResetUpdateComment() 中重新加载一次评论列表，不然用户会看到修改后但未提交的不对称信息
      this.editCommentForm = Object.assign({}, comment)
    },
    onSubmitUpdateComment () {
      this.editCommentForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editCommentForm .form-control-feedback').remove()
      $('#editCommentForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editCommentForm.body) {
        this.editCommentForm.errors++
        this.editCommentForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#editCommentForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editCommentForm .md-editor').after('<small class="form-control-feedback">' + this.editCommentForm.bodyError + '</small>')
      } else {
        this.editCommentForm.bodyError = null
      }

      if (this.editCommentForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      // 先隐藏 Modal
      $('#editCommentModal').modal('hide')

      const path = `/api/comments/${this.editCommentForm.id}`
      const payload = {
        body: this.editCommentForm.body
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.getPostComments(this.$route.params.id)
          this.$toasted.success('Successed update the comment.', { icon: 'fingerprint' })
          this.editCommentForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onResetUpdateComment () {
      // 先移除错误
      $('#editCommentForm .form-control-feedback').remove()
      $('#editCommentForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editCommentModal').modal('hide')
      this.$toasted.info('Cancelled, the comment is not update.', { icon: 'fingerprint' })
    },
    onDeleteComment (comment) {
      this.$swal({
        title: "Are you sure?",
        text: "该操作将彻底删除这条评论, 请慎重",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/comments/${comment.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this comment', 'success')
              this.getPostComments(this.$route.params.id)
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
            })
        } else {
          this.$swal('Cancelled', 'The comment is safe :)', 'error')
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
    this.getPostComments(post_id)
    // 初始化 bootstrap-markdown 编辑器
    $(document).ready(function() {
      $("#editPostFormBody, #commentFormBody, #editCommentFormBody").markdown({
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
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
    })
  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getPost(to.params.id)
    this.getPostComments(to.params.id)
  },
  mounted () {
    highlightCode()
  },
  updated () {
    highlightCode()
  }
}
</script>
