import Vue from 'vue'
import UpdateViewSetComponent from '../../../components/UpdateViewSetComponent'
import {{ self.component }} from './{{ self.component }}'

export default Vue.extend({
  mixins: [UpdateViewSetComponent],
  components: { InstanceForm: {{ self.component }} },
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model }}',
      objectName: '{{ self.model }}',
      routeName: '{{ self.route }}',
    }
  },
})