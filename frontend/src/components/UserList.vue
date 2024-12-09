<template>
  <div class="user-list">
    <h1>Сотрудники</h1>
    <div v-if="error" class="error">
      <p>Не удалось загрузить список сотрудников. Попробуйте еще раз позже.</p>
    </div>
    <div v-if="users.length === 0 && !loading && !error" class="no-users">
      <p>Нет доступных сотрудников.</p>
    </div>
    <div v-else class="user-cards">
      <div v-for="user in users" :key="user.id" class="user-card" @click="goToUserDetail(user.id)">
        <img :src="user.photoUrl" alt="User Photo" class="user-photo" />
        <div class="user-info">
          <h2>{{ user.name }}</h2>
          <p class="user-position">{{ user.position }}</p>
        </div>
        <button @click.stop="deleteUser(user.id)" class="delete-button">Удалить</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      loading: true,
      error: false,
      currentUserId: null,
    };
  },
  async created() {
    this.getCurrentUserId();
    await this.fetchUsers();
  },
  methods: {
    getCurrentUserId() {
      this.currentUserId = localStorage.getItem('userId');
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:8000/employees');
        this.users = response.data.map(user => ({
          id: user.id,
          name: user.FIO,
          position: user.post,
          photoUrl: `http://localhost:8000/employees/${user.id}/photo`
        }));
        this.loading = false;
      } catch (error) {
        console.error('Ошибка при загрузке списка сотрудников:', error);
        this.error = true;
        this.loading = false;
      }
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`http://localhost:8000/employees/${userId}`);
        // Обновляем список пользователей после удаления
        this.users = this.users.filter(user => user.id !== userId);
      } catch (error) {
        console.error('Ошибка при удалении сотрудника:', error);
        alert('Не удалось удалить сотрудника. Попробуйте еще раз позже.');
      }
    },
    
    goToUserDetail(userId) {
      if (parseInt(userId) === parseInt(this.currentUserId)) {
        this.$router.push({ name: 'Lk' }); // Переход на личный кабинет
      } else {
        this.$router.push({ name: 'UserDetail', params: { id: userId } }); // Переход на страницу деталей сотрудника
      }
    }
  }
}
</script>
<style scoped>
.user-list {
  padding: 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7f900;
  min-height: 100vh;
}

.user-list h1 {
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 600;
  color: #f6a400;
  text-align: center;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #6e6e6e;
}

.user-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.user-card {
  background-color: rgb(37, 47, 61);
  border: 1px solid #424242;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 240px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  position: relative;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.user-photo {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.user-info {
  padding: 15px;
  background: rgb(37, 47, 61);
}

.user-info h2 {
  margin: 10px 0;
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
}

.user-position {
  color: #888;
  font-size: 16px;
}

.no-users {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #666;
}

.delete-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #ff1a1a;
}
</style>
