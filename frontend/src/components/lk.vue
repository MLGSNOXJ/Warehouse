<template>
  <div class="main_container">
    <div class="dashboard-container">
      <div class="main-content">
        <!-- Блок личных данных -->
        <div class="card personal-data">
          <h2>Личные данные</h2>
          <input type="text" placeholder="Имя" v-model="username" />
          <input type="text" placeholder="Фамилия" v-model="surname" />
          <input type="text" placeholder="Должность" v-model="post" />
          <input type="email" placeholder="Почта" v-model="email" />
          <input type="text" placeholder="Телефон" v-model="phone" />
          <button @click="saveUserProfile">Сохранить</button>
          <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        </div>

        <!-- Блок добавления фото -->
        <div class="card add-photo">
          <h2>Добавить фото</h2>
          <div class="photo-preview-container">
            <img :src="imgSource" class="photo-preview" alt="Uploaded Photo" />
          </div>
          <input type="file" @change="onFileChange" class="file-input" />
          <button @click="saveUserProfile">Загрузить фото</button>
        </div>

        <!-- Блок безопасности -->
        <div class="card settings">
          <h2>Безопасность</h2>
          <input type="password" placeholder="Введите старый пароль" v-model="oldPassword" />
          <input type="password" placeholder="Введите новый пароль" v-model="newPassword" />    
          <button @click="savePassword">Сохранить</button>
          <p v-if="successMessage_1" class="success-message">{{ successMessage_1 }}</p>
        </div>

        <!-- Таблица продуктов -->
        <div class="card product">
          <h2>Продукты</h2>
          <button @click="openTransferModal">Передать продукты</button>
          <div class="content">
            <table class="product-table">
              <thead>
                <tr>
                  <th>Название</th>
                  <th>Производитель</th>
                  <th>Артикул (п)</th>
                  <th>Артикул (в)</th>
                  <th>Цена</th>
                  <th>Заводской номер</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in products" :key="product.id">
                  <td>{{ product.name }}</td>
                  <td>{{ product.manufacturer }}</td>
                  <td>{{ product.article_p }}</td>
                  <td>{{ product.article_v }}</td>
                  <td>{{ product.cost }} руб.</td>
                  <td>{{ product.factory_number }}</td>
                </tr>
              </tbody>
            </table>
            <p v-if="products.length === 0">Нет доступных продуктов.</p>
          </div>
        </div>
        <!-- Модальное окно -->
        <div v-if="showModal" class="modal">
          <div class="modal-content">
            <span class="close" @click="showModal = false">&times;</span>
            <h2>Передать продукты</h2>
            <div>
              <label for="employeeSelect">Выберите сотрудника:</label>
              <select id="employeeSelect" v-model="selectedEmployee">
                <option value="" disabled>Выберите сотрудника</option> <!-- Убирает пустоту по умолчанию -->
                <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                  {{ employee.FIO }}
                </option>
              </select>
            </div>
            <div>
              <label for="productSelect">Выберите продукт:</label>
              <select id="productSelect" v-model="selectedProduct">
                <option v-for="product in products" :key="product.id" :value="product.id">
                  {{ product.name }}
                </option>
                <option value="all">Все</option>
              </select>
            </div>
            <button @click="transferProducts">Передать</button>
            <p v-if="modalMessage" class="success-message">{{ modalMessage }}</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'Lk',
  data() {
    return {
      userId: null,
      username: '',
      surname: '',
      post: '',
      email: '',
      phone: '',
      photo: null,
      imgSource: 'https://via.placeholder.com/150',
      successMessage: '',
      successMessage_1: '',
      oldPassword: '',
      newPassword: '',
      products: [],
      showModal: false,
      employees: [], // Список сотрудников
      selectedEmployee: null,
      selectedProduct: null,
      modalMessage: '',
    };
  },
  methods: {
    async loadUserProfile() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/employees/user-employee/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const user = response.data;
        this.userId = user.id;
        this.username = user.FIO;
        this.surname = user.surname; // Не забудьте добавить это поле, если оно у вас есть
        this.post = user.post;
        this.email = user.email;
        this.phone = user.phone;
        this.loadUserPhoto(user.id);
        this.loadUserProducts(user.id);
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя:', error);
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
          this.imgSource = URL.createObjectURL(response.data);
        }
      } catch (error) {
        console.error('Ошибка при загрузке фото пользователя:', error);
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      this.photo = file;
      this.imgSource = URL.createObjectURL(file);
    },
    async loadUserProducts(userId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:8000/products/employee/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.products = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке продуктов пользователя:', error);
        if (error.response && error.response.status === 404) {
          this.products = [];
        }
      }
    },
    async saveUserProfile() {
      try {
        const token = localStorage.getItem('access_token');
        const formData = new FormData();
        formData.append('FIO', this.username);
        formData.append('surname', this.surname); // Обновите это поле
        formData.append('post', this.post);
        formData.append('email', this.email);
        formData.append('phone', this.phone);
        if (this.photo) {
          formData.append('photo', this.photo);
        }

        await axios.put(`http://localhost:8000/employees/${this.userId}`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        });

        this.loadUserProfile();
        this.successMessage = 'Данные пользователя успешно сохранены';
      } catch (error) {
        console.error('Ошибка при сохранении данных пользователя:', error);
        this.successMessage = 'Ошибка при сохранении данных пользователя';
      }
    },
    async savePassword() {
  try {
    const token = localStorage.getItem('access_token');
    const payload = {
      old_password: this.oldPassword,
      new_password: this.newPassword,
    };
    
    console.log('Sending payload:', payload);  // Логирование отправляемого payload

    const response = await axios.put(`http://localhost:8000/users/change-password/${this.userId}`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    
    console.log('Password change response:', response.data); // Логирование ответа

    this.successMessage_1 = 'Пароль успешно изменен';
    this.oldPassword = '';
    this.newPassword = '';
  } catch (error) {
    console.error('Ошибка при изменении пароля:', error);

    if (error.response && error.response.data) {
      console.error('Server response:', error.response.data); // Логирование ошибки сервера
      this.successMessage_1 = `Ошибка: ${error.response.data.detail || 'Не удалось изменить пароль'}`;
    } else {
      this.successMessage_1 = 'Ошибка при изменении пароля';
    }
  }
},
    async loadEmployees() {
      try {
        const response = await axios.get('http://localhost:8000/employees/');
        this.employees = response.data;
        console.log('Employees loaded:', this.employees); // Добавьте логирование
      } catch (error) {
        console.error('Ошибка при получении сотрудников:', error);
      }
    },
    openTransferModal() {
      this.showModal = true;
      this.loadEmployees(); // Загрузка списка сотрудников при открытии модального окна
    },
    async transferProducts() {
  try {
    const token = localStorage.getItem('access_token');
    const url = `http://localhost:8000/products/transfer-products/`;
    const formData = new FormData();
    formData.append('from_employee_id', this.userId); // ID текущего сотрудника
    formData.append('to_employee_id', this.selectedEmployee);

    if (this.selectedProduct === 'all') {
      // Передача всех продуктов
      await axios.put(url, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      this.modalMessage = 'Все продукты успешно переданы';
    } else {
      // Передача одного продукта
      const productUrl = `http://localhost:8000/products/transfer-product/`;
      formData.append('product_id', this.selectedProduct);

      await axios.put(productUrl, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      this.modalMessage = 'Продукт успешно передан';
    }
    
    this.showModal = false;
  } catch (error) {
    console.error('Ошибка при передаче продуктов:', error);
    this.modalMessage = 'Ошибка при передаче продуктов';
  }
},
  },
  mounted() {
    this.loadUserProfile();
    this.loadEmployees();
  },
};
</script>


<style scoped>


body {
  background-color: rgb(41, 52, 70);
  color: #fffefe;
  font-family: 'Arial', serif;
  margin: 0;
  padding: 20px 0 0 0;
}

.dashboard-container {
  display: flex;
  height: calc(100vh - 20px);
  padding-top: 70px;
}

.sidebar {
  margin-top: 84px;
  position: fixed; /*  Закрепляем блок на экране */
  top: 0;
  left: 0;
  width: 250px;
  height: 100%; /* Занимает всю высоту экрана */
  background-color: rgb(41, 52, 70);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto; /* Добавляем вертикальную прокрутку, если контент превышает высоту экрана */
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

.menu ul {
  list-style-type: none;
  padding: 0;
}

.menu ul li {
  margin: 15px 0;
}

.menu ul li a {
  color: #ddd;
  text-decoration: none;
}

.main-content {
  margin-top: -30px;
  margin-left: 165px; /* Добавляем отступ слева, чтобы освободить место для фиксированного блока */
  padding: 0px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: auto;
  gap: 20px;
}

.card {
  background-color: rgb(41, 52, 70);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Set the personal-data block to span two columns */
.personal-data {
  grid-column: span 2;
}

/* Adjust add-photo block to be one column */
.add-photo {
  grid-column: span 1;
}

.product, .investments {
  grid-column: span 2;
}

.product ul {
  padding: 0;
  list-style: none;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  color: #fff;
  font-size: 14px;
}

.product-table th,
.product-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.product-table th {
  background-color: #f6a400;
  color: white;
  text-align: left;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
  border-radius: 10px;
  text-align: center;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #7a7979;
  background-color: rgb(37, 47, 61);
  color: #fff;
}


h2 {
  font-family: 'Arial', serif;
  font-size: 24px;
  text-align: center;
  color: #f6a400;
  margin-bottom: 20px;
}

input, button {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: none;
  box-sizing: border-box;
}

input {
  background-color: rgb(37, 47, 61);
  color: #fff;
  border: 1px solid #7a7979;
}

button {
  background-color: #f6a400;
  color: white;
  cursor: pointer;
  font-family: 'Arial', sans-serif;
}

button:hover {
  background-color: #45a049;
}

.success-message {
  color: #4CAF50;
  margin-top: 10px;
  text-align: center;
}

.photo-preview-container {
  width: 100%;
  height: 200px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(37, 47, 61);
  border-radius: 10px;
}

.photo-preview {
  max-width: 100%;
  max-height: 100%;
  border-radius: 10px;
  object-fit: contain;
}
</style>
