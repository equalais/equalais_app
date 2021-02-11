"""Standardized logging configuration."""
import logging.config
from logging import Logger

LOGGING_CONFIG_STDOUT = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr; stderr causes Azure releases to fail
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def get_main_logger(
    repo_acronym: str, module_name: str, descriptor: str = None
) -> Logger:
    """Returns a standard configured logger used in __main__ module scripts.

    Args:
        repo_acronym (str): Acronym of repository using logger (e.g., "m3")
        module_name (str): Name of module using logger (e.g., preprocess, train, score)
        descriptor (str, optional): Descriptor for distinguishing modules (e.g., evaluation).
            Defaults to None.

    Returns:
        Logger: Logging object for logging to stdout.
    """
    logging.config.dictConfig(LOGGING_CONFIG_STDOUT)
    logging.captureWarnings(
        True
    )  # captures warnings from 3rd party packages (e.g., sklearn)
    if descriptor is None:
        name = f"{repo_acronym} {module_name}"
    else:
        name = f"{repo_acronym} {module_name} {descriptor}"
    name = name.upper()
    logger = logging.getLogger(name)
    logger.debug("Logging is configured.")
    return logger
    """

    Args:
        name (str): Name of logger. Pass __name__ to link logger to module.

    Returns:

    """
