<template>
  <div>
    <div id="app">
      <a-p-i-root-view/>
    </div>
    <div class="grid">
      <router-view name="nav"/>
      <router-view/>
    </div>
  </div>
</template>

<script>
  import APIRootView from './modules/rest_framework/components/APIRootView'

  export default {
    components: {APIRootView},
    name: 'app',
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  .grid {
    display: grid;
    grid-auto-columns: auto auto;
    grid-auto-flow: column;
  }
</style>
