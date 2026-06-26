import sys
from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.productdemand.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.productdemand.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        data_ingestor = DataIngestionTrainingPipeline()
        data_ingestor.initiate_data_ingestion()
        
        data_validation = DataValidationTrainingPipeline()
        data_validation.initiate_data_validation()

        data_transformation = DataTransformationTrainingPipeline()
        data_transformation.initiate_data_transformation()

    except Exception as e:
        raise CustomException(e,sys)

