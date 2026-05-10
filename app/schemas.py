from pydantic import BaseModel, Field

class HeartDiseaseInput(BaseModel):
    age: int = Field(..., description="Age in years", example=54)
    sex: int = Field(..., description="Sex (1 = male, 0 = female)", example=1)
    cp: int = Field(..., description="Chest pain type (0-3)", example=0)
    trestbps: int = Field(..., description="Resting blood pressure in mm Hg", example=125)
    chol: int = Field(..., description="Serum cholesterol in mg/dl", example=212)
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)", example=0)
    restecg: int = Field(..., description="Resting ECG results (0, 1, 2)", example=1)
    thalach: int = Field(..., description="Maximum heart rate achieved", example=168)
    exang: int = Field(..., description="Exercise induced angina (1 = yes, 0 = no)", example=0)
    oldpeak: float = Field(..., description="ST depression induced by exercise relative to rest", example=1.0)
    slope: int = Field(..., description="Slope of the peak exercise ST segment (0-2)", example=2)
    ca: int = Field(..., description="Number of major vessels colored by flouroscopy (0-3)", example=2)
    thal: int = Field(..., description="Thal (0 = normal, 1 = fixed defect, 2 = reversable defect)", example=3)

class PredictionOutput(BaseModel):
    heart_disease: bool
    confidence: float
    message: str
