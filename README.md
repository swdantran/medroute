MedRoute
A hospital recommendation system that combines predicted emergency-room wait times with real-world travel times to rank hospitals by estimated time-to-care. Exposed through a FastAPI backend with a React/Next.js frontend.
Stack
- Frontend: React, Next.js, TypeScript
- API: FastAPI, Python
- ML: scikit-learn, pandas
- Routing: Google Routes API
- Caching: AWS DynamoDB
- Database / data: CSV-based training data + DynamoDB route cache
- Models: Linear Regression, Random Forest, Gradient Boosting
Project structure
backend/
  app/
    main.py              # FastAPI application
    routes/
      recommend.py       # POST /recommend
    services/
      routing.py         # Google Routes API integration
      predictor.py       # wait-time model inference
      ranking.py         # time-to-care ranking logic
      cache.py           # DynamoDB cache access
    models/
      schemas.py         # Pydantic request/response models

  ml/
    train.py             # train and evaluate regression models
    preprocess.py        # dataset preprocessing
    model.pkl            # serialized trained model

frontend/
  app/
    page.tsx             # main recommendation UI
  components/
    HospitalMap.tsx      # hospital map
    Recommendation.tsx   # ranked hospital results

data/
  hospital_wait_times.csv
Setup
1. Install backend dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Configure environment
cp .env.example .env
Required variables:
Variable	Description
GOOGLE_ROUTES_API_KEY	Google Routes API key
AWS_REGION	AWS region used by DynamoDB
DYNAMODB_TABLE	DynamoDB cache table name3. Install frontend dependencies
cd frontend
npm install
Running
Start the backend:
source .venv/bin/activate
uvicorn app.main:app --reload
Backend runs on:
http://localhost:8000
Start the frontend:
cd frontend
npm run dev
Frontend runs on:
http://localhost:3000
API
POST /recommend
Ranks nearby hospitals using predicted wait time and driving time.
Example request:
{
  "latitude": 42.3251,
  "longitude": -72.6412,
  "triage_level": "urgent"
}
Example response:
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
Recommendation pipeline
Stage	Component	Description
1	routing.py	Fetch nearby hospital travel times from Google Routes
2	cache.py	Return cached routing data from DynamoDB when available
3	predictor.py	Predict hospital wait time from triage and hospital features
4	ranking.py	Compute drive time + predicted wait time
5	recommend.py	Return hospitals ranked by estimated time-to-careModel evaluation
The model was trained on 5,000 hospital wait-time records using a 4,000 / 1,000 train-test split.
Model	MAE	RMSE	R²
Baseline	34.45	46.61	-0.000
Linear Regression	28.14	40.48	0.246
Random Forest	28.79	41.32	0.214
Gradient Boosting	28.08	40.70	0.238Gradient Boosting was selected based on the lowest validation MAE.
Evaluation
MedRoute was tested across 100 simulated patient scenarios.
Nearest-hospital avg. time-to-care: 71.84 min
MedRoute avg. time-to-care:         71.76 min
Different hospital selected:        8%
The results showed that the geographically nearest hospital was not always the fastest option, while also highlighting the importance of higher-quality real-time wait-time data for improving routing decisions.
