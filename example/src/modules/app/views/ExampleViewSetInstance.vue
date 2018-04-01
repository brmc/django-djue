<template>
<destroy-example-view-set-component></destroy-example-view-set-component>
<example-serializer></example-serializer>
<retrieve-example-view-set-component></retrieve-example-view-set-component>
</template>

<script>
import ExampleSerializer from '.././components/ExampleSerializer.vue'
import DestroyExampleViewSetComponent from '.././components/DestroyExampleViewSetComponent.vue'
import RetrieveExampleViewSetComponent from '.././components/RetrieveExampleViewSetComponent.vue'

export default {
  components: {
    ExampleSerializer,
    DestroyExampleViewSetComponent,
    RetrieveExampleViewSetComponent,
  }
}

</script>

<style>

</style>