<template>
  <div>
    <div v-if="errors" v-for="error in errors">
      {{error}}
    </div>
    <div>
      <retrieve-component v-if="!edit"/>
      <update-component v-else/>
      <a href="#" v-if="edit" @click.prevent.stop="edit = false">Cancel</a>
      <a href="#" v-else @click.prevent.stop="edit = true">Edit</a>
      <destroy-component/>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  import stateModule from '../util'

  export default {
    data () {
      return {
        edit: false,
      }
    },
    computed: {
      ...mapState({
        stateModule,
        object (state) {
          return this.stateModule.objects.local[this.$route.params.pk]
        },
        errors (state) {
          return this.stateModule.errors
        },
      }),
      routeDescription () {
        return {
          name: this.routeName,
          params: {
            pk: this.object.id.value,
          },
        }
      },
    },
    watch: {
      $route (to, from) {
        this.edit = false
        this.retrieve(to)
      },
    },
    created () {
      this.retrieve(this.$route)
    },
    methods: {
      ...mapActions({
        retrieve (dispatch, route) {
          return dispatch(`${this.namespace}/retrieve`, route)
        }
      }),
    },
  }
</script>

<style>
</style>