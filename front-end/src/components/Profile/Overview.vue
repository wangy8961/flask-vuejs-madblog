<template>
  <div>
    <!-- Username -->
    <div class="d-flex align-items-center justify-content-sm-between g-mb-5">
      <h2 v-if="user.name" class="g-font-weight-300 g-mr-10">{{ user.name }}</h2>
      <h2 v-else class="g-font-weight-300 g-mr-10">{{ user.username }}</h2>
    </div>
    <!-- End Username -->

    <!-- Member since -->
    <h4 v-if="user.member_since" class="h6 g-font-weight-300 g-mb-10">
      <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Member since : {{ $moment(user.member_since).format('LLL') }}
    </h4>
    <!-- End Member since -->

    <!-- Last seen -->
    <h4 v-if="user.last_seen" class="h6 g-font-weight-300 g-mb-10">
      <i class="icon-eye g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Last seen : {{ $moment(user.last_seen).fromNow() }}
    </h4>
    <!-- End Last seen -->

    <!-- User Info -->
    <ul class="list-inline g-font-weight-300">
      <li class="list-inline-item g-mr-20">
        <i class="icon-check g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Verified User
      </li>
      <li v-if="user.email" class="list-inline-item g-mr-20">
        <i class="icon-link g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>  <a class="g-color-main g-color-primary--hover" v-bind:href="'mailto:' + user.email">{{ user.email }}</a>
      </li>
    </ul>
    <!-- End User Info -->

    <!-- Location -->
    <h4 v-if="user.location" class="h6 g-font-weight-300 g-mb-10">
      <i class="icon-location-pin g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> {{ user.location }}
    </h4>
    <!-- End Location -->

    <div v-if="user.about_me">
      <div class="u-divider u-divider-db-dashed u-divider-center g-brd-gray-light-v2 g-mt-50 g-mb-30">
        <i class="u-divider__icon u-divider__icon--indented g-bg-gray-light-v4 g-color-gray-light-v1 rounded-circle">Me</i>
      </div>
      <p class="g-line-height-1_8 g-font-weight-300">{{ user.about_me }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Overview',  //this is the name of the component
  data () {
    return {
      user: ''
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    const user_id = this.$route.params.id
    this.getUser(user_id)
  },
  // 进入子路由后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUser(to.params.id)
  }
}
</script>