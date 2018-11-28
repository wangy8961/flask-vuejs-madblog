<template>
  <div class="container">
    <h1>Sign In</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.usernameError}">
            <label for="username">Username</label>
            <input type="text" v-model="loginForm.username" class="form-control" id="username" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.usernameError">{{ loginForm.usernameError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.passwordError}">
            <label for="password">Password</label>
            <input type="password" v-model="loginForm.password" class="form-control" id="password" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.passwordError">{{ loginForm.passwordError }}</small>
          </div>
          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
      </div>
    </div>
    <br>
    <p>New User? <router-link to="/register">Click to Register!</router-link></p>
    <p>
        Forgot Your Password?
        <router-link v-bind:to="{ name: 'ResetPasswordRequest' }">Click to Reset It</router-link>
    </p>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Login',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.loginForm.errors = 0  // 重置

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/tokens'
      // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$axios.post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      }).then((response) => {
          // handle success
          window.localStorage.setItem('madblog-token', response.data.token)
          store.loginAction()

          this.$toasted.success(`Welcome ${this.sharedState.user_name}!`, { icon: 'fingerprint' })

          if (typeof this.$route.query.redirect == 'undefined') {
            this.$router.push('/')
          } else {
            this.$router.push(this.$route.query.redirect)
          }
        })
        .catch((error) => {
          // handle error
          // console.log('failed', error.response);
          if (typeof error.response != 'undefined') {
            if (error.response.status == 401) {
              this.loginForm.usernameError = 'Invalid username or password.'
              this.loginForm.passwordError = 'Invalid username or password.'
            } else {
              console.log(error.response)
            }
          }
        })
    }
  }
}
</script>