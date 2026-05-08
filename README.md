# 🚆 RailTrack AI — Railway Delay Prediction

A full-stack web application that tracks Indian trains in real time and predicts arrival delays at future stations using a trained XGBoost machine learning model.

![Tech Stack](https://img.shields.io/badge/React-19-blue?style=flat-square&logo=react)
![Tech Stack](https://img.shields.io/badge/Express-5-green?style=flat-square&logo=express)
![Tech Stack](https://img.shields.io/badge/XGBoost-ML-orange?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square&logo=python)

---

## Features

- **Live train tracking** via the RailRadar API
- **AI delay prediction** for future stations using XGBoost
- **Station-by-station timeline** showing scheduled, actual, and predicted times
- **Delay trend chart** visualising actual vs predicted delay across the route
- **Destination ETA** with current delay context
- **Station autocomplete** for route search

---

## Architecture

```
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│  React Frontend │──────▶│  Express.js Backend  │──────▶│  RailRadar API   │
│  (Vite + TW)    │◀──────│  (Node.js / port 5000│       │  (live data)     │
└─────────────────┘       └──────────┬───────────┘       └──────────────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  Python (XGBoost)    │
                          │  predict_xgb.py      │
                          │  best_model_v1.pkl   │
                          └──────────────────────┘
```

---

## ML Model

| Metric | Value |
|--------|-------|
| Algorithm | XGBoost Regressor |
| Training rows | ~22,000 |
| MAE | 5.34 min |
| RMSE | 9.00 min |
| R² Score | 0.76 |

**Target**: Delay delta at next station (minutes ahead/behind predicted).

**Key features**: `prev_delay_arrival`, `sequence`, `scheduled_hour`, `inter_station_scheduled_mins`, `dwell_time_scheduled_mins`, `day_of_week`, `platform_num`

---

## Getting Started

### Prerequisites

- Node.js ≥ 20
- Python ≥ 3.10
- pip packages: `xgboost`, `scikit-learn`, `pandas`, `joblib`

### 1. Clone the repo

```bash
git clone https://github.com/AniketSonar/RAILWAY-DELAY-PREDICTION.git
cd RAILWAY-DELAY-PREDICTION
```

### 2. Backend setup

```bash
cd backend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env and add your RAILRADAR_API_KEY

# Install Python dependencies
pip install xgboost scikit-learn pandas joblib

# Place your trained model at:
# backend/models/best_model_v1.pkl

npm start
```

### 3. Frontend setup

```bash
cd frontend
npm install

# Optional: set custom API URL
cp .env.example .env

npm run dev
```

The app runs at **http://localhost:5173**

---

## Project Structure

```
RAILWAY-DELAY-PREDICTION/
├── backend/
│   ├── server.js               # Express API server
│   ├── predict_xgb.py          # Python prediction script
│   ├── train_delay_delta_model.py  # Model training script
│   ├── validate_model.py       # Model validation
│   ├── models/
│   │   └── best_model_v1.pkl   # Trained XGBoost model (not in repo)
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx        # Train search
│   │   │   └── TrainDetails.jsx # Prediction results
│   │   └── components/
│   │       ├── Header.jsx
│   │       ├── TrainCard.jsx
│   │       ├── LiveStationTimeline.jsx
│   │       └── DelayTrendChart.jsx
│   └── .env.example
└── validate.txt                # Latest model metrics
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `PORT` | Server port (default: 5000) |
| `RAILRADAR_API_KEY` | Your RailRadar API key |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend URL (default: http://localhost:5000) |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/search-trains` | Find trains between two stations |
| POST | `/predict-future-stations` | Get live + predicted timeline |
| GET | `/search-stations?query=` | Autocomplete station search |

---

## Training Your Own Model

```bash
cd backend

# Make sure railway_ml_data.csv is present
python train_delay_delta_model.py

# Validate the model
python validate_model.py

# Move model to correct location
mv delay_delta_xgb_model.pkl models/best_model_v1.pkl
```

---
