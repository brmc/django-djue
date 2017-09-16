import T from '../views/T.vue'
import ExampleCreateView from '../views/ExampleCreateView.vue'
import ExampleDeleteView from '../views/ExampleDeleteView.vue'
import ExampleDetailView from '../views/ExampleDetailView.vue'
import ExampleUpdateView from '../views/ExampleUpdateView.vue'
import ExampleListView from '../views/ExampleListView.vue'

export default [{
  path: '',
  name: 'app',
  children: [{
    path: '/?',
    component: T,
  }, {
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
