<template>
  <div class="container">
    <h1>Reset Your Password</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <div class="form-group" v-bind:class="{'u-has-error-v1': resetPasswordForm.emailError}" >
            <label for="email">Email address</label>
            <input type="email" v-model="resetPasswordForm.email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="">
            <small class="form-control-feedback" v-show="resetPasswordForm.emailError">{{ resetPasswordForm.emailError }}</small>
          </div>
          <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',  // this is the name of the component
  data () {
    return {
      resetPasswordForm: {
        email: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        emailError: null,
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.resetPasswordForm.errors = 0  // 重置

      if (!this.resetPasswordForm.email) {
        this.resetPasswordForm.errors++
        this.resetPasswordForm.emailError = 'Email required.'
      } else if (!this.validEmail(this.resetPasswordForm.email)) {
        this.resetPasswordForm.errors++
        this.resetPasswordForm.emailError = 'Valid email required.'
      } else {
        this.resetPasswordForm.emailError = null
      }

      if (this.resetPasswordForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/reset-password-request'
      const payload = {
        confirm_email_base_url: window.location.href.split('/', 4).join('/') + '/reset-password/?token=',
        email: this.resetPasswordForm.email
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          this.$router.push('/login')
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    validEmail: function (email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  }
}
</script>