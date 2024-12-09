<template>
  <div class="main_container">
    <div class="dashboard-container">
      
      <div class="main-content">
        <!-- Блок личных данных -->
        <div class="card personal-data" v-if="user">
          <h2>Личные данные</h2>
          <input type="text" placeholder="Имя" v-model="user.name" />
          <input type="text" placeholder="Фамилия" v-model="user.lastname" />
          <input type="text" placeholder="Должность" v-model="user.position" />
          <input type="email" placeholder="Почта" v-model="user.email" />
          <input type="text" placeholder="Телефон" v-model="user.phone" />
        </div>
        <!-- Таблица продуктов -->
        <div class="card product">
          <h2>Продукты</h2>
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
      </div>
    </div>
  </div>

  
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDetail',
  data() {
    return {
      user: null,
      products: [],
    };
  },
  async created() {
    await this.fetchUser();
    await this.fetchUserProducts();
  },
  methods: {
    async fetchUser() {
      const userId = this.$route.params.id;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:8000/employees/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const userData = response.data;
        this.user = {
          id: userData.id,
          name: userData.FIO,
          lastname: userData.lastname,
          position: userData.post,
          photoUrl: `http://localhost:8000/employees/${userData.id}/photo`,
          email: userData.email,
          phone: userData.phone,
        };
      } catch (error) {
        console.error('Ошибка при загрузке информации о сотруднике:', error);
      }
    },
    async fetchUserProducts() {
      const userId = this.$route.params.id;
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
    async updateUser() {
      const userId = this.$route.params.id;
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(`http://localhost:8000/employees/${userId}`, this.user, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        alert('Данные успешно обновлены!');
      } catch (error) {
        console.error('Ошибка при обновлении информации о сотруднике:', error);
      }
    },
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

