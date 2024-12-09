<template>
  <div class="container">
    <div class="product-container">
      <!-- Form to add product details -->
      <div class="form-container">
        <h2>Добавить продукт</h2>

        <!-- Product input fields -->
        <label for="name">Название:</label>
        <input type="text" v-model="formData.name" id="name" />

        <label for="manufacturer">Производитель:</label>
        <input type="text" v-model="formData.manufacturer" id="manufacturer" />

        <label for="article_v">Артикул производителя:</label>
        <input type="text" v-model="formData.article_v" id="article_v" />

        <label for="article_p">Артикул внутренний:</label>
        <input type="text" v-model="formData.article_p" id="article_p" />

        <label for="cost">Стоимость:</label>
        <input type="number" v-model="formData.cost" id="cost" />

        <label for="factory_number">Заводской номер:</label>
        <input type="number" v-model="formData.factory_number" id="factory_number" />

        <label for="supplier_id">Поставщик:</label>
        <select v-model="formData.supplier_id" id="supplier_id">
          <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">{{ supplier.name }}</option>
        </select>
        <button class="styled-btn-small" @click="openSupplierModal">Добавить Поставщика</button>

        <label for="category_id">Категория:</label>
        <select v-model="formData.category_id" id="category_id">
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
        <button class="styled-btn-small" @click="openCategoryModal">Добавить Категорию</button>

        <!-- Cascading dropdowns for storage location -->
        <label for="shelving_number">Номер стеллажа:</label>
        <select v-model="selectedShelvingNumber" id="shelving_number">
          <option v-for="shelving in shelvingNumbers" :key="shelving" :value="shelving">{{ shelving }}</option>
        </select>

        <label for="shelf_number">Номер полки:</label>
        <select v-model="formData.storage_location_id" id="shelf_number">
          <option v-for="location in filteredShelfNumbers" :key="location.id" :value="location.id">{{ location.shelf_number }}</option>
        </select>

        <label for="warehouse_id">Склад:</label>
        <select v-model="formData.warehouse_id" id="warehouse_id">
          <option v-for="warehouse in warehouses" :key="warehouse.id" :value="warehouse.id">{{ warehouse.name }}</option>
        </select>
        <button class="styled-btn-small" @click="openWarehouseModal">Добавить Склад</button>

        <label for="employee_id">Сотрудник:</label>
        <select v-model="formData.employee_id" id="employee_id">
          <option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.FIO }}</option>
          <option v-if="employees.length === 0" disabled>Нет сотрудников</option>
        </select>

        <label for="quantity">Кол-во единиц товара:</label>
        <input type="number" v-model="formData.quantity" id="quantity" />

        <!-- New field for product photo -->
        <label for="photo">Фото продукта:</label>
        <input type="file" @change="handleFileUpload" id="photo" accept="image/*" />

        <!-- Display uploaded photo -->
        <div v-if="formData.photoPreview">
          <h3>Предпросмотр фото:</h3>
          <img :src="formData.photoPreview" alt="Product Photo" style="max-width: 200px; margin-top: 10px;" />
        </div>

        <button class="styled-btn" @click="saveProduct">Сохранить продукт</button>
      </div>
    </div>

    <!-- Info container for UPD, invoice, and storage location -->
    <div class="info-container">
      <!-- Блок добавления УПД -->
      <div class="info-block">
        <h2>УПД</h2>
        <button class="styled-btn" @click="openUPDModal">Добавить УПД</button>
        <div v-if="formData.upd_id">
          <label for="upd_number">ID УПД:</label>
          <input type="text" v-model="formData.upd_id" id="upd_number" readonly />
        </div>
      </div>

      <!-- Блок добавления счета -->
      <div class="info-block">
        <h2>Счет</h2>
        <button class="styled-btn" @click="openInvoiceModal">Добавить счет</button>
        <div v-if="formData.account_id">
          <label for="account_number">ID счета:</label>
          <input type="text" v-model="formData.account_id" id="account_number" readonly />
        </div>
      </div>

      <!-- Блок добавления места хранения -->
      <div class="info-block">
        <h2>Место хранения</h2>
        <button class="styled-btn" @click="openStorageLocationModal">Добавить место хранения</button>
        <div v-if="formData.storage_location_id">
          <label for="storage_location_id">ID места хранения:</label>
          <input type="text" v-model="formData.storage_location_id" id="storage_location_id" readonly />
        </div>
      </div>

      <!-- Модальное окно для УПД -->
      <div v-if="showUPDModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeUPDModal">&times;</span>
          <h2>Добавить УПД</h2>

          <label for="doc_number">Номер УПД:</label>
          <input type="text" v-model="updData.doc_number" id="doc_number" />

          <label for="supplier">Поставщик:</label>
          <select v-model="updData.supplier_id" id="supplier">
            <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">{{ supplier.name }}</option>
          </select>

          <label for="upd_file">Файл УПД (PDF):</label>
          <input type="file" ref="updFileInput" id="upd_file" />

          <button class="styled-btn" @click="saveUPD">Сохранить УПД</button>
        </div>
      </div>

      <!-- Модальное окно для счета -->
      <div v-if="showInvoiceModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeInvoiceModal">&times;</span>
          <h2>Добавить счет</h2>

          <label for="account_number">Номер счета:</label>
          <input type="text" v-model="invoiceData.account_number" id="account_number" />

          <label for="supplier">Поставщик:</label>
          <select v-model="invoiceData.supplier_id" id="supplier">
            <option v-for="supplier in suppliers" :key="supplier.id" :value="supplier.id">{{ supplier.name }}</option>
          </select>

          <label for="summ">Сумма:</label>
          <input type="text" v-model="invoiceData.summ" id="summ" />

          <label for="invoice_file">Файл счета (PDF)</label>
          <input type="file" ref="invoiceFileInput" id="invoice_file" />

          <button class="styled-btn" @click="saveInvoice">Сохранить Счет</button>
        </div>
      </div>

      <!-- Модальное окно для места хранения -->
      <div v-if="showStorageLocationModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeStorageLocationModal">&times;</span>
          <h2>Добавить место хранения</h2>

          <label for="shelving_number">Номер стеллажа:</label>
          <input type="number" v-model="storageLocationData.shelving_number" id="shelving_number" />

          <label for="shelf_number">Номер полки:</label>
          <input type="number" v-model="storageLocationData.shelf_number" id="shelf_number" />

          <label for="description">Описание:</label>
          <input type="text" v-model="storageLocationData.description" id="description" />

          <label for="quanity">Кол-во места:</label>
          <input type="text" v-model="storageLocationData.location_count" id="location_count" />

          <button class="styled-btn" @click="saveStorageLocation">Сохранить место хранения</button>
        </div>
      </div>

      <!-- Модальное окно для Поставщика -->
      <div v-if="showSupplierModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeSupplierModal">&times;</span>
          <h2>Добавить Поставщика</h2>

          <label for="supplier_name">Название:</label>
          <input type="text" v-model="supplierData.name" id="supplier_name" />

          <label for="supplier_inn">ИНН:</label>
          <input type="text" v-model="supplierData.inn" id="supplier_inn" />

          <label for="supplier_address">Юридический адрес:</label>
          <input type="text" v-model="supplierData.ur_adress" id="supplier_address" />

          <label for="supplier_account">Расчетный счет:</label>
          <input type="text" v-model="supplierData.payment_account" id="supplier_account" />

          <label for="supplier_bank">Банк:</label>
          <input type="text" v-model="supplierData.bank" id="supplier_bank" />

          <label for="supplier_bik">БИК:</label>
          <input type="text" v-model="supplierData.bik" id="supplier_bik" />

          <label for="supplier_corr_account">Корреспондентский счет:</label>
          <input type="text" v-model="supplierData.corr_account" id="supplier_corr_account" />

          <label for="supplier_manager">ФИО менеджера:</label>
          <input type="text" v-model="supplierData.fio_manager" id="supplier_manager" />

          <label for="supplier_email">Email:</label>
          <input type="email" v-model="supplierData.email" id="supplier_email" />

          <label for="supplier_phone">Телефон:</label>
          <input type="text" v-model="supplierData.phone" id="supplier_phone" />

          <button class="styled-btn" @click="saveSupplier">Сохранить Поставщика</button>
        </div>
      </div>

      <!-- Модальное окно для Категории -->
      <div v-if="showCategoryModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeCategoryModal">&times;</span>
          <h2>Добавить Категорию</h2>

          <label for="category_name">Название:</label>
          <input type="text" v-model="categoryData.name" id="category_name" />

          <label for="company_id">ID Компании:</label>
          <input type="number" v-model="categoryData.company_id" id="company_id" />

          <button class="styled-btn" @click="saveCategory">Сохранить Категорию</button>
        </div>
      </div>

      <!-- Модальное окно для Склада -->
      <div v-if="showWarehouseModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeWarehouseModal">&times;</span>
          <h2>Добавить Склад</h2>

          <label for="warehouse_name">Название склада:</label>
          <input type="text" v-model="warehouseData.name" id="warehouse_name" />

          <label for="company_id">ID Компании:</label>
          <input type="number" v-model="warehouseData.company_id" id="company_id" />

          <button class="styled-btn" @click="saveWarehouse">Сохранить Склад</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showMenu: false,
      showInvoiceModal: false,
      showUPDModal: false,
      showStorageLocationModal: false,
      showSupplierModal: false,
      showCategoryModal: false,
      showWarehouseModal: false,
      formData: {
        name: '',
        manufacturer: '',
        article_p: '',
        article_v: '',
        cost: '',
        quantity: '',
        factory_number: '',
        supplier_id: null,
        category_id: null,
        storage_location_id: null,
        warehouse_id: null,
        employee_id: null,
        account_id: null,
        upd_id: null,
        photo: null, // Add photo property
        photoPreview: null // Add photoPreview property
        
      },
      invoiceData: {
        account_number: '',
        summ: '',
        supplier_id: null
      },
      updData: {
        doc_number: '',
        supplier_id: null
      },
      storageLocationData: {
        shelving_number: '',
        shelf_number: '',
        description: '',
        location_count: ''
      },
      supplierData: {
        name: '',
        inn: '',
        ur_adress: '',
        payment_account: '',
        bank: '',
        bik: '',
        corr_account: '',
        fio_manager: '',
        email: '',
        phone: ''
      },
      categoryData: {
        name: '',
        company_id: null
      },
      warehouseData: {
        name: '',
        company_id: null
      },
      suppliers: [],
      categories: [],
      storageLocations: [],
      warehouses: [],
      employees: [],
      selectedShelvingNumber: null  // New state for selected shelving number
    };
  },
  computed: {
    shelvingNumbers() {
      return [...new Set(this.storageLocations.map(loc => loc.shelving_number))];
    },
    filteredShelfNumbers() {
      return this.storageLocations.filter(loc => loc.shelving_number === this.selectedShelvingNumber);
    }
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    openInvoiceModal() {
      this.showInvoiceModal = true;
    },
    closeInvoiceModal() {
      this.showInvoiceModal = false;
      this.invoiceData = {
        account_number: '',
        summ: '',
        supplier_id: null
      };
    },
    openUPDModal() {
      this.showUPDModal = true;
    },
    closeUPDModal() {
      this.showUPDModal = false;
      this.updData = {
        doc_number: '',
        supplier_id: null
      };
    },
    openStorageLocationModal() {
      this.showStorageLocationModal = true;
    },
    closeStorageLocationModal() {
      this.showStorageLocationModal = false;
      this.storageLocationData = {
        shelving_number: '',
        shelf_number: '',
        description: '',
        location_count: ''
      };
    },

    openSupplierModal() {
      this.showSupplierModal = true;
    },
    closeSupplierModal() {
      this.showSupplierModal = false;
      this.resetSupplierData();
    },
    openCategoryModal() {
      this.showCategoryModal = true;
    },
    closeCategoryModal() {
      this.showCategoryModal = false;
      this.resetCategoryData();
    },
    openWarehouseModal() {
      this.showWarehouseModal = true;
    },
    closeWarehouseModal() {
      this.showWarehouseModal = false;
      this.resetWarehouseData();
    },

    resetSupplierData() {
      this.supplierData = {
        name: '',
        inn: '',
        ur_adress: '',
        payment_account: '',
        bank: '',
        bik: '',
        corr_account: '',
        fio_manager: '',
        email: '',
        phone: ''
      };
    },
    resetCategoryData() {
      this.categoryData = {
        name: '',
        company_id: null
      };
    },
    resetWarehouseData() {
      this.warehouseData = {
        name: '',
        company_id: null
      };
    },

    async fetchSuppliers() {
      try {
        const response = await axios.get('http://localhost:8000/products/suppliers/');
        this.suppliers = response.data;
      } catch (error) {
        console.error('Ошибка при получении поставщиков:', error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://localhost:8000/products/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Ошибка при получении категорий:', error);
      }
    },
    async fetchStorageLocations() {
      try {
        const response = await axios.get('http://localhost:8000/products/storage-locations/');
        this.storageLocations = response.data;
      } catch (error) {
        console.error('Ошибка при получении мест хранения:', error);
      }
    },
    async fetchWarehouses() {
      try {
        const response = await axios.get('http://localhost:8000/products/warehouses/');
        this.warehouses = response.data;
      } catch (error) {
        console.error('Ошибка при получении складов:', error);
      }
    },
    async fetchEmployees() {
      try {
        const response = await axios.get('http://localhost:8000/employees/');
        this.employees = response.data;
      } catch (error) {
        console.error('Ошибка при получении сотрудников:', error);
      }
    },
    async fetchCompanies() {
    try {
      const response = await axios.get('http://localhost:8000/companies/');
      this.companies = response.data;
    } catch (error) {
      console.error('Ошибка при получении компаний:', error);
    }
  },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.formData.photo = file;

        // Create a preview URL for the selected photo
        this.formData.photoPreview = URL.createObjectURL(file);
      } else {
        this.formData.photo = null;
        this.formData.photoPreview = null;
      }
    },

    async saveProduct() {
  if (!this.validateProductData()) return;

  const formData = new FormData();

  try {
    // Добавляем данные в FormData
    formData.append('name', this.formData.name);
    formData.append('manufacturer', this.formData.manufacturer);
    formData.append('article_p', this.formData.article_p);
    formData.append('article_v', this.formData.article_v);
    formData.append('cost', parseFloat(this.formData.cost));
    formData.append('factory_number', parseInt(this.formData.factory_number));
    formData.append('quantity', parseInt(this.formData.quantity)); // Fixed typo

    // Добавляем только если есть валидное значение
    if (this.formData.account_id) {
      formData.append('account_id', parseInt(this.formData.account_id));
    }

    if (this.formData.upd_id) {
      formData.append('upd_id', parseInt(this.formData.upd_id));
    }

    if (this.formData.supplier_id) {
      formData.append('supplier_id', parseInt(this.formData.supplier_id));
    }

    if (this.formData.category_id) {
      formData.append('category_id', parseInt(this.formData.category_id));
    }

    if (this.formData.storage_location_id) {
      formData.append('storage_location_id', parseInt(this.formData.storage_location_id));
    }

    if (this.formData.warehouse_id) {
      formData.append('warehouse_id', parseInt(this.formData.warehouse_id));
    }

    if (this.formData.employee_id) {
      formData.append('employee_id', parseInt(this.formData.employee_id));
    }

    if (this.formData.photo) {
      formData.append('photo', this.formData.photo);
    }

    // Отправка данных на сервер
    await axios.post('http://localhost:8000/products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    alert('Продукт успешно сохранен!');
  } catch (error) {
    const errorMsg = error.response?.data?.detail || error.message;
    console.error('Ошибка при сохранении продукта:', errorMsg);

    if (error.response && error.response.data) {
      console.error('Подробная ошибка:', JSON.stringify(error.response.data, null, 2));
      alert('Ошибка при сохранении продукта: ' + JSON.stringify(error.response.data, null, 2));
    } else {
      alert('Ошибка при сохранении продукта: ' + errorMsg);
    }
  }
},
    async saveInvoice() {
      if (!this.validateInvoiceData()) {
        return;
      }

      const formData = new FormData();
      formData.append('account_number', this.invoiceData.account_number);
      formData.append('summ', this.invoiceData.summ);
      formData.append('supplier_id', this.invoiceData.supplier_id);
      formData.append('file', this.$refs.invoiceFileInput.files[0]);

      try {
        const response = await axios.post('http://localhost:8000/products/invoices/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.data && response.data.id) {
          this.formData.account_id = response.data.id;
          alert('Счет успешно сохранен!');
          this.closeInvoiceModal();
        } else {
          alert('Ошибка: Сервер не вернул ID счета.');
        }
      } catch (error) {
        console.error('Ошибка при сохранении счета:', error);
        alert('Ошибка при сохранении счета: ' + (error.response ? JSON.stringify(error.response.data) : error.message));
      }
    },
    async saveUPD() {
      if (!this.validateUPDData()) {
        return;
      }

      const formData = new FormData();
      formData.append('doc_number', this.updData.doc_number);
      formData.append('supplier_id', this.updData.supplier_id);
      formData.append('file', this.$refs.updFileInput.files[0]);

      try {
        const response = await axios.post('http://localhost:8000/products/upds/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        this.formData.upd_id = response.data.id;
        alert('УПД успешно сохранен!');
        this.closeUPDModal();
      } catch (error) {
        console.error('Ошибка при сохранении УПД:', error);
        alert('Ошибка при сохранении УПД: ' + (error.response ? JSON.stringify(error.response.data) : error.message));
      }
    },
    async saveStorageLocation() {
  if (!this.validateStorageLocationData()) {
    return;
  }

  const formData = new FormData();
  formData.append('shelving_number', this.storageLocationData.shelving_number);
  formData.append('shelf_number', this.storageLocationData.shelf_number);
  formData.append('description', this.storageLocationData.description);
  formData.append('location_count', this.storageLocationData.location_count)

  try {
    const response = await axios.post('http://localhost:8000/products/storage-locations/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (response.data && response.data.id) {
      this.formData.storage_location_id = response.data.id;
      alert('Место хранения успешно сохранено!');
      this.closeStorageLocationModal();
      this.fetchStorageLocations();  // Update storage locations list
    } else {
      alert('Ошибка: Сервер не вернул ID места хранения.');
    }
  } catch (error) {
    console.error('Ошибка при сохранении места хранения:', error);
    alert('Ошибка при сохранении места хранения: ' + (error.response ? JSON.stringify(error.response.data) : error.message));
  }
},
    async saveSupplier() {
      console.log('Supplier Data being sent:', this.supplierData);

      // Create a FormData object to properly format the data for the backend
      const formData = new FormData();
      formData.append('name', this.supplierData.name);
      formData.append('inn', this.supplierData.inn);
      formData.append('ur_adress', this.supplierData.ur_adress);
      formData.append('payment_account', this.supplierData.payment_account);
      formData.append('bank', this.supplierData.bank);
      formData.append('bik', this.supplierData.bik);
      formData.append('corr_account', this.supplierData.corr_account);
      formData.append('fio_manager', this.supplierData.fio_manager);
      formData.append('email', this.supplierData.email);
      formData.append('phone', this.supplierData.phone);

      try {
        const response = await axios.post('http://localhost:8000/products/suppliers/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('Supplier Saved:', response.data);
        alert('Поставщик успешно добавлен!');
        this.closeSupplierModal();
        this.fetchSuppliers();  // Refresh the supplier list
      } catch (error) {
        if (error.response && error.response.data) {
          console.error('Server Response:', error.response.data);

          let errorMessage = 'Ошибка при сохранении поставщика: ';
          if (Array.isArray(error.response.data.detail)) {
            errorMessage += error.response.data.detail.map(detail => detail.msg || JSON.stringify(detail)).join('; ');
          } else {
            errorMessage += error.response.data.detail;
          }

          alert(errorMessage);
        } else {
          console.error('Ошибка при сохранении поставщика:', error.message);
          alert('Ошибка при сохранении поставщика: ' + error.message);
        }
      }
    },
    async saveCategory() {
      console.log('Category Data being sent:', this.categoryData);

      // Create a FormData object to properly format the data for the backend
      const formData = new FormData();
      formData.append('name', this.categoryData.name);
      formData.append('company_id', this.categoryData.company_id);

      try {
        const response = await axios.post('http://localhost:8000/products/categories/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('Category Saved:', response.data);
        alert('Категория успешно добавлена!');
        this.closeCategoryModal();
        this.fetchCategories();
      } catch (error) {
        if (error.response && error.response.data) {
          console.error('Server Response:', error.response.data);

          let errorMessage = 'Ошибка при сохранении категории: ';
          if (Array.isArray(error.response.data.detail)) {
            errorMessage += error.response.data.detail.map(detail => detail.msg || JSON.stringify(detail)).join('; ');
          } else {
            errorMessage += error.response.data.detail;
          }

          alert(errorMessage);
        } else {
          console.error('Ошибка при сохранении категории:', error.message);
          alert('Ошибка при сохранении категории: ' + error.message);
        }
      }
    },
    async saveWarehouse() {
      console.log('Warehouse Data being sent:', this.warehouseData);

      // Create a FormData object to properly format the data for the backend
      const formData = new FormData();
      formData.append('name', this.warehouseData.name);
      formData.append('company_id', this.warehouseData.company_id);

      try {
        // Send the FormData to the backend
        const response = await axios.post('http://localhost:8000/products/warehouses/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log('Warehouse Saved:', response.data);
        alert('Склад успешно добавлен!');
        this.closeWarehouseModal();
        this.fetchWarehouses();  // Refresh the warehouse list
      } catch (error) {
        if (error.response && error.response.data) {
          console.error('Server Response:', error.response.data);

          let errorMessage = 'Ошибка при сохранении склада: ';
          if (Array.isArray(error.response.data.detail)) {
            errorMessage += error.response.data.detail.map(detail => detail.msg || JSON.stringify(detail)).join('; ');
          } else {
            errorMessage += error.response.data.detail;
          }

          alert(errorMessage);
        } else {
          console.error('Ошибка при сохранении склада:', error.message);
          alert('Ошибка при сохранении склада: ' + error.message);
        }
      }
    },
    validateProductData() {
      // Validation logic here...
      return true;
    },
    validateInvoiceData() {
      // Validation logic here...
      return true;
    },
    validateUPDData() {
      // Validation logic here...
      return true;
    },
    validateStorageLocationData() {
      // Validation logic here...
      return true;
    }
  },
  async created() {
    await this.fetchSuppliers();
    await this.fetchCategories();
    await this.fetchStorageLocations();
    await this.fetchWarehouses();
    await this.fetchEmployees();
    await this.fetchCompanies();
  }
};
</script>

<style scoped>
:root {
  --background-color-light: #f9f9f9;
  --background-color-dark: #293446;
  --text-color-light: #333; /* Текст для светлой темы */
  --text-color-dark: #dfdfdf; /* Текст для тёмной темы */
  --input-bg-color-light: #fff;
  --input-bg-color-dark: #252f3d;
  --button-bg-color-light: #007bff;
  --button-bg-color-dark: #f6a400;
  --button-hover-bg-color-light: #0056b3;
  --button-hover-bg-color-dark: #d48900;
  --modal-bg-color-light: rgba(255, 255, 255, 0.9);
  --modal-bg-color-dark: rgba(37, 47, 61, 0.9);
  --form-bg-color-light: #f0f0f0;
  --form-bg-color-dark: #293446;
  --title-color-light: #007bff; /* Цвет заголовков для светлой темы */
  --title-color-dark: #f6a400; /* Цвет заголовков для тёмной темы */
  --link-color-light: #007bff; /* Цвет ссылок для светлой темы */
  --link-color-dark: #f6a400; /* Цвет ссылок для тёмной темы */
}

body[data-theme='light'] {
  --background-color: var(--background-color-light);
  --text-color: var(--text-color-light);
  --input-bg-color: var(--input-bg-color-light);
  --button-bg-color: var(--button-bg-color-light);
  --button-hover-bg-color: var(--button-hover-bg-color-light);
  --modal-bg-color: var(--modal-bg-color-light);
  --form-bg-color: var(--form-bg-color-light);
  --title-color: var(--title-color-light);
  --link-color: var(--link-color-light);
}

body[data-theme='dark'] {
  --background-color: var(--background-color-dark);
  --text-color: var(--text-color-dark);
  --input-bg-color: var(--input-bg-color-dark);
  --button-bg-color: var(--button-bg-color-dark);
  --button-hover-bg-color: var(--button-hover-bg-color-dark);
  --modal-bg-color: var(--modal-bg-color-dark);
  --form-bg-color: var(--form-bg-color-dark);
  --title-color: var(--title-color-dark);
  --link-color: var(--link-color-dark);
}

/* Контейнеры и текст */
.container {
  display: flex;
  gap: 20px;
}

.product-container {
  margin-left: 410px;
  flex: 2;
  font-family: 'Arial', serif;
}

.info-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-container,
.info-block {
  max-width: 600px;
  padding: 20px;
  background-color: var(--form-bg-color);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-top: 50px;
  margin-right: 50px;
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: var(--title-color); /* Заголовок меняет цвет в зависимости от темы */
  font-weight: bold;
  font-size: 24px;
}

label {
  display: block;
  margin-top: 15px;
  color: var(--text-color); /* Цвет текста меняется в зависимости от темы */
  font-weight: 600;
  font-size: 14px;
}

/* Поля ввода и текст */
input[type="text"],
input[type="number"],
input[type="email"],
select {
  width: 100%;
  color: var(--text-color); /* Текст внутри полей ввода меняется в зависимости от темы */
  padding: 12px 15px;
  margin-top: 8px;
  margin-bottom: 15px;
  border: 1px solid #7a7979;
  border-radius: 8px;
  background-color: var(--input-bg-color); /* Цвет фона полей ввода меняется */
  box-sizing: border-box;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

input[type="file"] {
  margin-top: 8px;
  margin-bottom: 15px;
}

.styled-btn,
.styled-btn-small {
  background-color: var(--button-bg-color);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}

.styled-btn {
  display: inline-block;
  width: 100%;
  padding: 12px 0;
  margin-top: 10px;
}

.styled-btn:hover {
  background-color: var(--button-hover-bg-color);
}

.styled-btn-small {
  margin-top: -10px;
  margin-bottom: 10px;
  padding: 5px 10px;
  font-size: 12px;
}

.styled-btn-small:hover {
  background-color: var(--button-hover-bg-color);
}

/* Стили модальных окон */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--modal-bg-color);
  padding: 20px 30px;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  max-height: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  position: relative;
  animation: fadeIn 0.3s ease;
}

.modal-content h2 {
  text-align: center;
  color: var(--title-color); /* Цвет заголовков меняется в модальном окне */
  font-size: 22px;
  margin-bottom: 20px;
}

label {
  color: var(--text-color); /* Цвет текста в модальных окнах */
}

.close {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 24px;
  color: var(--text-color); /* Цвет кнопки закрытия модального окна */
  cursor: pointer;
}

.close:hover {
  color: var(--button-bg-color);
}

/* Анимация появления и исчезновения для модальных окон */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Ссылки и их поведение в зависимости от темы */
a {
  color: var(--link-color); /* Ссылки меняют цвет в зависимости от темы */
}

a:hover {
  text-decoration: underline;
}

</style>
