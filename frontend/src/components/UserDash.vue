<script>
import axios from "axios";

export default {
  data() {
    return {
      fullname: ""
    };
  },
  async mounted() {
    const isAdmin = localStorage.getItem("is_admin") === "true";
    const fullname = localStorage.getItem("fullname");

    if (isAdmin || !fullname) {
      this.$router.push("/smartpark/login");
      return;
    }

    this.fullname = fullname;
  },
  methods: {
    handleLogout() {
      localStorage.removeItem("token");
      localStorage.removeItem("fullname");
      localStorage.removeItem("is_admin");
      this.$router.push("/");
    },
    async exportCSV() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.post("http://127.0.0.1:5000/api/export_csv", {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert(res.data.message || "Export started. You will receive the CSV soon.");
      } catch (err) {
        alert(err.response?.data?.message || "Failed to start export");
      }
    }
  }
};
</script>

<template>
  <div class="app-wrapper">
    <nav class="navbar navbar-expand-lg custom-navbar sticky-top">
      <div class="container-fluid">
        <b><span class="navbar-brand">SmartPark</span></b>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link fw-bold" to="/user/dashboard">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link fw-bold" to="/user/dashboard/summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-bold text-danger" href="javascript:void(0)" @click="handleLogout">Logout</a>
          </li>
          <li class="nav-item">
            <button class="btn btn-outline-info btn-sm fw-bold ms-2" @click="exportCSV">
              <i class="bi bi-download"></i> Export CSV
            </button>
          </li>
        </ul>
        <div class="d-flex align-items-center">
          <span class="fw-bold text-white me-2">Welcome, {{ fullname }}</span>
          <div
            class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-2"
            style="width: 45px; height: 45px; font-weight: bold; font-size: 18px;"
          >
            {{ fullname.split(" ").map(w => w[0]).join("").toUpperCase() }}
          </div>
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

.nav-item .btn-outline-info {
  margin-top: 5px;
  transition: all 0.2s ease;
}

.nav-item .btn-outline-info:hover {
  background-color: #38bdf8;
  color: rgb(42, 78, 145);
}
</style>
