import { mapState, mapActions } from 'vuex'

export default {
  {% autoescape off %}
  data () {
    return {
      loading: true,
      // todo: include relevant data
    }
  },
  computed: {
    ...mapState('{{ self.app }}/{{ self.model }}', {
      objects: state => state.objects
    })
  },
  created () {
    this.{{ self.action }}()
  },
  watch: {
    '$route': '{{ self.action }}',
  },
  methods: {
    ...mapActions('{{ self.app }}/{{ self.model }}', [
      '{{ self.action }}'
    ])
  },
}{% endautoescape %}

