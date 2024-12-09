<template>
    <!-- Top bar with user info, settings, and cart -->
<div class="top-bar">
  <div class="profile-section" @click="toggleMenu">
    <span class="username">{{ username }}</span>
    <img :src="imgSource" alt="User Profile" class="profile-image" />
  </div>

  <button class="settings-button" @click="openSettings">
    <div class="icon-container">
      <img class="ellipse" :src="require('./assets/shapka/Ellipse.svg')" alt="Ellipse Icon" />
      <img class="vector" :src="require('./assets/shapka/Vector.svg')" alt="Vector Icon" />
    </div>
  </button>
    
    <button @click="$router.push('/basket')" class="cart-button">
      <img class="vector" :src="require('./assets/shapka/basket.svg')" alt="Basket Icon" />
      <!-- Кружочек с количеством товаров в левом верхнем углу -->
      <span v-if="cartItemCount > 0" class="cart-count">{{ cartItemCount }}</span>
    </button>
</div>
      <!-- Sidebar Menu -->
    <div class="dashboard-container">
      
      <div class="sidebar">
        <nav class="menu">
          <!-- Transparent container for the name and buttons -->
        <div class="transparent-container">
          <div class="indrive-container">
            <!-- Container for name and images -->
            <div class="content-container">
              <!-- Name box -->
              <div class="namebox">
                <img class="text" :src="require('./assets/InDrive.svg')" alt="indrive">
              </div>
              <!-- Arrow images -->
              <div class="image-container">
                <div class="imagine">
                  <img class="imagine1" :src="require('./assets/strelka.svg')" alt="indrive" @click="toggleSidebar">
                  <img class="imagine1" :src="require('./assets/strelka.svg')" alt="indrive" @click="toggleSidebar">
                </div>
              </div>
            </div>
          </div>
          <div>
            <img class="line" :src="require('./assets/line.svg')" alt="indrive" @click="toggleSidebar">
          </div>
            <!-- Общий контейнер для кнопок управления -->
            <div class="control-buttons-container">
              <ul class="menu-items">
                <!-- Обернутые кнопки -->
                <li class="button-container" v-if="isLoggedIn">
                  <button @click="$router.push('/check_product')" class="svg-button">
                    <div class = "button-img">
                    <!-- SVG, который будет виден по умолчанию -->
                    <div class = "icon-img">
                      <img class = "default-svg" :src="require('./assets/spimglight.svg')" alt="indrive" @click="toggleSidebar">
                      <img class = "hover-svg" :src="require('./assets/spimgdark.svg')" alt="indrive" @click="toggleSidebar">                    
                  </div>
                  <div class = "text-img">
                    <img class = "default-svg" :src="require('./assets/splight.svg')" alt="indrive" @click="toggleSidebar">
                    <img class = "hover-svg" :src="require('./assets/spdark.svg')" alt="indrive" @click="toggleSidebar">
                  </div>
                </div>
                  </button>
              </li>
                <li class="button-container" v-if="isLoggedIn">
                  <button @click="$router.push('/add_product')" class = "svg-button">
                    <div class = "button-img">
                    <div class = "icon-img">
                      <img class = "default-svg" :src="require('./assets/dpimglight.svg')" alt="indrive" @click="toggleSidebar">
                      <img class = "hover-svg" :src="require('./assets/dpimgdark.svg')" alt="indrive" @click="toggleSidebar">
                  </div>
                  <div class = "text-img">
                    <img class = "default-svg" :src="require('./assets/dplight.svg')" alt="indrive" @click="toggleSidebar">
                    <img class = "hover-svg" :src="require('./assets/dpdark.svg')" alt="indrive" @click="toggleSidebar">
                  </div>
                </div>
                  </button>
                </li>
                <li class="button-container">
                  <button @click="$router.push('/')" class = "svg-button">
                    <div class = "button-img">
                    <div class = "icon-img">                   
                      <img class = "default-svg" :src="require('./assets/himglight.svg')" alt="indrive" @click="toggleSidebar">
                      <img class = "hover-svg" :src="require('./assets/himgdark.svg')" alt="indrive" @click="toggleSidebar">                   
                  </div>
                  <div class = "text-img">              
                    <img class = "default-svg" :src="require('./assets/hlight.svg')" alt="indrive" @click="toggleSidebar">
                    <img class = "hover-svg" :src="require('./assets/hdark.svg')" alt="indrive" @click="toggleSidebar">
                  </div>
                </div>
                  </button>
                </li>
                <li class="button-container" v-if="isLoggedIn">
                  <button @click="$router.push('/userlist')" class = "svg-button">
                    <div class = "button-img">
                    <div class = "icon-img">                
                      <img class = "default-svg" :src="require('./assets/sotimglight.svg')" alt="indrive" @click="toggleSidebar">
                      <img class = "hover-svg" :src="require('./assets/sotimgdark.svg')" alt="indrive" @click="toggleSidebar">    
                  </div>
                  <div class = "text-img">
                    <img class = "default-svg" :src="require('./assets/sotlight.svg')" alt="indrive" @click="toggleSidebar">
                    <img class = "hover-svg" :src="require('./assets/sotdark.svg')" alt="indrive" @click="toggleSidebar">     
                  </div>
                </div>
                  </button>
                </li>
                <li class="button-container" v-if="isLoggedIn">
                  <button @click="$router.push('/basket')" class = "svg-button">
                    <div class = "button-img">
                    <div class = "icon-img">                  
                      <img class = "default-svg" :src="require('./assets/korimglight.svg')" alt="indrive" @click="toggleSidebar">
                      <img class = "hover-svg" :src="require('./assets/korimgdark.svg')" alt="indrive" @click="toggleSidebar">                
                  </div>
                  <div class = "text-img">
                    <img class = "default-svg" :src="require('./assets/korlight.svg')" alt="indrive" @click="toggleSidebar">
                    <img class = "hover-svg" :src="require('./assets/kordark.svg')" alt="indrive" @click="toggleSidebar">                   
                  </div>
                </div>
                  </button>
                </li>
              </ul>
            </div>
          </div>

          
        </nav>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>

     <!-- Dropdown Menu -->
  <transition name="fade">
    <div v-if="showMenu" class="dropdown-menu">
      <div class="dropdown-header">
        <img :src="imgSource" class="dropdown-profile-image" />
        <div class="dropdown-info">
          <p class="dropdown-username">{{ username }}</p>
          <p class="dropdown-position">{{ position }}</p>
        </div>
      </div>
      <router-link to="/lk" class="menu-link">Личный кабинет</router-link>
      <button @click="logout" class="logout-button">Выйти из аккаунта</button>
    </div>
  </transition>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      showMenu: false, // Управляет показом выпадающего меню
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
        acceptTerms: false
      },
      username: '', // Имя пользователя
      position: '', // Позиция пользователя
      imgSource: 'https://via.placeholder.com/50', // Фото пользователя по умолчанию
      userId: null,  // ID пользователя
      theme: 'theme-light', // Тема: светлая или темная
      themeIcon: 'path/to/light-theme-icon.png', // Иконка для светлой темы
      isCollapsed: false,

      cart: [], // Корзина с товарами (каждый элемент — это вид товара)
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('access_token') || localStorage.getItem('guest') === 'true';
    },
    cartItemCount() {
    // Количество видов товаров в корзине
    return this.cart.length;
    }
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu; // Открытие/закрытие меню
    },
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('guest');

      // Сбрасываем данные пользователя
      this.username = '';
      this.position = '';
      this.imgSource = 'https://via.placeholder.com/50';
      this.userId = null;

      // Скрываем меню, если оно открыто
      this.showMenu = false;

      // Перенаправляем на страницу HomePage
      this.$router.push('/');
    },
    showForm(formType) {
      this.currentForm = formType;
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed; // Toggle collapsed state
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
          this.username = user.FIO; // Имя пользователя
          this.position = user.post; // Позиция пользователя
          this.userId = user.id; // Устанавливаем ID пользователя
          this.loadUserPhoto(user.id); // Загружаем фото пользователя
        } catch (error) {
          console.error('Ошибка при загрузке данных пользователя:', error);
        }
      }
    },
    async loadUserPhoto(userId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:8000/employees/${userId}/photo/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          responseType: 'blob',
        });

        if (response.data) {
          this.imgSource = URL.createObjectURL(response.data); // Устанавливаем фото пользователя
        }
      } catch (error) {
        console.error('Ошибка при загрузке фото пользователя:', error);
      }
    },
    async fetchCartItems() {
      try {
        // Предполагаем, что есть пользователь с определенным employee_id
        const employeeId = 1; // Замените на реальный идентификатор пользователя
        const response = await axios.get(`http://localhost:8000/cart?employee_id=${employeeId}`);
        this.cart = response.data;
      } catch (error) {
        console.error("Ошибка при получении корзины:", error);
      }
    },
    openSettings() {
      // Логика открытия страницы настроек
      alert('Открыть настройки');
    },
    openCart() {
      // Логика открытия корзины
      alert('Открыть корзину');
    },
    addTestItem() {
      // Добавляем тестовый товар в корзину
      this.cart.push({
        id: this.cart.length + 1,
        name: `Товар ${this.cart.length + 1}`
      });
    },
    addToCart(item) {
    // Проверяем, если товар уже есть в корзине
    const existingItem = this.cart.find(cartItem => cartItem.id === item.id);
    if (!existingItem) {
      // Если товара ещё нет в корзине, добавляем его
      this.cart.push(item);
    }
  }
  },
  mounted() {
    this.loadUserProfile(); // Загрузка профиля при монтировании компонента
    this.fetchCartItems();
  },
};
</script>




