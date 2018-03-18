<template>
  <div>
    <div v-if="!object">...loading</div>
    <div v-else v-for="field in fieldNames">{{ field }}: {{
      object[field].value }}
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import stateModule from '../util'

  export default {
    computed: {
      ...mapState({
        stateModule,
        object (state) {
          return this.stateModule.objects.local[this.$route.params.pk]
        },
        fieldNames (state) {
          return Object.keys(this.stateModule.fields)
        },
      }),
    },
  }

</script>

<style>
</style>