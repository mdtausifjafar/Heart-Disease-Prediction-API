# Heart Disease Prediction API

A FastAPI application that predicts the presence of heart disease using a Random Forest classifier trained on the Heart Disease Dataset. The app is fully Dockerized and deployable to Render.

---

## Project Structure

```
heart-disease-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI routes and app logic
│   └── schemas.py           # Pydantic input/output models
├── model/
│   └── heart_model.joblib   # Trained Random Forest pipeline
├── train_model.py           # Script to train and save the model
├── heart_disease_dataset.csv
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Model Details

| Property      | Value                                    |
| ------------- | ---------------------------------------- |
| Algorithm     | Random Forest Classifier                 |
| Pipeline      | StandardScaler → RandomForestClassifier |
| Dataset       | Heart Disease Dataset (1025 samples)     |
| Features      | 13 clinical features                     |
| Test Accuracy | 99%                                      |

---

## API Endpoints

| Method | Endpoint     | Description                            |
| ------ | ------------ | -------------------------------------- |
| GET    | `/health`  | Health check - confirms API is running |
| GET    | `/info`    | Model metadata and feature list        |
| POST   | `/predict` | Returns heart disease prediction       |
| GET    | `/docs`    | Swagger UI (interactive docs)          |

---

## Input Features

| Feature      | Type  | Description                                       |
| ------------ | ----- | ------------------------------------------------- |
| `age`      | int   | Age in years                                      |
| `sex`      | int   | 1 = male, 0 = female                              |
| `cp`       | int   | Chest pain type (0–3)                            |
| `trestbps` | int   | Resting blood pressure (mm Hg)                    |
| `chol`     | int   | Serum cholesterol (mg/dl)                         |
| `fbs`      | int   | Fasting blood sugar > 120 mg/dl (1=true, 0=false) |
| `restecg`  | int   | Resting ECG results (0, 1, 2)                     |
| `thalach`  | int   | Maximum heart rate achieved                       |
| `exang`    | int   | Exercise induced angina (1=yes, 0=no)             |
| `oldpeak`  | float | ST depression induced by exercise                 |
| `slope`    | int   | Slope of peak exercise ST segment (0–2)          |
| `ca`       | int   | Major vessels colored by flouroscopy (0–3)       |
| `thal`     | int   | 0 = normal, 1 = fixed defect, 2 = reversable      |

---

## Running Locally with Docker

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/heart-disease-api.git
cd heart-disease-api
```

### 2. Build the Docker image

```bash
docker-compose build
```

### 3. Start the container

```bash
docker-compose up
```

### 4. Open Swagger UI

Visit [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Test with curl

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 54, "sex": 1, "cp": 0, "trestbps": 125,
    "chol": 212, "fbs": 0, "restecg": 1, "thalach": 168,
    "exang": 0, "oldpeak": 1.0, "slope": 2, "ca": 2, "thal": 3
  }'
```

Expected response:

```json
{
  "heart_disease": false,
  "confidence": 0.97,
  "message": "No heart disease detected. Stay healthy!"
}
```

---

## Retraining the Model

If you want to retrain the model from scratch:

```bash
pip install -r requirements.txt
python train_model.py
```

This regenerates `model/heart_model.joblib`.

---

## Deploying to Render

1. Push this repository to GitHub.
2. Go to [https://render.com](https://render.com) and sign in.
3. Click **New → Web Service**.
4. Connect your GitHub repository.
5. Set the following:
   - **Environment**: Docker
   - **Build Command**: *(leave empty — Render uses the Dockerfile)*
   - **Start Command**: *(leave empty — defined in Dockerfile CMD)*
6. Click **Deploy**.
7. Once live, visit `https://YOUR-APP-NAME.onrender.com/docs` to test.

---

## Tech Stack

- **FastAPI** - web framework
- **scikit-learn** - model training
- **joblib** - model serialization
- **Docker** - containerization
- **Render** - cloud deployment
