<template>
  <div class="main-container">

    <!-- Overlay -->
    <transition name="fade">
      <div v-if="showModal" class="overlay" @click="closeModal"></div>
    </transition>

    <!-- Sign-In / Register Modal -->
    <transition name="fade">
      <div v-if="showModal" class="main-popup">
        <div class="popup-header">
          <div id="popup-close-button" @click="closeModal" class="close-button">&times;</div>
          <ul>
            <li :class="{ active: currentForm === 'signIn' }"><a href="#" @click="showForm('signIn')">Войти</a></li>
            <li :class="{ active: currentForm === 'register' || currentForm === 'employeeInfo' }">
              <a href="#" @click="showForm('employeeInfo')">Регистрация</a>
            </li>
          </ul>
        </div>
        <div class="popup-content">
          <!-- Sign-In Form -->
          <form v-if="currentForm === 'signIn'" @submit.prevent="signIn" class="form">
            <label for="username">Никнейм:</label>
            <input type="text" id="username" v-model="signInData.username" placeholder="Имя пользователя" class="input-field"/>
            <label for="password">Пароль:</label>
            <input type="password" id="password" v-model="signInData.password" placeholder="Пароль" class="input-field"/>
            <p class="check-mark">
              <input type="checkbox" id="remember-me" v-model="signInData.rememberMe" class="checkbox"/>
              <label for="remember-me">Запомнить меня</label>
            </p>
            <input type="submit" id="submit" value="Войти" class="submit-button"/>
          </form>

          <!-- Employee Info Form -->
          <form v-if="currentForm === 'employeeInfo'" @submit.prevent="submitEmployeeInfo" class="form">
            <label for="employee-name">Имя:</label>
            <input type="text" id="employee-name" v-model="employeeData.FIO" placeholder="Имя" class="input-field"/>
            <label for="employee-surname">Фамилия:</label>
            <input type="text" id="employee-surname" v-model="employeeData.surname" placeholder="Фамилия" class="input-field"/>
            <label for="employee-position">Должность:</label>
            <input type="text" id="employee-position" v-model="employeeData.post" placeholder="Должность" class="input-field"/>
            <input type="submit" id="submit" value="Далее" class="submit-button"/>
          </form>

          <!-- Register Form -->
          <form v-if="currentForm === 'register'" @submit.prevent="register" class="form">
            <label for="username-register">Никнейм:</label>
            <input type="text" id="username-register" v-model="registerData.username" placeholder="Имя пользователя" class="input-field"/>
            <label for="email-register">Электронная почта:</label>
            <input type="email" id="email-register" v-model="registerData.email" placeholder="Email" class="input-field"/>
            <label for="password-register">Пароль:</label>
            <input type="password" id="password-register" v-model="registerData.password" placeholder="Пароль" class="input-field"/>
            <label for="password-confirmation">Подтвердите пароль:</label>
            <input type="password" id="password-confirmation" v-model="registerData.passwordConfirmation" placeholder="Подтвердите пароль" class="input-field"/>
            <p class="check-mark">
              <input type="checkbox" id="accept-terms" v-model="registerData.acceptTerms" class="checkbox"/>
              <label for="accept-terms">Я согласен с <a href="#">условиями</a></label>
            </p>
            <input type="submit" id="submit" value="Создать аккаунт" class="submit-button"/>
          </form>
        </div>
      </div>
    </transition>

    <!-- Not Logged In Card -->
    <div class="content">
      <div v-if="!isLoggedIn" class="auth-card">
        <p class="auth-message">
            Вы не авторизованы. 
            <a href="#" @click="openModal" class="auth-link">Войти</a> или 
            <a href="#" @click="openModal" class="auth-link">Зарегистрироваться</a>
            <br>
            Или <a href="#" @click="continueAsGuest" class="auth-link">Продолжить как гость(Для того, чтобы работал вход в html)</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HeaderWithProfile',
  data() {
    return {
      showMenu: false,
      showModal: false,
      currentForm: 'signIn',
      signInData: {
        username: '',
        password: '',
        rememberMe: false
      },
      registerData: {
        username: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        acceptTerms: false,
        employee_id: null
      },
      employeeData: {
        FIO: '',
        surname: '',
        post: ''
      },
      username: '',
      position: '',
      imgSource: 'https://via.placeholder.com/50',
    };
  },
  computed: {
    computed: {
    isLoggedIn() {
        return !!localStorage.getItem('access_token') || localStorage.getItem('guest') === 'true';
    },
},
  },
  methods: {
    
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('employee_id'); // Удаляем ID из localStorage
    localStorage.removeItem('guest'); // Удаляем флаг гостя
    this.$router.push('/');
    window.location.reload();
},
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    showForm(formType) {
      this.currentForm = formType;
    },
    continueAsGuest() {
        // Устанавливаем флаг гостевого доступа
        localStorage.setItem('guest', 'true');
        // Опционально, устанавливаем данные пользователя по умолчанию
        this.username = 'Гость';
        this.position = '';
        // Перенаправляем пользователя на основную страницу сайта
        this.$router.push('/check_product').then(() => {
            window.location.reload();
        });
    },
    async signIn() {
  try {
    const response = await axios.post('http://localhost:8000/users/login', {
      username: this.signInData.username,
      password: this.signInData.password,
    });

    const { access_token, employee_id } = response.data;

    // Сохраняем в localStorage
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('employee_id', employee_id);

    // Сохраняем в Vuex
    this.$store.commit('setEmployeeId', employee_id);
    this.$store.commit('setToken', access_token);
    console.log('Успешный вход: employeeId', employee_id); // Отладка
    // Загружаем профиль
    await this.loadUserProfile();

    this.closeModal();
    this.$router.push('/check_product').then(() => window.location.reload());
  } catch (error) {
    console.error('Ошибка входа:', error);
    alert('Ошибка входа. Проверьте введенные данные.');
  }
},
    async submitEmployeeInfo() {
      try {
        const response = await axios.post('http://localhost:8000/employees/', {
          FIO: this.employeeData.FIO,
          surname: this.employeeData.surname,
          post: this.employeeData.post,
        });

        this.registerData.employee_id = response.data.id;
        this.showForm('register');
      } catch (error) {
        console.error('Ошибка создания сотрудника:', error);
        alert('Ошибка создания сотрудника. Пожалуйста, попробуйте еще раз.');
      }
    },
    async register() {
  try {
    if (this.registerData.password !== this.registerData.passwordConfirmation) {
      alert('Пароли не совпадают');
      return;
    }
    if (!this.registerData.acceptTerms) {
      alert('Необходимо согласие с условиями');
      return;
    }

    await axios.post('http://localhost:8000/users/register', {
      username: this.registerData.username,
      email: this.registerData.email,
      password: this.registerData.password,
      employee_id: this.registerData.employee_id
    });

    alert('Регистрация успешна. Теперь вы можете войти.');
    this.showForm('signIn');

    // После успешной регистрации перенаправляем на страницу с продуктами
    this.$router.push('/check_product').then(() => {
      window.location.reload();
    });
  } catch (error) {
    console.error('Ошибка регистрации:', error);
    alert('Ошибка регистрации. Пожалуйста, попробуйте еще раз.');
  }
},
    async loadUserProfile() {
  if (this.isLoggedIn) {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get('http://localhost:8000/employees/user-employee/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const user = response.data;
      this.username = user.FIO;
      this.position = user.post;
      if (user.photo) {
        this.imgSource = `http://localhost:8000/employees/${user.id}/photo/`;
      }
    } catch (error) {
      console.error('Ошибка при загрузке данных пользователя:', error);
    }
  }
},
  },
  mounted() {
    this.loadUserProfile();
  },
};
</script>

