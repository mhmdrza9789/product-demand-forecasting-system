import sys
from src.productdemand.exception.custom_exception import CustomException
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline


logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        data_ingestor = DataIngestionTrainingPipeline()
        data_ingestor.initiate_data_ingestion()
    except Exception as e:
        raise CustomException(e,sys)

