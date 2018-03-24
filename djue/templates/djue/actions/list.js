import Vue from 'vue'
import ListViewSetComponent from '../../../components/ListViewSetComponent'

export default Vue.extend({
  mixins: [ListViewSetComponent],
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model }}',
      routeName: '{{ self.model|lower }}-list',
      detailRouteName: '{{ self.model|lower }}-detail',
    }
  },
})