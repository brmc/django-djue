/**
 * @param {Object} local
 * @param {Object} master
 * @param {string[]} fields
 * @return {boolean}
 */
export function areEqual (local, master, fields) {
  fields = fields || Object.getOwnPropertyNames(local)
  for (const field of fields) {
    if (local[field].value !== master[field].value) {
      return false
    }
  }

  return true
}

/**
 * Vuex only allows dynamic namespaces inside mapped functions
 * Mapped actions can be dispatched by passing the namespaced string, but
 * there is no equivalent for mapped state.  It's possible to get
 * the state using brackets [] but this breaks down when dealing
 * with nested name spaces.
 *
 * This utility is expected to be passed into a components
 * `mapState` computed field.
 *
 * PS, it does not need to be bound because of how Vue wires things
 * together. `this` will refer to component it is attached to
 *
 * @param {Object} state
 * @return {Object}
 */
export default function stateModule (state) {
  this.namespace.split('/').forEach(n => state = state[n])
  return state
}