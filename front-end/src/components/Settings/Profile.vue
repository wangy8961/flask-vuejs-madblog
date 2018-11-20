<template>
  <div>
    <h1>Public profile</h1>
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="name">Real Name</label>
        <input type="text" v-model="profileForm.name" class="form-control" id="name" placeholder="">
      </div>
      <div class="form-group">
        <label for="location">Location</label>
        <input type="text" v-model="profileForm.location" class="form-control" id="location" placeholder="">
      </div>
      <div class="form-group">
        <label for="about_me">About Me</label>
        <textarea v-model="profileForm.about_me" class="form-control" id="about_me" rows="5" placeholder=""></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Profile',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      profileForm: {
        name: '',
        location: '',
        about_me: ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          this.profileForm.name = response.data.name
          this.profileForm.location = response.data.location
          this.profileForm.about_me = response.data.about_me
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    onSubmit (e) {
      const user_id = this.sharedState.user_id
      const path = `/api/users/${user_id}`
      const payload = {
        name: this.profileForm.name,
        location: this.profileForm.location,
        about_me: this.profileForm.about_me
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed modify your profile.', { icon: 'fingerprint' })
          this.$router.push({ path: `/user/${user_id}/overview` })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    
  },
  created () {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
  }
}
</script>