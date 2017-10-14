{% autoescape off %}{% for import in imports %}
{{ import }}{% endfor %}

export default {
  components: { {% for name in names %}
    {{ name }}, {% endfor %}
  }
}{% endautoescape %}