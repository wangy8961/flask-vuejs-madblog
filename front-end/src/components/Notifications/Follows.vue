<template>
  <div>
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-people g-pos-rel g-top-1 g-mr-5"></i> All Follows <small v-if="followers">(共 {{ followers._meta.total_items }} 个, {{ followers._meta.total_pages }} 页)</small>
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
      <div v-if="followers" class="card-block g-pa-0" >

        <div class="d-flex justify-content-start g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-10"
          v-for="(follower, index) in followers.items" v-bind:key="index">
          <div class="g-mt-2">
            <router-link v-bind:to="{ path: `/user/${follower.id}` }">
              <img class="g-width-50 g-height-50 rounded-circle mCS_img_loaded" v-bind:src="follower._links.avatar" v-bind:alt="follower.name || follower.username">
            </router-link>
          </div>
          <div class="align-self-center g-px-10">
            <h5 class="h5 g-color-gray-dark-v1 mb-0">
              <router-link v-bind:to="{ path: `/user/${follower.id}` }" class="g-text-underline--none--hover">
                <span class="g-mr-5">{{ follower.name || follower.username }}</span>
              </router-link>
              <small class="g-font-size-12 g-color-deeporange">{{ follower.followers_count }} followers</small>, <small class="g-font-size-12 g-color-aqua">{{ follower.followeds_count }} following </small>
              <span class="h6">关注了你</span>
            </h5>
            <p class="m-0">{{ $moment(follower.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</p>
          </div>
          <div class="align-self-center ml-auto">
            <button v-if="follower.is_following" v-on:click="onUnfollowUser(follower)" class="btn btn-block u-btn-outline-red g-rounded-20 g-px-10">Unfollow</button>
            <button v-if="!follower.is_following && follower.id != sharedState.user_id" v-on:click="onFollowUser(follower)" class="btn btn-block u-btn-outline-primary g-rounded-20 g-px-10">Follow</button>
          </div>
        </div>

      </div>
      <!-- End Panel Body -->
    </div>
  
    <!-- Pagination #04 -->
    <div v-if="followers && followers._meta.total_pages > 1">
      <pagination
        v-bind:cur-page="followers._meta.page"
        v-bind:per-page="followers._meta.per_page"
        v-bind:total-pages="followers._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../../store'
import Pagination from '../Base/Pagination'

export default {
  name: 'Follows',  // this is the name of the component
  components: {
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      followers: ''
    }
  },
  methods: {
    getUserFollowers (id) {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/api/users/${id}/followers/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.followers = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onFollowUser (follower) {
      const path = `/api/follow/${follower.id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          this.getUserFollowers(this.sharedState.user_id)
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onUnfollowUser (follower) {
      const path = `/api/unfollow/${follower.id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          this.getUserFollowers(this.sharedState.user_id)
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    this.getUserFollowers(this.sharedState.user_id)
  },
  // 进入子路由后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUserFollowers(this.sharedState.user_id)
  }
}
</script>