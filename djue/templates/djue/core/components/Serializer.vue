<template></template>

<script>
  import Vue from 'vue'
  import { mapActions, mapState } from 'vuex'
  import stateModule from '../util'

  export default Vue.extend({
    props: ['method', 'action', 'object'],
    created() {
      console.assert(this.namespace,
          "You must set `data.namespace` when creating a Serializer")
    },
    computed: {
      ...mapState({
        stateModule,
        fieldNames (state) {
          return Object.keys(this.stateModule.fields)
        },
      }),
    },
    methods: {
      ...mapActions({
        validateField (dispatch, payload) {
          dispatch(`${this.namespace}/validateField`, payload)
        },
      }),
      save (e) {
        const payload = {}
        let isValid = true

        this.fieldNames.forEach(fieldName => {
          const field = this.object[fieldName]
          if (field.errors.length > 0) {
            isValid = false
          }
          payload[fieldName] = field.value
        })

        if (!isValid) {
          return
        }

        this.method({url: this.action, payload: payload})
            .then(response => {
              if (response.status === 201 || response.status === 200) {
                this.$emit('success')
              }
            })
      },
      validate (e) {
        const payload = {
          object: this.object,
          field: e.target.name,
          id: this.object.id.value,
          value: e.target.value,
          error: e.target.validationMessage,
        }
        this.validateField({payload})
      },
    },
  })

</script>

<style>
  input:invalid {
    border: solid 1px red
  }
</style>