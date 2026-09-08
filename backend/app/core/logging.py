import logging
import sys


def setup_logging() -> None:
    """Configure structured global logging for the application."""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Adjust verbosity for specific third-party loggers if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Global application logger instance
logger = logging.getLogger("notes_app")