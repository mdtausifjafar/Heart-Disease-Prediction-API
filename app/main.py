from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import joblib
import pandas as pd
import os

from app.schemas import HeartDiseaseInput, PredictionOutput

# Define the feature order so input matches what the model was trained on
FEATURE_ORDER = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal"
]

MODEL_TYPE = "Random Forest Classifier with StandardScaler pipeline"

# Load the model once at startup and keep it in memory
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = os.getenv("MODEL_PATH", "model/heart_model.joblib")
    # Load the saved model from disk
    model = joblib.load(model_path)
    yield
    # Nothing special needed on shutdown

# Initialize the FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="Predicts the presence of heart disease using a Random Forest classifier trained on the Heart Disease dataset.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", tags=["Status"])
def health_check():
    # Simple check to confirm the API is running and model is loaded
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/info", tags=["Status"])
def model_info():
    # Return metadata about the deployed model
    return {
        "model_type": MODEL_TYPE,
        "features": FEATURE_ORDER,
        "target": "heart_disease (true = disease present, false = disease absent)",
        "dataset": "Heart Disease Dataset (1025 samples, 13 features)",
        "trained_accuracy": "99.02%"
    }

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(data: HeartDiseaseInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    # Build a DataFrame with named columns so the model gets the same format it was trained on
    features = pd.DataFrame([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal
    ]], columns=FEATURE_ORDER)

    # Get prediction and probability from the model
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    # probability[1] is the confidence for disease being present
    confidence = float(probability[prediction])
    has_disease = bool(prediction == 1)

    message = (
        "Heart disease detected. Please consult a doctor."
        if has_disease
        else "No heart disease detected. Stay healthy!"
    )

    return PredictionOutput(
        heart_disease=has_disease,
        confidence=round(confidence, 4),
        message=message
    )
