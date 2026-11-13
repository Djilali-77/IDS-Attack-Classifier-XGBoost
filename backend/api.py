from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="IDS Attack Classifier API", version="1.0")

# Only our own frontend can call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# No try/except here on purpose: if a file is missing, the app should stop
# right away instead of starting in a broken state.
model = joblib.load("saved_models/xgb_model.pkl")
scaler = joblib.load("saved_models/preprocessor_scaler.pkl")
encoder = joblib.load("saved_models/label_encoder.pkl")
benign_medians = joblib.load("saved_models/benign_medians.pkl")

# The exact feature names, in the exact order used during training
FEATURE_NAMES = list(benign_medians.index)
print("Models loaded successfully!")


class NetworkTraffic(BaseModel):
    features: dict


def predict_flows(df: pd.DataFrame) -> np.ndarray:
    """Takes a DataFrame that has all the features and returns the attack names."""
    X_scaled = scaler.transform(df[FEATURE_NAMES])
    predictions = model.predict(X_scaled)
    return encoder.inverse_transform(predictions)


@app.get("/")
def health_check():
    return {"status": "success", "message": "IDS Attack Classifier API is running!"}


@app.post("/predict")
def predict_attack(data: NetworkTraffic):
    unknown = [name for name in data.features if name not in FEATURE_NAMES]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown features: {unknown}")

    # Start from a normal flow, then overwrite it with what the user typed
    row = benign_medians.copy()
    for name, value in data.features.items():
        row[name] = value
    df_input = pd.DataFrame([row])

    attack_name = predict_flows(df_input)[0]

    if attack_name == "BENIGN":
        return {"status": "success", "message": "NORMAL TRAFFIC", "prediction": attack_name}
    return {"status": "danger", "message": f"ATTACK DETECTED: {attack_name}", "prediction": attack_name}


@app.post("/predict-batch")
def predict_batch(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the file as a CSV.")

    # CICIDS2017 column names often have extra spaces around them
    df.columns = df.columns.str.strip()

    missing = [name for name in FEATURE_NAMES if name not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"CSV is missing columns: {missing[:5]}")

    # Keep only the model features (this also drops Label and Destination Port)
    df = df[FEATURE_NAMES]

    # Infinite values become missing, then we fill them with the normal-traffic median
    df = df.replace([np.inf, -np.inf], np.nan).fillna(benign_medians)

    attack_names = predict_flows(df)
    counts = pd.Series(attack_names).value_counts()
    total = len(attack_names)
    attacks = total - int(counts.get("BENIGN", 0))

    return {
        "status": "danger" if attacks > 0 else "success",
        "message": f"Scanned {total} flows, found {attacks} attacks",
        "total_scanned": total,
        "attacks_found": attacks,
        "breakdown": {name: int(count) for name, count in counts.items()},
    }