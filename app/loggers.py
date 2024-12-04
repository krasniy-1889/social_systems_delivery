from loguru import logger


def set_logger(logger_name: str, level: str = "DEBUG"):
    """
    Настраивает логгер
    """
    logger.add(f"logs/{logger_name}.log", level=level)
