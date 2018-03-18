<template>
  <div>
    <div v-if="confirmDelete">
      <p> Are you sure you would like to delete this object?</p>
      <a href="#" @click.prevent.stop="destroy">Yes</a>
      <a href="#" @click.prevent.stop="confirmDelete=false">No</a>
    </div>
    <div v-else>
      <input type="button" @click.prevent.stop="confirmDelete=true"
         value="Delete"/>
    </div>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    data () {
      return {
        confirmDelete: false,
      }
    },
    computed: {
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
      $route () {
        this.confirmDelete = false
      },
    },
    methods: {
      ...mapActions({
        destroy (dispatch) {
          return dispatch(`${this.namespace}/destroy`, this.routeDescription)
        },
      }),
    },
  }
</script>

<style>
</style>