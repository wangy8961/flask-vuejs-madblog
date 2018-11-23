<template>
  <div class="container g-pt-20">
    <div class="row">
      <!-- Profile Settings -->
      <div class="col-lg-3 g-mb-50">
        <aside class="g-brd-around g-brd-gray-light-v4 rounded g-px-20 g-py-30">
          <!-- Profile Picture -->
          <div v-if="user" class="text-center g-pos-rel g-mb-30">
            <div class="g-width-100 g-height-100 mx-auto mb-3">
              <img class="img-fluid rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username">
            </div>

            <span class="d-block g-font-weight-500">{{ user.name || user.username }}</span>

            <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }">
              <span class="u-icon-v3 u-icon-size--xs g-color-white--hover g-bg-primary--hover rounded-circle g-pos-abs g-top-0 g-right-15 g-cursor-pointer" title="Go To Your Profile"
                    data-toggle="tooltip"
                    data-placement="top">
                <i class="icon-finance-067 u-line-icon-pro"></i>
              </span>
            </router-link>
          </div>
          <!-- End Profile Picture -->

          <hr class="g-brd-gray-light-v4 g-my-30">

          <!-- Profile Settings List -->
          <ul class="list-unstyled mb-0">
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'SettingProfile' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-media-112 u-line-icon-pro"></i></span>
                Profile
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'SettingAccount' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-medical-071 u-line-icon-pro"></i></span>
                Account
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'SettingEmail' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-communication-154 u-line-icon-pro"></i></span>
                Email
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'SettingNotification' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-electronics-031 u-line-icon-pro"></i></span>
                Notification
              </router-link>
            </li>
          </ul>
          <!-- End Profile Settings List -->
        </aside>
      </div>
      <!-- End Profile Settings -->

      <!-- Payment Options -->
      <div class="col-lg-9 g-mb-50">
        <!-- Products Block -->
        <div class="rounded g-brd-around g-brd-gray-light-v4 g-overflow-x-scroll g-overflow-x-visible--lg g-pa-30">
          
          <router-view></router-view>

        </div>
        <!-- End Products Block -->
      </div>
      <!-- End Payment Options -->
    </div>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Settings',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
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
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
    })
  }
}
</script>