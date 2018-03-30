{% autoescape off %}{% for import in imports %}
{{ import }}{% endfor %}


export default Vue.extend({
  mixins: [ViewSetInstance],
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model }}',
      routeName: '{{ self.model|lower }}-detail'
    }
  },
  components: { {% for name in names %}
  {{ name }}, {% endfor %}
  },
})
export default {

}{% endautoescape %}