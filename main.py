from src.productdemand.logger.custom_logger import get_logger

def main():
    logger = get_logger(__name__)

    logger.info("Data ingestion started")


if __name__ == "__main__":
    main()
