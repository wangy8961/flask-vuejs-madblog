<template>
  <div>
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-people g-pos-rel g-top-1 g-mr-5"></i> User Followeds <small v-if="followeds">(共 {{ followeds._meta.total_items }} 个, {{ followeds._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 个
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 个
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 个
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 个
            </router-link>
            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="followeds" class="card-block g-pa-0" >

        <member v-for="(followed, index) in followeds.items" v-bind:key="index"
          v-bind:member="followed"
          v-on:follow-user="onFollowUser(followed)"
          v-on:unfollow-user="onUnfollowUser(followed)">
        </member>

      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="followeds">
      <pagination
        v-bind:cur-page="followeds._meta.page"
        v-bind:per-page="followeds._meta.per_page"
        v-bind:total-pages="followeds._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import Member from '../Base/Member'
import Pagination from '../Base/Pagination'

export default {
  name: 'Following',  //this is the name of the component
  components: {
    Member,
    Pagination
  },
  data () {
    return {
      followeds: ''
    }
  },
  methods: {
    getUserFolloweds (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/followeds/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.followeds = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onFollowUser (followed) {
      const path = `/api/follow/${followed.id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          // 必须加个动态参数，不然路由没变化的话，User 组件不会重新执行 getUser()，就不会更新 Following 计数
          this.$router.push({ path: this.$route.fullPath, query: { timestamp: Number(new Date()) } })
          // this.getUserFolloweds(this.$route.params.id || this.sharedState.user_id)
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onUnfollowUser (followed) {
      const path = `/api/unfollow/${followed.id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          // 必须加个动态参数，不然路由没变化的话，User 组件不会重新执行 getUser()，就不会更新 Following 计数
          this.$router.push({ path: this.$route.fullPath, query: { timestamp: Number(new Date()) } })
          // this.getUserFolloweds(this.$route.params.id || this.sharedState.user_id)
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    const user_id = this.$route.params.id || this.sharedState.user_id
    this.getUserFolloweds(user_id)
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    const user_id = to.params.id || this.sharedState.user_id
    this.getUserFolloweds(user_id)
  }
}
</script>