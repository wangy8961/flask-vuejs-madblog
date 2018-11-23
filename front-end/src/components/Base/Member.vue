<template>
  <div>
    <div class="d-flex justify-content-start g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-10">
      <div class="g-mt-2">
        <router-link v-bind:to="{ path: `/user/${member.id}` }">
          <span v-if="member.is_new" class="d-inline-block g-pos-rel">
            <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
            <img class="g-brd-around g-brd-gray-light-v4 g-pa-2 g-width-50 g-height-50 rounded-circle" v-bind:src="member._links.avatar" v-bind:alt="member.name || member.username">
          </span>
          <img v-else class="g-brd-around g-brd-gray-light-v4 g-pa-2 g-width-50 g-height-50 rounded-circle" v-bind:src="member._links.avatar" v-bind:alt="member.name || member.username">
        </router-link>
      </div>
      <div class="align-self-center g-px-10">
        <h5 class="h5 g-color-gray-dark-v1 mb-0">
          <router-link v-bind:to="{ path: `/user/${member.id}` }" class="g-text-underline--none--hover">
            <span class="g-mr-5">{{ member.name || member.username }}</span>
          </router-link>
          <small class="g-font-size-12 g-color-deeporange">{{ member.followers_count }} followers</small>, <small class="g-font-size-12 g-color-aqua">{{ member.followeds_count }} following </small>
        </h5>
        <p class="m-0">{{ $moment(member.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</p>
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