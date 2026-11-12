from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Network Intrusion Detection API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = joblib.load("saved_models/xgb_model.pkl")
    scaler = joblib.load("saved_models/preprocessor_scaler.pkl")
    encoder = joblib.load("saved_models/label_encoder.pkl")
    print("AI Models loaded successfully!")
except Exception as e:
    print(f"Error loading models. Make sure they exist in the 'saved_models' folder: {e}")

class NetworkTraffic(BaseModel):
    features: dict 


@app.get("/")
def health_check():
    return {"status": "success", "message": "Zero-Day API is running!"}


# 4. Endpoint (Prediction)
@app.post("/predict")
def predict_attack(data: NetworkTraffic):
    try:
        # 1. Convert dict to DataFrame
        df_input = pd.DataFrame([data.features])

        # 2. Scale features
        X_processed = scaler.transform(df_input)
        
        # 3. Predict (returns an array like [2])
        prediction_num = model.predict(X_processed)
        
        # 4. Decode to string name (inverse transform)
        attack_name = encoder.inverse_transform(prediction_num)[0]
        
        # 5. Return JSON
        return {"prediction": attack_name}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    