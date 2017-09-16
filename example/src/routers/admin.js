import index from '../views/index.vue'
import login from '../views/login.vue'
import logout from '../views/logout.vue'
import passwordChange from '../views/passwordChange.vue'
import passwordChangeDone from '../views/passwordChangeDone.vue'
import i18nJavascript from '../views/i18nJavascript.vue'
import shortcut from '../views/shortcut.vue'

export default [{
  path: 'admin/',
  name: 'admin',
  children: [{
    path: '',
    component: index,
    name: 'index',
  }, {
    path: 'login/',
    component: login,
    name: 'login',
  }, {
    path: 'logout/',
    component: logout,
    name: 'logout',
  }, {
    path: 'password_change/',
    component: passwordChange,
    name: 'password_change',
  }, {
    path: 'password_change/done/',
    component: passwordChangeDone,
    name: 'password_change_done',
  }, {
    path: 'jsi18n/',
    component: i18nJavascript,
    name: 'jsi18n',
  }, {
    path: 'r/:content_type_id/:object_id/',
    component: shortcut,
    name: 'view_on_site',
  }, ]
}];
