import os, sys
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler

from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.entity.config_entity import DataTransformationConfig

logger = get_logger(__name__)

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_validation_status(self) -> bool:
        """
        
        """
        try:
            status_path = Path("artifacts/data_validation/status.txt")
            if not status_path.exists():
                logger.info(f"Error: Status file not found at {status_path}")
                return False
            
            with open(status_path, "r") as f:
                
                first_line = f.readline()
                status = first_line.split(":")[1].strip().lower()
                
            return status == "true"
        except Exception as e:
            logger.info(f"Error reading validation status: {e}")
            return False

    def clean_target_column(self, df: pd.DataFrame) -> pd.DataFrame:
        target = self.config.target_column

        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in dataframe")

        df[target] = df[target].astype(str)

        
        df[target] = df[target].str.replace("(", "-", regex=False)
        df[target] = df[target].str.replace(")", "", regex=False)

        
        df[target] = df[target].str.replace(",", "", regex=False)
        df[target] = df[target].str.strip()

        df[target] = pd.to_numeric(df[target], errors="coerce")

        return df

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        if "Date" not in df.columns:
            raise ValueError("Date column not found in dataframe")

        df = df.copy()

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        df = df.sort_values("Date").reset_index(drop=True)

        df["year"] = df["Date"].dt.year
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["dayofweek"] = df["Date"].dt.dayofweek
        df["weekofyear"] = df["Date"].dt.isocalendar().week.astype(int)

        df.drop(columns=["Date"], inplace=True)

        return df


    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        target = self.config.target_column

        
        df = df.dropna(subset=[target])

        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        
        object_cols = df.select_dtypes(include=["object"]).columns
        for col in object_cols:
            if df[col].mode().empty:
                df[col] = df[col].fillna("Unknown")
            else:
                df[col] = df[col].fillna(df[col].mode()[0])

        return df

    def handle_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        object_cols = df.select_dtypes(include=["object"]).columns

        label_encoders = {}

        for col in object_cols:
            encoder = LabelEncoder()
            df[col] = df[col].astype(str)
            df[col] = encoder.fit_transform(df[col])
            label_encoders[col] = encoder

        encoder_path = os.path.join(self.config.root_dir, "label_encoders.pkl")
        joblib.dump(label_encoders, encoder_path)

        return df

    def create_sequences(self, data: np.ndarray, window_size: int = 30):
        X, y = [], []

        for i in range(len(data) - window_size):
            X.append(data[i:i + window_size, :-1])
            y.append(data[i + window_size, -1])

        return np.array(X), np.array(y)

    def save_regression_data(self, train: pd.DataFrame, test: pd.DataFrame):
        target = self.config.target_column

        X_train = train.drop(columns=[target])
        y_train = train[target]

        X_test = test.drop(columns=[target])
        y_test = test[target]

        
        X_train = X_train.select_dtypes(include=[np.number])
        X_test = X_test[X_train.columns]

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        joblib.dump(
            scaler,
            os.path.join(self.config.root_dir, self.config.scaler_name)
        )

        train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        train_scaled[target] = y_train.values

        test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
        test_scaled[target] = y_test.values

        train_scaled.to_csv(
            os.path.join(self.config.regression_dir, "train.csv"),
            index=False
        )

        test_scaled.to_csv(
            os.path.join(self.config.regression_dir, "test.csv"),
            index=False
        )

    def save_ensemble_data(self, train: pd.DataFrame, test: pd.DataFrame):
        train.to_csv(
            os.path.join(self.config.ensemble_dir, "train.csv"),
            index=False
        )

        test.to_csv(
            os.path.join(self.config.ensemble_dir, "test.csv"),
            index=False
        )

    def save_lstm_data(self, df: pd.DataFrame, window_size: int = 30):
        target = self.config.target_column

        lstm_df = df.copy()

        if "Date" in lstm_df.columns:
            lstm_df = lstm_df.drop(columns=["Date"])

        
        feature_cols = [col for col in lstm_df.columns if col != target]
        lstm_df = lstm_df[feature_cols + [target]]

        lstm_df = lstm_df.select_dtypes(include=[np.number])

        if target not in lstm_df.columns:
            raise ValueError(f"Target column '{target}' removed during numeric selection")

        split_index = int(len(lstm_df) * 0.8)

        train_lstm_df = lstm_df.iloc[:split_index]
        test_lstm_df = lstm_df.iloc[split_index:]

        lstm_scaler = MinMaxScaler()

        train_scaled = lstm_scaler.fit_transform(train_lstm_df)
        test_scaled = lstm_scaler.transform(test_lstm_df)

        joblib.dump(
            lstm_scaler,
            os.path.join(self.config.root_dir, self.config.lstm_scaler_name)
        )

        X_train_lstm, y_train_lstm = self.create_sequences(
            train_scaled,
            window_size=window_size
        )

        X_test_lstm, y_test_lstm = self.create_sequences(
            test_scaled,
            window_size=window_size
        )

        np.save(os.path.join(self.config.lstm_dir, "X_train.npy"), X_train_lstm)
        np.save(os.path.join(self.config.lstm_dir, "X_test.npy"), X_test_lstm)
        np.save(os.path.join(self.config.lstm_dir, "y_train.npy"), y_train_lstm)
        np.save(os.path.join(self.config.lstm_dir, "y_test.npy"), y_test_lstm)

        print("LSTM data saved successfully.")
        print(f"X_train_lstm shape: {X_train_lstm.shape}")
        print(f"X_test_lstm shape: {X_test_lstm.shape}")
        print(f"y_train_lstm shape: {y_train_lstm.shape}")
        print(f"y_test_lstm shape: {y_test_lstm.shape}")

    def initiate_data_transformation(self):

        if not self.get_validation_status():
            message = "CRITICAL: Data Validation failed. Transformation aborted."
            logger.info(message)
            return message

        try:
            logger.info("Validation PASSED. Starting Transformation...")
            
            
            df = pd.read_csv(self.config.data_path)
            
            
            df = self.clean_target_column(df)
            df = self.feature_engineering(df)
            df = self.handle_missing_values(df)
            df = self.handle_encoding(df)

            
            train, test = train_test_split(df, test_size=0.2, shuffle=False)

           
            self.save_regression_data(train, test)
            self.save_ensemble_data(train, test)
            self.save_lstm_data(df)

            logger.info("Transformation Pipeline completed successfully.")
            
        except Exception as e:
            raise CustomException(e,sys)

        
