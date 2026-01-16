# SmartPark_V2
## SmartPark Project - WSL Setup Commands

```bash
# Unzip and enter project folder
unzip SmartPark_23f3004186.zip
cd SmartPark

# ---------------------------
# Backend Setup & Start Flask App (Terminal 1)
# ---------------------------
cd backend
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python3 app.py  # Runs Flask backend at http://127.0.0.1:5000

# ---------------------------
# Start MailHog (Terminal 2)
# ---------------------------
mailhog  # Opens MailHog at http://localhost:8025

# ---------------------------
# Start Redis (Terminal 3)
# ---------------------------
redis-cli ping  # should return 'PONG'; if not running, use below command
redis-server

# ---------------------------
# Celery Worker (Terminal 4)
# ---------------------------
cd backend
source .env/bin/activate
celery -A app.celery worker --loglevel=info

# ---------------------------
# Celery Beat (Terminal 5)
# ---------------------------
cd backend
source .env/bin/activate
celery -A app.celery beat --loglevel=info

# ---------------------------
# Frontend Setup (Terminal 6)
# ---------------------------
cd frontend
npm install
npm run dev  # Starts frontend at http://localhost:5173
