<script>
import axios from "axios"

export default {
  data() {
    return {
      lots: [],
      error: "",
      success: "",

      name: "",
      address: "",
      price: "",
      total_spots: "",
      pin_code: "",


      editId: null,
      editName: "",
      editAddress: "",
      editPrice: "",
      editTotalSpots: "",
      editPinCode: "",


      viewSpots: [],
      viewLotName: ""
    }
  },
  methods: {
    async fetchLots() {
      try {
        const token = localStorage.getItem("token")
        const response = await axios.get("http://127.0.0.1:5000/api/parkinglots", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.lots = response.data
      } catch (err) {
        this.error = "Failed to load parking lots"
      }
    },

    async deleteLot(lotId) {
      if (!confirm("Are you sure you want to delete this lot?")) return
      try {
        const token = localStorage.getItem("token")
        await axios.delete(`http://127.0.0.1:5000/api/parkinglots/${lotId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.fetchLots()
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to delete parking lot"
        alert(this.error)
      }
    },

    async createLot() {
      this.error = ""
      this.success = ""
      try {
        const token = localStorage.getItem("token")
        await axios.post(
          "http://127.0.0.1:5000/api/parkinglots",
          {
            name: this.name,
            address: this.address,
            price: this.price,
            total_spots: this.total_spots,
            pin_code: this.pin_code
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )

        this.fetchLots()


        this.name = this.address = this.price = this.total_spots = this.pin_code = ""

        const modal = bootstrap.Modal.getInstance(document.getElementById("addLotModal"))
        modal.hide()
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to create parking lot"
      }
    },

    openEditModal(lot) {
      this.editId = lot.id
      this.editName = lot.name
      this.editAddress = lot.address
      this.editPrice = lot.price
      this.editTotalSpots = lot.total_spots
      this.editPinCode = lot.pin_code

      const modal = new bootstrap.Modal(document.getElementById("editLotModal"))
      modal.show()
    },

    async updateLot() {
      try {
        const token = localStorage.getItem("token")
        await axios.put(
          `http://127.0.0.1:5000/api/parkinglots/${this.editId}`,
          {
            name: this.editName,
            address: this.editAddress,
            price: this.editPrice,
            total_spots: this.editTotalSpots,
            pin_code: this.editPinCode
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )

        this.fetchLots()
        const modal = bootstrap.Modal.getInstance(document.getElementById("editLotModal"))
        modal.hide()
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to update parking lot"
      }
    },

    async viewLot(lotId, lotName) {
      this.error = ""
      this.viewSpots = []
      this.viewLotName = lotName

      try {
        const token = localStorage.getItem("token")
        const response = await axios.get(
          `http://127.0.0.1:5000/api/parkinglots/${lotId}/spots`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.viewSpots = response.data.spots

        const modal = new bootstrap.Modal(document.getElementById("viewSpotsModal"))
        modal.show()
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to load spots"
      }
    }
  },
  mounted() {
    this.fetchLots()
  }
}
</script>

<template>
  <div class="parkinglot-container">
    <div class="container mt-4">

      <div class="d-flex justify-content-between align-items-center mb-5 mt-2">
        <h4 class=" section-title fw-bold mb-0">
          <i class="bi bi-table"></i>
          Parking Lots Management</h4>
        <button
          class="btn btn-addlot d-flex align-items-center"
          data-bs-toggle="modal"
          data-bs-target="#addLotModal"
        >
          <i class="bi bi-geo-alt me-2"></i>
           Add Lot
        </button>
      </div>

      <div class="row g-4">
        <div class="col-md-4" v-for="lot in lots" :key="lot.id">
          <div class="card lot-card shadow-sm h-100">
            <div class="card-body">
              <h5 class="fw-bold"># {{ lot.name }}</h5>
              <b class="mb-1">
                <i class="bi bi-geo-alt"></i> {{ lot.address }}
              </b>
              <p class="mb-1">PIN: {{ lot.pin_code }}</p>
              <b class="mb-1 text-success">₹ {{ lot.price }}/hr</b>
              <p>
                <span class="badge bg-success me-2">
                  {{ lot.spots.filter(s => s.status === 'A').length }} Available
                </span>
                <span class="badge bg-danger me-2">
                  {{ lot.spots.filter(s => s.status === 'O').length }} Occupied
                </span>
                <span class="badge bg-secondary">
                  Total {{ lot.spots.length }}
                </span>
              </p>
              <div class="card-actions mt-3">
                <button
                  class="btn btn-outline-light btn-sm me-2"
                  @click="viewLot(lot.id, lot.name)"
                >
                  <i class="bi bi-eye"></i> View
                </button>

                <button
                  class="btn btn-outline-info btn-sm me-2"
                  @click="openEditModal(lot)"
                >
                  <i class="bi bi-pencil-square"></i> Edit
                </button>
                <button
                  class="btn btn-outline-danger btn-sm"
                  @click="deleteLot(lot.id)"
                >
                  <i class="bi bi-trash3"></i> Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Lot Modal -->
    <div class="modal fade" id="addLotModal" tabindex="-1" aria-labelledby="addLotModalLabel">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header position-relative">
            <h5 class="modal-title fw-bold position-absolute start-50 translate-middle-x ms-1" id="addLotModalLabel">
              <i class="bi bi-building-add"></i>
              New Parking Lot
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div v-if="error" class="alert alert-danger text-center fw-bold">{{ error }}</div>

          <div class="modal-body">
            <form @submit.prevent="createLot">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" id="name" required>
              </div>

              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea v-model="address" class="form-control" rows="2" id="address"></textarea>
              </div>

              <div class="row mb-3">
                <div class="col">
                  <label for="price" class="form-label">Price (₹)/Hrs</label>
                  <input v-model="price" type="number" class="form-control" id="price" required>
                </div>
                <div class="col">
                  <label for="total_spots" class="form-label">Total Spots</label>
                  <input v-model="total_spots" type="number" class="form-control" id="total_spots" required>
                </div>
              </div>

              <div class="mb-3">
                <label for="pin_code" class="form-label">Pincode</label>
                <input v-model="pin_code" type="number" class="form-control" id="pin_code" required>
              </div>

              <div class="d-flex justify-content-center gap-2">
                <button type="submit" class="btn btn-primary btn-lg px-5 mx-2 w-45">Add</button>
                <button type="button" class="btn btn-danger btn-lg px-5 mx-2 w-45" data-bs-dismiss="modal">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Lot Modal -->
    <div class="modal fade" id="editLotModal" tabindex="-1" aria-labelledby="editLotModalLabel">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header position-relative">
            <h5 class="modal-title fw-bold position-absolute start-50 translate-middle-x ms-1" id="editLotModalLabel">
              <i class="bi bi-pencil-square"></i>
              Edit Parking Lot
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>

          <div v-if="error" class="alert alert-danger text-center fw-bold">{{ error }}</div>
          <div class="modal-body">
            <form @submit.prevent="updateLot">
              <div class="mb-3">
                <label for="editName" class="form-label">Name</label>
                <input v-model="editName" type="text" class="form-control" id="editName" required>
              </div>

              <div class="mb-3">
                <label for="editAddress" class="form-label">Address</label>
                <textarea v-model="editAddress" class="form-control" rows="2" id="editAddress"></textarea>
              </div>

              <div class="row mb-3">
                <div class="col">
                  <label for="editPrice" class="form-label">Price (₹)/Hrs</label>
                  <input v-model="editPrice" type="number" class="form-control" id="editPrice" required>
                </div>
                <div class="col">
                  <label for="editTotalSpots" class="form-label">Total Spots</label>
                  <input v-model="editTotalSpots" type="number" class="form-control" id="editTotalSpots" required>
                </div>
              </div>

              <div class="mb-3">
                <label for="editPinCode" class="form-label">Pincode</label>
                <input v-model="editPinCode" type="number" class="form-control" id="editPinCode" required>
              </div>

              <div class="d-flex justify-content-center gap-2">
                <button type="submit" class="btn btn-primary btn-lg px-5 mx-2 w-45">Update</button>
                <button type="button" class="btn btn-danger btn-lg px-5 mx-2 w-45" data-bs-dismiss="modal">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

    <!-- View Spots Modal -->
    <div class="modal fade" id="viewSpotsModal" tabindex="-1" aria-labelledby="viewSpotsModalLabel">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header position-relative">
            <h5 class="modal-title fw-bold" id="viewSpotsModalLabel">
              <i class="bi bi-arrow-return-right"></i>
              Spots in {{ viewLotName }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="viewSpots.length === 0" class="text-center text-muted">
              No spots found.
            </div>
            <div v-else>
              <div class="row">
                <div
                  v-for="spot in viewSpots"
                  :key="spot.id"
                  class="col-3 mb-3"
                >
                  <div
                    class="p-3 rounded text-center fw-bold"
                    :class="spot.status === 'A' ? 'bg-success text-white' : 'bg-danger text-white'"
                  >
                  <i class="bi bi-taxi-front"></i>
                    {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Close</button>
          </div>
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
  padding-left: 10px;
}

.parkinglot-container {
  min-height: 100vh;
  background-color: #0f172a;
  padding: 30px;
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
}


h4 {
  font-size: 28px;
  color: #fff;
  letter-spacing: 1px;
  text-align: center;
  margin-bottom: 25px;
}


.lot-card {
  background-color: #1e293b;
  border: 2px solid #334155;
  border-radius: 14px;
  color: #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
  border-color: #64748b;
}


.card-actions .btn {
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.2s ease;
}
.card-actions .btn:hover {
  transform: scale(1.05);
}


.modal-content {
  background: linear-gradient(145deg, #1e293b, #0f172a);
  color: #e2e8f0;
  border-radius: 16px;
  border: 1px solid #334155;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
}


.modal-header {
  border-bottom: 1px solid #334155;
  background-color: #1e293b;
  color: #f8fafc;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}


.modal-header .btn-close {
  filter: invert(1);
}



.modal-title {
  font-size: 20px;
  font-weight: bold;
  color: #f1f5f9;
}


.modal-body .form-control,
.modal-body textarea {
  background-color: #0f172a;
  border: 1px solid #475569;
  color: #f1f5f9;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.modal-body .form-control:focus,
.modal-body textarea:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 6px rgba(96, 165, 250, 0.7);
  outline: none;
}


.modal-body .btn-primary {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border: none;
  font-weight: bold;
}

.modal-body .btn-primary:hover {
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  transform: scale(1.03);
}

.modal-body .btn-danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
  border: none;
  font-weight: bold;
}

.modal-body .btn-danger:hover {
  background: linear-gradient(90deg, #dc2626, #b91c1c);
  transform: scale(1.03);
}

.btn-addlot {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  padding: 10px 22px;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.btn-addlot:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}

.btn-addlot:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 3px 8px rgba(0,0,0,0.3);
}


</style>

