<script>
export default {
  data() {
    return {
      fullname: "",
    }
  },
  computed: {
    initials() {
      if (!this.fullname) return ""
      return this.fullname
        .split(" ")
        .map(word => word[0].toUpperCase())
        .join("")
    }
  },
  mounted() {
    const isAdmin = localStorage.getItem('is_admin') === 'true'
    const fullname = localStorage.getItem('fullname')

    if (!isAdmin || !fullname) {
      this.$router.push("/smartpark/login")
    } else {
      this.fullname = fullname
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token')
      localStorage.removeItem('fullname')
      localStorage.removeItem('is_admin')
      this.$router.push("/")
    }
  }
}

</script>

<template>
  <div class="app-wrapper">
    <nav class="navbar navbar-expand-lg custom-navbar sticky-top">
      <div class="container-fluid">
        <b><span class="navbar-brand">SmartPark</span></b>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <b><router-link class="nav-link" to="/admin/dashboard">Home</router-link></b>
          </li>
          <li class="nav-item">
            <b><router-link class="nav-link" to="/admin/dashboard/parkinglots">Parking Lot</router-link></b>
          </li>
          <li class="nav-item">
            <b><router-link class="nav-link" to="/admin/dashboard/users">Users</router-link></b>
          </li>
          <li class="nav-item">
            <b>
              <a class="nav-link text-danger" href="javascript:void(0)" @click="handleLogout">Logout</a>
            </b>
          </li>
        </ul>
        <div class="d-flex align-items-center">
          <div
            class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-2"
            style="width: 45px; height: 45px; font-weight: bold; font-size: 18px;"
          >
            {{ initials }}
          </div>
          <span class="fw-bold text-white">Hi! {{ fullname }}</span>
        </div>
      </div>
    </nav>

    <div class="page-body">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  background-color: #0f172a;
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
}


.page-body {
  padding: 20px;
}


.custom-navbar {
  background: linear-gradient(90deg, #1e293b, #0f172a);
  padding: 10px 20px;
}

.custom-navbar .navbar-brand {
  font-family: 'Times New Roman', Times, serif;
  font-size: 32px;
  color: #60a5fa;
}

.custom-navbar .nav-link {
  color: #e2e8f0;
  font-weight: 600;
  transition: color 0.2s ease;
}

.custom-navbar .nav-link:hover {
  color: #60a5fa;
}

.custom-navbar .nav-link.text-danger {
  color: #f87171 !important;
}
</style>