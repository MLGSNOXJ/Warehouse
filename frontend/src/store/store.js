import { createStore } from 'vuex';

const store = createStore({
  state: {
    employeeId: null, // Добавляем employeeId
    token: null,
  },
  mutations: {
    setEmployeeId(state, employeeId) {
      console.log('Установка employeeId в Vuex:', employeeId); // Отладка
      state.employeeId = employeeId;
    },
    setToken(state, token) {
      console.log('Установка токена в Vuex:', token); // Отладка
      state.token = token;
    },
  },
  actions: {
    authenticate({ commit }, { employeeId, token }) {
      commit('setEmployeeId', employeeId);
      commit('setToken', token);
    },
  },
});

export default store;
