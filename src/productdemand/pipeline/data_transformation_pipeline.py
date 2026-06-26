import sys
from src.productdemand.config.configuration import ConfigurationManager
from src.productdemand.components.data_transformation import DataTransformation
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException

STAGE_NAME="data validation stage"

logger = get_logger(__name__)

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_transformation(self):
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
            
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()

            data_transformation = DataTransformation(
            config=data_transformation_config
        )

            data_transformation.initiate_data_transformation()
    
            logger.info(f">>>>>> Stage {STAGE_NAME} completed successfully <<<<<<\n\nx==========x")

        except Exception as e:
            raise CustomException(e,sys)