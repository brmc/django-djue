{% autoescape off %}{% for component in components %}
{{ component.relative_module_import_string }}{% endfor %}

export default {
  components: { {% for component in components %}
    {{ component.name }}, {% endfor %}
  }
}{% endautoescape %}