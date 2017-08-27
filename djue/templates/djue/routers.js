{% autoescape off %}{% for import in imports %}
{{ import }}{% endfor %}

export default [
  {% include "djue/route.js" with route=route %}
];
{% endautoescape %}