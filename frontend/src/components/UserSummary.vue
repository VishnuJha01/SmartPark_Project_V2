<script>
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';
Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default {
  name: "UserSummary",
  data() {
    return {
      summary: {
        total_bookings: 0,
        active_bookings: 0,
        completed_bookings: 0,
        total_spent: 0,
      },
      chart: null
    };
  },
  mounted() {
    this.fetchSummary();
  },
  methods: {
    async fetchSummary() {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch("http://127.0.0.1:5000/api/user/dashboard/summary", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        this.summary = data;
        this.renderChart();
      } catch (error) {
        console.error("Error fetching user summary:", error);
      }
    },
    renderChart() {
      if (this.chart) this.chart.destroy();

      const ctx = document.getElementById("userSummaryChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Total", "Active", "Completed", "Spent (₹)"],
          datasets: [
            {
              label: "User Summary",
              data: [
                this.summary.total_bookings,
                this.summary.active_bookings,
                this.summary.completed_bookings,
                this.summary.total_spent,
              ],
              backgroundColor: ["#3b82f6", "#6366f1", "#22c55e", "#ef4444"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            title: { display: true, text: "User Parking Summary", color: "#ffffff", font: { size: 16 } },
          },
          scales: {
            x: {
              ticks: { color: "#ffffff" },
              grid: { color: "rgba(255,255,255,0.1)" },
            },
            y: {
              beginAtZero: true,
              ticks: { color: "#ffffff" },
              grid: { color: "rgba(255,255,255,0.1)" },
            },
          },
        },
      });
    },
  },
};
</script>

<template>
  <div class="container">
    <div class="header">
      <h1><i class="bi bi-person-lines-fill"></i> User Summary</h1>
    </div>

    <div class="cards">
      <div class="card">
        <h4>Total Bookings</h4>
        <span class="badge total">{{ summary.total_bookings }}</span>
      </div>
      <div class="card">
        <h4>Active Bookings</h4>
        <span class="badge active">{{ summary.active_bookings }}</span>
      </div>
      <div class="card">
        <h4>Completed Bookings</h4>
        <span class="badge completed">{{ summary.completed_bookings }}</span>
      </div>
      <div class="card">
        <h4>Total Spent (₹)</h4>
        <span class="badge spent">{{ summary.total_spent }}</span>
      </div>
    </div>

    <div class="chart-container">
      <canvas id="userSummaryChart"></canvas>
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

.header h1 {
  font-size: 24px;
  font-weight: bold;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.card {
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

.badge.active {
  background-color: #6366f1;
}

.badge.completed {
  background-color: #22c55e;
}

.badge.spent {
  background-color: #ef4444;
}

.chart-container {
  background-color: #1e293b;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #334155;
}
</style>

