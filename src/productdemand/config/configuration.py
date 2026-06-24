import sys
from pathlib import Path
from src.productdemand.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.productdemand.utils.common import read_yaml, create_directories
from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.entity.config_entity import DataIngestionConfig

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
