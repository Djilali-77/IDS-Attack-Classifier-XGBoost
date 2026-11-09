from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
import numpy as np

class ModelTuner:
    def __init__(self):
        pass

    def tune_random_forest(self, model, X_sample, y_sample):
        param_dist = {
            "n_estimators": [50, 100, 200],
            "max_depth": [10, 20, None],
            "min_samples_split": [2, 5, 10]
        }
        random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, cv=3, n_iter=5)
        random_search.n_jobs = -1
        random_search.fit(X_sample, y_sample)

        return random_search.best_estimator_, random_search.best_params_

    def tune_xgboost(self, model, X_sample, y_sample):
        param_dist = {
                "learning_rate" : [0.01, 0.1, 0.2],
                "max_depth" : [3, 6, 10],
                "subsample" : [0.8, 1.0]
            }
        random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, cv=3, n_iter=5)
        random_search.n_jobs = -1
        random_search.fit(X_sample, y_sample)
        
        return random_search.best_estimator_, random_search.best_params_