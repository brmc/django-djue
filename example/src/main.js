import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import axios from 'axios'

new Vue({
  el: 'body',
  components: {App},
})

window.v = VueRouter

let a = {
  url: '/Example',
  method: 'get', // default
  baseURL: 'http://localhost:8000',

  headers: {'X-Requested-With': 'XMLHttpRequest'},

  data: {
    firstName: 'Fred',
  },

  timeout: 1000,

  withCredentials: false, // default

  auth: {
    username: 'janedoe',
    password: 's00pers3cret',
  },

  responseType: 'text', // default

  // `xsrfCookieName` is the name of the cookie to use as a value for xsrf token
  xsrfCookieName: 'XSRF-TOKEN', // default

  // `xsrfHeaderName` is the name of the http header that carries the xsrf token value
  xsrfHeaderName: 'X-XSRF-TOKEN', // default

  onUploadProgress: function (progressEvent) {
    // Do whatever you want with the native progress event
  },

  // `onDownloadProgress` allows handling of progress events for downloads
  onDownloadProgress: function (progressEvent) {
    // Do whatever you want with the native progress event
  },

  // `maxContentLength` defines the max size of the http response content allowed
  maxContentLength: 2000,

  validateStatus: function (status) {
    return status >= 200 && status < 300 // default
  },
}

axios.get('/Example', a).catch(function (error) {
  console.log(error)
}).then(function (response) {
  console.log('yeeeeea')
  console.log(response)
})
