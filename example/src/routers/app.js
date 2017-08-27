import ExampleCreateView from '../views/app/ExampleCreateView.js'
import ExampleDeleteView from '../views/app/ExampleDeleteView.js'
import ExampleDetailView from '../views/app/ExampleDetailView.js'
import ExampleUpdateView from '../views/app/ExampleUpdateView.js'
import ExampleListView from '../views/app/ExampleListView.js'

export default [{
  path: '',
  name: 'app',
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
