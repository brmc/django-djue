import {mapActions, mapState} from 'vuex'

export default {
  {% autoescape off %}
  data () {
    return {
      loading: true,
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
