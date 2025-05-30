import statistics
import logging
from logging.handlers import TimedRotatingFileHandler

def is_valid_numeric_value(value, min_val=1, max_val=9000):
    """Check if the value is a digit and within a reasonable range."""
    if not value.isdigit():
        return False
    val_int = int(value)
    return min_val <= val_int <= max_val

def is_monotonic_increase(value, history):
        """Check if the current value is strictly greater than the last value in the history."""
        if not value.isdigit():
            return False
        val_int = int(value)
        return len(history) == 0 or val_int > history[-1]

def is_outlier(value, history, threshold=0.3):
    """Detect if a value is a significant outlier based on recent median."""
    if len(history) < 3:
        return False
    median = statistics.median(history)
    deviation = abs(int(value) - median) / median
    return deviation > threshold

def setup_logger():
    """Set up the logger with console and file handlers."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotation: daily, backup 7 days
    file_handler = TimedRotatingFileHandler("teleinfo.log", when="midnight", interval=1, backupCount=7, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