<style scoped>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

/* Основные стили */
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

.dashboard-container {
  display: flex;
}
/* Боковое меню */
.sidebar {
  position: fixed;
  width: 258px;
  height: 100vh;
  top: 0px;
  border-right: 1px;
  gap: 15px;
  background-color: #ffffff
}

.line{
margin-top: 18px;
margin-bottom: -18px;
}
/* Основные стили */
.transparent-container {
  width: 228px; /* Fixed width */
  height: auto; /* Hug */
  min-height: 395px; /* Минимальная высота */
  gap: 18px;
  opacity: 1; /* Сделано видимым */

  padding-top: 22px;
  padding-right: 10px;
  padding-bottom: 20px;
  padding-left: 16px;
}

/* Контейнер для текста и изображений */
.content-container {
  width: auto; /* Hug */
  height: auto; /* Hug */
  min-height: 48px; /* Минимальная высота */
  gap: 0px;
  opacity: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Контейнер для текста */
.namebox {
  width: 180px; /* Fixed */
  height: 48px; /* Fixed */
  gap: 0px;
  opacity: 1;
  
}

.text {
  display: flex;
  margin-top: 12px;
 
  gap: 10px;
  opacity: 1;
  
}

/* Текст */
.indrive-text {
  width: 175px; /* Fixed */
  height: 28px; /* Fixed */
  font-family: 'Montserrat';
  font-size: 24px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
  color: #3D495B;
  opacity: 1;
  margin: 0;
}

/* Контейнер для изображений */
.image-container {
  display: flex;
  flex-direction: row;
  width: 48px; /* Hug */
  height: 48px  ; /* Hug */
  gap: 0px; /* Убираем расстояние между изображениями */
  opacity: 1;
  
}
.imagine{
  display: flex;
  width: 24px;
  height: 24px;
  gap: 0px;
  opacity: 0px;
  margin-top: 12px;
  margin-bottom:12px;
  margin-left: 12px;
  margin-right: 12px;
  justify-content: center; /* Выравнивание по горизонтали */
  align-items: center;     /* Выравнивание по вертикали */
  
}
.imagine1{
gap: 0px;
border: 2px 0px 0px 0px;
opacity: 0px;
margin: 0;
}

.menu ul li button:hover {
  background-color: #3D495B;
  color: white;
}

.svg-button {
  position: relative;
}


.default-svg {
  display: inline-block;
}

.hover-svg {
  display: none;
}

.svg-button:hover .default-svg {
  display: none;
}

.svg-button:hover .hover-svg {
  display: inline-block;
}

/* Контейнер для кнопок управления */
.control-buttons-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0px;
  gap: 18px;
  width: 228px;
  height: auto;
  flex: none;
  order: 2;
  flex-grow: 0;
}

