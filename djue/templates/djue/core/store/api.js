import axios from 'axios'
import router from '../router'

const BASEURL = 'http://localhost:8000'

let config = {
  baseURL: BASEURL,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
  timeout: 1000,
  withCredentials: false, // default
  responseType: 'text', // default
  xsrfCookieName: 'csrftoken', // default
  xsrfHeaderName: 'X-XSRF-TOKEN', // default
  onUploadProgress (progressEvent) {},
  onDownloadProgress: function (progressEvent) {},
  // `maxContentLength` defines the max size of the http response content allowed
  maxContentLength: 2000,

  validateStatus: function (status) {
    return status >= 200 && status < 300 // default
  },
}

/**
 * @param {string|Object} stuff
 * @return {string}
 */
function buildPath (stuff) {
  if (typeof stuff === 'string') {
    return stuff
  }

  if (typeof stuff !== 'object') {
    throw 'You\'re trying to build a path from stupid stuff. You need to pass '
  }

  // .resolve() throws an error due to property descriptor limitations
  // so a clone is necessary
  const clone = Object.assign({}, stuff)

  return router.resolve(clone).location.path
}

export default {
  /**
   * @param {string|Object} url can be a literal path or a vue route description
   * @return {AxiosPromise<any>}
   */
  get (url) {
    url = buildPath(url)
    return axios.get(url, config)
  },
  /**
   * @param {string|Object} url can be a literal path or a vue route description
   * @param {Object} payload data to be json-encoded and sent to the server
   * @return {AxiosPromise<any>}
   */
  post (url, payload) {
    url = buildPath(url)
    return axios.post(url, payload, config)
  },
  /**
   * @param {string|Object} url can be a literal path or a vue route description
   * @param {Object} payload data to be json-encoded and sent to the server
   * @return {AxiosPromise<any>}
   */
  put (url, payload) {
    url = buildPath(url)
    return axios.put(url, payload, config)
  },
  /**
   * @param {string|Object} url can be a literal path or a vue route description
   * @return {AxiosPromise<any>}
   */
  destroy (url) {
    url = buildPath(url)
    return axios.delete(url, config)
  },
}