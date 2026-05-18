<template>
  <div class="users">
    <h2>用户列表</h2>
    <div v-if="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <table v-else class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>邮箱</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.created_at }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !error && users.length === 0">暂无用户数据</p>
  </div>
</template>

<script>
export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('/api/users')
        if (!response.ok) {
          throw new Error('获取用户列表失败')
        }
        const data = await response.json()
        this.users = data.users || []
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.users {
  padding: 20px;
}
.user-table {
  margin: 20px auto;
  border-collapse: collapse;
  width: 80%;
  max-width: 800px;
}
.user-table th,
.user-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.user-table th {
  background-color: #42b983;
  color: white;
}
.user-table tr:nth-child(even) {
  background-color: #f2f2f2;
}
.error {
  color: red;
}
</style>
