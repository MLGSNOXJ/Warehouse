<template>
  <div class="product-page">
    <!-- Filters Block -->
    <div class="filters-container">

  <input 
    id="product-search-input" 
    v-model="searchQuery" 
    type="text" 
    src="require('./assets/strelka.svg')"
    placeholder="Поиск" 
    @input="resetPagination" 
    class="search-input"
  />


  <input 
    id="warehouse-select" 
    v-model="selectedWarehouse" 
    @input="filterByWarehouse" 
    class="filter-select" 
    placeholder="Выберите склад"
    list="warehouses-list"
  />
  <datalist id="warehouses-list">
    <option :value="null">Все склады</option>
    <option v-for="warehouse in warehouses" :key="warehouse.id" :value="warehouse.name">
      {{ warehouse.name }}
    </option>
  </datalist>

</div>


    <div class="table-pagination-container">
      <!-- Products Table -->
      <table class="product-table">
        <thead>
    <tr>
      <th>Фото</th>
      <th>Название</th>
      <th>Артикул (п)</th>
      <th>Артикул (в)</th>
      <th>Цена</th>
      <th>Заводской номер</th>
      
      <!-- Sortable Column: Стеллаж -->
      <th @click="sortBy('storage_location.shelving_number')" class="sortable-header">
        Стеллаж 
        <span :class="getSortClass('storage_location.shelving_number')">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.4364 2.43726C13.5856 2.43726 13.7287 2.49652 13.8341 2.60201L17.2727 6.04061C17.4924 6.26027 17.4924 6.61643 17.2727 6.8361C17.0531 7.05577 16.6969 7.05577 16.4772 6.8361L13.9989 4.35775V14.9998C13.9989 15.3104 13.7471 15.5623 13.4364 15.5623C13.1257 15.5623 12.8739 15.3104 12.8739 14.9998V4.35775L10.3956 6.8361C10.1759 7.05577 9.81973 7.05577 9.60006 6.8361C9.38039 6.61643 9.38039 6.26027 9.60006 6.04061L13.0387 2.60201C13.1441 2.49652 13.2872 2.43726 13.4364 2.43726Z" fill="#E7E7E7"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5.31384 15.5623C5.46303 15.5623 5.6061 15.503 5.71159 15.3975L9.15019 11.9589C9.36985 11.7392 9.36985 11.3831 9.15019 11.1634C8.93052 10.9437 8.57436 10.9437 8.35469 11.1634L5.87634 13.6418V2.99976C5.87634 2.6891 5.6245 2.43726 5.31384 2.43726C5.00318 2.43726 4.75134 2.6891 4.75134 2.99976V13.6418L2.27299 11.1634C2.05332 10.9437 1.69717 10.9437 1.4775 11.1634C1.25783 11.3831 1.25783 11.7392 1.4775 11.9589L4.91609 15.3975C5.02158 15.503 5.16466 15.5623 5.31384 15.5623Z" fill="#C6C6C6"/>
          </svg>
        </span>
      </th>

      <!-- Sortable Column: Полка -->
      <th @click="sortBy('storage_location.shelf_number')" class="sortable-header">
        Полка 
        <span :class="getSortClass('storage_location.shelf_number')">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.4364 2.43726C13.5856 2.43726 13.7287 2.49652 13.8341 2.60201L17.2727 6.04061C17.4924 6.26027 17.4924 6.61643 17.2727 6.8361C17.0531 7.05577 16.6969 7.05577 16.4772 6.8361L13.9989 4.35775V14.9998C13.9989 15.3104 13.7471 15.5623 13.4364 15.5623C13.1257 15.5623 12.8739 15.3104 12.8739 14.9998V4.35775L10.3956 6.8361C10.1759 7.05577 9.81973 7.05577 9.60006 6.8361C9.38039 6.61643 9.38039 6.26027 9.60006 6.04061L13.0387 2.60201C13.1441 2.49652 13.2872 2.43726 13.4364 2.43726Z" fill="#E7E7E7"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5.31384 15.5623C5.46303 15.5623 5.6061 15.503 5.71159 15.3975L9.15019 11.9589C9.36985 11.7392 9.36985 11.3831 9.15019 11.1634C8.93052 10.9437 8.57436 10.9437 8.35469 11.1634L5.87634 13.6418V2.99976C5.87634 2.6891 5.6245 2.43726 5.31384 2.43726C5.00318 2.43726 4.75134 2.6891 4.75134 2.99976V13.6418L2.27299 11.1634C2.05332 10.9437 1.69717 10.9437 1.4775 11.1634C1.25783 11.3831 1.25783 11.7392 1.4775 11.9589L4.91609 15.3975C5.02158 15.503 5.16466 15.5623 5.31384 15.5623Z" fill="#C6C6C6"/>
          </svg>
        </span>
      </th>

      <th @click="sortBy('storage_location.shelf_number')" class="sortable-header">Количество
        <span :class="getSortClass('storage_location.shelf_number')">
          <svg class = "svg" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M13.4364 2.43726C13.5856 2.43726 13.7287 2.49652 13.8341 2.60201L17.2727 6.04061C17.4924 6.26027 17.4924 6.61643 17.2727 6.8361C17.0531 7.05577 16.6969 7.05577 16.4772 6.8361L13.9989 4.35775V14.9998C13.9989 15.3104 13.7471 15.5623 13.4364 15.5623C13.1257 15.5623 12.8739 15.3104 12.8739 14.9998V4.35775L10.3956 6.8361C10.1759 7.05577 9.81973 7.05577 9.60006 6.8361C9.38039 6.61643 9.38039 6.26027 9.60006 6.04061L13.0387 2.60201C13.1441 2.49652 13.2872 2.43726 13.4364 2.43726Z" fill="#E7E7E7"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5.31384 15.5623C5.46303 15.5623 5.6061 15.503 5.71159 15.3975L9.15019 11.9589C9.36985 11.7392 9.36985 11.3831 9.15019 11.1634C8.93052 10.9437 8.57436 10.9437 8.35469 11.1634L5.87634 13.6418V2.99976C5.87634 2.6891 5.6245 2.43726 5.31384 2.43726C5.00318 2.43726 4.75134 2.6891 4.75134 2.99976V13.6418L2.27299 11.1634C2.05332 10.9437 1.69717 10.9437 1.4775 11.1634C1.25783 11.3831 1.25783 11.7392 1.4775 11.9589L4.91609 15.3975C5.02158 15.503 5.16466 15.5623 5.31384 15.5623Z" fill="#C6C6C6"/>
          </svg>
        </span>
      </th>
      <th>Действия</th>
    </tr>
  </thead>
        <tbody>
          <tr v-for="product in paginatedProducts" :key="product.id">
            <td class="product-photo-column"
                @mouseover="showPhotoPopup($event, product)"
                @mousemove="updatePopupPosition($event)"
                @mouseleave="hidePhotoPopup">
              <img :src="product.photoUrl || '/images/default-image.jpg'" alt="Фото" class="product-photo" />
            </td>
            <td>{{ product.name }}</td>
            <td>{{ product.article_p }}</td>
            <td>{{ product.article_v }}</td>
            <td>{{ product.cost }} руб.</td>
            <td>{{ product.factory_number }}</td>
            <td>{{ product.storage_location.shelving_number }}</td>
            <td 
              @mouseover="showShelfPopup($event, product.storage_location)"
              @mousemove="updatePopupPosition($event)"
              @mouseleave="hideShelfPopup">
              {{ product.storage_location.shelf_number }}
            </td>
            <td>{{ product.quantity }}</td>
            <td>
  <div v-if="!product.selectedQuantity" class="button-container">
    <button @click="selectProduct(product)" class="actions-button">В корзину</button>
  </div>

  <div v-else class="quantity-container">
    <button @click="decreaseQuantity(product)" class="quantity-button ">
      <svg width="14" height="2" viewBox="0 0 14 2" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12.3334 1L1.66675 1" stroke="#3D495B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    
    </button>
    <div class="quantity-input-wrapper">
  <input 
    type="number" 
    v-model="product.selectedQuantity" 
    min="1" 
    :max="product.quantity" 
    readonly
    class="quantity-input"
  />
