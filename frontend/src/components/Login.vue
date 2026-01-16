<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          email: this.email,
          password: this.password
        })

      
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem("fullname", response.data.fullname)
        localStorage.setItem('is_admin', response.data.is_admin ? 'true' : 'false')
        

      
        if (response.data.is_admin) {
          this.$router.push("/admin/dashboard")
        } else {
          this.$router.push("/user/dashboard")
        }

      } catch (err) {
        this.error = err.response?.data?.message || "Login failed"
      }
    }
  }
}
</script>



<template>
  <div class="login-container">
    <div class="card">
      <div class="card-body">
        <h3 class="text-center"><strong>Login</strong></h3>

        <form @submit.prevent="loginUser">
          <div class="mb-3 mt-3">
            <label class="form-label">Email:</label>
            <input v-model="email" type="email" class="form-control" placeholder="Enter email" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password:</label>
            <input v-model="password" type="password" class="form-control" placeholder="Enter password" required>
          </div>

          <div class="mb-3 text-center">
            <span class="me-2">Don't have an account?</span>
            <router-link to="/smartpark/register" class="btn register">
              Register
            </router-link>
          </div>

          <button type="submit" class="btn btn-primary d-flex align-items-center  justify-content-center gap-2">Login
          </button>

        </form>

        <p v-if="error" style="color:red; margin-top:10px;">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  background: url('../assets/login.png') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register {
  padding: 6px 16px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  background: linear-gradient(135deg, #0d81fd, #7b2ff7);
  color: #fff !important;
  border: none;
  transition: all 0.3s ease;
  display: inline-block;
}

.register:hover {
  background: linear-gradient(135deg, #7b2ff7, #0d81fd);
  box-shadow: 0 5px 15px rgba(13, 129, 253, 0.4);
  transform: scale(1.05);
}


.card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.form-label {
  font-weight: 500;
  color: #fff;
}

.form-control {
  border-radius: 10px;
  padding: 12px;
  font-size: 1rem;
  border: none;
  outline: none;

  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.form-control:focus {
  border: 2px solid #0d81fd;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 12px rgba(13, 129, 253, 0.7);
}


.btn-primary {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  background: linear-gradient(135deg, #0d81fd, #7b2ff7);
  color: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary:hover {
  transform: scale(1.03);
  box-shadow: 0 5px 20px rgba(123, 47, 247, 0.5);
}

</style>
