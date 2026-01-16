<script>
import axios from "axios";

export default {
  data() {
    return {
      lots: [],
      reservations: [],
      showModal: false,
      bookingLot: null,
      bookingSpotId: null,
      bookingPrice: null,
      vehicleNumber: "",
      showReleaseModal: false,
      releaseData: null
    };
  },
  async mounted() {
    await this.fetchLots();
    await this.fetchReservations();
  },
  methods: {
    async fetchLots() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/parkinglots", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.lots = res.data;
      } catch (err) {
        console.error("Error loading lots", err);
      }
    },

    async fetchReservations() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/user/reservations", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.reservations = res.data;
      } catch (err) {
        console.error("Error loading reservations", err);
      }
    },

    openBooking(lot) {
      const availableSpot = lot.spots.find(s => s.status === "A");
      if (!availableSpot) {
        alert("No available spots in this lot!");
        return;
      }
      this.bookingLot = lot;
      this.bookingSpotId = availableSpot.id;
      this.bookingPrice = lot.price;
      this.vehicleNumber = "";
      this.showModal = true;
    },

    async confirmBooking() {
      const token = localStorage.getItem("token");
      try {
        await axios.post(
          "http://127.0.0.1:5000/api/book",
          {
            lot_id: this.bookingLot.id,
            vehicle_number: this.vehicleNumber
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert("Booking Successful!");
        this.showModal = false;
        await this.fetchLots();
        await this.fetchReservations();
      } catch (err) {
        alert(err.response?.data?.message || "Booking Failed");
      }
    },

    openRelease(res) {
      this.releaseData = {
        id: res.id,
        lot_name: res.lot_name,
        lot_id: res.lot_id,
        parking_time: res.parking_timestamp,
        leaving_time: res.leaving_timestamp || new Date().toLocaleString([], { hour: "2-digit", minute: "2-digit" }),
        vehicle_number: res.vehicle_number,
        cost: res.cost
      };
      this.showReleaseModal = true;
    },

    async confirmRelease() {
      const token = localStorage.getItem("token");
      try {
        await axios.put(`http://127.0.0.1:5000/api/release/${this.releaseData.id}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Payment Successful!");
        this.showReleaseModal = false;
        await this.fetchLots();
        await this.fetchReservations();
      } catch (err) {
        alert(err.response?.data?.message || "Release Failed");
      }
    }
  }
};
</script>

<template>
  <div class="page-body">
    <div class="container py-4">
      <h3 class="section-title"><i class="bi bi-p-square"></i> Available Parkings</h3>
      <div class="row g-4">
        <div class="col-md-4" v-for="lot in lots" :key="lot.id">
          <div class="card shadow-sm h-100 lot-card">
            <div class="card-body">
              <h5 class="card-title fw-bold text-white">Lot #{{ lot.name }}</h5>
              <p class="mb-1"><i class="bi bi-geo-alt"></i> {{ lot.address }}, {{ lot.pin_code }}</p>
              <b class="mb-1 text-success">₹{{ lot.price }}/hr</b>
              <p>
                <span class="badge bg-success me-2">{{ lot.spots.filter(s => s.status === 'A').length }} Available</span>
                <span class="badge bg-danger me-2">{{ lot.spots.filter(s => s.status === 'O').length }} Occupied</span>
                <span class="badge bg-secondary">{{ lot.spots.length }} Total</span>
              </p>
              <button class="btn btn-primary w-100 rounded-pill mt-2" @click="openBooking(lot)">
                <i class="bi bi-bookmark-plus"></i> Book Spot
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Reservations -->
      <h3 class="section-title mt-5"><i class="bi bi-clock-history"></i> Recent Parkings</h3>
      <div class="table-responsive shadow-sm rounded mt-3 p-3 bg-dark">
        <table class="table table-hover align-middle text-center mb-0 recent-table">
          <thead>
            <tr>
              <th>Parking Name</th>
              <th>Parking Time</th>
              <th>Leaving Time</th>
              <th>Vehicle No.</th>
              <th>Cost</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in reservations" :key="res.id">
              <td><span class="badge bg-primary">#{{ res.lot_name }}</span></td>
              <td>{{ res.parking_timestamp }}</td>
              <td>{{ res.leaving_timestamp || '-' }}</td>
              <td>{{ res.vehicle_number }}</td>
              <td>₹{{ res.cost || '-' }}</td>
              <td>
                <button
                  class="btn btn-danger btn-sm rounded-pill"
                  @click="openRelease(res)"
                  :disabled="res.leaving_timestamp"
                >
                  <i class="bi bi-sign-no-parking-fill"></i>
                  {{ res.leaving_timestamp ? "Released" : "Parkout" }}
                </button>
              </td>
            </tr>
            <tr v-if="reservations.length === 0">
              <td colspan="6">No recent reservations found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showModal" class="modal-backdrop"></div>
    <div class="modal fade show" tabindex="-1" style="display: block;" v-if="showModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header position-relative">
            <h5 class="modal-title fw-bold position-absolute start-50 translate-middle-x">
              <i class="bi bi-book"></i> Book Parking Spot
            </h5>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">Lot ID</label>
                <input type="text" class="form-control" :value="bookingLot.id" readonly>
              </div>
              <div class="mb-3">
                <label class="form-label">Spot ID</label>
                <input type="text" class="form-control" :value="bookingSpotId" readonly>
              </div>
              <div class="mb-3">
                <label class="form-label">Price (₹)</label>
                <input type="text" class="form-control" :value="bookingPrice" readonly>
              </div>
              <div class="mb-3">
                <label class="form-label">Vehicle Number</label>
                <input type="text" class="form-control" v-model="vehicleNumber" style="text-transform: uppercase;" required>
              </div>
            </form>
          </div>
          <div class="d-flex justify-content-center gap-2">
            <button class="btn btn-primary btn-md custom-btn" @click="confirmBooking">Confirm</button>
            <button class="btn btn-danger btn-md custom-btn" @click="showModal=false">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Release Modal -->
    <div v-if="showReleaseModal" class="modal-backdrop"></div>
    <div class="modal fade show" tabindex="-1" style="display: block;" v-if="showReleaseModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header position-relative">
            <h5 class="modal-title fw-bold position-absolute start-50 translate-middle-x">
              <i class="bi bi-credit-card"></i> Payment Summary
            </h5>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3"><label class="form-label">Parking Name</label><input type="text" class="form-control" :value="releaseData.lot_name" readonly></div>
              <div class="mb-3"><label class="form-label">Lot ID</label><input type="text" class="form-control" :value="releaseData.lot_id" readonly></div>
              <div class="mb-3"><label class="form-label">Vehicle Number</label><input type="text" class="form-control" :value="releaseData.vehicle_number" readonly></div>
              <div class="mb-3"><label class="form-label">Total Duration</label><input type="text" class="form-control" :value="releaseData.parking_time + ' → ' + releaseData.leaving_time" readonly></div>
              <div class="mb-3"><label class="form-label">Total Price(₹)</label><input type="text" class="form-control" :value="releaseData.cost" readonly></div>
            </form>
          </div>
          <div class="d-flex justify-content-center gap-2">
            <button class="btn btn-primary btn-md custom-btn" @click="confirmRelease">Pay Now</button>
            <button class="btn btn-danger btn-md custom-btn" @click="showReleaseModal=false">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.page-body {
  min-height: 100vh;
  background-color: #0f172a;
  color: #e2e8f0;
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  padding: 20px;
}

.section-title {
  color: #60a5fa;
  font-weight: 600;
  margin-bottom: 20px;
}

.lot-card {
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border: none;
  border-radius: 15px;
  color: #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

.table {
  color: #e2e8f0;
}

.table thead {
  background-color: #1e293b;
}


.recent-table {
  width: 100%;
  background-color: #1e293b;
  color: #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.recent-table th {
  background-color: #0d6efd;
  color: #fff;
  font-weight: 600;
  padding: 12px 15px;
  text-align: center;
}

.recent-table td {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 10px 12px;
  text-align: center;
  border-top: 1px solid #334155;
}

.recent-table tbody tr:hover td {
  background-color: #334155;
  transition: background-color 0.2s ease;
}

.modal-content {
  background-color: #1e293b;
  color: #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.5);
}

.modal-header {
  border-bottom: 1px solid #334155;
  background-color: #0f172a;
  color: #60a5fa;
  text-align: center;
  padding: 15px;
}

.modal-title {
  font-weight: 600;
  font-size: 1.2rem;
}

.form-label {
  color: #93c5fd;
  font-weight: 500;
}

.form-control {
  background-color: #1e293b;
  border: 1px solid #334155;
  color: #e2e8f0;
  border-radius: 8px;
}

.form-control:focus {
  background-color: #1e293b;
  color: #fff;
  border-color: #3b82f6;
  box-shadow: 0 0 5px rgba(59,130,246,0.5);
}

.btn-primary {
  background-color: #3b82f6;
  border: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-danger {
  background-color: #ef4444;
  border: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-danger:hover {
  background-color: #dc2626;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(15, 23, 42, 0.85);
  z-index: 1040;
}

.modal .custom-btn {
  width: 130px;
  font-weight: 600;
}

.d-flex.justify-content-center.gap-2 {
  padding-bottom: 20px;
}

</style>
