import os
import sys
import shutil
from pathlib import Path
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.entity.config_entity import DataIngestionConfig

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> None:
        """
        Copies the source local dataset to the artifacts data ingestion directory.
        """
        try:
            source_path = Path(self.config.source_file)
            local_path = Path(self.config.local_data_file)

            
            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found at: {source_path.resolve()}")

          
            if not local_path.exists():
                logger.info("Copying local dataset to artifacts directory", 
                            source=str(source_path), 
                            destination=str(local_path))
                
                shutil.copy(src=source_path, dst=local_path)
                logger.info("Dataset ingested successfully", destination=str(local_path))
            else:
                logger.info("File already exists in ingestion directory, skipping copy", 
                            destination=str(local_path))

        except Exception as e:
            raise CustomException(e, sys)
