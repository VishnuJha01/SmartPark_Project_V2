<template>
  <div class="base-container">
    <nav class="navbar navbar-expand-lg navbar-dark custom-navbar">
      <div class="container-fluid">
        <a class="navbar-brand brand-text" href="/">SmartPark</a>

        <div class="navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item"><a class="nav-link" href="#">About</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Contact</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Privacy</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Terms</a></li>
          </ul>
          <div class="d-flex">
            <router-link to="/smartpark/login" class="btn btn-login me-2">Login</router-link>
            <router-link to="/smartpark/register" class="btn btn-signup">Sign up for free</router-link>
          </div>
        </div>
      </div>
    </nav>


    <div class="container centered-container">
      <div class="card p-5 text-center fade-in">
        <h1 class="mb-3 title"><strong>SmartPark<span class="highlight">.com</span></strong></h1>
        <p class="mb-4 subtitle">
          Finding parking shouldn't be a hassle.<br />
          Let's get you parked and on to the bigger things.
        </p>
        <div class="button">
          <router-link to="/smartpark/login" class="btn start-btn">
            <strong>Get Started</strong>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.base-container {
  background: linear-gradient(
      rgba(0, 0, 0, 0.4),
      rgba(0, 0, 0, 0.6)
    ),
    url('../assets/base.jpg') no-repeat center center fixed;
  background-size: cover;
  height: 100vh;
  margin: 0;
}


.custom-navbar {
  background: rgba(30, 30, 30, 0.9);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  padding: 0.6rem 1.5rem;
  position: fixed;
  width: 100%;
  z-index: 100;
}

.brand-text {
  color: #fff !important;
  font-weight: 600;
  font-size: 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 6px 14px;
  border-radius: 20px;
  background: linear-gradient(145deg, #1c1c1c, #2a2a2a);
  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.05);
}

.navbar-nav .nav-link {
  color: #ddd !important;
  font-weight: 500;
  margin-right: 15px;
  transition: color 0.3s ease;
}

.navbar-nav .nav-link:hover {
  color: #ff7b00 !important;
}


.btn-login {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border-radius: 20px;
  padding: 6px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.25);
}

.btn-signup {
  background: linear-gradient(135deg, #ff7b00, #ffb347);
  color: #000000;
  border-radius: 20px;
  padding: 6px 18px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-signup:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 123, 0, 0.6);
}


.centered-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 80px;
}

.card {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 1rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
  color: #fff;
  animation: slide-up 1s ease forwards;
}

.title {
  font-family: 'Times New Roman', Times, serif;
  font-weight: 700;
  font-size: 2.5rem;
}

.highlight {
  color: #ff7b00;
}

.subtitle {
  font-family: 'Work Sans', sans-serif;
  font-weight: 300;
  font-size: 1.1rem;
  opacity: 0.9;
}

.start-btn {
  background: linear-gradient(135deg, #ff7b00, #ffb347);
  color: white !important;
  padding: 0.7rem 2.2rem;
  border-radius: 12px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.05rem;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(255, 123, 0, 0.5);
}

.start-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 20px rgba(255, 140, 0, 0.8);
}
</style>
