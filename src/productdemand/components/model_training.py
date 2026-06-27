import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.utils.common import save_json
from src.productdemand.entity.config_entity import ModelTrainerConfig

logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig):
        self.config = config

        self.models = {
            "LinearRegression": LinearRegression(),
            "RandomForestRegressor": RandomForestRegressor(
                random_state=42, n_jobs=2
            ),
            "XGBRegressor": XGBRegressor(
                random_state=42, verbosity=0, n_jobs=2
            ),
            "AdaBoostRegressor": AdaBoostRegressor(
                random_state=42
            )
        }

        # light param grid for laptop
        self.params = {
            "LinearRegression": {
                "fit_intercept": [True, False]
            },
            "RandomForestRegressor": {
                "n_estimators": [100],
                "max_depth": [10, None],
                "min_samples_split": [2, 5]
            },
            "XGBRegressor": {
                "n_estimators": [100],
                "max_depth": [3, 5],
                "learning_rate": [0.05, 0.1]
            },
            "AdaBoostRegressor": {
                "n_estimators": [50, 100],
                "learning_rate": [0.05, 0.1]
            }
        }

    def split_features_target(self, df: pd.DataFrame):
        X = df.drop(columns=[self.config.target_column], axis=1)
        y = df[self.config.target_column]
        return X, y

    def load_data(self):
        train_scaled = pd.read_csv(self.config.train_scaled_path)
        test_scaled = pd.read_csv(self.config.test_scaled_path)
        train_unscaled = pd.read_csv(self.config.train_unscaled_path)
        test_unscaled = pd.read_csv(self.config.test_unscaled_path)


        X_train_scaled, y_train = self.split_features_target(train_scaled)
        X_test_scaled, y_test = self.split_features_target(test_scaled)

        X_train_unscaled, _ = self.split_features_target(train_unscaled)
        X_test_unscaled, _ = self.split_features_target(test_unscaled)

        return (
            X_train_scaled,
            X_test_scaled,
            y_train,
            y_test,
            X_train_unscaled,
            X_test_unscaled
        )

    def get_data_for_model(
        self,
        model_name,
        X_train_scaled,
        X_test_scaled,
        X_train_unscaled,
        X_test_unscaled
    ):
        if model_name == "LinearRegression":
            return X_train_scaled, X_test_scaled
        return X_train_unscaled, X_test_unscaled

    def evaluate_predictions(self, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        return {
            "r2_score": float(r2),
            "mae": float(mae),
            "rmse": float(rmse)
        }


    def initiate_model_trainer(self):
        (
            X_train_scaled,
            X_test_scaled,
            y_train,
            y_test,
            X_train_unscaled,
            X_test_unscaled
        ) = self.load_data()

        results = {}
        best_model = None
        best_model_name = None
        best_score = -np.inf

        for model_name, model in self.models.items():
            print(f"\nTraining {model_name} ...")

            X_train_current, X_test_current = self.get_data_for_model(
                model_name,
                X_train_scaled,
                X_test_scaled,
                X_train_unscaled,
                X_test_unscaled
            )

            grid_search = GridSearchCV(
                estimator=model,
                param_grid=self.params[model_name],
                cv=3,
                scoring="r2",
                n_jobs=-1,
                verbose=1
            )

            grid_search.fit(X_train_current, y_train)

            best_estimator = grid_search.best_estimator_
            y_pred = best_estimator.predict(X_test_current)

            metrics = self.evaluate_predictions(y_test, y_pred)

            results[model_name] = {
                "best_params": grid_search.best_params_,
                "r2_score": metrics["r2_score"],
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "input_type": "scaled" if model_name == "LinearRegression" else "unscaled"
            }

            if metrics["r2_score"] > best_score:
                best_score = metrics["r2_score"]
                best_model = best_estimator
                best_model_name = model_name

        # save best model
        Path(self.config.trained_model_file_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_model, self.config.trained_model_file_path)

        results["best_model"] = {
            "model_name": best_model_name,
            "best_r2_score": float(best_score),
            "input_type": "scaled" if best_model_name == "LinearRegression" else "unscaled"
        }

        metadata = {
            "model_name": best_model_name,
            "target_column": self.config.target_column,
            "model_file_path": self.config.trained_model_file_path,
            "input_type": "scaled" if best_model_name == "LinearRegression" else "unscaled"
        }

        save_json(self.config.results_file_path, results)
        save_json(self.config.metadata_file_path, metadata)

        return results
