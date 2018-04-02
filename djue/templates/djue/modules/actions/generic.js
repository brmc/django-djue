import {mapActions, mapState} from 'vuex'

export default {
  {% autoescape off %}
  data () {
    return {
      loading: true,{% if model %}
      namespace: '{{ app }}/{{ model }}',
      objectName: '{{ model }}',{% endif %}{% if route %}
      routeName: '{{ route }}',{% endif %}
      // todo: include relevant data
    }
  },
  computed: {
      ...mapState({

    })
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
