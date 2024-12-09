<template>
  <div>
    <!-- Шапка -->
    <header class="header">
      <button @click="$router.push('/')">На главную</button>
    </header>

    <!-- Основное содержимое -->
    <div class="form-container">
      <h1>Вход</h1>
      <input type="text" v-model="username" placeholder="Имя пользователя">
      <input type="password" v-model="password" placeholder="Пароль">
      <button @click="login" class="btn btn-primary">Войти</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/login', {
          username: this.username,
          password: this.password
        });
        // Предполагая, что сервер возвращает токен доступа
        localStorage.setItem('access_token', response.data.access_token);
        this.$router.push('/');
      } catch (error) {
        console.error('Ошибка входа:', error);
        alert('Ошибка входа. Проверьте введенные данные.');
      }
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: rgb(210, 210, 210);
}

.menu-btn {
  font-size: 20px;
}

.dropdown-menu {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 50px;
  right: 10px;
  background-color: rgb(210, 210, 210);
  border: 1px solid silver;
  border-radius: 3px;
  padding: 10px;
}

.dropdown-item {
  background: none;
  border: none;
  padding: 10px 15px;
  text-align: left;
  width: 100%;
  cursor: pointer;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

input {
  display: block;
  margin-bottom: 10px;
  border-radius: 3px;
  border: 1px solid silver;
  outline: none;
  padding: 10px 15px;
  background: rgb(210, 210, 210);
  color: gray;
  width: 100%;
  max-width: 300px;
}
</style>
