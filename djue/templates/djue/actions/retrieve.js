import Vue from 'vue'
import RetrieveViewSetComponent from '../../../components/RetrieveViewSetComponent'

export default Vue.extend({
  mixins: [RetrieveViewSetComponent],
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model }}',
    }
  },
})