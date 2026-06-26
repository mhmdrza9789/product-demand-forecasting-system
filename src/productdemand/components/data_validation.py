import pandas as pd
import sys

from src.productdemand.entity.config_entity import DataValidationConfig
from src.productdemand.logger.custom_logger import get_logger
from src.productdemand.exception.custom_exception import CustomException

logger = get_logger(__name__)


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True

            data = pd.read_csv(self.config.data_file, encoding="utf-8")
            all_cols = list(data.columns)
            all_schema_cols = list(self.config.all_schema.keys())

            missing_cols = [col for col in all_schema_cols if col not in all_cols]
            unexpected_cols = [col for col in all_cols if col not in all_schema_cols]

            if missing_cols or unexpected_cols:
                validation_status = False

            with open(self.config.status_file, "w", encoding="utf-8") as f:
                f.write(f"Validation status: {validation_status}\n")
                f.write(f"Missing columns: {missing_cols}\n")
                f.write(f"Unexpected columns: {unexpected_cols}\n")

            logger.info(f"validation status is {validation_status}")

            return validation_status

        except Exception as e:
            raise CustomException(e,sys)