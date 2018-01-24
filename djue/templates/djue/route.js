{% if route.view %}{
    path: '{{route.url|safe}}',{% if route.view %}
    component: {{route.view.name}},{% else %}component: Home,{% endif %}{% if route.name %}
    name: '{{ route.lookup_name }}', {% endif %}{% if route.children %}
    children: [{% for child in route.children %}
      {% include 'djue/route.js' with route=child %},{% endfor %}
    ]{% endif %}
  }{% else %}{% for child in route.children %}{% include 'djue/route.js' with route=child prefix=child.path %}{% if not forloop.last %},
{% endif %}{% endfor %}{% endif %}