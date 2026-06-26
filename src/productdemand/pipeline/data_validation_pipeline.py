import sys
from src.productdemand.config.configuration import ConfigurationManager
from src.productdemand.components.data_validation import DataValidation
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException

STAGE_NAME="data validation stage"

logger = get_logger(__name__)

class DataValidationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_validation(self):
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
            
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(data_validation_config)
            result = data_validation.validate_all_columns()
            
            logger.info(f"Validation Result:{result}")

            logger.info(f">>>>>> Stage {STAGE_NAME} completed successfully <<<<<<\n\nx==========x")

        except Exception as e:
            raise CustomException(e,sys)