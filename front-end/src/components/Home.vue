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

    <form v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAdd" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
        <input type="text" v-model="postForm.title" class="form-control" id="post_title" placeholder="标题">
        <small class="form-control-feedback" v-show="postForm.titleError">{{ postForm.titleError }}</small>
      </div>
      <div class="form-group">
        <input type="text" v-model="postForm.summary" class="form-control" id="post_summary" placeholder="摘要">
      </div>
      <div class="form-group">
        <textarea v-model="postForm.body" class="form-control" id="post_body" rows="5" placeholder=" 内容"></textarea>
        <small class="form-control-feedback" v-show="postForm.bodyError">{{ postForm.bodyError }}</small>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Posts <small v-if="posts">(共 {{ posts._meta.total_items }} 篇, {{ posts._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>
            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="posts" class="card-block g-pa-0" >
        <div v-for="(post, index) in posts.items" v-bind:key="index" class="media g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-20">
          <router-link v-bind:to="{ name: 'Profile', params: { id: post.author.id }}" v-bind:title="post.author.name || post.author.username">
            <img class="d-flex g-width-50 g-height-50 g-mt-3 g-mr-20" v-bind:src="post.author._links.avatar" v-bind:alt="post.author.name || post.author.username">
          </router-link>
          
          <div class="media-body">
            <div class="d-sm-flex justify-content-sm-between align-items-sm-center g-mb-15 g-mb-10--sm">
              <h5 class="h4 g-font-weight-300 g-mr-10 g-mb-5 g-mb-0--sm">
                <router-link v-bind:to="{ name: 'Post', params: { id: post.id }}" class="g-text-underline--none--hover">{{ post.title }}</router-link>
              </h5>
              <div class="text-nowrap g-font-size-12">
                <span>{{ $moment(post.timestamp).fromNow() }}</span> / <router-link v-bind:to="{ name: 'Profile', params: { id: post.author.id }}"><span v-if="post.author.name">{{ post.author.name }}</span><span v-else>{{ post.author.username }}</span></router-link>
              </div>
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
                  <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="page-profile-comments-1.html#">
                    <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.views }}
                  </a>
                </li>
              </ul>
              <ul class="list-inline mb-0 ml-auto">
                <li class="list-inline-item g-mr-5">
                  <router-link v-bind:to="{ name: 'Post', params: { id: post.id }}" class="btn btn-xs u-btn-outline-primary">阅读全文</router-link>
                </li>
                <li v-if="post.author.id == sharedState.user_id" class="list-inline-item g-mr-5">
                  <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#updatePostModal">编辑</button>
                </li>
                <li v-if="post.author.id == sharedState.user_id" class="list-inline-item">
                  <button v-on:click="onDeletePost(post)" class="btn btn-xs u-btn-outline-red">删除</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- End Panel Body -->
    </div>

    <!-- Pagination #04 -->
    <nav v-if="posts" aria-label="Page Navigation" class="g-mb-50">
      <ul class="list-inline">
        <li class="list-inline-item">
          <router-link v-bind:to="{ name: 'Home', query: { page: posts._meta.page - 1, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1__item--disabled': posts._meta.page == 1}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Previous">
            <span aria-hidden="true">
              <i class="fa fa-angle-left"></i>
            </span>
            <span class="sr-only">Previous</span>
          </router-link>
        </li>

        <li v-if="page != 'NaN'" v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item g-hidden-sm-down">
          <router-link v-bind:to="{ name: 'Home', query: { page: page, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1-1--active': $route.query.page == page || (!$route.query.page && page == 1)}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-19">{{ page }}</router-link>
        </li>
        <li v-else class="list-inline-item g-hidden-sm-down">
          <span class="g-pa-12-19">...</span>
        </li>
        
        <li class="list-inline-item">
          <router-link v-bind:to="{ name: 'Home', query: { page: posts._meta.page + 1, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1__item--disabled': posts._meta.page == posts._meta.total_pages }" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Next">
            <span aria-hidden="true">
              <i class="fa fa-angle-right"></i>
            </span>
            <span class="sr-only">Next</span>
          </router-link>
        </li>
        <li class="list-inline-item float-right">
          <span class="u-pagination-v1__item-info g-pa-12-19">Page {{ posts._meta.page }} of {{ posts._meta.total_pages }}</span>
        </li>
      </ul>
    </nav>
    <!-- End Pagination #04 -->

  </div>
</template>

<script>
import store from '../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'Home',  //this is the name of the component
  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state,
      posts: '',
      iter_pages: [],  // 分页导航栏
      postForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      editForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      }
    }
  },
  methods: {
    getPosts () {
      let page = 1
      let per_page = 3
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/posts?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
          // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
          let arr = [1, 2, this.posts._meta.page-2, this.posts._meta.page-1, this.posts._meta.page, this.posts._meta.page+1, this.posts._meta.page+2, this.posts._meta.total_pages-1, this.posts._meta.total_pages]
          // 小于1，或大于最大页数的都是非法的，要去除
          arr = arr.filter(item => item > 0 && item <= this.posts._meta.total_pages)
          // 去除重复项
          this.iter_pages = [...new Set(arr)]
          // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
          if (this.posts._meta.page + 2 < this.posts._meta.total_pages - 2) {
            this.iter_pages.splice(-2, 0, 'NaN')
          }
          // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
          if (this.posts._meta.page - 3 > 2) {
            this.iter_pages.splice(2, 0, 'NaN')
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    onSubmitAdd (e) {
      this.postForm.errors = 0  // 重置

      if (!this.postForm.title) {
        this.postForm.errors++
        this.postForm.titleError = 'Title is required.'
      } else {
        this.postForm.titleError = null
      }

      if (!this.postForm.body) {
        this.postForm.errors++
        this.postForm.bodyError = 'Body is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.postForm.bodyError = null
      }

      if (this.postForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/posts'
      const payload = {
        title: this.postForm.title,
        summary: this.postForm.summary,
        body: this.postForm.body
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getPosts()
          this.$toasted.success('Successed add a new post.', { icon: 'fingerprint' })
          this.postForm.title = '',
          this.postForm.summary = '',
          this.postForm.body = ''
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
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
          this.getPosts()
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
              // this.$toasted.success('Successed delete the post.', { icon: 'fingerprint' })
              this.getPosts()
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
            })
        } else {
          this.$swal('Cancelled', 'The post is safe :)', 'error')
        }
      })
    }
  },
  created () {
    this.getPosts()
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#post_body, #editform_body").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当查询参数 page 或 per_page 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    // 注意：要先执行 next() 不然 this.$route.query 还是之前的
    next()
    this.getPosts()
  }
}
</script>