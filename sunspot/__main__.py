#!/usr/bin/env python3
# -*- coding: utf8 -*-

import signal
import sys
import traceback

from utils.logger import crate_log_file, get_logger
from utils.settings import ApplicationSettings

from sunspot import Sunspot

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = ""
"""Copyrighted"""

__credits__ = []
"""Credits"""

__license__ = ""
"""License
@see """

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = ["Orlin Dimitrov", "Martin Maslyankov", "Nikola Atanasov"]
"""Name of the maintainer."""

__email__ = ""
"""E-mail of the author."""

__class_name__ = ""
"""Class name."""

#endregion

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
    settings.load()

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
    sunspot = Sunspot()

    # Init
    sunspot.init()

    # Update
    while not __TIME_TO_STOP:
        sunspot.update()

    # Shutdown
    sunspot.shutdown()

    __LOGGER.info("Application stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        __LOGGER.error(traceback.format_exc())
        sys.exit(0)
