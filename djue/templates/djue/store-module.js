import {mapState} from 'vuex'

export default {
    namespaced: true,
    state: {{% for field in fields %}
        [{{ field }}]: null,
    {% endfor %}
    }
}
