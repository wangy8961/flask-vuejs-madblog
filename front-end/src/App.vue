<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Base/Navbar'

export default {
  name: 'App',
  components: {
    navbar: Navbar
  }
}
</script>

<style>
</style>