<style scoped>
/* Основные стили для контейнера и шапки */
.main-container {
  margin: 90px auto;
  font-family: 'Arial', sans-serif;
  color: #fff;
  background-color: #293446;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.dropdown-menu {
  position: absolute;
  right: 20px;
  top: 60px;
  background-color: #2b374e;
  border: 1px solid #1e2a3a;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 200px;
}

.dropdown-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.dropdown-profile-image {
  border-radius: 50%;
  height: 50px;
  width: 50px;
  margin-right: 10px;
}

.dropdown-info {
  flex: 1;
}

.dropdown-username {
  font-weight: bold;
  font-size: 16px;
}

.dropdown-position {
  font-size: 14px;
  color: #ddd;
}

.menu-link {
  display: block;
  margin: 10px 0;
  color: #f6a400;
  text-decoration: none;
}

.menu-link:hover {
  color: #ffc107;
}

.logout-button {
  background-color: #e03a3e;
  border: none;
  color: #fff;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 500;
}

.main-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #2b374e;
  padding: 40px;
  border-radius: 10px;
  z-index: 1000;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.popup-header {
  text-align: center;
  margin-bottom: 20px;
}

.popup-header ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
}

.popup-header ul li {
  margin: 0 10px;
}

.popup-header ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
}

.popup-header ul li.active a {
  color: #f6a400;
}

.popup-content {
  text-align: left;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.form {
  display: flex;
  flex-direction: column;
}

.input-field {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: #1e2a3a;
  color: #fff;
}

.input-field::placeholder {
  color: #ddd;
}

.submit-button {
  background-color: #f6a400;
  border: none;
  padding: 10px;
  color: #fff;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #ffca28;
}

.check-mark {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: #ddd;
}

.checkbox {
  margin-right: 5px;
}

.auth-card {
  background-color: #2b374e;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.auth-message {
  color: #ddd;
}

.auth-link {
  color: #f6a400;
  text-decoration: none;
  font-weight: bold;
}

.auth-link:hover {
  color: #ffc107;
}

/* Плавные переходы для анимаций */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
