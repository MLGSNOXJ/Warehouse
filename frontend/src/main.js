import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store/store';

const app = createApp(App);
app.use(router);
app.use(store); // Регистрация Store
app.mount('#app');
