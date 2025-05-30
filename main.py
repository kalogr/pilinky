import logging
from reader import TeleinfoReader
from utils import setup_logger

if __name__ == "__main__":
    setup_logger()
    logging.info("Starting teleinfo frame reading...")
    reader = TeleinfoReader()
    reader.run()
