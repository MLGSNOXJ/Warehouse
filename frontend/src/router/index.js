import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import lk from '../components/lk.vue';
import AddProduct from '../components/AddProduct.vue';
import CheckProduct from '../components/CheckProduct.vue';
import UserList from '@/components/UserList.vue';
import UserDetail from '@/components/UserDetail.vue';
import basket from '@/components/basket.vue';

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/lk', name: 'Lk', component: lk, meta: { requiresAuth: true } },
  { path: '/add_product', name: 'AddProduct', component: AddProduct },
  { path: '/check_product', name: 'CheckProduct', component: CheckProduct },
  { path: '/userlist', name: 'UserList', component: UserList },
  { path: '/user/:id', name: 'UserDetail', component: UserDetail, props: true },
  { path: '/basket', name: 'basket', component: basket, props: true },
  { path: '/:pathMatch(.*)*', redirect: '/' } // Добавляем маршрут для 404
];

const router = createRouter({
  history: createWebHashHistory(), // Меняем на hash режим
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!localStorage.getItem('access_token')) {
      next({ path: '/login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
