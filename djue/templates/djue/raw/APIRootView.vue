<template>
  <div>
    <ul>
      <li v-if="!urls">...loading</li>
      <li v-else="" v-for="(url, name) in urls">
        <router-link :to="url">{% verbatim %}{{ name }}{% endverbatim %}</router-link>
      </li>
    </ul>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  export default {
    computed: {
      urls () {
        return this.$store.state.urls
      },
    },
  }

</script>

<style>
</style>