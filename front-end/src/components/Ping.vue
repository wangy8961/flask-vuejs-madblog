<template>
  <div class="container">
    <alert 
      v-for="(alert, index) in alerts" :key="index"
      v-bind:variant="alert.variant"
      v-bind:message="alert.message">
    </alert>

    <button type="button" class="btn btn-primary">{{ msg }}</button>

    <span class="d-inline-block g-pos-rel g-mr-20 g-mb-20">
      <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
      <img class="media-object g-rounded-50x u-image-icon-size-md" src="http://www.madmalls.com/static/main/images/avatar.jpg" alt="Image Description">
    </span>
  </div>
</template>

<script>
import Alert from './Base/Alert'

export default {
  name: 'Ping',
  components: {
    alert: Alert
  },
  data() {
    return {
      msg: '',
      alerts: [
        {
          variant: 'info',
          message: 'Hi'
        },
        {
          variant: 'danger',
          message: 'Oops..'
        },
        {
          variant: 'success',
          message: 'OK'
        }
      ]
    }
  },
  methods: {
    getMessage () {
      const path = '/api/ping'
      this.$axios.get(path)
        .then((res) => {
          this.msg = res.data
          this.$toasted.info('Success connect to Flask API', { icon: 'fingerprint' })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  },
  created () {
    this.getMessage()
  }
}
</script>
