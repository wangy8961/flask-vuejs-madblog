<template>
  <div>
    <!-- 用户收到的私信列表 -->
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> Received Messages <small v-if="messages">(共 {{ messages._meta.total_items }} 条, {{ messages._meta.total_pages }} 页)</small>
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
      <div class="d-flex justify-content-start g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-10"
        v-for="(message, index) in messages.items" v-bind:key="index">
        <div class="g-mt-2">
          <router-link v-bind:to="{ path: `/user/${message.sender.id}` }">
            <span v-if="message.is_new" class="d-inline-block g-pos-rel">
              <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
              <img class="g-brd-around g-brd-gray-light-v4 g-pa-2 g-width-50 g-height-50 rounded-circle" v-bind:src="message.sender._links.avatar" v-bind:alt="message.sender.name || message.sender.username">
            </span>
            <img v-else class="g-brd-around g-brd-gray-light-v4 g-pa-2 g-width-50 g-height-50 rounded-circle" v-bind:src="message.sender._links.avatar" v-bind:alt="message.sender.name || message.sender.username">
          </router-link>
        </div>
        <div class="align-self-center g-px-10">
          <h5 class="h5 g-color-gray-dark-v1 mb-0">
            <router-link v-bind:to="{ path: `/user/${message.sender.id}` }" class="g-text-underline--none--hover">
              <span class="g-mr-5">{{ message.sender.name || message.sender.username }}</span>
            </router-link>
            <small class="g-font-size-12 g-color-aqua">给你发送了<small v-if="message.new_count" class="g-font-size-12 g-color-deeporange"> {{ message.new_count }} 条新 </small>私信</small>
          </h5>
          <p class="m-0">{{ $moment(message.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</p>
        </div>
        <ul class="list-inline mb-0 align-self-center ml-auto">
          <li v-if="!message.is_blocking" class="list-inline-item g-mr-5">
            <button v-on:click="onBlock(message.sender.id)" class="btn btn-block u-btn-outline-red g-rounded-20 g-px-10">拉黑</button>
          </li>
          <li v-else class="list-inline-item g-mr-5">
            <button v-on:click="onUnblock(message.sender.id)" class="btn btn-block u-btn-outline-aqua g-rounded-20 g-px-10">取消拉黑</button>
          </li>

          <li class="list-inline-item">
            <router-link v-bind:to="{ name: 'MessagesHistory', query: { from: message.sender.id } }">
              <button class="btn btn-block u-btn-outline-primary g-rounded-20 g-px-10">聊天记录</button>
            </router-link>
          </li>
        </ul> 
      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="messages">
      <pagination
        v-bind:cur-page="messages._meta.page"
        v-bind:per-page="messages._meta.per_page"
        v-bind:total-pages="messages._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../../../store'
import Pagination from '../../Base/Pagination'

export default {
  name: 'List',  // this is the name of the component
  components: {
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      messages: ''
    }
  },
  methods: {
    getUserMessagesSenders (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/messages-senders/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.messages = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onBlock (id) {
      this.$swal({
        title: "Are you sure?",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, block he!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/block/${id}`
          this.$axios.get(path)
            .then((response) => {
              // handle success
              this.$swal('Successed', response.data.message, 'success')
              this.getUserMessagesSenders(this.sharedState.user_id)
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
              this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
            })
        } else {
          this.$swal('Cancelled', 'You are not blocking this user yet :)', 'error')
        }
      })
    },
    onUnblock (id) {
      const path = `/api/unblock/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.$swal('Successed', response.data.message, 'success')
          this.getUserMessagesSenders(this.sharedState.user_id)
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    }
  },
  created () {
    this.getUserMessagesSenders(this.sharedState.user_id)
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUserMessagesSenders(this.sharedState.user_id)
  }
}
</script>
