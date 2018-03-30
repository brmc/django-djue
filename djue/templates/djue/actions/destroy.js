import Vue from 'vue'
import { mapState } from 'vuex'

import DestroyViewSetComponent from '../../../components/DestroyViewSetComponent'

export default Vue.extend({
  mixins: [DestroyViewSetComponent],
  data () {
    return {
      namespace: '{{ self.app }}/{{ self.model }}',
      routeName: '{{ self.route }}',
    }
  },
  computed: {
    ...mapState('{{ self.app }}/{{ self.model }}', {
      object: function (state) {
        return state.objects.local[this.$route.params.pk]
      }
    }),
  },
})
