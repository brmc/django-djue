{% if route.view or route.url == '/' %}  {
    path: '{{route.url}}',{% if route.view %}
    component: {{route.view.name}},{% else %}component: Home,{% endif %}{% if route.name %}
    name: '{{ route.lookup_name }}', {% endif %}{% if route.children %}
    children: [{% for child in route.children %}
      {% include 'djue/route.js' with route=child %},{% endfor %}
    ]{% endif %}
  } {% else %}{% for child in route.children %}{% include 'djue/route.js' with route=child %}{% if not forloop.last %},{% endif %}{% endfor %}{% endif %}