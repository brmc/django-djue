import Vue from 'vue'
import Serializer from '../../../components/Serializer'

export default Vue.extend({
  mixins: [Serializer],

  data () {
    return {
      namespace: '{{ app }}/{{ model }}'
    }
  },
})