/* Контейнер для каждой кнопки */
.button-container {
  display: flex;
  width: 228px;
  height: 46px;
  gap: 0px;
  opacity: 0px;
  
}
.top-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 10px;
  gap: 20px; /* Ensures 20px space between all elements including profile and settings */
  margin-right: 22px;
  position: fixed; /* Fix the top bar */
  top: 0;
  right: 0; /* Align the top bar to the right edge */
  z-index: 1000;
  height: 60px;
  width: 30%; /* Set top bar width to 30% of the screen */
}

.profile-section {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 20px; /* Ensures 20px gap between username and profile image */
}

.profile-image {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  
}

.username { 
  gap: 0px;
  font-family: "PT Sans", "Arial", sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 20px;
  text-align: left;
  color: #121212; /* Dark background */
}


.settings-button, .cart-button {
  width: 48px;
  height: 48px;
  background: #3D495B;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 1;
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.ellipse {
  width: 10px;
  height: 10px;
  position: fixed;
}

.vector {
  width: 22px;
  height: 22px;
}

.cart-button {
  position: relative;
  width: 48px;
  height: 48px;
  background: #3D495B;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}




.settings-button{
  margin-left: -10px;
}


/* Dropdown Menu Styles */
.dropdown-menu {
  position: absolute;
  top: 60px;
  right: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  z-index: 1000;
  width: 250px;
}

.dropdown-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: rgb(243, 233, 57);
}

.dropdown-profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.dropdown-info {
  flex-grow: 1;
}

.dropdown-username {
  font-weight: bold;
}

.dropdown-position {
  font-size: 0.9em;
}

.menu-link, .logout-button {
  display: block;
  padding: 15px;
  text-align: left;
  width: 100%;
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.logout-button:hover, .menu-link:hover {
  background-color: #f1f1f1;
}
.button-container button {
  width: 100%;
  height: 100%;
  background-color: transparent;
  border: none;
  color: #FFFFFF;
  font-family: 'Montserrat', sans-serif;
  font-size: 16px;
  text-align: left;
  cursor: pointer;
}

.button-container button:hover {
  background-color: #276AED;
  border-radius: 8px;
}

.button-img{
  display: flex;
  align-items: center;
  margin-top: -3px;
  width: 144px;
  height: 30px;
  gap: 10px;
  opacity: 0px;
  

}
.icon-img{
  display: flex;
  width: 24px;
height: 24px;
gap: 0px;
opacity: 0px;

}
.text-img{
  display: flex;
  width: 120px;
height: 30px;
gap: 10px;
opacity: 0px;

  
}

.cart-button {
  position: relative; /* Чтобы разместить кружочек поверх кнопки */
  width: 48px;
  height: 48px;
  background: #3D495B;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cart-count {
  position: absolute;
  top: -5px; /* Смещаем кружок вверх */
  right: -5px; /* Смещаем кружок вправо */
  background-color: #BCED0A; /* Цвет кружка */
  color: #3D495B;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
  font-family: Calibri;
  line-height: 20px; /* Чтобы текст был по центру */
}

/* Основной контент */
.main-content {
  margin-left: 268px; /* Совпадает с шириной sidebar */
    padding: 20px;
    width: calc(100% - 268px);
    transition: background-color 0.5s ease;
    min-height: 100vh; /* Обеспечивает, что контент занимает всю высоту окна */
    box-sizing: border-box;
}
/* Прочие стили (сохранены как есть) */
.logo-image {
  height: 50px;
}

.profile-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}



.profile-pic-container {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 10px;
}

.profile-pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-id {
  font-family: 'Arial', serif;
  color: #f1f1f1;
  margin-bottom: 20px;
  text-align: center;
}

.user-id span {
  color: #f1f1f1; /* Цвет текста ID и имени для светлой темы */
}

 
.menu ul {
  list-style-type: none;
  padding: 0;
}

.menu ul li {
  margin: 15px 0;
}

.menu ul li button {
  background: none;
  border: none;
  color: #3D495B;
  cursor: pointer;
  text-align: left;
  font-size: 16px;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
}


/* Dropdown Menu */
.dropdown-menu {
  position: fixed;
  top: 84px;
  right: 620px;
  background: rgb(246, 164, 0);
  color: rgb(255, 255, 255);
  font-family: 'Arial', sans-serif;
  border-radius: 8px;
  z-index: 1000;
  width: 250px;
}


.dropdown-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: rgb(243, 233, 57);
}

