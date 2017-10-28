const state = {
  objects: {
    all: [],
    master: [],
  },
  fields: {{% for field in fields %}
{{ field.name }}: {
  validators: [{% for validator in field.validator_names %}
    {{ validator }}, {% endfor %}
  ]
},{% endfor %}
}
}

// getters
const getters = {
  getAll () {

  },

  getById () {

  },
}

// actions
const actions = {
  validate ({commit, state}, object) {
    let errors = {}
    let isValid = true
    for (const [name, value] of object) {
      let messages = []
      for (let validator of state.fields[name].validators) {
        validator = new validator(value)

        if (validator.isValid()) {
          continue
        }
        isValid = false
        messages.push(validator.message)
      }

      if (messages.length === 0) {
        continue
      }
      errors[name] = messages
    }

    if (isValid) {
      commit('ACCEPT_CHANGES', {object})
    } else {
      commit('REJECT_CHANGES', {object, errors})
    }
  },
  revert ({commit, state}, object) {
    const master = state.getMaster(object.id)

    commit('SET_STATE', master)
  },
}

// mutations
const mutations = {
  ['REJECT_CHANGES'] (state, {object, errors}) {
    for (const [name, _] of state.fields) {
      state.objects.all[object.id].errors = errors[name] || []
    }
  },

  ['ACCEPT_CHANGES'] (state, {object}) {
    for (const field of object) {
      field.errors = []
    }

    state.objects.all[object.id] = object
  },
}

export default {
  state,
//    getters,
  actions,
  mutations,
}
