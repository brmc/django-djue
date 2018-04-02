import {mapActions, mapState} from 'vuex'

export default {
  {% autoescape off %}
  data () {
    return {
      loading: true,{% if model %}
      namespace: '{{ app }}/{{ model }}',
      objectName: '{{ model }}',{% endif %}{% if route %}
      routeName: '{{ route }}',{% endif %}{% for var in preserved_vars %}
      {{ var }}: 'Placeholder value for "{{ var }}"',{% endfor %}
      // todo: include relevant data
    }
  },
  computed: {
    ...mapState({{% if context_obj_name %}
      stateModule,
      {{ context_obj_name }} (state) {
        return this.stateModule.objects.local[this.$route.params.pk]
      },
      fieldNames (state) {
        return Object.keys(this.stateModule.fields)
      },{% endif %}
    }),
  },
  created () {
    this.fetchData()
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    ...mapActions({

    }),
    fetchData () {
      // todo: customize fetchdata logic
    },
  },
}{% endautoescape %}
