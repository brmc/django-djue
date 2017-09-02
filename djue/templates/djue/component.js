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
      let object = this.$store.state.items[this.$route.params.id] || {}

      Object.assign(this, object)
      this.object = object
      this.loading = false
    },
    save (a, b, c) {
      let object = this.id === this.$route.params.id ? this.object : {}
      Object.assign(this, object)

      this.$store.dispatch('MODEL_SAVES', {object})
    },

    save () {
      $store.dispatch('MODEL_{{ model|upper }}_SAVE')
    },

    delete () {
      $store.commit('MODEL_{{ model|upper }}_DELETE')
    },

    revert () {
      $store.dispatch('MODEL_{{ model|upper }}_REVERT')
    }
  },
}{% endautoescape %}
