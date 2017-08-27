import index from '../views/admin/index.js'
import login from '../views/admin/login.js'
import logout from '../views/admin/logout.js'
import passwordChange from '../views/admin/passwordChange.js'
import passwordChangeDone from '../views/admin/passwordChangeDone.js'
import i18nJavascript from '../views/admin/i18nJavascript.js'
import shortcut from '../views/admin/shortcut.js'

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