.dropdown-profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.dropdown-info {
  flex-grow: 1;
}

.dropdown-username {
  font-weight: bold;
  margin: 0;
}

.dropdown-position {
  font-size: 0.9em;
  color:rgb(246,164,0);
  font-family: 'Arial', sans-serif;
  margin: 0;
}

.menu-link {
  display: block;
  padding: 15px;
  color: rgb(255, 255, 255);
  font-family: 'Arial', sans-serif;
  text-decoration: none;
  transition: background-color 0.3s;
}

.menu-link:hover {
  background-color: rgb(246,164,0);
}

.logout-button {
  display: block;
  width: 100%;
  color: rgb(255, 255, 255);
  background-color: red;
  border: none;
  padding: 15px;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.3s;  
}

.logout-button:hover {
  font-family: 'Arial', sans-serif;
  background-color: rgb(246,164,0);
}

/* Modal Styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.main-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 300px;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.popup-header ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.popup-header li {
  margin-right: 20px;
}

.popup-header a {
  text-decoration: none;
  color: black;
  font-weight: bold;
}

.popup-header li.active a {
  color: #fd6a02;
}

.popup-content {
  padding-top: 10px;
}

.form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form .input-field {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form .checkbox {
  margin-right: 5px;
}

.form .submit-button {
  width: 100%;
  padding: 10px;
  background-color: #fd6a02;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.form .submit-button:hover {
  background-color: #e05a02;
}

.close-button {
  font-size: 20px;
  cursor: pointer;
}

/* Transition Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* одно и то же, что и fade-leave-active в версии ниже 2.1.8 */ {
  opacity: 0;
}


</style>
