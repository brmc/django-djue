<template>
  <div>
    <button v-if="active !== 0" @click='activate(0)'>List</button>
    <button v-if="active !== 1" @click='activate(1)'>Create</button>
    <keep-alive>
      <list-component v-if="active === 0"/>
    </keep-alive>
    <create-component v-if="active === 1"/>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        active: 0,
      }
    },
    methods: {
      /**
       * @param {Number} i
       */
      activate (i) {
        this.active = i
      },
    },
  }

</script>