</div>
    <button @click="increaseQuantity(product)" class="quantity-button">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M7 1.66675V12.3334" stroke="#3D495B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M1.66675 7H12.3334" stroke="#3D495B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>

    </button>
  </div>
</td>

          </tr>
        </tbody>
      </table>

      <!-- Pagination Controls -->
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1" class="arrow-btn">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M13.0893 4.41083C13.4148 4.73626 13.4148 5.2639 13.0893 5.58934L8.67859 10.0001L13.0893 14.4108C13.4148 14.7363 13.4148 15.2639 13.0893 15.5893C12.7639 15.9148 12.2363 15.9148 11.9108 15.5893L6.91083 10.5893C6.58539 10.2639 6.58539 9.73626 6.91083 9.41083L11.9108 4.41083C12.2363 4.08539 12.7639 4.08539 13.0893 4.41083Z" fill="#E7E7E7"/>
          </svg>

        </button>
        <template v-for="page in visiblePages" :key="page">
          <span v-if="page === '...'" class="ellipsis">...</span>
          <span 
            v-else
            @click="goToPage(page)" 
            :class="{ 'page-number': true, 'active': currentPage === page }"
          >
            {{ page }}
          </span>
        </template>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="arrow-btn">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.91066 4.41083C6.58523 4.73626 6.58523 5.2639 6.91066 5.58934L11.3214 10.0001L6.91066 14.4108C6.58523 14.7363 6.58523 15.2639 6.91066 15.5893C7.2361 15.9148 7.76374 15.9148 8.08917 15.5893L13.0892 10.5893C13.4146 10.2639 13.4146 9.73626 13.0892 9.41083L8.08917 4.41083C7.76374 4.08539 7.2361 4.08539 6.91066 4.41083Z" fill="#3D495B"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Всплывающее окно с увеличенным фото -->
    <div v-if="showPopup"
         :style="{ top: popupPosition.y + 'px', left: popupPosition.x + 'px' }"
         class="photo-popup">
      <img :src="popupImageUrl" alt="Фото" />
    </div>

    <!-- Всплывающее окно с количеством свободных мест на полке -->
    <div v-if="showShelfInfoPopup"
         :style="{ top: popupPosition.y + 'px', left: popupPosition.x + 'px' }"
         class="shelf-info-popup">
      <p>Свободных мест: {{ shelfInfo.freeSpaces }}</p>
      <p>Всего мест: {{ shelfInfo.totalSpaces }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductPage',
  data() {
    return {
      products: [],
      employees: [],
      warehouses: [],
      selectedWarehouse: null,
      selectedEmployee: null,
      searchQuery: '',
      sortKey: 'name',
      sortOrder: 'asc',
      currentPage: 1,
      pageSize: 7,
      showPopup: false,
      showShelfInfoPopup: false,
      shelfInfo: {
        freeSpaces: 0,
        totalSpaces: 0
      },
      popupImageUrl: '',
      popupPosition: { x: 0, y: 0 },
      employeeId: null // ID текущего сотрудника
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredProducts().length / this.pageSize);
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.sortedProducts().slice(start, end);
    },
    visiblePages() {
      const totalVisible = 6;
      const pages = [];
      
      if (this.totalPages <= totalVisible) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        const leftBound = Math.max(1, this.currentPage - 1);
        const rightBound = Math.min(this.totalPages - 3, this.currentPage + 1);

        for (let i = leftBound; i <= this.currentPage; i++) {
          pages.push(i);
        }
        for (let i = this.currentPage + 1; i <= rightBound; i++) {
          pages.push(i);
        }
        if (rightBound < this.totalPages - 3) {
          pages.push('...');
        }
        for (let i = Math.max(rightBound + 1, this.totalPages - 2); i <= this.totalPages; i++) {
          pages.push(i);
        }
      }

      return pages;
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://localhost:8000/products/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.status === 200) {
          this.products = response.data.map(product => ({
            ...product,
            photoUrl: `http://localhost:8000/products/products/${product.id}/photo`
          }));
        } else {
          console.error('Ошибка при получении списка продуктов');
        }
      } catch (error) {
        console.error('Ошибка при подключении к серверу', error);
      }
    },
    showShelfPopup(event, storageLocation) {
      this.shelfInfo = {
        freeSpaces: storageLocation.free_spaces || 0,
        totalSpaces: storageLocation.total_spaces || 0
      };
      this.popupPosition = { x: event.clientX + 10, y: event.clientY + 10 };
      this.showShelfInfoPopup = true;
    },
    hideShelfPopup() {
      this.showShelfInfoPopup = false;
    },
    showPhotoPopup(event, product) {
      this.popupImageUrl = product.photoUrl || '/images/default-image.jpg';
      this.popupPosition = { x: event.clientX + 20, y: event.clientY + 20 };
      this.showPopup = true;
    },
    updatePopupPosition(event) {
      this.popupPosition = { x: event.clientX + 20, y: event.clientY + 20 };
    },
    hidePhotoPopup() {
      this.showPopup = false;
    },
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
      this.resetPagination();
    },
    getSortClass(column) {
      if (this.sortKey !== column) return '';
      return this.sortOrder === 'asc' ? 'sort-asc' : 'sort-desc';
    },
    filteredProducts() {
      let products = this.products;
      if (this.selectedWarehouse) {
        products = products.filter(product => product.warehouse_id === this.selectedWarehouse.id);
      }
      if (this.selectedEmployee) {
        products = products.filter(product => product.employee_id === this.selectedEmployee.id);
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        products = products.filter(product => product.name.toLowerCase().includes(query));
      }
      return products;
    },
    sortedProducts() {
      return this.filteredProducts().sort((a, b) => {
        let comparison = 0;
        if (a[this.sortKey] > b[this.sortKey]) {
          comparison = 1;
        } else if (a[this.sortKey] < b[this.sortKey]) {
          comparison = -1;
        }
        return this.sortOrder === 'asc' ? comparison : -comparison;
      });
    },
    async loadEmployeeId() {
  try {
    const token = localStorage.getItem('access_token');
    const response = await axios.get('http://localhost:8000/employees/user-employee/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    this.employeeId = response.data.id;
  } catch (error) {
    console.error('Ошибка при загрузке employeeId:', error);
  }
},
selectProduct(product) {
  if (!this.employeeId) {
    alert('Сначала выберите сотрудника.');
    return;
  }

  axios.post('http://localhost:8000/api/cart/', {
    product_id: product.id,
    quantity: 1,
    employee_id: this.employeeId,
  }, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    }
  }).then(response => {
    alert('Товар успешно добавлен в корзину');
    // Опционально: Обновление корзины в Vuex
    this.$store.commit('addToCart', { 
      ...response.data.product, 
      quantity: response.data.quantity 
    });
  }).catch(error => {
    console.error('Ошибка при добавлении в корзину:', error);
    alert('Не удалось добавить товар в корзину');
  });
},
    confirmAddToCart(product) {
      if (product.selectedQuantity > product.quantity) {
        alert('Вы пытаетесь добавить больше, чем есть на складе');
        return;
      }

      let cart = JSON.parse(localStorage.getItem('cart')) || [];
      const index = cart.findIndex(item => item.id === product.id);

      if (index === -1) {
        cart.push({ ...product, quantity: product.selectedQuantity });
      } else {
        cart[index].quantity += product.selectedQuantity;
      }

      localStorage.setItem('cart', JSON.stringify(cart));
      alert('Товар добавлен в корзину');
      product.selectedQuantity = null;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    goToPage(page) {
      if (typeof page === 'number' && page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  
  addToCart(product) {
    const existingProduct = this.$store.state.cart.find(item => item.id === product.id);
    if (existingProduct) {
      // Если товар уже есть в корзине, увеличиваем количество на 1
      this.$store.commit('updateQuantity', product.id);
    } else {
      // Если товара нет в корзине, добавляем с количеством 1
      this.$store.commit('addToCart', { ...product, quantity: 1 });
    }
  },
  increaseQuantity(product) {
    if (product.selectedQuantity < product.quantity) {
      product.selectedQuantity += 1;
    }
  },
  // Уменьшение количества
  decreaseQuantity(product) {
    if (product.selectedQuantity > 1) {
      product.selectedQuantity -= 1;
    }
  },
    resetPagination() {
      this.currentPage = 1;
    }
  },
  mounted() {
    this.loadEmployeeId(); // Загрузка employeeId
    this.fetchProducts();
  }
};
</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #2e2e2e;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #919191;
}

