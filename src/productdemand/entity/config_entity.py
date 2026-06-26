from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_file: Path
    local_data_file: Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    status_file: Path
    data_file: Path
    all_schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    regression_dir: Path
    ensemble_dir: Path
    lstm_dir: Path
    scaler_name: str
    lstm_scaler_name: str
    target_column: str