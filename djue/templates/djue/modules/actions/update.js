import Vue from 'vue'
import UpdateViewSetComponent from '../../../components/UpdateViewSetComponent'
import {{ component.name }} from './{{ component.name }}'

export default Vue.extend({
  mixins: [UpdateViewSetComponent],
  components: { InstanceForm: {{ component.name }} },
  data () {
    return {
      namespace: '{{ app }}/{{ model }}',
      objectName: '{{ model }}',
      routeName: '{{ route }}',
    }
  },
})