import Vue from 'vue'
import CreateViewSetComponent from '../../../components/CreateViewSetComponent'
import {{ component.name }} from './{{ component.name }}'

export default Vue.extend({
  mixins: [CreateViewSetComponent],
  components: {InstanceForm: {{ component.name }}},
  data () {
    return {
      namespace: '{{ app }}/{{ model|capfirst }}',
      objectName: '{{ model|capfirst }}',
      routeName: '{{ route }}',
    }
  },
})