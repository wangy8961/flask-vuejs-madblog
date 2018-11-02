<template>
  <div class="container">
    <alert 
      v-if="showAlert"
      v-bind:variant="alertVariant"
      v-bind:message="alertMessage">
    </alert>
    <button type="button" class="btn btn-primary">ProfilePage</button>
  </div>
</template>

<script>
import Alert from './Alert'

export default {
  name: 'Profile',  //this is the name of the component
  components: {
    alert: Alert
  },
  data () {
    return {
      showAlert: true,
      alertVariant: 'danger',
      alertMessage: 'You can see me when you have sign in'
    }
  }
}
</script>
