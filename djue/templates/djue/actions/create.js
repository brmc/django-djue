import Vue from 'vue'
import CreateViewSetComponent from '../../../components/CreateViewSetComponent'
import {{ self.component }} from './{{ self.component }}'

export default Vue.extend({
  mixins: [CreateViewSetComponent],
  components: {InstanceForm: {{ self.component }}},
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model|capfirst }}',
      objectName: '{{ self.model|capfirst }}',
      routeName: '{{ self.model|lower }}-list',
    }
  },
})