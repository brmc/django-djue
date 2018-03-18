import api from './api'
import { areEqual } from '../util'

/**
 * @param {Function} commit
 * @param {Object} state
 * @param {string|Object} path can be a literal path or a vue route description
 * @return {Promise<T>}
 */
function list ({commit, state}, path) {
  return api.get(path)
      .then(response => commit('LOAD_ALL', response))
      .catch(error => {
        commit('LOAD_ERRORS', error)
        return error
      })
}

/**
 * @param {Function} commit
 * @param {Object} state
 * @param {string|Object} path can be a literal path or a vue route description
 * @return {Promise<T>}
 */
function retrieve ({commit, state}, path) {
  const pk = path.params.pk
  const local = state.objects.local[pk]
  const master = state.objects.master[pk]
  const fields = Object.keys(state.fields)

  if (local && master && !areEqual(local, master, fields)) {
    return commit('LOAD_LOCAL', local)
  }

  return api.get(path)
      .then(response => commit('LOAD_ONE', response))
      .catch(error => {
        commit('LOAD_ERRORS', error)
        return error
      })
}

/**
 * @param {Function} commit
 * @param {Object} state
 * @param {string|Object} url can be a literal path or a vue route description
 * @param {Object} payload data to be json-encoded and sent to the server
 * @return {Promise<T>}
 */
function create ({commit, state}, {url, payload}) {
  return api.post(url, payload)
      .then(response => {
        commit('LOAD_ONE', response)
        return response
      })
      .catch(error => {
        commit('LOAD_ERRORS', error)
        return error
      })
}

/**
 * @param {Function} commit
 * @param {Object} state
 * @param {string|Object} url can be a literal path or a vue route description
 * @param {Object} payload data to be json-encoded and sent to the server
 * @return {Promise<T>}
 */
function update ({commit, state}, {url, payload}) {
  return api.put(url, payload)
      .then(response => {
        commit('LOAD_ONE', response)
        return response
      })
      .catch(error => {
        commit('LOAD_ERRORS', error)
        return error
      })
}

/**
 * @param {Function} commit
 * @param {Object} state
 * @param {string|Object} url can be a literal path or a vue route description
 * @return {Promise<T>}
 */
function destroy ({commit, state}, url) {
  return api.destroy(url)
      .then(response => commit('REMOVE', response))
      .catch(error => {
        commit('LOAD_ERRORS', error)
        return error
      })
}

/**
 * @param {Function} commit
 * @param {Object} state
 */
function resetNew ({commit, state}) {
  commit('RESET_NEW', state)
}

/**
 * @param {Function} commit
 * @param {number} id
 */
function revert ({commit}, id) {
  commit('REVERT', id)
}

/**
 * @param {Function} commit
 * @param {Object} payload
 */
function validateField ({commit}, {payload}) {
  commit('VALIDATE_FIELD', {payload})
}

export default {
  create,
  update,
  retrieve,
  destroy,
  list,
  resetNew,
  revert,
  validateField,
}