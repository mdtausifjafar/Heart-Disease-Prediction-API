import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load the dataset
df = pd.read_csv("heart_disease_dataset.csv")

# Separate features and target
X = df.drop("target", axis=1)
y = df["target"]

# Split into train and test sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Build a pipeline: scale features then train Random Forest
# Scaling helps even for tree models when used in a pipeline with other tools
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        class_weight="balanced",  # handles any class imbalance
        random_state=42
    ))
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate on test set to verify it works
y_pred = pipeline.predict(X_test)
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["No Disease", "Disease"]))

# Save the trained pipeline to disk
os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/heart_model.joblib")
print("\nModel saved to model/heart_model.joblib")
