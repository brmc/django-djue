  {
    path: '{{route.url}}',{% if route.view %}
    component: {{route.view.name}},{% elif route.url == '/' %}component: Home,{% endif %}{% if route.name %}
    name: '{{ route.lookup_name }}', {% endif %}{% if route.children %}
    children: [{% for child in route.children %}
      {% include 'djue/route.js' with route=child %},{% endfor %}
    ]{% endif %}
  }