main {
  flex: 1;
  padding: 20px;
  background-color: #2e2e2e;
}

.product-page {
  font-family: 'Arial', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 60px 20px 20px 20px;
  box-sizing: border-box;
}

.table-pagination-container {
  width: calc(100% - 312px);
  height: calc(100vh - 114px);
  position: fixed;
  top: 92px;
  left: 290px;
  gap: 0px;
  border-radius: 20px;
  opacity: 1;
  background-color: white;
  overflow: hidden;
  right: 22px;
  bottom: 22px;
  display: flex;
  flex-direction: column;
}

.shelf-info-popup {
  position: absolute;
  z-index: 1000;
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.filter-select,
.search-input {   
  width: 300px;
  height: 44px;
  border-radius: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  background-color: #fff;
  color: #333;
   /* Отступ для текста и плейсхолдера */
}
.filter-select{
  padding-left: 16px;
}
.search-input{
  padding-left: 40px;
  background-image: url('@/assets/search.svg');
  background-repeat: no-repeat;
  background-position: 17px center; /* Позиционируем иконку внутри поля */
}
.search-input::placeholder,
.filter-select::placeholder {
  color: #aaa;
}


.filters-container {
  display: flex;
  position: fixed;
  justify-content: flex-start;
  gap: 20px;
  margin-left: -18px;
  margin-top: -62px;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 60px;
  table-layout: fixed;
}

.product-table th,
.product-table td {
  padding-left: 16px; /* Adds 16px padding to the left */
  height: 56px;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px; /* Ensures correct line spacing */
  text-align: left;
  border: 1px solid #ddd;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


.product-table th {
  font-weight: normal;
  font-size: 14px;
  background-color: #f5f5f5;
  white-space: nowrap;
}

/* Specific styling for sortable headers */
/* Sortable header styles */
.sortable-header {
  position: relative;
  cursor: pointer;
  padding-right: 20px; /* Оставляем место для иконки */
  white-space: nowrap;
}

/* SVG Icon styles */
.sortable-header svg {
  position: absolute;
 
  top: 50%;
  transform: translateY(-50%); /* Центрируем иконку по вертикали */
  width: 16px; /* Размер иконки */
  height: 16px;
  margin-left: 8px; /* Отступ слева от текста */
}

/* Centering container */
.button-container {
  display: flex;
  justify-content: center; /* Centers horizontally */
  align-items: center; /* Centers vertically */
  margin-right: 10%;
  height: 100%; /* Ensures it takes the full cell height */
}

/* Button styles */
.actions-button {
  width: 116px;
  height: 28px;
  border-radius: 6px; /* Fully rounded button */
  background-color: #3D495B;
  color: white;
  font-size: 12px;
  font-weight: 400;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.actions-button:hover {
  background-color: #4A5667; /* Slightly lighter color on hover */
}


.product-photo {
  width: 40px; /* Размер фото */
  height: 40px;
  object-fit: cover;
  border-radius: 4px; /* Скругленные углы */
  display: block; /* Чтобы изображение не учитывало текстовые выравнивания */
}

.product-table td:nth-child(1),
.product-table th:nth-child(1) {
  width: 50px;
}
.product-table td:nth-child(1) {
  text-align: center; /* Горизонтальное выравнивание */
  vertical-align: middle; /* Вертикальное выравнивание */
  padding: 0; /* Убираем отступы для точного центрирования */
}
.product-table td:nth-child(2),
.product-table th:nth-child(2) {
  width: 150px;
}

.product-table td:nth-child(3),
.product-table th:nth-child(3),
.product-table td:nth-child(4),
.product-table th:nth-child(4) {
  width: 100px;
}

.product-table td:nth-child(5),
.product-table th:nth-child(5) {
  width: 80px;
}

.product-table td:nth-child(6),
.product-table th:nth-child(6) {
  width: 100px;
}

.product-table td:nth-child(7),
.product-table th:nth-child(7),
.product-table td:nth-child(8),
.product-table th:nth-child(8) {
  width: 70px;
}

.product-table td:nth-child(9),
.product-table th:nth-child(9) {
  width: 90px;
}

.product-table td:nth-child(10),
.product-table th:nth-child(10) {
  width: 100px;
}
.product-table th:nth-child(10) {
  text-align: left; /* Выровнять по левому краю */
  padding-left: 40px; /* Настройте этот отступ для выравнивания с кнопкой */
}
.product-table td {
  vertical-align: middle;
  font-size: 14px;
}

.pagination-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: transparent; /* Убираем фон */
  padding: 10px;
  border-radius: 4px;
  box-shadow: none; /* Убираем тень */
}

.arrow-btn {
  background-color: transparent; /* Убираем фон */
  color: #3D495B; /* Темный цвет для стрелок */
  border: none; /* Убираем рамку */
  padding: 0;
  font-size: 24px; /* Увеличиваем размер символов */
  cursor: pointer;
  transition: color 0.2s;
}

.arrow-btn:hover:not(:disabled) {
  color: #888; /* Более светлый цвет при наведении */
}

.arrow-btn:disabled {
  color: #cccccc; /* Цвет для отключенной кнопки */
  cursor: not-allowed;
}

.page-number {
  color: #3D495B; /* Цвет текста */
  font-size: 18px; /* Размер шрифта */
  padding: 0;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
  background-color: transparent; /* Убираем фон */
  border: none; /* Убираем рамку */
}

.page-number:hover:not(.active) {
  color: #888; /* Более светлый цвет при наведении */
}

.page-number.active {
  color: #000; /* Цвет активной страницы */
  cursor: default;
}

.ellipsis {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  user-select: none;
}


.product-photo {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  display: block;
  margin: 8px auto;
}

.product-table tr:hover {
  background-color: #f0f0f0;
}



/* Centering container */
.quantity-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 11%;
  gap: 5px;
  height: 100%;
}

/* Minus and Plus Button Styles */
.quantity-button {
  width: 27px; /* Fixed width */
  height: 27px; /* Fixed height */
  padding: 4px 6px;
  border-radius: 6px;
  background-color: #BCED0A80;
  border: none;
  color: #333;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: none; /* Remove hover effect */
}


.quantity-button:hover {
  background-color: #BCED0A; /* Slightly darker shade on hover */
}

/* Wrapper for quantity input */
.quantity-input-wrapper {
  width: 48px;
  height: 27px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F6F7FA;
  border: 1px solid #BCED0A;
  border-radius: 6px;
  box-sizing: border-box;
}

/* Input centered text, with number type-specific adjustments */
.quantity-input {
  width: 100%;
  height: 100%;
  text-align: center; /* Centers text horizontally */
  font-size: 14px;
  color: #333;
  border: none;
  outline: none;
  background: transparent;
  padding: 0;
  margin: 0;
  box-sizing: border-box
}

.quantity-input::-webkit-inner-spin-button, 
.quantity-input::-webkit-outer-spin-button {
  -webkit-appearance: none; /* Chrome, Safari */
  margin: 0; /* Ensures no unwanted spacing */
}



.photo-popup {
  position: absolute;
  z-index: 1000;
  border: 2px solid #888;
  background-color: #fff;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.photo-popup img {
  max-width: 180px;
  max-height: 180px;
  border-radius: 4px;
}

@media screen and (max-width: 1200px) {
  .table-pagination-container {
    width: calc(100% - 40px);
    left: 20px;
  }
}

@media screen and (max-width: 768px) {
  .filter {
    max-width: 100%;
  }
  
  .pagination-controls {
    right: 50%;
    transform: translateX(50%);
  }
}

</style>
