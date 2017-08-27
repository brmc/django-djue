import ExampleCreateView from '../views/default/ExampleCreateView.js'
import ExampleDeleteView from '../views/default/ExampleDeleteView.js'
import ExampleDetailView from '../views/default/ExampleDetailView.js'
import ExampleUpdateView from '../views/default/ExampleUpdateView.js'
import ExampleListView from '../views/default/ExampleListView.js'

export default [{
  path: '',
  name: 'default',
  children: [{
    path: 'Example/~create/',
    component: ExampleCreateView,
    name: 'Example_create',
  }, {
    path: 'Example/:pk/~delete/',
    component: ExampleDeleteView,
    name: 'Example_delete',
  }, {
    path: 'Example/:pk/',
    component: ExampleDetailView,
    name: 'Example_detail',
  }, {
    path: 'Example/:pk/~update/',
    component: ExampleUpdateView,
    name: 'Example_update',
  }, {
    path: 'Example/',
    component: ExampleListView,
    name: 'Example_list',
  }, ]
}];
