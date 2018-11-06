<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
export default {
  name: 'Ping',
  data() {
    return {
      msg: ''
    }
  },
  methods: {
    getMessage () {
      const path = '/ping'
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
