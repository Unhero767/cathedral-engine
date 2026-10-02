# cathedral_engine/app/logging/config.py

import logging
import sys


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("ash_archive.ledger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
