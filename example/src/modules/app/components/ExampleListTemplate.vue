<template>
You must create a template
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      // todo: include relevant data
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
      // todo: customize fetchdata logic
    },
  },
}

</script>

<style>

</style>