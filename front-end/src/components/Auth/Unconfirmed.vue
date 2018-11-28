<template>
  <div class="container">
    <alert 
      v-for="(alert, index) in alerts" :key="index"
      v-bind:variant="alert.variant"
      v-bind:message="alert.message">
    </alert>

    <h5 class="h5 g-color-gray-dark-v1 mb-0">
      <span class="g-color-red">Need another confirmation email?</span>
      <button v-on:click="onResendConfirm()" type="button" class="btn btn-primary">Click here</button>
    </h5>
  </div>
</template>

<script>
import store from '../../store'
import Alert from '../Base/Alert'

export default {
  name: 'Confirm',
  components: {
    alert: Alert
  },
  data() {
    return {
      sharedState: store.state,
      user: '',
      alerts: ''
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
          this.alerts = [
            {
              variant: 'info',
              message: `Hello, ${this.user.name || this.user.username}`
            },
            {
              variant: 'danger',
              message: 'You have not confirmed your account yet.'
            },
            {
              variant: 'success',
              message: 'Before you can access this site you need to confirm your account. Check your inbox, you should have received an email with a confirmation link.'
            }
          ]
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onResendConfirm () {
      const path = '/api/resend-confirm'
      const payload = {
        confirm_email_base_url: window.location.href.split('/', 4).join('/') + '/unconfirmed/?token='
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onConfirm (token) {
      this.$axios.get(`/api/confirm/${token}`)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          // 更新 JWT
          window.localStorage.setItem('madblog-token', response.data.token)
          store.loginAction()
          // 路由跳转
          this.$router.push('/')
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    }
  },
  created () {
    // 点击邮件中的链接后，确认账户
    if (this.$route.query.token) {
      this.onConfirm(this.$route.query.token)
    }

    // 未确认的用户，显示提示信息
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
  }
}
</script>
