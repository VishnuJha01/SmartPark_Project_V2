<script setup>
import { ref, onMounted, nextTick } from "vue";
import Chart from "chart.js/auto";

const summary = ref({
  total_lots: 0,
  total_spots: 0,
  available_spots: 0,
  occupied_spots: 0
});

let chartInstance = null;

const fetchSummary = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:5000/api/admin/dashboard", {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await response.json();
    summary.value = data;

    await nextTick();
    renderChart();
  } catch (error) {
    console.error("Error fetching summary:", error);
  }
};

const renderChart = () => {
  const ctx = document.getElementById("adminChart");
  if (!ctx) return;

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Total Lots", "Total Spots", "Available Spots", "Occupied Spots"],
      datasets: [
        {
          label: "Parking Summary",
          data: [
            summary.value.total_lots,
            summary.value.total_spots,
            summary.value.available_spots,
            summary.value.occupied_spots
          ],
          backgroundColor: ["#3b82f6", "#6366f1", "#22c55e", "#ef4444"]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Parking Summary Overview",
          color: "#ffffff"
        },
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          ticks: { color: "#ffffff" },
          grid: { color: "rgba(255,255,255,0.1)" }
        },
        y: {
          beginAtZero: true,
          ticks: { color: "#ffffff" },
          grid: { color: "rgba(255,255,255,0.1)" }
        }
      }
    }
  });
};

onMounted(fetchSummary);
</script>

<template>
  <div class="container">
    <div class="header">
      <h1><i class="bi bi-bar-chart-line"></i> Summary</h1>
    </div>

    <div class="cards">
      <div class="card">
        <h4>Total Lots</h4>
        <span class="badge total">{{ summary.total_lots }}</span>
      </div>
      <div class="card">
        <h4>Total Spots</h4>
        <span class="badge total">{{ summary.total_spots }}</span>
      </div>
      <div class="card">
        <h4>Available Spots</h4>
        <span class="badge available">{{ summary.available_spots }}</span>
      </div>
      <div class="card">
        <h4>Occupied Spots</h4>
        <span class="badge occupied">{{ summary.occupied_spots }}</span>
      </div>
    </div>

    <!-- Bar Chart -->
    <div class="chart-container">
      <canvas id="adminChart"></canvas>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1100px;
  margin: 40px auto;
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  color: white;
  background-color: #0f172a;
  padding: 40px;
  border-radius: 10px;
}


.header {
  border-left: 4px solid #3b82f6;
  padding-left: 10px;
  margin-bottom: 30px;
}

.header h2 {
  font-size: 24px;
  font-weight: bold;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
}


.cards {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}

.card {
  flex: 1 1 22%;
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: 0.3s ease;
}

.card:hover {
  transform: translateY(-3px);
  border-color: #3b82f6;
}

.card h4 {
  color: #cbd5e1;
  margin-bottom: 10px;
}

.badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: bold;
  color: white;
  font-size: 18px;
}

.badge.total {
  background-color: #3b82f6;
}

.badge.available {
  background-color: #22c55e;
}

.badge.occupied {
  background-color: #ef4444;
}

.chart-container {
  background-color: #1e293b;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #334155;
}
</style>
