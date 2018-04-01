import Vue from 'vue'
import ListViewSetComponent from '../../../components/ListViewSetComponent'

export default Vue.extend({
  mixins: [ListViewSetComponent],
  data () {
    return {
      namespace: '{{ app }}/{{ model }}',
      routeName: '{{ route }}',
      detailRouteName: '{{ model|lower }}-detail',
    }
  },
})