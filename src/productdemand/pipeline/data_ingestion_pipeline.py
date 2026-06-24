import sys
from src.productdemand.config.configuration import ConfigurationManager
from src.productdemand.components.data_ingestion import DataIngestion
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException

STAGE_NAME="data ingestion stage"
logger = get_logger(__name__)

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_ingestion(self):
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()
        
        logger.info(f">>>>>> Stage {STAGE_NAME} completed successfully <<<<<<\n\nx==========x")

