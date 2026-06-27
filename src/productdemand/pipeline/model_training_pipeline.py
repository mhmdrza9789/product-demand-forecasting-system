import sys
from src.productdemand.config.configuration import ConfigurationManager
from src.productdemand.components.model_training import ModelTrainer
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException

STAGE_NAME="model training stage"

logger = get_logger(__name__)

class ModelTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_model_training(self):
        try:
            logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
            
            config = ConfigurationManager()
            model_training_config = config.get_model_trainer_config()
            trainer = ModelTrainer(model_training_config)
            result = trainer.initiate_model_trainer()
            
            logger.info(f"Training Result:{result}")

            logger.info(f">>>>>> Stage {STAGE_NAME} completed successfully <<<<<<\n\nx==========x")

        except Exception as e:
            raise CustomException(e,sys)