  {
    path: '{{route.path}}',{% if route.component %}
    component: {{route.component}},{% endif %}{% if route.name %}
    name: '{{ route.name }}', {% endif %}{% if route.children %}
    children: [{% for child in route.children %}
      {% include 'djue/route.js' with route=child %},{% endfor %}
    ]{% endif %}
  }