import Vue from 'vue'

function loadFieldErrors (state, data) {
  const objId = this.getters.getRoutePK
  let target = state.objects.local[objId] || state.objects.new

  for (const [field, errors] of Object.entries(data)) {
    Vue.set(target[field], 'errors', errors)
  }
}

function loadGeneralErrors (state, data) {
  Vue.set(state, 'errors', data)
}

function clearGeneralErrors (state) {
  Vue.set(state, 'errors', null)
}

export default {
  LOAD_ERRORS (state, error) {
    const response = error.response
    const data = response.data

    switch (response.status) {
      case 400:
        loadFieldErrors.call(this, state, data)
        break
      default:
        loadGeneralErrors.call(this, state, Object.values(data))
    }
  },
  LOAD_ALL (state, response) {
    let objects = response.data
    let data = {}
    for (let obj of objects) {
      let inner = {}
      for (let key of Object.getOwnPropertyNames(obj)) {
        inner[key] = {
          value: obj[key],
          errors: [],
        }
      }
      data[obj.id] = inner
    }
    let clone = JSON.parse(JSON.stringify(data))
    Vue.set(state.objects, 'local', data)
    Vue.set(state.objects, 'master', clone)
    clearGeneralErrors(state)
  },
  LOAD_ONE (state, response) {
    let object = response.data
    let data = {}
    for (let key of Object.getOwnPropertyNames(object)) {
      data[key] = {
        value: object[key],
        errors: [],
      }
    }

    const objects = state.objects
    const id = data.id.value

    let clone = JSON.parse(JSON.stringify(data))
    Vue.set(objects.local, id, data)
    Vue.set(objects.master, id, clone)
    clearGeneralErrors(state)
  },
  LOAD_LOCAL (state, local) {
    Vue.set(state.objects.local, local.id.value, local)
  },
  REMOVE (state, response) {
    const id = this.getters.getRoutePK
    const objects = state.objects
    Vue.set(objects.local, id, null)
    Vue.set(objects.master, id, null)
    delete objects.local[id]
    delete objects.master[id]
    clearGeneralErrors(state)
  },
  REVERT (state, id) {
    const objects = state.objects
    const active = objects.local[id]
    const original = objects.master[id]
    const clone = JSON.parse(JSON.stringify(original))
    Vue.set(objects.local, id, clone)

    for (let [name, field] of Object.entries(active)) {
      field.value = original[name].value
    }

  },
  RESET_NEW (state) {
    for (let [name, field] of Object.entries(state.objects.new)) {
      Vue.set(field, 'value', '')
      Vue.set(field, 'errors', [])
    }
  },
  VALIDATE_FIELD (state, {payload}) {
    const {object, field, value, id, error} = payload
    let errors = error ? [error] : []

    const validators = state.fields[field].validators

    validators.forEach(validator => {
      let [isValid, error] = validator.validate(value)

      if (!isValid) {
        errors.push(error)
      }
    })

    const obj = object[field]

    Vue.set(obj, 'value', value)
    Vue.set(obj, 'errors', errors)
  },
}