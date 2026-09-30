# MedRoute

A hospital recommendation system that combines predicted emergency-room wait times with real-world travel times to rank hospitals by estimated time-to-care.

## Stack

- **Frontend:** React, Next.js, TypeScript
- **Backend:** Python, FastAPI
- **Machine Learning:** scikit-learn, pandas
- **Routing:** Google Routes API
- **Caching:** AWS DynamoDB

## Project structure

```text
backend/
  app/
    main.py
    routes/
      recommend.py
    services/
      routing.py
      predictor.py
      ranking.py
      cache.py
    models/
      schemas.py
  ml/
    train.py
    preprocess.py
    model.pkl

frontend/
  app/
    page.tsx
  components/
    HospitalMap.tsx
    Recommendation.tsx

data/
  hospital_wait_times.csv
```

## Setup

### 1. Install backend dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Required variables:

| Variable | Description |
| --- | --- |
| `GOOGLE_ROUTES_API_KEY` | Google Routes API key |
| `AWS_REGION` | AWS region used by DynamoDB |
| `DYNAMODB_TABLE` | DynamoDB cache table name |

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

## Running

Start the backend:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

Start the frontend:

```bash
cd frontend
npm run dev
```

Frontend runs on:

```text
http://localhost:3000
```

## API

### `POST /recommend`

Ranks nearby hospitals using predicted wait time and driving time.

Example request:

```json
{
  "latitude": 42.3251,
  "longitude": -72.6412,
  "triage_level": "urgent"
}
```

Example response:

```json
{
  "recommendations": [
    {
      "hospital": "Cooley Dickinson Hospital",
      "distance_miles": 8.19,
      "drive_minutes": 15.3,
      "predicted_wait_minutes": 40.6,
      "time_to_care_minutes": 55.9
    }
  ]
}
```

## Recommendation pipeline

| Stage | Component | Description |
| --- | --- | --- |
| 1 | `routing.py` | Fetch hospital travel times from Google Routes |
| 2 | `cache.py` | Return cached routing data from DynamoDB when available |
| 3 | `predictor.py` | Predict hospital wait time from triage and hospital features |
| 4 | `ranking.py` | Compute drive time + predicted wait time |
| 5 | `recommend.py` | Return hospitals ranked by estimated time-to-care |

## Model evaluation

The model was trained on 5,000 hospital wait-time records using a 4,000 / 1,000 train-test split.

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Baseline | 34.45 | 46.61 | -0.000 |
| Linear Regression | 28.14 | 40.48 | 0.246 |
| Random Forest | 28.79 | 41.32 | 0.214 |
| Gradient Boosting | **28.08** | 40.70 | 0.238 |

Gradient Boosting was selected based on the lowest MAE.

## Evaluation

MedRoute was evaluated across 100 simulated patient scenarios.

```text
Nearest-hospital average time-to-care: 71.84 min
MedRoute average time-to-care:         71.76 min
Different hospital selected:           8%
```

The evaluation showed that the geographically nearest hospital was not always the fastest option, while also highlighting the importance of higher-quality real-time wait-time data.
