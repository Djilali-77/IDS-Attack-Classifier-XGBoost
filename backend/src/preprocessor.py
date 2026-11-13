from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def encode_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Label"] = self.label_encoder.fit_transform(df["Label"])
        return df

    def split_features_and_target(self, df: pd.DataFrame):
        x = df.drop(columns=['Label'])
        y = df['Label']
        return x, y

    def scale_and_split(self, X: pd.DataFrame, y: pd.Series):

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test) 


        return X_train_scaled, X_test_scaled, y_train, y_test

    def drop_unnecessary_features(self, df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
        df = df.drop(columns_to_drop, axis=1)
        return df