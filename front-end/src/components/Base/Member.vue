<template>
  <div>
    <div class="d-flex justify-content-start g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-10">
      <div class="g-mt-2">
        <router-link v-bind:to="{ path: `/user/${member.id}` }">
          <img class="g-width-50 g-height-50 rounded-circle mCS_img_loaded" v-bind:src="member._links.avatar" v-bind:alt="member.name || member.username">
        </router-link>
      </div>
      <div class="align-self-center g-px-10">
        <h5 class="h6 g-font-weight-600 g-color-black g-mb-3">
          <span class="g-mr-5">{{ member.name || member.username }}</span>
          <small class="g-font-size-12 g-color-blue">{{ member.followeds_count }} followeds </small>, <small class="g-font-size-12 g-color-pink">{{ member.followers_count }} followers</small>
        </h5>
        <p class="m-0"><strong>Follow Since: </strong> {{ $moment(member.timestamp).format('LLL') }}</p>
      </div>
      <div class="align-self-center ml-auto">
        <button v-if="member.is_following" v-on:click="$emit('unfollow-user')" class="btn btn-block u-btn-outline-red g-rounded-20 g-px-10">Unfollow</button>
        <button v-if="!member.is_following && member.id != sharedState.user_id" v-on:click="$emit('follow-user')" class="btn btn-block u-btn-outline-primary g-rounded-20 g-px-10">Follow</button>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Member',  //this is the name of the component
  props: ['member'],
  data () {
    return {
      sharedState: store.state
    }
  }
}
</script>