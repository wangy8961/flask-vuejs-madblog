<template>
  <div class="container">
    <alert 
      v-for="(alert, index) in alerts" :key="index"
      v-if="alert.showAlert"
      v-bind:variant="alert.alertVariant"
      v-bind:message="alert.alertMessage">
    </alert>
    <button type="button" class="btn btn-primary">HomePage</button>
  </div>
</template>

<script>
import Alert from './Alert'

export default {
  name: 'Home',  //this is the name of the component
  components: {
    alert: Alert
  },
  data () {
    return {
      alerts: [
        {
          showAlert: true,
          alertVariant: 'danger',
          alertMessage: 0
        },
        {
          showAlert: true,
          alertVariant: 'info',
          alertMessage: 1
        },
        {
          showAlert: true,
          alertVariant: 'dark',
          alertMessage: 2
        }
      ]
    }
  }
}
</script>