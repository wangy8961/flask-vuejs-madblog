<template>
  <div class="container">
    <h1>Change Your Password</h1>
    <form @submit.prevent="onSubmit">
      <div class="form-group" v-bind:class="{'u-has-error-v1': changePasswordForm.oldPasswordError}">
        <label for="oldPassword">Old Password</label>
        <input type="password" v-model="changePasswordForm.oldPassword" class="form-control" id="oldPassword" placeholder="">
        <small class="form-control-feedback" v-show="changePasswordForm.oldPasswordError">{{ changePasswordForm.oldPasswordError }}</small>
      </div>
      <div class="form-group" v-bind:class="{'u-has-error-v1': changePasswordForm.newPasswordError}">
        <label for="newPassword">New Password</label>
        <input type="password" v-model="changePasswordForm.newPassword" class="form-control" id="newPassword" placeholder="">
        <small class="form-control-feedback" v-show="changePasswordForm.newPasswordError">{{ changePasswordForm.newPasswordError }}</small>
      </div>
      <button type="submit" class="btn btn-primary">Update Password</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Account',  // this is the name of the component
  data () {
    return {
      changePasswordForm: {
        oldPassword: '',
        newPassword: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        oldPasswordError: null,
        newPasswordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.changePasswordForm.errors = 0  // 重置

      if (!this.changePasswordForm.oldPassword) {
        this.changePasswordForm.errors++
        this.changePasswordForm.oldPasswordError = 'Old Password required.'
      } else {
        this.changePasswordForm.oldPasswordError = null
      }

      if (!this.changePasswordForm.newPassword) {
        this.changePasswordForm.errors++
        this.changePasswordForm.newPasswordError = 'New Password required.'
      } else {
        this.changePasswordForm.newPasswordError = null
      }

      if (this.changePasswordForm.errors > 0) {
        // 如果旧密码或新密码为空时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      } else if (this.changePasswordForm.newPassword == this.changePasswordForm.oldPassword) {
        // 旧密码与新密码不为空，但值相等，也不允许
        this.changePasswordForm.oldPasswordError = 'The new password can not be equal to the old password.'
        this.changePasswordForm.newPasswordError = 'The new password can not be equal to the old password.'
        return false
      }

      const path = `/api/update-password`
      const payload = {
        old_password: this.changePasswordForm.oldPassword,
        new_password: this.changePasswordForm.newPassword
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
    }
  }
}
</script>