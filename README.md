# 🧠 AI Expense Tracker

An AI-powered Expense Tracker application built with **React (Frontend)**, **Flask (Backend)**, and a **Machine Learning model** for spending predictions. The app allows users to **track expenses**, **categorize spending**, and **get AI-driven financial insights**.

---

## 🚀 Features
- ✅ **Add & manage expenses** with category and date
- ✅ **AI predictions** for future spending trends
- ✅ **Visual analytics** with charts
- ✅ **Responsive React UI**
- ✅ **Flask REST API** for data handling
- ✅ **ML model** for expense prediction
- ✅ **Dockerized for easy deployment**

---

## 🛠 Tech Stack
- **Frontend:** React (Vite or CRA), Axios, TailwindCSS
- **Backend:** Flask (Python), Flask-RESTful
- **Database:** SQLite (can be swapped with PostgreSQL/MySQL)
- **Machine Learning:** Scikit-learn
- **Deployment:** Docker + Docker Compose (AWS-ready)
- **Optional:** Nginx reverse proxy for production

---

## 📂 Project Structure
AI-MonoRepo/
│
├── backend/
│ ├── app.py # Flask API
│ ├── requirements.txt # Python dependencies
│ ├── model.pkl # Trained ML model
│ ├── Dockerfile
│
├── frontend/
│ ├── src/
│ ├── package.json
│ ├── Dockerfile
│
├── docker-compose.yml
└── README.md

## 📂 Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py


## 📂 Frontend
cd frontend
npm install
npm start

UI runs on http://localhost:3000


## 🐳 Docker Deployment

Build and run both services using Docker Compose:

docker-compose up --build


Frontend → http://localhost:3000
Backend → http://localhost:5000

## 📦 Environment Variables

Create .env files in backend & frontend:

# backend/.env
FLASK_ENV=development
DATABASE_URL=sqlite:///expenses.db

# frontend/.env
REACT_APP_API_URL=http://localhost:5000