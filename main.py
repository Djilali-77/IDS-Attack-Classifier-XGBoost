from src.data_loader import NetworkDataLoader
from src.preprocessor import DataPreprocessor
from src.models import IntrusionDetectionModels
from src.evaluate import ModelEvaluator

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
    # 3. Train model
    # ==========================================
    print("3. Training models... \n")

    ids_models = IntrusionDetectionModels()

    print("Training Random Forest... \n")
    ids_models.train_random_forest(X_train_scaled, y_train)

    print("Training XGBoost... \n")
    ids_models.train_xgboost(X_train_scaled, y_train)

    # ==========================================
    # 4. Prediction
    # ==========================================
    print("4. Evaluating models... \n")
    evaluator = ModelEvaluator()

    print("\n--- Random Forest Results --- \n")
    y_pred_rf = ids_models.predict_random_forest(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_rf)
    evaluator.get_confusion_matrix(y_test, y_pred_rf)
    evaluator.print_full_report(y_test, y_pred_rf)

    print("\n--- XGBoost Results --- \n")
    y_pred_xgb = ids_models.predict_xgboost(X_test_scaled)
    evaluator.evaluate(y_test, y_pred_xgb)
    evaluator.get_confusion_matrix(y_test, y_pred_xgb)
    evaluator.print_full_report(y_test, y_pred_xgb)

    ids_models.get_feature_importance("rf", X.columns)
    ids_models.get_feature_importance("xgb", X.columns)

if __name__ == "__main__":

    main()