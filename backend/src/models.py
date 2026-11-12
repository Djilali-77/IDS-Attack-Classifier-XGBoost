from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import pandas as pd
import numpy as np

class IntrusionDetectionModels:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.xgb_model = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1)

    def train_random_forest(self, X_train, y_train):
        return self.rf_model.fit(X_train, y_train)

    def train_xgboost(self, X_train, y_train):
        return self.xgb_model.fit(X_train, y_train)

    def predict_random_forest(self, X_test):
        return self.rf_model.predict(X_test)

    def predict_xgboost(self, X_test):
        return self.xgb_model.predict(X_test)

    def get_feature_importance(self, model_name: str, feature_names: list) -> pd.DataFrame:
        model_name = model_name.lower()
        if model_name == "rf":
            chosen_model = self.rf_model
        elif model_name == "xgb":
            chosen_model = self.xgb_model
        else:
            raise ValueError("Model not supported. Use 'rf' or 'xgb'")
        importances = pd.Series(chosen_model.feature_importances_, index=feature_names)
        sorting = importances.sort_values(ascending=False)
        print(f"10 important features : \n {sorting.head(10)} \n")
        return sorting.to_frame()
