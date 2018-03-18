<template>
  <div>
    <div v-if="success">{{successMessage}}</div>
    <instance-form :object="object"
                   :method="update"
                   :action='routeDescription'
                   @reset="undo"
                   @success="handleSuccess"/>
  </div>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import stateModule from '../util'

  export default {
    data () {
      return {
        objectName: 'Object',
        success: false,
      }
    },
    computed: {
      successMessage () {
        return `${this.objectName} was saved`
      },
      ...mapState({
        stateModule,
        object (state) {
          return this.stateModule.objects.local[this.$route.params.pk]
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
    created () {
      if (!this.object) {}
    },
    watch: {
      $route (from, to) {
        this.success = false
      },
    },
    methods: {
      ...mapActions({
        update (dispatch, {url, payload}) {
          return dispatch(`${this.namespace}/update`, {url, payload})
        },
        revert (dispatch, id) {
          return dispatch(`${this.namespace}/revert`, id)
        },
      }),
      handleSuccess () {
        this.success = true
      },
      undo () {
        this.revert(this.object.id.value)
      },
    },
  }
</script>

<style>
  input:invalid {
    border: solid 1px red
  }
</style>