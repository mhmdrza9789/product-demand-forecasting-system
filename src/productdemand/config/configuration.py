import sys
from pathlib import Path
from src.productdemand.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.productdemand.utils.common import read_yaml, create_directories
from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                                     DataTransformationConfig, ModelTrainerConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        try:
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            self.schema = read_yaml(schema_filepath)

             
            create_directories([Path(self.config.artifacts_root)])
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config.data_ingestion
            create_directories([Path(config.root_dir)])

            data_ingestion_config = DataIngestionConfig(
                root_dir=Path(config.root_dir),
                source_file=Path(config.source_file),
                local_data_file=Path(config.local_data_file)
            )

            return data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([Path(config.root_dir)])

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            status_file=Path(config.STATUS_FILE),
            data_file=Path(self.config.data_ingestion.local_data_file),
            all_schema=dict(schema),
        )

        return data_validation_config 


    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        schema = self.schema.TARGET_COLUMN

        create_directories([
            Path(config.root_dir),
            Path(config.regression_dir),
            Path(config.ensemble_dir),
            Path(config.lstm_dir)
        ])

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            regression_dir=Path(config.regression_dir),
            ensemble_dir=Path(config.ensemble_dir),
            lstm_dir=Path(config.lstm_dir),
            scaler_name=config.scaler_name,
            lstm_scaler_name=config.lstm_scaler_name,
            target_column=schema.name
        ) 

        return data_transformation_config 
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        schema = self.schema

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            
            root_dir=Path(config.root_dir),
            trained_model_file_path=Path(config.trained_model_file_path),
            results_file_path=Path(config.results_file_path),
            metadata_file_path=Path(config.metadata_file_path),

            train_scaled_path=Path(config.train_scaled_path),
            test_scaled_path=Path(config.test_scaled_path),

            train_unscaled_path=Path(config.train_unscaled_path),
            test_unscaled_path=Path(config.test_unscaled_path),

            target_column=schema.TARGET_COLUMN.name
        )

        return model_trainer_config
