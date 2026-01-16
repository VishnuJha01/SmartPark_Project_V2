<script>
import axios from "axios"

export default {
  data() {
    return {
      users: [],
      selectedUser: null,
      showDetails: false
    }
  },
  async mounted() {
    const token = localStorage.getItem("token")
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/users", {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.users = res.data
    } catch (err) {
      console.error("Error loading users:", err.response?.data || err.message)
    }
  },
  methods: {
    async viewDetails(userId) {
      const token = localStorage.getItem("token")
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.selectedUser = res.data
        this.showDetails = true
      } catch (err) {
        console.error("Error fetching details:", err.response?.data || err.message)
      }
    },
    closeDetails() {
      this.showDetails = false
      this.selectedUser = null
    }
  }
}
</script>

<template>
  <div class="container py-4">
    <h3 class="section-title">
      <i class="bi bi-people-fill me-2"></i>
      Users
    </h3>
    <div class="table-responsive shadow-lg rounded mt-3 p-3 recent-table-wrapper">
      <table class="table table-hover align-middle mb-0 recent-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Address</th>
            <th>Pin Code</th>
            <th>Role</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td class="fw-semibold">{{ user.fullname }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.pin_code }}</td>
            <td>
              <span 
                class="badge role-badge"
                :class="user.is_admin ? 'bg-danger' : 'bg-success'"
              >
                {{ user.is_admin ? 'Admin' : 'User' }}
              </span>
            </td>
            <td>
              <button class="btn btn-details" @click="viewDetails(user.id)">
                <i class="bi bi-eye me-1"></i> See Details
              </button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="7" class="py-3 text-center">No users found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- User Details -->
    <div v-if="showDetails" class="details-overlay">
      <div class="details-card position-relative">
        <button type="button" class="btn-close btn-close-white position-absolute top-0 end-0 m-3" aria-label="Close" @click="closeDetails"></button>
        
        <h4 class="mb-3"><i class="bi bi-person-circle me-2"></i>{{ selectedUser.fullname }}</h4>
        <p><strong><i class="bi bi-envelope-arrow-down-fill me-2"></i>Email:</strong> {{ selectedUser.email }}</p>
        <p><strong><i class="bi bi-house-door-fill me-2"></i>Address:</strong> {{ selectedUser.address }}</p>
        <p><strong>Pin Code:</strong> {{ selectedUser.pin_code }}</p>

        <h5 class="mt-4 mb-2">Booking History</h5>
        <div v-if="selectedUser.booking_history.length > 0">
          <table class="table table-sm table-bordered text-light">
            <thead>
              <tr>
                <th>Lot</th>
                <th>Vehicle</th>
                <th>Parking Time</th>
                <th>Parkout Time</th>
                <th>Cost</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in selectedUser.booking_history" :key="b.reservation_id">
                <td>{{ b.lot_name }}</td>
                <td>{{ b.vehicle_number }}</td>
                <td>{{ b.parking_timestamp }}</td>
                <td>
                  <span v-if="!b.leaving_timestamp" class="badge bg-success">Active</span>
                  <span v-else>{{ b.leaving_timestamp }}</span>
                </td>
                <td>₹{{ b.parking_cost }}</td>
              </tr>

            </tbody>
          </table>
        </div>
        <p v-else><i class="bi bi-emoji-frown me-2"></i>No booking history found!</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.section-title {
  font-weight: bold;
  color: #e2e8f0;
  margin-bottom: 20px;
  border-left: 5px solid #0d6efd;
  padding-left: 12px;
  font-size: 1.75rem;
}


.recent-table-wrapper {
  background-color: #1e293b;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}


.recent-table {
  color: #e2e8f0;
  table-layout: fixed;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.recent-table th {
  background-color: #0d6efd;
  color: #fff;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  padding: 10px 8px;
  white-space: nowrap;
}

.recent-table td {
  background-color: #1e293b;
  color: #e2e8f0;
  vertical-align: middle;
  padding: 10px 8px;
  font-size: 0.9rem;
  border-top: 1px solid #334155;
}

.recent-table tbody tr:hover td {
  background-color: #334155;
  transition: background-color 0.2s ease-in-out;
}


.role-badge {
  font-size: 0.75rem;
  padding: 5px 10px;
  border-radius: 20px;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}


.btn-details {
  background: linear-gradient(135deg, #0d6efd, #0a58ca);
  color: #fff;
  font-size: 0.8rem;
  font-weight: 500;
  border: none;
  border-radius: 18px;
  padding: 5px 12px;
  transition: all 0.2s ease-in-out;
}
.btn-details:hover {
  background: linear-gradient(135deg, #0a58ca, #084298);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.3);
}


.details-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(2px);
}


.details-card {
  background-color: #0f172a;
  color: #e2e8f0;
  border-radius: 16px;
  padding: 30px;
  width: 90%;
  max-width: 650px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.5);
  animation: fadeIn 0.3s ease;
  border: 1px solid #334155;
}


.details-card h4 {
  font-weight: 700;
  color: #60a5fa;
  border-bottom: 2px solid #1e3a8a;
  padding-bottom: 8px;
  margin-bottom: 15px;
}


.details-card p {
  margin: 6px 0;
  font-size: 0.95rem;
}
.details-card strong {
  color: #93c5fd;
}


.details-card table {
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.details-card th {
  background-color: #1e3a8a;
  color: #fff;
  font-size: 0.85rem;
  text-transform: uppercase;
  padding: 8px;
}
.details-card td {
  background-color: #1e293b;
  color: #e2e8f0;
  font-size: 0.9rem;
  padding: 8px;
  text-align: center;
}

/* Close Button */
.details-card .btn-secondary {
  background-color: #475569;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 20px;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}
.details-card .btn-secondary:hover {
  background-color: #334155;
  transform: translateY(-1px);
}


@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
