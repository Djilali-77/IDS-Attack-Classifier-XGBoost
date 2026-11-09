from src.data_loader import NetworkDataLoader
from src.preprocessor import DataPreprocessor
from sklearn.preprocessing import LabelEncoder
from src.models import IntrusionDetectionModels
from src.evaluate import ModelEvaluator
from src.tunnel import ModelTuner
import pandas as pd
import numpy as np

def main() :
    print("1. Loading and cleaning data... \n")
    DATA_DIR = './data/'
    loader = NetworkDataLoader(DATA_DIR)
    final_data = loader.get_clean_data()

    print(f"Data shape after cleaning: {final_data.shape} \n")

    # ==========================================
    # 2. Preprocessing
    # ==========================================
    print("2. Preprocessing data... \n")

    preprocessor = DataPreprocessor()
    df_encoded = preprocessor.encode_labels(final_data)

    columns_to_drop = ['Destination Port']
    new_df = preprocessor.drop_unnecessary_features(df_encoded, columns_to_drop)

    X, y = preprocessor.split_features_and_target(new_df)
    X_train_scaled, X_test_scaled, y_train, y_test = preprocessor.scale_and_split(X, y)

    print("Classes found:", preprocessor.label_encoder.classes_)

    # ==========================================
    # 3. Hyperparameter Tuning & Training
    # ==========================================
    print("3. Tuning models on a sample of data... \n")
    
    # 1. Sample Data
    X_sample = X_train_scaled[:50000]
    y_sample = y_train[:50000]
    
    tuner = ModelTuner()
    ids_models = IntrusionDetectionModels()
    
    # --- Tuning Random Forest (The Tank) ---
    print("Tuning Random Forest...")
    best_rf, rf_params = tuner.tune_random_forest(ids_models.rf_model, X_sample, y_sample)
    print(f"Best RF Parameters: {rf_params} \n")
    
    # --- Tuning XGBoost (The Strict Math Teacher) ---
    print("Tuning XGBoost...")
    unique_classes, counts = np.unique(y_sample, return_counts=True)
    valid_classes = unique_classes[counts >= 5]
    mask = np.isin(y_sample, valid_classes)
    
    X_sample_xgb = X_sample[mask]
    y_sample_xgb = y_sample[mask]
    
    temp_encoder = LabelEncoder()
    y_sample_xgb_encoded = temp_encoder.fit_transform(y_sample_xgb)
    
    _, xgb_params = tuner.tune_xgboost(ids_models.xgb_model, X_sample_xgb, y_sample_xgb_encoded)
    print(f"Best XGBoost Parameters: {xgb_params} \n")
    
    best_xgb = ids_models.xgb_model
    best_xgb.set_params(**xgb_params)
    
    # ==========================================
    # Retraining on FULL data
    # ==========================================
    print("Retraining the best models on the FULL training dataset... \n")
    best_rf.fit(X_train_scaled, y_train)
    best_xgb.fit(X_train_scaled, y_train)

    # ==========================================
    # 4. Prediction
    # ==========================================
    print("4. Evaluating models... \n")
    evaluator = ModelEvaluator()

    print("\n--- Random Forest Results --- \n")
    y_pred_rf = best_rf.predict(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_rf)
    evaluator.get_confusion_matrix(y_test, y_pred_rf)
    evaluator.print_full_report(y_test, y_pred_rf)

    print("\n--- XGBoost Results --- \n")
    y_pred_xgb = best_xgb.predict(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_xgb)
    evaluator.get_confusion_matrix(y_test, y_pred_xgb)
    evaluator.print_full_report(y_test, y_pred_xgb)

if __name__ == "__main__":

    main()