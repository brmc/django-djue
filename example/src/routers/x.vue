<template>
  <p><label for="id_name">Name:</label> <input type="text" name="name"
                                               v-model="name" maxlength="50"
                                               required id="id_name"/></p>
  <p><label for="id_description">Description:</label> <textarea
      name="description" cols="40" rows="10" required id="id_description"
      v-model="description">
</textarea></p>
</template>

<script>
  export default {}
</script>

<style>

</style>