<template>
<div><list-example-view-set-component></list-example-view-set-component>
<example-serializer></example-serializer></div>
</template>

<script>
import ExampleSerializer from '.././components/ExampleSerializer.vue'
import ListExampleViewSetComponent from '.././components/ListExampleViewSetComponent.vue'

export default {
  components: {
    ListExampleViewSetComponent,
    ExampleSerializer,
  }
}

</script>

<style>

</style>