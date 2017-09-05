export default {{% autoescape off %}
  data () {
    return {
      loading: true,
      // todo: include relevant data
    }
  },
  created () {
    this.fetchData()
  },
  watch: {
    '$route': 'fetchData',
  },
  methods: {
    fetchData () {
      // todo: customize fetchdata logic
    },
  },
}{% endautoescape %}
