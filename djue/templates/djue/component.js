import mapGetters from 'vuex'

export default {{% autoescape off %}
  data () {
    return {
      loading: true, {% for field in form %}
      {{ field.name }}: null,{% endfor %}
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
      this.loading = true
      let object = this.$store.state.{{ app }}.{{ model }}.objects.all[this.$route.params.id] ||
        this.$store.state.{{ app }}.{{ model }}.objects.new

      Object.assign(this, object)
      this.object = object
      this.loading = false
    },
    save () {
      let object = this.id === this.$route.params.id ? this.object : {}
      Object.assign(this, object)

      this.$store.dispatch('{{ app }}/save', {object})
    },

    remove () {
      this.$store.commit('MODEL_{{ model|upper }}_DELETE')
    },

    revert () {
      this.$store.dispatch('MODEL_{{ model|upper }}_REVERT')
    }
  },
}{% endautoescape %}
