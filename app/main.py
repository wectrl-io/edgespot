#!/usr/bin/env python3
# -*- coding: utf8 -*-

import signal
import sys

from utils.logger import crate_log_file, get_logger
from utils.settings import ApplicationSettings

from sunspot import Sunspot

__LOGGER = None
"""Logger
"""

__TIME_TO_STOP = False
"""Stop flag.
"""

def interrupt_handler(signum, frame):
    """Interrupt handler."""

    global __TIME_TO_STOP, __LOGGER

    if signum == 2:
        __LOGGER.warning("Stopped by interrupt.")

    elif signum == 15:
        __LOGGER.warning("Stopped by termination.")

    else:
        __LOGGER.warning("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    # Raise the termination flag.
    __TIME_TO_STOP = True

def main():
    """Main function.
    """

    global __TIME_TO_STOP, __LOGGER

    # Add signal handler.
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # Get settings.
    settings = ApplicationSettings.get_instance()

    # Read settings content.
    settings.read()

    # Create log.
    crate_log_file()
    __LOGGER = get_logger(__name__)

    # Wait for settings.
    if not settings.exists:
        settings.create_default()
        __LOGGER.warning(f"Creating default application settings file.\
            Please edit before next start. ({settings.path})")
        sys.exit(0)

    __LOGGER.info("Starting the application.")

    # The mantra ...Ohmmm

    # Create
    worker = Sunspot()

    # Init
    worker.init()

    # Update
    while not __TIME_TO_STOP:
        worker.update()

    # Shutdown
    worker.shutdown()

    __LOGGER.info("Application stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        __LOGGER.error(exception)
