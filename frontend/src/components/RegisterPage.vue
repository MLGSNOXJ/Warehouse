<template>
  <div>
    <!-- Шапка -->
    <header class="header">
      <button @click="$router.push('/')">На главную</button>
    </header>

    <!-- Основное содержимое -->
    <div class="form-container">
      <h1>Регистрация</h1>
      <input type="text" v-model="username" placeholder="Имя пользователя">
      <input type="password" v-model="password" placeholder="Пароль">
      <input type="email" v-model="email" placeholder="Email">
      <button @click="register" class="btn btn-primary">Зарегистрироваться</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: ''
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('http://localhost:8000/register', {
          username: this.username,
          password: this.password,
          email: this.email
        });
        alert('Регистрация успешна. Теперь вы можете войти.');
        this.$router.push('/login');
      } catch (error) {
        console.error('Ошибка регистрации:', error);
        alert('Ошибка регистрации. Пожалуйста, попробуйте еще раз.');
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
