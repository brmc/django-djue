  {
    path: '{{route.path}}',{% if route.view %}
    component: {{route.view.name}},{% endif %}{% if route.name %}
    name: '{{ route.name }}', {% endif %}{% if route.children %}
    children: [{% for child in route.children %}
      {% include 'djue/route.js' with route=child %},{% endfor %}
    ]{% endif %}
  }