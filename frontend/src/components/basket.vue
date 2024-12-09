<template>
  <div class="basket">
    <h1>Your Basket</h1>
    <div class="employee-info" v-if="employeeId">
      <p><strong>Employee ID:</strong> {{ employeeId }}</p>
    </div>
    <div class="debug-info">
      <p>Employee ID: {{ employeeId || 'Not set' }}</p>
    </div>
    <div>
      <p>Cart Items:</p>
      <pre>{{ cartItems }}</pre>
    </div>
    <div v-if="!isAuthenticated" class="auth-warning">
      <p>Please log in to view your basket.</p>
      <button @click="redirectToLogin">Go to Login</button>
    </div>
    <div v-else-if="cartItems.length === 0" class="empty-basket">
      <p>Your basket is empty or contains unauthorized items!</p>
    </div>
    <div v-else>
      <table class="basket-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Manufacturer</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Total</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartItems" :key="item.id">
            <td>{{ item.product?.name || 'No name' }}</td>
            <td>{{ item.product?.manufacturer || 'No manufacturer' }}</td>
            <td>{{ formatPrice(item.product?.cost) }}</td>
            <td>
              <input
                type="number"
                v-model.number="item.quantity"
                min="1"
                @change="updateQuantity(item)"
              />
            </td>
            <td>{{ formatPrice(item.product?.cost * item.quantity) }}</td>
            <td>
              <button @click="removeFromCart(item.id)">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="basket-summary">
        <p>Total: <strong>{{ formatPrice(calculateTotal()) }}</strong></p>
        <button @click="proceedToCheckout">Proceed to Checkout</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      employeeId: null, // Сохраняем текущий employee_id
      cartItems: [], // Элементы корзины
    };
  },
  methods: {
    async loadEmployeeId() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/employees/user-employee/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.employeeId = response.data.id; // Сохраняем employee_id
        this.loadBasket(); // Загружаем корзину после получения employee_id
      } catch (error) {
        console.error('Ошибка при загрузке employeeId:', error);
      }
    },
    async loadBasket() {
      if (!this.employeeId) {
        console.warn('Employee ID отсутствует. Невозможно загрузить корзину.');
        return;
      }

      try {
        const response = await axios.get('http://localhost:8000/api/cart', {
          params: { employee_id: this.employeeId },
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        });

        // Преобразуем ответ в формат, который мы ожидаем
        if (response.data && response.data.length > 0) {
          this.cartItems = response.data; // Сохраняем данные корзины
        } else {
          console.info('Корзина пуста или не существует.');
        }
      } catch (error) {
        console.error('Ошибка загрузки корзины:', error.response?.data || error.message);
      }
    },
    formatPrice(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(value || 0);
    },
    calculateTotal() {
      return this.cartItems.reduce((total, item) => {
        return total + (item.product?.cost || 0) * item.quantity;
      }, 0);
    },
    updateQuantity(item) {
      // Логика обновления количества товара в корзине
      console.log('Изменение количества:', item);
    },
    removeFromCart(itemId) {
      // Логика удаления товара из корзины
      console.log('Удаление товара с ID:', itemId);
    },
    proceedToCheckout() {
      // Логика перехода к оформлению заказа
      console.log('Переход к оформлению заказа');
    },
    redirectToLogin() {
      // Переход на страницу входа
      console.log('Переход к странице входа');
    },
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('access_token');
    },
  },
  mounted() {
    this.loadEmployeeId(); // Загружаем employee_id при монтировании компонента
  },
};
</script>

<style scoped>
.basket {
  padding: 20px;
}

.employee-info {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f0f8ff;
  border: 1px solid #cce7ff;
  border-radius: 5px;
}

.employee-info p {
  font-size: 1.1em;
  color: #0056b3;
  margin: 0;
}

.basket-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.basket-table th,
.basket-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

.basket-summary {
  text-align: right;
  margin-top: 20px;
}

.auth-warning,
.empty-basket {
  text-align: center;
  padding: 20px;
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  border-radius: 5px;
  margin: 20px 0;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

input[type="number"] {
  width: 60px;
  text-align: center;
}
</style>



