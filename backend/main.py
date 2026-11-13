from src.data_loader import NetworkDataLoader
from src.preprocessor import DataPreprocessor
from src.models import IntrusionDetectionModels
from src.evaluate import ModelEvaluator
from src.tuner import ModelTuner
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import os


def main():
    print("1. Loading and cleaning data...\n")
    # We run this script from the backend folder, so the data folder is one level up
    DATA_DIR = "../data/"
    loader = NetworkDataLoader(DATA_DIR)
    final_data = loader.get_clean_data()
    print(f"Data shape after cleaning: {final_data.shape}\n")

    print("2. Preprocessing data...\n")
    preprocessor = DataPreprocessor()
    df_encoded = preprocessor.encode_labels(final_data)

    # Destination Port is easy for an attacker to fake, so the model must not rely on it
    new_df = preprocessor.drop_unnecessary_features(df_encoded, ["Destination Port"])

    # Without the port, more rows become exact copies. Remove them so the
    # same row can't end up in both train and test.
    rows_before = len(new_df)
    new_df = new_df.drop_duplicates()
    print(f"Removed {rows_before - len(new_df)} duplicate rows\n")

    X, y = preprocessor.split_features_and_target(new_df)

    # Median of normal traffic for every feature.
    # The API uses it to fill the features the user does not type in.
    benign_id = preprocessor.label_encoder.transform(["BENIGN"])[0]
    benign_medians = X[y == benign_id].median()

    X_train_scaled, X_test_scaled, y_train, y_test = preprocessor.scale_and_split(X, y)
    class_names = preprocessor.label_encoder.classes_
    print("Classes found:", class_names)

    print("3. Tuning models on a sample of data...\n")
    X_sample = X_train_scaled[:50000]
    y_sample = y_train[:50000]

    tuner = ModelTuner()
    ids_models = IntrusionDetectionModels()

    print("Tuning Random Forest...")
    best_rf, rf_params = tuner.tune_random_forest(ids_models.rf_model, X_sample, y_sample)
    print(f"Best RF Parameters: {rf_params}\n")

    print("Tuning XGBoost...")
    # XGBoost needs every class in every fold, so drop classes with fewer than 5 rows here
    unique_classes, counts = np.unique(y_sample, return_counts=True)
    valid_classes = unique_classes[counts >= 5]
    mask = np.isin(y_sample, valid_classes)

    X_sample_xgb = X_sample[mask]
    y_sample_xgb = y_sample[mask]

    temp_encoder = LabelEncoder()
    y_sample_xgb_encoded = temp_encoder.fit_transform(y_sample_xgb)

    _, xgb_params = tuner.tune_xgboost(ids_models.xgb_model, X_sample_xgb, y_sample_xgb_encoded)
    print(f"Best XGBoost Parameters: {xgb_params}\n")

    best_xgb = ids_models.xgb_model
    best_xgb.set_params(**xgb_params)

    print("Retraining the best models on the FULL training set...\n")
    best_rf.fit(X_train_scaled, y_train)
    best_xgb.fit(X_train_scaled, y_train)

    os.makedirs("saved_models", exist_ok=True)
    joblib.dump(best_xgb, "saved_models/xgb_model.pkl")
    joblib.dump(preprocessor.scaler, "saved_models/preprocessor_scaler.pkl")
    joblib.dump(preprocessor.label_encoder, "saved_models/label_encoder.pkl")
    joblib.dump(benign_medians, "saved_models/benign_medians.pkl")

    print("4. Evaluating models...\n")
    evaluator = ModelEvaluator()

    print("--- Random Forest Results ---\n")
    y_pred_rf = best_rf.predict(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_rf)
    evaluator.get_confusion_matrix(y_test, y_pred_rf)
    evaluator.print_full_report(y_test, y_pred_rf, class_names)

    print("--- XGBoost Results ---\n")
    y_pred_xgb = best_xgb.predict(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_xgb)
    evaluator.get_confusion_matrix(y_test, y_pred_xgb)
    evaluator.print_full_report(y_test, y_pred_xgb, class_names)

    # Save which features matter most, we use this for the README
    importance = ids_models.get_feature_importance("xgb", list(X.columns))
    importance.to_csv("saved_models/feature_importance.csv")


if __name__ == "__main__":
    main()