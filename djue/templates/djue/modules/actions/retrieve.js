import Vue from 'vue'
import RetrieveViewSetComponent from '../../../components/RetrieveViewSetComponent'

export default Vue.extend({
  mixins: [RetrieveViewSetComponent],
  data () {
    return {
      namespace: '{{ app }}/{{ model }}',
    }
  },
})