<template>{% if template %}
  {{ template }}{% else %}
  <{{ component }}></{{ component }}>{% endif %}
</template>

<script>{% for import in import %}
  {{ import }}{% endfor %}

  export default {
    components: { {% for component in components %}
      {{ component }},{% endfor %}
    }
  }
</script>
