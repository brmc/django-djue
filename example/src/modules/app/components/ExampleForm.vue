<template>
<form action="." method="post">
  <div v-if="loading">...Loading</div>
  <div v-else="">
    <p><label for="id_name">Name:</label>
 <input type="text" name="name" v-model="name.value" maxlength="50" required id="id_name" />
<div v-if="name.errors">
  <div v-for="error in name.errors">
    
    {{ error }}
    
  </div>
</div></p>
<p><label for="id_description">Description:</label>
 <textarea name="description" cols="40" rows="10" required id="id_description"
          v-model="description">
</textarea>
<div v-if="description.errors">
  <div v-for="error in description.errors">
    
    {{ error }}
    
  </div>
</div></p>

    <input type='button' @click="save" value="Save"/>
    <input v-if="id" type='button' @click="delete" value="Delete"/>
    <input type='button' @click="revert" value="Revert"/>
  </div>
</form>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      name: null,
      description: null,
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    '$route': 'fetchData',
  },
  methods: {
    fetchData() {
      this.loading = true
      let object = this.$store.state.items[this.$route.params.id] || {}

      Object.assign(this, object)
      this.object = object
      this.loading = false
    },
    save(a, b, c) {
      let object = this.id === this.$route.params.id ? this.object : {}
      Object.assign(this, object)

      this.$store.dispatch('MODEL_EXAMPLE_SAVE', { object })
    },

    delete() {
      this.$store.commit('MODEL_EXAMPLE_DELETE')
    },

    revert() {
      this.$store.dispatch('MODEL_EXAMPLE_REVERT')
    }
  },
}

</script>

<style>

</style>