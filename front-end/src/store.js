export default {
  debug: true,
  state: {
    is_new: false,
    is_authenticated: window.localStorage.getItem('madblog-token') ? true : false
  },
  setNewAction () {
    if (this.debug) { console.log('setNewAction triggered') }
    this.state.is_new = true
  },
  resetNotNewAction () {
    if (this.debug) { console.log('resetNotNewAction triggered') }
    this.state.is_new = false
  },
  loginAction () {
    if (this.debug) { console.log('loginAction triggered') }
    this.state.is_authenticated = true
  },
  logoutAction () {
    if (this.debug) console.log('logoutAction triggered')
    window.localStorage.removeItem('madblog-token')
    this.state.is_authenticated = false
  }
}